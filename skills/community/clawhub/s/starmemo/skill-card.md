## Description: <br>
starmemo is an OpenClaw memory skill that stores structured memories, maintains a knowledge base, recalls prior context heuristically, and can use AI optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nandujia](https://clawhub.ai/user/nandujia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use starmemo to let an OpenClaw agent save structured conversation memories, search prior context, and maintain a local knowledge base with optional AI processing and web learning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory may save normal conversation text, including sensitive personal or business data if entered. <br>
Mitigation: Review settings and stored memory files before use, and do not enter secrets or sensitive personal or business data unless that storage is intended and approved. <br>
Risk: AI optimization and web features may send memory content to configured external services. <br>
Mitigation: Keep AI and web features disabled unless the configured external services are trusted and approved for the data being processed. <br>
Risk: API keys can be exposed through command-line history or local configuration if handled carelessly. <br>
Mitigation: Avoid passing API keys on the command line and review local provider configuration before enabling external AI calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nandujia/starmemo) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent local memory and knowledge files; optional AI and web features can send content to configured external services.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
