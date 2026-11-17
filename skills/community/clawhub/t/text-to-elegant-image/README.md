# text-to-elegant-image

> Turn Markdown or plain text into beautifully typeset, high-resolution long images (share cards / posters) — with 18 built-in visual styles.

Generates a self-contained HTML file and renders it to a crisp PNG via headless Chrome (Puppeteer). Designed for AI agents (OpenClaw / Claude Code / Cursor, etc.) as a skill, but the scripts also run standalone.

## Features

- **18 built-in visual styles** — Cyberpunk/Tech, Minimalist, Apple Premium, Cowork Light-Tech, Newspaper, Bloomberg Terminal, Ink Scroll, Steampunk, XiaoHongShu/REDNote, Morandi, Glassmorphism, Palace, Fresh, Earthy, Dreamy, Macaron, Carbon, Vivid — one self-contained file per style under `resources/styles/`.
- **Visualization component library** — KPI cards, progress bars, comparison bars, donut charts, flow steps, timelines (`resources/components.css`), themed per style via `--t2e-*` CSS variables.
- **Signature web-font injection** — 6 curated display fonts (public Google Fonts CDN) wired into matching styles, with system-font fallback so rendering never blocks.
- **Poster & cover layouts** — fixed 3:4 (600×800) quote-poster / cover-card modes via `--fixed-height 800`, alongside the default auto-height long-image mode.
- **Frame padding** — uniform 32px canvas frame on all four edges by default; tune with `--frame <px>` or disable with `--frame 0`.
- **High-DPI output** — 2× `deviceScaleFactor` for retina-sharp PNGs.
- **Auto height cropping** — measures the real content height and trims trailing whitespace precisely.
- **Scripted emoji check** — `scripts/check_emoji.py` catches emoji before screenshotting (headless Chrome renders them as tofu boxes).
- **No external assets** — icons are pure CSS/inline SVG; the only allowed network resource is the public font CDN (with fallback).
- **Cross-platform Chrome detection** — Linux / macOS / WSL, no manual config.
- **Configurable output dir** — via `T2EI_OUTPUT_DIR` env var (defaults to `./output`).
- **Footer control** — default footer, custom author line, or no footer.

## Requirements

- **Node.js** ≥ 18
- **Chrome / Chromium** (any recent build; auto-detected)
- **puppeteer-core** (installed on first run via `setup.sh`)

## Quick Start

```bash
# Clone
git clone https://github.com/Songhonglei/text-to-elegant-image.git
cd text-to-elegant-image

# Install dependency (puppeteer-core)
bash scripts/setup.sh

# Render an HTML file to PNG
node scripts/export_image.js /path/to/page.html ./output/card.png 600
```

As an AI-agent skill, point your agent at `SKILL.md` — it describes the full workflow (parse content → pick a style from `resources/styles/` → generate HTML → emoji check → screenshot).

## Output directory

Resolved in this priority order:

1. Path passed explicitly on the command line
2. `T2EI_OUTPUT_DIR` environment variable
3. Default: `./output`

```bash
export T2EI_OUTPUT_DIR="$HOME/my-images"   # optional, persist in ~/.bashrc
```

## Styles

Each of the 18 styles lives in its own file under [`resources/styles/`](./resources/styles/) (`01_cyberpunk.md` … `18_vivid.md`), containing complete CSS, an HTML skeleton, component color-variable mapping, optional font injection and signature decorations. [`resources/styles/_BASE.md`](./resources/styles/_BASE.md) holds the shared HTML skeleton and typography rules. Each style uses a `.container` base plus a namespaced class set (e.g. `.mo-*` for Morandi, `.gl-*` for Glass), so styles never collide.

> ⚠️ **No emoji in generated HTML** — headless Chrome lacks color-emoji fonts and renders them as tofu boxes. Use CSS shapes / inline SVG instead. (Enforced in `SKILL.md`.)

📄 **Full render verification + `--frame` / `--flat` / `--fixed-height` parameter deep-dive (bilingual EN/中文):** see [`docs/VERIFICATION.md`](./docs/VERIFICATION.md).

## Image delivery


This open-source edition focuses purely on **text → elegant image** generation and returns a local PNG path. Auto-pushing images to IM channels (WeChat / Telegram / Slack, etc.) is **not built in** — wire up your platform's Bot/API downstream if you need it (optional adapters may come in a future version).

## Install in your AI agent

| Agent | Install |
|---|---|
| OpenClaw | `clawhub install text-to-elegant-image` |
| Claude Code | Manual: copy to `~/.claude/skills/` |
| Cursor | Manual: copy to `.cursor/skills/` |

## License

MIT — see [LICENSE](./LICENSE).

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for details.

### v1.1.0 (2026-07-27)

- Architecture: split the single style reference into 18 per-style files (`resources/styles/`), added visualization component library (`resources/components.css`), signature web-font injection, `--frame` canvas padding, adaptive screenshot height, fixed 3:4 poster/cover layouts (`--fixed-height`), and scripted emoji checking (`scripts/check_emoji.py`).

### v1.0.0 (2026-07-13)

- Initial public release: 18 visual styles, high-DPI headless-Chrome rendering, configurable output dir.

---

## Appendix: Style Gallery / 附录：样式画廊

All 18 built-in styles, rendered from the same content. 全部 18 种内置样式（相同内容、不同样式渲染）。

