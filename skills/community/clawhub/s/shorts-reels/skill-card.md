## Description:

shorts-reels helps agents generate priced batches of cheap vertical 9:16 Ofox video drafts, compare contact-sheet options, and promote one selected take through a separately approved re-render.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting social-video creators, marketers, and developers use this skill to price and run batches of vertical Shorts/Reels/TikTok draft material before paying for a higher-quality promoted take. It is intended for option generation and selection, not for a single finished clip request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can spend money through the user's Ofox account after approval.

Mitigation: Review dry-run cost tables before approving any paid run, and use the approval flag only after the quoted cost has been accepted.

Risk: The skill depends on a separate ofox-video-core installation for API execution and safety behavior.

Mitigation: Confirm ofox-video-core 2.0.0 or newer is installed, and have the user install missing dependencies rather than letting an agent run broad installer commands silently.

Risk: Promoting a draft is a new generation and may not reproduce the selected take exactly.

Mitigation: Describe promotion as a separate paid roll, keep the prompt byte-identical where possible, and require a second dry-run and approval before promotion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/shorts-reels)
- [Skill homepage](https://github.com/ofoxai/skills/tree/main/skills/shorts-reels)
- [Ofox API keys](https://app.ofox.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash command blocks, cost-approval summaries, and output-path reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OFOX_API_KEY, curl, jq, and a compatible ofox-video-core skill; paid generation commands are presented with explicit dry-run pricing and approval steps.]

## Skill Version(s):

2.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
