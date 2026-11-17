---
name: wechat-miniprogram-helper
version: 0.1.2
description: This skill should be used when a user wants to build, develop, debug, or publish a WeChat Mini Program (微信小程序), from scaffolding a project to submitting it for review and release. It covers the dual-thread architecture, the four-file page structure (wxml/wxss/js/json), rpx units, setData, Canvas 2D, common errors (invalid app.json disableScroll, "ctx is not defined", jank/卡顿), AppID vs test accounts, experience-member permissions, and the upload/review/release workflow. Trigger phrases include "微信小程序", "做个小程序", "小程序上线", "小程序报错", "小程序发布", "小程序体验权限".
agent_created: true
---

# 微信小程序从零到上线助手

## Overview

Guide the user through the full lifecycle of a WeChat Mini Program: understanding the architecture → scaffolding a runnable project → developing pages (including Canvas 2D) → debugging common errors → setting up AppID / accounts → submitting for review → releasing. Apply the bundled procedural knowledge and reusable assets so the user ends up with a real, runnable project rather than just an explanation.

## When To Use

- User says "做个小程序 / 微信小程序 / 小程序助手 / 小程序模板".
- User hits a mini program error (e.g., 无效的 app.json window["disableScroll"], `ReferenceError: ctx is not defined`, 卡顿/掉帧).
- User asks about 发布 / 上线 / 体验权限 / AppID / 测试号 / 审核.
- User wants a boilerplate mini program project to start from.

## Workflow

### 1. Clarify scope (only if unclear)

Determine: target device (phone only / also need 管理后台?), must-have pages, whether a backend is needed (wx.request to own server), and whether payment/login is required. If the user just wants to start, skip straight to scaffolding.

### 2. Scaffold a runnable project

Run the bundled scaffolder to generate a complete, importable project:

```bash
python <skill>/scripts/scaffold_miniprogram.py <target_dir> [--appid APPID] [--name NAME]
```

This creates `app.js / app.json / app.wxss / project.config.json / sitemap.json` and `pages/index/*` (the four-file set). The user imports the folder into 微信开发者工具 (WeChat DevTools) and can preview immediately. Then customize pages per the request.

### 3. Develop pages and logic

Consult `references/architecture-and-basics.md` for:
- Dual-thread architecture (逻辑层 AppService vs 视图层 WebView).
- The four-file page structure and how they interact.
- `rpx` units, data binding `{{ }}`, `bindtap` events.
- `setData` mechanics and its size/performance limits.
- Page/App lifecycle.
- Canvas 2D (`type="2d"` + `SelectorQuery` + `requestAnimationFrame` + dpr).
- `wx.request` and the domain whitelist gotcha.

### 4. Debug common errors

Consult `references/common-pitfalls.md` for the exact fixes to:
- 无效的 app.json window["disableScroll"] (only valid at page-level json).
- `ctx is not defined` inside Canvas drawing (capture `const ctx = canvas.getContext('2d')`).
- 卡顿/掉帧 (drop `shadowBlur`, cap dpr at 2, cache measured text widths, limit particle count).
- "暂无体验权限" on QR preview (test accounts have no experience-member entry; needs official AppID + 体验成员 added in backend).

### 5. Publish and release

Consult `references/publishing.md` for:
- Test account (`touristappid`) vs official AppID trade-offs.
- Where to set/change the AppID (project.config.json `appid` field or DevTools 详情).
- How to add 体验成员 so others can preview.
- The upload → 提交审核 → 发布 pipeline, plus personal vs enterprise account limits.

## Resources

- `scripts/scaffold_miniprogram.py` — generate a runnable boilerplate project.
- `references/architecture-and-basics.md` — architecture, four-file structure, rpx, setData, lifecycle, Canvas 2D, network.
- `references/common-pitfalls.md` — error catalog with exact fixes.
- `references/publishing.md` — AppID, accounts, experience members, review/release flow.

## Notes

- Prefer native WeChat mini program (WXML/WXSS/JS/JSON), zero-dependency, runs directly in DevTools.
- When generating code, keep it minimal and runnable; avoid features the user did not ask for.
- For visual effects (particles, fireworks), use Canvas 2D with the performance rules in `common-pitfalls.md`.
