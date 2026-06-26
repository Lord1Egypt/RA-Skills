## Description: <br>
Fetches public X/Twitter data through Apify actors for tweet search, user profiles, specific tweets, replies, and local caching to reduce repeated API costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve public X/Twitter search results, user timelines, and individual tweet threads through Apify-backed helper scripts. It is useful when an agent needs current public social media data in JSON or concise summary form while controlling API cost with local caching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: X/Twitter searches, usernames, and tweet URLs are sent to Apify and the selected actor. <br>
Mitigation: Avoid sensitive lookups, use a dedicated Apify token where possible, and use --no-cache or --clear-cache for sensitive sessions. <br>
Risk: Apify actor runs can consume account credits. <br>
Mitigation: Monitor Apify credit usage, keep result limits appropriate, and use the built-in local cache for repeat queries. <br>
Risk: The documented default actor and the code's default actor may differ. <br>
Mitigation: Verify the selected actor before use and set APIFY_ACTOR_ID explicitly when actor behavior, pricing, or data fields matter. <br>
Risk: Cached results may retain queried public social data on disk. <br>
Mitigation: Use --no-cache for one-off sensitive lookups, clear cached results after use, and keep X_APIFY_CACHE_DIR inside the skill directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/robbyczgw-cla/x-apify) <br>
- [Apify Pricing](https://apify.com/pricing) <br>
- [Apify API Token Setup](https://console.apify.com/account/integrations) <br>
- [Twitter Scraper Actor](https://apify.com/quacker/twitter-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; helper script output is JSON or human-readable summary text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests library, and APIFY_API_TOKEN; optional APIFY_ACTOR_ID and X_APIFY_CACHE_DIR configure actor selection and local cache behavior.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence, package.json, and changelog; frontmatter still lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
