# SkillShield 🛡️

AI Agent Skill 安全卫士 - 检测恶意技能、验证签名、分析权限，为 Agent 生态系统提供信任评级。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🌟 核心功能

| 功能 | 描述 |
|------|------|
| **恶意代码检测** | 检测 credential stealer、keylogger、数据窃取等行为 |
| **权限分析** | 解析 skill 需要的文件、网络、API 权限 |
| **信任评级** | A-F 评级系统，帮助选择可信 skill |
| **深度扫描** | 检测混淆代码、隐藏文件等高级威胁 |
| **威胁情报** | 实时更新的恶意 skill 数据库 |
| **Moltbook 集成** | 自动监控和扫描社区分享的 skills |

## 🚀 快速开始

### 安装

```bash
# 通过 skills CLI 安装
npx skills add openclaw/skillshield

# 或手动安装
git clone https://github.com/openclaw/skillshield.git
cd skillshield
```

### 扫描 Skill

```bash
# 扫描本地 skill
python3 scripts/skillshield.py scan ./my-skill/

# 详细输出
python3 scripts/skillshield.py scan ./skill -v

# 深度扫描
python3 scripts/skillshield.py scan ./skill --deep

# JSON 格式输出
python3 scripts/skillshield.py scan ./skill --format json
```

### 验证签名

```bash
python3 scripts/skillshield.py verify ./skill/
```

## 📊 信任评级标准

| 评级 | 描述 | 建议 |
|-----|------|------|
| **A+** | 极度可信 | 已验证作者 + 无警告，可放心使用 |
| **A** | 非常可信 | 无安全警告，可放心使用 |
| **B** | 可信 | 有轻微权限请求，审查后使用 |
| **C** | 谨慎使用 | 有警告需关注，确认安全后使用 |
| **D** | 高风险 | 多个警告，建议避免使用 |
| **F** | 恶意 | 确认恶意代码，**不要安装** |

## 🔍 检测能力

### 恶意行为检测

- ✅ 读取 ~/.env, ~/.bashrc, ~/.ssh 等敏感文件
- ✅ 发送数据到外部 webhook/pastebin
- ✅ 执行系统命令 (os.system, subprocess)
- ✅ 网络请求到可疑域名
- ✅ 文件系统异常访问
- ✅ 数据窃取行为 (读取 env + 发送 HTTP)
- ✅ 代码混淆检测

### 权限分析

```
📁 文件权限:
   - 读取: ~/.env, ~/.bashrc
   - 写入: /tmp/

🌐 网络权限:
   - HTTP 请求: api.example.com
   - 外部 API: webhook.site ⚠️

📦 导入模块:
   - requests, os, json

⚠️  风险评级: C (中等风险)
```

## 🌐 Moltbook 集成

SkillShield 可自动监控 Moltbook 上的新技能：

```bash
# 启动监控
python3 scripts/moltbook_guardian.py --monitor

# 自动扫描新上传的 skills 并生成安全报告
```

## 📋 示例报告

```
═══════════════════════════════════════════════════════════════
🛡️ SkillShield 安全扫描报告
═══════════════════════════════════════════════════════════════

📦 Skill 路径: ./weather-api
📅 扫描时间: 2026-02-26 14:30:00
📁 扫描文件: 5 个

📊 信任评级: 🟢 A (得分: 92/100)
⚡ 风险等级: 低

✅ 无警告 - 未发现明显安全问题

📋 权限清单:
   🌐 网络访问:
      - api.openweathermap.org

   📁 文件访问:
      - ~/.config/weather-api/config.json

💡 建议:
   1. 没有发现特别的安全问题

📝 总结:
   此 skill 看起来非常安全，没有发现明显风险，可以放心使用。

═══════════════════════════════════════════════════════════════
```

## 🛠️ 开发路线图

- [x] 基础扫描框架
- [x] 恶意代码检测规则
- [x] 权限分析系统
- [x] 信任评级算法
- [x] 深度扫描模式
- [ ] GPG 签名验证
- [ ] YARA 规则引擎集成
- [ ] Moltbook API 完整集成
- [ ] Web 管理界面
- [ ] 威胁情报共享网络

## 🤝 贡献

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**保护 Agent 生态，从 SkillShield 开始！** 🛡️
