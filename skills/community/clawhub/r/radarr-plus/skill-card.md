## Description:

Adds and manages movies in a Radarr instance via its HTTP API, including lookup, profile and root-folder listing, movie adds by title/year or TMDB ID, and optional search triggering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalchaudhary](https://clawhub.ai/user/vishalchaudhary)

### License/Terms of Use:


## Use Case:

External users and operators use Radarr+ in trusted chat workflows to request movies, confirm ambiguous matches, choose quality profile and root folder defaults when needed, add movies to Radarr, and receive progress updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a broad asset downloader that can fetch arbitrary URLs and write to arbitrary writable paths.

Mitigation: Use the downloader only for trusted poster URLs and constrain output paths to the intended outbound Radarr asset directory.

Risk: Credential transport may be weak if Radarr or Plex are configured over plain HTTP.

Mitigation: Prefer HTTPS Radarr and Plex URLs, keep API keys and tokens in the OpenClaw environment file, and limit access to trusted hosts.

Risk: Chat-triggered movie requests can be abused if untrusted users can invoke the skill.

Mitigation: Restrict group and direct-message usage with trusted OpenClaw allowlists before enabling the skill.

Risk: Progress tracking stores movie state and chat targets locally.

Mitigation: Run the skill in a workspace with appropriate file permissions and review local state retention for the deployment.

Risk: Optional Plex integration uses an additional service credential.

Mitigation: Configure Plex only when the deployment intends to use Plex links, and rotate or remove the token when no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vishalchaudhary/skills/radarr-plus)
- [Onboarding](references/onboarding.md)
- [Setup](references/setup.md)
- [Radarr API Notes](references/radarr-api-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with shell commands, JSON script output, and local tracking/outbox files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Radarr URL and API key; optional TMDB, OMDb, and Plex credentials enable richer cards and Plex links.]

## Skill Version(s):

0.1.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
