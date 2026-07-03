# Trip Planner — HTML Output Spec (Design System)

This is the **output specification** for the final travel-plan HTML. It is adapted from the
`study-notes` skill's design system — the proven scaffold, color system, dark-mode theme,
collapsible blocks, hierarchical TOC + sub-heading navigator, colored callouts, and scroll-position
memory are kept verbatim. The math/KaTeX machinery is removed and replaced with travel components:
an embedded **Leaflet + OpenStreetMap** map, **per-day timeline cards**, **POI (point-of-interest)
cards**, **transport-segment cards**, a **budget table**, and an interactive **pre-departure
checklist**.

Produce **ONE standalone HTML file**. Everything (CSS, JS) is inline. The only external resources
are the Leaflet CDN (JS/CSS) and OpenStreetMap raster tiles — both need **no API key**. If they fail
to load (e.g. offline), the JS degrades gracefully and the rest of the page still works.

Copy the CSS block and the HTML/JS template **verbatim**, then fill in the content.

---

## What is kept from study-notes vs. what is new

| Mechanism | Status |
|---|---|
| Color tokens + dark-mode (`@media prefers-color-scheme:dark`) | **kept verbatim** |
| `.page` wrapper, header, tags | kept |
| Hierarchical TOC (`.toc-l1` / `.toc-l2`) | kept |
| `.sec-COLOR` section wrappers + `.section-header` | kept (each **day** is a section) |
| `.card` (h3/h4/h5, lists, paragraphs) | kept |
| Collapsible `<details>` / `<summary>` / `.details-body` | kept |
| Colored `.callout` family | kept base CSS, **retargeted** to travel semantics |
| `.steps` (numbered steps) | kept (use for "如何前往" directions) |
| Floating navigator (tracks `.sec-COLOR` + `.card h3`) | **kept verbatim** |
| Scroll-position memory (localStorage) | kept (KaTeX gating removed) |
| KaTeX, math macros, `.fbox`/`.frow`/`.big-formula`, error banner | **removed** |
| Embedded Leaflet/OSM map (`#map`, markers, day routes) | **new** |
| `.poi` cards, `.day-meta`, `.transport` cards | **new** |
| `.budget` table, `.checklist` with localStorage persistence | **new** |

---

## Full CSS

