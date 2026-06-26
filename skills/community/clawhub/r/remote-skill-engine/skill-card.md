## Description: <br>
Cache and use skills from ClawHub and GitHub as if locally installed. Stores remote skills in local cache folder for offline use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oki3505F](https://clawhub.ai/user/oki3505F) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to discover, compare, cache, update, and use remote agent skills from ClawHub, GitHub, or direct URLs as local skills, including offline use after caching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote skills can be promoted into the active local skill set and persist as cached instructions. <br>
Mitigation: Install only reviewed and intentionally selected skills; inspect downloaded SKILL.md and script files before using them; remove cached symlinks for skills that should no longer remain active. <br>
Risk: Fetching skills from arbitrary URLs or untrusted networks can introduce untrusted instructions or files. <br>
Mitigation: Use reviewed, pinned sources; avoid arbitrary URLs; prefer trusted registries or repository references; avoid these helpers on untrusted networks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oki3505F/remote-skill-engine) <br>
- [registry-urls.md](references/registry-urls.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, file paths, JSON examples, and script-generated terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create cached skill files, metadata, and symlinks in the user's local OpenClaw workspace when its helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
