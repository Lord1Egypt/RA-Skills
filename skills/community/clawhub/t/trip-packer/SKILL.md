---
name: trip-packer
slug: trip-packer
version: 1.0.0
description: |
  帮助用户将旅行行程数据打包成独立的 HTML 地图网页。
  引导用户完成行程规划、生成符合 Schema 的 JSON、调用 trip-packer CLI 构建产物，并在构建完成后将 HTML 结果呈现给用户。
metadata: {"openclaw":{"emoji":"🗺️","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## When to Use

当用户有以下意图时触发：
- 想生成旅行地图、制作行程 HTML、使用 trip-packer
- 想规划某城市行程并导出可分享的网页
- 提供了行程信息，希望打包成单一 HTML 文件
- 询问如何把自己的旅行数据变成地图页面

## Core Rules

1. **先规划，后写数据**：若用户只给了模糊需求，先用 `planning-guide.md` 引导问答，收集目的地、天数、住宿、每日景点/餐厅、交通方式，再写 JSON。
2. **默认落盘到 skill data 目录**：将生成的 `{city}.json` 和 `{city}-map.html` 优先放在 `skills/trip-packer/data/` 下；若用户指定了其他目录，按用户要求存放。
3. **严格遵循 Schema**：写 JSON 时参考 `references/schema-reference.md` 中的字段类型与必填要求，避免使用未定义的 `type`（如 `"food"`）。
4. **Schema 校验必过**：写完后必须执行 `npx trip-packer validate -d <文件>`；出现错误时逐条解释并修正，校验通过后再构建。
5. **正确调用 CLI 构建**：
   - 单城市：`npx trip-packer build -d xxx.json -o xxx-map.html`
   - 多城市：多次 `-d`，可用 `--default-city` 指定默认城市
   - 若需要同时生成分享图片，追加 `--images`，会在 HTML 同目录下自动生成 `xxx-map-panorama.png`（全景横图）和 `xxx-map-itinerary-vertical.png`（完整竖图）
6. **必须交付产物**：每次 `build` 成功后，向用户汇报产物文件路径、文件大小，并提示可直接用浏览器打开查看。若使用了 `--images`，需一并汇报两张 PNG 的路径和大小。
7. **不污染源码**：不要直接修改仓库 `src/data/` 下的硬编码数据文件（如 `seoul.json`），除非用户明确指令这么做。
8. **鼓励迭代**：先做一个最小可行版本（2 天、3-4 个地点），验证并构建出 HTML 让用户看到效果，再逐步扩展。

## Quick Reference

| 需求 | 文件 |
|------|------|
| 行程规划对话流程 | `planning-guide.md` |
| 完整 JSON 字段说明 | `references/schema-reference.md` |
| JSON 结构示例 | `references/sample-itinerary.json` |
