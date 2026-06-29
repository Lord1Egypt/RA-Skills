// index.ts
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { readFile } from "fs/promises";
import { appendFileSync } from "fs";
import { randomUUID } from "crypto";
var DEBUG = process.env.VOICE_BRIDGE_DEBUG === "1" || process.env.VOICE_BRIDGE_DEBUG === "true";
var DEBUG_LOG = process.env.VOICE_BRIDGE_DEBUG_LOG || "/tmp/voice-bridge-debug.log";
function debugLog(msg) {
  if (!DEBUG) return;
  var redacted = msg.replace(/sk-[a-zA-Z0-9]{10,}/g, "sk-***REDACTED***").replace(/ghp_[a-zA-Z0-9]{10,}/g, "ghp_***REDACTED***").replace(/Bearer\s+[a-zA-Z0-9._-]{10,}/gi, "Bearer ***REDACTED***").replace(/[a-f0-9]{32,}/gi, "***REDACTED***");
  try { appendFileSync(DEBUG_LOG, `${new Date().toISOString()} ${redacted}\n`); } catch {}
}
var DEFAULT_TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe";
var cachedApiKey = null;
async function setSnarlingState(state) {
  try {
    const http = await import("http");
    await new Promise((resolve, reject) => {
      const payload = JSON.stringify({ state });
      const req = http.request({
        hostname: "localhost",
        port: 5e3,
        path: "/state",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(payload)
        }
      }, (res) => {
        res.on("data", () => {
        });
        res.on("end", resolve);
      });
      req.on("error", reject);
      req.write(payload);
      req.end();
    });
  } catch (_e) {
  }
}
async function resolveOpenAIKey(runtime) {
  if (cachedApiKey) return cachedApiKey;
  if (runtime?.modelAuth?.resolveApiKeyForProvider) {
    try {
      const auth = await runtime.modelAuth.resolveApiKeyForProvider({ provider: "openai" });
      if (auth?.apiKey) {
        cachedApiKey = auth.apiKey;
        console.info(`[openclaw-voice-bridge] Resolved OpenAI key via modelAuth (source: ${auth.source || "unknown"})`);
        debugLog(`Resolved key via modelAuth (source: ${auth.source || "unknown"})`);
        return auth.apiKey;
      }
    } catch (e) {
      console.error(`[openclaw-voice-bridge] modelAuth resolution failed: ${e?.message || String(e)}`);
      debugLog(`modelAuth failed: ${e?.message || String(e)}`);
    }
  }
  try {
    const key = await runtime?.auth?.resolveKey?.("openai:default");
    if (key) {
      cachedApiKey = key;
      console.info(`[openclaw-voice-bridge] Resolved OpenAI key via auth.resolveKey`);
      debugLog("Resolved key via auth.resolveKey");
      return key;
    }
  } catch (_e) {
  }
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
async function transcribeAudio(audioPath, apiKey, model) {
  const audioBuffer = await readFile(audioPath);
  const boundary = `----FormBoundary${randomUUID().replace(/-/g, "")}`;
  const filename = "recording.wav";
  const parts = [];
  parts.push(Buffer.from(`--${boundary}\r
Content-Disposition: form-data; name="file"; filename="${filename}"\r
Content-Type: audio/wav\r
\r
`));
  parts.push(audioBuffer);
  parts.push(Buffer.from(`\r
--${boundary}\r
Content-Disposition: form-data; name="model"\r
\r
${model}\r
`));
  parts.push(Buffer.from(`--${boundary}\r
Content-Disposition: form-data; name="response_format"\r
\r
text\r
`));
  parts.push(Buffer.from(`--${boundary}--\r
`));
  const body = Buffer.concat(parts);
  return new Promise((resolve, reject) => {
    import("https").then((https) => {
      const req = https.request({
        hostname: "api.openai.com",
        port: 443,
        path: "/v1/audio/transcriptions",
        method: "POST",
        headers: {
          "Authorization": `Bearer ${apiKey}`,
          "Content-Type": `multipart/form-data; boundary=${boundary}`,
          "Content-Length": body.length
        }
      }, (res) => {
        let data = "";
        res.on("data", (chunk) => data += chunk);
        res.on("end", () => {
          try {
            const json = JSON.parse(data);
            resolve(json.text || json.error?.message || "");
          } catch {
            resolve(data.trim());
          }
        });
      });
      req.on("error", (e) => reject(new Error(`Transcription request failed: ${e.message}`)));
      req.write(body);
      req.end();
    }).catch((e) => reject(new Error(`Failed to import https: ${e.message}`)));
  });
}
var index_default = definePluginEntry({
  id: "openclaw-voice-bridge",
  name: "OpenClaw Voice Bridge",
  description: "Receives WAV audio paths from snarling, transcribes via OpenAI, and injects transcript into agent session",
  register(api) {
    console.info("[openclaw-voice-bridge] v3 registering, api keys:", Object.keys(api || {}));
    console.info("[openclaw-voice-bridge] api.runtime:", typeof api?.runtime, api?.runtime ? Object.keys(api.runtime) : "null");
    api.registerHttpRoute({
      method: "POST",
      path: "/transcribe-and-reply",
      auth: "gateway",
      match: "exact",
      replaceExisting: true,
      handler: async (req, res) => {
        let body = null;
        try {
          const chunks = [];
          for await (const chunk of req) {
            chunks.push(typeof chunk === "string" ? Buffer.from(chunk) : chunk);
          }
          const raw = Buffer.concat(chunks).toString();
          if (raw) body = JSON.parse(raw);
        } catch (_e) {
        }
        const wavPath = body?.wav_path;
        if (!wavPath) {
          res.statusCode = 400;
          res.end(JSON.stringify({ error: "wav_path required" }));
          return true;
        }
        debugLog(`/transcribe-and-reply wav_path=${wavPath}`);
        res.statusCode = 200;
        res.end(JSON.stringify({ status: "transcribing" }));
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
            const voiceText = `\u{1F3A4} Voice input: ${transcript}`;
            const sessionKey = "agent:main:main";
            try {
              const subagent = api.runtime?.subagent;
              if (subagent?.run) {
                const subagentPrompt = [
                  "You are a voice assistant. Snar just spoke into a device and said:",
                  `"${transcript}"`,
                  "",
                  "Answer briefly and naturally (under 80 chars if possible).",
                  "Then send the answer to the Snarling display using the send_notification tool.",
                  "Call send_notification with your answer as the message and priority \"normal\".",
                ].join("\n");
                debugLog("Spawning subagent for voice input");
                const result = await subagent.run({
                  sessionKey,
                  message: subagentPrompt,
                  lightContext: true
                });
                const runId = result?.runId ?? "unknown";
                console.info(`[openclaw-voice-bridge] Subagent spawned: runId=${runId}`);
                debugLog(`Subagent spawned: runId=${runId}`);
                if (subagent.waitForRun) {
                  try {
                    const waitResult = await subagent.waitForRun({ runId, timeoutMs: 45e3 });
                    const status = waitResult?.status ?? "unknown";
                    debugLog(`Subagent wait: status=${status} error=${waitResult?.error || "none"}`);
                    console.info(`[openclaw-voice-bridge] Subagent completed: ${status}`);
                  } catch (we) {
                    debugLog(`Subagent wait error: ${we?.message}`);
                  }
                }
              } else {
                debugLog("subagent.run not available, falling back to enqueueSystemEvent");
                const systemApi = api.runtime?.system;
                if (systemApi?.enqueueSystemEvent) {
                  systemApi.enqueueSystemEvent(voiceText, { sessionKey });
                  debugLog(`Enqueued into ${sessionKey} (fallback)`);
                }
                if (systemApi?.runHeartbeatOnce) {
                  const result2 = await systemApi.runHeartbeatOnce({ heartbeat: { target: "last" } });
                  debugLog(`runHeartbeatOnce: status=${result2?.status} (fallback)`);
                }
              }
            } catch (err) {
              console.error(`[openclaw-voice-bridge] Subagent error: ${err?.message || err}`);
              debugLog(`Subagent error: ${err?.message || err}`);
            }
            setSnarlingState("sleeping").catch(() => {
            });
          } catch (err) {
            console.error(`[openclaw-voice-bridge] Error: ${err instanceof Error ? err.message : String(err)}`);
            debugLog(`ERROR: ${err instanceof Error ? err.message + " | " + err.stack : String(err)}`);
            const errMsg = err instanceof Error ? err.message : String(err);
            if (errMsg.includes("EAI_AGAIN") || errMsg.includes("ENETUNREACH") || errMsg.includes("fetch failed") || errMsg.includes("Transcription request failed")) {
              await setSnarlingState("error");
            } else {
              await setSnarlingState("sleeping");
            }
          }
        })();
        return true;
      }
    });
    console.info("[openclaw-voice-bridge] Registered /transcribe-and-reply route");
    api.registerHttpRoute({
      method: "GET",
      path: "/audio-status",
      auth: "gateway",
      match: "exact",
      replaceExisting: true,
      handler: async (_req, res) => {
        res.statusCode = 200;
        res.end(JSON.stringify({
          version: 3,
          transcriptionModel: DEFAULT_TRANSCRIPTION_MODEL,
          authAvailable: cachedApiKey ? true : "unknown"
        }));
        return true;
      }
    });
    api.registerHttpRoute({
      method: "POST",
      path: "/start-listening",
      auth: "gateway",
      match: "exact",
      replaceExisting: true,
      handler: async (_req, res) => {
        res.statusCode = 410;
        res.end(JSON.stringify({ error: "Deprecated \u2014 use /transcribe-and-reply with wav_path", hint: "Snarling should record locally and POST wav_path" }));
        return true;
      }
    });
    console.info("[openclaw-voice-bridge] v3 ready");
  }
});
export {
  index_default as default
};