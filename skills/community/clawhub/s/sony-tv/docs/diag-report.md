# Sony TV 浏览器能力检测报告

## 设备信息

| 项目 | 值 |
|------|-----|
| 型号 | Sony Bravia KD-55X9500G |
| 浏览器 | Chrome 77.0.3865.116 |
| WebAppRuntime | 2.1.2+10 |
| GPU | Mali-G71 |
| 屏幕分辨率 | 1920x1080 @1x |
| 视口尺寸 | 1920x1080 |
| 颜色深度 | 24-bit |
| localStorage 容量 | ~1.6 MB (1638200 bytes) |
| 系统语言 | zh-CN / zh-CN, en-US |

## 完整 User Agent

```
Mozilla/5.0 (Linux; BRAVIA 4K UR2 Build/QTG3.200305.006.S90) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.116 Safari/537.36 MRC/1.2.21 SonyCEBrowser/1.0 (KD-55X9500G; CTV/PKG6.6216.0724CNA; CHN) WebAppRuntime/2.1.2+10
```

## 测试汇总

| 通过 ✅ | 不支持 ❌ | 部分支持 ⚠️ | 总计 |
|---------|----------|-------------|------|
| 45 | 1 | 11 | 57 |

---

## 系统信息

| 测试项 | 状态 | 详情 |
|--------|------|------|
| User Agent | ✅ | Chrome 77.0.3865.116 |
| 浏览器引擎 | ✅ | Chrome |
| 语言 | ✅ | zh-CN / zh-CN, en-US |
| 屏幕分辨率 | ✅ | 1920x1080 @1x |
| 视口尺寸 | ✅ | 1920x1080 |
| 颜色深度 | ✅ | 24-bit |
| 在线状态 | ✅ | 在线 |

---

## JavaScript API

| 测试项 | 状态 | 说明 |
|--------|------|------|
| Promise | ✅ | 支持 |
| async/await | ✅ | 支持 |
| Fetch API | ✅ | 支持 |
| XMLHttpRequest | ✅ | 支持 |
| Web Workers | ✅ | 支持 |
| Service Worker | ❌ | **不支持** |
| IntersectionObserver | ✅ | 支持 |
| MutationObserver | ✅ | 支持 |
| requestAnimationFrame | ✅ | 支持 |
| requestIdleCallback | ✅ | 支持 |
| Intl (国际化) | ✅ | 支持 |
| WebAssembly | ✅ | 支持 |
| Proxy 对象 | ✅ | 支持 |
| WeakMap / WeakSet | ✅ | 支持 |
| Map / Set | ✅ | 支持 |
| Symbol | ✅ | 支持 |
| ArrayBuffer / TypedArray | ✅ | 支持 |
| BigInt | ✅ | 支持 |

---

## 存储能力

| 测试项 | 状态 | 详情 |
|--------|------|------|
| localStorage | ✅ | 支持 (~1.6 MB) |
| sessionStorage | ✅ | 支持 |
| IndexedDB | ✅ | 支持 |
| Cookies | ✅ | 支持 |

---

## 媒体能力

| 测试项 | 状态 | 详情 |
|--------|------|------|
| Audio API | ✅ | MP3: probably, OGG: maybe |
| Video API | ✅ | H.264: probably, VP9: probably, HLS: maybe |
| Canvas 2D | ✅ | 支持 |
| WebGL | ✅ | Mali-G71 |

---

## 网络能力

| 测试项 | 状态 | 说明 |
|--------|------|------|
| WebSocket | ✅ | 支持 |
| EventSource (SSE) | ✅ | 支持 |
| Beacon API | ✅ | 支持 |
| XHR (跨域) | ⚠️ | 取决于 CORS 配置 |

---

## Sony TV 专有 API

| 测试项 | 状态 | 能力 |
|--------|------|------|
| WebAppRuntime | ✅ | 检测到 sony 命名空间 |
| sony.tv.systemevents | ✅ | `addListener`, `removeListener` |
| sony.tv.picturemode | ✅ | `getPictureMode`, `setPictureMode` |
| sony.tv.DirectoryReader | ✅ | 支持 USB 存储读取 |
| decimated-video (HDMI 嵌入) | ✅ | `open`, `close`, `setWideMode` |
| multicast-video (组播视频) | ✅ | `show`, `close` |
| 4k-photo (高清图片) | ✅ | `open`, `show`, `preload` |

### TV 遥控器键码

| 键码 | 值 |
|------|-----|
| VK_RED | 403 |
| VK_GREEN | 404 |
| VK_YELLOW | 405 |
| VK_BLUE | 406 |
| VK_PLAY | 415 |
| VK_PAUSE | 463 |
| VK_STOP | 413 |

---

## 性能测试

| 测试项 | 状态 | 说明 |
|--------|------|------|
| Performance API | ✅ | 支持 |
| 页面加载时间 | ⚠️ | 尚未完成加载 |
| DOM Ready 时间 | ⚠️ | 尚未完成 |
| FPS (1秒) | ⚠️ | 测试中 |

---

## 输入设备

| 测试项 | 状态 | 说明 |
|--------|------|------|
| Touch Events | ✅ | 支持 (maxTouchPoints: 0) |
| Keyboard Events | ✅ | 支持 |
| Gamepad API | ✅ | 支持 |

---

## 安全

| 测试项 | 状态 | 说明 |
|--------|------|------|
| HTTPS | ⚠️ | 当前使用 http: |
| CSP | ⚠️ | 未设置 Content Security Policy |

---

## 关键结论

1. **所有 Sony 专有 API 均可用**，包括系统事件、画面模式控制、HDMI 嵌入、组播视频和高清图片渲染
2. **Chrome 77 内核**较旧，不支持 Service Worker，但其他现代 JS API 几乎全部支持
3. **媒体能力完整**，支持 H.264、VP9、HLS、WebGL (Mali-G71)
4. **localStorage 容量 ~1.6 MB**，足够存储应用配置和缓存数据
5. **遥控器键码可检测**，可通过 `keydown` 事件监听 VK_RED/GREEN/YELLOW/BLUE/PLAY/PAUSE/STOP
6. **WebAppRuntime 2.1.2+10** 版本完整支持 `sony.tv.*` API 和三种自定义 `<object>` 标签

## 原始数据

完整 JSON 结果见: [diag-results.json](./diag-results.json)
