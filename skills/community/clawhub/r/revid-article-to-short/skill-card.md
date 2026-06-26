## Description: <br>
Turn any news article or long-form post URL into a 30-60 second 9:16 short with stock visuals, narration, and captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert a supplied article, blog post, press release, or essay URL into a short vertical video summary through Revid. It is intended for edited summaries with narration, stock visuals, music, and captions rather than talking-head videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article URLs and generated video content are sent to Revid as a third-party processor. <br>
Mitigation: Avoid private, internal, authenticated, sensitive, or paywalled URLs unless the user has permission and has reviewed Revid's privacy and retention terms. <br>
Risk: The skill requires a sensitive REVID_API_KEY credential. <br>
Mitigation: Provide the key only through runtime configuration and avoid exposing it in prompts, logs, examples, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/api00/revid-article-to-short) <br>
- [Revid render API endpoint](https://www.revid.ai/api/public/v3/render) <br>
- [Revid status API endpoint](https://www.revid.ai/api/public/v3/status) <br>
- [Example payload](examples/article-techreview.json) <br>
- [Example shell runner](examples/run.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command snippets plus a returned video URL or render-status JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVID_API_KEY and a public article URL; default output target is a 30-60 second 9:16 video.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
