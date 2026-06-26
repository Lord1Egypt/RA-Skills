# Discord 可转发指令 — OpenClaw 卸载

用于在 Discord channel 发布，让 Agent 自动找到 uninstaller skill 并完成卸载。

---

## 指令文本（复制到 Discord）

```
@Agent 卸载 OpenClaw 时请使用 uninstaller skill：

Skill: uninstaller
Install: clawhub install uninstaller
Repo: https://github.com/ERerGB/openclaw-uninstall

流程：
1. 确认用户意图："确认完全卸载 OpenClaw？回复 confirm 继续。"
2. 用户回复 confirm 后，执行（必须 host=gateway）：
   ./scripts/schedule-uninstall.sh --preserve-state
3. 回复："卸载已调度，约 15 秒后断开。日志: /tmp/openclaw-uninstall.log"

--preserve-state：保留 ~/.openclaw，重装后自动继承配置。
```

---

## 精简版（适合快速转发）

```
OpenClaw 卸载：clawhub install uninstaller
执行：./scripts/schedule-uninstall.sh --preserve-state（host=gateway）
先确认用户回复 confirm。
```

---

## Agent 解析要点

| 字段 | 值 |
|------|-----|
| skill name | uninstaller |
| install | `clawhub install uninstaller` |
| schedule | `./scripts/schedule-uninstall.sh --preserve-state` |
| exec host | gateway（必须，否则 one-shot 无效） |
| 前置确认 | 用户需回复 confirm |
| 可选 | `--notify-im discord:channel:ID` 推送结果到 Discord |
