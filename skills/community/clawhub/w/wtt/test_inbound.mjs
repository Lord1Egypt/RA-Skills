import assert from "node:assert/strict";

import { createInboundMessageRelay, normalizeInboundWsMessage, routeInboundWsMessage, wttPlugin } from "./dist/channel.js";

function createAccount(agentId = "agent-main", name = "default", config = {}) {
  return {
    accountId: "default",
    name,
    enabled: true,
    configured: true,
    cloudUrl: "https://example.com",
    agentId,
    token: "tok",
    config,
  };
}

function createRuntimeMock() {
  const calls = {
    route: [],
    finalize: [],
    record: [],
    dispatch: [],
  };

  const runtime = {
    routing: {
      resolveAgentRoute(input) {
        calls.route.push(input);
        return {
          agentId: "main",
          accountId: input.accountId ?? "default",
          sessionKey: `agent:main:${input.channel}:${input.peer?.kind ?? "direct"}:${input.peer?.id ?? "x"}`,
        };
      },
    },
    session: {
      resolveStorePath() {
        return "/tmp/wtt-session-store";
      },
      readSessionUpdatedAt() {
        return null;
      },
      async recordInboundSession(params) {
        calls.record.push(params);
      },
    },
    reply: {
      resolveEnvelopeFormatOptions() {
        return {};
      },
      formatAgentEnvelope({ body }) {
        return `[env] ${body}`;
      },
      finalizeInboundContext(ctx) {
        calls.finalize.push(ctx);
        return ctx;
      },
      async dispatchReplyWithBufferedBlockDispatcher({ ctx, dispatcherOptions }) {
        calls.dispatch.push(ctx);
        await dispatcherOptions.deliver({ text: "ack from mock" });
      },
    },
  };

  return { runtime, calls };
}

async function testNormalizeP2P() {
  const normalized = normalizeInboundWsMessage({
    msg: {
      type: "new_message",
      message: {
        id: "msg-1",
        topic_id: "topic-p2p",
        sender_id: "alice",
        topic_type: "p2p",
        content: "hello",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
  });

  assert.equal(normalized.chatType, "direct");
  assert.equal(normalized.routePeerId, "topic-p2p");
  assert.equal(normalized.to, "topic:topic-p2p");
}

async function testNormalizeTopic() {
  const normalized = normalizeInboundWsMessage({
    msg: {
      type: "new_message",
      message: {
        id: "msg-2",
        topic_id: "topic-abc",
        sender_id: "bob",
        topic_type: "discussion",
        topic_name: "Team room",
        sender_display_name: "Bob",
        content_type: "TEXT",
        semantic_type: "POST",
        content: "status update",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
  });

  assert.equal(normalized.chatType, "group");
  assert.equal(normalized.routePeerId, "topic-abc");
  assert.equal(normalized.to, "topic:topic-abc");
}

async function testRouteInboundAndDeliver() {
  const { runtime, calls } = createRuntimeMock();
  const deliveries = [];

  await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-main"),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-3",
        topic_id: "topic-p2p-1",
        sender_id: "alice",
        topic_type: "p2p",
        content: "please help",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
    deliver: async (payload) => {
      deliveries.push(payload);
    },
  });

  assert.equal(calls.route.length, 1);
  assert.equal(calls.route[0].peer.kind, "direct");
  assert.equal(calls.route[0].peer.id, "topic-p2p-1");

  assert.equal(calls.record.length, 1);
  assert.equal(calls.finalize[0].To, "topic:topic-p2p-1");
  assert.equal(deliveries.length, 1);
  assert.equal(deliveries[0].to, "topic:topic-p2p-1");
  assert.equal(deliveries[0].payload.text, "ack from mock");
}

async function testRouteSkipsSelfEcho() {
  const { runtime, calls } = createRuntimeMock();

  await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-main"),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-4",
        topic_id: "topic-echo",
        sender_id: "agent-main",
        content: "self message",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
  });

  assert.equal(calls.route.length, 0);
  assert.equal(calls.record.length, 0);
  assert.equal(calls.dispatch.length, 0);
}

async function testPollMessagesRouted() {
  const { runtime, calls } = createRuntimeMock();
  const deliveries = [];

  const relay = createInboundMessageRelay({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-main"),
    channelRuntime: runtime,
    deliver: async (payload) => {
      deliveries.push(payload);
    },
  });

  const result = await relay.handlePollResult({
    messages: [
      {
        id: "poll-msg-1",
        topic_id: "topic-p2p-2",
        sender_id: "alice",
        topic_type: "p2p",
        content: "hello from poll",
        created_at: "2026-03-21T00:00:00Z",
      },
    ],
  });

  assert.equal(result.fetched, 1);
  assert.equal(result.routed, 1);
  assert.equal(result.dedupDropped, 0);
  assert.equal(calls.route.length, 1);
  assert.equal(deliveries.length, 1);
  assert.equal(deliveries[0].to, "topic:topic-p2p-2");
}

