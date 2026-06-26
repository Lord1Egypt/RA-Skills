import test from "node:test";
import assert from "node:assert/strict";

import {
  parseArgs,
  runOpenListCopy
} from "../scripts/openlist-copy.mjs";

test("parseArgs accepts source, destination, and object name positionals", () => {
  const args = parseArgs(["/pan/quark/备份资源", "/影视资源备份/影视", "绿皮书"]);

  assert.equal(args.srcDir, "/pan/quark/备份资源");
  assert.equal(args.dstDir, "/影视资源备份/影视");
  assert.deepEqual(args.names, ["绿皮书"]);
  assert.equal(args.format, "json");
  assert.equal(args.yes, false);
});

test("runOpenListCopy previews source and destination before mutation", async () => {
  let copyCalled = false;
  const result = await runOpenListCopy({
    env: {
      OPENLIST_BASE_URL: "http://openlist.test",
      OPENLIST_TOKEN: "token",
      OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
    },
    args: {
      srcDir: "/pan/quark/备份资源",
      names: ["绿皮书"],
      yes: false
    },
    fetchImpl: async (url, options) => {
      const text = String(url);
      if (text.endsWith("/api/fs/copy")) copyCalled = true;
      if (text.endsWith("/api/fs/list")) {
        const body = JSON.parse(options.body);
        if (body.path === "/pan/quark/备份资源") {
          return jsonResponse({
            code: 200,
            message: "success",
            data: { content: [{ name: "绿皮书", is_dir: true }] }
          });
        }
        if (body.path === "/影视资源备份/影视") {
          return jsonResponse({
            code: 200,
            message: "success",
            data: { content: [] }
          });
        }
      }
      throw new Error(`Unexpected request: ${text}`);
    }
  });

  assert.equal(copyCalled, false);
  assert.equal(result.ok, true);
  assert.equal(result.dryRun, true);
  assert.equal(result.nextAction, "confirm_before_copy");
  assert.deepEqual(result.copyPlan.names, ["绿皮书"]);
  assert.deepEqual(result.copyPlan.expectedPaths, ["/影视资源备份/影视/绿皮书"]);
});

test("runOpenListCopy verifies success through done task and refreshed target", async () => {
  const calls = [];
  const result = await runOpenListCopy({
    env: {
      OPENLIST_BASE_URL: "http://openlist.test",
      OPENLIST_TOKEN: "token",
      OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
    },
    args: {
      srcDir: "/pan/quark/备份资源",
      names: ["绿皮书"],
      yes: true,
      pollTimeoutMs: 100,
      intervalMs: 1
    },
    fetchImpl: async (url, options) => {
      const text = String(url);
      calls.push(text);
      if (text.endsWith("/api/fs/list")) {
        const body = JSON.parse(options.body);
        if (body.path === "/pan/quark/备份资源") {
          return jsonResponse({
            code: 200,
            message: "success",
            data: { content: [{ name: "绿皮书", is_dir: true }] }
          });
        }
        if (body.path === "/影视资源备份/影视") {
          const copied = calls.includes("http://openlist.test/api/task/copy/done");
          return jsonResponse({
            code: 200,
            message: "success",
            data: { content: copied ? [{ name: "绿皮书", is_dir: true }] : [] }
          });
        }
      }
      if (text.endsWith("/api/fs/copy")) {
        assert.deepEqual(JSON.parse(options.body), {
          src_dir: "/pan/quark/备份资源",
          dst_dir: "/影视资源备份/影视",
          names: ["绿皮书"]
        });
        return jsonResponse({
          code: 200,
          message: "success",
          data: {
            task: { id: "copy-1", name: "copy 绿皮书", state: 0, progress: 0 }
          }
        });
      }
      if (text.endsWith("/api/task/copy/undone")) {
        return jsonResponse({ code: 200, message: "success", data: [] });
      }
      if (text.endsWith("/api/task/copy/done")) {
        return jsonResponse({
          code: 200,
          message: "success",
          data: [{ id: "copy-1", name: "copy 绿皮书", progress: 100, error: "" }]
        });
      }
      throw new Error(`Unexpected request: ${text}`);
    }
  });

  assert.equal(result.ok, true);
  assert.equal(result.dryRun, false);
  assert.equal(result.nextAction, "copy_complete");
  assert.equal(result.copyTask.id, "copy-1");
  assert.equal(result.verification.targetFound, true);
});

test("runOpenListCopy asks for confirmation when target already exists", async () => {
  const result = await runOpenListCopy({
    env: {
      OPENLIST_BASE_URL: "http://openlist.test",
      OPENLIST_TOKEN: "token",
      OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
    },
    args: {
      srcDir: "/pan/quark/备份资源",
      names: ["绿皮书"],
      yes: false
    },
    fetchImpl: async (url, options) => {
      const text = String(url);
      if (text.endsWith("/api/fs/list")) {
        const body = JSON.parse(options.body);
        if (body.path === "/pan/quark/备份资源") {
          return jsonResponse({
            code: 200,
            message: "success",
            data: { content: [{ name: "绿皮书", is_dir: true }] }
          });
        }
        if (body.path === "/影视资源备份/影视") {
          return jsonResponse({
            code: 200,
            message: "success",
            data: { content: [{ name: "绿皮书", is_dir: true }] }
          });
        }
      }
      throw new Error(`Unexpected request: ${text}`);
    }
  });

  assert.equal(result.ok, true);
  assert.equal(result.nextAction, "confirm_copy_over_existing");
  assert.deepEqual(result.destination.existingTargetNames, ["绿皮书"]);
});

test("runOpenListCopy reports source mismatch before copy", async () => {
  const result = await runOpenListCopy({
    env: { OPENLIST_BASE_URL: "http://openlist.test", OPENLIST_TOKEN: "token" },
    args: {
      srcDir: "/pan/quark/备份资源",
      dstDir: "/影视资源备份/影视",
      names: ["不存在的资源"],
      yes: true
    },
    fetchImpl: async (url, options) => {
      const text = String(url);
      if (text.endsWith("/api/fs/list")) {
        const body = JSON.parse(options.body);
        if (body.path === "/pan/quark/备份资源") {
          return jsonResponse({
            code: 200,
            message: "success",
            data: { content: [{ name: "绿皮书", is_dir: true }] }
          });
        }
        if (body.path === "/影视资源备份/影视") {
          return jsonResponse({ code: 200, message: "success", data: { content: [] } });
        }
      }
      throw new Error(`Unexpected request: ${text}`);
    }
  });

  assert.equal(result.ok, false);
  assert.equal(result.nextAction, "fix_copy_source");
  assert.deepEqual(result.source.missingNames, ["不存在的资源"]);
});

function jsonResponse(body, options = {}) {
  return {
    ok: options.ok ?? true,
    status: options.status ?? 200,
    async text() {
      return JSON.stringify(body);
    }
  };
}
