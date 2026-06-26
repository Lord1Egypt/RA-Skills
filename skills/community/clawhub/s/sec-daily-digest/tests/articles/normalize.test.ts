import { describe, expect, test } from "bun:test";
import { dedupeByUrl, filterByHours, normalizeUrl, applyArchivePenalty } from "../../src/articles/normalize";

describe("normalize helpers", () => {
  test("normalizeUrl strips utm_* parameters", () => {
    const normalized = normalizeUrl("https://example.com/a?utm_source=rss&a=1&utm_medium=email");
    expect(normalized).toContain("a=1");
    expect(normalized.includes("utm_")).toBe(false);
  });

  test("dedupeByUrl keeps first unique normalized url", () => {
    const items = dedupeByUrl([
      { link: "https://example.com/a?utm_source=rss", title: "one" },
      { link: "https://example.com/a", title: "two" },
      { link: "https://example.com/b", title: "three" },
    ]);
    expect(items.length).toBe(2);
    expect(items[0]?.title).toBe("one");
  });

  test("filterByHours keeps recent entries", () => {
    const now = new Date("2026-02-27T12:00:00.000Z");
    const data = [
      { pubDate: new Date("2026-02-27T10:00:00.000Z"), id: 1 },
      { pubDate: new Date("2026-02-25T10:00:00.000Z"), id: 2 },
    ];
    const kept = filterByHours(data, 24, now);
    expect(kept.length).toBe(1);
    expect(kept[0]?.id).toBe(1);
  });
});

describe("applyArchivePenalty", () => {
  test("applies -5 penalty to seen URLs", () => {
    const seen = new Set(["https://example.com/old"]);
    const items = [
      { link: "https://example.com/old", score: 8 },
      { link: "https://example.com/new", score: 8 },
    ];
    const result = applyArchivePenalty(items, seen);
    expect(result[0]?.score).toBe(3);
    expect(result[1]?.score).toBe(8);
  });

  test("score floors at 0 (no negative scores)", () => {
    const seen = new Set(["https://example.com/a"]);
    const items = [{ link: "https://example.com/a", score: 2 }];
    const result = applyArchivePenalty(items, seen);
    expect(result[0]?.score).toBe(0);
  });

  test("does not modify items with unseen URLs", () => {
    const seen = new Set(["https://other.com/x"]);
    const items = [{ link: "https://example.com/a", score: 7 }];
    const result = applyArchivePenalty(items, seen);
    expect(result[0]?.score).toBe(7);
  });

  test("handles UTM-stripped URL matching", () => {
    const seen = new Set(["https://example.com/a"]);
    const items = [{ link: "https://example.com/a?utm_source=rss", score: 6 }];
    // normalizeUrl strips utm_, so this should match
    const result = applyArchivePenalty(items, seen);
    expect(result[0]?.score).toBe(1);
  });
});
