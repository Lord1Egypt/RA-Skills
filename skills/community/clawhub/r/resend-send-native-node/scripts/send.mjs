#!/usr/bin/env node
// resend-send-native-node/scripts/send.mjs
// Send an email via the Resend.com HTTPS API - native Node.js, zero dependencies.
// Requires Node 18+ (uses native fetch). Reads RESEND_API_KEY from the process environment only.

import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const ENDPOINT = "https://api.resend.com/emails";
const SEND_TIMEOUT_MS = 30_000;

function die(msg, code = 1) {
  process.stderr.write(`error: ${msg}\n`);
  process.exit(code);
}

// -------- credentials --------

function loadApiKey() {
  const key = (process.env.RESEND_API_KEY || "").trim();
  if (!key) die("RESEND_API_KEY not set in process environment. Create one at https://resend.com, check current pricing/limits, and export RESEND_API_KEY.");
  return key;
}

function loadAllowedRecipients() {
  const raw = (process.env.RESEND_ALLOWED_TO || "").trim();
  return new Set(raw.split(",").map(s => s.trim().toLowerCase()).filter(Boolean));
}

function validateAddressList(label, list) {
  const simpleEmail = /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/;
  for (const addr of list) {
    if (!simpleEmail.test(addr)) die(`${label} contains an invalid email address: ${addr}`);
  }
}

function extractEmailAddress(value) {
  const text = String(value || "").trim();
  const angle = text.match(/<([^<>\s]+@[^<>\s]+)>$/);
  return angle ? angle[1] : text;
}

function validateSender(from) {
  const email = extractEmailAddress(from);
  validateAddressList("--from", [email]);
}

function checkRecipientAllowlist(payload) {
  const allowed = loadAllowedRecipients();
  const recipients = [...(payload.to || []), ...(payload.cc || []), ...(payload.bcc || [])];
  if (!allowed.size) return { configured: false, recipients, blocked: recipients };
  const blocked = recipients.filter(addr => !allowed.has(String(addr).toLowerCase()));
  return { configured: true, recipients, blocked };
}

// -------- arg parser --------

function parseArgs(argv) {
  const out = {
    to: [],
    cc: [],
    bcc: [],
    subject: "",
    body: "",
    html: false,
    from: null,      // e.g. "Example Sender <onboarding@resend.dev>"
    replyTo: null,
    dryRun: false,
    send: false,
    json: false,
    inputJsonStdin: false,
    _messageFlagSeen: false,
  };
  const listFlags = new Set(["--to", "--cc", "--bcc"]);
  const singleFlags = new Set(["--subject", "--body", "--from", "--reply-to"]);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--html") { out.html = true; out._messageFlagSeen = true; continue; }
    if (a === "--input-json-stdin") { out.inputJsonStdin = true; continue; }
    if (a === "--dry-run") { out.dryRun = true; continue; }
    if (a === "--send") { out.send = true; continue; }
    if (a === "--json") { out.json = true; continue; }
    if (a === "-h" || a === "--help") { printHelp(); process.exit(0); }
    if (listFlags.has(a)) {
      const v = argv[++i];
      if (v === undefined) die(`flag ${a} needs a value`);
      out._messageFlagSeen = true;
      const key = a.slice(2);
      out[key].push(...v.split(",").map(s => s.trim()).filter(Boolean));
      continue;
    }
    if (singleFlags.has(a)) {
      const v = argv[++i];
      if (v === undefined) die(`flag ${a} needs a value`);
      out._messageFlagSeen = true;
      switch (a) {
        case "--subject":  out.subject = v; break;
        case "--body":     out.body    = v; break;
        case "--from":     out.from    = v; break;
        case "--reply-to": out.replyTo = v; break;
      }
      continue;
    }
    if (a === "--body-file") die("--body-file is not supported in the public package. Review file contents yourself and pass approved text with --body.");
    die(`unknown arg: ${a}. Try --help.`);
  }
  if (out.inputJsonStdin) applyInputJsonFromStdin(out);
  delete out._messageFlagSeen;
  return out;
}

function asStringList(label, value) {
  if (value === undefined || value === null) return [];
  if (Array.isArray(value)) {
    return value.map((item) => {
      if (typeof item !== "string") die(`${label} entries must be strings in --input-json-stdin payload`);
      return item.trim();
    }).filter(Boolean);
  }
  if (typeof value === "string") return value.split(",").map(s => s.trim()).filter(Boolean);
  die(`${label} must be a string or string array in --input-json-stdin payload`);
}

