/**
 * 长期记忆 / 知识图谱 — 前端可视化
 * 使用 ECharts 力导向图
 */

// ── 全局状态 ────────────────────────────────────────────────────────────
const state = {
    chart: null,
    graphData: { nodes: [], links: [] },
    currentFilter: { type: '', relation: '', importanceMin: 0 },
    entityMap: {},  // id → entity cache
};

// ── API 封装 ────────────────────────────────────────────────────────────
const API = {
    async get(params = {}) {
        const qs = new URLSearchParams(params).toString();
        const r = await fetch('/api/graph' + (qs ? '?' + qs : ''));
        return r.json();
    },
    async stats() {
        const r = await fetch('/api/stats');
        return r.json();
    },
    async entity(id) {
        const r = await fetch('/api/entity/' + id);
        return r.json();
    },
    async path(from, to) {
        const r = await fetch('/api/path?from=' + from + '&to=' + to);
        return r.json();
    },
    async timeline(id) {
        const r = await fetch('/api/timeline/' + id);
        return r.json();
    },
    async search(q) {
        const r = await fetch('/api/search?q=' + encodeURIComponent(q));
        return r.json();
    },
    async types() {
        const r = await fetch('/api/types');
        return r.json();
    },
    async neighbors(id, params = {}) {
        const qs = new URLSearchParams(params).toString();
        const r = await fetch('/api/neighbors/' + id + '?' + qs);
        return r.json();
    },
    async taskStatus() {
        const r = await fetch('/api/task-status');
        return r.json();
    },
    async archiveStats() {
        const r = await fetch('/api/archive-stats');
        return r.json();
    },
};

// ── ECharts 图谱渲染 ────────────────────────────────────────────────────
function initChart() {
    const el = document.getElementById('graphChart');
    state.chart = echarts.init(el);
    state.chart.on('click', 'series', (params) => {
        if (params.dataType === 'node') {
            const node = params.data;
            showEntityDetail(node.id || node.name);
        }
    });
    window.addEventListener('resize', () => state.chart.resize());
}

function renderGraph(data) {
    state.graphData = data;
    const nodes = data.nodes || [];
    const links = data.links || [];

    if (nodes.length === 0) {
        document.getElementById('emptyState').style.display = 'block';
        state.chart.clear();
        return;
    }
    document.getElementById('emptyState').style.display = 'none';

    // 按类型着色的类别映射
    const typeColors = {
        person: '#1d9bf0',
        project: '#00ba7c',
        task: '#ff7a00',
        event: '#f91880',
        document: '#8b5cf6',
        org: '#ffd400',
        concept: '#8899a6',
        custom: '#8899a6',
    };
    const categories = Object.keys(typeColors).map(t => ({ name: t }));

    const chartNodes = nodes.map(n => {
        state.entityMap[n.id] = n;
        return {
            id: n.id,
            name: n.name,
            symbolSize: Math.max(20, Math.min(60, (n.importance || 0.5) * 60)),
            category: Object.keys(typeColors).includes(n.type) ? n.type : 'concept',
            itemStyle: { color: typeColors[n.type] || '#8899a6' },
            label: { show: true },
            // 自定义字段
            _type: n.type,
            _importance: n.importance,
        };
    });

    const chartLinks = links.map(l => ({
        source: l.source,
        target: l.target,
        value: l.relation,
        lineStyle: {
            width: Math.max(1, (l.weight || 1) * 2),
            curveness: 0.2,
            color: '#2f3336',
        },
        label: {
            show: true,
            formatter: l.relation,
            fontSize: 10,
            color: '#8899a6',
        },
    }));

    const option = {
        backgroundColor: '#0f1419',
        tooltip: {
            trigger: 'item',
            formatter: (p) => {
                if (p.dataType === 'node') {
                    return `<b>${p.data.name}</b><br/>类型: ${p.data._type || 'concept'}<br/>重要度: ${(p.data._importance || 0).toFixed(2)}`;
                }
                if (p.dataType === 'edge') {
                    const src = state.entityMap[p.data.source]?.name || p.data.source;
                    const tgt = state.entityMap[p.data.target]?.name || p.data.target;
                    return `${src} → ${tgt}<br/>关系: ${p.data.value}`;
                }
                return '';
            },
        },
        legend: {
            data: categories.map(c => c.name),
            textStyle: { color: '#8899a6' },
            bottom: 10,
        },
        series: [{
            type: 'graph',
            layout: 'force',
            roam: true,           // 可缩放/拖拽画布
            draggable: true,      // 节点可拖拽
            focusNodeAdjacency: true,
            categories: categories.map(c => ({ name: c.name, itemStyle: { color: typeColors[c.name] || '#8899a6' } })),
            data: chartNodes,
            links: chartLinks,
            force: {
                repulsion: 300,
                edgeLength: [80, 200],
                gravity: 0.1,
            },
            label: {
                show: true,
                position: 'bottom',
                color: '#e7e9ea',
                fontSize: 12,
            },
            lineStyle: {
                color: '#2f3336',
                curveness: 0.2,
            },
            emphasis: {
                focus: 'adjacency',
                lineStyle: { width: 4 },
            },
        }],
    };

    state.chart.setOption(option, true);
}

