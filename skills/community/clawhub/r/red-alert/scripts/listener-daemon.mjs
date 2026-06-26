#!/usr/bin/env node
/**
 * Persistent Red Alert listener daemon
 * - Connects via socket.io to redalert.orielhaim.com
 * - Stores all alerts to JSONL file
 * - Writes new alerts to a "pending" file for the notification cron to pick up
 */
import { io } from "socket.io-client";
import fs from "fs";

const ALERTS_FILE = "/data/clawd/tmp/redalert-live.jsonl";
const PENDING_FILE = "/data/clawd/tmp/redalert-pending.jsonl";

const socket = io("https://redalert.orielhaim.com", {
  auth: process.env.RED_ALERT_API_KEY ? { apiKey: process.env.RED_ALERT_API_KEY } : undefined,
  transports: ["websocket"],
  reconnection: true,
  reconnectionDelay: 2000,
  reconnectionDelayMax: 30000,
  reconnectionAttempts: Infinity
});

socket.on("connect", () => {
  const msg = JSON.stringify({ event: "connected", id: socket.id, time: new Date().toISOString() });
  console.log(msg);
  fs.appendFileSync(ALERTS_FILE, msg + "\n");
});

socket.on("disconnect", (reason) => {
  console.log(JSON.stringify({ event: "disconnected", reason, time: new Date().toISOString() }));
});

socket.on("connect_error", (err) => {
  console.error(`Reconnecting... (${err.message})`);
});

// Alert events
const ALERT_EVENTS = ["alert", "missiles", "rockets", "hostileAircraftIntrusion", 
                       "tsunami", "earthquake", "terroristInfiltration"];

socket.onAny((eventName, ...args) => {
  if (eventName === "connect" || eventName === "disconnect" || eventName === "connect_error") return;
  
  for (const alertData of args) {
    if (!alertData || typeof alertData !== "object") continue;
    
    const record = {
      event: alertData.type || eventName,
      cities: alertData.cities || [],
      title: alertData.title || "",
      instructions: alertData.instructions || "",
      cityCount: (alertData.cities || []).length,
      receivedAt: new Date().toISOString()
    };
    
    const line = JSON.stringify(record);
    fs.appendFileSync(ALERTS_FILE, line + "\n");
    fs.appendFileSync(PENDING_FILE, line + "\n");
    console.log(line);
  }
});

// Keep alive
setInterval(() => {}, 60000);

process.on("SIGTERM", () => { socket.disconnect(); process.exit(0); });
process.on("SIGINT", () => { socket.disconnect(); process.exit(0); });
