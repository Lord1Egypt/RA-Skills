// Load environment variables from .env file
import 'dotenv/config';

import type { ChannelPlugin, OpenClawPluginApi } from "openclaw/plugin-sdk";
import { buildChannelConfigSchema, emptyPluginConfigSchema } from "openclaw/plugin-sdk";
import { xiaozhiPlugin } from "./src/channel.js";
import { setXiaozhiRuntime } from "./src/runtime.js";

const plugin = {
  id: "xiaozhi-channel",
  name: "XiaoZhi Channel",
  description: "XiaoZhi AI ESP32 hardware voice channel",
  configSchema: emptyPluginConfigSchema(),
  register(api: OpenClawPluginApi) {
    setXiaozhiRuntime(api.runtime);
    api.registerChannel({ plugin: xiaozhiPlugin as ChannelPlugin });
  },
};

export default plugin;
