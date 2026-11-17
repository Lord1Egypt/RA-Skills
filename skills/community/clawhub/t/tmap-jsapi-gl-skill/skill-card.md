## Description:

腾讯地图 JavaScript GL（JSAPIGL）开发指南。适用于地图应用或者工具的编写。在编写、审查或调试使用腾讯地图 API的代码时应运用此技能。适用于涉及地图初始化、覆盖物展示、图层控制、事件处理、控件交互、可视化渲染、地图工具、检索、路线规划、查地址、行政区划、ip定位、几何计算、三维模型展示、性能优化的任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[vajrabodhi](https://clawhub.ai/user/vajrabodhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, review, and debug Tencent Maps JavaScript GL applications, including map initialization, overlays, layers, events, search, routing, geocoding, geometry, 3D models, and visualization features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled demos include a concrete Tencent Maps API key.

Mitigation: Create and restrict your own Tencent Maps key, keep it in TMAP_JSAPI_KEY, and replace concrete keys before copying code.

Risk: Runnable demos may send map queries, addresses, coordinates, IP-derived location, and browser requests to Tencent or loaded third-party scripts.

Mitigation: Open demos only with data you are comfortable transmitting, and review external script and service calls before reuse.

## Reference(s):

- [TMap JSAPI GL Skill](artifact/SKILL.md)
- [JSAPI GL Overview](artifact/references/jsapigl/docs/概述.md)
- [JSAPI GL Map API](artifact/references/jsapigl/docs/地图.md)
- [JSAPI GL Service Library](artifact/references/jsapigl/docs/附加库：服务类库.md)
- [Visualization Reference Manual](artifact/references/visualization/docs/参考手册.md)
- [ClawHub Skill Page](https://clawhub.ai/vajrabodhi/skills/tmap-jsapi-gl-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with HTML and JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference TMAP_JSAPI_KEY for Tencent Maps API access.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
