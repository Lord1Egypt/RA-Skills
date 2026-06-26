import {
  getChatChannelMeta,
  type ChannelPlugin,
  type ResolvedAccount,
  type ChannelMessage,
  type OpenClawConfig,
} from "openclaw/plugin-sdk";
import { getXiaozhiRuntime } from "./runtime.js";
import { startXiaozhiWebSocketServer } from "./websocket-server.js";

const meta = getChatChannelMeta("xiaozhi");

interface ResolvedXiaozhiAccount extends ResolvedAccount {
  deviceId: string;
  wsUrl: string;
}

export const xiaozhiPlugin: ChannelPlugin<ResolvedXiaozhiAccount, any> = {
  id: "xiaozhi",
  meta: {
    ...meta,
    quickstartAllowFrom: true,
  },
  onboarding: {
    adapter: {
      type: "manual",
      instructions: "Configure XiaoZhi device to connect to WebSocket server",
    },
  },
  pairing: {
    idLabel: "deviceId",
    normalizeAllowEntry: (entry) => entry.trim(),
    notifyApproval: async ({ cfg, id }) => {
      // Send approval message to XiaoZhi device
      console.log(`XiaoZhi device ${id} pairing approved`);
    },
  },
  capabilities: {
    chatTypes: ["direct"],
    reactions: false,
    threads: false,
    media: true,
    nativeCommands: false,
    blockStreaming: false,
  },
  resolveAccount: async (cfg: OpenClawConfig, accountId?: string) => {
    const defaultId = accountId || "default";
    return {
      id: defaultId,
      name: "XiaoZhi Device",
      enabled: true,
      deviceId: defaultId,
      wsUrl: `ws://localhost:8080`,
    };
  },
  messaging: {
    send: async (ctx) => {
      const { message, account } = ctx;
      // Send text message to XiaoZhi device
      console.log(`Sending to XiaoZhi ${account.deviceId}: ${message}`);
      // TODO: Implement actual WebSocket message sending
      return { success: true };
    },
    receive: async (ctx) => {
      // Receive message from XiaoZhi device
      // This will be called by WebSocket server when audio/text arrives
      return null;
    },
  },
  startup: async (ctx) => {
    // Start WebSocket server when plugin loads
    const port = ctx.cfg.extensions?.xiaozhiclaw?.port || 8080;
    console.log(`Starting XiaoZhi WebSocket server on port ${port}`);
    startXiaozhiWebSocketServer(port, ctx);
  },
};
