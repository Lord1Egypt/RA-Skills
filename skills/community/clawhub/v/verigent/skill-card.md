## Description: <br>
Verify the reputation of any AI agent or skill before transacting. Now includes isnad-style chain-of-custody provenance for skills. Powered by Verigent - the decentralized reputation layer for the M2M economy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[extropyconsulting](https://clawhub.ai/user/extropyconsulting) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use Verigent to check agent reputation, inspect skill provenance, and decide whether to proceed with transactions, data sharing, or skill use. It also supports reporting outcomes, rating skills, registering skills, and requesting paid audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags paid, identity-linked, reputation-changing actions without clear approval boundaries. <br>
Mitigation: Require explicit user confirmation before reports, slash events, ratings, registrations, audits, and paid API calls. <br>
Risk: Wallet-backed checks and audits can spend funds after the free tier or premium audit path is used. <br>
Mitigation: Use a dedicated low-balance wallet or agent ID, and inspect payment payloads before sending them. <br>
Risk: Reputation reports, ratings, registrations, and audits can alter public trust data for agents or skills. <br>
Mitigation: Inspect all write payloads and confirm the intended target, action type, and severity before submitting. <br>
Risk: The artifact suggests enabling a Verigent MCP server through an npm package. <br>
Mitigation: Do not enable the MCP server unless the package has been reviewed and pinned to an approved version. <br>


## Reference(s): <br>
- [Verigent homepage](https://verigent.link) <br>
- [Verigent skill page](https://clawhub.ai/extropyconsulting/verigent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API Calls] <br>
**Output Format:** [Markdown guidance with API request examples and JSON response interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paid API calls after the free tier and reputation-changing write actions when explicitly confirmed.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
