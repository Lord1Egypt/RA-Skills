const $ = (sel) => document.querySelector(sel);

const ERROR_LABELS = {
  rate_limit: "限流 429",
  server_overload: "过载 503",
  timeout: "超时",
  auth_failed: "认证失败",
  network_error: "网络错误",
  model_unavailable: "模型不可用",
  context_too_long: "上下文过长",
  token_parse_error: "Token 解析错误",
  invalid_model_output: "模型输出格式错误",
  session_runtime_error: "会话运行错误",
  unknown: "未知",
};

const SESSION_LABELS = {
  prompt_aborted: "Prompt 中断",
  tool_execution_failed: "工具失败",
  shell_parse_error: "Shell 解析",
  session_takeover: "会话接管",
  task_timeout: "任务超时",
  browser_workflow_failed: "浏览器流程",
  permission_denied: "权限拒绝",
  config_error: "配置错误",
  external_side_effect_risk: "外部副作用",
  unknown_session_error: "未知会话错误",
};

const STATUS_LABELS = {
  queued: "待恢复",
  injected: "已注入",
  retrying: "重试中",
  recovered: "已恢复",
  failed: "失败",
  manual_required: "需人工",
  skipped: "已跳过",
};

let refreshTimer = null;
let localInstanceId = null;
let selectedInstance = "all";

function getInstance() {
  return $("#instanceSelect").value || "all";
}

function qs() {
  const inst = getInstance();
  return inst && inst !== "all" ? `?instance=${encodeURIComponent(inst)}` : "";
}

function formatMs(ms) {
  if (!Number.isFinite(Number(ms)) || Number(ms) < 0) return "invalid";
  ms = Number(ms);
  if (ms === 0) return "0s";
  if (ms < 60_000) {
    const seconds = ms / 1000;
    return `${seconds >= 10 ? Math.round(seconds) : seconds.toFixed(1)}s`;
  }
  if (ms < 3_600_000) {
    const minutes = ms / 60_000;
    return `${Number.isInteger(minutes) ? minutes : minutes.toFixed(1)}分钟`;
  }
  const hours = ms / 3_600_000;
  return `${Number.isInteger(hours) ? hours : hours.toFixed(1)}小时`;
}

function toast(msg) {
  const el = $("#toast");
  el.textContent = msg;
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 2500);
}

async function api(path, opts = {}) {
  const sep = path.includes("?") ? "&" : "?";
  const inst = getInstance();
  const suffix =
    inst && inst !== "all" && !path.includes("instance=")
      ? `${path.includes("?") ? "&" : "?"}instance=${encodeURIComponent(inst)}`
      : "";
  const url = path + suffix;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) {
    let msg = await res.text();
    try {
      const j = JSON.parse(msg);
      msg = j.error || msg;
    } catch {
      /* raw */
    }
    throw new Error(msg);
  }
  return res.json();
}

async function loadInstances() {
  const { instances, localInstanceId: local } = await api("/api/instances");
  localInstanceId = local;
  const sel = $("#instanceSelect");
  const prev = sel.value || "all";
  sel.innerHTML =
    '<option value="all">全部实例（聚合）</option>' +
    (instances || [])
      .map(
        (i) =>
          `<option value="${i.id}">${i.label}${i.id === local ? " · 本机" : ""}${i.isLegacy ? " (legacy)" : ""}</option>`
      )
      .join("");
  if ([...sel.options].some((o) => o.value === prev)) sel.value = prev;
  else sel.value = "all";
  selectedInstance = sel.value;
}

