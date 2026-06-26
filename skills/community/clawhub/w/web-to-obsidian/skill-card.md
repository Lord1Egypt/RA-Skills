## Description: <br>
Web-to-obsidian fetches web articles, optionally translates non-Chinese content into Chinese, and saves the result as Obsidian-compatible Markdown with metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ioriiod0](https://clawhub.ai/user/ioriiod0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, knowledge workers, and Obsidian users use this skill to capture web articles, blogs, and documentation as structured Obsidian notes with source links, tags, summaries, and optional Chinese translation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs may be processed by third-party fetch and conversion services. <br>
Mitigation: Use only public, non-sensitive URLs unless the workflow is changed to require explicit third-party opt-in or local fetching. <br>
Risk: HTTPS verification is weakened in the bundled fetch scripts. <br>
Mitigation: Review and update the fetch scripts to use normal HTTPS certificate verification before handling sensitive content. <br>
Risk: Fetched content is written into an Obsidian vault and may include private or untrusted material. <br>
Mitigation: Review generated Markdown before import and avoid saving private, intranet, token-bearing, or otherwise sensitive pages. <br>
Risk: A fixed temporary filename can overwrite or expose intermediate content in the working directory. <br>
Mitigation: Use a unique secure temporary file and remove it after import. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ioriiod0/web-to-obsidian) <br>
- [Publisher profile](https://clawhub.ai/user/ioriiod0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Obsidian-compatible Markdown with YAML frontmatter and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a temporary Markdown file before importing it into an Obsidian vault.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
