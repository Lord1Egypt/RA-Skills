# tencent-exmail-webbridge

通过 Kimi WebBridge 自动化操作腾讯企业邮箱 Web 端（exmail.qq.com）的技能。

## 核心问题

腾讯企业邮箱没有官方 API，只能通过 Web 端模拟操作。Kimi WebBridge 提供浏览器内 JavaScript 执行能力，但实际操作中面临三大挑战：

1. **iframe 嵌套** — 页面采用多层 iframe，需要准确穿透
2. **中文编码** — WebBridge 传输会破坏 UTF-8，需码点编码协议
3. **动态 DOM** — 回复/转发操作后 iframe 内容动态切换，需状态判断

## 已验证功能

- ✅ 读取邮件列表
- ✅ 打开邮件阅读
- ✅ 回复 / 回复全部 / 转发
- ✅ 修改主题
- ✅ 安全追加正文（不覆盖签名）
- ✅ 存草稿
- ✅ 关闭窗口
- ✅ 文件夹导航

## 使用方式

此技能为纯规范/文档型技能，无需安装脚本。Agent 加载后会获得：

- iframe 穿透映射表
- 中文编码协议（String.fromCharCode / chr()）
- 操作模板（回复、正文追加、收件人读取）
- 安全红线（绝不自动发送）

## 文件结构

```
tencent-exmail-webbridge/
├── SKILL.md         # 主指令（操作规范 + 快速参考）
├── REFERENCE.md     # 详细技术文档（完整代码示例）
└── config.json      # 技能元数据
```

## 安全声明

本技能不提供自动发送邮件功能。所有涉及发送的操作必须经过用户明确确认，默认操作是存草稿或关闭。

## 许可证

MIT-0 — 可自由使用、修改和分发，无需署名。
