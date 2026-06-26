import fs from "node:fs";
import path from "node:path";
import process from "node:process";

export function isRecord(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

export function asTrimmedString(value) {
  if (value === undefined || value === null) {
    return undefined;
  }
  const text = String(value).trim();
  return text.length > 0 ? text : undefined;
}

export function parseTokenClaims(rawToken) {
  const token = asTrimmedString(rawToken);
  if (!token) {
    return undefined;
  }
  const parts = token.split(".");
  if (parts.length < 2) {
    return undefined;
  }
  try {
    const payload = Buffer.from(parts[1], "base64url").toString("utf8");
    const parsed = JSON.parse(payload);
    return isRecord(parsed) ? parsed : undefined;
  } catch {
    return undefined;
  }
}

export function extractTokenFromWsUrl(rawUrl) {
  const text = asTrimmedString(rawUrl);
  if (!text) {
    return undefined;
  }
  try {
    const parsed = new URL(text);
    return asTrimmedString(parsed.searchParams.get("x-clickzetta-token"));
  } catch {
    return undefined;
  }
}

/**
 * Write JSON to stdout and exit, waiting for the write to flush
 * so the caller always receives complete JSON.
 */
export function writeJsonAndExit(payload, code) {
  const data = `${JSON.stringify(payload)}\n`;
  if (process.stdout.write(data)) {
    process.exit(code);
  } else {
    process.stdout.once("drain", () => process.exit(code));
  }
}

/**
 * Atomically write a JSON file by writing to a temp file first,
 * then renaming. Prevents partial reads under concurrent access.
 */
export function atomicWriteJsonSync(filePath, data) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  const tmp = `${filePath}.${process.pid}.tmp`;
  try {
    fs.writeFileSync(tmp, `${JSON.stringify(data, null, 2)}\n`, "utf8");
    fs.renameSync(tmp, filePath);
  } catch (err) {
    try {
      fs.unlinkSync(tmp);
    } catch {
      // ignore cleanup failure
    }
    throw err;
  }
}
