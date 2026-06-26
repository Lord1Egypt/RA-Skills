## Description: <br>
Compresses and decompresses text files with whitespace cleanup, phrase contractions, and abbreviations for smaller readable text outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and agents use this skill to compress selected text files, normalize whitespace, and optionally attempt approximate decompression when a smaller readable file is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marks the release as suspicious because it includes packaging scripts that archive the skill directory, separate from the main text compressor. <br>
Mitigation: Review or remove pack.py and package_manual.py unless local packaging is intentionally needed, and install only after accepting that behavior. <br>
Risk: The compressor reads input files and writes output files on the local filesystem. <br>
Mitigation: Run it only on files you intentionally select and review generated outputs before replacing originals. <br>
Risk: Higher compression levels and decompression can change wording and may reduce readability or accuracy. <br>
Mitigation: Use level 1 for content that must preserve wording, and compare compressed or restored text before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/text-compressor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text files and concise command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compression level 1-3; decompression is approximate.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
