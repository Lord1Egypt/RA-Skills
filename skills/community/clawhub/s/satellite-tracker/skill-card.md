## Description:

Real-time satellite and spacecraft tracking powered by SGP4 orbit prediction, supporting Tiangong, ISS, Hubble, and arbitrary NORAD catalog IDs with position and pass-prediction output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengyucn](https://clawhub.ai/user/fengyucn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and space enthusiasts use this skill to answer where a satellite or space station is, inspect orbital details, and predict visible passes from observer coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public TLE data from Celestrak and writes a local cache file.

Mitigation: Allow network access only for expected Celestrak TLE requests and review the local cache behavior before deployment.

Risk: The `sgp4` dependency is installed without a pinned version.

Mitigation: Pin and review the dependency version in managed environments before installing the skill.

Risk: Large `--passes` values or continuous `--watch` mode can create long-running local work.

Mitigation: Use reasonable pass counts and watch intervals, and stop continuous tracking when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengyucn/skills/satellite-tracker)
- [Celestrak TLE data endpoint](https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=tle)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON from command-line execution, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include current coordinates, altitude, speed, orbital parameters, geographic region, and optional pass predictions.]

## Skill Version(s):

1.1.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
