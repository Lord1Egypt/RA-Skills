## Description:

Turn video links/files into source-grounded, editable short-video posters and key frames/stories into memory journals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legithubhh](https://clawhub.ai/user/legithubhh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to turn video sources or key frames into evidence-grounded short-video posters, editable Chinese typography systems, and memory journal layouts. It is also useful for agents that need structured provenance, visual review, and anti-leakage checks before handing off poster or journal assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can ask an agent to fetch arbitrary video URLs, which may expose unsafe internal or redirected network destinations if media retrieval is not controlled.

Mitigation: Run media fetching through a sandboxed downloader or proxy that blocks private, loopback, link-local, metadata, and redirected internal destinations, with strict size and timeout limits.

Risk: Archive, delete, optimization, and media-processing workflows may affect user privacy if source material or user content is retained or reused without confirmation.

Mitigation: Keep these workflows user-confirmed and privacy-bounded, and avoid storing raw prompts, video links, media pixels, IP addresses, keys, or personal content in optimization artifacts.

## Reference(s):

- [Portable data contracts](references/data-contracts.md)
- [Poster Typography Director](references/poster-typography.md)
- [Product principles](references/product-principles.md)
- [Tool-agnostic prompt pack](references/prompt-pack.md)
- [Journal style profiles](references/style-profiles.md)
- [Usage-evidence optimization workflow](references/usage-optimization.md)
- [Evidence-Grounded Video Poster Workflow](references/video-poster-workflow.md)
- [Workflow playbook](references/workflow-playbook.md)
- [Typography plan example](references/typography-plan.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured JSON specifications with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include source records, evidence indexes, narrative briefs, concept comparisons, typography plans, editable poster or journal structures, audits, warnings, blockers, and provenance notes.]

## Skill Version(s):

2.6.0 (source: evidence.json release.version and README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
