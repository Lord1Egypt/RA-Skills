## Description:

Automatically routes oversized tool results to compressed local files and returns concise metadata so agent conversations are not flooded by large payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suda6632](https://clawhub.ai/user/suda6632)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to wrap tools whose results may exceed context limits, spilling large outputs to local compressed files while returning paths, size metadata, hashes, and previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe tool names or supplied result paths can allow reads or writes outside the documented result directory.

Mitigation: Validate filenames, constrain reads and writes to the managed results directory, and avoid untrusted tool names or result paths until those controls are in place.

Risk: Spilled tool results may contain sensitive data retained on disk.

Mitigation: Document retention behavior, restrict access to stored result files, and run cleanup for expired results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suda6632/skills/tool-result-size-controller)

## Skill Output:

**Output Type(s):** [Text, Code, Files, Configuration, Guidance]

**Output Format:** [Python API behavior returning original data or JSON-like spill metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large results are written as gzip-compressed files with size metadata, content hashes, previews, and cleanup support.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
