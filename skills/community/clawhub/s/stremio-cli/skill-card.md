## Description:

Stremio CLI automates Stremio Web with the Torrentio add-on on a Mac Mini to search for movies or shows, choose high-seeded streams, and start playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bearly-hodling](https://clawhub.ai/user/bearly-hodling)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a Mac Mini Stremio setup use this skill to have an agent search Stremio Web, choose an episode or movie stream through Torrentio, and start playback. The skill is intended for media playback requests where missing season or episode details should be confirmed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill text exposes a Stremio account email and relies on an existing logged-in account on the Mac Mini.

Mitigation: Remove account details from the skill text and keep credentials in the operating system credential store or another approved secret store.

Risk: Playback can start content from a user media request when season, episode, or title details are ambiguous.

Mitigation: Require explicit confirmation of the title and season or episode before selecting a stream or starting playback.

Risk: The bundled legacy script has under-documented casting behavior, unsafe browser flags, and stream URL handling.

Mitigation: Delete the legacy script before release or document and constrain its casting behavior, browser settings, and stream URL handling before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bearly-hodling/skills/stremio-cli)

## Skill Output:

**Output Type(s):** [Guidance, Browser automation]

**Output Format:** [Markdown guidance with browser-tool actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing Stremio login on the Mac Mini and should confirm ambiguous season or episode selections before playback.]

## Skill Version(s):

1.1.0 (source: evidence.release.version; artifact _meta.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
