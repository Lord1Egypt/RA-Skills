## Description: <br>
Generates block randomization lists for randomized controlled trials, clinical studies, and animal studies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, study teams, and research operations staff use this skill to generate ready-to-use block randomization tables with configurable subject counts, groups, and block sizes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Python script can overwrite the CSV file path selected by the user. <br>
Mitigation: Use a workspace-local output filename, check whether the file already exists, and confirm overwrite intent before running the skill. <br>
Risk: Generated randomization outputs may be used in regulated clinical or study workflows without independent validation. <br>
Mitigation: Validate the randomization method and generated allocation table before using the output for regulated or high-stakes study work. <br>


## Reference(s): <br>
- [Randomization Gen on ClawHub](https://clawhub.ai/aipoch-ai/randomization-gen) <br>
- [AIpoch publisher profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Files, CSV, Shell commands, Guidance] <br>
**Output Format:** [CSV randomization table with concise execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or overwrites a CSV at the selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
