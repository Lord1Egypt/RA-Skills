## Description: <br>
Manage Tencent Weiyun files with free-version workflows for directory browsing, batch download, and two-phase upload through MCP tooling and local hashing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and automation agents use this skill to browse Tencent Weiyun directories, obtain download links, and upload local files with required token and path checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local files and upload or download Weiyun data using user credentials. <br>
Mitigation: Confirm exact local file paths before transfer and avoid wildcard-driven file operations. <br>
Risk: WEIYUN_MCP_TOKEN and download cookies can grant access to cloud files. <br>
Mitigation: Keep credentials out of logs and skill files, use environment variables, and regenerate tokens if exposed. <br>
Risk: Broad routing text may cause the skill to activate for unrelated analytics or reporting tasks. <br>
Mitigation: Use the skill only for Weiyun file browsing, downloads, and uploads; route unrelated analytics or reporting tasks elsewhere. <br>
Risk: Arbitrary or unverified MCP server URLs could redirect file data or credentials. <br>
Mitigation: Use only verified Weiyun or QQ endpoints and independently confirm any custom MCP server URL before use. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/thcjp/skills/weiyun-toolkit-free) <br>
- [Tencent Weiyun](https://www.weiyun.com) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline command examples and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, Weiyun file identifiers, pdir_key values, cookies, download URLs, token environment variables, and upload parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
