import React, { useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import katex from "katex";
import "katex/dist/katex.min.css";
import {
  Bot,
  Check,
  FileText,
  HelpCircle,
  Loader2,
  RefreshCw,
  Settings,
  Square,
  Upload,
  Wand2,
  X
} from "lucide-react";
import "./styles.css";

const API = "/api";
const ACCEPTED_EXTENSIONS = [".doc", ".docx", ".wps"];

type Task = {
  id: string;
  name: string;
  status: string;
  source_name?: string;
  latest_version_id?: string;
};

type Candidate = {
  id: string;
  text: string;
  context: string;
  confidence: number;
  default_action: string;
  page_number: number;
  local_latex: string;
  local_action?: string;
  ai_latex?: string | null;
  ai_action?: string | null;
  ai_reason?: string | null;
  ai_status?: string | null;
};

type TaskState = {
  source_name?: string;
  engine?: string;
  mode?: string;
  page_count?: number;
  summary?: Record<string, number>;
  candidates?: Candidate[];
  selections?: Record<string, Choice>;
  ai_ready?: boolean;
  ai_running?: boolean;
  ai_model?: string;
  ai_summary?: { done?: number; total?: number; failed?: number };
  latest_version_id?: string;
};

type Version = {
  id: string;
  label: string;
  created_at: string;
  converted: number;
  kept: number;
  failed: number;
};

type AiConfig = {
  api_key: string;
  base_url: string;
  model: string;
  batch_size?: number;
  max_workers?: number;
  failure_fallback?: string;
};

type Choice = "source" | "local" | "ai" | "keep" | "convert" | "review";

const DEFAULT_AI_CONFIG: AiConfig = {
  api_key: "",
  base_url: "https://api.openai.com/v1",
  model: "gpt-4.1-mini"
};
const GREEK_COMMANDS = [
  "alpha",
  "beta",
  "gamma",
  "delta",
  "epsilon",
  "varepsilon",
  "zeta",
  "eta",
  "theta",
  "vartheta",
  "kappa",
  "lambda",
  "mu",
  "nu",
  "xi",
  "pi",
  "rho",
  "sigma",
  "tau",
  "phi",
  "chi",
  "psi",
  "omega",
  "Gamma",
  "Delta",
  "Theta",
  "Lambda",
  "Xi",
  "Pi",
  "Sigma",
  "Phi",
  "Psi",
  "Omega",
  "ell"
].join("|");
const GREEK_COMMAND_FOLLOWED_BY_LETTER = new RegExp(`\\\\(${GREEK_COMMANDS})(?=[A-Za-z])`, "g");

function App() {
  const [task, setTask] = useState<Task | null>(null);
  const [state, setState] = useState<TaskState>({});
  const [versions, setVersions] = useState<Version[]>([]);
  const [busy, setBusy] = useState("");
  const [message, setMessage] = useState("");
  const [engine, setEngine] = useState("auto");
  const [mode, setMode] = useState("balanced");
  const [aiBatchSize, setAiBatchSize] = useState(10);
  const [aiWorkers, setAiWorkers] = useState(5);
  const [aiFallback, setAiFallback] = useState("rule");
  const [aiConfig, setAiConfig] = useState<AiConfig>(DEFAULT_AI_CONFIG);
  const [draftAiConfig, setDraftAiConfig] = useState<AiConfig>(DEFAULT_AI_CONFIG);
  const [draftAiBatchSize, setDraftAiBatchSize] = useState(10);
  const [draftAiWorkers, setDraftAiWorkers] = useState(5);
  const [draftAiFallback, setDraftAiFallback] = useState("rule");
  const [aiConfigOpen, setAiConfigOpen] = useState(false);
  const [aiTestState, setAiTestState] = useState<"idle" | "testing" | "ok" | "failed">("idle");
  const [aiTestMessage, setAiTestMessage] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [activeCandidate, setActiveCandidate] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const listRef = useRef<HTMLDivElement>(null);
  const pollRef = useRef<number | null>(null);

  const candidates = state.candidates ?? [];
  const selections = normalizeSelections(state.selections ?? {}, candidates);
  const pageCount = state.page_count ?? 0;
  const latestVersion = versions[versions.length - 1];
  const hasCurrentWork = Boolean(state.source_name || candidates.length || latestVersion);
  const isProcessing = Boolean(busy && busy.includes("预览"));
  const isAiRunning = Boolean(state.ai_running || busy.includes("AI 转换中"));

  useEffect(() => {
    void loadSession();
    void loadAiConfig();
    return () => {
      if (pollRef.current) window.clearInterval(pollRef.current);
    };
  }, []);

  async function loadSession() {
    const payload = await api<{ task: Task; state: TaskState; versions: Version[] }>("/session");
    setTask(payload.task);
    setState(payload.state ?? {});
    setVersions(payload.versions ?? []);
    syncSettings(payload.state ?? {});
    focusFirstCandidate(payload.state ?? {});
  }

  async function loadAiConfig() {
    const config = await api<AiConfig>("/ai-config");
    setAiConfig(config);
    setDraftAiConfig(config);
    setAiBatchSize(config.batch_size ?? 10);
    setAiWorkers(config.max_workers ?? 5);
    setAiFallback(config.failure_fallback ?? "rule");
  }

  function syncSettings(nextState: TaskState) {
    if (nextState.engine) setEngine(nextState.engine);
    if (nextState.mode) setMode(nextState.mode);
  }

  async function resetSession(confirmFirst = true) {
    if (confirmFirst && !window.confirm("当前任务及所有历史文件将被删除，确认继续吗？")) return null;
    setBusy("正在清空当前任务");
    setMessage("");
    try {
      const payload = await api<{ task: Task; state: TaskState; versions: Version[] }>("/session/reset", { method: "POST" });
      setTask(payload.task);
      setState(payload.state ?? {});
      setVersions(payload.versions ?? []);
      setCurrentPage(1);
      setActiveCandidate(null);
      setMessage("已清空，可以上传新的 Word 文档");
      return payload.task;
    } finally {
      setBusy("");
    }
  }

  async function handleFileSelected(file: File) {
    if (!isAcceptedFile(file)) {
      setMessage("仅支持 .doc / .docx / .wps 文件");
      return;
    }
    let currentTask = task;
    if (hasCurrentWork) {
      if (!window.confirm("上传新文档会删除当前任务及所有历史文件，确认继续吗？")) return;
      currentTask = await resetSession(false);
    }
    if (!currentTask) {
      const payload = await api<{ task: Task; state: TaskState; versions: Version[] }>("/session");
      currentTask = payload.task;
      setTask(payload.task);
    }
    await uploadFile(currentTask.id, file);
  }

  async function uploadFile(taskId: string, file: File) {
    setBusy("预览及公式识别中");
    setMessage("");
    setState((prev) => ({ ...prev, source_name: file.name, page_count: 0, candidates: [], selections: {} }));
    const form = new FormData();
    form.append("file", file);
    try {
      const payload = await api<{ task: Task; state: TaskState }>(
        `/tasks/${taskId}/upload?engine=${engine}&mode=${mode}&skip_bibliography=true`,
        { method: "POST", body: form, json: false }
      );
      setTask(payload.task);
      setState(payload.state);
      setVersions([]);
      syncSettings(payload.state);
      focusFirstCandidate(payload.state);
      setMessage(`已识别 ${payload.state.candidates?.length ?? 0} 个疑似公式`);
    } catch (exc) {
      setMessage(exc instanceof Error ? exc.message : "上传或识别失败");
    } finally {
      setBusy("");
      setDragActive(false);
    }
  }

  function setChoice(candidateId: string, choice: Choice) {
    setState((prev) => ({
      ...prev,
      selections: { ...prev.selections, [candidateId]: choice }
    }));
  }

  function bulkSelect(choice: Choice) {
    const next: Record<string, Choice> = {};
    candidates.forEach((candidate) => {
      next[candidate.id] = choice;
    });
    setState((prev) => ({ ...prev, selections: next }));
  }

  async function runAiReview() {
    if (!task) return;
    if (pollRef.current) window.clearInterval(pollRef.current);
    setBusy("AI 转换中");
    setMessage("");
    try {
      const payload = await api<{ state: TaskState; job_id: string }>(`/tasks/${task.id}/ai-review/start`, {
        method: "POST",
        body: JSON.stringify({
          api_key: aiConfig.api_key,
          base_url: aiConfig.base_url,
          model: aiConfig.model,
          batch_size: aiBatchSize,
          max_workers: aiWorkers,
          failure_fallback: aiFallback,
          timeout_seconds: 60,
          retries: 1
        })
      });
      setState(payload.state);
      setMessage("AI 转换已开始");
      pollRef.current = window.setInterval(() => void pollAiStatus(task.id), 900);
    } catch (exc) {
      setMessage(exc instanceof Error ? exc.message : "AI 转换失败");
      setBusy("");
    }
  }

  async function stopAiReview() {
    if (!task) return;
    setMessage("正在停止 AI 请求");
    try {
      const payload = await api<{ state: TaskState; running: boolean; summary?: { done?: number; total?: number; failed?: number } }>(
        `/tasks/${task.id}/ai-review/stop`,
        { method: "POST" }
      );
      setState(payload.state);
      if (pollRef.current) window.clearInterval(pollRef.current);
      pollRef.current = null;
      setBusy("");
      const done = payload.summary?.done ?? payload.state.ai_summary?.done ?? payload.state.candidates?.length ?? 0;
      const total = payload.summary?.total ?? payload.state.ai_summary?.total ?? payload.state.candidates?.length ?? 0;
      setMessage(`AI 请求已停止，未完成内容已按失败策略回退：${done} / ${total}`);
    } catch (exc) {
      setMessage(exc instanceof Error ? exc.message : "停止 AI 请求失败");
    }
  }

  async function pollAiStatus(taskId: string) {
    try {
      const payload = await api<{ state: TaskState; running: boolean; actions: Record<string, number>; summary?: { done?: number; total?: number; failed?: number } }>(
        `/tasks/${taskId}/ai-review/status`
      );
      setState(payload.state);
      const done = payload.summary?.done ?? 0;
      const total = payload.summary?.total ?? payload.state.candidates?.length ?? 0;
      const failed = payload.summary?.failed ?? 0;
      setMessage(payload.running ? `AI 转换中：${done} / ${total}` : `AI 转换完成：${done} / ${total}${failed ? `，回退 ${failed}` : ""}`);
      if (!payload.running) {
        if (pollRef.current) window.clearInterval(pollRef.current);
        pollRef.current = null;
        setBusy("");
      }
    } catch (exc) {
      if (pollRef.current) window.clearInterval(pollRef.current);
      pollRef.current = null;
      setBusy("");
      setMessage(exc instanceof Error ? exc.message : "AI 状态同步失败");
    } finally {
    }
  }

  async function applySelections() {
    if (!task) return;
    setBusy("正在生成转换后的 Word 文档");
    setMessage("");
    try {
      const payload = await api<{ version: Version }>(`/tasks/${task.id}/apply`, {
        method: "POST",
        body: JSON.stringify({
          selections,
          label: state.ai_ready ? "AI-assisted conversion" : "Local algorithm conversion"
        })
      });
      setVersions((prev) => [...prev, payload.version]);
      setState((prev) => ({ ...prev, latest_version_id: payload.version.id }));
      setMessage(`已生成 Word：转换 ${payload.version.converted} 条，保留 ${payload.version.kept} 条`);
      window.location.href = `${API}/versions/${payload.version.id}/download`;
    } catch (exc) {
      setMessage(exc instanceof Error ? exc.message : "生成失败");
    } finally {
      setBusy("");
    }
  }

  async function testAiConfig() {
    setAiTestState("testing");
    setAiTestMessage("");
    const result = await api<{ ok: boolean; reply?: string; error?: string }>("/ai-config/test", {
      method: "POST",
      body: JSON.stringify(draftAiConfig)
    });
    if (result.ok) {
      setAiTestState("ok");
      setAiTestMessage(`模型配置成功：${result.reply ?? "已收到回复"}`);
    } else {
      setAiTestState("failed");
      setAiTestMessage(`模型配置失败：${result.error ?? "无法获取回复"}`);
    }
  }

  async function saveAiConfig() {
    if (aiTestState === "failed" && !window.confirm("当前模型测试失败，可能无法正常使用。仍然保存吗？")) return;
    const payload = await api<{ config: AiConfig }>("/ai-config", {
      method: "POST",
      body: JSON.stringify({
        ...draftAiConfig,
        batch_size: Math.max(1, Number(draftAiBatchSize) || 10),
        max_workers: Math.max(1, Number(draftAiWorkers) || 5),
        failure_fallback: draftAiFallback
      })
    });
    setAiConfig(payload.config);
    setDraftAiConfig(payload.config);
    setAiBatchSize(payload.config.batch_size ?? Math.max(1, Number(draftAiBatchSize) || 10));
    setAiWorkers(payload.config.max_workers ?? Math.max(1, Number(draftAiWorkers) || 5));
    setAiFallback(payload.config.failure_fallback ?? draftAiFallback);
    setAiConfigOpen(false);
    setMessage("AI 模型配置已保存");
  }

  function openAiConfig() {
    setDraftAiConfig(aiConfig);
    setDraftAiBatchSize(aiBatchSize);
    setDraftAiWorkers(aiWorkers);
    setDraftAiFallback(aiFallback);
    setAiTestState("idle");
    setAiTestMessage("");
    setAiConfigOpen(true);
  }

  function trackVisibleCandidate(candidate: Candidate) {
    setActiveCandidate(candidate.id);
    if (candidate.page_number) setCurrentPage(candidate.page_number);
  }

  function chooseCandidate(candidate: Candidate, choice: Choice) {
    setChoice(candidate.id, choice);
  }

  function focusFirstCandidate(nextState: TaskState) {
    const first = nextState.candidates?.[0];
    if (first) {
      setActiveCandidate(first.id);
      setCurrentPage(first.page_number || 1);
    } else if (nextState.page_count) {
      setActiveCandidate(null);
      setCurrentPage(1);
    }
  }

  function handlePreviewDrop(event: React.DragEvent<HTMLElement>) {
    event.preventDefault();
    setDragActive(false);
    const file = event.dataTransfer.files?.[0];
    if (file) void handleFileSelected(file);
  }

  useEffect(() => {
    const list = listRef.current;
    if (!list || candidates.length === 0) return;
    let frame = 0;
    const syncVisibleCandidate = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const listRect = list.getBoundingClientRect();
        const trackingLine = listRect.top + listRect.height * 0.35;
        const cards = Array.from(list.querySelectorAll<HTMLElement>("[data-candidate-id]"));
        const visible = cards
          .map((card) => ({
            id: card.dataset.candidateId,
            distance: Math.abs(card.getBoundingClientRect().top - trackingLine)
          }))
          .filter((item): item is { id: string; distance: number } => Boolean(item.id))
          .sort((a, b) => a.distance - b.distance)[0];
        if (!visible || visible.id === activeCandidate) return;
        const candidate = candidates.find((item) => item.id === visible.id);
        if (!candidate) return;
        trackVisibleCandidate(candidate);
      });
    };
    list.addEventListener("scroll", syncVisibleCandidate, { passive: true });
    return () => {
      cancelAnimationFrame(frame);
      list.removeEventListener("scroll", syncVisibleCandidate);
    };
  }, [activeCandidate, candidates]);

  return (
    <div className="app-shell">
      <header className="top-header panel">
        <div className="brand">
          <div className="brand-logo">∑</div>
          <div>
            <strong>Word 公式快速转换</strong>
            <span>一次上传 · 公式审核 · 生成下载</span>
          </div>
        </div>
        <div className="settings-strip">
          <button className="settings-title" onClick={openAiConfig}>
            <Settings size={16} />
            <strong>AI模型配置</strong>
          </button>
          <label>
            <span>转换引擎 <InfoButton text="Auto 会在 macOS 和 Windows 上优先调用 Microsoft Word；只有 Word 调用失败才回退到 LibreOffice。Linux 下会使用 LibreOffice。" /></span>
            <select value={engine} onChange={(event) => setEngine(event.target.value)}>
              <option value="auto">Auto · Word 优先</option>
              <option value="word">Microsoft Word</option>
              <option value="libreoffice">LibreOffice</option>
            </select>
          </label>
          <label>
            <span>严谨度 <InfoButton text="Balanced 适合多数论文；Conservative 更少误转；Aggressive 会尝试转换更多候选；Display only 偏向完整展示型公式。" /></span>
            <select value={mode} onChange={(event) => setMode(event.target.value)}>
              <option value="balanced">Balanced</option>
              <option value="conservative">Conservative</option>
              <option value="aggressive">Aggressive</option>
              <option value="display-only">Display only</option>
            </select>
          </label>
        </div>

        <div className="toolbar-actions">
          <button className="secondary" disabled={Boolean(busy)} onClick={() => void resetSession(true)}>
            <RefreshCw size={15} />
            新任务/清空
          </button>
          {isAiRunning ? (
            <button className="danger" disabled={!isAiRunning} onClick={() => void stopAiReview()}>
              <Square size={14} />
              停止AI请求
            </button>
          ) : (
            <button disabled={!candidates.length || Boolean(busy)} onClick={() => void runAiReview()}>
              <Bot size={15} />
              AI 转换
            </button>
          )}
          <button disabled={!candidates.length || Boolean(busy)} onClick={() => void applySelections()}>
            <Wand2 size={15} />
            生成 Word
          </button>
        </div>
      </header>

      <main className="workspace">
        <section className="preview-panel panel">
          <div className="panel-header">
            <div>
              <h2>页面预览</h2>
              <span>{state.source_name ?? "点击或拖拽上传 Word 文档"}</span>
            </div>
            <div className="page-controls">
              <button disabled={currentPage <= 1} onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}>上一页</button>
              <strong>{pageCount ? `${currentPage} / ${pageCount}` : "无预览"}</strong>
              <button disabled={!pageCount || currentPage >= pageCount} onClick={() => setCurrentPage((p) => Math.min(pageCount, p + 1))}>下一页</button>
            </div>
          </div>
          <div
            className={`preview-stage ${dragActive ? "drag-active" : ""}`}
            onDragEnter={(event) => {
              event.preventDefault();
              setDragActive(true);
            }}
            onDragOver={(event) => event.preventDefault()}
            onDragLeave={(event) => {
              if (event.currentTarget === event.target) setDragActive(false);
            }}
            onDrop={handlePreviewDrop}
          >
            {isProcessing ? (
              <div className="preview-empty processing">
                <Loader2 size={38} />
                <strong>预览及公式识别中</strong>
                <p>正在调用 Word/LibreOffice 生成预览，并提取疑似公式。</p>
              </div>
            ) : task && pageCount ? (
              <img
                src={`${API}/tasks/${task.id}/preview/pages/${currentPage}?v=${state.source_name ?? ""}`}
                alt={`page ${currentPage}`}
              />
            ) : (
              <label className="preview-upload">
                <Upload size={24} />
                <strong>上传 Word 文档</strong>
                <span>点击选择，或将 .doc / .docx / .wps 拖拽到这里</span>
                <input
                  type="file"
                  accept=".doc,.docx,.wps"
                  disabled={Boolean(busy)}
                  onChange={(event) => {
                    const file = event.target.files?.[0];
                    if (file) void handleFileSelected(file);
                    event.currentTarget.value = "";
                  }}
                />
              </label>
            )}
          </div>
        </section>

        <section className="formula-panel panel">
          <div className="formula-topbar compact">
            <div>
              <h2>公式审核</h2>
              <span>{message || "滚动列表时，左侧预览会跟随当前公式所在页。"}</span>
            </div>
            <div className="header-actions">
              <button className="secondary" disabled={!candidates.length || Boolean(busy)} onClick={() => bulkSelect("source")}>
                全用原文
              </button>
              <button className="secondary" disabled={!candidates.length || Boolean(busy)} onClick={() => bulkSelect("local")}>
                全用算法
              </button>
              <button className="secondary" disabled={!state.ai_ready || Boolean(busy)} onClick={() => bulkSelect("ai")}>
                全用 AI
              </button>
            </div>
          </div>

          <div className="candidate-head">
            <span>原文公式片段</span>
            <span>算法转换结果</span>
            <span>AI转换结果</span>
          </div>
          <div className="candidate-list" ref={listRef}>
            {candidates.length === 0 && <Empty text="上传文档后，这里会列出所有疑似公式和本地转换结果。" />}
            {candidates.map((candidate) => {
              const choice = normalizeChoice(selections[candidate.id], candidate);
              return (
                <article
                  key={candidate.id}
                  data-candidate-id={candidate.id}
                  className={`candidate-card ${candidate.id === activeCandidate ? "active" : ""}`}
                >
                  <CandidateOption
                    active={choice === "source"}
                    title={`第 ${candidate.page_number} 页`}
                    badge={`匹配度 ${Math.round(candidate.confidence * 100)}%`}
                    value={candidate.text}
                    onClick={() => chooseCandidate(candidate, "source")}
                  />
                  <CandidateOption
                    active={choice === "local"}
                    title="算法转换结果"
                    value={candidate.local_latex}
                    math
                    onClick={() => chooseCandidate(candidate, "local")}
                  />
                  <CandidateOption
                    active={choice === "ai"}
                    title={aiResultTitle(candidate)}
                    value={aiResultValue(candidate, state.ai_ready)}
                    math={Boolean(candidate.ai_latex)}
                    disabled={!candidate.ai_latex}
                    onClick={() => chooseCandidate(candidate, "ai")}
                  />
                </article>
              );
            })}
          </div>
        </section>
      </main>

      {aiConfigOpen && (
        <div className="modal-backdrop">
          <section className="ai-modal">
            <div className="modal-header">
              <div>
                <h2>AI模型配置</h2>
                <p>配置会保存到项目根目录 `.env`，之后无需重复填写。</p>
              </div>
              <button className="icon-only secondary" onClick={() => setAiConfigOpen(false)}>
                <X size={17} />
              </button>
            </div>
            <div className="modal-body">
              <label>
                API Key
                <input
                  value={draftAiConfig.api_key}
                  onChange={(event) => {
                    setDraftAiConfig((prev) => ({ ...prev, api_key: event.target.value }));
                    setAiTestState("idle");
                  }}
                  placeholder="sk-..."
                />
              </label>
              <label>
                Base URL
                <input
                  value={draftAiConfig.base_url}
                  onChange={(event) => {
                    setDraftAiConfig((prev) => ({ ...prev, base_url: event.target.value }));
                    setAiTestState("idle");
                  }}
                  placeholder="https://api.openai.com/v1"
                />
              </label>
              <label>
                Model
                <input
                  value={draftAiConfig.model}
                  onChange={(event) => {
                    setDraftAiConfig((prev) => ({ ...prev, model: event.target.value }));
                    setAiTestState("idle");
                  }}
                  placeholder="gpt-4.1-mini"
                />
              </label>
              <div className="modal-grid">
                <label>
                  AI batch
                  <input
                    type="number"
                    min={1}
                    max={50}
                    value={draftAiBatchSize}
                    onChange={(event) => setDraftAiBatchSize(Number(event.target.value))}
                  />
                </label>
                <label>
                  AI Workers
                  <input
                    type="number"
                    min={1}
                    max={10}
                    value={draftAiWorkers}
                    onChange={(event) => setDraftAiWorkers(Number(event.target.value))}
                  />
                </label>
              </div>
              <label>
                失败策略
                <select value={draftAiFallback} onChange={(event) => setDraftAiFallback(event.target.value)}>
                  <option value="rule">本地规则接管</option>
                  <option value="keep">失败保留原文</option>
                  <option value="review">失败进入复核</option>
                </select>
              </label>
              {aiTestMessage && <p className={`test-message ${aiTestState}`}>{aiTestMessage}</p>}
            </div>
            <div className="modal-actions">
              <button className="secondary" onClick={() => setAiConfigOpen(false)}>取消</button>
              <button className="secondary" disabled={aiTestState === "testing"} onClick={() => void testAiConfig()}>
                {aiTestState === "testing" && <Loader2 size={14} />}
                测试模型
              </button>
              <button onClick={() => void saveAiConfig()}>保存</button>
            </div>
          </section>
        </div>
      )}
    </div>
  );
}

