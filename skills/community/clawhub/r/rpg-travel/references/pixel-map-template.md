# 杀戮尖塔风格冒险地图 HTML 模板

> **核心原则：AI 只替换数据，不重新生成 HTML 结构。**

## 默认风格

**游戏内UI风**（半透明深色面板 + 高亮标记色 + 任务侧栏感）

## 风格映射 — CSS 变量替换

生成时，用对应风格的 CSS 变量替换模板中 `:root` 区块：

| 风格 | CSS 变量值 |
|------|-----------|
| 游戏内UI风 | `--bg:#0d1117; --canvas:rgba(22,27,34,0.95); --border:#30363d; --text:#c9d1d9; --text-dim:#8b949e; --accent:#58a6ff; --green:#3fb950; --gold:#d29922; --red:#f85149; --purple:#bc8cff; --pixel-font:'SF Mono',Monaco,Consolas,monospace;` |
| 复古羊皮纸 | `--bg:#1a1208; --canvas:rgba(42,31,20,0.95); --border:#8b4513; --text:#d4c5a9; --text-dim:#a09070; --accent:#daa520; --green:#228b22; --gold:#daa520; --red:#c41e3a; --purple:#8b6914; --pixel-font:'Noto Serif SC','Songti SC',Georgia,serif;` |
| 旅行手账风 | `--bg:#f5f0e8; --canvas:#faf6ee; --border:#8b7355; --text:#3d2b1f; --text-dim:#a08060; --accent:#c41e3a; --green:#2d8a4e; --gold:#d4a017; --red:#c41e3a; --purple:#6b4c8a; --pixel-font:'Noto Serif SC','Songti SC','SimSun',Georgia,serif;` |
| 现代极简卡片 | `--bg:#f8f9fa; --canvas:#ffffff; --border:#e9ecef; --text:#212529; --text-dim:#868e96; --accent:#4263eb; --green:#20c997; --gold:#fcc419; --red:#fa5252; --purple:#7950f2; --pixel-font:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;` |
| 像素复古 | `--bg:#1a1a2e; --canvas:#16213e; --border:#0f3460; --text:#e0e0e0; --text-dim:#888; --accent:#e94560; --green:#4ecca3; --gold:#f0c040; --red:#e94560; --purple:#a855f7; --pixel-font:'SF Mono',Monaco,Consolas,'Courier New',monospace;` |
| 都市霓虹 | `--bg:#0a0a1a; --canvas:#1a0a2e; --border:#2a1a4e; --text:#e0e0e0; --text-dim:#888; --accent:#ff2d55; --green:#00ff88; --gold:#ffd700; --red:#ff2d55; --purple:#a855f7; --pixel-font:'SF Mono',Monaco,Consolas,monospace;` |
| 和风武士 | `--bg:#1a1a2e; --canvas:#2a1a1e; --border:#3a2a2e; --text:#e0e0e0; --text-dim:#888; --accent:#ff6b6b; --green:#4ecdc4; --gold:#d4a574; --red:#ff6b6b; --purple:#a78bfa; --pixel-font:'Noto Serif SC','Hiragino Sans',sans-serif;` |
| 中国古风 | `--bg:#1a0a0a; --canvas:#2a1a1a; --border:#3a2a1a; --text:#e0d5c5; --text-dim:#a09080; --accent:#c41e3a; --green:#2d8a4e; --gold:#d4a017; --red:#c41e3a; --purple:#8b5cf6; --pixel-font:'Noto Serif SC','Songti SC','SimSun',serif;` |
| 科幻未来 | `--bg:#0a0a1a; --canvas:#0a1a2a; --border:#1a2a3a; --text:#e0e0e0; --text-dim:#888; --accent:#00d4ff; --green:#00ff88; --gold:#ffffff; --red:#ff4444; --purple:#a855f7; --pixel-font:'SF Mono',Monaco,Consolas,monospace;` |

