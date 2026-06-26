import { describe, expect, test } from "bun:test";
import { renderDigest, renderKolSection, formatMetric } from "../../src/report/markdown";

describe("renderDigest", () => {
  test("renders key sections for security researchers", () => {
    const markdown = renderDigest({
      date: "2026-02-27",
      highlights: "今日趋势：AI 网关安全成为核心议题。",
      ai: [
        {
          titleZh: "中文标题",
          title: "English title",
          link: "https://example.com/a",
          summaryZh: "中文摘要",
          reasonZh: "推荐理由",
          category: "ai-ml",
          keywords: ["agent"],
          score: 8.5,
          sourceName: "feed-a",
        },
      ],
      security: [],
      vulnerabilities: [
        {
          key: "CVE-2026-12345",
          title: "Major RCE",
          summary: "Impact summary",
          cves: ["CVE-2026-12345"],
          references: [{ source: "feed-a", link: "https://example.com/v1" }],
        },
      ],
    });

    expect(markdown).toContain("## AI发展");
    expect(markdown).toContain("## 安全动态");
    expect(markdown).toContain("## 📝 今日趋势");
    expect(markdown).toContain("## 漏洞专报");
    expect(markdown).toContain("CVE-2026-12345");
    expect(markdown).toContain("[English title](https://example.com/a)");
  });

  test("score uses 🔥 prefix instead of ⭐", () => {
    const markdown = renderDigest({
      date: "2026-02-27",
      highlights: "",
      ai: [
        {
          titleZh: "标题",
          title: "Title",
          link: "https://example.com/a",
          summaryZh: "摘要",
          reasonZh: "",
          category: "ai-ml",
          keywords: [],
          score: 7.4,
          sourceName: "feed",
        },
      ],
      security: [],
      vulnerabilities: [],
    });

    expect(markdown).toContain("🔥7");
    expect(markdown).not.toContain("⭐");
  });

  test("KOL section rendered when kols provided", () => {
    const markdown = renderDigest({
      date: "2026-02-27",
      highlights: "",
      ai: [],
      security: [],
      vulnerabilities: [],
      kols: [
        {
          displayName: "Tavis Ormandy",
          handle: "taviso",
          text: "Found a critical vuln",
          link: "https://twitter.com/taviso/status/123",
          tweetId: "123",
          metrics: { like_count: 500, retweet_count: 200, reply_count: 30, quote_count: 10, impression_count: 12345 },
        },
      ],
    });

    expect(markdown).toContain("## 🔐 Security KOL Updates");
    expect(markdown).toContain("Tavis Ormandy");
    expect(markdown).toContain("@taviso");
  });

  test("KOL section not rendered when kols is empty or undefined", () => {
    const noKols = renderDigest({
      date: "2026-02-27",
      highlights: "",
      ai: [],
      security: [],
      vulnerabilities: [],
    });
    expect(noKols).not.toContain("🔐 Security KOL Updates");

    const emptyKols = renderDigest({
      date: "2026-02-27",
      highlights: "",
      ai: [],
      security: [],
      vulnerabilities: [],
      kols: [],
    });
    expect(emptyKols).not.toContain("🔐 Security KOL Updates");
  });

  test("health warnings rendered when provided", () => {
    const markdown = renderDigest({
      date: "2026-02-27",
      highlights: "",
      ai: [],
      security: [],
      vulnerabilities: [],
      healthWarnings: ["Unhealthy Feed A", "Broken Feed B"],
    });
    expect(markdown).toContain("⚠️ Source Health Warnings");
    expect(markdown).toContain("Unhealthy Feed A");
  });

  test("health warnings not rendered when empty", () => {
    const markdown = renderDigest({
      date: "2026-02-27",
      highlights: "",
      ai: [],
      security: [],
      vulnerabilities: [],
      healthWarnings: [],
    });
    expect(markdown).not.toContain("⚠️ Source Health Warnings");
  });
});

describe("formatMetric", () => {
  test("displays >= 1000 as K with one decimal", () => {
    expect(formatMetric(12345)).toBe("12.3K");
    expect(formatMetric(1000)).toBe("1.0K");
    expect(formatMetric(9999)).toBe("10.0K");
  });

  test("displays < 1000 as-is", () => {
    expect(formatMetric(0)).toBe("0");
    expect(formatMetric(45)).toBe("45");
    expect(formatMetric(999)).toBe("999");
  });
});

describe("renderKolSection", () => {
  test("formats metrics correctly", () => {
    const kols = [
      {
        displayName: "Test User",
        handle: "testuser",
        text: "My tweet",
        link: "https://twitter.com/testuser/status/1",
        tweetId: "1",
        metrics: { like_count: 1200, retweet_count: 230, reply_count: 45, quote_count: 10, impression_count: 12300 },
      },
    ];
    const section = renderKolSection(kols);
    expect(section).toContain("12.3K");
    expect(section).toContain("230");
    expect(section).toContain("45");
    expect(section).toContain("1.2K");
  });

  test("returns empty string for empty array", () => {
    expect(renderKolSection([])).toBe("");
  });
});
