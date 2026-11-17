import { readFileSync } from "node:fs";

const server = readFileSync("src/hosted-mcp/server.mjs", "utf8");

function assertContains(needle, label) {
  if (!server.includes(needle)) {
    throw new Error(`${label} missing expected text: ${needle}`);
  }
}

function assertNotContains(needle, label) {
  if (server.includes(needle)) {
    throw new Error(`${label} still contains forbidden text: ${needle}`);
  }
}

assertContains("function generateCodexPairPollToken()", "pair poll token generator");
assertContains('return "ppt_" + randomBytes(32).toString("base64url");', "pair poll token entropy");
assertContains("function getBearerToken(req)", "bearer token helper");
assertContains("const pollToken = generateCodexPairPollToken();", "pair-init mints poll token");
assertContains("poll_token: pollToken,", "pair state stores poll token");
assertContains("poll_token_used: false,", "pair state tracks token consumption");
assertContains("pair_poll_token: pollToken,", "pair-init returns poll token to daemon");
assertContains('json(res, 401, { error: "pair_poll_token_expired" });', "expired token rejected");
assertContains('json(res, 401, { error: "invalid_pair_poll_token" });', "missing or wrong token rejected");
assertContains("if (!pollToken || pollToken !== p.poll_token || p.poll_token_used)", "pair-status validates token");
assertContains("p.poll_token_used = true;", "completed credential response consumes token");

function pairStatusModel(pair, bearer, now) {
  if (now > pair.expires) return { code: 401, body: { error: "pair_poll_token_expired" } };
  if (!bearer || bearer !== pair.poll_token || pair.poll_token_used) {
    return { code: 401, body: { error: "invalid_pair_poll_token" } };
  }
  if (pair.status === "completed") {
    pair.poll_token_used = true;
    return { code: 200, body: { status: "completed", api_key: pair.apiKey, handle: pair.handle } };
  }
  return { code: 200, body: { status: pair.status } };
}

const pair = {
  status: "pending",
  expires: 10_000,
  poll_token: "ppt_good",
  poll_token_used: false,
  apiKey: "ck_secret",
  handle: "Parker",
};

if (pairStatusModel({ ...pair }, null, 1).code !== 401) {
  throw new Error("missing poll token should fail");
}
if (pairStatusModel({ ...pair }, "ppt_wrong", 1).code !== 401) {
  throw new Error("wrong poll token should fail");
}
if (pairStatusModel({ ...pair }, "ppt_good", 20_000).code !== 401) {
  throw new Error("expired poll token should fail");
}
if (pairStatusModel({ ...pair }, "ppt_good", 1).body.status !== "pending") {
  throw new Error("correct poll token should return pending before completion");
}

const completedPair = { ...pair, status: "completed" };
const completed = pairStatusModel(completedPair, "ppt_good", 1);
if (completed.code !== 200 || completed.body.api_key !== "ck_secret") {
  throw new Error("correct poll token should return completed credential once");
}
const replay = pairStatusModel(completedPair, "ppt_good", 1);
if (replay.code !== 401) {
  throw new Error("reused completed poll token should fail");
}

console.log("crc pair-status poll token checks passed");
