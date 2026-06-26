## Description: <br>
Create, schedule, list, edit, and delete drafts on Typefully, including single tweets, threads, and multi-platform posts for X, LinkedIn, Threads, Bluesky, and Mastodon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chapati23](https://clawhub.ai/user/chapati23) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and social media operators use this skill to manage Typefully drafts from an agent workflow, including creating, editing, scheduling, publishing, listing, and deleting draft posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Typefully API key and can access or change drafts in the connected account. <br>
Mitigation: Install only when the publisher is trusted, prefer a scoped Typefully key if available, and store the key through the documented environment variable or password store path. <br>
Risk: Scheduling or publishing actions may send content at the wrong time or immediately when requested. <br>
Mitigation: Review draft content, target platforms, social set, and publish time before allowing schedule or publish commands. <br>


## Reference(s): <br>
- [Typefully](https://typefully.com) <br>
- [Typefully Skill on ClawHub](https://clawhub.ai/chapati23/typefully-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/chapati23) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples; Typefully API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TYPEFULLY_API_KEY and can use TYPEFULLY_SOCIAL_SET_ID when multiple social sets exist.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter declares 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
