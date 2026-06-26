#!/usr/bin/env node
/**
 * Create a Tencent Meeting.
 *
 * Usage:
 *   node create_meeting.js '<JSON>'
 *
 * JSON fields:
 *   subject      (required) - Meeting subject
 *   userid       (required) - Creator's userid
 *   type         (optional) - 0: scheduled (default), 1: instant
 *   start_time   (required) - ISO 8601 or unix timestamp (seconds)
 *   end_time     (required) - ISO 8601 or unix timestamp (seconds)
 *   password     (optional) - 4-6 digit string
 *   instanceid   (optional) - Device type, default 1 (PC)
 *   invitees     (optional) - Array of {userid} objects
 *   settings     (optional) - Meeting settings object
 *
 * Env: TM_SECRET_ID, TM_SECRET_KEY, TM_APP_ID, TM_SDK_ID
 */

const { buildHeaders } = require("./sign");

const API_BASE = "https://api.meeting.qq.com";

function parseTime(val) {
  if (typeof val === "number") return val.toString();
  const ts = Math.floor(new Date(val).getTime() / 1000);
  if (isNaN(ts)) { console.error(`Invalid time: ${val}`); process.exit(1); }
  return ts.toString();
}

async function createMeeting(params) {
  const body = {
    userid: params.userid,
    instanceid: params.instanceid || 1,
    subject: params.subject,
    type: params.type ?? 0,
    start_time: parseTime(params.start_time),
    end_time: parseTime(params.end_time),
  };

  if (params.password) body.password = params.password;
  if (params.invitees) body.invitees = params.invitees;
  if (params.settings) body.settings = params.settings;
  if (params.meeting_type != null) body.meeting_type = params.meeting_type;
  if (params.recurring_rule) body.recurring_rule = params.recurring_rule;
  if (params.enable_live != null) body.enable_live = params.enable_live;
  if (params.time_zone) body.time_zone = params.time_zone;
  if (params.location) body.location = params.location;
  if (params.hosts) body.hosts = params.hosts;

  const uri = "/v1/meetings";
  const bodyStr = JSON.stringify(body);
  const headers = buildHeaders("POST", uri, bodyStr);

  const resp = await fetch(`${API_BASE}${uri}`, {
    method: "POST",
    headers,
    body: bodyStr,
  });

  const data = await resp.json();
  if (!resp.ok) {
    console.error("API Error:", resp.status, JSON.stringify(data, null, 2));
    process.exit(1);
  }
  console.log(JSON.stringify(data, null, 2));
}

// CLI
if (require.main === module) {
  const input = process.argv[2];
  if (!input) {
    console.error("Usage: node create_meeting.js '<JSON>'");
    process.exit(1);
  }
  createMeeting(JSON.parse(input)).catch(e => { console.error(e); process.exit(1); });
}

module.exports = { createMeeting };
