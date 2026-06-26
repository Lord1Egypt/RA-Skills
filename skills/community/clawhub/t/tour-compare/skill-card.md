## Description: <br>
Tour Compare helps agents compare OTA tour products from links, screenshots, or JSON and produce structured recommendations, risk reminders, and exportable reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangnex](https://clawhub.ai/user/liangnex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel users, assistants, and developers use this skill to compare group-tour products across OTA platforms, identify price, itinerary, rating, hotel, shopping, and cancellation-policy differences, and choose options for traveler personas such as elderly, family, student, honeymoon, friends, or business travelers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied OTA URLs may trigger live web fetching and depend on unstable third-party pages. <br>
Mitigation: Use JSON input or --no-fetch for sensitive comparisons, and verify current prices and terms on the official OTA before acting. <br>
Risk: Submitted screenshots may contain personal or booking information, and OCR quality can affect extracted facts. <br>
Mitigation: Redact screenshots before use and review extracted fields before relying on the comparison. <br>
Risk: Report export writes local files and could overwrite paths supplied by the user. <br>
Mitigation: Choose dedicated output paths and avoid writing over important files. <br>
Risk: Optional browser, OCR, and image-export dependencies increase the local execution surface. <br>
Mitigation: Install only the dependencies needed for the intended mode and review package sources before enabling advanced features. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/liangnex/tour-compare) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [Input Guide](artifact/docs/INPUT_GUIDE.md) <br>
- [Output Flow](artifact/docs/OUTPUT_FLOW.md) <br>
- [Supported Platforms](artifact/docs/PLATFORMS.md) <br>
- [Usage Examples](artifact/examples/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown-style comparison summaries with optional local HTML or PNG report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch live OTA pages unless JSON input or --no-fetch is used; exported reports are written to local paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json reports 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
