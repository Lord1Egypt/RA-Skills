import os from "node:os";
import path from "node:path";

export const DEFAULT_BASE_URL = "https://api.twexapi.io";
export const CONFIG_FILE_NAME = "config.json";
export const DEFAULT_CONFIG_DIR =
  process.env.TWEXAPI_CONFIG_DIR ||
  path.join(os.homedir(), ".twexapi");
export const DEFAULT_CONFIG = {
  version: 1,
  currentApp: "",
  currentProfile: "",
  apps: {},
  profiles: {},
};

export const LEADING_GLOBAL_OPTIONS = {
  "-X": { takesValue: true, key: "method" },
  "--method": { takesValue: true, key: "method" },
  "-d": { takesValue: true, key: "data" },
  "--data": { takesValue: true, key: "data" },
  "-H": { takesValue: true, key: "header" },
  "--header": { takesValue: true, key: "header" },
  "--app": { takesValue: true, key: "appName" },
  "--profile": { takesValue: true, key: "profileName" },
  "--api-key": { takesValue: true, key: "apiKey" },
  "--base-url": { takesValue: true, key: "baseUrl" },
  "--config-dir": { takesValue: true, key: "configDir" },
  "--dry-run": { takesValue: false, key: "dryRun" },
  "--raw": { takesValue: false, key: "raw" },
  "-h": { takesValue: false, key: "help" },
  "--help": { takesValue: false, key: "help" },
};
