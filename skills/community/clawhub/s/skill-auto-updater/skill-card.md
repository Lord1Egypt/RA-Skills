## Description: <br>
Local-modification-preserving clawhub skill updater. Saves changes as diff patch, applies to new versions, reports conflicts clearly. No forced overwrites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tempest-01](https://clawhub.ai/user/tempest-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw or ClawHub users use this skill to update ClawHub-installed skills while preserving local modifications as patches and surfacing merge conflicts for manual resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The updater can persistently change installed skill files. <br>
Mitigation: Use it only on backed-up skills, prefer targeting one skill at a time, and review generated patches and conflict reports before accepting changes. <br>
Risk: Automatic preservation and dry-run behavior may not fully match the stated safety expectations. <br>
Mitigation: Treat dry-run output as advisory, verify the resulting files manually, and avoid relying on automatic preservation for important local changes. <br>
Risk: Patch merges can conflict with newer skill versions. <br>
Mitigation: Resolve reported conflicts manually or discard saved changes only after confirming that accepting the newer version is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tempest-01/skill-auto-updater) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [ClawHub registry](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local patch, snapshot, and conflict-report files under managed skill directories.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