function renderMetrics(overview) {
  const today = overview.today;
  const hour = overview.hour;
  const el = $("#metrics");
  const instLabel =
    overview.instance === "all"
      ? `聚合 ${overview.instances?.length ?? 0} 个实例`
      : overview.instances?.find((i) => i.id === overview.instance)?.label ?? overview.instance;

  if (!today) {
    el.innerHTML = `
      <div class="metric"><div class="label">范围</div><div class="value" style="font-size:0.95rem">${instLabel}</div></div>
      <div class="metric"><div class="label">今日调用</div><div class="value">0</div></div>
      <div class="metric"><div class="label">今日失败</div><div class="value">0</div></div>
      <div class="metric"><div class="label">今日成功率</div><div class="value ok">100%</div></div>
      <div class="metric"><div class="label">活跃重试</div><div class="value">${Object.keys(overview.activeRetries || {}).length}</div></div>
      <div class="metric"><div class="label">会话待恢复</div><div class="value">${overview.sessionRetriesSummary?.pending ?? 0}</div></div>
      <div class="metric"><div class="label">需人工处理</div><div class="value ${overview.sessionRetriesSummary?.manualRequired ? "bad" : ""}">${overview.sessionRetriesSummary?.manualRequired ?? 0}</div></div>
    `;
    return;
  }
  const rateClass = today.successRate >= 95 ? "ok" : "bad";
  el.innerHTML = `
    <div class="metric"><div class="label">范围</div><div class="value" style="font-size:0.95rem">${instLabel}</div></div>
    <div class="metric"><div class="label">今日调用</div><div class="value">${today.totalCalls}</div></div>
    <div class="metric"><div class="label">今日失败</div><div class="value bad">${today.failedCalls}</div></div>
    <div class="metric"><div class="label">今日成功率</div><div class="value ${rateClass}">${today.successRate}%</div></div>
    <div class="metric"><div class="label">本小时失败</div><div class="value">${hour?.failedCalls ?? 0}</div></div>
    <div class="metric"><div class="label">活跃重试</div><div class="value">${Object.keys(overview.activeRetries || {}).length}</div></div>
    <div class="metric"><div class="label">会话待恢复</div><div class="value">${overview.sessionRetriesSummary?.pending ?? 0}</div></div>
    <div class="metric"><div class="label">需人工处理</div><div class="value ${overview.sessionRetriesSummary?.manualRequired ? "bad" : ""}">${overview.sessionRetriesSummary?.manualRequired ?? 0}</div></div>
  `;
}

function renderErrorChart(today) {
  const el = $("#errorChart");
  if (!today?.errorsByType) {
    el.innerHTML = '<p class="empty">无错误</p>';
    return;
  }
  const entries = Object.entries(today.errorsByType)
    .filter(([, n]) => n > 0)
    .sort((a, b) => b[1] - a[1]);
  if (entries.length === 0) {
    el.innerHTML = '<p class="empty">今日无错误 ✅</p>';
    return;
  }
  const max = Math.max(...entries.map(([, n]) => n));
  el.innerHTML = entries
    .map(([type, count]) => {
      const pct = Math.round((count / max) * 100);
      return `
        <div class="bar-row">
          <span>${ERROR_LABELS[type] || type}</span>
          <div class="bar-track"><div class="bar-fill danger" style="width:${pct}%"></div></div>
          <span>${count}</span>
        </div>`;
    })
    .join("");
}

function renderActiveRetries(activeRetries) {
  const el = $("#activeRetries");
  const keys = Object.keys(activeRetries || {});
  if (keys.length === 0) {
    el.innerHTML = '<li class="empty">无进行中的重试</li>';
    return;
  }
  el.innerHTML = keys
    .map((k) => {
      const s = activeRetries[k];
      const tag = s.instanceLabel
        ? `<span class="instance-tag">${s.instanceLabel}</span>`
        : "";
      return `<li>${tag}<strong>${k.split(":").pop()?.slice(0, 20) ?? k}…</strong><br/>第 ${s.attempt} 次 · ${s.strategyName}<br/><small>${s.nextRetryAt}</small></li>`;
    })
    .join("");
}

