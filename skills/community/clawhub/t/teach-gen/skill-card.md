## Description:

根据教案、教材或课件生成交互式教学HTML网页。

This skill is ready for commercial/non-commercial use.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and instructional content creators use this skill to convert lesson plans, textbooks, slide content, or Markdown into interactive HTML teaching pages for math, physics, and chemistry lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may execute untrusted lesson content in the browser.

Mitigation: Use trusted input files, review generated pages before sharing, and prefer a revised version that escapes lesson content or sanitizes any allowed HTML.

Risk: Generated pages may contact third-party CDNs and run remote browser scripts without clear disclosure.

Mitigation: Review online dependency behavior before deployment and prefer bundling, integrity-pinning, or clearly documenting external dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erich1566/skills/teach-gen)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands]

**Output Format:** [Standalone HTML file with concise CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports subject, grade, theme, and output path options; generated pages may execute browser code and load third-party CDN scripts.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
