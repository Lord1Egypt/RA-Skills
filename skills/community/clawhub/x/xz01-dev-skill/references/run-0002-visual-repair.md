# run-0002 visual repair notes

Use these notes when an xz01 temporary homepage run renders successfully but AI visual review says it is still not close enough to `demo_xz01`, has viewport defects, or has right-side alignment problems.

## Visual target learned from run-0002

A homepage that is merely functional is not enough when the user asks to continue improving toward `xz01_demo`. The closer target is a high-density download-station portal:

- PC: orange/red gradient header, search/navigation, dense first screen, icon recommendations, category keyword rows, carousel/news area, rank/sidebar, activities/gifts/news columns, hot games/apps, topic collections.
- Mobile: red/orange header, search/nav pills, hero banner, daily recommendations, news banner/list, hot games/apps, strategy/news blocks, topic collections.

## AI visual repair loop pattern

1. Generate/upgrade the template in the run directory.
2. Deploy to `/www/wwwroot/www.900az.com/public/themes/default/` with a backup and clear runtime cache.
3. Validate HTTP 200 and compiled PHP syntax after rendering both PC and mobile.
4. Take screenshots and run AI visual checks for both ends.
5. Treat AI visual findings as repair input, not final caveats. Patch the run and deployment copy, clear cache, and re-validate.
6. Only report pass after the final AI check confirms the visible defect is fixed.

## Domain + User-Agent validation rule

The user corrected this explicitly: **M-domain validation must use a real mobile User-Agent. Do not validate `https://m.900az.com/` with the same desktop/browser access mode used for PC.**

Use separate access modes:

```bash
UA_PC='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
UA_M='Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'

curl -k -L -A "$UA_PC" https://www.900az.com/
curl -k -L -A "$UA_M" https://m.900az.com/

/usr/bin/google-chrome --headless=new --no-sandbox --disable-gpu --ignore-certificate-errors \
  --window-size=1365,1800 --user-agent="$UA_PC" \
  --screenshot=/root/.hermes/workspace/xz01-factory/runs/<run_id>/screenshots/pc.png \
  https://www.900az.com/

/usr/bin/google-chrome --headless=new --no-sandbox --disable-gpu --ignore-certificate-errors \
  --window-size=390,1600 --user-agent="$UA_M" \
  --screenshot=/root/.hermes/workspace/xz01-factory/runs/<run_id>/screenshots/mobile.png \
  https://m.900az.com/
```

Verification expectations:

- PC response should contain PC markers such as `xz-pc-header`, and not mobile markers.
- Mobile response should contain mobile markers such as `xz-m-header`, and not PC markers.
- Mobile response must have no `target="_blank"`.
- Both should be HTTP 200 and have no `系统发生错误`.

## PC repair patterns from run-0002

AI flagged that PC was closer to the demo but still had:

- hot game/app modules with too few cards and large blank areas;
- topic cards whose oversized background text interfered with foreground titles;
- overly loose spacing that felt more like a modern card site than a dense download portal;
- right-side layout misalignment: the sidebar extended farther right than lower sections, and the page showed horizontal overflow.

Durable fixes:

- Provide enough fallback items to fill the grid, e.g. 8-12 hot game/app cards rather than 3-4.
- Compress module margins/gaps/padding when targeting demo-like density.
- Lower opacity/saturation or reposition decorative large text in topic cards.
- Keep rank/sidebar/list blocks dense and visible in the first screen.
- If adding content under the PC right-side “本周专题” makes the right sidebar taller than the left hero card, do not leave the left column visually empty. Either keep the grid `align-items:start` and add meaningful left-column content (e.g. quick topic cards) or reduce the right-side content height so the lower three-column section does not appear disconnected.
- A practical repair for the PC right sidebar is: `下载排行 → 本周专题 → 专题推荐` on the right, plus a short `xz-quick-row` of 4 cards at the bottom of the left “今日推荐” card to balance the two columns.
- For stubborn PC gaps just above lower modules such as `游戏活动`, adjust both sides of the seam: compress `.xz-triple-news` top spacing and reduce the sidebar inter-card `gap`; otherwise one column can still create a small visual shelf even after the quick cards are tightened.
- Use `minmax(0,1fr)` for grids so fixed gaps do not push right edges out.
- Add `html,body{overflow-x:hidden}` only as a guard after fixing the actual over-wide elements.
- Decorative pseudo-elements inside right-side cards should not increase `scrollWidth`; keep them inside the card (`right:12px`) or safely clipped.

