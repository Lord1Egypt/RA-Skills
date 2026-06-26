## Description: <br>
Blazingly fast text search tool - recursively searches directories for regex patterns with respect to gitignore rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Arnarsson](https://clawhub.ai/user/Arnarsson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to get ripgrep command guidance for fast recursive text search, file type and path filtering, and careful search or replacement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can search hidden or ignored files and expose sensitive matches if used carelessly. <br>
Mitigation: Preview matches, scope searches to intended paths, and be deliberate when using --hidden or --no-ignore. <br>
Risk: Bulk replacement examples can modify many files at once when piped into commands such as sed -i. <br>
Mitigation: Review matched files and preview replacements before running bulk edits, especially outside version-controlled directories. <br>


## Reference(s): <br>
- [ClawHub Ripgrep Release](https://clawhub.ai/Arnarsson/ripgrep) <br>
- [ripgrep GitHub Repository](https://github.com/BurntSushi/ripgrep) <br>
- [ripgrep User Guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the rg binary; install metadata includes Homebrew and apt package options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
