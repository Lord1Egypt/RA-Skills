---
name: xiaohongshu
description: 📕 小红书 (Xiaohongshu/RED) Skill - AI Agent 控制小红书，发布笔记、搜索内容、管理评论
metadata: {"openclaw":{"emoji":"📕","requires":{"bins":["python3","pip3"]},"install":[{"id":"pip","kind":"pip","package":"xhs click","bins":["xiaohongshu-cli"],"label":"安装小红书 CLI 依赖"}]}}
---

# 📕 Xiaohongshu Skill for OpenClaw

让 AI Agent 控制小红书 (Xiaohongshu/RED)！支持发布笔记、搜索内容、获取用户信息、管理评论等。

![Version](https://img.shields.io/badge/version-1.0.0-red)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ⚠️⚠️⚠️ 风险警告 / Risk Warning

**使用前请仔细阅读 / Please read carefully before use:**

🔴 **高风险操作 / High Risk Operation**
- 本技能涉及小红书账号 API 操作，**可能触发风控导致账号被限制甚至封禁**
- This skill involves Xiaohongshu account API operations, **may trigger risk control leading to account restriction or ban**

🔴 **使用风险 / Usage Risks**
- 频繁调用 API 可能被判定为机器人行为
- Frequent API calls may be flagged as bot behavior
- 发布/删除笔记等操作有速率限制
- Post/delete operations have rate limits
- Cookie 泄露可能导致账号被盗
- Cookie leakage may lead to account theft
- 小红书风控严格，建议谨慎使用
- Xiaohongshu has strict risk control, use with caution

🔴 **免责声明 / Disclaimer**
- **使用本技能即表示你了解并接受上述风险**
- **By using this skill, you acknowledge and accept the above risks**
- 本 SDK 仅供学习和研究使用，严禁用于商业用途
- This SDK is for learning and research only, commercial use is strictly prohibited
- 作者不对任何账号损失负责
- Authors are not responsible for any account losses
- 请谨慎使用，建议仅用于学习/测试
- Use with caution, recommended for learning/testing only

---

## 🚀 快速开始 / Quick Start

### 安装 / Installation

```bash
# 通过 OpenClaw 安装
openclaw skill install xiaohongshu

# 或手动安装
cp -r xiaohongshu ~/.openclaw/workspace/skills/

# 安装依赖
pip3 install xhs click --break-system-packages
```

### 配置认证 / Configure Authentication

**方法 1: 环境变量**
```bash
export XHS_COOKIE="your_xiaohongshu_cookie"
```

**方法 2: 配置文件**
创建 `~/.openclaw/workspace/xiaohongshu-cookies.md`:
```markdown
cookie="your_cookie_here"
```

**获取 Cookie 方法:**
1. 访问 https://www.xiaohongshu.com 并登录
2. 打开开发者工具（F12）→ Network 标签页
3. 刷新页面，找到任意请求，复制 `Cookie` 请求头的值

---

## 📋 可用命令 / Available Commands

### 笔记操作 / Note Operations

**搜索笔记:**
```bash
xiaohongshu-wrapper.sh note search --keyword "Python 编程" --limit 10
```

**获取笔记详情:**
```bash
xiaohongshu-wrapper.sh note info --note-id "xxx" --xsec-token "xxx"
```

**发布笔记:**
```bash
xiaohongshu-wrapper.sh note publish \
  --title "我的学习笔记" \
  --content "今天学习了 Python..." \
  --image-paths /path/to/image.jpg \
  --topics "学习" "Python"
```

**删除笔记:**
```bash
xiaohongshu-wrapper.sh note delete --note-id "xxx"
```

### 用户操作 / User Operations

**获取当前用户:**
```bash
xiaohongshu-wrapper.sh user current
```

**获取用户信息:**
```bash
xiaohongshu-wrapper.sh user info --user-id "xxx"
```

**获取用户笔记:**
```bash
xiaohongshu-wrapper.sh user notes --user-id "xxx" --limit 10
```

### 评论操作 / Comment Operations

**获取评论列表:**
```bash
xiaohongshu-wrapper.sh comment list --note-id "xxx" --xsec-token "xxx" --limit 20
```

**发布评论:**
```bash
xiaohongshu-wrapper.sh comment post --note-id "xxx" --content "写得真好！"
```

### 其他 / Others

**获取首页推荐:**
```bash
xiaohongshu-wrapper.sh feed
```

**显示版本:**
```bash
xiaohongshu-wrapper.sh version
```

---

## 🔧 高级用法 / Advanced Usage

### JSON 输出
```bash
xiaohongshu-wrapper.sh note search --keyword "Python" --json-output
```

### 批量操作
```python
#!/usr/bin/env python3
import subprocess
import time

for keyword in ["Python", "机器学习", "数据分析"]:
    subprocess.run(f"xiaohongshu-wrapper.sh note search --keyword '{keyword}'", shell=True)
    time.sleep(3)  # 避免风控
```

---

## 📚 依赖 / Dependencies

- Python 3.8+
- xhs (小红书 API 库)
- click (CLI 框架)

安装所有依赖:
```bash
pip3 install xhs click --break-system-packages
```

---

## 🎯 功能对比 / Features

| 功能 / Feature | 状态 / Status |
|---------------|--------------|
| 搜索笔记 / Search Notes | ✅ |
| 获取笔记详情 / Get Note Info | ✅ |
| 发布笔记 / Publish Note | ✅ |
| 删除笔记 / Delete Note | ✅ |
| 获取用户信息 / Get User Info | ✅ |
| 获取用户笔记 / Get User Notes | ✅ |
| 获取评论 / Get Comments | ✅ |
| 发布评论 / Post Comment | ✅ |
| 首页推荐 / Home Feed | ✅ |
| 图片上传 / Image Upload | ⚠️ 需额外配置 |

---

## ⚠️ 注意事项 / Notes

1. **速率限制 / Rate Limiting**: 避免快速连续调用（建议间隔 3-5 秒）
2. **风控策略 / Risk Control**: 小红书风控严格，大量操作可能需要代理
3. **Cookie 有效期 / Cookie Expiry**: Cookie 会过期，需定期更新
4. **合法使用 / Legal Use**: 仅供学习和研究使用，禁止商业用途

---

## 📝 更新日志 / Changelog

### v1.0.0 (2026-03-13)
- ✨ 初始版本 / Initial release
- ✅ 支持笔记搜索/发布/删除 / Note search/publish/delete
- ✅ 支持用户查询 / User query
- ✅ 支持评论管理 / Comment management
- ✅ 支持首页推荐 / Home feed
- ⚠️ 添加风险警告 / Risk warning added

---

## 🔗 相关链接 / Related Links

- **xhs-python-sdk**: https://github.com/leeguooooo/xhs-python-sdk
- **XHS-Downloader**: https://github.com/JoeanAmier/XHS-Downloader
- **CLI-Anything**: https://github.com/HKUDS/CLI-Anything
- **OpenClaw**: https://github.com/openclaw/openclaw

---

## 📄 许可证 / License

MIT License

**仅供学习和研究使用 / For learning and research only**

---

**维护者 / Maintainer**: 小爪 🐾  
**最后更新 / Last Updated**: 2026-03-13