```css
:root {
  --bg:#ffffff; --bg2:#f7f6f2; --bg3:#f0ede6; --bg4:#e8e4db;
  --text:#1a1a18; --text2:#5a5a56; --text3:#8a8a84;
  --border:rgba(0,0,0,0.11);
  --purple:#534AB7; --purple-light:#EEEDFE; --purple-dark:#3C3489; --purple-mid:#7F77DD;
  --teal:#0F6E56;   --teal-light:#E1F5EE;   --teal-dark:#085041;   --teal-mid:#1D9E75;
  --coral:#993C1D;  --coral-light:#FAECE7;  --coral-dark:#712B13;  --coral-mid:#D85A30;
  --amber:#BA7517;  --amber-light:#FAEEDA;  --amber-dark:#854F0B;  --amber-mid:#EF9F27;
  --blue:#185FA5;   --blue-light:#E6F1FB;   --blue-dark:#0C447C;   --blue-mid:#378ADD;
  --green:#3B6D11;  --green-light:#EAF3DE;  --green-dark:#27500A;  --green-mid:#639922;
  --red:#A32D2D;    --red-light:#FCEBEB;    --red-dark:#791F1F;
  --pink:#993556;   --pink-light:#FBEAF0;
  --radius:10px;
}
@media(prefers-color-scheme:dark){
  :root{
    --bg:#1e1e1c; --bg2:#252523; --bg3:#2c2c2a; --bg4:#333330;
    --text:#e8e6de; --text2:#a8a69e; --text3:#706e68;
    --border:rgba(255,255,255,0.1);
    --purple-light:#26215C; --teal-light:#04342C; --coral-light:#4A1B0C;
    --amber-light:#412402; --blue-light:#042C53; --green-light:#173404;
    --red-light:#501313; --pink-light:#4B1528;
  }
}
*{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);font-size:15px;line-height:1.8;}
.page{max-width:900px;margin:0 auto;padding:32px 24px 100px;}
/* Safety net: if a div escapes .page due to a tag mismatch, body still constrains width */
body>*:not(.page){max-width:900px;margin-left:auto;margin-right:auto;padding-left:24px;padding-right:24px;}

/* ── Global width normalisation ── */
.card,.callout,.poi,.transport,.toc,table,.two-col,.steps,.map-card,.checklist,.highlight-box,.hotel{
  width:100%;max-width:100%;box-sizing:border-box;
}
/* Wide tables may scroll horizontally on the table element itself */
table{overflow-x:auto;display:block;}

/* ── Themed hero header ── a gradient banner keyed to the trip's subject.
   Always give .header one theme-* class; optionally one deco-* overlay.
   Text sits at z-index:1 above the decorative ::after layer. Works in light
   AND dark mode (it's a self-contained dark banner with light text). */
.header{position:relative;overflow:hidden;text-align:center;color:#f4f3ff;
  border-radius:18px;padding:54px 28px 40px;margin:0 0 42px;
  background:linear-gradient(160deg,#27408b 0%,#3a3f8f 45%,#1d8a6e 100%);}
.header h1{font-size:30px;font-weight:700;margin-bottom:10px;letter-spacing:-0.5px;
  position:relative;z-index:1;color:#fff;}
.header .subtitle{font-size:14px;margin-bottom:18px;position:relative;z-index:1;
  color:rgba(255,255,255,0.82);line-height:1.7;}
.tags{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;position:relative;z-index:1;}
/* translucent pills that read on any gradient — the "包起来" look */
.tag{display:inline-flex;align-items:center;gap:6px;padding:5px 13px;border-radius:20px;
  font-size:12px;font-weight:600;color:#fff;
  background:rgba(255,255,255,0.16);border:1px solid rgba(255,255,255,0.28);}

/* Theme gradient presets — pick the one matching the trip's mood, or write a
   custom `background:linear-gradient(...)` inline on .header to fit the place. */
.theme-night {background:linear-gradient(160deg,#1a1f4b 0%,#2d2a6e 38%,#0f6e56 100%);} /* 观星/沙漠夜/极光 */
.theme-ocean {background:linear-gradient(160deg,#0b3a6f 0%,#1167a8 45%,#1d9e9e 100%);} /* 海岛/海滨/潜水 */
.theme-sunset{background:linear-gradient(160deg,#6e2545 0%,#c0432f 50%,#e7972a 100%);} /* 城市夜景/浪漫/沙漠日落 */
.theme-forest{background:linear-gradient(160deg,#123421 0%,#1f6e4e 50%,#3f8a3a 100%);} /* 雨林/山野/徒步/茶园 */
.theme-city  {background:linear-gradient(160deg,#232a45 0%,#34407a 50%,#4d6fae 100%);} /* 都市/购物/现代建筑 */
.theme-sakura{background:linear-gradient(160deg,#8a3a6b 0%,#b65a86 45%,#7b6fd0 100%);} /* 日本/赏花/春季粉调 */
.theme-snow  {background:linear-gradient(160deg,#243b63 0%,#3f6fb0 55%,#86b6e6 100%);} /* 滑雪/雪国/冬季 */
.theme-desert{background:linear-gradient(160deg,#5e3417 0%,#b5762f 52%,#dcab53 100%);} /* 沙漠/戈壁/丝路 */

/* Decorative overlays (optional, theme-flavoured). Add e.g. class="header theme-night deco-stars". */
.deco-stars::after{content:"";position:absolute;inset:0;pointer-events:none;opacity:0.85;
  background-image:
    radial-gradient(1.4px 1.4px at 12% 22%,#fff 50%,transparent),
    radial-gradient(1.2px 1.2px at 28% 60%,#fff 50%,transparent),
    radial-gradient(1.6px 1.6px at 47% 30%,#fff 50%,transparent),
    radial-gradient(1.1px 1.1px at 63% 70%,#fff 50%,transparent),
    radial-gradient(1.7px 1.7px at 78% 18%,#fff 50%,transparent),
    radial-gradient(1.2px 1.2px at 88% 52%,#fff 50%,transparent),
    radial-gradient(1.3px 1.3px at 38% 82%,#fff 50%,transparent),
    radial-gradient(1.1px 1.1px at 70% 40%,#fff 50%,transparent);}
/* soft light blobs — good for ocean/sunset/sakura warmth */
.deco-glow::after{content:"";position:absolute;inset:0;pointer-events:none;opacity:0.5;
  background:radial-gradient(40% 60% at 80% 12%,rgba(255,255,255,0.35),transparent 70%),
            radial-gradient(46% 64% at 14% 90%,rgba(255,255,255,0.18),transparent 70%);}

/* TOC — hierarchical outline style */
.toc{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:22px 26px;margin-bottom:44px;}
.toc-title{font-size:12px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:14px;}
.toc-l1{margin-bottom:2px;}
.toc-l1>a{display:flex;align-items:center;gap:8px;color:var(--text);text-decoration:none;
  font-size:14px;font-weight:600;padding:5px 6px;border-radius:6px;transition:background 0.12s;}
.toc-l1>a:hover{background:var(--bg3);}
.toc-l1>a .sec-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.toc-l2{padding-left:22px;margin-top:1px;margin-bottom:3px;}
.toc-l2 a{display:flex;align-items:center;gap:7px;color:var(--blue);text-decoration:none;
  font-size:13px;padding:3px 6px;border-radius:5px;transition:background 0.12s;
  border-left:2px solid var(--border);}
.toc-l2 a:hover{background:var(--bg3);text-decoration:none;}
.toc-l2 a .sec-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;opacity:0.7;}

/* Section (= one day, or a top-level block like 概览 / 预算 / 清单) */
.section{margin-bottom:60px;}
.section-header{display:flex;align-items:center;gap:14px;margin-bottom:22px;padding-bottom:14px;border-bottom:2.5px solid var(--border);}
.section-num{min-width:36px;height:36px;padding:0 8px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;flex-shrink:0;}
.section-header .sh-text{flex:1;}
.section h2{font-size:23px;font-weight:700;}
.section .sh-sub{font-size:13px;color:var(--text2);font-weight:500;margin-top:2px;}

/* ── Cards ── */
.card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:22px 26px;margin-bottom:16px;}
.card h3{font-size:17px;font-weight:700;margin:0 0 16px;padding-bottom:10px;border-bottom:1px solid var(--border);}
.card h4{font-size:14px;font-weight:700;margin:20px 0 8px;padding-left:10px;
  border-left:3px solid var(--border);color:var(--text);line-height:1.4;}
.card h5{font-size:13px;font-weight:600;margin:14px 0 6px;color:var(--text2);letter-spacing:0.02em;}
.card p{margin-bottom:10px;line-height:1.8;}
.card p:last-child{margin-bottom:0;}
.card ul,.card ol{padding-left:22px;margin-bottom:10px;}
.card li{margin-bottom:6px;line-height:1.8;font-size:14px;}

/* Highlight box — for the trip overview / a key fact (replaces study-notes' .fbox) */
.highlight-box{background:var(--bg3);border-left:3.5px solid var(--blue);border-radius:0 10px 10px 0;padding:16px 20px;margin:14px 0;}
.highlight-box .hl-label{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:8px;opacity:0.75;}

/* Callouts — base CSS kept from study-notes; classes retargeted to travel use */
.callout{border-radius:9px;padding:14px 18px;margin:14px 0;display:flex;gap:13px;}
.callout-icon{font-size:15px;flex-shrink:0;margin-top:3px;line-height:1;}
.callout-body{flex:1;}
.callout-body > strong{display:block;font-size:13px;font-weight:700;margin-bottom:5px;}
.callout-body p strong,.callout-body li strong{display:inline;font-size:inherit;font-weight:700;}
.callout-body p,.callout-body li{font-size:14px;margin:0 0 4px;line-height:1.7;}
.callout-body ul{padding-left:18px;margin:0;}
/* Travel callout semantics:
   info=blue💡 须知/一般信息 | tip=teal✦ 省钱省时小技巧 | warn=amber⚠ 注意(排队/天气/治安)
   must=red★ 必订/必约/需提前预订 | avoid=pink✗ 避雷/不推荐 | weather=purple🌧 雨天/极端天气 Plan B */
.info{background:var(--blue-light);border:1px solid rgba(24,95,165,0.18);}
.info .callout-icon::before{content:"💡";}
.tip{background:var(--teal-light);border:1px solid rgba(15,110,86,0.18);}
.tip .callout-icon::before{content:"✦";color:var(--teal);font-size:13px;}
.warn{background:var(--amber-light);border:1px solid rgba(186,117,23,0.2);}
.warn .callout-icon::before{content:"⚠";color:var(--amber);}
.must{background:var(--red-light);border:1px solid rgba(163,45,45,0.22);}
.must .callout-icon::before{content:"★";color:var(--red);}
.avoid{background:var(--pink-light);border:1px solid rgba(153,53,86,0.2);}
.avoid .callout-icon::before{content:"✗";color:var(--pink);font-size:13px;}
.weather{background:var(--purple-light);border:1px solid rgba(83,74,183,0.2);}
.weather .callout-icon::before{content:"🌧";}

/* Tables (incl. budget) */
table{width:100%;border-collapse:collapse;font-size:14px;margin:14px 0;}
th{background:var(--bg3);font-weight:600;padding:10px 14px;text-align:left;border:1px solid var(--border);}
td{padding:10px 14px;border:1px solid var(--border);vertical-align:middle;line-height:1.7;}
tr:nth-child(even) td{background:var(--bg2);}
.budget td.num,.budget th.num{text-align:right;font-variant-numeric:tabular-nums;}
.budget tr.dayhead td{font-weight:700;background:var(--bg3);color:var(--text);border-top:2px solid var(--border);}
.budget tr.subtotal td{font-weight:600;background:var(--bg2);color:var(--text2);}
.budget tr.total td{font-weight:700;background:var(--blue-light);border-top:2px solid var(--blue);}

/* Collapsible details */
details{border:1px solid var(--border);border-radius:9px;margin-bottom:10px;overflow:visible;}
summary{padding:13px 18px;font-weight:600;font-size:14px;cursor:pointer;background:var(--bg2);display:flex;align-items:center;gap:8px;list-style:none;user-select:none;}
summary::-webkit-details-marker{display:none;}
summary::before{content:"▶";font-size:9px;color:var(--text3);transition:transform 0.2s;flex-shrink:0;}
details[open] summary::before{transform:rotate(90deg);}
.details-body{padding:18px 20px;}
.details-body p{margin-bottom:8px;font-size:14px;}

/* Numbered steps (e.g. 如何前往 / 换乘指引) */
.steps{margin:8px 0;}
.step{display:flex;gap:14px;margin-bottom:16px;}
.step-num{width:28px;height:28px;border-radius:50%;font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;}
.step-body{flex:1;font-size:14px;line-height:1.75;}
.step-body > strong{display:block;margin-bottom:4px;}
.step-body p strong,.step-body li strong{display:inline;font-weight:700;}

/* ── POI (point-of-interest) card ── one stop in a day's timeline.
   Lives inside a day section as <div class="card poi sec-aware">. The left color bar
   comes from the enclosing .sec-COLOR via the accent rules further down. */
.poi{position:relative;border-left:4px solid var(--border);}
.poi .poi-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:10px;
  padding-bottom:0;border-bottom:none;}
.poi .poi-time{font-size:14px;font-weight:700;font-variant-numeric:tabular-nums;
  background:var(--bg3);border:1px solid var(--border);border-radius:6px;padding:2px 9px;flex-shrink:0;}
.poi h3{font-size:17px;font-weight:700;margin:0;padding:0;border:none;flex:1;min-width:0;}
.poi .poi-meta{display:flex;flex-wrap:wrap;gap:7px;margin:4px 0 10px;}
.meta-chip{display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:600;
  background:var(--bg3);border:1px solid var(--border);border-radius:20px;padding:3px 11px;color:var(--text2);}
.meta-chip .mc-ico{font-size:12px;opacity:0.85;}
.poi .poi-tip{font-size:13px;color:var(--text2);background:var(--bg);border:1px dashed var(--border);
  border-radius:7px;padding:8px 12px;margin-top:8px;line-height:1.6;}
.poi .poi-tip::before{content:"💬 ";opacity:0.8;}

/* Day overview strip (under the day section header): 当日花费 + 步数 + 主要点数 */
.day-meta{display:flex;flex-wrap:wrap;gap:8px;margin:-8px 0 18px;}
.day-meta .meta-chip{background:var(--bg2);}
.day-meta .spend{background:var(--green-light);border-color:rgba(59,109,17,0.3);color:var(--green-dark);}

/* ── Transit connector ── sits BETWEEN two POI cards = 到下一点的通勤/路线段.
   Mirrors the day's route on the map: mode + distance + time. */
.transit{display:flex;justify-content:center;align-items:center;gap:8px;margin:-4px 0 12px;
  font-size:12.5px;color:var(--text2);}
.transit .tpill{display:inline-flex;align-items:center;gap:6px;background:var(--bg2);
  border:1px solid var(--border);border-radius:20px;padding:3px 12px;font-weight:600;white-space:nowrap;}
.transit .tarrow{color:var(--text3);font-size:13px;}

/* ── Transport segment card (flight / train / intercity) ── */
.transport{background:var(--bg2);border:1px solid var(--border);border-left:4px solid var(--blue);
  border-radius:var(--radius);padding:18px 22px;margin-bottom:16px;}
.transport .tr-head{display:flex;align-items:center;gap:10px;margin-bottom:12px;}
.transport .tr-ico{font-size:20px;flex-shrink:0;}
.transport .tr-title{font-size:15px;font-weight:700;}
.transport .tr-route{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:10px 0;}
.transport .tr-node{text-align:center;min-width:84px;}
.transport .tr-node .t-time{font-size:18px;font-weight:700;font-variant-numeric:tabular-nums;}
.transport .tr-node .t-place{font-size:12px;color:var(--text2);margin-top:2px;}
.transport .tr-arrow{flex:1;min-width:60px;text-align:center;color:var(--text3);font-size:12px;
  border-top:2px dashed var(--border);position:relative;top:8px;}
.transport .tr-arrow span{position:relative;top:-10px;background:var(--bg2);padding:0 8px;}
.transport .tr-foot{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px;}
.transport .tr-price{font-size:14px;font-weight:700;color:var(--green-dark);}
.btn-link{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;
  text-decoration:none;color:var(--blue-dark);background:var(--blue-light);
  border:1px solid rgba(24,95,165,0.25);border-radius:7px;padding:5px 12px;transition:filter .12s;}
.btn-link:hover{filter:brightness(0.96);}

/* ── Multi-platform price comparison (机票必做：查多个平台比价) ── inside a flight .transport card */
.price-compare{margin-top:11px;border-top:1px dashed var(--border);padding-top:9px;}
.price-compare .pc-title{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;
  color:var(--text3);margin-bottom:6px;}
.pc-row{display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:13px;padding:3px 0;}
.pc-row .pc-plat{color:var(--text2);}
.pc-row .pc-price{font-variant-numeric:tabular-nums;font-weight:600;}
.pc-row.cheapest .pc-plat{color:var(--green-dark);font-weight:600;}
.pc-row.cheapest .pc-price{color:var(--green-dark);}
.pc-row.cheapest .pc-plat::after{content:" ✓ 最低";font-size:11px;font-weight:700;color:var(--green-dark);}

/* ── Hotel option card (住宿备选) ── group ≥3 .hotel blocks inside one .card (h3 = 住宿备选).
   If the user already has accommodation, replace with ONE 已订住宿 card and put
   data-hotels="user-booked" on that .card so check_html.py knows the omission is deliberate. */
.hotel{border:1px solid var(--border);border-radius:9px;padding:14px 16px;margin:12px 0;background:var(--bg);}
.hotel:first-of-type{margin-top:4px;}
.hotel .h-head{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:6px;}
.hotel .h-name{font-size:15px;font-weight:700;}
.hotel .h-rating{display:inline-flex;align-items:baseline;gap:4px;margin-left:auto;font-size:12px;color:var(--text3);white-space:nowrap;}
.hotel .h-rating b{font-size:15px;color:var(--green-dark);font-variant-numeric:tabular-nums;}
.chain-badge{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:700;
  background:var(--teal-light);color:var(--teal-dark);border:1px solid rgba(15,110,86,0.25);
  border-radius:5px;padding:1px 8px;}
.hotel .h-meta{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0;}
/* 评论体检 — the "we read the reviews, not the blurb" box */
.review-check{font-size:12.5px;line-height:1.65;background:var(--bg2);border:1px solid var(--border);
  border-radius:7px;padding:9px 12px;margin:8px 0;}
.review-check .rc-title{font-weight:700;font-size:10px;text-transform:uppercase;letter-spacing:0.05em;
  color:var(--text3);margin-bottom:4px;}
.review-check .rc-good{color:var(--green-dark);font-weight:600;}
.review-check .rc-bad{color:var(--coral-dark);font-weight:600;}
.rank-tag{display:inline-block;font-size:10px;font-weight:700;border-radius:4px;padding:1px 7px;}
.rank-tag.rec{background:var(--green-light);color:var(--green-dark);}
.rank-tag.alt{background:var(--bg3);color:var(--text2);}

/* ── Pre-departure / packing checklist ── */
.checklist{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:14px 20px;margin-bottom:16px;}
.checklist label{display:flex;align-items:flex-start;gap:10px;padding:7px 4px;font-size:14px;
  cursor:pointer;border-bottom:1px solid var(--border);line-height:1.6;}
.checklist label:last-child{border-bottom:none;}
.checklist input[type=checkbox]{width:17px;height:17px;margin-top:3px;flex-shrink:0;accent-color:var(--teal);cursor:pointer;}
.checklist input:checked + span{color:var(--text3);text-decoration:line-through;}

/* ── Embedded Leaflet map ── */
.map-card{padding:0;overflow:hidden;border:1px solid var(--border);border-radius:var(--radius);
  background:var(--bg2);margin-bottom:16px;}
#map{height:440px;width:100%;}
@media(max-width:580px){#map{height:340px;}}
.map-hint{font-size:12px;color:var(--text3);padding:8px 16px;border-top:1px solid var(--border);}
.map-legend{display:flex;flex-wrap:wrap;gap:14px;padding:10px 16px;border-top:1px solid var(--border);}
.leg-item{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:600;color:var(--text2);}
.leg-dot{width:13px;height:13px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px var(--border);flex-shrink:0;}
/* Leaflet numbered pin (built via divIcon in JS) */
.pin{width:24px;height:24px;border-radius:50%;color:#fff;font-size:12px;font-weight:700;
  display:flex;align-items:center;justify-content:center;border:2px solid #fff;
  box-shadow:0 1px 4px rgba(0,0,0,.45);}
.leaflet-popup-content{font-size:13px;line-height:1.5;}

/* Two-column layout */
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0;}
@media(max-width:580px){.two-col{grid-template-columns:1fr;}}

/* Badges */
.badge{display:inline-block;padding:2px 9px;border-radius:4px;font-size:11px;font-weight:600;margin-right:4px;}
.b-purple{background:var(--purple-light);color:var(--purple-dark);}
.b-teal{background:var(--teal-light);color:var(--teal-dark);}
.b-coral{background:var(--coral-light);color:var(--coral-dark);}
.b-amber{background:var(--amber-light);color:var(--amber-dark);}
.b-blue{background:var(--blue-light);color:var(--blue-dark);}
.b-green{background:var(--green-light);color:var(--green-dark);}
.b-red{background:var(--red-light);color:var(--red-dark);}

/* ── Chips ── reusable pill for wrapping short items anywhere in the body
   (必吃清单、亮点、随手鸟点/物种、关键词…). Wrap a run of them; they flow + wrap.
   .star = 招牌/必看 (amber highlight); .muted = 机会/备选 (dashed, dimmed). */
.chips{display:flex;flex-wrap:wrap;gap:6px 7px;margin:8px 0;}
.chip{display:inline-flex;align-items:center;gap:5px;background:var(--bg3);border:1px solid var(--border);
  border-radius:20px;padding:3px 11px;font-size:12px;font-weight:600;color:var(--text2);
  white-space:nowrap;line-height:1.7;}
.chip.star{background:var(--amber-light);border-color:rgba(186,117,23,0.3);color:var(--amber-dark);}
.chip.muted{opacity:0.72;border-style:dashed;font-weight:500;}

/* Section color accents — apply to the wrapper, e.g. <div class="sec-teal"> */
.sec-purple .section-num{background:var(--purple-light);color:var(--purple-dark);}
.sec-purple .section h2{color:var(--purple-dark);}
.sec-purple .poi{border-left-color:var(--purple);}
.sec-purple .step-num{background:var(--purple-light);color:var(--purple-dark);}
.sec-teal .section-num{background:var(--teal-light);color:var(--teal-dark);}
.sec-teal .section h2{color:var(--teal-dark);}
.sec-teal .poi{border-left-color:var(--teal);}
.sec-teal .step-num{background:var(--teal-light);color:var(--teal-dark);}
.sec-coral .section-num{background:var(--coral-light);color:var(--coral-dark);}
.sec-coral .section h2{color:var(--coral-dark);}
.sec-coral .poi{border-left-color:var(--coral);}
.sec-coral .step-num{background:var(--coral-light);color:var(--coral-dark);}
.sec-amber .section-num{background:var(--amber-light);color:var(--amber-dark);}
.sec-amber .section h2{color:var(--amber-dark);}
.sec-amber .poi{border-left-color:var(--amber);}
.sec-amber .step-num{background:var(--amber-light);color:var(--amber-dark);}
.sec-blue .section-num{background:var(--blue-light);color:var(--blue-dark);}
.sec-blue .section h2{color:var(--blue-dark);}
.sec-blue .poi{border-left-color:var(--blue);}
.sec-blue .step-num{background:var(--blue-light);color:var(--blue-dark);}
.sec-green .section-num{background:var(--green-light);color:var(--green-dark);}
.sec-green .section h2{color:var(--green-dark);}
.sec-green .poi{border-left-color:var(--green);}
.sec-green .step-num{background:var(--green-light);color:var(--green-dark);}
.sec-red .section-num{background:var(--red-light);color:var(--red-dark);}
.sec-red .section h2{color:var(--red-dark);}
.sec-red .poi{border-left-color:var(--red);}
.sec-red .step-num{background:var(--red-light);color:var(--red-dark);}

/* ── Floating section navigator ── */
#nav-btn{
  position:fixed;bottom:24px;right:24px;z-index:9999;
  width:34px;height:34px;border-radius:8px;
  background:var(--bg2);color:var(--text2);
  border:1px solid var(--border);cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 1px 6px rgba(0,0,0,0.18);
  transition:background 0.15s,color 0.15s,box-shadow 0.15s;
  font-size:15px;line-height:1;
}
#nav-btn:hover{background:var(--bg3);color:var(--text);box-shadow:0 2px 12px rgba(0,0,0,0.22);}
#nav-panel{
  position:fixed;bottom:66px;right:24px;z-index:9998;
  background:var(--bg);border:1px solid var(--border);border-radius:10px;
  box-shadow:0 4px 20px rgba(0,0,0,0.18);
  width:240px;max-height:65vh;overflow-y:auto;
  padding:8px 0;
  opacity:0;transform:translateY(8px) scale(0.97);
  pointer-events:none;transition:opacity 0.15s,transform 0.15s;
}
#nav-panel.open{opacity:1;transform:none;pointer-events:auto;}
#nav-panel a{
  display:flex;align-items:center;gap:9px;
  padding:6px 14px;font-size:13px;color:var(--text);
  text-decoration:none;line-height:1.4;
  transition:background 0.1s;
}
#nav-panel a:hover{background:var(--bg2);}
#nav-panel .nav-title{
  font-size:10px;font-weight:700;color:var(--text3);
  text-transform:uppercase;letter-spacing:0.08em;
  padding:0 14px 5px;border-bottom:1px solid var(--border);margin-bottom:3px;
}
```

