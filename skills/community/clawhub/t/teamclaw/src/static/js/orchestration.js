// ── Orchestration State ──
const orch = {
    experts: [],
    nodes: [],
    edges: [],
    groups: [],
    selectedNodes: new Set(),
    nid: 1, eid: 1, gid: 1,
    dragging: null,
    connecting: null,
    selecting: null,
    contextMenu: null,
    sessionStatuses: {},
    // Zoom & pan state
    zoom: 1,
    panX: 0,
    panY: 0,
};

// ── Zoom / Pan helpers ──
function orchApplyTransform() {
    const inner = document.getElementById('orch-canvas-inner');
    if (inner) inner.style.transform = `translate(${orch.panX}px, ${orch.panY}px) scale(${orch.zoom})`;
    document.getElementById('orch-zoom-label').textContent = Math.round(orch.zoom * 100) + '%';
}
function orchZoom(delta) {
    orch.zoom = Math.min(3, Math.max(0.15, orch.zoom + delta));
    orchApplyTransform();
}
function orchPanBy(dx, dy) {
    orch.panX += dx; orch.panY += dy;
    orchApplyTransform();
}
function orchResetView() {
    orch.zoom = 1; orch.panX = 0; orch.panY = 0;
    orchApplyTransform();
}
/** Convert page-level clientX/Y to canvas-inner coordinates (accounting for zoom+pan) */
function orchClientToCanvas(clientX, clientY) {
    const area = document.getElementById('orch-canvas-area');
    const rect = area.getBoundingClientRect();
    return {
        x: (clientX - rect.left - orch.panX) / orch.zoom,
        y: (clientY - rect.top  - orch.panY) / orch.zoom,
    };
}

function orchInit() {
    orchLoadExperts();
    orchLoadSessionAgents();
    orchLoadOpenClawSessions();
    orchSetupCanvas();
    orchSetupSettings();
    orchSetupFileDrop();
    // Bind manual injection card events (dragstart + dblclick)
    const mc = document.getElementById('orch-manual-card');
    if (mc) {
        mc.addEventListener('dragstart', e => {
            e.dataTransfer.setData('application/json', JSON.stringify({type:'manual', name:t('orch_manual_inject'), tag:'manual', emoji:'📝', temperature:0}));
            e.dataTransfer.effectAllowed = 'copy';
        });
        mc.addEventListener('dblclick', () => orchAddNodeCenter({type:'manual', name:t('orch_manual_inject'), tag:'manual', emoji:'📝', temperature:0}));
    }
}

// ── Load experts (public + custom) ──
async function orchLoadExperts() {
    try {
        const r = await fetch('/proxy_visual/experts');
        orch.experts = await r.json();
    } catch(e) { console.error('Load experts failed:', e); }
    orchRenderExpertSidebar();
}

function orchRenderExpertSidebar() {
    const pubList = document.getElementById('orch-expert-list-public');
    const custList = document.getElementById('orch-expert-list-custom');
    pubList.innerHTML = '';
    custList.innerHTML = '';

    orch.experts.forEach(exp => {
        const card = document.createElement('div');
        card.className = 'orch-expert-card';
        card.draggable = true;
        const isCustom = exp.source === 'custom';
        card.innerHTML = `<span class="orch-emoji">${exp.emoji}</span><div style="min-width:0;flex:1;"><div class="orch-name" title="${escapeHtml(exp.name)}">${escapeHtml(exp.name)}</div><div class="orch-tag">${escapeHtml(exp.tag)}</div></div><span class="orch-temp">${exp.temperature||''}</span>${isCustom ? '<button class="orch-expert-del-btn" title="' + t('orch_ctx_delete') + '" style="font-size:10px;background:none;border:none;cursor:pointer;color:#dc2626;padding:0 2px;margin-left:2px;">✕</button>' : ''}`;
        card.addEventListener('dragstart', e => {
            e.dataTransfer.setData('application/json', JSON.stringify({type:'expert', ...exp}));
            e.dataTransfer.effectAllowed = 'copy';
        });
        card.addEventListener('dblclick', () => orchAddNodeCenter({type:'expert', ...exp}));
        if (isCustom) {
            card.querySelector('.orch-expert-del-btn').addEventListener('click', async (ev) => {
                ev.stopPropagation();
                if (!confirm(t('orch_confirm_del_expert', {name: exp.name}))) return;
                try {
                    await fetch('/proxy_visual/experts/custom/' + encodeURIComponent(exp.tag), { method: 'DELETE' });
                    orchToast(t('orch_toast_expert_deleted', {name: exp.name}));
                    orchLoadExperts();
                } catch(e) { orchToast(t('orch_toast_expert_del_fail')); }
            });
            custList.appendChild(card);
        } else {
            pubList.appendChild(card);
        }
    });

    if (!custList.children.length) {
        custList.innerHTML = '<div style="padding:6px 10px;font-size:10px;color:#d1d5db;text-align:center;">' + t('orch_no_custom') + '</div>';
    }
}

// ── Load session agents ──
async function orchLoadSessionAgents() {
    const list = document.getElementById('orch-expert-list-sessions');
    list.innerHTML = '<div style="padding:6px 10px;font-size:10px;color:#9ca3af;text-align:center;">' + t('orch_modal_loading') + '</div>';
    try {
        const resp = await fetch('/proxy_sessions');
        const data = await resp.json();
        list.innerHTML = '';
        if (!data.sessions || data.sessions.length === 0) {
            list.innerHTML = '<div style="padding:6px 10px;font-size:10px;color:#d1d5db;text-align:center;">' + t('orch_no_session') + '</div>';
            return;
        }
        data.sessions.sort((a, b) => b.session_id.localeCompare(a.session_id));
        for (const s of data.sessions) {
            const card = document.createElement('div');
            card.className = 'orch-expert-card';
            card.draggable = true;
            const title = s.title || 'Untitled';
            card.innerHTML = `<span class="orch-emoji">🤖</span><div style="min-width:0;flex:1;"><div class="orch-name" title="${escapeHtml(title)}">${escapeHtml(title)}</div><div class="orch-tag" style="color:#6366f1;font-family:monospace;">#${s.session_id.slice(-8)}</div></div><span class="orch-temp" style="font-size:9px;color:#9ca3af;">${s.message_count||0}msg</span>`;
            const sessionData = {type:'session_agent', name: title, tag: 'session', emoji:'🤖', temperature: 0.7, session_id: s.session_id};
            card.addEventListener('dragstart', e => {
                e.dataTransfer.setData('application/json', JSON.stringify(sessionData));
                e.dataTransfer.effectAllowed = 'copy';
            });
            card.addEventListener('dblclick', () => orchAddNodeCenter(sessionData));
            list.appendChild(card);
        }
    } catch(e) {
        list.innerHTML = '<div style="padding:6px 10px;font-size:10px;color:#dc2626;text-align:center;">' + t('orch_load_fail') + '</div>';
    }
}

