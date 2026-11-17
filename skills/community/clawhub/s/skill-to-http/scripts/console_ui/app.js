// ── Toast helper ─────────────────────────────────────────────────
// error 类型常驻（需手动关闭），success/info 3s 自动消失
function showToast(msg, type) {
  // 认证引导弹窗打开时，抑制零散的 error toast（403 会集中在引导弹窗处理）
  if (type === "error" && window.__sttAuthRequired) return;
  const container = document.getElementById("toast-container");
  if (!container) return;
  const el = document.createElement("div");
  el.className = "toast " + (type || "info");

  const text = document.createElement("span");
  text.textContent = msg;
  el.appendChild(text);

  // error 常驻，加关闭按钮
  if (type === "error") {
    const btn = document.createElement("button");
    btn.className = "toast-close";
    btn.textContent = "×";
    btn.onclick = () => {
      el.classList.add("toast-leave");
      setTimeout(() => el.remove(), 300);
    };
    el.appendChild(btn);
  } else {
    setTimeout(() => {
      el.classList.add("toast-leave");
      setTimeout(() => el.remove(), 300);
    }, 3000);
  }

  container.appendChild(el);
}

// ── Helper: API fetch with auto X-API-Key ──────────────────────────
function apiFetch(path, options = {}, timeoutMs = 8000) {
  const key = localStorage.getItem('stt-api-key') || '';
  const headers = { ...(options.headers || {}) };
  if (key) headers['X-API-Key'] = key;
  const controller = new AbortController();
  const tid = setTimeout(() => controller.abort(), timeoutMs);
  return fetch(path, { ...options, headers, signal: controller.signal })
    .then((res) => {
      // 集中处理认证失败：弹出 API Key 引导弹窗（只弹一次）
      if (res.status === 403) {
        window.dispatchEvent(new CustomEvent('stt-auth-required'));
      }
      return res;
    })
    .finally(() => clearTimeout(tid));
}

