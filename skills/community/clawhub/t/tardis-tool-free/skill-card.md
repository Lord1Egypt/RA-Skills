## Description: <br>
生活事件追踪-免费版 helps individual users record, categorize, search, review, and export personal life events with simple, detailed, and story-based recording modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal productivity agents use this skill to maintain local life-event records, review timelines, search prior entries, and export Markdown reports for personal reflection or archival use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains mismatched SEO trigger text that could cause an agent to invoke it outside the intended life-event tracking use case. <br>
Mitigation: Review or remove the SEO trigger language before deployment so invocation is limited to personal event tracking, timeline review, search, and export tasks. <br>
Risk: The input schema includes callback_url behavior while the release security summary flags under-disclosed network-capable inputs. <br>
Mitigation: Disable or explicitly document callback notifications before use, and confirm that personal records are not sent to external services unexpectedly. <br>
Risk: The skill handles personal life records stored on disk, which may include sensitive information. <br>
Mitigation: Use a local storage path with appropriate access controls and export or share Markdown reports only after reviewing the contents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/tardis-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes local JSON-backed storage, Markdown export, and optional callback_url behavior that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