---

## HTML Page Template

Fill in the `TRIP` JS object (map data), the TOC, and the day sections. Keep the `<head>`, the
`<script>` at the bottom, and the CSS verbatim.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DESTINATION N日游 · 行程计划</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧭</text></svg>">
<!-- Leaflet (OpenStreetMap, no API key). Degrades gracefully if it fails to load. -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<!-- Disable browser scroll-restoration so our localStorage restore wins -->
<script>if('scrollRestoration' in history) history.scrollRestoration = 'manual';</script>
<style>
/* PASTE FULL CSS HERE */

/* ── Mobile adaptation (≤640px) ── phones get tighter spacing, stacked transport
   routes, wrapped price rows and a full-width floating nav. Required on every trip page;
   check_html.py fails the build without it. */
@media(max-width:640px){
  .page{padding:16px 12px 76px;}
  body>*:not(.page){padding-left:12px;padding-right:12px;}
  .header{padding:30px 16px 24px;margin-bottom:28px;border-radius:13px;}
  .header h1{font-size:21px;letter-spacing:0;line-height:1.35;}
  .header .subtitle{font-size:12.5px;margin-bottom:13px;}
  .tags{gap:6px;}
  .tag{padding:4px 10px;font-size:11.5px;}
  .toc{padding:14px 13px;margin-bottom:28px;}
  .section{margin-bottom:38px;}
  .section-header{gap:10px;margin-bottom:15px;padding-bottom:10px;}
  .section-num{min-width:30px;height:30px;font-size:12.5px;}
  .section h2{font-size:18.5px;}
  .card{padding:14px 13px;}
  .card h3{font-size:15.5px;}
  .callout{padding:11px 11px;gap:9px;margin:11px 0;}
  table{font-size:12.5px;}
  th,td{padding:7px 7px;}
  .poi .poi-head{gap:8px;}
  .transport{padding:13px 13px;}
  .transport .tr-route{flex-direction:column;align-items:flex-start;gap:3px;}
  .transport .tr-node{display:flex;align-items:baseline;gap:8px;text-align:left;min-width:0;}
  .transport .tr-node .t-time{font-size:16px;}
  .transport .tr-arrow{flex:none;width:auto;text-align:left;border:none;padding-left:24px;}
  .transport .tr-arrow span{position:static;background:none;padding:0;}
  .transport .tr-arrow span::before{content:"↓ ";}
  .pc-row{flex-direction:column;align-items:flex-start;gap:1px;padding:6px 0;
    border-bottom:1px dotted var(--border);}
  .pc-row:last-child{border-bottom:none;}
  .transit{flex-wrap:wrap;}
  .hotel{padding:12px 11px;}
  .hotel .h-rating{margin-left:0;width:100%;}
  .checklist{padding:11px 13px;}
  #map{height:320px;}
  #nav-btn{right:12px;bottom:12px;}
  #nav-panel{left:12px;right:12px;width:auto;bottom:54px;max-height:55vh;}
  html,body{max-width:100%;overflow-x:hidden;}
  .transit .tpill,.chip,.hotel .h-rating,.meta-chip{white-space:normal;}
  .transit{margin-left:0;margin-right:0;}
  .header,.toc,.card,.callout,.transport,.hotel,.poi,.checklist,.day-meta,.tags,.price-compare{
    max-width:100%;box-sizing:border-box;}
  .header *,.card *,.callout *{max-width:100%;box-sizing:border-box;overflow-wrap:break-word;}
}
</style>
</head>
<body>
<div class="page">

