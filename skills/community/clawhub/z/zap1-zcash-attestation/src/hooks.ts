import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-runtime";

interface Zap1HookConfig {
  apiUrl: string;
  apiKey: string;
  agentId: string;
  proofInterval: number;
}

function getHookConfig(api: OpenClawPluginApi): Zap1HookConfig | null {
  const cfg = api.config as any;
  if (!cfg?.apiKey || !cfg?.agentId) return null;
  return {
    apiUrl: cfg.apiUrl || "https://pay.frontiercompute.io",
    apiKey: cfg.apiKey,
    agentId: cfg.agentId,
    proofInterval: cfg.proofInterval || 10,
  };
}

async function attestEvent(
  cfg: Zap1HookConfig,
  eventType: string,
  fields: Record<string, unknown>,
): Promise<string | null> {
  try {
    const resp = await fetch(`${cfg.apiUrl}/event`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${cfg.apiKey}`,
      },
      body: JSON.stringify({
        event_type: eventType,
        wallet_hash: cfg.agentId,
        ...fields,
      }),
    });
    if (!resp.ok) return null;
    const data = (await resp.json()) as { leaf_hash?: string };
    return data.leaf_hash ?? null;
  } catch {
    return null;
  }
}

async function sha256Hex(input: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(input);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
}

export function registerZap1Hooks(api: OpenClawPluginApi) {
  const cfg = getHookConfig(api);
  if (!cfg) return;

  let actionCounter = 0;

  // Hook: attest outbound messages and check policy on tool references
  api.registerHook("message:sent", async (event) => {
    const ctx = event.context as Record<string, unknown>;
    const content = (ctx.content as string) || "";

    if (content.length > 0) {
      const outputHash = await sha256Hex(content.slice(0, 4096));
      const channelId = (ctx.channelId as string) || "unknown";
      await attestEvent(cfg, "AGENT_ACTION", {
        agent_id: cfg.agentId,
        action_type: "message_send",
        input_hash: await sha256Hex(channelId),
        output_hash: outputHash,
      });
      actionCounter++;
    }
  });

  // Hook: attest inbound messages with sender identity
  api.registerHook("message:received", async (event) => {
    const ctx = event.context as Record<string, unknown>;
    const content = (ctx.content as string) || "";

    if (content.length > 0) {
      const senderId = (ctx.from as string) || "unknown";
      const channel = (ctx.channelId as string) || "unknown";
      const messageId = (ctx.messageId as string) || "";

      await attestEvent(cfg, "AGENT_ACTION", {
        agent_id: cfg.agentId,
        action_type: "message_received",
        input_hash: await sha256Hex(`${channel}:${senderId}:${messageId}`),
        output_hash: await sha256Hex(content.slice(0, 4096)),
      });
      actionCounter++;
    }
  });

  // Hook: attest preprocessed messages (LLM input pipeline)
  api.registerHook("message:preprocessed", async (event) => {
    const ctx = event.context as Record<string, unknown>;
    const body = (ctx.bodyForAgent as string) || (ctx.body as string) || "";

    if (body.length > 0) {
      const outputHash = await sha256Hex(body.slice(0, 8192));
      await attestEvent(cfg, "AGENT_ACTION", {
        agent_id: cfg.agentId,
        action_type: "message_preprocessed",
        input_hash: await sha256Hex((ctx.channelId as string) || "unknown"),
        output_hash: outputHash,
      });
      actionCounter++;
    }
  });

  // Hook: attest transcribed audio
  api.registerHook("message:transcribed", async (event) => {
    const ctx = event.context as Record<string, unknown>;
    const transcript = (ctx.transcript as string) || "";

    if (transcript.length > 0) {
      await attestEvent(cfg, "AGENT_ACTION", {
        agent_id: cfg.agentId,
        action_type: "audio_transcription",
        input_hash: await sha256Hex((ctx.messageId as string) || "unknown"),
        output_hash: await sha256Hex(transcript.slice(0, 4096)),
      });
      actionCounter++;
    }
  });

  // Hook: attest agent bootstrap
  api.registerHook("agent:bootstrap", async (event) => {
    await attestEvent(cfg, "AGENT_ACTION", {
      agent_id: cfg.agentId,
      action_type: "session_start",
      input_hash: await sha256Hex(event.timestamp.toISOString()),
      output_hash: await sha256Hex("active"),
    });
  });

  // Hook: attest session patches (config changes, state transitions)
  api.registerHook("session:patch", async (event) => {
    const ctx = event.context as Record<string, unknown>;
    await attestEvent(cfg, "AGENT_ACTION", {
      agent_id: cfg.agentId,
      action_type: "session_patch",
      input_hash: await sha256Hex(event.sessionKey),
      output_hash: await sha256Hex(JSON.stringify(ctx).slice(0, 4096)),
    });
    actionCounter++;
  });

  // Hook: attest gateway startup
  api.registerHook("gateway:startup", async (event) => {
    await attestEvent(cfg, "AGENT_ACTION", {
      agent_id: cfg.agentId,
      action_type: "gateway_start",
      input_hash: await sha256Hex(event.timestamp.toISOString()),
      output_hash: await sha256Hex("startup"),
    });
  });

  // Hook: attest command events and inject proof checkpoints
  api.registerHook("command", async (event) => {
    await attestEvent(cfg, "AGENT_ACTION", {
      agent_id: cfg.agentId,
      action_type: `command:${event.action}`,
      input_hash: await sha256Hex(event.sessionKey),
      output_hash: await sha256Hex(event.action),
    });
    actionCounter++;

    // Proof checkpoint injection
    if (cfg.proofInterval > 0 && actionCounter > 0 && actionCounter % cfg.proofInterval === 0) {
      try {
        const resp = await fetch(`${cfg.apiUrl}/agent/${cfg.agentId}`);
        if (!resp.ok) return;
        const status = (await resp.json()) as any;

        const statsResp = await fetch(`${cfg.apiUrl}/stats`);
        if (!statsResp.ok) return;
        const stats = (await statsResp.json()) as any;

        event.messages.push(
          [
            `Attestation checkpoint (${actionCounter} actions this session):`,
            `  Events: ${status.total_events || 0}`,
            `  Actions: ${status.actions || 0}`,
            `  Anchors: ${stats.total_anchors || 0}`,
            `  Verify: ${cfg.apiUrl}/agent/${cfg.agentId}`,
          ].join("\n"),
        );
      } catch {
        // Checkpoint fetch failed, skip silently
      }
    }
  });
}
