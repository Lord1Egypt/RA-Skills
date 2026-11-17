## Description:

Generates Python script and application templates for CLI tools, Flask APIs, FastAPI services, Django commands, scrapers, and bots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to scaffold Python scripts and application templates for automation, API services, data collection, bots, and project starter structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator may overwrite existing Python files such as main.py or a selected NAME.py in the working directory.

Mitigation: Run it only in a disposable project directory and check for existing target files before execution.

Risk: The release evidence describes the generator as overstated and broken, with advertised Flask, Django, scraper, and bot support that should not be relied on as-is.

Mitigation: Review and fix the generator before use, and manually verify generated projects before adopting them.

Risk: Dependency guidance may lead users to install unpinned third-party packages.

Mitigation: Use a virtual environment and pin dependency versions before running generated applications.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunshine-del-ux/skills/python-script-generator)
- [Publisher Profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [code, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, and generated Python files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files may include Python entrypoints, requirements, setup files, tests, and README content depending on template support.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