// ── Load OpenClaw sessions ──
async function orchLoadOpenClawSessions() {
    const list = document.getElementById('orch-expert-list-openclaw');
    if (!list) return;
    list.innerHTML = '<div style="padding:6px 10px;font-size:10px;color:#9ca3af;text-align:center;">⏳ ' + t('loading') + '</div>';
    try {
        const resp = await fetch('/proxy_openclaw_sessions');
        const data = await resp.json();
        list.innerHTML = '';
        if (!data.available) {
            list.innerHTML = '<div style="padding:6px 10px;font-size:10px;color:#d1d5db;text-align:center;">🚫 Not configured</div>';
            return;
        }
        if (!data.sessions || data.sessions.length === 0) {
            list.innerHTML = '<div style="padding:6px 10px;font-size:10px;color:#d1d5db;text-align:center;">No OpenClaw sessions</div>';
            return;
        }
        const openclawUrl = data.openclaw_api_url || '';
        const openclawKey = data.openclaw_api_key || '';
        for (const s of data.sessions) {
            const card = document.createElement('div');
            card.className = 'orch-expert-card';
            card.draggable = true;
            const title = s.key || 'Untitled';
            const chan = (s.channel && s.channel !== 'unknown' && s.channel !== 'auto') ? s.channel : '';
            const mdl = (s.model && s.model !== 'unknown' && s.model !== 'auto') ? s.model : '';
            const tagParts = [chan, mdl].filter(Boolean).join(' · ');
            card.innerHTML = `<span class="orch-emoji">🦞</span><div style="min-width:0;flex:1;"><div class="orch-name" title="${escapeHtml(title)}">${escapeHtml(title)}</div>${tagParts ? '<div class="orch-tag" style="color:#10b981;font-family:monospace;">' + escapeHtml(tagParts) + '</div>' : ''}</div><span class="orch-temp" style="font-size:9px;color:#9ca3af;">${s.contextTokens||0}tk</span>`;
            // s.key is already in full format like "agent:main:sessionName"
            const sessionKey = s.key || 'default';
            const modelStr = sessionKey.startsWith('agent:') ? sessionKey : ('agent:main:' + sessionKey);
            const nodeData = {
                type: 'external', name: title, tag: 'openclaw', emoji: '🦞', temperature: 0.7,
                api_url: openclawUrl, api_key: openclawKey,
                model: modelStr,
                headers: {'x-openclaw-session-key': sessionKey}, ext_id: sessionKey,
                openclaw_session: s
            };
            card.addEventListener('dragstart', e => {
                e.dataTransfer.setData('application/json', JSON.stringify(nodeData));
                e.dataTransfer.effectAllowed = 'copy';
            });
            card.addEventListener('dblclick', () => orchAddNodeCenter(nodeData));
            list.appendChild(card);
        }
    } catch(e) {
        list.innerHTML = '<div style="padding:6px 10px;font-size:10px;color:#dc2626;text-align:center;">❌ ' + t('error') + '</div>';
    }
}

