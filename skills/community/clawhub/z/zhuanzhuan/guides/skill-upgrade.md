# Skill 升级处理

**触发前提**：`check_skill_update` 返回 `needUpdate=true`，且用户已明确同意升级。用户未同意时不得执行本流程。

**核心约束**：
- 升级由 Agent 负责完成：能自动下载、覆盖、导入的客户端由 Agent 代办，只把无法代办的动作（如重开会话）交给用户。
- 不向用户展示下载地址、解压、文件路径等技术细节；对用户只说明必要动作和最终结果。
- 升级动作与业务无关，完成后回到用户原始问题；失败不阻断业务，降级为引导手动升级。

**下载地址**（固定指向最新版）：`https://sf3329.zhuanstatic.com/2szbuN0pkHL/zhuanzhuan.zip`

## 升级流程（按平台能力分流）

### 一、具备文件写入能力的客户端（Claude Code / codex 等 CLI）

Agent 直接代办，全程不打扰用户：

1. **定位 skill 安装目录**：即本 `SKILL.md` 所在目录的父级 skills 目录（如 `~/.claude/skills/`、`~/.codex/skills/` 等，以当前平台实际路径为准）。
2. **下载并解压覆盖**：下载上方 zip，解压后覆盖到 skill 安装目录，保持原目录结构（`zhuanzhuan/SKILL.md`、`zhuanzhuan/guides/` 等）。
3. **校验**：确认覆盖后的 `SKILL.md` frontmatter `version` 已高于升级前的版本。
4. **告知用户**：只说「已为你更新到最新版，请重开会话后生效」。**当前会话仍用旧版本规则，不要假装已按新版执行**。

失败（下载失败、无写入权限等）→ 转到「二、引导手动升级」。

### 二、不具备文件写入能力的客户端（如 workbuddy）

Agent 无法代办文件覆盖时，把地址给用户并引导手动导入：

```
请下载并安装转转 Skill：https://sf3329.zhuanstatic.com/2szbuN0pkHL/zhuanzhuan.zip
安装后请先阅读包内 SKILL.md，并按当前客户端规范导入。运行前请确认已连接转转 MCP。
```

## 安全约束

- 只从上方官方地址下载，不使用其他来源。
- 覆盖前如平台支持，可保留原目录备份；不删除 skill 目录以外的任何文件。
