const byId = (id) => document.getElementById(id);
let currentActionId = "";
let currentLang = (navigator.language || "").toLowerCase().startsWith("zh") ? "zh" : "en";

const I18N = {
  en: {
    eyebrow: "Review Dashboard",
    hero_copy: "Inspect the current mission, ranked actions, memory, and recent executions without digging through raw JSON.",
    refresh: "Refresh State",
    ready: "Ready.",
    mission: "Mission",
    no_mission: "No mission loaded",
    action_plan: "Action Plan",
    no_action_plan: "No action plan found.",
    current_action: "Current Action",
    preflight: "Preflight",
    dry_run: "Dry Run",
    execute_live: "Execute Live",
    no_action: "No proposed action found.",
    memory: "Memory",
    learning_loop: "Learning Loop",
    no_memory: "No memory file found.",
    top_opportunities: "Top Opportunities",
    no_opportunities: "No scored opportunities found.",
    recent_executions: "Recent Executions",
    no_executions: "No executions recorded.",
    generated_files: "Generated Files",
    no_files: "No generated files found.",
    no_data: "No data available.",
    none: "None",
    goal: "Goal",
    voice: "Voice",
    risk: "Risk",
    topics: "Topics",
    keywords: "Keywords",
    accounts: "Accounts",
    cta: "CTA",
    actions_count: (n) => `${n} actions`,
    items_count: (n) => `${n} items`,
    events_count: (n) => `${n} events`,
    unknown: "unknown",
    score: "score",
    readiness: "readiness",
    draft: "Draft",
    no_draft_text: "No draft text.",
    successful_topics: "Successful Topics",
    action_types: "Action Types",
    high_signal_accounts: "High Signal Accounts",
    avoid_accounts: "Avoid Accounts",
    no_signals: "No signals yet.",
    status_refreshing: "Refreshing state...",
    status_refreshed: "State refreshed.",
    status_drafting: (id) => `Drafting action for ${id}...`,
    status_drafted: (id) => `Draft created from ${id}.`,
    status_preflight: "Running preflight...",
    status_preflight_decision: (d) => `Preflight decision: ${d}.`,
    status_dry_run: "Executing dry run...",
    status_dry_run_done: "Dry run executed.",
    confirm_live: "Execute current action live on X API?",
    status_live_run: "Executing live action...",
    status_live_run_done: "Live execution completed.",
    lang_toggle: "中文",
  },
  zh: {
    eyebrow: "审核面板",
    hero_copy: "无需手动翻 JSON，直接查看 mission、动作优先级、记忆信号与执行记录。",
    refresh: "刷新状态",
    ready: "已就绪。",
    mission: "运营任务",
    no_mission: "尚未加载 mission",
    action_plan: "行动计划",
    no_action_plan: "暂无行动计划。",
    current_action: "当前动作",
    preflight: "预检查",
    dry_run: "演练执行",
    execute_live: "真实执行",
    no_action: "暂无待执行动作。",
    memory: "记忆",
    learning_loop: "反馈学习",
    no_memory: "未找到记忆文件。",
    top_opportunities: "机会池（Top）",
    no_opportunities: "暂无已评分机会。",
    recent_executions: "最近执行",
    no_executions: "暂无执行记录。",
    generated_files: "生成文件",
    no_files: "暂无生成文件。",
    no_data: "暂无数据。",
    none: "无",
    goal: "目标",
    voice: "语气",
    risk: "风险",
    topics: "主题",
    keywords: "关键词",
    accounts: "账号",
    cta: "行动号召",
    actions_count: (n) => `${n} 个动作`,
    items_count: (n) => `${n} 条`,
    events_count: (n) => `${n} 条记录`,
    unknown: "未知",
    score: "分数",
    readiness: "互动可行性",
    draft: "起草",
    no_draft_text: "暂无草稿文案。",
    successful_topics: "高表现主题",
    action_types: "高表现动作类型",
    high_signal_accounts: "高信号账号",
    avoid_accounts: "避开账号",
    no_signals: "暂无可用信号。",
    status_refreshing: "正在刷新状态...",
    status_refreshed: "状态已刷新。",
    status_drafting: (id) => `正在为 ${id} 生成草稿...`,
    status_drafted: (id) => `已根据 ${id} 生成草稿。`,
    status_preflight: "正在进行预检查...",
    status_preflight_decision: (d) => `预检查结果：${d}。`,
    status_dry_run: "正在执行演练...",
    status_dry_run_done: "演练执行完成。",
    confirm_live: "确认真实执行当前动作并发往 X 吗？",
    status_live_run: "正在真实执行...",
    status_live_run_done: "真实执行已完成。",
    lang_toggle: "EN",
  },
};

