# Verification & Rendering Options / 验证报告与渲染参数说明

> Full render verification of all 18 built-in styles, plus a deep dive into the frame padding, card-background and fixed-height (poster/cover) options exposed by `scripts/export_image.js`.
> 全部 18 种内置风格的完整渲染验证，以及 `scripts/export_image.js` 暴露的相框边距、卡片背景、固定版式（海报/封面卡）参数详解。

---

## 1. Render Verification Summary / 验证总结

**EN** — All 18 styles (+ XiaoHongShu Style B, 19 renders total) passed a full render pass: HTML generation → emoji check → screenshot → visual review. 6 signature web fonts loaded correctly via the public Google Fonts CDN with system-font fallback. No CSS breakage, no garbled text, no layout overflow across any style.

**中文** — 全部 18 种风格（含小红书风模式 B，共 19 次渲染）均通过完整验证流程：HTML 生成 → emoji 检查 → 截图 → 视觉复核。6 种特色 Web 字体均通过公开 Google Fonts CDN 加载成功，并有系统字体兜底。所有风格均无 CSS 破损、无乱码、无布局溢出。

| Check / 检查项 | Result / 结果 |
|---|---|
| Styles rendered / 渲染风格数 | 19 / 19 ✅ |
| Emoji check / emoji 检查 | 19 / 19 PASS（无 emoji）|
| Signature fonts loaded / 特色字体加载 | 6 / 6 via Google Fonts CDN |
| Frame padding / 相框边距 | Uniform 32px on all four edges by default / 默认四边统一 32px |
| Card background / 卡片背景 | On by default for all 18 styles / 18 种风格默认开启 |

---

## 2. `export_image.js` Options / 参数详解

```bash
node scripts/export_image.js <html> <output.png> [width] \
  [--author "text" | --no-footer] [--fixed-height <px>] [--frame <px>] [--flat]
```

### `--frame <px>` — Canvas frame padding / 画布相框边距

**EN** — In long-image mode (default), the canvas width is `content width + frame × 2`, and the body's top/bottom padding is force-set to `frame` px — producing a uniform frame on all four edges instead of the content touching the canvas edge. Default `32`. Pass `--frame 0` to disable (content flush to the edge). Fixed-height mode (`--fixed-height`) ignores this flag automatically, since the poster/cover container already fills the canvas with its own internal padding.

**中文** — 长图模式（默认）下，画布宽度 = 内容宽度 + `frame × 2`，body 上下 padding 被强制设为 `frame` px，从而产生四边统一的相框效果，而不是内容直接贴边。默认 `32`。传 `--frame 0` 可关闭（内容贴边）。固定版式（`--fixed-height`）会自动忽略该参数，因为海报/封面卡容器本身已占满画布并自带内部留白。

```bash
node scripts/export_image.js page.html out.png 560              # 默认 32px 相框 / default 32px frame
node scripts/export_image.js page.html out.png 560 --frame 48   # 自定义边距 / custom frame
node scripts/export_image.js page.html out.png 560 --frame 0    # 关闭相框，内容贴边 / disable, edge-to-edge
```

### `--flat` — Card background toggle / 卡片背景开关

