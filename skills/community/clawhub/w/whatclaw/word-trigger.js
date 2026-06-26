#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { execFile } = require("child_process");

const DATA_DIR = path.join(__dirname, "data");
const WHITELIST_FILE = path.join(DATA_DIR, "whitelist.json");
const MESSAGE_STORE_FILE = path.join(DATA_DIR, "message-store.json");

function ensureDataFiles() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  if (!fs.existsSync(WHITELIST_FILE)) {
    fs.writeFileSync(WHITELIST_FILE, JSON.stringify({ sets: {} }, null, 2));
  }
  if (!fs.existsSync(MESSAGE_STORE_FILE)) {
    fs.writeFileSync(
      MESSAGE_STORE_FILE,
      JSON.stringify({ messages: {}, updatedAt: new Date().toISOString() }, null, 2)
    );
  }
}

function readJson(filePath, fallback) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (_err) {
    return fallback;
  }
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2));
}

function nowIso() {
  return new Date().toISOString();
}

function normalizePhone(phone) {
  if (typeof phone !== "string") {
    return null;
  }
  const trimmed = phone.trim();
  if (!trimmed) {
    return null;
  }
  const digits = trimmed.replace(/[^\d+]/g, "");
  const withPlus = digits.startsWith("+") ? digits : `+${digits.replace(/\+/g, "")}`;
  const onlyDigits = withPlus.replace("+", "");
  if (!/^\d{8,15}$/.test(onlyDigits)) {
    return null;
  }
  return `+${onlyDigits}`;
}

function setNameValid(name) {
  return typeof name === "string" && /^[a-zA-Z0-9_-]{1,64}$/.test(name);
}

function execOpenclaw(args) {
  return new Promise((resolve, reject) => {
    execFile("openclaw", args, { maxBuffer: 10 * 1024 * 1024 }, (error, stdout, stderr) => {
      if (error) {
        reject(new Error(stderr || stdout || error.message));
        return;
      }
      resolve({ stdout, stderr });
    });
  });
}

async function checkWhatsAppConnected() {
  const { stdout } = await execOpenclaw(["channels", "status", "--probe"]);
  return /whatsapp/i.test(stdout) && /connected/i.test(stdout) && !/error/i.test(stdout);
}

function getWhitelistData() {
  const data = readJson(WHITELIST_FILE, { sets: {} });
  if (!data.sets || typeof data.sets !== "object") {
    return { sets: {} };
  }
  return data;
}

function saveWhitelistData(data) {
  writeJson(WHITELIST_FILE, data);
}

function getMessageStore() {
  const data = readJson(MESSAGE_STORE_FILE, { messages: {}, updatedAt: nowIso() });
  if (!data.messages || typeof data.messages !== "object") {
    return { messages: {}, updatedAt: nowIso() };
  }
  return data;
}

function saveMessageStore(data) {
  data.updatedAt = nowIso();
  writeJson(MESSAGE_STORE_FILE, data);
}

async function sendWhatsAppMessage(to, options) {
  const args = ["message", "send", "--channel", "whatsapp", "--target", to];
  if (options.message) {
    args.push("--message", options.message);
  }
  if (options.media) {
    args.push("--media", options.media);
  }
  args.push("--json");

  const { stdout } = await execOpenclaw(args);
  const parsed = JSON.parse(stdout);
  const result = parsed && parsed.payload && parsed.payload.result ? parsed.payload.result : null;
  if (!result || !result.messageId) {
    throw new Error("OpenClaw send succeeded but messageId was missing.");
  }
  return result;
}

async function enrichMessageStatus(messageId) {
  try {
    const { stdout } = await execOpenclaw(["channels", "logs", "--channel", "whatsapp", "--json", "--lines", "1000"]);
    const parsed = JSON.parse(stdout);
    const lines = Array.isArray(parsed.lines) ? parsed.lines : [];
    const matching = lines.filter((line) => {
      const message = String(line.message || "");
      const raw = String(line.raw || "");
      return message.includes(messageId) || raw.includes(messageId);
    });
    if (matching.length === 0) {
      return "unknown";
    }
    const combined = matching.map((line) => `${line.message || ""} ${line.raw || ""}`).join(" ").toLowerCase();
    if (combined.includes(" read")) return "read";
    if (combined.includes("deliver")) return "delivered";
    if (combined.includes("sent message") || combined.includes(" sent ")) return "sent";
    if (combined.includes("failed") || combined.includes("error")) return "failed";
    return "unknown";
  } catch (_err) {
    return "unknown";
  }
}