// ── Add custom expert modal ──
function orchShowAddExpertModal() {
    const overlay = document.createElement('div');
    overlay.className = 'orch-modal-overlay';
    overlay.id = 'orch-add-expert-overlay';
    overlay.innerHTML = `
        <div class="orch-modal" style="min-width:380px;max-width:460px;">
            <h3>${t('orch_add_expert_title')}</h3>
            <div style="display:flex;flex-direction:column;gap:8px;margin:10px 0;">
                <label style="font-size:11px;font-weight:600;color:#374151;">${t('orch_label_name')} <input id="orch-ce-name" type="text" placeholder="${t('orch_ph_name')}" style="width:100%;padding:6px 8px;border:1px solid #d1d5db;border-radius:6px;font-size:12px;margin-top:2px;"></label>
                <label style="font-size:11px;font-weight:600;color:#374151;">${t('orch_label_tag')} <input id="orch-ce-tag" type="text" placeholder="${t('orch_ph_tag')}" style="width:100%;padding:6px 8px;border:1px solid #d1d5db;border-radius:6px;font-size:12px;margin-top:2px;"></label>
                <label style="font-size:11px;font-weight:600;color:#374151;">${t('orch_label_temp')} <input id="orch-ce-temp" type="number" value="0.7" min="0" max="2" step="0.1" style="width:80px;padding:6px 8px;border:1px solid #d1d5db;border-radius:6px;font-size:12px;margin-top:2px;"></label>
                <label style="font-size:11px;font-weight:600;color:#374151;">${t('orch_label_persona')}
                    <textarea id="orch-ce-persona" rows="4" placeholder="${t('orch_ph_persona')}" style="width:100%;padding:6px 8px;border:1px solid #d1d5db;border-radius:6px;font-size:12px;margin-top:2px;resize:vertical;"></textarea>
                </label>
            </div>
            <div class="orch-modal-btns">
                <button id="orch-ce-cancel" style="padding:6px 14px;border-radius:6px;border:1px solid #d1d5db;background:white;color:#374151;cursor:pointer;font-size:12px;">${t('orch_modal_cancel')}</button>
                <button id="orch-ce-save" style="padding:6px 14px;border-radius:6px;border:none;background:#2563eb;color:white;cursor:pointer;font-size:12px;">${t('orch_modal_save')}</button>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);
    overlay.querySelector('#orch-ce-cancel').addEventListener('click', () => overlay.remove());
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
    overlay.querySelector('#orch-ce-save').addEventListener('click', async () => {
        const name = document.getElementById('orch-ce-name').value.trim();
        const tag = document.getElementById('orch-ce-tag').value.trim();
        const temperature = parseFloat(document.getElementById('orch-ce-temp').value) || 0.7;
        const persona = document.getElementById('orch-ce-persona').value.trim();
        if (!name || !tag || !persona) { orchToast(t('orch_toast_fill_info')); return; }
        try {
            const r = await fetch('/proxy_visual/experts/custom', {
                method: 'POST', headers: {'Content-Type':'application/json'},
                body: JSON.stringify({name, tag, temperature, persona}),
            });
            const res = await r.json();
            if (r.ok) {
                orchToast(t('orch_toast_custom_added', {name}));
                overlay.remove();
                orchLoadExperts();
            } else {
                orchToast(t('orch_toast_load_fail') + ': ' + (res.detail || res.error || ''));
            }
        } catch(e) { orchToast(t('orch_toast_net_error')); }
    });
}

function orchRenderSidebar() {
    orchRenderExpertSidebar();
    // Manual card
    const mc = document.getElementById('orch-manual-card');
    mc.addEventListener('dragstart', e => {
        e.dataTransfer.setData('application/json', JSON.stringify({type:'manual', name:t('orch_manual_inject'), tag:'manual', emoji:'📝', temperature:0}));
        e.dataTransfer.effectAllowed = 'copy';
    });
    mc.addEventListener('dblclick', () => orchAddNodeCenter({type:'manual', name:t('orch_manual_inject'), tag:'manual', emoji:'📝', temperature:0}));
}

// ── Settings ──
function orchSetupSettings() {
    document.getElementById('orch-threshold').addEventListener('input', e => {
        document.getElementById('orch-threshold-val').textContent = e.target.value;
    });
}
function orchGetSettings() {
    return {
        repeat: document.getElementById('orch-repeat').checked,
        max_rounds: parseInt(document.getElementById('orch-rounds').value) || 5,
        use_bot_session: document.getElementById('orch-bot-session').checked,
        cluster_threshold: parseInt(document.getElementById('orch-threshold').value) || 150,
    };
}

// ── Node Management ──
function orchNextInstance(data) {
    // Compute next instance number for this agent identity
    const key = data.type === 'session_agent' ? ('sa:' + (data.session_id||'')) : data.type === 'external' ? ('ext:' + (data.ext_id || data.tag||'custom')) : ('ex:' + (data.tag||'custom'));
    let maxInst = 0;
    orch.nodes.forEach(n => {
        const nk = n.type === 'session_agent' ? ('sa:' + (n.session_id||'')) : n.type === 'external' ? ('ext:' + (n.ext_id || n.tag||'custom')) : ('ex:' + (n.tag||'custom'));
        if (nk === key && n.instance > maxInst) maxInst = n.instance;
    });
    return maxInst + 1;
}

function orchAddNode(data, x, y) {
    const id = 'on' + orch.nid++;
    const inst = data.instance || orchNextInstance(data);
    const node = { id, name: data.name, tag: data.tag||'custom', emoji: data.emoji||'⭐', x: Math.round(x), y: Math.round(y), type: data.type||'expert', temperature: data.temperature||0.5, author: data.author||t('orch_default_author'), content: data.content||'', session_id: data.session_id||'', source: data.source||'', instance: inst };
    // Preserve external agent extra fields
    if (data.type === 'external') {
        node.api_url = data.api_url || '';
        node.ext_id = data.ext_id || '1';
        if (data.headers && typeof data.headers === 'object') node.headers = data.headers;
        if (data.api_key) node.api_key = data.api_key;
        if (data.model) node.model = data.model;
    }
    orch.nodes.push(node);
    orchRenderNode(node);
    orchUpdateYaml();
    orchUpdateStatus();
    document.getElementById('orch-canvas-hint').style.display = 'none';
    return node;
}

function orchAddNodeCenter(data) {
    const area = document.getElementById('orch-canvas-area');
    const cx = (area.offsetWidth / 2 - orch.panX) / orch.zoom - 60;
    const cy = (area.offsetHeight / 2 - orch.panY) / orch.zoom - 20;
    const n = orch.nodes.length;
    const angle = n * 137.5 * Math.PI / 180;
    const radius = 80 * Math.sqrt(n) * 0.5;
    return orchAddNode(data, cx + radius * Math.cos(angle), cy + radius * Math.sin(angle));
}

function orchRenderNode(node) {
    const area = document.getElementById('orch-canvas-inner');
    const el = document.createElement('div');
    const isSession = node.type === 'session_agent';
    const isExternal = node.type === 'external';
    el.className = 'orch-node' + (node.type === 'manual' ? ' manual-type' : '') + (isSession ? ' session-type' : '') + (isExternal ? ' external-type' : '');
    el.id = 'onode-' + node.id;
    el.style.left = node.x + 'px';
    el.style.top = node.y + 'px';
    if (isSession) el.style.borderColor = '#6366f1';
    if (isExternal) el.style.borderColor = '#2ecc71';

    const status = orch.sessionStatuses[node.tag] || orch.sessionStatuses[node.name] || 'idle';
    const instBadge = `<span style="display:inline-block;background:#2563eb;color:#fff;font-size:9px;font-weight:700;border-radius:50%;min-width:16px;height:16px;line-height:16px;text-align:center;margin-left:3px;flex-shrink:0;">${node.instance||1}</span>`;
    let tagLine;
    if (isSession) {
        tagLine = `<div class="orch-node-tag" style="color:#6366f1;font-family:monospace;">#${(node.session_id||'').slice(-8)}</div>`;
    } else if (isExternal) {
        let extDesc = '';
        if (node.api_url) {
            extDesc = `🌐 ${node.api_url}`;
            if (node.model) extDesc += '\n📦 ' + node.model;
        } else {
            extDesc = '⚠️ Double-click to set URL';
        }
        if (node.headers && typeof node.headers === 'object') {
            const hdrParts = Object.entries(node.headers).map(([k,v]) => `${k}: ${v}`);
            if (hdrParts.length) extDesc += '\n' + hdrParts.join('\n');
        }
        tagLine = `<div class="orch-node-tag" style="color:#2ecc71;white-space:pre-line;word-break:break-all;font-size:9px;">${escapeHtml(extDesc)}</div>`;
    } else {
        tagLine = `<div class="orch-node-tag">${escapeHtml(node.tag)}</div>`;
    }
    el.innerHTML = `
        <span class="orch-node-emoji">${node.emoji}</span>
        <div style="min-width:0;flex:1;"><div class="orch-node-name" style="display:flex;align-items:center;">${escapeHtml(node.name)}${instBadge}</div>${tagLine}</div>
        <div class="orch-node-del" title="${t('orch_node_remove')}">×</div>
        <div class="orch-port port-in" data-node="${node.id}" data-dir="in"></div>
        <div class="orch-port port-out" data-node="${node.id}" data-dir="out"></div>
        <div class="orch-node-status ${status}"></div>
    `;

    el.querySelector('.orch-node-del').addEventListener('click', e => { e.stopPropagation(); orchRemoveNode(node.id); });

    el.addEventListener('mousedown', e => {
        if (e.target.classList.contains('orch-port') || e.target.classList.contains('orch-node-del')) return;
        e.stopPropagation();
        if (!e.shiftKey && !orch.selectedNodes.has(node.id)) orchClearSelection();
        orchSelectNode(node.id);
        const cp = orchClientToCanvas(e.clientX, e.clientY);
        orch.dragging = { nodeId: node.id, offX: cp.x - node.x, offY: cp.y - node.y, multi: orch.selectedNodes.size > 1, starts: {} };
        if (orch.selectedNodes.size > 1) {
            orch.selectedNodes.forEach(nid => { const n = orch.nodes.find(nn=>nn.id===nid); if(n) orch.dragging.starts[nid]={x:n.x,y:n.y}; });
        }
    });

    el.querySelectorAll('.orch-port').forEach(port => {
        port.addEventListener('mousedown', e => {
            e.stopPropagation();
            if (port.dataset.dir === 'out') {
                const portRect = port.getBoundingClientRect();
                const cp = orchClientToCanvas(portRect.left + 5, portRect.top + 5);
                orch.connecting = { sourceId: node.id, sx: cp.x, sy: cp.y };
            }
        });
        port.addEventListener('mouseup', e => {
            e.stopPropagation();
            if (orch.connecting && port.dataset.dir === 'in' && port.dataset.node !== orch.connecting.sourceId) {
                orchAddEdge(orch.connecting.sourceId, node.id);
            }
            orch.connecting = null;
            orchRemoveTempLine();
        });
    });

    el.addEventListener('contextmenu', e => {
        e.preventDefault(); e.stopPropagation();
        if (!orch.selectedNodes.has(node.id)) { orchClearSelection(); orchSelectNode(node.id); }
        orchShowContextMenu(e.clientX, e.clientY, node);
    });
    el.addEventListener('dblclick', () => { if (node.type === 'manual') orchShowManualModal(node); else if (node.type === 'external') orchShowExternalModal(node); });
    area.appendChild(el);
}

function orchRemoveNode(id) {
    orch.nodes = orch.nodes.filter(n => n.id !== id);
    orch.edges = orch.edges.filter(e => e.source !== id && e.target !== id);
    orch.selectedNodes.delete(id);
    orch.groups.forEach(g => { g.nodeIds = g.nodeIds.filter(nid => nid !== id); });
    const el = document.getElementById('onode-' + id);
    if (el) el.remove();
    orchRenderEdges();
    orchUpdateYaml();
    orchUpdateStatus();
    if (orch.nodes.length === 0) document.getElementById('orch-canvas-hint').style.display = '';
}

function orchSelectNode(id) { orch.selectedNodes.add(id); const el=document.getElementById('onode-'+id); if(el) el.classList.add('selected'); }
function orchClearSelection() { orch.selectedNodes.forEach(id => { const el=document.getElementById('onode-'+id); if(el) el.classList.remove('selected'); }); orch.selectedNodes.clear(); }

// ── Edge Management ──
function orchAddEdge(src, tgt) {
    if (orch.edges.some(e => e.source === src && e.target === tgt)) return;
    orch.edges.push({ id: 'oe' + orch.eid++, source: src, target: tgt });
    orchRenderEdges();
    orchUpdateYaml();
}

