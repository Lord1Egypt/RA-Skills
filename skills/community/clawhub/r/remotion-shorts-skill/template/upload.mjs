#!/usr/bin/env node
// Upload one file to a WoopSocial media upload session (no extra packages).
//
//   node upload.mjs session.json out/short/short.mp4
//
// 1. The agent calls media_uploads_create_session with the projectId and the exact file size.
// 2. It saves the response as session.json and runs this script, which PUTs every part.
// 3. The agent calls media_uploads_complete_session and waits for READY (it returns the mediaId).
//
// If a network allowlist blocks the upload, allow *.r2.cloudflarestorage.com.

import fs from "node:fs";

const [sessionPath, filePath] = process.argv.slice(2);
if (!sessionPath || !filePath) {
  console.log("Usage: node upload.mjs session.json video.mp4");
  process.exit(1);
}

const session = JSON.parse(fs.readFileSync(sessionPath, "utf8"));
const partSize = Number(session.partSizeInBytes);
const parts = [...session.parts].sort((a, b) => a.partNumber - b.partNumber);
const partCount = Number(session.partCount ?? parts.length);
const size = fs.statSync(filePath).size;
const needed = Math.ceil(size / partSize);
if (needed !== partCount || parts.length !== partCount) {
  console.error(`The session expects ${partCount} part(s) but the file needs ${needed}. Create the session with the exact file size: ${size} bytes.`);
  process.exit(1);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const fd = fs.openSync(filePath, "r");

for (const part of parts) {
  const offset = (part.partNumber - 1) * partSize;
  const length = Math.min(partSize, size - offset);
  const chunk = Buffer.alloc(length);
  fs.readSync(fd, chunk, 0, length, offset);
  let problem = "";
  let ok = false;
  for (let attempt = 1; attempt <= 4 && !ok; attempt++) {
    try {
      const res = await fetch(part.uploadUrl, { method: "PUT", body: chunk, headers: { "Content-Type": "application/octet-stream" } });
      if (res.ok) ok = true;
      else if (res.status === 403) {
        console.error(`Part ${part.partNumber} was refused (HTTP 403): the upload links have probably expired. Create a new upload session and run this again.`);
        process.exit(1);
      } else problem = `HTTP ${res.status}`;
    } catch (e) {
      problem = e.cause?.message ?? e.message;
    }
    if (!ok && attempt < 4) {
      console.error(`part ${part.partNumber}: ${problem}; retrying in ${5 * attempt} s`);
      await sleep(5000 * attempt);
    }
  }
  if (!ok) {
    console.error(`Part ${part.partNumber} failed after 4 tries (${problem}). Check the connection; if a network allowlist is on, allow *.r2.cloudflarestorage.com.`);
    process.exit(1);
  }
  console.log(`part ${part.partNumber}/${partCount} uploaded`);
}
fs.closeSync(fd);
console.log("All parts uploaded. Now call media_uploads_complete_session.");
