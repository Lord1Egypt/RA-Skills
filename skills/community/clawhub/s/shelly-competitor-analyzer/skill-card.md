## Description:

Generates a structured competitor report for a company name or URL, covering market position, pricing, social presence, recent news, competitors, and a short assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudiodrusus](https://clawhub.ai/user/claudiodrusus)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to gather quick competitive intelligence for a company by name or URL and produce a markdown report for review or follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted company name can trigger local Python code execution through the shell script's input handling.

Mitigation: Review before running, use only trusted company names or URLs, and fix the script to pass the query to Python as an argument rather than interpolating it into Python source.

Risk: Company names, URLs, or targets entered into the script are sent to DuckDuckGo during standalone searches.

Mitigation: Avoid confidential targets and run the skill only where external web searches are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claudiodrusus/skills/shelly-competitor-analyzer)
- [Publisher profile](https://clawhub.ai/user/claudiodrusus)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report written to a competitor-report file and echoed to standard output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access; standalone mode sends search queries to DuckDuckGo.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
