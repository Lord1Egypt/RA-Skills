#!/usr/bin/env node
/**
 * List cloud recording files for a meeting.
 *
 * Usage:
 *   node list_records.js --meeting-id <MID> --userid <UID>
 *   node list_records.js --meeting-record-id <MRID> --userid <UID>
 *
 * Env: TM_SECRET_ID, TM_SECRET_KEY, TM_APP_ID, TM_SDK_ID
 *       TM_STS_TOKEN (required for record detail since 2026-02-10)
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

async function listRecords(opts) {
  let uri;
  if (opts.meeting_record_id) {
    // Get single record detail
    uri = `/v1/records/${opts.meeting_record_id}?userid=${opts.userid}`;
  } else if (opts.meeting_id) {
    // List records for a meeting
    uri = `/v1/meetings/${opts.meeting_id}/records?userid=${opts.userid}`;
  } else {
    console.error("Provide --meeting-id or --meeting-record-id");
    process.exit(1);
  }

  const headers = buildHeaders("GET", uri, "");
  const stsToken = opts.sts_token || process.env.TM_STS_TOKEN;
  if (stsToken) headers["STS-Token"] = stsToken;

  const resp = await fetch(`${API_BASE}${uri}`, { method: "GET", headers });
  const data = await resp.json();

  if (!resp.ok) {
    console.error("API Error:", resp.status, JSON.stringify(data, null, 2));
    process.exit(1);
  }
  console.log(JSON.stringify(data, null, 2));
}

if (require.main === module) {
  const args = parseArgs(process.argv);
  if (!args.userid) {
    console.error("Usage: node list_records.js --meeting-id <MID> --userid <UID>");
    process.exit(1);
  }
  listRecords(args).catch(e => { console.error(e); process.exit(1); });
}

module.exports = { listRecords };
