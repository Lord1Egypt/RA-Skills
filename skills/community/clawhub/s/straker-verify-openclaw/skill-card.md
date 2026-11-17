## Description:

Straker Verify helps agents request AI translation, translation quality boosts, and optional human verification through Straker across 100+ languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indynz](https://clawhub.ai/user/indynz)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to translate text or files, improve existing translations, manage translation projects, and request professional human review through Straker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translation text or uploaded files are sent to Straker's external API.

Mitigation: Use the skill only when Straker is an approved external translation provider for the content being submitted.

Risk: Secrets, regulated data, or confidential documents may be exposed if submitted for translation or human review without approval.

Mitigation: Do not submit those materials unless the organization has approved Straker's privacy, retention, and human-review terms.

## Reference(s):

- [Straker Verify API Documentation](https://api-verify.straker.ai/docs)
- [Straker.ai](https://straker.ai)
- [ClawHub Skill Page](https://clawhub.ai/indynz/skills/straker-verify-openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional JSON or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STRAKER_VERIFY_API_KEY; translation text and uploaded files may be sent to Straker's external API.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and changelog state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
