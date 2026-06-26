import test from "node:test";
import assert from "node:assert/strict";

import {
  parseArgs,
  validateReadyConfig
} from "../scripts/check-ready.mjs";

test("parseArgs defaults to agent JSON output", () => {
  const args = parseArgs([]);

  assert.equal(args.envFile, ".env");
  assert.equal(args.format, "json");
});

test("validateReadyConfig passes with Baidu-only provider and OpenList target", async () => {
  const result = await validateReadyConfig(
    {
      BAIDU_COOKIE: "baidu-cookie",
      BAIDU_DEFAULT_SAVE_PATH: "/NAS资源下载",
      OPENLIST_TOKEN: "openlist-token",
      OPENLIST_BASE_URL: "http://openlist.test",
      OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
    },
    {
      fetchImpl: async (url) => {
        const text = String(url);
        if (text.includes("/xpan/nas")) return jsonResponse({ errno: 0, username: "tester" });
        if (text.includes("/xpan/file")) return jsonResponse({ errno: 0, list: [] });
        if (text.includes("/api/fs/list")) return jsonResponse({ code: 200, message: "success", data: { content: [] } });
        throw new Error(`Unexpected URL: ${text}`);
      }
    }
  );

  assert.equal(result.ok, true);
  assert.equal(result.nextAction, "ready");
  assert.deepEqual(result.validProviders, ["baidu"]);
  assert.equal(result.openList.ok, true);
  assert.equal(result.providerTargets[0].targetPath, "/NAS资源下载");
});

test("validateReadyConfig passes with Quark path target when it can be resolved", async () => {
  const result = await validateReadyConfig(
    {
      QUARK_COOKIE: "quark-cookie",
      QUARK_DEFAULT_SAVE_URL: "/备份资源",
      OPENLIST_TOKEN: "openlist-token",
      OPENLIST_BASE_URL: "http://openlist.test",
      OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
    },
    {
      fetchImpl: async (url) => {
        const text = String(url);
        if (text.includes("drive-pc.quark.cn") && text.includes("pdir_fid=0")) {
          return jsonResponse({ code: 0, data: { list: [{ fid: "backup-fid", file_name: "备份资源", dir: true }] } });
        }
        if (text.includes("/api/fs/list")) return jsonResponse({ code: 200, message: "success", data: { content: [] } });
        throw new Error(`Unexpected URL: ${text}`);
      }
    }
  );

  assert.equal(result.ok, true);
  assert.deepEqual(result.validProviders, ["quark"]);
  assert.equal(result.providerTargets[0].fid, "backup-fid");
});

test("validateReadyConfig fails when no provider is complete", async () => {
  const result = await validateReadyConfig(
    {
      OPENLIST_TOKEN: "openlist-token",
      OPENLIST_BASE_URL: "http://openlist.test",
      OPENLIST_DEFAULT_COPY_DST_PATH: "/影视资源备份/影视"
    },
    {
      fetchImpl: async () => jsonResponse({ code: 200, message: "success", data: { content: [] } })
    }
  );

  assert.equal(result.ok, false);
  assert.equal(result.nextAction, "configure_provider");
  assert.match(result.recommendations.join("\n"), /至少配置一个完整网盘/);
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
