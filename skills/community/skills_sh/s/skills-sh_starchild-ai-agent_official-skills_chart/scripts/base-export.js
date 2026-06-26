/* Chart Skill — Export Utilities v3 (project-based)
 * Strategy: ECharts native getDataURL() + Canvas merge
 *
 * Functions exposed:
 *   downloadPNG()       — merge all charts into one PNG and download
 *   copyToClipboard()   — copy merged PNG to clipboard (fallback: download)
 *   saveToProject()     — POST PNG to /save-chart and save into current project dir
 */

/* ── Toast notification ─────────────────────────────────── */
function showToast(msg, type = 'info') {
  let t = document.getElementById('toast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'toast';
    t.style.cssText = `
      position:fixed;bottom:24px;right:24px;z-index:9999;
      background:#1e2130;border:1px solid #2d3148;color:#e1e4ea;
      padding:10px 18px;border-radius:8px;font-size:0.85rem;
      opacity:0;transition:opacity 0.25s;pointer-events:none;
      box-shadow:0 4px 20px rgba(0,0,0,0.4);
    `;
    document.body.appendChild(t);
  }
  t.style.borderColor = type === 'success' ? '#34d399' : type === 'error' ? '#ef4444' : '#2d3148';
  t.style.color = type === 'success' ? '#34d399' : type === 'error' ? '#ef4444' : '#e1e4ea';
  t.textContent = msg;
  t.style.opacity = '1';
  clearTimeout(t._hideTimer);
  t._hideTimer = setTimeout(() => { t.style.opacity = '0'; }, 2500);
}

/* ── Preview-safe API URL helpers ─────────────────────────── */
function getPreviewBasePath() {
  const m = window.location.pathname.match(/^(\/preview\/[^/]+\/)/);
  return m ? m[1] : '/';
}

function apiUrl(endpoint) {
  const base = getPreviewBasePath();
  const ep = String(endpoint || '').replace(/^\/+/, '');
  return `${base}${ep}`;
}

/* ── Resolve current project from pathname ───────────────── */
function getCurrentProjectPath() {
  // expected path: /preview/<id>/<project>/index.html
  // or /<project>/index.html
  let path = window.location.pathname;
  path = path.replace(/^\/preview\/[^/]+\//, '/');
  path = path.replace(/^\//, '');

  // remove filename
  const parts = path.split('/').filter(Boolean);
  if (!parts.length) return '';
  if (parts[parts.length - 1].includes('.')) parts.pop();
  return parts.join('/');
}

/* ── Collect all ECharts instances from page ─────────────── */
function getAllChartInstances() {
  if (window.CHART_INSTANCES && window.CHART_INSTANCES.length > 0) {
    return window.CHART_INSTANCES.filter(i => i && !i.isDisposed());
  }
  if (!window.echarts) return [];
  const containers = document.querySelectorAll('[_echarts_instance_]');
  const instances = [];
  containers.forEach(c => {
    const inst = echarts.getInstanceByDom(c);
    if (inst && !inst.isDisposed()) instances.push(inst);
  });
  return instances;
}

/* ── Merge multiple chart canvases into one PNG DataURL ───── */
async function mergeChartsToDataURL() {
  const instances = getAllChartInstances();
  if (instances.length === 0) throw new Error('No ECharts instances found');

  instances.forEach(inst => { try { inst.resize(); } catch(e) {} });
  await new Promise(r => setTimeout(r, 150));

  const images = instances.map(inst => ({
    dataUrl: inst.getDataURL({
      type: 'png',
      pixelRatio: 2,
      backgroundColor: '#1a1d27',
      excludeComponents: []
    }),
    width: inst.getWidth(),
    height: inst.getHeight()
  }));

  // Always compose onto a new canvas so output consistently includes title
  // (even when there's only one chart).
  const layout = window.CHART_LAYOUT || 'vertical';
  const PR = 2;
  const PAD = 24 * PR;

  let canvasW, canvasH;
  const cols = layout === 'grid' ? Math.min(2, images.length) : 1;
  const rows = Math.ceil(images.length / cols);

  // Reserve explicit title area so both button-save and one-click screenshot are equivalent
  const title = document.querySelector('h1')?.textContent || document.title || 'Chart';
  const subtitle = document.querySelector('.subtitle')?.textContent || '';
  const titleHeight = PAD * 2.2;

  if (layout === 'grid') {
    canvasW = (images[0].width * PR * cols) + PAD * (cols + 1);
    canvasH = titleHeight + (images[0].height * PR * rows) + PAD * (rows + 1);
  } else {
    canvasW = Math.max(...images.map(i => i.width)) * PR + PAD * 2;
    canvasH = titleHeight + images.reduce((s, i) => s + i.height * PR, 0) + PAD * (images.length + 1);
  }

  const canvas = document.createElement('canvas');
  canvas.width = canvasW;
  canvas.height = canvasH;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#0f1117';
  ctx.fillRect(0, 0, canvasW, canvasH);

  ctx.fillStyle = '#f0f2f5';
  ctx.font = `bold ${28}px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;
  ctx.fillText(title, PAD, PAD * 1.1);
  if (subtitle) {
    ctx.fillStyle = '#9aa0b4';
    ctx.font = `normal ${16 * PR / 2}px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;
    ctx.fillText(subtitle, PAD, PAD * 1.7);
  }

  const loadImg = (dataUrl) => new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = dataUrl;
  });

  const imgs = await Promise.all(images.map(i => loadImg(i.dataUrl)));

  for (let idx = 0; idx < imgs.length; idx++) {
    const img = imgs[idx];
    const w = images[idx].width * PR;
    const h = images[idx].height * PR;
    let x, y;

    if (layout === 'grid') {
      const col = idx % cols;
      const row = Math.floor(idx / cols);
      x = PAD + col * (w + PAD);
      y = titleHeight + PAD + row * (h + PAD);
    } else {
      x = PAD;
      y = titleHeight + images.slice(0, idx).reduce((s, i) => s + i.height * PR + PAD, 0);
    }
    ctx.drawImage(img, x, y, w, h);
  }

  return canvas.toDataURL('image/png');
}

