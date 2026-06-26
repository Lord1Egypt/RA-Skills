## Description: <br>
Sends WeChat text messages to selected friends after querying contacts and confirming the recipient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aw11100](https://clawhub.ai/user/aw11100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who operate the configured WeChat messaging API can use this skill to look up a friend by name, disambiguate matches, and send a confirmed text message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contact lookups and message contents are sent through a fixed private API whose operator and sending account are not explained. <br>
Mitigation: Install and use the skill only if you operate or explicitly trust the configured API and know which WeChat account it controls. <br>
Risk: A message could be sent to the wrong WeChat contact if a name lookup returns an unexpected or ambiguous recipient. <br>
Mitigation: Before confirming a send, verify the selected recipient, wxId, sender account, and exact message text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aw11100/wechatmessaging) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Plain text prompts and API request parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before sending; contact lookup and message delivery use the configured WeChat API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
