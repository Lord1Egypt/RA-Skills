## Description:

Checks whether the active Python environment can run a PDF summarization and translation pipeline, and can optionally install the required libraries for LangChain, PaddleOCR, and HTML-to-PDF rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergeypetrakov](https://clawhub.ai/user/sergeypetrakov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before summarizing or translating a user-provided PDF to verify the local runtime and, when requested, install missing dependencies. It is useful when preparing a fresh environment for a PDF OCR, summarization, translation, and HTML-to-PDF workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional install mode modifies the active Python environment and downloads many Python packages plus Chromium.

Mitigation: Run the skill in a virtual environment and use install mode only when preparing an environment for this PDF workflow.

Risk: The import check calls python-dotenv, which may load a local .env file into the script process.

Mitigation: Run from a controlled working directory and review local environment files before executing the check.

Risk: The workflow depends on Python 3.11 and external system tooling such as poppler for PDF rendering support.

Mitigation: Confirm Python 3.11 and required system packages are available before relying on a successful pipeline run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergeypetrakov/skills/sum-and-translate-install-check)
- [Publisher profile](https://clawhub.ai/user/sergeypetrakov)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Text status report with OK, FAIL, SKIP, and WARN lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns exit code 0 when required imports are available and exit code 1 when imports are missing.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
