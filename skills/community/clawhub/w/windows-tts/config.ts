import { PluginConfig } from "./types";

export { PluginConfig };

export function validateConfig(config: Record<string, unknown>): PluginConfig {
  if (!config.url) {
    throw new Error("Windows TTS plugin requires 'url' configuration. Example: http://192.168.1.60:5000");
  }

  const url = String(config.url).replace(/\/$/, "");
  
  // Validate URL format
  try {
    new URL(url);
  } catch {
    throw new Error(`Invalid URL format: ${config.url}. Must be a valid HTTP/HTTPS URL.`);
  }

  const defaultVoice = config.defaultVoice ? String(config.defaultVoice) : "zh-CN-XiaoxiaoNeural";
  const defaultVolume = config.defaultVolume !== undefined ? Number(config.defaultVolume) : 1.0;
  const timeout = config.timeout !== undefined ? Number(config.timeout) : 10000;

  // Validate volume range
  if (defaultVolume < 0 || defaultVolume > 1) {
    throw new Error("defaultVolume must be between 0.0 and 1.0");
  }

  // Validate timeout
  if (timeout < 1000 || timeout > 60000) {
    throw new Error("timeout must be between 1000 and 60000 milliseconds");
  }

  return {
    url,
    defaultVoice,
    defaultVolume,
    timeout
  };
}
