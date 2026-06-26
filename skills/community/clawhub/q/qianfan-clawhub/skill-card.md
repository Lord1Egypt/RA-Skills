## Description: <br>
Search and install Baidu Qianfan ecosystem skills with fuzzy matching across slug, name, and description fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiduQianfanGroup](https://clawhub.ai/user/baiduQianfanGroup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to search the Baidu Qianfan skills marketplace, identify skills by slug, name, or description, and install selected skills into a local or custom workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports that install paths and ZIP extraction are not safely constrained enough for automatic trust. <br>
Mitigation: Install only trusted Baidu Qianfan skills, review downloaded content before use, and avoid sensitive workspaces until ZIP path validation and stricter install-directory containment are added. <br>
Risk: Using --force or a custom/shared workdir can overwrite or place files in a destination that has not been reviewed. <br>
Mitigation: Avoid --force and custom or shared workdirs unless the destination and downloaded skill contents have been reviewed. <br>
Risk: The skill depends on authenticated access to the Baidu Qianfan endpoint through BAIDU_API_KEY. <br>
Mitigation: Use a scoped key where possible and avoid exposing the key in logs, shared shells, or committed configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baiduQianfanGroup/qianfan-clawhub) <br>
- [Publisher profile](https://clawhub.ai/user/baiduQianfanGroup) <br>
- [Baidu AppBuilder endpoint](https://appbuilder.baidu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requires BAIDU_API_KEY and returns marketplace skill slugs and names; install writes downloaded skill files to the configured skills directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
