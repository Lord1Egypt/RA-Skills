import type { GatewayBrowserClient } from "../gateway";
import type { AppViewState } from "../app-view-state.ts";

export interface BgSession {
  key: string;
  sessionId: string;
  label: string;
  updatedAt: number;
  running: boolean;
}

export interface BgMessage {
  role: string;
  text: string;
  timestamp?: number;
  toolName?: string;
}

// Type for the subset of app state we need to read/write
type BgState = Pick<
  AppViewState,
  | "bgSessionsPanelOpen"
  | "bgSessionsList"
  | "bgSessionsLoading"
  | "bgSessionsSelectedKey"
  | "bgSessionsHistory"
  | "bgSessionsHistoryLoading"
  | "bgSessionsInput"
  | "bgSessionsSending"
>;

let _historyPollTimer: ReturnType<typeof setInterval> | null = null;

function stopHistoryPoll() {
  if (_historyPollTimer !== null) {
    clearInterval(_historyPollTimer);
    _historyPollTimer = null;
  }
}

export async function loadBgSessions(client: GatewayBrowserClient, state: BgState & { requestUpdate?: () => void }): Promise<void> {
  state.bgSessionsLoading = true;
  state.requestUpdate?.();
  try {
    const res = await client.request<{ ok?: boolean; sessions?: BgSession[] }>("bgSessions.list", {});
    if (res && Array.isArray(res.sessions)) {
      state.bgSessionsList = res.sessions;
      state.requestUpdate?.();
      // Auto-select first if none selected
      if (!state.bgSessionsSelectedKey && res.sessions.length > 0) {
        state.bgSessionsSelectedKey = res.sessions[0].key;
        await loadBgSessionHistory(client, state, state.bgSessionsSelectedKey);
      } else if (state.bgSessionsSelectedKey) {
        await loadBgSessionHistory(client, state, state.bgSessionsSelectedKey);
      }
    }
  } catch {
    // ignore
  } finally {
    state.bgSessionsLoading = false;
    state.requestUpdate?.();
  }
}

export async function loadBgSessionHistory(
  client: GatewayBrowserClient,
  state: BgState & { requestUpdate?: () => void },
  sessionKey: string,
): Promise<void> {
  state.bgSessionsHistoryLoading = true;
  state.requestUpdate?.();
  try {
    const res = await client.request<{ ok?: boolean; messages?: BgMessage[] }>(
      "bgSessions.history",
      { sessionKey, limit: 200 },
    );
    if (res && Array.isArray(res.messages)) {
      state.bgSessionsHistory = res.messages;
      state.requestUpdate?.();
    }
  } catch {
    // ignore
  } finally {
    state.bgSessionsHistoryLoading = false;
    state.requestUpdate?.();
  }
}

export function startBgSessionsPolling(
  client: GatewayBrowserClient,
  state: BgState & { requestUpdate?: () => void },
): void {
  stopHistoryPoll();
  _historyPollTimer = setInterval(async () => {
    if (!state.bgSessionsPanelOpen) {
      stopHistoryPoll();
      return;
    }
    if (state.bgSessionsSelectedKey) {
      await loadBgSessionHistory(client, state, state.bgSessionsSelectedKey);
    }
  }, 3000);
}

export function stopBgSessionsPolling(): void {
  stopHistoryPoll();
}

export async function sendBgMessage(
  client: GatewayBrowserClient,
  state: BgState & { requestUpdate?: () => void },
): Promise<void> {
  const message = state.bgSessionsInput.trim();
  const sessionKey = state.bgSessionsSelectedKey;
  if (!message || !sessionKey) return;

  state.bgSessionsSending = true;
  state.bgSessionsInput = "";
  state.requestUpdate?.();
  try {
    await client.request("chat.send", {
      sessionKey,
      message,
      idempotencyKey: `bg-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    });
    // Refresh history after send
    await loadBgSessionHistory(client, state, sessionKey);
  } catch {
    state.bgSessionsInput = message; // restore on failure
  } finally {
    state.bgSessionsSending = false;
    state.requestUpdate?.();
  }
}

export async function selectBgSession(
  client: GatewayBrowserClient,
  state: BgState & { requestUpdate?: () => void },
  key: string,
): Promise<void> {
  state.bgSessionsSelectedKey = key;
  state.bgSessionsHistory = null;
  state.requestUpdate?.();
  await loadBgSessionHistory(client, state, key);
}

export function openBgSessionsPanel(
  client: GatewayBrowserClient,
  state: BgState & { requestUpdate?: () => void },
): void {
  state.bgSessionsPanelOpen = true;
  state.requestUpdate?.();
  loadBgSessions(client, state);
  startBgSessionsPolling(client, state);
}

export function closeBgSessionsPanel(state: BgState & { requestUpdate?: () => void }): void {
  state.bgSessionsPanelOpen = false;
  state.requestUpdate?.();
  stopBgSessionsPolling();
}
