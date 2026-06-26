# Design System — Wesley Dashboard

## Philosophie visuelle

**Bloomberg Terminal meets Trading Journal Public.**
Sombre, dense, professionnel. Quelqu'un qui reçoit le lien comprend en 3 secondes que c'est sérieux.
Les chiffres bougent. Les dots clignotent. On voit Wesley qui travaille EN DIRECT.

---

## Variables CSS — copier dans chaque `<style>`

```css
:root {
  /* Backgrounds */
  --bg: #020608;
  --surface: #080e12;
  --surface2: #0d1820;
  --border: #0f2233;

  /* Couleurs fonctionnelles */
  --accent: #00d4ff;       /* Bleu cyan — info, titres */
  --accent2: #00ff88;      /* Vert — profits, wins, actif */
  --danger: #ff3b5c;       /* Rouge — pertes, alerts */
  --gold: #f5a623;         /* Or — signaux, highlights */
  --purple: #9b59b6;       /* Violet — VIP badge */

  /* Texte */
  --text: #e0f0ff;
  --muted: #4a7a9b;
  --subtle: #1e3a4a;

  /* Typographie */
  --mono: 'Space Mono', monospace;   /* chiffres, code, labels */
  --sans: 'Syne', sans-serif;        /* titres, valeurs importantes */
}
```

## Import Google Fonts (dans `<head>`)

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap" rel="stylesheet">
```

---

## Effets globaux body

```css
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--mono);
  min-height: 100vh;
  overflow-x: hidden;
}

/* Scanlines — effet terminal */
body::before {
  content: '';
  position: fixed; inset: 0;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 2px,
    rgba(0,212,255,0.012) 2px, rgba(0,212,255,0.012) 4px
  );
  pointer-events: none; z-index: 1000;
}

/* Grille de fond */
body::after {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(0,212,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,0.025) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none; z-index: 0;
}

/* Tout le contenu au-dessus des effets */
.container, nav, header { position: relative; z-index: 1; }
```

---

## Navigation

### Desktop (sidebar gauche)
```html
<nav class="sidebar">
  <div class="logo">WES<span>LEY</span></div>
  <a href="index.html" class="nav-item active">🏠 Home</a>
  <a href="trading.html" class="nav-item">📊 Trading</a>
  <a href="signals.html" class="nav-item">📡 Signaux</a>
  <a href="journal.html" class="nav-item">📸 Journal</a>
</nav>
```

### Mobile (barre bottom)
```html
<nav class="bottom-nav">
  <a href="index.html" class="bn-item active">🏠<span>Home</span></a>
  <a href="trading.html" class="bn-item">📊<span>Trading</span></a>
  <a href="signals.html" class="bn-item">📡<span>Signaux</span></a>
  <a href="journal.html" class="bn-item">📸<span>Journal</span></a>
</nav>
```

```css
/* Bottom nav mobile */
.bottom-nav {
  display: none;
  position: fixed; bottom: 0; left: 0; right: 0;
  background: rgba(8,14,18,0.98);
  border-top: 1px solid var(--border);
  z-index: 200;
  backdrop-filter: blur(10px);
}

@media (max-width: 768px) {
  .sidebar { display: none; }
  .bottom-nav {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
  }
  .bn-item {
    display: flex; flex-direction: column;
    align-items: center; gap: 3px;
    padding: 10px 0;
    font-size: 9px; letter-spacing: 0.5px;
    color: var(--muted); text-decoration: none;
  }
  .bn-item.active { color: var(--accent); }
  .bn-item span { font-size: 18px; }
}
```

---

## Composants

### Stat Card (chiffre hero)
```html
<div class="stat-card" style="--bar-color: var(--accent2)">
  <div class="stat-label">PORTFOLIO VALUE</div>
  <div class="stat-value" id="stat-portfolio">$1,247.83</div>
  <div class="stat-delta delta-up">↑ 2.82%</div>
</div>
```
```css
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 24px;
  position: relative;
  overflow: hidden;
}
.stat-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0;
  height: 2px;
  background: var(--bar-color, var(--accent));
}
.stat-label {
  font-size: 9px; letter-spacing: 2.5px;
  color: var(--muted); text-transform: uppercase;
  margin-bottom: 12px;
}
.stat-value {
  font-family: var(--sans); font-size: 36px;
  font-weight: 800; line-height: 1; margin-bottom: 8px;
}
.stat-delta { font-size: 11px; }
.delta-up { color: var(--accent2); }
.delta-dn { color: var(--danger); }
```

### Panel (conteneur)
```html
<div class="panel">
  <div class="panel-header">
    <span class="panel-title">TITRE</span>
    <span class="panel-badge">LIVE</span>
  </div>
  <!-- contenu -->
