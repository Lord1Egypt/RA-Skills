## Description: <br>
Search YouTube and retrieve video metadata. Use for finding videos, checking view counts, channel info, or AI training suitability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scavio-ai](https://clawhub.ai/user/scavio-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search YouTube, retrieve structured video metadata, and check whether videos have transcript or license signals relevant to AI training workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube search terms and video IDs to Scavio APIs. <br>
Mitigation: Use it only when sharing those queries and identifiers with Scavio is acceptable for the workflow. <br>
Risk: The skill requires a Scavio API key stored in the agent environment. <br>
Mitigation: Store SCAVIO_API_KEY in a managed secret or environment variable and avoid committing it to files or prompts. <br>
Risk: Optional LangChain integration adds an extra package dependency. <br>
Mitigation: Install langchain-scavio only when that integration is needed. <br>


## Reference(s): <br>
- [Scavio Documentation](https://scavio.dev/docs) <br>
- [Scavio Youtube ClawHub Listing](https://clawhub.ai/scavio-ai/scavio-youtube) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with API examples, shell commands, and structured JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; configured timeout is 90 seconds and throttle is 1 request per second.] <br>

## Skill Version(s): <br>
2.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
