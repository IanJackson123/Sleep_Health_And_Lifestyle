import pandas as pd

# Load CSV file
csv_file = "Sleep_health_and_lifestyle_dataset.csv"  # Change to your CSV file path
df = pd.read_csv(csv_file)

# Save as Excel file using xlsxwriter
excel_file = "data.xlsx"  # Change to desired Excel file path
df.to_excel(excel_file, index=False, engine='xlsxwriter')

print(f"CSV file '{csv_file}' successfully saved as Excel file '{excel_file}'.")