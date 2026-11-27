// 北向示例（Node.js ESM）：轮询变化 → 推 Webhook（HMAC 签名）。
//
// 不依赖第三方包（技能自带 lib/north_client.mjs）。
//
// 运行：
//   set AIOT_DEVICE=DEV-1
//   set AIOT_WEBHOOK_URL=https://app.example.com/aiot/events
//   node bridge_webhook.mjs

import { createHmac } from "node:crypto";
import { NorthClient } from "../lib/north_client.mjs";

const DEVICE = process.env.AIOT_DEVICE || "";
const WEBHOOK_URL = process.env.AIOT_WEBHOOK_URL || "";
const SECRET = process.env.AIOT_WEBHOOK_SECRET || "";
const INTERVAL = Number(process.env.AIOT_POLL_INTERVAL || 5) * 1000;

if (!DEVICE) {
  console.error("请设置 AIOT_DEVICE");
  process.exit(2);
}

const c = await NorthClient.fromEnv();
let last;
let seq = 0;

setInterval(async () => {
  try {
    const data = await c.telemetry(DEVICE);
    const values = data.values ?? data.data ?? data;
    const text = JSON.stringify(values);
    if (text === last) return;
    last = text;
    seq += 1;
    const payload = { seq, ts: Math.floor(Date.now() / 1000), deviceId: DEVICE, values, online: data.online };
    console.log("变化:", payload);

    if (WEBHOOK_URL) {
      const raw = JSON.stringify(payload);
      const headers = { "Content-Type": "application/json", "X-AIoT-Event": "telemetry" };
      if (SECRET) headers["X-AIoT-Signature"] = "sha256=" + createHmac("sha256", SECRET).update(raw).digest("hex");
      const res = await fetch(WEBHOOK_URL, { method: "POST", headers, body: raw });
      console.log("webhook:", res.status);
    }
  } catch (e) {
    console.error("轮询失败:", e.message);
  }
}, INTERVAL);
