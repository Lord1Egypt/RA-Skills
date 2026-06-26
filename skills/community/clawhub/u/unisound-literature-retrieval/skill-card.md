## Description: <br>
Helps clinician-facing research workflows restructure clinical questions into PICO, summarize user-provided literature snippets, and suggest next searches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians and clinical research staff use this skill to turn a clinical or research question plus optional pasted abstracts into a PICO-aligned evidence narrative and follow-up search plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical questions and pasted literature excerpts are sent to the disclosed Hivoice medical model endpoint. <br>
Mitigation: Use only with organizational approval, treat the app key as a credential, and avoid sending patient identifiers, regulated health information, or confidential research text. <br>
Risk: The skill produces draft evidence narratives and search suggestions rather than a real-time database search or systematic review. <br>
Mitigation: Verify claims against source literature and distinguish unanchored search strategy advice from evidence grounded in supplied passages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/unisound-literature-retrieval) <br>
- [Disclosed Hivoice medical model endpoint](https://maas-api.hivoice.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON object containing status metadata and Markdown narrative text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an app key and accepts a clinical question, optional literature passages, and optional constraints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
