## Description: <br>
Generates structured restaurant review drafts from a shop link or address, food photos, store search results, and a fixed review format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ysredcity](https://clawhub.ai/user/ysredcity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to draft restaurant reviews for platforms such as Dianping and Amap after providing a store link or address and food photos. The skill is intended to combine visual observations, store information, and menu or review search results into a concise review draft. <br>

### Deployment Geography for Use: <br>
Global; most useful where the referenced restaurant, map, and review services are available. <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send shop or location context and photo-derived information to external services. <br>
Mitigation: Avoid private or sensitive photos and confirm that users are comfortable with external lookups before using the skill. <br>
Risk: Generated reviews can sound authentic while containing incorrect or unverified claims. <br>
Mitigation: Verify store details, dish names, and experience claims before posting, and consider disclosing AI assistance. <br>
Risk: The artifact includes an embedded Amap API key and a TLS fallback noted by security guidance. <br>
Mitigation: Prefer user-provided configuration, validate network destinations, and remove unverified TLS fallback behavior before production deployment. <br>
Risk: HEIC conversion can create derivative image files that may retain sensitive photo content. <br>
Mitigation: Document where converted files are written and delete derived images when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ysredcity/shop-review-generator) <br>
- [Review format specification](references/review-format-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review draft with optional shell command guidance for HEIC conversion or Amap POI lookup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be manually checked for factual accuracy, privacy, and platform disclosure expectations before publication.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
