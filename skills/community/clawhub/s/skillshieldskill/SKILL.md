---
name: skillshield
description: AI Agent Skill Security Scanner - Detect malicious skills, verify signatures, analyze permissions, and provide trust ratings for the agent ecosystem. Protects against credential stealers, data exfiltration, and unauthorized access.
triggers:
  - skillshield
  - scan skill
  - skill security
  - check skill
  - verify skill
  - skill audit
  - security scan
  - skill guard
  - skill safety
---

# SkillShield 🛡️ - Skill 安全卫士

守护 AI Agent 生态的 skill 供应链安全。

## 快速开始

### 扫描本地 Skill

```bash
python3 ~/.agents/skills/skillshield/scripts/skillshield.py scan ./skill/
```

### 详细扫描报告

```bash
python3 ~/.agents/skills/skillshield/scripts/skillshield.py scan ./skill -v
```

### 深度扫描模式

```bash
python3 ~/.agents/skills/skillshield/scripts/skillshield.py scan ./skill --deep
```

### JSON 格式输出

```bash
python3 ~/.agents/skills/skillshield/scripts/skillshield.py scan ./skill --format json
```

### 验证签名

```bash
python3 ~/.agents/skills/skillshield/scripts/skillshield.py verify ./skill/
```

## 信任评级系统

| 评级 | 风险等级 | 建议 |
|-----|---------|------|
| **A+** | 极低 | 已验证作者，无警告，放心使用 |
| **A** | 低 | 无安全警告，放心使用 |
| **B** | 中低 | 有轻微权限请求，审查后使用 |
| **C** | 中等 | 有警告需关注，确认安全后使用 |
| **D** | 高 | 多个警告，建议避免使用 |
| **F** | 极高 | 确认恶意代码，**不要安装** |

## 检测能力

### 已实现的检测

- ✅ 敏感文件访问 (~/.env, ~/.ssh, credentials)
- ✅ 网络请求分析 (HTTP/HTTPS)
- ✅ 系统命令执行 (os.system, subprocess)
- ✅ 数据窃取检测 (env + HTTP 组合)
- ✅ 可疑域名识别 (webhook, pastebin)
- ✅ 代码混淆检测 (base64, hex)
- ✅ 动态代码执行 (exec, eval)
- ✅ 隐藏文件检测

### 权限分析

自动提取 skill 需要的：
- 文件读写权限
- 网络访问域名
- 导入的 Python/Node 模块
- 系统命令调用

## Moltbook 集成

自动监控 Moltbook 新上传的 skills：

```bash
# 启动守护进程
python3 ~/.agents/skills/skillshield/scripts/moltbook_guardian.py --monitor
```

## 示例输出

```
═══════════════════════════════════════════════════════════════
🛡️ SkillShield 安全扫描报告
═══════════════════════════════════════════════════════════════

📦 Skill 路径: ./my-skill
📅 扫描时间: 2026-02-26 14:30:00
📁 扫描文件: 5 个

📊 信任评级: 🟢 A (得分: 92/100)
⚡ 风险等级: 低

✅ 无警告 - 未发现明显安全问题

📋 权限清单:
   🌐 网络访问:
      - api.example.com
   📁 文件访问:
      - ~/.config/config.json
   📦 导入模块:
      - requests, os, json

💡 建议:
   1. 没有发现特别的安全问题

📝 总结:
   此 skill 看起来非常安全，没有发现明显风险，可以放心使用。
═══════════════════════════════════════════════════════════════
```

## 版本信息

- **版本**: 1.0.0
- **作者**: OpenClaw Community
- **许可证**: MIT
- **仓库**: https://github.com/openclaw/skillshield

## 保护 Agent 生态，从 SkillShield 开始！ 🛡️