// ── 加载图谱数据 ─────────────────────────────────────────────────────────
async function loadGraph(params = {}) {
    try {
        const data = await API.get({ ...state.currentFilter, ...params });
        if (data.error && data.total === 0) {
            document.getElementById('emptyState').style.display = 'block';
            state.chart.clear();
            return;
        }
        renderGraph(data);
    } catch (e) {
        console.error('加载图谱失败:', e);
    }
}

// ── 实体详情 ─────────────────────────────────────────────────────────────
async function showEntityDetail(idOrName) {
    let entityId = idOrName;
    // 如果是名称，先搜索
    if (typeof idOrName === 'string' && isNaN(Number(idOrName))) {
        const searchRes = await API.search(idOrName);
        if (searchRes.results && searchRes.results.length > 0) {
            entityId = searchRes.results[0].id;
        } else {
            alert('未找到该实体');
            return;
        }
    }

    try {
        const e = await API.entity(entityId);
        if (e.error) { alert(e.error); return; }
        renderEntityDetail(e);
    } catch (err) {
        console.error('加载实体详情失败:', err);
    }
}

function renderEntityDetail(e) {
    const container = document.getElementById('detailContent');
    document.getElementById('detailTitle').textContent = e.name;

    let html = `
        <div class="entity-name">${e.name}</div>
        <span class="entity-type">${e.type}</span>
    `;

    // 属性
    if (e.facts && e.facts.length > 0) {
        html += '<div class="section-title">📋 属性</div>';
        for (const f of e.facts) {
            html += `<div class="fact-item"><span class="fact-predicate">${f.predicate}</span>${f.value}</div>`;
        }
    }

    // 关系
    if (e.relations && e.relations.length > 0) {
        html += '<div class="section-title">🔗 关联</div>';
        for (const r of e.relations) {
            const isOut = r.from && r.from !== e.id;
            const other = isOut ? (r.from_name || r.to_name) : (r.to_name || r.from_name);
            const dir = isOut ? '←' : '→';
            html += `<div class="relation-item">${dir} <span class="relation-target" onclick="showEntityDetail(${r.from_id === e.id ? r.to_id : r.from_id})">${other}</span> (${r.relation})</div>`;
        }
    }

    // 时间线按钮
    html += `<div class="section-title">📅 操作</div>`;
    html += `<span class="btn-timeline" onclick="showTimeline(${e.id})">查看时间线</span>`;

    container.innerHTML = html;
}

// ── 模态框控制 ─────────────────────────────────────────────────────────────
function openModal(id) {
    document.getElementById(id).style.display = 'flex';
}
function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

// ── 时间线 ─────────────────────────────────────────────────────────────
async function showTimeline(id) {
    try {
        const data = await API.timeline(id);
        const body = document.getElementById('timelineBody');
        document.getElementById('timelineTitle').textContent = data.entity?.name + ' — 时间线';
        if (data.events && data.events.length > 0) {
            body.innerHTML = data.events.map(ev => {
                const date = ev.date || '-';
                if (ev.type === 'fact') {
                    return `<div class="timeline-event"><span class="event-date">${date}</span><span class="event-type">属性变更</span>${ev.predicate}: ${ev.value}</div>`;
                }
                return `<div class="timeline-event"><span class="event-date">${date}</span><span class="event-type">关系建立</span>${ev.other_name} (${ev.relation})</div>`;
            }).join('');
        } else {
            body.innerHTML = '<p style="color:#8899a6;text-align:center;">暂无时间线数据</p>';
        }
        openModal('timelineModal');
    } catch (e) {
        console.error('时间线加载失败:', e);
    }
}

