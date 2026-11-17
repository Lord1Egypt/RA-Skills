## Description:

Turns a novel or script excerpt into an anime-style storyboard video workflow that uses Ofox image generation for character opening frames and Ofox video generation for each shot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn story excerpts into anime-style clips with a brief, image-based character setup, dry-run cost checks, and explicit approval before paid video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Story text, prompts, and images are sent to Ofox for processing with the user's OFOX_API_KEY.

Mitigation: Use the skill only when the user is comfortable sharing those inputs with Ofox, and avoid sending sensitive material unless approved.

Risk: Paid image or video generation can spend credits if approval steps are skipped.

Mitigation: Run dry-run quoting first, show the cost table, wait for explicit approval, and keep the --approved flag only on approved real video runs.

Risk: Generated files can be written to an unintended project location.

Mitigation: Use a deliberate output directory and report only paths printed by the Ofox scripts.

Risk: Recovery commands that use unpinned npx installers may modify the user's skill setup.

Mitigation: Treat installer commands as user-reviewed commands and do not run them automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/seedance-anime-drama)
- [Server-listed skill homepage](https://github.com/ofoxai/skills/tree/main/skills/seedance-anime-drama)
- [Ofox API key setup](https://app.ofox.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands, approval tables, file paths, and generation status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OFOX_API_KEY plus curl and jq; uses dry-run quotes and explicit approval before paid generation.]

## Skill Version(s):

2.0.0 (source: server evidence, frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
