# Antibody Variable Region Numbering Example

Use this example when a user wants antibody variable-region numbering and the agent needs a verified `job submit` payload for `Antibody Numbering v2`.

## Why This Example Matters

The tricky field is `Numbering Scheme`.

`module get <module_id> --params-json --method "Variable Region (Fv)"` reports:
- `field`: `Numbering Scheme`
- `format`: `MultipleChoice`
- `options`: `kabat`, `chothia`, `imgt`, `martin`

The backend requires this field to be sent as an array, even when selecting only one scheme.

This means:

```json
{"Numbering Scheme":"imgt"}
```

fails with:

```text
DBDataInvalid: 数组 Numbering Scheme 值无效: imgt
```

but:

```json
{"Numbering Scheme":["imgt"]}
```

works.

## Verified Input FASTA

Use this FASTA content as the reproducible input for the example:

```fasta
>demo_heavy_chain
QVQLVQSGAEVKKPGASVKVSCKASGYTFTNYGMNWVRQAPGQGLEWMGWINTYTGEPTYAADFKRRFTFSLDTSKSTAYLQMNSLRAEDTAVYYCAR
>demo_light_chain
DIQMTQSPSSLSASVGDRVTITCRASQDISNYLAWYQQKPGKAPKLLIYAASNLESGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQYNSYPYTFGQGTKVEIK
```

## Verified Command Sequence

Inspect the method schema first:

```bash
wemol-cli module get <module_id> --params-json --method "Variable Region (Fv)"
```

Submit a job with a single numbering scheme:

```bash
wemol-cli job submit \
  --module-id <module_id> \
  --method "Variable Region (Fv)" \
  --params '{"Fasta File":"/path/to/input.fasta","Numbering Scheme":["imgt"]}'
```

Check status:

```bash
wemol-cli job status <job_id>
```

Get task IDs:

```bash
wemol-cli job tasks <job_id>
```

Trying structured output fails:

```bash
wemol-cli job output <job_id> --task-id <task_id> --name output
```

Observed result:

```text
Output 'output' was not found for task <task_id> in job <job_id>. This module may publish result files instead. Try 'wemol-cli job download <job_id>'.
```

Download the actual result files:

```bash
wemol-cli job download <job_id> \
  --output /path/to/numbering_result
wemol-cli job download <job_id> \
  --output /path/to/numbering_result \
  --retry 3 \
  --concurrency 6
wemol-cli job download <job_id> \
  --output /path/to/numbering_result \
  --no-resume
```

Observed downloaded files:
- `output_imgt.csv`
- `output_imgt.json`
- `output_nonfv.fasta`
- `stdout.txt`

## Agent Rules From This Example

- For `Variable Region (Fv)`, treat `Numbering Scheme` as an array-valued field because the format is `MultipleChoice`.
- Do not send `IMGT` or `imgt` as a bare string.
- Accepted values are lowercase option values from `--params-json`: `kabat`, `chothia`, `imgt`, `martin`.
- Do not assume `job output` will expose a named `output` key for this module.
- Use `job tasks` before `job output`.
- If `job output` says the output is missing, switch to `job download`.
- Prefer `--retry` and `--concurrency` when result artifacts are large or network is unstable.

## Extra Caution

When retrying the same submission, avoid firing multiple identical uploads in parallel. In a verified run, concurrent retries against the same FASTA file triggered a backend blob deduplication error:

```text
pq: duplicate key value violates unique constraint "blob_size_sha256_key"
```

Prefer serial retries for file-upload jobs.