function renderRecentErrors(errors) {
  const el = $("#recentErrors");
  if (!errors?.length) {
    el.innerHTML = '<li class="empty">无最近错误</li>';
    return;
  }
  el.innerHTML = errors
    .map((e) => {
      const t = new Date(e.timestamp).toLocaleTimeString();
      const tag = e.instanceLabel
        ? `<span class="instance-tag">${e.instanceLabel}</span>`
        : "";
      return `<li>${tag}[${t}] ${e.errorLabel || e.errorType}: ${(e.errorMessage || "").slice(0, 50)}</li>`;
    })
    .join("");
}

function renderSessionRetries(data) {
  const summaryEl = $("#sessionRetrySummary");
  const listEl = $("#sessionRetries");
  const summary = data?.summary || data?.sessionRetriesSummary || {};
  const records = data?.records || data?.sessionRetries || [];
  const topCategory = Object.entries(summary.byCategory || {})
    .filter(([, n]) => n > 0)
    .sort((a, b) => b[1] - a[1])[0];

  summaryEl.innerHTML = `
    <div class="mini-metric"><span>总数</span><strong>${summary.total ?? 0}</strong></div>
    <div class="mini-metric"><span>待恢复</span><strong>${summary.pending ?? 0}</strong></div>
    <div class="mini-metric"><span>可重试</span><strong>${summary.retryable ?? 0}</strong></div>
    <div class="mini-metric warn"><span>需人工</span><strong>${summary.manualRequired ?? 0}</strong></div>
    <p class="empty">${topCategory ? `主要类型：${SESSION_LABELS[topCategory[0]] || topCategory[0]} × ${topCategory[1]}` : "暂无会话级错误"}</p>
  `;

  if (!records.length) {
    listEl.innerHTML = '<li class="empty">暂无会话或工具恢复记录</li>';
    return;
  }

  listEl.innerHTML = records
    .slice(0, 12)
    .map((r) => {
      const time = new Date(r.updatedAt || r.createdAt).toLocaleTimeString();
      const tag = r.instanceLabel
        ? `<span class="instance-tag">${r.instanceLabel}</span>`
        : "";
      const statusClass =
        r.status === "manual_required" || r.status === "failed"
          ? "danger"
          : r.status === "queued" || r.status === "retrying"
            ? "warn"
            : "ok";
      const target = r.toolName || r.taskId || r.runId || r.sessionKey || "session";
      return `
        <li>
          ${tag}<span class="status-badge ${statusClass}">${STATUS_LABELS[r.status] || r.status}</span>
          <strong>${SESSION_LABELS[r.category] || r.category}</strong>
          <span class="queue-meta">${time} · ${target} · ${r.attempt}/${r.maxAttempts}</span>
          <p>${(r.errorMessage || "").slice(0, 120)}</p>
        </li>`;
    })
    .join("");
}

async function renderModels() {
  const { models } = await api("/api/models");
  const tbody = $("#modelTable tbody");
  const entries = Object.values(models || {});
  if (entries.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" class="empty">暂无模型数据</td></tr>';
    return;
  }
  tbody.innerHTML = entries
    .sort((a, b) => b.failedCalls - a.failedCalls)
    .map(
      (m) => `
      <tr>
        <td>${m.model}</td>
        <td>${m.totalCalls}</td>
        <td>${m.failedCalls}</td>
        <td>${m.successRate}%</td>
        <td>${formatMs(m.avgDurationMs)}</td>
      </tr>`
    )
    .join("");
}

