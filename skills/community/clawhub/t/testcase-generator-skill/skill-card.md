## Description:

Generates Chinese-language functional test case workbooks from requirement documents, API definitions, database schemas, and existing examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hughzmflying](https://clawhub.ai/user/hughzmflying)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and test analysts use this skill to draft standardized functional, API, data, UI, boundary, and priority-labeled test cases from product or technical inputs. It can also propose shell-command usage for generating spreadsheet outputs with the bundled script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill has overstated capabilities and does not show real parsing support for Swagger/OpenAPI, database DDL, DOCX, or XLSX references.

Mitigation: Treat generated workbooks as drafts, review them against the source requirements, and confirm parser behavior before relying on API, database, DOCX, or XLSX claims.

Risk: The skill reads the user-specified local input file and writes generated test cases to disk.

Mitigation: Run it only on intended local files and inspect the output path and workbook contents before sharing or using the results.

## Reference(s):

- [Priority Guide](references/priority_guide.md)
- [Testcase Examples](references/testcase_examples.md)
- [ClawHub Skill Page](https://clawhub.ai/hughzmflying/skills/testcase-generator-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance and local spreadsheet files such as XLSX or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workbooks should be reviewed before use; the bundled script reads a named local input file and writes a local output file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
