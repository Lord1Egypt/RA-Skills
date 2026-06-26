import test from "node:test";
import assert from "node:assert/strict";

import {
  filterTasks,
  parseArgs,
  runOpenListTasks
} from "../scripts/openlist-tasks.mjs";

test("parseArgs defaults to listing undone copy tasks as JSON", () => {
  const args = parseArgs([]);

  assert.equal(args.action, "list");
  assert.equal(args.group, "copy");
  assert.equal(args.state, "undone");
  assert.equal(args.format, "json");
});

test("filterTasks can select Baidu copy tasks", () => {
  const tasks = [
    { id: "a", name: "copy [/bdy](/NAS资源下载/A.mp4) to [/影视资源备份](/影视/A)" },
    { id: "b", name: "copy [/pan/quark](/备份资源/B.mkv) to [/影视资源备份](/影视/B)" }
  ];

  assert.deepEqual(filterTasks(tasks, { provider: "baidu" }).map((task) => task.id), ["a"]);
  assert.deepEqual(filterTasks(tasks, { provider: "quark" }).map((task) => task.id), ["b"]);
});

test("runOpenListTasks lists tasks with injected fetch", async () => {
  const result = await runOpenListTasks({
    env: { OPENLIST_BASE_URL: "http://openlist.test", OPENLIST_TOKEN: "token" },
    args: { action: "list", group: "copy", state: "undone" },
    fetchImpl: async (url) => {
      assert.equal(String(url), "http://openlist.test/api/task/copy/undone");
      return jsonResponse({
        code: 200,
        message: "success",
        data: [{ id: "task-1", name: "copy A", state: 1, progress: 50 }]
      });
    }
  });

  assert.equal(result.ok, true);
  assert.equal(result.nextAction, "report_tasks");
  assert.equal(result.tasks[0].id, "task-1");
});

test("runOpenListTasks previews cancel without yes", async () => {
  let cancelCalled = false;
  const result = await runOpenListTasks({
    env: { OPENLIST_BASE_URL: "http://openlist.test", OPENLIST_TOKEN: "token" },
    args: { action: "cancel", group: "copy", state: "undone", provider: "baidu", yes: false },
    fetchImpl: async (url) => {
      const text = String(url);
      if (text.endsWith("/api/task/copy/undone")) {
        return jsonResponse({
          code: 200,
          message: "success",
          data: [
            { id: "baidu-task", name: "copy [/bdy](/NAS资源下载/A.mp4) to [/影视资源备份](/影视/A)" }
          ]
        });
      }
      if (text.includes("/cancel")) cancelCalled = true;
      return jsonResponse({ code: 200, message: "success", data: null });
    }
  });

  assert.equal(cancelCalled, false);
  assert.equal(result.ok, true);
  assert.equal(result.dryRun, true);
  assert.equal(result.nextAction, "confirm_task_cancel");
  assert.deepEqual(result.matchedIds, ["baidu-task"]);
});

test("runOpenListTasks cancels matched tasks with yes", async () => {
  const calledUrls = [];
  const result = await runOpenListTasks({
    env: { OPENLIST_BASE_URL: "http://openlist.test", OPENLIST_TOKEN: "token" },
    args: { action: "cancel", group: "copy", state: "undone", provider: "baidu", yes: true },
    fetchImpl: async (url) => {
      const text = String(url);
      calledUrls.push(text);
      if (text.endsWith("/api/task/copy/undone")) {
        return jsonResponse({
          code: 200,
          message: "success",
          data: [
            { id: "baidu-task", name: "copy [/bdy](/NAS资源下载/A.mp4) to [/影视资源备份](/影视/A)" }
          ]
        });
      }
      assert.equal(text, "http://openlist.test/api/task/copy/cancel_some");
      return jsonResponse({ code: 200, message: "success", data: {} });
    }
  });

  assert.equal(result.ok, true);
  assert.equal(result.dryRun, false);
  assert.equal(result.nextAction, "verify_tasks_cancelled");
  assert.deepEqual(result.cancelledIds, ["baidu-task"]);
  assert.equal(calledUrls.length, 2);
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
