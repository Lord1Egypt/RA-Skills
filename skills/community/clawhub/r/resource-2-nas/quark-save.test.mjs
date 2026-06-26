import test from "node:test";
import assert from "node:assert/strict";

import {
  applyEnvDefaults,
  buildQuarkSubagentPreview,
  buildSavePayload,
  buildRenamePlan,
  classifyResource,
  normalizeShareItems,
  normalizeContextName,
  parseQuarkFolderUrl,
  parseQuarkShareUrl,
  parseSelection,
  resolveRenamePlan,
  renderShareItemsTable
} from "../scripts/quark-save.mjs";

test("parseQuarkShareUrl extracts share id, passcode, and optional folder fid", () => {
  assert.deepEqual(parseQuarkShareUrl("https://pan.quark.cn/s/bcbd9d24fe5a#/list/share"), {
    pwdId: "bcbd9d24fe5a",
    passcode: "",
    pdirFid: "0"
  });

  assert.deepEqual(
    parseQuarkShareUrl(
      "https://pan.quark.cn/s/abc123?pwd=7788#/list/share/e38b48835b404f8092b2a7e5cc054b0d-%E6%9D%A5%E8%87%AA"
    ),
    {
      pwdId: "abc123",
      passcode: "7788",
      pdirFid: "e38b48835b404f8092b2a7e5cc054b0d"
    }
  );
});

test("parseQuarkFolderUrl extracts destination fid and decoded name", () => {
  assert.deepEqual(
    parseQuarkFolderUrl(
      "https://pan.quark.cn/list#/list/all/e38b48835b404f8092b2a7e5cc054b0d-%E6%9D%A5%E8%87%AA%EF%BC%9A%E5%88%86%E4%BA%AB"
    ),
    {
      fid: "e38b48835b404f8092b2a7e5cc054b0d",
      name: "来自：分享"
    }
  );
});

test("parseQuarkFolderUrl accepts cloud-drive paths for later fid resolution", () => {
  assert.deepEqual(parseQuarkFolderUrl("/备份资源"), {
    fid: "",
    name: "备份资源",
    path: "/备份资源",
    inputType: "path",
    needsResolution: true
  });
});

test("applyEnvDefaults uses configured default Quark save URL", () => {
  const args = applyEnvDefaults(
    {
      shareUrl: "https://pan.quark.cn/s/example",
      toUrl: "",
      cookieEnv: "QUARK_COOKIE"
    },
    {
      QUARK_COOKIE: "cookie-value",
      QUARK_DEFAULT_SAVE_URL: "/备份资源"
    }
  );

  assert.equal(args.toUrl, "/备份资源");
  assert.equal(args.env.QUARK_COOKIE, "cookie-value");
});

test("normalizeShareItems maps Quark detail rows into confirmable resources", () => {
  const items = normalizeShareItems([
    {
      fid: "file-fid",
      share_fid_token: "file-token",
      file_name: "蜘蛛侠.mkv",
      size: 1536,
      dir: false,
      updated_at: 1710000000000
    },
    {
      fid: "dir-fid",
      share_fid_token: "dir-token",
      file_name: "花絮",
      include_items: 2,
      dir: true,
      l_updated_at: 1710100000000
    }
  ]);

  assert.deepEqual(
    items.map((item) => ({
      rank: item.rank,
      fid: item.fid,
      shareFidToken: item.shareFidToken,
      name: item.name,
      isDir: item.isDir,
      sizeLabel: item.sizeLabel,
      itemCount: item.itemCount
    })),
    [
      {
        rank: 1,
        fid: "file-fid",
        shareFidToken: "file-token",
        name: "蜘蛛侠.mkv",
        isDir: false,
        sizeLabel: "1.5 KB",
        itemCount: null
      },
      {
        rank: 2,
        fid: "dir-fid",
        shareFidToken: "dir-token",
        name: "花絮",
        isDir: true,
        sizeLabel: "-",
        itemCount: 2
      }
    ]
  );
});

test("parseSelection supports all, comma lists, and numeric ranges", () => {
  const items = normalizeShareItems([
    { fid: "a", share_fid_token: "ta", file_name: "A" },
    { fid: "b", share_fid_token: "tb", file_name: "B" },
    { fid: "c", share_fid_token: "tc", file_name: "C" }
  ]);

  assert.deepEqual(parseSelection("all", items).map((item) => item.fid), ["a", "b", "c"]);
  assert.deepEqual(parseSelection("1,3", items).map((item) => item.fid), ["a", "c"]);
  assert.deepEqual(parseSelection("2-3", items).map((item) => item.fid), ["b", "c"]);
  assert.throws(() => parseSelection("4", items), /out of range/);
});

test("buildSavePayload uses selected fids and target directory fid", () => {
  const payload = buildSavePayload({
    pwdId: "bcbd9d24fe5a",
    stoken: "share-token",
    destinationFid: "e38b48835b404f8092b2a7e5cc054b0d",
    selectedItems: [
      { fid: "file-fid", shareFidToken: "file-token" },
      { fid: "dir-fid", shareFidToken: "dir-token" }
    ]
  });

  assert.deepEqual(payload, {
    fid_list: ["file-fid", "dir-fid"],
    fid_token_list: ["file-token", "dir-token"],
    to_pdir_fid: "e38b48835b404f8092b2a7e5cc054b0d",
    pwd_id: "bcbd9d24fe5a",
    stoken: "share-token",
    pdir_fid: "0",
    scene: "link"
  });
});