function CandidateOption(props: {
  active: boolean;
  title: string;
  value: string;
  badge?: string;
  math?: boolean;
  disabled?: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      className={`candidate-option ${props.active ? "selected" : ""} ${props.disabled ? "disabled" : ""}`}
      onClick={(event) => {
        event.stopPropagation();
        if (!props.disabled) props.onClick();
      }}
      disabled={props.disabled}
    >
      <span className="option-title">
        <strong>{props.title}</strong>
        {props.badge && <em>{props.badge}</em>}
      </span>
      <span className="formula-value">{props.math ? <MathText latex={props.value} /> : props.value}</span>
      {props.active && <Check className="checkmark" size={15} />}
    </button>
  );
}

function MathText({ latex }: { latex: string }) {
  const html = useMemo(() => {
    try {
      return katex.renderToString(normalizeLatexForDisplay(latex || ""), { throwOnError: false, displayMode: false });
    } catch {
      return latex;
    }
  }, [latex]);
  return <span className="math-render" dangerouslySetInnerHTML={{ __html: html }} />;
}

function aiResultTitle(candidate: Candidate) {
  if (candidate.ai_status === "待转换" || candidate.ai_status === "转换中") return candidate.ai_status;
  if (candidate.ai_status === "请求失败回退结果") return "请求失败回退结果";
  if (candidate.ai_latex) return "AI转换结果";
  return "待转换";
}

