import assert from "node:assert/strict";
import { createWTTCommandRouter, parseWTTCommandText } from "./dist/commands/router.js";
import { processWTTCommandText } from "./dist/channel.js";

class MockClient {
  connected = true;

  async list(limit) {
    return [
      { id: "topic-1", name: "AI", type: "discussion", member_count: 8, description: "大模型与Agent" },
      { id: "topic-2", name: "AutoDrive", type: "broadcast", member_count: 16 },
    ].slice(0, limit ?? 2);
  }

  async find(query) {
    return [{ id: "topic-find", name: `命中:${query}`, type: "discussion", member_count: 3 }];
  }

  async join(topicId) {
    return { message: "Joined successfully", topic_id: topicId };
  }

  async leave(topicId) {
    return { message: "Left topic", topic_id: topicId };
  }

  async publish(topicId, content) {
    return { id: "msg-pub-1", topic_id: topicId, content };
  }

  async poll() {
    return {
      messages: [
        {
          id: "msg-1",
          topic_id: "topic-1",
          sender_id: "agent-a",
          content_type: "text",
          content: "hello from topic",
          created_at: "2026-03-20T11:00:00Z",
        },
      ],
      topics: [{ id: "topic-1", name: "AI" }],
    };
  }

  async history(topicId) {
    return [
      {
        id: "msg-h-1",
        topic_id: topicId,
        sender_id: "agent-b",
        content_type: "text",
        content: "history line",
        created_at: "2026-03-20T10:00:00Z",
      },
    ];
  }

  async p2p(targetAgentId, content) {
    return { id: "msg-p2p-1", target_agent_id: targetAgentId, content };
  }

  async detail(topicId) {
    return {
      id: topicId,
      name: "AI",
      type: "discussion",
      visibility: "public",
      join_method: "open",
      member_count: 12,
      creator_agent_id: "agent-owner",
      description: "技术交流",
    };
  }

  async subscribed() {
    return [{ id: "topic-sub", name: "Subscribed", type: "discussion", my_role: "member", member_count: 5 }];
  }

  async decryptMessage(content) {
    return content;
  }
}

function createFetchResponse({ ok, status, statusText = "", body = {}, contentType = "application/json" }) {
  return {
    ok,
    status,
    statusText,
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

function createCommandApiFetch() {
  return async (url, init = {}) => {
    const u = new URL(url);
    const method = (init.method ?? "GET").toUpperCase();
    const path = u.pathname.replace(/^\/api(?:\/v1)?/, "");
    const body = init.body ? JSON.parse(init.body) : undefined;

    if (method === "GET" && path === "/tasks") {
      return createFetchResponse({
        ok: true,
        status: 200,
        body: [
          { id: "task-1", title: "实现命令路由", status: "doing", priority: "P1", owner_agent_id: "agent-owner" },
          { id: "task-2", title: "补充测试", status: "todo", priority: "P2", owner_agent_id: "agent-owner" },
          { id: "task-3", title: "审查返工", status: "review", priority: "P2", owner_agent_id: "agent-owner" },
        ],
      });
    }

    if (method === "GET" && path === "/tasks/task-1") {
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-1",
          title: "实现命令路由",
          status: "doing",
          priority: "P1",
          owner_agent_id: "agent-owner",
          runner_agent_id: "agent-runner",
          pipeline_id: "pipe-1",
          description: "确保 parser + handler 对齐",
        },
      });
    }

    if (method === "GET" && path === "/tasks/task-2") {
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-2",
          title: "补充测试",
          status: "todo",
          priority: "P2",
          owner_agent_id: "agent-owner",
          runner_agent_id: "agent-runner",
          pipeline_id: "pipe-2",
          topic_id: "topic-task-2",
          task_type: "analysis",
          exec_mode: "sync",
          description: "补齐 task run 成功路径",
        },
      });
    }

    if (method === "GET" && path === "/tasks/task-3") {
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-3",
          title: "审查返工",
          status: "review",
          priority: "P2",
          owner_agent_id: "agent-owner",
          runner_agent_id: "agent-runner",
          pipeline_id: "pipe-3",
        },
      });
    }

    if (method === "POST" && path === "/tasks") {
      assert.equal(body?.title, "新任务");
      return createFetchResponse({ ok: true, status: 200, body: { id: "task-new-1" } });
    }

    if (method === "POST" && path === "/tasks/task-2/run") {
      assert.equal(body?.trigger_agent_id, "agent-123");
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-2",
          title: "补充测试",
          status: "doing",
          priority: "P2",
          owner_agent_id: "agent-owner",
          runner_agent_id: "agent-runner",
          pipeline_id: "pipe-2",
          topic_id: "topic-task-2",
          task_type: "analysis",
          exec_mode: "sync",
          description: "run with runtime hook",
        },
      });
    }

    if (method === "PATCH" && path === "/tasks/task-2") {
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-2",
          title: "补充测试",
          status: body?.status ?? "review",
          priority: "P2",
          owner_agent_id: "agent-owner",
          runner_agent_id: "agent-runner",
          pipeline_id: "pipe-2",
          topic_id: "topic-task-2",
        },
      });
    }

    if (method === "POST" && path === "/tasks/task-3/review") {
      assert.equal(body?.action, "reject");
      return createFetchResponse({
        ok: true,
        status: 200,
        body: {
          id: "task-3",
          title: "审查返工",
          status: "doing",
          priority: "P2",
          owner_agent_id: "agent-owner",
          runner_agent_id: "agent-runner",
          pipeline_id: "pipe-3",
        },
      });
    }

    if (method === "GET" && path === "/tasks/pipelines") {
      return createFetchResponse({
        ok: true,
        status: 200,
        body: [
          { id: "pipe-1", name: "默认流水线", description: "用于回归" },
        ],
      });
    }

    if (method === "POST" && path === "/tasks/pipelines") {
      assert.equal(body?.name, "交付流");
      return createFetchResponse({ ok: true, status: 200, body: { id: "pipe-new-1" } });
    }

    if (method === "POST" && path === "/tasks/pipeline/execute") {
      assert.equal(body?.pipeline_id, "pipe-1");
      return createFetchResponse({ ok: true, status: 200, body: { message: "execution started" } });
    }

    if (method === "GET" && path === "/manager/delegations") {
      assert.equal(u.searchParams.get("manager_agent_id"), "agent-123");
      return createFetchResponse({
        ok: true,
        status: 200,
        body: [
          { target_agent_id: "agent-a", can_publish: true, can_p2p: true },
        ],
      });
    }

    if (method === "POST" && path === "/manager/delegations") {
      assert.equal(body?.target_agent_id, "agent-b");
      return createFetchResponse({ ok: true, status: 200, body: { message: "ok" } });
    }

    if (method === "DELETE" && path === "/manager/delegations") {
      assert.equal(u.searchParams.get("target_agent_id"), "agent-b");
      return createFetchResponse({ ok: true, status: 200, body: { message: "removed" } });
    }

    return createFetchResponse({ ok: false, status: 404, body: { detail: "not found" } });
  };
}

