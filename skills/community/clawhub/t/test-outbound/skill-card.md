## Description: <br>
登录外呼系统并调用 save_session.py 保存浏览器会话到 auth.json。用于首次登录、会话失效或开始任务前重新准备登录态。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RingoRangers](https://clawhub.ai/user/RingoRangers) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users use this skill to prepare or refresh a reusable browser login state for an outbound call workbench before running downstream outbound workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles plaintext login credentials and creates auth.json, which may be equivalent to an active logged-in session. <br>
Mitigation: Inspect the referenced save_session.py and target URL before use, restrict permissions on login_credentials.json and auth.json, keep both out of source control, and delete or rotate them when no longer needed. <br>


## Reference(s): <br>
- [Session Contract](references/session-contract.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/RingoRangers/test-outbound) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and a Playwright auth.json session file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces auth.json for downstream browser-session reuse; treat login_credentials.json and auth.json as secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
