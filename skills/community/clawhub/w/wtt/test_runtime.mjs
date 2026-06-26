import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";

import { createWTTCommandRouter } from "./dist/commands/router.js";
import { createProgressHeartbeatScheduler } from "./dist/runtime/progress-ticker.js";
import { createTaskRunExecutorLoop } from "./dist/runtime/task-executor.js";
import { createTaskStatusEventHandler } from "./dist/runtime/task-status-handler.js";
import { validateTaskTransition } from "./dist/runtime/status-transition.js";

function createFetchResponse({ ok, status, body = {}, contentType = "application/json" }) {
  return {
    ok,
    status,
    headers: {
      get(name) {
        if (name.toLowerCase() === "content-type") return contentType;
        return null;
      },
    },
    async json() {
      return body;
    },
    async text() {
      return typeof body === "string" ? body : JSON.stringify(body);
    },
  };
}

function createDeferred() {
  let resolve;
  const promise = new Promise((r) => {
    resolve = r;
  });
  return { promise, resolve };
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitFor(check, timeoutMs = 3000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    if (await check()) return;
    await sleep(10);
  }
  throw new Error("waitFor timeout");
}

function runtimeMetadata(taskId, status = "todo") {
  return {
    id: taskId,
    title: `task:${taskId}`,
    status,
    priority: "P1",
    ownerAgentId: "agent-owner",
    runnerAgentId: "agent-runner",
    pipelineId: "pipe-main",
    topicId: "topic-main",
    description: `desc:${taskId}`,
    taskType: "analysis",
    execMode: "sync",
  };
}

function invokeInferenceMock(outputText = "STEP: done\nMID: done\nCHANGE: done") {
  return async () => ({
    outputText,
    provider: "mock-runtime",
  });
}

function assertExecutionResult(result) {
  assert.equal(result.deduplicated, false);
  return result;
}

async function testTransitionGuardCompatibility() {
  const runFromReady = validateTaskTransition({
    currentStatus: "ready",
    intent: { kind: "run" },
  });
  assert.equal(runFromReady.allowed, true);
  assert.equal(runFromReady.toStatus, "doing");

  const reviewApproveFromDoing = validateTaskTransition({
    currentStatus: "doing",
    intent: { kind: "review", action: "approve" },
  });
  assert.equal(reviewApproveFromDoing.allowed, true);
  assert.equal(reviewApproveFromDoing.toStatus, "done");
}

async function testQueueEnqueueDequeueFlow() {
  const executor = createTaskRunExecutorLoop();
  const firstGate = createDeferred();
  const apiOrder = [];

  const first = executor.enqueueRun({
    taskId: "task-a",
    metadata: runtimeMetadata("task-a", "todo"),
    accountId: "default",
    apiRequest: async (request) => {
      apiOrder.push(`a:${request.path}`);
      await firstGate.promise;
      return { ok: true };
    },
    invokeTaskInference: invokeInferenceMock("output-a"),
  });

  await Promise.resolve();
  assert.equal(executor.isProcessing(), true);

  const second = executor.enqueueRun({
    taskId: "task-b",
    metadata: runtimeMetadata("task-b", "todo"),
    accountId: "default",
    apiRequest: async (request) => {
      apiOrder.push(`b:${request.path}`);
      return { ok: true };
    },
    invokeTaskInference: invokeInferenceMock("output-b"),
  });

  await waitFor(() => executor.getQueueDepth() === 1);
  firstGate.resolve();

  const [firstRaw, secondRaw] = await Promise.all([first, second]);
  const firstResult = assertExecutionResult(firstRaw);
  const secondResult = assertExecutionResult(secondRaw);
  assert.equal(firstResult.transitionApplied, "run_endpoint");
  assert.equal(secondResult.transitionApplied, "run_endpoint");
  assert.equal(firstResult.finalStatus, "review");
  assert.equal(secondResult.finalStatus, "review");
  assert.deepEqual(apiOrder, [
    "a:/tasks/task-a/run",
    "a:/tasks/task-a",
    "a:/tasks/task-a",
    "b:/tasks/task-b/run",
    "b:/tasks/task-b",
    "b:/tasks/task-b",
  ]);
  assert.equal(executor.getQueueDepth(), 0);

  await executor.stopGracefully();
}

