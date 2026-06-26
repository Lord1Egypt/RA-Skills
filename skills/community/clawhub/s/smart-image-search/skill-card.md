## Description: <br>
Searches multiple public image engines from a text query and returns the best matching image, candidate results, source pages, or ready-to-open search links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mumu-0922](https://clawhub.ai/user/mumu-0922) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find images, reference images, logos, avatars, wallpapers, memes, or official visual assets and to receive either a downloaded best match or ranked candidate links when confidence is limited. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to public image search engines including Bing, Baidu, and Sogou. <br>
Mitigation: Avoid confidential, personal, medical, workplace, or proprietary queries unless that external exposure is acceptable. <br>
Risk: Selected images may be saved locally in a temporary search-image directory. <br>
Mitigation: Review downloaded files before reuse and remove local copies when they are no longer needed. <br>
Risk: Image search results can be low-confidence, mismatched, or noisy. <br>
Mitigation: Use the skill's confidence bands, entity-consistency checks, and candidate-link fallback instead of treating every best match as definitive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mumu-0922/smart-image-search) <br>
- [Query parameters](artifact/references/parameters.md) <br>
- [Intent routing](artifact/references/intent-routing.md) <br>
- [Relevance ranking](artifact/references/relevance.md) <br>
- [Confidence policy](artifact/references/confidence.md) <br>
- [Quality filtering](artifact/references/quality-filtering.md) <br>
- [Entity consistency](artifact/references/entity-consistency.md) <br>
- [Multi-entity hard gating](artifact/references/entity-gating.md) <br>
- [Official-source strengthening](artifact/references/official-sources.md) <br>
- [Official whitelist and directed search](artifact/references/official-whitelist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Code] <br>
**Output Format:** [Brief text or Markdown responses with image attachments, candidate URLs, search URLs, and JSON emitted by helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return one best image or multiple candidates; selected images may be saved locally in a temporary search-image directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
