## Description: <br>
Verify claims, fact-check content, check URL trustworthiness, and trace claims to their origin using the TruthCheck CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiyishr](https://clawhub.ai/user/baiyishr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run TruthCheck CLI workflows for claim verification, URL trust checks, publisher lookup, and tracing claims to their source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external truthcheck CLI package. <br>
Mitigation: Verify the package source before installing and confirm it is the intended CLI. <br>
Risk: Claims, URLs, or proprietary text may be sent to remote LLM or search providers when those integrations are used. <br>
Mitigation: Use only necessary API keys, avoid confidential inputs unless provider handling is acceptable, or use non-LLM mode or local Ollama for more private checks. <br>


## Reference(s): <br>
- [Truthcheck ClawHub page](https://clawhub.ai/baiyishr/truthcheck) <br>
- [Publisher profile](https://clawhub.ai/user/baiyishr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose CLI commands that produce TruthScore summaries, URL trust checks, claim traces, publisher lookups, and optional JSON output from the external truthcheck CLI.] <br>

## Skill Version(s): <br>
0.4.4 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