async function testHeartbeatSchedulingPayloadGeneration() {
  const emitted = [];
  let intervalHandler;

  const scheduler = createProgressHeartbeatScheduler({
    taskId: "task-hb",
    status: "doing",
    action: "执行中",
    heartbeatSeconds: 60,
    now: () => new Date("2026-03-20T12:00:00.000Z"),
    publish: async (payload) => {
      emitted.push(payload);
    },
    setIntervalFn: (handler) => {
      intervalHandler = handler;
      return 1;
    },
    clearIntervalFn: () => {},
  });

  await scheduler.emitNow();
  scheduler.start();
  assert.equal(typeof intervalHandler, "function");

  intervalHandler();
  await Promise.resolve();
  scheduler.stop();

  const payloads = scheduler.getGeneratedPayloads();
  assert.equal(payloads.length, 2);
  assert.equal(payloads[0].heartbeatSeconds, 60);
  assert.ok(payloads[1].text.includes("状态=doing"));
  assert.equal(emitted.length, 2);
}

async function testPersistenceReloadQueue() {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "wtt-runtime-persist-"));
  const queueFile = path.join(tempDir, "queue.json");

  try {
    const firstGate = createDeferred();
    const executor = createTaskRunExecutorLoop({
      persistence: {
        enabled: true,
        filePath: queueFile,
      },
    });

    const first = executor.enqueueRun({
      taskId: "task-persist-a",
      metadata: runtimeMetadata("task-persist-a", "todo"),
      accountId: "default",
      apiContext: { cloudUrl: "https://example.com", token: "tok_x" },
      apiRequest: async () => {
        await firstGate.promise;
        return { ok: true };
      },
      invokeTaskInference: invokeInferenceMock("persist-a"),
    });

    const second = executor.enqueueRun({
      taskId: "task-persist-b",
      metadata: runtimeMetadata("task-persist-b", "todo"),
      accountId: "default",
      apiContext: { cloudUrl: "https://example.com", token: "tok_x" },
      apiRequest: async () => ({ ok: true }),
      invokeTaskInference: invokeInferenceMock("persist-b"),
    });

    void second.catch(() => {});

    await waitFor(() => {
      const snap = executor.getSnapshot();
      return snap.runningTaskId === "task-persist-a" && snap.queueLength === 1;
    });

    const stopPromise = executor.stopGracefully();
    firstGate.resolve();
    await Promise.all([first, stopPromise]);

    const persisted = JSON.parse(await readFile(queueFile, "utf8"));
    assert.equal(persisted.queued.length, 1);
    assert.equal(persisted.queued[0].intent.taskId, "task-persist-b");
    assert.equal(persisted.running, undefined);

    const recoveredCalls = [];
    const recoveredResults = [];

    const reloaded = createTaskRunExecutorLoop({
      persistence: {
        enabled: true,
        filePath: queueFile,
      },
      createRecoveredApiRequest: (intent) => async (request) => {
        recoveredCalls.push(`${intent.taskId}:${request.path}`);
        return { ok: true };
      },
      onRecoveredExecutionResult: (result) => {
        recoveredResults.push(result);
      },
    });

    await waitFor(() => recoveredResults.length === 1);
    const recovered = assertExecutionResult(recoveredResults[0]);
    assert.equal(recovered.taskId, "task-persist-b");
    assert.equal(recovered.persistence.recoveredFrom, "queued");
    assert.ok(recoveredCalls.includes("task-persist-b:/tasks/task-persist-b/run"));

    await reloaded.stopGracefully();
  } finally {
    await rm(tempDir, { recursive: true, force: true });
  }
}

