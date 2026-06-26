# Protein Physico-chemical Properties Example

Use this example when the user wants bulk sequence-level descriptors from a FASTA input, such as molecular weight, isoelectric point, aromaticity, GRAVY, net charge, or secondary-structure fractions.

## Why This Example Matters

This is a representative sequence-analysis workflow:
- input is a FASTA file
- job submission uses a file field plus several scalar fields
- the module publishes CSV artifacts through `job download`
- `stdout.txt` may contain warnings even when the job status is `Done`

## Verified Module Pattern

`module get <module_id> --params-json` for `Protein Physico-chemical Properties` reports one method:
- method: `Fasta File`
- required file field: `Protein Sequence File`
- required text field: `Output File`
- optional fields include `Merge Chain`, `Merge Output File`, `Job Number`, `pH Value`, `DeepSP Output`

## Example Input FASTA

```fasta
>demo_protein
MKWVTFISLLFLFSSAYSRGVFRRDTHKSEIAHRFKDLGE
```

## Verified Submit Pattern

```bash
wemol-cli job submit \
  --module-id <module_id> \
  --method "Fasta File" \
  --params '{"Protein Sequence File":"/path/to/input.fasta","Output File":"result.csv","Merge Chain":"True","Merge Output File":"merged.csv","Job Number":1,"pH Value":7,"DeepSP Output":"deepsp_descriptors.csv"}'
```

## Verified Result Pattern

The job completed with `Status: Done`, but the default structured output path still failed:

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
- `result.csv`
- `merged.csv`
- `stdout.txt`

Representative `result.csv` columns included:
- `Molecular Weight`
- `Isoelectric Point`
- `Instability Index`
- `Aromaticity`
- `Grand average of hydropathicity (GRAVY)`
- `Net Charge`

## Agent Rules From This Example

- Treat this module as a file-download result producer, not a structured `job output` producer.
- Keep output file names explicit in the payload so the downloaded artifact names are predictable.
- `Merge Chain` is a `SingleChoice` field with string values like `"True"` and `"False"`, not a JSON boolean.
- A `Done` job can still include non-fatal warnings in `stdout.txt`.
- Prefer `--retry` and `--concurrency` when downloading larger artifact sets.

## Important Warning Pattern

In a verified run, `stdout.txt` contained a DeepSP warning because the demo sequence was not recognized as an antibody variable chain, but the main physicochemical CSV outputs were still produced successfully.

Interpretation:
- warnings inside downloaded logs do not automatically mean the whole job failed
- inspect the actual result files before declaring failure
