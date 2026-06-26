# Wangcut Skill 安装指南

本文档说明如何在 Claude Code / OpenClaw 中安装和使用 Wangcut 视频剪辑 Skill。

## 前置要求

- Claude Code 或 [OpenClaw](https://openclaw.ai)
- Python 3.8+
- 依赖: `pip install requests`

---

## 安装方式

### 方式一：Claude Code（本地安装）

将 skill 复制到 Claude Code 的 skills 目录：

```bash
# 复制到全局 skills 目录
cp -r .claude/skills/wangcut ~/.claude/skills/
```

### 方式二：OpenClaw 工作区 Skills（推荐）

将 skill 放在项目的 `/skills` 目录，仅对当前工作区生效：

```
你的项目目录/
└── skills/
    └── wangcut/
        ├── SKILL.md
        ├── config.example.ini
        ├── docs/
        │   └── INSTALL.md
        └── scripts/
            └── wangcut_api.py
```

### 方式三：OpenClaw 全局 Skills

将 skill 放在用户目录，所有工作区可用：

```
~/.openclaw/skills/
└── wangcut/
    ├── SKILL.md
    ├── config.example.ini
    └── scripts/
        └── wangcut_api.py
```

### 方式四：ClawHub 安装（推荐）

从 ClawHub 一键安装（即将上线）：

```
/openclaw install wangcut
```

---

## 配置账号

### 自动配置（推荐）

首次使用时会自动检测配置状态，按提示提供账号密码：

```
⚠️ 旺剪配置异常: 账号密码未配置
请提供账号密码进行配置，格式：账号 158xxx 密码 xxx
```

或主动说：**"配置旺剪账号 158xxx 密码 xxx"**

### 手动配置

在项目根目录创建 `config.ini`：

```ini
[wangcut]
username = 15812345678
password = your_password
base_url = https://cloud.qinsilk.com/aicut/api/v1
folder_id =
download_dir = ./downloads

[task_defaults]
voice_type = f_liuyuxi_20251009
voice_speed = 1.3
resolution_width = 1080
resolution_height = 1920
subtitle_enabled = true
subtitle_font_color = yellow
music_enabled = true
music_volume = 0.4
```

---

## 验证安装

```python
import sys
sys.path.insert(0, '.claude/skills/wangcut/scripts')
from wangcut_api import check_config, get_config_status_message

# 检查配置状态
print(get_config_status_message())
# 输出: ✅ 旺剪账号已配置
```

---

## 使用示例

### 创建视频

```
/wangcut 创建一个视频，文案：良心是什么...
```

### 查看任务

```
/wangcut 查看最近的视频任务
```

### 下载视频

```
/wangcut 下载最新的视频到本地
```

---

## Skills 加载优先级

| 优先级 | 位置 | 作用域 |
|-------|------|--------|
| 1 (最高) | `/skills/` | 当前工作区 |
| 2 | `~/.openclaw/skills/` | 当前用户 |
| 3 | ClawHub 安装 | 当前用户 |

---

## 安全注意事项

- `config.ini` 包含敏感信息，**请勿提交到版本控制**
- 添加到 `.gitignore`:
  ```
  config.ini
  downloads/
  __pycache__/
  ```

---

## 故障排除

### Skill 未加载

1. 检查目录结构是否正确
2. 确认 `SKILL.md` 格式正确（YAML frontmatter）
3. 重启 Claude Code / OpenClaw 会话

### API 调用失败

1. 检查账号密码是否正确
2. 确认网络连接正常
3. 查看错误提示，按引导重新配置

### 导入错误

```bash
pip install requests
```

---

## 相关链接

- [秦丝旺剪官网](https://cloud.qinsilk.com)
- [OpenClaw Skills 文档](https://docs.openclaw.ai/tools/skills)
- [ClawHub](https://clawhub.com)
