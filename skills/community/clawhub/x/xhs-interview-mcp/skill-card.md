## Description: <br>
操作小红书（搜索笔记、获取面经、查看热门内容）。当用户想搜索小红书面经、查找面试经验、了解某公司/岗位的面试情况时使用。基于本地 MCP 服务（localhost:18060）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krisdontknowcoding](https://clawhub.ai/user/krisdontknowcoding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help users search Xiaohongshu for interview experience posts, retrieve note details, review popular content, and summarize useful interview signals from returned results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run an external Xiaohongshu MCP binary and connect it to a local MCP endpoint. <br>
Mitigation: Install only from a trusted source, keep the localhost endpoint private, and stop the background process when finished. <br>
Risk: The workflow depends on Xiaohongshu session cookies stored in cookies.json. <br>
Mitigation: Protect or delete cookies.json after use and avoid sharing the file or logs that may expose session data. <br>
Risk: The artifact describes account-changing actions such as like, favorite, and comment. <br>
Mitigation: Require explicit user confirmation before any action that modifies a Xiaohongshu account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krisdontknowcoding/xhs-interview-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, API Calls] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local MCP setup steps, mcporter command examples, search guidance, and result interpretation notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
