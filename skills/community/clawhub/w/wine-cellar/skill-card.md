## Description: <br>
Comprehensive wine cellar management skill for tracking inventory, providing meal-based recommendations, acting as a virtual sommelier, tracking consumption/purchases, and supporting barcode lookup to retrieve bottle details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzysb](https://clawhub.ai/user/fuzzysb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal cellar managers use this skill to track wine inventory, look up bottles by barcode, get meal-based pairing suggestions, and maintain purchase or consumption notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local inventory and cache files can retain personal wine, purchase, consumption, pricing, and social-event details. <br>
Mitigation: Treat the JSON files as personal data, back them up intentionally, delete them when no longer needed, and avoid recording sensitive social or spending details. <br>


## Reference(s): <br>
- [Wine database reference](artifact/references/wine_database.json) <br>
- [ClawHub release page](https://clawhub.ai/fuzzysb/wine-cellar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON-backed local data and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON inventory, barcode cache, and wine reference files; no server-resolved GitHub provenance is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
