## Description: <br>
xiaoqianran-duck helps agents use DuckDB to import, query, preview, and export local files and Hugging Face datasets through a CLI, Node.js helper, preview server, and Rust backend examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoqianran](https://clawhub.ai/user/xiaoqianran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to add local analytical data exploration with DuckDB, including imports from CSV, TSV, JSON, Parquet, Excel, and Hugging Face datasets, SQL querying, exports, and desktop app integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read selected local files and create or modify a local DuckDB database. <br>
Mitigation: Run it only on data the operator is authorized to process and review file paths before import, export, or query operations. <br>
Risk: The preview server exposes browser-driven SQL execution against the local DuckDB database. <br>
Mitigation: Use the preview server only on trusted machines and data; bind it to localhost, add access controls when shared, and restrict queries to safe read-only usage. <br>
Risk: Hugging Face tokens may be loaded from environment variables or a nearby .env file. <br>
Mitigation: Use least-privilege tokens, keep .env files out of commits, and avoid running with tokens that grant unnecessary access. <br>
Risk: Hugging Face dataset access and DuckDB extension loading can use network access. <br>
Mitigation: Review outbound network expectations and run in an environment where Hugging Face and DuckDB extension access are permitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoqianran/skills/xiaoqianran-duck) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoqianran) <br>
- [Skill README](artifact/skills/xiaoqianran-duck/README.md) <br>
- [Skill definition](artifact/skills/xiaoqianran-duck/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local filesystem paths, DuckDB database files, Hugging Face dataset URLs, and environment variables such as HF_TOKEN.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
