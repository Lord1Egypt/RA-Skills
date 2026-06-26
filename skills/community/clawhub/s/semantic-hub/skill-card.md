## Description: <br>
Semantic Hub lets AI agents collaborate with human teams on shared project boards by listing boards, creating and updating tasks, adding comments, uploading and attaching files, filtering work items, and viewing activity history with a scoped API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simplysemantics](https://clawhub.ai/user/simplysemantics) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External teams, project managers, developers, and AI agents use this skill to coordinate work on Semantic Hub boards by creating and updating cards, adding comments, attaching files or URLs, filtering work items, and reviewing board activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and update shared board data, post comments, upload files, attach URLs, and view member emails on authorized boards. <br>
Mitigation: Use a scoped Semantic Hub API key limited to required boards, rotate or revoke it when access changes, and require review before important board changes or uploads. <br>
Risk: Security review notes that the privacy disclosures understate that uploaded file contents and member email data can be handled by Semantic Hub. <br>
Mitigation: Treat uploaded files, card text, comments, assignees, member emails, and attachment metadata as data shared with Semantic Hub. <br>


## Reference(s): <br>
- [Semantic Hub homepage](https://www.simplysemantics.com/semantic-hub.html) <br>
- [ClawHub listing](https://clawhub.ai/simplysemantics/semantic-hub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown summaries with REST API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEMANTIC_HUB_API_KEY scoped to authorized Semantic Hub boards.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and CHANGELOG, released 2026-03-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
