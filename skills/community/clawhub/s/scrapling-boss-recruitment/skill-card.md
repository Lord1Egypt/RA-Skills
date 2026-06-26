## Description: <br>
Helps agents use Scrapling-based tools to search Boss Zhipin candidates, retrieve resumes, send batch greetings, and parse structured recruiting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuritu](https://clawhub.ai/user/wuritu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, recruiting operations teams, and developers use this skill to automate Boss Zhipin candidate search, resume retrieval, outreach preparation, and resume parsing from an authorized account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires live Boss Zhipin account cookies and may expose sensitive session credentials if they are pasted into chats, logs, or shared files. <br>
Mitigation: Use only accounts you control, keep cookies and proxy credentials in local environment variables or secret storage, and avoid sharing credentials in agent conversations or committed files. <br>
Risk: Candidate resumes and contact details are personal data, and the skill can collect or process that data at scale. <br>
Mitigation: Run the skill only with authorization and applicable legal or privacy review; keep daily limits, random delays, and human review in place before collecting resumes or sending outreach. <br>
Risk: Optional LLM resume parsing can send candidate data to an external model provider. <br>
Mitigation: Disable external LLM parsing unless candidates and the organization have approved that data flow, or use an approved private model endpoint with appropriate data handling controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wuritu/scrapling-boss-recruitment) <br>
- [Boss Zhipin crawler configuration guide](references/config.md) <br>
- [Boss Zhipin CSS selector reference](references/selectors.md) <br>
- [Boss Zhipin](https://www.zhipin.com) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; runtime helpers can return Python objects and JSON-formatted resume data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Boss Zhipin session cookies; optional proxy settings and optional external LLM parsing may be configured by the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
