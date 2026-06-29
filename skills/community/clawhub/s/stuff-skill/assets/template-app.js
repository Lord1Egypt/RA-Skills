// ===== PWA Generator — App Template =====
// Replace __TABLE__ with actual table name, __FIELDS__ with field config

const API = '/api/__TABLE__';
const $ = s => document.querySelector(s);
const listEl = $('#list');
const countEl = $('#count');
const searchEl = $('#search');
const emptyEl = $('#empty');
const editor = $('#editor');
const form = $('#editorForm');
const titleEl = $('#editorTitle');
const deleteBtn = $('#deleteInEditor');
let editingId = null;

/* --- Field config (generated from schema) --- */
// __FIELD_CONFIG__
// Example:
// const FIELDS = [
//   { key: 'name', label: '名称', type: 'text', required: true, searchable: true, display: 'title' },
//   { key: 'status', label: '状态', type: 'enum', options: ['在用','库存','退役'], filterable: true, display: 'badge' },
//   { key: 'brand', label: '品牌', type: 'smart-select', filterable: true, display: 'tag' },
// ];
// const SMART_FIELDS = FIELDS.filter(f => f.type === 'smart-select').map(f => f.key);
// const SEARCHABLE = FIELDS.filter(f => f.searchable).map(f => f.key);
// const TITLE_FIELD = FIELDS.find(f => f.display === 'title')?.key || 'name';
// const STATUS_FIELD = FIELDS.find(f => f.type === 'enum' && f.filterable)?.key || 'status';

/* --- Data --- */
let items = [];

async function fetchItems() {
  try {
    const res = await fetch(API);
    items = await res.json();
  } catch (e) {
    console.warn('Cloud fetch failed, using local cache', e);
    const local = localStorage.getItem('__TABLE__-cache');
    if (local) items = JSON.parse(local);
  }
  localStorage.setItem('__TABLE__-cache', JSON.stringify(items));
}

async function saveItem(item) {
  try {
    await fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(item),
    });
  } catch (e) {
    console.warn('Cloud save failed', e);
  }
}

async function deleteItem(id) {
  try {
    await fetch(`${API}?id=${encodeURIComponent(id)}`, { method: 'DELETE' });
  } catch (e) {
    console.warn('Cloud delete failed', e);
  }
}

/* --- Filters --- */
// __FILTER_VARS__
// Example:
// let filterStatus = '';
// let filterBrand = '';

function setupChips(containerId, onSelect) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.addEventListener('click', e => {
    const btn = e.target.closest('.chip');
    if (!btn) return;
    container.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    onSelect(btn.dataset.val);
  });
}

// __SETUP_CHIPS__
// Example:
// setupChips('statusChips', v => { filterStatus = v; render(); });
// setupChips('brandChips', v => { filterBrand = v; render(); });
searchEl.addEventListener('input', render);

/* --- Sort --- */
let sortMode = 'status';
const sortBar = document.getElementById('sortBar');
if (sortBar) {
  sortBar.addEventListener('click', e => {
    const btn = e.target.closest('.sort-btn');
    if (!btn) return;
    sortBar.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    sortMode = btn.dataset.sort;
    render();
  });
}

/* --- Render --- */
function render() {
  const q = searchEl.value.trim().toLowerCase();
  const filtered = items.filter(item => {
    // __FILTER_LOGIC__
    // Example:
    // if (filterStatus && item.status !== filterStatus) return false;
    // if (filterBrand && item.brand !== filterBrand) return false;
    if (q) {
      const searchText = SEARCHABLE.map(k => item[k] || '').join(' ').toLowerCase();
      if (!searchText.includes(q)) return false;
    }
    return true;
  });

  // __SORT_LOGIC__
  // Example: sort by status order, or by date

  countEl.textContent = `${filtered.length}/${items.length}`;
  emptyEl.style.display = filtered.length ? 'none' : 'block';

  listEl.innerHTML = filtered.map(item => {
    // __CARD_TEMPLATE__
    // Example: return card HTML string using item fields
    return `<article class="card" data-id="${item.id}">...</article>`;
  }).join('');
}

