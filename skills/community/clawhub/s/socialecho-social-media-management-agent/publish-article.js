#!/usr/bin/env node
import fs from "node:fs";

import { buildRequestOptions, callJsonPost, getOption, parseArgs, printAndExit } from "./client.js";

const args = parseArgs(process.argv);
const payloadPath = getOption(args, "payload");

const selectedMusicFields = [
  "url",
  "uuid",
  "cover",
  "title",
  "artist",
  "duration",
  "selection",
  "music_volume",
  "original_sound_volume"
];

function validateSelectedMusic(payload) {
  const music = payload?.extra?.music;
  if (music === undefined || music === null || music.selection === "none") return;
  if (typeof music !== "object" || Array.isArray(music)) {
    throw new Error("extra.music must be an object");
  }
  if (!["trending_clip", "full_track"].includes(music.selection)) {
    throw new Error("extra.music.selection must be none, trending_clip, or full_track");
  }
  const missing = selectedMusicFields.filter((field) => {
    const value = music[field];
    return value === undefined || value === null || (typeof value === "string" && !value.trim());
  });
  if (missing.length) throw new Error(`Selected extra.music is missing: ${missing.join(", ")}`);
  for (const field of ["music_volume", "original_sound_volume"]) {
    if (!Number.isInteger(music[field]) || music[field] < 0 || music[field] > 100) {
      throw new Error(`extra.music.${field} must be an integer between 0 and 100`);
    }
  }
}

let body;
try {
  const raw = fs.readFileSync(payloadPath, "utf8");
  body = JSON.parse(raw);
  validateSelectedMusic(body);
} catch (e) {
  console.error(`Failed to read/parse --payload JSON file: ${payloadPath}`);
  console.error(e?.message || e);
  process.exit(2);
}

const accountId = Number(body?.account_id);
if (!Number.isInteger(accountId) || accountId < 1) {
  throw new Error("payload.account_id must be a positive integer");
}

if (args.execute !== true) {
  console.log(JSON.stringify({
    ok: true,
    dry_run: true,
    action: "publish_article",
    preview: body,
    next: `After explicit user authorization for this exact payload, rerun with --execute --confirm-account-id ${accountId}`
  }, null, 2));
  process.exit(0);
}

const confirmedAccountId = Number(getOption(args, "confirm-account-id"));
if (confirmedAccountId !== accountId) {
  throw new Error(`--confirm-account-id must match payload.account_id (${accountId})`);
}

const options = buildRequestOptions(args);
const result = await callJsonPost("/v1/publish/article", body, options);
printAndExit(result);
