#!/usr/bin/env node
/**
 * Research Report HTML Generator
 *
 * Accepts a structured JSON research context and generates
 * a self-contained interactive HTML report.
 *
 * Usage:
 *   node generate-report.js < research-data.json > report.html
 *   node generate-report.js --input data.json --output report.html
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// --- CLI argument parsing ---
function parseArgs() {
  const args = process.argv.slice(2);
  let input = null, output = null;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--input' || args[i] === '-i') input = args[++i];
    if (args[i] === '--output' || args[i] === '-o') output = args[++i];
  }
  return { input, output };
}

// --- Escape HTML ---
function esc(str) {
  if (!str) return '';
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// --- Tool badge class ---
function toolClass(tool) {
  const map = {
    web_search: 'search', search: 'search',
    api_call: 'api', api: 'api',
    browse: 'browse', web_browse: 'browse',
    analyze: 'analyze', analysis: 'analyze', synthesis: 'analyze',
  };
  return map[(tool || '').toLowerCase().replace(/\s+/g, '_')] || 'search';
}

// --- Tool emoji ---
function toolEmoji(tool) {
  const map = {
    web_search: '🔍', search: '🔍',
    api_call: '⚡', api: '⚡',
    browse: '🌐', web_browse: '🌐',
    analyze: '🧠', analysis: '🧠',
    synthesis: '✅',
  };
  return map[(tool || '').toLowerCase().replace(/\s+/g, '_')] || '🔧';
}

// --- Sentiment class ---
function sentimentClass(sentiment) {
  if (!sentiment) return 'neutral';
  const s = sentiment.toLowerCase();
  if (s === 'positive' || s === 'bullish' || s === 'up') return 'positive';
  if (s === 'negative' || s === 'bearish' || s === 'down') return 'negative';
  return 'neutral';
}
function sentimentEmoji(sentiment) {
  const map = { positive: '📈', negative: '📉', neutral: '📰', bullish: '📈', bearish: '📉', up: '📈', down: '📉', warning: '⚠️' };
  return map[(sentiment || '').toLowerCase()] || '📰';
}

// --- Render research steps timeline ---
function renderTimeline(steps) {
  if (!steps || !steps.length) return '';
  return steps.map((step, i) => {
    const sourcesHtml = (step.sources || []).map(src =>
      `<a class="source-item" href="${esc(src.url || '#')}" target="_blank" rel="noopener">
        <span class="source-icon">${esc(src.icon || '📄')}</span> ${esc(src.title || src.url || 'Source')}
      </a>`
    ).join('\n');

    const detailsBlock = sourcesHtml ? `
      <div class="step-details">
        <div class="step-sources">
          <div class="src-label">Sources</div>
          ${sourcesHtml}
        </div>
      </div>` : '';

    return `
      <div class="step active" onclick="toggleDetails(this)">
        <div class="step-dot"><div class="inner"></div></div>
        <div class="step-card">
          <div class="step-header">
            <span class="step-tool ${toolClass(step.tool)}">${toolEmoji(step.tool)} ${esc(step.tool_label || step.tool || 'Step')}</span>
            <span class="step-time">${esc(step.time_range || '')}</span>
          </div>
          ${step.query ? `<div class="step-query">${esc(step.query)}</div>` : ''}
          <div class="step-summary">${esc(step.summary)}</div>
          ${detailsBlock}
        </div>
      </div>`;
  }).join('\n');
}

// --- Render line chart SVG ---
function renderLineChart(chartData) {
  if (!chartData || !chartData.series || !chartData.series.length) return '';

  const colors = ['#00d2a0', '#6c5ce7', '#ff9f43', '#4da6ff', '#ff6b6b'];
  const gradients = ['greenGrad', 'purpleGrad', 'orangeGrad', 'blueGrad', 'redGrad'];
  const W = 800, H = 300, PAD_L = 55, PAD_R = 20, PAD_T = 30, PAD_B = 30;
  const plotW = W - PAD_L - PAD_R;
  const plotH = H - PAD_T - PAD_B;

  const allVals = chartData.series.flatMap(s => s.values);
  const minV = chartData.y_min != null ? chartData.y_min : Math.floor(Math.min(...allVals) / 5) * 5;
  const maxV = chartData.y_max != null ? chartData.y_max : Math.ceil(Math.max(...allVals) / 5) * 5;
  const range = maxV - minV || 1;

  function toY(v) { return PAD_T + plotH - ((v - minV) / range) * plotH; }
  function toX(i, len) { return PAD_L + (i / (len - 1)) * plotW; }

  // Grid lines
  const gridSteps = 5;
  let gridHtml = '';
  for (let i = 0; i <= gridSteps; i++) {
    const v = minV + (range / gridSteps) * i;
    const y = toY(v);
    gridHtml += `<line x1="${PAD_L}" y1="${y}" x2="${W - PAD_R}" y2="${y}" stroke="#1e1e2e" stroke-width="1"/>`;
    gridHtml += `<text x="${PAD_L - 8}" y="${y + 4}" fill="#555568" font-size="11" text-anchor="end">${chartData.y_format === 'percent' ? Math.round(v) + '%' : Math.round(v)}</text>`;
  }

  // X labels
  const labels = chartData.x_labels || [];
  let xLabelHtml = '';
  labels.forEach((label, i) => {
    const x = PAD_L + (i / (labels.length - 1)) * plotW;
    xLabelHtml += `<text x="${x}" y="${H - 5}" fill="#555568" font-size="11" text-anchor="middle">${esc(label)}</text>`;
  });

  // Gradient defs
  let defsHtml = chartData.series.map((s, si) => {
    const c = colors[si % colors.length];
    return `<linearGradient id="${gradients[si]}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="${c}" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="${c}" stop-opacity="0"/>
    </linearGradient>`;
  }).join('\n');

  // Series
  let seriesHtml = '';
  chartData.series.forEach((s, si) => {
    const c = colors[si % colors.length];
    const pts = s.values.map((v, i) => `${toX(i, s.values.length)},${toY(v)}`).join(' ');

    // Area fill (only for first 2 series)
    if (si < 2) {
      const lastX = toX(s.values.length - 1, s.values.length);
      const firstX = toX(0, s.values.length);
      seriesHtml += `<path d="M${pts.split(' ').join(' L')} L${lastX},${PAD_T + plotH} L${firstX},${PAD_T + plotH} Z"
        fill="url(#${gradients[si]})" opacity="0.5"/>`.replace(/M(\d)/,'M$1');
    }

    // Line
    const dash = si >= 2 ? ' stroke-dasharray="6,4"' : '';
    seriesHtml += `<polyline points="${pts}" fill="none" stroke="${c}" stroke-width="2.5"
      stroke-linecap="round" stroke-linejoin="round"${dash}/>`;

    // End dot + label
    const lastVal = s.values[s.values.length - 1];
    const lastPt = { x: toX(s.values.length - 1, s.values.length), y: toY(lastVal) };
    seriesHtml += `<circle cx="${lastPt.x}" cy="${lastPt.y}" r="5" fill="${c}" opacity="0.9"/>`;
    const labelText = chartData.y_format === 'percent' ? Math.round(lastVal) + '%' : lastVal;
    seriesHtml += `<text x="${lastPt.x - 20}" y="${lastPt.y - 10}" fill="${c}" font-size="12" font-weight="600">${labelText}</text>`;
  });

  // Legend
  const legendHtml = chartData.series.map((s, si) =>
    `<span><span class="legend-dot" style="background:${colors[si % colors.length]}"></span> ${esc(s.name)}</span>`
  ).join('\n');

  return `
    <div class="chart-container">
      <div class="chart-header">
        <div class="chart-title">${esc(chartData.title || 'Trend Chart')}</div>
        <div class="chart-legend">${legendHtml}</div>
      </div>
      <svg class="chart-svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMid meet">
        <defs>${defsHtml}</defs>
        ${gridHtml}
        ${xLabelHtml}
        ${seriesHtml}
      </svg>
    </div>`;
}

// --- Render market cards ---
function renderMarketCards(markets) {
  if (!markets || !markets.length) return '';
  return `<div class="market-grid">
    ${markets.map(m => {
      const changeClass = (m.change_7d || 0) >= 0 ? 'up' : 'down';
      const changeArrow = (m.change_7d || 0) >= 0 ? '↑' : '↓';
      return `
      <div class="market-card">
        <div class="market-name">${esc(m.name)}</div>
        <div class="market-odds">
          <div><div class="odds-tag yes">${m.yes_price}¢</div><div class="odds-label">YES</div></div>
          <div><div class="odds-tag no">${m.no_price}¢</div><div class="odds-label">NO</div></div>
        </div>
        <div class="market-volume">
          Vol: $${esc(m.volume || '0')} &nbsp;·&nbsp;
          <span class="market-change ${changeClass}">${changeArrow} ${m.change_7d >= 0 ? '+' : ''}${m.change_7d}% 7d</span>
        </div>
      </div>`;
    }).join('\n')}
  </div>`;
}

// --- Render world map ---
function renderWorldMap(mapData) {
  if (!mapData || !mapData.regions || !mapData.regions.length) return '';

  // Simplified continent paths
  const continentPaths = {
    'north_america': 'M150,80 L280,60 L300,100 L310,160 L290,200 L250,220 L200,200 L160,170 L130,130 Z',
    'united_states': 'M150,80 L280,60 L300,100 L310,160 L290,200 L250,220 L200,200 L160,170 L130,130 Z',
    'canada': 'M150,30 L280,20 L300,60 L280,60 L150,80 L120,60 Z',
    'mexico': 'M160,220 L250,220 L240,270 L200,290 L160,260 Z',
    'south_america': 'M230,300 L290,280 L310,330 L300,400 L270,440 L240,420 L220,370 Z',
    'europe': 'M430,70 L530,50 L560,80 L550,130 L520,150 L470,140 L440,110 Z',
    'africa': 'M440,170 L530,160 L560,200 L550,320 L500,370 L450,340 L430,260 Z',
    'russia': 'M560,40 L780,30 L820,80 L800,120 L700,130 L600,120 L560,80 Z',
    'middle_east': 'M560,130 L630,120 L650,160 L620,190 L570,180 Z',
    'east_asia': 'M700,100 L800,90 L830,130 L810,180 L760,190 L720,170 L700,140 Z',
    'china': 'M700,100 L800,90 L830,130 L810,180 L760,190 L720,170 L700,140 Z',
    'southeast_asia': 'M740,200 L810,190 L840,230 L820,270 L770,260 L740,230 Z',
    'australia': 'M800,330 L880,310 L920,350 L900,400 L840,400 L800,370 Z',
  };

  const highlightedIds = new Set(mapData.regions.map(r => r.id.toLowerCase()));
  const regionInfoMap = {};
  mapData.regions.forEach(r => { regionInfoMap[r.id.toLowerCase()] = r; });

  let pathsHtml = '';
  for (const [id, d] of Object.entries(continentPaths)) {
    const isHighlight = highlightedIds.has(id);
    const region = regionInfoMap[id];
    const cls = isHighlight ? ' class="highlight"' : '';
    const dataAttrs = isHighlight && region
      ? ` data-region="${esc(region.name)}" data-info="${esc(region.info)}" onmouseenter="showTooltip(event, this)" onmouseleave="hideTooltip()"`
      : ` data-region="${esc(id)}"`;
    pathsHtml += `<path${cls} d="${d}"${dataAttrs}/>\n`;
  }

  return `
    <div class="map-container">
      <div class="map-tooltip" id="mapTooltip"></div>
      <svg class="map-svg" viewBox="0 0 1000 500" preserveAspectRatio="xMidYMid meet">
        ${pathsHtml}
      </svg>
      <div class="map-legend">
        <div class="map-legend-item"><div class="map-legend-dot" style="background:rgba(108,92,231,0.5)"></div> High impact region</div>
        <div class="map-legend-item"><div class="map-legend-dot" style="background:#1a1a2e"></div> Low / indirect impact</div>
      </div>
    </div>`;
}

// --- Render news cards ---
function renderNewsCards(news) {
  if (!news || !news.length) return '';
  return `<div class="news-list">
    ${news.map(n => `
      <a class="news-item" href="${esc(n.url || '#')}" target="_blank" rel="noopener">
        <div class="news-sentiment ${sentimentClass(n.sentiment)}">${sentimentEmoji(n.sentiment)}</div>
        <div class="news-body">
          <div class="news-title">${esc(n.title)}</div>
          <div class="news-meta">
            <span>${esc(n.source || '')}</span>
            <span>${esc(n.date || '')}</span>
          </div>
          ${n.tag ? `<span class="news-tag">${esc(n.tag)}</span>` : ''}
        </div>
      </a>`
    ).join('\n')}
  </div>`;
}

// --- Render bar chart SVG ---
function renderBarChart(chartData) {
  if (!chartData || !chartData.bars || !chartData.bars.length) return '';
  const bars = chartData.bars;
  const maxVal = Math.max(...bars.map(b => b.value));
  const defaultColors = ['#00d2a0','#6c5ce7','#ff9f43','#4da6ff','#ff6b6b','#ffd93d'];

  const barsHtml = bars.map((b, i) => {
    const pct = maxVal > 0 ? (b.value / maxVal) * 100 : 0;
    const color = b.color || defaultColors[i % defaultColors.length];
    return `<div class="bar-row">
      <div class="bar-label">${esc(b.label)}</div>
      <div class="bar-track"><div class="bar-fill" style="width:${pct}%;background:${color}">${esc(String(b.value))}</div></div>
    </div>`;
  }).join('\n');

  return `<div class="chart-container">
    <div class="chart-title">${esc(chartData.title || 'Comparison')}</div>
    <div class="bar-chart">${barsHtml}</div>
  </div>`;
}

// --- Render stat cards ---
function renderStatCards(stats) {
  if (!stats || !stats.length) return '';
  return `<div class="stat-grid">
    ${stats.map(s => {
      const trendClass = (s.trend || '').toLowerCase() === 'up' ? 'up' : (s.trend || '').toLowerCase() === 'down' ? 'down' : 'neutral';
      return `<div class="stat-card">
        <div class="stat-icon">${esc(s.icon || '📊')}</div>
        <div class="stat-value">${esc(s.value)}</div>
        <div class="stat-label">${esc(s.label)}</div>
        ${s.change ? `<div class="stat-change ${trendClass}">${esc(s.change)}</div>` : ''}
      </div>`;
    }).join('\n')}
  </div>`;
}

// --- Render comparison table ---
function renderComparisonTable(tableData) {
  if (!tableData || !tableData.headers || !tableData.rows) return '';
  const hl = tableData.highlight_col;
  const headHtml = tableData.headers.map((h, i) =>
    `<th${i === hl ? ' class="highlight"' : ''}>${esc(h)}</th>`
  ).join('');
  const rowsHtml = tableData.rows.map(row =>
    `<tr>${row.map((c, i) => `<td${i === hl ? ' class="highlight"' : ''}>${esc(c)}</td>`).join('')}</tr>`
  ).join('\n');
  return `<div class="table-wrap"><table class="comp-table"><thead><tr>${headHtml}</tr></thead><tbody>${rowsHtml}</tbody></table></div>`;
}

// --- Render quote blocks ---
function renderQuoteBlock(quotes) {
  if (!quotes || !quotes.length) return '';
  return `<div class="quotes-list">
    ${quotes.map(q => `<blockquote class="quote-card">
      <div class="quote-text">"${esc(q.text)}"</div>
      <div class="quote-author">— ${esc(q.author)}${q.role ? `, <span class="quote-role">${esc(q.role)}</span>` : ''}</div>
    </blockquote>`).join('\n')}
  </div>`;
}

// --- Render key points ---
function renderKeyPoints(points) {
  if (!points || !points.length) return '';
  return `<div class="key-points">
    ${points.map(p => `<div class="kp-item">
      <span class="kp-icon">${esc(p.icon || '•')}</span>
      <div><div class="kp-title">${esc(p.title)}</div><div class="kp-text">${esc(p.text)}</div></div>
    </div>`).join('\n')}
  </div>`;
}

// --- Render visualizations by type ---
function renderVisualization(viz) {
  switch (viz.type) {
    case 'line_chart': return renderLineChart(viz.data);
    case 'bar_chart': return renderBarChart(viz.data);
    case 'market_cards': return renderMarketCards(viz.data);
    case 'world_map': return renderWorldMap(viz.data);
    case 'news_cards': return renderNewsCards(viz.data);
    case 'stat_cards': return renderStatCards(viz.data);
    case 'comparison_table': return renderComparisonTable(viz.data);
    case 'quote_block': return renderQuoteBlock(viz.data);
    case 'key_points': return renderKeyPoints(viz.data);
    default: return `<!-- Unknown visualization type: ${esc(viz.type)} -->`;
  }
}

// --- Main HTML template ---
function generateHTML(data) {
  const id = crypto.randomBytes(6).toString('hex');
  const totalSteps = (data.steps || []).length;
  const totalSources = (data.steps || []).reduce((n, s) => n + (s.sources || []).length, 0);

  // Render each visualization section
  const vizSections = (data.visualizations || []).map(viz => `
    <div class="section fade-in">
      ${viz.section_title ? `<div class="section-title">${esc(viz.section_title)}</div>` : ''}
      ${renderVisualization(viz)}
    </div>`
  ).join('\n');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Research Report — ${esc(data.title)}</title>
<meta property="og:title" content="${esc(data.title)}">
<meta property="og:description" content="AI Research Report — ${totalSteps} steps, ${totalSources} sources analyzed">
<meta name="twitter:card" content="summary">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0a0a0f; --bg-card: #12121a; --bg-card-hover: #1a1a25;
  --border: #1e1e2e; --text: #e0e0e8; --text-dim: #8888a0; --text-muted: #555568;
  --accent: #6c5ce7; --accent-glow: rgba(108,92,231,0.3);
  --green: #00d2a0; --green-dim: rgba(0,210,160,0.15);
  --red: #ff6b6b; --red-dim: rgba(255,107,107,0.15);
  --blue: #4da6ff; --yellow: #ffd93d; --orange: #ff9f43;
  --radius: 12px; --radius-sm: 8px;
}
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; min-height: 100vh; }
.container { max-width: 900px; margin: 0 auto; padding: 20px 16px 60px; }

.header { text-align: center; padding: 40px 0 30px; }
.header-badge { display: inline-flex; align-items: center; gap: 6px; background: var(--accent-glow); border: 1px solid rgba(108,92,231,0.4); border-radius: 20px; padding: 4px 14px; font-size: 12px; color: var(--accent); margin-bottom: 16px; letter-spacing: 0.5px; }
.header-badge .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1}50%{opacity:0.4} }
.header h1 { font-size: clamp(22px,5vw,32px); font-weight: 700; margin-bottom: 8px; background: linear-gradient(135deg,#fff,#a0a0c0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.header .subtitle { color: var(--text-dim); font-size: 14px; }
.header .meta { display: flex; justify-content: center; gap: 20px; margin-top: 16px; font-size: 12px; color: var(--text-muted); }
.header .meta span { display: flex; align-items: center; gap: 4px; }

.conclusion-card { background: linear-gradient(135deg,rgba(108,92,231,0.12),rgba(0,210,160,0.08)); border: 1px solid rgba(108,92,231,0.3); border-radius: var(--radius); padding: 24px; margin-bottom: 32px; position: relative; overflow: hidden; }
.conclusion-card::before { content: ''; position: absolute; top:0; left:0; right:0; height:2px; background: linear-gradient(90deg,var(--accent),var(--green)); }
.conclusion-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--accent); margin-bottom: 10px; }
.conclusion-text { font-size: 18px; font-weight: 600; line-height: 1.5; margin-bottom: 16px; }
.confidence-bar { display: flex; align-items: center; gap: 12px; }
.confidence-bar .label { font-size: 12px; color: var(--text-dim); white-space: nowrap; }
.confidence-track { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.confidence-fill { height: 100%; border-radius: 3px; background: linear-gradient(90deg,var(--accent),var(--green)); transition: width 1.5s ease; }
.confidence-val { font-size: 14px; font-weight: 600; color: var(--green); }

.section { margin-bottom: 32px; }
.section-title { font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted); margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.section-title::after { content: ''; flex: 1; height: 1px; background: var(--border); }

.timeline { position: relative; }
.timeline::before { content: ''; position: absolute; left: 18px; top: 0; bottom: 0; width: 2px; background: linear-gradient(180deg,var(--accent),var(--border)); }
.step { position: relative; padding-left: 48px; padding-bottom: 24px; cursor: pointer; }
.step:last-child { padding-bottom: 0; }
.step-dot { position: absolute; left: 10px; top: 4px; width: 18px; height: 18px; border-radius: 50%; background: var(--bg); border: 2px solid var(--accent); display: flex; align-items: center; justify-content: center; z-index: 1; transition: all 0.3s; }
.step-dot .inner { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); transition: all 0.3s; }
.step.active .step-dot { border-color: var(--green); box-shadow: 0 0 12px var(--green-dim); }
.step.active .step-dot .inner { background: var(--green); }
.step-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; transition: all 0.3s; }
.step:hover .step-card { background: var(--bg-card-hover); border-color: rgba(108,92,231,0.3); }
.step-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.step-tool { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; padding: 3px 10px; border-radius: 12px; font-weight: 600; }
.step-tool.search { background: rgba(77,166,255,0.12); color: var(--blue); }
.step-tool.api { background: rgba(0,210,160,0.12); color: var(--green); }
.step-tool.analyze { background: rgba(108,92,231,0.12); color: var(--accent); }
.step-tool.browse { background: rgba(255,159,67,0.12); color: var(--orange); }
.step-time { font-size: 11px; color: var(--text-muted); }
.step-query { font-size: 13px; color: var(--text-dim); margin-bottom: 6px; font-style: italic; }
.step-summary { font-size: 14px; line-height: 1.6; }
.step-details { max-height: 0; overflow: hidden; transition: max-height 0.4s ease, margin 0.3s ease; }
.step-details.open { max-height: 500px; margin-top: 12px; }
.step-sources { padding-top: 12px; border-top: 1px solid var(--border); }
.step-sources .src-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.source-item { display: flex; align-items: center; gap: 8px; padding: 6px 0; font-size: 13px; color: var(--blue); text-decoration: none; }
.source-item:hover { text-decoration: underline; }
.source-icon { width: 16px; height: 16px; border-radius: 4px; background: rgba(77,166,255,0.12); display: flex; align-items: center; justify-content: center; font-size: 9px; }

.chart-container { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; }
.chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 8px; }
.chart-title { font-size: 15px; font-weight: 600; }
.chart-legend { display: flex; gap: 16px; font-size: 12px; flex-wrap: wrap; }
.chart-legend span { display: flex; align-items: center; gap: 6px; }
.legend-dot { width: 8px; height: 8px; border-radius: 50%; }
.chart-svg { width: 100%; height: auto; }

.market-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(260px,1fr)); gap: 12px; }
.market-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 16px; transition: all 0.3s; }
.market-card:hover { border-color: rgba(108,92,231,0.3); transform: translateY(-2px); }
.market-name { font-size: 14px; font-weight: 600; margin-bottom: 8px; line-height: 1.4; }
.market-odds { display: flex; gap: 8px; margin-bottom: 10px; }
.odds-tag { font-size: 20px; font-weight: 700; }
.odds-tag.yes { color: var(--green); }
.odds-tag.no { color: var(--red); }
.odds-label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; }
.market-volume { font-size: 12px; color: var(--text-muted); }
.market-change { display: inline-flex; align-items: center; gap: 3px; font-size: 12px; font-weight: 600; padding: 2px 8px; border-radius: 10px; }
.market-change.up { background: var(--green-dim); color: var(--green); }
.market-change.down { background: var(--red-dim); color: var(--red); }

.map-container { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; position: relative; }
.map-svg { width: 100%; height: auto; }
.map-svg path { fill: #1a1a2e; stroke: #2a2a40; stroke-width: 0.5; transition: fill 0.3s; }
.map-svg path.highlight { fill: rgba(108,92,231,0.4); stroke: var(--accent); }
.map-svg path.highlight:hover { fill: rgba(108,92,231,0.6); }
.map-tooltip { position: absolute; background: rgba(18,18,26,0.95); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 10px 14px; font-size: 13px; pointer-events: none; opacity: 0; transition: opacity 0.2s; z-index: 10; max-width: 220px; }
.map-tooltip.visible { opacity: 1; }
.map-legend { display: flex; gap: 16px; margin-top: 12px; justify-content: center; flex-wrap: wrap; }
.map-legend-item { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-dim); }
.map-legend-dot { width: 10px; height: 10px; border-radius: 3px; }

.news-list { display: flex; flex-direction: column; gap: 10px; }
.news-item { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px 16px; display: flex; gap: 14px; align-items: flex-start; transition: all 0.3s; text-decoration: none; color: inherit; }
.news-item:hover { border-color: rgba(108,92,231,0.3); background: var(--bg-card-hover); }
.news-sentiment { flex-shrink: 0; width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.news-sentiment.positive { background: var(--green-dim); }
.news-sentiment.negative { background: var(--red-dim); }
.news-sentiment.neutral { background: rgba(255,255,255,0.06); }
.news-body { flex: 1; }
.news-title { font-size: 14px; font-weight: 600; margin-bottom: 4px; line-height: 1.4; }
.news-meta { font-size: 12px; color: var(--text-muted); display: flex; gap: 12px; }
.news-tag { display: inline-block; background: rgba(108,92,231,0.12); color: var(--accent); font-size: 11px; padding: 2px 8px; border-radius: 8px; margin-top: 6px; }

.bar-chart { display: flex; flex-direction: column; gap: 10px; }
.bar-row { display: flex; align-items: center; gap: 12px; }
.bar-label { width: 120px; font-size: 13px; text-align: right; color: var(--text-dim); flex-shrink: 0; }
.bar-track { flex: 1; height: 28px; background: rgba(255,255,255,0.04); border-radius: 6px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 6px; display: flex; align-items: center; justify-content: flex-end; padding-right: 10px; font-size: 12px; font-weight: 600; color: #fff; min-width: 40px; transition: width 1s ease; }

.stat-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(160px,1fr)); gap: 12px; }
.stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 18px 16px; text-align: center; transition: all 0.3s; }
.stat-card:hover { border-color: rgba(108,92,231,0.3); transform: translateY(-2px); }
.stat-icon { font-size: 24px; margin-bottom: 8px; }
.stat-value { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
.stat-label { font-size: 12px; color: var(--text-muted); margin-bottom: 6px; }
.stat-change { font-size: 13px; font-weight: 600; padding: 2px 8px; border-radius: 10px; display: inline-block; }
.stat-change.up { background: var(--green-dim); color: var(--green); }
.stat-change.down { background: var(--red-dim); color: var(--red); }
.stat-change.neutral { background: rgba(255,255,255,0.06); color: var(--text-dim); }

.table-wrap { overflow-x: auto; }
.comp-table { width: 100%; border-collapse: collapse; background: var(--bg-card); border-radius: var(--radius); overflow: hidden; }
.comp-table th,.comp-table td { padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); font-size: 13px; }
.comp-table th { background: rgba(108,92,231,0.08); color: var(--accent); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
.comp-table td.highlight,.comp-table th.highlight { background: rgba(0,210,160,0.08); }
.comp-table tr:last-child td { border-bottom: none; }

.quotes-list { display: flex; flex-direction: column; gap: 14px; }
.quote-card { background: var(--bg-card); border-left: 3px solid var(--accent); border-radius: 0 var(--radius) var(--radius) 0; padding: 18px 20px; margin: 0; }
.quote-text { font-size: 15px; font-style: italic; line-height: 1.6; margin-bottom: 10px; color: var(--text); }
.quote-author { font-size: 13px; color: var(--text-dim); }
.quote-role { color: var(--text-muted); }

.key-points { display: flex; flex-direction: column; gap: 12px; }
.kp-item { display: flex; gap: 14px; align-items: flex-start; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px 16px; }
.kp-icon { font-size: 20px; flex-shrink: 0; margin-top: 2px; }
.kp-title { font-size: 14px; font-weight: 600; margin-bottom: 4px; }
.kp-text { font-size: 13px; color: var(--text-dim); line-height: 1.5; }

.footer { text-align: center; padding: 32px 0 16px; font-size: 12px; color: var(--text-muted); }
.footer a { color: var(--accent); text-decoration: none; }
.footer a:hover { text-decoration: underline; }

.fade-in { opacity: 0; transform: translateY(16px); transition: opacity 0.5s ease, transform 0.5s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }

@media (max-width:768px) {
  .container { padding: 14px 12px 40px; }
  .header { padding: 20px 0 16px; }
  .header h1 { font-size: 20px; line-height: 1.4; }
  .header .subtitle { font-size: 13px; }
  .header .meta { flex-wrap: wrap; gap: 8px; justify-content: center; font-size: 11px; }
  .header-badge { font-size: 11px; padding: 3px 10px; }

  .conclusion-card { padding: 14px; margin-bottom: 24px; }
  .conclusion-label { font-size: 10px; margin-bottom: 8px; }
  .conclusion-text { font-size: 14px; line-height: 1.7; margin-bottom: 12px; }
  .confidence-bar { flex-wrap: wrap; gap: 6px; }
  .confidence-bar .label { width: 100%; font-size: 11px; }
  .confidence-val { font-size: 13px; }

  .section { margin-bottom: 24px; }
  .section-title { font-size: 11px; letter-spacing: 1px; margin-bottom: 12px; }

  /* Timeline - hide line on mobile, use top-border instead */
  .timeline::before { display: none; }
  .step { padding-left: 0; padding-bottom: 12px; }
  .step-dot { display: none; }
  .step-card { border-left: 3px solid var(--green); }
  .step-card { padding: 10px 12px; }
  .step-header { flex-direction: column; align-items: flex-start; gap: 4px; margin-bottom: 6px; }
  .step-tool { font-size: 10px; padding: 2px 8px; }
  .step-time { font-size: 10px; }
  .step-query { font-size: 12px; margin-bottom: 4px; }
  .step-summary { font-size: 12px; line-height: 1.6; }
  .source-item { font-size: 12px; padding: 4px 0; }

  /* Charts */
  .chart-container { padding: 12px; }
  .chart-header { flex-direction: column; align-items: flex-start; gap: 6px; margin-bottom: 12px; }
  .chart-title { font-size: 14px; }
  .chart-legend { font-size: 11px; gap: 10px; }

  /* Market cards */
  .market-grid { grid-template-columns: 1fr; gap: 8px; }
  .market-card { padding: 12px; }
  .market-name { font-size: 13px; margin-bottom: 6px; }
  .odds-tag { font-size: 16px; }
  .market-volume { font-size: 11px; }

  /* Stat cards */
  .stat-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; }
  .stat-card { padding: 12px 10px; }
  .stat-icon { font-size: 18px; margin-bottom: 4px; }
  .stat-value { font-size: 16px; margin-bottom: 2px; }
  .stat-label { font-size: 10px; margin-bottom: 4px; }
  .stat-change { font-size: 10px; padding: 1px 6px; }

  /* News */
  .news-list { gap: 8px; }
  .news-item { padding: 10px; gap: 8px; }
  .news-sentiment { width: 28px; height: 28px; font-size: 14px; border-radius: 8px; }
  .news-title { font-size: 12px; margin-bottom: 3px; }
  .news-meta { font-size: 10px; gap: 8px; }
  .news-tag { font-size: 10px; padding: 1px 6px; margin-top: 4px; }

  /* Map */
  .map-container { padding: 12px; }
  .map-legend { gap: 8px; font-size: 11px; }
  .map-legend-item { font-size: 11px; }

  /* Bar chart */
  .bar-row { flex-direction: column; align-items: stretch; gap: 3px; }
  .bar-label { width: auto; text-align: left; font-size: 11px; }
  .bar-track { height: 24px; }
  .bar-fill { font-size: 10px; }

  /* Table - scrollable with hint */
  .table-wrap { margin: 0 -12px; padding: 0 12px; }
  .comp-table { font-size: 12px; min-width: 380px; }
  .comp-table th { padding: 8px 10px; font-size: 10px; }
  .comp-table td { padding: 8px 10px; font-size: 11px; line-height: 1.5; }

  /* Quotes */
  .quote-card { padding: 12px 14px; }
  .quote-text { font-size: 13px; line-height: 1.6; margin-bottom: 8px; }
  .quote-author { font-size: 12px; }

  /* Key points */
  .key-points { gap: 8px; }
  .kp-item { padding: 10px 12px; gap: 10px; }
  .kp-icon { font-size: 16px; }
  .kp-title { font-size: 12px; margin-bottom: 2px; }
  .kp-text { font-size: 11px; line-height: 1.5; }

  .footer { padding: 24px 0 12px; font-size: 10px; }
}

