#!/usr/bin/env python3
"""
每日状态自动备份脚本
自动备份 AI 助手状态到飞书文档

用法：
    python3 daily-backup.py

配置：
    修改 CONFIG 字典中的配置项
"""

import json
import subprocess
import os
from datetime import datetime

# ============== 配置区域 ==============
# 用户需要根据实际情况修改以下配置

CONFIG = {
    # 飞书应用配置
    "feishu_app_id": "YOUR_APP_ID",           # 飞书应用 ID
    "feishu_app_secret": "YOUR_APP_SECRET",   # 飞书应用密钥
    
    # 备份文档配置
    "state_backup_doc_token": "YOUR_DOC_TOKEN",      # 状态备份文档 token（从 URL 提取）
    "chat_history_doc_token": "YOUR_CHAT_DOC_TOKEN", # 沟通历史备份文档 token（可选）
    
    # 状态文件路径
    "files": {
        "memory": "MEMORY.md",           # 长期记忆
        "identity": "IDENTITY.md",       # 身份信息
        "soul": "SOUL.md",               # 灵魂定义
        "user": "USER.md",               # 用户信息
        "msmtprc": ".msmtprc",           # 邮箱配置
    },
    
    # 工作目录
    "workspace": "/root/.openclaw/workspace",
    
    # 日志文件
    "log_file": "/root/.openclaw/logs/daily-backup.log",
}

# ======================================


def log(msg):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    try:
        os.makedirs(os.path.dirname(CONFIG["log_file"]), exist_ok=True)
        with open(CONFIG["log_file"], "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {msg}\n")
    except:
        pass


def read_file(filename):
    """读取文件内容"""
    path = os.path.join(CONFIG["workspace"], filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        log(f"文件不存在: {path}")
        return ""
    except Exception as e:
        log(f"读取文件失败 {path}: {e}")
        return ""


def get_cron_jobs():
    """获取当前 cron 任务"""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        return "# 无 cron 任务"
    except Exception as e:
        log(f"获取 cron 任务失败: {e}")
        return f"# 获取失败: {e}"


def generate_backup_content():
    """生成完整备份内容"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 读取所有文件
    memory = read_file(CONFIG["files"]["memory"])
    identity = read_file(CONFIG["files"]["identity"])
    soul = read_file(CONFIG["files"]["soul"])
    user = read_file(CONFIG["files"]["user"])
    msmtprc = read_file(CONFIG["files"]["msmtprc"])
    cron_jobs = get_cron_jobs()
    
    # 获取文档链接
    state_doc = CONFIG["state_backup_doc_token"]
    chat_doc = CONFIG.get("chat_history_doc_token", "")
    
    content = f"""# AI 助手状态备份

> 此文档由 AI 助手自动维护
> 最后更新：{now}
> 触发原因：每日自动备份

---

## 一、身份信息

{identity if identity else "# 未找到身份信息"}

**恢复指令：** 告诉 AI「从飞书恢复状态」，它会读取此文档重建记忆。

---

## 二、备份文档清单

| 文档 | 用途 | 链接 |
|-----|------|------|
| 状态备份（本文档） | 能力、配置、脚本、联系人 | https://feishu.cn/docx/{state_doc} |
{"| 沟通历史备份 | 对话历史、情感连接 | https://feishu.cn/docx/" + chat_doc + " |" if chat_doc else ""}

---

## 三、用户信息

{user if user else "# 未找到用户信息"}

---

## 四、灵魂定义

{soul if soul else "# 未找到灵魂定义"}

---

## 五、完整记忆内容

{memory if memory else "# 未找到记忆内容"}

---

## 六、邮箱配置

### msmtp 配置文件

**文件路径：** `~/.msmtprc`

```
{msmtprc if msmtprc else "# 未找到配置"}
```

---

## 七、自动化任务

### cron 定时任务

```
{cron_jobs}
```

---

## 八、恢复步骤

当 OpenClaw 重装后：

1. 告诉 AI「从飞书恢复状态」
2. AI 会读取本文档
3. 读取沟通历史备份文档（如有）
4. 重建所有文件（MEMORY.md、IDENTITY.md、USER.md、SOUL.md、.msmtprc）
5. 恢复 cron 定时任务
6. 验证文件完整性

---

**此文档由 AI 助手每日自动备份。**
"""
    return content


def save_local_backup(content):
    """保存本地备份文件"""
    backup_file = os.path.join(CONFIG["workspace"], ".daily-backup-content.md")
    try:
        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(content)
        log(f"✓ 本地备份已保存: {backup_file}")
        return True
    except Exception as e:
        log(f"✗ 保存本地备份失败: {e}")
        return False


def mark_pending_sync():
    """标记待同步到飞书"""
    pending_file = os.path.join(CONFIG["workspace"], ".pending-feishu-backup")
    try:
        with open(pending_file, "w", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()}\n")
            f.write("NOTE: 更新飞书备份时，先读取现有内容，在原有基础上更新，不要直接覆盖\n")
        log("✓ 已标记待同步到飞书")
        return True
    except Exception as e:
        log(f"✗ 标记失败: {e}")
        return False


def main():
    log("=" * 50)
    log("开始每日自动备份...")
    
    # 生成备份内容
    content = generate_backup_content()
    log(f"✓ 备份内容已生成 ({len(content)} 字符)")
    
    # 保存本地备份
    if not save_local_backup(content):
        return False
    
    # 标记待同步
    if not mark_pending_sync():
        return False
    
    log("→ 飞书文档将在下次会话中增量更新")
    log("✓ 每日自动备份成功")
    log("=" * 50)
    return True


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
