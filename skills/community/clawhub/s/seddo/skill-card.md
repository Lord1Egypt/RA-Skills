## Description: <br>
Coordinate a swarm of AI agents across machines using a private GitHub Gist as a shared communication bus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dofbi](https://clawhub.ai/user/dofbi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Seddo to coordinate AI agents running on different machines or agent frameworks through shared tasks, messages, lessons, and activity logs in a private GitHub Gist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs GitHub Gist access and may use sensitive credentials. <br>
Mitigation: Prefer `gh auth login` or a credential store, avoid pasting tokens into shell history, and confirm the token has only the required gist access. <br>
Risk: Coordination messages, tasks, lessons, and activity are stored in GitHub Gists. <br>
Mitigation: Use only trusted gist IDs and do not place secrets, client data, or other sensitive project details in the shared gist. <br>
Risk: The installer and CLI perform local file installation and remote Gist writes. <br>
Mitigation: Review the installer before running it and run `seddo doctor` to verify GitHub CLI authentication, gist access, and local configuration. <br>
Risk: GitHub Gist writes are last-write-wins and the artifact notes non-atomic read-modify-write behavior. <br>
Mitigation: Run `seddo sync` before writing, avoid simultaneous edits to the same file, and use the documented `LOCK:` convention when contention is likely. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dofbi/seddo) <br>
- [README.md](artifact/README.md) <br>
- [ARCHITECTURE.md](artifact/ARCHITECTURE.md) <br>
- [AGENTS.md](artifact/AGENTS.md) <br>
- [OPENCODE.md](artifact/OPENCODE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated coordination Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates GitHub Gist-backed coordination files for tasks, messages, lessons, roster, protocol, registry, and activity.] <br>

## Skill Version(s): <br>
2.6.5 (source: server release metadata and scripts/seddo.sh) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
