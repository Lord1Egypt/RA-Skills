# AudioClaw Cross-Platform Overlay

这是给当前 `subtitle_overlay.swift` 预留的跨平台替代壳，目标技术栈是：

- `Tauri`
- `React`
- `TypeScript`

## 现在已经有什么

- 圆球 + 卫星按钮的前端原型
- 最近项目侧卡
- 双行字幕展示区
- 和本地能力层的桥接接口草案：
  - 实时 ASR
  - 项目操作
  - 剪贴板处理
  - SenseAudio TTS 音色切换

## 当前机器为什么还不能直接跑

这台机器目前缺少以下工具链：

- `node`
- `npm`
- `cargo`
- `rustc`

所以我先把源码骨架搭好，等工具链装好后即可继续。

## 后续启动方式

```bash
npm install
npm run tauri dev
```

## 建议的迁移顺序

1. 先把 UI 和交互完全搬到 React/Tauri
2. 再把当前 Swift 版本的状态机抽成可复用协议
3. 最后把 macOS 专属能力下沉为平台桥接

## 建议保留在平台层的能力

- 系统音频采集
- 系统悬浮窗/置顶
- 剪贴板监听
- 本地脚本调用
- SenseAudio / audioclaw 的本地进程桥接
