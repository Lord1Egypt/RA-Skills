## Description:

Star Office UI Master helps an agent deploy and operate a pixel-art office dashboard for visualizing AI assistant status, multi-agent collaboration, mobile viewing, and optional public access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinke](https://clawhub.ai/user/pinke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OpenClaw users use this skill to set up a local or shared status dashboard where agents publish work state, join an office view, and expose a controlled access URL when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public-sharing workflows can expose admin actions, mutating endpoints, and local memory content.

Mitigation: Use trusted local deployment by default; before public exposure, authenticate mutating and memo endpoints and avoid publishing OpenClaw memory contents.

Risk: Weak default credentials and unset Flask secrets can allow unintended asset or session access.

Mitigation: Set strong ASSET_DRAWER_PASS and Flask secret values before sharing the service outside a trusted local environment.

Risk: Status-push clients and join keys can reveal recurring state details or grant access beyond the intended audience.

Mitigation: Confirm status clients send data only to trusted office URLs, rotate join keys, and limit concurrent or expired joins.

Risk: Bundled art assets are described as non-commercial even though the code is licensed separately.

Mitigation: For commercial deployments, replace bundled art with original or properly licensed assets and verify license terms before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pinke/skills/star-office-ui-master)
- [README.en.md](artifact/README.en.md)
- [Star Office UI overview](artifact/docs/STAR_OFFICE_UI_OVERVIEW.md)
- [March 2026 changelog](artifact/docs/CHANGELOG_2026-03.md)
- [Desktop pet state API](artifact/desktop-pet/STATE_API.md)
- [Guest join skill](artifact/frontend/join-office-skill.md)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, configuration snippets, and API endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local service setup steps, state update commands, public tunnel guidance, and optional Gemini API configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