async function testRecoveryOfRunningItem() {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "wtt-runtime-recovery-"));
  const queueFile = path.join(tempDir, "queue.json");

  try {
    const seed = {
      version: 1,
      updatedAt: new Date().toISOString(),
      queued: [],
      running: {
        enqueuedAt: new Date().toISOString(),
        intent: {
          taskId: "task-recover-running",
          metadata: runtimeMetadata("task-recover-running", "doing"),
          accountId: "default",
          triggerAgentId: "agent-main",
          runnerAgentId: "agent-runner",
          note: "recovery test",
          heartbeatSeconds: 60,
          apiContext: { cloudUrl: "https://example.com", token: "tok_test" },
        },
      },
    };

    await writeFile(queueFile, `${JSON.stringify(seed, null, 2)}\n`, "utf8");

    const recoveredResults = [];

    const executor = createTaskRunExecutorLoop({
      persistence: {
        enabled: true,
        filePath: queueFile,
      },
      createRecoveredApiRequest: () => async () => ({ ok: true }),
      onRecoveredExecutionResult: (result) => {
        recoveredResults.push(result);
      },
    });

    await waitFor(() => recoveredResults.length === 1);

    const result = assertExecutionResult(recoveredResults[0]);
    assert.equal(result.persistence.recoveredFrom, "running");
    assert.ok(result.summary.notes.some((note) => note.includes("running 未完成")));
    assert.ok(result.heartbeatPayloads[0].text.includes("恢复模式重新入队"));
    assert.equal(result.recovery?.retryCount, 1);
    assert.equal(result.recovery?.maxRetryCount, 2);

    await executor.stopGracefully();
  } finally {
    await rm(tempDir, { recursive: true, force: true });
  }
}

async function testSnapshotStatusChangesThroughLifecycle() {
  const executor = createTaskRunExecutorLoop();
  const gate = createDeferred();

  const initial = executor.getStatus();
  assert.equal(initial.queueLength, 0);
  assert.equal(initial.runningTaskId, null);
  assert.equal(initial.dedupHits, 0);
  assert.equal(initial.recovery.retryAttempts, 0);

  const first = executor.enqueueRun({
    taskId: "task-snap-a",
    metadata: runtimeMetadata("task-snap-a", "todo"),
    accountId: "default",
    apiRequest: async () => {
      await gate.promise;
      return { ok: true };
    },
    invokeTaskInference: invokeInferenceMock("snap-a"),
  });

  await waitFor(() => executor.getSnapshot().runningTaskId === "task-snap-a");
  const running = executor.getSnapshot();
  assert.equal(running.queueLength, 0);
  assert.equal(running.runningTaskId, "task-snap-a");

  const second = executor.enqueueRun({
    taskId: "task-snap-b",
    metadata: runtimeMetadata("task-snap-b", "todo"),
    accountId: "default",
    apiRequest: async () => ({ ok: true }),
    invokeTaskInference: invokeInferenceMock("snap-b"),
  });

  await waitFor(() => executor.getSnapshot().queueLength === 1);
  const queued = executor.getSnapshot();
  assert.equal(queued.runningTaskId, "task-snap-a");
  assert.equal(queued.queueLength, 1);

  gate.resolve();
  await Promise.all([first, second]);

  await waitFor(() => {
    const snap = executor.getSnapshot();
    return snap.queueLength === 0 && snap.runningTaskId === null;
  });

  const done = executor.getSnapshot();
  assert.equal(done.lastError, null);

  await executor.stopGracefully();
}

async function testDuplicateEnqueueBlocked() {
  const executor = createTaskRunExecutorLoop();
  const gate = createDeferred();

  const first = executor.enqueueRun({
    taskId: "task-dedup",
    metadata: runtimeMetadata("task-dedup", "todo"),
    accountId: "default",
    apiRequest: async () => {
      await gate.promise;
      return { ok: true };
    },
    invokeTaskInference: invokeInferenceMock("dedup"),
  });

  await waitFor(() => executor.getSnapshot().runningTaskId === "task-dedup");

  const second = await executor.enqueueRun({
    taskId: "task-dedup",
    metadata: runtimeMetadata("task-dedup", "todo"),
    accountId: "default",
    apiRequest: async () => ({ ok: true }),
    invokeTaskInference: invokeInferenceMock("dedup-2"),
  });

  assert.equal(second.deduplicated, true);
  assert.equal(second.idempotency.decision, "deduplicated");
  assert.equal(second.idempotency.duplicateState, "running");

  const snap = executor.getSnapshot();
  assert.equal(snap.enqueueAccepted, 1);
  assert.equal(snap.dedupHits, 1);

  gate.resolve();
  const firstResult = assertExecutionResult(await first);
  assert.equal(firstResult.idempotency.decision, "enqueued");

  await executor.stopGracefully();
}

