## Description:

Local analytical data tool powered by DuckDB. Supports importing and querying CSV, TSV, JSON, Parquet, Excel and direct Hugging Face datasets via hf:// protocol with token support. Includes CLI, Node helper, preview server, and Rust backend for Tauri/Electron/Qt apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoqianran](https://clawhub.ai/user/xiaoqianran)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to import local or Hugging Face-hosted datasets into DuckDB, run analytical SQL, export results, and prototype desktop data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The preview server and helper can run powerful SQL over local or Hugging Face-backed data.

Mitigation: Run the preview server only on loopback, do not expose it to a network, and do not submit untrusted SQL or table names.

Risk: The tool can access local files, write DuckDB databases and exports, and use network-backed Hugging Face datasets.

Mitigation: Use a non-sensitive working directory and database for evaluation, and review file paths and dataset sources before import or export.

Risk: Hugging Face tokens may be loaded from environment variables or a local .env file.

Mitigation: Keep tokens out of committed files, prefer controlled environment variables or secure local storage, and rotate any token that may have been exposed.

Risk: Native DuckDB dependencies and lockfiles are part of the runtime surface.

Mitigation: Regenerate lockfiles from a trusted registry and review dependency provenance before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoqianran/skills/xiaoqianran-duck)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SQL examples, local file paths, DuckDB database paths, export formats, and Hugging Face token setup guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
