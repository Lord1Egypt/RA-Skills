## Description: <br>
Summarize YouTube videos into structured Markdown with youtube2md, including chaptered notes, timestamp links, and key takeaways. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunghyo](https://clawhub.ai/user/sunghyo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and other external users use this skill to convert one or more YouTube URLs into structured study notes, transcript-based summaries, timestamped chapters, key takeaways, or machine-readable JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the pinned youtube2md npm package and its dependencies, which creates an installation-time supply-chain trust boundary. <br>
Mitigation: Install the pinned package only after reviewing or approving the package and dependencies; use a vetted internal mirror or vendored package in stricter environments. <br>
Risk: When OPENAI_API_KEY is set, full summarization mode may send transcript content or related video content to OpenAI APIs. <br>
Mitigation: Leave OPENAI_API_KEY unset for sensitive videos and use extract-only mode with local summarization from prepared transcript text. <br>
Risk: Generated transcript, summary, or JSON files may remain on disk after use. <br>
Mitigation: Write outputs only to approved locations and remove generated files when retention is not intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunghyo/youtube-summary) <br>
- [Output format](references/output-format.md) <br>
- [Security and installation considerations](references/security.md) <br>
- [Summarization behavior](references/summarization-behavior.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, transcript text, optional JSON status, and shell commands for running youtube2md.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Full mode can produce Markdown through youtube2md when OPENAI_API_KEY is set; extract mode produces transcript JSON and prepared text for local summarization.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
