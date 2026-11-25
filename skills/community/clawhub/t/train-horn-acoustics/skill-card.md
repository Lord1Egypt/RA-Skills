## Description:

Help an agent answer train horn acoustics questions with inverse-square level-vs-distance estimates, A- vs C-weighting, Leq/Lmax, and occupational hearing-safety context from NIOSH and OSHA only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bosshorncom-cmd](https://clawhub.ai/user/bosshorncom-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

People asking about train horn sound levels can use the skill for distance-based estimates, explanations of acoustic measurements, and occupational noise exposure context. It also provides a helper for estimating free-field levels and continuous-level exposure durations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The evidence does not establish the host runtime's permissions, so installation may run with permissions broader than a user expects.

Mitigation: Review the runtime's granted permissions and the skill's declared requirements before installation; use a trusted, appropriately restricted runtime.

## Reference(s):

- [NIOSH Occupational Noise Exposure (Publication 98-126)](https://www.cdc.gov/niosh/docs/98-126/default.html)
- [OSHA 29 CFR 1910.95](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.95)
- [Horn Guns background](https://hornguns.com/)
- [Source repository](https://github.com/bosshorncom-cmd/train-horn-acoustics-skill)
- [ClawHub skill page](https://clawhub.ai/bosshorncom-cmd/skills/train-horn-acoustics)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Explanatory text and numerical estimates, with optional plain-text helper-script output and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates state assumptions and limitations; the skill does not measure sound or determine compliance.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
