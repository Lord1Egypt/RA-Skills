const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function createSession(): Promise<string> {
  const res = await fetch(`${API_BASE}/sessions`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to create session");
  const data = await res.json();
  return data.session_id;
}

export interface ChatResult {
  response: string;
  issues_count: number;
  elicitations_count: number;
  gated: boolean;
}

export async function sendMessage(
  sessionId: string,
  message: string
): Promise<ChatResult> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  if (!res.ok) throw new Error("Failed to send message");
  return res.json();
}

export interface SessionInfo {
  session_id: string;
  issues: Array<{ name: string; options: string[] }>;
  learned_weights: Record<string, number>;
  message_count: number;
}

export async function getSession(sessionId: string): Promise<SessionInfo> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`);
  if (!res.ok) throw new Error("Session not found");
  return res.json();
}

export async function unlockSession(sessionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/unlock`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });
  if (!res.ok) throw new Error("Failed to unlock session");
}

export interface SessionHistory {
  messages: Array<{ role: "user" | "coach"; content: string }>;
  unlocked: boolean;
}

export async function getSessionHistory(
  sessionId: string
): Promise<SessionHistory> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}/history`);
  if (!res.ok) throw new Error("Failed to get history");
  return res.json();
}