function esc(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

/* --- Card click → edit --- */
listEl.addEventListener('click', e => {
  const card = e.target.closest('.card');
  if (!card) return;
  const item = items.find(x => x.id === card.dataset.id);
  if (!item) return;
  openEditor(item);
});

/* --- Smart Select --- */
// const PREDEFINED = { /* fields with fixed options */ };

function getFieldValues(field) {
  return [...new Set(items.map(b => b[field]).filter(Boolean))].sort();
}

function initSmartSelects() {
  SMART_FIELDS.forEach(field => {
    const sel = document.querySelector(`.smart-select[data-field="${field}"]`);
    const hidden = document.querySelector(`input[name="${field}"][type="hidden"]`);
    const customInput = document.querySelector(`.smart-input[data-field="${field}"]`);
    if (!sel || !hidden) return;

    const values = PREDEFINED[field] || getFieldValues(field);
    sel.innerHTML = '<option value="">请选择</option>'
      + values.map(v => '<option value="' + v.replace(/"/g,'&quot;') + '">' + v + '</option>').join('')
      + '<option value="__custom__">✏️ 手动输入…</option>';

    const curVal = hidden.value;
    if (curVal && values.includes(curVal)) {
      sel.value = curVal;
      if (customInput) customInput.style.display = 'none';
    } else if (curVal) {
      sel.value = '__custom__';
      if (customInput) { customInput.value = curVal; customInput.style.display = 'block'; }
    }

    sel.onchange = () => {
      if (sel.value === '__custom__') {
        if (customInput) { customInput.style.display = 'block'; customInput.value = ''; customInput.focus(); }
        hidden.value = '';
      } else {
        if (customInput) customInput.style.display = 'none';
        hidden.value = sel.value;
      }
    };
    if (customInput) customInput.oninput = () => { hidden.value = customInput.value; };
  });
}

/* --- Editor --- */
function openEditor(item) {
  editingId = item ? item.id : null;
  titleEl.textContent = item ? '编辑' : '新增';
  deleteBtn.style.display = item ? 'block' : 'none';
  form.reset();
  if (item) {
    Object.entries(item).forEach(([k, v]) => {
      if (form.elements[k]) form.elements[k].value = v ?? '';
    });
    SMART_FIELDS.forEach(f => {
      const h = document.querySelector(`input[name="${f}"][type="hidden"]`);
      if (h) h.value = item[f] || '';
    });
  } else {
    SMART_FIELDS.forEach(f => {
      const h = document.querySelector(`input[name="${f}"][type="hidden"]`);
      if (h) h.value = '';
    });
  }
  editor.showModal();
  setTimeout(initSmartSelects, 50);
}

$('#addBtn').addEventListener('click', () => openEditor(null));
$('#cancelBtn').addEventListener('click', () => editor.close());
$('#closeEditor').addEventListener('click', () => editor.close());

form.addEventListener('submit', async e => {
  e.preventDefault();
  const fd = new FormData(form);
  const data = Object.fromEntries(fd.entries());

  if (editingId) {
    const updated = { ...items.find(b => b.id === editingId), ...data };
    items = items.map(b => b.id === editingId ? updated : b);
    await saveItem(updated);
  } else {
    const newItem = { id: 'id-' + Date.now(), ...data };
    items.unshift(newItem);
    await saveItem(newItem);
  }

  localStorage.setItem('__TABLE__-cache', JSON.stringify(items));
  editor.close();
  render();
});

deleteBtn.addEventListener('click', async () => {
  if (!editingId) return;
  if (!confirm('确认删除这条记录？')) return;
  await deleteItem(editingId);
  items = items.filter(x => x.id !== editingId);
  localStorage.setItem('__TABLE__-cache', JSON.stringify(items));
  editor.close();
  render();
});

/* --- Smart Select Manager --- */
const smartSelectManager = $('#smartSelectManager');
const smartSelectManagerTitle = $('#smartSelectManagerTitle');
const smartSelectManagerList = $('#smartSelectManagerList');

$('#closeSmartSelectManager').addEventListener('click', () => smartSelectManager.close());
$('#closeSmartSelectManager2').addEventListener('click', () => smartSelectManager.close());

function openSmartSelectManager(field) {
  const fieldConfig = FIELDS.find(f => f.key === field);
  smartSelectManagerTitle.textContent = '管理' + (fieldConfig ? fieldConfig.label : field);
  const values = getFieldValues(field);
  if (!values.length) {
    smartSelectManagerList.innerHTML = '<div class="smart-manager-empty">还没有记录</div>';
    smartSelectManager.showModal();
    return;
  }
  smartSelectManagerList.innerHTML = values.map(v => {
    const count = items.filter(x => x[field] === v).length;
    return '<div class="smart-manager-item" data-value="' + esc(v) + '" data-field="' + field + '">'
      + '<span class="smart-manager-name">' + esc(v) + '</span>'
      + '<span class="smart-manager-count">' + count + '条</span>'
      + '<div class="smart-manager-actions">'
      + '<button type="button" class="smart-manager-action" data-action="rename" title="改名">✏️</button>'
      + '<button type="button" class="smart-manager-action danger" data-action="delete" title="删除">🗑</button>'
      + '</div></div>';
  }).join('');

  smartSelectManagerList.querySelectorAll('.smart-manager-action').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const row = e.target.closest('.smart-manager-item');
      const oldVal = row.dataset.value;
      const f = row.dataset.field;
      const action = e.target.closest('[data-action]').dataset.action;

      if (action === 'delete') {
        const count = items.filter(x => x[f] === oldVal).length;
        if (!confirm('删除「' + oldVal + '」？\n将清空 ' + count + ' 条记录的该字段。')) return;
        for (const item of items) {
          if (item[f] === oldVal) {
            item[f] = '';
            await saveItem(item);
          }
        }
        localStorage.setItem('__TABLE__-cache', JSON.stringify(items));
        render();
        openSmartSelectManager(f);
        initSmartSelects();
      }

      if (action === 'rename') {
        const newName = prompt('将「' + oldVal + '」改名为：', oldVal);
        if (!newName || newName.trim() === '' || newName.trim() === oldVal) return;
        const trimmed = newName.trim();
        for (const item of items) {
          if (item[f] === oldVal) {
            item[f] = trimmed;
            await saveItem(item);
          }
        }
        localStorage.setItem('__TABLE__-cache', JSON.stringify(items));
        render();
        openSmartSelectManager(f);
        initSmartSelects();
      }
    });
  });

  smartSelectManager.showModal();
}

// Attach manage buttons to smart-select fields
document.querySelectorAll('.smart-manage-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    openSmartSelectManager(btn.dataset.field);
  });
});

/* --- PWA --- */
if ('serviceWorker' in navigator) navigator.serviceWorker.register('./sw.js');

/* --- Init --- */
await fetchItems();
document.addEventListener('visibilitychange', async () => {
  if (document.visibilityState === 'visible') {
    await fetchItems();
    render();
  }
});
render();
