## Description: <br>
Seoul Subway assistant for real-time arrivals, route planning, and service alerts (Korean/English) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dukbong](https://clawhub.ai/user/dukbong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travelers use this agent skill to ask for Seoul Subway arrivals, station lookup, route planning, service alerts, last-train times, exit, accessibility, quick-exit, and restroom information in Korean or English. <br>

### Deployment Geography for Use: <br>
Global use; transit coverage is Seoul, South Korea. <br>

## Known Risks and Mitigations: <br>
Risk: Transit lookups are sent to a hosted third-party proxy, including station names, route parameters, IP address, and User-Agent. <br>
Mitigation: Use session-only permission unless the user trusts the proxy, and avoid sending sensitive personal details in station or route search parameters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dukbong/seoul-subway) <br>
- [Skill homepage](https://github.com/dukbong/seoul-subway) <br>
- [Transit proxy API base](https://vercel-proxy-henna-eight.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown transit answers with bilingual Korean and English tables, summaries, and error guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WebFetch-backed proxy requests; no API key is required.] <br>

## Skill Version(s): <br>
0.1.19 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
