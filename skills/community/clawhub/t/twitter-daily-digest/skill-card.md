## Description: <br>
Fetches recent Twitter/X posts from followed or specified accounts, saves objective tweet facts, and supports agent-authored Chinese daily digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceylonlatte](https://clawhub.ai/user/ceylonlatte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to gather recent Twitter/X activity from followed or specified accounts, then create a readable Chinese digest with links, metrics, and failure awareness. It also supports saving the final Markdown locally and optionally syncing that existing Markdown to Notion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an authenticated Twitter/X CLI to fetch followed accounts and recent posts, which can expose account activity and leave digest data on disk. <br>
Mitigation: Run it only with an account the user intends to use for this purpose, choose output paths deliberately, and review or remove generated digest files according to local retention needs. <br>
Risk: Optional Notion sync can create pages using local Notion credentials and a default parent page destination. <br>
Mitigation: Verify or override the Notion parent page, use a limited Notion integration token, and require an explicit user action before any Notion write. <br>
Risk: Twitter/X fetches can be partially successful when individual accounts fail. <br>
Mitigation: Check failed account information in the JSON facts, disclose partial results in the digest when relevant, and retry failed accounts before treating the digest as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ceylonlatte/twitter-daily-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON fact files, Chinese text or Markdown digest content, and shell-command workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May leave digest files on disk and can optionally write Markdown content to a configured Notion parent page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
