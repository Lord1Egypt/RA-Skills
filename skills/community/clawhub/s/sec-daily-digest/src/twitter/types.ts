import type { Article } from "../rss/parse";
export type { TwitterSourceConfig } from "../config/sources";

export interface TweetMetrics {
  like_count: number;
  retweet_count: number;
  reply_count: number;
  quote_count: number;
  impression_count: number;
}

export interface TweetArticle extends Article {
  tweetId: string;
  handle: string;
  displayName: string;
  metrics: TweetMetrics;
}