<!-- HERO HEADER — give it ONE theme-* class matching the trip's subject (see
     "Themed hero header" below); optionally add a deco-* overlay. The .tag pills
     are the headline facts of THIS trip (3–6 of them, each an emoji + short fact). -->
<div class="header theme-ocean deco-glow">
  <h1>DESTINATION · N日游</h1>
  <p class="subtitle">出发地 → 目的地 · 日期范围 · 同行构成 · 节奏</p>
  <div class="tags">
    <span class="tag">🏖️ 海岛 5 天</span>
    <span class="tag">👨‍👩‍👧 亲子</span>
    <span class="tag">🐢 悠闲节奏</span>
    <span class="tag">💰 中等预算</span>
    <span class="tag">🤿 2 次浮潜</span>
  </div>
</div>

<!-- TOC — one .toc-l1 per top block; days list their stops as .toc-l2 -->
<div class="toc">
  <div class="toc-title">目录</div>
  <div class="toc-l1">
    <a href="#overview"><span class="sec-dot" style="background:var(--blue-mid)"></span>行程概览 &amp; 地图</a>
  </div>
  <div class="toc-l1">
    <a href="#stay"><span class="sec-dot" style="background:var(--coral-mid)"></span>住宿备选</a>
  </div>
  <div class="toc-l1">
    <a href="#day1"><span class="sec-dot" style="background:var(--purple-mid)"></span>Day 1 · 抵达 &amp; 市区漫步</a>
    <div class="toc-l2">
      <a href="#day1-p1"><span class="sec-dot" style="background:var(--purple-mid)"></span>浅草寺</a>
      <a href="#day1-p2"><span class="sec-dot" style="background:var(--purple-mid)"></span>晴空塔</a>
    </div>
  </div>
  <div class="toc-l1">
    <a href="#day2"><span class="sec-dot" style="background:var(--teal-mid)"></span>Day 2 · ……</a>
  </div>
  <div class="toc-l1">
    <a href="#budget"><span class="sec-dot" style="background:var(--green-mid)"></span>预算估算</a>
  </div>
  <div class="toc-l1">
    <a href="#checklist"><span class="sec-dot" style="background:var(--amber-mid)"></span>出发前清单</a>
  </div>
</div>

<!-- ════ OVERVIEW + MAP ════ -->
<div class="sec-blue" id="overview">
<div class="section">
  <div class="section-header">
    <div class="section-num">🗺️</div>
    <div class="sh-text"><h2>行程概览 &amp; 地图</h2>
      <div class="sh-sub">N 天 · 主要城市 · 关键交通</div></div>
  </div>

  <div class="highlight-box">
    <div class="hl-label">一句话概览</div>
    <p>第 1 天抵达后市区轻度活动，第 2–3 天主玩 …，最后一天上午机动、下午赶回程。整体悠闲，每天 2–3 个主要点。</p>
  </div>

  <!-- The embedded map -->
  <div class="map-card">
    <div id="map"></div>
    <div class="map-legend" id="map-legend"></div>
    <div class="map-hint">点击地图后可用滚轮缩放；点击图钉看停留点信息。地图数据 © OpenStreetMap 贡献者。</div>
  </div>

  <div class="callout info">
    <div class="callout-icon"></div>
    <div class="callout-body"><strong>怎么用这份计划</strong>
      <p>每个景点卡显示<strong>到达时间 / 停留时长 / 票价 / 营业时间</strong>，点开可看更多。右下角 ≡ 可在各天之间跳转，关掉网页再打开会回到上次看的位置。</p>
    </div>
  </div>
