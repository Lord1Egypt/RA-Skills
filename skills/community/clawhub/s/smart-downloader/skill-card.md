## Description:

Smart file downloader with multi-threading, resumable downloads, and progress display

This skill is for research and development only.

## Publisher:

[dkgee](https://clawhub.ai/user/dkgee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to download multiple files or large files with concurrent transfers, resumable downloads, retry handling, custom headers, proxy configuration, and progress display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs real network downloads from broad user-provided URLs.

Mitigation: Review before installing and use only trusted public URLs.

Risk: Custom headers and proxies can expose sensitive request data if misused.

Mitigation: Avoid passing cookies, tokens, or other secrets in headers unless necessary.

Risk: Temporary-file and output-directory behavior can leave or overwrite local files.

Mitigation: Use a dedicated empty output directory and review downloaded files before use.

Risk: Advertised integrity verification should not be treated as authoritative.

Mitigation: Do not rely on the advertised integrity verification; verify important files with independent checksums from trusted sources.

Risk: Unpinned dependencies or shared environments can increase installation risk.

Mitigation: Install dependencies in an isolated environment with pinned versions.

## Reference(s):

- [Sample URLs](references/sample_urls.txt)
- [ClawHub skill page](https://clawhub.ai/dkgee/skills/smart-downloader)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Downloaded files, terminal progress text, and Markdown usage guidance with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use custom request headers, proxies, retry counts, timeouts, chunk sizes, and an output directory with temporary download files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
