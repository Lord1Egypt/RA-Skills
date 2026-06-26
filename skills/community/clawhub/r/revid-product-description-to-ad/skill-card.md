## Description: <br>
Turn a product description (free-form text -- no URL needed) into a punchy 15-30 second AI-generated ad with hooks, CTA, and visuals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn pasted product descriptions, spec sheets, feature lists, and optional product images into short-form Revid ad video workflows with hook, benefit, and CTA structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product descriptions, product images, brand notes, and generated creative requests are sent to Revid for video generation. <br>
Mitigation: Avoid confidential product plans, unreleased creative assets, or regulated data unless Revid processing is acceptable and allowed by the API account terms. <br>
Risk: The workflow requires a sensitive Revid API key. <br>
Mitigation: Provide REVID_API_KEY through secure local configuration and avoid pasting it into prompts, logs, shared files, or generated examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/api00/revid-product-description-to-ad) <br>
- [Revid render API endpoint](https://www.revid.ai/api/public/v3/render) <br>
- [Revid status API endpoint](https://www.revid.ai/api/public/v3/status?pid=$PID) <br>
- [Example ad payload](examples/aeropods-ad.json) <br>
- [Example polling script](examples/run.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with JSON payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVID_API_KEY; generated media is returned as a Revid video URL after status polling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