// ── Shared helpers ───────────────────────────────────────────────
function fmtLocalTime(utcStr) {
  if (!utcStr) return '—';
  try {
    const d = new Date(utcStr.replace(' ', 'T'));
    if (isNaN(d.getTime())) return utcStr.slice(0, 16);
    // 时间格式跟随当前语言：zh → zh-CN，en → en-US
    let locale = 'zh-CN';
    try {
      if (window.Alpine && Alpine.store && Alpine.store('i18n') && Alpine.store('i18n').lang === 'en') locale = 'en-US';
    } catch (_) {}
    return d.toLocaleString(locale, { hour12: false, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
  } catch (_) { return utcStr.slice(0, 16); }
}

// ── All Alpine registrations inside alpine:init ─────────────────────
document.addEventListener('alpine:init', () => {

  // ── Global store ──────────────────────────────────────────────────
  Alpine.store('nav', {
    page: 'all',
    skillFilter: '',
    jobSkillFilter: '',
    setPage(p, sf, jsf) {
      this.page = p;
      if (sf !== undefined) this.skillFilter = sf;
      if (jsf !== undefined) this.jobSkillFilter = jsf;
    }
  });

  // ── appState ──────────────────────────────────────────────────────
  Alpine.data('appState', () => ({
    apiKey: localStorage.getItem('stt-api-key') || '',
    // ── API Key 引导弹窗 ──
    showAuthGuide: false,
    authGuideKey: '',
    authGuideSaving: false,
    authGuideError: '',
    // Confirm modal state
    showConfirm: false,
    confirmTitle: '',
    confirmMessage: '',
    confirmResolve: null,

    async askConfirm(title, message) {
      this.confirmTitle = title;
      this.confirmMessage = message;
      this.showConfirm = true;
      return new Promise((resolve) => {
        this.confirmResolve = resolve;
      });
    },

    confirmAction() {
      this.showConfirm = false;
      if (this.confirmResolve) this.confirmResolve(true);
      this.confirmResolve = null;
    },

    cancelAction() {
      this.showConfirm = false;
      if (this.confirmResolve) this.confirmResolve(false);
      this.confirmResolve = null;
    },

    status: {
      running: false, port: 0, uptime_seconds: 0,
      executor: '—', skills_count: 0, active_jobs: 0,
      server_version: ''
    },

    init() {
      const removeLoading = () => {
        const el = document.getElementById('global-loading');
        if (el) { el.classList.add('fade-out'); setTimeout(() => el.remove(), 350); }
      };
      // 安全兆底：最多等 5s，无论如何移除遮罩
      const safeTimeout = setTimeout(removeLoading, 5000);
      this.refreshStatus().finally(() => {
        clearTimeout(safeTimeout);
        removeLoading();
      });
      setInterval(() => this.refreshStatus(), 5000);
      // 认证失败 → 弹 API Key 引导弹窗（只弹一次，直到用户处理）
      window.addEventListener('stt-auth-required', () => {
        if (this.showAuthGuide) return;
        window.__sttAuthRequired = true;   // 抑制零散 error toast
        this.authGuideKey = this.apiKey || '';
        this.authGuideError = '';
        this.showAuthGuide = true;
        this.$nextTick(() => { try { this.$refs.authGuideInput.focus(); } catch (_) {} });
      });
    },

    // ── API Key 引导弹窗逻辑 ──
    async submitAuthGuide() {
      const key = (this.authGuideKey || '').trim();
      if (!key) { this.authGuideError = t('auth.keyEmpty'); return; }
      this.authGuideSaving = true;
      this.authGuideError = '';
      try {
        // 先验证 key 是否正确，避免存错 key 后反复弹窗
        const res = await fetch('/api/status', { headers: { 'X-API-Key': key } });
        if (res.status === 403) {
          this.authGuideError = t('toast.authInvalid');
          return;
        }
        // 验证通过：保存 + 刷新页面（让所有组件用新 key 重新加载）
        localStorage.setItem('stt-api-key', key);
        this.apiKey = key;
        window.__sttAuthRequired = false;
        this.showAuthGuide = false;
        showToast(t('toast.authOk'), 'success');
        setTimeout(() => window.location.reload(), 600);
      } catch (e) {
        this.authGuideError = t('auth.verifyFail', { msg: e.message });
      } finally {
        this.authGuideSaving = false;
      }
    },

    dismissAuthGuide() {
      // 用户暂不填写：关闭弹窗并恢复正常 toast（后续 403 不再重复弹）
      this.showAuthGuide = false;
      window.__sttAuthRequired = false;
    },

    get page() { return Alpine.store('nav').page; },
    set page(v) { Alpine.store('nav').page = v; },
    get skillFilter() { return Alpine.store('nav').skillFilter; },
    set skillFilter(v) { Alpine.store('nav').skillFilter = v; },

    saveApiKey() {
      localStorage.setItem('stt-api-key', this.apiKey);
    },

    async refreshStatus() {
      try {
        const res = await apiFetch('/api/status');
        if (res.ok) this.status = await res.json();
      } catch (_) {}
    },

    starting: false,

    async startService() {
      if (this.starting) return;
      this.starting = true;
      try {
        // 启动含最长 30s 的就绪轮询，超时须大于后端轮询窗口
        const res = await apiFetch('/api/service/start', { method: 'POST' }, 45000);
        const data = await res.json();
        showToast(data.ok ? (data.message || t('toast.startOk')) : t('toast.startFail', { msg: data.message || t('common.unknownError') }), data.ok ? 'success' : 'error');
        await this.refreshStatus();
      } catch (e) {
        const msg = (e && e.name === 'AbortError')
          ? t('toast.startTimeout')
          : e.message;
        showToast(t('toast.startFail', { msg }), 'error');
      } finally {
        this.starting = false;
      }
    },

    async stopService() {
      const confirmed = await this.askConfirm(t('cf.title'), t('cf.stopMsg'));
      if (!confirmed) return;
      try {
        const res = await apiFetch('/api/service/stop', { method: 'POST' });
        const data = await res.json();
        showToast(data.message, 'success');
        await this.refreshStatus();
      } catch (e) {
        showToast(t('toast.stopFail', { msg: e.message }), 'error');
      }
    },

    async reloadService() {
      try {
        const res = await apiFetch('/api/service/reload', { method: 'POST' });
        const data = await res.json();
        showToast(data.ok ? t('toast.reloadOk') : t('toast.reloadFail', { msg: data.detail || '' }), data.ok ? 'success' : 'error');
        await this.refreshStatus();
      } catch (e) {
        showToast(t('toast.reloadFail', { msg: e.message }), 'error');
      }
    },

    formatUptime(seconds) {
      if (!seconds || seconds <= 0) return '—';
      const h = Math.floor(seconds / 3600);
      const m = Math.floor((seconds % 3600) / 60);
      return h > 0 ? `${h}h ${m}m` : `${m}m`;
    }
  }));

  // ── skillList ─────────────────────────────────────────────────────
  Alpine.data('skillList', () => ({
    skills: [],
    search: '',
    loading: true,
    expanded: null,
    testing: null,
    testMessage: '',
    testingJobId: null,
    testStatus: null,
    testResult: null,
    testError: null,
    testPollCount: 0,
    _pollTimer: null,

    init() {
      this.loadSkills();
    },

    async loadSkills() {
      this.loading = true;
      try {
        const res = await apiFetch('/api/skills');
        if (res.ok) this.skills = await res.json();
      } catch (e) {
        console.error('Failed to load skills:', e);
      }
      this.loading = false;
    },

    filteredSkills() {
      const filter = Alpine.store('nav').skillFilter;
      let list = this.skills;
      if (filter === 'exposed') list = list.filter(s => s.exposed);
      else if (filter === 'hidden') list = list.filter(s => !s.exposed);
      if (this.search) {
        const q = this.search.toLowerCase();
        list = list.filter(s =>
          s.name.toLowerCase().includes(q) ||
          (s.description || '').toLowerCase().includes(q)
        );
      }
      return list;
    },

    toggleExpand(name) {
      this.expanded = this.expanded === name ? null : name;
    },

    // 依赖确认弹窗状态
    depConfirmSkill: null,
    depConfirmDeps: [],
    depConfirmEvidence: [],

    async exposeSkill(name) {
      try {
        const res = await apiFetch('/api/skills/' + encodeURIComponent(name) + '/expose', { method: 'POST' });
        const data = await res.json();
        if (!data.ok) { showToast(t('toast.exposeFail', { msg: data.message }), 'error'); return; }
        await this.loadSkills();
        // 如有发现依赖，弹确认弹窗
        if (data.needs_confirm && data.dep_scan && data.dep_scan.deps.length > 0) {
          this.depConfirmSkill = name;
          this.depConfirmDeps = data.dep_scan.deps;
          this.depConfirmEvidence = data.dep_scan.evidence || [];
        }
      } catch (e) {
        showToast(t('toast.exposeFail', { msg: e.message }), 'error');
      }
    },

    async confirmDeps(name, confirmed) {
      // confirmed=true: 确认有依赖，用 speed mode 时注入
      // confirmed=false: 忽略，正常走速度模式
      try {
        await apiFetch('/api/skills/' + encodeURIComponent(name) + '/deps', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            deps: confirmed ? this.depConfirmDeps : [],
            confirmed_by_user: true,
            use_speed_mode: true,  // 两种情况都用极速模式，有依赖时注入
          })
        });
      } catch (e) { /* non-critical */ }
      this.depConfirmSkill = null;
      this.depConfirmDeps = [];
      this.depConfirmEvidence = [];
    },

    async hideSkill(name) {
      try {
        const res = await apiFetch('/api/skills/' + encodeURIComponent(name) + '/hide', { method: 'POST' });
        const data = await res.json();
        if (data.ok) await this.loadSkills();
        else showToast(t('toast.hideFail', { msg: data.message }), 'error');
      } catch (e) {
        showToast(t('toast.hideFail', { msg: e.message }), 'error');
      }
    },

    startTest(name) {
      this.expanded = name;
      this.testing = name;
      this.testMessage = '';
      this.testingJobId = null;
      this.testStatus = null;
      this.testResult = null;
      this.testError = null;
      this.testPollCount = 0;
      if (this._pollTimer) clearInterval(this._pollTimer);
    },

    async runTest(name) {
      if (!this.testMessage.trim()) return;

      // 前置检查：主服务未运行时给出可操作的引导，而不是让 fetch 报晦涩错误
      if (!this.status.running) {
        this.testError = null;
        this.testResult = null;
        this.testStatus = null;
        showToast(t('toast.serverNotRunning'), 'error');
        return;
      }

      try {
        const res = await apiFetch('/api/skills/' + encodeURIComponent(name) + '/run', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: this.testMessage })
        }, 15000);  // proxy 到主服务最长约 10s，给 15s 余量
        let data = null;
        try { data = await res.json(); } catch (_) { /* 非 JSON 响应 */ }

        if (res.ok && data && data.job_id) {
          this.testingJobId = data.job_id;
          this.testStatus = 'pending';
          this.testPollCount = 0;
          this._startPolling(data.job_id);
          return;
        }

        // 后端明确返回 503 / detail 含 "not running"：给引导
        if (res.status === 503 || (data && /not running|未运行/i.test(JSON.stringify(data)))) {
          showToast(t('toast.serverStopped'), 'error');
          return;
        }
        const detail = (data && (data.detail || data.message)) || `HTTP ${res.status}`;
        showToast(t('toast.execFail', { msg: detail }), 'error');
      } catch (e) {
        // AbortError = 前端超时；TypeError/Failed to fetch = 网络/控制台不可达
        if (e && e.name === 'AbortError') {
          showToast(t('toast.reqTimeout'), 'error');
        } else if (/Failed to fetch|NetworkError/i.test(e.message || '')) {
          showToast(t('toast.netError'), 'error');
        } else {
          showToast(t('toast.execFail', { msg: e.message }), 'error');
        }
      }
    },

    _startPolling(jobId) {
      if (this._pollTimer) clearInterval(this._pollTimer);
      const MAX_POLLS = 80; // 80 次 × 3s = 240s
      this._pollTimer = setInterval(async () => {
        this.testPollCount++;
        if (this.testPollCount > MAX_POLLS) {
          clearInterval(this._pollTimer);
          this.testError = t('test.pollTimeout');
          return;
        }
        try {
          // 先查控制台 SQLite（history_store）
          const res = await apiFetch('/api/jobs/' + jobId);
          if (res.ok) {
            const job = await res.json();
            this.testStatus = job.status;
            if (job.status === 'completed') {
              this.testResult = job.result;
              clearInterval(this._pollTimer);
              return;
            } else if (job.status === 'failed') {
              this.testError = job.error || t('test.execFail');
              clearInterval(this._pollTimer);
              return;
            }
          }
          // SQLite 还没写入时，尝试直接查主服务的 job
          const res2 = await apiFetch('/api/status');
          if (res2.ok) {
            const srvStatus = await res2.json();
            if (srvStatus.running && srvStatus.port) {
              try {
                const r3 = await fetch('http://' + location.hostname + ':' + srvStatus.port + '/jobs/' + jobId);
                if (r3.ok) {
                  const job2 = await r3.json();
                  this.testStatus = job2.status;
                  if (job2.status === 'completed') {
                    this.testResult = job2.result;
                    clearInterval(this._pollTimer);
                  } else if (job2.status === 'failed') {
                    this.testError = job2.error || t('test.execFail');
                    clearInterval(this._pollTimer);
                  }
                }
              } catch (_) {}
            }
          }
        } catch (_) {}
      }, 3000);
    },

    destroy() {
      if (this._pollTimer) clearInterval(this._pollTimer);
    }
  }));

  // ── jobHistory ────────────────────────────────────────────────────
  Alpine.data('jobHistory', () => ({
    jobs: [],
    jobSkillFilter: Alpine.store('nav').jobSkillFilter || '',
    expandedJob: null,
    detailJob: null,

    init() {
      this.loadJobs();
    },

    async loadJobs() {
      try {
        let url = '/api/jobs?limit=50';
        if (this.jobSkillFilter) url += '&skill=' + encodeURIComponent(this.jobSkillFilter);
        const res = await apiFetch(url);
        if (res.ok) this.jobs = await res.json();
      } catch (e) {
        console.error('Failed to load jobs:', e);
      }
    },

    toggleExpand(jobId) {
      this.expandedJob = this.expandedJob === jobId ? null : jobId;
    },

    async openDetailModal(job) {
      // 先用列表数据展示，再异步拉完整字段
      this.detailJob = { ...job, _loading: true };
      try {
        const res = await apiFetch('/api/jobs/' + encodeURIComponent(job.job_id));
        if (res.ok) {
          this.detailJob = await res.json();
        } else {
          // 请求失败：保留列表缓存，去掉 loading 标记，加警告
          this.detailJob = { ...job, _fetch_warn: t('detail.loadFail') };
        }
      } catch (e) {
        this.detailJob = { ...job, _fetch_warn: t('detail.netError', { msg: e.message }) };
      }
    },

    copyText(text) {
      if (!text) return;
      navigator.clipboard.writeText(text).then(
        () => showToast(t('toast.copyOk', { label: t('cp.content') }), 'success'),
        () => showToast(t('toast.copyFail'), 'error')
      );
    }
  }));

  // ── serverLog ─────────────────────────────────────────────────────
  Alpine.data('serverLog', () => ({
    log: '',
    _defaultText: '',

    init() {
      // 语言可能未 ready，safe fallback
      try { this.log = t('log.loading'); this._defaultText = this.log; } catch(_) { this.log = 'Loading...'; }
      this.refresh();
    },

    async refresh() {
      try {
        const res = await apiFetch('/api/logs');
        if (res.ok) {
          const data = await res.json();
          this.log = data.content || t('log.empty');
        }
      } catch (e) {
        this.log = t('log.loadFail', { msg: e.message });
      }
    }
  }));

