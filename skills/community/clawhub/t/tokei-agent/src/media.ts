// media:upload — shared upload used by BOTH the CLI command and the MCP
// media_upload tool. ONE request: POST /api/v1/media as multipart/form-data
// with a `file` part; the server stores the bytes and answers 201 with the
// object.
//
// This replaced a two-step signed-ticket flow (POST for a ticket, then a raw
// PUT to Supabase) in Phase 1 item 8. R2 has no RLS and therefore no equivalent
// of a Supabase signed upload token, so the ticket shape cannot survive the
// migration. The server accepts multipart whether or not R2 is switched on, so
// this client works against both — it is not coupled to the cutover.
//
// Deliberately imports from NEITHER index.ts NOR mcp.ts (only from http.ts,
// which imports nothing) — index.ts and mcp.ts already have a lazy import
// cycle between them (mcp.ts imports Io/VERSION from index.ts; index.ts
// imports createMcpSession from mcp.ts), and this module is imported by both,
// so it must not deepen that cycle.
import { requestMultipart } from "./http.js";
import type { BinaryFetchLike } from "./http.js";

/**
 * Client-side mirror of CONTENT_TYPE_TO_EXT in src/features/public-api/model/media-upload.ts
 * (server), inverted (extension -> content type) and lowercased for lookup.
 * The CLI cannot import app code (separate package, separate build target),
 * so this is duplicated by necessity — keep the two in sync by hand if the
 * server's MEDIA_CONTENT_TYPES allowlist ever changes. Server side is the
 * source of truth; this only labels the part before sending, and the server
 * validates the bytes for real.
 */
export const EXT_TO_CONTENT_TYPE: Record<string, string> = {
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".mp4": "video/mp4",
  ".webm": "video/webm",
  ".mov": "video/quicktime",
};

const SUPPORTED_EXTENSIONS = Object.keys(EXT_TO_CONTENT_TYPE).join(", ");

/** Matches MEDIA_MAX_BYTES / the file-utils min-size check (src/features/media/model/file-utils.ts) server-side. */
export const MEDIA_MAX_BYTES = 4 * 1024 * 1024;
export const MEDIA_MIN_BYTES = 100;

export function contentTypeForPath(path: string): string | undefined {
  const dot = path.lastIndexOf(".");
  if (dot === -1) return undefined;
  const ext = path.slice(dot).toLowerCase();
  return EXT_TO_CONTENT_TYPE[ext];
}

/** Last path segment, forward- or back-slash — never node:path, to keep cli/src runtime-agnostic. */
function basename(filePath: string): string {
  const normalized = filePath.replace(/\\/g, "/");
  const idx = normalized.lastIndexOf("/");
  return idx === -1 ? normalized : normalized.slice(idx + 1);
}

export interface UploadMediaArgs {
  filePath: string;
  contentTypeOverride?: string;
  apiKey: string;
  baseUrl: string;
  // Optional so embedders without a filesystem / binary fetch can omit them
  // (the upload then reports a usage error) — same idiom as Io.readFile.
  binaryFetchImpl?: BinaryFetchLike;
  readFileBytes?: (path: string) => Uint8Array;
}

export type UploadMediaOutcome =
  | { kind: "usage_error"; message: string }
  | { kind: "result"; exitCode: 0 | 1; payload: unknown };

export async function uploadMedia(args: UploadMediaArgs): Promise<UploadMediaOutcome> {
  const {
    filePath,
    contentTypeOverride,
    apiKey,
    baseUrl,
    binaryFetchImpl,
    readFileBytes,
  } = args;

  const contentType = contentTypeOverride ?? contentTypeForPath(filePath);
  if (!contentType) {
    return {
      kind: "usage_error",
      message: `Cannot infer a content type for "${filePath}". Supported extensions: ${SUPPORTED_EXTENSIONS} (or pass --content-type).`,
    };
  }

  if (!readFileBytes || !binaryFetchImpl) {
    return {
      kind: "usage_error",
      message: "media:upload is not supported in this environment (no file system / network access).",
    };
  }

  let bytes: Uint8Array;
  try {
    bytes = readFileBytes(filePath);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    return { kind: "usage_error", message: `Could not read ${filePath}: ${message}` };
  }

  if (bytes.length > MEDIA_MAX_BYTES) {
    return {
      kind: "usage_error",
      message: `${filePath} is ${bytes.length} bytes, over the 4MB (${MEDIA_MAX_BYTES} byte) upload limit — this applies to video as well as images.`,
    };
  }
  if (bytes.length < MEDIA_MIN_BYTES) {
    return {
      kind: "usage_error",
      message: `${filePath} is ${bytes.length} bytes, below the ${MEDIA_MIN_BYTES} byte minimum (possibly empty or corrupt).`,
    };
  }

  const result = await requestMultipart(
    {
      baseUrl,
      apiKey,
      path: "/media",
      filename: basename(filePath),
      contentType,
      bytes,
    },
    binaryFetchImpl,
  );

  // The 201 body already carries public_url / path / content_type / filename /
  // size_bytes, plus `backend` and `bucket`, and http.ts has attached
  // rate_limit — so it is passed through rather than rebuilt. On failure this
  // is the API's own error body, exactly as every other command reports one.
  return { kind: "result", exitCode: result.exitCode, payload: result.payload };
}
