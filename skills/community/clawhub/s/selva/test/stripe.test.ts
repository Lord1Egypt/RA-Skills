import { describe, expect, it } from "vitest";
import { parseExpiry } from "../src/stripe.js";

describe("parseExpiry", () => {
  it("parses two digit year", () => {
    expect(parseExpiry("12/25")).toEqual({ month: 12, year: 2025 });
  });

  it("parses four digit year", () => {
    expect(parseExpiry("01/2031")).toEqual({ month: 1, year: 2031 });
  });

  it("rejects invalid format", () => {
    expect(() => parseExpiry("2025-01")).toThrowError(/Invalid expiry format/);
  });
});
