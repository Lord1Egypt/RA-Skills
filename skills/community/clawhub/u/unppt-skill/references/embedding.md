# 嵌入与控制播放器（JS bridge）

转码产物自带零依赖播放器（约 58KB，gzip 后约 21KB）。同一套指令/事件，支持三种宿主：同页 JS（`window.unppt`）、iframe（`postMessage`）、原生 App WebView（`window.unppt.handle`）。

## 播放器内建操作（无需代码）

| 操作 | 效果 |
|---|---|
| 单击画面 / → / ↓ / PageDown / 空格 / 回车 | 下一步 |
| ← / ↑ / PageUp / Backspace | 上一步 |
| Home / End | 第一页 / 最后一页 |
| 输入数字后回车（2 秒内） | 跳到那一页（从 1 开始，含隐藏页） |
| B 或 `.` / W 或 `,` | 黑屏 / 白屏；再按任意键恢复 |
| 触屏左右滑动 | 下一步 / 上一步 |

## iframe 嵌入

```html
<div style="width:960px; aspect-ratio:16/9;">
  <iframe src="https://cdn.example.com/deck/index.html?ui=0"
          style="width:100%; height:100%; border:0;"
          allow="autoplay; fullscreen"></iframe>
</div>
```

播放器按比例缩放到 iframe 大小，多余留黑边，宽高比最好与幻灯片一致（常见 16:9）。`allow="autoplay"` 让音视频更易自动播放。

## URL 参数

| 参数 | 例子 | 作用 |
|---|---|---|
| `slide` | `?slide=3` | 打开时到第 4 页（从 0 开始） |
| `step` | `?slide=3&step=1` | 打开到第 4 页第 1 步的最终状态 |
| `ui` | `?ui=0` | 隐藏自带翻页按钮（点击/键盘/触屏照常），自己做按钮 |
| `mode` | `?mode=watch` | 观看模式：只能由 JS 驱动（直播课学生端）。默认 `present` |
| `links` | `?links=0` | 点外部网址不自动开新窗口，只发 `link` 事件给宿主 |
| `timings` | `?timings=0/1` | 关/开"按排练计时自动换片"。没写时：带 `slide`/`step` 就不自动换片，否则按课件设置 |
| `static` | `?static=1` | 每页所有对象原样显示，不放动画（比对工具用） |
| `origin` | `?origin=https://a.com,https://b.com` | 只接受这些源发来的指令（安全） |

## 指令（cmd）

| cmd | args | 作用 |
|---|---|---|
| `next` | 无 | 下一步；本页点完翻下一页（跳过隐藏页）；最后再 next 发 `end` 事件 |
| `prev` | 无 | 上一步；第 0 步时回到上一页最后一步 |
| `goto` | `{ slide, step }` | 确定性跳转：直接显示目标状态，不播切换和动画 |
| `sync` | 整个 PlayerState | 观看端跟上演绎端：正好是下一步时播动画，否则直接跳 |
| `getState` | 无 | 读当前状态 |

## 事件（event）

| event | 何时发 | data |
|---|---|---|
| `ready` | 播放器启动好（只通过 iframe/原生通道发） | 状态 |
| `change` | 翻页、走一步、触发器、黑/白屏、音视频变化后**立即**发（不等动画播完） | 状态 |
| `end` | 最后一页最后一步再 `next`（循环放映不发） | 状态 |
| `link` | 点击课件里的外部网址 | 状态 + `url` |

## PlayerState

```json
{ "slide": 2, "step": 1, "slideCount": 12, "stepCount": 3 }
```

| 字段 | 说明 |
|---|---|
| `slide` / `step` | 当前页、步，从 **0** 开始 |
| `slideCount` | 总页数，**含隐藏页**（顺序翻页跳过隐藏页，`goto` 可跳过去） |
| `stepCount` | 当前页主序列点击次数（不含触发器动画） |
| `blank`（可选） | 黑/白屏颜色 |
| `triggers`（可选） | 每个触发器已播到第几组 `{ 形状编号: 组数 }` |
| `media`（可选） | 播放过的音视频 `[{ uid, playing, time }]`，`time` 秒 |

## postMessage 协议（宿主 ↔ iframe）

