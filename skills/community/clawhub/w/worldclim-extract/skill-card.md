## Description:

Extracts WorldClim 2.1 BIO1-BIO19 bioclimatic variables from GeoTIFF rasters for longitude/latitude samples, with batch input from Excel or CSV and output to Excel or CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zd200572](https://clawhub.ai/user/zd200572)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to extract climate variables such as annual mean temperature and annual precipitation for sample locations. It supports ecological, population genetics, and geospatial workflows that need WorldClim values joined back to tabular coordinate data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First use may download WorldClim ZIP files into a local cache, so network availability and dataset integrity can affect results.

Mitigation: Run in a virtual environment, use an intentional cache directory, and manually verify or pre-stage WorldClim data for sensitive workflows.

Risk: The script processes user-supplied Excel or CSV coordinate files and writes derived datasets locally.

Mitigation: Use trusted input files, review coordinate column choices and output paths, and keep generated files in an expected working directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zd200572/skills/worldclim-extract)
- [WorldClim 2.1 bioclimatic data base URL](https://geodata.ucdavis.edu/climate/worldclim/2_1/base)
- [WorldClim 2.1 10m BIO ZIP](https://geodata.ucdavis.edu/climate/worldclim/2_1/base/wc2.1_10m_bio.zip)
- [WorldClim 2.1 2.5m BIO ZIP](https://geodata.ucdavis.edu/climate/worldclim/2_1/base/wc2.1_2.5m_bio.zip)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands and code that read local Excel or CSV inputs, download WorldClim ZIP data, cache GeoTIFF rasters, and write Excel or CSV outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
