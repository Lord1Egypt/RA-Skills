## Description:

Downloads local A-share historical market data through a configured QMT trading terminal, with Chinese natural-language commands, CLI parameters, CSV output, and an optional localhost monitoring dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diudiuhuang](https://clawhub.ai/user/diudiuhuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who operate QMT use this skill to download A-share stock and index K-line history into local CSV files for later analysis or trading-data workflows. It is intended for environments where QMT is already installed, configured, logged in, and allowed to fetch market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web dashboard can start, stop, and reconfigure data downloads.

Mitigation: Keep the dashboard bound to localhost and do not expose the Flask/Socket.IO service on a network.

Risk: The release depends on QMT, xtquant, Python packages, and bundled or fallback frontend assets.

Mitigation: Verify the QMT installation, xtquant source, external resource files, and dependency versions before production use.

Risk: Downloads write market data to configured local paths and may overwrite or merge CSV files.

Mitigation: Review config.json paths and keep backups or a test output directory before running large download jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diudiuhuang/skills/stock-qdata)
- [ClawHub publisher profile](https://clawhub.ai/user/diudiuhuang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Console text, local CSV files, JSON API responses, and a localhost web dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local QMT/xtquant access, configured output paths, stock and index list CSV files, and optional web controls for starting, pausing, resuming, and stopping downloads.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
