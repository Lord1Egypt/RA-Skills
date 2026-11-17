## Description:

Guides an agent through yt-mem-ai CLI workflows for ingesting YouTube videos, discovering uploads, searching a local library, rating recommendations, compiling highlights, building supercuts, checking status, and managing configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dasein108](https://clawhub.ai/user/dasein108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate the yt-mem-ai YouTube memory CLI from an agent session, including video ingestion, discovery, search, recommendations, summaries, highlight compilation, supercut generation, and configuration management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run the current third-party yt-mem-ai package through uvx at use time.

Mitigation: Use a pinned and reviewed package version, and run the CLI in a sandboxed environment before allowing it to process important data.

Risk: Some workflows may require browser cookies, Keychain access, or proxy credentials.

Mitigation: Use a dedicated browser profile for YouTube cookies, avoid granting Keychain or browser-cookie access unless necessary, and rotate or remove stored proxy credentials after use.

Risk: The skill can download media, write configuration, and generate local output files.

Mitigation: Review proposed commands before execution and check reported output paths for generated digests, compilations, frames, or supercuts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dasein108/skills/yt-mem)
- [Publisher profile](https://clawhub.ai/user/dasein108)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated local files such as digests, compilations, frames, and supercuts when CLI commands create them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
