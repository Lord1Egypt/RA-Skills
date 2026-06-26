## Description: <br>
Download Sentinel satellite imagery (Sentinel-1/2/5P) via STAC API with cloud cover filtering and batch download support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruiduobao](https://clawhub.ai/user/ruiduobao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Remote-sensing developers, analysts, and engineers use this skill to search Sentinel-1, Sentinel-2, and Sentinel-5P imagery by bounding box and date range, optionally filtering by cloud cover and downloading matching assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts remote STAC services and can download large imagery files. <br>
Mitigation: Use trusted STAC endpoints, test searches with a low result limit first, and run downloads only on stable networks. <br>
Risk: Remote item metadata and asset URLs influence local download paths and filenames. <br>
Mitigation: Choose a non-sensitive output directory and review downloaded filenames before using the files in downstream workflows. <br>
Risk: The shell wrapper can install Python dependencies when run with --check-deps. <br>
Mitigation: Use a virtual environment and run --check-deps only when package installation is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ruiduobao/sentinel-downloader-skill) <br>
- [Microsoft Planetary Computer STAC API](https://planetarycomputer.microsoft.com/api/stac/v1) <br>
- [AWS Earth Search STAC API](https://earth-search.aws.element84.com/v1) <br>
- [Sentinel Hub Catalog API](https://services.sentinel-hub.com/api/v1/catalog) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, JSON, Files] <br>
**Output Format:** [Command-line output as table text or JSON, with downloaded imagery files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches remote STAC services and writes downloads to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