Useful overflow probe in browser console:

```js
(() => {
  const ww = document.documentElement.clientWidth;
  return [...document.querySelectorAll('*')]
    .map(e => {
      const r = e.getBoundingClientRect();
      return { tag:e.tagName, cls:e.className, text:(e.innerText||'').slice(0,20), x:r.x, w:r.width, right:r.right, scrollW:e.scrollWidth, clientW:e.clientWidth };
    })
    .filter(o => o.right > ww + 1 || o.x < -1 || o.scrollW > o.clientW + 1)
    .slice(0,50);
})()
```

## Mobile viewport repair patterns from run-0002

Browser UI snapshots may show content, while a real 390px screenshot can reveal horizontal clipping. Always verify with a true small screenshot plus mobile UA, not only the default browser viewport.

If AI reports left blank strip, right-side clipping, or right-side misalignment:

- Do not stop at `overflow-x:hidden`; fix the actual container/grid sizing.
- Do not set mobile containers to a fixed `max-width:390px`; it can look correct in a 390px test but leave an empty right strip on wider real phones. Use `width:100%; max-width:100%` under phone breakpoints unless intentionally centering a phone shell.
- Keep grids as `repeat(2, minmax(0, 1fr))` for daily recommendations and topic/strategy blocks.
- Ensure cards use `min-width:0` and the parent grid/card widths fit inside the visible viewport.
- Clip decorative hero/topic overflow without clipping main card content.
- Use flex for section titles and MORE buttons so the right edge is stable across modules.
- Use flex for app/game list rows: icon fixed, info `flex:1; min-width:0`, download button `flex:0 0 auto`.
- Re-run the 390px screenshot and AI check after every viewport patch.
- Also take a long 390px screenshot (e.g. height 3000) to include lower modules such as 热门应用 / 攻略 / 精选专辑; a first-viewport screenshot is not enough to verify the lower right edge.

Example final guard used in run-0002:

```css
@media (max-width:600px){
  .xz-m-header,.xz-m-main,.xz-m-footer{width:100%;max-width:100%;margin-left:0;margin-right:0}
  .xz-m-main{padding-left:10px;padding-right:10px;overflow:hidden}
  .xz-m-visual,.xz-m-card,.xz-m-banner,.xz-m-strategy-top a,.xz-m-album-card{overflow:hidden}
  .xz-m-visual{width:calc(100% + 20px);max-width:none;margin-left:-10px;margin-right:-10px}
  .xz-m-recom-grid,.xz-m-strategy-top,.xz-m-album-grid{max-width:100%;grid-template-columns:repeat(2,minmax(0,1fr))}
  .xz-m-section-title{display:flex;align-items:center;justify-content:space-between;gap:8px}
  .xz-m-section-title a{flex:0 0 auto;max-width:58px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .xz-m-recom-card{min-width:0;overflow:hidden}
  .xz-m-item{display:flex;align-items:center;gap:8px;overflow:hidden}
  .xz-m-item .info{flex:1;min-width:0;margin:0}
  .xz-m-item .btn{flex:0 0 auto;white-space:nowrap}
  .xz-backtop{right:10px}
}
```

## Screenshot artifact rule

For Hermes WebUI reporting, save/copy screenshots under `/root/.hermes/workspace/...` and reference them with `MEDIA:/absolute/path`. Do not rely on `/www/...` paths for WebUI media display.

## Reporting pattern

Use the user's current concise xz01 format:

- conclusion;
- completed changes;
- issues found and fixed;
- validation result;
- artifact links and screenshots;
- remaining small issues.

Do not use the old 10-column OpenClaw table unless explicitly requested.
