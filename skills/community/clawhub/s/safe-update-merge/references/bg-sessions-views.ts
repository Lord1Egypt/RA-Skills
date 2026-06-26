import { html, css, nothing } from "lit";
import type { AppViewState } from "../app-view-state.ts";
import type { GatewayBrowserClient } from "../gateway";
import {
  closeBgSessionsPanel,
  loadBgSessions,
  selectBgSession,
  sendBgMessage,
  startBgSessionsPolling,
  type BgMessage,
  type BgSession,
} from "../controllers/bg-sessions.ts";

type BgState = AppViewState & { requestUpdate?: () => void };

function roleLabel(role: string): string {
  switch (role) {
    case "user": return "You";
    case "assistant": return "Agent";
    case "tool": return "→ tool";
    case "tool_result": return "← result";
    case "system": return "system";
    default: return role;
  }
}

function roleClass(role: string): string {
  switch (role) {
    case "user": return "msg-user";
    case "assistant": return "msg-assistant";
    case "tool": return "msg-tool";
    case "tool_result": return "msg-tool-result";
    default: return "msg-system";
  }
}

function renderMessage(msg: BgMessage, idx: number) {
  const ts = msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }) : "";
  return html`
    <div class="msg ${roleClass(msg.role)}" data-idx=${idx}>
      <span class="msg-role">${roleLabel(msg.role)}</span>
      ${ts ? html`<span class="msg-ts">${ts}</span>` : nothing}
      <pre class="msg-text">${msg.text}</pre>
    </div>
  `;
}

export function renderBgSessionsPanel(
  state: BgState,
  client: GatewayBrowserClient,
): ReturnType<typeof html> {
  if (!state.bgSessionsPanelOpen) return html`${nothing}`;

  const sessions = state.bgSessionsList ?? [];
  const messages = state.bgSessionsHistory ?? [];
  const selectedKey = state.bgSessionsSelectedKey;

  const onClose = () => closeBgSessionsPanel(state);
  const onRefresh = () => loadBgSessions(client, state);
  const onSelectSession = (e: Event) => {
    const key = (e.target as HTMLSelectElement).value;
    selectBgSession(client, state, key);
  };
  const onInputChange = (e: Event) => {
    state.bgSessionsInput = (e.target as HTMLTextAreaElement).value;
  };
  const onKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendBgMessage(client, state);
    }
  };
  const onSend = () => sendBgMessage(client, state);

  return html`
    <div class="bg-sessions-overlay" @click=${(e: Event) => { if ((e.target as HTMLElement).classList.contains("bg-sessions-overlay")) onClose(); }}>
      <div class="bg-sessions-panel">

        <!-- Header -->
        <div class="panel-header">
          <span class="panel-title">🔄 Background Sessions</span>
          <div class="panel-actions">
            <button class="icon-btn" title="Refresh" @click=${onRefresh}>
              ${state.bgSessionsLoading ? html`<span class="spinner">⟳</span>` : html`⟳`}
            </button>
            <button class="icon-btn" title="Close" @click=${onClose}>✕</button>
          </div>
        </div>

        <!-- Session selector -->
        <div class="session-selector">
          ${sessions.length === 0 ? html`
            <div class="no-sessions">
              ${state.bgSessionsLoading ? "Loading sessions…" : "No background sessions found."}
            </div>
          ` : html`
            <select class="session-select" @change=${onSelectSession} .value=${selectedKey ?? ""}>
              ${sessions.map(
                (s: BgSession) => html`
                  <option value=${s.key}>
                    ${s.running ? "🟢" : "⚪"} ${s.label}
                  </option>
                `,
              )}
            </select>
          `}
        </div>

        <!-- Transcript -->
        <div class="transcript" id="bg-transcript">
          ${state.bgSessionsHistoryLoading && messages.length === 0
            ? html`<div class="loading-msg">Loading transcript…</div>`
            : messages.length === 0
              ? html`<div class="loading-msg">No messages yet.</div>`
              : messages.map((m, i) => renderMessage(m, i))}
        </div>

        <!-- Input -->
        <div class="input-row">
          <textarea
            class="msg-input"
            placeholder="Send a message to this session… (Enter to send, Shift+Enter for newline)"
            .value=${state.bgSessionsInput}
            @input=${onInputChange}
            @keydown=${onKeyDown}
            rows="2"
            ?disabled=${state.bgSessionsSending || !selectedKey}
          ></textarea>
          <button
            class="send-btn"
            @click=${onSend}
            ?disabled=${state.bgSessionsSending || !state.bgSessionsInput.trim() || !selectedKey}
          >
            ${state.bgSessionsSending ? "…" : "Send"}
          </button>
        </div>

      </div>
    </div>
  `;
}

