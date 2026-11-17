"use strict";

const assert = require("assert");
const {
  DEFAULT_AI_SOURCE,
  DEFAULT_REG_SOURCE,
  resolveAiSource,
  resolveRegSource,
} = require("../scripts/source_params.js");

assert.strictEqual(resolveAiSource(), DEFAULT_AI_SOURCE);
assert.strictEqual(resolveAiSource(""), DEFAULT_AI_SOURCE);
assert.strictEqual(resolveAiSource("13"), 13);
assert.throws(() => resolveAiSource("-1"), /非负整数/);
assert.throws(() => resolveAiSource("1.5"), /非负整数/);

assert.strictEqual(resolveRegSource(), DEFAULT_REG_SOURCE);
assert.strictEqual(resolveRegSource("  "), DEFAULT_REG_SOURCE);
assert.strictEqual(resolveRegSource("workbuddy"), "workbuddy");
assert.strictEqual(resolveRegSource(" custom-source "), "custom-source");
assert.throws(() => resolveRegSource("invalid source"), /只能包含/);

console.log("source_params tests passed");