function orchRenderEdges() {
    const svg = document.getElementById('orch-edge-svg');
    const defs = svg.querySelector('defs');
    svg.innerHTML = '';
    svg.appendChild(defs);
    orch.edges.forEach(edge => {
        const sn = orch.nodes.find(n => n.id === edge.source);
        const tn = orch.nodes.find(n => n.id === edge.target);
        if (!sn || !tn) return;
        const se = document.getElementById('onode-' + edge.source);
        const te = document.getElementById('onode-' + edge.target);
        if (!se || !te) return;
        const x1 = sn.x + se.offsetWidth, y1 = sn.y + se.offsetHeight/2;
        const x2 = tn.x, y2 = tn.y + te.offsetHeight/2;
        const cpx = (x1+x2)/2;
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', `M${x1},${y1} C${cpx},${y1} ${cpx},${y2} ${x2},${y2}`);
        path.setAttribute('stroke', '#2563eb');
        path.setAttribute('stroke-width', '2');
        path.setAttribute('fill', 'none');
        path.setAttribute('marker-end', 'url(#orch-arrowhead)');
        path.style.cursor = 'pointer';
        path.style.pointerEvents = 'all';
        path.addEventListener('click', e => { e.stopPropagation(); orch.edges = orch.edges.filter(ee=>ee.id!==edge.id); orchRenderEdges(); orchUpdateYaml(); });
        path.addEventListener('mouseenter', () => { path.setAttribute('stroke','#ef4444'); path.setAttribute('stroke-width','3'); });
        path.addEventListener('mouseleave', () => { path.setAttribute('stroke','#2563eb'); path.setAttribute('stroke-width','2'); });
        svg.appendChild(path);
    });
}

function orchRemoveTempLine() { const svg=document.getElementById('orch-edge-svg'); const t=svg.querySelector('.temp-line'); if(t)t.remove(); }
function orchDrawTempLine(x1,y1,x2,y2) {
    const svg=document.getElementById('orch-edge-svg'); orchRemoveTempLine();
    const line=document.createElementNS('http://www.w3.org/2000/svg','line');
    line.classList.add('temp-line');
    line.setAttribute('x1',x1); line.setAttribute('y1',y1); line.setAttribute('x2',x2); line.setAttribute('y2',y2);
    line.setAttribute('stroke','#2563eb80'); line.setAttribute('stroke-width','2'); line.setAttribute('stroke-dasharray','5,5');
    line.style.pointerEvents = 'none';
    svg.appendChild(line);
}

// ── Group Management ──
function orchCreateGroup(type) {
    if (orch.selectedNodes.size < 2 && type !== 'all') { orchToast(t('orch_toast_select_2')); return; }
    const members = [...orch.selectedNodes];
    const nodes = members.map(id => orch.nodes.find(n=>n.id===id)).filter(Boolean);
    const pad = 30;
    const x = Math.min(...nodes.map(n=>n.x)) - pad;
    const y = Math.min(...nodes.map(n=>n.y)) - pad;
    const w = Math.max(...nodes.map(n=>n.x+120)) - x + pad;
    const h = Math.max(...nodes.map(n=>n.y+50)) - y + pad;
    const id = 'og' + orch.gid++;
    const labelMap = {parallel: t('orch_group_parallel'), all: t('orch_group_all')};
    const group = { id, name: labelMap[type]||type, type, x, y, w, h, nodeIds: members };
    orch.groups.push(group);
    orchRenderGroup(group);
    orchUpdateYaml();
}

function orchRenderGroup(group) {
    const area = document.getElementById('orch-canvas-inner');
    const el = document.createElement('div');
    el.className = 'orch-group ' + group.type;
    el.id = 'ogroup-' + group.id;
    el.style.cssText = `left:${group.x}px;top:${group.y}px;width:${group.w}px;height:${group.h}px;`;
    el.innerHTML = `<span class="orch-group-label">${group.name}</span><div class="orch-group-del" title="${t('orch_group_dissolve')}">×</div>`;
    el.querySelector('.orch-group-del').addEventListener('click', e => {
        e.stopPropagation();
        orch.groups = orch.groups.filter(g=>g.id!==group.id);
        el.remove();
        orchUpdateYaml();
    });
    area.appendChild(el);
}

function orchUpdateGroupBounds(group) {
    const members = orch.nodes.filter(n => group.nodeIds.includes(n.id));
    if (!members.length) return;
    const pad = 30;
    group.x = Math.min(...members.map(n=>n.x)) - pad;
    group.y = Math.min(...members.map(n=>n.y)) - pad;
    group.w = Math.max(...members.map(n=>n.x+120)) - group.x + pad;
    group.h = Math.max(...members.map(n=>n.y+50)) - group.y + pad;
    const el = document.getElementById('ogroup-' + group.id);
    if (el) { el.style.left=group.x+'px'; el.style.top=group.y+'px'; el.style.width=group.w+'px'; el.style.height=group.h+'px'; }
}

// ── Canvas Events ──
function orchSetupCanvas() {
    const canvas = document.getElementById('orch-canvas-area');

    // ── Drag-and-drop from sidebar ──
    canvas.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'copy'; });
    canvas.addEventListener('drop', e => {
        e.preventDefault();
        try {
            const data = JSON.parse(e.dataTransfer.getData('application/json'));
            const cp = orchClientToCanvas(e.clientX, e.clientY);
            orchAddNode(data, cp.x - 55, cp.y - 20);
        } catch(err) {}
    });

    // ── Mousedown: selection rect ──
    canvas.addEventListener('mousedown', e => {
        const inner = document.getElementById('orch-canvas-inner');
        if (e.target === canvas || e.target === inner || e.target.id === 'orch-canvas-hint') {
            orchClearSelection();
            const cp = orchClientToCanvas(e.clientX, e.clientY);
            orch.selecting = { sx: cp.x, sy: cp.y };
        }
    });

    // ── Mousemove: drag nodes / connect / select ──
    canvas.addEventListener('mousemove', e => {
        if (orch.dragging) {
            const d = orch.dragging;
            const cp = orchClientToCanvas(e.clientX, e.clientY);
            if (d.multi) {
                const dx = cp.x - d.offX - d.starts[d.nodeId].x;
                const dy = cp.y - d.offY - d.starts[d.nodeId].y;
                orch.selectedNodes.forEach(nid => {
                    const n = orch.nodes.find(nn=>nn.id===nid);
                    if (n && d.starts[nid]) { n.x = d.starts[nid].x + dx; n.y = d.starts[nid].y + dy; const el=document.getElementById('onode-'+nid); if(el){el.style.left=n.x+'px';el.style.top=n.y+'px';} }
                });
            } else {
                const n = orch.nodes.find(nn=>nn.id===d.nodeId);
                if (n) { n.x = cp.x - d.offX; n.y = cp.y - d.offY; const el=document.getElementById('onode-'+n.id); if(el){el.style.left=n.x+'px';el.style.top=n.y+'px';} }
            }
            orchRenderEdges();
            orch.groups.forEach(g => orchUpdateGroupBounds(g));
        } else if (orch.connecting) {
            const cp = orchClientToCanvas(e.clientX, e.clientY);
            orchDrawTempLine(orch.connecting.sx, orch.connecting.sy, cp.x, cp.y);
        } else if (orch.selecting) {
            const s = orch.selecting;
            const cp = orchClientToCanvas(e.clientX, e.clientY);
            let existing = document.querySelector('.orch-sel-rect');
            const inner = document.getElementById('orch-canvas-inner');
            if (!existing) { existing = document.createElement('div'); existing.className='orch-sel-rect'; inner.appendChild(existing); }
            const x = Math.min(s.sx, cp.x), y = Math.min(s.sy, cp.y);
            const w = Math.abs(cp.x - s.sx), h = Math.abs(cp.y - s.sy);
            existing.style.cssText = `left:${x}px;top:${y}px;width:${w}px;height:${h}px;`;
        }
    });

    // ── Mouseup ──
    canvas.addEventListener('mouseup', e => {
        if (orch.dragging) { orch.dragging = null; orchUpdateYaml(); }
        if (orch.connecting) { orch.connecting = null; orchRemoveTempLine(); }
        if (orch.selecting) {
            const s = orch.selecting;
            const cp = orchClientToCanvas(e.clientX, e.clientY);
            const x1 = Math.min(s.sx, cp.x), y1 = Math.min(s.sy, cp.y);
            const x2 = Math.max(s.sx, cp.x), y2 = Math.max(s.sy, cp.y);
            if (Math.abs(x2-x1) > 10 && Math.abs(y2-y1) > 10) {
                orch.nodes.forEach(n => { if (n.x > x1 && n.x < x2 && n.y > y1 && n.y < y2) orchSelectNode(n.id); });
            }
            orch.selecting = null;
            document.querySelectorAll('.orch-sel-rect').forEach(el => el.remove());
        }
    });

    // ── Context menu ──
    canvas.addEventListener('contextmenu', e => {
        e.preventDefault();
        orchShowContextMenu(e.clientX, e.clientY);
    });

    // ── Keyboard shortcuts ──
    document.addEventListener('keydown', e => {
        if (currentPage !== 'orchestrate') return;
        if (e.key === 'Delete' || e.key === 'Backspace') {
            if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') return;
            orch.selectedNodes.forEach(id => orchRemoveNode(id));
        }
        if ((e.ctrlKey || e.metaKey) && e.key === 'g') {
            e.preventDefault();
            if (orch.selectedNodes.size >= 2) orchCreateGroup('parallel');
        }
        if ((e.ctrlKey || e.metaKey) && e.key === 'a' && currentPage === 'orchestrate') {
            e.preventDefault();
            orch.nodes.forEach(n => orchSelectNode(n.id));
        }
        if (e.key === 'Escape') { orchClearSelection(); orchHideContextMenu(); }
    });
    document.addEventListener('keyup', e => {});
}

