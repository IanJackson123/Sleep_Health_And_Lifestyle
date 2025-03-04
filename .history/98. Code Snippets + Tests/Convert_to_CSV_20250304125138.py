# Convert Excel File as it was used in Tableau to a CSV file

import pandas as pd

# Load the Excel file
df = pd.read_excel("your_file.xlsx")  # Replace with your file name

# Save as CSV
df.to_csv("your_file.csv", index=False) 