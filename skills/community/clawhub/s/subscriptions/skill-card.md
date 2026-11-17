## Description:

Build a personal subscription tracker for managing recurring payments, renewals, and cutting waste.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to maintain a local subscription tracker, review recurring spending, identify unused services, and receive renewal or price-increase reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist sensitive financial metadata from broad subscription-related triggers.

Mitigation: Ask the agent to confirm before adding entries, omit payment card fragments unless needed, and treat the ~/subscriptions/ folder as sensitive local financial data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/subscriptions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown subscription records and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local files under ~/subscriptions/; entries may contain sensitive subscription costs, billing dates, usage notes, and payment method fragments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
