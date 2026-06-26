## Description: <br>
ClawHub Guard helps agents browse, search, audit, and install ClawHub skills with lightweight marketplace risk checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangxianzhan](https://clawhub.ai/user/huangxianzhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to scan and search the ClawHub marketplace, rank skills by rough risk signals, audit installed skills, and review a skill before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install other skills and persistently change the local skill environment. <br>
Mitigation: Use scan and search results as rough discovery only; manually inspect any skill before installing it. <br>
Risk: The skill may overstate the strength of its automated checks. <br>
Mitigation: Treat it as an experimental marketplace helper, not a trusted security gate. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/huangxianzhan/skill-market-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-like terminal text with risk labels, recommendations, and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute ClawHub CLI subprocesses for marketplace search, inspection, listing, and installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, frontmatter, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
