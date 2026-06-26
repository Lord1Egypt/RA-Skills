## Description: <br>
Generate, schedule, and publish posts to X, LinkedIn, and Threads in your voice using AI, with tools for preferences and billing status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmoon90](https://clawhub.ai/user/jmoon90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to draft, manage, schedule, and publish social posts across connected X, LinkedIn, and Threads accounts. It also supports media upload, style preferences, billing checks, and account discovery for post workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or schedule live posts and upload media to external social accounts. <br>
Mitigation: Review generated content before publishing, prefer drafts or scheduling for important posts, and confirm the target social account before live actions. <br>
Risk: The skill requires an XREPLY_TOKEN credential for connected XreplyAI account access. <br>
Mitigation: Keep the token private, store it only in the intended agent configuration, and refresh it if authentication fails. <br>
Risk: Media upload actions send selected local image or video files outside the local environment. <br>
Mitigation: Double-check file paths, file types, and file sizes before upload. <br>


## Reference(s): <br>
- [XreplyAI homepage](https://xreplyai.com) <br>
- [ClawHub skill page](https://clawhub.ai/jmoon90/xreplyai) <br>
- [Publisher profile](https://clawhub.ai/user/jmoon90) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XREPLY_TOKEN credential and mcporter or npx to call the XreplyAI MCP server.] <br>

## Skill Version(s): <br>
0.3.20 (source: server release metadata; artifact frontmatter reports 0.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
