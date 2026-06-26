## Description: <br>
QA Pilot guides AI agents to test web apps against the original request, fix defects, and report completion only after verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helal-muneer](https://clawhub.ai/user/helal-muneer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use QA Pilot to make coding agents run systematic web and application QA, compare implemented behavior with the original request, fix defects, and provide an honest QA report before marking work complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may test against production systems, external services, payment flows, or forms that submit real data. <br>
Mitigation: Use local or staging environments, test credentials, and test data; require explicit approval before production or external-service testing. <br>
Risk: The self-fix loop may modify application code while resolving QA findings. <br>
Mitigation: Keep normal code review controls around edits, inspect diffs, and re-test changed workflows before accepting completion. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/helal-muneer/qa-pilot) <br>
- [QA Pilot Methodology](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Security Policy](artifact/SECURITY.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance and QA reports, with code edits or shell commands when fixes are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include test plans, issue lists, fix summaries, and retest results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, skill.yaml, changelog released 2026-04-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
