## Description: <br>
Summarize documents in EN/CN/BM/ID with cross-language support. Optimized for Southeast Asian languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wms2537](https://clawhub.ai/user/wms2537) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to summarize English, Chinese, Bahasa Malaysia, and Bahasa Indonesia documents, optionally translating summaries across those languages. It also extracts key points, action items, named entities, source language, and word counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill charges a paid billing endpoint before use. <br>
Mitigation: Confirm the charge and payment terms before invoking the skill. <br>
Risk: The billing check sends the user's identifier to the disclosed SkillPay/Cloudflare endpoint. <br>
Mitigation: Use only when sharing that user identifier with the billing endpoint is acceptable. <br>
Risk: Summaries and translations may omit nuance or misclassify multilingual content. <br>
Mitigation: Review generated summaries, entities, and action items against the source document before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wms2537/sea-doc-summarizer) <br>
- [SEA document summarizer billing endpoint](https://sea-doc-summarizer.swmengappdev.workers.dev/charge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, API calls, guidance] <br>
**Output Format:** [JSON summary object with summary text, key points, entities, source language, and word counts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports brief, detailed, and action-items summary styles; may translate summaries when the target language differs from the source language.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