// ── Alpine.data: TLS / HTTPS Certificate ───────────────────────────
  Alpine.data('tlsPage', () => ({
    tls: { tls_enabled: false, cert_path: '', key_path: '', cert_status: null },
    loading: false,
    renewing: false,
    renewResult: '',
    showRenewConfirm: false,

    // 复制文本到剪贴板（带降级），供"复制命令/复制给 Agent"按钮使用
    async copyText(text, label) {
      const okMsg = () => t('toast.copyOk', { label: label || t('cp.content') });
      try {
        await navigator.clipboard.writeText(text);
        showToast(okMsg(), 'success');
      } catch (_) {
        // http 非安全上下文降级方案
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try {
          document.execCommand('copy');
          showToast(okMsg(), 'success');
        } catch (e2) {
          showToast(t('toast.copyFail'), 'error');
        }
        ta.remove();
      }
    },

    get upgradeCmd() {
      // 引用 $store.i18n.tick 强制切语言时重算
      const _ = window.Alpine && Alpine.store('i18n') ? Alpine.store('i18n').tick : 0;
      return t('tls.upgradeCmd');
    },

    get agentUpgradeMsg() {
      const _ = window.Alpine && Alpine.store('i18n') ? Alpine.store('i18n').tick : 0;
      return t('tls.agentUpgradeMsg');
    },

    get agentRenewMsg() {
      const _ = window.Alpine && Alpine.store('i18n') ? Alpine.store('i18n').tick : 0;
      return t('tls.agentRenewMsg');
    },

    async init() {
      await this.refresh();
    },

    async refresh() {
      this.loading = true;
      try {
        const res = await apiFetch('/api/tls');
        if (res.ok) {
          this.tls = await res.json();
        } else {
          showToast(t('toast.certLoadFail', { code: res.status }), 'error');
        }
      } catch (e) {
        showToast(t('toast.certLoadFail', { code: e.message }), 'error');
      } finally {
        this.loading = false;
      }
    },

    confirmRenew() {
      this.showRenewConfirm = true;
    },

    async doRenew() {
      this.showRenewConfirm = false;
      this.renewing = true;
      this.renewResult = '';
      try {
        const res = await apiFetch('/api/tls/renew', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
          this.renewResult = (data.stdout || '') + (data.stderr ? '\n[stderr]\n' + data.stderr : '');
          showToast(t('toast.renewOk'), 'success');
          // 刷新证书状态
          await this.refresh();
        } else {
          this.renewResult = 'ERROR: ' + (data.error || data.stderr || t('common.unknownError'));
          showToast(t('toast.renewFail', { msg: '' }), 'error');
        }
      } catch (e) {
        showToast(t('toast.renewFail', { msg: e.message }), 'error');
      } finally {
        this.renewing = false;
      }
    }
  }));

