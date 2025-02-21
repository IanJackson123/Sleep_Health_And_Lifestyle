import numpy as np
import pandas as pd

# Set seed for reproducibility
np.random.seed(42)

# Load the existing dataset
df_orig = pd.read_csv("/mnt/data/Sleep_health_and_lifestyle_dataset.csv")

# Define target size and outlier count
target_size = 2000
outlier_count = 100
normal_count = target_size - outlier_count

# Get unique categories from the original data
# For Gender, if only one category exists, we may add another for variety.
genders = df_orig["Gender"].unique()
if len(genders) == 1:
    genders = np.array(["Male", "Female"])
occupations = df_orig["Occupation"].unique()
bmi_categories = df_orig["BMI Category"].unique()  # e.g., "Normal", "Overweight", "Obese"

# Estimate basic statistics from the original data for normal synthesis
sleep_duration_mean = df_orig["Sleep Duration"].mean()
sleep_duration_std = df_orig["Sleep Duration"].std()

physical_activity_mean = df_orig["Physical Activity Level"].mean()
physical_activity_std = df_orig["Physical Activity Level"].std()

stress_mean = df_orig["Stress Level"].mean()
stress_std = df_orig["Stress Level"].std()

heart_rate_mean = df_orig["Heart Rate"].mean()
heart_rate_std = df_orig["Heart Rate"].std()

# Function to simulate blood pressure based on BMI category
def generate_bp(bmi):
    if bmi == "Normal":
        systolic = np.random.randint(115, 126)
        diastolic = np.random.randint(75, 86)
    elif bmi == "Overweight":
        systolic = np.random.randint(120, 131)
        diastolic = np.random.randint(80, 91)
    elif bmi == "Obese":
        systolic = np.random.randint(135, 146)
        diastolic = np.random.randint(85, 96)
    else:
        systolic = np.random.randint(115, 146)
        diastolic = np.random.randint(75, 96)
    return f"{systolic}/{diastolic}"

# Function to simulate heart rate based on BMI category
def generate_hr(bmi):
    if bmi == "Normal":
        return np.random.randint(65, 76)
    elif bmi == "Overweight":
        return np.random.randint(70, 81)
    elif bmi == "Obese":
        return np.random.randint(75, 91)
    else:
        return int(np.random.normal(heart_rate_mean, heart_rate_std))

# Function to simulate sleep disorder
def generate_sleep_disorder():
    # 15% chance of having a disorder
    if np.random.rand() < 0.15:
        # Choose a disorder (70% Sleep Apnea, 30% Insomnia)
        return np.random.choice(["Sleep Apnea", "Insomnia"], p=[0.7, 0.3])
    else:
        return np.nan  # Use NaN for no sleep disorder

# Generate normal synthetic rows
normal_rows = []
for _ in range(normal_count):
    row = {}
    # Gender: sample from genders with equal probability
    row["Gender"] = np.random.choice(genders, p=[0.55, 0.45]) if len(genders)==2 else genders[0]
    # Age: Uniformly sample between 18 and 70
    row["Age"] = np.random.randint(18, 71)
    # Occupation: sample from the existing occupations
    row["Occupation"] = np.random.choice(occupations)
    # Sleep Duration: normal distribution around the mean, clipped to a reasonable range
    sd = np.clip(np.random.normal(sleep_duration_mean, sleep_duration_std), 4, 10)
    row["Sleep Duration"] = round(sd, 1)
    # Quality of Sleep: loosely correlated with sleep duration plus noise; clip between 1 and 10
    q_sleep = np.clip(round(sd + np.random.normal(0, 1)), 1, 10)
    row["Quality of Sleep"] = q_sleep
    # Physical Activity Level: normal distribution based on original stats; ensure positive
    pa = np.clip(np.random.normal(physical_activity_mean, physical_activity_std), 10, 120)
    row["Physical Activity Level"] = int(round(pa))
    # Stress Level: can inversely relate to sleep duration (but add randomness), clip between 1 and 10
    stress = np.clip(round(10 - sd + np.random.normal(0, 1)), 1, 10)
    row["Stress Level"] = stress
    # BMI Category: sample from existing categories (using assumed probabilities if needed)
    row["BMI Category"] = np.random.choice(bmi_categories, p=[0.3, 0.35, 0.35]) if len(bmi_categories)==3 else np.random.choice(bmi_categories)
    # Blood Pressure: based on BMI
    row["Blood Pressure"] = generate_bp(row["BMI Category"])
    # Heart Rate: based on BMI
    row["Heart Rate"] = generate_hr(row["BMI Category"])
    # Daily Steps: correlate with physical activity level (multiplier with random factor)
    row["Daily Steps"] = int(round(row["Physical Activity Level"] * np.random.uniform(80, 180)))
    # Sleep Disorder: assign using our function (NaN if none)
    row["Sleep Disorder"] = generate_sleep_disorder()
    
    normal_rows.append(row)

