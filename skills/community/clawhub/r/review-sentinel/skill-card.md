## Description: <br>
Monitor, analyze, and respond to Google reviews for local businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rolarenagent-cpu](https://clawhub.ai/user/rolarenagent-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and business teams use this skill to monitor Google reviews, detect rating or review-count changes, analyze themes, draft human-approved replies, and generate reputation reports for local businesses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Google Places API key. <br>
Mitigation: Use the GOOGLE_PLACES_API_KEY environment variable, restrict the key in Google Cloud, and avoid storing credentials in local files unless necessary. <br>
Risk: Review monitoring stores business review data, state snapshots, and reports locally. <br>
Mitigation: Periodically remove old state and report files that are no longer needed, especially for sensitive business contexts. <br>
Risk: Drafted review replies can affect customer relationships or regulated communications. <br>
Mitigation: Keep replies human-approved and manual, and avoid referencing patient conditions or other sensitive details in healthcare or professional-service responses. <br>
Risk: The fallback web scraping scripts are fragile and may break when Google changes page structure. <br>
Mitigation: Prefer the Google Places API workflow and treat scraping output as best-effort evidence that should be checked before action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rolarenagent-cpu/review-sentinel) <br>
- [State schema](references/state-schema.md) <br>
- [Google Places API Text Search endpoint](https://places.googleapis.com/v1/places:searchText) <br>
- [Google Places API Place Details endpoint](https://places.googleapis.com/v1/{place_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON summaries, local state files, report files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Google Places API key and may store local business review state and generated reports.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
