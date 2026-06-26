# ADMET-AI Example

Use this example when the user wants ADMET endpoint prediction for one or more small molecules from a SMILES table.

## Why This Example Matters

This is a representative small-molecule batch workflow:
- input is a CSV file, not FASTA or plain text
- the required file column name must match the payload field configuration
- the module returns a wide prediction table through `job download`
- `stderr.txt` may contain model-loading warnings even when the job finishes successfully

## Verified Module Pattern

`module get <module_id> --params-json` for `ADMET-AI` reports one method:
- method: `ADMET-AI`
- required file field: `Small Molecule File`
- optional text field: `Smiles Column Name`
- optional text field: `Predicted Results`

## Example Input CSV

```csv
smiles,name
CCO,ethanol
CC(=O)OC1=CC=CC=C1C(=O)O,aspirin
```

## Verified Submit Pattern

```bash
wemol-cli job submit \
  --module-id <module_id> \
  --method "ADMET-AI" \
  --params '{"Small Molecule File":"/path/to/input.csv","Smiles Column Name":"smiles","Predicted Results":"predicted_results.csv"}'
```

## Verified Result Pattern

The job completed with `Status: Done`, but `job output` using the default `output` name did not return structured values:

```bash
wemol-cli job output <job_id> --task-id <task_id> --name output
```

Observed behavior:

```text
Output 'output' was not found for task <task_id> in job <job_id>. This module may publish result files instead. Try 'wemol-cli job download <job_id>'.
```

Use downloads instead:

```bash
wemol-cli job download <job_id> --output /path/to/result_dir
wemol-cli job download <job_id> --output /path/to/result_dir --retry 3 --concurrency 6
wemol-cli job download <job_id> --output /path/to/result_dir --no-resume
```

Observed files:
- `predicted_results.csv`
- `stdout.txt`
- `stderr.txt`

Representative `predicted_results.csv` columns included:
- `molecular_weight`
- `logP`
- `QED`
- `Lipinski`
- `AMES`
- `DILI`
- `hERG`
- `Solubility_AqSolDB`

## Agent Rules From This Example

- Treat this module as a CSV-in, CSV-out workflow.
- Ensure the `Smiles Column Name` matches the actual CSV header exactly.
- Keep `Predicted Results` explicit in the payload to control output naming.
- Download files even if `job status` already says `Done`; the useful payload is in the artifact CSV.
- Prefer `--retry` and `--concurrency` for larger CSV batches or unstable networks.

## Important Warning Pattern

In a verified run, `stderr.txt` included `chemprop` and `torch.load` future warnings plus progress-bar output, while the prediction CSV was still generated successfully.

Interpretation:
- backend library warnings in `stderr.txt` do not necessarily indicate a failed ADMET prediction
- prioritize the presence and readability of `predicted_results.csv`
