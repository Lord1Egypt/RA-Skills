## Description:

AI-powered tool for extracting structured data from scientific literature PDFs

This skill is for research and development only.

## Publisher:

[jackkuo666](https://clawhub.ai/user/jackkuo666)

### License/Terms of Use:

CC BY 4.0

## Use Case:

Researchers, developers, and external users use this skill to extract structured data from scientific literature PDFs into Markdown tables or CSV files for research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scientific PDFs may be sent to the configured LLM provider or Mathpix during extraction.

Mitigation: Only process documents approved for those providers, verify the configured base URL, and avoid confidential or regulated PDFs unless the endpoint and provider policy are approved.

Risk: Installation instructions include fetching an external installer with curl piped to a shell.

Mitigation: Prefer the documented venv, pip, or conda setup path, and pin or verify installation sources before installing dependencies.

Risk: AI-extracted scientific data may be incomplete or inaccurate.

Mitigation: Manually validate extracted values against the original literature before using them in research outputs or downstream datasets.

Risk: Batch extraction can process many documents through cloud services.

Mitigation: Use a dedicated API key with limits and review document sensitivity before enabling batch mode.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackkuo666/skills/sci-data-extractor)
- [Mathpix API](https://api.mathpix.com/)
- [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Original Project: Automated Enzyme Kinetics Extractor](https://huggingface.co/spaces/jackkuo/Automated-Enzyme-Kinetics-Extractor)
- [Related Paper: Enzyme Co-Scientist](https://www.biorxiv.org/content/10.1101/2025.03.02.153459v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown tables or CSV files, with shell commands and configuration guidance for setup and extraction.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an LLM API key for extraction; optional Mathpix credentials enable OCR.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
