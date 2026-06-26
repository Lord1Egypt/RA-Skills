import test from "node:test";
import assert from "node:assert/strict";

import {
  buildSearchQueryParams,
  normalizeCheckLinksResponse,
  normalizePanSouSearchResponse,
  parseArgs,
  renderMarkdownTable
} from "../scripts/search-rrdynb.mjs";

test("parseArgs defaults search to Baidu and Quark with a 50 candidate cap", () => {
  const args = parseArgs(["蜘蛛侠"]);

  assert.equal(args.title, "蜘蛛侠");
  assert.equal(args.maxCandidates, 50);
  assert.deepEqual(args.cloudTypes, ["baidu", "quark"]);
});

test("buildSearchQueryParams serializes PanSou GET parameters", () => {
  const params = buildSearchQueryParams({
    title: "蜘蛛侠",
    cloudTypes: ["quark", "baidu"],
    plugins: ["wanou"],
    channels: ["tgsearchers4"],
    include: ["合集", "4K"],
    exclude: ["预告"],
    refresh: true,
    resultType: "merge",
    sourceType: "all",
    concurrency: 12,
    ext: { title_en: "Spider-Man" }
  });

  assert.equal(params.get("kw"), "蜘蛛侠");
  assert.equal(params.get("cloud_types"), "quark,baidu");
  assert.equal(params.get("plugins"), "wanou");
  assert.equal(params.get("channels"), "tgsearchers4");
  assert.equal(params.get("refresh"), "true");
  assert.equal(params.get("res"), "merge");
  assert.equal(params.get("src"), "all");
  assert.equal(params.get("conc"), "12");
  assert.equal(params.get("filter"), JSON.stringify({ include: ["合集", "4K"], exclude: ["预告"] }));
  assert.equal(params.get("ext"), JSON.stringify({ title_en: "Spider-Man" }));
});

test("normalizePanSouSearchResponse defaults to Baidu and Quark results only", () => {
  const normalized = normalizePanSouSearchResponse(
    {
      data: {
        total: 4,
        merged_by_type: {
          aliyun: [{ url: "https://www.aliyundrive.com/s/aliyun-id", note: "阿里结果" }],
          baidu: [{ url: "https://pan.baidu.com/s/baidu-id?pwd=8888", password: "8888", note: "百度结果" }],
          magnet: [{ url: "magnet:?xt=urn:btih:example", note: "磁力结果" }],
          quark: [{ url: "https://pan.quark.cn/s/quark-id", note: "夸克结果" }]
        }
      }
    },
    { title: "蜘蛛侠" }
  );

  assert.equal(normalized.returnedCount, 2);
  assert.deepEqual(normalized.candidates.map((candidate) => candidate.diskType), ["baidu", "quark"]);
});

test("normalizePanSouSearchResponse converts merged_by_type into candidates and downloadLinks", () => {
  const normalized = normalizePanSouSearchResponse(
    {
      code: 0,
      message: "success",
      data: {
        total: 3,
        merged_by_type: {
          quark: [
            {
              url: "https://pan.quark.cn/s/quark-id",
              password: "",
              note: "蜘蛛侠：纵横宇宙 4K",
              datetime: "2026-01-01T00:00:00Z",
              source: "plugin:wanou"
            }
          ],
          baidu: [
            {
              url: "https://pan.baidu.com/s/baidu-id?pwd=8888",
              password: "8888",
              note: "蜘蛛侠合集",
              datetime: "2025-01-01T00:00:00Z",
              source: "tg:movies"
            }
          ]
        }
      }
    },
    { title: "蜘蛛侠", selectedQuery: "蜘蛛侠", maxCandidates: 2 }
  );

  assert.equal(normalized.ok, true);
  assert.equal(normalized.availableTotal, 3);
  assert.equal(normalized.returnedCount, 2);
  assert.equal(normalized.total, 2);
  assert.deepEqual(
    normalized.candidates.map((candidate) => ({
      rank: candidate.rank,
      name: candidate.name,
      provider: candidate.provider,
      url: candidate.downloadLinks[0].url,
      extractionCode: candidate.downloadLinks[0].extractionCode,
      source: candidate.source
    })),
    [
      {
        rank: 1,
        name: "蜘蛛侠：纵横宇宙 4K",
        provider: "夸克网盘",
        url: "https://pan.quark.cn/s/quark-id",
        extractionCode: null,
        source: "plugin:wanou"
      },
      {
        rank: 2,
        name: "蜘蛛侠合集",
        provider: "百度网盘",
        url: "https://pan.baidu.com/s/baidu-id?pwd=8888",
        extractionCode: "8888",
        source: "tg:movies"
      }
    ]
  );
  assert.equal(normalized.downloadLinks.length, 2);
});