test("renderShareItemsTable outputs a confirmation table", () => {
  const markdown = renderShareItemsTable({
    shareTitle: "蜘蛛侠合集",
    contextName: "蜘蛛侠合集",
    destinationName: "来自：分享",
    items: normalizeShareItems([
      {
        fid: "file-fid",
        share_fid_token: "file-token",
        file_name: "蜘蛛侠.mkv",
        size: 1024,
        dir: false,
        updated_at: 1710000000000
      }
    ])
  });

  assert.match(markdown, /### 夸克分享资源/);
  assert.match(markdown, /目标目录：来自：分享/);
  assert.match(markdown, /资源类型：电影\/合集/);
  assert.match(markdown, /\| 1 \| 文件 \| 蜘蛛侠\.mkv \| 1 KB \| 2024-03-09 \|/);
});

test("buildQuarkSubagentPreview creates structured confirmation payload", () => {
  const items = normalizeShareItems([
    {
      fid: "file-fid",
      share_fid_token: "file-token",
      file_name: "蜘蛛侠.mkv",
      size: 1024,
      dir: false,
      updated_at: 1710000000000
    }
  ]);
  const payload = buildQuarkSubagentPreview({
    args: {
      shareUrl: "https://pan.quark.cn/s/example",
      toUrl: "https://pan.quark.cn/list#/list/all/e38b48835b404f8092b2a7e5cc054b0d-%E5%A4%87%E4%BB%BD",
      dryRun: true
    },
    result: {
      shareTitle: "蜘蛛侠合集",
      contextName: "蜘蛛侠合集",
      destination: { fid: "dest-fid", name: "备份" },
      classification: classifyResource({ resourceType: "collection", contextName: "蜘蛛侠合集", items }),
      items,
      selectedPreview: items,
      renamePlan: []
    }
  });

  assert.equal(payload.provider, "quark");
  assert.equal(payload.mode, "preview");
  assert.equal(payload.nextAction, "confirm_before_save");
  assert.equal(payload.confirmation.source, "https://pan.quark.cn/s/example");
  assert.equal(payload.confirmation.target.pathOrUrl, "https://pan.quark.cn/list#/list/all/e38b48835b404f8092b2a7e5cc054b0d-%E5%A4%87%E4%BB%BD");
  assert.equal(payload.confirmation.selectedItems[0].name, "蜘蛛侠.mkv");
});

test("classifyResource detects series from context and item names", () => {
  const classification = classifyResource({
    contextName: "暗影蜘蛛侠 第一季 完结",
    shareTitle: "暗影蜘蛛.265-HiveWeb",
    items: normalizeShareItems([
      { fid: "a", share_fid_token: "ta", file_name: "Dark.Spider.S01E01.1080p.mkv" }
    ])
  });

  assert.equal(classification.isSeries, true);
  assert.equal(classification.label, "剧集");
  assert.equal(classification.reason, "匹配到剧集/季/集关键词");
});

test("classifyResource respects Agent-provided resource type", () => {
  const classification = classifyResource({
    resourceType: "series",
    contextName: "你的友好邻居蜘蛛侠",
    shareTitle: "你的友好邻居蜘蛛侠"
  });

  assert.equal(classification.isSeries, true);
  assert.equal(classification.label, "剧集");
  assert.equal(classification.reason, "Agent 根据上下文判定为剧集");
});

test("normalizeContextName cleans evasive separators in resource titles", () => {
  assert.equal(normalizeContextName("N 你的丨友好邻丨居蜘丨蛛侠 第一季"), "你的友好邻居蜘蛛侠 第一季");
});

test("buildRenamePlan uses context name and episode labels for saved files", () => {
  const items = normalizeShareItems([
    { fid: "a", share_fid_token: "ta", file_name: "Dark.Spider.S01E01.1080p.mkv" },
    { fid: "b", share_fid_token: "tb", file_name: "Dark.Spider.S01E02.1080p.mkv" }
  ]);
  const plan = buildRenamePlan({
    contextName: "暗影蜘蛛侠 第一季",
    shareTitle: "暗影蜘蛛.265-HiveWeb",
    selectedItems: items,
    savedFids: ["saved-a", "saved-b"]
  });

  assert.deepEqual(plan, [
    {
      fid: "saved-a",
      originalName: "Dark.Spider.S01E01.1080p.mkv",
      suggestedName: "暗影蜘蛛侠 第一季 S01E01.mkv",
      reason: "按上下文资源名修正剧集文件名"
    },
    {
      fid: "saved-b",
      originalName: "Dark.Spider.S01E02.1080p.mkv",
      suggestedName: "暗影蜘蛛侠 第一季 S01E02.mkv",
      reason: "按上下文资源名修正剧集文件名"
    }
  ]);
});

test("resolveRenamePlan applies Agent-provided rename decisions by selected index", () => {
  const items = normalizeShareItems([
    { fid: "a", share_fid_token: "ta", file_name: "raw.folder", dir: true },
    { fid: "b", share_fid_token: "tb", file_name: "bonus.mkv" }
  ]);
  const plan = resolveRenamePlan({
    selectedItems: items,
    savedFids: ["saved-a", "saved-b"],
    agentRenamePlan: [
      {
        index: 1,
        name: "你的友好邻居蜘蛛侠 第一季",
        reason: "Agent 根据搜索上下文修正规避字符和季名"
      }
    ]
  });

  assert.deepEqual(plan, [
    {
      fid: "saved-a",
      originalName: "raw.folder",
      suggestedName: "你的友好邻居蜘蛛侠 第一季",
      reason: "Agent 根据搜索上下文修正规避字符和季名"
    }
  ]);
});
