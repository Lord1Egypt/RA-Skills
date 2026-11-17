import { readFile } from "node:fs/promises";
import assert from "node:assert/strict";

const skill = await readFile(new URL("../SKILL.md", import.meta.url), "utf8");
const review = await readFile(new URL("../AGENT-REVIEW.md", import.meta.url), "utf8");

assert.match(skill, /evidence_document_count/);
assert.match(skill, /has_evidence/);
assert.match(skill, /current non-deleted evidence documents/);
assert.match(skill, /legacy `evidence_layer_status` field and search filter are deprecated/);
assert.doesNotMatch(skill, /strongest credibility signal/i);
assert.doesNotMatch(skill, /more credibility surface/i);
assert.doesNotMatch(skill, /operating with worse information/i);
assert.doesNotMatch(review, /Evidence may be absent or incomplete/i);
assert.match(review, /do not assess authenticity, relevance, quality, sufficiency, or campaign verification/);

console.log("evidence availability skill contract: ok");