// ── 路径查找 ─────────────────────────────────────────────────────────────
async function findPath() {
    const from = document.getElementById('pathFrom').value.trim();
    const to = document.getElementById('pathTo').value.trim();
    if (!from || !to) { alert('请输入起点和终点实体'); return; }

    const resolveId = async (nameOrId) => {
        if (!isNaN(Number(nameOrId))) return Number(nameOrId);
        const r = await API.search(nameOrId);
        return r.results?.[0]?.id;
    };

    try {
        const fromId = await resolveId(from);
        const toId = await resolveId(to);
        if (!fromId || !toId) { alert('实体未找到'); return; }

        const result = await API.path(fromId, toId);
        const body = document.getElementById('pathBody');
        if (!result.path || result.path.length === 0) {
            body.innerHTML = '<p style="color:#8899a6;text-align:center;">未找到关联路径</p>';
        } else {
            let html = '';
            for (let i = 0; i < result.path.length; i++) {
                const step = result.path[i];
                if (i > 0) html += '<span class="path-arrow"> → </span>';
                html += `<span class="path-step">${step.to_name || step.to}</span>`;
                html += `<br/><span class="path-relation">　${step.relation}　</span>`;
            }
            body.innerHTML = '<div style="line-height:2;">' + html + '</div>';
        }
        openModal('pathModal');
    } catch (e) {
        console.error('路径查找失败:', e);
    }
}

// ── 搜索 ─────────────────────────────────────────────────────────────
async function doSearch() {
    const q = document.getElementById('searchInput').value.trim();
    if (!q) { loadGraph(); return; }
    try {
        const r = await API.search(q);
        if (r.results && r.results.length > 0) {
            if (r.results.length === 1) {
                showEntityDetail(r.results[0].id);
                loadGraph(); // 高亮？
            } else {
                // 显示搜索结果为节点列表
                const nodeIds = r.results.map(e => e.id);
                loadGraph().then(() => {
                    // 在已渲染的图上高亮搜索结果（通过过滤实现）
                });
                alert(`找到 ${r.count} 个实体:\n` + r.results.map(e => `  [${e.type}] ${e.name}`).join('\n'));
            }
        } else {
            alert('未找到匹配实体');
        }
    } catch (e) {
        console.error('搜索失败:', e);
    }
}

// ── 过滤 ─────────────────────────────────────────────────────────────
async function applyFilter() {
    const type = document.getElementById('filterType').value;
    const relation = document.getElementById('filterRelation').value;
    const importance = parseFloat(document.getElementById('filterImportance').value);
    state.currentFilter = {
        type,
        relation,
        importanceMin: importance,
    };
    await loadGraph();
}

// ── 填充过滤选项 ─────────────────────────────────────────────────────────
async function fillFilterOptions() {
    // 类型
    const typesEl = document.getElementById('filterType');
    try {
        const t = await API.types();
        if (t.types) {
            t.types.forEach(ty => {
                const opt = document.createElement('option');
                opt.value = ty; opt.textContent = ty;
                typesEl.appendChild(opt);
            });
        }
    } catch (e) {}

    // 关系类型（从统计获取）
    try {
        const s = await API.stats();
        const relEl = document.getElementById('filterRelation');
        if (s.relation_distribution) {
            Object.keys(s.relation_distribution).forEach(r => {
                const opt = document.createElement('option');
                opt.value = r; opt.textContent = `${r} (${s.relation_distribution[r]})`;
                relEl.appendChild(opt);
            });
        }
        fillStatsPanel(s);
    } catch (e) {}
}

function fillStatsPanel(s) {
    const panel = document.getElementById('statsPanel');
    panel.innerHTML = `
        <div style="margin-bottom:12px;">
            <div style="font-size:24px;font-weight:600;color:#1d9bf0;">${s.entities_total}</div>
            <div style="font-size:12px;color:#8899a6;">实体数</div>
        </div>
        <div style="margin-bottom:12px;">
            <div style="font-size:24px;font-weight:600;color:#1d9bf0;">${s.relations_total}</div>
            <div style="font-size:12px;color:#8899a6;">关系数</div>
        </div>
        <div>
            <div style="font-size:24px;font-weight:600;color:#1d9bf0;">${s.memories_total}</div>
            <div style="font-size:12px;color:#8899a6;">记忆数</div>
        </div>
    `;
}

// ── 统计模态框 ─────────────────────────────────────────────────────────
async function showStatsModal() {
    try {
        const s = await API.stats();
        const body = document.getElementById('statsBody');
        let html = '<div class="stats-grid">';
        html += `<div class="stats-card"><div class="number">${s.entities_total}</div><div class="label">实体数</div></div>`;
        html += `<div class="stats-card"><div class="number">${s.relations_total}</div><div class="label">关系数</div></div>`;
        html += `<div class="stats-card"><div class="number">${s.memories_total}</div><div class="label">记忆数</div></div>`;
        html += '</div>';
        if (s.type_distribution) {
            html += '<h4 style="margin:16px 0 8px;font-size:13px;color:#8899a6;">实体类型分布</h4>';
            for (const [t, c] of Object.entries(s.type_distribution)) {
                html += `<div style="font-size:13px;padding:4px 0;">${t}: <b>${c}</b></div>`;
            }
        }
        body.innerHTML = html;
        openModal('statsModal');
    } catch (e) {
        console.error('统计加载失败:', e);
    }
}

