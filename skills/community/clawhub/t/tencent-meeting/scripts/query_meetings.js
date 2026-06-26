#!/usr/bin/env node
/**
 * Query meetings by meeting ID or meeting code.
 *
 * Usage:
 *   node query_meetings.js --meeting-id <ID> --userid <UID>
 *   node query_meetings.js --meeting-code <CODE> --userid <UID>
 *
 * Env: TM_SECRET_ID, TM_SECRET_KEY, TM_APP_ID, TM_SDK_ID
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

async function queryMeetings(opts) {
  let uri;
  if (opts.meeting_id) {
    uri = `/v1/meetings/${opts.meeting_id}?userid=${opts.userid}&instanceid=${opts.instanceid || 1}`;
  } else if (opts.meeting_code) {
    uri = `/v1/meetings?meeting_code=${opts.meeting_code}&userid=${opts.userid}&instanceid=${opts.instanceid || 1}`;
  } else {
    console.error("Provide --meeting-id or --meeting-code");
    process.exit(1);
  }

  const headers = buildHeaders("GET", uri, "");
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
    console.error("Usage: node query_meetings.js --meeting-id <ID> --userid <UID>");
    process.exit(1);
  }
  queryMeetings(args).catch(e => { console.error(e); process.exit(1); });
}

module.exports = { queryMeetings };
