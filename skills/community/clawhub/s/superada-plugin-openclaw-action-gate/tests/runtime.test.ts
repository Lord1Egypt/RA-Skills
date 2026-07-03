import test from "node:test";
import assert from "node:assert/strict";
import {
  beforeDispatchHandler,
  configureActionGatePluginForTests,
  messageSendingHandler,
  messageSentHandler,
  resetActionGatePluginForTests
} from "../src/index.ts";

test.afterEach(() => {
  delete process.env.ACTION_GATE_ENABLED;
  delete process.env.ACTION_GATE_AGENT;
  resetActionGatePluginForTests();
});

test("disabled mode is no-op and ACTION_GATE_ENABLED=false forces disabled", async () => {
  let called = false;
  configureActionGatePluginForTests({
    enabled: true,
    gateFactory: async () => {
      called = true;
      throw new Error("gate should not be loaded");
    }
  });
  process.env.ACTION_GATE_ENABLED = "false";

  assert.equal(await beforeDispatchHandler({ content: "hi" }, {}), undefined);
  assert.equal(await messageSendingHandler({ to: "discord", content: "hi" }, {}), undefined);
  assert.equal(await messageSentHandler({ to: "discord", content: "hi", success: true }, {}), undefined);
  assert.equal(called, false);
});

test("message_sending denial returns OpenClaw cancel shape", async () => {
  configureActionGatePluginForTests({
    enabled: true,
    gateFactory: async () => ({
      reserveOutbox: async () => ({
        decision: "non_owner_denied",
        dedupe_key: "dedupe-1",
        owner_agent: "ada",
        policy: { send_allowed: false, edit_allowed: false },
        reason: "protected public send belongs to scope owner"
      })
    })
  });

  const result = await messageSendingHandler({
    to: "discord",
    content: "public reply",
    metadata: {
      actionGate: {
        scopeKey: "discord:guild:thread",
        logicalActionKey: "reply-1",
        agent: "codex"
      }
    }
  }, { channelId: "thread", accountId: "guild" });

  assert.equal(result.cancel, true);
  assert.equal(result.cancelReason, "protected public send belongs to scope owner");
  assert.equal(result.metadata.actionGate.dedupeKey, "dedupe-1");
});

test("message_sending resolves Discord thread scope from target instead of provider name", async () => {
  const requests = [];
  configureActionGatePluginForTests({
    enabled: true,
    gateFactory: async () => ({
      reserveOutbox: async (request) => {
        requests.push(request);
        return {
          decision: "non_owner_denied",
          dedupe_key: "dedupe-thread",
          owner_agent: "book",
          policy: { send_allowed: false, edit_allowed: false },
          reason: "protected public send belongs to scope owner"
        };
      }
    })
  });

  const result = await messageSendingHandler({
    to: "channel:234567890123456789",
    content: "public reply"
  }, { channelId: "discord", accountId: "123456789012345678", sessionKey: "ada" });

  assert.equal(result.cancel, true);
  assert.equal(requests[0].scope_key, "discord:123456789012345678:234567890123456789");
  assert.equal(requests[0].agent, "ada");
});


test("message_sent completion path records receipt through adapter/core stub", async () => {
  const completions = [];
  configureActionGatePluginForTests({
    enabled: true,
    gateFactory: async () => ({
      reserveOutbox: async () => ({
        decision: "reserved",
        dedupe_key: "dedupe-2",
        owner_agent: "ada",
        policy: { send_allowed: true, edit_allowed: false }
      }),
      completeOutbox: async (request) => {
        completions.push(request);
        return { dedupe_key: request.dedupe_key, state: request.result };
      }
    })
  });

  const event = {
    to: "discord",
    content: "sent reply",
    metadata: {
      actionGate: {
        scopeKey: "discord:guild:thread",
        logicalActionKey: "reply-2",
        agent: "ada"
      }
    }
  };
  await messageSendingHandler(event, { channelId: "thread", accountId: "guild", sessionKey: "ada-session" });
  await messageSentHandler({ ...event, success: true, messageId: "discord-message-1" }, {
    channelId: "thread",
    accountId: "guild",
    sessionKey: "ada-session"
  });

  assert.equal(completions.length, 1);
  assert.deepEqual(completions[0], {
    dedupe_key: "dedupe-2",
    discord_message_id: "discord-message-1",
    result: "sent",
    metadata: {
      pluginId: "openclaw-action-gate",
      to: "discord",
      sessionKey: "ada-session",
      runId: undefined,
      error: undefined
    }
  });
});
