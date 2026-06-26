## Description: <br>
Turn a one-line idea into a full short video; Revid writes the script, picks visuals, and assembles the cut. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a topic, question, or one-line concept into a short Revid-generated video when they do not already have a script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends video prompts, style notes, and render settings to Revid for processing. <br>
Mitigation: Do not include secrets, regulated data, private customer information, or confidential brand plans unless external sharing with Revid is approved. <br>
Risk: The skill requires a sensitive Revid API key. <br>
Mitigation: Store REVID_API_KEY in approved secret management or environment configuration and avoid committing it to skill files, examples, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/api00/revid-prompt-to-video) <br>
- [Publisher profile](https://clawhub.ai/user/api00) <br>
- [Revid render endpoint](https://www.revid.ai/api/public/v3/render) <br>
- [Revid status endpoint](https://www.revid.ai/api/public/v3/status) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVID_API_KEY and sends the user's prompt, style notes, and render settings to Revid.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
