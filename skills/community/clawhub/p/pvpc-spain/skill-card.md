## Description: <br>
PVPC España helps agents query Spanish PVPC 2.0TD electricity prices, classify current prices, identify tariff periods, find low-cost hourly ranges, and schedule appliance use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[didelco](https://clawhub.ai/user/didelco) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer PVPC electricity-price questions for Spain and recommend lower-cost times for household appliance usage. It is intended for tariff guidance, price comparison, and daily consumption planning for domestic 2.0TD users. <br>

### Deployment Geography for Use: <br>
Spain <br>

## Known Risks and Mitigations: <br>
Risk: Holiday handling may classify Spanish national, regional, or local holidays as normal weekdays. <br>
Mitigation: Manually account for applicable holidays before relying on tariff-period decisions. <br>
Risk: Live price queries may fail or return incomplete guidance when the public ESIOS endpoint is unavailable. <br>
Mitigation: Treat failed API responses as unavailable data and retry or confirm prices from an official source before scheduling high-cost usage. <br>


## Reference(s): <br>
- [PVPC Espana ClawHub release](https://clawhub.ai/didelco/pvpc-spain) <br>
- [ESIOS public PVPC JSON archive](https://api.esios.ree.es/archives/70/download_json?locale=es&date={date_str}) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from Python scripts, often accompanied by agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on live public PVPC data from ESIOS and local date/time handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
