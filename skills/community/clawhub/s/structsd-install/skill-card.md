## Description: <br>
Installs the structsd binary by guiding agents through prebuilt release downloads or source builds with Go 1.23+. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when structsd is missing, when setting up a new machine, or when they need to install or update the Structs chain binary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Go replacement snippets can remove an existing /usr/local/go toolchain. <br>
Mitigation: Confirm how Go is currently installed before running sudo rm -rf /usr/local/go, and prefer prebuilt structsd releases when they fit the platform. <br>
Risk: The optional Ignite installer uses a curl-to-bash command. <br>
Mitigation: Treat Ignite as a separate optional installer and review it before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abstrct/structsd-install) <br>
- [structsd releases](https://github.com/playstructs/structsd/releases) <br>
- [structsd source repository](https://github.com/playstructs/structsd.git) <br>
- [Structs tools configuration](https://structs.ai/TOOLS) <br>
- [structs-onboarding skill](https://structs.ai/skills/structs-onboarding/SKILL) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides separate install paths for prebuilt binaries, source builds, updates, verification, optional Ignite setup, and troubleshooting.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
