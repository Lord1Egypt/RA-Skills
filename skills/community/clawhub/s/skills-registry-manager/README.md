# Skill Registry Manager

一个 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill，用于管理和安装其他 Claude Code skills。

维护一份常用 skills 注册表（`registry.yaml`），支持订阅远程或本地注册表，便于共享和分发 skills 列表。

## 功能

- 列出所有已注册的 skills 及其安装状态
- 支持通过编号或名称选择安装
- 支持全局安装（`~/.claude/skills/`）和项目级安装（`.claude/skills/`）
- 自动解析和安装依赖的 skills
- 支持三种安装来源：`npx`、`git`、`local`
- **订阅管理**：添加、列出、删除注册表订阅
- **嵌套订阅**：注册表可递归引用其他注册表（本地和远程可混用）
- **路径解析**：支持环境变量（`$HOME`、`$HOSTNAME`）、`~` 展开和相对路径

## 安装

```bash
# 通过 npx 安装（推荐）
cd ~/.claude/skills && npx skills add gavinyao/skill-registry-manager -y -g

# 或手动复制
cp -r . ~/.claude/skills/skill-registry-manager

# 或使用符号链接
ln -s $(pwd) ~/.claude/skills/skill-registry-manager
```

## 使用

在 Claude Code 中直接说：

- "列出可用 skills" / "有哪些 skills"
- "安装 skill-creator" / "装一下 xxx skill"
- "管理 skills"
- "添加订阅" / "订阅 xxx URL"
- "列出订阅" / "查看订阅"
- "删除订阅" / "取消订阅 xxx"

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | Skill 定义文件，Claude Code 自动加载 |
| `registry.yaml` | 注册表配置，定义可安装的 skills 和订阅 |
| `registry.example.yaml` | 完整配置示例，涵盖所有场景 |

## 注册表格式

`registry.yaml` 采用统一的 YAML 格式（完整示例见 [`registry.example.yaml`](registry.example.yaml)）：

```yaml
# 订阅其他注册表（支持递归加载，本地和远程可混用）
subscriptions:
  - name: upstream
    url: https://example.com/skills-registry.yaml
  - name: local-shared
    url: $HOME/shared-skills/registry.yaml
  - name: team
    url: ~/team/skills-registry.yaml

# 本地 skills 列表
skills:
  - name: example-skill
    description: 示例 skill
    source: npx
    install: "npx skills add owner/repo@skill-name -y -g"
    repo: https://github.com/owner/repo  # 可选，展示为链接
    depends: []                           # 可选，依赖的其他 skill

  - name: local-skill
    description: 本地 skill
    source: local
    install: ./local-skill  # 相对路径，基于注册表文件所在目录
```

### 来源类型

| 类型 | 说明 | `install` 字段 |
|------|------|----------------|
| `npx` | 通过 npx 运行安装命令 | npx 命令 |
| `git` | 克隆 git 仓库 | 仓库 URL |
| `local` | 复制本地目录 | 本地路径（支持环境变量和相对路径） |

### 路径格式

`url`（订阅）和 `install`（local source）字段支持以下路径格式：

| 格式 | 示例 |
|------|------|
| 环境变量 | `$HOME/path/to/file.yaml` |
| `~` 简写 | `~/path/to/file.yaml` |
| 绝对路径 | `/absolute/path/to/file.yaml` |
| 相对路径 | `./relative/path`（基于注册表文件所在目录） |

### 多机器共享

通过订阅机制，可以构建分层的注册表结构，实现多机器共享和本机定制：

```
skill-registry/registry.yaml          ← 入口
├── shared-registry                   ← 多机器共享注册表（通过 dotfiles 同步）
│   ├── skill-creator
│   ├── find-skills
│   └── 订阅 team-skills              ← 团队 skills
└── host-registry                     ← 本机专属（按需定制）
    └── (特定于本机的 skills)
```

## License

[MIT](LICENSE)
