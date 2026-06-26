## Description: <br>
Generates personalized Vedic horoscopes and birth charts based on birth data and astrological calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, astrology practitioners, wellness platforms, and application teams use this skill to call a hosted API that creates Vedic horoscope PDFs from personal, family, contact, and birth details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for unusually sensitive identity, family, contact, and birth details without clear privacy or retention disclosures. <br>
Mitigation: Only submit this data if the service operator is trusted and has clear answers on purpose, transmission, storage duration, access, and deletion handling. <br>
Risk: Generated horoscope PDFs may include personal data and remain available through downloadable URLs. <br>
Mitigation: Treat generated PDF URLs as sensitive, share them only with intended recipients, and confirm deletion or retention controls before production use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-vedic-horoscope) <br>
- [API docs](https://api.mkkpro.com:8159/docs) <br>
- [Kong route](https://api.mkkpro.com/lifestyle/vedic-horoscope) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, Guidance] <br>
**Output Format:** [JSON responses with downloadable PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated responses include success status, message, PDF URL, and timestamp when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
