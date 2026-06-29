# wechat-claude-code-installer

> 一键装好「微信 ↔ Claude Code 桥」并避开 6 个新手大坑

包装上游 [`Wechat-ggGitHub/wechat-claude-code`](https://github.com/Wechat-ggGitHub/wechat-claude-code) 的安装流程，自动修掉首次使用一定遇到的几个体验问题：

- ✅ cwd 僵尸字段（setup 输了不算，daemon 用别的源）
- ✅ Hook 元话术泄露（每条回复都带"评估：xxx"）
- ✅ 闲置睡眠中断（不动键鼠 5 分钟 daemon 假死）
- ✅ `ANTHROPIC_BASE_URL` 代理合规检测（避免对话经公司日志而不自知）
- ✅ launchd 不死鸟（`kill -9` 杀不掉的处理）
- ✅ setup 卡在交互式输入（一行命令灌答案）

## 安装

```bash
# Claude Code skills
mkdir -p ~/.claude/skills/wechat-claude-code-installer
cp SKILL.md ~/.claude/skills/wechat-claude-code-installer/

# 或者 ClawHub
clawhub install wechat-claude-code-installer
```

## 使用

在 Claude Code 里说：「装一下微信桥」 / 「微信里用 Claude Code」 / `/wechat-claude-code-installer`

skill 会按 6 步引导你装好 + 自动修复全部已知坑。

## 适用平台

- macOS（用 launchd 守护）
- Linux：上游支持 systemd / nohup，但本 skill 修复脚本只测试过 macOS

## 前置条件

- Node.js ≥ 18
- 微信号（建议小号 / 测试号，不要用工作号）
- 已经在用 Claude Code

## 我做了什么 vs 上游做了什么

| | 上游 wechat-claude-code | 本 skill |
|---|---|---|
| 微信扫码绑定 | ✅ | 包装 |
| 消息桥接 | ✅ | 不修改 |
| 文件双向收发 | ✅ | 不修改 |
| 工作目录修复 | ❌（有 bug） | ✅ |
| 元话术拦截 | ❌ | ✅ |
| 防闲置睡眠 | ❌（作者 TODO） | ✅ |
| 代理合规提醒 | ❌ | ✅ |

## 参考

- 上游项目：https://github.com/Wechat-ggGitHub/wechat-claude-code
- 灵感原文：[在你微信里用爽 Claude Code](https://mp.weixin.qq.com/s/xxx)（公众号「逛逛GitHub」，2026-06）
- 腾讯 iLink AI 官方机器人通道：`ilinkai.weixin.qq.com`

## License

MIT
