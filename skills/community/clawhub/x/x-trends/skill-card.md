## Description: <br>
Fetches current top trending topics on X (Twitter) for any country using public aggregators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anishtr4](https://clawhub.ai/user/anishtr4) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to fetch current public X trend names, volumes, ranks, and source links for a selected country or worldwide view. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Returned trend names, volumes, and links are untrusted public web data. <br>
Mitigation: Review, validate, or sanitize the output before passing it to downstream automation or publishing workflows. <br>
Risk: The CLI depends on getdaytrends.com availability and page structure. <br>
Mitigation: Handle empty results and fetch errors explicitly, and avoid treating the output as an authoritative source without corroboration. <br>
Risk: The package relies on npm dependencies at install and runtime. <br>
Mitigation: Install from the reviewed release artifact and keep dependency scanning in the normal release process. <br>


## Reference(s): <br>
- [getdaytrends.com](https://getdaytrends.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Colorized terminal table or JSON array of trend objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trend objects include rank, name, volume, and link when available.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact frontmatter and package.json report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
