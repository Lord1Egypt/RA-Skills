## Description: <br>
Get surf forecasts and current conditions from Surfline public endpoints (no login). Use to look up Surfline spot IDs, fetch forecasts/conditions for specific spots, and summarize multiple favorite spots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MiguelCarranza](https://clawhub.ai/user/MiguelCarranza) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search Surfline spot IDs, retrieve current surf forecasts and conditions for individual spots, and summarize configured favorite spots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, spot IDs, and forecast requests are sent to Surfline public endpoints. <br>
Mitigation: Install only if sharing searched spot names and Surfline spot IDs with Surfline is acceptable. <br>
Risk: Cached forecast responses and favorites can remain on the local machine under Surfline cache and configuration paths. <br>
Mitigation: Delete cached/configured Surfline files when no longer needed or set SURFLINE_CACHE_DIR to an approved location. <br>
Risk: Surfline endpoint or response-field changes can make reports incomplete or inaccurate. <br>
Mitigation: Review results before relying on them and update scripts/surfline_client.py if Surfline changes endpoint behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MiguelCarranza/surfline) <br>
- [Surfline public services endpoint](https://services.surfline.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summaries and JSON payloads from command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Surfline endpoints, no login, and local caching controlled by SURFLINE_CACHE_DIR and SURFLINE_CACHE_TTL_SEC.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
