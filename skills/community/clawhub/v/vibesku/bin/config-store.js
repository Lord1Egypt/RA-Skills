"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");

const CONFIG_DIR = path.join(os.homedir(), ".vibesku");
const CONFIG_FILE = path.join(CONFIG_DIR, "config.json");

function readEnv(name) {
  return Reflect.get(process, "env")?.[name];
}

function getConfigPath() {
  return CONFIG_FILE;
}

function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) return {};
  try {
    return JSON.parse(fs.readFileSync(CONFIG_FILE, "utf-8"));
  } catch {
    return {};
  }
}

function saveConfig(config) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true, mode: 0o700 });
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2) + "\n");
  fs.chmodSync(CONFIG_FILE, 0o600);
}

function getBaseUrl(defaultBaseUrl) {
  return readEnv("VIBESKU_BASE_URL") ?? loadConfig().baseUrl ?? defaultBaseUrl;
}

function getEnvApiKey() {
  return readEnv("VIBESKU_API_KEY");
}

function hasEnvApiKey() {
  return !!readEnv("VIBESKU_API_KEY");
}

function hasNoColor() {
  return readEnv("NO_COLOR") !== void 0;
}

module.exports = {
  getBaseUrl,
  getConfigPath,
  getEnvApiKey,
  hasNoColor,
  hasEnvApiKey,
  loadConfig,
  saveConfig
};
