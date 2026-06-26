import test from "node:test";
import assert from "node:assert/strict";

import {
  applyEnvDefaults,
  buildBaiduSubagentPreview,
  buildBaiduTransferRequest,
  extractBaiduShareContextFromHtml,
  normalizeBaiduShareItems,
  parseBaiduSavePath,
  parseBaiduShareUrl,
  renderBaiduShareItemsTable
} from "../scripts/baidu-save.mjs";

test("parseBaiduShareUrl extracts feature string, verify surl, and passcode", () => {
  assert.deepEqual(parseBaiduShareUrl("https://pan.baidu.com/s/1abcDEF?pwd=8888#/list/share"), {
    featureStr: "1abcDEF",
    verifySurl: "abcDEF",
    passcode: "8888",
    sharePageUrl: "https://pan.baidu.com/s/1abcDEF"
  });

  assert.deepEqual(parseBaiduShareUrl("https://pan.baidu.com/share/init?surl=xyz789&pwd=1234"), {
    featureStr: "1xyz789",
    verifySurl: "xyz789",
    passcode: "1234",
    sharePageUrl: "https://pan.baidu.com/s/1xyz789"
  });
});

test("applyEnvDefaults uses configured Baidu cookie and default save path", () => {
  const args = applyEnvDefaults(
    {
      shareUrl: "https://pan.baidu.com/s/1abcDEF?pwd=8888",
      savePath: "",
      cookieEnv: "BAIDU_COOKIE"
    },
    {
      BAIDU_COOKIE: "BDUSS=abc; STOKEN=def",
      BAIDU_DEFAULT_SAVE_PATH: "/我的资源/影视"
    }
  );

  assert.equal(args.savePath, "/我的资源/影视");
  assert.equal(args.env.BAIDU_COOKIE, "BDUSS=abc; STOKEN=def");
});

test("parseBaiduSavePath decodes Baidu folder URLs and keeps direct paths", () => {
  assert.equal(parseBaiduSavePath("/NAS资源下载"), "/NAS资源下载");
  assert.equal(
    parseBaiduSavePath(
      "https://pan.baidu.com/disk/main#/index?category=all&path=%2FNAS%E8%B5%84%E6%BA%90%E4%B8%8B%E8%BD%BD"
    ),
    "/NAS资源下载"
  );
});

test("applyEnvDefaults normalizes Baidu default save URL into cloud-drive path", () => {
  const args = applyEnvDefaults(
    {
      shareUrl: "https://pan.baidu.com/s/1abcDEF?pwd=8888",
      savePath: "",
      cookieEnv: "BAIDU_COOKIE"
    },
    {
      BAIDU_COOKIE: "BDUSS=abc; STOKEN=def",
      BAIDU_DEFAULT_SAVE_PATH:
        "https://pan.baidu.com/disk/main#/index?category=all&path=%2FNAS%E8%B5%84%E6%BA%90%E4%B8%8B%E8%BD%BD"
    }
  );

  assert.equal(args.savePath, "/NAS资源下载");
});

test("extractBaiduShareContextFromHtml reads transfer tokens and share files", () => {
  const context = extractBaiduShareContextFromHtml(`
<script>
window.yunData.setData({"loginstate":1,"bdstoken":"bd-token","shareid":12345,"share_uk":67890,"file_list":[{"fs_id":111,"server_filename":"蜘蛛侠.mkv","isdir":0,"size":2048,"server_mtime":1710000000}]});
</script>
`);

  assert.equal(context.bdstoken, "bd-token");
  assert.equal(context.shareId, "12345");
  assert.equal(context.shareUk, "67890");
  assert.equal(context.files[0].fs_id, 111);
});

test("extractBaiduShareContextFromHtml supports current yunData and locals.mset page shape", () => {
  const context = extractBaiduShareContextFromHtml(`
<script>
window.yunData={skinName:'white', neglect:1, bdstoken:'bd-token', uk:'4267601248', loginstate:'1', share_uk:"987654321", shareid:"12345678901"};
locals.mset({"bdstoken":"bd-token","share_uk":"987654321","shareid":12345678901,"file_list":[{"fs_id":756464633449793,"server_filename":"暗影蜘蛛","isdir":1,"size":0,"server_mtime":1779892650}]});
</script>
`);

  assert.equal(context.bdstoken, "bd-token");
  assert.equal(context.shareId, "12345678901");
  assert.equal(context.shareUk, "987654321");
  assert.equal(context.files[0].server_filename, "暗影蜘蛛");
});