async function renderStrategies() {
  const inst = getInstance();
  const data = await api("/api/strategies");
  const { strategies, defaultStrategy, editable, instanceId } = data;
  const el = $("#strategies");
  const hint =
    inst === "all"
      ? '<p class="empty">聚合视图下请选择单个实例以编辑策略（本机实例可直接编辑）</p>'
      : !editable
        ? `<p class="empty">实例「${instanceId}」为只读；在本 Gateway 上运行才可修改其策略文件</p>`
        : "";

  if (!strategies?.length) {
    el.innerHTML = hint + '<p class="empty">无策略配置</p>';
    return;
  }

  el.innerHTML =
    hint +
    strategies
      .map((s) => {
        const isDef = s.name === defaultStrategy || s.isDefault;
        const readonly = !editable ? " readonly" : "";
        const intervals =
          s.type === "fixed"
            ? formatMs(s.intervals[0] || 0)
            : (s.intervals || []).map(formatMs).join(" → ");
        return `
        <article class="strategy ${isDef ? "default" : ""}${readonly}" data-name="${s.name}">
          <h3>${s.name} ${isDef ? '<span class="badge">默认</span>' : ""}</h3>
          <dl>
            <div>类型: ${s.type} · 最多 ${s.maxRetries} 次</div>
            <div>间隔: ${intervals}</div>
            <div>触发: ${(s.retryOn || []).map((t) => ERROR_LABELS[t] || t).join(", ")}</div>
            <div>冷却: ${formatMs(s.cooldownMs)}</div>
          </dl>
          <div class="actions">
            <button type="button" class="btn" data-action="default" ${!editable ? "disabled" : ""}>设为默认</button>
            <button type="button" class="btn ghost" data-action="bump-retries" ${!editable ? "disabled" : ""}>+1 重试次数</button>
          </div>
        </article>`;
      })
      .join("");

  if (!editable) return;

  el.querySelectorAll("[data-action]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const card = btn.closest(".strategy");
      const name = card.dataset.name;
      try {
        if (btn.dataset.action === "default") {
          await api("/api/strategies/default", {
            method: "POST",
            body: JSON.stringify({ name }),
          });
          toast(`已将「${name}」设为默认策略`);
        } else {
          const { strategies: list } = await api("/api/strategies");
          const s = list.find((x) => x.name === name);
          await api(`/api/strategies/${encodeURIComponent(name)}`, {
            method: "PUT",
            body: JSON.stringify({ maxRetries: (s?.maxRetries ?? 3) + 1 }),
          });
          toast(`已增加「${name}」最大重试次数`);
        }
        await renderStrategies();
      } catch (err) {
        toast(err.message);
      }
    });
  });
}

async function refreshAll() {
  try {
    await loadInstances();
    const overview = await api("/api/overview");
    renderMetrics(overview);
    renderErrorChart(overview.today);
    renderActiveRetries(overview.activeRetries);
    renderRecentErrors(overview.recentErrors);
    renderSessionRetries(overview);
    await renderModels();
    await renderStrategies();
    const inst = getInstance();
    $("#lastSync").textContent = `更新于 ${new Date().toLocaleTimeString()} · ${inst === "all" ? "全部" : inst}`;
  } catch (err) {
    $("#lastSync").textContent = `连接失败: ${err.message}`;
    toast("无法连接 API，请确认 OpenClaw Gateway 已启动");
  }
}

function setupRefresh() {
  if (refreshTimer) clearInterval(refreshTimer);
  const ms = Number($("#refreshInterval").value);
  if (ms > 0) refreshTimer = setInterval(refreshAll, ms);
}

$("#instanceSelect").addEventListener("change", () => {
  selectedInstance = getInstance();
  const url = new URL(window.location.href);
  if (selectedInstance === "all") url.searchParams.delete("instance");
  else url.searchParams.set("instance", selectedInstance);
  window.history.replaceState({}, "", url);
  refreshAll();
});

$("#refreshInterval").addEventListener("change", setupRefresh);
$("#btnRefresh").addEventListener("click", refreshAll);
$("#btnResetStrategies").addEventListener("click", async () => {
  if (getInstance() === "all") {
    toast("请先选择本机实例再重置策略");
    return;
  }
  if (!confirm("确定恢复为默认重试策略？")) return;
  try {
    await api("/api/strategies/reset", { method: "POST" });
    toast("已恢复默认策略");
    await renderStrategies();
  } catch (err) {
    toast(err.message);
  }
});

(function initFromUrl() {
  const p = new URLSearchParams(window.location.search).get("instance");
  if (p) selectedInstance = p;
})();

setupRefresh();
refreshAll();
