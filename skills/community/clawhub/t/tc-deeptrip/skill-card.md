## Description:

DeepTrip is a travel assistant skill for hotel search, transportation options, attraction recommendations, and itinerary planning, with product links for booking flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tclxhai-lv](https://clawhub.ai/user/tclxhai-lv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search hotels, compare transportation choices, get destination recommendations, and produce trip plans with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed travel requests are sent to Tongcheng's remote API.

Mitigation: Tell users before sending travel details to the external service and avoid including sensitive itinerary, identity, contact, or payment information unless the user explicitly accepts that sharing.

Risk: The skill promotes Tongcheng login or app usage as part of the travel booking flow.

Mitigation: Present login as optional for a smoother booking experience and let users continue with non-login travel information requests when possible.

Risk: API keys passed directly on the command line can be exposed through shell history or process inspection.

Mitigation: Prefer the skill's configuration-file flow or another secret-handling mechanism, and avoid pasting real API keys into shared terminals or logs.

## Reference(s):

- [DeepTrip ClawHub Skill Page](https://clawhub.ai/tclxhai-lv/skills/tc-deeptrip)
- [DeepTrip API Endpoint](https://dtgw.ly.com/deeptrip/claw/chat)
- [Tongcheng Login Link](https://open.weixin.qq.com/connect/qrconnect?appid=wx3827070276e49e30&redirect_uri=http%3a%2f%2fwx.17u.cn%2fflight%2fgetwxuserinfo.html%3furl%3dhttps%253a%252f%252fpassport.ly.com%252fThirdParty%252fWeChatLogin%253fpageUrl%253dhttps%25253a%25252f%25252fdeeptrip.ly.com%25252f%252523%25252f%2526state%253d0abb2c15e81f4da2906cf7222c57dbb7&response_type=code&scope=snsapi_login#wechat_redirect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown or plain text travel recommendations with product links; the script also consumes and returns JSON from the remote API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include PC and mobile booking links. Each request is independent and should include the needed travel context.]

## Skill Version(s):

1.0.4 (source: server evidence release.version and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
