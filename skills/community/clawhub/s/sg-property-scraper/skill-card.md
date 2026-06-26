## Description: <br>
Searches Singapore property rental and sale listings with flexible filters for listing type, property type, bedrooms, bathrooms, price, size, TOP year, MRT proximity, room details, availability, and optional commute time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[5kbpers](https://clawhub.ai/user/5kbpers) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search and compare Singapore rental or sale listings with filters for property type, price, size, MRT proximity, room details, and optional commute time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commute calculation can send destination and listing-address data to Google Routes API when GOOGLE_MAPS_API_KEY is configured. <br>
Mitigation: Use a restricted Google Maps API key with quotas, and avoid entering sensitive home or workplace addresses unless that disclosure is acceptable. <br>
Risk: The scraper depends on external listing pages and may return empty, stale, or failed results when the site layout, network access, or anti-bot controls change. <br>
Mitigation: Review results before relying on them, use dry-run mode to inspect generated URLs, and treat scraper failures or empty responses as operational signals rather than authoritative market conclusions. <br>
Risk: Python dependencies and external scraping behavior expand the runtime surface for this skill. <br>
Mitigation: Install dependencies in a virtual environment and run the skill with only the credentials and network access needed for the requested search. <br>


## Reference(s): <br>
- [PropertyGuru Parameter Reference](references/params.md) <br>
- [PropertyGuru Singapore](https://www.propertyguru.com.sg) <br>
- [ClawHub skill page](https://clawhub.ai/5kbpers/sg-property-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/5kbpers) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON array on stdout by default, with optional text output and dry-run URL output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Python dependencies; optional commute calculations require GOOGLE_MAPS_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
