# SKILL.md — WorkBuddy 换肤（AI 用）

给 WorkBuddy 桌面端应用本仓库的皮肤。全程命令行，无需用户逐步操作。

## 流程

1. 提醒用户：apply 会重启 WorkBuddy 为调试模式，请先保存进行中的任务
2. 运行 `node src/apply.mjs`（项目根目录下）
3. 输出 `✓ 皮肤已注入` 即成功
4. 用户想还原：`node src/pause.mjs`

## 改皮肤

- 改配色/样式：编辑 `src/theme.css` 后重新 `node src/apply.mjs`（需先在页面里清 flag：用 `tools/cdp.mjs 'window.__wbsMounted=false'` 再 apply，或先 pause 再 apply）
- 调 DOM 结构先探查：`node tools/cdp.mjs '<js>'`（如 `[...document.querySelectorAll("[data-view-id]")].map(e=>e.dataset.viewId)`）

## 边界

- 不修改 `/Applications/WorkBuddy.app`，不碰 `app.asar`
- 注入只在当前 renderer 存活，WorkBuddy 完全重启后需重新 apply