function t(key, ...args) {
  const value = I18N[currentLang]?.[key] ?? I18N.en[key] ?? key;
  return typeof value === "function" ? value(...args) : value;
}

function localizeActionType(value) {
  if (currentLang !== "zh") return value || t("none");
  const mapping = {
    post: "原创",
    reply: "回复",
    quote_post: "引用转发",
    observe: "观察",
    thread: "线程",
  };
  return mapping[String(value || "").toLowerCase()] || value || t("none");
}

function localizePriority(value) {
  if (currentLang !== "zh") return value || t("none");
  const mapping = { high: "高", medium: "中", low: "低" };
  return mapping[String(value || "").toLowerCase()] || value || t("none");
}

function localizeRisk(value) {
  if (currentLang !== "zh") return value || t("none");
  const mapping = { high: "高", medium: "中", low: "低" };
  return mapping[String(value || "").toLowerCase()] || value || t("none");
}

function localizeReadiness(value) {
  if (currentLang !== "zh") return value || t("unknown");
  const mapping = {
    open: "可互动",
    restricted: "受限",
    thread_reply: "线程回复受限",
    unknown: "未知",
  };
  return mapping[String(value || "").toLowerCase()] || value || t("unknown");
}

function localizeStatus(value) {
  if (currentLang !== "zh") return value || t("unknown");
  const mapping = {
    executed: "已执行",
    recorded: "已记录",
    proposed: "待审核",
    dry_run_executed: "演练完成",
    blocked: "已拦截",
  };
  return mapping[String(value || "").toLowerCase()] || value || t("unknown");
}

function localizeDecision(value) {
  if (currentLang !== "zh") return value || t("unknown");
  const mapping = { allow: "允许", block: "阻断", review: "人工复核", unknown: "未知" };
  return mapping[String(value || "").toLowerCase()] || value || t("unknown");
}

function applyStaticI18n() {
  document.documentElement.lang = currentLang === "zh" ? "zh-CN" : "en";
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const key = node.dataset.i18n;
    node.textContent = t(key);
  });
  byId("languageToggle").textContent = t("lang_toggle");
}

function setStatus(message, kind = "info") {
  const target = byId("statusBanner");
  if (!target) return;
  target.textContent = message;
  target.style.color = kind === "error" ? "#8c2c1a" : kind === "success" ? "#2c5a46" : "";
}

async function postJson(path, payload = {}) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body = await response.json();
  if (!response.ok || body.ok === false) {
    throw new Error(body.error || `Request failed: ${response.status}`);
  }
  return body;
}

function renderKeyValueBlock(target, entries) {
  if (!entries.length) {
    target.innerHTML = `<div class="empty-state">${t("no_data")}</div>`;
    return;
  }
  target.innerHTML = entries
    .map(
      ([label, value]) => `
        <div class="meta-item">
          <span class="meta-label">${label}</span>
          <span class="meta-value">${value}</span>
        </div>
      `
    )
    .join("");
}

function renderTagList(values) {
  if (!values || !values.length) return `<span class="muted">${t("none")}</span>`;
  return values.map((value) => `<span class="tag">${value}</span>`).join("");
}

function renderMission(mission) {
  byId("missionName").textContent = mission?.name || t("no_mission");
  renderKeyValueBlock(byId("missionMeta"), [
    [t("goal"), mission?.goal || t("none")],
    [t("voice"), mission?.voice || t("none")],
    [t("risk"), localizeRisk(mission?.risk_tolerance || t("none"))],
    [t("topics"), renderTagList(mission?.primary_topics || [])],
    [t("keywords"), renderTagList(mission?.watch_keywords || [])],
    [t("accounts"), renderTagList(mission?.watch_accounts || [])],
    [t("cta"), mission?.cta || t("none")],
  ]);
}

