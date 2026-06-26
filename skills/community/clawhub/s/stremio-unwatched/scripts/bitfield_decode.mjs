#!/usr/bin/env node
// Decodes Stremio's watched bitfield format.
// Usage: node bitfield_decode.mjs <serialized_bitfield> <video_ids_json>
// Output: JSON object mapping video_id -> watched (boolean)
//
// The serialized format is: {anchorVideoId}:{anchorLength}:{base64_zlib_data}
// Since anchorVideoId contains colons (e.g. tt123:1:5), parse by popping from the right.

import { inflateSync } from "node:zlib";

function decodeWatchedBitfield(serialized, videoIds) {
  if (!serialized || !videoIds.length) {
    return Object.fromEntries(videoIds.map((id) => [id, false]));
  }

  const parts = serialized.split(":");
  if (parts.length < 3) {
    return Object.fromEntries(videoIds.map((id) => [id, false]));
  }

  const base64Data = parts.pop();
  const anchorLength = parseInt(parts.pop(), 10);
  const anchorVideoId = parts.join(":");

  let rawBytes;
  try {
    rawBytes = inflateSync(Buffer.from(base64Data, "base64"));
  } catch {
    return Object.fromEntries(videoIds.map((id) => [id, false]));
  }

  const anchorIdx = videoIds.indexOf(anchorVideoId);
  if (anchorIdx === -1) {
    return Object.fromEntries(videoIds.map((id) => [id, false]));
  }

  const offset = anchorLength - 1 - anchorIdx;

  function getBit(i) {
    if (i < 0 || i >= rawBytes.length * 8) return false;
    return (rawBytes[Math.floor(i / 8)] & (1 << (i % 8))) !== 0;
  }

  const result = {};
  for (let i = 0; i < videoIds.length; i++) {
    result[videoIds[i]] = getBit(i + offset);
  }
  return result;
}

// CLI interface
const [serialized, videoIdsJson] = process.argv.slice(2);
if (!serialized || !videoIdsJson) {
  console.error(
    "Usage: node bitfield_decode.mjs <serialized_bitfield> <video_ids_json>"
  );
  process.exit(1);
}

const videoIds = JSON.parse(videoIdsJson);
const result = decodeWatchedBitfield(serialized, videoIds);
console.log(JSON.stringify(result));
