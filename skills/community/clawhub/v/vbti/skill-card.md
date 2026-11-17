## Description:

VBTI scans local Claude Code transcript history, classifies the user as one of 16 vibe-coder types, and generates a diagnostic-style HTML card on the Desktop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and coding-agent users use this novelty diagnostic skill to summarize local vibe-coding habits from Claude transcript history and produce a shareable HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans all local Claude project transcripts, which may contain private prompts, command output, file paths, code, secrets, or work information.

Mitigation: Run it only on accounts and machines where scanning local transcript history is acceptable; review transcript sensitivity before execution.

Risk: The generated Desktop HTML card is easy to share and may expose derived behavioral information from private coding history.

Mitigation: Inspect the generated card before sharing it and delete the file when it is no longer needed.

Risk: The HTML template imports Google Fonts even though the artifact claims it does not use the network.

Mitigation: Remove the external font import or run in an offline or sandboxed environment before relying on the no-network claim.

Risk: The script auto-opens the generated report in a browser.

Mitigation: Disable auto-open before running if browser launch or visible local output is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinadu-ai/skills/vbti)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Text guidance with inline shell commands; the runtime script writes a local HTML file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a Desktop HTML report and may auto-open it in the browser.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
