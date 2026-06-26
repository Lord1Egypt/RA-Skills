## Description: <br>
Extracts WorldClim 2.1 bioclimatic variables from GeoTIFF rasters for longitude and latitude coordinates in Excel or CSV files, with optional automatic data download and Excel or CSV output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zd200572](https://clawhub.ai/user/zd200572) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to match geographic sample points to climate variables such as annual mean temperature and annual precipitation. It is intended for batch extraction workflows that append WorldClim BIO1-BIO19 values to existing coordinate datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script reads coordinate files supplied on the command line. <br>
Mitigation: Run it only on files you intend to process and avoid placing unrelated sensitive data in the input workbook or CSV. <br>
Risk: The script can download large WorldClim raster archives from geodata.ucdavis.edu. <br>
Mitigation: In restricted environments, pre-download and verify the raster archives, then point the script at a dedicated cache directory. <br>
Risk: Python package and geospatial library versions can affect runtime behavior. <br>
Mitigation: Use a virtual environment and verify the documented dependencies before processing production datasets. <br>


## Reference(s): <br>
- [WorldClim 2.1 bioclimatic data base URL](https://geodata.ucdavis.edu/climate/worldclim/2_1/base) <br>
- [ClawHub release page](https://clawhub.ai/zd200572/worldclim-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash, Python, and R code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The provided script writes Excel or CSV files containing the original input columns plus extracted WorldClim BIO columns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
