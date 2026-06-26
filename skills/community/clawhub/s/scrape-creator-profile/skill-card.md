## Description: <br>
Scrape and extract structured data from public creator profiles across platforms such as YouTube, Instagram, TikTok, Twitter/X, LinkedIn, Twitch, and personal websites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahqazi-dev](https://clawhub.ai/user/ahqazi-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to look up public creator profiles, extract normalized profile JSON, compare profiles, and prepare summaries or exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live scraping and managed browser sessions can access profile data through an authenticated session. <br>
Mitigation: Use only authorized public-profile lookups and require explicit confirmation before using logged-in browser sessions. <br>
Risk: Apify fallback sends scraping requests through a third-party service when an API token is configured. <br>
Mitigation: Use Apify only when the user confirms the fallback and accepts third-party processing for the requested profile. <br>
Risk: Saved exports can persist scraped creator data to disk. <br>
Mitigation: Confirm before saving scraped data, use an explicit output path, and avoid storing private contact information or phone numbers. <br>
Risk: Broad lead-list or monitoring workflows may exceed normal public-profile lookup expectations. <br>
Mitigation: Avoid broad lead-list or monitoring use unless the user has a clearly appropriate, authorized purpose. <br>


## Reference(s): <br>
- [Platform Selectors Reference](references/platform-selectors.md) <br>
- [Apify Actors - Fallback Scraping Reference](references/apify-actors.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ahqazi-dev/scrape-creator-profile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational Markdown summaries, normalized JSON objects, Markdown comparison tables, CSV exports, and saved JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes multiple profiles sequentially with a configurable delay; fields not found are returned as null.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
