## Description:

Download wallpapers in batch from wallhaven.cc via API v1 with flexible query parameters for query, category, purity, sorting, resolution, ratio, color, page, and seed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingyuan9527](https://clawhub.ai/user/jingyuan9527)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate Wallhaven wallpaper download commands and run a bundled downloader for filtered wallpaper collections. It is suited for batch downloads into a chosen output folder with a manifest of downloaded items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Wallhaven API key can be exposed in local process arguments.

Mitigation: Avoid passing the API key on the command line; use a low-risk Wallhaven key and rotate it if exposure is suspected.

Risk: Downloads may follow redirects outside the stated host limits.

Mitigation: Run the skill in a controlled environment and use a dedicated output directory until redirect handling is reviewed.

Risk: The skill downloads remote image files to a user-selected folder.

Mitigation: Choose a dedicated destination directory and review the generated manifest before using the downloaded files elsewhere.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jingyuan9527/skills/wallhaven-downloader)
- [Wallhaven API Search Endpoint](https://wallhaven.cc/api/v1/search)
- [Wallhaven Search](https://wallhaven.cc/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples and JSON manifest output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The downloader writes image files and a manifest.json file in the selected output directory.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