function aiResultValue(candidate: Candidate, aiReady?: boolean) {
  if (candidate.ai_status === "转换中") return "已发送给大模型，等待结果反馈";
  if (candidate.ai_status === "待转换") return "排队中，尚未发送给大模型";
  if (candidate.ai_latex) return candidate.ai_latex;
  return aiReady ? "无 AI 结果" : "点击顶部「AI 转换」后显示";
}

function InfoButton({ text }: { text: string }) {
  return (
    <button
      type="button"
      className="info-button"
      onClick={(event) => {
        event.preventDefault();
        event.stopPropagation();
        window.alert(text);
      }}
      aria-label="参数说明"
    >
      <HelpCircle size={13} />
    </button>
  );
}

function Empty({ text }: { text: string }) {
  return <div className="empty-state">{text}</div>;
}

function normalizeSelections(raw: Record<string, Choice>, candidates: Candidate[]) {
  const out: Record<string, Choice> = {};
  candidates.forEach((candidate) => {
    out[candidate.id] = normalizeChoice(raw[candidate.id], candidate);
  });
  return out;
}

function normalizeChoice(value: Choice | undefined, candidate: Candidate): "source" | "local" | "ai" {
  if (value === "ai") return "ai";
  if (value === "source" || value === "keep" || value === "review") return "source";
  if (value === "local" || value === "convert") return "local";
  return candidate.default_action === "convert" ? "local" : "source";
}