function renderPlan(plan) {
  const items = plan?.items || [];
  byId("planCount").textContent = t("actions_count", items.length);
  const target = byId("planList");
  if (!items.length) {
    target.className = "list-block empty-state";
    target.textContent = t("no_action_plan");
    return;
  }
  target.className = "list-block";
  target.innerHTML = items
    .map(
      (item) => `
        <article class="list-item">
          <div class="list-item-head">
            <strong>${localizeActionType(item.action_type)}</strong>
            <span class="chip small">${localizePriority(item.priority)}</span>
          </div>
          <p>${item.target_account || t("unknown")} · ${t("score")} ${item.score} · ${t("readiness")} ${localizeReadiness(item.interaction_readiness)}</p>
          <p class="muted">${item.why_now || ""}</p>
          <div class="list-item-actions">
            <button class="secondary-button draft-button" data-opportunity-id="${item.opportunity_id}">${t("draft")}</button>
          </div>
        </article>
      `
    )
    .join("");
}

function renderCurrentAction(action) {
  currentActionId = action?.id || "";
  byId("actionType").textContent = localizeActionType(action?.action_type || t("none"));
  const target = byId("currentAction");
  const disabled = !currentActionId;
  byId("preflightButton").disabled = disabled;
  byId("dryRunButton").disabled = disabled;
  byId("executeButton").disabled = disabled;
  if (!action || !action.id) {
    target.className = "action-card empty-state";
    target.textContent = t("no_action");
    return;
  }
  target.className = "action-card";
  target.innerHTML = `
    <p><strong>${localizeActionType(action.action_type)}</strong> · ${t("score")} ${action.score ?? "n/a"} · ${t("risk")} ${localizeRisk(action.risk_level ?? "n/a")}</p>
    <p class="draft">${action.draft_text || t("no_draft_text")}</p>
    <p class="muted">${action.rationale || ""}</p>
  `;
}

function renderMemory(memory) {
  const target = byId("memoryBlock");
  if (!memory || !Object.keys(memory).length) {
    target.className = "memory-grid empty-state";
    target.textContent = t("no_memory");
    return;
  }
  target.className = "memory-grid";
  const cards = [
    [t("successful_topics"), memory.successful_topics || {}],
    [t("action_types"), memory.successful_action_types || {}],
    [t("high_signal_accounts"), memory.high_signal_accounts || {}],
    [t("avoid_accounts"), memory.avoid_accounts || {}],
  ];
  target.innerHTML = cards
    .map(([title, obj]) => {
      const entries = Object.entries(obj);
      return `
        <div class="memory-card">
          <h3>${title}</h3>
          ${
            entries.length
              ? entries
                  .slice(0, 5)
                  .map(([key, value]) => `<div class="memory-row"><span>${key}</span><strong>${value}</strong></div>`)
                  .join("")
              : `<div class="muted">${t("no_signals")}</div>`
          }
        </div>
      `;
    })
    .join("");
}

function renderOpportunities(payload) {
  const items = payload?.items || [];
  byId("opportunityCount").textContent = t("items_count", items.length);
  const target = byId("opportunityList");
  if (!items.length) {
    target.className = "list-block empty-state";
    target.textContent = t("no_opportunities");
    return;
  }
  target.className = "list-block";
  target.innerHTML = items
    .slice(0, 6)
    .map(
      (item) => `
        <article class="list-item">
          <div class="list-item-head">
            <strong>${item.source_account || t("unknown")}</strong>
            <span class="chip small">${localizeActionType(item.recommended_action)}</span>
          </div>
          <p>${item.score} · ${localizeRisk(item.risk_level)} · ${localizeReadiness((item.algorithm_hints || {}).interaction_readiness || "unknown")}</p>
          <p class="muted">${(item.text || "").slice(0, 140)}</p>
          ${
            item.recommended_action && item.recommended_action !== "observe"
              ? `<div class="list-item-actions"><button class="secondary-button draft-button" data-opportunity-id="${item.id}">${t("draft")}</button></div>`
              : ""
          }
        </article>
      `
    )
    .join("");
}

