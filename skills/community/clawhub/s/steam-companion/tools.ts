import type { SteamCompanionToolDefinition } from './types.js';
import type { SteamCompanionService } from './service.js';
import type {
  Game,
  GameIdentifier,
  SteamAchievementProgress,
  Recommendation,
  RecommendationContext,
  ReviewContext,
  SteamSetupCheck,
  SteamLibrarySnapshot,
  SteamFeedback,
  SteamProfilePatch,
  SteamWishlistSaleItem,
  UserPreference,
  WishlistItem,
} from './types.js';
import { STEAM_COMPANION_TOOL_NAMES } from './constants.js';

export interface ToolInputWithUser {
  userId: string;
}

export interface ToolInputWithGame extends ToolInputWithUser {
  game: Game;
}

export interface ToolInputWithGameIdentifier extends ToolInputWithUser {
  game: Game | GameIdentifier;
}

export interface ToolInputWithWishlistItem extends ToolInputWithUser {
  item: WishlistItem;
}

export interface ToolInputWithPreference extends ToolInputWithUser {
  preference: UserPreference;
}

export interface ToolInputWithFeedback extends ToolInputWithUser {
  feedback: SteamFeedback;
}

export interface ToolInputWithRecommendationCandidates extends ToolInputWithUser {
  candidates: Game[];
  limit?: number;
  includeOwned?: boolean;
  includeFavorites?: boolean;
  includeWishlist?: boolean;
  includeDisliked?: boolean;
}

export interface ToolInputWithRecommendationContext extends ToolInputWithUser {
  candidates?: Game[];
  limit?: number;
  includeOwned?: boolean;
  includeFavorites?: boolean;
  includeWishlist?: boolean;
  includeDisliked?: boolean;
}

export interface ToolInputWithReviewContext extends ToolInputWithUser {
  game: Game;
}

export interface ToolInputWithLibraryOverview extends ToolInputWithUser {
  games: Game[];
  topLimit?: number;
  recentLimit?: number;
}

export interface ToolInputWithDiscoveryContext extends ToolInputWithUser {
  candidates?: Game[];
  limit?: number;
  includeOwned?: boolean;
  includeFavorites?: boolean;
  includeWishlist?: boolean;
  includeDisliked?: boolean;
  mood?: string;
  timeAvailable?: string;
}

export interface ToolInputWithWishlistContext extends ToolInputWithUser {
  saleItems?: SteamWishlistSaleItem[];
  wishlist?: WishlistItem[];
  limit?: number;
}

export interface ToolInputWithAchievementContext extends ToolInputWithUser {
  game: Game;
  progress: SteamAchievementProgress;
}

export interface ToolInputWithGameLookup extends ToolInputWithUser {
  game: Game;
  source?: string;
  sourceNotes?: string[];
}

export interface ToolInputWithSetupContext extends ToolInputWithUser {
  check: SteamSetupCheck;
}

export interface ToolInputWithProfilePatch extends ToolInputWithUser {
  patch: SteamProfilePatch;
}

export interface ToolInputWithSteamSnapshot extends ToolInputWithUser {
  snapshot: SteamLibrarySnapshot;
}

export interface SteamCompanionToolSpec {
  name: string;
  description: string;
  inputSchema: {
    type: 'object';
    properties: Record<string, unknown>;
    required?: string[];
    additionalProperties?: boolean;
  };
}

