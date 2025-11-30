import pandas as pd
import gzip
import io

# 1. Define the correct OpenCelliD headers
headers = [
    "radio", "mcc", "mnc", "lac", "cid", "psc",
    "lon", "lat", "range", "samples", "changeable",
    "created", "updated", "averageSignal"
]

# 2. Load the raw data
# (Assuming the file is '334.csv.gz/334.csv' based on your upload)
input_file = '334.csv.gz/334.csv'

try:
    # Try reading as a standard CSV first
    df = pd.read_csv(input_file, names=headers, header=None)
except:
    # If that fails, it might be a GZIP file
    with gzip.open(input_file, 'rt') as f:
        df = pd.read_csv(f, names=headers, header=None)

# 3. Create a 'Carrier' column for your charts
# Mapping MNC codes to Carrier Names for Mexico (MCC 334)
def get_carrier(mnc):
    if mnc in [20, 2]: return 'Telcel'
    if mnc in [30, 3]: return 'Movistar'
    if mnc in [50, 90, 10, 40, 1, 80, 70]: return 'AT&T'
    if mnc == 140: return 'Altán Redes'
    return 'Other'

df['Carrier'] = df['mnc'].apply(get_carrier)

# 4. Save the fixed file for Kepler.gl (This is the one you drag into the map)
df.to_csv('mexico_towers_for_kepler.csv', index=False)
print("File 1 Created: mexico_towers_for_kepler.csv (Use this for your 3D Map)")

# --- Generate Data for Supporting Visualizations ---

# 5. Data for Donut Chart (Technology Breakdown)
tech_counts = df['radio'].value_counts().reset_index()
tech_counts.columns = ['Technology', 'Count']
tech_counts.to_csv('viz_tech_breakdown.csv', index=False)
print("File 2 Created: viz_tech_breakdown.csv (Use for Donut Chart)")

# 6. Data for Treemap (Carrier Market Share)
carrier_counts = df['Carrier'].value_counts().reset_index()
carrier_counts.columns = ['Carrier', 'Total_Towers']
carrier_counts.to_csv('viz_carrier_share.csv', index=False)
print("File 3 Created: viz_carrier_share.csv (Use for Treemap)")

# 7. Data for Stacked Bar (Tech Mix by Carrier)
# Group by Carrier AND Technology
tech_mix = df.groupby(['Carrier', 'radio']).size().unstack(fill_value=0)
tech_mix.to_csv('viz_tech_mix.csv')
print("File 4 Created: viz_tech_mix.csv (Use for Stacked Bar Chart)")