## Description: <br>
Watermark Pro helps agents add text or logo watermarks to images, Word documents, PowerPoint files, and PDFs with diagonal, centered, or tiled layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare local watermarking code and commands for image, Word, PowerPoint, and PDF files. It is useful when a user asks to add Chinese or English text watermarks, logo watermarks, or denser layout patterns to existing documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watermarking modifies document or media outputs and may overwrite important files if output paths are chosen carelessly. <br>
Mitigation: Use explicit output filenames, keep backups of originals, and review generated files before relying on them. <br>
Risk: The PDF workflow briefly writes a local _temp_wm.png file in the output directory. <br>
Mitigation: Run the workflow in a controlled output directory and verify temporary files are removed after processing. <br>
Risk: The skill depends on Python packages for image and document processing. <br>
Mitigation: Install only the listed packages from trusted package indexes and maintain normal dependency review practices. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the pillow, python-docx, python-pptx, and pymupdf Python packages; generated watermarked files are local outputs.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