</div>
```
```css
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  overflow: hidden;
}
.panel-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border);
}
.panel-title {
  font-size: 9px; letter-spacing: 2.5px;
  color: var(--muted); text-transform: uppercase;
}
.panel-badge {
  font-size: 9px; padding: 3px 8px;
  background: rgba(0,212,255,0.1);
  border: 1px solid rgba(0,212,255,0.15);
  color: var(--accent); letter-spacing: 1px;
}
```

### Pulse dot (agent actif)
```html
<div class="agent-dot dot-active"></div>
```
```css
.agent-dot { width: 8px; height: 8px; border-radius: 50%; }
.dot-active { background: var(--accent2); animation: pulse 2s infinite; }
.dot-idle   { background: var(--muted); }
.dot-pending{ background: var(--gold); }

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.4; transform: scale(0.85); }
}
```

### Signal item (feed)
```html
<div class="signal-item">
  <div class="signal-icon type-long">🟢</div>
  <div class="signal-body">
    <div class="signal-asset">BTC/USDT</div>
    <div class="signal-detail">OBI divergence + VWAP breakout | Entry: $84,200</div>
  </div>
  <div class="signal-meta">
    <span class="signal-edge">8.4</span>
    <span class="badge-vip">VIP</span>
    <span class="signal-time">06:14</span>
  </div>
</div>
```
```css
.signal-item {
  display: grid; grid-template-columns: 40px 1fr auto;
  gap: 14px; align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid rgba(15,34,51,0.8);
  animation: slideIn 0.4s ease;
}
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-8px); }
  to   { opacity: 1; transform: translateX(0); }
}
.signal-icon { width: 36px; height: 36px; border-radius: 4px;
  display: flex; align-items: center; justify-content: center; font-size: 16px; }
.type-long  { background: rgba(0,255,136,0.1); border: 1px solid rgba(0,255,136,0.2); }
.type-short { background: rgba(255,59,92,0.1); border: 1px solid rgba(255,59,92,0.2); }
.type-alert { background: rgba(245,166,35,0.1); border: 1px solid rgba(245,166,35,0.2); }
.signal-asset { font-weight: 700; font-size: 13px; margin-bottom: 3px; }
.signal-detail { font-size: 11px; color: var(--muted); line-height: 1.4; }
.signal-edge {
  font-family: var(--sans); font-weight: 800;
  font-size: 20px; color: var(--accent2); display: block; text-align: right;
}
.badge-vip {
  font-size: 9px; padding: 2px 6px;
  background: rgba(155,89,182,0.2); border: 1px solid rgba(155,89,182,0.3);
  color: #c39bd3; letter-spacing: 1px;
}
.badge-free {
  font-size: 9px; padding: 2px 6px;
  background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.2);
  color: var(--accent); letter-spacing: 1px;
}
.signal-time { font-size: 10px; color: var(--muted); }
```

### CTA VIP Sticky
```html
<div class="cta-vip">
  <div class="cta-text">
    <div class="cta-title">Accède aux signaux VIP</div>
    <div class="cta-sub">4 signaux/jour • Edge moyen 7.8 • 29€/mois USDC</div>
  </div>
  <a href="https://TON-LIEN-LANDING-PAGE" class="cta-btn">Rejoindre →</a>
</div>
```
```css
.cta-vip {
  position: sticky; bottom: 60px; /* au-dessus de la bottom nav */
  margin: 16px;
  background: linear-gradient(135deg, rgba(155,89,182,0.2), rgba(0,212,255,0.1));
  border: 1px solid rgba(155,89,182,0.3);
  padding: 16px 20px;
  display: flex; justify-content: space-between; align-items: center;
  gap: 12px;
  backdrop-filter: blur(10px);
}
.cta-title { font-weight: 700; font-size: 13px; margin-bottom: 4px; }
.cta-sub { font-size: 10px; color: var(--muted); }
.cta-btn {
  background: var(--purple); color: white;
  padding: 10px 18px; font-size: 12px; font-weight: 700;
  border: none; cursor: pointer; letter-spacing: 0.5px;
  white-space: nowrap; text-decoration: none;
  transition: opacity 0.2s;
}
.cta-btn:hover { opacity: 0.85; }
```

### Barre de progression (objectif mensuel)
```html
<div class="progress-block">
  <div class="progress-header">
    <span>Objectif mars 2026</span>
    <span id="progress-label">$247 / $1,000</span>
  </div>
  <div class="progress-track">
    <div class="progress-fill" id="progress-bar" style="width: 24.7%"></div>
  </div>
  <div class="progress-sub">24.7% — encore $753 pour atteindre 1,000€/mois 🎯</div>
