## Description:

PullThatUpJamie helps agents search a semantically indexed podcast corpus, build timestamped research sessions, discover podcast appearances, ingest feeds, and generate shareable audio/video clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unclejim21](https://clawhub.ai/user/unclejim21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve podcast evidence, assemble research sessions with timestamped audio deeplinks, generate clips, and ingest new podcast feeds when the desired source is not yet indexed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid access uses L402 and optional NWC values that function as sensitive bearer credentials.

Mitigation: Store credentials securely, avoid logging or sharing them, and use a low-balance wallet with strict limits.

Risk: The optional wallet workflow documents unpinned local package execution through npx.

Mitigation: Prefer the free tier or a normal wallet first; only run local payment tooling after independently verifying and pinning the package.

Risk: Research sessions and share links may expose curated podcast research material.

Mitigation: Do not upload sensitive or private research material into sessions or public share links.

## Reference(s):

- [PullThatUpJamie homepage](https://pullthatupjamie.ai)
- [ClawHub skill page](https://clawhub.ai/unclejim21/skills/pullthatupjamie)
- [RRA - Retrieve, Research, Analyze](references/podcast-rra.md)
- [Create Module - Audio Clip Generation](references/create.md)
- [L402 protocol](https://docs.lightning.engineering/the-lightning-network/l402)
- [lnget](https://github.com/lightninglabs/lnget)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTTP examples, JSON API responses, timestamped deeplinks, research session URLs, and clip URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require optional L402 bearer credentials for paid API calls; free tier and corpus browsing are documented.]

## Skill Version(s):

1.6.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
