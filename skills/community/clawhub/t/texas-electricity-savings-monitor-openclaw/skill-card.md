## Description: <br>
Guides Texas residential electricity users through address confirmation, ESIID lookup, usage estimation, plan recommendation, self-service plan routing, and daily or weekly savings monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catkennel](https://clawhub.ai/user/catkennel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users in Texas use this skill to confirm a service address, compare residential electricity plans, route to a Personalized Energy address page, and set a daily or weekly monitoring preference. <br>

### Deployment Geography for Use: <br>
United States - Texas residential electricity market <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports an embedded live bearer token. <br>
Mitigation: Remove or rotate the token before installation and use a managed secret instead of a hard-coded credential. <br>
Risk: The security evidence reports that household address and utility data are sent to PowerLego and Personalized Energy services. <br>
Mitigation: Disclose the external data sharing to users before lookup and avoid sending addresses unless the user has asked for electricity-plan assistance. <br>
Risk: Plan availability, usage estimates, rates, and projected savings may change or be unavailable for a confirmed address. <br>
Mitigation: Present results as current estimates, avoid guaranteed savings claims, and route users to the live Personalized Energy address page for final review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/catkennel/texas-electricity-savings-monitor-openclaw) <br>
- [Publisher Profile](https://clawhub.ai/user/catkennel) <br>
- [Personalized Energy Texas Electricity Rates](https://www.personalized.energy/electricity-rates/texas) <br>
- [Address Completeness](references/address-completeness.md) <br>
- [Intent Routing](references/intent-routing.md) <br>
- [OpenClaw Execution](references/openclaw-execution.md) <br>
- [Response Strategy](references/response-strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain English or Markdown responses with address candidates, plan summaries, next-step links, and monitoring recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a confirmed Texas service address before producing downstream plan or monitoring guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