@media (max-width:430px) {
  .container { padding: 10px 10px 36px; }
  .header h1 { font-size: 18px; }
  .header .subtitle { font-size: 12px; }
  .conclusion-text { font-size: 13px; }
  .stat-grid { grid-template-columns: 1fr 1fr; gap: 6px; }
  .stat-value { font-size: 14px; }
  .stat-label { font-size: 9px; }
  .stat-change { font-size: 9px; }
  .step { padding-left: 0; }
  .step-summary { font-size: 11px; }
  .news-title { font-size: 11px; }
  .kp-text { font-size: 10px; }
  .comp-table td { font-size: 10px; }
}

@media (max-width:360px) {
  .header h1 { font-size: 16px; }
  .header .meta { font-size: 10px; gap: 6px; }
  .conclusion-text { font-size: 12px; }
  .stat-grid { grid-template-columns: 1fr; gap: 6px; }
  .step-card { padding: 8px 10px; }
}
</style>
</head>
<body>
<div class="container">
  <div class="header fade-in">
    <div class="header-badge"><span class="dot"></span> Research Complete</div>
    <h1>${esc(data.title)}</h1>
    ${data.subtitle ? `<p class="subtitle">${esc(data.subtitle)}</p>` : ''}
    <div class="meta">
      ${data.research_time ? `<span>🕐 ${esc(data.research_time)}</span>` : ''}
      <span>📊 ${totalSteps} steps completed</span>
      <span>🔗 ${totalSources} sources analyzed</span>
    </div>
  </div>

  ${data.conclusion ? `
  <div class="conclusion-card fade-in">
    <div class="conclusion-label">Key Finding</div>
    <div class="conclusion-text">${esc(data.conclusion.text)}</div>
    ${data.conclusion.confidence != null ? `
    <div class="confidence-bar">
      <span class="label">Research Confidence</span>
      <div class="confidence-track">
        <div class="confidence-fill" style="width:0%" data-target="${Math.round(data.conclusion.confidence * 100)}"></div>
      </div>
      <span class="confidence-val">${Math.round(data.conclusion.confidence * 100)}%</span>
    </div>` : ''}
  </div>` : ''}

  ${(data.steps && data.steps.length) ? `
  <div class="section fade-in">
    <div class="section-title">Research Process</div>
    <div class="timeline">
      ${renderTimeline(data.steps)}
    </div>
  </div>` : ''}

  ${vizSections}

  <div class="footer">
    <p>Generated by <a href="https://a2ui.me">OpenClaw Research Visualizer</a> · Powered by AI</p>
    <p style="margin-top:4px">This is an AI-generated research report. Not financial advice.</p>
  </div>
