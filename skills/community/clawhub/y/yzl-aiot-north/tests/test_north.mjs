// 北向 JS 离线自测：需要先起 tests/mock_north.py（默认 18082 端口）。
// 运行：node tests/test_north.mjs http://127.0.0.1:18082

import { NorthClient, NorthError } from "../lib/north_client.mjs";

const base = process.argv[2] || "http://127.0.0.1:18082";
let pass = 0;
let fail = 0;
const check = (name, ok, extra = "") => {
  if (ok) { pass += 1; console.log("  ✅", name); }
  else { fail += 1; console.log("  ❌", name, extra); }
};

const c = new NorthClient({ baseUrl: base, account: "tester", password: "pw" });
const devices = await c.listDevices({ maxResults: 5 });
check("设备列表", devices.items?.length === 1);
check("默认脱敏", devices.items[0].password === "***");
check("profile", (await c.profile()).id === "u1");
check("telemetry", (await c.telemetry("DEV-1")).values.wd === "25.3");
check("history", Array.isArray((await c.history("DEV-1", { limit: 5 })).items));
check("send command", (await c.sendCommand("DEV-1", "set", ["sw", "1"])).tra === "tra-1");
check("commands", Array.isArray((await c.listCommands({ deviceId: "DEV-1" })).items));
check("alarms", Array.isArray((await c.listAlarms()).items));
check("products", (await c.listProducts()).items[0].id === "RSTICQ");
check("update metric", (await c.updateMetric("RSTICQ", "in1", { access: "rw" })).after.access === "rw");
check("ports", (await c.gatewayPorts()).tcp[0] === 41032);

let caught = null;
try { await c.listAlarms({ status: "ratelimit" }); } catch (e) { caught = e; }
check("429 抛错", caught instanceof NorthError && caught.code === 429);

console.log(`\n结果: ${pass} passed, ${fail} failed`);
process.exitCode = fail === 0 ? 0 : 1;