</div>
</div>

<!-- ════ 住宿备选 (HOTELS) ════ ≥3 options, grouped in one .card. 看评论非简介、优先连锁、多平台比价。 -->
<div class="sec-coral" id="stay">
<div class="section">
  <div class="section-header">
    <div class="section-num">🏨</div>
    <div class="sh-text"><h2>住宿备选</h2><div class="sh-sub">看的是评论区 · 优先连锁 · 多平台比价</div></div>
  </div>
  <div class="card">
    <h3 id="stay-list">市中心 · 近地铁（3 选）</h3>

    <div class="hotel">
      <div class="h-head">
        <span class="rank-tag rec">推荐</span>
        <span class="chain-badge">🏨 华住·全季</span>
        <span class="h-name">全季酒店（春熙路店）</span>
        <span class="h-rating">点评 2,310 · <b>4.6</b></span>
      </div>
      <div class="h-meta">
        <span class="meta-chip"><span class="mc-ico">📍</span>地铁2/3号线 5 min</span>
        <span class="meta-chip"><span class="mc-ico">🚶</span>到 Day2 熊猫线起点 12 min</span>
        <span class="meta-chip"><span class="mc-ico">🛏️</span>大床/双床·含早</span>
      </div>
      <div class="review-check">
        <div class="rc-title">评论体检（读的是评论区，不是简介）</div>
        <p><span class="rc-good">可信</span>：2,300+ 条、近一月仍更新、好评具体（隔音/早餐/前台）；评分分布正常，无水军式同质刷分。<span class="rc-bad">差评集中</span>：临街房偏吵 → 订房备注「安静楼层」即可。</p>
      </div>
      <div class="price-compare">
        <div class="pc-title">每晚比价（浏览器实时查 · 7/15）</div>
        <div class="pc-row cheapest"><span class="pc-plat"><a class="btn-link" style="padding:1px 8px" href="https://www.huazhu.com" target="_blank" rel="noopener">华住会App·会员</a></span><span class="pc-price">¥318</span></div>
        <div class="pc-row"><span class="pc-plat">美团</span><span class="pc-price">¥335</span></div>
        <div class="pc-row"><span class="pc-plat">携程</span><span class="pc-price">¥339</span></div>
      </div>
    </div>

    <div class="hotel">
      <div class="h-head">
        <span class="rank-tag alt">次选</span>
        <span class="chain-badge">🏨 锦江·维也纳</span>
        <span class="h-name">维也纳国际酒店（XX店）</span>
        <span class="h-rating">点评 1,540 · <b>4.5</b></span>
      </div>
      <div class="h-meta">
        <span class="meta-chip"><span class="mc-ico">📍</span>地铁口 3 min</span>
        <span class="meta-chip"><span class="mc-ico">🛏️</span>房间略大</span>
      </div>
      <div class="review-check">
        <div class="rc-title">评论体检</div>
        <p><span class="rc-good">可信</span>：评论真实、性价比口碑稳。<span class="rc-bad">注意</span>：早餐一般，电梯高峰排队——可避高峰。</p>
      </div>
      <div class="price-compare">
        <div class="pc-title">每晚比价（浏览器实时查 · 7/15）</div>
        <div class="pc-row cheapest"><span class="pc-plat">去哪儿</span><span class="pc-price">¥285</span></div>
        <div class="pc-row"><span class="pc-plat">携程</span><span class="pc-price">¥299</span></div>
      </div>
    </div>

    <div class="hotel">
      <div class="h-head">
        <span class="rank-tag alt">备选</span>
        <span class="chain-badge">🏨 如家·首旅</span>
        <span class="h-name">如家精选（XX店）</span>
        <span class="h-rating">点评 980 · <b>4.4</b></span>
      </div>
      <div class="review-check">
        <div class="rc-title">评论体检</div>
        <p><span class="rc-good">可信</span>：连锁基准、干净稳定，预算更省。差评零散无重大复发项。</p>
      </div>
      <div class="price-compare">
        <div class="pc-title">每晚比价（浏览器实时查 · 7/15）</div>
        <div class="pc-row cheapest"><span class="pc-plat">飞猪</span><span class="pc-price">¥246</span></div>
        <div class="pc-row"><span class="pc-plat">携程</span><span class="pc-price">¥259</span></div>
      </div>
    </div>

    <div class="callout warn" style="margin:10px 0 0;">
      <div class="callout-icon"></div>
      <div class="callout-body"><strong>选房原则</strong>
        <p>连锁优先（卫生/服务有底），但<strong>评论压过品牌</strong>——某家分店近期差评集中就换掉。价格随时变，订前再核。</p>
      </div>
    </div>
  </div>
</div>
</div>

<!-- ════ ONE SECTION PER DAY ════
     .page > .sec-COLOR#dayN > .section > .section-header / .day-meta / transport / .card.poi …
     Cycle section colors across days (purple→teal→coral→amber→blue→green→red).
-->
<div class="sec-purple" id="day1">
<div class="section">
  <div class="section-header">
    <div class="section-num">D1</div>
    <div class="sh-text"><h2>Day 1 · 抵达 &amp; 市区漫步</h2>
      <div class="sh-sub">周三 6/24 · 晴 28°C / 19°C · 浅草—墨田区一带</div></div>
  </div>

  <!-- day overview line: 当日花费 + 步数 + 主要点（spend 必须等于预算表里该天的小计） -->
  <div class="day-meta">
    <span class="meta-chip spend"><span class="mc-ico">💰</span>当日 ¥520</span>
    <span class="meta-chip"><span class="mc-ico">👣</span>~9,000 步（≈ 6.5 km）</span>
    <span class="meta-chip"><span class="mc-ico">📍</span>2 个主要点</span>
  </div>

  <!-- arrival transport at the top of day 1 (see transport card template below) -->
  <div class="transport">
    <div class="tr-head"><span class="tr-ico">✈️</span><span class="tr-title">去程航班 · MU523</span></div>
    <div class="tr-route">
      <div class="tr-node"><div class="t-time">09:05</div><div class="t-place">上海浦东 PVG</div></div>
      <div class="tr-arrow"><span>约 3h · 直飞</span></div>
      <div class="tr-node"><div class="t-time">13:10</div><div class="t-place">东京成田 NRT</div></div>
    </div>
    <div class="tr-foot">
      <span class="tr-price">最低 ¥1,820</span>
      <span class="meta-chip"><span class="mc-ico">🧳</span>含 23kg 托运</span>
      <a class="btn-link" href="https://flights.ctrip.com" target="_blank" rel="noopener">查余票 ↗</a>
    </div>
    <!-- flights ONLY:用浏览器实查多平台，最便宜的加 class="cheapest"。班次相同、价格随时变，注明"浏览器实时查 + 时点"。 -->
    <div class="price-compare">
      <div class="pc-title">多平台比价 · 同一航班（浏览器实时查 · 6/10 14:30）</div>
      <div class="pc-row cheapest"><span class="pc-plat"><a class="btn-link" style="padding:1px 8px" href="https://flight.qunar.com" target="_blank" rel="noopener">去哪儿</a></span><span class="pc-price">¥1,820</span></div>
      <div class="pc-row"><span class="pc-plat">飞猪</span><span class="pc-price">¥1,880</span></div>
      <div class="pc-row"><span class="pc-plat">携程</span><span class="pc-price">¥1,920</span></div>
      <div class="pc-row"><span class="pc-plat">东航官网</span><span class="pc-price">¥1,950</span></div>
    </div>
  </div>

  <div class="callout warn" style="margin:0 0 16px;">
    <div class="callout-icon"></div>
    <div class="callout-body"><strong>赶车缓冲</strong>
      <p>成田到市区 NEX 约 1 小时，落地+入关+取行李预留 90 分钟，所以当天第一个景点排在 16:00 之后。</p>
    </div>
  </div>

  <!-- POI card: one per stop. h3 id must match the TOC l2 href so the navigator lists it. -->
  <div class="card poi">
    <div class="poi-head">
      <span class="poi-time">16:30</span>
      <h3 id="day1-p1">浅草寺 雷门</h3>
    </div>
    <div class="poi-meta">
      <span class="meta-chip"><span class="mc-ico">⏱️</span>停留 1.5h</span>
      <span class="meta-chip"><span class="mc-ico">🎫</span>免费</span>
      <span class="meta-chip"><span class="mc-ico">🕒</span>境内 24h（堂内 6:00–17:00）</span>
      <span class="meta-chip"><span class="mc-ico">🚇</span>浅草站步行 5 min</span>
    </div>
    <p>东京最古老的寺院，雷门大灯笼是地标。仲见世商店街适合边走边吃小食。</p>
    <p class="poi-tip">傍晚人少、灯笼亮灯好出片；周末白天极挤，亲子/银发建议避开正午。</p>
    <details>
      <summary>更多：如何前往 · 周边吃喝</summary>
      <div class="details-body">
        <div class="steps">
          <div class="step"><div class="step-num">1</div><div class="step-body"><strong>地铁</strong>银座线「浅草」站 1 号口出，步行 5 分钟到雷门。</div></div>
          <div class="step"><div class="step-num">2</div><div class="step-body"><strong>晚餐</strong>商店街附近「大黑家」天妇罗盖饭（17:00 后排队短）。</div></div>
        </div>
      </div>
    </details>
  </div>

  <!-- transit connector: 上一站 → 下一站（步行/地铁/打车 + 距离 + 时间）。This is the route between stops. -->
  <div class="transit">
    <span class="tarrow">↓</span>
    <span class="tpill">🚶 约 600 m · 步行 8 min</span>
  </div>

  <div class="card poi">
    <div class="poi-head">
      <span class="poi-time">18:30</span>
      <h3 id="day1-p2">东京晴空塔</h3>
    </div>
    <div class="poi-meta">
      <span class="meta-chip"><span class="mc-ico">⏱️</span>停留 1h</span>
      <span class="meta-chip"><span class="mc-ico">🎫</span>¥2,100（展望台）</span>
      <span class="meta-chip"><span class="mc-ico">🕒</span>10:00–22:00</span>
    </div>
    <p>夜景制高点，从浅草步行/一站地铁可达，串成「黄昏—夜景」一条线。</p>
    <div class="callout must" style="margin:8px 0 0;">
      <div class="callout-icon"></div>
      <div class="callout-body"><strong>建议提前订</strong>
        <p>官网可买<strong>定时票</strong>免现场排队，旺季日落时段常售罄。</p>
      </div>
    </div>
  </div>

