## Description: <br>
4-stage content pipeline orchestrator: Research -> Ideate -> Write -> Queue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runesleo](https://clawhub.ai/user/runesleo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators and content teams use this skill to turn a topic or URL into researched, review-ready content drafts and maintain a local queue for review, approval, adaptation, publishing, and archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update local queue and research files. <br>
Mitigation: Use it only in workspaces where content-queue.json and research/ file changes are expected, and review generated drafts before publishing. <br>
Risk: The URL workflow may retrieve and process links supplied by the user. <br>
Mitigation: Avoid private intranet, authenticated, or sensitive URLs unless you explicitly want that content processed. <br>


## Reference(s): <br>
- [Content Pipeline skill page](https://clawhub.ai/runesleo/runesleo-content-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, guidance] <br>
**Output Format:** [Markdown responses, JSON queue entries, and local research markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update content-queue.json and dated files under research/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
