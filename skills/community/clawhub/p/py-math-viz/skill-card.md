## Description: <br>
Py Math Viz helps agents create clear Python math and data visualizations as PNG files using matplotlib/seaborn, with helpers for JSON-driven plots, image tiling, and optional OpenCV post-processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rokokol](https://clawhub.ai/user/rokokol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to turn math functions, CSV data, simulation outputs, model comparisons, and weather data into readable PNG plots and tiled image summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional weather rendering sends latitude, longitude, and timezone to Open-Meteo when scripts/weather.py is run. <br>
Mitigation: Run the weather helper only when that data sharing is intended, and review the command arguments before execution. <br>
Risk: Plot and tiling scripts read local JSON, CSV, and image paths and write output files. <br>
Mitigation: Use trusted input files, keep generated outputs in a dedicated out/ directory, and review generated specs or shell commands before running them. <br>
Risk: Generated visualizations can mislead if the input data, labels, or plot specification are wrong. <br>
Mitigation: Check source data, axes, units, legends, and titles before using plots in decisions or publications. <br>


## Reference(s): <br>
- [Py Math Viz ClawHub page](https://clawhub.ai/rokokol/py-math-viz) <br>
- [Plot spec](references/spec.md) <br>
- [Quick recipes](references/quick-recipes.md) <br>
- [JSON spec recipes](references/recipes-spec-json.md) <br>
- [Seaborn snippet recipes](references/recipes-seaborn-snippets.md) <br>
- [Image tiling recipes](references/recipes-images.md) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with JSON specs, Python snippets, shell commands, and PNG file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PNG plots and tiled images; optional weather rendering can also print a short text summary.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
