## Description: <br>
Real-time satellite and spacecraft tracking powered by SGP4 orbit prediction for Tiangong, ISS, Hubble, or any NORAD catalog ID, with coordinates, speed, altitude, pass predictions, and geographic region display using Celestrak TLE data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengyucn](https://clawhub.ai/user/fengyucn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to locate satellites or space stations, track spacecraft by name or NORAD ID, and estimate pass times from observer coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public TLE data from Celestrak and can fall back to cached orbital data if the network or upstream source is unavailable. <br>
Mitigation: Run with network access only when live tracking is needed, refresh with --update, and check cache age before relying on coordinates or pass predictions. <br>
Risk: The skill depends on the Python sgp4 package for orbit propagation. <br>
Mitigation: Install sgp4 from a trusted package source and review dependency provenance before deployment. <br>
Risk: Requests for API keys, tokens, or broader filesystem access are unexpected for this skill. <br>
Mitigation: Deny credential requests and limit filesystem write access to the skill cache file unless a reviewed update justifies more access. <br>


## Reference(s): <br>
- [ClawHub Satellite Tracker release page](https://clawhub.ai/fengyucn/satellite-tracker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fengyucn) <br>
- [Celestrak TLE data endpoint](https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=tle) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text or JSON from the tracking script; markdown guidance when invoked by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update tle_cache.json and depends on fresh Celestrak TLE data.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
