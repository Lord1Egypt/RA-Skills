## Description: <br>
Fetch, transcribe, summarize, and filter YouTube channels or individual videos for analysis and reusable structured outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ulyanas](https://clawhub.ai/user/ulyanas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers and researchers use this skill to analyze YouTube channels or individual videos, collect transcripts, filter videos by metadata or content, and produce summaries, notes, reports, and reusable datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports weakened HTTPS checks. <br>
Mitigation: Prefer fixing certificate or proxy configuration; use certificate-check bypasses only in trusted environments after explicit user acceptance. <br>
Risk: The security evidence reports optional browser or session cookie use for YouTube access. <br>
Mitigation: Avoid cookies and browser-derived credentials unless the user intentionally wants account-linked YouTube access for the task. <br>
Risk: The skill downloads YouTube content, writes multiple local output files, and installs Python packages at runtime. <br>
Mitigation: Run it only in an environment where those downloads, file writes, and runtime package installs are acceptable. <br>


## Reference(s): <br>
- [Dependencies](references/dependencies.md) <br>
- [Filtering](references/filtering.md) <br>
- [Outputs](references/outputs.md) <br>
- [ClawHub release page](https://clawhub.ai/ulyanas/youtube-channel-parse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, plain-text transcripts, JSON datasets, CSV datasets, and command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local inventory, filtered dataset, transcript, and report files under an output directory named from the requested prefix.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
