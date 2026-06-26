## Description: <br>
Generates Xiaohongshu-style social media cover images with npx xhscover, including setup, balance, and history workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwchris](https://clawhub.ai/user/xwchris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate social media cover images from prompts, choose aspect ratios, check credit balance, and review generation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the external xhscover npm package and xhscover.cn service. <br>
Mitigation: Install only if you trust the package and service, and review the package before use in sensitive environments. <br>
Risk: Cover prompts and API keys are sent to api.xhscover.cn. <br>
Mitigation: Avoid sensitive personal or business information in prompts, monitor credit usage, and remove or rotate the ~/.xhscover API key when no longer using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xwchris/xhs-cover) <br>
- [xhscover website](https://xhscover.cn) <br>
- [xhscover npm package](https://www.npmjs.com/package/xhscover) <br>
- [xhscover CLI repository](https://github.com/xwchris/xhscover-cli) <br>
- [xhs-cover MCP repository](https://github.com/xwchris/xhs-cover-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated image file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses npx xhscover; prompts and API keys are sent to api.xhscover.cn during execution.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