- 指令：`iframe.contentWindow.postMessage({ unppt: 1, id, cmd, args }, 目标源)` —— `unppt: 1` 固定，播放器靠它识别消息。
- 回复：`{ unppt: 1, re: <id>, ok: true, result: 状态 }`；失败 `{ ok: false, error }`。未知指令返回失败。
- 事件：`{ unppt: 1, event, data }`。
- 监听时校验 `e.source === iframe.contentWindow`。
- **可能错过 `ready`**（播放器先于监听代码加载完）：在 iframe 的 `load` 事件里再发一次 `getState`。

最小实现：

```js
const iframe = document.getElementById('player');
const PLAYER_ORIGIN = location.origin;   // 跨域时写播放器域名；file:// 只能 '*'
let seq = 0;
const waiting = new Map();

function send(cmd, args) {
  const id = ++seq;
  return new Promise((resolve, reject) => {
    waiting.set(id, { resolve, reject });
    iframe.contentWindow.postMessage({ unppt: 1, id, cmd, args }, PLAYER_ORIGIN);
  });
}

window.addEventListener('message', (e) => {
  if (e.source !== iframe.contentWindow) return;
  const d = e.data;
  if (!d || d.unppt !== 1) return;
  if ('re' in d) {
    const w = waiting.get(Number(d.re));
    if (!w) return;
    waiting.delete(Number(d.re));
    d.ok ? w.resolve(d.result) : w.reject(new Error(d.error));
    return;
  }
  if (d.event === 'ready' || d.event === 'change') show(d.data);
});

iframe.addEventListener('load', () => send('getState').then(show));  // 防错过 ready
function show(s) { console.log(`第 ${s.slide + 1} / ${s.slideCount} 页，第 ${s.step} / ${s.stepCount} 步`); }
```

## 官方小工具 UnpptFrame（host.js）

`host.js` 未单独发 npm，需克隆 unppt 仓库 `npm install && npm run build` 后取 `packages/player/dist/host.js`。

```js
import { UnpptFrame } from './host.js';
const deck = new UnpptFrame(document.getElementById('ppt'), 'https://cdn.example.com'); // 第二参 targetOrigin，生产建议写具体域名
await deck.ready;                 // 第一份状态
await deck.next();                // 下一步（先播动画再翻页）
await deck.goto(3, 0);            // 跳第 4 页第 0 步（页码从 0 起）
deck.on('change', (s) => console.log(s.slide, s.step, s.slideCount, s.stepCount));
const off = deck.on('end', () => {});  // 返回取消监听函数
deck.destroy();                   // 移除监听，未完成指令全部失败
```

- API：`ready`、`next()`、`prev()`、`goto(slide, step=0)`、`getState()`、`on(event, fn)`、`destroy()`，都返回/得到 `PlayerState`。
- 每条指令 10 秒无回复即失败（"播放器没有响应"）。
- 没有 `sync` 方法：直播课同步直接发 postMessage（见下）。

## 同页 JS 与原生 App

播放器页面里可用的 `window.unppt`：

```js
await window.unppt.next();
await window.unppt.goto({ slide: 3, step: 0 });   // 也可 goto(3, 0)
const s = await window.unppt.getState();
const off = window.unppt.on('change', (s) => console.log(s.slide, s.step));
off();   // 等同 window.unppt.off('change', fn)
```

原生 App（iOS WKWebView / Android WebView / React Native WebView）：向播放器页面注入或执行

```js
window.unppt.handle('{"cmd":"next"}')        // 也可带 id：'{"id":1,"cmd":"goto","args":{"slide":3}}'
// 结果和事件通过原生 bridge 回调返回（JSON 同 postMessage 协议）
```

## 直播课同步（演绎端 / 观看端）

- 老师端：普通播放（`present` 模式），把每次 `change` 事件的状态广播给学生端（WebSocket / 信令通道自备）。
- 学生端：`index.html?mode=watch&ui=0`，收到状态后发 `sync` 指令：

```js
iframe.contentWindow.postMessage({ unppt: 1, cmd: 'sync', args: state }, PLAYER_ORIGIN);
```

`sync` 的语义：和演绎端正好差一步时播动画（学生看到平滑过渡），落后多步或跳页时直接显示目标状态。可运行示例见 unppt 仓库 `examples/live-class.html`。

## 安全注意事项

- 生产环境给播放器地址加 `?origin=https://你的域名`，只接受可信源的指令。
- postMessage 的目标源尽量写具体域名，不要用 `'*'`（`file://` 本地调试时除外）。
- 宿主收消息时校验 `e.source`，避免其他 iframe 的消息串扰。