function orchShowContextMenu(x, y, targetNode) {
    orchHideContextMenu();
    const menu = document.createElement('div');
    menu.className = 'orch-context-menu';
    menu.id = 'orch-ctx-menu';
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';

    const hasSelection = orch.selectedNodes.size > 0;
    const items = [];

    // ── Node-specific: duplicate / set instance ──
    if (targetNode) {
        items.push({label: t('orch_ctx_duplicate'), action: () => {
            orchAddNode({...targetNode, instance: targetNode.instance}, targetNode.x + 40, targetNode.y + 40);
        }});
        items.push({label: t('orch_ctx_new_instance'), action: () => {
            orchAddNode({...targetNode, instance: undefined}, targetNode.x + 40, targetNode.y + 40);
        }});
        items.push({divider: true});
    }

    if (hasSelection && orch.selectedNodes.size >= 2) {
        items.push({label: t('orch_ctx_group_parallel'), action: () => orchCreateGroup('parallel')});
        items.push({label: t('orch_ctx_group_all'), action: () => orchCreateGroup('all')});
        items.push({divider: true});
    }
    if (hasSelection) {
        items.push({label: t('orch_ctx_delete'), action: () => { orch.selectedNodes.forEach(id => orchRemoveNode(id)); }});
    }
    items.push({label: t('orch_ctx_refresh_yaml'), action: () => orchUpdateYaml()});
    items.push({label: t('orch_ctx_clear'), action: () => orchClearCanvas()});

    items.forEach(item => {
        if (item.divider) { const d = document.createElement('div'); d.className='orch-menu-divider'; menu.appendChild(d); return; }
        const d = document.createElement('div');
        d.className = 'orch-menu-item';
        d.textContent = item.label;
        d.addEventListener('click', () => { item.action(); orchHideContextMenu(); });
        menu.appendChild(d);
    });

    document.body.appendChild(menu);
    document.addEventListener('click', orchHideContextMenu, {once: true});
}
function orchHideContextMenu() { const m = document.getElementById('orch-ctx-menu'); if(m) m.remove(); }

// ── Manual Edit Modal ──
function orchShowManualModal(node) {
    const overlay = document.createElement('div');
    overlay.className = 'orch-modal-overlay';
    overlay.id = 'orch-manual-modal';
    overlay.innerHTML = `<div class="orch-modal">
        <h3>${t('orch_modal_edit_manual')}</h3>
        <input type="text" id="orch-man-author" value="${node.author||t('orch_default_author')}" placeholder="${t('orch_modal_author_ph')}">
        <textarea id="orch-man-content" placeholder="${t('orch_modal_content_ph')}">${node.content||''}</textarea>
        <div class="orch-modal-btns">
            <button onclick="document.getElementById('orch-manual-modal').remove()">${t('orch_modal_cancel')}</button>
            <button class="primary" onclick="orchSaveManual('${node.id}')">${t('orch_modal_save')}</button>
        </div>
    </div>`;
    document.body.appendChild(overlay);
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
}
function orchSaveManual(nodeId) {
    const node = orch.nodes.find(n=>n.id===nodeId);
    if (node) {
        node.author = document.getElementById('orch-man-author').value;
        node.content = document.getElementById('orch-man-content').value;
    }
    document.getElementById('orch-manual-modal')?.remove();
    orchUpdateYaml();
}

// ── External Agent Edit Modal ──
function orchShowExternalModal(node) {
    const overlay = document.createElement('div');
    overlay.className = 'orch-modal-overlay';
    overlay.id = 'orch-external-modal';
    const hdrs = (node.headers && typeof node.headers === 'object') ? JSON.stringify(node.headers, null, 2) : '';
    overlay.innerHTML = `<div class="orch-modal" style="max-width:480px;">
        <h3>🌐 ${escapeHtml(node.name)} — External Agent</h3>
        <label style="font-size:11px;color:#9ca3af;margin-bottom:2px;display:block;">API URL *</label>
        <input type="text" id="orch-ext-url" value="${escapeHtml(node.api_url||'')}" placeholder="https://api.example.com/v1" style="font-family:monospace;font-size:12px;">
        <label style="font-size:11px;color:#9ca3af;margin-bottom:2px;margin-top:8px;display:block;">API Key</label>
        <input type="text" id="orch-ext-key" value="${escapeHtml(node.api_key||'')}" placeholder="sk-xxx (optional)" style="font-family:monospace;font-size:12px;">
        <label style="font-size:11px;color:#9ca3af;margin-bottom:2px;margin-top:8px;display:block;">Model</label>
        <input type="text" id="orch-ext-model" value="${escapeHtml(node.model||'')}" placeholder="gpt-4 / deepseek-chat (optional)" style="font-family:monospace;font-size:12px;">
        <label style="font-size:11px;color:#9ca3af;margin-bottom:2px;margin-top:8px;display:block;">Headers (JSON)</label>
        <textarea id="orch-ext-headers" placeholder='{"X-Custom": "value"}' style="font-family:monospace;font-size:11px;min-height:60px;">${escapeHtml(hdrs)}</textarea>
        <div class="orch-modal-btns">
            <button onclick="document.getElementById('orch-external-modal').remove()">${t('orch_modal_cancel')}</button>
            <button class="primary" onclick="orchSaveExternal('${node.id}')">${t('orch_modal_save')}</button>
        </div>
    </div>`;
    document.body.appendChild(overlay);
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
}
function orchSaveExternal(nodeId) {
    const node = orch.nodes.find(n=>n.id===nodeId);
    if (node) {
        node.api_url = document.getElementById('orch-ext-url').value.trim();
        node.api_key = document.getElementById('orch-ext-key').value.trim();
        node.model = document.getElementById('orch-ext-model').value.trim();
        const hdrsStr = document.getElementById('orch-ext-headers').value.trim();
        if (hdrsStr) {
            try { node.headers = JSON.parse(hdrsStr); } catch(e) { alert('Headers JSON parse error: ' + e.message); return; }
        } else {
            node.headers = {};
        }
        // Re-render node to update display
        const el = document.getElementById('onode-' + nodeId);
        if (el) el.remove();
        orchRenderNode(node);
        orchRedrawEdges();
    }
    document.getElementById('orch-external-modal')?.remove();
    orchUpdateYaml();
}

