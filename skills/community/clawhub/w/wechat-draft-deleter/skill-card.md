## Description: <br>
Deletes drafts from a WeChat Official Account draft box, including single draft deletion and batch deletion by Media ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bigkingcn](https://clawhub.ai/user/Bigkingcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and WeChat Official Account operators use this skill to remove test, obsolete, or batch-listed drafts by Media ID through the WeChat Official Account API. It is suited to controlled cleanup and automation workflows where draft deletion is intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs irreversible deletion of WeChat Official Account drafts. <br>
Mitigation: Verify every Media ID list before execution, keep confirmation enabled for routine use, and reserve --force for separately approved automation. <br>
Risk: The skill uses WeChat account credentials and the artifact includes unsafe credential-handling examples. <br>
Mitigation: Use only credentials for accounts where draft deletion is intended, keep AppSecret values out of scripts, logs, and source control, and replace examples with placeholders. <br>
Risk: Automated or batch deletion can remove more drafts than intended if the input file is stale or generated incorrectly. <br>
Mitigation: Review generated input files, run a dry approval step before deletion, and check result summaries after execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bigkingcn/wechat-draft-deleter) <br>
- [Publisher profile](https://clawhub.ai/user/Bigkingcn) <br>
- [WeChat draft delete API endpoint](https://api.weixin.qq.com/cgi-bin/draft/delete) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Text] <br>
**Output Format:** [Markdown with shell command examples and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat AppID and AppSecret credentials and Media IDs supplied by argument or file.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
