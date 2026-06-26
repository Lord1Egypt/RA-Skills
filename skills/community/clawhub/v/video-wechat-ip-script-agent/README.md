# video-wechat-ip-script-agent-enhanced

增强版 OpenClaw 技能目录，包含：
- OpenClaw 可识别的 `SKILL.md`
- 规则文件 `AGENTS.md`
- Prompt 模板
- 配置文件
- 输出 Schema
- 示例与验收清单

## 安装
将整个目录放入：
- `~/.openclaw/skills/`
- 或 `<workspace>/skills/`

## 调试建议
1. 先用“选题生成”测试结构是否稳定。
2. 再用“脚本生成”验证输出完整性。
3. 最后用“风格改写”和“合规检查”验证边界。

## 常用命令

```bash
npm run build
npm run validate-config
npm test
npm run check
```

## 请求样例

可直接复用这些 JSON 做本地联调：
- `examples/requests/topics.json`
- `examples/requests/script.json`
- `examples/requests/rewrite.json`
- `examples/requests/compliance.json`

示例：

```bash
node dist/openclaw.js --file ./examples/requests/script.json
```

## 后续扩展
- 在 `config/styles.json` 中新增风格
- 在 `config/platforms.json` 中新增平台
- 在 `prompts/` 中新增任务提示词


## 开发版补充

本目录额外包含 `services/` 与 `lib/`，用于把 Prompt、配置、输出校验、兜底逻辑拆开，便于 Cursor / Codex 继续开发。
