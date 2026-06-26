## Description: <br>
A Tencent Maps development assistant for WebService API usage, geocoding, route planning, map SDK integration, and WeChat Mini Program map workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill as a Tencent Maps reference for integrating location services, building geocoding and route planning calls, and configuring WeChat Mini Program map components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Maps API keys or SK signing secrets could be exposed if examples are copied directly into client-side production code. <br>
Mitigation: Keep secrets server-side where possible, restrict API keys, enable SK signing or domain allowlists, and review example code before production use. <br>
Risk: Untrusted SDK downloads could introduce supply-chain risk. <br>
Mitigation: Download Tencent Maps SDK files only from official Tencent sources before adding them to an application. <br>
Risk: Location, IP address, or routing requests may send real user location data to Tencent Maps. <br>
Mitigation: Review privacy and legal requirements before sending production user location or IP data to Tencent Maps APIs. <br>
Risk: High request volume may exceed Tencent Maps quota or rate limits described by the skill. <br>
Mitigation: Use batch endpoints where appropriate, add throttling, and handle Tencent Maps error responses in application code. <br>


## Reference(s): <br>
- [ClawHub Tencent Map skill page](https://clawhub.ai/zhangifonly/tencent-map) <br>
- [Tencent Maps API base URL](https://apis.map.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with API examples, JavaScript snippets, configuration notes, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reference guidance only; it does not include executable bundled code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
