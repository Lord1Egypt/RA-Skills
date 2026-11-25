# Executable and command reference

Use an existing trusted checkout when available:

```bash
git clone https://github.com/ambitioncn/taskforce-model-foundry.git
cd taskforce-model-foundry
node bin/tmf.mjs --version
node bin/tmf.mjs help
```

All examples below use `tmf`. In a source checkout substitute
`node /absolute/path/to/taskforce-model-foundry/bin/tmf.mjs` for `tmf`.
With an installed npm package use its `node_modules/.bin/tmf` executable.
Before relying on npm installation, check that the desired real version is
publicly available; a staged placeholder is not an operational release.

```bash
npm view taskforce-model-foundry versions --json
# Only after verifying that 0.4.0 is an operational public version:
npm install taskforce-model-foundry@0.4.0
./node_modules/.bin/tmf --version
```

Use an absolute project directory in place of `/path/to/project`, and a stable
job ID in place of `example-job`. `init` creates synthetic data and config and
refuses to overwrite an existing config.

```bash
tmf doctor --json
tmf backends --json
tmf init -C /path/to/project
tmf config validate -C /path/to/project --json
tmf train -C /path/to/project --job example-job --json
tmf status example-job -C /path/to/project --json
tmf evaluate -C /path/to/project --job example-job --json
tmf export -C /path/to/project --job example-job --report /path/to/reviewed-report.json --out /path/to/bundle --json
```

For long local jobs, use the independent background worker and retain its
`requestId` from the JSON response. Do not resubmit a running request:

```bash
tmf train -C /path/to/project --job example-job --background --json
tmf train-status example-job REQUEST_ID -C /path/to/project --json
tmf evaluate -C /path/to/project --job example-job --background --json
tmf evaluate-status example-job REQUEST_ID -C /path/to/project --json
```

For a predeclared campaign, see `docs/campaign.md` in the installed package.
The plan can list candidates or authorize a bounded proposal search. A
`reflective` proposal records failed gate evidence, hypothesis, and the next
permitted configuration; it cannot lower gates or change model/data. Start and
query the standalone worker without relying on an agent harness:

```bash
tmf campaign start --plan /path/to/campaign.json --json
tmf campaign status --plan /path/to/campaign.json --json
tmf campaign cancel --plan /path/to/campaign.json
```

After an intentional cancellation, continue only when authorized with
`tmf campaign start --plan /path/to/campaign.json --resume-cancelled`.

`tmf train-cancel example-job REQUEST_ID` cancels a background train. A failed
or interrupted background request needs explicit `--retry`; use the CLI's
receipt and check durable status before doing so. On Linux, systemd user units
can isolate workers from Gateway restarts; inspect `restartDurable` instead of
assuming the stronger mode. This does not prove survival across host power loss.

Read the evaluation JSON to obtain the real report path; do not guess it.
Export without `--report` performs evaluation again. To verify an exported bundle:

```bash
cd /path/to/bundle
sha256sum -c checksums.txt
```

For foreground cancellation send SIGINT or SIGTERM to the training process.
Inspect status after it exits, then use the exact resume command it prints,
equivalent to:

```bash
tmf train -C /path/to/project --job example-job --resume-cancelled --json
```

Do not use `--no-resume` as routine recovery: it ignores existing job state.
Exit codes: 0 success; 1 failed job/check; 2 usage error; 130 operator cancellation.

For HF/PEFT, `TMF_PYTHON` selects the Python interpreter. Verify imports of
`torch`, `transformers`, `peft`, `datasets`, and `accelerate` in that interpreter.
Consult the installed tutorial for backend/model/resource configuration; changing
backend does not itself install Python packages or provision hardware.
