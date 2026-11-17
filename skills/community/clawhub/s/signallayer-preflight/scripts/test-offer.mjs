import { test } from "node:test";
import assert from "node:assert/strict";
import { EXPECTED, inspectOffer } from "./offer-terms.mjs";

const resourceUrl = "https://signallayer.floot.app/_api/v1/agent/preflight?target=https%3A%2F%2Fexample.com%2F";
function validChallenge() {
  return {
    x402Version: 2,
    resource: { url: resourceUrl },
    accepts: [{ ...EXPECTED }]
  };
}

test("allows a correct unsigned x402 V2 offer", () => {
  assert.deepEqual(inspectOffer(validChallenge(), { resourceUrl }), {
    valid: true, issues: [], matchingOffers: 1, offeredCount: 1
  });
});
test("rejects a different recipient", () => {
  const x = validChallenge();
  x.accepts[0].payTo = "0x0000000000000000000000000000000000000001";
  assert.equal(inspectOffer(x).valid, false);
});
test("rejects Base Sepolia instead of Base Mainnet", () => {
  const x = validChallenge();
  x.accepts[0].network = "eip155:84532";
  assert.equal(inspectOffer(x).valid, false);
});
test("rejects a different token contract", () => {
  const x = validChallenge();
  x.accepts[0].asset = "0x0000000000000000000000000000000000000002";
  assert.equal(inspectOffer(x).valid, false);
});
test("rejects an increased charge", () => {
  const x = validChallenge();
  x.accepts[0].amount = "100000";
  assert.equal(inspectOffer(x).valid, false);
});
test("rejects unsupported scheme and protocol version", () => {
  const x = validChallenge();
  x.accepts[0].scheme = "upto";
  x.x402Version = 1;
  assert.equal(inspectOffer(x).valid, false);
});
test("rejects empty or malformed offers", () => {
  assert.equal(inspectOffer(null).valid, false);
  assert.equal(inspectOffer({ x402Version: 2, accepts: [] }).valid, false);
});
test("rejects a 402 challenge for another resource", () => {
  const x = validChallenge();
  x.resource.url = "https://untrusted.example/x";
  assert.ok(inspectOffer(x, { resourceUrl }).issues.includes("challenge_resource_mismatch"));
});
test("accepts mixed-case checksummed EVM addresses", () => {
  const x = validChallenge();
  x.accepts[0].asset = EXPECTED.asset.toLowerCase();
  x.accepts[0].payTo = EXPECTED.payTo.toLowerCase();
  assert.equal(inspectOffer(x).valid, true);
});
test("does not accept a good-looking offer if its resource mismatches", () => {
  const x = validChallenge();
  x.resource.url = "https://signallayer.floot.app/_api/v1/market/execution-intel";
  assert.equal(inspectOffer(x, {resourceUrl}).valid, false);
});
