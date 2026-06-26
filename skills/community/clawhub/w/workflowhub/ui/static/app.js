const state = {
  workflows: [],
  filtered: [],
  selectedId: null,
  originalId: null,
  template: null,
  meta: null,
  previewTimer: null,
  previewDirty: true,
};

const els = {
  workflowList: document.getElementById("workflow-list"),
  workflowDir: document.getElementById("workflow-dir"),
  workflowCount: document.getElementById("workflow-count"),
  statusBanner: document.getElementById("status-banner"),
  editorTitle: document.getElementById("editor-title"),
  jsonPreview: document.getElementById("json-preview"),
  searchInput: document.getElementById("search-input"),
  form: document.getElementById("workflow-form"),
  newButton: document.getElementById("new-workflow"),
  refreshButton: document.getElementById("refresh-list"),
  reloadButton: document.getElementById("reload-current"),
  deleteButton: document.getElementById("delete-workflow"),
};

document.addEventListener("DOMContentLoaded", () => {
  bindEvents();
  initialize();
});

async function initialize() {
  await Promise.all([loadTemplate(), loadMeta(), loadWorkflows()]);
  if (state.filtered[0]) {
    await selectWorkflow(state.filtered[0].id);
  } else if (state.template) {
    populateForm(cloneData(state.template), null);
  }
}

function bindEvents() {
  els.searchInput.addEventListener("input", applySearch);
  els.form.addEventListener("submit", onSave);
  els.form.addEventListener("input", schedulePreviewRefresh);
  els.newButton.addEventListener("click", createFromTemplate);
  els.refreshButton.addEventListener("click", async () => {
    await loadMeta();
    await loadWorkflows();
  });
  els.reloadButton.addEventListener("click", reloadCurrent);
  els.deleteButton.addEventListener("click", deleteCurrentWorkflow);

  document.querySelectorAll("[data-tab]").forEach((button) => {
    button.addEventListener("click", () => activateTab(button.dataset.tab));
  });

  document.querySelectorAll("[data-add-row]").forEach((button) => {
    button.addEventListener("click", () => addRow(button.dataset.addRow));
  });

  document.body.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
      return;
    }
    if (target.matches("[data-remove-row]")) {
      target.closest(".row")?.remove();
      refreshStepLabels();
      refreshPreviewNow();
    }
  });
}

async function loadTemplate() {
  state.template = await fetchJson("/api/template");
}

async function loadMeta() {
  state.meta = await fetchJson("/api/meta");
  els.workflowDir.textContent = state.meta.workflows_dir;
  els.workflowDir.title = state.meta.workflows_dir;
}

async function loadWorkflows() {
  state.workflows = await fetchJson("/api/workflows");
  applySearch();
  els.workflowCount.textContent = String(state.workflows.length);
}

function applySearch() {
  const query = els.searchInput.value.trim().toLowerCase();
  state.filtered = state.workflows.filter((workflow) => {
    if (!query) {
      return true;
    }
    const haystack = [
      workflow.id,
      workflow.name,
      workflow.summary,
      ...(workflow.keywords || []),
    ]
      .join(" ")
      .toLowerCase();
    return haystack.includes(query);
  });
  renderWorkflowList();
}

function renderWorkflowList() {
  if (!state.filtered.length) {
    els.workflowList.innerHTML = '<div class="empty-state">No workflows yet.</div>';
    return;
  }

  els.workflowList.innerHTML = "";
  state.filtered.forEach((workflow) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "workflow-item";
    if (workflow.id === state.selectedId) {
      button.classList.add("is-active");
    }
    const updated = workflow.updated_at
      ? new Date(workflow.updated_at * 1000).toLocaleString()
      : "Unknown";
    button.innerHTML = `
      <h3>${escapeHtml(workflow.name)}</h3>
      <div class="workflow-summary">${escapeHtml(workflow.summary || "No summary yet.")}</div>
      <div class="pill-row">
        ${(workflow.keywords || []).slice(0, 3).map((keyword) => `<span class="pill">${escapeHtml(keyword)}</span>`).join("")}
      </div>
      <div class="workflow-summary">Updated ${escapeHtml(updated)}</div>
    `;
    button.addEventListener("click", () => selectWorkflow(workflow.id));
    els.workflowList.appendChild(button);
  });
}

async function selectWorkflow(id) {
  const workflow = await fetchJson(`/api/workflows/${encodeURIComponent(id)}`);
  populateForm(workflow, id);
  state.selectedId = id;
  updateDeleteButton();
  renderWorkflowList();
  setStatus(`Loaded workflow ${id}.`);
}

