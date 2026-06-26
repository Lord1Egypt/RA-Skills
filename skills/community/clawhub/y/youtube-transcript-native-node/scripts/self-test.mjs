#!/usr/bin/env node
// Offline regression tests for youtube-transcript-native-node.
// No network, no real yt-dlp invocation.

import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { delimiter, join } from "node:path";
import {
  dedupRollingCues,
  dedupRollingPhrases,
  isAllowedYouTubeUrl,
  parseArgs,
  parseVtt,
} from "./fetch.mjs";

const skillRoot = new URL("..", import.meta.url);

function runFetch(args, env = process.env) {
  return spawnSync(process.execPath, ["scripts/fetch.mjs", ...args], {
    cwd: skillRoot,
    encoding: "utf8",
    env,
  });
}

function selfTestEnv(extra = {}) {
  return { ...process.env, YOUTUBE_TRANSCRIPT_SELFTEST: "1", ...extra };
}

function withFakeYtDlp(callback) {
  const fakeDir = mkdtempSync(join(tmpdir(), "fake-ytdlp-"));
  const fakeScript = join(fakeDir, "fake-ytdlp.mjs");
  writeFileSync(fakeScript, `
import { dirname, join } from "node:path";
import { mkdirSync, writeFileSync } from "node:fs";
const args = process.argv.slice(2);
const outIndex = args.indexOf("-o");
const outTemplate = outIndex >= 0 ? args[outIndex + 1] : join(process.cwd(), "%(id)s.%(ext)s");
const dir = dirname(outTemplate);
mkdirSync(dir, { recursive: true });
if (process.env.FAKE_YTDLP_SLEEP_MS) await new Promise(r => setTimeout(r, Number(process.env.FAKE_YTDLP_SLEEP_MS)));
const large = process.env.FAKE_YTDLP_LARGE ? " word".repeat(200) : "alpha beta gamma delta";
const repeated = "one two three one two three four";
const vtt = "WEBVTT\\n\\n00:00:01.000 --> 00:00:02.000\\nalpha beta gamma\\n\\n00:00:02.000 --> 00:00:03.000\\n" + (process.env.FAKE_YTDLP_REPEAT ? repeated : large) + "\\n";
const lang = process.env.FAKE_YTDLP_LANG || "en";
if (!process.env.FAKE_YTDLP_NO_VTT) writeFileSync(join(dir, "abc." + lang + ".vtt"), vtt, "utf8");
const stderr = process.env.FAKE_YTDLP_STDERR || "";
if (stderr) process.stderr.write(stderr.replaceAll("<TMPDIR>", dir));
const meta = process.env.FAKE_YTDLP_MANUAL
  ? { title: "Fixture Video", subtitles: { [lang]: [{}] }, automatic_captions: {} }
  : { title: "Fixture Video", subtitles: {}, automatic_captions: { [lang]: [{}] } };
process.stdout.write(JSON.stringify(meta) + "\\n");
process.exit(Number(process.env.FAKE_YTDLP_CODE || "0"));
`, "utf8");
  const env = selfTestEnv({ PATH: `${fakeDir}${delimiter}${process.env.PATH || ""}`, YOUTUBE_TRANSCRIPT_TEST_YTDLP_SCRIPT: fakeScript });
  try { return callback(env, fakeScript); }
  finally { rmSync(fakeDir, { recursive: true, force: true }); }
}

const sampleVtt = `WEBVTT
Kind: captions
Language: en

cue-1
00:00:01.000 --> 00:00:03.000
<c>Hello &amp; welcome</c>

00:03.500 --> 00:05.000
<00:00:03.500>Hello &amp; welcome to the show</c>

00:00:05.000 --> 00:00:08.000
welcome to the show today
`;

const cues = parseVtt(sampleVtt);
assert.deepEqual(cues, [
  { start: "00:00:01", text: "Hello & welcome" },
  { start: "00:00:03", text: "Hello & welcome to the show" },
  { start: "00:00:05", text: "welcome to the show today" },
]);

const shortCue = parseVtt(`WEBVTT\n\n00:01.100 --> 00:02.200\nshort cue\n`);
assert.deepEqual(shortCue, [{ start: "00:00:01", text: "short cue" }]);

const rolling = dedupRollingCues([
  { start: "00:00:01", text: "alpha beta gamma" },
  { start: "00:00:02", text: "alpha beta gamma delta epsilon" },
  { start: "00:00:03", text: "gamma delta epsilon zeta eta" },
]);
assert.deepEqual(rolling, [
  { start: "00:00:01", text: "alpha beta gamma" },
  { start: "00:00:02", text: "delta epsilon" },
  { start: "00:00:03", text: "zeta eta" },
]);

