(function(){
  const minifiedTreeEl = document.getElementById('minifiedTree');
  const appConfig = document.getElementById('appConfig');
  const minifiedRootWrapped = appConfig ? appConfig.dataset.minifiedRootWrapped === 'true' : false;
  let minifiedTree = null;
  let minifiedRoot = null;
  if (minifiedTreeEl) {
    try {
      minifiedTree = JSON.parse(minifiedTreeEl.textContent || "{}");
      minifiedRoot = minifiedTree?.root || null;
    } catch (err) {
      minifiedTree = null;
      minifiedRoot = null;
    }
  }

  const toast = document.getElementById('copiedToast');
  const toastDefaultText = toast?.textContent || 'Copied';
  let toastTimer = null;
  const showToast = (message) => {
    if (!toast) return;
    toast.textContent = message || toastDefaultText;
    toast.classList.add('visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove('visible');
      toast.textContent = toastDefaultText;
    }, 1200);
  };

  const copyText = async (text) => {
    if (navigator.clipboard?.writeText && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch (err) {
        // fallback below
      }
    }
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    textarea.setSelectionRange(0, textarea.value.length);
    try {
      const ok = document.execCommand('copy');
      if (ok) return true;
    } catch (err) {
      // ignore and fallback below
    } finally {
      document.body.removeChild(textarea);
    }
    try {
      window.prompt('Copy the text below manually', text);
    } catch (err) {
      // ignore
    }
    return false;
  };

  const debugToggleBtn = document.getElementById('debugToggleBtn');
  const layoutRight = document.querySelector('.layout-right');
  if (debugToggleBtn && layoutRight) {
    debugToggleBtn.addEventListener('click', () => {
      const isOpen = layoutRight.classList.toggle('open');
      debugToggleBtn.textContent = isOpen ? 'Close Debug' : 'Layer Debug';
      debugToggleBtn.classList.toggle('active', isOpen);
    });
  }

  // Multi-select mode
  const multiSelectBtn = document.getElementById('multiSelectBtn');
  const multiSelectToolbar = document.getElementById('multiSelectToolbar');
  const multiSelectCount = document.getElementById('multiSelectCount');
  const multiCopyButton = document.getElementById('multiCopyButton');
  const multiCopyAlignedButton = document.getElementById('multiCopyAlignedButton');
  const multiClearButton = document.getElementById('multiClearButton');

  let multiSelectMode = false;
  // Map<descId, { layerEl, descItem }>
  const multiSelectedMap = new Map();

  const updateMultiToolbar = () => {
    const count = multiSelectedMap.size;
    if (multiSelectCount) multiSelectCount.textContent = `${count} selected`;
    if (multiSelectToolbar) multiSelectToolbar.classList.toggle('visible', multiSelectMode && count > 0);
  };

  const clearMultiSelection = () => {
    for (const { layerEl, descItem } of multiSelectedMap.values()) {
      layerEl.classList.remove('multi-selected');
      if (descItem) descItem.classList.remove('multi-selected');
    }
    multiSelectedMap.clear();
    updateMultiToolbar();
  };

  const toggleMultiItem = (layerEl) => {
    if (!layerEl) return;
    const descItem = resolveDescItem(layerEl);
    const descId = layerEl.getAttribute('data-layer-desc-id') || layerEl.getAttribute('data-layer-id') || '';
    if (!descId) return;
    if (multiSelectedMap.has(descId)) {
      multiSelectedMap.delete(descId);
      layerEl.classList.remove('multi-selected');
      if (descItem) descItem.classList.remove('multi-selected');
    } else {
      multiSelectedMap.set(descId, { layerEl, descItem });
      layerEl.classList.add('multi-selected');
      if (descItem) descItem.classList.add('multi-selected');
    }
    updateMultiToolbar();
  };

  if (multiSelectBtn) {
    multiSelectBtn.addEventListener('click', () => {
      multiSelectMode = !multiSelectMode;
      multiSelectBtn.classList.toggle('active', multiSelectMode);
      multiSelectBtn.textContent = multiSelectMode ? 'Exit Multi-Select' : 'Multi-Select';
      if (!multiSelectMode) clearMultiSelection();
      updateMultiToolbar();
    });
  }

  const copyMultiSelected = async (mode) => {
    const entries = Array.from(multiSelectedMap.values());
    if (!entries.length) return;
    const payloads = entries.map(({ descItem }) => {
      if (!descItem) return null;
      if (mode === 'minified') {
        return buildMinifiedPayload(descItem);
      }
      const data = descriptionToJSON(descItem);
      if (!data) return null;
      return JSON.stringify(enrichDescriptionJSON(data, descItem, [1]), null, 2);
    }).filter(Boolean);
    if (!payloads.length) return;
    const ok = await copyText(payloads.join('\n\n---\n\n'));
    showToast(ok ? `Copied ${payloads.length} layer(s)` : 'Copy failed');
  };

  if (multiCopyButton) {
    multiCopyButton.addEventListener('click', () => copyMultiSelected('minified').catch(() => showToast('Copy failed')));
  }
  if (multiCopyAlignedButton) {
    multiCopyAlignedButton.addEventListener('click', () => copyMultiSelected('aligned').catch(() => showToast('Copy failed')));
  }
  if (multiClearButton) {
    multiClearButton.addEventListener('click', clearMultiSelection);
  }
  // ──────────────────────────────────────────────────────────

  const instructionStorageKey = (appConfig && appConfig.dataset.storageKey) || 'zeplin-layer-instructions';
  const loadInstructionStore = () => {
    try {
      const raw = window.localStorage ? window.localStorage.getItem(instructionStorageKey) : null;
      if (!raw) return {};
      const parsed = JSON.parse(raw);
      return parsed && typeof parsed === 'object' ? parsed : {};
    } catch (err) {
      return {};
    }
  };
  const instructionStore = loadInstructionStore();
  const saveInstructionStore = () => {
    try {
      if (window.localStorage) {
        window.localStorage.setItem(instructionStorageKey, JSON.stringify(instructionStore));
      }
    } catch (err) {
      // ignore persistence failure
    }
  };
  const getInstructionText = (descId) => {
    if (!descId) return '';
    const value = instructionStore[descId];
    return typeof value === 'string' ? value : '';
  };
  const setInstructionText = (descId, value) => {
    if (!descId) return;
    const nextValue = String(value || '').trim();
    if (nextValue) instructionStore[descId] = nextValue;
    else delete instructionStore[descId];
    saveInstructionStore();
  };

  const contextMenu = document.getElementById('contextCopyMenu');
  const contextEditInstructionButton = document.getElementById('contextEditInstructionButton');
  const contextCopyButton = document.getElementById('contextCopyButton');
  const contextCopyAlignedButton = document.getElementById('contextCopyAlignedButton');
  if (minifiedTree && contextCopyButton) {
    contextCopyButton.textContent = 'Copy Prompt (Minified)';
  }
  let contextCopyPayload = '';
  let contextCopyAlignedPayload = '';
  let contextEditableItem = null;

  const hideContextMenu = () => {
    if (contextMenu) contextMenu.style.display = 'none';
    contextCopyPayload = '';
    contextCopyAlignedPayload = '';
    contextEditableItem = null;
  };

  const showContextMenu = (event, payloads = {}) => {
    if (!contextMenu) return;
    contextCopyPayload = payloads.raw || '';
    contextCopyAlignedPayload = payloads.aligned || '';
    contextEditableItem = payloads.editableItem || null;
    if (contextEditInstructionButton) {
      if (contextEditableItem) {
        const descId = contextEditableItem.getAttribute('data-layer-desc-id');
        contextEditInstructionButton.textContent = getInstructionText(descId) ? 'Edit Prompt' : 'Add Prompt';
        contextEditInstructionButton.style.display = '';
      } else {
        contextEditInstructionButton.style.display = 'none';
      }
    }
    contextMenu.style.display = 'flex';
    const offset = 8;
    contextMenu.style.left = (event.clientX + offset) + 'px';
    contextMenu.style.top = (event.clientY + offset) + 'px';
  };

  if (contextEditInstructionButton) {
    contextEditInstructionButton.addEventListener('click', () => {
      if (!contextEditableItem) return hideContextMenu();
      showInstructionEditor(contextEditableItem);
      hideContextMenu();
    });
  }

  if (contextCopyButton) {
    contextCopyButton.addEventListener('click', () => {
      if (!contextCopyPayload) return hideContextMenu();
      copyText(contextCopyPayload)
        .then(ok => showToast(ok ? null : 'Copy failed. Prompt dialog opened.'))
        .catch(() => showToast('Copy failed'));
      hideContextMenu();
    });
  }
  if (contextCopyAlignedButton) {
    contextCopyAlignedButton.addEventListener('click', () => {
      if (!contextCopyAlignedPayload) return hideContextMenu();
      copyText(contextCopyAlignedPayload)
        .then(ok => showToast(ok ? null : 'Copy failed. Prompt dialog opened.'))
        .catch(() => showToast('Copy failed'));
      hideContextMenu();
    });
  }

  const summariseStyle = (styleObj = {}) => {
    const entries = Object.entries(styleObj);
    if (!entries.length) return {};
    const result = {};
    for (const [key, value] of entries) {
      if (value != null && value !== '') result[key] = value;
    }
    return result;
  };

  const decodeHtml = (text) => {
    if (text == null) return '';
    const helper = document.createElement('textarea');
    helper.innerHTML = text;
    return helper.value;
  };

  const parseDataJSON = (target, key) => {
    const raw = target.getAttribute(key);
    if (!raw) return null;
    try { return JSON.parse(raw); } catch (e) { return null; }
  };

  const parsePathAttr = (item) => {
    if (!item) return [];
    const raw = item.getAttribute('data-layer-path');
    if (!raw) return [];
    return raw
      .split('.')
      .map(part => parseInt(part, 10))
      .filter(num => Number.isFinite(num) && num > 0);
  };

  const resolveMinifiedNode = (path) => {
    if (!minifiedRoot || !Array.isArray(path) || !path.length) return null;
    let node = minifiedRoot;
    let startIndex = 0;
    if (!minifiedRootWrapped) {
      if (path[0] !== 1) return null;
      startIndex = 1;
    }
    for (let i = startIndex; i < path.length; i += 1) {
      const idx = path[i] - 1;
      node = node?.c?.[idx];
      if (!node) return null;
    }
    return node;
  };

  const buildMinifiedPayload = (descItem) => {
    if (!minifiedTree || !minifiedRoot) return null;
    const path = parsePathAttr(descItem);
    if (!path.length) return null;
    const node = resolveMinifiedNode(path);
    if (!node) return null;
    const cloneMinifiedNodeWithInstructions = (minifiedNode, descNode) => {
      if (!minifiedNode) return null;
      const next = {
        ...minifiedNode
      };
      const descId = descNode?.getAttribute('data-layer-desc-id');
      const instruction = getInstructionText(descId);
      if (instruction) {
        next.p = instruction;
      }
      if (Array.isArray(minifiedNode.c) && minifiedNode.c.length) {
        const childDescItems = descNode
          ? Array.from(descNode.querySelectorAll(':scope > details > ul > li.layer-desc'))
          : [];
        next.c = minifiedNode.c.map((childNode, index) => {
          const childDesc = childDescItems[index] || null;
          return cloneMinifiedNodeWithInstructions(childNode, childDesc);
        });
      }
      return next;
    };
    const enrichedNode = cloneMinifiedNodeWithInstructions(node, descItem);
    const payload = JSON.stringify({
      v: minifiedTree.v,
      dict: minifiedTree.dict,
      root: enrichedNode
    });
    const prefix = [
      "How to Read:",
      "1. Root shape: {v, dict, root}",
      "2. dict.f: [fontFamily, fontName, fontSize, fontWeight, lineHeight]",
      "3. dict.c: color string (rgba/hex)",
      "4. dict.i: image name or url",
      "5. Node fields: t(type), f([x,y,w,h]), c(children), x(text), fn(fontId), cl(colorId), i(imageId), ru(text runs), p(instruction)",
      "6. Resolve fn/cl/i through dict; root is the selected subtree"
    ].join("\n");
    return prefix + "\n\n" + payload;
  };

  const fitTextWithinFrame = (textEl) => {
    if (!textEl) return;
    const container = textEl.parentElement;
    if (!container) return;
    const maxLetterTighten = -1.5;
    const letterStep = -0.25;
    const computed = window.getComputedStyle(textEl);
    let letterSpacing = parseFloat(computed.letterSpacing);
    if (!Number.isFinite(letterSpacing)) letterSpacing = 0;

    const isOverflowing = () =>
      textEl.scrollWidth > container.clientWidth || textEl.scrollHeight > container.clientHeight;

    let guard = 0;
    while (guard < 12 && isOverflowing() && letterSpacing + letterStep >= maxLetterTighten) {
      letterSpacing += letterStep;
      textEl.style.letterSpacing = String(letterSpacing) + "px";
      guard += 1;
    }

    // line-height tightening disabled by request
  };

  const canvas = document.querySelector('.canvas');
  const previewInstructionEditor = document.getElementById('previewInstructionEditor');
  const previewInstructionTitle = document.getElementById('previewInstructionTitle');
  const previewInstructionTextarea = document.getElementById('previewInstructionTextarea');
  const previewInstructionSaveButton = document.getElementById('previewInstructionSaveButton');
  const previewInstructionCloseButton = document.getElementById('previewInstructionCloseButton');
  let highlight = null;
  let tooltip = null;
  if (canvas) {
    highlight = document.getElementById('layerHighlight');
    if (!highlight) {
      highlight = document.createElement('div');
      highlight.id = 'layerHighlight';
      canvas.appendChild(highlight);
    }
  }

  const fitAllText = () => {
    document.querySelectorAll('.text-content').forEach(fitTextWithinFrame);
  };
  window.requestAnimationFrame(() => window.requestAnimationFrame(fitAllText));

  let currentTarget = null;
  let lastPreviewClick = null;
  const hoverNodes = [];
  const selectedNodes = [];

  const descriptionSection = document.querySelector('.description-panel');
  const descriptionList = document.getElementById('layerDescriptionList');
  const descriptionItemsById = new Map();
  const registerDescItem = (key, item) => {
    if (!key) return;
    if (!descriptionItemsById.has(key)) descriptionItemsById.set(key, item);
  };
  if (descriptionList) {
    descriptionList.querySelectorAll('.layer-desc[data-layer-desc-id]').forEach(item => {
      const id = item.getAttribute('data-layer-desc-id');
      const originalId = item.getAttribute('data-layer-original-id');
      registerDescItem(id, item);
      registerDescItem(originalId, item);
    });
  }
  const updateInstructionMarker = (item) => {
    if (!item) return;
    const descId = item.getAttribute('data-layer-desc-id');
    const hasInstruction = Boolean(getInstructionText(descId));
    item.classList.toggle('has-instruction', hasInstruction);
    let layerEl = null;
    if (canvas && descId) {
      const safeId = (window.CSS && window.CSS.escape) ? window.CSS.escape(descId) : descId.replace(/"/g, '"');
      layerEl = canvas.querySelector('.layer[data-layer-desc-id="' + safeId + '"]');
    }
    if (layerEl) {
      layerEl.classList.toggle('has-instruction', hasInstruction);
    }
  };
  let activeInstructionItem = null;
  const hideInstructionEditor = () => {
    if (previewInstructionEditor) previewInstructionEditor.classList.remove('visible');
    activeInstructionItem = null;
  };
  const saveInstructionEditor = () => {
    if (!activeInstructionItem || !previewInstructionTextarea) return;
    const descId = activeInstructionItem.getAttribute('data-layer-desc-id');
    setInstructionText(descId, previewInstructionTextarea.value);
    updateInstructionMarker(activeInstructionItem);
  };
  const showInstructionEditor = (item) => {
    if (!item || !previewInstructionEditor || !previewInstructionTextarea) return;
    activeInstructionItem = item;
    const descId = item.getAttribute('data-layer-desc-id');
    const summary = item.querySelector(':scope > details > summary');
    const titleText = summary ? summary.textContent.trim() : 'Edit Prompt';
    if (previewInstructionTitle) {
      previewInstructionTitle.textContent = 'Edit Prompt: ' + titleText;
    }
    previewInstructionTextarea.value = getInstructionText(descId);
    previewInstructionEditor.classList.add('visible');
    previewInstructionTextarea.focus();
    previewInstructionTextarea.setSelectionRange(
      previewInstructionTextarea.value.length,
      previewInstructionTextarea.value.length
    );
  };
  if (previewInstructionTextarea) {
    previewInstructionTextarea.addEventListener('keydown', (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
        saveInstructionEditor();
        hideInstructionEditor();
      }
    });
  }
  if (previewInstructionSaveButton) {
    previewInstructionSaveButton.addEventListener('click', () => {
      saveInstructionEditor();
      hideInstructionEditor();
    });
  }
  if (previewInstructionCloseButton) {
    previewInstructionCloseButton.addEventListener('click', hideInstructionEditor);
  }
  if (descriptionList) {
    descriptionList.querySelectorAll('.layer-desc[data-layer-desc-id]').forEach(updateInstructionMarker);
  }
  const hoveredDescItems = [];
  const selectedDescItems = [];
  const getLayerKey = (el) => (
    el?.getAttribute('data-layer-original-id') ||
    el?.getAttribute('data-layer-desc-id') ||
    el?.getAttribute('data-layer-id') ||
    ""
  );
  const resolveDescItem = (layerEl) => {
    let cur = layerEl;
    while (cur && cur !== canvas) {
      const id = getLayerKey(cur);
      if (id && descriptionItemsById.has(id)) {
        return descriptionItemsById.get(id);
      }
      cur = cur.parentElement?.closest('.layer');
    }
    return null;
  };

  const clearDescHover = () => {
    while (hoveredDescItems.length) {
      const el = hoveredDescItems.pop();
      el.classList.remove('hovered');
    }
  };

  const applyDescHover = (layerEl) => {
    clearDescHover();
    if (!layerEl) return;
    let matched = false;
    const stack = [layerEl, ...layerEl.querySelectorAll('.layer')];
    for (const el of stack) {
      const id = getLayerKey(el);
      if (!id) continue;
      const desc = descriptionItemsById.get(id);
      if (desc) {
        desc.classList.add('hovered');
        hoveredDescItems.push(desc);
        matched = true;
      }
    }
    if (!matched) {
      const fallback = resolveDescItem(layerEl);
      if (fallback) {
        fallback.classList.add('hovered');
        hoveredDescItems.push(fallback);
      }
    }
  };

  const clearDescSelected = () => {
    while (selectedDescItems.length) {
      const el = selectedDescItems.pop();
      el.classList.remove('selected');
    }
  };

  const scrollDescToPreferredSpot = (element) => {
    if (!element) return;
    if (typeof element.scrollIntoView === 'function') {
      element.scrollIntoView({ block: 'center', inline: 'nearest', behavior: 'smooth' });
      return;
    }
    const container = descriptionList || descriptionSection;
    if (!container) return;
    const containerRect = container.getBoundingClientRect();
    const elementRect = element.getBoundingClientRect();
    const distanceFromTop = elementRect.top - containerRect.top;
    const targetOffset = distanceFromTop - container.clientHeight * 0.25;
    container.scrollBy({ top: targetOffset, behavior: 'smooth' });
  };

  const applyDescSelected = (layerEl, options = {}) => {
    clearDescSelected();
    if (!layerEl) return;
    let primaryDesc = null;
    let matched = false;
    const stack = [layerEl, ...layerEl.querySelectorAll('.layer')];
    for (const el of stack) {
      const id = getLayerKey(el);
      if (!id) continue;
      const desc = descriptionItemsById.get(id);
      if (desc) {
        if (!primaryDesc) primaryDesc = desc;
        desc.classList.add('selected');
        selectedDescItems.push(desc);
        matched = true;
      }
    }
    if (!matched) {
      const fallback = resolveDescItem(layerEl);
      if (fallback) {
        primaryDesc = primaryDesc || fallback;
        fallback.classList.add('selected');
        selectedDescItems.push(fallback);
      }
    }
    if (primaryDesc && options.scroll !== false) {
      scrollDescToPreferredSpot(primaryDesc);
    }
  };

  let clearSelection = () => {};

  const clearHoverClasses = () => {
    while (hoverNodes.length) {
      const el = hoverNodes.pop();
      el.classList.remove('hover-target', 'hover-descendant');
    }
    clearDescHover();
  };

  const applyHoverClasses = (target) => {
    clearHoverClasses();
    if (!target) return;
    target.classList.add('hover-target');
    hoverNodes.push(target);
    const descendants = target.querySelectorAll('.layer');
    descendants.forEach(desc => {
      if (desc === target) return;
      desc.classList.add('hover-descendant');
      hoverNodes.push(desc);
    });
    applyDescHover(target);
  };

  const clearSelectedClasses = () => {
    while (selectedNodes.length) {
      const el = selectedNodes.pop();
      el.classList.remove('selected-target', 'selected-descendant');
    }
    clearDescSelected();
  };

  const applySelectedClasses = (target, options = {}) => {
    clearSelectedClasses();
    if (!target) return;
    target.classList.add('selected-target');
    selectedNodes.push(target);
    const descendants = target.querySelectorAll('.layer');
    descendants.forEach(desc => {
      if (desc === target) return;
      desc.classList.add('selected-descendant');
      selectedNodes.push(desc);
    });
    applyDescSelected(target, { scroll: options.scrollDesc !== false });
  };

  const hideHover = () => {
    if (highlight) highlight.style.display = 'none';
    if (tooltip) tooltip.style.display = 'none';
    currentTarget = null;
    clearHoverClasses();
  };

  clearSelection = () => {
    clearSelectedClasses();
    lastPreviewClick = null;
  };

  if (descriptionList) {
    descriptionList.addEventListener('click', (event) => {
      const item = event.target.closest('.layer-desc[data-layer-desc-id]');
      if (!item) return;
      const layerId = item.getAttribute('data-layer-original-id') || item.getAttribute('data-layer-desc-id');
      if (!layerId || !canvas) return;
      const safeId = (window.CSS && window.CSS.escape) ? window.CSS.escape(layerId) : layerId.replace(/"/g, '"');
      const selector = '.layer[data-layer-original-id="' + safeId + '"], .layer[data-layer-id="' + safeId + '"]';
      const targetLayer = canvas.querySelector(selector);
      if (!targetLayer) return;
      lastPreviewClick = null;
      applyHoverClasses(targetLayer);
      applySelectedClasses(targetLayer, { scrollDesc: true });
    });
  }

  const describeLayer = (el) => {
    const descAttr = decodeHtml(el.getAttribute('data-layer-desc'));
    const name = decodeHtml(el.getAttribute('data-layer-name'));
    const type = Array.from(el.classList).find(cls => cls.startsWith('layer-'))?.replace('layer-', '');
    const id = el.getAttribute('data-layer-id');
    if (descAttr) return descAttr;
    const parts = [];
    if (name) parts.push('Name: ' + name);
    if (type) parts.push('Type: ' + type);
    if (id) parts.push('ID: ' + id);
    return parts.length ? parts.join(' · ') : 'Unnamed Layer';
  };

  const collectLayerDescriptions = (el, depth = 0, lines = []) => {
    const indent = depth ? '• '.repeat(depth) : '';
    lines.push(indent + describeLayer(el));
    const childNodes = Array.from(el.children).filter(child => child.classList.contains('layer'));
    for (let i = 0; i < childNodes.length; i++) {
      const child = childNodes[i];
      collectLayerDescriptions(child, depth + 1, lines);
    }
    return lines;
  };

  const collectDescSummaries = (item, lines = []) => {
    if (!item) return lines;
    const summary = item.querySelector(':scope > details > summary');
    if (summary) {
      lines.push(summary.textContent.trim());
    }
    const children = item.querySelectorAll(':scope > details > ul > li.layer-desc');
    children.forEach(child => collectDescSummaries(child, lines));
    return lines;
  };

  const applyTooltip = () => {};

  const updateHighlight = (target) => {
    if (!highlight || !canvas || !target) return;
    const rect = target.getBoundingClientRect();
    const canvasRect = canvas.getBoundingClientRect();
    highlight.style.left = (rect.left - canvasRect.left) + 'px';
    highlight.style.top = (rect.top - canvasRect.top) + 'px';
    highlight.style.width = Math.max(rect.width, 1) + 'px';
    highlight.style.height = Math.max(rect.height, 1) + 'px';
    highlight.style.display = 'block';
  };

  const buildPreviewTargetChain = (target) => {
    const chain = [];
    let cur = target;
    const seen = new Set();
    while (cur && cur !== canvas) {
      if (seen.has(cur)) break;
      seen.add(cur);
      if (resolveDescItem(cur)) {
        chain.push(cur);
      }
      cur = cur.parentElement?.closest('.layer');
    }
    return chain;
  };

  const resolvePreviewTarget = (event, options = {}) => {
    if (!canvas || !event) return null;
    const directTarget = event.target?.closest?.('.layer');
    const sourceElements = typeof document.elementsFromPoint === 'function'
      ? document.elementsFromPoint(event.clientX, event.clientY)
      : [event.target];
    const seen = new Set();
    const candidates = [];

    for (const sourceEl of sourceElements) {
      const layerEl = sourceEl?.closest?.('.layer');
      if (!layerEl || !canvas.contains(layerEl) || seen.has(layerEl)) continue;
      seen.add(layerEl);
      if (!resolveDescItem(layerEl)) continue;
      candidates.push(layerEl);
    }

    const preferred = candidates.length ? candidates[0] : (directTarget && canvas.contains(directTarget) ? directTarget : null);
    if (!preferred) return null;

    if (options.cycleFromSelected && lastPreviewClick && selectedNodes.length) {
      const sameSpot = Math.abs(lastPreviewClick.x - event.clientX) <= 4 &&
        Math.abs(lastPreviewClick.y - event.clientY) <= 4;
      if (sameSpot) {
        const chain = buildPreviewTargetChain(preferred);
        const selectedKey = getLayerKey(selectedNodes[0]);
        const selectedIndex = chain.findIndex(item => getLayerKey(item) === selectedKey);
        if (selectedIndex !== -1 && selectedIndex + 1 < chain.length) {
          return chain[selectedIndex + 1];
        }
      }
    }

    return preferred;
  };

  const handleMouseMove = (event) => {
    if (!canvas) return;
    const target = resolvePreviewTarget(event);
    if (!target || !canvas.contains(target)) {
      hideHover();
      return;
    }
    if (currentTarget !== target) {
      currentTarget = target;
      updateHighlight(target);
      applyHoverClasses(target);
    } else if (highlight && highlight.style.display === 'none') {
      updateHighlight(target);
      applyHoverClasses(target);
    }
    applyTooltip(event, target);
  };

  const handleClick = (event) => {
    if (!canvas) return;
    if (multiSelectMode) {
      const target = resolvePreviewTarget(event);
      if (!target || !canvas.contains(target)) return;
      event.preventDefault();
      toggleMultiItem(target);
      return;
    }
    const target = resolvePreviewTarget(event, { cycleFromSelected: true });
    if (!target || !canvas.contains(target)) return;
    event.preventDefault();
    lastPreviewClick = { x: event.clientX, y: event.clientY };
    applySelectedClasses(target, { scrollDesc: true });
    applySelectedClasses(target, { scrollDesc: true });
  };

  const descriptionToJSON = (item) => {
    if (!item) return null;
    const serialiseDescNode = (li) => {
      const summary = li.querySelector(':scope > details > summary');
      const text = summary ? summary.textContent.trim() : '';
      const match = text.match(/^•*\s*([^·]+) · (.*)$/);
      const name = match ? match[1].trim() : text;
      const metaRaw = match ? match[2].trim() : '';
      const node = { title: name };
      if (metaRaw) {
        const attrs = metaRaw.split('·').map(part => part.trim()).filter(Boolean);
        const metaObj = {};
        for (const attr of attrs) {
          if (!attr) continue;
          if (attr.toLowerCase().startsWith('constraints:')) {
            const [, constraintBodyRaw = ''] = attr.split(':', 2);
            const constraintPairs = constraintBodyRaw.split(',').map(s => s.trim()).filter(Boolean);
            const constraintObj = {};
            for (const pair of constraintPairs) {
              const [ck, ...cRest] = pair.split('=');
              const cKey = ck ? ck.trim() : null;
              const cVal = cRest.length ? cRest.join('=').trim() : null;
              if (!cKey) continue;
              constraintObj[cKey] = cVal ?? true;
            }
            if (Object.keys(constraintObj).length) {
              metaObj.constraints = constraintObj;
            }
            continue;
          }
          const [k, ...restParts] = attr.split('=');
          const key = k ? k.trim() : null;
          const value = restParts.length ? restParts.join('=').trim() : null;
          if (!key) continue;
          metaObj[key] = value ?? true;
        }
        if (Object.keys(metaObj).length) node.meta = metaObj;
      }
      if (canvas) {
        const descId = li.getAttribute('data-layer-desc-id');
        const instruction = getInstructionText(descId);
        if (instruction) {
          node.instruction = instruction;
        }
        if (descId) {
          const safeId = (window.CSS && window.CSS.escape) ? window.CSS.escape(descId) : descId.replace(/"/g, '"');
          const layerEl = canvas.querySelector('.layer[data-layer-desc-id="' + safeId + '"]');
          if (layerEl) {
            const imageInfo = parseDataJSON(layerEl, 'data-layer-image');
            if (imageInfo?.imgUrl) {
              node.imgUrl = imageInfo.imgUrl;
            }
          }
        }
      }
      const children = Array.from(li.querySelectorAll(':scope > details > ul > li.layer-desc')).map(child => serialiseDescNode(child));
      if (children.length) node.children = children;
      return node;
    };
    return serialiseDescNode(item);
  };

  const parsePixelValue = (value) => {
    if (value == null) return null;
    const num = parseFloat(String(value).replace('px', ''));
    return Number.isFinite(num) ? num : null;
  };

  const getElementSize = (el) => {
    if (!el) return { width: null, height: null };
    if (el === canvas) {
      const width = parsePixelValue(canvas.style.width) ?? canvas.clientWidth ?? null;
      const height = parsePixelValue(canvas.style.height) ?? canvas.clientHeight ?? null;
      return { width, height };
    }
    const style = parseDataJSON(el, 'data-layer-style') || {};
    const width = parsePixelValue(style.width);
    const height = parsePixelValue(style.height);
    if (width != null || height != null) {
      return { width, height };
    }
    const rect = el.getBoundingClientRect();
    return { width: rect.width || null, height: rect.height || null };
  };

  const resolveLayerElement = (descItem) => {
    if (!descItem || !canvas) return null;
    const descId = descItem.getAttribute('data-layer-desc-id');
    if (!descId) return null;
    const safeId = (window.CSS && window.CSS.escape) ? window.CSS.escape(descId) : descId.replace(/"/g, '"');
    return canvas.querySelector('.layer[data-layer-desc-id="' + safeId + '"]');
  };

  const computeAlignment = (layerEl) => {
    if (!layerEl) return null;
    const parentLayer = layerEl.parentElement?.closest('.layer') || canvas;
    const style = parseDataJSON(layerEl, 'data-layer-style') || {};
    const left = parsePixelValue(style.left);
    const top = parsePixelValue(style.top);
    const width = parsePixelValue(style.width);
    const height = parsePixelValue(style.height);
    const parentSize = getElementSize(parentLayer);
    if (
      left == null || top == null || width == null || height == null ||
      parentSize.width == null || parentSize.height == null
    ) {
      return null;
    }
    const right = parentSize.width - (left + width);
    const bottom = parentSize.height - (top + height);
    const centerX = left + width / 2;
    const centerY = top + height / 2;
    const parentCenterX = parentSize.width / 2;
    const parentCenterY = parentSize.height / 2;
    const epsilon = 0.5;
    const approx = (a, b) => Math.abs(a - b) <= epsilon;
    let horizontal = 'custom';
    if (approx(left, 0) && approx(right, 0)) horizontal = 'stretch';
    else if (approx(left, 0)) horizontal = 'left';
    else if (approx(right, 0)) horizontal = 'right';
    else if (approx(centerX, parentCenterX)) horizontal = 'center';
    let vertical = 'custom';
    if (approx(top, 0) && approx(bottom, 0)) vertical = 'stretch';
    else if (approx(top, 0)) vertical = 'top';
    else if (approx(bottom, 0)) vertical = 'bottom';
    else if (approx(centerY, parentCenterY)) vertical = 'center';
    const round = (value) => Math.round(value * 100) / 100;
    return {
      horizontal,
      vertical,
      offsets: {
        left: round(left),
        right: round(right),
        top: round(top),
        bottom: round(bottom)
      }
    };
  };

  const computeConstraintsFromEntries = (entries, parentEl) => {
    if (!entries.length) return;
    const parentSize = getElementSize(parentEl);
    const epsilon = 0.5;
    const round = (value) => Math.round(value * 100) / 100;
    const rangesOverlap = (a1, a2, b1, b2) => Math.max(a1, b1) < Math.min(a2, b2);
    const items = [];
    const entryById = new Map();
    for (const entry of entries) {
      const style = parseDataJSON(entry.el, 'data-layer-style') || {};
      const x = parsePixelValue(style.left);
      const y = parsePixelValue(style.top);
      const w = parsePixelValue(style.width);
      const h = parsePixelValue(style.height);
      const id = entry.node?.id;
      if (id == null || x == null || y == null || w == null || h == null) continue;
      const item = { id, x, y, w, h };
      items.push(item);
      entryById.set(id, entry);
    }
    if (!items.length) return;
    const maxRight = Number.isFinite(parentSize.width)
      ? parentSize.width
      : Math.max(...items.map(i => i.x + i.w));
    const maxBottom = Number.isFinite(parentSize.height)
      ? parentSize.height
      : Math.max(...items.map(i => i.y + i.h));
    const sorted = [...items].sort((a, b) => (a.y - b.y) || (a.x - b.x));
    for (const cur of sorted) {
      const sameRow = sorted.filter(i => i.id !== cur.id && Math.abs(i.y - cur.y) <= epsilon);
      const sameCol = sorted.filter(i => i.id !== cur.id && Math.abs(i.x - cur.x) <= epsilon);
      const leftCandidates = sorted.filter(
        i =>
          i.id !== cur.id &&
          i.x + i.w <= cur.x + epsilon &&
          rangesOverlap(i.y, i.y + i.h, cur.y, cur.y + cur.h)
      );
      const topCandidates = sorted.filter(
        i =>
          i.id !== cur.id &&
          i.y + i.h <= cur.y + epsilon &&
          rangesOverlap(i.x, i.x + i.w, cur.x, cur.x + cur.w)
      );
      const leftNeighbor = leftCandidates.sort((a, b) => (b.x + b.w) - (a.x + a.w))[0];
      const topNeighbor = topCandidates.sort((a, b) => (b.y + b.h) - (a.y + a.h))[0];
      const c = {};
      if (sameCol.length) {
        const anchor = sameCol.sort((a, b) => a.y - b.y)[0];
        c.left = cur.id + ".left = " + anchor.id + ".left";
      } else if (sameRow.length && leftNeighbor) {
        const offset = round(cur.x - (leftNeighbor.x + leftNeighbor.w));
        c.left = cur.id + ".left = " + leftNeighbor.id + ".right + " + offset;
      } else {
        c.left = cur.id + ".left = super.left + " + round(cur.x);
      }
      if (topNeighbor) {
        const offset = round(cur.y - (topNeighbor.y + topNeighbor.h));
        c.top = cur.id + ".top = " + topNeighbor.id + ".bottom + " + offset;
      } else if (sameRow.length) {
        const anchor = sameRow.sort((a, b) => a.x - b.x)[0];
        c.top = cur.id + ".top = " + anchor.id + ".top";
      } else {
        c.top = cur.id + ".top = super.top + " + round(cur.y);
      }
      const rightInset = round(maxRight - (cur.x + cur.w));
      const bottomInset = round(maxBottom - (cur.y + cur.h));
      c.right = cur.id + ".right = super.right - " + rightInset;
      c.bottom = cur.id + ".bottom = super.bottom - " + bottomInset;
      const entry = entryById.get(cur.id);
      if (!entry) continue;
      entry.node.meta = entry.node.meta || {};
      entry.node.meta.constraints = c;
    }
  };

  const getStableNodeId = (descItem, layerEl, path) => {
    const originalId = layerEl?.getAttribute('data-layer-original-id');
    if (originalId) return originalId;
    const descId = descItem?.getAttribute('data-layer-desc-id');
    if (descId) return descId;
    const layerId = layerEl?.getAttribute('data-layer-id');
    if (layerId) return layerId;
    const pathKey = path.length ? path.join("_") : "root";
    return "node_" + pathKey;
  };

  const buildAttributedString = (textRuns) => {
    if (!Array.isArray(textRuns) || textRuns.length <= 1) return null;
    const attributedString = textRuns
      .map(run => {
        const style = run?.style || {};
        const entry = {
          text: typeof run?.text === 'string' ? run.text : ''
        };
        if (style.color) entry.color = style.color;
        if (style.colorHex) entry.colorHex = style.colorHex;
        if (style.colorName) entry.colorName = style.colorName;
        if (style.fontSize) entry.fontSize = style.fontSize;
        if (style.fontWeight) entry.fontWeight = style.fontWeight;
        if (style.fontFamily || style.fontPostscriptName) entry.fontFamily = style.fontFamily || style.fontPostscriptName;
        if (style.fontName) entry.fontName = style.fontName;
        return entry;
      })
      .filter(run => run.text);
    return attributedString.length > 1 ? attributedString : null;
  };

  const enrichDescriptionJSON = (node, descItem, path = []) => {
    if (!node || !descItem) return node;
    const layerEl = resolveLayerElement(descItem);
    const stableId = getStableNodeId(descItem, layerEl, path);
    const next = {
      ...node,
      id: stableId,
      meta: node.meta
        ? {
            ...node.meta,
            constraints: node.meta.constraints ? { ...node.meta.constraints } : undefined
          }
        : undefined
    };
    if (layerEl) {
      const layerId = layerEl.getAttribute('data-layer-id');
      if (layerId) next.layerId = layerId;
      const imageInfo = parseDataJSON(layerEl, 'data-layer-image');
      if (imageInfo?.imgUrl) next.imgUrl = imageInfo.imgUrl;
      const textRuns = parseDataJSON(layerEl, 'data-layer-text-runs');
      const attributedString = buildAttributedString(textRuns);
      if (attributedString) next.attributedString = attributedString;
    }
    const alignment = computeAlignment(layerEl);
    if (alignment) next.alignment = alignment;
    const childItems = Array.from(descItem.querySelectorAll(':scope > details > ul > li.layer-desc'));
    if (node.children && childItems.length) {
      const childEntries = [];
      next.children = node.children.map((child, index) => {
        const childItem = childItems[index];
        const childNode = enrichDescriptionJSON(child, childItem, path.concat(index + 1));
        const childEl = resolveLayerElement(childItem);
        if (childEl && childNode) {
          childEntries.push({ node: childNode, el: childEl });
        }
        return childNode;
      });
      if (childEntries.length) {
        childEntries.sort((a, b) => {
          const aStyle = parseDataJSON(a.el, 'data-layer-style') || {};
          const bStyle = parseDataJSON(b.el, 'data-layer-style') || {};
          const aTop = parsePixelValue(aStyle.top) ?? 0;
          const bTop = parsePixelValue(bStyle.top) ?? 0;
          if (aTop !== bTop) return aTop - bTop;
          const aLeft = parsePixelValue(aStyle.left) ?? 0;
          const bLeft = parsePixelValue(bStyle.left) ?? 0;
          return aLeft - bLeft;
        });
        next.children = childEntries.map(entry => entry.node);
        const parentEl = layerEl || canvas;
        if (parentEl) computeConstraintsFromEntries(childEntries, parentEl);
      }
    }
    return next;
  };

  if (canvas) {
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseleave', hideHover);
    canvas.addEventListener('click', handleClick);
  }

  document.addEventListener('click', (event) => {
    const inMenu = contextMenu && contextMenu.contains(event.target);
    if (!inMenu) hideContextMenu();
    if (descriptionSection && descriptionSection.contains(event.target)) return;
    if (canvas && canvas.contains(event.target)) return;
    clearSelection();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      clearSelection();
      hideContextMenu();
      hideInstructionEditor();
    }
  });

  const serialiseLayerNode = (el) => {
    const style = parseDataJSON(el, 'data-layer-style');
    const textStyle = parseDataJSON(el, 'data-layer-text-style');
    const textRuns = parseDataJSON(el, 'data-layer-text-runs');
    const imageInfo = parseDataJSON(el, 'data-layer-image');
    const gradientInfo = parseDataJSON(el, 'data-layer-gradient');
    const descId = el.getAttribute('data-layer-desc-id');
    const node = {
      id: el.getAttribute('data-layer-id') || undefined,
      name: el.getAttribute('data-layer-name') || undefined,
      type: Array.from(el.classList).find(cls => cls.startsWith('layer-'))?.replace('layer-', '') || undefined,
      relativeStyle: summariseStyle(style),
      textStyle: summariseStyle(textStyle),
      children: []
    };

    const textContent = el.querySelector('.text-content');
    if (textContent) {
      node.text = textContent.textContent || '';
    }
    const attributedString = buildAttributedString(textRuns);
    if (attributedString) {
      node.attributedString = attributedString;
    }
    const constraints = parseDataJSON(el, 'data-layer-constraints');
    if (constraints && Object.keys(constraints).length) {
      node.constraints = constraints;
    }
    if (imageInfo) {
      node.image = imageInfo;
      if (imageInfo.imgUrl) {
        node.imgUrl = imageInfo.imgUrl;
      }
    }
    if (gradientInfo) {
      node.gradient = gradientInfo;
      if (gradientInfo.description) {
        node.gradientColor = gradientInfo.description;
      }
    }
    const instruction = getInstructionText(descId);
    if (instruction) {
      node.instruction = instruction;
    }

    const childNodes = Array.from(el.children).filter(child => child.classList.contains('layer'));
    for (const child of childNodes) {
      node.children.push(serialiseLayerNode(child));
    }
    if (!node.children.length) delete node.children;
    if (!Object.keys(node.relativeStyle).length) delete node.relativeStyle;
    if (!node.textStyle || !Object.keys(node.textStyle).length) delete node.textStyle;
    return node;
  };

  const serialiseLayerTree = (root) => {
    const rootNode = serialiseLayerNode(root);
    const buildRelativeFrame = (node, parentLeft = 0, parentTop = 0) => {
      const style = node.relativeStyle || {};
      const left = parseFloat((style.left || '0').replace('px',''));
      const top = parseFloat((style.top || '0').replace('px',''));
      const width = parseFloat((style.width || '0').replace('px',''));
      const height = parseFloat((style.height || '0').replace('px',''));
      node.frame = {
        x: Number.isFinite(left) ? left : 0,
        y: Number.isFinite(top) ? top : 0,
        width: Number.isFinite(width) ? width : undefined,
        height: Number.isFinite(height) ? height : undefined
      };
      node.absoluteFrame = {
        x: parentLeft + (node.frame.x || 0),
        y: parentTop + (node.frame.y || 0),
        width: node.frame.width,
        height: node.frame.height
      };
      if (node.children) {
        for (const child of node.children) {
          buildRelativeFrame(child, node.absoluteFrame.x || 0, node.absoluteFrame.y || 0);
        }
      }
    };
    buildRelativeFrame(rootNode, 0, 0);
    return rootNode;
  };

  const handlePreviewContextMenu = (event) => {
    if (!canvas) return;
    const target = resolvePreviewTarget(event);
    if (!target || !canvas.contains(target)) return;
    event.preventDefault();
    event.stopPropagation();
    let descItem = resolveDescItem(target);
    if (!descItem && descriptionList) {
      const safeEscape = (value) => (
        (window.CSS && window.CSS.escape)
          ? window.CSS.escape(value)
          : value.replace(/"/g, '"')
      );
      const originalId = target.getAttribute('data-layer-original-id');
      if (originalId) {
        const selector = '.layer-desc[data-layer-original-id="' + safeEscape(originalId) + '"]';
        descItem = descriptionList.querySelector(selector);
      }
      if (!descItem) {
        const layerId = target.getAttribute('data-layer-id');
        if (layerId) {
          const selector = '.layer-desc[data-layer-desc-id="' + safeEscape(layerId) + '"]';
          descItem = descriptionList.querySelector(selector);
        }
      }
    }
    if (!descItem) return;
    const data = descriptionToJSON(descItem);
    if (!data) return;
    const aligned = enrichDescriptionJSON(data, descItem, [1]);
    const minifiedPayload = buildMinifiedPayload(descItem);
    showContextMenu(event, {
      editableItem: descItem,
      raw: minifiedPayload || JSON.stringify(data, null, 2),
      aligned: JSON.stringify(aligned, null, 2)
    });
  };

  if (canvas) {
    canvas.addEventListener('contextmenu', handlePreviewContextMenu);
  }
})();
