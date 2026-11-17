import assert from "node:assert/strict";
import { mkdir, mkdtemp, rm, symlink, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { readHttpIniPort } from "../zhanfu_http.mjs";

async function withAppData(appdata, fn) {
  const prev = process.env.APPDATA;
  process.env.APPDATA = appdata;
  try {
    return await fn();
  } finally {
    if (prev == null) delete process.env.APPDATA;
    else process.env.APPDATA = prev;
  }
}

test("Http.ini 读不到时才跟随外联", async (t) => {
  if (process.platform !== "win32") {
    t.skip("Http.ini 外联回退以 Windows 目录联接为准");
    return;
  }
  const root = await mkdtemp(path.join(os.tmpdir(), "zhanfu-http-ini-"));
  t.after(() => rm(root, { recursive: true, force: true }));

  const plain = path.join(root, "plain");
  await mkdir(path.join(plain, "ZhanFu"), { recursive: true });
  await withAppData(plain, async () => {
    assert.equal(readHttpIniPort(), null);
    await writeFile(path.join(plain, "ZhanFu", "Http.ini"), "[Common]\nhttpport=12678\n");
    assert.equal(readHttpIniPort(), 12678);
    await writeFile(path.join(plain, "ZhanFu", "Http.ini"), "[Common]\nhttpport=nope\n");
    assert.equal(readHttpIniPort(), null);
  });

  const linkedRoot = path.join(root, "linked");
  const target = path.join(linkedRoot, "other-disk");
  const link = path.join(linkedRoot, "appdata", "ZhanFu");
  await mkdir(target, { recursive: true });
  await mkdir(path.dirname(link), { recursive: true });
  await writeFile(path.join(target, "Http.ini"), "[Common]\nhttpport=23456\n");
  await symlink(target, link, "junction");
  await withAppData(path.dirname(link), async () => {
    assert.equal(readHttpIniPort(), 23456);
  });

  const opaqueRoot = path.join(root, "opaque");
  const opaqueTarget = path.join(opaqueRoot, "moved");
  const opaqueLink = path.join(opaqueRoot, "appdata", "ZhanFu");
  await mkdir(opaqueTarget, { recursive: true });
  await mkdir(path.dirname(opaqueLink), { recursive: true });
  await writeFile(path.join(opaqueTarget, "Http.ini"), "[Common]\nhttpport=34567\n");
  await symlink(`\\??\\${opaqueTarget}`, opaqueLink, "junction");
  await withAppData(path.dirname(opaqueLink), async () => {
    assert.equal(readHttpIniPort(), 34567);
  });

  const emptyRoot = path.join(root, "empty-link");
  const emptyTarget = path.join(emptyRoot, "moved");
  const emptyLink = path.join(emptyRoot, "appdata", "ZhanFu");
  await mkdir(emptyTarget, { recursive: true });
  await mkdir(path.dirname(emptyLink), { recursive: true });
  await symlink(emptyTarget, emptyLink, "junction");
  await withAppData(path.dirname(emptyLink), async () => {
    assert.equal(readHttpIniPort(), null);
  });
});
