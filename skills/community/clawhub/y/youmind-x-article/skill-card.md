## Description:

Writes and publishes X (Twitter) tweets and threads with YouMind-assisted topic research, 280-character adaptation, numbered multi-tweet sequencing, and publishing through the user's X account connected in YouMind.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and publishing teams use this skill to draft, adapt, preview, and optionally publish short X posts or native reply-chain threads from topics, talking points, raw text, or longer source articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured YouMind API key can enable publishing through the user's connected X account.

Mitigation: Keep the key in the canonical YouMind config, connect only the intended X account, and require explicit user approval before every publish action.

Risk: Deletion behavior is under-disclosed in the release evidence.

Mitigation: Review or remove the delete command before install, and require explicit confirmation before any delete request.

Risk: Local image paths may be uploaded through credential-bearing YouMind network calls.

Mitigation: Avoid passing local image paths unless the file contents are intended for upload; prefer already-hosted YouMind CDN URLs.

Risk: Changing the YouMind base URL can redirect credential-bearing requests.

Mitigation: Keep youmind.base_url fixed to https://youmind.com/openapi/v1 except in a reviewed local testing setup.

Risk: Dependency installation is performed without a reviewed lockfile in the artifact.

Mitigation: Use a reviewed lockfile-based install before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mindy-youmind/skills/youmind-x-article)
- [YouMind X OpenAPI Reference](references/api-reference.md)
- [X Publishing Pipeline](references/pipeline.md)
- [X Platform DNA](references/platform-dna.md)
- [Generation Playbook](references/content-generation-playbook.md)
- [Adaptation Playbook](references/content-adaptation-playbook.md)
- [Dispatch Integration Protocol](shared/DISPATCH_CONTRACT.md)
- [YouMind Home Directory](shared/YOUMIND_HOME.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown drafts, plain-text tweet or thread content, CLI command output, result links, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish through YouMind OpenAPI when the user has configured a YouMind API key, connected X account, eligible plan, available credits, and explicit publish approval.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, toolkit/package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
