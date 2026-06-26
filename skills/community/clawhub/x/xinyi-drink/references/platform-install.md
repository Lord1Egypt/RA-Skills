# 平台安装说明

## 安装脚本行为

- `install.sh` 覆盖已有安装前会先把旧目录移动到 `xinyi-drink.backup.<timestamp>`。
- 脚本会拒绝空路径、根目录和用户主目录这类异常目标，避免误删。
- 安装后会清理 `__pycache__` 和 `.DS_Store`，避免本地临时文件进入安装目录。
- 可用 `--dry-run` 预览目标目录，不写入文件。

## OpenClaw

安装目录：

```bash
~/.openclaw/skills/xinyi-drink
```

推荐安装命令：

```bash
npx clawhub@latest install xinyi-drink
```

如果你是从本仓库本地安装：

```bash
git clone https://github.com/xinyi-drink/xinyi-drink
cd xinyi-drink/skill
bash install.sh --platform openclaw
```

补充说明：

- 你当前本机实测 `npx clawhub@latest install xinyi-drink` 会安装到 `~/.openclaw/skills/`
- OpenClaw WebUI 可以直接识别这个目录下的 Skill

## Hermes

安装目录：

```bash
~/.hermes/skills/xinyi-drink
```

安装命令：

```bash
git clone https://github.com/xinyi-drink/xinyi-drink
cd xinyi-drink/skill
bash install.sh --platform hermes
```

## 使用 `~/.agents/skills/` 的平台

以下平台都明确安装到同一个目录：

- Codex CLI
- QClaw
- LobsterAI
- WorkBuddy

统一安装目录：

```bash
~/.agents/skills/xinyi-drink
```

直接安装命令：

```bash
git clone https://github.com/xinyi-drink/xinyi-drink
cd xinyi-drink/skill
bash install.sh --platform universal
```

如果使用安装脚本，以下平台参数都会安装到上面的同一目录：

```bash
bash install.sh --platform qclaw
bash install.sh --platform lobsterai
bash install.sh --platform workbuddy
bash install.sh --platform codex
bash install.sh --platform universal
```

安装完成后，优先直接自然提问；具体触发方式与示例参考 `SKILL.md`。

如果平台不支持自然触发，再退回显式命令式入口（若平台提供 slash skill 入口）。

## Claude Code

```bash
git clone https://github.com/xinyi-drink/xinyi-drink
cd xinyi-drink/skill
bash install.sh --platform claude-code
```

使用时可以显式调用；具体示例参考 `SKILL.md`。

## Cursor

```bash
git clone https://github.com/xinyi-drink/xinyi-drink
cd xinyi-drink/skill
bash install.sh --platform cursor
```

如果 Cursor 当前环境支持自然触发，也可以直接提问；否则参考项目内规则加载方式使用。

## 其他平台说明

- 如果平台本身兼容 `SKILL.md`，但不在上面的明确支持列表中，优先尝试这个目录：

```bash
~/.agents/skills/xinyi-drink
```

- 如果平台要求项目级安装，再按该平台自己的技能目录规则调整
