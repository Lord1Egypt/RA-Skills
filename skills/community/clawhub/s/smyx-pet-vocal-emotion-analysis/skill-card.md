## Description: <br>
Recognizes cat and dog vocalizations with pet voiceprint AI and returns emotions, behavioral intent, structured results, suggestions, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze cat or dog audio/video inputs, infer likely vocal emotion and intent, and retrieve prior cloud-generated pet vocal analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says this skill sends pet media, file paths or URLs, and linked report history to the publisher's cloud service. <br>
Mitigation: Use only with media and report history you are comfortable sharing with the publisher, and review the cloud API behavior before deployment. <br>
Risk: The security review flags automatic identity creation, local token storage, and cloud history retrieval as broader than pet vocal analysis alone. <br>
Mitigation: Confirm that automatic identity handling, local state, and history access match your privacy expectations before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-vocal-emotion-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON-like structured analysis text with optional report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save analysis output to a user-specified file and may print cloud report history as Markdown tables.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
