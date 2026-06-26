import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
import type { ChannelPlugin, OpenClawConfig } from "openclaw/plugin-sdk/core";

import { listQuantumImAccountIds, resolveQuantumImAccount, type QuantumImAccount } from "./src/config.js";
import { QuantumImApi } from "./src/api.js";

// Cache for API clients
const apiClients = new Map<string, QuantumImApi>();

function getOrCreateApi(account: QuantumImAccount): QuantumImApi {
  const cacheKey = account.accountId ?? "default";
  if (!apiClients.has(cacheKey)) {
    apiClients.set(cacheKey, new QuantumImApi({
      robotId: account.robotId,
      key: account.key,
      host: account.host,
    }));
  }
  return apiClients.get(cacheKey)!;
}

// Start webhook server for inbound messages
let webhookServer: any = null;

function isGatewayRuntime(): boolean {
  if ((process.env.OPENCLAW_SERVICE_KIND || "").toLowerCase() === "gateway") {
    return true;
  }
  return process.argv.includes("gateway");
}

function startWebhookServer(account: QuantumImAccount, pluginApi: any) {
  if (webhookServer) {
    console.log("[quantum-im] webhook server already running");
    return;
  }

  const { createServer } = require("http");
  
  webhookServer = createServer(async (req: any, res: any) => {
    if (req.method === "OPTIONS") {
      res.setHeader("Access-Control-Allow-Origin", "*");
      res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
      res.setHeader("Access-Control-Allow-Headers", "Content-Type");
      res.statusCode = 200;
      res.end();
      return;
    }

    if (req.url !== account.webhookPath || req.method !== "POST") {
      res.statusCode = 404;
      res.end("Not Found");
      return;
    }

    let body = "";
    req.on("data", (chunk: any) => {
      body += chunk.toString();
    });

    req.on("end", async () => {
      try {
        const payload = JSON.parse(body);
        await handleIncomingMessage(account, payload, pluginApi);
        
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify({ success: true }));
      } catch (error) {
        console.error("[quantum-im] Webhook error:", error);
        res.statusCode = 400;
        res.end(JSON.stringify({ error: "Invalid payload" }));
      }
    });
  });

  webhookServer.on("error", (error: any) => {
    if (error?.code === "EADDRINUSE") {
      console.warn(
        `[quantum-im] Webhook port ${account.webhookPort} already in use, reusing existing listener`,
      );
      webhookServer = null;
      return;
    }
    console.error("[quantum-im] Webhook server error:", error);
  });

  webhookServer.listen(account.webhookPort, () => {
    console.log(`[quantum-im] Webhook server listening on port ${account.webhookPort}`);
    console.log(`[quantum-im] Webhook path: ${account.webhookPath}`);
    console.log(`[quantum-im] Full URL: http://localhost:${account.webhookPort}${account.webhookPath}`);
  });
}

async function handleIncomingMessage(
  account: QuantumImAccount,
  payload: any,
  pluginApi: any,
) {
  const { type, phone, groupId, callBackUrl, textMsg, imageMsg, fileMsg, news } = payload;

  const isGroup = Boolean(groupId);
  const chatType = isGroup ? "group" : "direct";
  const peerId = isGroup ? groupId! : phone;
  let content = "";
  let messageType = "text";

  if (type === "text" && textMsg) {
    content = textMsg.content;
    messageType = "text";
  } else if (type === "image" && imageMsg) {
    content = `[图片 fileId: ${imageMsg.fileId}]`;
    messageType = "image";
  } else if (type === "file" && fileMsg) {
    content = `[文件 fileId: ${fileMsg.fileId}]`;
    messageType = "file";
  } else if (type === "news" && news) {
    content = `[图文] ${news.info.title}\n${news.info.description || ""}\n${news.info.url}`;
    messageType = "news";
  } else {
    content = `[未知消息类型：${type}]`;
  }

  console.log(`[quantum-im] Received ${messageType} from ${phone}${isGroup ? ` in group ${groupId}` : ""}: ${content.substring(0, 100)}`);

  // Get OpenClaw config and runtime
  const cfg: OpenClawConfig | undefined = pluginApi?.config;
  const channelRuntime = pluginApi?.runtime?.channel;
  
  if (!cfg || !channelRuntime) {
    console.error("[quantum-im] runtime or config unavailable");
    return;
  }

  try {
    // Resolve agent route for this message
    const route = channelRuntime.routing.resolveAgentRoute({
      cfg,
      channel: "quantum-im",
      accountId: account.accountId ?? "default",
      peer: { kind: isGroup ? "group" : "direct", id: peerId },
    });

    if (!route?.agentId || !route?.sessionKey) {
      console.warn(`[quantum-im] No agent route for ${chatType}:${peerId}`);
      return;
    }

    // Build message context for reply
    const msgContext = channelRuntime.reply.finalizeInboundContext({
      Body: content,
      CommandBody: content,
      From: phone,
      To: peerId,
      AccountId: account.accountId ?? "default",
      MessageSid: `${Date.now()}-${phone}`,
      Timestamp: Date.now(),
      Provider: "quantum-im",
      Surface: "quantum-im",
      ChatType: chatType,
      SenderId: phone,
      SenderName: phone,
      WasMentioned: textMsg?.isMentioned ?? false,
      OriginatingChannel: "quantum-im",
      OriginatingTo: peerId,
      SessionKey: route.sessionKey,
      UntrustedContext: [
        `callback_url=${String(callBackUrl ?? "")}`,
        `group_id=${String(groupId ?? "")}`,
        `robot_id=${account.robotId}`,
      ],
    });

    // Resolve session store path
    const storePath = channelRuntime.session.resolveStorePath(cfg.session?.store, {
      agentId: route.agentId,
    });

    // Record inbound session
    await channelRuntime.session.recordInboundSession({
      storePath,
      sessionKey: route.sessionKey,
      ctx: msgContext,
      updateLastRoute: {
        sessionKey: route.mainSessionKey ?? route.sessionKey,
        channel: "quantum-im",
        to: peerId,
        accountId: account.accountId ?? "default",
      },
      onRecordError: (err: unknown) => {
        console.error("[quantum-im] recordInboundSession error:", err);
      },
    });

    // Get API client for outbound messages
    const quantumApi = getOrCreateApi(account);

    // Dispatch reply with buffered block dispatcher
    await channelRuntime.reply.dispatchReplyWithBufferedBlockDispatcher({
      ctx: msgContext,
      cfg,
      dispatcherOptions: {
        deliver: async (replyPayload: any) => {
          const text = String(replyPayload?.text ?? "").trim();
          const mediaUrl = replyPayload?.mediaUrl ?? replyPayload?.mediaUrls?.[0];

          if (text) {
            console.log(`[quantum-im] Sending reply to ${phone}: ${text.substring(0, 100)}`);
            await quantumApi.sendText(phone, text, isGroup ? groupId : undefined);
          }

          if (mediaUrl) {
            const mediaPath = String(mediaUrl);
            const isImageMedia = /\.(jpg|jpeg|png|gif|webp)$/i.test(mediaPath);
            console.log(`[quantum-im] Sending media to ${phone}: ${mediaPath}`);
            if (isImageMedia) {
              await quantumApi.sendImage(phone, mediaPath, isGroup ? groupId : undefined);
            } else {
              await quantumApi.sendFile(phone, mediaPath, isGroup ? groupId : undefined);
            }
          }
        },
        onError: (err: unknown) => {
          console.error("[quantum-im] dispatch deliver error:", err);
        },
      },
    });
  } catch (error) {
    console.error("[quantum-im] handleIncomingMessage error:", error);
  }
}

