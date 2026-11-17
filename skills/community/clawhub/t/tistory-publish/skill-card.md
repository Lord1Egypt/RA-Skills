## Description:

Automate Tistory blog publishing via OpenClaw Playwright CDP, including TinyMCE editor manipulation, OG card insertion, banner upload, tag registration, category setting, and representative image selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garibong-labs](https://clawhub.ai/user/garibong-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to prepare and publish Tistory blog posts through an authenticated OpenClaw-controlled browser session. It supports HTML body insertion, category selection, tags, image upload, OG cards, and public or private publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish live Tistory posts through an authenticated browser session.

Mitigation: Use --private or a test blog first, then review title, body, category, tags, images, and OG cards before public publishing.

Risk: The login helper can use a Kakao credential file to recover a Tistory session.

Mitigation: Keep credential files outside shared repositories with tight file permissions, and pass them only via --cred-file or TISTORY_CRED_FILE when needed.

Risk: Untrusted body HTML or blog host values can affect browser automation and OG placeholder handling.

Mitigation: Use trusted body files and known Tistory blog domains until the evidence guidance notes that OG placeholder escaping and host validation issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/garibong-labs/skills/tistory-publish)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, HTML content expectations, and JSON status responses from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update public or private Tistory posts through an authenticated browser session.]

## Skill Version(s):

5.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
