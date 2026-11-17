/** @jest-environment node */
// Tests for the media:upload CLI command / MCP tool's shared implementation
// (cli/src/media.ts): client-side validation, the single multipart POST, and
// error mapping. Mirrors the harness pattern in commands.test.ts.
//
// The upload went from two steps (POST for a signed ticket, then a raw PUT to
// Supabase) to one multipart POST in Phase 1 item 8 — R2 has no equivalent of a
// Supabase signed upload token. The client-side guards either side of it are
// unchanged, which is why those tests are untouched.
import { main } from "../index.js";
import type { Io } from "../index.js";
import type { HttpResponse } from "../http.js";
import { contentTypeForPath } from "../media.js";

const RL_HEADERS = {
  "X-RateLimit-Limit": "50",
  "X-RateLimit-Remaining": "49",
  "X-RateLimit-Reset": "1753000000",
};

function jsonRes(body: unknown, status = 200): HttpResponse {
  const lower: Record<string, string> = {};
  for (const [k, v] of Object.entries(RL_HEADERS)) lower[k.toLowerCase()] = v;
  return {
    status,
    headers: { get: (name: string) => lower[name.toLowerCase()] ?? null },
    text: async () => JSON.stringify(body),
  };
}

function textRes(status: number, text = ""): HttpResponse {
  return {
    status,
    headers: { get: () => null },
    text: async () => text,
  };
}

/** The 201 body POST /api/v1/media answers with for a multipart upload. */
const UPLOADED_DATA = {
  bucket: "tokei-media",
  path: "api-uploads/u1/uuid.png",
  public_url: "https://media.tokei.io/api-uploads/u1/uuid.png",
  content_type: "image/png",
  filename: "hero.PNG",
  size_bytes: 150,
  backend: "r2",
};

/**
 * Pull the single `file` part back out of a multipart body, so the tests assert
 * what the server will actually receive rather than a byte blob.
 */
function decodePart(
  contentTypeHeader: string,
  body: Uint8Array,
): { headers: string; bytes: Uint8Array } {
  const boundary = /boundary=(.+)$/.exec(contentTypeHeader)?.[1];
  if (!boundary) throw new Error(`no boundary in ${contentTypeHeader}`);

  const text = Buffer.from(body).toString("latin1");
  const headerEnd = text.indexOf("\r\n\r\n");
  const headers = text.slice(text.indexOf("\r\n") + 2, headerEnd);
  const bodyStart = headerEnd + 4;
  const bodyEnd = text.lastIndexOf(`\r\n--${boundary}--`);
  return { headers, bytes: body.slice(bodyStart, bodyEnd) };
}

interface JsonCall {
  url: string;
  init: { method: string; headers: Record<string, string>; body?: string };
}
interface UploadCall {
  url: string;
  init: { method: string; headers: Record<string, string>; body: Uint8Array };
}

interface Harness {
  io: Io;
  out: string[];
  err: string[];
  jsonCalls: JsonCall[];
  uploadCalls: UploadCall[];
}

function harness(
  opts: {
    env?: Record<string, string | undefined>;
    jsonResponse?: HttpResponse | Error;
    uploadResponse?: HttpResponse | Error;
    files?: Record<string, Uint8Array>;
    omitReadFileBytes?: boolean;
    omitBinaryFetch?: boolean;
  } = {},
): Harness {
  const out: string[] = [];
  const err: string[] = [];
  const jsonCalls: JsonCall[] = [];
  const uploadCalls: UploadCall[] = [];
  const jsonResponse = opts.jsonResponse ?? jsonRes({ success: true, data: UPLOADED_DATA }, 201);
  const uploadResponse =
    opts.uploadResponse ?? jsonRes({ success: true, data: UPLOADED_DATA }, 201);
  const files = opts.files ?? {};

  const base: Io = {
    env: opts.env ?? { TOKEI_API_KEY: "tokei_k_test" },
    fetchImpl: async (
      url: string,
      init: { method: string; headers: Record<string, string>; body?: string },
    ) => {
      jsonCalls.push({ url, init });
      if (jsonResponse instanceof Error) throw jsonResponse;
      return jsonResponse;
    },
    stdout: (line: string) => out.push(line),
    stderr: (line: string) => err.push(line),
  };
  if (!opts.omitBinaryFetch) {
    base.binaryFetchImpl = async (
      url: string,
      init: { method: string; headers: Record<string, string>; body: Uint8Array },
    ) => {
      uploadCalls.push({ url, init });
      if (uploadResponse instanceof Error) throw uploadResponse;
      return uploadResponse;
    };
  }
  if (!opts.omitReadFileBytes) {
    base.readFileBytes = (path: string) => {
      if (files[path]) return files[path];
      throw new Error(`ENOENT: no such file, open '${path}'`);
    };
  }
  return { io: base, out, err, jsonCalls, uploadCalls };
}