export const steamCompanionToolDefinitions: SteamCompanionToolSpec[] = [
  {
    name: 'getProfile',
    description: 'Read the current Steam Companion profile.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
      },
      required: ['userId'],
      additionalProperties: false,
    },
  },
  {
    name: 'updateProfile',
    description: 'Apply a structured profile patch.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        patch: { type: 'object' },
      },
      required: ['userId', 'patch'],
      additionalProperties: false,
    },
  },
  {
    name: 'syncSteamSnapshot',
    description: 'Merge a Steam snapshot fetched by the steam-mcp MCP server into the local profile.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        snapshot: { type: 'object' },
      },
      required: ['userId', 'snapshot'],
      additionalProperties: false,
    },
  },
  {
    name: 'addFavoriteGame',
    description: 'Add a game to the favorite list.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        game: { type: 'object' },
      },
      required: ['userId', 'game'],
      additionalProperties: false,
    },
  },
  {
    name: 'removeFavoriteGame',
    description: 'Remove a game from the favorite list.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        game: { type: 'object' },
      },
      required: ['userId', 'game'],
      additionalProperties: false,
    },
  },
  {
    name: 'addOwnedGame',
    description: 'Add a game to the owned library.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        game: { type: 'object' },
      },
      required: ['userId', 'game'],
      additionalProperties: false,
    },
  },
  {
    name: 'removeOwnedGame',
    description: 'Remove a game from the owned library.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        game: { type: 'object' },
      },
      required: ['userId', 'game'],
      additionalProperties: false,
    },
  },
  {
    name: 'addWishlistGame',
    description: 'Add a game to the wishlist.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        item: { type: 'object' },
      },
      required: ['userId', 'item'],
      additionalProperties: false,
    },
  },
  {
    name: 'removeWishlistGame',
    description: 'Remove a game from the wishlist.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        game: { type: 'object' },
      },
      required: ['userId', 'game'],
      additionalProperties: false,
    },
  },
  {
    name: 'savePreference',
    description: 'Persist an explicit or inferred preference signal.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        preference: { type: 'object' },
      },
      required: ['userId', 'preference'],
      additionalProperties: false,
    },
  },
  {
    name: 'saveFeedback',
    description: 'Learn from explicit gameplay or review feedback.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        feedback: { type: 'object' },
      },
      required: ['userId', 'feedback'],
      additionalProperties: false,
    },
  },
  {
    name: 'recommendGames',
    description: 'Rank candidate games against the stored profile.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        candidates: { type: 'array' },
        limit: { type: 'number' },
        includeOwned: { type: 'boolean' },
        includeFavorites: { type: 'boolean' },
        includeWishlist: { type: 'boolean' },
        includeDisliked: { type: 'boolean' },
      },
      required: ['userId', 'candidates'],
      additionalProperties: false,
    },
  },
  {
    name: 'buildRecommendationContext',
    description: 'Build structured context for an AI recommendation response.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        candidates: { type: 'array' },
        limit: { type: 'number' },
        includeOwned: { type: 'boolean' },
        includeFavorites: { type: 'boolean' },
        includeWishlist: { type: 'boolean' },
        includeDisliked: { type: 'boolean' },
      },
      required: ['userId'],
      additionalProperties: false,
    },
  },
  {
    name: 'buildReviewContext',
    description: 'Build structured context for writing a Steam review.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        game: { type: 'object' },
      },
      required: ['userId', 'game'],
      additionalProperties: false,
    },
  },
  {
    name: 'buildLibraryOverviewContext',
    description: 'Build structured context for Steam library stats, backlog, and active play.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        games: { type: 'array' },
        topLimit: { type: 'number' },
        recentLimit: { type: 'number' },
      },
      required: ['userId', 'games'],
      additionalProperties: false,
    },
  },
  {
    name: 'buildDiscoveryContext',
    description: 'Build structured context for mood/time-based play recommendations.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        candidates: { type: 'array' },
        limit: { type: 'number' },
        includeOwned: { type: 'boolean' },
        includeFavorites: { type: 'boolean' },
        includeWishlist: { type: 'boolean' },
        includeDisliked: { type: 'boolean' },
        mood: { type: 'string' },
        timeAvailable: { type: 'string' },
      },
      required: ['userId'],
      additionalProperties: false,
    },
  },
  {
    name: 'buildWishlistContext',
    description: 'Build structured context for wishlist sales and priority items.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        saleItems: { type: 'array' },
        wishlist: { type: 'array' },
        limit: { type: 'number' },
      },
      required: ['userId'],
      additionalProperties: false,
    },
  },
  {
    name: 'buildAchievementContext',
    description: 'Build structured context for Steam achievement progress.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        game: { type: 'object' },
        progress: { type: 'object' },
      },
      required: ['userId', 'game', 'progress'],
      additionalProperties: false,
    },
  },
  {
    name: 'buildGameLookupContext',
    description: 'Build structured context for a game lookup or metadata summary.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        game: { type: 'object' },
        source: { type: 'string' },
        sourceNotes: { type: 'array' },
      },
      required: ['userId', 'game'],
      additionalProperties: false,
    },
  },
  {
    name: 'buildSetupContext',
    description: 'Build structured context for Steam setup verification and troubleshooting.',
    inputSchema: {
      type: 'object',
      properties: {
        userId: { type: 'string' },
        check: { type: 'object' },
      },
      required: ['userId', 'check'],
      additionalProperties: false,
    },
  },
];

