#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { createInterface } from "node:readline";
import { main } from "../dist/index.js";

// Track the readline interface so it can be torn down explicitly — a live
// stdin handle would otherwise keep the process alive after main() resolves.
let rl = null;

main(process.argv.slice(2), {
  env: process.env,
  fetchImpl: fetch,
  stdout: (line) => process.stdout.write(line + "\n"),
  stderr: (line) => process.stderr.write(line + "\n"),
  // Raw stream access for the interactive UI. src/ has no @types/node and
  // never touches `process`, so every environment fact is injected here.
  // isTTY is false for pipes, redirects and MCP, which is what keeps stdout
  // pure JSON everywhere except a real human terminal.
  term: {
    write: (chunk) => process.stdout.write(chunk),
    isTTY: Boolean(process.stdout.isTTY),
    columns: process.stdout.columns,
    env: process.env,
    platform: process.platform,
    onInterrupt: (handler) => {
      const onSig = () => {
        handler();
        process.removeListener("SIGINT", onSig);
        // Re-raise so the shell sees a normal Ctrl+C. Never process.exit():
        // see the teardown note in .finally below.
        process.kill(process.pid, "SIGINT");
      };
      process.on("SIGINT", onSig);
      return () => process.removeListener("SIGINT", onSig);
    },
  },
  readFile: (path) => readFileSync(path, "utf8"),
  // media:upload's file-bytes read and multipart POST. A Buffer IS a
  // Uint8Array, so readFileSync's return value satisfies readFileBytes as-is.
  readFileBytes: (path) => readFileSync(path),
  binaryFetchImpl: fetch,
  // Lazy: readline only attaches to stdin if the command iterates (mcp).
  stdin: {
    [Symbol.asyncIterator]: () => {
      rl = createInterface({ input: process.stdin, crlfDelay: Infinity });
      return rl[Symbol.asyncIterator]();
    },
  },
})
  .then((code) => {
    process.exitCode = code;
  })
  .catch((err) => {
    process.stderr.write(
      JSON.stringify({ ok: false, error: { type: "internal_error", message: String(err) } }) + "\n",
    );
    process.exitCode = 1;
  })
  .finally(() => {
    // Never call process.exit(): on Node 24 / Windows it aborts libuv teardown
    // mid-close (Assertion failed: !(handle->flags & UV_HANDLE_CLOSING),
    // src\win\async.c) and corrupts the exit code. Setting exitCode and letting
    // the loop drain exits cleanly with the same code — and guarantees stdout
    // is flushed. Close stdin explicitly if mcp attached it, so it cannot hold
    // the loop open.
    if (rl) {
      rl.close();
      if (typeof process.stdin.unref === "function") process.stdin.unref();
    }
    // Belt-and-braces cursor restore: the UI restores it on every path of its
    // own, but an unexpected throw must never leave a TTY with a hidden cursor.
    if (process.stdout.isTTY) process.stdout.write("\x1b[?25h");
    // Backstop for a stray handle (e.g. a keep-alive socket) holding the loop
    // open: force the recorded code after a grace period. unref() so the timer
    // itself never keeps the process alive.
    setTimeout(() => process.exit(process.exitCode ?? 0), 2000).unref();
  });
