
import pandas as pd
from pathlib import Path

# Load original NASA dataset
file_path = Path("nasa_research/OSD575_CMP.csv")
df = pd.read_csv(file_path)

# Extract participant and mission timepoint

df["Participant"] = df["Sample Name"].str.extract(r"^(C\d+)")

df["Timepoint"] = df["Sample Name"].str.extract(
    r"(L-\d+|R\+\d+)$"
)

# Four parameters selected for dashboard analysis
parameters = {
    "Glucose": {
        "value": "glucose_value_milligram_per_deciliter",
        "min": "glucose_range_min_milligram_per_deciliter",
        "max": "glucose_range_max_milligram_per_deciliter",
        "unit": "mg/dL"
    },
    "Albumin": {
        "value": "albumin_value_gram_per_deciliter",
        "min": "albumin_range_min_gram_per_deciliter",
        "max": "albumin_range_max_gram_per_deciliter",
        "unit": "g/dL"
    },
    "Creatinine": {
        "value": "creatinine_value_milligram_per_deciliter",
        "min": "creatinine_range_min_milligram_per_deciliter",
        "max": "creatinine_range_max_milligram_per_deciliter",
        "unit": "mg/dL"
    },
    "Sodium": {
        "value": "sodium_value_millimol_per_liter",
        "min": "sodium_range_min_millimol_per_liter",
        "max": "sodium_range_max_millimol_per_liter",
        "unit": "mmol/L"
    }
}

print("=" * 65)
print("ASTRA VITALIS | NASA OSD-575 DATA VALIDATION")
print("=" * 65)

print("\nDATASET OVERVIEW")
print("-" * 65)
print("Total records:", len(df))
print("Total columns:", len(df.columns))
print("Participants:", df["Participant"].nunique())
print("Timepoints:", df["Timepoint"].nunique())

audit_records = []

for name, columns in parameters.items():

    value_col = columns["value"]
    min_col = columns["min"]
    max_col = columns["max"]

    # Convert values to numeric safely
    values = pd.to_numeric(df[value_col], errors="coerce")
    lower = pd.to_numeric(df[min_col], errors="coerce")
    upper = pd.to_numeric(df[max_col], errors="coerce")

    valid = values.notna() & lower.notna() & upper.notna()

    below = valid & (values < lower)
    above = valid & (values > upper)
    within = valid & (values >= lower) & (values <= upper)

    print(f"\n{name.upper()} ({columns['unit']})")
    print("-" * 65)
    print("Available measurements:", values.notna().sum())
    print("Missing measurements:", values.isna().sum())
    print("Valid reference comparisons:", valid.sum())
    print("Below reference range:", below.sum())
    print("Above reference range:", above.sum())
    print("Within reference range:", within.sum())
    print("Missing reference comparisons:", (~valid).sum())

    # Record individual comparisons
    for index in df.index:
        if pd.isna(values.loc[index]):
            status = "Missing measurement"
        elif pd.isna(lower.loc[index]) or pd.isna(upper.loc[index]):
            status = "Reference range unavailable"
        elif values.loc[index] < lower.loc[index]:
            status = "Below reference range"
        elif values.loc[index] > upper.loc[index]:
            status = "Above reference range"
        else:
            status = "Within reference range"

        audit_records.append({
            "Sample": df.loc[index, "Sample Name"],
            "Participant": df.loc[index, "Participant"],
            "Timepoint": df.loc[index, "Timepoint"],
            "Parameter": name,
            "Value": values.loc[index],
            "Reference Min": lower.loc[index],
            "Reference Max": upper.loc[index],
            "Unit": columns["unit"],
            "Status": status
        })

# Create detailed audit report
audit_df = pd.DataFrame(audit_records)

print("\n\nINDIVIDUAL RECORDS OUTSIDE REFERENCE RANGES")
print("=" * 65)

flagged = audit_df[
    audit_df["Status"].isin([
        "Below reference range",
        "Above reference range"
    ])
]

if flagged.empty:
    print("No records outside reference ranges.")
else:
    print(flagged.to_string(index=False))

# Missing data overview
print("\n\nMISSING DATA CHECK")
print("=" * 65)

missing_columns = df.isna().sum()
missing_columns = missing_columns[missing_columns > 0]

if missing_columns.empty:
    print("No missing values.")
else:
    print(missing_columns.to_string())

# Save detailed report
output_path = Path("nasa_research/OSD575_validation_report.csv")
audit_df.to_csv(output_path, index=False)

print("\n" + "=" * 65)
print("VALIDATION COMPLETE")
print("Report saved to:", output_path)
print("=" * 65)