async function testRecoveryRetryCapSkipsRequeue() {
  const tempDir = await mkdtemp(path.join(os.tmpdir(), "wtt-runtime-retry-cap-"));
  const queueFile = path.join(tempDir, "queue.json");

  try {
    const seed = {
      version: 1,
      updatedAt: new Date().toISOString(),
      queued: [],
      running: {
        enqueuedAt: new Date().toISOString(),
        intent: {
          taskId: "task-retry-cap",
          metadata: runtimeMetadata("task-retry-cap", "doing"),
          accountId: "default",
          triggerAgentId: "agent-main",
          runnerAgentId: "agent-runner",
          note: "retry cap test",
          heartbeatSeconds: 60,
          apiContext: { cloudUrl: "https://example.com", token: "tok_test" },
          recovery: {
            retryCount: 2,
            maxRetryCount: 2,
          },
        },
      },
    };

    await writeFile(queueFile, `${JSON.stringify(seed, null, 2)}\n`, "utf8");

    let recoveredApiCalls = 0;
    const recoveredResults = [];
    const executor = createTaskRunExecutorLoop({
      persistence: {
        enabled: true,
        filePath: queueFile,
      },
      createRecoveredApiRequest: () => async () => {
        recoveredApiCalls += 1;
        return { ok: true };
      },
      onRecoveredExecutionResult: (result) => {
        recoveredResults.push(result);
      },
    });

    await waitFor(() => executor.getSnapshot().recovery.loadedRunning === 1);
    await sleep(50);

    const snap = executor.getSnapshot();
    assert.equal(snap.recovery.skippedByRetryCap, 1);
    assert.equal(snap.recovery.requeued, 0);
    assert.equal(recoveredApiCalls, 0);
    assert.equal(recoveredResults.length, 0);

    await executor.stopGracefully();

    const persisted = JSON.parse(await readFile(queueFile, "utf8"));
    assert.equal(Array.isArray(persisted.queued), true);
    assert.equal(persisted.queued.length, 0);
    assert.equal(persisted.running, undefined);
  } finally {
    await rm(tempDir, { recursive: true, force: true });
  }
}

async function testDrainLockPreventsParallelProcessing() {
  const executor = createTaskRunExecutorLoop();
  const firstStarted = createDeferred();

  let inflight = 0;
  let maxInflight = 0;

  const createRun = (taskId, shouldSignal) => executor.enqueueRun({
    taskId,
    metadata: runtimeMetadata(taskId, "todo"),
    accountId: "default",
    apiRequest: async () => {
      inflight += 1;
      maxInflight = Math.max(maxInflight, inflight);
      if (shouldSignal) firstStarted.resolve();
      await sleep(25);
      inflight -= 1;
      return { ok: true };
    },
    invokeTaskInference: invokeInferenceMock(taskId),
  });

  const runs = [];
  runs.push(createRun("task-lock-1", true));
  await firstStarted.promise;

  for (let i = 2; i <= 6; i += 1) {
    runs.push(createRun(`task-lock-${i}`, false));
  }

  const rawResults = await Promise.all(runs);
  rawResults.forEach((result) => {
    const execResult = assertExecutionResult(result);
    assert.equal(execResult.idempotency.decision, "enqueued");
  });

  assert.equal(maxInflight, 1);
  const snap = executor.getSnapshot();
  assert.ok(snap.drainLockContention >= 1);

  await executor.stopGracefully();
}

async function testStatusFlowTodoDoingReviewSuccess() {
  const executor = createTaskRunExecutorLoop();
  const statusWrites = [];

  const resultRaw = await executor.enqueueRun({
    taskId: "task-status-success",
    metadata: runtimeMetadata("task-status-success", "todo"),
    accountId: "default",
    apiRequest: async (request) => {
      if (request.method === "PATCH" && request.path === "/tasks/task-status-success") {
        statusWrites.push(request.body?.status);
      }
      return { ok: true };
    },
    fetchTaskDetail: async () => ({
      id: "task-status-success",
      title: "status-success",
      description: "verify status flow",
      topic_id: "topic-status",
      task_type: "analysis",
      exec_mode: "sync",
      status: "doing",
    }),
    invokeTaskInference: invokeInferenceMock("STEP\nMID\nCHANGE"),
  });

  const result = assertExecutionResult(resultRaw);
  assert.equal(result.finalStatus, "review");
  assert.equal(result.inference.succeeded, true);
  assert.equal(statusWrites.includes("review"), true);

  await executor.stopGracefully();
}

