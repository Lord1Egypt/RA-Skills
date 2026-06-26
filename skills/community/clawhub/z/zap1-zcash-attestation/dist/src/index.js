import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { createZap1Tools } from "./tools.js";
export default definePluginEntry({
    id: "zap1",
    name: "ZAP1 Attestation",
    description: "ZAP1 protocol tools for Zcash. Verify proofs, check anchors, decode memos, create lifecycle events.",
    register(api) {
        for (const tool of createZap1Tools(api)) {
            api.registerTool(tool);
        }
    },
});
