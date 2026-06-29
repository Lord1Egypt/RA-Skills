## Description: <br>
Typecho Publisher helps an agent create, query, update, delete, and publish Markdown posts to a configured Typecho blog through the bundled typecho-cli tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolingrabbit](https://clawhub.ai/user/coolingrabbit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blog operators use this skill to let an agent manage a Typecho-based knowledge blog, including publishing new technical notes, reviewing existing posts, and updating or deleting posts by cid. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording and direct publish or delete authority can cause accidental public blog changes. <br>
Mitigation: Use explicit user requests for publish, update, and delete actions, and confirm the target blog, post title, status, and exact cid before executing write operations. <br>
Risk: Full-text updates can overwrite existing post content if only a partial edit is submitted. <br>
Mitigation: Fetch the current post with typecho-cli get and submit the complete revised Markdown body when updating. <br>
Risk: The blog API token grants write access to the configured Typecho site. <br>
Mitigation: Store the token outside public content, keep it limited and rotated, and never include it in published Markdown. <br>


## Reference(s): <br>
- [Typecho Documentation](https://typecho.org/docs/) <br>
- [OpenClawTypecho Plugin Repository](https://github.com/CoolingRabbit/OpenClawTypecho) <br>
- [OpenClawTypecho Releases](https://github.com/CoolingRabbit/OpenClawTypecho/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content, shell commands, configuration snippets, and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can trigger create, update, publish, query, and delete operations against a configured Typecho blog.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter, plugin.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
