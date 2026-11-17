## Description:

Rail CLI helps agents use UK National Rail data for live departures, arrivals, station search, destination filtering, batch station search, and field-selected outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shan8851](https://clawhub.ai/user/shan8851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Rail CLI to query UK National Rail boards, resolve station names and CRS codes, filter departures or arrivals, and produce text or JSON results for automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The global npm install is unpinned and could introduce supply-chain exposure.

Mitigation: Pin or review the @shan8851/rail-cli package version before installation.

Risk: Departures and arrivals require DARWIN_ACCESS_TOKEN.

Mitigation: Keep DARWIN_ACCESS_TOKEN scoped to rail data use and avoid placing broader secrets in the same environment.

## Reference(s):

- [Rail CLI homepage](https://rail-cli.xyz)
- [National Rail Darwin OpenLDBWS registration](https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/Registration)
- [@shan8851/rail-cli npm package](https://www.npmjs.com/package/@shan8851/rail-cli)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output may be text or JSON envelopes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Departures and arrivals require DARWIN_ACCESS_TOKEN; station search can run without the token.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
