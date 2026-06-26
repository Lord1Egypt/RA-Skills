function getHookConfig(api) {
    const cfg = api.config;
    if (!cfg?.apiKey || !cfg?.agentId)
        return null;
    return {
        apiUrl: cfg.apiUrl || "https://pay.frontiercompute.io",
        apiKey: cfg.apiKey,
        agentId: cfg.agentId,
        proofInterval: cfg.proofInterval || 10,
    };
}
async function attestEvent(cfg, eventType, fields) {
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
        if (!resp.ok)
            return null;
        const data = (await resp.json());
        return data.leaf_hash ?? null;
    }
    catch {
        return null;
    }
}
async function sha256Hex(input) {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
}
export function registerZap1Hooks(api) {
    const cfg = getHookConfig(api);
    if (!cfg)
        return;
    let actionCounter = 0;
    // Hook: attest outbound messages and check policy on tool references
    api.registerHook("message:sent", async (event) => {
        const ctx = event.context;
        const content = ctx.content || "";
        if (content.length > 0) {
            const outputHash = await sha256Hex(content.slice(0, 4096));
            const channelId = ctx.channelId || "unknown";
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
        const ctx = event.context;
        const content = ctx.content || "";
        if (content.length > 0) {
            const senderId = ctx.from || "unknown";
            const channel = ctx.channelId || "unknown";
            const messageId = ctx.messageId || "";
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
        const ctx = event.context;
        const body = ctx.bodyForAgent || ctx.body || "";
        if (body.length > 0) {
            const outputHash = await sha256Hex(body.slice(0, 8192));
            await attestEvent(cfg, "AGENT_ACTION", {
                agent_id: cfg.agentId,
                action_type: "message_preprocessed",
                input_hash: await sha256Hex(ctx.channelId || "unknown"),
                output_hash: outputHash,
            });
            actionCounter++;
        }
    });
    // Hook: attest transcribed audio
    api.registerHook("message:transcribed", async (event) => {
        const ctx = event.context;
        const transcript = ctx.transcript || "";
        if (transcript.length > 0) {
            await attestEvent(cfg, "AGENT_ACTION", {
                agent_id: cfg.agentId,
                action_type: "audio_transcription",
                input_hash: await sha256Hex(ctx.messageId || "unknown"),
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
        const ctx = event.context;
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
                if (!resp.ok)
                    return;
                const status = (await resp.json());
                const statsResp = await fetch(`${cfg.apiUrl}/stats`);
                if (!statsResp.ok)
                    return;
                const stats = (await statsResp.json());
                event.messages.push([
                    `Attestation checkpoint (${actionCounter} actions this session):`,
                    `  Events: ${status.total_events || 0}`,
                    `  Actions: ${status.actions || 0}`,
                    `  Anchors: ${stats.total_anchors || 0}`,
                    `  Verify: ${cfg.apiUrl}/agent/${cfg.agentId}`,
                ].join("\n"));
            }
            catch {
                // Checkpoint fetch failed, skip silently
            }
        }
    });
}
