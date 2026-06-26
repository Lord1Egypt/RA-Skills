/**
 * Visual Agent Orchestration System - Canvas Events & YAML Export
 * Continuation of app.js: event handlers, YAML generation, UI helpers.
 */

// ── Canvas Event Setup ──
function setupCanvasEvents() {
    const area = document.getElementById('canvas-area');

    // Drag over for drop from sidebar
    area.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
    });

    // Drop from sidebar to create node
    area.addEventListener('drop', (e) => {
        e.preventDefault();
        try {
            const data = JSON.parse(e.dataTransfer.getData('application/json'));
            const rect = area.getBoundingClientRect();
            const dropX = e.clientX - rect.left;
            const dropY = e.clientY - rect.top;
            // Check if dropped near center (within 50px of center hint area)
            const cX = rect.width / 2;
            const cY = rect.height / 2;
            const distToCenter = Math.sqrt((dropX - cX) ** 2 + (dropY - cY) ** 2);
            if (distToCenter < 50 && state.nodes.length === 0) {
                // First node dropped near center → place exactly at center
                addNodeToCenter(data);
            } else {
                addNodeToCanvas(data, dropX - 60, dropY - 20);
            }
        } catch (err) {
            console.error('Drop failed:', err);
        }
    });

    // Mouse move for dragging nodes and drawing connections
    document.addEventListener('mousemove', (e) => {
        const rect = area.getBoundingClientRect();

        // Node dragging
        if (state.dragging && state.dragging.nodeId) {
            const node = state.nodes.find(n => n.id === state.dragging.nodeId);
            if (!node) return;

            const newX = e.clientX - state.dragging.offsetX;
            const newY = e.clientY - state.dragging.offsetY;
            const dx = newX - node.x;
            const dy = newY - node.y;

            if (state.dragging.multiDrag) {
                // Move all selected nodes
                state.selectedNodes.forEach(nid => {
                    const n = state.nodes.find(nn => nn.id === nid);
                    if (n) {
                        n.x += dx;
                        n.y += dy;
                        const el = document.getElementById('node-' + nid);
                        if (el) {
                            el.style.left = n.x + 'px';
                            el.style.top = n.y + 'px';
                        }
                    }
                });
            } else {
                node.x = newX;
                node.y = newY;
                const el = document.getElementById('node-' + node.id);
                if (el) {
                    el.style.left = node.x + 'px';
                    el.style.top = node.y + 'px';
                }
            }

            // Update groups containing moved nodes
            state.groups.forEach(g => {
                const moved = state.dragging.multiDrag
                    ? [...state.selectedNodes]
                    : [state.dragging.nodeId];
                if (moved.some(nid => g.nodeIds.includes(nid))) {
                    updateGroupBounds(g);
                }
            });

            renderAllEdges();
        }

        // Connection drawing
        if (state.connecting) {
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;
            drawTempLine(state.connecting.startX, state.connecting.startY, mx, my);
        }

        // Selection rectangle
        if (state.selecting) {
            const sx = state.selecting.startX;
            const sy = state.selecting.startY;
            const cx = e.clientX - rect.left;
            const cy = e.clientY - rect.top;

            let selRect = document.querySelector('.selection-rect');
            if (!selRect) {
                selRect = document.createElement('div');
                selRect.className = 'selection-rect';
                area.appendChild(selRect);
            }
            selRect.style.left = Math.min(sx, cx) + 'px';
            selRect.style.top = Math.min(sy, cy) + 'px';
            selRect.style.width = Math.abs(cx - sx) + 'px';
            selRect.style.height = Math.abs(cy - sy) + 'px';
        }
    });

    // Mouse up
    document.addEventListener('mouseup', (e) => {
        // Finish selection
        if (state.selecting) {
            const rect = area.getBoundingClientRect();
            const sx = state.selecting.startX;
            const sy = state.selecting.startY;
            const ex = e.clientX - rect.left;
            const ey = e.clientY - rect.top;

            const selX = Math.min(sx, ex);
            const selY = Math.min(sy, ey);
            const selW = Math.abs(ex - sx);
            const selH = Math.abs(ey - sy);

            if (selW > 10 && selH > 10) {
                clearSelection();
                state.nodes.forEach(n => {
                    const nel = document.getElementById('node-' + n.id);
                    if (!nel) return;
                    const nw = nel.offsetWidth;
                    const nh = nel.offsetHeight;
                    // Check overlap
                    if (n.x + nw > selX && n.x < selX + selW &&
                        n.y + nh > selY && n.y < selY + selH) {
                        selectNode(n.id);
                    }
                });
            }

            const selRect = document.querySelector('.selection-rect');
            if (selRect) selRect.remove();
            state.selecting = null;
        }

        if (state.dragging) {
            state.dragging = null;
            updateYamlOutput();
        }

        if (state.connecting) {
            state.connecting = null;
            removeTempLine();
        }
    });

    // Canvas click to deselect
    area.addEventListener('mousedown', (e) => {
        if (e.target === area || e.target.id === 'edge-svg') {
            clearSelection();
            hideContextMenu();

            // Start selection rectangle
            const rect = area.getBoundingClientRect();
            state.selecting = {
                startX: e.clientX - rect.left,
                startY: e.clientY - rect.top,
            };
        }
    });

    // Right-click context menu on canvas
    area.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        showContextMenu(e.clientX, e.clientY);
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        // Delete selected nodes
        if (e.key === 'Delete' || e.key === 'Backspace') {
            [...state.selectedNodes].forEach(nid => removeNode(nid));
        }

        // Ctrl+A select all
        if (e.key === 'a' && (e.ctrlKey || e.metaKey)) {
            e.preventDefault();
            state.nodes.forEach(n => selectNode(n.id));
        }

        // Ctrl+G group selected as parallel
        if (e.key === 'g' && (e.ctrlKey || e.metaKey)) {
            e.preventDefault();
            groupSelectedNodes('parallel');
        }

        // Escape
        if (e.key === 'Escape') {
            clearSelection();
            hideContextMenu();
        }
    });
}

