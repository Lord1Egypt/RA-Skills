## Description:

Searches local images with Chinese or English natural-language queries by building and querying a local Chinese-CLIP and FAISS image index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobemsk](https://clawhub.ai/user/tobemsk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up local semantic image search, scan configured image locations, update the image index, and retrieve matching image paths from natural-language queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default behavior can scan broad local image locations and store image paths and feature data in image_db.

Mitigation: Review and narrow SCAN_ROOTS before scanning, exclude sensitive directories, and handle the generated index as local private data.

Risk: The skill downloads model files through hf-mirror.com and relies on unpinned Python dependency ranges.

Mitigation: Install in an isolated Python environment, pin and review dependencies, and use trusted or pre-vetted model sources for production use.

Risk: The image path list is stored with pickle, which is unsafe to load from untrusted sources.

Mitigation: Only load indexes created locally in a trusted environment, or replace the pickle-based path list with a safer serialization format before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobemsk/skills/tobemsk-image-search)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Hugging Face mirror endpoint](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and Python configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on installing dependencies, configuring scan roots, building or updating the local index, and running searches that save text results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