function createFromTemplate() {
  const template = cloneData(state.template || {});
  populateForm(template, null);
  state.selectedId = null;
  state.originalId = null;
  updateDeleteButton();
  renderWorkflowList();
  setStatus("Started a new workflow from the template.");
}

async function reloadCurrent() {
  if (state.selectedId) {
    await selectWorkflow(state.selectedId);
    return;
  }
  createFromTemplate();
}

function populateForm(workflow, originalId) {
  state.originalId = originalId;
  els.editorTitle.textContent = originalId ? (workflow.name || originalId) : "New Workflow";
  setInput("name", workflow.name || "");
  setInput("summary", workflow.summary || "");
  setInput("match_keywords", listToComma(workflow.match?.keywords));
  fillRows("steps", mergeStepsWithTools(workflow.steps || [], workflow.tool_preferences || []), renderStepRow);
  autosizeStepTextareas();
  refreshPreviewNow();
}

function updateDeleteButton() {
  els.deleteButton.disabled = !state.selectedId;
}

function setInput(name, value) {
  const field = els.form.elements.namedItem(name);
  if (field) {
    field.value = value;
  }
}

function fillRows(containerId, items, rowRenderer) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  items.forEach((item) => container.appendChild(rowRenderer(item)));
  if (containerId === "steps") {
    refreshStepLabels();
  }
}

function addRow(type) {
  const map = {
    steps: () => renderStepRow({ instruction: "", tool: "" }),
  };
  const factory = map[type];
  if (!factory) {
    return;
  }
  document.getElementById(type).appendChild(factory());
  if (type === "steps") {
    refreshStepLabels();
    autosizeStepTextareas();
  }
  refreshPreviewNow();
}

function renderToolPreferenceRow(item) {
  const row = cloneTemplate("row-template-two");
  configureRow(row, [
    ["first", "tool", item.tool || "", "Tool"],
    ["second", "purpose", item.purpose || "", "Purpose"],
  ]);
  return row;
}

function renderStepRow(item) {
  const row = cloneTemplate("row-template-three");
  configureRow(row, [
    ["second", "instruction", item.instruction || "", "Instruction"],
    ["third", "tool", item.tool || "", "Tool"],
  ]);
  return row;
}

function cloneTemplate(id) {
  return document.getElementById(id).content.firstElementChild.cloneNode(true);
}

function configureRow(row, fieldConfigs) {
  fieldConfigs.forEach(([slot, name, value, placeholder]) => {
    const el = row.querySelector(`[data-field="${slot}"]`);
    if (!el) {
      return;
    }
    el.dataset.name = name;
    el.value = value;
    el.placeholder = placeholder;
    if (el instanceof HTMLTextAreaElement) {
      autosizeTextarea(el);
      el.addEventListener("input", () => autosizeTextarea(el));
    }
  });
}

function collectRows(containerId) {
  return Array.from(document.querySelectorAll(`#${containerId} .row`));
}

function buildWorkflowFromForm() {
  const name = getValue("name").trim();
  const generatedId = slugify(name);
  const steps = collectSteps();
  const workflow = {
    id: generatedId,
    name,
    summary: getValue("summary").trim(),
    match: {
      keywords: commaToList(getValue("match_keywords")),
    },
    steps,
    tool_preferences: collectToolPreferences(steps),
    version: 1,
  };
  return workflow;
}

function collectObjects(containerId) {
  return collectRows(containerId)
    .map((row) => {
      const values = {};
      row.querySelectorAll("[data-name]").forEach((input) => {
        const raw = input.value.trim();
        if (raw) {
          values[input.dataset.name] = raw;
        }
      });
      return values;
    })
    .filter((item) => Object.keys(item).length > 0);
}

function collectSteps() {
  return collectRows("steps")
    .map((row, index) => {
      const instruction = row.querySelector('[data-name="instruction"]').value.trim();
      const tool = row.querySelector('[data-name="tool"]').value.trim();
      if (!instruction && !tool) {
        return null;
      }
      return {
        id: `step-${index + 1}`,
        title: `Step ${index + 1}`,
        instruction,
        tool,
      };
    })
    .filter(Boolean);
}

function getValue(name) {
  return els.form.elements.namedItem(name).value || "";
}