</div>
</div>
<!-- repeat .sec-COLOR#dayN blocks for each day -->

<!-- ════ BUDGET ════ -->
<div class="sec-green" id="budget">
<div class="section">
  <div class="section-header">
    <div class="section-num">💰</div>
    <div class="sh-text"><h2>预算估算</h2><div class="sh-sub">2 人 · 不含购物 · 单位 ¥</div></div>
  </div>
  <div class="card">
    <!-- 固定大项分一组，其余按天拆小计；每个 Day 小计必须等于该天 .day-meta 的「当日花费」 -->
    <table class="budget">
      <thead><tr><th>项目</th><th class="num">明细</th><th class="num">小计 (¥)</th></tr></thead>
      <tbody>
        <tr class="dayhead"><td colspan="3">固定大项（往返交通 + 住宿）</td></tr>
        <tr><td>往返机票（2 人）</td><td class="num">¥1,820 ×2</td><td class="num">3,640</td></tr>
        <tr><td>住宿 4 晚</td><td class="num">¥650 ×4</td><td class="num">2,600</td></tr>
        <tr class="subtotal"><td colspan="2">固定大项小计</td><td class="num">6,240</td></tr>

        <tr class="dayhead"><td colspan="3">Day 1 · 抵达 &amp; 市区</td></tr>
        <tr><td>门票（晴空塔 ×2）</td><td class="num">¥150 ×2</td><td class="num">300</td></tr>
        <tr><td>餐饮</td><td class="num">—</td><td class="num">180</td></tr>
        <tr><td>市内交通</td><td class="num">—</td><td class="num">40</td></tr>
        <tr class="subtotal"><td colspan="2">Day 1 小计（= 当日 ¥520）</td><td class="num">520</td></tr>

        <tr class="dayhead"><td colspan="3">Day 2 · ……</td></tr>
        <tr><td>……</td><td class="num">—</td><td class="num">……</td></tr>
        <tr class="subtotal"><td colspan="2">Day 2 小计（= 当日 ¥…）</td><td class="num">…</td></tr>

        <!-- 其余每天一组，同上 -->
        <tr class="total"><td colspan="2">合计（不含购物）</td><td class="num">¥9,920</td></tr>
      </tbody>
    </table>
    <div class="callout tip" style="margin-top:12px;">
      <div class="callout-icon"></div>
      <div class="callout-body"><strong>省钱点</strong>
        <p>地铁 72h 通票比单程划算；午餐定食比晚餐便宜 30%。</p>
      </div>
    </div>
  </div>
</div>
</div>

<!-- ════ PRE-DEPARTURE CHECKLIST ════ -->
<div class="sec-amber" id="checklist">
<div class="section">
  <div class="section-header">
    <div class="section-num">✅</div>
    <div class="sh-text"><h2>出发前清单</h2><div class="sh-sub">勾选状态会自动保存在本机</div></div>
  </div>
  <div class="card">
    <h3>必订 / 必办（按截止时间排序）</h3>
    <div class="checklist">
      <label><input type="checkbox"><span>机票出票（越早越便宜）</span></label>
      <label><input type="checkbox"><span>护照有效期 ≥ 6 个月、签证</span></label>
      <label><input type="checkbox"><span>晴空塔展望台定时票</span></label>
      <label><input type="checkbox"><span>住宿确认单（截图离线）</span></label>
    </div>
  </div>
  <div class="card">
    <h3>必带物品</h3>
    <div class="checklist">
      <label><input type="checkbox"><span>转换插头（日本 A 型）/ 充电宝</span></label>
      <label><input type="checkbox"><span>常用药 + 创可贴</span></label>
      <label><input type="checkbox"><span>现金（部分小店不收卡）</span></label>
    </div>
  </div>
</div>
</div>

<div style="text-align:center;color:var(--text3);font-size:12px;padding:24px 0 8px;border-top:1px solid var(--border);margin-top:20px;">
  DESTINATION N日游行程 · 仅供参考，出行前请再次核对营业时间与票价
</div>

</div><!-- closes .page -->

<!-- ── Floating section navigator ── -->
<button id="nav-btn" title="行程导航" aria-label="行程导航">≡</button>
<div id="nav-panel" role="navigation" aria-label="行程列表">
  <div class="nav-title">行程导航</div>
  <div id="nav-list"></div>
</div>

<script>
/* ════════════ MAP DATA — fill this in ════════════
   Every stop needs lat/lng (decimal degrees). Look them up during research; city-level
   coordinates are an acceptable fallback. Colors should match each day's .sec-COLOR. */
var TRIP = {
  center: [35.68, 139.76], zoom: 11,
  days: [
    { label: 'Day 1', color: '#534AB7', stops: [
      { name: '浅草寺', lat: 35.7148, lng: 139.7967, time: '16:30' },
      { name: '东京晴空塔', lat: 35.7101, lng: 139.8107, time: '18:30' }
    ]},
    { label: 'Day 2', color: '#0F6E56', stops: [
      { name: '示例点', lat: 35.6586, lng: 139.7454, time: '09:30' }
    ]}
  ]
};

/* ════════════ Leaflet init (degrades gracefully) ════════════ */
(function(){
  if (typeof L === 'undefined') return;                 // CDN failed / offline
  var el = document.getElementById('map');
  if (!el || !window.TRIP || !TRIP.days) return;
  var map = L.map('map', { scrollWheelZoom: false })
              .setView(TRIP.center || [0,0], TRIP.zoom || 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19, attribution: '© OpenStreetMap'
  }).addTo(map);
  map.on('click', function(){ map.scrollWheelZoom.enable(); });   // don't hijack page scroll

  var all = [], legend = document.getElementById('map-legend');
  TRIP.days.forEach(function(day){
    var pts = [];
    (day.stops || []).forEach(function(s, si){
      if (typeof s.lat !== 'number' || typeof s.lng !== 'number') return;
      var ll = [s.lat, s.lng]; pts.push(ll); all.push(ll);
      var icon = L.divIcon({ className:'', iconSize:[24,24], iconAnchor:[12,12],
        html:'<div class="pin" style="background:'+day.color+'">'+(si+1)+'</div>' });
      L.marker(ll, {icon:icon}).addTo(map)
        .bindPopup('<b>'+day.label+' · '+(si+1)+'</b><br>'+s.name+(s.time?'<br>🕒 '+s.time:''));
    });
    if (pts.length > 1)
      L.polyline(pts, {color:day.color, weight:3, opacity:0.75, dashArray:'6 7'}).addTo(map);
    if (legend){
      var item = document.createElement('span'); item.className = 'leg-item';
      item.innerHTML = '<span class="leg-dot" style="background:'+day.color+'"></span>'+day.label;
      legend.appendChild(item);
    }
  });
  if (all.length) map.fitBounds(all, { padding:[34,34], maxZoom:15 });
  setTimeout(function(){ map.invalidateSize(); }, 250);
})();

