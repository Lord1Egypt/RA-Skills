/* ============================================================
 * Trip Todo 同步模块 + 勾选沉底交互
 * ============================================================
 *
 * 直接把整段贴到 index.html 的 <script> 里即可。
 *
 * HTML 要求：
 *   1. 每个 <li class="todo-item" data-id="u0">...</li>
 *   2. <ul class="todo-list" id="todoUrgent">...</ul>
 *      <ul class="todo-list" id="todoPack">...</ul>
 *   3. 进度条 DOM（可选）：#progressText / #progressBar / #progressPercent
 *
 * 同步后端（修改下方 SYNC_BACKEND 切换）：
 *   - 'local'     : 仅本地 localStorage（默认，零配置）
 *   - 'gist'      : GitHub Gist（需 PAT）
 *   - 'jsonbin'   : JSONBin.io（需 Master Key）
 *   - 'workers'   : 自建 Cloudflare Workers
 *   - 'custom'    : 自己实现 customBackend 对象
 * ============================================================ */

// ======================== 配置区 ========================

// 🔧 改成你的房间 ID（全局唯一，多攻略别重名）
const SYNC_ROOM = 'my-trip-2026';

// 🔧 选择同步后端
const SYNC_BACKEND = 'local';  // 'local' | 'gist' | 'jsonbin' | 'workers' | 'custom'

// GitHub Gist 配置（仅 SYNC_BACKEND='gist' 时）
const GIST_CONFIG = {
  token: 'ghp_xxx',            // Personal Access Token（scope: gist）
  gistId: '',                  // 首次留空，自动创建；后续填写 Gist ID
  filename: SYNC_ROOM + '.json',
};

// JSONBin 配置（仅 SYNC_BACKEND='jsonbin' 时）
const JSONBIN_CONFIG = {
  masterKey: '$2a$10$xxx',     // X-Master-Key
  binId: '',                   // 首次留空，自动创建；后续填写 Bin ID
};

// Cloudflare Workers 配置（仅 SYNC_BACKEND='workers' 时）
const WORKERS_CONFIG = {
  baseUrl: 'https://your-worker.your-subdomain.workers.dev',
};

// localStorage key（自动按 roomId 前缀隔离）
const TODO_KEY = 'trip_' + SYNC_ROOM + '_todos';
const TODO_TS_KEY = 'trip_' + SYNC_ROOM + '_todos_ts';

// ======================== 同步后端实现 ========================

const LocalBackend = {
  async load() { return null; },  // 永远走 localStorage
  async save() { return { ok: true, ts: Date.now() }; },
};

