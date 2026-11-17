## Description:

Provides real-time web browsing and content extraction by navigating URLs and summarizing page text up to 2000 characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrslu01](https://clawhub.ai/user/zrslu01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to let a Thundarr agent fetch web pages and summarize page text for web research, documentation lookup, and news or current-information checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web page summaries may omit important content because the artifact states that output is limited to the first 2000 characters and does not support JavaScript-heavy SPA rendering.

Mitigation: Use the skill for lightweight browsing and summarization, and verify important claims against the source page or another browser when completeness matters.

Risk: Functionality may be incomplete in environments that do not provide the referenced browse.py tool.

Mitigation: Install only in an environment that supplies the expected browsing capability, and test a representative URL before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zrslu01/skills/thundarr-browser)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown responses with extracted page summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are limited to the first 2000 characters of page text; JavaScript-heavy SPA rendering is not supported.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