// ── Layout Data ──
function orchGetLayoutData() {
    return {
        nodes: orch.nodes.map(n => ({...n})),
        edges: orch.edges.map(e => ({...e})),
        groups: orch.groups.map(g => ({...g})),
        settings: orchGetSettings(),
        view: { zoom: orch.zoom, panX: orch.panX, panY: orch.panY },
    };
}

// ── YAML Generation (Rule-based) ──
async function orchUpdateYaml() {
    orchUpdateStatus();
    const data = orchGetLayoutData();
    if (orch.nodes.length === 0) {
        document.getElementById('orch-yaml-content').textContent = t('orch_rule_yaml_hint');
        return;
    }
    try {
        const r = await fetch('/proxy_visual/generate-yaml', {
            method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data),
        });
        const res = await r.json();
        document.getElementById('orch-yaml-content').textContent = res.yaml || '# Error: ' + (res.error || 'Unknown');
    } catch(e) {
        document.getElementById('orch-yaml-content').textContent = '# Error: ' + e.message;
    }
}

// ── AI Generate YAML (with session selection) ──
let orchTargetSessionId = null;

async function orchGenerateAgentYaml() {
    if (orch.nodes.length === 0) { orchToast(t('orch_toast_add_first')); return; }
    orchShowSessionSelectModal();
}

async function orchShowSessionSelectModal() {
    const overlay = document.createElement('div');
    overlay.className = 'orch-modal-overlay';
    overlay.id = 'orch-session-select-overlay';

    overlay.innerHTML = `
        <div class="orch-modal" style="min-width:400px;max-width:500px;">
            <h3>${t('orch_modal_select_session')}</h3>
            <p style="font-size:12px;color:#6b7280;margin-bottom:10px;">${t('orch_modal_select_desc')}</p>
            <div class="orch-session-list" id="orch-session-select-list">
                <div style="text-align:center;padding:20px;color:#9ca3af;font-size:12px;">${t('orch_modal_loading')}</div>
            </div>
            <div class="orch-modal-btns">
                <button id="orch-session-cancel-btn" style="padding:6px 14px;border-radius:6px;border:1px solid #d1d5db;background:white;color:#374151;cursor:pointer;font-size:12px;">${t('orch_modal_cancel')}</button>
                <button id="orch-session-confirm-btn" disabled style="padding:6px 14px;border-radius:6px;border:none;background:#2563eb;color:white;cursor:pointer;font-size:12px;opacity:0.5;">${t('orch_modal_confirm_gen')}</button>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);

    let selectedSid = null;

    overlay.querySelector('#orch-session-cancel-btn').addEventListener('click', () => overlay.remove());
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

    const listEl = overlay.querySelector('#orch-session-select-list');
    try {
        const resp = await fetch('/proxy_sessions');
        const data = await resp.json();
        listEl.innerHTML = '';

        const newSessionId = Date.now().toString(36) + Math.random().toString(36).substr(2, 4);
        const newItem = document.createElement('div');
        newItem.className = 'orch-session-new';
        newItem.innerHTML = `<span style="font-size:18px;">🆕</span><div style="flex:1;"><div style="font-size:13px;font-weight:500;color:#2563eb;">${t('orch_modal_new_session')}</div><div style="font-size:10px;color:#9ca3af;font-family:monospace;">#${newSessionId.slice(-6)}</div></div>`;
        newItem.addEventListener('click', () => {
            listEl.querySelectorAll('.orch-session-item,.orch-session-new').forEach(el => el.classList.remove('selected'));
            newItem.classList.add('selected');
            selectedSid = newSessionId;
            const btn = overlay.querySelector('#orch-session-confirm-btn');
            btn.disabled = false; btn.style.opacity = '1';
        });
        listEl.appendChild(newItem);

        if (data.sessions && data.sessions.length > 0) {
            data.sessions.sort((a, b) => b.session_id.localeCompare(a.session_id));
            for (const s of data.sessions) {
                const item = document.createElement('div');
                item.className = 'orch-session-item';
                item.innerHTML = `<span class="orch-session-icon">💬</span><div style="flex:1;min-width:0;"><div class="orch-session-title">${escapeHtml(s.title || 'Untitled')}</div><div class="orch-session-id">#${s.session_id.slice(-6)} · ${t('orch_msg_count', {count: s.message_count||0})}</div></div>`;
                item.addEventListener('click', () => {
                    listEl.querySelectorAll('.orch-session-item,.orch-session-new').forEach(el => el.classList.remove('selected'));
                    item.classList.add('selected');
                    selectedSid = s.session_id;
                    const btn = overlay.querySelector('#orch-session-confirm-btn');
                    btn.disabled = false; btn.style.opacity = '1';
                });
                listEl.appendChild(item);
            }
        }
    } catch(e) {
        listEl.innerHTML = '<div style="text-align:center;padding:20px;color:#dc2626;font-size:12px;">' + t('orch_load_session_fail') + '</div>';
    }

    overlay.querySelector('#orch-session-confirm-btn').addEventListener('click', () => {
        if (!selectedSid) return;
        orchTargetSessionId = selectedSid;
        overlay.remove();
        orchDoGenerateAgentYaml();
    });
}

async function orchDoGenerateAgentYaml() {
    const data = orchGetLayoutData();
    // Attach the user-selected target session_id
    data.target_session_id = orchTargetSessionId || null;

    const statusEl = document.getElementById('orch-agent-status');
    const promptEl = document.getElementById('orch-prompt-content');
    const yamlEl = document.getElementById('orch-agent-yaml');
    statusEl.textContent = t('orch_status_communicating', {id: (orchTargetSessionId||'').slice(-6)});
    statusEl.style.cssText = 'color:#2563eb;background:#eff6ff;border-color:#bfdbfe;';
    promptEl.textContent = t('orch_status_generating');
    yamlEl.textContent = t('orch_status_waiting');

    const oldBtn = document.getElementById('orch-goto-chat-container');
    if (oldBtn) oldBtn.remove();

    try {
        const r = await fetch('/proxy_visual/agent-generate-yaml', {
            method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data),
        });
        const res = await r.json();
        if (res.prompt) promptEl.textContent = res.prompt;
        if (res.error) {
            yamlEl.textContent = '# ⚠️ ' + res.error;
            statusEl.textContent = '⚠️ ' + (res.error.includes('401') ? t('orch_status_auth_fail') : t('orch_status_agent_unavail'));
            statusEl.style.cssText = 'color:#dc2626;background:#fef2f2;border-color:#fca5a5;';
            orchToast(t('orch_toast_agent_unavail'));
            return;
        }
        if (res.agent_yaml) {
            yamlEl.textContent = res.agent_yaml;
            if (res.validation?.valid) {
                let statusMsg = t('orch_yaml_valid', {steps: res.validation.steps, types: res.validation.step_types.join(', ')});
                if (res.saved_file && !res.saved_file.startsWith('save_error')) {
                    statusMsg += t('orch_yaml_saved_suffix', {file: res.saved_file});
                }
                statusEl.textContent = statusMsg;
                statusEl.style.cssText = 'color:#16a34a;background:#f0fdf4;border-color:#86efac;';
                orchToast(res.saved_file ? t('orch_toast_yaml_generated') : t('orch_toast_agent_valid'));
            } else {
                statusEl.textContent = t('orch_yaml_warn', {error: res.validation?.error||''});
                statusEl.style.cssText = 'color:#d97706;background:#fffbeb;border-color:#fbbf24;';
            }
            orchShowGotoChatButton();
        }
    } catch(e) {
        promptEl.textContent = t('orch_comm_fail', {msg: e.message});
        statusEl.textContent = t('orch_status_conn_error');
        statusEl.style.cssText = 'color:#dc2626;background:#fef2f2;border-color:#fca5a5;';
    }
}