// ── Alpine.data: Speed Mode ────────────────────────────────────────
  Alpine.data('speedMode', () => ({
    smStatus: { enabled: false, applicable: true, agent_registered: false },
    smShowConfirm: false,
    smShowDisableConfirm: false,
    initializing: false,
    progressLogs: [],

    init() {
      this.loadStatus();
    },

    async loadStatus() {
      try {
        const res = await apiFetch('/api/speed_mode/status');
        if (res.ok) this.smStatus = await res.json();
      } catch (e) {}
    },

    handleToggle() {
      if (!this.smStatus.applicable) return;
      if (this.smStatus.enabled) {
        this.smShowDisableConfirm = true;
      } else {
        this.smShowConfirm = true;
      }
    },

    async doEnable() {
      this.smShowConfirm = false;
      this.initializing = true;
      this.progressLogs = [];

      try {
        const res = await apiFetch('/api/speed_mode/enable', { method: 'POST' }, 0);
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buf = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buf += decoder.decode(value, { stream: true });
          const lines = buf.split('\n');
          buf = lines.pop();
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const evt = JSON.parse(line.slice(6));
                this.progressLogs.push(evt);
                if (evt.done) {
                  await this.loadStatus();
                }
              } catch (e) {}
            }
          }
        }
      } catch (e) {
        this.progressLogs.push({ step: 0, total: 6, msg: t('sm.connectFail', { msg: e.message }), error: true });
      } finally {
        this.initializing = false;
      }
    },

    async doDisable() {
      this.smShowDisableConfirm = false;
      try {
        const res = await apiFetch('/api/speed_mode/disable', { method: 'POST' });
        const data = await res.json();
        showToast(data.ok ? t('toast.speedOff') : t('toast.speedFail', { msg: data.message }), data.ok ? 'success' : 'error');
        await this.loadStatus();
      } catch (e) {
        showToast(t('toast.speedFail', { msg: e.message }), 'error');
      }
    },

    btnLabel() {
      if (this.initializing) return t('sm.btnInitializing');
      if (!this.smStatus.applicable) return t('sm.btnLabel');
      return this.smStatus.enabled ? t('sm.btnOn') : t('sm.btnLabel');
    },

    btnClass() {
      if (!this.smStatus.applicable) return 'btn-speed-na';
      if (this.smStatus.enabled) return 'btn-speed-on';
      return '';
    },

    btnTitle() {
      if (!this.smStatus.applicable)
        return t('sm.titleNa', { exec: this.smStatus.executor || 'auto' });
      if (this.smStatus.enabled) return t('sm.titleOn');
      return t('sm.titleOff');
    }
  }));

}); // end alpine:init
