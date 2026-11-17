# HyperFrames Handoff — 分镜方案包 → HTML Composition

> 本文档是 `text-to-video` 的核心衔接文档。读完就能把一份 `[视频标题]_video_plan.md` 翻译成 hyperframes 的 `index.html`。

## 1. 输入：分镜方案包

Stage 1 产出的 `[视频标题]_video_plan.md` 长这样（节选）：

```markdown
## 2. 视频脚本与分镜大纲
| 时间轴 | 场景描述 | 画面建议 | 旁白建议 |
| :--- | :--- | :--- | :--- |
| 00:00-00:08 | 开场 hook | 大字"为什么大厂都在做 AI 眼镜"+ Google/Meta logo | 最近在看 AI 硬件 |
| 00:08-00:14 | 玩家扩展 | 智能戒指名牌卡片 Samsung/ŌURA/Oasis | 戒指也来了 |
| 00:14-00:18 | 转折金句 | 全屏大字"谁能更自然地获取你的 context" | 看起来不同，其实相同 |
| ... |
```

## 2. 翻译规则：分镜行 → HTML card

每行分镜 = 一个 `<div class="card-host clip" data-start="..." data-duration="..." data-track-index="N">`。

**模板**：

```html
<div
  class="card-host clip"
  data-card-id="card-01"           <!-- 自取，遵循 card-NN 命名 -->
  data-start="0"                   <!-- 秒，浮点 -->
  data-duration="8"                <!-- 秒 -->
  data-track-index="2"             <!-- 2 起，让 audio=0、video=1 -->
  style="left:0;top:0;width:1080px;height:1920px;visibility:hidden;opacity:0;"
>
  <div class="card" data-card-id="card-01">
    <div class="root">
      <!-- 画面：按"画面建议"列写 DOM -->
      <div class="kicker" id="c01-kicker">最近在看 AI 硬件</div>
      <h1 class="title" id="c01-title">为什么大厂都在做 <em>AI 眼镜</em>？</h1>
      ...
    </div>
  </div>
</div>
```

**关键点**：
- `data-start` 用秒（GSAP timeline 的时间单位）
- `data-duration` 必须 ≥ 实际 GSAP 入场动画时间 + 停留 + 离场动画
- `data-track-index`：**所有 card 用同一个值**（2 或更高），hyperframes 靠 z-index/track 排序
- `class="clip"` 必需（hyperframes 用来管可见性）
- `style="visibility:hidden;opacity:0"` 初始隐藏（GSAP 后续 .fromTo/.to 控制显隐）

## 3. 时间线构造

每个 card 配 3 个动画：入场 / 停留 / 离场。

```js
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });

// 工具函数（可复制到 index.html）
function enter(id, t) {
  tl.set(`.card-host[data-card-id="${id}"]`, { visibility: "visible" }, t);
  tl.fromTo(`.card-host[data-card-id="${id}"]`,
    { opacity: 0 },
    { opacity: 1, duration: 0.35, ease: "power2.out" }, t);
}
function exit(id, tEnd) {
  tl.to(`.card-host[data-card-id="${id}"]`,
    { opacity: 0, duration: 0.3, ease: "power2.in" }, tEnd - 0.3);
  tl.set(`.card-host[data-card-id="${id}"]`, { visibility: "hidden" }, tEnd);
}
function rise(sel, t, d = 0.5) {
  tl.fromTo(sel, { opacity: 0, y: 34 },
    { opacity: 1, y: 0, duration: d, ease: "power2.out" }, t);
}

// 同步构建（不要放在延时回调、Promise 或 async 里）
enter("card-01", 0.8);
rise("#c01-kicker", 1.0);
rise("#c01-title", 1.3);
exit("card-01", 7.6);

enter("card-02", 7.8);
// ...

window.__timelines["main"] = tl;
```

## 4. 媒体（Rule 3 硬约束）

**HTML composition 里这两个元素必须存在，并放在 host root 直接子位置**：

```html
<video id="bg-video" class="video-wrapper" src="input-video.mp4" muted playsinline
       data-start="0" data-duration="66" data-track-index="1"
       style="position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;z-index:5;"></video>

<audio id="voice" src="audio.mp3"
       data-start="0" data-duration="66" data-track-index="0"></audio>
```

**严禁**：
- `<div><video>...</video></div>` （嵌套） → 黑屏
- `<video autoplay>` / `video.play()` / `currentTime = ...` → hyperframes 拒收
- 同一源给 `<video>` 和 `<audio>` 共享不拆开 → 内存泄漏 + 音画不同步

## 5. 画幅 / 字体

**画幅**：
- 竖屏 9:16（抖音/Reels/小红书）：`1080×1920`
- 横屏 16:9（B 站/YouTube）：`1920×1080`
- 方形 1:1（Instagram）：`1080×1080`

**字体**：
1. **woff/woff2 字体**：下载到 `fonts/`，用 `@font-face` 声明
   ```css
   @font-face {
     font-family: "Noto Serif SC";
     src: url("fonts/noto-serif-sc-600.woff") format("woff");
     font-weight: 600; font-display: block;
   }
   ```
2. **系统字体**（PingFang SC / Hiragino Sans GB / Songti SC）：用 `src: local("...")` 否则 lint 报错
   ```css
   @font-face { font-family: "PingFang SC"; src: local("PingFang SC"); font-display: block; }
   ```
3. **统一字体建议**：所有中文用同一种 serif（如 Noto Serif SC），不同 weight 区分

## 6. 资源资产

把素材拷到项目根的对应目录：

```
<项目>/
  assets/        # 图片（svg/png/jpg）+ 视频（mp4）+ 短音频
  fonts/         # 字体 woff/woff2
  audio/         # TTS 音轨（多个场景分文件时）
  input-video.mp4  # 底视频（如有）
```

引用：`src="assets/google.svg"` / `src="fonts/noto-serif-sc-600.woff"`

## 7. 完整骨架模板

参考 `templates/composition_skeleton.html`。

## 8. 常见错误速查

| 错误 | 原因 | 修法 |
|---|---|---|
| 视频黑屏 | `<video>` 套了 `<div>` | 把 video 提到 root 直系 |
| 视频无声 | `<audio>` 没单独加 | 加独立 `<audio>` 元素 |
| 时间线不动 | timeline 没注册或注册晚了 | 检查 `window.__timelines["<id>"]` 且 id 匹配 |
| Lint 报 font | `@font-face` 缺 | 补字体声明 |
| 渲染卡第一帧 | GSAP 放异步延时回调里 | 同步写在 `<script>` 顶部 |
| 黑屏 +1 | 用了 `video.play()` | 删掉，让 hyperframes 控制 |

## 9. 渲染完核对

```bash
# 抽 5 帧看效果
for t in 5 15 25 40 55; do
  ffmpeg -y -ss $t -i renders/final.mp4 -frames:v 1 -q:v 2 /tmp/check-$t.jpg
done
```

把 5 帧给用户看 → 通过就交付。