</div>
```
```css
.progress-block { padding: 16px 20px; }
.progress-header {
  display: flex; justify-content: space-between;
  font-size: 11px; color: var(--muted); margin-bottom: 10px;
}
.progress-track {
  height: 6px; background: var(--border);
  border-radius: 3px; overflow: hidden; margin-bottom: 8px;
}
.progress-fill {
  height: 100%; border-radius: 3px;
  background: linear-gradient(90deg, var(--accent2), var(--accent));
  transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.progress-sub { font-size: 10px; color: var(--muted); }
```

### Bouton screenshot (partage viral)
```html
<button class="share-btn" onclick="captureScreenshot()">
  📱 Capturer pour Instagram/X
</button>
```
```javascript
async function captureScreenshot() {
  // Utilise html2canvas CDN
  const canvas = await html2canvas(document.body, {
    backgroundColor: '#020608',
    scale: 2,
    useCORS: true
  });
  const link = document.createElement('a');
  link.download = `wesley-${new Date().toISOString().slice(0,10)}.png`;
  link.href = canvas.toDataURL('image/png');
  link.click();
}
// CDN à ajouter : <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
```

---

## Chart.js — Courbe equity

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<canvas id="equityChart" height="120"></canvas>
```
```javascript
function drawEquityChart(data) {
  const ctx = document.getElementById('equityChart').getContext('2d');
  const grad = ctx.createLinearGradient(0, 0, 0, 200);
  grad.addColorStop(0, 'rgba(0,212,255,0.3)');
  grad.addColorStop(1, 'rgba(0,212,255,0)');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map((_, i) => `J-${data.length - 1 - i}`),
      datasets: [{
        data: data,
        borderColor: '#00d4ff',
        backgroundColor: grad,
        borderWidth: 2,
        pointRadius: 4,
        pointBackgroundColor: '#00d4ff',
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: 'rgba(15,34,51,0.5)' }, ticks: { color: '#4a7a9b', font: { size: 10 } } },
        y: { grid: { color: 'rgba(15,34,51,0.5)' }, ticks: { color: '#4a7a9b', font: { size: 10 },
          callback: v => `$${v.toLocaleString()}` } }
      }
    }
  });
}
```

### Donut win rate
```javascript
function drawWinRate(rate) {
  const ctx = document.getElementById('winrateChart').getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      datasets: [{
        data: [rate, 100 - rate],
        backgroundColor: ['#00ff88', '#0f2233'],
        borderWidth: 0
      }]
    },
    options: {
      cutout: '75%',
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false }
      }
    }
  });
  // Label central
  const label = document.getElementById('winrate-label');
  if (label) label.textContent = `${rate.toFixed(1)}%`;
}
```

---

## Animations utiles

```css
/* Slide in depuis la gauche */
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-12px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* Compteur qui flash quand il se met à jour */
@keyframes countFlash {
  0%   { color: var(--accent); }
  100% { color: inherit; }
}
.updating { animation: countFlash 0.4s ease; }

/* Entrée staggerée pour les listes */
.list-item:nth-child(1) { animation-delay: 0.05s; }
.list-item:nth-child(2) { animation-delay: 0.10s; }
.list-item:nth-child(3) { animation-delay: 0.15s; }
.list-item:nth-child(4) { animation-delay: 0.20s; }
```

---

## Meta tags OG (à mettre dans chaque `<head>`)

```html
<meta property="og:title" content="Wesley Capital — Live Trading Dashboard">
<meta property="og:description" content="Agent IA qui trade en temps réel. +24% en 12 jours.">
<meta property="og:image" content="https://TON-TUNNEL.trycloudflare.com/assets/og-image.png">
<meta property="og:url" content="https://TON-TUNNEL.trycloudflare.com">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Wesley Capital — IA Trading Live">
<meta name="twitter:description" content="Signaux crypto & Polymarket en temps réel. Rejoins le VIP.">
```

---

## Responsive — règles de base

```css
/* Layout desktop : sidebar + contenu */
@media (min-width: 769px) {
  .app { display: grid; grid-template-columns: 200px 1fr; min-height: 100vh; }
  .sidebar { background: var(--surface); border-right: 1px solid var(--border); padding: 24px 0; }
  .main { padding: 24px; }
}

/* Layout mobile : bottom nav + scroll vertical */
@media (max-width: 768px) {
  .app { display: block; }
  .main { padding: 12px 12px 80px; } /* 80px = espace bottom nav */
  .hero { grid-template-columns: 1fr 1fr; gap: 8px; }
  .stat-value { font-size: 26px; }
}
```
