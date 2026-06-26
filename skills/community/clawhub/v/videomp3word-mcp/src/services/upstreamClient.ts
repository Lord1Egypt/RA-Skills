import type { ExecutionMode } from "../schemas.js";
import type { ServerConfig } from "../config.js";
import { assertSafeRemoteUrl } from "../utils/network.js";

type JsonLineEvent = {
  type?: string;
  data?: unknown;
  details?: unknown;
  code?: unknown;
};

type ParsedJsonLineResult = {
  stdout: string[];
  stderr: string[];
  result: Record<string, unknown> | null;
  errors: string[];
  exitCode: number | null;
};

const AUDIO_EXTENSIONS = new Set(["aac", "amr", "flac", "m4a", "mp3", "ogg", "opus", "wav", "wma"]);

function buildUpstreamHeaders(config: ServerConfig): HeadersInit {
  const headers: Record<string, string> = {
    accept: "application/json, text/plain;q=0.9, */*;q=0.8",
    cookie: config.sessionCookie,
  };
  if (config.upstreamApiKey) {
    headers.authorization = `Bearer ${config.upstreamApiKey}`;
  }
  return headers;
}

async function parseJsonLineResponse(response: globalThis.Response): Promise<ParsedJsonLineResult> {
  const result: ParsedJsonLineResult = { stdout: [], stderr: [], result: null, errors: [], exitCode: null };
  if (!response.body) return result;

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      let parsed: JsonLineEvent | null = null;
      try {
        parsed = JSON.parse(trimmed) as JsonLineEvent;
      } catch {
        result.stdout.push(line);
        continue;
      }
      if (parsed.type === "stdout" && typeof parsed.data === "string") {
        result.stdout.push(parsed.data);
        continue;
      }
      if (parsed.type === "stderr" && typeof parsed.data === "string") {
        result.stderr.push(parsed.data);
        continue;
      }
      if (parsed.type === "result" && parsed.data && typeof parsed.data === "object") {
        result.result = parsed.data as Record<string, unknown>;
        continue;
      }
      if (parsed.type === "error") {
        const message = typeof parsed.data === "string" ? parsed.data : typeof parsed.details === "string" ? parsed.details : "Upstream transcription failed.";
        result.errors.push(message);
        continue;
      }
      if (parsed.type === "exit" && typeof parsed.code === "number") {
        result.exitCode = parsed.code;
      }
    }
  }

  if (buffer.trim()) result.stdout.push(buffer.trim());
  return result;
}

function detectRoute(sourceUrl: string) {
  const pathname = new URL(sourceUrl).pathname;
  const extension = pathname.includes(".") ? pathname.split(".").pop()?.toLowerCase() || "" : "";
  if (AUDIO_EXTENSIONS.has(extension)) {
    return { route: "/api/mp32word", kind: "audio" as const, modelLabel: "videomp3word-mp32word" };
  }
  return { route: "/api/video2word", kind: "video" as const, modelLabel: "videomp3word-video2word" };
}

async function extractUpstreamError(response: globalThis.Response): Promise<string> {
  const text = await response.text();
  try {
    const parsed = JSON.parse(text) as { error?: string; details?: string };
    return [parsed.error, parsed.details].filter(Boolean).join(": ") || `Upstream request failed with status ${response.status}.`;
  } catch {
    return text || `Upstream request failed with status ${response.status}.`;
  }
}

export class UpstreamTranscriptionClient {
  constructor(private readonly config: ServerConfig) {}

  async transcribe(sourceUrl: string, mode: ExecutionMode) {
    const safeUrl = await assertSafeRemoteUrl(sourceUrl);
    const route = detectRoute(safeUrl.href);
    const payload: Record<string, unknown> = {
      url: safeUrl.href,
      speaker: mode !== "fast",
      restore: mode === "high_accuracy",
    };

    const response = await fetch(new URL(route.route, this.config.baseUrl), {
      method: "POST",
      headers: {
        "content-type": "application/json",
        ...buildUpstreamHeaders(this.config),
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(await extractUpstreamError(response));
    }

    const parsed = await parseJsonLineResponse(response);
    const transcript = parsed.stdout.join("").trim();
    if (!transcript) {
      throw new Error(parsed.errors[0] || "No transcript returned from upstream.");
    }

    return {
      transcript,
      sourceUrl: safeUrl.href,
      kind: route.kind,
      route: route.route,
      modelLabel: `${route.modelLabel}:${mode}`,
    };
  }
}