export function createSteamCompanionToolHandlers(service: SteamCompanionService) {
  return {
    getProfile: ({ userId }: ToolInputWithUser) => service.getProfile(userId),
    updateProfile: ({ userId, patch }: ToolInputWithProfilePatch) => service.updateProfile(userId, patch),
    syncSteamSnapshot: ({ userId, snapshot }: ToolInputWithSteamSnapshot) => service.syncSteamSnapshot(userId, snapshot),
    addFavoriteGame: ({ userId, game }: ToolInputWithGame) => service.addFavoriteGame(userId, game),
    removeFavoriteGame: ({ userId, game }: ToolInputWithGameIdentifier) => service.removeFavoriteGame(userId, game),
    addOwnedGame: ({ userId, game }: ToolInputWithGame) => service.addOwnedGame(userId, game),
    removeOwnedGame: ({ userId, game }: ToolInputWithGameIdentifier) => service.removeOwnedGame(userId, game),
    addWishlistGame: ({ userId, item }: ToolInputWithWishlistItem) => service.addWishlistGame(userId, item),
    removeWishlistGame: ({ userId, game }: ToolInputWithGameIdentifier) => service.removeWishlistGame(userId, game),
    savePreference: ({ userId, preference }: ToolInputWithPreference) => service.savePreference(userId, preference),
    saveFeedback: ({ userId, feedback }: ToolInputWithFeedback) => service.saveFeedback(userId, feedback),
    recommendGames: ({ userId, candidates, limit, includeOwned, includeFavorites, includeWishlist, includeDisliked }: ToolInputWithRecommendationCandidates) =>
      service.recommendGames(userId, candidates, { limit, includeOwned, includeFavorites, includeWishlist, includeDisliked }),
    buildRecommendationContext: ({ userId, candidates = [], limit, includeOwned, includeFavorites, includeWishlist, includeDisliked }: ToolInputWithRecommendationContext) =>
      service.buildRecommendationContext(userId, candidates, { limit, includeOwned, includeFavorites, includeWishlist, includeDisliked }),
    buildReviewContext: ({ userId, game }: ToolInputWithReviewContext) => service.buildReviewContext(userId, game),
    buildLibraryOverviewContext: ({ userId, games, topLimit, recentLimit }: ToolInputWithLibraryOverview) =>
      service.buildLibraryOverviewContext(userId, games, { topLimit, recentLimit }),
    buildDiscoveryContext: ({ userId, candidates = [], limit, includeOwned, includeFavorites, includeWishlist, includeDisliked, mood, timeAvailable }: ToolInputWithDiscoveryContext) =>
      service.buildDiscoveryContext(userId, candidates, { limit, includeOwned, includeFavorites, includeWishlist, includeDisliked, mood, timeAvailable }),
    buildWishlistContext: ({ userId, saleItems = [], wishlist = [], limit }: ToolInputWithWishlistContext) =>
      service.buildWishlistContext(userId, saleItems, wishlist, { limit }),
    buildAchievementContext: ({ userId, game, progress }: ToolInputWithAchievementContext) =>
      service.buildAchievementContext(userId, game, progress),
    buildGameLookupContext: ({ userId, game, source, sourceNotes = [] }: ToolInputWithGameLookup) =>
      service.buildGameLookupContext(userId, game, { source, sourceNotes }),
    buildSetupContext: ({ userId, check }: ToolInputWithSetupContext) =>
      service.buildSetupContext(userId, check),
  } as const;
}

export function createRegisteredSteamCompanionToolDefinitions(service: SteamCompanionService) {
  const handlers = createSteamCompanionToolHandlers(service);

  return steamCompanionToolDefinitions.map((definition) => {
    const name = definition.name as keyof typeof handlers;
    return {
      ...definition,
      execute: handlers[name] as (input: object) => Promise<unknown>,
    } as SteamCompanionToolDefinition<object, unknown>;
  });
}

export const steamCompanionToolCatalog = steamCompanionToolDefinitions.map((definition) => ({
  name: definition.name,
  description: definition.description,
}));

export const steamCompanionToolNames = STEAM_COMPANION_TOOL_NAMES;