## 完整 HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[游戏名] — 圣地巡礼冒险地图</title>
  <style>
    :root {
      --bg: #0d1117;
      --canvas: rgba(22,27,34,0.95);
      --border: #30363d;
      --text: #c9d1d9;
      --text-dim: #8b949e;
      --accent: #58a6ff;
      --green: #3fb950;
      --gold: #d29922;
      --red: #f85149;
      --purple: #bc8cff;
      --pixel-font: 'SF Mono', Monaco, Consolas, monospace;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: var(--bg);
      font-family: var(--pixel-font);
      color: var(--text);
      min-height: 100vh;
    }

    /* === 全屏背景 === */
    .bg-image {
      position: fixed;
      inset: 0;
      z-index: 0;
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
    }
    .content-layer {
      position: relative;
      z-index: 1;
    }

    /* === 顶部栏 === */
    .top-bar {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(22,27,34,0.85);
      border-bottom: 1px solid rgba(255,255,255,0.06);
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      backdrop-filter: blur(16px);
    }
    .game-title {
      font-size: 16px;
      color: var(--gold);
      letter-spacing: 2px;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .game-title span { color: var(--text-dim); font-size: 11px; }
    .player-stats {
      display: flex;
      gap: 16px;
      font-size: 11px;
      flex-wrap: wrap;
      align-items: center;
    }
    .player-stats .stat { color: var(--green); }

    /* === 背景故事区 === */
    .lore-section {
      max-width: 900px;
      margin: 20px auto;
      padding: 0 24px;
    }
    .lore-card {
      background: rgba(22,27,34,0.75);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 8px;
      padding: 24px;
      position: relative;
      backdrop-filter: blur(8px);
      margin-bottom: 16px;
    }
    .lore-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--accent), var(--gold), var(--red));
    }
    .lore-title {
      font-size: 16px;
      color: var(--gold);
      margin-bottom: 12px;
      letter-spacing: 1px;
    }
    .lore-text {
      font-size: 13px;
      line-height: 1.8;
      color: var(--text-dim);
    }
    .lore-text strong { color: var(--text); }

    /* === 旅行贴士区 === */
    .tips-section {
      max-width: 900px;
      margin: 0 auto 20px;
      padding: 0 24px;
    }
    .tips-card {
      background: rgba(22,27,34,0.75);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 8px;
      padding: 20px 24px;
      backdrop-filter: blur(8px);
    }
    .tips-title {
      font-size: 14px;
      color: var(--accent);
      margin-bottom: 12px;
      letter-spacing: 1px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .tips-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }
    .tip-item {
      background: rgba(0,0,0,0.2);
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 6px;
      padding: 10px 12px;
      font-size: 11px;
      line-height: 1.6;
    }
    .tip-item strong {
      color: var(--gold);
      display: block;
      margin-bottom: 4px;
      font-size: 12px;
    }
    .tip-item.warn { border-left: 3px solid var(--red); }
    .tip-item.tip { border-left: 3px solid var(--green); }
    .tip-item.info { border-left: 3px solid var(--accent); }

    /* === 地图区域 === */
    .map-section {
      max-width: 900px;
      margin: 0 auto;
      padding: 0 24px 40px;
    }
    .map-title {
      font-size: 14px;
      color: var(--accent);
      margin-bottom: 20px;
      letter-spacing: 1px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .map-title::after {
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }

    /* 路线容器 */
    .route {
      position: relative;
      padding-left: 40px;
    }
    .route::before {
      content: '';
      position: absolute;
      left: 18px;
      top: 0;
      bottom: 0;
      width: 2px;
      background: repeating-linear-gradient(
        0deg,
        var(--border) 0px,
        var(--border) 8px,
        transparent 8px,
        transparent 16px
      );
    }

    /* 节点 */
    .node {
      position: relative;
      margin-bottom: 24px;
    }
    .node-dot {
      position: absolute;
      left: -30px;
      top: 16px;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      border: 3px solid var(--border);
      background: var(--bg);
      z-index: 2;
    }
    .node--start .node-dot { border-color: var(--green); background: var(--green); box-shadow: 0 0 12px var(--green); }
    .node--combat .node-dot { border-color: var(--red); background: var(--red); box-shadow: 0 0 12px var(--red); }
    .node--boss .node-dot { border-color: var(--red); background: var(--red); box-shadow: 0 0 16px var(--red); width: 24px; height: 24px; left: -32px; top: 14px; }
    .node--rest .node-dot { border-color: var(--gold); background: var(--gold); box-shadow: 0 0 12px var(--gold); }
    .node--shop .node-dot { border-color: var(--purple); background: var(--purple); box-shadow: 0 0 12px var(--purple); }
    .node--transport .node-dot { border-color: var(--accent); background: var(--accent); box-shadow: 0 0 12px var(--accent); }
    .node--end .node-dot { border-color: var(--green); background: var(--green); box-shadow: 0 0 12px var(--green); }

    .node-card {
      background: rgba(22,27,34,0.75);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 8px;
      padding: 16px;
      transition: all 0.2s;
      backdrop-filter: blur(8px);
    }
    .node-card:hover {
      border-color: var(--accent);
      transform: translateX(4px);
    }
    .node--combat .node-card { border-left: 4px solid var(--red); }
    .node--boss .node-card { border-left: 4px solid var(--red); }
    .node--rest .node-card { border-left: 4px solid var(--gold); }
    .node--shop .node-card { border-left: 4px solid var(--purple); }
    .node--transport .node-card { border-left: 4px solid var(--accent); }

    .node-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
    }
    .node-icon { font-size: 20px; }
    .node-name { font-size: 14px; font-weight: bold; }
    .node-badge {
      font-size: 9px;
      padding: 2px 6px;
      border-radius: 3px;
      border: 1px solid currentColor;
      margin-left: auto;
      white-space: nowrap;
    }
    .node-badge--main { color: var(--red); }
    .node-badge--side { color: var(--text-dim); }

    .node-time {
      font-size: 11px;
      color: var(--text-dim);
      margin-bottom: 8px;
    }

    /* 游戏 vs 现实 */
    .node-desc {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 10px;
      font-size: 11px;
    }
    .desc-game {
      background: rgba(248,81,73,0.08);
      border: 1px solid rgba(248,81,73,0.2);
      padding: 8px;
      border-radius: 4px;
    }
    .desc-reality {
      background: rgba(63,185,80,0.08);
      border: 1px solid rgba(63,185,80,0.2);
      padding: 8px;
      border-radius: 4px;
    }
    .desc-label {
      font-size: 9px;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 4px;
    }
    .desc-game .desc-label { color: var(--red); }
    .desc-reality .desc-label { color: var(--green); }

    /* 剧情关联 */
    .node-story {
      background: rgba(212,153,34,0.08);
      border-left: 3px solid var(--gold);
      padding: 8px 10px;
      margin-bottom: 10px;
      font-size: 11px;
      line-height: 1.6;
      color: var(--text-dim);
      border-radius: 0 4px 4px 0;
    }
    .node-story strong { color: var(--gold); }

    /* 剧情概要 */
    .node-plot {
      background: rgba(188,140,255,0.06);
      border: 1px solid rgba(188,140,255,0.15);
      border-radius: 6px;
      padding: 10px 12px;
      margin-bottom: 10px;
    }
    .node-plot-title {
      font-size: 10px;
      color: var(--purple);
      letter-spacing: 1px;
      margin-bottom: 6px;
      font-weight: bold;
    }
    .node-plot-summary {
      font-size: 11px;
      line-height: 1.7;
      color: var(--text);
      margin-bottom: 8px;
    }
    .node-dialogue {
      background: rgba(0,0,0,0.3);
      border-radius: 4px;
      padding: 8px 10px;
      margin-bottom: 6px;
      border-left: 3px solid var(--purple);
    }
    .node-dialogue:last-child { margin-bottom: 0; }
    .node-dialogue-speaker {
      font-size: 10px;
      color: var(--purple);
      font-weight: bold;
      margin-bottom: 2px;
    }
    .node-dialogue-text {
      font-size: 11px;
      line-height: 1.6;
      color: var(--text);
      font-style: italic;
    }
    .node-related-locations {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
    }
    .node-related-loc {
      font-size: 9px;
      padding: 3px 8px;
      border-radius: 10px;
      border: 1px solid rgba(188,140,255,0.3);
      color: var(--purple);
      background: rgba(188,140,255,0.08);
    }

    /* 图片对比 */
    .node-images {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 10px;
    }
    .node-img {
      border-radius: 4px;
      overflow: hidden;
      border: 1px solid var(--border);
      position: relative;
      cursor: zoom-in;
    }
    .node-img:hover {
      border-color: var(--accent);
    }
    .node-img img {
      width: 100%;
      height: 120px;
      object-fit: cover;
      display: block;
    }
    .node-img .img-placeholder {
      width: 100%;
      height: 120px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      color: var(--text-dim);
      letter-spacing: 2px;
    }
    .node-img-label {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 4px 8px;
      background: rgba(0,0,0,0.7);
      font-size: 9px;
      color: var(--text);
    }

    /* 飞猪购买卡片 */
    .buy-card {
      background: rgba(0,0,0,0.4);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 6px;
      padding: 10px 12px;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .buy-info { flex: 1; min-width: 150px; }
    .buy-name { font-size: 12px; color: var(--text); margin-bottom: 2px; }
    .buy-reason { font-size: 10px; color: var(--text-dim); }
    .buy-price {
      font-size: 18px;
      font-weight: bold;
      color: var(--gold);
      white-space: nowrap;
    }
    .buy-price small { font-size: 11px; color: var(--text-dim); }
    .buy-actions { display: flex; gap: 6px; }
    .buy-btn {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 8px 16px;
      background: var(--accent);
      color: #fff;
      text-decoration: none;
      border-radius: 6px;
      font-size: 12px;
      font-family: var(--pixel-font);
      font-weight: bold;
      white-space: nowrap;
      transition: all 0.2s;
    }
    .buy-btn:hover { opacity: 0.85; transform: translateY(-1px); }
    .copy-btn {
      padding: 8px 12px;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-dim);
      border-radius: 6px;
      font-size: 11px;
      cursor: pointer;
      font-family: var(--pixel-font);
      white-space: nowrap;
      transition: all 0.2s;
    }
    .copy-btn:hover { border-color: var(--green); color: var(--green); }
    .copy-btn.copied { border-color: var(--green); color: var(--green); }

    /* 打卡 */
    .checkin-btn {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      margin-top: 10px;
      padding: 6px 14px;
      background: var(--green);
      border: none;
      color: var(--bg);
      font-family: var(--pixel-font);
      font-size: 11px;
      cursor: pointer;
      border-radius: 4px;
      font-weight: bold;
    }
    .checkin-btn:hover { opacity: 0.85; }
    .checkin-btn.checked { background: var(--text-dim); cursor: default; }

    /* 预算警告 */
    .budget-warning {
      background: rgba(248,81,73,0.1);
      border: 1px solid var(--red);
      border-radius: 6px;
      padding: 12px 16px;
      margin: 16px 0;
      font-size: 12px;
      color: var(--red);
      line-height: 1.6;
    }

    /* 底部预算总览 */
    .budget-section {
      max-width: 900px;
      margin: 0 auto 40px;
      padding: 0 24px;
    }
    .budget-card {
      background: rgba(22,27,34,0.75);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 8px;
      padding: 20px;
      backdrop-filter: blur(8px);
    }
    .budget-title {
      font-size: 14px;
      color: var(--gold);
      margin-bottom: 16px;
      letter-spacing: 1px;
    }
    .budget-items {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-bottom: 16px;
    }
    .budget-item {
      background: rgba(0,0,0,0.3);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 6px;
      padding: 12px;
    }
    .budget-item-label { font-size: 10px; color: var(--text-dim); margin-bottom: 4px; }
    .budget-item-price { font-size: 20px; font-weight: bold; color: var(--gold); }
    .budget-item-price small { font-size: 11px; color: var(--text-dim); }
    .budget-total {
      border-top: 2px solid var(--border);
      padding-top: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }
    .budget-total-label { font-size: 14px; color: var(--text); }
    .budget-total-price { font-size: 24px; font-weight: bold; color: var(--gold); }
    .budget-total-price small { font-size: 12px; color: var(--text-dim); }

    /* 进度条 */
    .progress-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      background: rgba(0,0,0,0.4);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 4px;
      font-size: 11px;
    }
    .progress-track {
      flex: 1;
      height: 6px;
      background: rgba(255,255,255,0.1);
      border-radius: 3px;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      background: var(--green);
      transition: width 0.3s ease;
      border-radius: 3px;
    }
    .progress-text { color: var(--green); white-space: nowrap; }

    /* Toast */
    .toast {
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: var(--green);
      color: var(--bg);
      padding: 8px 20px;
      border-radius: 4px;
      font-size: 12px;
      font-family: var(--pixel-font);
      transition: transform 0.3s ease;
      z-index: 200;
    }
    .toast.show { transform: translateX(-50%) translateY(0); }

    /* Lightbox */
    .lightbox-overlay {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 9999;
      background: rgba(0,0,0,0.9);
      align-items: center;
      justify-content: center;
      cursor: zoom-out;
    }
    .lightbox-overlay.active { display: flex; }
    .lightbox-overlay img {
      max-width: 90vw;
      max-height: 90vh;
      object-fit: contain;
      border-radius: 8px;
      box-shadow: 0 0 40px rgba(0,0,0,0.5);
    }
    .lightbox-close {
      position: absolute;
      top: 20px;
      right: 24px;
      font-size: 28px;
      color: #fff;
      cursor: pointer;
      background: rgba(0,0,0,0.5);
      border: none;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .lightbox-close:hover { background: rgba(0,0,0,0.8); }

    /* 响应式 */
    @media (max-width: 600px) {
      .route { padding-left: 30px; }
      .route::before { left: 12px; }
      .node-dot { left: -24px; }
      .node-desc { grid-template-columns: 1fr; }
      .node-images { grid-template-columns: 1fr; }
      .tips-grid { grid-template-columns: 1fr; }
      .buy-card { flex-direction: column; align-items: flex-start; }
      .buy-actions { width: 100%; }
      .buy-btn, .copy-btn { flex: 1; justify-content: center; }
      .top-bar { padding: 10px 16px; }
      .game-title { font-size: 14px; }
    }
  </style>
</head>
<body>

  <!-- 全屏背景图 -->
  <div class="bg-image" style="background-image: url('[BG_IMAGE_URL]'); filter: brightness(0.6) saturate(0.8);"></div>

  <!-- 内容层 -->
  <div class="content-layer">

  <!-- 顶部栏 -->
  <div class="top-bar">
    <div class="game-title">⚔️ [游戏名] <span>圣地巡礼 · [日期]</span></div>
    <div class="player-stats">
      <div>🎮 Lv.<span id="player-level">[等级]</span></div>
      <div>📍 [出发城市] → [取景地城市]</div>
      <div>💰 ¥[预算]</div>
    </div>
  </div>

  <!-- 背景故事 -->
  <div class="lore-section">
    <div class="lore-card">
      <div class="lore-title">📖 世界观 · [游戏名]</div>
      <div class="lore-text">[LORE_TEXT]</div>
    </div>
  </div>

  <!-- 旅行贴士 -->
  <div class="tips-section">
    <div class="tips-card">
      <div class="tips-title">🎒 旅行贴士 · 行前必看</div>
      <div class="tips-grid">
        <!-- TIPS_ITEMS -->
      </div>
    </div>
  </div>

  <!-- 地图区域 -->
  <div class="map-section">
    <div class="map-title">🗺️ 冒险路线</div>

    <div class="progress-bar" style="margin-bottom:20px;">
      <span>📍 打卡</span>
      <div class="progress-track">
        <div class="progress-fill" id="progress-fill" style="width:0%"></div>
      </div>
      <span class="progress-text" id="progress-text">0/0</span>
    </div>

    <div class="route" id="route">
      <!-- NODES_START -->
      <!-- NODES_END -->
    </div>

    <!-- 预算警告 -->
    <!-- BUDGET_WARNING -->
  </div>

  <!-- 底部预算总览 -->
  <div class="budget-section">
    <div class="budget-card">
      <div class="budget-title">💰 冒险经费总览</div>
      <div class="budget-items">
        <div class="budget-item">
          <div class="budget-item-label">✈️ 传送门（交通）</div>
          <div class="budget-item-price">¥[FLIGHT_TOTAL]<small>/人</small></div>
        </div>
        <div class="budget-item">
          <div class="budget-item-label">🔥 存档点（住宿）</div>
          <div class="budget-item-price">¥[HOTEL_TOTAL]<small>/[NIGHTS]晚</small></div>
        </div>
        <div class="budget-item">
          <div class="budget-item-label">🎫 副本门票（景点）</div>
          <div class="budget-item-price">¥[POI_TOTAL]</div>
        </div>
        <div class="budget-item">
          <div class="budget-item-label">🍜 回血道具（餐饮）</div>
          <div class="budget-item-price">¥[FOOD_TOTAL]</div>
        </div>
      </div>
      <div class="budget-total">
        <div class="budget-total-label">📊 合计</div>
        <div class="budget-total-price">¥[TOTAL]<small>/人</small></div>
      </div>
    </div>
  </div>

  <!-- Toast -->
  <div class="toast" id="toast"></div>

  <!-- Lightbox -->
  <div class="lightbox-overlay" id="lightbox" onclick="closeLightbox()">
    <button class="lightbox-close" onclick="closeLightbox()">✕</button>
    <img id="lightbox-img" src="" alt="放大图片" />
  </div>

  <script>
    // 打卡数据
    const checkpoints = [CHECKPOINT_KEYS];
    let checkedCount = 0;

    function checkin(btn, key) {
      if (btn.classList.contains('checked')) return;
      btn.classList.add('checked');
      btn.textContent = '✅ 已打卡';
      localStorage.setItem('rpg-checkin-' + key, '1');
      checkedCount++;
      updateProgress();
      showToast('🎉 打卡成功！');
    }

    function updateProgress() {
      const total = checkpoints.length;
      const pct = total ? Math.round((checkedCount / total) * 100) : 0;
      document.getElementById('progress-fill').style.width = pct + '%';
      document.getElementById('progress-text').textContent = checkedCount + '/' + total;
    }

    function copyLink(url, btn) {
      navigator.clipboard.writeText(url).then(function() {
        if (btn) {
          btn.classList.add('copied');
          btn.textContent = '✅ 已复制';
          setTimeout(function() {
            btn.classList.remove('copied');
            btn.textContent = '📋 复制';
          }, 2000);
        }
        showToast('📋 链接已复制');
      }).catch(function() {
        var ta = document.createElement('textarea');
        ta.value = url;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        showToast('📋 链接已复制');
      });
    }

    function showToast(msg) {
      var toast = document.getElementById('toast');
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(function() { toast.classList.remove('show'); }, 2000);
    }

    // Lightbox
    function openLightbox(el) {
      var img = el.querySelector('img');
      if (!img) return;
      document.getElementById('lightbox-img').src = img.src;
      document.getElementById('lightbox').classList.add('active');
      document.body.style.overflow = 'hidden';
    }
    function closeLightbox() {
      document.getElementById('lightbox').classList.remove('active');
      document.body.style.overflow = '';
    }
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeLightbox();
    });

    // 恢复打卡状态
    window.addEventListener('load', function() {
      checkpoints.forEach(function(key) {
        if (localStorage.getItem('rpg-checkin-' + key) === '1') {
          checkedCount++;
          var btn = document.querySelector('[data-checkin="' + key + '"]');
          if (btn) {
            btn.classList.add('checked');
            btn.textContent = '✅ 已打卡';
          }
        }
      });
      updateProgress();
    });
  </script>
  </div>
  <!-- /content-layer -->
