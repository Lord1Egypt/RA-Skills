## Description: <br>
Queries public ClawHub skill statistics such as stars, downloads, current installs, and all-time installs through curl and the ClawHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tjefferson](https://clawhub.ai/user/tjefferson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, maintainers, and marketplace operators use this skill to check and compare public ClawHub skill popularity and usage metrics without opening the web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill slugs or search terms are sent to ClawHub when the generated commands are run. <br>
Mitigation: Use only public or acceptable-to-share slugs and search terms, and review the generated curl commands before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tjefferson/skills-stats) <br>
- [ClawHub Skill API Endpoint](https://clawhub.ai/api/skill?slug={slug}) <br>
- [ClawHub Search API Endpoint](https://clawhub.ai/api/search?q=SEARCH_TERM) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, guidance] <br>
**Output Format:** [Markdown with bash commands and inline Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3; queries public ClawHub endpoints without credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
