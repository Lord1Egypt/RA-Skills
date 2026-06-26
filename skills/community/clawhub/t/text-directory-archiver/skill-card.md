## Description: <br>
Package directory structures into a single plain text file, or restore directory structures from text files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turinfohlen](https://clawhub.ai/user/turinfohlen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to serialize project directories into portable text archives, restore those archives, and exchange multi-file project snapshots in environments where direct file transfer is inconvenient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpacking archives from untrusted text can write or remove local files and create symlinks. <br>
Mitigation: Use only trusted archives, unpack into a new empty temporary directory, and inspect the manifest before running the unpack command. <br>
Risk: Archive manifests may contain unsafe destinations such as absolute paths, parent-directory path segments, symlinks, executable files, or unexpected targets. <br>
Mitigation: Reject archives with absolute paths, '..' path segments, symlinks, executable files, or destinations outside the intended temporary directory, and review restored code before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/turinfohlen/text-directory-archiver) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with protocol examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python script can produce or consume plain text archive files representing directories, text files, base64-encoded binary files, and symlink records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