describe("contentTypeForPath", () => {
  it("infers the content type from a lowercased extension", () => {
    expect(contentTypeForPath("hero.PNG")).toBe("image/png");
    expect(contentTypeForPath("clip.jpeg")).toBe("image/jpeg");
    expect(contentTypeForPath("clip.mov")).toBe("video/quicktime");
  });

  it("returns undefined for an unsupported extension", () => {
    expect(contentTypeForPath("doc.svg")).toBeUndefined();
  });
});

describe("main — media:upload", () => {
  it("unknown extension -> usage error naming supported extensions, zero HTTP calls", async () => {
    const h = harness({ files: { "x.svg": new Uint8Array(200).fill(1) } });
    const code = await main(["media:upload", "x.svg"], h.io);
    expect(code).toBe(2);
    expect(h.out).toEqual([]);
    const errBody = JSON.parse(h.err[0]);
    expect(errBody.error.type).toBe("usage_error");
    expect(errBody.error.message).toMatch(/\.jpg/);
    expect(errBody.error.message).toMatch(/\.mp4/);
    expect(h.jsonCalls).toEqual([]);
    expect(h.uploadCalls).toEqual([]);
  });

  it("file over 4MB -> usage error mentioning 4MB, zero HTTP calls", async () => {
    const bytes = new Uint8Array(6 * 1024 * 1024);
    const h = harness({ files: { "big.png": bytes } });
    const code = await main(["media:upload", "big.png"], h.io);
    expect(code).toBe(2);
    expect(JSON.parse(h.err[0]).error.message).toMatch(/4MB/);
    expect(h.jsonCalls).toEqual([]);
    expect(h.uploadCalls).toEqual([]);
  });

  it("file under the 100 byte minimum -> usage error, zero HTTP calls", async () => {
    const bytes = new Uint8Array(50);
    const h = harness({ files: { "tiny.png": bytes } });
    const code = await main(["media:upload", "tiny.png"], h.io);
    expect(code).toBe(2);
    const errBody = JSON.parse(h.err[0]);
    expect(errBody.error.type).toBe("usage_error");
    expect(h.jsonCalls).toEqual([]);
    expect(h.uploadCalls).toEqual([]);
  });

  it("happy path: ONE multipart POST carrying the file part, success envelope", async () => {
    const bytes = new Uint8Array(150).fill(7);
    const h = harness({ files: { "photos/hero.PNG": bytes } });
    const code = await main(["media:upload", "photos/hero.PNG"], h.io);
    expect(code).toBe(0);

    // No JSON call at all — the ticket round-trip is gone.
    expect(h.jsonCalls).toEqual([]);
    expect(h.uploadCalls).toHaveLength(1);

    const call = h.uploadCalls[0];
    const url = new URL(call.url);
    expect(url.origin + url.pathname).toBe("https://tokei.io/api/v1/media");
    expect(call.init.method).toBe("POST");
    expect(call.init.headers.Authorization).toBe("Bearer tokei_k_test");
    expect(call.init.headers["Content-Type"]).toMatch(/^multipart\/form-data; boundary=.+/);

    const part = decodePart(call.init.headers["Content-Type"], call.init.body);
    expect(part.headers).toContain('name="file"');
    expect(part.headers).toContain('filename="hero.PNG"');
    expect(part.headers).toContain("Content-Type: image/png");
    expect(part.bytes).toEqual(bytes);

    const stdout = JSON.parse(h.out[0]);
    expect(stdout.success).toBe(true);
    expect(stdout.data.public_url).toBe(UPLOADED_DATA.public_url);
    expect(stdout.data.path).toBe(UPLOADED_DATA.path);
    expect(stdout.data.size_bytes).toBe(150);
    expect(stdout.rate_limit).toEqual({ limit: 50, remaining: 49, reset: 1753000000 });
  });

  it("422 from the API -> exit 1, the API's own envelope printed", async () => {
    const errBody = {
      success: false,
      error: { code: "VALIDATION_ERROR", message: "Request body failed validation.", status: 422 },
    };
    const h = harness({
      files: { "hero.png": new Uint8Array(150).fill(1) },
      uploadResponse: jsonRes(errBody, 422),
    });
    const code = await main(["media:upload", "hero.png"], h.io);
    expect(code).toBe(1);
    const stdout = JSON.parse(h.out[0]);
    expect(stdout.error.code).toBe("VALIDATION_ERROR");
  });

  it("413 from the API -> exit 1, reported like any other API error", async () => {
    const errBody = {
      success: false,
      error: { code: "PAYLOAD_TOO_LARGE", message: "File exceeds the 4MB limit.", status: 413 },
    };
    const h = harness({
      files: { "hero.png": new Uint8Array(150).fill(1) },
      uploadResponse: jsonRes(errBody, 413),
    });
    const code = await main(["media:upload", "hero.png"], h.io);
    expect(code).toBe(1);
    const stdout = JSON.parse(h.out[0]);
    expect(stdout.error.code).toBe("PAYLOAD_TOO_LARGE");
    expect(stdout.error.message).toMatch(/4MB/);
  });

  it("a non-JSON error body still exits 1 with a readable envelope", async () => {
    const h = harness({
      files: { "hero.png": new Uint8Array(150).fill(1) },
      uploadResponse: textRes(502, "<html>bad gateway</html>"),
    });
    const code = await main(["media:upload", "hero.png"], h.io);
    expect(code).toBe(1);
    const stdout = JSON.parse(h.out[0]);
    expect(stdout.ok).toBe(false);
    expect(stdout.error.type).toBe("http_error");
    expect(stdout.error.status).toBe(502);
  });

  it("--content-type overrides extension inference", async () => {
    const h = harness({ files: { "clip.dat": new Uint8Array(150).fill(2) } });
    const code = await main(["media:upload", "clip.dat", "--content-type", "video/mp4"], h.io);
    expect(code).toBe(0);
    const call = h.uploadCalls[0];
    const part = decodePart(call.init.headers["Content-Type"], call.init.body);
    expect(part.headers).toContain("Content-Type: video/mp4");
  });

  it("Io without readFileBytes -> usage error, 'not supported in this environment', zero HTTP calls", async () => {
    const h = harness({ omitReadFileBytes: true, files: { "hero.png": new Uint8Array(150).fill(1) } });
    const code = await main(["media:upload", "hero.png"], h.io);
    expect(code).toBe(2);
    expect(JSON.parse(h.err[0]).error.message).toMatch(/not supported in this environment/);
    expect(h.jsonCalls).toEqual([]);
    expect(h.uploadCalls).toEqual([]);
  });

  it("Io without binaryFetchImpl -> usage error, 'not supported in this environment', zero HTTP calls", async () => {
    const h = harness({ omitBinaryFetch: true, files: { "hero.png": new Uint8Array(150).fill(1) } });
    const code = await main(["media:upload", "hero.png"], h.io);
    expect(code).toBe(2);
    expect(JSON.parse(h.err[0]).error.message).toMatch(/not supported in this environment/);
    expect(h.jsonCalls).toEqual([]);
    expect(h.uploadCalls).toEqual([]);
  });

  it("no <file> argument -> usage error, exit 2, zero HTTP calls", async () => {
    const h = harness();
    const code = await main(["media:upload"], h.io);
    expect(code).toBe(2);
    expect(JSON.parse(h.err[0]).error.type).toBe("usage_error");
    expect(h.jsonCalls).toEqual([]);
    expect(h.uploadCalls).toEqual([]);
  });
});