assert.equal(
  dedupRollingPhrases("one two three one two three four five six"),
  "one two three four five six"
);

const manualCues = parseVtt(`WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nkeep this phrase\n\n00:00:02.000 --> 00:00:03.000\nkeep this phrase\n`);
assert.deepEqual(manualCues, [{ start: "00:00:01", text: "keep this phrase" }]);

for (const url of [
  "https://youtu.be/abc123",
  "https://www.youtube.com/watch?v=abc123",
  "https://m.youtube.com/watch?v=abc123",
]) assert.equal(isAllowedYouTubeUrl(url), true, `${url} should pass`);
for (const url of [
  "https://example.com/watch?v=abc123",
  "https://youtube.com.evil.com/watch?v=abc123",
  "https://youtube.com@evil.com/watch?v=abc123",
  "file:///tmp/video",
]) assert.equal(isAllowedYouTubeUrl(url), false, `${url} should fail`);

for (const lang of ["../../etc", "en;rm-rf", "", "a".repeat(33)]) {
  const r = runFetch(["--url", "https://youtu.be/abc123", "--lang", lang]);
  assert.notEqual(r.status, 0, `${lang} should be rejected`);
  assert.match(r.stderr, /--lang must/);
}
assert.equal(parseArgs(["--url", "https://youtu.be/abc123", "--lang", "en-US"]).lang, "en-US");
for (const argv of [["--url", "https://example.com/watch?v=nope"], ["--url", "https://youtu.be/abc123", "--unknown"]]) {
  const r = runFetch(argv);
  assert.notEqual(r.status, 0, `${argv.join(" ")} should fail`);
}

const missingDepDir = mkdtempSync(join(tmpdir(), "missing-ytdlp-"));
try {
  const missing = runFetch(["--url", "https://youtu.be/abc123"], { ...process.env, PATH: missingDepDir });
  assert.notEqual(missing.status, 0);
  assert.match(missing.stderr, /yt-dlp not found on PATH/);
  assert.equal(missing.stdout, "");
} finally { rmSync(missingDepDir, { recursive: true, force: true }); }

const syntheticHomePath = join(tmpdir(), "synthetic-home", "youtube-transcript-native-node", "scripts", "fetch.mjs");
const thrownPath = runFetch(["--url", "https://youtu.be/abc123"], selfTestEnv({ YOUTUBE_TRANSCRIPT_TEST_THROW_PATH: syntheticHomePath }));
assert.notEqual(thrownPath.status, 0);
assert.equal(thrownPath.stdout, "");
assert.match(thrownPath.stderr, /unexpected error/);
assert.doesNotMatch(thrownPath.stderr, /synthetic-home|youtube-transcript-native-node|fetch\.mjs/);
assert.match(thrownPath.stderr, /<tmp>|<home>/);

const forwardSlashPath = `${homedir().replaceAll("\\", "/")}/youtube-transcript-native-node/scripts/fetch.mjs`;
const thrownForwardSlashPath = runFetch(["--url", "https://youtu.be/abc123"], selfTestEnv({ YOUTUBE_TRANSCRIPT_TEST_THROW_PATH: `file:///${forwardSlashPath}` }));
assert.notEqual(thrownForwardSlashPath.status, 0);
assert.equal(thrownForwardSlashPath.stdout, "");
assert.match(thrownForwardSlashPath.stderr, /unexpected error/);
assert.doesNotMatch(thrownForwardSlashPath.stderr, /Users|youtube-transcript-native-node|fetch\.mjs/);
assert.match(thrownForwardSlashPath.stderr, /<home>/);