/* ── Unified export helpers (single pipeline) ───────────── */
async function exportMergedPNG() {
  const dataUrl = await mergeChartsToDataURL();
  const blob = await (await fetch(dataUrl)).blob();
  return { dataUrl, blob };
}

async function blobToDataURL(blob) {
  return await new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

/* ── Download PNG ───────────────────────────────────────── */
async function downloadPNG(btn) {
  btn = btn || event?.currentTarget;
  const orig = btn?.textContent;
  if (btn) { btn.textContent = '⏳...'; btn.disabled = true; }
  try {
    const { blob } = await exportMergedPNG();
    const filename = (document.title || 'chart').replace(/[^a-zA-Z0-9\u4e00-\u9fff-_]/g, '_') + '_' +
                     new Date().toISOString().slice(0,10) + '.png';

    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    if (window.self !== window.top) {
      window.open(url, '_blank', 'noopener');
    }

    setTimeout(() => URL.revokeObjectURL(url), 2000);

    if (btn) { btn.textContent = '✅'; btn.style.borderColor = '#34d399'; btn.style.color = '#34d399'; }
    showToast('PNG ready (download/new tab)', 'success');
    setTimeout(() => {
      if (btn) { btn.textContent = orig; btn.disabled = false; btn.style.borderColor = ''; btn.style.color = ''; }
    }, 2000);
  } catch(e) {
    console.error('[chart] download failed:', e);
    if (btn) { btn.textContent = '❌'; btn.disabled = false; }
    showToast('Export failed: ' + e.message, 'error');
    setTimeout(() => { if (btn) { btn.textContent = orig; } }, 2000);
  }
}

/* ── Copy to Clipboard (same output as save/download) ───── */
async function copyToClipboard(btn) {
  btn = btn || event?.currentTarget;
  const orig = btn?.textContent;
  if (btn) { btn.textContent = '⏳...'; btn.disabled = true; }
  try {
    const { blob } = await exportMergedPNG();

    if (navigator.clipboard && typeof ClipboardItem !== 'undefined') {
      await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]);
      if (btn) { btn.textContent = '✅'; btn.style.borderColor = '#34d399'; btn.style.color = '#34d399'; }
      showToast('Image copied to clipboard ✓', 'success');
    } else {
      // Fallback still uses the exact same merged PNG bytes
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank', 'noopener');
      setTimeout(() => URL.revokeObjectURL(url), 3000);
      showToast('Clipboard N/A — opened same exported image in new tab', 'info');
    }
  } catch(e) {
    console.warn('[chart] clipboard failed, fallback to download:', e.message);
    try {
      const { blob } = await exportMergedPNG();
      const filename = (document.title || 'chart').replace(/[^a-zA-Z0-9\u4e00-\u9fff-_]/g, '_') + '_'+
                       new Date().toISOString().slice(0,10) + '.png';
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = filename;
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(url), 2000);
      showToast('Clipboard N/A — downloaded same exported image', 'info');
    } catch(e2) {
      showToast('Export failed: ' + e2.message, 'error');
    }
  } finally {
    setTimeout(() => {
      if (btn) { btn.textContent = orig; btn.disabled = false; btn.style.borderColor = ''; btn.style.color = ''; }
    }, 2000);
  }
}

/* ── Save to Project ────────────────────────────────────── */
async function saveToProject(btn) {
  btn = btn || event?.currentTarget;
  const orig = btn?.textContent;
  if (btn) { btn.textContent = '⏳ Saving...'; btn.disabled = true; }
  try {
    const project = getCurrentProjectPath();
    if (!project) throw new Error('Cannot detect project folder from URL');

    const { blob } = await exportMergedPNG();
    const dataUrl = await blobToDataURL(blob);
    const filename = 'screenshot.png';

    const resp = await fetch(apiUrl('save-chart'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dataUrl, filename, project })
    });

    if (!resp.ok) throw new Error(`Server returned ${resp.status}`);
    const result = await resp.json();

    if (btn) { btn.textContent = '✅ Saved!'; btn.style.borderColor = '#34d399'; btn.style.color = '#34d399'; }
    showToast(`Saved: ${result.url}`, 'success');
  } catch(e) {
    console.warn('[chart] saveToProject failed:', e.message);
    showToast('Save API not available — downloading PNG...', 'info');
    await downloadPNG(null);
    if (btn) { btn.textContent = '📥 Downloaded'; }
  } finally {
    setTimeout(() => {
      if (btn) { btn.textContent = orig; btn.disabled = false; btn.style.borderColor = ''; btn.style.color = ''; }
    }, 3000);
  }
}

/* ── Backward-compat aliases ────────────────────────────── */
window.saveToWorkspace = saveToProject;
window.savePage = function(btn) {
  showToast('savePage removed in project-based mode', 'info');
};

/* ── Auto-resize all ECharts on window resize ───────────── */
window.addEventListener('resize', () => {
  if (!window.echarts) return;
  getAllChartInstances().forEach(inst => {
    try { inst.resize(); } catch(e) {}
  });
});
