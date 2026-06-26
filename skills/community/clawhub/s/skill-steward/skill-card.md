## Description: <br>
Adds a concise Chinese footer after each assistant response that reports which non-built-in specialized skills were used in the turn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chn012cjus](https://clawhub.ai/user/chn012cjus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to make skill usage visible in each reply by listing specialized ClawHub or user-installed skills while omitting built-in tools and the reporting skill itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill appends a usage footer to every assistant response, which may add unwanted disclosure or formatting in contexts where skill usage should not be shown. <br>
Mitigation: Install it only in environments where a per-response skill-usage footer is expected, and review downstream formatting requirements before use. <br>
Risk: The helper script can retain a temporary local history of skill names in skill_usage_log.json under TEMP or /tmp. <br>
Mitigation: Clear that file or avoid the helper script if local retention of skill usage history is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chn012cjus/skill-steward) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown/plain text footer appended to assistant responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One skill name per line, or a no-skill message when no specialized skill was used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
