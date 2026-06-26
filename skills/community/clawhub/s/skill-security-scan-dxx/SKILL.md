---
name: skill-security-scan
description: Scan installed OpenClaw skills for potential security risks. Use when you want to check if skills contain dangerous commands, access sensitive paths, or have other security issues.
triggers:
  keywords:
    - "skill安全"
    - "扫描skill"
    - "检查skill"
    - "skill风险"
    - "skill安全扫描"
    - "skill安全检查"
    - "skill藏毒"
  conditions:
    - "需要检查skill安全性"
    - "担心skill有恶意代码"
    - "要扫描已安装的skill"
---

# Skill Security Scan

扫描已安装的 OpenClaw skill，检测潜在的安全风险。

## 功能

- 🔍 扫描所有已安装 skill
- ⚠️ 检测危险命令（rm -rf /、fork 炸弹等）
- 🔒 检查敏感路径访问
- 🌐 检查网络请求安全性
- 📊 生成风险报告

## 使用方法

```bash
# 运行安全扫描
python3 ~/.openclaw/workspace/skills/skill-security-scan/skill_scan.py
```

## 检查项

### 高风险
- `rm -rf /` - 删除根目录
- `rm -rf ~` - 删除用户目录
- Fork 炸弹
- 直接写入磁盘设备

### 中风险
- 访问敏感路径（/etc/passwd、~/.ssh/ 等）
- 使用 eval/exec

### 低风险
- 网络请求未验证 SSL
- 使用 os.system/subprocess

## 安全建议

1. **只安装可信来源的 skill**
   - 优先使用 clawhub 官方 skill
   - 检查 GitHub 仓库的 star 数和更新频率

2. **检查 skill 代码**
   - 阅读 SKILL.md 了解功能
   - 检查 scripts/ 目录下的代码

3. **隔离测试**
   - 新 skill 先在测试环境运行
   - 观察是否有异常行为

4. **定期扫描**
   - 定期运行安全检查
   - 及时更新 skill 到最新版本

5. **最小权限原则**
   - 不给 skill 不必要的权限
   - 敏感操作需要确认
