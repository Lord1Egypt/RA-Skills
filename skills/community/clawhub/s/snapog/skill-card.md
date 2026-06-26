## Description: <br>
Generate social images and OG cards from professional templates via the SnapOG API. One API call = one pixel-perfect PNG. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beameasy](https://clawhub.ai/user/beameasy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketers, and content teams use SnapOG to generate social images, OG cards, and marketing visuals from templates through the SnapOG API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends generation text, titles, tags, image or logo URLs, and template parameters to the SnapOG API. <br>
Mitigation: Avoid sending secrets, sensitive internal content, or private asset URLs in generation requests. <br>
Risk: Generation requests require access to a SnapOG API key. <br>
Mitigation: Store SNAPOG_API_KEY in the agent environment only when needed, limit who can access it, and monitor account usage for quota or billing impact. <br>
Risk: Webhook URLs can send generation results or request context to an external destination. <br>
Mitigation: Use webhook URLs only when you control or trust the destination. <br>


## Reference(s): <br>
- [SnapOG homepage](https://snapog.dev) <br>
- [SnapOG API documentation endpoint](https://api.snapog.dev/v1/docs) <br>
- [ClawHub SnapOG listing](https://clawhub.ai/beameasy/snapog) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance, Files] <br>
**Output Format:** [Markdown with API examples and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SNAPOG_API_KEY for generation requests; preview and template listing endpoints work without authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
