## Description: <br>
Exports WeChat public account articles from wewe-rss or JSON Feed sources into cleaned DOCX documents, with optional date-prefixed filenames and ZIP packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n1neman](https://clawhub.ai/user/n1neman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to export wewe-rss style WeChat public account feeds into cleaned Word document bundles for review, delivery, or archiving. It supports small validation exports and larger batches with optional retained HTML/Markdown artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches a user-provided feed URL and downloads embedded article images. <br>
Mitigation: Use trusted feed URLs, run exports in a dedicated workspace, and review the generated files before reuse or sharing. <br>
Risk: The exporter writes local DOCX outputs and may replace an existing ZIP at the selected output path. <br>
Mitigation: Choose a dedicated output directory and confirm the target ZIP path before using the ZIP option. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/n1neman/wewe-rss-wechat-export) <br>
- [README.md](artifact/README.md) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands that produce DOCX files, index.txt summaries, optional ZIP archives, and optional HTML/Markdown validation artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, pandoc, curl, and python3; fetches a user-provided HTTP(S) feed URL and writes outputs to a local export directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, manifest.yaml, _meta.json, and changelog released 2026-03-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
