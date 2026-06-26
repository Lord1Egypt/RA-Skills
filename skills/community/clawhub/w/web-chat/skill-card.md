## Description: <br>
Use when the user wants to interact with Google Gemini or ChatGPT via browser automation; it sends the user's query to the selected chatbot and returns the response verbatim. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljie-PI](https://clawhub.ai/user/ljie-PI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to route prompts to Gemini or ChatGPT from an agent workflow and receive the chatbot response, including citation links when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent logged-in Chrome profile can be controlled through a local debugging port. <br>
Mitigation: Use a dedicated account and Chrome profile, avoid sending secrets or private data, close Chrome when finished, and delete the profile when stored sessions are no longer wanted. <br>
Risk: Chatbot site changes or login state can prevent the browser automation from finding inputs or returning complete responses. <br>
Mitigation: Confirm login manually when prompted, retry with a longer timeout for slow responses, and update selectors before relying on the skill after site UI changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ljie-PI/web-chat) <br>
- [Google Gemini](https://gemini.google.com) <br>
- [ChatGPT](https://chatgpt.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON from the selected chatbot automation script, with citation links when found.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is designed to return chatbot responses verbatim; operational status and error details may be emitted separately.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
