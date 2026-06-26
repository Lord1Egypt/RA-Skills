#!/usr/bin/env node
/**
 * GET /v1/upload/url — body 必填 content_type（MIME），与 socialEchoApidocs_cn.md §5.5 一致。
 */
import {
  buildRequestOptions,
  callJsonGet,
  parseArgs,
  printAndExit
} from "./client.js";

export const CONTENT_TYPE_ENUM = [
  "image/jpeg",
  "image/jpg",
  "image/png",
  "image/gif",
  "image/webp",
  "image/bmp",
  "video/mp4",
  "video/avi",
  "video/mov",
  "video/wmv",
  "video/flv",
  "video/webm",
  "video/mkv",
  "video/3gp",
  "video/quicktime"
];

const args = parseArgs(process.argv);

const contentType = String(
  args["content-type"] || args.content_type || ""
).trim();
if (!contentType) {
  console.error(
    "Usage: ./upload-url.js --api-key <key> --content-type <mime> [--base-url ...] [--team-id ...] [--lang zh_CN]\n" +
      "mime must be one of: " +
      CONTENT_TYPE_ENUM.join(", ")
  );
  process.exit(2);
}

if (!CONTENT_TYPE_ENUM.includes(contentType)) {
  console.error("Invalid --content-type. Allowed values:\n" + CONTENT_TYPE_ENUM.join("\n"));
  process.exit(2);
}

const options = buildRequestOptions(args);
const result = await callJsonGet(
  "/v1/upload/url",
  { content_type: contentType },
  options
);
printAndExit(result);
