import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const serverSource = readFileSync("src/hosted-mcp/server.mjs", "utf8");
assert.match(serverSource, /startsAt: "2026-05-21T07:00:00\.000Z"/);
assert.match(serverSource, /keysCreated: 3/);
assert.match(serverSource, /genericKaleidoscopes: 11/);
assert.match(serverSource, /imageKaleidoscopes: 3/);

const start = serverSource.indexOf("function parseTimestampMs");
const end = serverSource.indexOf("function loadLiveWallState()");
assert.notEqual(start, -1, "baseline helper block start not found");
assert.notEqual(end, -1, "baseline helper block end not found");
assert.ok(end > start, "baseline helper block is malformed");

const helperSource = `
const KALEIDOSCOPE_PUBLIC_STATS_BASELINE = Object.freeze({
  timezone: "America/Los_Angeles",
  date: "2026-05-21",
  startsAt: "2026-05-21T07:00:00.000Z",
  counts: Object.freeze({
    keysCreated: 3,
    genericKaleidoscopes: 11,
    imageKaleidoscopes: 3,
  }),
});
${serverSource.slice(start, end)}
globalThis.__statsHelpers = {
  KALEIDOSCOPE_PUBLIC_STATS_BASELINE,
  deriveKaleidoscopePublicStats,
  isWipTestHandle,
  createdAtSinceBaseline,
};
`;

const context = {
  console,
  Date,
  Object,
  Number,
  String,
  Array,
  isPublicWallImageUrl(value) {
    return typeof value === "string" && value.startsWith("https://wip.computer/media/kaleidoscope/generated/");
  },
};

vm.createContext(context);
vm.runInContext(helperSource, context);

const {
  KALEIDOSCOPE_PUBLIC_STATS_BASELINE,
  deriveKaleidoscopePublicStats,
  isWipTestHandle,
  createdAtSinceBaseline,
} = context.__statsHelpers;

assert.deepEqual(JSON.parse(JSON.stringify(KALEIDOSCOPE_PUBLIC_STATS_BASELINE.counts)), {
  keysCreated: 3,
  genericKaleidoscopes: 11,
  imageKaleidoscopes: 3,
});
assert.equal(KALEIDOSCOPE_PUBLIC_STATS_BASELINE.startsAt, "2026-05-21T07:00:00.000Z");
assert.equal(isWipTestHandle("wiptest-parker"), true);
assert.equal(isWipTestHandle("WIPTEST-PARKER"), true);
assert.equal(isWipTestHandle("passkey-123"), false);
assert.equal(createdAtSinceBaseline({ createdAt: "2026-05-21T06:59:59.999Z" }), false);
assert.equal(createdAtSinceBaseline({ createdAt: "2026-05-21T07:00:00.000Z" }), true);

const images = [
  {
    url: "https://wip.computer/media/kaleidoscope/generated/prebaseline-generic.jpg",
    kind: "generic",
    createdAt: "2026-05-20T00:00:00.000Z",
  },
  {
    url: "https://wip.computer/media/kaleidoscope/generated/postbaseline-generic.jpg",
    kind: "generic",
    createdAt: "2026-05-21T07:00:00.000Z",
  },
  {
    url: "https://wip.computer/media/kaleidoscope/generated/postbaseline-image.jpg",
    kind: "image",
    createdAt: "2026-05-21T08:00:00.000Z",
  },
  {
    url: "https://wip.computer/media/kaleidoscope/generated/older-image.jpg",
    kind: "image",
    createdAt: "2026-05-20T01:00:00.000Z",
  },
];
const passkeyEntries = [
  { handle: "passkey-before", createdAt: "2026-05-20T00:00:00.000Z" },
  { handle: "wiptest-after", createdAt: "2026-05-21T08:00:00.000Z" },
  { handle: "user-after", createdAt: "2026-05-21T09:00:00.000Z" },
  { handle: "wiptest-newest", createdAt: "2026-05-21T09:15:00.000Z" },
];

const stats = deriveKaleidoscopePublicStats({
  images,
  passkeyEntries,
  now: new Date("2026-05-21T09:30:00.000Z"),
});

assert.equal(images.length, 4, "stats helper must not remove live-wall images");
assert.equal(stats.genericKaleidoscopes, 12);
assert.equal(stats.imageKaleidoscopes, 4);
assert.equal(stats.keysCreated, 4);
assert.equal(stats.publicWallImages, 4);
assert.deepEqual(JSON.parse(JSON.stringify(stats.newSinceBaseline)), {
  genericKaleidoscopes: 1,
  imageKaleidoscopes: 1,
  keysCreated: 1,
  total: 3,
});
assert.equal(stats.last24Hours.wallImages, 2);
assert.equal(stats.last24Hours.keysCreated, 1);
assert.equal(stats.lastCreated, "2026-05-21T09:00:00.000Z");

const wiptestOnly = deriveKaleidoscopePublicStats({
  images: [],
  passkeyEntries: [{ handle: "wiptest-only", createdAt: "2026-05-21T10:00:00.000Z" }],
  now: new Date("2026-05-21T10:00:00.000Z"),
});
assert.equal(wiptestOnly.keysCreated, 3);
assert.equal(wiptestOnly.newSinceBaseline.keysCreated, 0);

console.log("kaleidoscope public stats baseline tests passed");
