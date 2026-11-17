#!/usr/bin/env node

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { handleRequest } from "./lib/runtime.mjs";
import { publicDevice } from "./lib/response.mjs";

const METHODS = [
  "get_prop", "set_ct_abx", "set_rgb", "set_hsv", "set_bright", "set_power", "toggle", "set_default", "start_cf", "stop_cf", "set_scene", "cron_add", "cron_get", "cron_del", "set_adjust", "set_music", "set_name", "bg_set_rgb", "bg_set_hsv", "bg_set_ct_abx", "bg_start_cf", "bg_stop_cf", "bg_set_scene", "bg_set_default", "bg_set_power", "bg_set_bright", "bg_set_adjust", "bg_toggle", "dev_toggle", "adjust_bright", "adjust_ct", "adjust_color", "bg_adjust_bright", "bg_adjust_ct", "bg_adjust_color",
];

const devices = [
  { id: "0x0123456789abcdef", endpoint: { host: "192.168.50.21", port: 55443 }, model: "mock-color-a", name: "客厅灯 A", support: METHODS, state: { power: "off", bright: 40, ct: 3500, rgb: 16711680, hue: 0, sat: 100, color_mode: 2, name: "客厅灯 A" } },
  { id: "0x0123456789abcdee", endpoint: { host: "192.168.50.22", port: 55443 }, model: "mock-color-b", name: "客厅灯 B", support: METHODS, state: { power: "off", bright: 40, ct: 3500, rgb: 16711680, hue: 0, sat: 100, color_mode: 2, name: "客厅灯 B" } },
  { id: "0x0123456789abcded", endpoint: { host: "192.168.50.23", port: 55443 }, model: "mock-color-c", name: "卧室灯", support: METHODS, state: { power: "off", bright: 25, ct: 3000, rgb: 255, hue: 220, sat: 80, color_mode: 2, name: "卧室灯" } },
];

const stateById = new Map(devices.map((device) => [device.id, structuredClone(device.state)]));

class MockTransport {
  constructor(device) { this.device = device; this.warnings = []; }
  async request(method, params) {
    const state = stateById.get(this.device.id);
    if (method === "get_prop") return params.map((property) => state[property]);
    if (method === "set_power" || method === "bg_set_power") state[method.startsWith("bg_") ? "bg_power" : "power"] = params[0];
    else if (method === "set_bright" || method === "bg_set_bright") state[method.startsWith("bg_") ? "bg_bright" : "bright"] = params[0];
    else if (method === "set_ct_abx" || method === "bg_set_ct_abx") state[method.startsWith("bg_") ? "bg_ct" : "ct"] = params[0];
    else if (method === "set_rgb" || method === "bg_set_rgb") state[method.startsWith("bg_") ? "bg_rgb" : "rgb"] = params[0];
    else if (method === "set_hsv" || method === "bg_set_hsv") { const prefix = method.startsWith("bg_") ? "bg_" : ""; state[`${prefix}hue`] = params[0]; state[`${prefix}sat`] = params[1]; }
    else if (method === "set_name") state.name = params[0];
    else if (method === "set_music") state.music_on = params[0];
    else if (method === "toggle") state.power = state.power === "on" ? "off" : "on";
    else if (method === "bg_toggle") state.bg_power = state.bg_power === "on" ? "off" : "on";
    else if (method === "dev_toggle") { state.power = state.power === "on" ? "off" : "on"; state.bg_power = state.bg_power === "on" ? "off" : "on"; }
    return ["ok"];
  }
  async collectNotifications() { return []; }
  close() {}
}

async function main() {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), "yeelight-wifi-demo-"));
  const runtime = {
    storeOptions: { directory },
    discover: async () => ({ devices }),
    transportFactory: (device) => new MockTransport(device),
  };
  const calls = [
    ["discover", {}],
    ["device.alias.batch_set", { deviceIds: [devices[0].id], alias: "客厅主灯", confirm: true }],
    ["room.create", { name: "客厅", confirm: true }],
    ["room.device.batch_move", { deviceIds: [devices[0].id, devices[1].id], roomId: "room-missing", confirm: true }],
  ];
  const outputs = [];
  for (const [operation, input] of calls.slice(0, 3)) outputs.push(await handleRequest({ operation, ...input }, runtime));
  const roomRef = (await handleRequest({ operation: "room.list" }, runtime)).result.rooms[0];
  const storeStatus = await handleRequest({ operation: "store.export" }, runtime);
  const roomName = roomRef.name;
  outputs.push(await handleRequest({ operation: "room.device.batch_move", target: [devices[0].id, devices[1].id], roomId: roomName, confirm: true }, runtime));
  outputs.push(await handleRequest({ operation: "group.create", name: "客厅组", members: [devices[0].id, devices[1].id], confirm: true }, runtime));
  outputs.push(await handleRequest({ operation: "group.create", name: "交叠组", members: [devices[1].id, devices[2].id], confirm: true }, runtime));
  outputs.push(await handleRequest({ operation: "power.set", target: { type: "group", name: "客厅组" }, power: "on", executionRequested: true, preview: false }, runtime));
  outputs.push(await handleRequest({ operation: "scene.create", name: "晚间", scope: { type: "home" }, actions: [{ set: { power: true, brightness: 50, colorTemperature: 3000 } }], confirm: true }, runtime));
  outputs.push(await handleRequest({ operation: "scene.list" }, runtime));
  outputs.push(await handleRequest({ operation: "schedule.create_draft", name: "晚间计划", timezone: "Asia/Shanghai", cadence: { type: "daily", time: "21:30" }, sceneName: "晚间", confirm: true }, runtime));
  const failed = outputs.find((item) => item.status === "error");
  if (failed) throw new Error(`mock demo failed: ${JSON.stringify(failed)}`);
  console.log(JSON.stringify({ ok: true, steps: outputs.length, home: roomName, exported: storeStatus.status }));
  await fs.rm(directory, { recursive: true, force: true });
}

await main();
