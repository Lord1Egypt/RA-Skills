## Description: <br>
Provides a patient-facing general health education entry point that matches user topics and keywords against article content and generates concise educational summaries with source references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care-support teams use this skill to find patient-facing health education content from provided article lists by topic or keyword. It returns matched articles, short Markdown explanations, source URLs when available, and a reminder that education content does not replace clinical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health topics, keywords, and matched article content can be sent to the documented remote medical-model API. <br>
Mitigation: Use only approved app keys and avoid submitting private medical records or PHI unless that remote service is approved for the intended use. <br>
Risk: Office, PDF, and image inputs may invoke local parsers, converters, or OCR tools on user-selected files. <br>
Mitigation: Prefer JSON or trusted files; process untrusted documents only in a patched, sandboxed environment. <br>
Risk: Generated health education summaries could be mistaken for clinical diagnosis or individualized treatment advice. <br>
Mitigation: Keep the documented disclaimer and review outputs for medical appropriateness before user-facing deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-health-education) <br>
- [Referenced WellAlly health knowledge-base skill](https://agent-skills.md/skills/huifer/WellAlly-health/wellally-tech) <br>
- [Configured medical-model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [UTF-8 JSON containing structured matched-article data and Markdown natural-language health education text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an app key for the remote medical-model API; supports JSON, text, table, document, PDF, and image inputs through preprocessing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
