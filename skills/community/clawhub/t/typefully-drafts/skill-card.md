## Description: <br>
Create, schedule, list, edit, and delete Typefully drafts, including single posts, threads, and multi-platform posts for X, LinkedIn, Threads, Bluesky, and Mastodon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chapati23](https://clawhub.ai/user/chapati23) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and social media operators use this skill to have an agent manage Typefully drafts through the Typefully API for drafting, editing, scheduling, listing, or deleting posts and threads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete drafts or publish immediately when those actions are invoked. <br>
Mitigation: Before delete or publish actions, have the agent show the draft ID, content, platform list, and scheduled time; avoid immediate publishing unless explicitly requested. <br>
Risk: The skill requires a Typefully API key that can manage drafts. <br>
Mitigation: Install only when comfortable granting draft-management access, and provide the key through the documented environment variable or password-store mechanism. <br>


## Reference(s): <br>
- [ClawHub Typefully Skill Page](https://clawhub.ai/chapati23/typefully-drafts) <br>
- [Typefully](https://typefully.com) <br>
- [Typefully API v2 Endpoint](https://api.typefully.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [JSON responses with Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TYPEFULLY_API_KEY and optionally TYPEFULLY_SOCIAL_SET_ID; operations can create, edit, schedule, publish, or delete Typefully drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
