export type DataSourceMode = 'user_only' | 'partial_enriched' | 'fully_enriched';

export type DecisionMode = 'compare' | 'single_judgement' | 'need_driven';

export type UserIntent =
  | 'buy_now'
  | 'compare_only'
  | 'worth_it'
  | 'find_direction'
  | 'undecided';

export type CandidateSource =
  | 'taobao'
  | 'tmall'
  | 'jd'
  | 'pdd'
  | 'manual'
  | 'other';

export type ShopType =
  | 'flagship'
  | 'official'
  | 'authorized'
  | 'marketplace'
  | 'individual'
  | 'unknown';

export type PriceLabel =
  | 'list_price'
  | 'discounted'
  | 'coupon_price'
  | 'bundle_price'
  | 'estimated'
  | 'unknown';

export type EvidenceType =
  | 'user_input'
  | 'screenshot_ocr'
  | 'page_parse'
  | 'manual_note'
  | 'review_summary'
  | 'other';

export type RecommendedAction =
  | 'buy_now'
  | 'wait'
  | 'gather_more_info'
  | 'change_direction'
  | 'compare_more';

export interface ShoppingInput {
  query?: string;
  category?: string;
  budget?: {
    min?: number;
    max?: number;
    currency?: string;
  };
  scenario?: string;
  priorities?: string[];
  decision_mode?: DecisionMode;
  items?: InputItem[];
  notes?: string;
}

export interface InputItem {
  url?: string;
  title?: string;
  source?: CandidateSource;
  screenshot_path?: string;
  raw_text?: string;
  price_hint?: number;
}

export interface ShoppingContext {
  query: Query;
  candidates: Candidate[];
  market_context?: MarketContext;
  meta: Meta;
}

export interface Query {
  category?: string;
  budget?: Budget;
  scenario?: string;
  priorities?: string[];
  decision_mode: DecisionMode;
  user_intent?: UserIntent;
  notes?: string;
}

export interface Budget {
  min?: number;
  max?: number;
  currency?: string;
  flexible?: boolean;
}

export interface Candidate {
  id: string;
  title: string;
  source: CandidateSource;
  url?: string;
  brand?: string;
  model?: string;
  variant?: string;
  price?: Price;
  seller?: Seller;
  specs?: Record<string, string | number | boolean | null>;
  bundle?: Bundle;
  strengths?: string[];
  risks?: string[];
  fit_tags?: string[];
  evidence?: Evidence[];
  confidence?: number;
}

export interface Price {
  list_price?: number;
  final_price?: number;
  currency?: string;
  price_label?: PriceLabel;
  captured_at?: string;
}

export interface Seller {
  shop_name?: string;
  shop_type?: ShopType;
  platform_flags?: string[];
  after_sales_summary?: string;
}

export interface Bundle {
  includes?: string[];
  notes?: string;
  bundle_risk?: string;
}

export interface Evidence {
  type: EvidenceType;
  value: string;
  source_ref?: string;
}

export interface MarketContext {
  category_baseline?: CategoryBaseline;
  timing?: Timing;
}

export interface CategoryBaseline {
  typical_price_band?: [number, number];
  common_tradeoffs?: string[];
}

export interface Timing {
  promotion_sensitive?: boolean;
  note?: string;
}

export interface Meta {
  data_source_mode: DataSourceMode;
  adapter?: string;
  generated_at?: string;
  missing_fields?: string[];
  warnings?: string[];
}

export interface DecisionReport {
  summary: Summary;
  rankings?: Rankings;
  price_explanations?: PriceExplanation[];
  pitfalls?: string[];
  alternative_directions?: string[];
  missing_info?: string[];
  candidate_summaries?: CandidateSummary[];
}

export interface Summary {
  worth_buying?: boolean | null;
  confidence?: number;
  decision: string;
  recommended_action?: RecommendedAction;
}

export interface Rankings {
  lowest_price?: string;
  best_after_sales?: string;
  best_value?: string;
  best_fit?: string;
}

export interface PriceExplanation {
  pair: [string, string];
  reason: string;
  worth_paying?: boolean | null;
}

export interface CandidateSummary {
  candidate_id: string;
  pros?: string[];
  cons?: string[];
  best_for?: string;
  not_ideal_for?: string;
}
