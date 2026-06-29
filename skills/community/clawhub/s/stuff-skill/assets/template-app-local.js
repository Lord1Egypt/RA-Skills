// ===== PWA Generator — Local-Only App Template =====
// 纯本地模式：数据全部存 localStorage，不需要任何后端/API/Cloudflare
// 用户双击 index.html 即可使用
// Replace __TABLE__ with actual table name, __FIELDS__ with field config

const STORE_KEY = '__TABLE__-data';
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

/* --- Data (localStorage only) --- */
let items = [];

function loadItems() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    items = raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.warn('Failed to load data from localStorage', e);
    items = [];
  }
}

function saveItems() {
  localStorage.setItem(STORE_KEY, JSON.stringify(items));
}

function saveItem(item) {
  const idx = items.findIndex(x => x.id === item.id);
  if (idx >= 0) {
    items[idx] = item;
  } else {
    items.unshift(item);
  }
  saveItems();
}

function deleteItemById(id) {
  items = items.filter(x => x.id !== id);
  saveItems();
}

/* --- Export/Import (数据备份，弥补不能跨设备同步的缺陷) --- */
function exportData() {
  const blob = new Blob([JSON.stringify(items, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = '__TABLE__-backup-' + new Date().toISOString().slice(0, 10) + '.json';
  a.click();
  URL.revokeObjectURL(url);
}

function importData(file) {
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const data = JSON.parse(e.target.result);
      if (!Array.isArray(data)) throw new Error('Invalid format');
      if (!confirm(`将导入 ${data.length} 条记录，会覆盖当前数据。确定？`)) return;
      items = data;
      saveItems();
      render();
    } catch (err) {
      alert('导入失败：文件格式不正确');
    }
  };
  reader.readAsText(file);
}

// Bind export button if exists
const exportBtn = $('#exportBtn');
if (exportBtn) exportBtn.addEventListener('click', exportData);

// Bind import input if exists
const importInput = $('#importInput');
if (importInput) {
  importInput.addEventListener('change', e => {
    if (e.target.files[0]) importData(e.target.files[0]);
    e.target.value = ''; // reset so same file can be imported again
  });
}

/* --- Filters --- */
// __FILTER_VARS__

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
    if (q) {
      const searchText = SEARCHABLE.map(k => item[k] || '').join(' ').toLowerCase();
      if (!searchText.includes(q)) return false;
    }
    return true;
  });

  // __SORT_LOGIC__

  countEl.textContent = `${filtered.length}/${items.length}`;
  emptyEl.style.display = filtered.length ? 'none' : 'block';

  listEl.innerHTML = filtered.map(item => {
    // __CARD_TEMPLATE__
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

form.addEventListener('submit', e => {
  e.preventDefault();
  const fd = new FormData(form);
  const data = Object.fromEntries(fd.entries());

  if (editingId) {
    const updated = { ...items.find(b => b.id === editingId), ...data };
    saveItem(updated);
  } else {
    const newItem = { id: 'id-' + Date.now(), ...data };
    saveItem(newItem);
  }

  editor.close();
  render();
});

deleteBtn.addEventListener('click', () => {
  if (!editingId) return;
  if (!confirm('确认删除这条记录？')) return;
  deleteItemById(editingId);
  editor.close();
  render();
});

/* --- Init --- */
loadItems();
render();
