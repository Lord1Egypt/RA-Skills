export type BrandProfile = {
  brand_name: string;
  voice: string;
  tone: string;
  target_audience: string;
  products_services: string[];
  unique_selling_points: string[];
  brand_values: string[];
  geographic_focus: string;
  languages: string[];
  website_url: string;
};

export type GeneratedAd = {
  intent: string;
  hook: string;
  body: string;
  cta: string;
  visual_direction: string;
  why_it_works: string;
  targeting: Record<string, unknown>;
  adset_schedule: unknown[];
};

export const REQUIRED_AD_FIELDS: Array<keyof GeneratedAd> = [
  "intent",
  "hook",
  "body",
  "cta",
  "visual_direction",
  "why_it_works",
  "targeting",
  "adset_schedule",
];

export type ScrapeResult = {
  url: string;
  pages_crawled: number;
  content: string;
};

export type AdTone = "professional" | "funny" | "offensive";

export const AD_TONES: { key: AdTone; label: string; emoji: string }[] = [
  { key: "professional", label: "Professional", emoji: "💼" },
  { key: "funny", label: "Funny", emoji: "😂" },
  { key: "offensive", label: "Offensive / Edgy", emoji: "🔥" },
];

export type NumberedAd = GeneratedAd & {
  number: number;
  tone: AdTone;
};

export type WebsiteToAdsResult = {
  url: string;
  brand: BrandProfile;
  ads: NumberedAd[];
  budget: string;
};

export type CachedBrand = {
  url: string;
  brand: BrandProfile;
  scraped_content: string;
  cached_at: string;
};

export type CivicAuthResult = {
  verified: boolean;
  method?: "civic" | "disabled";
  userId?: string;
  displayName?: string;
  reason?: string;
};
