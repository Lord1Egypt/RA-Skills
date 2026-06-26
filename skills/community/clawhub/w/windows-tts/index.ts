import pluginManifest from "./openclaw.plugin.json";
import { WindowsTtsClient } from "./client";
import { validateConfig } from "./config";
import { createTools } from "./tools";
import { OpenClawApi } from "./types";

const TOOL_NAMES = [
  "tts_notify",
  "tts_get_status",
  "tts_list_voices",
  "tts_set_volume"
] as const;

export default function init(api: OpenClawApi): void {
  const config = validateConfig(api.config ?? {});
  const client = new WindowsTtsClient(config);
  const tools = createTools({ client, config });

  const register = api.registerTool ?? api.tool;
  if (!register) {
    throw new Error("OpenClaw API does not expose registerTool/tool.");
  }

  TOOL_NAMES.forEach((name) => {
    register(name, async (input) => (tools as Record<string, (arg: unknown) => Promise<unknown>>)[name](input));
  });
}

export const manifest = pluginManifest;
export { createTools } from "./tools";
export { WindowsTtsClient } from "./client";
export { validateConfig } from "./config";
export type { PluginConfig } from "./config";
export type {
  TtsNotifyInput,
  TtsListVoicesInput,
  TtsSetVolumeInput,
  TtsStatusResponse,
  VoiceInfo,
  WindowsTtsClientLike,
  WindowsTtsError
} from "./types";