function orchShowGotoChatButton() {
    const old = document.getElementById('orch-goto-chat-container');
    if (old) old.remove();

    if (!orchTargetSessionId) return;

    const container = document.createElement('div');
    container.id = 'orch-goto-chat-container';
    container.style.cssText = 'padding: 8px 12px; text-align: center;';

    const sessionLabel = '#' + orchTargetSessionId.slice(-6);
    container.innerHTML = `
        <button class="orch-goto-chat-btn" onclick="orchGotoChat()">
            ${t('orch_goto_chat', {session: escapeHtml(sessionLabel)})}
        </button>
    `;

    const statusEl = document.getElementById('orch-agent-status');
    if (statusEl && statusEl.parentNode) {
        statusEl.parentNode.insertBefore(container, statusEl.nextSibling);
    }
}

async function orchGotoChat() {
    if (!orchTargetSessionId) { orchToast(t('orch_toast_no_session')); return; }

    const prevSessionId = currentSessionId;
    if (currentSessionId === orchTargetSessionId) {
        currentSessionId = '__temp_orch__';
    }

    switchPage('chat');
    await switchToSession(orchTargetSessionId);

    orchToast(t('orch_toast_jumped', {id: orchTargetSessionId.slice(-6)}));
}

// ── Session Status ──
async function orchRefreshSessions() {
    try {
        const r = await fetch('/proxy_visual/sessions-status');
        const sessions = await r.json();
        orch.sessionStatuses = {};
        if (Array.isArray(sessions)) {
            sessions.forEach(s => {
                const sid = s.session_id || s.id || '';
                const isRunning = s.is_running || s.status === 'running' || false;
                orch.sessionStatuses[sid] = isRunning ? 'running' : 'idle';
            });
        }
        orch.nodes.forEach(n => {
            const el = document.getElementById('onode-' + n.id);
            if (!el) return;
            const dot = el.querySelector('.orch-node-status');
            if (!dot) return;
            const isRunning = Object.entries(orch.sessionStatuses).some(([sid, st]) =>
                st === 'running' && (sid.includes(n.name) || sid.includes(n.tag))
            );
            dot.className = 'orch-node-status ' + (isRunning ? 'running' : 'idle');
        });
        orchToast(t('orch_toast_session_updated'));
    } catch(e) {
        orchToast(t('orch_toast_session_fail'));
    }
}

// ── Actions ──
function orchClearCanvas() {
    orch.nodes = []; orch.edges = []; orch.groups = []; orch.selectedNodes.clear();
    orch.zoom = 1; orch.panX = 0; orch.panY = 0; orchApplyTransform();
    const area = document.getElementById('orch-canvas-inner');
    area.querySelectorAll('.orch-node,.orch-group').forEach(el => el.remove());
    orchRenderEdges();
    orchUpdateYaml();
    document.getElementById('orch-canvas-hint').style.display = '';
}

function orchAutoArrange() {
    const n = orch.nodes.length;
    if (n === 0) return;
    orch.zoom = 1; orch.panX = 0; orch.panY = 0; orchApplyTransform();
    const area = document.getElementById('orch-canvas-area');
    const cw = area.offsetWidth, ch = area.offsetHeight;
    const cols = Math.ceil(Math.sqrt(n));
    const gapX = Math.min(180, (cw - 60) / cols);
    const gapY = Math.min(90, (ch - 60) / Math.ceil(n / cols));
    orch.nodes.forEach((node, i) => {
        const col = i % cols, row = Math.floor(i / cols);
        node.x = 40 + col * gapX;
        node.y = 40 + row * gapY;
        const el = document.getElementById('onode-' + node.id);
        if (el) { el.style.left = node.x + 'px'; el.style.top = node.y + 'px'; }
    });
    orchRenderEdges();
    orch.groups.forEach(g => orchUpdateGroupBounds(g));
    orchUpdateYaml();
    orchToast(t('orch_toast_arranged'));
}

async function orchSaveLayout() {
    const name = prompt(t('orch_prompt_layout_name'), 'my-layout');
    if (!name) return;
    const data = orchGetLayoutData();
    data.name = name;
    try {
        await fetch('/proxy_visual/save-layout', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data) });
        orchToast(t('orch_toast_saved', {name}));
    } catch(e) { orchToast(t('orch_toast_save_fail')); }
}

