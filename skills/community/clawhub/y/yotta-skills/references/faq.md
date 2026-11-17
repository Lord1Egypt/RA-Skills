# 元阁常见问题

## 速查索引

- **安装目标**：未指定目标怎么办 · 支持哪些智能体 · 装完为什么看不到
- **网络与源**：国内访问慢 · 镜像延迟 · 网络失败
- **更新**：`update --check` 退出码 · 后台周检缓存 · 自动更新边界 · 幂等
- **版本**：默认 `--pin` 与 `--range` · 清单漂移 · 单技能安装
- **安全**：装前扫描 · 目标目录校验 · 失败恢复
- **授权**：会不会自动装技能 / 自动写全局记忆 / 自动改 MCP 配置

---

## 1. 安装时提示「未指定目标」怎么办？

这表示当前目录没有检测到项目级技能目录。两种解决方式：

```bash
npx -y @yottameta/yotta-skills --agent codex
npx -y @yottameta/yotta-skills --dir /path/to/skills
```

`--agent` 使用内置智能体默认目录；`--dir` 适合自定义目录或未收录智能体。

## 2. 支持哪些智能体？

内置 17 个键名：`claude`、`cursor`、`codex`、`gemini`、`goose`、`amp`、`opencode`、`windsurf`、`workbuddy`、`kiro`、`trae`、`trae-cn`、`qwen`、`comate`、`codebuddy`、`kimi`、`agents`。未收录的智能体用 `--dir` 指定目录。

## 3. 国内访问 npm 慢或失败怎么办？

可用 `YOTTA_SKILLS_NPM_FLAGS` 追加 registry 参数：

```bash
YOTTA_SKILLS_NPM_FLAGS="--registry=https://registry.npmmirror.com" npx -y @yottameta/yotta-skills --agent codex
```

新版本发布后镜像可能有延迟；如需立即获取，可临时改回 npm 官方源并配置代理。

## 4. `update --check` 的退出码是什么意思？

- `0`：全部最新
- `3`：存在可更新技能
- `1`：检查失败（网络或 registry 异常）

该命令只读，不修改文件。

## 4.1 `update --check --scheduled` 什么时候用？

它是后台周检入口：默认 7 天加 0 到 24 小时随机抖动，未到期不联网；到期只检查一次，
结果写入 `~/.yottaskills/update-check.json`。文本模式网络失败静默并退出 0，
`--json` 可读取 `error` / `cache` 诊断字段。会话开工只建议做本地 `--reindex`，
不默认联网更新检查。

## 5. `update --auto` 会更新所有技能吗？

只自动更新元阁家族内技能（`yotta-*` 且在清单中）。其他已装技能只提示，不自动改动。

## 6. 重复安装会重复占空间吗？

不会。默认按清单版本判断，已一致的技能跳过；需要强制覆盖时加 `--force`。

## 7. `--pin` 和 `--range` 怎么选？

默认是 `--pin`：按清单精确版本安装，完全可复现、不会静默跟随浮动版本。
只有你明确想跟随同 major 的最新 patch 时才加 `--range`。

## 8. 为什么清单和文档版本会不一致？

人工文档可能滞后。机器权威源是 `skills.json`，人工可读副本是 `references/skill-list.md`；当前版本已加入自动测试，两者不一致会导致测试失败。

## 9. 如何只安装部分技能？

```bash
npx -y @yottameta/yotta-skills install yotta-memory yotta-workflow --agent codex
```

也可以先用 `--route` 查看建议组合，再按需安装。

## 10. 安装前安全扫描怎么用？

家族安装默认执行元信门禁：没有元信时先自动自举，再扫描待装包。`DO NOT INSTALL`
和扫描失败会阻断；`INSTALL WITH CAUTION` / `REVIEW REQUIRED` 会继续但显示风险。
可用 `--verify <path>` 指定引擎。`--skip-scan` 只是人工应急路径，会标记
`explicit-unverified`，`update --auto` 不使用它。

## 11. 安装失败后如何恢复？

查看汇总中的失败原因。setup / doctor 失败时元阁会自动恢复旧版本；旧版本快照仍保存在
`~/.yottaskills/snapshots/`。可以先用 `doctor` 自检，再用 `rollback` 恢复最近快照：

```bash
npx -y @yottameta/yotta-skills doctor --dir /path/to/skills --slug <slug>
npx -y @yottameta/yotta-skills rollback --list --dir /path/to/skills
npx -y @yottameta/yotta-skills rollback --slug <slug> --dir /path/to/skills
```

如果只是安装源或网络问题，再单独安装失败技能：

```bash
npx -y @yottameta/yotta-skills install <slug> --dir /path/to/skills
```

## 12. 装完为什么智能体里看不到？

确认安装目录与智能体实际读取目录一致；安装后通常需要重启会话或重新加载技能列表。

## 13. `hook evaluate` 会真的拦截动作吗？

不一定。适配层先探测宿主能力：`native-block` 才能声明动作前阻断；`native-audit` 只能审计并触发一次纠偏，结果会标记 `explicit-unverified`；`wrapper-only` 仅在 wrapper 注册后保证；未知宿主全部按 `unsupported` 处理。当前 Codex 已实测能力见 `hook capabilities --host codex`。

## 14. 元阁会自动安装技能、写全局记忆或改 MCP 配置吗？

不会。元阁只给建议：`--route` 输出缺失技能与安装命令，安装动作由你执行或确认后才发生；
写客户端 `mcpServers` 配置、把编排护栏写进全局记忆（如 `AGENTS.md` / `CLAUDE.md`）都需要**事先明确同意**，
并会先展示目标文件与完整文本。你拒绝写入时，元阁不写任何文件，直接以 CLI 方式继续工作。

## 15. `decide-memory` 会替我删除技能或写记忆吗？

不会。`decide-memory` 默认只读，输出 `promote / hold / demote` 建议、分数与信号明细；
`--promote` 只写本地 `~/.yottaskills/memory-adjudication.json` 建议文件，并生成私密 `PREF` 记忆候选。
元忆写入由你或 AI 再显式调用元忆完成；技能本体与记忆都不会被自动删除。

## 16. `usage` 会记录我的需求原文吗？

不会。使用记录默认关闭；执行 `usage enable` 后才记录 `--route` 的结构化 route_hits 与组合对。
记录只含技能 slug、时间、信号类型、playbook / confidence 与组合对，不含需求原文、记忆正文、路径或身份信息。
`usage disable` 停止记录，`usage reset --yes` 清空记录。