</body>
</html>
```

## 使用方式

生成 HTML 时：
1. 读取本文件的完整 HTML 模板
2. 根据用户选择的风格，替换 `:root` 中的 CSS 变量
3. 替换所有 `[占位符]`
4. 为每个行程节点生成 HTML 卡片，替换 `<!-- NODES_START -->` 和 `<!-- NODES_END -->` 之间的内容
5. 替换 `[LORE_TEXT]`、`[GAME_IMAGE_URL]`、`[REALITY_IMAGE_URL]` 等背景故事内容
6. 替换预算区域的 `[FLIGHT_TOTAL]`、`[HOTEL_TOTAL]` 等
7. 输出完整 HTML 文件

## 节点 HTML 模板

每个节点替换为以下格式：

```html
<!-- 起点节点 -->
<div class="node node--start">
  <div class="node-dot"></div>
  <div class="node-card">
    <div class="node-header">
      <span class="node-icon">🏠</span>
      <span class="node-name">[城市名] — 冒险起点</span>
    </div>
    <div class="node-time">[日期] · 出发</div>
    <div class="node-story">
      <strong>📖 故事</strong><br/>
      [出发故事]
    </div>
  </div>
</div>

<!-- 交通节点 -->
<div class="node node--transport">
  <div class="node-dot"></div>
  <div class="node-card">
    <div class="node-header">
      <span class="node-icon">✈️</span>
      <span class="node-name">[航班号]</span>
      <span class="node-badge" style="color:var(--accent)">传送门</span>
    </div>
    <div class="node-time">[出发时间] · [出发站] → [到达站] · [耗时]</div>
    <div class="buy-card">
      <div class="buy-info">
        <div class="buy-name">[航班描述]</div>
        <div class="buy-reason">💡 [推荐理由]</div>
      </div>
      <div class="buy-price">¥[价格]<small>/人</small></div>
      <div class="buy-actions">
        <a href="[飞猪链接]" target="_blank" rel="noopener" class="buy-btn">🛒 飞猪购买</a>
        <button class="copy-btn" onclick="copyLink('[飞猪链接]', this)">📋 复制</button>
      </div>
    </div>
  </div>