function optionalString(label, value) {
  if (value === undefined || value === null || value === "") return null;
  if (typeof value !== "string") die(`${label} must be a string in --input-json-stdin payload`);
  return value;
}

function applyInputJsonFromStdin(out) {
  if (out._messageFlagSeen) die("--input-json-stdin cannot be combined with inline message flags such as --to, --subject, --body, --from, --reply-to, --cc, --bcc, or --html. Pass message content through stdin JSON and mode flags through argv.");
  let raw;
  try {
    raw = readFileSync(0, "utf8");
  } catch (e) {
    die(`failed to read --input-json-stdin payload: ${e.message || e}`);
  }
  if (!raw.trim()) die("--input-json-stdin requires a JSON object on stdin");
  let payload;
  try {
    payload = JSON.parse(raw);
  } catch (e) {
    die(`--input-json-stdin payload is not valid JSON: ${e.message || e}`);
  }
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) die("--input-json-stdin payload must be a JSON object");
  const allowed = new Set(["to", "cc", "bcc", "subject", "body", "html", "from", "replyTo", "reply_to"]);
  const unknown = Object.keys(payload).filter((key) => !allowed.has(key));
  if (unknown.length) die(`--input-json-stdin payload has unsupported field(s): ${unknown.join(", ")}`);
  out.to = asStringList("to", payload.to);
  out.cc = asStringList("cc", payload.cc);
  out.bcc = asStringList("bcc", payload.bcc);
  out.subject = optionalString("subject", payload.subject) || "";
  out.body = optionalString("body", payload.body) || "";
  if (payload.html !== undefined) {
    if (typeof payload.html !== "boolean") die("html must be a boolean in --input-json-stdin payload");
    out.html = payload.html;
  }
  out.from = optionalString("from", payload.from);
  out.replyTo = optionalString("replyTo", payload.replyTo ?? payload.reply_to);
}

function printHelp() {
  process.stdout.write(
    "Usage: send.mjs --to addr[,addr] --subject \"text\" --body \"text\" [flags]\n" +
    "\n" +
    "Required message fields (inline flags or --input-json-stdin):\n" +
    "  --to       comma-separated recipients\n" +
    "  --subject  message subject\n" +
    "  --body     message body text or HTML\n" +
    "\n" +
    "Optional:\n" +
    "  --cc         comma-separated cc recipients\n" +
    "  --bcc        comma-separated bcc recipients\n" +
    "  --from       sender (e.g. 'Example Sender <onboarding@resend.dev>'). Default: onboarding@resend.dev\n" +
    "  --reply-to   reply-to address\n" +
    "  --html       body is HTML instead of plain text\n" +
    "  --dry-run    build request but don't send; print the JSON payload\n" +
    "  --send       actually send; without this flag the script dry-runs by default\n" +
    "  --json       print a stable machine-readable receipt for dry-run or send\n" +
    "  --input-json-stdin\n" +
    "               read message fields from one JSON object on stdin; use this for\n" +
    "               agent-generated or arbitrary text to avoid shell interpolation\n" +
    "\n" +
    "Credentials (process environment only):\n" +
    "  RESEND_API_KEY    API key from https://resend.com (starts with re_)\n" +
    "  RESEND_ALLOWED_TO comma-separated recipient allowlist for real sends\n" +
    "                    operator-controlled; do not set/widen merely to make --send succeed\n"
  );
}