// ── Top Bar Events ──
function setupTopBarEvents() {
    document.getElementById('btn-clear').addEventListener('click', () => {
        if (confirm(i18n('confirm_clear'))) {
            clearCanvas();
        }
    });

    document.getElementById('btn-export').addEventListener('click', async () => {
        const yamlText = document.getElementById('yaml-content').textContent;
        try {
            await navigator.clipboard.writeText(yamlText);
            showToast(i18n('toast_yaml_copied'));
        } catch {
            // Fallback
            const ta = document.createElement('textarea');
            ta.value = yamlText;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            showToast(i18n('toast_yaml_copied'));
        }
    });

    document.getElementById('btn-save').addEventListener('click', async () => {
        const name = prompt(i18n('prompt_layout_name'), 'my-layout');
        if (!name) return;

        const payload = getLayoutData();
        payload.name = name;

        try {
            const resp = await fetch('/api/save-layout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const result = await resp.json();
            if (result.saved) showToast(i18n('toast_layout_saved'));
            else showToast(i18n('toast_save_failed') + result.error);
        } catch (e) {
            showToast(i18n('toast_save_failed') + e.message);
        }
    });

    document.getElementById('btn-load').addEventListener('click', async () => {
        try {
            const resp = await fetch('/api/load-layouts');
            const layouts = await resp.json();
            if (layouts.length === 0) {
                showToast(i18n('toast_no_layouts'));
                return;
            }
            const name = prompt(i18n('prompt_load_layout') + layouts.join(', '));
            if (!name) return;

            const resp2 = await fetch('/api/load-layout/' + encodeURIComponent(name));
            if (!resp2.ok) {
                showToast(i18n('toast_no_layouts'));
                return;
            }
            const data = await resp2.json();
            loadLayoutData(data);
            showToast(i18n('toast_layout_loaded'));
        } catch (e) {
            showToast(i18n('toast_load_failed') + e.message);
        }
    });

    document.getElementById('btn-auto-arrange').addEventListener('click', () => {
        autoArrangeNodes();
    });

    document.getElementById('btn-generate-prompt').addEventListener('click', async () => {
        await generateLLMPrompt();
    });
}

// ── Settings Events ──
function setupSettingsEvents() {
    document.getElementById('setting-repeat').addEventListener('change', (e) => {
        state.settings.repeat = e.target.checked;
        updateYamlOutput();
    });

    document.getElementById('setting-rounds').addEventListener('change', (e) => {
        state.settings.max_rounds = parseInt(e.target.value) || 5;
        updateYamlOutput();
    });

    document.getElementById('setting-bot-session').addEventListener('change', (e) => {
        state.settings.use_bot_session = e.target.checked;
        updateYamlOutput();
    });

    document.getElementById('setting-threshold').addEventListener('input', (e) => {
        state.settings.cluster_threshold = parseInt(e.target.value) || 150;
        document.getElementById('threshold-value').textContent = e.target.value + 'px';
        updateYamlOutput();
    });
}

// ── Context Menu ──
function showContextMenu(x, y) {
    hideContextMenu();
    const menu = document.createElement('div');
    menu.className = 'context-menu';
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';

    const hasSelection = state.selectedNodes.size > 0;
    const items = [];

    if (hasSelection && state.selectedNodes.size >= 2) {
        items.push({ icon: '🔀', label: i18n('ctx_group_parallel'), action: () => groupSelectedNodes('parallel') });
        items.push({ icon: '👥', label: i18n('ctx_group_all'), action: () => groupSelectedNodes('all') });
        items.push({ icon: '🔗', label: i18n('ctx_chain'), action: () => chainSelectedNodes() });
        items.push({ divider: true });
    }

    if (hasSelection) {
        items.push({ icon: '🗑️', label: i18n('ctx_delete'), action: () => {
            [...state.selectedNodes].forEach(nid => removeNode(nid));
        }});
        items.push({ divider: true });
    }

    items.push({ icon: '📝', label: i18n('ctx_add_manual'), action: () => {
        addNodeToCenter({
            type: 'manual',
            name: i18n('manual_injection'),
            tag: 'manual',
            emoji: '📝',
            author: '主持人',
            content: 'Please continue the discussion.',
        });
    }});

    items.push({ icon: '⭐', label: i18n('ctx_add_custom'), action: () => {
        showCustomExpertModal(x, y);
    }});

    items.push({ divider: true });
    items.push({ icon: '🧹', label: i18n('ctx_clear_all'), action: clearCanvas });

    items.forEach(item => {
        if (item.divider) {
            const d = document.createElement('div');
            d.className = 'divider';
            menu.appendChild(d);
        } else {
            const mi = document.createElement('div');
            mi.className = 'menu-item';
            mi.innerHTML = `<span>${item.icon}</span> ${item.label}`;
            mi.addEventListener('click', () => {
                hideContextMenu();
                item.action();
            });
            menu.appendChild(mi);
        }
    });

    document.body.appendChild(menu);
    state.contextMenu = menu;

    // Close on click outside
    setTimeout(() => {
        document.addEventListener('click', hideContextMenu, { once: true });
    }, 10);
}

function hideContextMenu() {
    if (state.contextMenu) {
        state.contextMenu.remove();
        state.contextMenu = null;
    }
}

// ── Group Selected Nodes ──
function groupSelectedNodes(type) {
    if (state.selectedNodes.size < 2) {
        showToast(i18n('toast_select_2'));
        return;
    }

    const nodeIds = [...state.selectedNodes];
    const members = state.nodes.filter(n => nodeIds.includes(n.id));
    if (members.length < 2) return;

    const padding = 30;
    const minX = Math.min(...members.map(n => n.x)) - padding;
    const minY = Math.min(...members.map(n => n.y)) - padding;
    const maxX = Math.max(...members.map(n => {
        const el = document.getElementById('node-' + n.id);
        return n.x + (el ? el.offsetWidth : 120);
    })) + padding;
    const maxY = Math.max(...members.map(n => {
        const el = document.getElementById('node-' + n.id);
        return n.y + (el ? el.offsetHeight : 50);
    })) + padding;

    createGroup(type, minX, minY, maxX - minX, maxY - minY, nodeIds);
    clearSelection();
}

// ── Chain Selected Nodes (create sequential edges) ──
function chainSelectedNodes() {
    if (state.selectedNodes.size < 2) {
        showToast(i18n('toast_select_2_chain'));
        return;
    }

    const nodeIds = [...state.selectedNodes];
    // Sort by x position (left to right)
    const sorted = nodeIds
        .map(id => state.nodes.find(n => n.id === id))
        .filter(Boolean)
        .sort((a, b) => a.x - b.x || a.y - b.y);

    for (let i = 0; i < sorted.length - 1; i++) {
        addEdge(sorted[i].id, sorted[i + 1].id);
    }
    clearSelection();
    showToast(i18n('toast_chained'));
}

// ── Auto-Arrange Nodes ──
function autoArrangeNodes() {
    const n = state.nodes.length;
    if (n === 0) return;

    const area = document.getElementById('canvas-area');
    const areaW = area.offsetWidth;
    const areaH = area.offsetHeight;
    const centerX = areaW / 2;
    const centerY = areaH / 2;
    const radius = Math.min(areaW, areaH) * 0.35;

    state.nodes.forEach((node, i) => {
        const angle = (2 * Math.PI * i) / n - Math.PI / 2;
        node.x = Math.round(centerX + radius * Math.cos(angle) - 60);
        node.y = Math.round(centerY + radius * Math.sin(angle) - 20);

        const el = document.getElementById('node-' + node.id);
        if (el) {
            el.style.left = node.x + 'px';
            el.style.top = node.y + 'px';
        }
    });

    // Update groups
    state.groups.forEach(g => updateGroupBounds(g));
    renderAllEdges();
    updateYamlOutput();
    showToast(i18n('toast_arranged'));
}

// ── YAML Output ──
async function updateYamlOutput() {
    const data = getLayoutData();
    try {
        const resp = await fetch('/api/generate-yaml', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const result = await resp.json();
        if (result.yaml) {
            document.getElementById('yaml-content').textContent = result.yaml;
        } else if (result.error) {
            document.getElementById('yaml-content').textContent = '# Error: ' + result.error;
        }
    } catch (e) {
        document.getElementById('yaml-content').textContent = '# Failed to generate YAML';
    }
}

// ── LLM Prompt Generation → Send to Main Agent → Get YAML ──
async function generateLLMPrompt() {
    const data = getLayoutData();
    if (state.nodes.length === 0) {
        showToast(i18n('toast_no_nodes'));
        return;
    }

    // Get credentials from the login form
    const username = (document.getElementById('agent-username')?.value || '').trim();
    const password = (document.getElementById('agent-password')?.value || '').trim();
    const authStatusEl = document.getElementById('auth-status');

    if (!username || !password) {
        showToast(i18n('toast_enter_creds'));
        if (authStatusEl) {
            authStatusEl.textContent = i18n('auth_missing');
            authStatusEl.style.color = '#e06060';
        }
        return;
    }

    // Attach credentials to request payload
    data.credentials = { username, password };

    const promptEl = document.getElementById('llm-prompt-content');
    const yamlEl = document.getElementById('agent-yaml-content');
    const statusEl = document.getElementById('agent-status');

    promptEl.textContent = i18n('status_building');
    if (yamlEl) yamlEl.textContent = i18n('status_waiting');
    if (statusEl) statusEl.textContent = i18n('status_loading', {user: username});
    if (statusEl) statusEl.className = 'agent-status loading';
    if (authStatusEl) {
        authStatusEl.textContent = i18n('auth_authenticating');
        authStatusEl.style.color = '#60a0e0';
    }

    try {
        const resp = await fetch('/api/agent-generate-yaml', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const result = await resp.json();

        // Show the prompt
        if (result.prompt) {
            promptEl.textContent = result.prompt;
        }

        // Handle error (agent not running, auth failed, etc.)
        if (result.error) {
            if (yamlEl) yamlEl.textContent = '# ⚠️ ' + result.error;
            const isAuthError = result.error.includes('401') || result.error.includes('认证') || result.error.includes('auth');
            if (statusEl) {
                statusEl.textContent = isAuthError
                    ? i18n('status_auth_fail')
                    : i18n('status_agent_unavail');
                statusEl.className = 'agent-status error';
            }
            if (authStatusEl) {
                authStatusEl.textContent = isAuthError
                    ? i18n('auth_failed')
                    : i18n('auth_conn_issue');
                authStatusEl.style.color = '#e06060';
            }
            showToast(isAuthError ? i18n('toast_auth_failed') : i18n('toast_agent_unavail'));
            return;
        }

        // Auth succeeded
        if (authStatusEl) {
            authStatusEl.textContent = i18n('auth_success') + ' ' + username;
            authStatusEl.style.color = '#60e080';
        }

        // Show agent-generated YAML
        if (result.agent_yaml) {
            if (yamlEl) yamlEl.textContent = result.agent_yaml;

            // Show validation status
            if (result.validation) {
                const v = result.validation;
                if (v.valid) {
                    if (statusEl) {
                        statusEl.textContent = i18n('status_valid_yaml', {steps: v.steps, types: v.step_types.join(', '), repeat: v.repeat});
                        statusEl.className = 'agent-status success';
                    }
                    showToast(i18n('toast_agent_valid'));
                } else {
                    if (statusEl) {
                        statusEl.textContent = i18n('status_yaml_warn', {error: v.error});
                        statusEl.className = 'agent-status warning';
                    }
                    showToast(i18n('toast_agent_warn'));
                }
            }
        } else {
            if (yamlEl) yamlEl.textContent = '# Agent returned no YAML';
            if (statusEl) {
                statusEl.textContent = i18n('status_no_yaml');
                statusEl.className = 'agent-status error';
            }
        }
    } catch (e) {
        promptEl.textContent = '# Failed to communicate with backend: ' + e.message;
        if (yamlEl) yamlEl.textContent = '# Error';
        if (statusEl) {
            statusEl.textContent = i18n('status_conn_error');
            statusEl.className = 'agent-status error';
        }
    }
}

// ── Copy Agent YAML ──
async function copyAgentYaml() {
    const yamlText = document.getElementById('agent-yaml-content')?.textContent || '';
    if (!yamlText || yamlText.startsWith('⏳') || yamlText.startsWith('#')) {
        showToast(i18n('toast_gen_first'));
        return;
    }
    try {
        await navigator.clipboard.writeText(yamlText);
        showToast(i18n('toast_agent_yaml_copied'));
    } catch {
        const ta = document.createElement('textarea');
        ta.value = yamlText;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        showToast(i18n('toast_agent_yaml_copied'));
    }
}

// ── Copy LLM Prompt ──
async function copyLLMPrompt() {
    const promptText = document.getElementById('llm-prompt-content').textContent;
    if (!promptText || promptText.startsWith('⏳') || promptText.startsWith('#')) {
        showToast(i18n('toast_prompt_first'));
        return;
    }
    try {
        await navigator.clipboard.writeText(promptText);
        showToast(i18n('toast_prompt_copied'));
    } catch {
        const ta = document.createElement('textarea');
        ta.value = promptText;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        showToast(i18n('toast_prompt_copied'));
    }
}

function getLayoutData() {
    return {
        nodes: state.nodes.map(n => ({
            id: n.id, name: n.name, tag: n.tag, emoji: n.emoji,
            x: n.x, y: n.y, type: n.type,
            temperature: n.temperature,
            author: n.author, content: n.content,
        })),
        edges: state.edges.map(e => ({ id: e.id, source: e.source, target: e.target })),
        groups: state.groups.map(g => ({
            id: g.id, name: g.name, type: g.type,
            x: g.x, y: g.y, w: g.w, h: g.h,
            nodeIds: g.nodeIds,
        })),
        settings: { ...state.settings },
    };
}

// ── Load Layout Data ──
function loadLayoutData(data) {
    clearCanvas();

    if (data.settings) {
        Object.assign(state.settings, data.settings);
        document.getElementById('setting-repeat').checked = state.settings.repeat;
        document.getElementById('setting-rounds').value = state.settings.max_rounds;
        document.getElementById('setting-bot-session').checked = state.settings.use_bot_session;
        document.getElementById('setting-threshold').value = state.settings.cluster_threshold;
        document.getElementById('threshold-value').textContent = state.settings.cluster_threshold + 'px';
    }

    (data.nodes || []).forEach(n => {
        state.nodes.push(n);
        renderNode(n);
        const idNum = parseInt(n.id.replace('n', ''));
        if (idNum >= state.nextNodeId) state.nextNodeId = idNum + 1;
    });

    (data.edges || []).forEach(e => {
        state.edges.push(e);
        const idNum = parseInt(e.id.replace('e', ''));
        if (idNum >= state.nextEdgeId) state.nextEdgeId = idNum + 1;
    });
    renderAllEdges();

    (data.groups || []).forEach(g => {
        state.groups.push(g);
        renderGroup(g);
        const idNum = parseInt(g.id.replace('g', ''));
        if (idNum >= state.nextGroupId) state.nextGroupId = idNum + 1;
    });

    updateYamlOutput();
    updateStatusBar();
}

// ── Clear Canvas ──
function clearCanvas() {
    state.nodes = [];
    state.edges = [];
    state.groups = [];
    state.selectedNodes.clear();

    const area = document.getElementById('canvas-area');
    area.querySelectorAll('.canvas-node, .group-zone, .selection-rect').forEach(el => el.remove());

    renderAllEdges();
    updateYamlOutput();
    updateStatusBar();
}

// ── Status Bar ──
function updateStatusBar() {
    const bar = document.getElementById('status-bar');
    if (bar) {
        bar.textContent = `${i18n('status_nodes')}: ${state.nodes.length} | ${i18n('status_edges')}: ${state.edges.length} | ${i18n('status_groups')}: ${state.groups.length} | ${i18n('status_selected')}: ${state.selectedNodes.size}`;
    }
}

// ── Modal: Edit Manual Node ──
function showManualEditModal(node) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
        <div class="modal">
            <h3>${i18n('modal_edit_manual')}</h3>
            <label style="font-size:13px;color:#aaa;margin-bottom:4px;display:block;">${i18n('modal_author')}</label>
            <input type="text" id="modal-author" value="${node.author || '主持人'}">
            <label style="font-size:13px;color:#aaa;margin-bottom:4px;display:block;">${i18n('modal_content')}</label>
            <textarea id="modal-content">${node.content || ''}</textarea>
            <div class="modal-buttons">
                <button id="modal-cancel">${i18n('modal_cancel')}</button>
                <button id="modal-save" class="primary">${i18n('modal_save')}</button>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#modal-cancel').addEventListener('click', () => overlay.remove());
    overlay.querySelector('#modal-save').addEventListener('click', () => {
        node.author = document.getElementById('modal-author').value;
        node.content = document.getElementById('modal-content').value;
        node.name = i18n('manual_injection') + ': ' + node.author;
        const el = document.getElementById('node-' + node.id);
        if (el) el.querySelector('.node-name').textContent = node.name;
        overlay.remove();
        updateYamlOutput();
    });
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
}

// ── Modal: Custom Expert ──
function showCustomExpertModal(x, y) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
        <div class="modal">
            <h3>${i18n('modal_add_custom')}</h3>
            <label style="font-size:13px;color:#aaa;margin-bottom:4px;display:block;">${i18n('modal_name')}</label>
            <input type="text" id="modal-expert-name" placeholder="${i18n('modal_ph_name')}">
            <label style="font-size:13px;color:#aaa;margin-bottom:4px;display:block;">${i18n('modal_tag')}</label>
            <input type="text" id="modal-expert-tag" placeholder="${i18n('modal_ph_tag')}">
            <label style="font-size:13px;color:#aaa;margin-bottom:4px;display:block;">${i18n('modal_persona')}</label>
            <textarea id="modal-expert-persona" placeholder="${i18n('modal_ph_persona')}"></textarea>
            <label style="font-size:13px;color:#aaa;margin-bottom:4px;display:block;">${i18n('modal_temperature')}</label>
            <input type="text" id="modal-expert-temp" value="0.7">
            <div class="modal-buttons">
                <button id="modal-cancel">${i18n('modal_cancel')}</button>
                <button id="modal-save" class="primary">${i18n('modal_add')}</button>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);

    overlay.querySelector('#modal-cancel').addEventListener('click', () => overlay.remove());
    overlay.querySelector('#modal-save').addEventListener('click', () => {
        const name = document.getElementById('modal-expert-name').value.trim();
        const tag = document.getElementById('modal-expert-tag').value.trim() || 'custom';
        const persona = document.getElementById('modal-expert-persona').value.trim();
        const temp = parseFloat(document.getElementById('modal-expert-temp').value) || 0.7;

        if (!name) { showToast(i18n('toast_name_required')); return; }

        addNodeToCenter({
            type: 'expert',
            name,
            tag,
            emoji: '⭐',
            temperature: Math.max(0, Math.min(1, temp)),
            persona,
        });

        overlay.remove();
    });
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });
}

// ── Toast Notification ──
function showToast(msg) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
}
