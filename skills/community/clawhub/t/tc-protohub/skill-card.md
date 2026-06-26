## Description: <br>
Manages ProtoHub prototypes by helping an agent package directories or ZIP files, publish or update prototypes, list existing prototypes, and retrieve preview links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airclear](https://clawhub.ai/user/airclear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prototype builders use this skill when they want an agent to publish, update, discover, or retrieve links for ProtoHub prototypes from local folders or ZIP archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing or updating the wrong prototype could overwrite a live ProtoHub entry. <br>
Mitigation: Confirm the target prototype ID or a single matched prototype name before running an update. <br>
Risk: Using an unintended ProtoHub server could publish prototype files to the wrong environment. <br>
Mitigation: Verify PROTOHUB_URL or the --url argument before running publish, list, or get-link commands. <br>
Risk: A broad API key could allow more access than this workflow requires. <br>
Mitigation: Use a scoped ProtoHub API key and avoid placeholder credentials. <br>
Risk: Publishing from a dirty or incorrect build folder could expose unintended files. <br>
Mitigation: Publish only from a clean output folder or vetted ZIP file that contains the intended index.html entry point. <br>


## Reference(s): <br>
- [tc-protohub on ClawHub](https://clawhub.ai/airclear/tc-protohub) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Evaluation scenarios](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May package user-selected prototype files, call the configured ProtoHub API, and return prototype IDs, preview links, share links, or validation errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
