## Description: <br>
This skill helps an agent use UAPI's GET /daily/news-image endpoint to retrieve a JPEG daily news summary image and explain request handling, authentication posture, and response codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they need an agent to select and prepare the UAPI daily news image endpoint for requests involving daily news posters, daily digests, or image-based news summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The endpoint returns JPEG image bytes rather than JSON, so clients that assume structured JSON may fail or mishandle the response. <br>
Mitigation: Handle the successful response as image/jpeg binary data and display or save it as an image. <br>
Risk: Realtime news collection and image rendering can take several seconds or fail because of upstream news-source availability. <br>
Mitigation: Use a reasonable request timeout, retry later for 500 or 502 responses, and explain transient upstream failures to the user. <br>
Risk: Anonymous or free quota may be exhausted if UAPI policy changes or returns a quota-related 429 response. <br>
Mitigation: Only provide a UAPI key when the user intentionally wants authenticated quota, and do not provide unrelated credentials. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/shuakami/uapi-get-daily-news-image) <br>
- [Publisher profile](https://clawhub.ai/user/shuakami) <br>
- [Quick start](references/quick-start.md) <br>
- [Daily news image operation](references/operations/get-daily-news-image.md) <br>
- [Daily resource overview](references/resources/Daily.md) <br>
- [UAPI service](https://uapis.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, api calls, configuration, markdown] <br>
**Output Format:** [Markdown guidance with endpoint details and optional HTTP request instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful endpoint responses are JPEG image bytes from UAPI, not JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
