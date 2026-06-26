## Description: <br>
Generates an animated GIF of current and recent weather radar over an OpenStreetMap base map for a specified city or coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaosconst](https://clawhub.ai/user/chaosconst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when someone requests a rain or precipitation radar image for a city or coordinates, generating a shareable animated GIF from RainViewer radar layers and OpenStreetMap tiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external RainViewer and OpenStreetMap services to generate radar imagery. <br>
Mitigation: Use it only in environments where those outbound requests are acceptable, and review the output path before running the script. <br>
Risk: Location requests can expose or infer user location when no explicit city or coordinates are provided. <br>
Mitigation: Prefer explicit city names or coordinates, and avoid relying on inferred precise user location unless the user has requested it. <br>


## Reference(s): <br>
- [ClawHub Weather Radar Release](https://clawhub.ai/chaosconst/weather-radar) <br>
- [RainViewer Public Weather Maps API](https://api.rainviewer.com/public/weather-maps.json) <br>
- [OpenStreetMap Tile Service](https://tile.openstreetmap.org/{zoom}/{x}/{y}.png) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Animated GIF file with concise text or Markdown delivery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated GIF is a 3x3 tile grid and defaults to zoom 7 with recent radar frames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