test("normalizePanSouSearchResponse prefers ranked results over grouped links", () => {
  const normalized = normalizePanSouSearchResponse(
    {
      data: {
        total: 2,
        results: [
          {
            title: "最相关的蜘蛛侠资源",
            channel: "ranked",
            datetime: "2026-02-01T00:00:00Z",
            links: [
              {
                type: "quark",
                url: "https://pan.quark.cn/s/ranked",
                password: "",
                work_title: "最相关的蜘蛛侠资源"
              }
            ]
          }
        ],
        merged_by_type: {
          baidu: [
            {
              url: "https://pan.baidu.com/s/grouped",
              password: "1234",
              note: "分组里的第一条"
            }
          ]
        }
      }
    },
    { title: "蜘蛛侠", maxCandidates: 1 }
  );

  assert.equal(normalized.candidates[0].provider, "夸克网盘");
  assert.equal(normalized.candidates[0].name, "最相关的蜘蛛侠资源");
});

test("normalizePanSouSearchResponse filters ranked results by requested cloud types", () => {
  const normalized = normalizePanSouSearchResponse(
    {
      data: {
        total: 2,
        results: [
          {
            title: "混合网盘结果",
            links: [
              { type: "uc", url: "https://drive.uc.cn/s/uc-id", password: "", work_title: "UC结果" },
              { type: "quark", url: "https://pan.quark.cn/s/quark-id", password: "", work_title: "夸克结果" }
            ]
          }
        ]
      }
    },
    { title: "蜘蛛侠", maxCandidates: 20, cloudTypes: ["quark"] }
  );

  assert.equal(normalized.returnedCount, 1);
  assert.equal(normalized.candidates[0].provider, "夸克网盘");
});

test("normalizeCheckLinksResponse unwraps link check state", () => {
  const normalized = normalizeCheckLinksResponse({
    code: 0,
    message: "success",
    data: {
      results: [
        {
          disk_type: "quark",
          url: "https://pan.quark.cn/s/quark-id",
          normalized_url: "https://pan.quark.cn/s/quark-id",
          state: "ok",
          cache_hit: false,
          checked_at: 1710000000000,
          expires_at: 1710086400000,
          summary: "链接有效"
        }
      ]
    }
  });

  assert.deepEqual(normalized, {
    ok: true,
    results: [
      {
        provider: "夸克网盘",
        diskType: "quark",
        url: "https://pan.quark.cn/s/quark-id",
        normalizedUrl: "https://pan.quark.cn/s/quark-id",
        state: "ok",
        cacheHit: false,
        checkedAt: 1710000000000,
        expiresAt: 1710086400000,
        summary: "链接有效"
      }
    ]
  });
});

test("renderMarkdownTable outputs ranked clickable resource rows", () => {
  const markdown = renderMarkdownTable({
    inputTitle: "蜘蛛侠",
    availableTotal: 30,
    returnedCount: 2,
    candidates: [
      {
        rank: 1,
        name: "蜘蛛侠：纵横宇宙",
        provider: "夸克网盘",
        diskType: "quark",
        datetime: "2026-01-01T00:00:00Z",
        source: "plugin:wanou",
        downloadLinks: [
          {
            provider: "夸克网盘",
            diskType: "quark",
            url: "https://pan.quark.cn/s/quark-id",
            extractionCode: null,
            source: "plugin:wanou",
            datetime: "2026-01-01T00:00:00Z"
          }
        ]
      },
      {
        rank: 2,
        name: "蜘蛛侠合集",
        provider: "百度网盘",
        diskType: "baidu",
        datetime: "2025-01-01T00:00:00Z",
        source: "tg:movies",
        downloadLinks: [
          {
            provider: "百度网盘",
            diskType: "baidu",
            url: "https://pan.baidu.com/s/baidu-id?pwd=8888",
            extractionCode: "8888",
            source: "tg:movies",
            datetime: "2025-01-01T00:00:00Z"
          }
        ]
      }
    ]
  });

  assert.match(markdown, /按 PanSou 相关度排序/);
  assert.match(markdown, /\| 1 \| 蜘蛛侠：纵横宇宙 \| 夸克网盘 \| \[打开\]\(https:\/\/pan\.quark\.cn\/s\/quark-id\) \| - \| plugin:wanou \| 2026-01-01 \|/);
  assert.match(markdown, /\| 2 \| 蜘蛛侠合集 \| 百度网盘 \| \[打开\]\(https:\/\/pan\.baidu\.com\/s\/baidu-id\?pwd=8888\) \| 8888 \| tg:movies \| 2025-01-01 \|/);
});
