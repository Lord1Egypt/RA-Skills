#!/usr/bin/env node

const https = require("https");

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
    } else {
      args[key] = next;
      i++;
    }
  }
  return args;
}

function parseType(input) {
  // Convert to string, lowercase it, and remove any accidental spaces
  const raw = String(input || "").toLowerCase().trim();
  
  const critList = ["critical", "crit", "failure", "error", "err", "fail", "alarm"];
  const warnList = ["warning", "warn", "alert"];
  const successList = ["success", "successful", "successfully", "ok", "done"];

  if (critList.includes(raw)) {
    return "crit";
  }
  if (warnList.includes(raw)) {
    return "warn";
  }
  if (successList.includes(raw)) {
    return "success";
  }
  
  return "info";
}

function escapeMultipartValue(value) {
  return String(value).replace(/\r?\n/g, "\r\n");
}

function buildMultipartForm(fields, boundary) {
  const chunks = [];
  for (const [name, value] of Object.entries(fields)) {
    chunks.push(Buffer.from(`--${boundary}\r\n`));
    chunks.push(Buffer.from(`Content-Disposition: form-data; name="${name}"\r\n\r\n`));
    chunks.push(Buffer.from(escapeMultipartValue(value)));
    chunks.push(Buffer.from("\r\n"));
  }
  chunks.push(Buffer.from(`--${boundary}--\r\n`));
  return Buffer.concat(chunks);
}

async function main() {
  console.log("DEBUG - Raw Process Args:", process.argv);
  const args = parseArgs(process.argv);
  console.log("DEBUG - Parsed Args Object:", args);

  const title = args.title || "No Title";
  const body = args.body || "No Body";
  
  // CRITICAL FIX: We re-assign the variable to the cleaned version immediately
  const finalType = parseType(args.type); 
  
  // Force critical flag if the type is "crit"
  const isCritical = (args.critical === "true" || finalType === "crit") ? "true" : "false";

  const clientKey = process.env.SIGNALGRID_CLIENT_KEY;
  const channel = process.env.SIGNALGRID_CHANNEL;

  if (!clientKey || !channel) {
    process.exit(1);
  }

  const boundary = `----signalgrid-${Date.now().toString(16)}`;
  
  // The payload now uses finalType, which is GUARANTEED to be crit, warn, success, or info
  const payload = buildMultipartForm({
    client_key: clientKey,
    channel,
    type: finalType, 
    title,
    body,
    critical: isCritical
  }, boundary);

  const options = {
    hostname: "api.signalgrid.co",
    port: 443,
    path: "/v1/push",
    method: "POST",
    headers: {
      "Content-Type": `multipart/form-data; boundary=${boundary}`,
      "Content-Length": payload.length
    }
  };

  await new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      res.on("data", () => {});
      res.on("end", () => resolve());
    });
    req.on("error", reject);
    req.write(payload);
    req.end();
  });

  console.log(JSON.stringify({ ok: true, sent_type: finalType, critical: isCritical }));
}

main().catch(() => process.exit(1));