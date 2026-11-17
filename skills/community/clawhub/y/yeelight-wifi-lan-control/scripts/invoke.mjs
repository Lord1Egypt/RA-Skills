#!/usr/bin/env node

import { handleRequest } from "./lib/runtime.mjs";
import { response } from "./lib/response.mjs";

export const MAX_INPUT_BYTES = 1024 * 1024;

export async function readSingleRequest(stream = process.stdin, maxBytes = MAX_INPUT_BYTES) {
  const chunks = [];
  let length = 0;
  for await (const chunk of stream) {
    const value = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    length += value.length;
    if (length > maxBytes) {
      const error = new Error("Request exceeds the 1 MiB input limit.");
      error.code = "input_too_large";
      throw error;
    }
    chunks.push(value);
  }
  const bytes = Buffer.concat(chunks);
  if (!bytes.length) {
    const error = new Error("A single JSON object is required on stdin.");
    error.code = "input_empty";
    throw error;
  }
  for (const byte of bytes) {
    if (byte === 0 || byte < 0x09 && byte !== 0x0a && byte !== 0x0d) {
      const error = new Error("Control characters are not allowed in the request framing.");
      error.code = "input_framing_invalid";
      throw error;
    }
  }
  let text;
  try {
    text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch {
    const error = new Error("Request stdin must be valid UTF-8.");
    error.code = "input_encoding_invalid";
    throw error;
  }
  let parsed;
  try { parsed = JSON.parse(text); } catch {
    const error = new Error("Request must contain exactly one valid JSON document.");
    error.code = "input_json_invalid";
    throw error;
  }
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    const error = new Error("The top-level request must be one JSON object.");
    error.code = "input_shape_invalid";
    throw error;
  }
  return parsed;
}

export async function main({ stdin = process.stdin, stdout = process.stdout, runtime = {} } = {}) {
  try {
    const request = await readSingleRequest(stdin);
    const result = await handleRequest(request, runtime);
    stdout.write(`${JSON.stringify(result)}\n`);
    return result;
  } catch (error) {
    const result = response({ operation: "", status: "error", error });
    stdout.write(`${JSON.stringify(result)}\n`);
    return result;
  }
}

if (import.meta.url === `file://${process.argv[1]}`) await main();
