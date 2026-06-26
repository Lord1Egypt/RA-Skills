## Description: <br>
Packages UOS/deepin desktop applications as Debian packages under /opt/apps/${appid}/ and helps generate compliant info, desktop, icon, and validation files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaneniu](https://clawhub.ai/user/zaneniu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and package maintainers use this skill to scaffold, build, inspect, and validate UOS/deepin application .deb packages that follow UnionTech packaging conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Debian packages can include maintainer scripts that run during install or removal. <br>
Mitigation: Inspect DEBIAN/preinst, postinst, prerm, and postrm before installing any generated package. <br>
Risk: udev rules and hardware-integration hooks can change system behavior. <br>
Mitigation: Include udev rules only when the packaged application truly needs hardware integration, then test in a disposable environment before installing on a main system. <br>
Risk: Packaging untrusted application sources can produce packages that install unwanted files or behavior. <br>
Mitigation: Build only from trusted application sources and validate the .deb contents before installation. <br>


## Reference(s): <br>
- [Uos Packager on ClawHub](https://clawhub.ai/zaneniu/uos-packager) <br>
- [references/template_build.sh](references/template_build.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated packaging file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated Debian packaging scripts, control files, desktop entries, icon placeholders, and validation steps.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
