import { describe, expect, test } from "bun:test";
import { RateLimiter } from "../../../src/twitter/backends/types";

describe("RateLimiter", () => {
  test("two calls at QPS=10 have total elapsed >= 90ms", async () => {
    const limiter = new RateLimiter(10);
    const start = Date.now();
    await limiter.wait();
    await limiter.wait();
    const elapsed = Date.now() - start;
    expect(elapsed).toBeGreaterThanOrEqual(90);
  });

  test("single call completes immediately", async () => {
    const limiter = new RateLimiter(10);
    const start = Date.now();
    await limiter.wait();
    const elapsed = Date.now() - start;
    // First call should be near-instant (< 50ms)
    expect(elapsed).toBeLessThan(50);
  });
});