withFakeYtDlp((env, fakeScript) => {
  const inertHook = runFetch(["--url", "https://youtu.be/abc123"], {
    ...process.env,
    PATH: mkdtempSync(join(tmpdir(), "no-real-ytdlp-")),
    YOUTUBE_TRANSCRIPT_TEST_YTDLP_SCRIPT: fakeScript,
  });
  assert.notEqual(inertHook.status, 0);
  assert.match(inertHook.stderr, /yt-dlp not found on PATH/);

  const ok = runFetch(["--url", "https://youtu.be/abc123", "--json"], env);
  assert.equal(ok.status, 0, ok.stderr);
  const payload = JSON.parse(ok.stdout);
  assert.equal(payload.title, "Fixture Video");
  assert.equal(payload.auto, true);
  assert.match(payload.transcript, /alpha beta gamma delta/);

  const plain = runFetch(["--url", "https://youtu.be/abc123"], env);
  assert.equal(plain.status, 0, plain.stderr);
  assert.match(plain.stdout, /alpha beta gamma delta/);
  assert.doesNotMatch(plain.stdout, /\[00:/);

  const stamped = runFetch(["--url", "https://youtu.be/abc123", "--timestamps"], env);
  assert.equal(stamped.status, 0, stamped.stderr);
  assert.match(stamped.stdout, /\[00:00:01\]/);

  const repeatedDedup = runFetch(["--url", "https://youtu.be/abc123", "--json"], { ...env, FAKE_YTDLP_REPEAT: "1" });
  const repeatedNoDedup = runFetch(["--url", "https://youtu.be/abc123", "--json", "--no-dedup"], { ...env, FAKE_YTDLP_REPEAT: "1" });
  assert.equal(repeatedDedup.status, 0, repeatedDedup.stderr);
  assert.equal(repeatedNoDedup.status, 0, repeatedNoDedup.stderr);
  assert.notEqual(JSON.parse(repeatedDedup.stdout).transcript, JSON.parse(repeatedNoDedup.stdout).transcript);

  const manual = runFetch(["--url", "https://youtu.be/abc123", "--json"], { ...env, FAKE_YTDLP_MANUAL: "1" });
  assert.equal(manual.status, 0, manual.stderr);
  assert.equal(JSON.parse(manual.stdout).auto, false);

  const es = runFetch(["--url", "https://youtu.be/abc123", "--json", "--lang", "es"], { ...env, FAKE_YTDLP_LANG: "es" });
  assert.equal(es.status, 0, es.stderr);
  assert.equal(JSON.parse(es.stdout).lang, "es");

  const noVtt = runFetch(["--url", "https://youtu.be/abc123", "--json"], { ...env, FAKE_YTDLP_NO_VTT: "1" });
  assert.notEqual(noVtt.status, 0);
  assert.equal(noVtt.stdout, "");
  assert.match(noVtt.stderr, /no subtitles available/);

  const nonzero = runFetch(["--url", "https://youtu.be/abc123", "--json"], { ...env, FAKE_YTDLP_CODE: "1", FAKE_YTDLP_STDERR: "HTTP Error 429 in <TMPDIR>\n" });
  assert.equal(nonzero.status, 0, nonzero.stderr);
  assert.match(nonzero.stderr, /warning: yt-dlp exited with code 1/);
  assert.match(nonzero.stderr, /rate-limiting/);
  assert.doesNotMatch(nonzero.stdout, /warning|yt-dlp exited/);
  assert.doesNotMatch(nonzero.stderr, /yt-transcript-|fake-ytdlp-/);
  JSON.parse(nonzero.stdout);

  const tooLarge = runFetch(["--url", "https://youtu.be/abc123", "--json"], { ...env, FAKE_YTDLP_LARGE: "1", YOUTUBE_TRANSCRIPT_TEST_MAX_CHARS: "10" });
  assert.notEqual(tooLarge.status, 0);
  assert.equal(tooLarge.stdout, "");
  assert.match(tooLarge.stderr, /transcript exceeds max output size/);

  const timeout = runFetch(["--url", "https://youtu.be/abc123"], { ...env, FAKE_YTDLP_SLEEP_MS: "200", YOUTUBE_TRANSCRIPT_TEST_TIMEOUT_MS: "20" });
  assert.notEqual(timeout.status, 0);
  assert.equal(timeout.stdout, "");
  assert.match(timeout.stderr, /yt-dlp timed out/);

  const readDirFailure = runFetch(["--url", "https://youtu.be/abc123", "--json"], { ...env, YOUTUBE_TRANSCRIPT_TEST_REMOVE_TEMP_BEFORE_READDIR: "1" });
  assert.notEqual(readDirFailure.status, 0);
  assert.equal(readDirFailure.stdout, "");
  assert.match(readDirFailure.stderr, /could not read temp dir/);
  assert.doesNotMatch(readDirFailure.stderr, /yt-transcript-|fake-ytdlp-|youtube-transcript-native-node|fetch\.mjs/);
  assert.match(readDirFailure.stderr, /<tmp>|<home>/);

  const readVttFailure = runFetch(["--url", "https://youtu.be/abc123", "--json"], { ...env, YOUTUBE_TRANSCRIPT_TEST_REMOVE_VTT_BEFORE_READ: "1" });
  assert.notEqual(readVttFailure.status, 0);
  assert.equal(readVttFailure.stdout, "");
  assert.match(readVttFailure.stderr, /could not read \.vtt file/);
  assert.doesNotMatch(readVttFailure.stderr, /yt-transcript-|fake-ytdlp-|youtube-transcript-native-node|fetch\.mjs/);
  assert.match(readVttFailure.stderr, /<tmp>|<home>/);
});

process.stdout.write("youtube-transcript-native-node offline self-test passed\n");
