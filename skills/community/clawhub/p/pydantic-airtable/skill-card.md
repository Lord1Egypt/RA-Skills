## Description: <br>
Manage Airtable tables and records via the pydantic-airtable Python library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grishick](https://clawhub.ai/user/grishick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Airtable bases, tables, records, and Pydantic-backed schemas through pydantic-airtable scripts or code guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete Airtable data when used with a token that has write or delete permissions. <br>
Mitigation: Use a least-privilege Airtable token, start with a test base, and review create, update, delete, and sync actions before execution. <br>
Risk: Model-driven operations import and execute a local Python module passed to model_ops.py --module. <br>
Mitigation: Only pass trusted local Python files to --module and inspect the code before running model operations. <br>
Risk: JSON arguments can be loaded from local @file.json inputs. <br>
Mitigation: Inspect file-based JSON payloads before use, especially for batch writes, updates, or schema changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/grishick/pydantic-airtable) <br>
- [pydantic-airtable API surface](references/api-surface.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples, plus JSON output from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Airtable API operations when run with AIRTABLE_ACCESS_TOKEN and AIRTABLE_BASE_ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