# Generate outlier rows with extreme values
outlier_rows = []
for _ in range(outlier_count):
    row = {}
    # Gender: randomly choose
    row["Gender"] = np.random.choice(genders, p=[0.55, 0.45]) if len(genders)==2 else genders[0]
    # Age: choose either very young or older extremes
    row["Age"] = np.random.choice([np.random.randint(18, 25), np.random.randint(60, 80)])
    # Occupation: random choice
    row["Occupation"] = np.random.choice(occupations)
    # Sleep Duration: pick extreme low (<4) or high (>10)
    row["Sleep Duration"] = round(np.random.choice([np.random.uniform(2, 4), np.random.uniform(10, 12)]), 1)
    # Quality of Sleep: extreme low or high, loosely tied to sleep duration
    row["Quality of Sleep"] = np.random.choice([np.random.randint(1, 3), np.random.randint(9, 11)])
    # Physical Activity Level: extreme low (e.g., sedentary) or high (e.g., overactive)
    row["Physical Activity Level"] = int(np.random.choice([np.random.randint(0, 10), np.random.randint(100, 150)]))
    # Stress Level: extreme values
    row["Stress Level"] = np.random.choice([np.random.randint(9, 11), np.random.randint(1, 3)])
    # BMI Category: still choose from the same categories, but later the vitals will be extreme
    row["BMI Category"] = np.random.choice(bmi_categories, p=[0.3, 0.35, 0.35]) if len(bmi_categories)==3 else np.random.choice(bmi_categories)
    # Blood Pressure: for outliers, set extreme high or low
    if np.random.rand() < 0.5:
        systolic = np.random.randint(150, 180)
        diastolic = np.random.randint(95, 110)
    else:
        systolic = np.random.randint(90, 105)
        diastolic = np.random.randint(60, 70)
    row["Blood Pressure"] = f"{systolic}/{diastolic}"
    # Heart Rate: extreme high or low
    row["Heart Rate"] = np.random.choice([np.random.randint(95, 120), np.random.randint(40, 55)])
    # Daily Steps: extreme values
    row["Daily Steps"] = int(np.random.choice([np.random.randint(0, 1000), np.random.randint(15000, 25000)]))
    # Sleep Disorder: still assign disorder if applicable (with our 15% chance, but can be overridden by outlier nature)
    row["Sleep Disorder"] = generate_sleep_disorder()
    
    outlier_rows.append(row)

# Combine normal and outlier rows into a DataFrame
df_normal = pd.DataFrame(normal_rows)
df_outliers = pd.DataFrame(outlier_rows)
df_combined = pd.concat([df_normal, df_outliers], ignore_index=True)

# Reset Person ID sequentially
df_combined.insert(0, "Person ID", range(1, len(df_combined) + 1))

# Optional: Shuffle the rows to mix outliers with normal data
df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the combined DataFrame to a CSV file
output_path = "/mnt/data/Sleep_health_and_lifestyle_dataset_expanded.csv"
df_combined.to_csv(output_path, index=False)

print(f"Expanded dataset with {len(df_combined)} rows has been saved to '{output_path}'.")
