## Description: <br>
Resource Master helps estimate and consolidate server hardware requirements for healthcare product projects from local knowledge-base resource-planning documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellohushuai](https://clawhub.ai/user/hellohushuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and implementation teams use this skill to plan healthcare project server resources, compare single-product estimates, and summarize consolidated infrastructure requirements across multiple products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server estimates can be misleading if the local kb folder contains outdated or untrusted resource-planning documents. <br>
Mitigation: Use only vetted kb documents and review the generated estimates before relying on them for procurement or deployment planning. <br>
Risk: Required planning inputs may be missing or ambiguous, such as annual outpatient volume, inpatient volume, staff count, or product list. <br>
Mitigation: Ask for missing inputs before producing final resource tables and keep source-path notes with the estimate. <br>
Risk: The server release version is 1.0.6 while bundled artifact metadata lists 1.0.5. <br>
Mitigation: Confirm that the version mismatch is expected before installing or publishing the card. <br>


## Reference(s): <br>
- [Hardware resource planning template](references/hardware-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/hellohushuai/resource-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown tables and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source-path notes for referenced kb documents when estimates are produced.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence; bundled artifact metadata lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
