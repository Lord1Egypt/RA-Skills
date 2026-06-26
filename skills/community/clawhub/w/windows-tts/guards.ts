import { PluginConfig } from "./types";

export function validatePlugin(config: PluginConfig): void {
  // URL validation
  if (!config.url) {
    throw new Error("Windows TTS plugin requires 'url' configuration");
  }

  try {
    new URL(config.url);
  } catch {
    throw new Error(`Invalid URL format: ${config.url}`);
  }

  // Volume validation
  if (config.defaultVolume !== undefined) {
    if (config.defaultVolume < 0 || config.defaultVolume > 1) {
      throw new Error("defaultVolume must be between 0.0 and 1.0");
    }
  }

  // Timeout validation
  if (config.timeout !== undefined) {
    if (config.timeout < 1000 || config.timeout > 60000) {
      throw new Error("timeout must be between 1000 and 60000ms");
    }
  }
}
