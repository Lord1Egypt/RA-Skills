## Description:

Analyze real estate investments with conservative underwriting, financing stress tests, diligence gates, and exit planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate real estate investment opportunities, define a buy box, screen deals, underwrite returns, pressure-test financing, sequence diligence, and decide whether to buy, watch, renegotiate, or pass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local notes may contain recurring strategy, deal, market, and decision information that could become sensitive if the user adds identity, lending, tax, or account details.

Mitigation: Store only decision-useful investment notes, avoid lender logins, tax IDs, full legal documents, account numbers, and other highly sensitive data, and keep the local directory permissioned for the user.

Risk: Real estate legal, tax, insurance, and lending conclusions can be jurisdiction-specific and may be wrong or incomplete without current source material.

Mitigation: Use the skill as decision support, verify material assumptions with authoritative documents or qualified professionals, and do not treat its output as licensed advice.

Risk: Optimistic assumptions can make an investment look safer than it is.

Mitigation: Require conservative underwriting, downside and ugly-case stress tests, explicit reserves, and a written kill-switch before recommending action.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ivangdavila/skills/real-estate-investing)
- [Skill homepage](https://clawic.com/skills/real-estate-investing)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with optional shell command blocks and local memory templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local notes under ~/real-estate-investing/ when the user approves.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
