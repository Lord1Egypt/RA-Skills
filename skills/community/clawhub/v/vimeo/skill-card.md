## Description: <br>
Vimeo provides API guidance for using Maton-managed OAuth to upload, manage, organize, and interact with Vimeo videos, folders, albums, showcases, and community features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work with Vimeo accounts through Maton's managed OAuth proxy. It supports account lookup, video management, folders, showcases, comments, likes, watch-later lists, followers, channels, and categories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Maton to broker OAuth access to the user's Vimeo account and uses a sensitive MATON_API_KEY. <br>
Mitigation: Install only if Maton is trusted for this access path and keep MATON_API_KEY private. <br>
Risk: Write operations can upload, edit, delete, comment, like, follow, or otherwise change Vimeo account content. <br>
Mitigation: Confirm the exact Vimeo account, target resource, and intended effect before approving any create, update, or delete operation. <br>
Risk: Unused Maton or Vimeo connections may retain account access longer than needed. <br>
Mitigation: Revoke unused Maton and Vimeo connections when they are no longer required. <br>


## Reference(s): <br>
- [Maton Homepage](https://maton.ai) <br>
- [Vimeo API Reference](https://developer.vimeo.com/api/reference) <br>
- [Vimeo Developer Portal](https://developer.vimeo.com) <br>
- [Vimeo API Authentication](https://developer.vimeo.com/api/authentication) <br>
- [Vimeo Upload API](https://developer.vimeo.com/api/upload/videos) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with API endpoint descriptions and inline bash, Python, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a MATON_API_KEY, and an authorized Vimeo connection] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
