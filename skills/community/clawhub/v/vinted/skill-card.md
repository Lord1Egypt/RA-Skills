## Description:

Buy and resell on Vinted with listing systems, price discipline, shipping workflows, and trust-first handling for offers, bundles, and disputes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for practical Vinted buying and resale workflows, including listing quality, pricing discipline, offers, bundles, shipping proof, disputes, and account-safe marketplace decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local marketplace memory under ~/vinted/ may contain preferences, inventory notes, parcel proof logs, or issue history.

Mitigation: Keep persistence off unless useful, and avoid saving personal buyer details or sensitive shipping proof.

Risk: Marketplace actions such as offers, listings, shipping steps, dispute handling, related skill installs, or syncs can affect the user's account or transactions.

Mitigation: Require explicit user approval before live Vinted traffic, irreversible marketplace actions, installs, or sync operations.

## Reference(s):

- [ClawHub Vinted Skill Page](https://clawhub.ai/ivangdavila/skills/vinted)
- [Vinted Marketplace](https://www.vinted.com)
- [Vinted Pro Portal](https://pro-portal.svc.vinted.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown with structured decision templates and local note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-approved marketplace next steps and local ~/vinted/ memory file structure; no hidden outbound requests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
