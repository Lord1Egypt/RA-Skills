## Description: <br>
Headless video rendering with Remotion v5 on any Linux server, including templates for chat demos, promos, and title cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvanhorn](https://clawhub.ai/user/mvanhorn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to scaffold Remotion video projects, install headless Linux browser dependencies, and render videos such as chat demos, promo clips, title cards, GIFs, and PNG sequences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script can change Linux system packages needed for headless browser rendering. <br>
Mitigation: Run it only on machines where package changes are acceptable and review package lists before approving sudo prompts. <br>
Risk: Generated Remotion projects download npm dependencies before rendering videos. <br>
Mitigation: Treat generated projects like normal JavaScript projects: review dependencies, lockfiles, and generated content before rendering or publishing. <br>


## Reference(s): <br>
- [Remotion](https://remotion.dev) <br>
- [Remotion Linux Dependencies](https://www.remotion.dev/docs/miscellaneous/linux-dependencies) <br>
- [ClawHub Skill Page](https://clawhub.ai/mvanhorn/remotion-server) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates npm-based Remotion project scaffolds and sample template data for local review before rendering.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