</div>

<script>
function toggleDetails(el){var d=el.querySelector('.step-details');if(d)d.classList.toggle('open')}
function showTooltip(e,el){var t=document.getElementById('mapTooltip'),r=el.getAttribute('data-region'),i=el.getAttribute('data-info');if(!i)return;t.innerHTML='<strong>'+r+'</strong><br/>'+i;t.classList.add('visible');var b=el.closest('.map-container').getBoundingClientRect();t.style.left=(e.clientX-b.left+10)+'px';t.style.top=(e.clientY-b.top-60)+'px'}
function hideTooltip(){document.getElementById('mapTooltip').classList.remove('visible')}
var obs=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target)}})},{threshold:0.1});
document.querySelectorAll('.fade-in').forEach(function(el){obs.observe(el)});
setTimeout(function(){var f=document.querySelector('.confidence-fill');if(f)f.style.width=f.dataset.target+'%'},500);
</script>
</body>
</html>`;
}

// --- Main ---
async function main() {
  const { input, output } = parseArgs();

  let jsonStr;
  if (input) {
    jsonStr = fs.readFileSync(path.resolve(input), 'utf-8');
  } else {
    // Read from stdin
    const chunks = [];
    for await (const chunk of process.stdin) chunks.push(chunk);
    jsonStr = Buffer.concat(chunks).toString('utf-8');
  }

  const data = JSON.parse(jsonStr);
  const html = generateHTML(data);

  if (output) {
    fs.writeFileSync(path.resolve(output), html, 'utf-8');
    console.error(`Report written to ${output}`);
  } else {
    process.stdout.write(html);
  }
}

main().catch(err => { console.error(err); process.exit(1); });
