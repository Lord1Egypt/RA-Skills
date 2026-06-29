// /home/openpi/.openclaw/extensions/openclaw-voice-bridge/index.ts
// Voice Bridge Plugin v3 — Snarling owns recording, plugin owns transcription + subagent injection
//
// Flow: snarling X press → arecord (in snarling thread) → POST wav_path to /transcribe-and-reply
// Plugin: receives wav_path → transcribes via OpenAI → subagent.run() → send_notification to display

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { readFile } from "fs/promises";
import { appendFileSync } from "fs";
import { randomUUID } from "crypto";

// Debug logging — opt-in via VOICE_BRIDGE_DEBUG env var
const DEBUG = process.env.VOICE_BRIDGE_DEBUG === "1" || process.env.VOICE_BRIDGE_DEBUG === "true";
const DEBUG_LOG = process.env.VOICE_BRIDGE_DEBUG_LOG || "/tmp/voice-bridge-debug.log";
function debugLog(msg: string): void {
  if (!DEBUG) return;
  const redacted = msg
    .replace(/sk-[a-zA-Z0-9]{10,}/g, "sk-***REDACTED***")
    .replace(/ghp_[a-zA-Z0-9]{10,}/g, "ghp_***REDACTED***")
    .replace(/Bearer\s+[a-zA-Z0-9._-]{10,}/gi, "Bearer ***REDACTED***")
    .replace(/[a-f0-9]{32,}/gi, "***REDACTED***");
  try { appendFileSync(DEBUG_LOG, `${new Date().toISOString()} ${redacted}\n`); } catch {}
}

const SNARLING_URL = "http://localhost:5000/state";
const DEFAULT_TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe";

// Cached API key to avoid re-resolving on every call
let cachedApiKey: string | null = null;

// Helper: set snarling state via /state API
async function setSnarlingState(state: string): Promise<void> {
  try {
    const http = await import('http');
    await new Promise<void>((resolve, reject) => {
      const payload = JSON.stringify({ state });
      const req = http.request({
        hostname: 'localhost',
        port: 5000,
        path: '/state',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload),
        },
      }, (res: any) => {
        res.on('data', () => {});
        res.on('end', resolve);
      });
      req.on('error', reject);
      req.write(payload);
      req.end();
    });
  } catch (_e) {
    // Snarling may be unreachable, that's ok
  }
}

// Helper: resolve OpenAI API key through OpenClaw auth runtime
async function resolveOpenAIKey(runtime: any): Promise<string | null> {
  // Try cached key first
  if (cachedApiKey) return cachedApiKey;

  // Try OpenClaw's auth runtime (modelAuth.resolveApiKeyForProvider)
  if (runtime?.modelAuth?.resolveApiKeyForProvider) {
    try {
      const auth = await runtime.modelAuth.resolveApiKeyForProvider({ provider: "openai" });
      if (auth?.apiKey) {
        cachedApiKey = auth.apiKey;
        console.info(`[openclaw-voice-bridge] Resolved OpenAI key via modelAuth (source: ${auth.source || "unknown"})`);
        debugLog(`Resolved key via modelAuth (source: ${auth.source || "unknown"})`);
        return auth.apiKey;
      }
    } catch (e: any) {
      console.error(`[openclaw-voice-bridge] modelAuth resolution failed: ${e?.message || String(e)}`);
      debugLog(`modelAuth failed: ${e?.message || String(e)}`);
    }
  }

  // Fallback: try runtime.auth.resolveKey (older API)
  try {
    const key = await runtime?.auth?.resolveKey?.("openai:default");
    if (key) {
      cachedApiKey = key;
      console.info(`[openclaw-voice-bridge] Resolved OpenAI key via auth.resolveKey`);
      debugLog("Resolved key via auth.resolveKey");
      return key;
    }
  } catch (_e) {}

  // Fallback: process.env
  const envKey = process.env.OPENAI_API_KEY;
  if (envKey) {
    cachedApiKey = envKey;
    console.info("[openclaw-voice-bridge] Resolved OpenAI key from process.env");
    debugLog("Resolved key from process.env");
    return envKey;
  }

  console.warn("[openclaw-voice-bridge] No OpenAI API key available");
  debugLog("No OpenAI key available");
  return null;
}

