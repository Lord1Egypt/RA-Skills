## Description: <br>
Generates Xiaohongshu-style social media cover images from prompts, and helps users check xhscover credit balance or generation history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwchris](https://clawhub.ai/user/xwchris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to generate Xiaohongshu-style covers or social media artwork from short prompts, and to inspect their xhscover balance or generation history through the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cover prompts and the local xhscover API key are sent to xhscover.cn for processing. <br>
Mitigation: Use only non-confidential prompt text, confirm that xhscover.cn is trusted for the use case, and avoid sharing sensitive account data. <br>
Risk: The skill executes the external xhscover npm CLI through npx, which introduces package supply-chain exposure. <br>
Mitigation: Review the npm package and CLI source before deployment, and use pinned or approved package versions where organizational policy requires it. <br>


## Reference(s): <br>
- [XHSCover website](https://xhscover.cn) <br>
- [xhscover npm package](https://www.npmjs.com/package/xhscover) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated image files from the xhscover CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer and uses the xhscover CLI for setup, generation, balance, and history commands.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
