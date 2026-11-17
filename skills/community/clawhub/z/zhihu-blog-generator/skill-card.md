## Description:

Generates Zhihu-style technical blog posts by selecting topics, collecting technical sources, drafting, refining, and exporting Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xieyuantao7](https://clawhub.ai/user/xieyuantao7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to create Chinese Zhihu-style technical blog drafts from a selected topic. The workflow gathers web, paper, and project source material, creates a draft, refines style and depth, and exports a final Markdown article.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command execution and path handling may affect runner safety.

Mitigation: Review and fix the runner before installation: remove shell execution, validate topic and session inputs, and keep outputs in a controlled directory.

Risk: Generated technical claims may be incorrect, outdated, or insufficiently supported.

Mitigation: Manually verify sources, links, data, code claims, and citations before publishing any generated article.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xieyuantao7/skills/zhihu-blog-generator)
- [Artifact README](artifact/README.md)
- [Artifact skill guide](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown articles with YAML front matter, plus JSON session metadata and logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes topic, collection, draft, refinement, and final output files under a configured session directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
