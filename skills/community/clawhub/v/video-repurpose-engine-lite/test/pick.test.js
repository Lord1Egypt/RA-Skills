import { test } from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promises as fs } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(new URL("../scripts/pick.js", import.meta.url));
const run = (args) =>
  new Promise((resolve) => {
    execFile(process.execPath, [SCRIPT, ...args], (err, stdout) =>
      resolve({ code: err?.code ?? 0, stdout }),
    );
  });

const SRT = `1
00:00:01,000 --> 00:00:08,000
Welcome back, today we talk about the biggest mistake.

2
00:00:08,000 --> 00:00:15,000
Everyone gets this wrong! Nobody tells you the truth.

3
00:00:15,000 --> 00:00:22,000
Here is exactly what happens when you ignore it.

4
00:00:22,000 --> 00:00:30,000
And then a long boring technical explanation follows.

5
00:02:00,000 --> 00:02:10,000
Remember when we almost lost everything? Story time.

6
00:02:10,000 --> 00:02:25,000
The secret nobody shares: it was never about the money!
`;

test("ranks clip windows with hook scoring", async () => {
  const f = path.join(await fs.mkdtemp(path.join(os.tmpdir(), "vid-")), "t.srt");
  await fs.writeFile(f, SRT);
  const { code, stdout } = await run([f, "--clips", "3", "--min", "5"]);
  assert.equal(code, 0);
  const r = JSON.parse(stdout);
  assert.equal(r.cues, 6);
  assert.ok(r.clips.length > 0 && r.clips.length <= 3);
  assert.ok(r.clips[0].score >= r.clips[r.clips.length - 1].score);
});

test("usage error exits 2", async () => {
  const { code } = await run([]);
  assert.equal(code, 2);
});
