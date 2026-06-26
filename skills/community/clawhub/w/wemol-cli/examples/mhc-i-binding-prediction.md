# MHC-I Binding Prediction Example

Use this example when the user wants a simple peptide-to-MHC screening job from a FASTA input and the module exposes a minimal payload with only one required file field.

## Why This Example Matters

This is a representative minimal FASTA workflow:
- the payload has only one required field
- the job reaches `Done` quickly
- `job output` may return empty-data errors instead of a missing-output-key message
- `job download` may still contain the only meaningful artifact

## Verified Module Pattern

`module get <module_id> --params-json --method "Prediction"` for `MHC-I Binding Prediction` reports one method:
- method: `Prediction`
- required file field: `Protein Sequence File`

## Example Input FASTA

```fasta
>mhc_demo
SIINFEKL
```

## Verified Submit Pattern

```bash
wemol-cli job submit \
  --module-id <module_id> \
  --method "Prediction" \
  --params '{"Protein Sequence File":"/path/to/input.fasta"}'
```

## Verified Result Pattern

After the job reaches `Status: Done`, inspect tasks first:

```bash
wemol-cli job tasks <job_id>
```

Trying structured output may fail with an empty-data error:

```bash
wemol-cli job output <job_id> --task-id <task_id> --name output
```

Observed behavior:

```text
DBDataNull: 数据为空!
Error meta: "ResultInfo.MapOutFile"
```

Even in that case, downloads may still exist:

```bash
wemol-cli job download <job_id> --output /path/to/result_dir
wemol-cli job download <job_id> --output /path/to/result_dir --retry 3 --concurrency 4
wemol-cli job download <job_id> --output /path/to/result_dir --no-resume
```

In a verified run, the only downloaded file was:
- `stdout.txt`

Observed content:

```text
[LOG] No TCE Found!
```

## Agent Rules From This Example

- A successful job may still have no structured output and no rich result file set.
- Treat `DBDataNull` from `job output` as a cue to try `job download`, not as immediate proof that the entire job failed.
- Inspect downloaded logs even when the artifact set is minimal.
- For minimal-payload modules, the main value may be a concise textual conclusion rather than a CSV or JSON table.
- Keep retry-enabled download commands available because these jobs may rely on log artifacts only.