async function testStatusFlowFailureMarksBlocked() {
  const executor = createTaskRunExecutorLoop();
  const statusWrites = [];

  const resultRaw = await executor.enqueueRun({
    taskId: "task-status-failed",
    metadata: runtimeMetadata("task-status-failed", "todo"),
    accountId: "default",
    apiRequest: async (request) => {
      if (request.method === "PATCH" && request.path === "/tasks/task-status-failed") {
        statusWrites.push(request.body?.status);
      }
      return { ok: true };
    },
    fetchTaskDetail: async () => ({
      id: "task-status-failed",
      title: "status-failed",
      description: "verify blocked fallback",
      topic_id: "topic-status",
      task_type: "analysis",
      exec_mode: "sync",
      status: "doing",
    }),
    invokeTaskInference: async () => {
      throw new Error("mock inference crashed");
    },
  });

  const result = assertExecutionResult(resultRaw);
  assert.equal(result.inference.succeeded, false);
  assert.equal(result.finalStatus, "blocked");
  assert.equal(statusWrites.includes("blocked"), true);

  await executor.stopGracefully();
}

async function testReviewPatchRetryThenSuccess() {
  const executor = createTaskRunExecutorLoop({
    reviewPatchRetryDelaysMs: [0],
  });

  let reviewPatchAttempts = 0;
  const statusWrites = [];

  const resultRaw = await executor.enqueueRun({
    taskId: "task-review-retry-success",
    metadata: runtimeMetadata("task-review-retry-success", "todo"),
    accountId: "default",
    apiRequest: async (request) => {
      if (request.method === "PATCH" && request.path === "/tasks/task-review-retry-success") {
        const status = request.body?.status;
        statusWrites.push(status);

        if (status === "review") {
          reviewPatchAttempts += 1;
          if (reviewPatchAttempts === 1) {
            throw new Error("mock transient review patch error");
          }
        }
      }

      return { ok: true };
    },
    fetchTaskDetail: async () => ({
      id: "task-review-retry-success",
      title: "review retry success",
      description: "verify retry path",
      topic_id: "topic-status",
      task_type: "analysis",
      exec_mode: "sync",
      status: "doing",
    }),
    invokeTaskInference: invokeInferenceMock("STEP\nMID\nCHANGE"),
  });

  const result = assertExecutionResult(resultRaw);
  assert.equal(result.inference.succeeded, true);
  assert.equal(result.finalStatus, "review");
  assert.equal(reviewPatchAttempts, 2);
  assert.equal(statusWrites.includes("blocked"), false);
  assert.ok(result.summary.notes.some((note) => note.includes("review_status_patch attempt 1/2 failed")));
  assert.ok(result.summary.notes.some((note) => note.includes("review_status_patch attempt 2/2 succeeded")));

  await executor.stopGracefully();
}

async function testReviewPatchRetryExhaustedMarksBlocked() {
  const executor = createTaskRunExecutorLoop({
    reviewPatchRetryDelaysMs: [0, 0],
    compensatingReviewDelayMs: 60_000,
    compensatingReviewRetryDelaysMs: [0],
  });

  let reviewPatchAttempts = 0;
  let blockedPatchAttempts = 0;

  const resultRaw = await executor.enqueueRun({
    taskId: "task-review-retry-failed",
    metadata: runtimeMetadata("task-review-retry-failed", "todo"),
    accountId: "default",
    apiRequest: async (request) => {
      if (request.method === "PATCH" && request.path === "/tasks/task-review-retry-failed") {
        const status = request.body?.status;
        if (status === "review") {
          reviewPatchAttempts += 1;
          throw new Error("mock review patch still failing");
        }
        if (status === "blocked") {
          blockedPatchAttempts += 1;
        }
      }

      return { ok: true };
    },
    fetchTaskDetail: async () => ({
      id: "task-review-retry-failed",
      title: "review retry failed",
      description: "verify watchdog path",
      topic_id: "topic-status",
      task_type: "analysis",
      exec_mode: "sync",
      status: "doing",
    }),
    invokeTaskInference: invokeInferenceMock("STEP\nMID\nCHANGE"),
  });

  const result = assertExecutionResult(resultRaw);
  assert.equal(result.inference.succeeded, true);
  assert.equal(result.finalStatus, "blocked");
  assert.equal(reviewPatchAttempts, 3);
  assert.ok(blockedPatchAttempts >= 1);
  assert.ok(result.inference.error?.includes("review patch failed"));
  assert.ok(result.summary.notes.some((note) => note.includes("watchdog")));
  assert.ok(result.summary.notes.some((note) => note.includes("补偿 review 回写")));

  await executor.stopGracefully();
}

