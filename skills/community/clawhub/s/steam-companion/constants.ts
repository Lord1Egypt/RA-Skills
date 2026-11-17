export const STEAM_COMPANION_SKILL_NAME = 'steam-companion' as const;
export const STEAM_COMPANION_DISPLAY_NAME = 'Steam Companion' as const;
export const STEAM_COMPANION_VERSION = '1.0.0' as const;

export const STEAM_COMPANION_CAPABILITIES = [
  'profile-management',
  'preference-learning',
  'library-overview',
  'discovery-routing',
  'game-recommendation',
  'wishlist-tracking',
  'achievement-context',
  'game-lookup',
  'setup-verification',
  'review-assistance',
  'recommendation-context',
] as const;

export const STEAM_COMPANION_TOOL_NAMES = [
  'getProfile',
  'updateProfile',
  'syncSteamSnapshot',
  'addFavoriteGame',
  'removeFavoriteGame',
  'addOwnedGame',
  'removeOwnedGame',
  'addWishlistGame',
  'removeWishlistGame',
  'savePreference',
  'saveFeedback',
  'recommendGames',
  'buildRecommendationContext',
  'buildReviewContext',
  'buildLibraryOverviewContext',
  'buildDiscoveryContext',
  'buildWishlistContext',
  'buildAchievementContext',
  'buildGameLookupContext',
  'buildSetupContext',
] as const;

export const STEAM_COMPANION_PROMPT_NAMES = [
  'steam-companion.core',
  'steam-companion.library',
  'steam-companion.discovery',
  'steam-companion.wishlist',
  'steam-companion.achievements',
  'steam-companion.lookup',
  'steam-companion.setup',
  'steam-companion.review',
] as const;

export type SteamCompanionToolName = (typeof STEAM_COMPANION_TOOL_NAMES)[number];
export type SteamCompanionPromptName = (typeof STEAM_COMPANION_PROMPT_NAMES)[number];

export const DEFAULT_RECOMMENDATION_LIMIT = 5;
export const DEFAULT_MAX_LIBRARY_ITEMS = 250;
export const DEFAULT_MAX_RECOMMENDATION_SCORE = 100;
export const DEFAULT_UNPLAYED_THRESHOLD_MINUTES = 60;
export const DEFAULT_ABANDONED_THRESHOLD_MINUTES = 300;

export const RECOMMENDATION_WEIGHTS = {
  favoriteMatch: 12,
  explicitLikeMatch: 10,
  inferredMatch: 6,
  wishlistMatch: 5,
  dislikedPenalty: -20,
  ownedPenalty: -30,
  favoritePenalty: -18,
  lengthMatch: 4,
  priceMatch: 4,
  platformMatch: 3,
  competitiveMatch: 3,
  cooperativeMatch: 3,
  noveltyPenalty: -2,
} as const;