// -------- main --------

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.to.length) die("at least one --to recipient is required");
  if (!args.subject) die("--subject is required");
  if (!args.body) die("--body is required");

  validateAddressList("--to", args.to);
  validateAddressList("--cc", args.cc);
  validateAddressList("--bcc", args.bcc);
  if (args.replyTo) validateAddressList("--reply-to", [args.replyTo]);

  const from = args.from || "onboarding@resend.dev";
  validateSender(from);

  // Resend accepts either `text` or `html` (or both); we pick based on --html.
  const payload = {
    from,
    to: args.to,
    subject: args.subject,
  };
  if (args.cc.length)  payload.cc  = args.cc;
  if (args.bcc.length) payload.bcc = args.bcc;
  if (args.replyTo)    payload.reply_to = args.replyTo;
  if (args.html) payload.html = args.body; else payload.text = args.body;

  const allowlist = checkRecipientAllowlist(payload);
  const bodyBytes = Buffer.byteLength(args.body || "", "utf8");
  const bodyHash = createHash("sha256").update(args.body || "", "utf8").digest("hex").slice(0, 12);

  const bodySha256 = createHash("sha256").update(args.body || "", "utf8").digest("hex");

  if (args.dryRun || !args.send) {
    if (args.json) {
      process.stdout.write(JSON.stringify({
        mode: "dry-run",
        sent: false,
        endpoint: ENDPOINT,
        to: args.to,
        cc: args.cc,
        bcc: args.bcc,
        from,
        replyTo: args.replyTo,
        subject: args.subject,
        contentType: args.html ? "html" : "text",
        bodyBytes,
        bodySha256,
        bodySha256Prefix: bodyHash,
        allowlist,
        payload,
      }, null, 2) + "\n");
      return;
    }
    process.stdout.write("--- DRY RUN: request would be sent ---\n");
    if (!args.send) process.stdout.write("note: add --send to perform a real send after explicit approval.\n");
    process.stdout.write(`body: ${bodyBytes} bytes, sha256:${bodyHash}\n`);
    if (!allowlist.configured) {
      process.stdout.write("WARNING: RESEND_ALLOWED_TO is not configured. Real sends will fail closed until an allowlist is set.\n");
    } else if (allowlist.blocked.length) {
      process.stdout.write(`WARNING: recipient(s) not in RESEND_ALLOWED_TO allowlist: ${allowlist.blocked.join(", ")}\n`);
    } else {
      process.stdout.write("allowlist: all recipients are allowed by RESEND_ALLOWED_TO.\n");
    }
    process.stdout.write(`POST ${ENDPOINT}\n`);
    process.stdout.write("Authorization: Bearer [redacted]\n\n");
    process.stdout.write(JSON.stringify(payload, null, 2) + "\n");
    return;
  }

  if (!allowlist.configured) die("RESEND_ALLOWED_TO must be set for real sends. Refusing --send without a recipient allowlist.");
  if (allowlist.blocked.length) die(`recipient not in RESEND_ALLOWED_TO allowlist: ${allowlist.blocked.join(", ")}`);
  const apiKey = loadApiKey();

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), SEND_TIMEOUT_MS);
  let resp;
  try {
    resp = await fetch(ENDPOINT, {
      method: "POST",
      redirect: "error",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
  } catch (e) {
    if (e?.name === "AbortError") die("network timeout after 30s; verify in the Resend dashboard before re-sending to avoid duplicates.");
    die(`network error: ${e.message || e}. If the request may have reached Resend, verify in the dashboard before retrying to avoid duplicates.`);
  } finally {
    clearTimeout(timeout);
  }

  let text;
  try {
    text = await resp.text();
  } catch (e) {
    die(`response read error: ${e.message || e}. Verify in the Resend dashboard before retrying to avoid duplicates.`);
  }
  if (!resp.ok) {
    let detail = text;
    try { const j = JSON.parse(text); detail = j.message || j.error || text; } catch {}
    const retryNote = resp.status >= 500 ? " If the request may have reached Resend, verify in the dashboard before retrying to avoid duplicates." : "";
    die(`HTTP ${resp.status}: ${String(detail).slice(0, 500)}${retryNote}`);
  }

  let data;
  try { data = JSON.parse(text); } catch { data = { raw: text }; }
  const id = data.id || "(no id)";
  if (args.json) {
    process.stdout.write(JSON.stringify({
      mode: "send",
      sent: true,
      endpoint: ENDPOINT,
      to: args.to,
      cc: args.cc,
      bcc: args.bcc,
      from,
      replyTo: args.replyTo,
      subject: args.subject,
      contentType: args.html ? "html" : "text",
      bodyBytes,
      bodySha256,
      bodySha256Prefix: bodyHash,
      allowlist,
      resendId: id,
    }, null, 2) + "\n");
    return;
  }
  process.stdout.write(`sent to ${args.to.join(", ")} (subject: ${args.subject}) - resend-id: ${id}\n`);
}

main().catch((e) => die(e?.message || String(e)));
