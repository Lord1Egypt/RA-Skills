import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import plugin from "../src/index.ts";

const root = resolve(import.meta.dirname, "..");

test("package manifest, OpenClaw manifest, and entry id agree", async () => {
  const packageJson = JSON.parse(await readFile(resolve(root, "package.json"), "utf8"));
  const manifest = JSON.parse(await readFile(resolve(root, "openclaw.plugin.json"), "utf8"));

  assert.equal(packageJson.type, "module");
  assert.deepEqual(packageJson.openclaw.extensions, ["./dist/index.js"]);
  assert.equal(manifest.id, "openclaw-action-gate");
  assert.equal(plugin.id, manifest.id);
  assert.equal(manifest.enabledByDefault, false);
  assert.equal(manifest.configSchema.properties.enabled.default, false);
  assert.equal(manifest.configSchema.properties.modeDefault.default, "observe");
  assert.equal(manifest.configSchema.properties.failClosedProtectedPublicSends.default, true);
});

test("source resolves definePluginEntry and registers required hooks", async () => {
  const source = await readFile(resolve(root, "src/index.ts"), "utf8");
  assert.match(source, /await import\("openclaw\/plugin-sdk\/plugin-entry"\)/);
  assert.match(source, /export default definePluginEntry\(/);
  assert.match(source, /api\.on\("before_dispatch", beforeDispatchHandler, \{ priority: 100 \}\);/);
  assert.match(source, /api\.on\("message_sending", messageSendingHandler, \{ priority: 100 \}\);/);
  assert.match(source, /api\.on\("message_sent", messageSentHandler, \{ priority: 100 \}\);/);
});

test("plugin register wires api.on hooks in priority order", () => {
  const calls = [];
  plugin.register({
    pluginConfig: {},
    rootDir: root,
    on(hookName, handler, options) {
      calls.push({ hookName, handlerName: handler.name, options });
    }
  });

  assert.deepEqual(calls, [
    { hookName: "before_dispatch", handlerName: "beforeDispatchHandler", options: { priority: 100 } },
    { hookName: "message_sending", handlerName: "messageSendingHandler", options: { priority: 100 } },
    { hookName: "message_sent", handlerName: "messageSentHandler", options: { priority: 100 } }
  ]);
});
