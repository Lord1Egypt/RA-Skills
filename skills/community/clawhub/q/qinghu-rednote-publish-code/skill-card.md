## Description:

Creates a RedNote scan-to-publish code from a post title, text, and images or video so users can open a prefilled post on RedNote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing teams use this skill to prepare RedNote posts and give users a code to scan for a prefilled publishing flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading the required package introduces third-party software.

Mitigation: Confirm trust in the qhkit package and approve Node/npm installation or upgrades before proceeding.

Risk: A Qinghu token must be supplied, and existing international-site settings may be overwritten.

Mitigation: Choose whether to store the token in configuration or an environment variable, and check the site setting before changing it.

Risk: Paid requests can consume Qinghu credits.

Mitigation: Disclose estimated charges and obtain authorization before making paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-rednote-publish-code)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Text or Markdown with a scan-to-publish code or link and setup guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishing content is prefilled for user review; authorized paid calls may consume Qinghu credits.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
