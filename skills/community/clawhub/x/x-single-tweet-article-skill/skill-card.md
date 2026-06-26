## Description: <br>
Fetch a single X tweet or X Article with charge-first billing (0.001 USDT/call). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangkefeng-ai](https://clawhub.ai/user/huangkefeng-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to retrieve the text and metadata of a single public X status or the text of a single X Article after billing succeeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds a billing API key in the runtime file. <br>
Mitigation: Remove the embedded key, rotate it, and require the billing API key to be supplied through a protected environment variable before deployment. <br>
Risk: The runtime can fetch or relay non-X URLs without clear limits. <br>
Mitigation: Restrict accepted inputs to public X/Twitter status and article URLs before making billing or fetch requests. <br>
Risk: Submitted URLs may be visible to third-party fetch services. <br>
Mitigation: Use only public X/Twitter URLs and avoid submitting private, sensitive, or access-controlled content. <br>
Risk: The skill uses charge-first billing. <br>
Mitigation: Confirm the billing terms before execution and ensure insufficient-balance handling returns a top-up link before any fetch attempt. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangkefeng-ai/x-single-tweet-article-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON object on success; error details and PAYMENT_URL on billing failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful tweet responses may include text, author, screen name, likes, retweets, views, created_at, and original_url. Article responses include title, full_text, and original_url.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
