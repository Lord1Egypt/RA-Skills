## Description: <br>
Fetches and summarizes the latest Singapore Pools TOTO results from official Singapore Pools data files for normal, cascade, hongbao, and special draws. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluesneed](https://clawhub.ai/user/bluesneed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current Singapore Pools TOTO draw details, cite the official source URL, and optionally produce JSON for automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs live web access to singaporepools.com.sg, so results can fail or become stale if the network is unavailable or the official page structure changes. <br>
Mitigation: Allow outbound access only to the documented Singapore Pools endpoints, include the reported source URL in responses, and retry or update the parser when fetch or parsing errors occur. <br>


## Reference(s): <br>
- [Singapore Pools TOTO result sources](references/source-endpoints.md) <br>
- [Official Singapore Pools TOTO results page](https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx) <br>
- [Singapore Pools lottery output data archive](https://www.singaporepools.com.sg/DataFileArchive/Lottery/Output/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text or JSON with source URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes draw date, draw number, winning numbers, additional number, Group 1 prize, winning shares, single-draw page URL, and source file URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
