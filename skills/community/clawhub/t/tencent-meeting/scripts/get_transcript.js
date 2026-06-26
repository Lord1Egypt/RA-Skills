#!/usr/bin/env node
/**
 * Get Tencent Meeting recording transcript.
 *
 * Usage:
 *   node get_transcript.js --record-file-id <ID> --operator-id <UID> [--meeting-id <MID>] [--operator-id-type 1] [--type 0] [--format text|json]
 *
 * Env: TM_SECRET_ID, TM_SECRET_KEY, TM_APP_ID, TM_SDK_ID
 *       TM_STS_TOKEN (required for transcript API since 2026-02-10)
 */

const { buildHeaders } = require("./sign");

const API_BASE = "https://api.meeting.qq.com";

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 2) {
    const key = argv[i].replace(/^--/, "").replace(/-/g, "_");
    args[key] = argv[i + 1];
  }
  return args;
}

async function getTranscript(opts) {
  const params = new URLSearchParams();
  params.set("record_file_id", opts.record_file_id);
  params.set("operator_id", opts.operator_id);
  params.set("operator_id_type", opts.operator_id_type || "1");
  if (opts.meeting_id) params.set("meeting_id", opts.meeting_id);
  if (opts.transcripts_type) params.set("transcripts_type", opts.transcripts_type);
  if (opts.pid) params.set("pid", opts.pid);
  if (opts.limit) params.set("limit", opts.limit);

  const uri = `/v1/records/transcripts/details?${params.toString()}`;
  const headers = buildHeaders("GET", uri, "");

  // STS-Token required since 2026-02-10
  const stsToken = opts.sts_token || process.env.TM_STS_TOKEN;
  if (stsToken) headers["STS-Token"] = stsToken;

  const resp = await fetch(`${API_BASE}${uri}`, { method: "GET", headers });
  const data = await resp.json();

  if (!resp.ok) {
    console.error("API Error:", resp.status, JSON.stringify(data, null, 2));
    process.exit(1);
  }

  const format = opts.format || "text";
  if (format === "json") {
    console.log(JSON.stringify(data, null, 2));
  } else {
    // Flatten to readable text
    const paragraphs = data.minutes?.paragraphs || [];
    for (const p of paragraphs) {
      const speaker = p.speaker_info?.username || "Unknown";
      const sentences = (p.sentences || [])
        .map(s => (s.words || []).map(w => w.text).join(""))
        .join("");
      const startSec = Math.floor((p.start_time || 0) / 1000);
      const min = Math.floor(startSec / 60);
      const sec = startSec % 60;
      const ts = `${String(min).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
      console.log(`[${ts}] ${speaker}: ${sentences}`);
    }
    if (data.minutes?.keywords?.length) {
      console.log(`\nKeywords: ${data.minutes.keywords.join(", ")}`);
    }
  }
}

// CLI
if (require.main === module) {
  const args = parseArgs(process.argv);
  if (!args.record_file_id || !args.operator_id) {
    console.error("Usage: node get_transcript.js --record-file-id <ID> --operator-id <UID> [--meeting-id <MID>] [--format text|json]");
    process.exit(1);
  }
  getTranscript(args).catch(e => { console.error(e); process.exit(1); });
}

module.exports = { getTranscript };