function renderExecutions(events) {
  const items = events || [];
  byId("executionCount").textContent = t("events_count", items.length);
  const target = byId("executionList");
  if (!items.length) {
    target.className = "list-block empty-state";
    target.textContent = t("no_executions");
    return;
  }
  target.className = "list-block";
  target.innerHTML = items
    .map(
      (item) => `
        <article class="list-item">
          <div class="list-item-head">
            <strong>${localizeActionType(item.action_type || t("unknown"))}</strong>
            <span class="chip small">${localizeStatus(item.status)}</span>
          </div>
          <p>${item.target_account || t("unknown")} · ${item.executed_at || "n/a"}</p>
          <p class="muted">${(item.draft_text || "").slice(0, 140)}</p>
        </article>
      `
    )
    .join("");
}

function renderFiles(files) {
  const target = byId("fileList");
  if (!files?.length) {
    target.className = "file-list empty-state";
    target.textContent = t("no_files");
    return;
  }
  target.className = "file-list";
  target.innerHTML = files.map((file) => `<span class="file-pill">${file}</span>`).join("");
}

async function loadState() {
  const response = await fetch("/api/state");
  const data = await response.json();
  renderMission(data.mission);
  renderPlan(data.action_plan);
  renderCurrentAction(data.current_action);
  renderMemory(data.memory);
  renderOpportunities(data.opportunities_scored);
  renderExecutions(data.execution_log);
  renderFiles(data.generated_files);
  wireActionButtons();
}

function wireActionButtons() {
  document.querySelectorAll(".draft-button").forEach((button) => {
    button.onclick = async () => {
      const opportunityId = button.dataset.opportunityId;
      if (!opportunityId) return;
      try {
        setStatus(t("status_drafting", opportunityId));
        await postJson("/api/draft", { opportunity_id: opportunityId });
        await loadState();
        setStatus(t("status_drafted", opportunityId), "success");
      } catch (error) {
        console.error(error);
        setStatus(error.message, "error");
      }
    };
  });
}

byId("refreshButton").addEventListener("click", async () => {
  try {
    setStatus(t("status_refreshing"));
    await loadState();
    setStatus(t("status_refreshed"), "success");
  } catch (error) {
    console.error(error);
    setStatus(error.message, "error");
  }
});

byId("preflightButton").addEventListener("click", async () => {
  if (!currentActionId) return;
  try {
    setStatus(t("status_preflight"));
    const response = await postJson("/api/preflight", {});
    const decisionRaw = response.preflight?.decision || "unknown";
    const decision = localizeDecision(decisionRaw);
    setStatus(t("status_preflight_decision", decision), decisionRaw === "allow" ? "success" : "error");
  } catch (error) {
    console.error(error);
    setStatus(error.message, "error");
  }
});

byId("dryRunButton").addEventListener("click", async () => {
  if (!currentActionId) return;
  try {
    setStatus(t("status_dry_run"));
    await postJson("/api/execute", { mode: "dry-run" });
    await loadState();
    setStatus(t("status_dry_run_done"), "success");
  } catch (error) {
    console.error(error);
    setStatus(error.message, "error");
  }
});

byId("executeButton").addEventListener("click", async () => {
  if (!currentActionId) return;
  if (!window.confirm(t("confirm_live"))) return;
  try {
    setStatus(t("status_live_run"));
    await postJson("/api/execute", { mode: "x-api" });
    await loadState();
    setStatus(t("status_live_run_done"), "success");
  } catch (error) {
    console.error(error);
    setStatus(error.message, "error");
  }
});

byId("languageToggle").addEventListener("click", async () => {
  currentLang = currentLang === "zh" ? "en" : "zh";
  applyStaticI18n();
  await loadState();
});

applyStaticI18n();
loadState().catch((error) => {
  console.error(error);
  setStatus(error.message, "error");
});
