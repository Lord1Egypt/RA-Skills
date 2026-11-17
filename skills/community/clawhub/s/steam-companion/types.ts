export interface GameIdentifier {
  appId?: number;
  name: string;
}

export type SteamDeckCompatibility = 'verified' | 'playable' | 'unsupported' | 'unknown';

export interface Game extends GameIdentifier {
  genres: string[];
  tags: string[];
  platforms: string[];
  playtimeHours?: number;
  playtimeMinutes?: number;
  playtime2WeeksMinutes?: number;
  priceCents?: number;
  currency?: string;
  releaseYear?: number;
  releaseDate?: string;
  storeUrl?: string;
  notes?: string;
  summary?: string;
  reviewScore?: number;
  reviewDescription?: string;
  deckCompatibility?: SteamDeckCompatibility;
  developer?: string;
  publisher?: string;
}

export type WishlistPriority = 'low' | 'medium' | 'high';

export type PreferenceKind =
  | 'genre'
  | 'mood'
  | 'length'
  | 'difficulty'
  | 'price'
  | 'playerCount'
  | 'pace'
  | 'platform'
  | 'mechanic'
  | 'narrative'
  | 'coop'
  | 'competitive'
  | 'note';

export type PreferenceSignal = 'like' | 'dislike' | 'neutral';
export type PreferenceSource = 'explicit' | 'inferred' | 'review' | 'playtime' | 'wishlist' | 'library';

export interface UserPreference {
  id: string;
  kind: PreferenceKind;
  value: string;
  signal: PreferenceSignal;
  weight: number;
  source: PreferenceSource;
  note?: string;
  observedAt: string;
  updatedAt: string;
}

export interface WishlistItem {
  id: string;
  game: Game;
  desiredPriceCents?: number;
  currency?: string;
  priority: WishlistPriority;
  addedAt: string;
  reason?: string;
}

export interface Recommendation {
  game: Game;
  score: number;
  confidence: number;
  reasons: string[];
  tradeoffs: string[];
  matchedPreferences: UserPreference[];
}

export interface SteamProfile {
  userId: string;
  displayName?: string;
  favoriteGames: Game[];
  ownedGames: Game[];
  dislikedGames: Game[];
  wishlist: WishlistItem[];
  preferences: UserPreference[];
  notes: string[];
  createdAt: string;
  updatedAt: string;
}

export interface SteamProfilePatch {
  displayName?: string;
  favoriteGames?: Game[];
  ownedGames?: Game[];
  dislikedGames?: Game[];
  wishlist?: WishlistItem[];
  preferences?: UserPreference[];
  notes?: string[];
}

export interface SteamLibrarySnapshot {
  displayName?: string;
  ownedGames?: Game[];
  favoriteGames?: Game[];
  dislikedGames?: Game[];
  wishlist?: WishlistItem[];
  preferences?: UserPreference[];
  notes?: string[];
  summary?: string;
  lastSyncedAt?: string;
}

export interface SteamFeedback {
  game?: Game | GameIdentifier;
  gameName?: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  reasons?: string[];
  notes?: string;
  inferredPreferences?: Array<
    Pick<UserPreference, 'kind' | 'value' | 'signal' | 'weight' | 'source' | 'note'>
  >;
  source?: PreferenceSource;
}

export interface RecommendationOptions {
  limit?: number;
  includeOwned?: boolean;
  includeFavorites?: boolean;
  includeWishlist?: boolean;
  includeDisliked?: boolean;
}

export interface RecommendationContext {
  profile: SteamProfile;
  summary: string;
  preferenceSummary: string[];
  librarySummary: string[];
  exclusionSummary: string[];
  recommendationRules: string[];
  candidateRecommendations: Recommendation[];
}

export interface SteamDiscoveryContext {
  profile: SteamProfile;
  summary: string;
  mood?: string;
  timeAvailable?: string;
  focusSignals: string[];
  recommendationRules: string[];
  candidateRecommendations: Recommendation[];
}

export interface SteamLibraryOverviewContext {
  profile: SteamProfile;
  summary: string;
  totalGames: number;
  playedCount: number;
  abandonedCount: number;
  unplayedCount: number;
  totalLifetimeHours: number;
  topPlayedGames: Game[];
  backlog: Game[];
  abandonedGames: Game[];
  recentlyActiveGames: Game[];
  nextActions: string[];
}

export interface SteamWishlistSaleItem {
  appId?: number;
  name: string;
  discountPercent: number;
  salePriceCents: number;
  originalPriceCents: number;
  reviewScore?: number;
  reviewDescription?: string;
  storeUrl?: string;
  priority?: WishlistPriority;
}

export interface SteamWishlistContext {
  profile: SteamProfile;
  summary: string;
  totalWishlistCount: number;
  saleItems: SteamWishlistSaleItem[];
  topWishlisted: WishlistItem[];
  nextActions: string[];
}

export interface SteamAchievementEntry {
  apiName: string;
  displayName: string;
  description?: string;
  unlocked: boolean;
  unlockTime?: string;
  hidden?: boolean;
}

export interface SteamAchievementProgress {
  appId?: number;
  gameName: string;
  unlockedCount: number;
  totalCount: number;
  completionPct: number;
  recentUnlocked: SteamAchievementEntry[];
  locked: SteamAchievementEntry[];
  hiddenLockedCount: number;
  privateData?: boolean;
}

export interface SteamAchievementContext {
  profile: SteamProfile;
  game: Game;
  summary: string;
  progress: SteamAchievementProgress;
  highlightPoints: string[];
  cautionPoints: string[];
  nextGoals: string[];
  spoilerGuardrails: string[];
}

export interface SteamGameLookupContext {
  profile: SteamProfile;
  game: Game;
  summary: string;
  highlights: string[];
  cautions: string[];
  sourceNotes: string[];
}

export interface SteamSetupCheck {
  steamApiKeyConfigured: boolean;
  libraryAccessible: boolean;
  wishlistAccessible: boolean;
  achievementsAccessible: boolean;
  igdbConfigured: boolean;
  notes?: string[];
}

export interface SteamSetupContext {
  profile: SteamProfile;
  summary: string;
  checks: string[];
  nextSteps: string[];
  troubleshooting: string[];
}

export interface ReviewContext {
  profile: SteamProfile;
  game: Game;
  summary: string;
  highlightPoints: string[];
  cautionPoints: string[];
  reviewAngles: string[];
  spoilerGuardrails: string[];
}

export interface SteamCompanionToolSchema {
  type: 'object';
  properties: Record<string, unknown>;
  required?: string[];
  additionalProperties?: boolean;
}

export interface SteamCompanionToolDefinition<TInput extends object, TOutput> {
  name: string;
  description: string;
  inputSchema: SteamCompanionToolSchema;
  execute(input: TInput): Promise<TOutput>;
}

export interface SteamCompanionManifestPrompt {
  name: string;
  description: string;
  template: string;
}

export interface SteamCompanionManifestTool {
  name: string;
  description: string;
}

export interface SteamCompanionManifest {
  name: string;
  displayName: string;
  description: string;
  version: string;
  capabilities: readonly string[];
  exportedTools: SteamCompanionManifestTool[];
  exportedPrompts: SteamCompanionManifestPrompt[];
}