// Helper: transcribe audio via OpenAI API
async function transcribeAudio(audioPath: string, apiKey: string, model: string): Promise<string> {
  const audioBuffer = await readFile(audioPath);

  const boundary = `----FormBoundary${randomUUID().replace(/-/g, "")}`;
  const filename = "recording.wav";

  const parts: Buffer[] = [];

  // File part
  parts.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${filename}"\r\nContent-Type: audio/wav\r\n\r\n`));
  parts.push(audioBuffer);
  parts.push(Buffer.from(`\r\n--${boundary}\r\nContent-Disposition: form-data; name="model"\r\n\r\n${model}\r\n`));

  // Response format
  parts.push(Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="response_format"\r\n\r\ntext\r\n`));

  parts.push(Buffer.from(`--${boundary}--\r\n`));

  const body = Buffer.concat(parts);

  return new Promise((resolve, reject) => {
    import('https').then((https) => {
      const req = https.request({
        hostname: 'api.openai.com',
        port: 443,
        path: '/v1/audio/transcriptions',
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': `multipart/form-data; boundary=${boundary}`,
          'Content-Length': body.length,
        },
      }, (res: any) => {
        let data = '';
        res.on('data', (chunk: any) => data += chunk);
        res.on('end', () => {
          try {
            const json = JSON.parse(data);
            resolve(json.text || json.error?.message || '');
          } catch {
            resolve(data.trim());
          }
        });
      });
      req.on('error', (e: any) => reject(new Error(`Transcription request failed: ${e.message}`)));
      req.write(body);
      req.end();
    }).catch((e: any) => reject(new Error(`Failed to import https: ${e.message}`)));
  });
}

// Plugin entry
export default definePluginEntry({
  id: "openclaw-voice-bridge",
  name: "OpenClaw Voice Bridge",
  description: "Receives WAV audio paths from snarling, transcribes via OpenAI, and injects transcript into agent session",
  register(api: any) {
    console.info("[openclaw-voice-bridge] v3 registering, api keys:", Object.keys(api || {}));
    console.info("[openclaw-voice-bridge] api.runtime:", typeof api?.runtime, api?.runtime ? Object.keys(api.runtime) : 'null');

  // Transcribe-and-reply endpoint — receives wav_path from snarling
  api.registerHttpRoute({
    method: "POST",
    path: "/transcribe-and-reply",
    auth: "gateway",
    match: "exact",
    replaceExisting: true,
    handler: async (req: any, res: any) => {
      let body: any = null;
      try {
        const chunks: Buffer[] = [];
        for await (const chunk of req) {
          chunks.push(typeof chunk === 'string' ? Buffer.from(chunk) : chunk);
        }
        const raw = Buffer.concat(chunks).toString();
        if (raw) body = JSON.parse(raw);
      } catch (_e) {}

      const wavPath = body?.wav_path;
      if (!wavPath) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: "wav_path required" }));
        return true;
      }

      debugLog(`/transcribe-and-reply wav_path=${wavPath}`);

      // Respond immediately
      res.statusCode = 200;
      res.end(JSON.stringify({ status: "transcribing" }));

      // Transcribe and inject — async
      (async () => {
        try {
          const apiKey = await resolveOpenAIKey(api.runtime);
          debugLog("API key resolved (redacted)");

          if (!apiKey) {
            console.warn("[openclaw-voice-bridge] No OpenAI API key available");
            debugLog("No OpenAI key");
            await setSnarlingState("sleeping");
            return;
          }

          // Show thinking state
          await setSnarlingState("processing");

          debugLog(`Starting transcription of ${wavPath}`);
          const transcript = await transcribeAudio(wavPath, apiKey, DEFAULT_TRANSCRIPTION_MODEL);
          console.info(`[openclaw-voice-bridge] Transcript: "${transcript}"`);
          debugLog(`Transcript: "${transcript}"`);

          if (!transcript) {
            console.info("[openclaw-voice-bridge] Empty transcript, nothing to send");
            await setSnarlingState("sleeping");
            return;
          }

          // Strategy: Use subagent.run to spawn an isolated agent turn.
          // The subagent answers the question and uses send_notification to push
          // the result to the Snarling display. This bypasses the broken heartbeat
          // wake path (phantom heartbeat bug #86090).
          const voiceText = `🎤 Voice input: ${transcript}`;
          const sessionKey = "agent:main:main";

          try {
            const subagent = (api.runtime as any)?.subagent;
            if (subagent?.run) {
              const subagentPrompt = [
                `You are a voice assistant. Snar just spoke into a device and said:`,
                `"${transcript}"`,
                ``,
                `Answer briefly and naturally (under 80 chars if possible).`,
                `Then send the answer to the Snarling display using the send_notification tool.`,
                `Call send_notification with your answer as the message and priority "normal".`,
              ].join('\n');

              debugLog("Spawning subagent for voice input");

              const result = await subagent.run({
                sessionKey,
                message: subagentPrompt,
                lightContext: true,
              });

              const runId = result?.runId ?? 'unknown';
              console.info(`[openclaw-voice-bridge] Subagent spawned: runId=${runId}`);
              debugLog(`Subagent spawned: runId=${runId}`);

              // Optionally wait for completion (best effort, don't block too long)
              if (subagent.waitForRun) {
                try {
                  const waitResult = await subagent.waitForRun({ runId, timeoutMs: 45000 });
                  const status = waitResult?.status ?? 'unknown';
                  debugLog(`Subagent wait: status=${status} error=${waitResult?.error || 'none'}`);
                  console.info(`[openclaw-voice-bridge] Subagent completed: ${status}`);
                } catch (we: any) {
                  debugLog(`Subagent wait error: ${we?.message}`);
                }
              }
            } else {
              // Fallback: enqueue system event if subagent.run not available
              debugLog("subagent.run not available, falling back to enqueueSystemEvent");
              const systemApi = (api.runtime as any)?.system;
              if (systemApi?.enqueueSystemEvent) {
                systemApi.enqueueSystemEvent(voiceText, { sessionKey });
                debugLog(`Enqueued into ${sessionKey} (fallback)`);
              }
              if (systemApi?.runHeartbeatOnce) {
                const result = await systemApi.runHeartbeatOnce({ heartbeat: { target: "last" } });
                debugLog(`runHeartbeatOnce: status=${result?.status} (fallback)`);
              }
            }

          } catch (err: any) {
            console.error(`[openclaw-voice-bridge] Subagent error: ${err?.message || err}`);
            debugLog(`Subagent error: ${err?.message || err}`);
          }

          // Go back to sleeping
          setSnarlingState("sleeping").catch(() => {});

        } catch (err) {
          console.error(`[openclaw-voice-bridge] Error: ${err instanceof Error ? err.message : String(err)}`);
          debugLog(`ERROR: ${err instanceof Error ? err.message + ' | ' + err.stack : String(err)}`);
          await setSnarlingState("sleeping");
        }
      })();

      return true;
    }
  });

  console.info("[openclaw-voice-bridge] Registered /transcribe-and-reply route");

  // Keep /audio-status and /start-listening as legacy endpoints
  api.registerHttpRoute({
    method: "GET",
    path: "/audio-status",
    auth: "gateway",
    match: "exact",
    replaceExisting: true,
    handler: async (_req: any, res: any) => {
      res.statusCode = 200;
      res.end(JSON.stringify({
        version: 3,
        transcriptionModel: DEFAULT_TRANSCRIPTION_MODEL,
        authAvailable: cachedApiKey ? true : "unknown"
      }));
      return true;
    }
  });

  // Legacy /start-listening — returns error directing to new flow
  api.registerHttpRoute({
    method: "POST",
    path: "/start-listening",
    auth: "gateway",
    match: "exact",
    replaceExisting: true,
    handler: async (_req: any, res: any) => {
      res.statusCode = 410;
      res.end(JSON.stringify({ error: "Deprecated — use /transcribe-and-reply with wav_path", hint: "Snarling should record locally and POST wav_path" }));
      return true;
    }
  });

  console.info("[openclaw-voice-bridge] v3 ready");
  }
});