// ── 导出图谱 ─────────────────────────────────────────────────────────────
async function exportGraph() {
    try {
        const data = await API.get({ limit: 5000 });
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'zwjh_graph_' + new Date().toISOString().slice(0,10) + '.json';
        a.click();
        URL.revokeObjectURL(url);
    } catch (e) {
        console.error('导出失败:', e);
    }
}

// ── 初始化事件绑定 ─────────────────────────────────────────────────────
function bindEvents() {
    document.getElementById('searchBtn').onclick = doSearch;
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') doSearch();
    });
    document.getElementById('btnRefresh').onclick = () => loadGraph();
    document.getElementById('btnStats').onclick = showStatsModal;
    document.getElementById('btnExport').onclick = exportGraph;
    document.getElementById('btnApplyFilter').onclick = applyFilter;
    document.getElementById('btnFindPath').onclick = findPath;
    document.getElementById('btnCloseDetail').onclick = () => {
        document.getElementById('detailContent').innerHTML = '<p class="placeholder">点击图谱中的节点查看详情</p>';
    };
    document.getElementById('btnCloseTimeline').onclick = () => closeModal('timelineModal');
    document.getElementById('btnClosePath').onclick = () => closeModal('pathModal');
    document.getElementById('btnCloseStats').onclick = () => closeModal('statsModal');

    // 点击模态框背景关闭
    ['timelineModal', 'pathModal', 'statsModal'].forEach(id => {
        document.getElementById(id).addEventListener('click', function(e) {
            if (e.target === this) closeModal(id);
        });
    });

    // 重要度滑块
    document.getElementById('filterImportance').addEventListener('input', (e) => {
        document.getElementById('importanceValue').textContent = parseFloat(e.target).value.toFixed(1);
    });

    // detail 面板中点击实体名称 → 跳转
    document.getElementById('detailContent').addEventListener('click', (e) => {
        if (e.target.classList.contains('relation-target')) {
            const id = parseInt(e.target.getAttribute('onclick').match(/\d+/)?.[0]);
            if (id) showEntityDetail(id);
        }
    });
}

// ── 任务状态面板 ─────────────────────────────────────────────────────
async function loadTaskStatus() {
    try {
        const data = await API.taskStatus();
        // 定时任务状态
        const setupEl = document.getElementById('setupStatus');
        if (data.setup && data.setup.ok) {
            setupEl.innerHTML = `<span class="ok">✅ 已注册</span><br/>${data.setup.output || ''}`;
        } else {
            setupEl.innerHTML = `<span class="warn">⚠️ 未注册</span><br/>${data.setup && data.setup.error ? data.setup.error : '运行 setup 命令注册'}`;
        }
        // 健康度
        const healthEl = document.getElementById('healthStatus');
        if (data.health) {
            const score = data.health.score || 0;
            const scoreClass = score >= 80 ? 'ok' : score >= 60 ? 'warn' : 'err';
            healthEl.innerHTML = `<span class="${scoreClass}">${score} / 100</span> (${data.health.tier}档)<br/>记忆 ${data.health.memories} · 实体 ${data.health.entities} · 关系 ${data.health.relations}`;
        }
        // 归档统计
        const archiveEl = document.getElementById('archiveStatus');
        if (data.archive && data.archive.total_archived > 0) {
            archiveEl.innerHTML = `已归档 ${data.archive.total_archived} 条<br/>热 ${data.archive.by_tier.hot} / 温 ${data.archive.by_tier.warm} / 冷 ${data.archive.by_tier.cold}<br/>节省 ${data.archive.saving_percent}%`;
        } else {
            archiveEl.innerHTML = '暂无归档数据';
        }
    } catch (e) {
        console.error('任务状态加载失败:', e);
    }
}

function toggleTaskStatus() {
    const panel = document.getElementById('taskStatusPanel');
    const btn = document.getElementById('btnToggleTaskStatus');
    panel.classList.toggle('collapsed');
    btn.textContent = panel.classList.contains('collapsed') ? '展开' : '收起';
}

// ── 启动 ─────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
    initChart();
    bindEvents();
    await fillFilterOptions();
    await loadGraph();
    await loadTaskStatus();
    // 绑定任务状态面板折叠
    document.getElementById('btnToggleTaskStatus').onclick = toggleTaskStatus;
});
