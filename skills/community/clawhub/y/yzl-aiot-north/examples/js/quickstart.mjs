// 北向示例（Node.js ESM）：设备列表 → 最新值 → 历史。
//
// 不依赖第三方包：直接用技能自带的 lib/north_client.mjs。
// 环境变量：AIOT_TOKEN 或 AIOT_ACCOUNT + AIOT_PASSWORD（也可用 AIOT_API_KEY）
//
// 运行：node quickstart.mjs

import { NorthClient } from "../lib/north_client.mjs";

const hasCreds = process.env.AIOT_TOKEN || process.env.AIOT_API_KEY
  || (process.env.AIOT_ACCOUNT && process.env.AIOT_PASSWORD);
if (!hasCreds) {
  console.error("请先设置 AIOT_TOKEN、AIOT_API_KEY 或 AIOT_ACCOUNT/AIOT_PASSWORD");
  process.exit(2);
}

const c = await NorthClient.fromEnv();
console.log("whoami:", await c.profile());

const devices = await c.listDevices({ maxResults: 10 });
console.log("设备数:", devices.items?.length ?? 0);
if (!devices.items?.length) process.exit(0);

const dev = devices.items[0];
console.log("第一个设备:", dev.id, dev.name ?? "");
console.log("最新值:", await c.telemetry(dev.id));
console.log("历史:", await c.history(dev.id, { limit: 20 }));
