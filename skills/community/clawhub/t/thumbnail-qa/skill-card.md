## Description: <br>
Thumbnail QA scans Next.js pages for poorly cropped fill-mode images, evaluates focal points, applies object-position fixes, and records before/after evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit image thumbnails in Next.js projects and propose or apply CSS object-position fixes with screenshot-backed review evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect a Next.js project, start a local development server, edit CSS, write .gstack reports and screenshots, and create git commits. <br>
Mitigation: Run it on a clean branch, review proposed edits and screenshot evidence before accepting changes, and require explicit confirmation before commits. <br>
Risk: Broad or automatic triggers can cause repository edits when thumbnail-related language or new public images are detected. <br>
Mitigation: Use the skill only in intended web project directories and confirm scope before allowing it to apply fixes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/thumbnail-qa) <br>
- [Publisher profile](https://clawhub.ai/user/kaicianflone) <br>
- [Project homepage](https://github.com/kaicianflone/thumbnail-qa-skill) <br>
- [gstack browser dependency](https://github.com/garrytan/gstack) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, screenshots, CSS edits, git commits, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces .gstack thumbnail QA reports and before/after screenshot evidence when run in a supported project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
