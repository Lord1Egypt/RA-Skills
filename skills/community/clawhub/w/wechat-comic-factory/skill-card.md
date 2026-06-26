## Description: <br>
Generates WeChat comic articles from a comic type, topic, and count, then can publish the generated content to the WeChat Official Account draft box by executing local Python pipeline scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archibald80000-ai](https://clawhub.ai/user/archibald80000-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and content operators use this skill to generate Chinese-language WeChat comic article packages from a supported comic type, topic, and count. It is also used to create WeChat Official Account draft-box entries for the latest generated task or a specified output directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generation commands can upload article images and create WeChat Official Account draft-box entries without a separate publish confirmation. <br>
Mitigation: Use --skip_publish for generation-only runs, or require explicit operator confirmation before uploads and draft creation. <br>
Risk: The skill requires model API keys and WeChat Official Account app credentials, and runtime files may contain tokens, outputs, logs, or publish results. <br>
Mitigation: Keep config.json, output, logs, publish_result.json, and cached WeChat tokens private; do not include them in release packages or shared logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archibald80000-ai/wechat-comic-factory) <br>
- [Publisher profile](https://clawhub.ai/user/archibald80000-ai) <br>
- [WeChat Official Account API base endpoint](https://api.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Structured JSON script results, with generated Markdown, HTML, image assets, logs, and WeChat draft metadata written by the pipeline.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generation supports supported comic types, topic, count, skip-publish mode, latest-task publishing, and explicit output-directory publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
