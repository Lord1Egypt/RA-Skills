## Description: <br>
Post to social media via VibePost API when publishing Twitter/X updates, sharing announcements, or posting other social content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JPaulGrayson](https://clawhub.ai/user/JPaulGrayson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and users use this skill to send approved short-form social media text to a configured posting service, primarily for Twitter/X updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user-provided text to an external VibePost/Replit endpoint where it may be published publicly. <br>
Mitigation: Preview the exact post text and target platform before running the posting command. <br>
Risk: The artifact includes a reusable posting API key. <br>
Mitigation: Remove and rotate the embedded key, then use a private secret or environment variable for authentication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JPaulGrayson/social-poster) <br>
- [VibePost posting endpoint](https://vibepost-jpaulgrayson.replit.app/api/quack/post) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Posts include text and an optional platform value, defaulting to twitter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