/* ════════════ Scroll-position memory ════════════ */
(function(){
  var SK = 'tp:' + location.pathname;
  function doRestore(y, tries){
    if (tries <= 0) return;
    if (document.body.scrollHeight >= y + window.innerHeight * 0.5){
      if (location.hash) history.replaceState(null, '', location.pathname + location.search);
      window.scrollTo({ top: y, behavior: 'instant' });
    } else {
      setTimeout(function(){ doRestore(y, tries - 1); }, 120);
    }
  }
  function tryRestore(){
    var raw = localStorage.getItem(SK);
    if (raw !== null && +raw > 0) doRestore(+raw, 25);
  }
  window.addEventListener('load', function(){ setTimeout(tryRestore, 80); });
  window.addEventListener('pageshow', function(e){ if (e.persisted) setTimeout(tryRestore, 80); });
  var saving = false;
  window.addEventListener('scroll', function(){
    if (!saving){ saving = true;
      requestAnimationFrame(function(){
        if (window.scrollY > 0) localStorage.setItem(SK, window.scrollY);
        saving = false;
      });
    }
  }, { passive:true });
})();

/* ════════════ Checklist persistence (per-file, in localStorage) ════════════ */
(function(){
  var boxes = document.querySelectorAll('.checklist input[type=checkbox]');
  boxes.forEach(function(cb, i){
    var key = 'tpchk:' + location.pathname + ':' + i;
    if (localStorage.getItem(key) === '1') cb.checked = true;
    cb.addEventListener('change', function(){
      localStorage.setItem(key, cb.checked ? '1' : '0');
    });
  });
})();

/* ════════════ Floating navigator: hierarchical heading tracking ════════════ */
(function(){
  var COLORS = {
    purple:'#534AB7', teal:'#0F6E56', coral:'#993C1D',
    amber:'#BA7517',  blue:'#185FA5', green:'#3B6D11', red:'#A32D2D'
  };
  if (window.matchMedia('(prefers-color-scheme:dark)').matches) COLORS = {
    purple:'#AFA9EC', teal:'#5DCAA5', coral:'#F0997B',
    amber:'#EF9F27',  blue:'#85B7EB', green:'#97C459', red:'#F09595'
  };
  var list  = document.getElementById('nav-list');
  var btn   = document.getElementById('nav-btn');
  var panel = document.getElementById('nav-panel');
  if (!list || !btn || !panel) return;

  var anchors = [];
  var secs = document.querySelectorAll(
    '[id].sec-purple,[id].sec-teal,[id].sec-coral,[id].sec-amber,[id].sec-blue,[id].sec-green,[id].sec-red'
  );
  secs.forEach(function(sec){
    var hdr = sec.querySelector('.section-header');
    if (!hdr) return;
    var num   = (hdr.querySelector('.section-num')||{}).textContent || '';
    var ttl   = (hdr.querySelector('h2')||{}).textContent || '';
    var cls   = (sec.className||'').match(/sec-(\w+)/);
    var color = cls ? (COLORS[cls[1]] || '#888') : '#888';

    var row = document.createElement('a');
    row.href = '#' + sec.id;
    row.style.cssText = 'display:flex;align-items:center;gap:8px;padding:7px 14px 5px;'+
      'font-size:13px;font-weight:600;color:inherit;text-decoration:none;'+
      'transition:background 0.1s;margin-top:2px;';
    var badge = document.createElement('span');
    badge.textContent = num;
    badge.style.cssText = 'min-width:22px;height:20px;border-radius:4px;font-size:10px;font-weight:700;'+
      'display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;padding:0 3px;'+
      'background:'+color+';color:#fff;';
    var lbl = document.createElement('span');
    lbl.textContent = ttl;
    lbl.style.cssText = 'flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;';
    row.appendChild(badge); row.appendChild(lbl);
    row.addEventListener('click', function(){ panel.classList.remove('open'); });
    list.appendChild(row);
    anchors.push({ el: hdr, link: row, level: 0, color: color });

    /* sub-headings: each POI / card h3 with an id */
    sec.querySelectorAll('.card h3').forEach(function(h3, i){
      if (!h3.id) h3.id = sec.id + '-s' + i;
    });
    sec.querySelectorAll('.card h3[id]').forEach(function(h3){
      var sub = document.createElement('a');
      sub.href = '#' + h3.id;
      sub.style.cssText = 'display:flex;align-items:center;gap:7px;'+
        'padding:3px 14px 3px 32px;font-size:12px;color:var(--text2,#a8a69e);'+
        'text-decoration:none;transition:background 0.1s,color 0.1s;'+
        'border-left:2px solid transparent;margin-left:0;';
      var dot = document.createElement('span');
      dot.style.cssText = 'width:4px;height:4px;border-radius:50%;background:'+color+';'+
        'flex-shrink:0;opacity:0.5;transition:opacity 0.1s;';
      var slbl = document.createElement('span');
      slbl.textContent = h3.textContent.replace(/^\s*[\d§.]+\s*/, '');
      slbl.style.cssText = 'flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;';
      sub.appendChild(dot); sub.appendChild(slbl);
      sub.addEventListener('click', function(){ panel.classList.remove('open'); });
      list.appendChild(sub);
      anchors.push({ el: h3, link: sub, level: 1, dot: dot, color: color });
    });
  });

  var active = null;
  function setActive(a){
    if (active === a) return;
    if (active){
      active.link.style.background = '';
      if (active.level === 0){ active.link.style.fontWeight = '600'; active.link.style.color = ''; }
      else { active.link.style.color = 'var(--text2,#a8a69e)';
             active.link.style.borderLeftColor = 'transparent';
             if (active.dot) active.dot.style.opacity = '0.5'; }
    }
    active = a;
    if (!a) return;
    a.link.style.background = 'var(--bg3,#2c2c2a)';
    if (a.level === 0){ a.link.style.fontWeight = '700'; a.link.style.color = 'var(--text,#e8e6de)'; }
    else { a.link.style.color = 'var(--text,#e8e6de)';
           a.link.style.borderLeftColor = a.color || '#378ADD';
           if (a.dot) a.dot.style.opacity = '1'; }
    if (panel.classList.contains('open')) a.link.scrollIntoView({ block:'nearest' });
  }
  function updateActive(){
    var threshold = window.innerHeight * 0.30, best = null;
    for (var i = 0; i < anchors.length; i++){
      var rect = anchors[i].el.getBoundingClientRect();
      if (rect.top <= threshold) best = anchors[i]; else break;
    }
    if (!best && anchors.length) best = anchors[0];
    setActive(best);
  }
  var ticking = false;
  window.addEventListener('scroll', function(){
    if (!ticking){ ticking = true; requestAnimationFrame(function(){ updateActive(); ticking = false; }); }
  }, { passive:true });
  setTimeout(updateActive, 300);
  window.addEventListener('load', function(){ setTimeout(updateActive, 200); });

  btn.addEventListener('click', function(e){
    e.stopPropagation();
    panel.classList.toggle('open');
    if (panel.classList.contains('open') && active)
      setTimeout(function(){ active.link.scrollIntoView({ block:'nearest' }); }, 160);
  });
  document.addEventListener('click', function(e){
    if (!panel.contains(e.target) && e.target !== btn) panel.classList.remove('open');
  });
})();
</script>