</div>

<!-- 战斗节点（景点/取景地） -->
<div class="node node--combat">
  <div class="node-dot"></div>
  <div class="node-card">
    <div class="node-header">
      <span class="node-icon">⚔️</span>
      <span class="node-name">[景点名]</span>
      <span class="node-badge node-badge--main">主线副本</span>
    </div>
    <div class="node-time">[日期] [时间] · 预计 [耗时]</div>
    <div class="node-images">
      <div class="node-img">
        <img src="[游戏图片URL]" alt="游戏中" onerror="this.parentElement.style.display='none'" />
        <div class="node-img-label">🎮 游戏中</div>
      </div>
      <div class="node-img">
        <img src="[现实图片URL]" alt="现实中" onerror="this.parentElement.style.display='none'" />
        <div class="node-img-label">🌍 现实中</div>
      </div>
    </div>
    <div class="node-desc">
      <div class="desc-game">
        <div class="desc-label">🎮 游戏中</div>
        [游戏描述]
      </div>
      <div class="desc-reality">
        <div class="desc-label">🌍 现实中</div>
        [现实描述]
      </div>
    </div>

    <!-- 剧情概要 + 台词 -->
    <div class="node-plot">
      <div class="node-plot-title">📖 剧情概要</div>
      <div class="node-plot-summary">[剧情概要：描述游戏中与此地相关的关键剧情段落，2-3句话]</div>
      <!-- 台词区块，可有多个 -->
      <div class="node-dialogue">
        <div class="node-dialogue-speaker">🗣️ [角色名]</div>
        <div class="node-dialogue-text">"[与此地相关的游戏台词或经典对白]"</div>
      </div>
      <div class="node-dialogue">
        <div class="node-dialogue-speaker">🗣️ [角色名]</div>
        <div class="node-dialogue-text">"[另一句相关台词]"</div>
      </div>
      <!-- 关联地点标签 -->
      <div class="node-related-locations">
        <span class="node-related-loc">📍 [关联地点1]</span>
        <span class="node-related-loc">📍 [关联地点2]</span>
      </div>
    </div>

    <div class="node-story">
      <strong>📖 剧情关联</strong><br/>
      [剧情关联描述：现实地点与游戏剧情的联系]
    </div>
    <div class="buy-card">
      <div class="buy-info">
        <div class="buy-name">[景点门票/体验]</div>
        <div class="buy-reason">💡 [推荐理由]</div>
      </div>
      <div class="buy-price">¥[价格]</div>
      <div class="buy-actions">
        <a href="[飞猪链接]" target="_blank" rel="noopener" class="buy-btn">🛒 飞猪购买</a>
        <button class="copy-btn" onclick="copyLink('[飞猪链接]', this)">📋 复制</button>
      </div>
    </div>
    <button class="checkin-btn" data-checkin="[节点key]" onclick="checkin(this, '[节点key]')">📍 打卡解锁</button>
  </div>
