## Description: <br>
Helps verify whether skill signing events are recorded in an independently auditable transparency log, exposing gaps between registry claims and independently verifiable signing history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and registry operators use this skill to audit whether skill signing records are backed by accessible, append-only transparency logs and to identify coverage gaps or cross-registry inconsistencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registry URL or skill-record inputs may be queried during an audit. <br>
Mitigation: Only provide registry URLs, skill identifiers, or records that are intended to be audited. <br>
Risk: Audit conclusions depend on the availability and quality of the underlying transparency-log data. <br>
Mitigation: Treat the report as evidence-gathering guidance and verify important findings against the relevant registry or log operator before acting. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown audit report with ratings, findings, risk assessment, and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference required local binaries curl and python3 when checking accessible registry or log data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
