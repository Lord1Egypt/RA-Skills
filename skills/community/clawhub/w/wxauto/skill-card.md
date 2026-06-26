## Description: <br>
wxauto helps agents operate WeChat through the wxautox4 RESTful API for sending messages, reading chat history, listening for new messages, and managing friends or groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cluic](https://clawhub.ai/user/cluic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to control an authorized local WeChat client, including sending messages, reading chat history, monitoring new messages, switching chats, and listing friends or groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private WeChat messages and perform WeChat actions through an authorized account. <br>
Mitigation: Use only with accounts and conversations the operator is authorized to access, and review actions before sending messages or reading chat history. <br>
Risk: The API token and base URL are configurable, and the default token is weak. <br>
Mitigation: Change the default token, keep the API bound to localhost or 127.0.0.1, and avoid remote base URLs unless the endpoint is fully trusted. <br>
Risk: The helper can automatically start a local wxauto-restful-api service from a discovered service directory. <br>
Mitigation: Inspect and trust the wxauto-restful-api directory before allowing automatic service startup. <br>


## Reference(s): <br>
- [ClawHub wxauto release page](https://clawhub.ai/cluic/wxauto) <br>
- [wxautox4 activation documentation](https://docs.wxauto.org/plus) <br>
- [wxauto-restful-api project referenced by the skill](https://github.com/cluic/wxauto-restful-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON API response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and a Windows wxautox4 setup with a local wxauto RESTful API service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