async function testDuplicateIdDroppedAcrossPushAndPoll() {
  const { runtime, calls } = createRuntimeMock();
  const deliveries = [];

  const relay = createInboundMessageRelay({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-main"),
    channelRuntime: runtime,
    deliver: async (payload) => {
      deliveries.push(payload);
    },
  });

  await relay.handlePush({
    type: "new_message",
    message: {
      id: "dup-msg-1",
      topic_id: "topic-p2p-3",
      sender_id: "alice",
      topic_type: "p2p",
      content: "dup hello",
      created_at: "2026-03-21T00:00:00Z",
    },
  });

  const result = await relay.handlePollResult({
    messages: [
      {
        id: "dup-msg-1",
        topic_id: "topic-p2p-3",
        sender_id: "alice",
        topic_type: "p2p",
        content: "dup hello",
        created_at: "2026-03-21T00:00:00Z",
      },
    ],
  });

  assert.equal(result.fetched, 1);
  assert.equal(result.routed, 0);
  assert.equal(result.dedupDropped, 1);
  assert.equal(calls.route.length, 1);
  assert.equal(deliveries.length, 1);
}

async function testDiscussionMentionSupportsDisplayAlias() {
  const { runtime, calls } = createRuntimeMock();
  const deliveries = [];

  const result = await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-real-001", "YZ Agent"),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-mention-alias",
        topic_id: "topic-discuss-1",
        sender_id: "human-1",
        topic_type: "discussion",
        content: "@yz_agent 请处理这个任务",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
    deliver: async (payload) => {
      deliveries.push(payload);
    },
  });

  assert.equal(result.routed, true);
  assert.equal(calls.route.length, 1);
  assert.equal(deliveries.length, 1);
}

async function testDiscussionMentionStrictTargeting() {
  const { runtime, calls } = createRuntimeMock();

  const result = await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("agent_x", "Worker X"),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-mention-strict",
        topic_id: "topic-discuss-2",
        sender_id: "human-2",
        topic_type: "discussion",
        content: "@agent_xxxx 只要你来处理",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
  });

  assert.equal(result.routed, false);
  assert.equal(result.reason, "discussion_no_mention");
  assert.equal(calls.route.length, 0);
}

async function testDiscussionMentionCjkSuffixStillTriggers() {
  const { runtime, calls } = createRuntimeMock();
  const deliveries = [];

  const result = await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("lyz_agent", "LYZ Agent"),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-mention-cjk-1",
        topic_id: "topic-discuss-cjk-1",
        sender_id: "human-cjk-1",
        topic_type: "discussion",
        content: "@lyz_agent看看这个问题",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
    deliver: async (payload) => {
      deliveries.push(payload);
    },
  });

  assert.equal(result.routed, true);
  assert.equal(calls.route.length, 1);
  assert.equal(deliveries.length, 1);
}

async function testDiscussionMentionAfterCjkPrefixStillTriggers() {
  const { runtime, calls } = createRuntimeMock();
  const deliveries = [];

  const result = await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("lyz_agent", "LYZ Agent"),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-mention-cjk-2",
        topic_id: "topic-discuss-cjk-2",
        sender_id: "human-cjk-2",
        topic_type: "discussion",
        content: "请@lyz_agent处理一下",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
    deliver: async (payload) => {
      deliveries.push(payload);
    },
  });

  assert.equal(result.routed, true);
  assert.equal(calls.route.length, 1);
  assert.equal(deliveries.length, 1);
}

async function testStandaloneSlashBypassesMentionGateWhenEnabled() {
  const { runtime, calls } = createRuntimeMock();
  const deliveries = [];

  const result = await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-slash", "Slash Agent", {
      slashCompat: true,
      slashBypassMentionGate: true,
    }),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-slash-bypass",
        topic_id: "topic-discuss-slash",
        sender_id: "human-slash",
        topic_type: "discussion",
        content: "/status",
        metadata: {
          command_target_agent_id: "agent-slash",
          command_scope: "single_agent",
        },
        created_at: "2026-03-21T00:00:00Z",
      },
    },
    deliver: async (payload) => {
      deliveries.push(payload);
    },
  });

  assert.equal(result.routed, true);
  assert.equal(calls.route.length, 1);
  assert.equal(deliveries.length, 1);
}

async function testStandaloneSlashWithoutTargetIsSkippedInDiscuss() {
  const { runtime, calls } = createRuntimeMock();

  const result = await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-slash", "Slash Agent", {
      slashCompat: true,
      slashBypassMentionGate: true,
    }),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-slash-gated",
        topic_id: "topic-discuss-slash-gated",
        sender_id: "human-slash-2",
        topic_type: "discussion",
        content: "/status",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
  });

  assert.equal(result.routed, false);
  assert.equal(result.reason, "agent_no_mention");
  assert.equal(calls.route.length, 0);
}

