## Description:

Run local SEO autopilot for boll-koll.se or hyresbyte.se and return PR link plus summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamhjort](https://clawhub.ai/user/adamhjort)

### License/Terms of Use:

MIT

## Use Case:

Developers and site operators use this skill to trigger an allowlisted local SEO automation run for boll-koll.se or hyresbyte.se and receive a pull request link plus a concise findings summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned local seo-autopilot executable through PATH.

Mitigation: Install seo-autopilot from a trusted source, keep untrusted directories out of PATH, and prefer a pinned absolute path or bundled reviewed implementation before routine use.

Risk: The skill may use local repository and network credentials while creating pull requests.

Mitigation: Run it only in a controlled repository environment with appropriately scoped credentials and review generated changes before merging.

Risk: The trigger is broad enough that accidental activation could start an SEO automation run.

Mitigation: Use a narrower trigger or add an explicit confirmation step before executing the local command.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown summary with a pull request URL and optional top SEO findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default target site is boll-koll.se; execution is limited to boll-koll.se and hyresbyte.se.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
