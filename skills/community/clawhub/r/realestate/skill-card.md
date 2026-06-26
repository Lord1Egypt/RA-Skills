## Description: <br>
Real estate transaction support with affordability analysis, property evaluation, and offer strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home buyers, sellers, renters, and their supporting agents use this skill for educational real-estate planning, affordability estimates, property evaluation checklists, offer planning, lease review support, and transaction milestone tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-estate and financial planning details may be saved locally by the skill. <br>
Mitigation: Install only if local storage of this information is acceptable, and manage retention or deletion of the agent workspace memory files. <br>
Risk: Affordability estimates, property evaluations, lease notes, and offer strategies may be incomplete or unsuitable for a specific jurisdiction or transaction. <br>
Mitigation: Treat outputs as educational support and verify decisions with licensed real-estate, mortgage, and legal professionals. <br>
Risk: The artifact references helper scripts that are not included in this release. <br>
Mitigation: Use only bundled files or trusted local code, and do not fetch missing helper scripts from untrusted sources. <br>


## Reference(s): <br>
- [RealEstate on ClawHub](https://clawhub.ai/AGIstack/realestate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with local script commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local real-estate planning records under the agent workspace memory directory.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
