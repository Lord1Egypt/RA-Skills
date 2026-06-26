---
name: skills-security-scanner
description: 审计和扫描技能的安全性。在启用新技能前使用此工具验证其安全性，确保符合安全策略。
---

# 安全扫描器 (Security Scanner)

通过将定义发送到本地分析服务，审计工作区中的其他技能是否存在潜在的安全风险。

## 何时使用

- **新技能**：发现或安装新技能时，请在首次使用前进行扫描。
- **审计**：定期扫描所有技能以确保符合安全策略。
- **开发**：在开发过程中检查自己的技能。
- **要求**：必须确保目标技能包含 `SKILL.md` 文件，因为它是扫描的主要输入。

## 用法

使用 `scripts/scan.py` 脚本执行扫描。**必须使用绝对路径，不要使用~**，因为运行目录不是 skill 目录。

脚本会自动打包目录（如果提供的是目录）并上传，始终输出包含扫描结果的 JSON 数组。Agent 负责解析此 JSON 并以易读的格式（中文）向用户展示结果（风险等级、详细信息、建议）。

### 扫描技能（目录或压缩包）

脚本会自动从同目录下的 `config.json` 读取配置（推荐），也可使用环境变量。

```bash
python3 ~/.openclaw/workspace/skills/skill-security-scanner/scripts/scan.py --name "bad_skills1" --path "/root/.openclaw/workspace/skills/bad_skills1"
```

**重要**：
- 脚本路径必须是**绝对路径**
- 目标路径也必须是**绝对路径**
- 确保 `scripts/config.json` 存在并包含正确的凭据

## 报告格式

向用户展示结果时，**必须**使用以下格式（中文）：

### 🛡️ 安全扫描报告：[SkillName]

**扫描时间**: [将 ScanEndTime 时间戳转换为可读日期格式]
**整体状态**: [✅ 通过 / ❌ 发现风险]

| 风险等级 | 规则名称 | 风险详情 |
| :--- | :--- | :--- |
| **[High/Medium/Low]** | [RuleName] | [RiskDetail] |

**发现的风险列表：**
（仅列出 High 和 Medium 级别的风险）

1. **[RuleName] (ID: [RuleID])**
   - **等级**: [RiskLevel]
   - **文件**: [FileName]
   - **详情**: [RiskDetail]
   - **建议**: 请检查上述文件中的代码，移除可疑的网络请求或敏感操作。

---
