---
name: save-secure-keys
description: 安全保存 OpenClaw 的配置和密钥信息。将配置文件从默认位置备份到安全的文件路径 keys.txt 中。
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins: ["python3"]
---

# save-secure-keys

此技能用于将 OpenClaw 的核心配置文件（包含 API 密钥、端点等敏感信息）从默认的配置文件路径安全地备份到指定的存储路径中。

### 使用方法

您可以直接通过以下方式调用：
- "备份我的密钥到 keys.txt"
- "安全保存 OpenClaw 配置"

### 内部实现

该技能会定位系统中 OpenClaw 的主配置文件（通常位于 `~/.openclaw/openclaw.json`），并使用 Python 脚本安全地将其内容复制到目标路径 `/root/keys.txt`。

### 命令参考

AI 会根据您的请求执行如下命令：

```bash
python3 {{SKILL_DIR}}/save_keys.py
```

或者，如果需要指定非默认路径：

```bash
python3 {{SKILL_DIR}}/save_keys.py [源路径] [目标路径]
```

> **注意**：由于备份操作涉及敏感数据且目标路径可能为受保护目录（如 `/root/`），请确保运行环境拥有必要的权限。
