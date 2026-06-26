# Skill Manage 🛠️

> 统一管理 OpenClaw 已安装 Skills：查看列表、检查更新、升级、卸载。

## 功能一览

| 命令 | 说明 |
|------|------|
| `list` | 扫描所有 Skill，列出名称/版本/来源/路径 |
| `info <name>` | 查看指定 Skill 详情 |
| `check [name]` | 检查更新（可指定单个或全部） |
| `update <name>` | 从对应来源升级指定 Skill |
| `uninstall <name>` | **彻底卸载**（扫描残留 + 凭证提示 + Dry Run） |
| `search <keyword>` | 在 SkillHub 搜索 Skills |
| `install <name>` | 从 SkillHub / GitHub 安装 Skill |

## 安装

```bash
# 从 GitHub 克隆
git clone https://github.com/andy8663/skill-manage.git
```

或直接下载 `scripts/skill_manage.py`，放入你的 skill-manage 目录下。

## 来源识别

| 来源 | 判断依据 | 更新方式 |
|------|----------|----------|
| **GitHub** | 目录下有 `.git` | `git pull` |
| **SkillHub** | 有 `_meta.json` | `skillhub install <slug>` |
| **Config** | 有 `config.json` | 随 QClaw 版本更新 |
| **Local** | 其他本地 Skill | 无自动更新路径 |

## 彻底卸载功能

`uninstall` 命令在删除主目录前会先**扫描残留痕迹**，包括：

- ✅ SkillHub 锁文件记录（从 `skillhub.lock.json` 移除）
- ✅ 配置文件（config.json / .env / .yaml）
- ✅ 缓存目录（cache/、TMP/、__pycache__/）
- ✅ workspace 中的残留文件
- ✅ OpenClaw 主配置引用

**凭证保护**：检测到 config.json 含敏感信息时，额外警告，可选择仅清理残留保留凭证文件。

```bash
# Dry Run - 先看不动
python scripts/skill_manage.py uninstall <name> --dry-run

# 跳过确认直接卸载
python scripts/skill_manage.py uninstall <name> --force
```

## 示例

```bash
# 查看所有已安装 Skills
python scripts/skill_manage.py list

# 检查所有 Skills 是否有更新
python scripts/skill_manage.py check

# 检查单个 Skill
python scripts/skill_manage.py check wechat-oa

# 升级指定 Skill
python scripts/skill_manage.py update wechat-oa

# 搜索 SkillHub
python scripts/skill_manage.py search wechat

# 安装 Skill（从 SkillHub）
python scripts/skill_manage.py install wechat-oa

# 彻底卸载（含残留扫描）
python scripts/skill_manage.py uninstall old-skill --dry-run
```

## 依赖

- Python 3.x
- 标准库：`argparse`, `pathlib`, `json`, `subprocess`, `shutil`, `urllib`, `datetime`
- 无第三方依赖

## License

MIT