const quantumImPlugin: ChannelPlugin<QuantumImAccount> = {
  id: "quantum-im",
  meta: {
    id: "quantum-im",
    label: "量子密信",
    selectionLabel: "量子密信 (Webhook)",
    docsPath: "/channels/quantum-im",
    docsLabel: "量子密信",
    blurb: "量子密信即时通讯渠道 - 支持文本、图片、文件消息",
    order: 80,
  },
  configSchema: {
    schema: {
      type: "object",
      additionalProperties: false,
      properties: {},
    },
  },
  capabilities: {
    chatTypes: ["direct", "group"],
    media: true,
    blockStreaming: false,
  },
  messaging: {
    targetResolver: {
      looksLikeId: (raw) => /^\d+$/.test(raw) || raw.endsWith("@im.quantum"),
    },
  },
  config: {
    listAccountIds: (cfg) => listQuantumImAccountIds(cfg),
    resolveAccount: (cfg, accountId) => resolveQuantumImAccount(cfg, accountId),
    isConfigured: (account) => account.configured,
    describeAccount: (account) => ({
      accountId: account.accountId,
      name: account.robotId,
      enabled: account.enabled,
      configured: account.configured,
    }),
  },
  outbound: {
    deliveryMode: "direct",
    sendText: async (ctx) => {
      const account = resolveQuantumImAccount(ctx.cfg, ctx.accountId);
      const api = getOrCreateApi(account);
      
      const result = await api.sendText(
        ctx.to,
        ctx.text,
        ctx.metadata?.groupId,
      );
      
      return { channel: "quantum-im", messageId: result.messageId };
    },
    sendMedia: async (ctx) => {
      const account = resolveQuantumImAccount(ctx.cfg, ctx.accountId);
      const api = getOrCreateApi(account);
      
      const filePath = ctx.mediaUrl;
      const isImage = filePath.match(/\.(jpg|jpeg|png|gif|webp)$/i);
      
      let result;
      if (isImage) {
        result = await api.sendImage(ctx.to, filePath, ctx.metadata?.groupId);
      } else {
        result = await api.sendFile(ctx.to, filePath, ctx.metadata?.groupId);
      }
      
      return { channel: "quantum-im", messageId: result.messageId };
    },
  },
  security: {
    dm: {
      channelKey: "quantum-im",
      resolvePolicy: (account) => account.dmSecurity,
      resolveAllowFrom: (account) => account.allowFrom,
      defaultPolicy: "pairing",
    },
  },
};

export default {
  id: "quantum-im",
  name: "量子密信",
  description: "量子密信渠道插件",
  configSchema: {
    type: "object",
    additionalProperties: false,
    properties: {},
  },
  register(api: OpenClawPluginApi) {
    api.registerChannel({ plugin: quantumImPlugin });

    const mode = (api as any).registrationMode;
    if (mode && mode !== "full") return;
    if (!isGatewayRuntime()) return;

    // Start webhook server after channel is registered
    setTimeout(() => {
      try {
        const fs = require("fs");
        const path = require("path");
        const configPath = path.join(process.env.HOME || "", ".openclaw/openclaw.json");
        const configContent = fs.readFileSync(configPath, "utf-8");
        const config = JSON.parse(configContent);
        
        const account = resolveQuantumImAccount(config, "default");
        
        if (account.enabled && account.configured) {
          startWebhookServer(account, api);
        }
      } catch (error) {
        console.error("[quantum-im] Failed to start webhook server:", error);
      }
    }, 2000);

    api.registerCli(({ program }) => {
      program
        .command("quantum-im")
        .description("量子密信渠道管理")
        .action(() => {
          console.log("量子密信渠道插件 v1.0.0");
          console.log("支持消息类型：文本、图片、文件、图文");
          console.log("配置方式：channels.quantum-im");
        });
    }, {
      commands: ["quantum-im"],
    });
  },
};
