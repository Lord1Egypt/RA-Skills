## Description:

Maps 10x Genomics Visium and Xenium spatial transcriptomics outputs onto tissue images for gene expression, clustering, and multi-gene visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to process Visium or Xenium spatial transcriptomics datasets and generate visual maps of gene expression, clusters, and multi-gene patterns on tissue imagery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing untrusted datasets may expose file-output and report-generation weaknesses.

Mitigation: Run the skill in an isolated Python environment as an unprivileged user and avoid untrusted datasets unless inputs have been reviewed.

Risk: Generated HTML reports may include unsanitized gene names or filenames from input data.

Mitigation: Do not open generated HTML reports from untrusted inputs until gene names and filenames have been escaped or sanitized.

Risk: Configurable output paths can write analysis artifacts outside the intended workspace if not contained.

Mitigation: Keep output paths in a disposable workspace and add output path containment checks before deployment.

Risk: Unpinned dependencies and the declared pil package can reduce reproducibility or install reliability.

Mitigation: Pin dependencies for the deployment environment and replace pil with Pillow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/spatial-transcriptomics-mapper)
- [10x Genomics Visium](https://www.10xgenomics.com/products/spatial-gene-expression)
- [10x Genomics Xenium](https://www.10xgenomics.com/platforms/xenium)
- [Scanpy documentation](https://scanpy.readthedocs.io/)
- [Squidpy documentation](https://squidpy.readthedocs.io/)
- [Matplotlib colormap reference](https://matplotlib.org/stable/tutorials/colors/colormaps.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and generated local image or HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate PNG spatial maps, multi-gene visualizations, clustering plots, and HTML reports in the configured output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact scripts/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
