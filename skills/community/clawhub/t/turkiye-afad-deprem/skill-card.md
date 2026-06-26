## Description: <br>
Turkiye AFAD deprem verisini kullanarak zaman, buyukluk ve bolge filtreli deprem ozeti uretir. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barancaki](https://clawhub.ai/user/barancaki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to retrieve recent public AFAD earthquake records and summarize them by time window, minimum magnitude, and location query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing the source URL could retrieve earthquake data from an untrusted endpoint. <br>
Mitigation: Keep the default AFAD endpoint unless another source is intentionally trusted. <br>
Risk: Fixture mode can read local JSON files supplied to the helper script. <br>
Mitigation: Use fixture mode only with known local JSON test files. <br>
Risk: Live AFAD network responses may be unavailable or change format. <br>
Mitigation: Handle network and parse errors and retry later when the public AFAD service is unavailable. <br>


## Reference(s): <br>
- [AFAD Source Notes](references/afad_source.md) <br>
- [Project homepage](https://github.com/barancaki/turkey_earthquake_skill) <br>
- [AFAD earthquake portal](https://deprem.afad.gov.tr/) <br>
- [AFAD event service](https://deprem.afad.gov.tr/event-service) <br>
- [AFAD event filter endpoint](https://deprem.afad.gov.tr/apiv2/event/filter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [Markdown summary with a table and source link; helper output is JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports time window, minimum magnitude, location query, timeout, source URL, and fixture inputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
