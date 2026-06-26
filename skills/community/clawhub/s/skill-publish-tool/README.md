# skill-publish-tool

自动化发布 OpenClaw Skill 到 GitHub 和 ClawHub 的工具。

## 功能特性

- 📦 **自动版本管理** - 支持 major/minor/patch 版本号递增
- 📝 **更新日志管理** - 自动更新 README.md 的更新日志部分
- 🔄 **Git 自动化** - 自动提交并推送到 GitHub
- 🚀 **ClawHub 发布** - 一键发布到 ClawHub 市场
- 📋 **多文件同步** - 同时更新 package.json 和 _meta.json

## 快速开始

```bash
# 安装 skill（如果是从 ClawHub 安装）
npx clawhub@latest install skill-publisher

# 使用示例
python3 scripts/publish_skill.py ~/.jvs/.openclaw/workspace/skills/cn-stock-volume \
  --slug cn-stock-volume \
  --changelog "新增创业板数据，修复合计计算逻辑"
```

## 完整文档

详见 [SKILL.md](SKILL.md)

## 使用场景

1. **发布 skill 更新** - 修改代码后自动发布新版本
2. **批量发布** - 多个 skill 需要更新时
3. **CI/CD 集成** - 可集成到自动化流程中

## 前置要求

- Node.js + npm
- Git
- ClawHub 账号

## 许可证

MIT License
