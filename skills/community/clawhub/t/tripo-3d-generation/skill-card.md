## Description: <br>
Tripo 3d turns text or images into 3D models and supports rigging, animation, stylization, texturing, and format conversion workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meterlong](https://clawhub.ai/user/meterlong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creators use this skill to generate 3D assets from text prompts, images, or file references, then rig, animate, stylize, texture, or convert those assets for games, AR, e-commerce, architecture, and 3D printing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: 3D prompts, public image URLs or file references, task metadata, and an anonymous quota ID are sent to Tripo or the listed proxy for generation workflows. <br>
Mitigation: Use the skill only when external processing is approved, and avoid confidential designs or private images unless the external service path has been reviewed. <br>
Risk: Free-tier use relies on the listed proxy, which adds proxy and privacy tradeoffs beyond direct Tripo API usage. <br>
Mitigation: Configure a personal Tripo API key when direct Tripo routing is preferred. <br>
Risk: The free-tier anonymous quota identifier can persist locally across runs. <br>
Mitigation: Delete ~/.tripo-skill-id when you need to reset the free-tier identifier. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meterlong/tripo-3d-generation) <br>
- [Tripo AI](https://www.tripo3d.ai/) <br>
- [Tripo API keys](https://platform.tripo3d.ai/api-keys) <br>
- [Tripo platform](https://platform.tripo3d.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Structured JSON-like responses with task identifiers, status fields, progress messages, and generated model download URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated assets may be exposed as GLB, FBX, OBJ, STL, USDZ, 3MF, rendered image, or PBR model URLs depending on the requested workflow.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release metadata and artifact manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
