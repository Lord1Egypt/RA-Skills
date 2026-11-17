## Description:

Helps Python developers configure Matplotlib to render Chinese text and minus signs by adding a Chinese font file, setting font family rcParams, and providing setup and test code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earl-chen](https://clawhub.ai/user/earl-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Matplotlib use this skill when Chinese titles, labels, legends, or minus signs render as boxes. It guides them to download or reference a Chinese font and apply reusable Python configuration in their plotting code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to download an external font file before configuration.

Mitigation: Verify the font source and license before use, and prefer a trusted project-local font file with an expected checksum when possible.

Risk: Server security guidance notes a syntax or legacy-code issue in references/plot_utils.py.

Mitigation: Prefer templates/setup_font.py for normal setup and review or test plot_utils.py before importing it into a project.

## Reference(s):

- [BabelStone Han font](https://www.babelstone.co.uk/Fonts/Han.html)
- [Matplotlib font manager API](https://matplotlib.org/stable/api/font_manager_api.html)
- [Matplotlib text tutorial](https://matplotlib.org/stable/tutorials/text/text_intro.html)
- [plot_utils.py](references/plot_utils.py)
- [test_chinese_font.py](references/test_chinese_font.py)
- [setup_font.py](templates/setup_font.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python and shell code snippets plus Python template and reference files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the user to provide or download a compatible Chinese font file and adjust project-relative font paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