async function testWttSlashCommandHandledBeforeInference() {
  const { runtime, calls } = createRuntimeMock();
  const deliveries = [];

  const result = await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-cmd", "Command Agent", {
      slashCompat: true,
      slashBypassMentionGate: true,
    }),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-wtt-help",
        topic_id: "topic-discuss-cmd",
        sender_id: "human-cmd",
        topic_type: "discussion",
        content: "/wtt help",
        metadata: {
          command_target_agent_id: "agent-cmd",
          command_scope: "single_agent",
        },
        created_at: "2026-03-21T00:00:00Z",
      },
    },
    deliver: async (payload) => {
      deliveries.push(payload);
    },
  });

  assert.equal(result.routed, true);
  assert.equal(calls.route.length, 0);
  assert.equal(calls.dispatch.length, 0);
  assert.equal(deliveries.length, 1);
  assert.ok(String(deliveries[0].payload?.text || "").includes("WTT 命令"));
}

async function testTaskLinkedDoesNotRequireMention() {
  const { runtime, calls } = createRuntimeMock();
  const deliveries = [];

  const result = await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-a", "Agent A"),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-task-mention",
        topic_id: "topic-task-1",
        topic_name: "TASK-abc123",
        task_id: "task-abc123",
        sender_id: "human-4",
        topic_type: "discussion",
        content: "@agent-b 你来做",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
    deliver: async (payload) => {
      deliveries.push(payload);
    },
  });

  assert.equal(result.routed, true);
  assert.equal(calls.route.length, 1);
  assert.equal(deliveries.length, 1);
}

async function testTaskLinkedRunnerMismatchSkipped() {
  const { runtime, calls } = createRuntimeMock();

  const result = await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-a", "Agent A"),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-task-runner-mismatch",
        topic_id: "topic-task-2",
        topic_name: "TASK-def456",
        task_id: "task-def456",
        topic_type: "discussion",
        sender_id: "human-6",
        runner_agent_id: "agent-b",
        content: "无需@，但runner不是你",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
  });

  assert.equal(result.routed, false);
  assert.equal(result.reason, "task_runner_mismatch");
  assert.equal(calls.route.length, 0);
}

async function testP2PAlwaysInferEvenWithOtherMention() {
  const { runtime, calls } = createRuntimeMock();
  const deliveries = [];

  const result = await routeInboundWsMessage({
    cfg: {},
    accountId: "default",
    account: createAccount("agent-a", "Agent A"),
    channelRuntime: runtime,
    msg: {
      type: "new_message",
      message: {
        id: "msg-p2p-mention",
        topic_id: "topic-p2p-strict",
        sender_id: "human-5",
        topic_type: "p2p",
        content: "@agent-b 你处理",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
    deliver: async (payload) => {
      deliveries.push(payload);
    },
  });

  assert.equal(result.routed, true);
  assert.equal(calls.route.length, 1);
  assert.equal(deliveries.length, 1);
}

async function testNormalizeTopicIdFallbackField() {
  const normalized = normalizeInboundWsMessage({
    msg: {
      type: "new_message",
      message: {
        id: "msg-topic-fallback",
        topicId: "topic-fallback-1",
        sender_id: "alice",
        content: "hello",
        created_at: "2026-03-21T00:00:00Z",
      },
    },
  });

  assert.equal(normalized.topicId, "topic-fallback-1");
}

async function testMessageToolHintsReturnsArray() {
  const hints = wttPlugin.agentPrompt.messageToolHints();
  assert.equal(Array.isArray(hints), true);
  assert.equal(hints.length >= 1, true);
}

async function run() {
  await testNormalizeP2P();
  await testNormalizeTopic();
  await testRouteInboundAndDeliver();
  await testRouteSkipsSelfEcho();
  await testPollMessagesRouted();
  await testDuplicateIdDroppedAcrossPushAndPoll();
  await testDiscussionMentionSupportsDisplayAlias();
  await testDiscussionMentionStrictTargeting();
  await testDiscussionMentionCjkSuffixStillTriggers();
  await testDiscussionMentionAfterCjkPrefixStillTriggers();
  await testStandaloneSlashBypassesMentionGateWhenEnabled();
  await testStandaloneSlashWithoutTargetIsSkippedInDiscuss();
  await testWttSlashCommandHandledBeforeInference();
  await testTaskLinkedDoesNotRequireMention();
  await testTaskLinkedRunnerMismatchSkipped();
  await testP2PAlwaysInferEvenWithOtherMention();
  await testNormalizeTopicIdFallbackField();
  await testMessageToolHintsReturnsArray();
  console.log("test_inbound: ok");
}

run().catch((err) => {
  console.error("test_inbound: failed", err);
  process.exitCode = 1;
});
