## Description: <br>
Splits SQL files into object-specific SQL files, analyzes dependencies, and generates dependency-ordered merge scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to split large SQL files into procedures, functions, views, triggers, tables, indexes, and constraints, then generate merge scripts and optional SQL Server to Dameng conversion outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create output SQL files and local license, checkpoint, and configuration files under the user's home directory. <br>
Mitigation: Review target paths before execution and keep generated state files in locations appropriate for the user's environment. <br>
Risk: The license system stores a local machine fingerprint. <br>
Mitigation: Review the license workflow before activation and avoid using production or sensitive machines unless that local identifier storage is acceptable. <br>
Risk: Automated SQL splitting and conversion can produce SQL that differs semantically from the source, including documented TRUNCATE to DELETE conversion behavior. <br>
Mitigation: Inspect generated SQL and test it in a non-production database before applying it to production systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fish1981bimmer/sql-splitter) <br>
- [SQL Server to Dameng Converter Design Notes](references/dm-converter-design.md) <br>
- [dm_converter v3.4.0 Change Notes](references/dm-converter-v340-fixes.md) <br>
- [dm_converter v3.3.0 Fix Notes](references/dm-converter-v330-fixes.md) <br>
- [HRBI Stage Real-World Test Record](references/hrbi-stage-real-world-test.md) <br>
- [Python Indentation Debugging Notes](references/python-indentation-debugging.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python code blocks; generated SQL files and merge scripts when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local output SQL files plus license, checkpoint, and configuration files under the user's home directory.] <br>

## Skill Version(s): <br>
3.4.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
