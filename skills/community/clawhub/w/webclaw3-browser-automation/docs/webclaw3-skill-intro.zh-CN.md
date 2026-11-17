# webclaw3 skill 内部

[English](./webclaw3-intro.md) | **中文**

这页给想深入了解这个 skill 到底是什么的人。产品故事和用法看 [README](../README.zh-CN.md)。

## 它是什么

webclaw3 以一个独立 skill 的形态交付（仓库名 `webclaw3`，安装为 `~/.claude/skills/webclaw3`），由两部分组成：

- **`SKILL.md`**——Agent 会读的浏览哲学与操作指引：目标导向、过程校验、条件不可达时灵活调整。Skill = 哲学 + 技术事实，不是操作手册；讲清 tradeoff，让 AI 自己推理。
- **`scripts/`**——真正触达浏览器的连接层。没有它，skill 会想不能动。

## 双通道，同一个真实 Chrome

两条通道驱动的是同一个真实 Chrome，能力等价，skill 自动选用。

| 通道 | 脚本 | 角色 |
|---|---|---|
| Extension Relay | `scripts/relay.mjs` | **默认主通道。** 桥接到 [wc3-chrome](https://github.com/fatmind/wc3-chrome) MV3 扩展（HTTP :3459 ↔ WebSocket ↔ 插件）。 |
| CDP 兜底 | `scripts/cdp-proxy.mjs` | **兜底通道。** 直连 Chrome DevTools Protocol（HTTP :3456 ↔ :9222），仅在 Extension 通道整体不可用时启用。 |

`scripts/webclaw3.mjs` 负责两者的启停和 `doctor` 健康检查——你说"帮我检查 webclaw3 环境"时 Agent 调的就是它。页面内真正的执行者是 wc3-chrome 扩展（L0）；本 skill 依赖它，但自带连接脚本，可独立运行。

## 能力

| 能力 | 说明 |
|---|---|
| **双通道触达** | Extension Relay 优先，CDP 兜底；同一真实 Chrome，能力等价 |
| 联网工具自主选型 | WebSearch / WebFetch / curl / 浏览器中继，按场景判断 |
| **Aria 树语义理解** | 压缩语义树（~500 行 vs DOM ~10000 行），低 token 看全貌 |
| **Aria 语义交互** | `page.click` / `page.fillForm` 按 `ref_N` 定位，抗改版 |
| **`page.eval` 任意 JS** | 穿透 Shadow DOM / iframe / SPA 数据层 |
| 并行分治 | 多目标分发子 Agent 并行执行 |
| 媒体提取 | 从 DOM 取图片/视频 URL，或对视频截帧分析 |

## 深入阅读

- 浏览哲学：[SKILL.md](../SKILL.md)
- 安装细节：[references/setup.md](../references/setup.md)
- CDP 兜底：[references/cdp-fallback.md](../references/cdp-fallback.md)
- 修复手册：[references/repair.md](../references/repair.md)
