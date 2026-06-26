## Description: <br>
Generate SEO-optimized title, SEO title, SEO description, SEO slug, and social tips for a blog post, using researched SEO best practices and current trends, and save the result as JSON in ~/blog-meta. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dishant0406](https://clawhub.ai/user/dishant0406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, marketers, and developers use this skill to generate search-focused metadata for a single local blog post. It reads the post from ~/blogs, researches public search and social signals, then writes a metadata JSON file for publication workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blog content or related search terms may be exposed to third-party public websites during SEO research. <br>
Mitigation: Use the skill on non-sensitive drafts or approve the research terms first; avoid unpublished material that should not leave the local environment. <br>
Risk: The skill writes a metadata JSON file under ~/blog-meta and could replace an existing file for the same slug. <br>
Mitigation: Ask the agent to confirm before overwriting an existing JSON file and review the saved metadata before publishing. <br>
Risk: Generated SEO metadata can be inaccurate, stale, or poorly matched to the post if research signals are misunderstood. <br>
Mitigation: Review the cited research sources and validate the title, description, slug, and social tips against the source blog before use. <br>


## Reference(s): <br>
- [Meta Research](references/meta-research.md) <br>
- [Meta Output](references/meta-output.md) <br>
- [Human Voice](references/human-voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Guidance] <br>
**Output Format:** [JSON file plus plain-text completion report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates ~/blog-meta/<seo_slug>.json and reports the source blog path, generated fields, research sources, and browser cleanup status.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
