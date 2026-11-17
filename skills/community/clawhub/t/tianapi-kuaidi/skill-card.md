## Description:

Queries global parcel tracking updates through TianAPI, with automatic tracking-number recognition and optional phone suffix support for carriers that require it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve parcel logistics status and tracking history from TianAPI for a supplied tracking number, optional carrier code, and optional sender phone suffix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parcel tracking numbers, carrier identifiers, and sometimes phone-number suffixes are sent to TianAPI.

Mitigation: Use the skill only when that disclosure is acceptable, send only the fields required for the lookup, and avoid using it for shipments that should not be shared with TianAPI.

Risk: API keys can be exposed through command-line arguments, shell history, logs, or an unprotected scripts/.env file.

Mitigation: Prefer TIANAPI_KUAIDI_KEY, use a dedicated quota-limited key, restrict access to any .env file, and rotate the key if it was pasted into shell history or logs.

## Reference(s):

- [TianAPI Kuaidi API documentation](https://www.tianapi.com/apiview/152)
- [TianAPI Kuaidi API endpoint](https://apis.tianapi.com/kuaidi/index)
- [ClawHub skill page](https://clawhub.ai/workxin/skills/tianapi-kuaidi)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [JSON from the helper script, typically summarized as concise text or Markdown by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TIANAPI_KUAIDI_KEY; accepts a tracking number plus optional carrier code and sender phone suffix.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
