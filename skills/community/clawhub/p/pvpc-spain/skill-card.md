## Description:

Consulta y optimiza precios de electricidad PVPC en España para la tarifa 2.0TD de usuarios domésticos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[didelco](https://clawhub.ai/user/didelco)

### License/Terms of Use:


## Use Case:

External users and agents serving Spanish household electricity customers use this skill to check current PVPC 2.0TD prices, identify valle/llano/punta periods and cheap hourly ranges, and schedule appliance use to reduce daily electricity cost.

### Deployment Geography for Use:

Spain

## Known Risks and Mitigations:

Risk: The skill depends on live requests to Red Electrica de Espana's public ESIOS API, so unavailable or changed API responses can prevent price lookup or optimization.

Mitigation: Confirm connectivity and review script errors before relying on current-price or scheduling recommendations.

Risk: Holiday handling is incomplete: national holidays are not automatically detected and may be treated as working days for tariff-period classification.

Mitigation: Check Spanish public-holiday status separately before relying on valle/llano/punta classifications for holidays.

Risk: ALTO/MEDIO/BAJO classifications are relative to the current day's prices and do not compare against historical prices.

Mitigation: Use the classification as same-day context only, and verify historical or billing-impact decisions with an authoritative electricity source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/didelco/skills/pvpc-spain)
- [didelco publisher profile](https://clawhub.ai/user/didelco)
- [ESIOS public PVPC archive endpoint](https://api.esios.ree.es/archives/70/download_json?locale=es&date={date_str})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, JSON]

**Output Format:** [Markdown guidance with shell commands and optional JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include current prices, daily statistics, tariff periods, cheap-hour ranges, appliance scheduling recommendations, and error messages when live PVPC data cannot be retrieved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
