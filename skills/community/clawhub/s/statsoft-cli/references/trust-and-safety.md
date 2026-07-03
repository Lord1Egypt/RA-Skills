# Trust & Safety 信任与安全

本技能执行**高风险操作**，使用前请了解风险等级 / This skill performs **high-risk operations**. Understand risk levels before use:

| 风险 / Risk | 等级 / Level | 说明 / Description |
|-------------|--------------|-------------------|
| 执行本地可执行文件 / Execute local executables | 🔴 高/High | Launches detected statistical software (e.g., `stats.exe`, `Rscript.exe`) |
| 下载与安装软件 / Download & install software | 🔴 高/High | Fetches R installer from CRAN, Anaconda installer from Anaconda repos |
| 修改 config.json / Modify config.json | 🟡 中/Medium | Writes software paths, backs up existing config |
| 设置环境变量 / Set environment variables | 🟡 中/Medium | Persists `STATSOFT_*` paths in user environment |
| 执行用户脚本 / Execute user-provided scripts | 🔴 高/High | Runs `.sps` content via SPSS Python, creating temporary wrapper scripts |
| 写入 MEMORY.md / Write to MEMORY.md | 🟡 中/Medium | Stores environment info in agent memory |
| 网络访问 / Network access | 🟡 中/Medium | Downloads installers from CRAN, Anaconda repositories |

**所需权限 / Permissions**: 本地文件读写 (config.json, temporary scripts)、进程执行 (statistical software binaries)、环境变量修改 (user-scoped)、网络访问 (CRAN/Anaconda repositories)。

**飞行前检查 / Pre-flight**: ✅ 审查所有脚本；✅ 确认 config.json 变更（自动备份）；✅ 确认任何下载任务；✅ 敏感项目需检查生成命令。
