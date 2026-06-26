import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { dirname, resolve } from "path";
const BASE = process.env.SURGE_DIR ?? resolve(process.env.HOME ?? "~", ".skill-surge-notifier");
const STATE_PATH = process.env.STATE_PATH ?? resolve(BASE, "state.json");
const CONFIG_PATH = process.env.CONFIG_PATH ?? resolve(BASE, "config.json");
export const DEFAULT_CONFIG = {
    intervalHours: 4,
    thresholds: {
        minDownloads: 50000,
        minStars: 200,
        minGrowthPct: 30,
        top10Alert: true,
    },
    topMovers: {
        enabled: true,
        count: 5,
    },
};
export function loadState() {
    if (!existsSync(STATE_PATH)) {
        return { lastChecked: "", skills: {} };
    }
    return JSON.parse(readFileSync(STATE_PATH, "utf8"));
}
export function saveState(state) {
    mkdirSync(dirname(STATE_PATH), { recursive: true });
    writeFileSync(STATE_PATH, JSON.stringify(state, null, 2));
}
export function loadConfig() {
    if (!existsSync(CONFIG_PATH))
        return DEFAULT_CONFIG;
    const saved = JSON.parse(readFileSync(CONFIG_PATH, "utf8"));
    return { ...DEFAULT_CONFIG, ...saved, thresholds: { ...DEFAULT_CONFIG.thresholds, ...saved.thresholds } };
}
export function saveConfig(config) {
    mkdirSync(dirname(CONFIG_PATH), { recursive: true });
    writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
}
