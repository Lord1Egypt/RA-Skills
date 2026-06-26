## Description: <br>
Handle archive and compression tasks including compressing, extracting, archiving, packaging, listing contents, and viewing files across formats such as zip, tar, gz, 7z, rar, zst, xz, and bz2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunrenyi](https://clawhub.ai/user/lunrenyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to choose and run x-cmd archive commands for compressing files, extracting archives, listing archive contents, and packaging backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing x-cmd with an automatic pipe-to-shell command can execute remote code without manual review. <br>
Mitigation: Prefer Homebrew or download and review the installer before execution, especially in sensitive environments. <br>
Risk: Extracting untrusted archives can write unexpected files or overwrite important paths. <br>
Mitigation: Review archive contents before extraction and avoid extracting untrusted archives into important directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lunrenyi/x-zuz) <br>
- [x-cmd skill repository](https://github.com/x-cmd/skill) <br>
- [x-cmd website](https://www.x-cmd.com) <br>
- [Installation guide](data/install.md) <br>
- [x-cmd releases](https://github.com/x-cmd/release) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include x-cmd installation guidance, command selection, and archive-handling precautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
