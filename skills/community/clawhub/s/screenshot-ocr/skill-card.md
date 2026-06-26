## Description: <br>
Screenshot OCR recognizes text from screenshots or image files and can copy or save the recognized text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill to extract Chinese, English, numeric text, and simple table content from screenshots, clipboard images, or local image files. It is useful when text in an image needs to be copied, reviewed, or saved as a TXT file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR can expose sensitive screenshot or clipboard text in the terminal, clipboard, or saved TXT files. <br>
Mitigation: Avoid processing passwords, private messages, payment details, or verification codes unless disclosure is intended, and delete saved outputs when finished. <br>
Risk: The skill depends on a local Python OCR script and local Tesseract, pytesseract, and Pillow installations. <br>
Mitigation: Install runtime dependencies only from trusted package sources and review the local script before execution. <br>


## Reference(s): <br>
- [Screenshot Ocr on ClawHub](https://clawhub.ai/SxLiuYu/screenshot-ocr) <br>
- [SxLiuYu ClawHub Profile](https://clawhub.ai/user/SxLiuYu) <br>
- [Tesseract Windows Installer Reference](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text output with optional TXT file output and clipboard copy] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OCR through Tesseract, pytesseract, and Pillow; can read clipboard images and write recognized text to a user-specified file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
