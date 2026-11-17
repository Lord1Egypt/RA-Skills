## Description:

Tencent Maps Map Assistant lets agents use Tencent Maps for trip planning, POI search, route planning, geocoding, weather, coordinate conversion, and map or mini-program guide generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer travel and location questions with Tencent Maps data, generate itineraries, retrieve POIs, routes, weather, and geocodes, and create shareable map guides or HTML map views.

### Deployment Geography for Use:

Global, subject to local compliance review for map display workflows.

## Known Risks and Mitigations:

Risk: Tencent Maps may receive location, POI, route, guide, phone-verification, and key-enrollment data for requested workflows.

Mitigation: Install and use the skill only when that data flow is acceptable, and review the Tencent Maps terms and privacy policy before phone-based key enrollment.

Risk: Usable Tencent Maps API keys can be stored in ~/.tencentmap/tempkey.json or exposed in generated HTML map files.

Mitigation: Treat the local key file as sensitive, prefer a scoped Tencent Maps key, avoid publishing HTML with plaintext keys, and use a proxy or key-delegation pattern for public pages.

Risk: The skill can create shareable mini-program guides and QR codes from searches, routes, or itineraries.

Mitigation: Ask the agent not to generate or save a guide unless a shareable map is explicitly desired, and review generated map content before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/tencentmap-map-assistant-skill)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Agent notes](artifact/references/agent-notes.md)
- [Tencent Maps JSAPI GL guide](artifact/references/jsapi-guide/README.md)
- [Tencent Maps API error codes](artifact/references/error-codes.md)
- [Tencent Maps AI scenario key API reference](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown and plain text, with optional Python snippets, shell commands, HTML map files, PNG QR-code files, and JSON-like API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local Markdown, HTML map files, PNG QR-code files, and persisted Tencent Maps key configuration when the user completes key enrollment.]

## Skill Version(s):

1.5.2 (source: server release metadata, SKILL.md frontmatter, setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
