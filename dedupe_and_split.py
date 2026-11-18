"""Deduplicate by report text and make leakage-free train/val/test JSONL files.

Rows sharing identical report text always land in the same split.
"""
import argparse, json, os, random
import pandas as pd

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="data/Medical_Reports_Simplification_Dataset.csv")
    p.add_argument("--out", default="data/processed")
    p.add_argument("--val", type=float, default=0.1)
    p.add_argument("--test", type=float, default=0.1)
    p.add_argument("--seed", type=int, default=42)
    a = p.parse_args()

    df = pd.read_csv(a.csv)
    before = len(df)
    df = df.drop_duplicates(subset="complex_medical_report").reset_index(drop=True)
    print(f"Dropped {before - len(df)} duplicate rows; {len(df)} unique reports remain.")

    idx = list(range(len(df)))
    random.Random(a.seed).shuffle(idx)
    n_test, n_val = int(len(idx) * a.test), int(len(idx) * a.val)
    splits = {
        "test": idx[:n_test],
        "val": idx[n_test:n_test + n_val],
        "train": idx[n_test + n_val:],
    }

    os.makedirs(a.out, exist_ok=True)
    for name, ids in splits.items():
        path = os.path.join(a.out, f"{name}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for i in ids:
                r = df.iloc[i]
                rec = {
                    "instruction": r["instruction_prompt"],
                    "input": r["complex_medical_report"],
                    "output": r["plain_language_summary_seed"],
                    "metadata": {
                        "specialty": str(r["medical_specialty"]).strip(),
                        "sample_name": r["sample_name"],
                    },
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"{name}: {len(ids)} -> {path}")

if __name__ == "__main__":
    main()
