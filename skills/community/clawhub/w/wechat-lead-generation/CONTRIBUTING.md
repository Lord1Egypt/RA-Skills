# Contributing to WeChat Lead Generation Skill

感谢你关注本项目的贡献！🎉

## 行为准则

- 尊重所有贡献者
- 接受建设性反馈
- 保持合规意识（微信自动化风险）

## 如何贡献

### 报告 Bug

请在 [GitHub Issues](https://github.com/ling-qian/openclaw-skills/issues) 提交：

- Bug 重现步骤
- 预期 vs 实际行为
- 环境信息（OpenClaw 版本、OS、Python 版本）
- 日志文件片段

### 提出新功能

1. 先搜索是否已有相关 Issue
2. 开新 Issue 描述：
   - 使用场景
   - 预期行为
   - 合规性评估（是否违反微信协议）
3. 等待社区反馈后再开始编码

### 提交 PR

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 PR，描述：
   - 修改内容
   - 测试方法
   - 相关 Issue 链接

## 开发指南

### 代码风格

- Python: 遵循 PEP 8，使用 black 格式化
- Shell/Node: 2 空格缩进，单引号优先

### 测试

```bash
cd ~/.openclaw/workspace/.agents/skills/wechat-lead-generation
bin/run --source groups --days_back 1 --keywords "test" --auto_reply false
```

确认：
- 报告成功生成
- 无异常错误
- 输出格式正确

### 合规性检查

所有 PR 必须确保：
- 不鼓励违反微信用户协议的行为
- 提供安全警告（auto_reply 风险）
- 默认使用半自动模式（auto_reply=false）
- 文档中明确标注风险

## Release 流程

1. 更新版本号（SKILL.md + CHANGELOG.md）
2. 打 tag: `git tag -a v0.2.0 -m "Release v0.2.0"`
3. 推送 tag: `git push origin v0.2.0`
4. GitHub Actions 自动构建发布
5. 更新 ClawHub 列表（提交更新 PR）

## 依赖说明

本技能依赖：
- `wechat-md-publish` / `bb-browser-openclaw`（用户自备）
- `agentmemory`（OpenClaw 插件）
- `trendradar`（可选）

贡献时请确保：
- 不硬编码敏感配置（微信 cookie）
- 提供环境变量文档
- 模拟数据层便于测试

## 许可证

贡献代码即同意 MIT 许可证条款（见 LICENSE 文件）。

## 免责声明

本技能仅供学习和合法使用。使用者需自行承担使用风险，开发者不对任何因使用本工具导致的账号封禁、法律纠纷等负责。
