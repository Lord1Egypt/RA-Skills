## Description: <br>
Turn scattered notes, metrics, and unfinished tasks into a weekly operating review with wins, misses, blockers, and next-week priorities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and team leads use this skill to turn weekly notes, metrics, tasks, calendar highlights, and goals into an actionable operating review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic trigger phrases may invoke the skill unintentionally. <br>
Mitigation: Confirm the user wants a weekly operating review before collecting inputs or producing outputs. <br>
Risk: The optional Python helper can create or replace its output JSON file. <br>
Mitigation: Run the helper only when the user asks for a local draft file, and use an explicit output path. <br>
Risk: Weekly reviews may include sensitive notes, metrics, task lists, calendar highlights, or goals. <br>
Mitigation: Request only the minimum inputs needed and keep assumptions explicit instead of fabricating missing facts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/weekly-ops-review) <br>
- [README](README.md) <br>
- [Review Template](resources/review_template.md) <br>
- [Example Prompt](examples/example-prompt.md) <br>
- [Smoke Test](tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review memo and structured JSON draft file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a weekly review memo, metrics snapshot, priority list, carry-over board, or a local JSON draft when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact changelog; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