test("normalizeBaiduShareItems maps share rows into confirmable resources", () => {
  const items = normalizeBaiduShareItems([
    {
      fs_id: 111,
      server_filename: "蜘蛛侠.mkv",
      isdir: 0,
      size: 1536,
      server_mtime: 1710000000
    },
    {
      fs_id: 222,
      server_filename: "花絮",
      isdir: 1,
      size: 0,
      server_mtime: 1710100000
    }
  ]);

  assert.deepEqual(
    items.map((item) => ({
      rank: item.rank,
      fsId: item.fsId,
      name: item.name,
      isDir: item.isDir,
      sizeLabel: item.sizeLabel,
      updatedAtLabel: item.updatedAtLabel
    })),
    [
      {
        rank: 1,
        fsId: 111,
        name: "蜘蛛侠.mkv",
        isDir: false,
        sizeLabel: "1.5 KB",
        updatedAtLabel: "2024-03-09"
      },
      {
        rank: 2,
        fsId: 222,
        name: "花絮",
        isDir: true,
        sizeLabel: "-",
        updatedAtLabel: "2024-03-10"
      }
    ]
  );
});

test("buildBaiduTransferRequest creates a share transfer request", () => {
  const request = buildBaiduTransferRequest({
    apiBase: "https://pan.baidu.com",
    bdstoken: "bd-token",
    shareId: "12345",
    shareUk: "67890",
    savePath: "/我的资源/影视",
    selectedItems: [
      { fsId: 111 },
      { fsId: 222 }
    ]
  });

  assert.equal(request.url.origin, "https://pan.baidu.com");
  assert.equal(request.url.pathname, "/share/transfer");
  assert.equal(request.url.searchParams.get("shareid"), "12345");
  assert.equal(request.url.searchParams.get("from"), "67890");
  assert.equal(request.url.searchParams.get("bdstoken"), "bd-token");
  assert.equal(request.url.searchParams.get("ondup"), "newcopy");
  assert.equal(request.body.get("fsidlist"), "[111,222]");
  assert.equal(request.body.get("path"), "/我的资源/影视");
});

test("buildBaiduTransferRequest normalizes Baidu folder URL save path", () => {
  const request = buildBaiduTransferRequest({
    bdstoken: "bd-token",
    shareId: "12345",
    shareUk: "67890",
    savePath: "https://pan.baidu.com/disk/main#/index?category=all&path=%2FNAS%E8%B5%84%E6%BA%90%E4%B8%8B%E8%BD%BD",
    selectedItems: [{ fsId: 111 }]
  });

  assert.equal(request.body.get("path"), "/NAS资源下载");
});

test("renderBaiduShareItemsTable outputs a confirmation table", () => {
  const markdown = renderBaiduShareItemsTable({
    shareTitle: "蜘蛛侠合集",
    contextName: "蜘蛛侠合集",
    savePath: "/我的资源/影视",
    items: normalizeBaiduShareItems([
      {
        fs_id: 111,
        server_filename: "蜘蛛侠.mkv",
        isdir: 0,
        size: 1024,
        server_mtime: 1710000000
      }
    ])
  });

  assert.match(markdown, /### 百度网盘分享资源/);
  assert.match(markdown, /目标目录：\/我的资源\/影视/);
  assert.match(markdown, /资源类型：电影\/合集/);
  assert.match(markdown, /\| 1 \| 文件 \| 蜘蛛侠\.mkv \| 1 KB \| 2024-03-09 \|/);
});

test("buildBaiduSubagentPreview creates structured confirmation payload", () => {
  const items = normalizeBaiduShareItems([
    {
      fs_id: 111,
      server_filename: "暗影蜘蛛",
      isdir: 1,
      size: 0,
      server_mtime: 1710000000
    }
  ]);
  const payload = buildBaiduSubagentPreview({
    args: {
      shareUrl: "https://pan.baidu.com/s/1abcDEF?pwd=8888",
      savePath: "/NAS资源下载",
      dryRun: true
    },
    result: {
      shareTitle: "暗影蜘蛛",
      contextName: "暗影蜘蛛",
      savePath: "/NAS资源下载",
      classification: {
        type: "collection",
        isSeries: false,
        label: "合集",
        reason: "Agent 根据上下文判定为合集"
      },
      items,
      selectedPreview: items,
      renamePlan: []
    }
  });

  assert.equal(payload.provider, "baidu");
  assert.equal(payload.mode, "preview");
  assert.equal(payload.nextAction, "confirm_before_save");
  assert.equal(payload.confirmation.source, "https://pan.baidu.com/s/1abcDEF?pwd=8888");
  assert.equal(payload.confirmation.target.pathOrUrl, "/NAS资源下载");
  assert.equal(payload.confirmation.selectedItems[0].name, "暗影蜘蛛");
});