function formatActionCounts(actions: Record<string, number>) {
  return Object.entries(actions)
    .filter(([, count]) => count > 0)
    .map(([key, count]) => `${actionLabel(key)} ${count}`)
    .join("，") || "无变更";
}

function actionLabel(action: string) {
  if (action === "convert") return "转换";
  if (action === "keep") return "保留";
  if (action === "review") return "复核";
  return action || "复核";
}

function normalizeLatexForDisplay(value: string) {
  return value
    .trim()
    .replace(/^\$+|\$+$/g, "")
    .replace(/^\\\(|\\\)$/g, "")
    .replace(/\\\\([a-zA-Z]+)/g, "\\$1")
    .replace(/\\backslash\s*([a-zA-Z]+)/g, "\\$1")
    .replace(GREEK_COMMAND_FOLLOWED_BY_LETTER, "\\$1 ");
}

function isAcceptedFile(file: File) {
  const lower = file.name.toLowerCase();
  return ACCEPTED_EXTENSIONS.some((suffix) => lower.endsWith(suffix));
}

async function api<T>(path: string, options: RequestInit & { json?: boolean } = {}): Promise<T> {
  const headers = new Headers(options.headers);
  const useJson = options.json !== false;
  if (useJson && options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const response = await fetch(`${API}${path}`, { ...options, headers });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }
  return response.json() as Promise<T>;
}

createRoot(document.getElementById("root")!).render(<App />);
