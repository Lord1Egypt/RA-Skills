(() => {
  'use strict';

  const deck = document.getElementById('deck');
  const runtime = window.TaoHtmlRuntime;
  const editToggle = document.getElementById('editToggle');
  const modeToggle = document.getElementById('modeToggle');
  if (!deck || !runtime || typeof runtime.setEditing !== 'function' || !editToggle) return;

  const VERSION = 1;
  const HISTORY_LIMIT = 100;
  const LOCK_SELECTOR = '[data-taohtml-edit-lock], [data-taohtml-edit="off"], [aria-hidden="true"]';
  const DISALLOWED_TEXT_TAGS = new Set([
    'INPUT', 'TEXTAREA', 'SELECT', 'OPTION', 'SCRIPT', 'STYLE',
    'NOSCRIPT', 'TEMPLATE', 'SVG', 'MATH', 'VIDEO', 'AUDIO', 'CANVAS', 'IFRAME',
    'OBJECT', 'EMBED',
  ]);
  const sessionKey = `taohtml:editor:v${VERSION}:${location.pathname}${location.search}`;
  const textTargets = new Map();
  const imageTargets = new Map();
  const undoStack = [];
  const redoStack = [];
  const lastTextValues = new Map();
  const reportIrTextBaseline = new Map();
  const reportIrImageBaseline = new Map();
  const REPORT_IR_PATCH_ID = 'taohtml-report-ir-runtime-patch';
  let active = false;
  let dirty = false;
  let recoveryAvailable = true;
  let pendingText = null;
  let pendingTextTimer = null;
  let pendingImageRead = null;
  let selectedImage = null;
  let toastTimer = null;
  let suppressMutations = false;
  let sourceBaseline;
  let checkpointBaseline;
  let documentSignature;
  let existingReportIrPatch = null;

  function isLocked(element) {
    return Boolean(element.closest(LOCK_SELECTOR));
  }

  function hasDirectText(element) {
    return [...element.childNodes].some(
      node => node.nodeType === Node.TEXT_NODE && Boolean(node.textContent.trim()),
    );
  }

  function isHardDisallowedTextTarget(element) {
    return DISALLOWED_TEXT_TAGS.has(element.localName.toUpperCase());
  }

  function discoverTextTargets() {
    const found = [];
    deck.querySelectorAll('.slide').forEach((slide, slideIndex) => {
      const candidates = [...slide.querySelectorAll('*')].filter(element => {
        if (isLocked(element)) return false;
        if (isHardDisallowedTextTarget(element)) return false;
        if (element.dataset.taohtmlEdit === 'text') return true;
        if (element.hasAttribute('contenteditable')) return false;
        return hasDirectText(element);
      });
      const forced = candidates.filter(element => element.dataset.taohtmlEdit === 'text');
      const forcedSet = new Set(forced);
      const candidateSet = new Set(candidates);
      const outermost = candidates.filter(element => {
        if (forcedSet.has(element)) return true;
        if (forced.some(target => element.contains(target) || target.contains(element))) return false;
        let ancestor = element.parentElement;
        while (ancestor && ancestor !== slide) {
          if (candidateSet.has(ancestor)) return false;
          ancestor = ancestor.parentElement;
        }
        return true;
      });
      outermost.forEach((element, ordinal) => {
        const id = `text:${slideIndex}:${ordinal}`;
        element.dataset.taohtmlEditorId = id;
        element.dataset.taohtmlEditorKind = 'text';
        textTargets.set(id, element);
        lastTextValues.set(id, element.innerHTML);
        found.push(element);
      });
    });
    return found;
  }

  function discoverImageTargets() {
    const found = [];
    deck.querySelectorAll('.slide').forEach((slide, slideIndex) => {
      [...slide.querySelectorAll('img')]
        .filter(image => !isLocked(image))
        .forEach((image, ordinal) => {
          const id = `image:${slideIndex}:${ordinal}`;
          image.dataset.taohtmlEditorId = id;
          image.dataset.taohtmlEditorKind = 'image';
          imageTargets.set(id, image);
          found.push(image);
        });
    });
    return found;
  }

  function captureImageState(image) {
    return {
      src: image.getAttribute('src'),
      srcset: image.getAttribute('srcset'),
      sizes: image.getAttribute('sizes'),
      aspectRatio: image.style.aspectRatio,
      objectPosition: image.style.objectPosition,
    };
  }

  function applyNullableAttribute(element, name, value) {
    if (value === null || value === undefined) element.removeAttribute(name);
    else element.setAttribute(name, value);
  }

  function applyImageState(image, state) {
    applyNullableAttribute(image, 'src', state.src);
    applyNullableAttribute(image, 'srcset', state.srcset);
    applyNullableAttribute(image, 'sizes', state.sizes);
    image.style.aspectRatio = state.aspectRatio || '';
    image.style.objectPosition = state.objectPosition || '';
  }

  function captureSnapshot() {
    return {
      texts: Object.fromEntries([...textTargets].map(([id, element]) => [id, element.innerHTML])),
      images: Object.fromEntries([...imageTargets].map(([id, image]) => [id, captureImageState(image)])),
    };
  }

  function applySnapshot(snapshot) {
    suppressMutations = true;
    Object.entries(snapshot.texts || {}).forEach(([id, value]) => {
      const element = textTargets.get(id);
      if (!element) return;
      element.innerHTML = value;
      lastTextValues.set(id, value);
    });
    Object.entries(snapshot.images || {}).forEach(([id, value]) => {
      const image = imageTargets.get(id);
      if (image) applyImageState(image, value);
    });
    suppressMutations = false;
  }

  function stableStringify(value) {
    if (Array.isArray(value)) return `[${value.map(stableStringify).join(',')}]`;
    if (value && typeof value === 'object') {
      const entries = Object.keys(value).sort().map(
        key => `${JSON.stringify(key)}:${stableStringify(value[key])}`,
      );
      return `{${entries.join(',')}}`;
    }
    return JSON.stringify(value);
  }

  function snapshotEquals(left, right) {
    return JSON.stringify(left) === JSON.stringify(right);
  }

  function hashString(value) {
    let hash = 2166136261;
    for (let index = 0; index < value.length; index += 1) {
      hash ^= value.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return (hash >>> 0).toString(16).padStart(8, '0');
  }

  function reportIrTarget(element) {
    const { irEditEntity: entity, irEditId: id, irEditField: field, irEditKey: key } = element.dataset;
    if (!entity || !id || !field || !key) return null;
    return { entity, id, field, key };
  }

  function reportIrImageValue(image) {
    const state = captureImageState(image);
    return {
      src_fingerprint: hashString(state.src || ''),
      object_position: state.objectPosition || '',
      aspect_ratio: state.aspectRatio || '',
    };
  }

  function collectReportIrValues(selector, valueReader) {
    const values = new Map();
    deck.querySelectorAll(selector).forEach(element => {
      const target = reportIrTarget(element);
      if (!target) return;
      const value = valueReader(element);
      if (values.has(target.key) && stableStringify(values.get(target.key).value) !== stableStringify(value)) {
        throw new Error(`Report IR edit target ${target.key} has divergent repeated instances.`);
      }
      values.set(target.key, { target, value, element });
    });
    return values;
  }

  function readExistingReportIrPatch() {
    const script = document.getElementById(REPORT_IR_PATCH_ID);
    if (!script) return null;
    try {
      const payload = JSON.parse(script.textContent || 'null');
      if (
        payload?.schema_version !== '1.0'
        || payload?.kind !== 'taohtml-report-ir-runtime-patch'
        || payload?.base_ir_sha256 !== deck.dataset.reportIrSha256
        || !Array.isArray(payload?.operations)
      ) return null;
      return payload;
    } catch (_error) {
      return null;
    }
  }

  function captureReportIrBaselines() {
    collectReportIrValues(
      '[data-ir-edit-kind="text"][data-ir-edit-key]',
      element => element.textContent || '',
    ).forEach(({ value }, key) => reportIrTextBaseline.set(key, value));
    collectReportIrValues(
      '[data-ir-edit-kind="image"][data-ir-edit-key]',
      element => reportIrImageValue(element),
    ).forEach(({ value }, key) => reportIrImageBaseline.set(key, value));
  }

  function buildReportIrPatch() {
    const baseHash = deck.dataset.reportIrSha256;
    if (!baseHash || deck.dataset.reportIrVersion !== '1.0') return null;
    const operations = new Map(
      (existingReportIrPatch?.operations || []).map(operation => [operation.target?.key, operation]),
    );
    collectReportIrValues(
      '[data-ir-edit-kind="text"][data-ir-edit-key]',
      element => element.textContent || '',
    ).forEach(({ target, value }, key) => {
      const baseline = reportIrTextBaseline.get(key);
      if (baseline === undefined || value === baseline) return;
      const existing = operations.get(key);
      const before = existing?.before ?? baseline;
      if (value === before) operations.delete(key);
      else operations.set(key, { op: 'replace_text', target, before, value });
    });
    collectReportIrValues(
      '[data-ir-edit-kind="image"][data-ir-edit-key]',
      element => reportIrImageValue(element),
    ).forEach(({ target, value, element }, key) => {
      const baseline = reportIrImageBaseline.get(key);
      if (!baseline || stableStringify(value) === stableStringify(baseline)) return;
      const existing = operations.get(key);
      const before = existing?.before ?? baseline;
      if (stableStringify(value) === stableStringify(before)) {
        operations.delete(key);
        return;
      }
      operations.set(key, {
        op: 'replace_image',
        target,
        asset_id: element.dataset.irEditAssetId || '',
        before,
        value: {
          ...value,
          dom_ref: { kind: 'data_ir_edit_key', value: key },
        },
      });
    });
    const ordered = [...operations.values()].sort((left, right) =>
      String(left.target?.key).localeCompare(String(right.target?.key))
    );
    return {
      schema_version: '1.0',
      kind: 'taohtml-report-ir-runtime-patch',
      base_ir_sha256: baseHash,
      report_id: deck.dataset.reportId || '',
      projection_id: deck.dataset.projectionId || '',
      extraction_contract: 'embedded-html-v1',
      operation_count: ordered.length,
      operations: ordered,
    };
  }

  function buildDelta(baseline, current) {
    const delta = { texts: {}, images: {} };
    Object.entries(current.texts).forEach(([id, value]) => {
      if (baseline.texts[id] !== value) delta.texts[id] = value;
    });
    Object.entries(current.images).forEach(([id, value]) => {
      if (!snapshotEquals(baseline.images[id], value)) delta.images[id] = value;
    });
    return delta;
  }

  function applyDelta(baseline, delta) {
    const merged = JSON.parse(JSON.stringify(baseline));
    Object.assign(merged.texts, delta.texts || {});
    Object.assign(merged.images, delta.images || {});
    return merged;
  }

  function emitEditorState() {
    const detail = getState();
    editToggle.textContent = active
      ? '退出编辑模式'
      : (dirty ? '继续编辑模式' : '编辑模式');
    window.dispatchEvent(new CustomEvent('taohtml:editorstatechange', { detail }));
  }

  function showToast(message, timeout = 4200) {
    toast.textContent = message;
    toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.hidden = true;
    }, timeout);
  }

  function clearRecovery() {
    try {
      sessionStorage.removeItem(sessionKey);
      recoveryAvailable = true;
    } catch (_error) {
      recoveryAvailable = false;
    }
  }

  function persistRecovery() {
    const current = captureSnapshot();
    dirty = !snapshotEquals(current, checkpointBaseline);
    if (!dirty) {
      clearRecovery();
      emitEditorState();
      return;
    }
    const payload = {
      version: VERSION,
      signature: documentSignature,
      updatedAt: new Date().toISOString(),
      delta: buildDelta(sourceBaseline, current),
    };
    try {
      sessionStorage.setItem(sessionKey, JSON.stringify(payload));
      recoveryAvailable = true;
    } catch (_error) {
      recoveryAvailable = false;
      showToast('修改仍在当前页面中，但图片较大，浏览器无法保存刷新恢复记录。请尽快导出新 HTML。', 7000);
    }
    emitEditorState();
  }

  function afterHistoryMutation() {
    persistRecovery();
  }

  function appendHistoryCommand(command) {
    undoStack.push(command);
    if (undoStack.length > HISTORY_LIMIT) undoStack.shift();
    redoStack.length = 0;
    afterHistoryMutation();
  }

  function pushCommand(command) {
    flushPendingText();
    appendHistoryCommand(command);
  }

  function flushPendingText() {
    clearTimeout(pendingTextTimer);
    pendingTextTimer = null;
    if (!pendingText) return;
    const { id, before } = pendingText;
    const element = textTargets.get(id);
    pendingText = null;
    if (!element) return;
    const after = element.innerHTML;
    lastTextValues.set(id, after);
    if (before === after) return;
    appendHistoryCommand({
      label: 'text',
      undo: () => {
        element.innerHTML = before;
        lastTextValues.set(id, before);
      },
      redo: () => {
        element.innerHTML = after;
        lastTextValues.set(id, after);
      },
    });
  }

  function scheduleTextCommit() {
    clearTimeout(pendingTextTimer);
    pendingTextTimer = setTimeout(flushPendingText, 450);
  }

  function undo() {
    flushPendingText();
    const command = undoStack.pop();
    if (!command) return false;
    suppressMutations = true;
    command.undo();
    suppressMutations = false;
    redoStack.push(command);
    afterHistoryMutation();
    return true;
  }

  function redo() {
    flushPendingText();
    const command = redoStack.pop();
    if (!command) return false;
    suppressMutations = true;
    command.redo();
    suppressMutations = false;
    undoStack.push(command);
    afterHistoryMutation();
    return true;
  }

  function insertPlainText(text) {
    if (document.queryCommandSupported?.('insertText')) {
      document.execCommand('insertText', false, text);
      return;
    }
    const selection = window.getSelection();
    if (!selection?.rangeCount) return;
    const range = selection.getRangeAt(0);
    range.deleteContents();
    const node = document.createTextNode(text);
    range.insertNode(node);
    range.setStartAfter(node);
    range.collapse(true);
    selection.removeAllRanges();
    selection.addRange(range);
    range.commonAncestorContainer.parentElement?.dispatchEvent(new InputEvent('input', { bubbles: true }));
  }

  function onTextInput(event) {
    if (!active || suppressMutations) return;
    const element = event.currentTarget;
    const id = element.dataset.taohtmlEditorId;
    if (!pendingText || pendingText.id !== id) {
      flushPendingText();
      pendingText = { id, before: lastTextValues.get(id) ?? element.innerHTML };
    }
    persistRecovery();
    scheduleTextCommit();
  }

  function onTextPaste(event) {
    if (!active) return;
    event.preventDefault();
    insertPlainText(event.clipboardData?.getData('text/plain') || '');
  }

  function onImageFileChange() {
    const image = selectedImage;
    const file = fileInput.files?.[0];
    fileInput.value = '';
    selectedImage = null;
    if (!image || !file) return;
    if (!file.type.startsWith('image/')) {
      showToast('请选择 PNG、JPEG、WebP、GIF 或 SVG 图片。');
      return;
    }
    flushPendingText();
    const reader = new FileReader();
    pendingImageRead = reader;
    reader.addEventListener('load', () => {
      if (pendingImageRead !== reader || !active) return;
      pendingImageRead = null;
      const before = captureImageState(image);
      const rect = image.getBoundingClientRect();
      const after = { ...before };
      after.src = String(reader.result);
      after.srcset = null;
      after.sizes = null;
      if (rect.width > 0 && rect.height > 0) {
        after.aspectRatio = `${rect.width} / ${rect.height}`;
      }
      applyImageState(image, after);
      pushCommand({
        label: 'image',
        undo: () => applyImageState(image, before),
        redo: () => applyImageState(image, after),
      });
      showToast('图片已替换。拖动图片可调整裁切焦点。');
    });
    reader.addEventListener('error', () => {
      if (pendingImageRead !== reader) return;
      pendingImageRead = null;
      showToast('图片读取失败，原图未修改。');
    });
    reader.readAsDataURL(file);
  }

  function suppressReportAction(event) {
    if (!active || !(event.target instanceof Element)) return;
    const action = event.target.closest('.slide a, .slide button');
    if (!action) return;
    event.preventDefault();
    event.stopImmediatePropagation();
  }

  function onImagePointerDown(event) {
    if (!active || event.button !== 0) return;
    event.preventDefault();
    const image = event.currentTarget;
    const before = captureImageState(image);
    const rect = image.getBoundingClientRect();
    const origin = { x: event.clientX, y: event.clientY };
    let moved = false;
    image.setPointerCapture?.(event.pointerId);

    function onMove(moveEvent) {
      const distance = Math.hypot(moveEvent.clientX - origin.x, moveEvent.clientY - origin.y);
      if (!moved && distance < 5) return;
      moved = true;
      const x = Math.max(0, Math.min(100, ((moveEvent.clientX - rect.left) / rect.width) * 100));
      const y = Math.max(0, Math.min(100, ((moveEvent.clientY - rect.top) / rect.height) * 100));
      image.style.objectPosition = `${x.toFixed(2)}% ${y.toFixed(2)}%`;
    }

    function finish() {
      image.removeEventListener('pointermove', onMove);
      image.removeEventListener('pointerup', finish);
      image.removeEventListener('pointercancel', finish);
      if (!moved) {
        selectedImage = image;
        fileInput.click();
        return;
      }
      const after = captureImageState(image);
      if (snapshotEquals(before, after)) return;
      pushCommand({
        label: 'crop',
        undo: () => applyImageState(image, before),
        redo: () => applyImageState(image, after),
      });
    }

    image.addEventListener('pointermove', onMove);
    image.addEventListener('pointerup', finish);
    image.addEventListener('pointercancel', finish);
  }

  function setTargetEditing(enabled) {
    textTargets.forEach(element => {
      if (enabled) {
        element.setAttribute('contenteditable', 'true');
        element.setAttribute('spellcheck', 'true');
      } else {
        element.removeAttribute('contenteditable');
        element.removeAttribute('spellcheck');
      }
    });
  }

  function enter() {
    if (active) return;
    active = true;
    runtime.setEditing(true);
    setTargetEditing(true);
    if (modeToggle) modeToggle.disabled = true;
    editorBar.hidden = false;
    emitEditorState();
  }

  function leave() {
    flushPendingText();
    active = false;
    setTargetEditing(false);
    if (modeToggle) modeToggle.disabled = false;
    editorBar.hidden = true;
    closeDialog();
    runtime.setEditing(false);
    emitEditorState();
  }

  function discard() {
    flushPendingText();
    applySnapshot(checkpointBaseline);
    undoStack.length = 0;
    redoStack.length = 0;
    clearRecovery();
    dirty = false;
    leave();
  }

  function openDialog() {
    dialog.hidden = false;
    dialog.querySelector('[data-action="continue"]')?.focus();
  }

  function closeDialog() {
    dialog.hidden = true;
  }

  function requestExit() {
    flushPendingText();
    if (pendingImageRead) {
      showToast('图片仍在读取，请稍候再退出编辑模式。');
      return;
    }
    if (!dirty) {
      leave();
      return;
    }
    openDialog();
  }

  function isPortableReference(value) {
    const normalized = (value || '').trim();
    return !normalized || /^(?:data:|blob:|#|mailto:|tel:)/i.test(normalized);
  }

  function collectExternalAssets(root) {
    const refs = new Set();
    root.querySelectorAll('[src], [srcset], [poster], [data-source], object[data], link[href], base[href]').forEach(element => {
      ['src', 'poster', 'data-source', 'data', 'href'].forEach(attribute => {
        const value = element.getAttribute(attribute);
        if (value && !isPortableReference(value)) refs.add(value);
      });
      const srcset = element.getAttribute('srcset');
      if (srcset && !srcset.trim().startsWith('data:')) {
        srcset.split(',').forEach(candidate => {
          const value = candidate.trim().split(/\s+/, 1)[0];
          if (value && !isPortableReference(value)) refs.add(value);
        });
      }
    });
    root.querySelectorAll('style, [style]').forEach(element => {
      const css = element.tagName === 'STYLE' ? element.textContent : element.getAttribute('style');
      [...(css || '').matchAll(/url\(\s*["']?([^"')]+)["']?\s*\)/gi)].forEach(match => {
        if (!isPortableReference(match[1])) refs.add(match[1]);
      });
      [...(css || '').matchAll(/@import\s+(?:url\()?\s*["']?([^"')\s;]+)/gi)].forEach(match => {
        if (!isPortableReference(match[1])) refs.add(match[1]);
      });
    });
    return [...refs].sort();
  }

  function cleanExportClone(clone) {
    clone.querySelectorAll('[data-taohtml-editor-ui]').forEach(element => element.remove());
    clone.querySelectorAll('[data-taohtml-editor-id], [data-taohtml-editor-kind]').forEach(element => {
      element.removeAttribute('data-taohtml-editor-id');
      element.removeAttribute('data-taohtml-editor-kind');
      element.removeAttribute('contenteditable');
      element.removeAttribute('spellcheck');
    });
    const cloneDeck = clone.querySelector('#deck');
    cloneDeck?.removeAttribute('data-taohtml-editing');
    cloneDeck?.classList.remove('controls-hidden');
    const cloneMore = clone.querySelector('#moreMenu');
    if (cloneMore) cloneMore.hidden = true;
    clone.querySelector('#moreToggle')?.setAttribute('aria-expanded', 'false');
    const cloneEditToggle = clone.querySelector('#editToggle');
    if (cloneEditToggle) cloneEditToggle.textContent = '编辑模式';
    const cloneModeToggle = clone.querySelector('#modeToggle');
    if (cloneModeToggle) cloneModeToggle.disabled = false;
    const cloneModal = clone.querySelector('#modal');
    cloneModal?.classList.remove('open');
    cloneModal?.setAttribute('aria-hidden', 'true');
    const cloneModalBody = clone.querySelector('#modalBody');
    if (cloneModalBody) cloneModalBody.replaceChildren();
  }

  function syncReportIrPatch(clone, patch) {
    let script = clone.querySelector(`#${REPORT_IR_PATCH_ID}`);
    if (!patch || patch.operation_count === 0) {
      script?.remove();
      return;
    }
    if (!script) {
      script = document.createElement('script');
      script.id = REPORT_IR_PATCH_ID;
      script.type = 'application/json';
      script.dataset.taohtmlEditLock = '';
      clone.querySelector('body')?.appendChild(script);
    }
    script.dataset.baseIrSha256 = patch.base_ir_sha256;
    script.textContent = JSON.stringify(patch).replace(/</g, '\\u003c');
  }

  function safeFilename() {
    const title = (document.title || 'taohtml').trim()
      .replace(/[\\/:*?"<>|\u0000-\u001f]+/g, '-')
      .replace(/\s+/g, '-')
      .replace(/^-+|-+$/g, '') || 'taohtml';
    const now = new Date();
    const stamp = [
      now.getFullYear(),
      String(now.getMonth() + 1).padStart(2, '0'),
      String(now.getDate()).padStart(2, '0'),
      '-',
      String(now.getHours()).padStart(2, '0'),
      String(now.getMinutes()).padStart(2, '0'),
      String(now.getSeconds()).padStart(2, '0'),
    ].join('');
    return `${title}-edited-${stamp}.html`;
  }

  async function exportHtml() {
    flushPendingText();
    let reportIrPatch;
    try {
      reportIrPatch = buildReportIrPatch();
    } catch (error) {
      showToast(`Report IR Patch 生成失败：${error.message}`, 9000);
      throw error;
    }
    const clone = document.documentElement.cloneNode(true);
    cleanExportClone(clone);
    syncReportIrPatch(clone, reportIrPatch);
    const externalAssets = collectExternalAssets(clone);
    const doctype = document.doctype ? '<!doctype html>\n' : '';
    const html = `${doctype}${clone.outerHTML}`;
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const filename = safeFilename();
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    anchor.hidden = true;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 30000);

    checkpointBaseline = captureSnapshot();
    undoStack.length = 0;
    redoStack.length = 0;
    dirty = false;
    clearRecovery();
    emitEditorState();
    if (externalAssets.length) {
      showToast('已导出新 HTML。此报告仍引用本地 assets；请将新 HTML 放回原 index.html 同级并保留 assets 文件夹。编辑器不会生成 ZIP。', 9000);
    } else {
      showToast('已导出新的离线单文件 HTML；原文件未被覆盖。', 6000);
    }
    return {
      filename,
      kind: externalAssets.length ? 'html-with-assets' : 'single-file',
      externalAssets,
      reportIrPatchOperations: reportIrPatch?.operation_count || 0,
    };
  }

  function getState() {
    return {
      active,
      dirty,
      canUndo: undoStack.length > 0 || Boolean(pendingText),
      canRedo: redoStack.length > 0,
      recoveryAvailable,
    };
  }

  function restoreRecovery() {
    let payload;
    try {
      payload = JSON.parse(sessionStorage.getItem(sessionKey) || 'null');
    } catch (_error) {
      clearRecovery();
      return;
    }
    if (!payload || payload.version !== VERSION || payload.signature !== documentSignature) {
      if (payload) clearRecovery();
      return;
    }
    const before = captureSnapshot();
    const after = applyDelta(sourceBaseline, payload.delta || {});
    if (snapshotEquals(before, after)) {
      clearRecovery();
      return;
    }
    applySnapshot(after);
    undoStack.push({
      label: 'recovery',
      undo: () => applySnapshot(before),
      redo: () => applySnapshot(after),
    });
    dirty = true;
    emitEditorState();
    showToast('已恢复此标签页刷新前尚未导出的修改。', 6500);
  }

  const editorBar = document.createElement('div');
  editorBar.className = 'taohtml-editor-bar';
  editorBar.dataset.taohtmlEditorUi = 'bar';
  editorBar.dataset.taohtmlEditLock = '';
  editorBar.hidden = true;
  editorBar.textContent = '编辑模式：直接修改文字；点击图片替换，拖动调整裁切焦点；Ctrl/Cmd+Z 撤销。';

  const dialog = document.createElement('div');
  dialog.className = 'taohtml-editor-dialog';
  dialog.dataset.taohtmlEditorUi = 'exit-dialog';
  dialog.dataset.taohtmlEditLock = '';
  dialog.hidden = true;
  dialog.setAttribute('role', 'dialog');
  dialog.setAttribute('aria-modal', 'true');
  dialog.setAttribute('aria-label', '退出编辑模式');
  dialog.innerHTML = `
    <div class="taohtml-editor-dialog-card">
      <h2>还有未导出的修改</h2>
      <p>继续编辑，放弃本轮修改，或下载一个新的 HTML。原文件不会被覆盖。</p>
      <div class="taohtml-editor-dialog-actions">
        <button type="button" data-action="continue">继续编辑</button>
        <button type="button" data-action="discard">放弃修改</button>
        <button type="button" data-action="export">导出新 HTML</button>
      </div>
    </div>`;

  const toast = document.createElement('div');
  toast.className = 'taohtml-editor-toast';
  toast.dataset.taohtmlEditorUi = 'toast';
  toast.dataset.taohtmlEditLock = '';
  toast.hidden = true;
  toast.setAttribute('role', 'status');
  toast.setAttribute('aria-live', 'polite');

  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = 'image/png,image/jpeg,image/webp,image/gif,image/svg+xml';
  fileInput.hidden = true;
  fileInput.dataset.taohtmlEditorUi = 'image-input';
  fileInput.dataset.taohtmlEditLock = '';

  deck.append(editorBar, dialog, toast);
  document.body.appendChild(fileInput);
  discoverTextTargets().forEach(element => {
    element.addEventListener('input', onTextInput);
    element.addEventListener('paste', onTextPaste);
    element.addEventListener('blur', flushPendingText);
  });
  discoverImageTargets().forEach(image => {
    image.addEventListener('pointerdown', onImagePointerDown);
  });
  deck.addEventListener('click', suppressReportAction, true);
  deck.addEventListener('auxclick', suppressReportAction, true);
  fileInput.addEventListener('change', onImageFileChange);
  editToggle.addEventListener('click', event => {
    event.stopPropagation();
    if (active) requestExit();
    else enter();
  });
  dialog.addEventListener('click', async event => {
    const action = event.target.closest('button')?.dataset.action;
    if (action === 'continue') closeDialog();
    if (action === 'discard') discard();
    if (action === 'export') {
      await exportHtml();
      leave();
    }
  });
  document.addEventListener('keydown', event => {
    if (!active || !(event.ctrlKey || event.metaKey) || event.altKey) return;
    const key = event.key.toLowerCase();
    if (key !== 'z') return;
    event.preventDefault();
    event.stopImmediatePropagation();
    if (event.shiftKey) redo();
    else undo();
  });

  sourceBaseline = captureSnapshot();
  checkpointBaseline = captureSnapshot();
  documentSignature = hashString(stableStringify(sourceBaseline));
  existingReportIrPatch = readExistingReportIrPatch();
  captureReportIrBaselines();
  restoreRecovery();
  emitEditorState();

  window.TaoHtmlEditor = Object.freeze({
    getState,
    enter,
    requestExit,
    undo,
    redo,
    exportHtml,
    getReportIrPatch: buildReportIrPatch,
  });
})();