</div>

<!-- 休息节点（酒店） -->
<div class="node node--rest">
  <div class="node-dot"></div>
  <div class="node-card">
    <div class="node-header">
      <span class="node-icon">🔥</span>
      <span class="node-name">[酒店名]</span>
      <span class="node-badge" style="color:var(--gold)">存档点</span>
    </div>
    <div class="node-time">[入住日期] · [地址]</div>

    <!-- 剧情概要 + 台词 -->
    <div class="node-plot">
      <div class="node-plot-title">📖 剧情概要</div>
      <div class="node-plot-summary">[剧情概要：描述游戏中与此存档点/休息地相关的关键剧情]</div>
      <div class="node-dialogue">
        <div class="node-dialogue-speaker">🗣️ [角色名]</div>
        <div class="node-dialogue-text">"[与此地相关的游戏台词或经典对白]"</div>
      </div>
      <div class="node-related-locations">
        <span class="node-related-loc">📍 [关联地点1]</span>
      </div>
    </div>

    <div class="node-desc">
      <div class="desc-game">
        <div class="desc-label">💤 HP 回复</div>
        8小时深度睡眠
      </div>
      <div class="desc-reality">
        <div class="desc-label">☕ MP 回复</div>
        [早餐信息] + WiFi
      </div>
    </div>
    <div class="buy-card">
      <div class="buy-info">
        <div class="buy-name">[酒店名] · [星级/评分]</div>
        <div class="buy-reason">💡 [推荐理由]</div>
      </div>
      <div class="buy-price">¥[价格]<small>/晚</small></div>
      <div class="buy-actions">
        <a href="[飞猪链接]" target="_blank" rel="noopener" class="buy-btn">🛒 飞猪购买</a>
        <button class="copy-btn" onclick="copyLink('[飞猪链接]', this)">📋 复制</button>
      </div>
    </div>
  </div>
