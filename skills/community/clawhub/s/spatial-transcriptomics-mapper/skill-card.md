## Description: <br>
Maps 10x Genomics Visium or Xenium spatial transcriptomics data onto tissue images for gene expression, clustering, multi-gene overlay, and report outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, bioinformatics analysts, and spatial biology teams use this skill to run bounded Visium or Xenium mapping workflows, visualize selected genes or clusters, and produce reproducible images or HTML reports from local datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpinned dependencies and the declared 'pil' package name can make production installs inconsistent or pull an unintended package. <br>
Mitigation: Use a virtual environment or container, replace 'pil' with pinned 'Pillow', and pin the remaining scientific Python dependencies before production use. <br>
Risk: The skill reads local user-provided Visium or Xenium datasets and writes reports or images that may contain sensitive sample-derived information. <br>
Mitigation: Provide only datasets intended for analysis, choose the output directory deliberately, and handle generated reports and images as sensitive derived data. <br>
Risk: Large Xenium or high-resolution image inputs can increase runtime and memory use. <br>
Mitigation: Use documented crop or downsampling options for large samples and validate outputs on a small subset before full processing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/spatial-transcriptomics-mapper) <br>
- [10x Genomics Visium Spatial Gene Expression](https://www.10xgenomics.com/products/spatial-gene-expression) <br>
- [10x Genomics Xenium Platform](https://www.10xgenomics.com/platforms/xenium) <br>
- [Scanpy Documentation](https://scanpy.readthedocs.io/) <br>
- [Squidpy Documentation](https://squidpy.readthedocs.io/) <br>
- [Matplotlib Colormap Reference](https://matplotlib.org/stable/tutorials/colors/colormaps.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG or HTML analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include gene spatial maps, heatmaps, multi-gene overlays, cluster maps, expression statistics, and an HTML report written to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/__init__.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
