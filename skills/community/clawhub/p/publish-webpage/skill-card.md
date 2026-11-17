## Description:

Helps an agent turn a non-technical user's idea into a live one-page website by writing, packaging, deploying to goclawgo, and returning a shareable URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerkn](https://clawhub.ai/user/nerkn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their assisting agents use this skill to publish simple webpages, landing pages, portfolios, and one-page sites without asking the user to handle code or hosting. The skill guides the agent through collecting the idea and deployment URL, creating an HTML page, deploying it, and returning the live result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill publishes user-provided content to the public internet.

Mitigation: Use it only for material intended to be public, and confirm the user understands that the deployed page may be shareable online.

Risk: The goclawgo Agent URL functions like a reusable deployment credential.

Mitigation: Handle the URL as sensitive, avoid exposing it in shared logs or chat transcripts, and rotate the project key if it is exposed.

Risk: Deployment commands include user-provided URL, path, and deployment id values.

Mitigation: Validate the Agent URL, local archive path, and deployment id before running shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerkn/skills/publish-webpage)
- [goclawgo](https://goclawgo.com)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an index.html file and deployment tarball, then return a live URL when deployment succeeds.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
