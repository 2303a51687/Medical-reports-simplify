"""Profile the CSV and print a summary; optionally write it as JSON."""
import argparse, json
import pandas as pd

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="data/Medical_Reports_Simplification_Dataset.csv")
    p.add_argument("--out", default=None, help="optional path for stats JSON")
    a = p.parse_args()

    df = pd.read_csv(a.csv)
    spec = df["medical_specialty"].str.strip()
    words = df["complex_medical_report"].fillna("").str.split().str.len()
    stats = {
        "records": int(len(df)),
        "specialties": int(spec.nunique()),
        "unique_reports": int(df["complex_medical_report"].nunique()),
        "duplicate_rows": int(df["complex_medical_report"].duplicated().sum()),
        "missing_findings": int(df["extracted_clinical_findings"].isna().sum()),
        "avg_words": round(float(words.mean()), 1),
        "median_words": float(words.median()),
        "top_specialties": spec.value_counts().head(12).to_dict(),
    }
    print(json.dumps(stats, indent=2))
    if a.out:
        with open(a.out, "w") as f:
            json.dump(stats, f, indent=2)

if __name__ == "__main__":
    main()