const GistBackend = {
  async load() {
    if (!GIST_CONFIG.gistId) return null;
    const r = await fetch('https://api.github.com/gists/' + GIST_CONFIG.gistId, {
      headers: { 'Authorization': 'token ' + GIST_CONFIG.token }
    });
    if (!r.ok) return null;
    const j = await r.json();
    const content = j.files[GIST_CONFIG.filename];
    if (!content) return null;
    try { return JSON.parse(content.content); } catch { return null; }
  },
  async save(payload) {
    const url = GIST_CONFIG.gistId
      ? 'https://api.github.com/gists/' + GIST_CONFIG.gistId
      : 'https://api.github.com/gists';
    const method = GIST_CONFIG.gistId ? 'PATCH' : 'POST';
    const body = {
      description: 'Trip Todo Sync - ' + SYNC_ROOM,
      public: false,
      files: { [GIST_CONFIG.filename]: { content: JSON.stringify(payload, null, 2) } }
    };
    const r = await fetch(url, {
      method,
      headers: {
        'Authorization': 'token ' + GIST_CONFIG.token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });
    if (!r.ok) throw new Error('Gist save failed');
    const j = await r.json();
    if (!GIST_CONFIG.gistId) {
      console.log('✅ Gist 创建成功，请把下面的 ID 写回 GIST_CONFIG.gistId：', j.id);
      GIST_CONFIG.gistId = j.id;
    }
    return { ok: true, ts: Date.now() };
  }
};

const JSONBinBackend = {
  async load() {
    if (!JSONBIN_CONFIG.binId) return null;
    const r = await fetch('https://api.jsonbin.io/v3/b/' + JSONBIN_CONFIG.binId + '/latest', {
      headers: { 'X-Master-Key': JSONBIN_CONFIG.masterKey }
    });
    if (!r.ok) return null;
    const j = await r.json();
    return j.record;
  },
  async save(payload) {
    const url = JSONBIN_CONFIG.binId
      ? 'https://api.jsonbin.io/v3/b/' + JSONBIN_CONFIG.binId
      : 'https://api.jsonbin.io/v3/b';
    const method = JSONBIN_CONFIG.binId ? 'PUT' : 'POST';
    const r = await fetch(url, {
      method,
      headers: {
        'X-Master-Key': JSONBIN_CONFIG.masterKey,
        'Content-Type': 'application/json',
        'X-Bin-Private': 'true'
      },
      body: JSON.stringify(payload)
    });
    if (!r.ok) throw new Error('JSONBin save failed');
    const j = await r.json();
    if (!JSONBIN_CONFIG.binId && j.metadata && j.metadata.id) {
      console.log('✅ Bin 创建成功，请把下面的 ID 写回 JSONBIN_CONFIG.binId：', j.metadata.id);
      JSONBIN_CONFIG.binId = j.metadata.id;
    }
    return { ok: true, ts: Date.now() };
  }
};

const WorkersBackend = {
  async load() {
    const r = await fetch(WORKERS_CONFIG.baseUrl + '/room/' + SYNC_ROOM, { cache: 'no-store' });
    if (!r.ok) return null;
    return r.json();
  },
  async save(payload) {
    const r = await fetch(WORKERS_CONFIG.baseUrl + '/room/' + SYNC_ROOM, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!r.ok) throw new Error('Workers save failed');
    return r.json();
  }
};

// 如需自定义，实现同样的 load() / save(payload) 两个 async 方法
const customBackend = {
  async load() { return null; },
  async save(payload) { return { ok: true, ts: Date.now() }; }
};

const BACKENDS = {
  local: LocalBackend,
  gist: GistBackend,
  jsonbin: JSONBinBackend,
  workers: WorkersBackend,
  custom: customBackend,
};
const backend = BACKENDS[SYNC_BACKEND] || LocalBackend;

// ======================== UI：状态徽章 ========================

let syncStatusEl = null;
function setSyncStatus(text, color) {
  if (!syncStatusEl) {
    syncStatusEl = document.createElement('div');
    syncStatusEl.style.cssText = [
      'position:fixed', 'bottom:20px', 'left:50%',
      'transform:translateX(-50%) translateY(8px)',
      'font-size:13px', 'font-weight:500', 'letter-spacing:0.3px',
      'padding:10px 18px 10px 14px', 'border-radius:999px',
      'background:rgba(15,28,46,0.82)',
      'backdrop-filter:blur(12px)', '-webkit-backdrop-filter:blur(12px)',
      'border:1px solid rgba(255,255,255,0.08)',
      'color:#e8f1ff',
      'box-shadow:0 8px 32px rgba(0,0,0,0.35),0 0 0 1px rgba(255,255,255,0.04) inset',
      'z-index:9999', 'pointer-events:none', 'opacity:0',
      'transition:opacity .25s ease,transform .25s ease',
      'display:flex', 'align-items:center', 'gap:8px', 'white-space:nowrap'
    ].join(';');
    document.body.appendChild(syncStatusEl);
  }
  const c = color || '#7dd3fc';
  syncStatusEl.innerHTML =
    '<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:' + c +
    ';box-shadow:0 0 8px ' + c + '"></span><span>' + text + '</span>';
  syncStatusEl.style.opacity = '1';
  syncStatusEl.style.transform = 'translateX(-50%) translateY(0)';
  clearTimeout(syncStatusEl._t);
  syncStatusEl._t = setTimeout(() => {
    syncStatusEl.style.opacity = '0';
    syncStatusEl.style.transform = 'translateX(-50%) translateY(8px)';
  }, 1800);
}

// ======================== 状态读写 ========================

const todoItems = document.querySelectorAll('.todo-item');
let syncTimer = null;

function collectState() {
  const state = {};
  todoItems.forEach(item => { state[item.dataset.id] = item.classList.contains('done'); });
  return state;
}

function applyState(saved) {
  if (!saved) return;
  todoItems.forEach(item => {
    if (saved[item.dataset.id] === true) item.classList.add('done');
    else if (saved[item.dataset.id] === false) item.classList.remove('done');
  });
  reorderAllLists();
}

// ======================== done 沉底排序 ========================

function reorderList(ul) {
  if (!ul) return;
  const items = Array.from(ul.children);
  const pending = items.filter(x => !x.classList.contains('done'));
  const done = items.filter(x => x.classList.contains('done'));
  const frag = document.createDocumentFragment();
  pending.concat(done).forEach(x => frag.appendChild(x));
  ul.appendChild(frag);
}
function reorderAllLists() {
  document.querySelectorAll('.todo-list').forEach(reorderList);
}

// ======================== 云端同步 ========================

async function uploadTodos() {
  const state = collectState();
  const ts = Date.now();
  try {
    localStorage.setItem(TODO_KEY, JSON.stringify(state));
    localStorage.setItem(TODO_TS_KEY, String(ts));
  } catch (e) {}
  if (SYNC_BACKEND === 'local') {
    setSyncStatus('已保存到本地', '#7dd3fc');
    return;
  }
  try {
    await backend.save({
      state,
      ts,
      updatedBy: navigator.userAgent.slice(0, 20),
    });
    setSyncStatus('已同步到云端', '#34d399');
  } catch (e) {
    setSyncStatus('离线，已保存到本地', '#fbbf24');
  }
}

function saveTodos() {
  try {
    localStorage.setItem(TODO_KEY, JSON.stringify(collectState()));
    localStorage.setItem(TODO_TS_KEY, String(Date.now()));
  } catch (e) {}
  updateProgress();
  clearTimeout(syncTimer);
  syncTimer = setTimeout(uploadTodos, 600);
}

async function loadTodos() {
  // 先用本地快速渲染
  try {
    const saved = JSON.parse(localStorage.getItem(TODO_KEY) || '{}');
    applyState(saved);
  } catch (e) {}
  updateProgress();

  if (SYNC_BACKEND === 'local') return;

  // 再拉云端，仅当云端比本地新才覆盖
  try {
    const remote = await backend.load();
    if (!remote || !remote.state) return;
    const localTs = parseInt(localStorage.getItem(TODO_TS_KEY) || '0', 10);
    const remoteTs = remote.ts || 0;
    if (remoteTs > localTs) {
      applyState(remote.state);
      try {
        localStorage.setItem(TODO_KEY, JSON.stringify(remote.state));
        localStorage.setItem(TODO_TS_KEY, String(remoteTs));
      } catch (e) {}
      updateProgress();
      setSyncStatus('已拉取云端最新数据', '#34d399');
    }
  } catch (e) {
    setSyncStatus('离线模式，显示本地记录', '#fbbf24');
  }
}

// ======================== 进度条 ========================

function updateProgress() {
  const active = document.querySelectorAll('#todoUrgent .todo-item, #todoPack .todo-item');
  const total = active.length;
  const done = [...active].filter(x => x.classList.contains('done')).length;
  const percent = total ? Math.round(done / total * 100) : 0;
  const pt = document.getElementById('progressText');
  const pb = document.getElementById('progressBar');
  const pp = document.getElementById('progressPercent');
  if (pt) pt.textContent = done + ' / ' + total;
  if (pb) pb.style.width = percent + '%';
  if (pp) pp.textContent = percent + '%';
}

// ======================== 点击交互 ========================

todoItems.forEach(item => {
  item.addEventListener('click', () => {
    const willBeDone = !item.classList.contains('done');
    item.classList.toggle('done');
    saveTodos();
    const ul = item.parentElement;
    if (!ul) return;
    if (willBeDone) {
      item.classList.add('flying');
      setTimeout(() => {
        ul.appendChild(item);
        item.classList.remove('flying');
      }, 220);
    } else {
      const firstDone = ul.querySelector('.todo-item.done');
      item.classList.add('flying');
      setTimeout(() => {
        if (firstDone && firstDone !== item) ul.insertBefore(item, firstDone);
        else ul.appendChild(item);
        item.classList.remove('flying');
      }, 180);
    }
  });
});

// ======================== 启动 ========================

loadTodos();
