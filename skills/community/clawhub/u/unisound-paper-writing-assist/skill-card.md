## Description: <br>
A clinical research paper-writing assistant that expands author-provided notes into IMRaD-style Chinese or English manuscript draft sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical researchers and manuscript authors use this skill to turn supplied section notes into draft abstract, introduction, methods, results, discussion, or related manuscript text. It also provides writing self-check reminders for reporting-guideline awareness without certifying compliance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied manuscript notes are sent to the disclosed external Hivoice model API. <br>
Mitigation: Install only when that data flow is approved, use a dedicated revocable API key, and avoid patient identifiers or confidential clinical details unless permitted by organizational policy. <br>
Risk: Generated manuscript text may contain unsupported scientific claims if users provide incomplete or incorrect notes. <br>
Mitigation: Require authors to review, edit, and verify all draft text, statistics, conclusions, and reporting-guideline reminders before submission or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-paper-writing-assist) <br>
- [Publisher profile](https://clawhub.ai/user/unisound-llm) <br>
- [Hivoice model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [JSON containing metadata and Markdown draft text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an input JSON object with section and notes, plus an app key for the external model API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
