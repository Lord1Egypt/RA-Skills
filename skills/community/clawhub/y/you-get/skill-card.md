## Description: <br>
You Get helps agents guide users through downloading videos, audio, and images from supported websites with the you-get CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install you-get, inspect available media formats, choose download options, and troubleshoot media downloads from supported websites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags broad command authority for downloads, package management, cookies, proxies, sudo, and firewall-related workflows. <br>
Mitigation: Review every command, URL, install source, and output path before execution; reject unexpected sudo, firewall-disabling, or system-changing actions. <br>
Risk: Cookie files and proxy settings can expose account access or route traffic through untrusted infrastructure. <br>
Mitigation: Do not paste raw cookies into chat, do not grant automatic browser cookie database access, and avoid untrusted proxies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cn-big-cabbage/you-get) <br>
- [you-get GitHub Repository](https://github.com/soimort/you-get) <br>
- [you-get Website](https://you-get.org/) <br>
- [you-get Wiki](https://github.com/soimort/you-get/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose media download, package installation, proxy, cookie, and file-output commands for user review.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
