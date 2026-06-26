## Description: <br>
This skill helps agents answer questions and generate code for Tencent Map JavaScript GL applications using bundled API documentation and examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill when building, reviewing, or debugging Tencent Map JSAPI GL map applications, including map setup, overlays, layers, events, controls, visualization, search, routing, geocoding, administrative regions, IP location, geometry calculations, 3D models, and performance tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated examples may include live Tencent Map API calls, remote scripts, or browser-side API key use. <br>
Mitigation: Use your own restricted Tencent Map key, avoid exposing signing secrets in client code, and review generated code before production use. <br>
Risk: Bundled demos include patterns such as JSONP and IP-based location that may be inappropriate for production or privacy-sensitive contexts. <br>
Mitigation: Prefer safer CORS or backend-proxied requests, and add notice and consent before adapting IP-location features. <br>


## Reference(s): <br>
- [Tencent Map JavaScript GL Guide](https://lbs.qq.com/webApi/javascriptGL/glGuide/glOverview) <br>
- [JSAPI GL overview](artifact/tencentmap-jsapi-gl-skill/references/jsapigl/docs/概述.md) <br>
- [Visualization reference manual](artifact/tencentmap-jsapi-gl-skill/references/visualization/docs/参考手册.md) <br>
- [Browser environment checks](artifact/tencentmap-jsapi-gl-skill/references/jsapigl/docs/环境检测.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, markdown, configuration] <br>
**Output Format:** [Markdown with JavaScript, HTML, and shell snippets when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference TMAP_JSAPI_KEY and Tencent Map JSAPI library URLs when generating examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
