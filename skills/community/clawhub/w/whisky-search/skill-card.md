## Description: <br>
Searches WhiskySpace for whisky bottles, brands, distilleries, prices, ratings, regions, cask types, recommendations, and WhiskySpace page links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengci](https://clawhub.ai/user/fengci) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer whisky search, comparison, recommendation, detail lookup, and WhiskySpace URL questions using WhiskySpace API responses as the source of truth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Whisky-related searches and URL lookups can be sent to WhiskySpace's public API. <br>
Mitigation: Avoid private information in search terms and use explicit whisky-related wording when invoking the skill. <br>
Risk: Prices, ratings, and review counts may be stale, sparse, or absent in API responses. <br>
Mitigation: Show recorded dates and review counts when available, and state clearly when a field is not provided. <br>
Risk: Incorrect route construction could misidentify WhiskySpace pages or confuse them with official brand websites. <br>
Mitigation: Use only API-returned identifiers and the declared canonical WhiskySpace routes; use the API website field only for official websites. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fengci/whisky-search) <br>
- [WhiskySpace search API](https://www.whiskyspace.com/api/search) <br>
- [WhiskySpace whisky details API](https://www.whiskyspace.com/api/whiskies/{slug_or_id}) <br>
- [WhiskySpace brand API](https://www.whiskyspace.com/api/brands/{identifier}) <br>
- [WhiskySpace search filters API](https://www.whiskyspace.com/api/search/filters) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown or plain text answers with WhiskySpace URLs and optional curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses API-returned fields, states when requested data is unavailable, and keeps link-only answers minimal.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