</body>
</html>
```

---

## Layout Consistency Rule (MANDATORY)

Keep the div nesting clean so the navigator and width normalisation work:

- **Each day** = exactly one `<div class="sec-COLOR" id="dayN"><div class="section"> … </div></div>`.
  Every section opens 2 divs and closes 2 divs. Never nest a `.sec-COLOR` inside another.
- **Each stop** = one `<div class="card poi">` whose `<h3 id="dayN-pK">` matches its TOC `.toc-l2`
  href. The `id` is what makes the stop appear in the floating navigator.
- Only these live **directly** inside `.section` (outside a `.card`): the `.section-header`, the
  `.day-meta` strip, `.transport` cards, a section-level banner `.callout` (add `margin:0 0 16px`),
  and the `.card` / `.card poi` blocks. Everything else goes inside a card.
- The map lives in `.map-card` inside the overview section.

## Themed hero header (use on EVERY trip)

Every trip plan opens with a **themed gradient hero header** — a banner whose color and
decoration evoke the trip's subject, with the headline facts wrapped as translucent pills. This is
a required, standard element (not optional decoration): it sets the tone and gives an at-a-glance
summary before the reader scrolls.

**How to build it:**

1. Give `.header` **one `theme-*` class** whose mood matches the destination/subject. Optionally add
   **one `deco-*` overlay** for extra flavor.
2. Put the title in `<h1>`, a one-line `subtitle` (出发地 → 目的地 · 日期 · 同行 · 节奏), and **3–6
   `.tag` pills** — each an emoji + a short headline fact (天数、核心体验、预算档、节奏、人数…). These
   pills are the "各个点包起来" look.

| Theme class | Mood / use for |
|---|---|
| `theme-night` | 观星 / 沙漠夜 / 极光（深蓝紫→teal，配 `deco-stars`） |
| `theme-ocean` | 海岛 / 海滨 / 潜水（蓝→青） |
| `theme-sunset` | 城市夜景 / 浪漫 / 沙漠日落（玫红→橙） |
| `theme-forest` | 雨林 / 山野 / 徒步 / 茶园（深绿→绿） |
| `theme-city` | 都市 / 购物 / 现代建筑（靛蓝→蓝） |
| `theme-sakura` | 日本 / 赏花 / 春季（粉→紫） |
| `theme-snow` | 滑雪 / 雪国 / 冬季（冷蓝→浅蓝） |
| `theme-desert` | 沙漠 / 戈壁 / 丝路（棕→金） |

Decorative overlays: `deco-stars` (star field — for night/stargazing), `deco-glow` (soft light blobs
— warmth for ocean/sunset/sakura). Omit the deco class for a clean flat gradient.

**No preset fits?** Write a custom gradient inline — `<div class="header" style="background:
linear-gradient(160deg,#... ,#...)">` — picking 2–3 colors from the destination's signature palette
(e.g. Santorini → white-blue; Provence lavender → purple; autumn Kyoto → coral-amber). Keep the text
light; the `.header` rules already force white text and layered z-index.

```html
<div class="header theme-night deco-stars">
  <h1>青甘环线 · 15 日游</h1>
  <p class="subtitle">广州 → 敦煌 → 兰州 · 8/12–8/26 · 观星+观鸟 · 适中节奏</p>
  <div class="tags">
    <span class="tag">🌠 流星雨主峰夜</span>
    <span class="tag">🐦 26 个鸟点</span>
    <span class="tag">🚄 铁路 + 包车</span>
    <span class="tag">📸 D750 + 300mm</span>
    <span class="tag">⏱️ 15 天</span>
  </div>
</div>
```

## Chips — wrap short items as pills anywhere

For any run of short items in the body — 必吃清单、每日亮点、随手鸟点/物种、关键词 tags — wrap them
in `.chip` pills inside a `.chips` row instead of a comma list. It reads cleaner and matches the
header's pill language. Use `.star` for 招牌/必看 items, `.muted` (dashed, dimmed) for 备选/机会项.

```html
<div class="chips">
  <span class="chip star">★ 牛肉面</span>
  <span class="chip">手抓羊肉</span>
  <span class="chip">酿皮</span>
  <span class="chip muted">甜醅（看运气）</span>
</div>
```

## Day-level details: transit · daily overview · per-day budget · flight price-compare

These four pieces make the plan feel like a real route with real costs. Use them on every plan.

**1. Transit connector (到下一点的通勤 = the route between stops).** Between two consecutive POI
cards, place a `.transit` connector showing **mode + distance + time** — `🚶 约 600 m · 步行 8 min`,
`🚇 地铁2号线 3站 · 12 min`, or `🚕 ~5 km · 打车 15 min`. This is the on-the-ground "路线" between
points; it should agree with the day's route line drawn on the map. Estimate honestly (city walking
≈ 70–80 m/min; add waiting for transit). For senior/family/悠闲 trips, keep walking legs short and say
so. Omit the connector only when two "stops" are effectively the same place.

**2. Daily overview line (`.day-meta`).** At the top of every day, right under the section header,
show three chips: **当日花费**（`.spend`, green）, **步数**（`👣 ~9,000 步（≈ 6.5 km）`）, and **主要点数**.
Steps ≈ walking distance × ~1,300 步/km — derive it from the day's transit legs, don't invent a wild
number. The 当日花费 chip **must equal that day's subtotal in the budget table** (see next).

**3. Per-day budget subtotals.** Group fixed big-ticket items (往返交通 + 住宿) in one block with a
`.subtotal` row, then **one block per day** (门票 + 餐饮 + 当日交通) each ending in a `.subtotal` row,
then a final `.total` grand total. Each day's subtotal ties back to its `.day-meta` 当日花费 chip so
the two never disagree. Use `tr.dayhead` for the group header, `tr.subtotal` for subtotals,
`tr.total` for the grand total.

**4. Flight price comparison (机票必须浏览器实查).** When a leg is a **flight**, don't trust a single
web_search number — **open the booking sites in a browser and read the live fare** for the *same*
flight on multiple platforms (去哪儿 / 携程 / 飞猪 / 航司官网, + Google Flights / Skyscanner for
international), then list them in a `.price-compare` block inside the `.transport` card, **cheapest row
tagged `class="cheapest"`** and linked. Stamp the exact query time (`浏览器实时查 · 6/10 14:30`) since
prices move, and keep `.tr-price` as "最低 ¥X". **At a login wall / captcha, defer it (don't block):** read what's
visible without login, park that tab on its login page, and move on; **after all platforms are queried,
prompt the user once with the whole needs-login list so they log into all of them in one batch**, then
go back and read each. You never type passwords or solve captchas. Fall back to web_search ranges only
for sites with no browser / that the user skips, and **label them "web_search 估价 · 未浏览器核实"** — never
pass an estimate off as verified. Trains: a single fare/区间 is
fine — no multi-platform compare (12306 is the source of truth). See `references/research-playbook.md`
for the browser procedure and the safety rails.

## Hotels (住宿备选)

Give **≥3 hotel options** in a dedicated `sec-coral id="stay"` section, grouped inside one `.card`
(`<h3>` = the area, e.g. "市中心 · 近地铁"). Each option is a `.hotel` block with:

- `.h-head`: an optional `.rank-tag` (`rec` 推荐 / `alt` 次选·备选), a `.chain-badge` (the chain, e.g.
  华住·全季 / 锦江·维也纳 / 如家), the `.h-name`, and `.h-rating` (`点评 N · <b>4.6</b>`).
- `.h-meta` chips: 区域 / 到地铁 / 到当天景点群的步行距离 / 房型.
- **`.review-check`** — the non-negotiable bit: a 1–2 line summary of **what the reviews actually say**
  (read the review section, not the listing). Use `.rc-good` for the trust verdict + concrete praise and
  `.rc-bad` for the recurring complaint(s) and how to dodge them. If reviews show recurring serious
  problems (卫生/虫/隔音/不安全/偷换房型/强制消费) or fake-review tells (100% 5★, generic dateless praise),
  **don't list the hotel** — pick another.
- **`.price-compare`** — same component as flights: per-night price across 携程/去哪儿/飞猪/美团 (+ the
  group's own App, often cheapest), cheapest tagged, query time noted. Same browser + defer-and-batch
  login flow; query-only.

Prefer chains for reliability (esp. 银发/亲子) but **reviews override the brand**. Pin the top pick on the
map. Full vetting method: `references/research-playbook.md` §2.5.

## Callout Quick Reference (travel semantics)

| Class | Icon | Use for |
|---|---|---|
| `info` | 💡 | 一般须知、说明、怎么用这份计划 |
| `tip` | ✦ | 省钱 / 省时 / 当地小技巧 |
| `warn` | ⚠ | 注意：排队、天气、治安、赶车缓冲、闭馆日 |
| `must` | ★ | **必订 / 必约 / 需提前预订**（门票、餐厅、热门体验） |
| `avoid` | ✗ | **避雷 / 不推荐 / 宰客**——具体说明为什么 |
| `weather` | 🌧 | 雨天或极端天气的室内 **Plan B** |

## Section Color Assignment

Cycle day colors in order so adjacent days are visually distinct and match their map routes:
`Day1 purple → Day2 teal → Day3 coral → Day4 amber → Day5 blue → Day6 green → Day7 red`
(wrap around for longer trips). Reserve **blue** for the overview/map block, **green** for budget,
**amber** for the checklist if those don't collide with a same-colored day — it's fine if they do,
the navigator keys off `id`, not color.

## Map data rules

- Fill `TRIP.center` with the main city center and `TRIP.zoom` (10–12 for a city).
- Every stop needs numeric `lat`/`lng`. Get them during research (search "<景点> 经纬度 / coordinates",
  or use well-known values). If a precise coordinate is unavailable, use the district/landmark
  coordinate — an approximate pin is far better than no pin. Never invent precise-looking fake
  coordinates; round to ~4 decimals.
- `day.color` must equal the hex of that day's `.sec-COLOR` (purple `#534AB7`, teal `#0F6E56`,
  coral `#993C1D`, amber `#BA7517`, blue `#185FA5`, green `#3B6D11`, red `#A32D2D`).
- The marker number is the stop's order within the day; the dashed polyline traces the day's route.

## Self-contained file

The output must be a single `.html`. The only externals are the Leaflet CDN and OSM tiles. Do **not**
add Google Maps, Mapbox, or anything needing a key. If you embed any image (e.g. a cropped map or a
photo), inline it as a base64 data-URI so the file stays portable.
