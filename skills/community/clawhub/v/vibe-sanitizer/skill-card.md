## Description: <br>
Use this skill when an agent needs to scan a Git repository for secrets, credentials, or machine-specific file paths, then sanitize safe findings in place or export a sanitized shareable copy using the bundled Python source in ./src. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macoloye](https://clawhub.ai/user/macoloye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to inspect local Git repositories for secrets, credentials, and machine-specific paths before commit, sharing, or publication. It can report findings, safely redact eligible findings in place, create a sanitized export, or generate a starter configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository scanning reads local source files and may surface sensitive findings. <br>
Mitigation: Run scans with the narrowest useful scope and summarize findings with masked previews instead of raw secrets or full local paths. <br>
Risk: In-place sanitization can modify repository files. <br>
Mitigation: Run scan first, review findings, use in-place sanitization only for safe cleanup, and review or re-stage modified files before committing. <br>
Risk: Sanitized exports could be confused with the primary repository. <br>
Mitigation: Export only to a directory outside the source repository and treat the exported copy as a shareable derivative rather than the default replacement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/macoloye/vibe-sanitizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scanner output may be text or JSON; sanitization may rewrite files or create a sanitized export directory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts agents to mask secrets and local paths, prefer narrow scan scopes, scan before sanitizing, and leave review-required findings unchanged unless explicitly directed.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
