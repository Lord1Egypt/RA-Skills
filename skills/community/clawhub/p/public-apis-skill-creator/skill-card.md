## Description: <br>
Finds free public APIs from the public-apis catalog, recommends options by task, generates curl, Python, and JavaScript examples, and can create a named API skill scaffold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[547895019](https://clawhub.ai/user/547895019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search for public APIs, compare authentication, HTTPS, and CORS details, generate minimal calling examples, and optionally scaffold a new API-focused skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent runnable skills from public API catalog data. <br>
Mitigation: Inspect the selected API entry and review the generated SKILL.md and scripts before running or publishing the generated skill. <br>
Risk: Generated skill names and API-derived content may overwrite or create unexpected workspace files. <br>
Mitigation: Use unique skill names, choose an explicit output directory when possible, and check the target directory before generation. <br>
Risk: The skill contacts GitHub, caches the public API list, and can probe selected external URLs. <br>
Mitigation: Run it only where those network calls are acceptable, use probing only for inspected APIs, and clear or review the cache when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/547895019/public-apis-skill-creator) <br>
- [public-apis catalog content endpoint](https://api.github.com/repos/public-apis/public-apis/contents/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, and JavaScript examples; optional generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch and cache the public-apis list, probe selected external URLs when requested, and write generated skill scaffolds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