async function orchLoadLayout() {
    try {
        const r = await fetch('/proxy_visual/load-layouts');
        const layouts = await r.json();
        if (!layouts.length) { orchToast(t('orch_toast_no_layouts')); return; }

        // Build visual selection modal
        const overlay = document.createElement('div');
        overlay.className = 'orch-modal-overlay';
        overlay.id = 'orch-load-layout-overlay';
        overlay.innerHTML = `
            <div class="orch-modal" style="min-width:360px;max-width:460px;">
                <h3>${t('orch_modal_select_layout')}</h3>
                <div class="orch-session-list" id="orch-layout-select-list" style="max-height:300px;overflow-y:auto;"></div>
                <div class="orch-modal-btns">
                    <button id="orch-layout-cancel-btn" style="padding:6px 14px;border-radius:6px;border:1px solid #d1d5db;background:white;color:#374151;cursor:pointer;font-size:12px;">${t('orch_modal_cancel')}</button>
                    <button id="orch-layout-del-btn" style="padding:6px 14px;border-radius:6px;border:1px solid #fca5a5;background:#fef2f2;color:#dc2626;cursor:pointer;font-size:12px;display:none;">${t('orch_modal_delete')}</button>
                    <button id="orch-layout-confirm-btn" disabled style="padding:6px 14px;border-radius:6px;border:none;background:#2563eb;color:white;cursor:pointer;font-size:12px;opacity:0.5;">${t('orch_modal_load')}</button>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        let selectedName = null;
        overlay.querySelector('#orch-layout-cancel-btn').addEventListener('click', () => overlay.remove());
        overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

        const listEl = overlay.querySelector('#orch-layout-select-list');
        for (const name of layouts) {
            const item = document.createElement('div');
            item.className = 'orch-session-item';
            item.innerHTML = `<span class="orch-session-icon">📋</span><div style="flex:1;min-width:0;"><div class="orch-session-title">${escapeHtml(name)}</div></div>`;
            item.addEventListener('click', () => {
                listEl.querySelectorAll('.orch-session-item').forEach(el => el.classList.remove('selected'));
                item.classList.add('selected');
                selectedName = name;
                const btn = overlay.querySelector('#orch-layout-confirm-btn');
                btn.disabled = false; btn.style.opacity = '1';
                overlay.querySelector('#orch-layout-del-btn').style.display = '';
            });
            listEl.appendChild(item);
        }

        overlay.querySelector('#orch-layout-del-btn').addEventListener('click', async () => {
            if (!selectedName || !confirm(t('orch_confirm_del_layout', {name: selectedName}))) return;
            try {
                await fetch('/proxy_visual/delete-layout/' + encodeURIComponent(selectedName), { method: 'DELETE' });
                orchToast(t('orch_toast_deleted', {name: selectedName}));
                overlay.remove();
                orchLoadLayout();
            } catch(e) { orchToast(t('orch_toast_del_fail')); }
        });

        overlay.querySelector('#orch-layout-confirm-btn').addEventListener('click', async () => {
            if (!selectedName) return;
            overlay.remove();
            await orchDoLoadLayout(selectedName);
        });
    } catch(e) { orchToast(t('orch_toast_load_fail')); }
}

async function orchDoLoadLayout(name) {
    try {
        const r2 = await fetch('/proxy_visual/load-layout/' + encodeURIComponent(name));
        const data = await r2.json();
        if (data.error) { orchToast(data.error); return; }
        orchClearCanvas();

        // Restore settings
        if (data.settings) {
            document.getElementById('orch-repeat').checked = data.settings.repeat === true;
            document.getElementById('orch-rounds').value = data.settings.max_rounds || 5;
            document.getElementById('orch-bot-session').checked = data.settings.use_bot_session || false;
            if (data.settings.cluster_threshold) {
                document.getElementById('orch-threshold').value = data.settings.cluster_threshold;
                document.getElementById('orch-threshold-val').textContent = data.settings.cluster_threshold;
            }
        }

        // Restore view (zoom/pan)
        if (data.view) {
            orch.zoom = data.view.zoom || 1;
            orch.panX = data.view.panX || 0;
            orch.panY = data.view.panY || 0;
            orchApplyTransform();
        }

        // Build id mapping: restore nodes with ORIGINAL ids preserved
        const idMap = {};
        (data.nodes||[]).forEach(n => {
            const origId = n.id;
            const newNode = orchAddNode(n, n.x, n.y);
            idMap[origId] = newNode.id;
        });

        // Restore edges using mapped ids
        (data.edges||[]).forEach(e => {
            const src = idMap[e.source];
            const tgt = idMap[e.target];
            if (src && tgt) orchAddEdge(src, tgt);
        });

        // Restore groups with mapped node ids
        (data.groups||[]).forEach(g => {
            const mappedGroup = {...g, nodeIds: (g.nodeIds||[]).map(nid => idMap[nid]).filter(Boolean)};
            if (mappedGroup.nodeIds.length > 0) {
                orch.groups.push(mappedGroup);
                orchRenderGroup(mappedGroup);
            }
        });

        orchRenderEdges();
        orchUpdateYaml();
        orchToast(t('orch_toast_loaded', {name}));
    } catch(e) { orchToast(t('orch_toast_load_fail') + ': ' + e.message); }
}

function orchExportYaml() {
    const yaml = document.getElementById('orch-yaml-content').textContent;
    if (!yaml || yaml.startsWith(t('orch_rule_yaml_hint').substring(0,2))) { orchToast(t('orch_toast_gen_yaml')); return; }
    navigator.clipboard.writeText(yaml).then(() => orchToast(t('orch_toast_yaml_copied'))).catch(() => {
        const ta = document.createElement('textarea'); ta.value = yaml; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); orchToast(t('orch_toast_yaml_copied'));
    });
}

// ── Download YAML as file ──
function orchDownloadYaml() {
    const yaml = document.getElementById('orch-yaml-content').textContent;
    if (!yaml || yaml.startsWith(t('orch_rule_yaml_hint').substring(0,2))) { orchToast(t('orch_toast_gen_yaml')); return; }
    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const fname = `oasis_${ts}.yaml`;
    const blob = new Blob([yaml], { type: 'application/x-yaml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = fname; a.style.display = 'none';
    document.body.appendChild(a); a.click();
    setTimeout(() => { document.body.removeChild(a); URL.revokeObjectURL(url); }, 200);
    orchToast(t('orch_toast_yaml_downloaded'));
}

// ── Upload YAML (button click) ──
function orchUploadYamlClick() {
    document.getElementById('orch-yaml-upload-input').click();
}

function orchHandleYamlUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    event.target.value = ''; // reset so re-selecting same file works
    orchImportYamlFile(file);
}

// ── Import a YAML file → upload to server → load as layout ──
async function orchImportYamlFile(file) {
    const fname = file.name || 'upload.yaml';
    if (!fname.endsWith('.yaml') && !fname.endsWith('.yml')) {
        orchToast(t('orch_toast_not_yaml'));
        return;
    }
    try {
        const text = await file.text();
        // Send YAML text to backend for saving and conversion
        const r = await fetch('/proxy_visual/upload-yaml', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: fname, content: text }),
        });
        const res = await r.json();
        if (res.error) { orchToast(t('orch_toast_yaml_upload_fail') + ': ' + res.error); return; }
        // Load the returned layout data
        if (res.layout) {
            orchClearCanvas();
            const data = res.layout;
            // Restore settings
            if (data.settings) {
                document.getElementById('orch-repeat').checked = data.settings.repeat === true;
                document.getElementById('orch-rounds').value = data.settings.max_rounds || 5;
                document.getElementById('orch-bot-session').checked = data.settings.use_bot_session || false;
                if (data.settings.cluster_threshold) {
                    document.getElementById('orch-threshold').value = data.settings.cluster_threshold;
                    document.getElementById('orch-threshold-val').textContent = data.settings.cluster_threshold;
                }
            }
            const idMap = {};
            (data.nodes || []).forEach(n => {
                const newNode = orchAddNode(n, n.x, n.y);
                idMap[n.id] = newNode.id;
            });
            (data.edges || []).forEach(e => {
                const src = idMap[e.source], tgt = idMap[e.target];
                if (src && tgt) orchAddEdge(src, tgt);
            });
            (data.groups || []).forEach(g => {
                const mapped = { ...g, nodeIds: (g.nodeIds || []).map(nid => idMap[nid]).filter(Boolean) };
                if (mapped.nodeIds.length > 0) { orch.groups.push(mapped); orchRenderGroup(mapped); }
            });
            orchRenderEdges();
            orchUpdateYaml();
            orchToast(t('orch_toast_yaml_uploaded', { name: fname }));
        } else {
            // Fallback: just show the YAML text
            document.getElementById('orch-yaml-content').textContent = text;
            orchToast(t('orch_toast_yaml_uploaded', { name: fname }));
        }
    } catch (e) {
        orchToast(t('orch_toast_yaml_upload_fail') + ': ' + e.message);
    }
}

// ── Drag & Drop YAML file onto canvas ──
function orchSetupFileDrop() {
    const canvas = document.getElementById('orch-canvas-area');
    const dropOverlay = document.createElement('div');
    dropOverlay.id = 'orch-drop-overlay';
    dropOverlay.className = 'orch-drop-overlay';
    dropOverlay.innerHTML = '<div class="orch-drop-content"><div style="font-size:48px;">📄</div><div>' + t('orch_drop_hint') + '</div></div>';
    canvas.style.position = 'relative';
    canvas.appendChild(dropOverlay);

    let dragCounter = 0;

    canvas.addEventListener('dragenter', e => {
        // Only show overlay for file drags (not sidebar card drags)
        if (e.dataTransfer.types.includes('Files')) {
            e.preventDefault();
            dragCounter++;
            dropOverlay.classList.add('visible');
        }
    });
    canvas.addEventListener('dragover', e => {
        if (e.dataTransfer.types.includes('Files')) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
        }
    });
    canvas.addEventListener('dragleave', e => {
        if (e.dataTransfer.types.includes('Files')) {
            dragCounter--;
            if (dragCounter <= 0) {
                dragCounter = 0;
                dropOverlay.classList.remove('visible');
            }
        }
    });
    canvas.addEventListener('drop', e => {
        dragCounter = 0;
        dropOverlay.classList.remove('visible');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            if (file.name.endsWith('.yaml') || file.name.endsWith('.yml')) {
                e.preventDefault();
                e.stopPropagation();
                orchImportYamlFile(file);
                return;
            }
        }
        // Let the original drop handler process non-file drags (sidebar cards)
    }, true);
}

function orchCopyPrompt() {
    const text = document.getElementById('orch-prompt-content').textContent;
    navigator.clipboard.writeText(text).catch(() => {}); orchToast(t('orch_toast_prompt_copied'));
}
function orchCopyAgentYaml() {
    const text = document.getElementById('orch-agent-yaml').textContent;
    navigator.clipboard.writeText(text).catch(() => {}); orchToast(t('orch_toast_agent_yaml_copied'));
}

function orchUpdateStatus() {
    document.getElementById('orch-status-bar').textContent = t('orch_status_bar', {nodes: orch.nodes.length, edges: orch.edges.length, groups: orch.groups.length});
}

function orchToast(msg) {
    const existing = document.querySelector('.orch-toast');
    if (existing) existing.remove();
    const t = document.createElement('div');
    t.className = 'orch-toast';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 2500);
}
