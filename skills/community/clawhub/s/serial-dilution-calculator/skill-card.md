## Description: <br>
Generate qPCR/ELISA dilution protocols with precise pipetting steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Wet-lab practitioners and agent workflows use this skill to calculate serial dilution concentrations and pipetting steps for qPCR standard curves, ELISA setup, drug response assays, and MIC determinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated wet-lab protocols may contain incorrect units, dilution math, or assumptions for a specific assay. <br>
Mitigation: Review concentrations, volumes, dilution factors, and assay requirements before using the output in the lab. <br>
Risk: The implemented script does not cover every feature advertised in the skill documentation. <br>
Mitigation: Confirm the generated output includes the needed protocol details before relying on it for plate setup or experiment planning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/serial-dilution-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text protocol with concentration rows and pipetting volumes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external dependencies; runs locally as a Python script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
