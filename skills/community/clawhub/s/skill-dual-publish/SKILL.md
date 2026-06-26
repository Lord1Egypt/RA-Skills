---
name: skill-publish
version: 1.0.0
homepage: https://github.com/spikesubingrui-design/skill-dual-publish
clawhub_slug: skill-dual-publish
description: >-
  将 workspace/skills 下的新技能自动发布到 GitHub 与 ClawHub 双端口。
  在创建/更新 SKILL.md 后必须执行。ClawHub slug: skill-dual-publish。
  触发词：发布 skill / skill publish / 双端口发布 / publish to clawhub
---

# Skill 双端口发布（GitHub + ClawHub）

Spike 创建的每个 workspace skill **必须** 发布到两个端口：

| 端口 | 用途 |
|------|------|
| **GitHub** | 开源仓库、README、Star、版本历史 |
| **ClawHub** | `clawhub install <slug>` 一键安装 |

## 何时执行（强制）

在以下任一场景**完成后立即运行**（不要等用户提醒）：

1. 新建 `workspace/skills/<name>/SKILL.md` 并通过用户认可
2. 对已有 skill 做值得发布的版本更新
3. `skillify` 脚手架完成、stub 替换为真实内容后

## 一键命令

```bash
bash ~/.openclaw/workspace/scripts/skill-publish-dual.sh <skill-name>
```

示例：

```bash
bash ~/.openclaw/workspace/scripts/skill-publish-dual.sh human-distill
bash ~/.openclaw/workspace/scripts/skill-publish-dual.sh my-skill --bump patch -c "Fix triggers"
bash ~/.openclaw/workspace/scripts/skill-publish-dual.sh my-skill --slug my-unique-slug   # ClawHub 重名时
```

**必须用 skill 文件夹名或绝对路径。** ClawHub 对相对路径 `.` 会报 `SKILL.md required`——脚本已用绝对路径规避。

ClawHub slug 默认等于 `SKILL.md` 的 `name`；若被占用，在 frontmatter 加 `clawhub_slug:` 或传 `--slug`。

## 发布前检查清单

- [ ] `SKILL.md` 含 `name`、`version`、`description`（semver）
- [ ] `name` 与文件夹名一致（kebab-case）
- [ ] 首次发布 `version: 1.0.0`；更新用 `--bump patch|minor|major`
- [ ] `clawhub whoami` 已通过（一次性 `clawhub login`）
- [ ] `gh auth status` 已通过

## 选项

| 标志 | 作用 |
|------|------|
| `--dry-run` | 只打印计划 |
| `--skip-github` | 仅 ClawHub |
| `--skip-clawhub` | 仅 GitHub |
| `--no-scaffold` | 不自动生成 README/LICENSE |
| `--no-agents` | 不写 AGENTS.md skillpack 行 |

## 配置

默认：[`skill-publish.defaults.json`](../skill-publish.defaults.json)

本地覆盖（不提交 git）：`skills/skill-publish.local.json`

```json
{
  "github_owner": "spikesubingrui-design",
  "github_visibility": "public"
}
```

## 脚本自动完成

1. 补齐 `LICENSE` / `README.md`（若缺失）
2. `git init` → `gh repo create` → `git push`（若无远程）
3. 更新 `SKILL.md` 的 `homepage:` 为 GitHub URL
4. `clawhub publish <绝对路径> --slug ... --version ...`
5. 在 `AGENTS.md` skillpack 表追加一行（若尚无）

## 失败处理

| 错误 | 处理 |
|------|------|
| `Not logged in` | 用户本机执行 `clawhub login` |
| ClawHub 版本已存在 | `--bump patch` 后重跑 |
| `SKILL.md required` | 勿手写 `clawhub publish .`；用本脚本 |

## 与 skillify 的关系

`skillify` 第 11 步 = 本 skill。十项检查全绿后执行 `skill-publish-dual.sh`。
