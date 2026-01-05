import requests
import pandas as pd
import json

# Header to bypass potential blocking by the website
headers = {'User-Agent': 'Our World In Data data fetch/1.0'}

# Direct URL to the CSV file (death rates by overdose types)
csv_url = "https://ourworldindata.org/grapher/drug-overdose-death-rates.csv?v=1&csvType=filtered&useColumnShortNames=true&overlay=download-data"

# Download the CSV file
response = requests.get(csv_url, headers=headers)

# Define file paths as constants
OVERDOSE_FULL_HISTORY_RATES_PATH = "../data/processed/overdose_full_history_rates.json"
DRUG_OVERDOSES_RAW_PATH = "../data/raw/drug_overdoses_raw.csv"

if response.status_code == 200:
    with open(DRUG_OVERDOSES_RAW_PATH, "wb") as f:
        f.write(response.content)
    print("CSV file downloaded successfully: drug_overdoses_raw.csv")
else:
    print(f"Download error: {response.status_code}")
    print(response.text[:500])
    exit()

# Read the CSV file
df = pd.read_csv(DRUG_OVERDOSES_RAW_PATH)

# Print column names (for verification)
print("\nColumns in the data:")
print(df.columns.tolist())

# Columns containing death rates (per 100,000 population)
rate_columns = [
    'Any opioid death rates (CDC WONDER)',
    'Cocaine overdose death rates (CDC WONDER)',
    'Heroin overdose death rates (CDC WONDER)',
    'Synthetic opioids death rates (CDC WONDER)',
    'Prescription Opioids death rates (US CDC WONDER)'
]

# Check if all required columns are present
missing_cols = [col for col in rate_columns if col not in df.columns]
if missing_cols:
    print(f"Missing columns: {missing_cols}")
    exit()

# Sum the rates to get a total overdose death rate estimate
df['Overdose_Death_Rate_Total'] = df[rate_columns].sum(axis=1)

# Rename columns for convenience
df = df.rename(columns={
    'Entity': 'Country',
    'Year': 'Year'
})

# Filter to keep only individual countries (remove World and other aggregates; data is mostly for USA)
countries = df[~df['Country'].str.contains('World|Income|Europe|Africa|Asia|Americas|Oceania|OECD|WHO', na=False, case=False)]

# Full historical dataset
full_data = countries[['Country', 'Year', 'Overdose_Death_Rate_Total'] + rate_columns].round(2)

# Convert to list of dictionaries and save as JSON
full_json = full_data.to_dict(orient='records')
with open(OVERDOSE_FULL_HISTORY_RATES_PATH, "w", encoding='utf-8') as f:
    json.dump(full_json, f, indent=4, ensure_ascii=False)

print("Full historical data saved to overdose_full_history_rates.json")
print("Done! The code now works with your columns and sums the rates.")