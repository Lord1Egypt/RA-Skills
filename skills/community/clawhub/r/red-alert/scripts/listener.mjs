#!/usr/bin/env node
/**
 * Persistent Red Alert listener — writes alerts to a JSONL file
 * and outputs to stdout for monitoring.
 */
import { io } from "socket.io-client";
import fs from "fs";

const ALERTS_FILE = "/data/clawd/tmp/redalert-live.jsonl";
const socket = io("https://redalert.orielhaim.com", {
  auth: process.env.RED_ALERT_API_KEY ? { apiKey: process.env.RED_ALERT_API_KEY } : undefined,
  transports: ["websocket"],
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 30000
});

socket.on("connect", () => {
  console.log(JSON.stringify({ event: "connected", id: socket.id, time: new Date().toISOString() }));
});

socket.on("disconnect", (reason) => {
  console.log(JSON.stringify({ event: "disconnected", reason, time: new Date().toISOString() }));
});

socket.onAny((event, ...args) => {
  if (event === "connect" || event === "disconnect") return;
  for (const alert of args) {
    const record = { event, ...alert, receivedAt: new Date().toISOString() };
    const line = JSON.stringify(record);
    console.log(line);
    fs.appendFileSync(ALERTS_FILE, line + "\n");
  }
});

process.on("SIGTERM", () => { socket.disconnect(); process.exit(0); });
process.on("SIGINT", () => { socket.disconnect(); process.exit(0); });
