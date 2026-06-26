## Description: <br>
Soul Sync personalizes an OpenClaw agent through an adaptive setup conversation, optional local data imports, and generated SOUL.md, USER.md, and MEMORY.md files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ocbenji](https://clawhub.ai/user/ocbenji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to bootstrap or refresh an agent profile so the agent can adapt to their identity, communication preferences, goals, boundaries, and workspace context. It is most useful during first-run setup, profile repair, or deeper personalization with explicitly approved imports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional importers can inspect sensitive account data and local-machine signals. <br>
Mitigation: Use only the importers you explicitly want, review each requested source separately, and avoid local-system scanning unless shell history, bookmarks, repository names, and SSH host aliases are acceptable inputs. <br>
Risk: Profiling artifacts may remain after personalization. <br>
Mitigation: Clear /tmp/soulsync and any .soulsync state files when retained profiling data is no longer wanted. <br>
Risk: Generated profile files may encode inaccurate or unwanted personal details. <br>
Mitigation: Review SOUL.md, USER.md, and MEMORY.md before approving writes, and edit or reject generated content that should not be saved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ocbenji/soul-sync) <br>
- [Google Cloud OAuth credentials](https://console.cloud.google.com/apis/credentials) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and generated workspace profile files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates SOUL.md, USER.md, and MEMORY.md only after user review and approval; optional importers may create local intermediate JSON insights.] <br>

## Skill Version(s): <br>
0.8.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
