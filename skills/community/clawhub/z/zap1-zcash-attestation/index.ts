import { definePluginEntry, type AnyAgentTool } from "openclaw/plugin-sdk/plugin-entry";
import { createZap1Tools } from "./src/tools.js";
import { registerZap1Hooks } from "./src/hooks.js";

export default definePluginEntry({
  id: "zap1",
  name: "openclaw-zap1",
  description:
    "Zcash attestation layer for OpenClaw agents. Policy enforcement, behavioral proof, and session tracking via 7 hooks + 14 protocol tools. Every action anchored to Zcash.",
  register(api) {
    for (const tool of createZap1Tools(api)) {
      api.registerTool(tool as AnyAgentTool);
    }
    registerZap1Hooks(api);
  },
});
