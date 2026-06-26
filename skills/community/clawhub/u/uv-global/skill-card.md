## Description: <br>
Provision and reuse a global uv environment for ad hoc Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqiao](https://clawhub.ai/user/guoqiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create and reuse a shared uv-managed Python environment for quick scripts that need extra packages without setting up a full project environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow creates a persistent shared Python environment and installs bundled packages. <br>
Mitigation: Inspect install.sh before running it and remove packages that are not needed for the intended work. <br>
Risk: Adding the global uv environment to PATH can change which Python and helper commands run by default. <br>
Mitigation: Only prepend ~/.uv-global/.venv/bin to PATH when the shared environment is intentionally needed. <br>
Risk: The install flow may rely on external uv installation and package supply chains. <br>
Mitigation: Run the install only in environments where the uv installer and package sources are trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guoqiao/uv-global) <br>
- [Publisher Profile](https://clawhub.ai/user/guoqiao) <br>
- [Source Homepage](https://github.com/guoqiao/skills/blob/main/uv-global/uv-global/SKILL.md) <br>
- [uv Installer](https://astral.sh/uv/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation and use of a persistent uv project at ~/.uv-global.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
