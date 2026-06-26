/**
 * Raon Chat Widget — Embeddable JS
 * 
 * Usage: <script src="https://your-domain/raon-chat.js" data-api="https://api.k-startup.ai"></script>
 * 
 * Options (data attributes on script tag):
 *   data-api     — API base URL (default: http://localhost:8400)
 *   data-title   — Widget title (default: 라온 AI 비서)
 *   data-model   — LLM model (default: qwen3:8b)
 */
(function() {
  'use strict';
  if (document.getElementById('raon-chat-widget')) return; // prevent double init

  const scriptTag = document.currentScript;
  const API_URL = (scriptTag && scriptTag.dataset.api) || 'http://localhost:8400';
  const TITLE = (scriptTag && scriptTag.dataset.title) || '라온 AI 비서';
  const MODEL = (scriptTag && scriptTag.dataset.model) || 'qwen3:8b';

  const container = document.createElement('div');
  container.id = 'raon-chat-widget';
  document.body.appendChild(container);

  const style = document.createElement('style');
  style.textContent = `
    #raon-chat-toggle{position:fixed;bottom:24px;right:24px;z-index:10000;width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#FF6B35,#F7C948);border:none;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.2);font-size:24px;color:#fff;transition:transform .2s}
    #raon-chat-toggle:hover{transform:scale(1.1)}
    #raon-chat-panel{position:fixed;bottom:92px;right:24px;z-index:10000;width:380px;max-height:520px;background:#fff;border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,.15);display:none;flex-direction:column;overflow:hidden;font-family:-apple-system,BlinkMacSystemFont,sans-serif}
    #raon-chat-panel.open{display:flex}
    .raon-header{background:linear-gradient(135deg,#FF6B35,#F7C948);color:#fff;padding:16px 20px;font-size:16px;font-weight:600;display:flex;justify-content:space-between;align-items:center}
    .raon-header button{background:none;border:none;color:#fff;font-size:20px;cursor:pointer;padding:0}
    .raon-messages{flex:1;overflow-y:auto;padding:16px;min-height:300px;max-height:360px}
    .raon-msg{margin-bottom:12px;max-width:85%;padding:10px 14px;border-radius:12px;font-size:14px;line-height:1.5;word-break:break-word}
    .raon-msg.bot{background:#f0f0f0;color:#333;border-bottom-left-radius:4px}
    .raon-msg.user{background:#FF6B35;color:#fff;margin-left:auto;border-bottom-right-radius:4px}
    .raon-msg.loading{color:#999;font-style:italic}
    .raon-input-area{display:flex;border-top:1px solid #eee;padding:12px;gap:8px;align-items:center}
    .raon-input-area input[type="text"]{flex:1;border:1px solid #ddd;border-radius:8px;padding:10px 14px;font-size:14px;outline:none}
    .raon-input-area input[type="text"]:focus{border-color:#FF6B35}
    .raon-input-area button{background:#FF6B35;color:#fff;border:none;border-radius:8px;padding:10px 16px;font-size:14px;cursor:pointer;font-weight:600}
    .raon-input-area button:disabled{opacity:.5;cursor:not-allowed}
    .raon-pdf-btn{background:none!important;color:#999!important;border:none!important;font-size:20px!important;padding:8px!important;cursor:pointer;border-radius:8px!important;transition:color .2s}
    .raon-pdf-btn:hover{color:#FF6B35!important}
    .raon-pdf-btn.has-file{color:#FF6B35!important}
    .raon-file-badge{font-size:11px;color:#FF6B35;padding:2px 8px;background:#FFF3ED;border-radius:8px;display:none;align-items:center;gap:4px}
    .raon-file-badge.visible{display:flex}
    .raon-file-badge button{background:none!important;border:none!important;color:#999!important;font-size:14px!important;padding:0!important;cursor:pointer}
    .raon-mode-selector{display:flex;gap:6px;padding:8px 16px;background:#fafafa;border-bottom:1px solid #eee;overflow-x:auto}
    .raon-mode-btn{background:#eee;border:none;border-radius:16px;padding:4px 12px;font-size:12px;cursor:pointer;white-space:nowrap;color:#555}
    .raon-mode-btn.active{background:#FF6B35;color:#fff}
    @media(max-width:480px){#raon-chat-panel{width:calc(100vw - 32px);right:16px;bottom:88px}}
  `;
  document.head.appendChild(style);

  container.innerHTML = `
    <button id="raon-chat-toggle">🌅</button>
    <div id="raon-chat-panel">
      <div class="raon-header"><span>${TITLE}</span><button id="raon-close">✕</button></div>
      <div class="raon-mode-selector">
        <button class="raon-mode-btn active" data-mode="evaluate">📊 평가</button>
        <button class="raon-mode-btn" data-mode="improve">💡 개선</button>
        <button class="raon-mode-btn" data-mode="match">🎯 매칭</button>
        <button class="raon-mode-btn" data-mode="checklist">✅ 체크리스트</button>
      </div>
      <div class="raon-messages" id="raon-messages"><div class="raon-msg bot">안녕하세요! 라온입니다 🌅<br>사업계획서를 붙여넣거나 PDF를 첨부해주세요.</div></div>
      <div class="raon-file-badge" id="raon-file-badge"><span id="raon-file-name"></span><button id="raon-file-clear">✕</button></div>
      <div class="raon-input-area">
        <input type="file" id="raon-file-input" accept=".pdf" style="display:none"/>
        <button class="raon-pdf-btn" id="raon-pdf-btn" title="PDF 업로드">📎</button>
        <input type="text" id="raon-input" placeholder="사업 아이디어를 입력하세요..."/>
        <button id="raon-send">전송</button>
      </div>
    </div>`;

  let mode = 'evaluate';
  let pendingPdfBase64 = null;
  const panel = document.getElementById('raon-chat-panel');
  const msgs = document.getElementById('raon-messages');
  const inp = document.getElementById('raon-input');
  const sendBtn = document.getElementById('raon-send');
  const fileInput = document.getElementById('raon-file-input');
  const pdfBtn = document.getElementById('raon-pdf-btn');
  const fileBadge = document.getElementById('raon-file-badge');
  const fileNameEl = document.getElementById('raon-file-name');
  const fileClear = document.getElementById('raon-file-clear');

  document.getElementById('raon-chat-toggle').onclick = () => panel.classList.toggle('open');
  document.getElementById('raon-close').onclick = () => panel.classList.remove('open');
  document.querySelectorAll('.raon-mode-btn').forEach(b => b.onclick = () => {
    document.querySelectorAll('.raon-mode-btn').forEach(x => x.classList.remove('active'));
    b.classList.add('active'); mode = b.dataset.mode;
  });

  pdfBtn.onclick = () => fileInput.click();
  fileInput.onchange = () => {
    const file = fileInput.files[0];
    if (!file) return;
    if (file.size > 10 * 1024 * 1024) {
      addMsg('⚠️ 파일이 너무 큽니다 (최대 10MB)', 'bot');
      fileInput.value = ''; return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      pendingPdfBase64 = reader.result.split(',')[1];
      fileNameEl.textContent = file.name;
      fileBadge.classList.add('visible');
      pdfBtn.classList.add('has-file');
    };
    reader.readAsDataURL(file);
  };
  fileClear.onclick = () => {
    pendingPdfBase64 = null; fileInput.value = '';
    fileBadge.classList.remove('visible');
    pdfBtn.classList.remove('has-file');
  };

  function addMsg(html, cls) {
    const d = document.createElement('div'); d.className = 'raon-msg ' + cls;
    d.innerHTML = html; msgs.appendChild(d); msgs.scrollTop = msgs.scrollHeight; return d;
  }

  async function send() {
    const t = inp.value.trim();
    if (!t && !pendingPdfBase64) return;

    const displayText = pendingPdfBase64
      ? '📄 ' + fileNameEl.textContent + (t ? ' — ' + t : '')
      : t;
    addMsg(displayText, 'user'); inp.value = ''; sendBtn.disabled = true;
    const ld = addMsg('분석 중...', 'bot loading');

    const payload = { model: MODEL };
    if (pendingPdfBase64) {
      payload.pdf_base64 = pendingPdfBase64;
      if (t) payload.text = t;
      pendingPdfBase64 = null; fileInput.value = '';
      fileBadge.classList.remove('visible');
      pdfBtn.classList.remove('has-file');
    } else {
      payload.text = t;
    }

    try {
      const r = await fetch(API_URL + '/v1/' + mode, {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify(payload)
      });
      const d = await r.json(); ld.remove();
      if (d.status === 'ok') {
        const res = (d.result||d.response||'').replace(/\n/g,'<br>').replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>');
        addMsg((d.score ? '<div style="font-size:20px;margin-bottom:8px">📊 '+d.score+'점</div>' : '') + res, 'bot');
      } else addMsg('⚠️ ' + (d.error||'오류'), 'bot');
    } catch(e) { ld.remove(); addMsg('⚠️ 서버 연결 실패', 'bot'); }
    sendBtn.disabled = false; inp.focus();
  }

  sendBtn.onclick = send;
  inp.onkeydown = e => { if (e.key === 'Enter') send(); };
})();
