# statsoft-cli — 进阶参考（开发者）

本文件收录普通用户无需关心的技术细节。日常使用请见 [README_zh-CN.md](README_zh-CN.md)。

## 平台支持

### 核心软件

| 软件 | Windows 脚本 | 跨平台脚本 | 验证 |
|---|---|---|---|
| SPSS Statistics | `scripts/windows-only/SPSS/setup_spss.ps1` | — | `stats.com -production silent -nologo "exit.spj"` |
| R | `scripts/windows-only/statsoft-r.ps1` | `scripts/cross-platform/R/setup_r.sh` | `Rscript --version` |
| Stata | — | `scripts/cross-platform/Stata/setup_stata.sh` | `stata-mp -b do "exit"` |
| SAS | `scripts/windows-only/statsoft-sas.ps1` | `scripts/cross-platform/SAS/setup_sas.sh` | `sas -version` |

（全部扩展软件包的完整路由表 — 详见 `ADDITIONAL_SOFTWARE.md`。）

## 目录结构

```
statsoft-cli/
├── SKILL.md
├── README.md / README_zh-CN.md
├── ADVANCED.md / ADVANCED_zh-CN.md
├── ADDITIONAL_SOFTWARE.md
├── LICENSE
├── config.json.example
├── scripts/
│   ├── cross-platform/   (_platform-detect.sh、scan/scan_all.sh、各工具 setup_*.sh)
│   └── windows-only/     (scan/scan_all.ps1、各工具 setup_*.ps1、statsoft-r.ps1、statsoft-sas.ps1)
├── references/           (command-examples.md、version-specifics.md、completion-prompts.md、config-templates.md、workflow.md、platform-support.md、trust-and-safety.md)
├── tests/
└── assets/icon.svg
```

## 激活边界与使用方式

本技能仅在**明确、限定范围的请求**下激活，且必须指名目标软件与动作（例如「配置 R」「运行 Stata <文件>」「将 data.sav 转为 data.dta」）。诸如「配置统计软件」这类宽泛表述不会自动触发高风险执行。

触发示例（需指名软件/动作）：
- 帮我关联 SPSS 26
- 配置 R 统计软件
- 将 data.sav 转换为 data.dta
- 运行 Stata .do 文件（批处理模式）

非触发示例（视为普通对话，不激活）：
- 我读了一篇关于 R 的论文
- 能给我讲讲 Stata 是什么吗？

## 授权与持久化模型

- opt-in 开关（`STATSOFT_AUTO_WRITE` / `STATSOFT_CONFIRM`）由**用户预先设置**；本技能**只读取、绝不写入**这些开关或任何其它环境变量。
- 本技能**唯一可能持久化的文件**是它自身目录下的 `config.json`，且**仅在显式 opt-in 之后**才写入（写入前备份为带时间戳的 `config.json.bak.*`；删除 `config.json` 即可完全回滚）。
- 本技能**不写入** `~/.workbuddy/MEMORY.md` 或任何技能目录以外的位置。

## 信任与安全（详情）

本技能执行高风险操作，使用前请了解风险等级：

| 风险 | 等级 |
|---|---|
| 执行本地可执行文件 | 🔴 高 |
| 下载并安装软件 | 🔴 高 |
| 执行用户脚本（如经 SPSS Python 运行 `.sps`） | 🔴 高 |
| 修改 config.json | 🟡 中 |
| 联网访问 | 🟡 中 |

**飞行前检查**：✅ 审阅全部脚本；✅ 确认 config.json 变更（自动备份）；✅ 确认任何下载；✅ 检查生成的命令是否涉及敏感项目。

各软件 CLI 命令示例：见 `references/command-examples.md`。