export const bgSessionsPanelStyles = css`
  .bg-sessions-overlay {
    position: fixed;
    inset: 0;
    z-index: 9000;
    background: rgba(0, 0, 0, 0.45);
    display: flex;
    justify-content: flex-end;
  }

  .bg-sessions-panel {
    width: min(520px, 100vw);
    height: 100vh;
    background: var(--bg-panel, #1a1a2e);
    border-left: 1px solid var(--border-color, #2e2e4a);
    display: flex;
    flex-direction: column;
    box-shadow: -4px 0 24px rgba(0, 0, 0, 0.5);
    font-family: var(--font-sans, system-ui, sans-serif);
    font-size: 13px;
    color: var(--text-primary, #e0e0f0);
  }

  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-color, #2e2e4a);
    background: var(--bg-header, #16162a);
    flex-shrink: 0;
  }

  .panel-title {
    font-weight: 600;
    font-size: 14px;
  }

  .panel-actions {
    display: flex;
    gap: 6px;
  }

  .icon-btn {
    background: none;
    border: none;
    color: var(--text-secondary, #888);
    cursor: pointer;
    font-size: 16px;
    padding: 4px 8px;
    border-radius: 4px;
    transition: background 0.15s;
  }

  .icon-btn:hover {
    background: var(--bg-hover, rgba(255,255,255,0.07));
    color: var(--text-primary, #e0e0f0);
  }

  .spinner {
    display: inline-block;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  .session-selector {
    padding: 8px 12px;
    border-bottom: 1px solid var(--border-color, #2e2e4a);
    flex-shrink: 0;
  }

  .session-select {
    width: 100%;
    background: var(--bg-input, #0f0f1e);
    border: 1px solid var(--border-color, #2e2e4a);
    color: var(--text-primary, #e0e0f0);
    padding: 6px 8px;
    border-radius: 6px;
    font-size: 13px;
    cursor: pointer;
  }

  .no-sessions {
    color: var(--text-secondary, #888);
    font-size: 12px;
    padding: 4px 0;
  }

  .transcript {
    flex: 1;
    overflow-y: auto;
    padding: 8px 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .loading-msg {
    color: var(--text-secondary, #888);
    font-size: 12px;
    padding: 12px 0;
    text-align: center;
  }

  .msg {
    border-radius: 6px;
    padding: 6px 10px;
    max-width: 100%;
    word-break: break-word;
  }

  .msg-role {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-right: 6px;
    opacity: 0.6;
  }

  .msg-ts {
    font-size: 10px;
    opacity: 0.4;
  }

  .msg-text {
    margin: 4px 0 0;
    font-size: 12px;
    line-height: 1.5;
    white-space: pre-wrap;
    font-family: var(--font-mono, monospace);
    overflow: hidden;
    max-height: 200px;
    overflow-y: auto;
  }

  .msg-user {
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.2);
  }

  .msg-assistant {
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.15);
  }

  .msg-tool {
    background: rgba(234, 179, 8, 0.08);
    border: 1px solid rgba(234, 179, 8, 0.15);
  }

  .msg-tool-result {
    background: rgba(148, 163, 184, 0.06);
    border: 1px solid rgba(148, 163, 184, 0.12);
  }

  .msg-system {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.15);
    opacity: 0.7;
  }

  .input-row {
    display: flex;
    gap: 8px;
    padding: 10px 12px;
    border-top: 1px solid var(--border-color, #2e2e4a);
    background: var(--bg-header, #16162a);
    flex-shrink: 0;
  }

  .msg-input {
    flex: 1;
    background: var(--bg-input, #0f0f1e);
    border: 1px solid var(--border-color, #2e2e4a);
    color: var(--text-primary, #e0e0f0);
    padding: 8px 10px;
    border-radius: 6px;
    font-size: 13px;
    resize: none;
    font-family: inherit;
    transition: border-color 0.15s;
  }

  .msg-input:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.5);
  }

  .send-btn {
    background: rgba(99, 102, 241, 0.8);
    border: none;
    color: white;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    transition: background 0.15s;
    align-self: flex-end;
  }

  .send-btn:hover:not(:disabled) {
    background: rgba(99, 102, 241, 1);
  }

  .send-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
`;
