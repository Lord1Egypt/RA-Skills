## Description:

Compare French micro-entreprise, regime reel, and versement liberatoire scenarios using Vestafolio API calls, while collecting missing simulator inputs before giving a personalized recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

French freelancers, consultants, and advisors use this skill to compare micro-entreprise options against a simplified regime reel scenario, including ACRE, CIPAV affiliation, marginal tax rate, fiscal parts, and RFR N-2 considerations. The skill is intended to produce estimates and guidance from the Vestafolio simulator, not standalone tax advice.

### Deployment Geography for Use:

France

## Known Risks and Mitigations:

Risk: The skill may transmit sensitive financial and household tax inputs to Vestafolio.

Mitigation: It requires the agent to summarize the exact fields and values first, obtain user agreement, and avoid sending unnecessary personal data or conversation history.

Risk: The simulator output may be mistaken for definitive tax advice.

Mitigation: The skill instructs the agent to ground answers in the API result, state assumptions and limits, and present the calculation as an estimate.

## Reference(s):

- [Vestafolio](https://www.vestafolio.com)
- [Vestafolio Micro-entreprise API](https://www.vestafolio.com/api/tools/v1/micro-entreprise)
- [Vestafolio Micro-entreprise Simulator](https://www.vestafolio.com/simulateurs/micro-entreprise)
- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-micro-entreprise)

## Skill Output:

**Output Type(s):** [Text, Guidance, API calls]

**Output Format:** [Markdown prose with summarized API inputs, assumptions, calculation results, and limitations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user agreement before sending simulator fields to Vestafolio; omits unnecessary personal data and conversation history.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
