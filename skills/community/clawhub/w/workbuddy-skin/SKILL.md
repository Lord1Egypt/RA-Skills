---
name: workbuddy-skin
description: 构建、修改、调试和发布 Windows 版 WorkBuddy Skin Studio（Tauri v2 + Rust）桌面换肤工具。用于用户要求为 WorkBuddy 制作 GUI 换肤器、调整主题/按钮/本地 CDP 注入流程、处理 WorkBuddy.exe 路径、创建自定义皮肤、或构建 NSIS 安装包时。
---

# 换皮肤

使用 `assets/wb-skin-studio/` 作为可复用的 Tauri v2 模板。不要在该 assets 目录中直接开发；复制到用户的工作区后再改。

## 工作流

1. 确认目标是 Windows WorkBuddy Desktop。此模板通过 `127.0.0.1:9223` 的 CDP 注入样式，不修改 WorkBuddy 的安装文件。
2. 将 `assets/wb-skin-studio/` 复制到用户指定的新目录；若已有项目，先检查其改动并就地修改。
3. 在项目根目录执行 `npm install`。使用 `npm run tauri dev` 调试；若变更 Rust 命令、Tauri 配置或插件，停止并重新启动开发模式。
4. 修改 UI 时保持四项核心操作可用：选择 WorkBuddy 目录、应用主题、暂停皮肤、状态/错误反馈。应用主题会重启 WorkBuddy，界面必须明确提示先保存任务。
5. 修改主题注入逻辑后，重新应用一次主题，才会更新已经打开的 WorkBuddy 右上角画板菜单。
6. 发布前执行 `npm run build`、`cargo check`，再执行 `npx tauri build --bundles nsis`。只交付 `src-tauri/target/release/bundle/nsis/*-setup.exe`，不要交付裸 `target/release/*.exe`。

## 资源与打包

安装版的资源根目录与开发目录不同。`src-tauri/tauri.conf.json` 必须保持显式资源映射：

```json
"resources": {
  "../src/": "src/",
  "../themes/": "themes/"
}
```

Rust 运行时以 `app.path().resource_dir()` 查找安装版资源。因此打包后必须可在资源根目录直接找到 `src/cli.mjs` 和 `themes/<theme-id>/theme.json`。

## 自定义皮肤开关

当 `src/skin-unlock_cy.js` 存在时，GUI 的“自定义皮肤”按钮应允许用户选择 PNG、JPG、JPEG 或 WebP，创建本地主题并应用；文件不存在时显示既有开通提示。不要默认创建这个文件，也不要将其作为模板资产分发。

## 安全边界

- CDP 仅可使用 `127.0.0.1`；不要改为局域网或公网监听。
- 不要修改 WorkBuddy 的 `app.asar`、安装目录或签名文件。
- 仅在用户明确提供时添加外部链接、广告、支付或联系信息。
- 分发版不需要项目源码、npm 或 Rust；接收方仍需要 WorkBuddy，且需要系统 Node 或 WorkBuddy 自带 Node。
