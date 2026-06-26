import type { TwitterSourceConfig } from "../../config/sources";
import type { TweetArticle } from "../types";

export type { TweetMetrics } from "../types";

export interface TwitterSourceResult {
  sourceId: string;
  handle: string;
  status: "ok" | "error";
  count: number;
  tweets: TweetArticle[];
  error?: string;
}

export interface TwitterBackend {
  fetch(sources: TwitterSourceConfig[], cutoff: Date): Promise<TwitterSourceResult[]>;
}

export class RateLimiter {
  private qps: number;
  private lastCallTime = 0;

  constructor(qps: number) {
    this.qps = qps;
  }

  async wait(): Promise<void> {
    const minInterval = 1000 / this.qps;
    const now = Date.now();
    const elapsed = now - this.lastCallTime;
    if (elapsed < minInterval) {
      await new Promise<void>((resolve) => setTimeout(resolve, minInterval - elapsed));
    }
    this.lastCallTime = Date.now();
  }
}