<table>
  <tr>
    <td width="50%" align="center" valign="top">
      <b>1. Cyberpunk / 赛博科技风</b><br/>
      <sub>Dark neon, SVG grid / 深色霓虹 · SVG 网格</sub><br/><br/>
      <img src="./assets/01-cyberpunk.png" width="300" alt="Cyberpunk / 赛博科技风"/>
    </td>
    <td width="50%" align="center" valign="top">
      <b>2. Minimalist / 极简优雅风</b><br/>
      <sub>White, serif, whitespace / 白底衬线 · 留白</sub><br/><br/>
      <img src="./assets/02-minimalist.png" width="300" alt="Minimalist / 极简优雅风"/>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <b>3. Apple / 苹果质感风</b><br/>
      <sub>Frosted cards, window dots / 毛玻璃卡片</sub><br/><br/>
      <img src="./assets/03-apple.png" width="300" alt="Apple / 苹果质感风"/>
    </td>
    <td width="50%" align="center" valign="top">
      <b>4. Cowork / 轻科技风</b><br/>
      <sub>Gray-white + accent blue / 灰白点缀蓝</sub><br/><br/>
      <img src="./assets/04-cowork.png" width="300" alt="Cowork / 轻科技风"/>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <b>5. Newspaper / 报纸杂志风</b><br/>
      <sub>Cream paper, letterpress / 米黄铅字</sub><br/><br/>
      <img src="./assets/05-newspaper.png" width="300" alt="Newspaper / 报纸杂志风"/>
    </td>
    <td width="50%" align="center" valign="top">
      <b>6. Bloomberg / 终端风</b><br/>
      <sub>Dark terminal, data rows / 深色终端</sub><br/><br/>
      <img src="./assets/06-bloomberg.png" width="300" alt="Bloomberg / 终端风"/>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <b>7. Ink Scroll / 水墨卷轴风</b><br/>
      <sub>Rice paper, ink, seal / 宣纸水墨印章</sub><br/><br/>
      <img src="./assets/07-ink-scroll.png" width="300" alt="Ink Scroll / 水墨卷轴风"/>
    </td>
    <td width="50%" align="center" valign="top">
      <b>8. Steampunk / 蒸汽朋克风</b><br/>
      <sub>Brass gears, rivets / 黄铜齿轮铆钉</sub><br/><br/>
      <img src="./assets/08-steampunk.png" width="300" alt="Steampunk / 蒸汽朋克风"/>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <b>9. XiaoHongShu / 小红书风</b><br/>
      <sub>Coral red note cards / 珊瑚红笔记卡</sub><br/><br/>
      <img src="./assets/09-xiaohongshu.png" width="300" alt="XiaoHongShu / 小红书风"/>
    </td>
    <td width="50%" align="center" valign="top">
      <b>10. Morandi / 莫兰迪高级灰</b><br/>
      <sub>Muted warm grays / 低饱和暖灰</sub><br/><br/>
      <img src="./assets/10-morandi.png" width="300" alt="Morandi / 莫兰迪高级灰"/>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <b>11. Glassmorphism / 玻璃拟态</b><br/>
      <sub>Gradient + backdrop blur / 渐变毛玻璃</sub><br/><br/>
      <img src="./assets/11-glassmorphism.png" width="300" alt="Glassmorphism / 玻璃拟态"/>
    </td>
    <td width="50%" align="center" valign="top">
      <b>12. Palace / 故宫风</b><br/>
      <sub>Gold & vermilion, classic / 金红国风</sub><br/><br/>
      <img src="./assets/12-palace.png" width="300" alt="Palace / 故宫风"/>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <b>13. Fresh / 清新自然绿风</b><br/>
      <sub>Light greens, nature / 浅绿自然</sub><br/><br/>
      <img src="./assets/13-fresh.png" width="300" alt="Fresh / 清新自然绿风"/>
    </td>
    <td width="50%" align="center" valign="top">
      <b>14. Earthy / 大地原木风</b><br/>
      <sub>Warm earth, wood / 大地色原木</sub><br/><br/>
      <img src="./assets/14-earthy.png" width="300" alt="Earthy / 大地原木风"/>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <b>15. Dreamy / 优雅紫梦幻风</b><br/>
      <sub>Purple gradient glow / 紫色梦幻</sub><br/><br/>
      <img src="./assets/15-dreamy.png" width="300" alt="Dreamy / 优雅紫梦幻风"/>
    </td>
    <td width="50%" align="center" valign="top">
      <b>16. Macaron / 马卡龙粉彩风</b><br/>
      <sub>Pastel candy colors / 马卡龙粉彩</sub><br/><br/>
      <img src="./assets/16-macaron.png" width="300" alt="Macaron / 马卡龙粉彩风"/>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <b>17. Carbon / 暗色极简风</b><br/>
      <sub>Deep dark, minimal / 深色极简</sub><br/><br/>
      <img src="./assets/17-carbon.png" width="300" alt="Carbon / 暗色极简风"/>
    </td>
    <td width="50%" align="center" valign="top">
      <b>18. Vivid / 活力渐变风</b><br/>
      <sub>Purple-pink-orange / 紫粉橙渐变</sub><br/><br/>
      <img src="./assets/18-vivid.png" width="300" alt="Vivid / 活力渐变风"/>
    </td>
  </tr>
</table>
