# Medical Reports Simplification Dataset

3,801 clinical reports across 39 specialties, packaged for training language
models to rewrite dense medical documentation in patient-friendly language.

**Live page:** https://YOUR-USERNAME.github.io/REPO-NAME/

## Repository layout

```
index.html                 Project web page (served by GitHub Pages)
scripts/
  profile_dataset.py       Summary statistics
  dedupe_and_split.py      Deduplicate and create train/val/test JSONL
  load_example.py          Load the JSONL with Hugging Face datasets
data/                      Put the dataset files here
requirements.txt
```

## Dataset files

| File | Description |
|---|---|
| `Medical_Reports_Simplification_Dataset.csv` | 9 columns: report text, extracted findings, keywords, prompt, summary seed |
| `medical_reports_simplification.jsonl` | `instruction` / `input` / `output` / `metadata` for TRL, SFTTrainer, Unsloth, Axolotl |

## Usage

```bash
pip install -r requirements.txt
python scripts/profile_dataset.py
python scripts/dedupe_and_split.py     # writes data/processed/{train,val,test}.jsonl
```

## Known issues

- The `output` field is a baseline **summary seed**, not a finished plain-language rewrite. Review or rewrite before treating it as ground truth.
- 1,984 rows repeat another row's report text (1,817 unique reports). Use `dedupe_and_split.py` to avoid train/test leakage.
- The original README states 3,813 CSV records; the files contain 3,801.
- 1,148 rows have no extracted findings.
- Not for clinical use. Have a qualified professional review any model output before it reaches patients.

## License

Add a license here after confirming you may redistribute the data.