async function testDoingStatusTaskRunsWithoutTodoPrelude() {
  const executor = createTaskRunExecutorLoop();
  let runCalls = 0;
  let reviewCalls = 0;

  const resultRaw = await executor.enqueueRun({
    taskId: "task-doing-entry",
    metadata: runtimeMetadata("task-doing-entry", "doing"),
    accountId: "default",
    apiRequest: async (request) => {
      if (request.method === "POST" && request.path === "/tasks/task-doing-entry/run") {
        runCalls += 1;
      }
      if (request.method === "PATCH" && request.path === "/tasks/task-doing-entry" && request.body?.status === "review") {
        reviewCalls += 1;
      }
      return { ok: true };
    },
    invokeTaskInference: invokeInferenceMock("STEP\nMID\nCHANGE"),
  });

  const result = assertExecutionResult(resultRaw);
  assert.equal(result.inference.succeeded, true);
  assert.equal(result.finalStatus, "review");
  assert.equal(runCalls, 0);
  assert.equal(reviewCalls, 1);
  assert.ok(result.summary.notes.some((note) => note.includes("当前已是 doing")));

  await executor.stopGracefully();
}

async function testRunCommandFallsBackWhenRuntimeHookUnavailable() {
  const router = createWTTCommandRouter({
    getClient: () => undefined,
    getAccount: () => ({
      accountId: "default",
      source: "channels.wtt.accounts.default",
      cloudUrl: "https://www.waxbyte.com",
      agentId: "agent-123",
      token: "tok_abc",
      enabled: true,
      configured: true,
    }),
  });

  let runCalls = 0;

  const fetchImpl = async (url, init = {}) => {
    const u = new URL(url);
    const method = (init.method ?? "GET").toUpperCase();
    const pathName = u.pathname.replace(/^\/api(?:\/v1)?/, "");

    if (method === "GET" && pathName === "/tasks/task-run") {
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-run",
          title: "执行内部 run",
          status: "ready",
          priority: "P1",
          owner_agent_id: "agent-owner",
          runner_agent_id: "agent-runner",
          pipeline_id: "pipe-main",
          topic_id: "topic-run",
          task_type: "analysis",
          exec_mode: "sync",
        },
      });
    }

    if (method === "POST" && pathName === "/tasks/task-run/run") {
      runCalls += 1;
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-run",
          status: "doing",
        },
      });
    }

    if (method === "PATCH" && pathName === "/tasks/task-run") {
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-run",
          status: "blocked",
        },
      });
    }

    return createFetchResponse({ ok: false, status: 404, body: { detail: "not found" } });
  };

  const runResp = await router.processText("@wtt task run task-run", { fetchImpl });
  assert.equal(runResp.handled, true);
  assert.ok(runResp.response?.includes("task run 执行失败"));
  assert.ok(runResp.response?.includes("状态推进(doing): POST /tasks/{task_id}/run"));
  assert.ok(runResp.response?.includes("最终状态: blocked"));
  assert.ok(runResp.response?.includes("invokeTaskInference"));
  assert.ok(runResp.response?.includes("summary.kind: task_run_summary"));
  assert.equal(runCalls, 1);

  const unavailableResp = await router.processText("@wtt task run task-run", {
    fetchImpl: async (url, init = {}) => {
      const u = new URL(url);
      const method = (init.method ?? "GET").toUpperCase();
      const pathName = u.pathname.replace(/^\/api(?:\/v1)?/, "");

      if (method === "GET" && pathName === "/tasks/task-run") {
        return createFetchResponse({
          ok: true,
          status: 200,
          body: {
            id: "task-run",
            title: "执行内部 run",
            status: "todo",
            priority: "P1",
            owner_agent_id: "agent-owner",
            runner_agent_id: "agent-runner",
            pipeline_id: "pipe-main",
          },
        });
      }

      return createFetchResponse({ ok: false, status: 404, body: { detail: "missing" } });
    },
  });

  assert.ok(unavailableResp.response?.includes("run 与 patch 状态接口均不可用"));
}