function printHelp() {
  console.log(`Word trigger mode (no HTTP API)

Usage:
  node word-trigger.js "<phrase>"

Examples:
  node word-trigger.js "check whatsapp"
  node word-trigger.js "create set demo_ops"
  node word-trigger.js "list sets"
  node word-trigger.js "add +918657704479 to demo_ops"
  node word-trigger.js "update +918657704479 to +918657704480 in demo_ops"
  node word-trigger.js "remove +918657704480 from demo_ops"
  node word-trigger.js "send 'Hello team' to demo_ops"
  node word-trigger.js "send 'Invoice attached' with media /path/to/invoice.pdf to demo_ops"
  node word-trigger.js "send media https://example.com/image.jpg to demo_ops"
  node word-trigger.js "status 3EB0F09EA29438B49F44F8"
`);
}

async function run(phrase) {
  const text = phrase.trim();
  const lower = text.toLowerCase();
  if (!text || lower === "help") {
    printHelp();
    return;
  }

  if (lower === "check whatsapp" || lower === "health") {
    const connected = await checkWhatsAppConnected();
    console.log(JSON.stringify({ whatsappConnected: connected, checkedAt: nowIso() }, null, 2));
    return;
  }

  if (lower === "list sets") {
    const data = getWhitelistData();
    console.log(JSON.stringify(data, null, 2));
    return;
  }

  const createMatch = text.match(/^create\s+set\s+([a-zA-Z0-9_-]{1,64})$/i);
  if (createMatch) {
    const setName = createMatch[1];
    const data = getWhitelistData();
    if (data.sets[setName]) {
      throw new Error(`Set '${setName}' already exists.`);
    }
    data.sets[setName] = [];
    saveWhitelistData(data);
    console.log(JSON.stringify({ setName, numbers: [] }, null, 2));
    return;
  }

  const showMatch = text.match(/^show\s+set\s+([a-zA-Z0-9_-]{1,64})$/i);
  if (showMatch) {
    const setName = showMatch[1];
    const data = getWhitelistData();
    if (!data.sets[setName]) {
      throw new Error(`Set '${setName}' not found.`);
    }
    console.log(JSON.stringify({ setName, numbers: data.sets[setName] }, null, 2));
    return;
  }

  const addMatch = text.match(/^add\s+(\+?\d[\d\s-]{6,20}\d)\s+to\s+([a-zA-Z0-9_-]{1,64})$/i);
  if (addMatch) {
    const number = normalizePhone(addMatch[1]);
    const setName = addMatch[2];
    if (!number || !setNameValid(setName)) {
      throw new Error("Invalid add command.");
    }
    const data = getWhitelistData();
    if (!data.sets[setName]) {
      throw new Error(`Set '${setName}' not found.`);
    }
    if (data.sets[setName].includes(number)) {
      throw new Error(`${number} already in set '${setName}'.`);
    }
    data.sets[setName].push(number);
    data.sets[setName].sort();
    saveWhitelistData(data);
    console.log(JSON.stringify({ setName, numbers: data.sets[setName] }, null, 2));
    return;
  }

  const updateMatch = text.match(
    /^update\s+(\+?\d[\d\s-]{6,20}\d)\s+to\s+(\+?\d[\d\s-]{6,20}\d)\s+in\s+([a-zA-Z0-9_-]{1,64})$/i
  );
  if (updateMatch) {
    const oldNumber = normalizePhone(updateMatch[1]);
    const newNumber = normalizePhone(updateMatch[2]);
    const setName = updateMatch[3];
    const data = getWhitelistData();
    if (!oldNumber || !newNumber || !data.sets[setName]) {
      throw new Error("Invalid update command or set not found.");
    }
    if (!data.sets[setName].includes(oldNumber)) {
      throw new Error(`Number ${oldNumber} not found in set '${setName}'.`);
    }
    const next = data.sets[setName].filter((n) => n !== oldNumber);
    if (next.includes(newNumber)) {
      throw new Error(`${newNumber} already exists in set '${setName}'.`);
    }
    next.push(newNumber);
    next.sort();
    data.sets[setName] = next;
    saveWhitelistData(data);
    console.log(JSON.stringify({ setName, numbers: next }, null, 2));
    return;
  }

  const removeMatch = text.match(/^remove\s+(\+?\d[\d\s-]{6,20}\d)\s+from\s+([a-zA-Z0-9_-]{1,64})$/i);
  if (removeMatch) {
    const number = normalizePhone(removeMatch[1]);
    const setName = removeMatch[2];
    const data = getWhitelistData();
    if (!number || !data.sets[setName]) {
      throw new Error("Invalid remove command or set not found.");
    }
    if (!data.sets[setName].includes(number)) {
      throw new Error(`Number ${number} not found in set '${setName}'.`);
    }
    data.sets[setName] = data.sets[setName].filter((n) => n !== number);
    saveWhitelistData(data);
    console.log(JSON.stringify({ setName, numbers: data.sets[setName] }, null, 2));
    return;
  }

  const sendMatch = text.match(
    /^send\s+(?:(?:'([^']+)')|(?:"([^"]+)")|([^"]+?))?(?:\s+with\s+media\s+(\S+))?\s+to\s+([a-zA-Z0-9_-]{1,64})$/i
  );
  const sendMediaOnlyMatch = text.match(/^send\s+media\s+(\S+)\s+to\s+([a-zA-Z0-9_-]{1,64})$/i);

  if (sendMatch || sendMediaOnlyMatch) {
    let message = "";
    let media = "";
    let setName = "";

    if (sendMediaOnlyMatch) {
      media = sendMediaOnlyMatch[1].trim();
      setName = sendMediaOnlyMatch[2];
    } else {
      message = (sendMatch[1] || sendMatch[2] || sendMatch[3] || "").trim();
      media = (sendMatch[4] || "").trim();
      setName = sendMatch[5];
    }

    if (!setNameValid(setName)) {
      throw new Error("Invalid setName.");
    }
    if (!message && !media) {
      throw new Error("Either message or media is required.");
    }

    const connected = await checkWhatsAppConnected();
    if (!connected) {
      throw new Error("WhatsApp integration is not connected.");
    }

    const whitelist = getWhitelistData();
    const set = whitelist.sets[setName];
    if (!set) {
      throw new Error(`Set '${setName}' not found.`);
    }
    if (set.length === 0) {
      throw new Error(`Set '${setName}' is empty.`);
    }

    const store = getMessageStore();
    const results = [];
    for (const to of set) {
      try {
        const result = await sendWhatsAppMessage(to, { message, media });
        store.messages[result.messageId] = {
          messageId: result.messageId,
          to,
          setName,
          message: message || null,
          media: media || null,
          runId: result.runId || null,
          toJid: result.toJid || null,
          status: "sent",
          statusSource: "send-result",
          createdAt: nowIso(),
          updatedAt: nowIso(),
        };
        results.push({ to, ok: true, messageId: result.messageId, status: "sent" });
      } catch (err) {
        results.push({ to, ok: false, error: String(err.message || err) });
      }
    }
    saveMessageStore(store);
    console.log(
      JSON.stringify(
        {
          setName,
          requested: set.length,
          success: results.filter((x) => x.ok).length,
          failed: results.filter((x) => !x.ok).length,
          results,
        },
        null,
        2
      )
    );
    return;
  }

  const statusMatch = text.match(/^status\s+([A-Za-z0-9]+)$/i);
  if (statusMatch) {
    const messageId = statusMatch[1];
    const store = getMessageStore();
    const item = store.messages[messageId];
    if (!item) {
      throw new Error("messageId not found in local store.");
    }
    const enriched = await enrichMessageStatus(messageId);
    if (enriched !== "unknown" && item.status !== enriched) {
      item.status = enriched;
      item.statusSource = "channels-logs";
      item.updatedAt = nowIso();
      store.messages[messageId] = item;
      saveMessageStore(store);
    }
    console.log(
      JSON.stringify(
        {
          messageId,
          status: item.status,
          statusSource: item.statusSource,
          to: item.to,
          setName: item.setName,
          createdAt: item.createdAt,
          updatedAt: item.updatedAt,
        },
        null,
        2
      )
    );
    return;
  }

  printHelp();
  throw new Error("Could not parse phrase. See examples above.");
}

ensureDataFiles();
const phrase = process.argv.slice(2).join(" ").trim();
run(phrase).catch((err) => {
  console.error(`Error: ${String(err.message || err)}`);
  process.exit(1);
});

