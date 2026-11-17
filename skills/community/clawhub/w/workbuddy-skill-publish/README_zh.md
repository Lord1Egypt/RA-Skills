# Skill Publish

审计、清理并发布 Agent Skill 到 ClawHub 和 GitHub。适用于 OpenClaw 生态中任何基于 SKILL.md 的 skill。

与 `skill-design-guide`（设计阶段）配合。

**版本**: v1.5.7（2026-09-16）

> ⚠️ **发布模式有外部副作用。** 审计模式为只读。发布模式会把清理后的 skill 内容传输到
> ClawHub 和 GitHub（公开服务）。捆绑的同步脚本只创建或更新文件——从不删除你的仓库或本机的
> 任何内容，也不修改本地文件。发布仅在完成审计并经你明确确认文件清单、目标仓库和版本后执行。
> 凡发布的内容都应视为公开可见。

## 模式

| 模式 | 触发词 | 说明 |
|------|--------|------|
| **审计** | "检查发布" / "audit skill" | 只读扫描，报告问题，不改动文件、不传输任何内容 |
| **发布** | "发布 skill" / "publish skill" | 审计并经确认后：在临时副本中清理 → 推送到 ClawHub/GitHub → 验证 |

## 检查项

1. **个人数据** — 持仓数量、成本价、账户金额、个人姓名
2. **Frontmatter** — 描述长度、语言、名称中的版本号
3. **内容** — 内部开发备注、参考章节、版本历史
4. **语言** — SKILL.md 英文主体、README 中英双语
5. **文件** — 个股脚本、元文档、过期文件

## 快速开始

```
# 审计一个 skill 目录
"检查发布 ~/.workbuddy/skills/my-skill"

# 发布到 ClawHub + GitHub
"发布 skill ~/.workbuddy/skills/my-skill@1.2.0"
```

## 捆绑脚本

`scripts/sync_skill_to_github.js` — 可选辅助脚本，把 publish 目录镜像同步到 GitHub 仓库（Contents API）。

- Token：仅从 `GITHUB_TOKEN` / `GITHUB_PAT` 环境变量读取，未设置时报错退出。不内置、不读文件、不打印日志。
- 网络：仅访问 `api.github.com`。只创建/更新文件（PUT），**从不删除**远端文件。
- 全参数化：`--owner`、`--repo`、`--dir`、`--message`、`--branch`、`--files`。无硬编码路径或用户名。

```bash
node scripts/sync_skill_to_github.js --owner <you> --repo <skill-repo> --dir ./publish-my-skill
```

## License

MIT
