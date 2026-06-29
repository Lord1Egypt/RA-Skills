## Description: <br>
Provides guidance, API references, sample Mini Program projects, and Tencent Maps SDK material for building map, location, marker, route planning, geocoding, POI search, clustering, and visualization features in WeChat Mini Programs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement Tencent Maps and WeChat Mini Program location features, including map display, markers, MapContext controls, location permissions, backend LBS service calls, and example project integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Maps API keys and SK/signing secrets could be exposed if embedded in client code or examples. <br>
Mitigation: Treat TMAP_MINIPROGRAM_KEY and signing secrets as credentials, keep signing material out of client-side Mini Program code, and review generated examples before deployment. <br>
Risk: Map and location features can collect precise or background location data and send it to Tencent services. <br>
Mitigation: Ensure the app explains location collection, Tencent processing, retention, and controls for disabling ongoing or background location access. <br>
Risk: The bundled experience-key mode has limited stability, rate limits, and unsupported endpoints. <br>
Mitigation: Use a formal Tencent Location Service key for production behavior and clearly distinguish restricted experience-key examples from production code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/tencentmap-miniprogram-skill) <br>
- [Tencent Maps developer console](https://lbs.qq.com/dev/console/key/manage) <br>
- [WeChat Mini Program map component documentation](https://developers.weixin.qq.com/miniprogram/dev/component/map.html) <br>
- [WeChat Mini Program location API documentation](https://developers.weixin.qq.com/miniprogram/dev/api/location/wx.getLocation.html) <br>
- [Tencent Location Service](https://lbs.qq.com/) <br>
- [Tencent Location Service Mini Program JavaScript SDK guide](https://lbs.qq.com/miniProgram/js/jsSdk/jsSdkGuide/jsSdkGuide) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands] <br>
**Output Format:** [Markdown with JavaScript, JSON, XML/WXML, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Tencent Maps API key setup guidance, WeChat Mini Program code snippets, and location-service implementation notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
