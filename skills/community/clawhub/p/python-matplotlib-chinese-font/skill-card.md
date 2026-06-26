## Description: <br>
Configures Matplotlib to display Chinese text by adding a local Chinese font file, setting the active font family, and disabling Unicode minus rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earl-chen](https://clawhub.ai/user/earl-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill when Matplotlib charts render Chinese labels, titles, legends, or minus signs incorrectly. It provides setup guidance, reusable Python helpers, and test code for project-local Chinese font configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks users to download and use an external font file. <br>
Mitigation: Verify the font source and license before installing or redistributing the font with a project. <br>
Risk: The test script writes a local test_chinese_font.png file when executed. <br>
Mitigation: Run examples in a project or temporary directory where generated image output is expected. <br>
Risk: One optional helper file may contain a syntax issue according to the server security guidance. <br>
Mitigation: Prefer the setup_font.py template or inspect and test helper code before copying it into a project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earl-chen/python-matplotlib-chinese-font) <br>
- [BabelStone Fonts](https://www.babelstone.co.uk/Fonts/Han.html) <br>
- [Matplotlib Font Management](https://matplotlib.org/stable/api/font_manager_api.html) <br>
- [Matplotlib Text Introduction](https://matplotlib.org/stable/tutorials/text/text_intro.html) <br>
- [plot_utils.py](references/plot_utils.py) <br>
- [test_chinese_font.py](references/test_chinese_font.py) <br>
- [setup_font.py](templates/setup_font.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or recommend local Python helper files and a test_chinese_font.png validation image when example scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
