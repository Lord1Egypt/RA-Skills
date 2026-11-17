## Description:

Translates one explicitly selected article from `ai-thoughts/docs/` into Simplified Chinese and writes a same-name `-zh-hans.md` file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writers use this skill to translate one named article into Simplified Chinese while preserving its structure, links, code, and technical terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a source-renaming instruction despite the skill's stated translation-only scope, and scan coverage was partial.

Mitigation: Review the source-renaming instruction before installation and confirm any source rename and resulting output path before allowing the skill to write files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/translate-to-zh-hans)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [A Simplified Chinese Markdown file with the source article's filename and a `-zh-hans.md` suffix.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Acts on one explicitly selected article and preserves its Markdown structure and technical terms.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
