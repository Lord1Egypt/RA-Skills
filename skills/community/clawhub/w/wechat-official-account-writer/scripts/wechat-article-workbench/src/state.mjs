import fs from "node:fs";
import { ensureDirs, statePath } from "./config.mjs";

export function loadState() {
  ensureDirs();
  if (!fs.existsSync(statePath)) {
    return { items: {}, coverMedia: {}, runs: [] };
  }

  const raw = fs.readFileSync(statePath, "utf8");
  if (!raw.trim()) {
    return { items: {}, coverMedia: {}, runs: [] };
  }

  const state = JSON.parse(raw);
  state.items ||= {};
  state.coverMedia ||= {};
  state.runs ||= [];
  return state;
}

export function saveState(state) {
  ensureDirs();
  fs.writeFileSync(statePath, `${JSON.stringify(state, null, 2)}\n`);
}

export function updateItem(state, sourceId, patch) {
  const now = new Date().toISOString();
  state.items[sourceId] = {
    ...(state.items[sourceId] || {}),
    ...patch,
    updatedAt: now
  };
  if (!state.items[sourceId].createdAt) {
    state.items[sourceId].createdAt = now;
  }
}
