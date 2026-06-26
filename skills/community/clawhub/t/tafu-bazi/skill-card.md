## Description: <br>
Use Tafu's paid API for deterministic BaZi chart calculation, thematic readings, synastry, and soul-song generation when users ask for Chinese astrology analysis based on birth data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhihao93li](https://clawhub.ai/user/zhihao93li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call Tafu's paid API for BaZi chart calculation, thematic Chinese astrology readings, compatibility analysis, and soul-song generation from user-provided birth data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth date, birth time, gender, and city-level location may be sent to Tafu's external paid service. <br>
Mitigation: Collect only the fields needed for the requested reading, avoid submitting another person's data without consent, and tell users when paid external processing is involved. <br>
Risk: TAFU_API_BASE_URL can redirect API requests, including the authorization header and birth data, to a configured endpoint. <br>
Mitigation: Set TAFU_API_BASE_URL only to a trusted endpoint and otherwise use the documented default Tafu API base URL. <br>
Risk: Example workflows use temporary JSON payload files that can contain real birth data. <br>
Mitigation: Use temporary files only when needed for complex payloads and remove files containing real user data after the API call. <br>
Risk: Paid reading, soul-song, and synastry endpoints can consume credits. <br>
Mitigation: Call paid endpoints only after the user clearly asks for that capability and surface creditsUsed or creditsRemaining when the API returns them. <br>


## Reference(s): <br>
- [Tafu developer portal](https://tafu.me/developers) <br>
- [Tafu API examples](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhihao93li/tafu-bazi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summaries with preserved JSON/API response details and shell command invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAFU_API_KEY; may include creditsUsed, creditsRemaining, viewUrl, or taskId when returned by the API.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
