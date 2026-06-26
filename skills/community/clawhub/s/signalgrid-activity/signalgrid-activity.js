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
  const args = parseArgs(process.argv);

  const title = args.title || "No Title";
  const body = args.body || "No Body";
  const type = args.type || "start";
  const finalType = parseType(args.severity) || "info";
  const start_text = args.start_text || "Activity Start";
  const end_text = args.end_text || "Activity End";
  const steps = args.steps || "5";
  const progress = (args.progress || "10").toString().replace(/\D/g, '');
  const progress_legend = args.progress_legend || "true";
  const update_token = args.update_token || "";
  const dismissal_delay = args.dismissal_delay || "60";

  const clientKey = process.env.SIGNALGRID_CLIENT_KEY;
  const channel = process.env.SIGNALGRID_CHANNEL;

  if (!clientKey || !channel) {
    process.exit(1);
  }

  const boundary = `----signalgrid-${Date.now().toString(16)}`;
  
  const payload = buildMultipartForm({
    client_key: clientKey,
    channel,
    severity: finalType, 
    title,
    body,
    type: type,
    start_text: start_text,
    end_text: end_text,
    steps: steps,
    progress: progress,
    progress_legend: progress_legend,
    token: update_token,
    dismissal_delay: dismissal_delay
  }, boundary);

  const options = {
    hostname: "api.signalgrid.co",
    port: 443,
    path: "/v1/activity",
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