**EN** — All 18 styles ship a themed card background on `.container` by default (background color + border + radius/shadow, matching each style's own palette — e.g. neon-outlined cards for Cyberpunk, paper-textured hairline borders for Ink Scroll), producing a "card floating on canvas" look together with the frame padding. Pass `--flat` to opt out and restore the flat, edge-to-edge look where content merges directly into the background with no card boundary.

> ⚠️ Not recommended for the **Glassmorphism** style (`11_glass`) — its frosted-glass card *is* the core visual effect; `--flat` would remove it entirely.

**中文** — 18 种风格的 `.container` 默认都自带一层主题化的卡片背景（背景色 + 描边 + 圆角/阴影，取各风格自己的色系与气质——例如赛博风的霓虹描边卡片、水墨风的纸感细边框），配合相框边距形成"卡片浮于画布"的装裱效果。传 `--flat` 可关闭，恢复老版本的扁平通栏效果：内容直接融入背景，无卡片边界。

> ⚠️ 不建议对**玻璃拟态风**（`11_glass`）使用 `--flat`——它的毛玻璃卡片本身就是核心视觉效果，关闭后该效果会完全消失。

```bash
node scripts/export_image.js page.html out.png 560           # 默认带卡片背景 / card background on
node scripts/export_image.js page.html out.png 560 --flat    # 关闭，回到扁平通栏 / flat, edge-to-edge
```

### `--fixed-height <px>` — Poster / cover card mode / 固定版式（海报 / 封面卡）

**EN** — Skips the automatic height measurement and outputs a canvas of exactly the given height, for fixed-ratio layouts such as 3:4 (600×800) quote posters and cover cards. The style's `.container` should switch to `width: 600px; height: 800px; display: flex; flex-direction: column; justify-content: center;` for vertically-centered content.

**中文** — 跳过自动高度测量，输出精确指定高度的画布，用于 3:4（600×800）等固定比例版式，如金句海报、封面卡。对应风格的 `.container` 应改为 `width: 600px; height: 800px; display: flex; flex-direction: column; justify-content: center;` 实现内容垂直居中。

```bash
node scripts/export_image.js poster.html poster.png 600 --fixed-height 800
```

<table>
  <tr>
    <td width="50%" align="center" valign="top">
      <b>Quote Poster / 金句海报</b><br/>
      <sub>Ink Scroll style, 600×800 / 水墨风，3:4 固定</sub><br/><br/>
      <img src="../assets/poster-quote-example.png" width="260" alt="Quote Poster example / 金句海报示例"/>
      <br/><sub>Vermilion seal + quote marks + centered quote + brush-stroke divider + attribution / 朱印标记 + 引号装饰 + 放大金句 + 毛笔横扫分割线 + 出处小字</sub>
    </td>
    <td width="50%" align="center" valign="top">
      <b>Cover Card / 封面卡</b><br/>
      <sub>XiaoHongShu style, 600×800 / 小红书风，3:4 固定</sub><br/><br/>
      <img src="../assets/cover-card-example.png" width="260" alt="Cover Card example / 封面卡示例"/>
      <br/><sub>Capsule badge + bold title + subtitle + selling-point cards + glow accents / 胶囊徽标 + 黑红对比大标题 + 副题 + 卡片式卖点列表 + 柔光晕装饰球</sub>
    </td>
  </tr>
</table>

---

## 3. Environment Notes / 环境坑记录

**EN**
1. If the container's proxy certificate chain is incomplete, Chrome may silently fail to load HTTPS font CDNs. Add `--ignore-certificate-errors` to the Puppeteer launch args (already applied in `scripts/export_image.js`).
2. Google Fonts CDN (`fonts.googleapis.com`) is used for the 6 signature fonts; in some regions a mirror may load faster — swap the `<link>` URL if needed. System-font fallback ensures rendering is never blocked.
3. `scripts/check_emoji.py` must pass (exit 0) before screenshotting — headless Chrome has no color-emoji font and renders emoji as tofu boxes.

**中文**
1. 若容器代理证书链不完整，Chrome 加载 HTTPS 字体 CDN 可能静默失败。需要在 Puppeteer 启动参数中加 `--ignore-certificate-errors`（`scripts/export_image.js` 已内置此项）。
2. 6 种特色字体使用 Google Fonts CDN（`fonts.googleapis.com`）；部分地区可替换为速度更快的镜像 `<link>` 地址。系统字体兜底确保渲染不会被阻塞。
3. 截图前必须让 `scripts/check_emoji.py` 通过（exit 0）——headless Chrome 没有彩色 emoji 字体，会把 emoji 渲染成方块乱码。

---

## Related docs / 相关文档

- [`README.md`](../README.md) — quick start, style list, style gallery / 快速开始、风格列表、样式画廊
- [`SKILL.md`](../SKILL.md) — full AI-agent workflow / 完整 AI Agent 工作流程
- [`CHANGELOG.md`](../CHANGELOG.md) — version history / 版本历史