async function testRunCommandReportsDedupHit() {
  const router = createWTTCommandRouter({
    getClient: () => undefined,
    getAccount: () => ({
      accountId: "default",
      source: "channels.wtt.accounts.default",
      cloudUrl: "https://www.waxbyte.com",
      agentId: "agent-123",
      token: "tok_abc",
      enabled: true,
      configured: true,
    }),
  });

  let runCalls = 0;
  const runGate = createDeferred();
  const runStarted = createDeferred();

  const fetchImpl = async (url, init = {}) => {
    const u = new URL(url);
    const method = (init.method ?? "GET").toUpperCase();
    const pathName = u.pathname.replace(/^\/api(?:\/v1)?/, "");

    if (method === "GET" && pathName === "/tasks/task-run-dedup") {
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-run-dedup",
          title: "执行内部 run dedup",
          status: "ready",
          priority: "P1",
          owner_agent_id: "agent-owner",
          runner_agent_id: "agent-runner",
          pipeline_id: "pipe-main",
        },
      });
    }

    if (method === "POST" && pathName === "/tasks/task-run-dedup/run") {
      runCalls += 1;
      runStarted.resolve();
      await runGate.promise;
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-run-dedup",
          status: "doing",
        },
      });
    }

    return createFetchResponse({ ok: false, status: 404, body: { detail: "not found" } });
  };

  const firstRunPromise = router.processText("@wtt task run task-run-dedup", { fetchImpl });
  await runStarted.promise;

  const secondRun = await router.processText("@wtt task run task-run-dedup", { fetchImpl });
  assert.ok(secondRun.response?.includes("命中幂等去重"));
  assert.ok(secondRun.response?.includes("幂等决策: deduplicated"));

  runGate.resolve();
  const firstRun = await firstRunPromise;
  assert.ok(firstRun.response?.includes("幂等决策: enqueued"));
  assert.equal(runCalls, 1);
}

async function testTaskStatusEventDedupDispatchesOnce() {
  let now = Date.parse("2026-03-21T01:00:00.000Z");
  let runCalls = 0;

  const handler = createTaskStatusEventHandler({
    dedupWindowMs: 30_000,
    nowMs: () => now,
    runTask: async ({ taskId, status }) => {
      runCalls += 1;
      return {
        deduplicated: false,
        detail: `${taskId}:${status}`,
      };
    },
  });

  const first = await handler.handle({
    type: "task_status",
    task_id: "task-status-event-1",
    status: "doing",
  });

  const second = await handler.handle({
    type: "task_status",
    task_id: "task-status-event-1",
    status: "doing",
  });

  assert.equal(first.decision, "accepted");
  assert.equal(second.decision, "dedup");
  assert.equal(second.dedupSource, "event");
  assert.equal(runCalls, 1);

  now += 31_000;
  const third = await handler.handle({
    type: "task_status",
    task_id: "task-status-event-1",
    status: "doing",
  });
  assert.equal(third.decision, "accepted");
  assert.equal(runCalls, 2);
}

async function main() {
  await testTransitionGuardCompatibility();
  await testQueueEnqueueDequeueFlow();
  await testHeartbeatSchedulingPayloadGeneration();
  await testPersistenceReloadQueue();
  await testRecoveryOfRunningItem();
  await testDuplicateEnqueueBlocked();
  await testRecoveryRetryCapSkipsRequeue();
  await testDrainLockPreventsParallelProcessing();
  await testSnapshotStatusChangesThroughLifecycle();
  await testStatusFlowTodoDoingReviewSuccess();
  await testStatusFlowFailureMarksBlocked();
  await testReviewPatchRetryThenSuccess();
  await testReviewPatchRetryExhaustedMarksBlocked();
  await testDoingStatusTaskRunsWithoutTodoPrelude();
  await testRunCommandFallsBackWhenRuntimeHookUnavailable();
  await testRunCommandReportsDedupHit();
  await testTaskStatusEventDedupDispatchesOnce();
  console.log("✅ runtime internal executor test passed");
}

main().catch((err) => {
  console.error("❌ runtime internal executor test failed", err);
  process.exit(1);
});
