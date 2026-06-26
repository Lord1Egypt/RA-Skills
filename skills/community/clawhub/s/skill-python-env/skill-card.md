## Description: <br>
Provides an internal Python virtual environment manager for other OpenClaw skills, creating shared versioned environments under ~/.python_env and installing uv automatically when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this internal helper when a skill needs a reusable Python runtime. It creates or reuses a requested Python version, optionally installs packages, and emits machine-readable environment paths for the calling skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically run remote installer code to install uv. <br>
Mitigation: Preinstall uv through an approved channel or review the installer source before allowing automatic installation. <br>
Risk: Shared mutable Python environments under ~/.python_env can be changed by any skill that calls this helper. <br>
Mitigation: Install only when trusted skills can call it, and treat each shared environment as mutable state that may affect multiple skills. <br>
Risk: Calling skills can request arbitrary package names for installation into the shared environment. <br>
Mitigation: Restrict or pin allowed package names and versions before using this helper in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liberalchang/skill-python-env) <br>
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/) <br>
- [uv Unix installer script](https://astral.sh/uv/install.sh) <br>
- [uv Windows installer script](https://astral.sh/uv/install.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text logs with machine-readable environment path lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emits PYTHON_ENV_ACTIVATE, PYTHON_ENV_DIR, and PYTHON_ENV_VERSION lines for caller parsing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
