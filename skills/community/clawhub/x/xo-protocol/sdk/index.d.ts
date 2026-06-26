export interface XOClientOptions {
  apiKey: string;
  baseUrl?: string;
}

export interface AuthUrlOptions {
  clientId: string;
  redirectUri: string;
  state: string;
  scopes?: string[];
}

export interface ExchangeCodeOptions {
  code: string;
  clientId: string;
  redirectUri: string;
  clientSecret?: string;
  codeVerifier?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  scope: string;
}

export interface IdentityResult {
  verified: boolean;
  trust_score: number;
  has_minted_sbt: boolean;
  attestations: Array<{ type: string; provider: string; verified: boolean }>;
  member_since: string;
}

export interface ConnectionResult {
  tmp_id: string;
  compatibility_score: number | null;
  topics: string[];
  verified: boolean;
}

export interface ConnectionsSearchResult {
  connections: ConnectionResult[];
  cursor: string | null;
  total: number;
}

export interface ReputationResult {
  tier: "novice" | "bronze" | "silver" | "gold" | "platinum" | "diamond" | "s";
  reputation_score: number;
}

export interface SocialSignalsResult {
  engagement_score: number | null;
  confidence: number;
}

export interface ProfileResult {
  interests: string[];
  topics: string[];
  preferences: Record<string, unknown>;
}

export interface NewsfeedPost {
  post_id: string;
  content: string;
  topics: string[];
  created_at: string;
}

export interface NewsfeedResult {
  posts: NewsfeedPost[];
  cursor: string | null;
  total: number;
}

export interface TrustProfile {
  identity: IdentityResult;
  reputation: ReputationResult;
  socialSignals: SocialSignalsResult;
}

export declare class XOClient {
  constructor(options: XOClientOptions);
  setAccessToken(token: string): void;
  getAuthorizationUrl(options: AuthUrlOptions): string;
  exchangeCode(options: ExchangeCodeOptions): Promise<TokenResponse>;
  verifyIdentity(): Promise<IdentityResult>;
  searchConnections(options?: {
    limit?: number;
    topicIds?: string;
    cursor?: string;
  }): Promise<ConnectionsSearchResult>;
  getReputation(token?: string): Promise<ReputationResult>;
  getSocialSignals(token?: string): Promise<SocialSignalsResult>;
  getProfile(token?: string): Promise<ProfileResult>;
  getNewsfeed(tmpId: string, options?: { limit?: number; cursor?: string }): Promise<NewsfeedResult>;
  getTrustProfile(): Promise<TrustProfile>;
}

export declare class XOError extends Error {
  status: number;
  type: string | null;
}