async function onSave(event) {
  event.preventDefault();
  const workflow = buildWorkflowFromForm();
  if (!workflow.name) {
    setStatus("Workflow name is required.", true);
    return;
  }
  const idTaken = state.workflows.some(
    (item) => item.id === workflow.id && item.id !== state.originalId
  );
  if (idTaken) {
    setStatus(`Workflow id "${workflow.id}" already exists.`, true);
    return;
  }
  try {
    await fetchJson("/api/workflows", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...workflow, _original_id: state.originalId }),
    });
    setStatus(`Saved ${workflow.id}.`);
    await loadMeta();
    await loadWorkflows();
    await selectWorkflow(workflow.id);
  } catch (error) {
    setStatus(error.message || "Save failed.", true);
  }
}

async function deleteCurrentWorkflow() {
  if (!state.selectedId) {
    return;
  }
  const label = state.selectedId;
  const confirmed = window.confirm(`Delete workflow "${label}"? This cannot be undone.`);
  if (!confirmed) {
    return;
  }
  try {
    await fetchJson(`/api/workflows/${encodeURIComponent(state.selectedId)}`, {
      method: "DELETE",
    });
    setStatus(`Deleted ${label}.`);
    state.selectedId = null;
    state.originalId = null;
    await loadMeta();
    await loadWorkflows();
    createFromTemplate();
  } catch (error) {
    setStatus(error.message || "Delete failed.", true);
  }
}

function schedulePreviewRefresh() {
  state.previewDirty = true;
  if (state.previewTimer) {
    window.clearTimeout(state.previewTimer);
  }
  state.previewTimer = window.setTimeout(() => {
    state.previewTimer = null;
    if (isJsonTabActive()) {
      refreshPreviewNow();
    }
  }, 120);
}

function refreshPreviewNow() {
  try {
    const workflow = buildWorkflowFromForm();
    els.jsonPreview.textContent = JSON.stringify(workflow, null, 2);
    state.previewDirty = false;
  } catch (_error) {
    els.jsonPreview.textContent = "{}";
    state.previewDirty = false;
  }
}

function activateTab(tabName) {
  document.querySelectorAll("[data-tab]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.tab === tabName);
  });
  document.querySelectorAll("[data-panel]").forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.panel === tabName);
  });
  if (tabName === "json" && state.previewDirty) {
    refreshPreviewNow();
  }
}

function setStatus(message, isError = false) {
  els.statusBanner.textContent = message;
  els.statusBanner.style.color = isError ? "#8c2917" : "";
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const payload = await response.json();
  if (!response.ok || payload.ok === false) {
    throw new Error(payload.error || "Request failed.");
  }
  return payload;
}

function commaToList(value) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function linesToList(value) {
  return value
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}

function listToComma(items) {
  return Array.isArray(items) ? items.join(", ") : "";
}

function listToLines(items) {
  return Array.isArray(items) ? items.join("\n") : "";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function cloneData(value) {
  return JSON.parse(JSON.stringify(value));
}

function refreshStepLabels() {
  collectRows("steps").forEach((row, index) => {
    const label = row.querySelector("[data-step-label]");
    if (label) {
      label.textContent = `Step ${index + 1}`;
    }
  });
}

function collectToolPreferences(steps) {
  const seen = new Set();
  return steps
    .map((step) => step.tool?.trim())
    .filter(Boolean)
    .filter((tool) => {
      if (seen.has(tool)) {
        return false;
      }
      seen.add(tool);
      return true;
    })
    .map((tool) => ({ tool, purpose: "" }));
}

function mergeStepsWithTools(steps, toolPreferences) {
  const fallbackTools = (toolPreferences || []).map((item) => item.tool).filter(Boolean);
  return (steps || []).map((step, index) => ({
    ...step,
    tool: step.tool || fallbackTools[index] || "",
  }));
}

function isJsonTabActive() {
  const activePanel = document.querySelector('[data-panel].is-active');
  return activePanel?.dataset.panel === "json";
}

function autosizeStepTextareas() {
  document
    .querySelectorAll('#steps textarea[data-name="instruction"]')
    .forEach((textarea) => autosizeTextarea(textarea));
}

function autosizeTextarea(textarea) {
  textarea.style.height = "0px";
  textarea.style.height = `${textarea.scrollHeight}px`;
}

function slugify(value) {
  return value
    .normalize("NFKC")
    .trim()
    .toLowerCase()
    .replace(/[\s/]+/gu, "-")
    .replace(/[^\p{L}\p{N}_-]+/gu, "")
    .replace(/-+/g, "-")
    .replace(/^[-_]+|[-_]+$/g, "") || "new-workflow";
}
