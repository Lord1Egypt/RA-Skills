## Description:

Lets an agent send user-provided prompts to Google Gemini or ChatGPT through Playwright browser automation and return the chatbot response verbatim.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljie-pi](https://clawhub.ai/user/ljie-pi)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill when they want an assistant to ask Gemini or ChatGPT from a logged-in Chrome profile and return the response and citation links without rewriting the answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Gemini or ChatGPT through a logged-in Chrome profile, so sensitive or regulated data may leave the local environment.

Mitigation: Use a dedicated account or browser profile and avoid submitting secrets, credentials, or regulated data.

Risk: The skill depends on Chrome remote debugging through a local CDP port and persistent browser state.

Mitigation: Keep the CDP port local, close the browser profile when finished, and do not expose the debugging port to untrusted networks.

Risk: The browser automation depends on third-party web UI selectors that may change.

Mitigation: Treat connection, login, input-field, and timeout errors as operational failures and update selectors before relying on affected responses.

Risk: The dependency requirement allows Playwright versions newer than 1.40.0.

Mitigation: Pin and review Playwright versions before rebuilding the virtual environment for controlled deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ljie-pi/skills/web-chat)
- [Google Gemini](https://gemini.google.com)
- [ChatGPT](https://chatgpt.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON containing chatbot response text, citation links, success status, and errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, Playwright, and a locally running Chrome instance with CDP on the configured port.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
