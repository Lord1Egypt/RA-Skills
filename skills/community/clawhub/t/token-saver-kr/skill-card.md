## Description: <br>
한국어 Context DB로 AI 토큰 사용량을 줄이도록 프롬프트 저장, 메모리 검색, 사용량 확인을 지원합니다. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorongss](https://clawhub.ai/user/dorongss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Korean-language AI users can use this skill to save reusable context, search memory at different detail levels, and reduce repeated prompt context. It is intended for workflows that connect to the TokenSaver remote API with a user-provided API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved and searched context is sent to a third-party remote memory service. <br>
Mitigation: Avoid storing secrets, regulated data, or private business context unless the provider's retention and deletion practices meet the user's requirements. <br>
Risk: The skill requires an API key for the TokenSaver service. <br>
Mitigation: Use a dedicated API key, keep it in TOKENSAVER_API_KEY or another protected secret store, and verify the package and provider before installation. <br>


## Reference(s): <br>
- [TokenSaver service](https://tokensaver.ai) <br>
- [TokenSaver API endpoint](https://api.tokensaver.ai) <br>
- [ClawHub skill page](https://clawhub.ai/dorongss/token-saver-kr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples, plus JSON-like API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TokenSaver API key via constructor argument or TOKENSAVER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: openclaw.skill.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
