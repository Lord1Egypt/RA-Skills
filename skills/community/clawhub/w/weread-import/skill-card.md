## Description: <br>
Exports WeRead highlights and notes to Markdown files, typically for Obsidian or another local reading directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnixner](https://clawhub.ai/user/gnixner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to import or sync WeRead notes into a local Markdown reading library. It supports single-book exports, full-library syncs, rerendering, and template or frontmatter tag adjustments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to WeRead account data through an API key, browser session, or cookie. <br>
Mitigation: Use the default Gateway API-key mode where possible and install only when the user accepts that account notes will be read for export. <br>
Risk: Browser fallback can start or use a persistent Chrome remote-debugging session. <br>
Mitigation: Close the managed Chrome or CDP session after browser-mode use, and prefer Gateway mode for routine imports and scheduled syncs. <br>
Risk: Legacy profile sync can duplicate sensitive Chrome login data. <br>
Mitigation: Avoid WEREAD_PROFILE_SYNC_MODE=legacy unless the user explicitly accepts copying browser profile data. <br>
Risk: Exports write Markdown files and sync state into the chosen notes directory. <br>
Mitigation: Run verification exports in a temporary directory before writing to a production Obsidian or reading folder. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gnixner/weread-import) <br>
- [GitHub repository](https://github.com/gnixner/weread-import) <br>
- [Workflow reference](references/workflows.md) <br>
- [Design notes](docs/DESIGN.md) <br>
- [Sample Markdown output](examples/sample-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one Markdown file per book plus sync state in the selected output directory.] <br>

## Skill Version(s): <br>
0.4.0 (source: server evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