</div>

<!-- 商店节点（美食/体验） -->
<div class="node node--shop">
  <div class="node-dot"></div>
  <div class="node-card">
    <div class="node-header">
      <span class="node-icon">🛒</span>
      <span class="node-name">[美食/体验名]</span>
      <span class="node-badge" style="color:var(--purple)">回血道具</span>
    </div>
    <div class="node-time">[时间] · [地址]</div>

    <!-- 剧情概要 + 台词 -->
    <div class="node-plot">
      <div class="node-plot-title">📖 剧情概要</div>
      <div class="node-plot-summary">[剧情概要：描述游戏中与此食物/道具相关的关键剧情或角色互动]</div>
      <div class="node-dialogue">
        <div class="node-dialogue-speaker">🗣️ [角色名]</div>
        <div class="node-dialogue-text">"[与此食物/道具相关的游戏台词]"</div>
      </div>
      <div class="node-related-locations">
        <span class="node-related-loc">📍 [关联地点1]</span>
      </div>
    </div>

    <div class="node-desc">
      <div class="desc-game">
        <div class="desc-label">🎮 Buff 效果</div>
        [Buff效果]
      </div>
      <div class="desc-reality">
        <div class="desc-label">🌍 现实</div>
        [现实描述] · ⭐ [评分]
      </div>
    </div>
    <div class="buy-card">
      <div class="buy-info">
        <div class="buy-name">[美食/体验名]</div>
        <div class="buy-reason">💡 [推荐理由]</div>
      </div>
      <div class="buy-price">¥[价格]<small>/人</small></div>
      <div class="buy-actions">
        <a href="[飞猪链接]" target="_blank" rel="noopener" class="buy-btn">🛒 飞猪购买</a>
        <button class="copy-btn" onclick="copyLink('[飞猪链接]', this)">📋 复制</button>
      </div>
    </div>
  </div>
</div>
```
