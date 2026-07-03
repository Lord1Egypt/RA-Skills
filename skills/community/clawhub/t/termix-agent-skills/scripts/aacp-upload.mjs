#!/usr/bin/env node
//
// PUT a local file to a presigned S3 upload URL. Used after any
// `.../upload-url` endpoint (listing media, delivery artifacts, dispute
// evidence, campaign proof) which returns { uploadUrl, s3Key, publicUrl,
// headers: { "content-type" } }.
//
// Usage:
//   node aacp-upload.mjs --url '<presigned PUT url>' --file <path> --content-type <mime>
//
// Prints { ok, status, etag }. The caller then registers the upload with the
// matching API (e.g. POST /orders/:id/delivery/artifacts) using s3Key/publicUrl
// and the file's sha256 (printed here as a convenience).
//
import { readFile } from "node:fs/promises";
import { createHash } from "node:crypto";

const args = process.argv.slice(2);
function arg(name) {
  const i = args.indexOf(`--${name}`);
  if (i < 0) return undefined;
  const v = args[i + 1];
  return v && !v.startsWith("--") ? v : true;
}

async function main() {
  const url = arg("url");
  const file = arg("file");
  const contentType = arg("content-type") || arg("ct");
  if (typeof url !== "string" || typeof file !== "string") {
    process.stderr.write("Usage: node aacp-upload.mjs --url '<presigned>' --file <path> --content-type <mime>\n");
    process.exit(2);
  }
  const buf = await readFile(file);
  const sha256 = "0x" + createHash("sha256").update(buf).digest("hex");
  const headers = {};
  if (typeof contentType === "string") headers["content-type"] = contentType;
  const res = await fetch(url, { method: "PUT", headers, body: buf });
  const text = await res.text().catch(() => "");
  if (!res.ok) {
    process.stderr.write(`PUT failed → HTTP ${res.status}\n`);
    console.log(JSON.stringify({ ok: false, status: res.status, body: text.slice(0, 300) }, null, 2));
    process.exit(1);
  }
  console.log(JSON.stringify({
    ok: true,
    status: res.status,
    etag: res.headers.get("etag"),
    sizeBytes: buf.length,
    sha256,
  }, null, 2));
}

main().catch((err) => {
  process.stderr.write(`error: ${err.message}\n`);
  process.exit(1);
});
