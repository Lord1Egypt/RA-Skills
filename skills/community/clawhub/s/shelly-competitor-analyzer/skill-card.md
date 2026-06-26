## Description: <br>
Generates a detailed report on a company's market position, pricing, social activity, recent news, and strengths by analyzing its name or URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudiodrusus](https://clawhub.ai/user/claudiodrusus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and market researchers use this skill to generate a structured competitor report for a company name or URL, including overview, pricing, social presence, recent news, and a brief strengths-and-weaknesses assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted company name or URL could exploit the shell script's input quoting issue and run local commands. <br>
Mitigation: Review or fix analyze.sh before installing, and run it only with trusted company names or URLs. <br>
Risk: Search queries for the target company are sent to DuckDuckGo and a markdown report is created in the current directory. <br>
Mitigation: Avoid sensitive targets unless that external search behavior and local report creation are acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/claudiodrusus/shelly-competitor-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown report printed to stdout and written to a local .md file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and internet access; standalone mode queries DuckDuckGo.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