async function main() {
  const mockClient = new MockClient();
  const baseAccount = {
    accountId: "default",
    source: "channels.wtt.accounts.default",
    cloudUrl: "https://www.waxbyte.com",
    agentId: "agent-123",
    token: "tok_1234567890",
    enabled: true,
    configured: true,
  };

  const router = createWTTCommandRouter({
    getClient: () => mockClient,
    getAccount: () => baseAccount,
    defaultAccountId: "default",
  });

  const parsed = parseWTTCommandText("@wtt publish topic-1 hello world");
  assert.deepEqual(parsed, { name: "publish", topicId: "topic-1", content: "hello world" });
  assert.deepEqual(parseWTTCommandText("@wtt config auto"), { name: "config", mode: "auto" });
  assert.deepEqual(parseWTTCommandText("@wtt bind"), { name: "bind" });
  assert.deepEqual(parseWTTCommandText("@wtt task detail task-1"), { name: "task", action: "detail", taskId: "task-1" });
  assert.deepEqual(parseWTTCommandText("@wtt task create \"新任务\" 描述内容"), {
    name: "task",
    action: "create",
    title: "新任务",
    description: "描述内容",
  });
  assert.deepEqual(parseWTTCommandText("@wtt task review task-1 approve looks good"), {
    name: "task",
    action: "review",
    taskId: "task-1",
    reviewAction: "approve",
    comment: "looks good",
  });
  assert.deepEqual(parseWTTCommandText("@wtt pipeline run pipe-1"), {
    name: "pipeline",
    action: "run",
    pipelineId: "pipe-1",
  });
  assert.deepEqual(parseWTTCommandText("@wtt delegate remove agent-x"), {
    name: "delegate",
    action: "remove",
    targetAgentId: "agent-x",
  });
  assert.deepEqual(parseWTTCommandText("/wtt list"), { name: "list" });
  assert.deepEqual(parseWTTCommandText("/wtt task list"), { name: "task", action: "list" });

  const nonCommand = await router.processText("hello");
  assert.equal(nonCommand.handled, false);

  const openclawSlash = await router.processText("/status");
  assert.equal(openclawSlash.handled, false);

  const checks = [
    ["@wtt list", "公开话题"],
    ["/wtt list", "公开话题"],
    ["@wtt find 自动驾驶", "搜索结果"],
    ["@wtt join topic-1", "已加入"],
    ["@wtt leave topic-1", "已离开"],
    ["@wtt publish topic-1 你好", "已发布"],
    ["@wtt poll", "新消息"],
    ["@wtt history topic-1", "历史消息"],
    ["@wtt p2p agent-z 私信测试", "已发送给"],
    ["@wtt detail topic-1", "可见性"],
    ["@wtt subscribed", "已订阅话题"],
    ["@wtt help", "WTT 命令"],
  ];

  for (const [cmd, expected] of checks) {
    const result = await router.processText(cmd);
    assert.equal(result.handled, true, `Expected handled=true for: ${cmd}`);
    assert.ok(result.response?.includes(expected), `Unexpected response for ${cmd}: ${result.response}`);
  }

  // New command happy paths
  const commandApiFetch = createCommandApiFetch();

  const taskList = await router.processText("@wtt task list", { fetchImpl: commandApiFetch });
  assert.ok(taskList.response?.includes("任务列表"));

  const taskDetail = await router.processText("@wtt task detail task-1", { fetchImpl: commandApiFetch });
  assert.ok(taskDetail.response?.includes("实现命令路由"));

  const taskCreate = await router.processText("@wtt task create 新任务 需要补齐集成测试", { fetchImpl: commandApiFetch });
  assert.ok(taskCreate.response?.includes("任务已创建"));

  const taskRun = await router.processText("@wtt task run task-2", {
    fetchImpl: commandApiFetch,
    runtimeHooks: {
      dispatchTaskInference: async ({ prompt }) => ({
        outputText: `STEP: plan\nMID: evaluate\nCHANGE: done\n${prompt.slice(0, 16)}`,
        provider: "runtime-hook-mock",
      }),
    },
  });
  assert.ok(taskRun.response?.includes("执行完成（已进入 review）"));
  assert.ok(taskRun.response?.includes("task_id: task-2"));
  assert.ok(taskRun.response?.includes("状态推进(doing): POST /tasks/{task_id}/run"));
  assert.ok(taskRun.response?.includes("幂等决策: enqueued"));
  assert.ok(taskRun.response?.includes("持久化队列: 已启用"));
  assert.ok(taskRun.response?.includes("summary.kind: task_run_summary"));

  const taskReview = await router.processText("@wtt task review task-3 reject 需要返工", { fetchImpl: commandApiFetch });
  assert.ok(taskReview.response?.includes("task review 已提交"));
  assert.ok(taskReview.response?.includes("task_id: task-3"));
  assert.ok(taskReview.response?.includes("状态迁移: review -> doing"));

  const pipelineList = await router.processText("@wtt pipeline list", { fetchImpl: commandApiFetch });
  assert.ok(pipelineList.response?.includes("流水线列表"));

  const pipelineCreate = await router.processText("@wtt pipeline create 交付流 含验证步骤", { fetchImpl: commandApiFetch });
  assert.ok(pipelineCreate.response?.includes("流水线已创建"));

  const pipelineRun = await router.processText("@wtt pipeline run pipe-1", { fetchImpl: commandApiFetch });
  assert.ok(pipelineRun.response?.includes("执行已触发"));

  const delegateList = await router.processText("@wtt delegate list", { fetchImpl: commandApiFetch });
  assert.ok(delegateList.response?.includes("委托列表"));

  const delegateCreate = await router.processText("@wtt delegate create agent-b", { fetchImpl: commandApiFetch });
  assert.ok(delegateCreate.response?.includes("委托已创建"));

  const delegateRemove = await router.processText("@wtt delegate remove agent-b", { fetchImpl: commandApiFetch });
  assert.ok(delegateRemove.response?.includes("委托已移除"));

  const bad = await router.processText("@wtt publish only-topic");
  assert.equal(bad.handled, true);
  assert.ok(bad.response?.includes("命令格式错误"));

  // task endpoint fallback - no API endpoint
  const taskUnavailable = await router.processText("@wtt task list", {
    fetchImpl: async () => createFetchResponse({ ok: false, status: 404, body: { detail: "missing" } }),
  });
  assert.ok(taskUnavailable.response?.includes("暂不可用"));

  // task unauthorized
  const taskUnauthorized = await router.processText("@wtt task list", {
    fetchImpl: async () => createFetchResponse({ ok: false, status: 401, body: { detail: "unauthorized" } }),
  });
  assert.ok(taskUnauthorized.response?.includes("鉴权失败"));

  // pipeline network error
  const pipelineNetworkErr = await router.processText("@wtt pipeline list", {
    fetchImpl: async () => {
      throw new Error("ENOTFOUND");
    },
  });
  assert.ok(pipelineNetworkErr.response?.includes("网络异常"));

  // delegate missing agentId
  let delegateFetchCalled = false;
  const delegateMissingAgentRouter = createWTTCommandRouter({
    getClient: () => undefined,
    getAccount: () => ({
      accountId: "default",
      source: "channels.wtt.accounts.default",
      cloudUrl: "https://www.waxbyte.com",
      token: "tok_x",
      agentId: "",
    }),
  });
  const delegateMissingAgent = await delegateMissingAgentRouter.processText("@wtt delegate list", {
    fetchImpl: async () => {
      delegateFetchCalled = true;
      return createFetchResponse({ ok: true, status: 200, body: [] });
    },
  });
  assert.ok(delegateMissingAgent.response?.includes("需要已配置 agentId"));
  assert.equal(delegateFetchCalled, false);

  // config auto - missing channels.wtt config
  const noAccountRouter = createWTTCommandRouter({
    getClient: () => undefined,
    defaultAccountId: "default",
  });
  const configNoAccount = await noAccountRouter.processText("@wtt config auto");
  assert.ok(configNoAccount.response?.includes("未检测到 channels.wtt 账户配置"));

  // config auto - detect channels.wtt config via processWTTCommandText wrapper
  const configFromCfg = await processWTTCommandText({
    text: "@wtt config auto",
    accountId: "default",
    cfg: {
      channels: {
        wtt: {
          accounts: {
            default: {
              cloudUrl: "https://api.example.com",
              agentId: "agent-from-cfg",
              token: "token-from-cfg",
            },
          },
        },
      },
    },
  });
  assert.ok(configFromCfg.response?.includes("channels.wtt.accounts.default"));
  assert.ok(configFromCfg.response?.includes("agent-from-cfg"));

  // config auto - partial config hints
  const partialRouter = createWTTCommandRouter({
    getClient: () => undefined,
    getAccount: () => ({
      accountId: "default",
      source: "channels.wtt.accounts.default",
      cloudUrl: "https://www.waxbyte.com",
      agentId: "agent-abc",
      token: "",
    }),
  });
  const configPartial = await partialRouter.processText("@wtt config auto");
  assert.ok(configPartial.response?.includes("缺少关键配置"));
  assert.ok(configPartial.response?.includes("token"));

  // bind success
  const bindCalls = [];
  const bindOk = await router.processText("@wtt bind", {
    fetchImpl: async (url, init) => {
      bindCalls.push({ url, init });
      return createFetchResponse({
        ok: true,
        status: 200,
        body: { code: "WTT-CLAIM-ABCD1234", expires_in_seconds: 900 },
      });
    },
  });
  assert.ok(bindOk.response?.includes("WTT-CLAIM-ABCD1234"));
  assert.equal(bindCalls.length, 1);
  assert.equal(bindCalls[0].url, "https://www.waxbyte.com/agents/claim-code");
  assert.equal(bindCalls[0].init?.method, "POST");
  assert.equal(bindCalls[0].init?.headers?.["X-Agent-Token"], "tok_1234567890");

  // bind unauthorized
  const bind401 = await router.processText("@wtt bind", {
    fetchImpl: async () => createFetchResponse({ ok: false, status: 401, body: { error: "unauthorized" } }),
  });
  assert.ok(bind401.response?.includes("鉴权失败"));

  // bind network failure
  const bindNetworkErr = await router.processText("@wtt bind", {
    fetchImpl: async () => {
      throw new Error("ECONNREFUSED");
    },
  });
  assert.ok(bindNetworkErr.response?.includes("网络异常"));

  // bind missing agentId
  let calledWhenMissing = false;
  const bindMissingCfgRouter = createWTTCommandRouter({
    getClient: () => undefined,
    getAccount: () => ({ accountId: "default", cloudUrl: "https://www.waxbyte.com", token: "tok_x" }),
  });
  const bindMissingCfg = await bindMissingCfgRouter.processText("@wtt bind", {
    fetchImpl: async () => {
      calledWhenMissing = true;
      return createFetchResponse({ ok: true, status: 200, body: {} });
    },
  });
  assert.ok(bindMissingCfg.response?.includes("缺少 agentId"));
  assert.equal(calledWhenMissing, false);

  console.log("✅ command router mock test passed");
}

main().catch((err) => {
  console.error("❌ command router mock test failed", err);
  process.exit(1);
});
