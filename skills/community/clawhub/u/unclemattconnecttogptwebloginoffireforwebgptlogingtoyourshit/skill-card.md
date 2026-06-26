## Description: <br>
Explicit-invocation ChatGPT/Codex web-login bridge for using an already-authenticated local Codex CLI session without copying credentials into the skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uncmatteth](https://clawhub.ai/user/uncmatteth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they explicitly want an agent or another skill to call a locally authenticated Codex/ChatGPT provider without handling raw tokens, cookies, API keys, or local auth files. It is intended for prompts the user is comfortable sending to the authenticated provider account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt text sent through ask or smoke is transmitted to the authenticated provider account. <br>
Mitigation: Use ask and smoke only for prompt content the user explicitly accepts sending to the provider; do not send secrets, private documents, cookies, API keys, or regulated personal data. <br>
Risk: The skill depends on an already-authenticated local Codex/ChatGPT session and cannot provide service when that local provider is unavailable. <br>
Mitigation: Run status first and stop if the authenticated provider cannot be confirmed instead of requesting or copying credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uncmatteth/unclemattconnecttogptwebloginoffireforwebgptlogingtoyourshit) <br>
- [Publisher profile](https://clawhub.ai/user/uncmatteth) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bridge status command avoids printing auth mode, token presence, API-key presence, local paths, or other sensitive environment metadata.] <br>

## Skill Version(s): <br>
1.420.69 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
