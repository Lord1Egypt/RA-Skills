import {
  DEFAULT_MAX_RECOMMENDATION_SCORE,
  DEFAULT_RECOMMENDATION_LIMIT,
  DEFAULT_ABANDONED_THRESHOLD_MINUTES,
  DEFAULT_UNPLAYED_THRESHOLD_MINUTES,
  RECOMMENDATION_WEIGHTS,
} from './constants.js';
import {
  cloneSteamProfile,
  createEmptySteamProfile,
  mergeGame,
  mergeGameLists,
  mergePreferenceLists,
  mergeStringLists,
  mergeWishlistLists,
  normalizeGameKey,
  normalizePreferenceKey,
  removeGameByIdentifier,
  removeWishlistItemByIdentifier,
  type SteamCompanionRepository,
} from './memory.js';
import type {
  SteamAchievementContext,
  SteamAchievementProgress,
  SteamDiscoveryContext,
  Game,
  GameIdentifier,
  SteamGameLookupContext,
  SteamLibraryOverviewContext,
  Recommendation,
  RecommendationContext,
  RecommendationOptions,
  ReviewContext,
  SteamSetupCheck,
  SteamSetupContext,
  SteamLibrarySnapshot,
  SteamFeedback,
  SteamProfilePatch,
  SteamProfile,
  UserPreference,
  SteamWishlistContext,
  SteamWishlistSaleItem,
  WishlistItem,
} from './types.js';

export interface SteamCompanionServiceOptions {
  clock?: () => Date;
}

export interface SteamLibraryOverviewOptions {
  topLimit?: number;
  recentLimit?: number;
}

export interface SteamDiscoveryOptions extends RecommendationOptions {
  mood?: string;
  timeAvailable?: string;
}

export interface SteamWishlistContextOptions {
  limit?: number;
}

export interface SteamGameLookupOptions {
  source?: string;
  sourceNotes?: string[];
}

export class SteamCompanionService {
  constructor(
    private readonly repository: SteamCompanionRepository,
    private readonly options: SteamCompanionServiceOptions = {},
  ) {}

  async getProfile(userId: string): Promise<SteamProfile> {
    const existing = await this.repository.get(userId);
    if (existing) {
      return existing;
    }

    const profile = createEmptySteamProfile(userId);
    await this.repository.save(profile);
    return cloneSteamProfile(profile) as SteamProfile;
  }

  async updateProfile(userId: string, patch: SteamProfilePatch): Promise<SteamProfile> {
    const profile = await this.getProfile(userId);
    const updated = this.applyProfilePatch(profile, patch);
    await this.repository.save(updated);
    return cloneSteamProfile(updated) as SteamProfile;
  }

  async syncSteamSnapshot(userId: string, snapshot: SteamLibrarySnapshot): Promise<SteamProfile> {
    const profile = await this.getProfile(userId);
    const now = this.now();

    if (snapshot.displayName !== undefined) {
      profile.displayName = snapshot.displayName;
    }

    if (snapshot.ownedGames) {
      profile.ownedGames = mergeGameLists(profile.ownedGames, snapshot.ownedGames);
    }

    if (snapshot.favoriteGames) {
      profile.favoriteGames = mergeGameLists(profile.favoriteGames, snapshot.favoriteGames);
    }

    if (snapshot.dislikedGames) {
      profile.dislikedGames = mergeGameLists(profile.dislikedGames, snapshot.dislikedGames);
    }

    if (snapshot.wishlist) {
      profile.wishlist = mergeWishlistLists(profile.wishlist, snapshot.wishlist);
    }

    if (snapshot.preferences) {
      profile.preferences = mergePreferenceLists(profile.preferences, snapshot.preferences);
    }

    if (snapshot.notes && snapshot.notes.length > 0) {
      profile.notes = mergeStringLists(profile.notes, snapshot.notes);
    }

    if (snapshot.summary) {
      profile.notes = mergeStringLists(profile.notes, [snapshot.summary]);
    }

    profile.updatedAt = snapshot.lastSyncedAt ?? now;
    await this.repository.save(profile);
    return cloneSteamProfile(profile) as SteamProfile;
  }

  async savePreference(userId: string, preference: UserPreference): Promise<SteamProfile> {
    const profile = await this.getProfile(userId);
    const now = this.now();
    const normalized: UserPreference = {
      ...preference,
      id: preference.id || this.createPreferenceId(preference),
      weight: preference.weight ?? 1,
      source: preference.source ?? 'explicit',
      observedAt: preference.observedAt || now,
      updatedAt: now,
    };

    profile.preferences = mergePreferenceLists(profile.preferences, [normalized]);
    profile.updatedAt = now;
    await this.repository.save(profile);
    return cloneSteamProfile(profile) as SteamProfile;
  }

  async addFavoriteGame(userId: string, game: Game): Promise<SteamProfile> {
    const profile = await this.getProfile(userId);
    profile.favoriteGames = mergeGameLists(profile.favoriteGames, [game]);
    profile.dislikedGames = removeGameByIdentifier(profile.dislikedGames, game);
    profile.updatedAt = this.now();
    await this.repository.save(profile);
    return cloneSteamProfile(profile) as SteamProfile;
  }

  async removeFavoriteGame(userId: string, game: Game | GameIdentifier): Promise<SteamProfile> {
    const profile = await this.getProfile(userId);
    profile.favoriteGames = removeGameByIdentifier(profile.favoriteGames, game);
    profile.updatedAt = this.now();
    await this.repository.save(profile);
    return cloneSteamProfile(profile) as SteamProfile;
  }

  async addOwnedGame(userId: string, game: Game): Promise<SteamProfile> {
    const profile = await this.getProfile(userId);
    profile.ownedGames = mergeGameLists(profile.ownedGames, [game]);
    profile.wishlist = removeWishlistItemByIdentifier(profile.wishlist, game);
    profile.updatedAt = this.now();
    await this.repository.save(profile);
    return cloneSteamProfile(profile) as SteamProfile;
  }

  async removeOwnedGame(userId: string, game: Game | GameIdentifier): Promise<SteamProfile> {
    const profile = await this.getProfile(userId);
    profile.ownedGames = removeGameByIdentifier(profile.ownedGames, game);
    profile.updatedAt = this.now();
    await this.repository.save(profile);
    return cloneSteamProfile(profile) as SteamProfile;
  }

  async addWishlistGame(userId: string, item: WishlistItem): Promise<SteamProfile> {
    const profile = await this.getProfile(userId);
    const normalizedItem: WishlistItem = {
      ...item,
      id: item.id || this.createWishlistItemId(item),
      priority: item.priority ?? 'medium',
      addedAt: item.addedAt || this.now(),
    };

    profile.wishlist = mergeWishlistLists(profile.wishlist, [normalizedItem]);
    profile.updatedAt = this.now();
    await this.repository.save(profile);
    return cloneSteamProfile(profile) as SteamProfile;
  }

  async removeWishlistGame(userId: string, game: Game | GameIdentifier): Promise<SteamProfile> {
    const profile = await this.getProfile(userId);
    profile.wishlist = removeWishlistItemByIdentifier(profile.wishlist, game);
    profile.updatedAt = this.now();
    await this.repository.save(profile);
    return cloneSteamProfile(profile) as SteamProfile;
  }

  async saveFeedback(userId: string, feedback: SteamFeedback): Promise<SteamProfile> {
    const profile = await this.getProfile(userId);
    const now = this.now();
    const game = this.resolveGameFeedbackTarget(feedback);
    const reasons = feedback.reasons ?? [];

    if (game) {
      if (feedback.sentiment === 'positive') {
        profile.favoriteGames = mergeGameLists(profile.favoriteGames, [game]);
        profile.dislikedGames = removeGameByIdentifier(profile.dislikedGames, game);
      } else if (feedback.sentiment === 'negative') {
        profile.dislikedGames = mergeGameLists(profile.dislikedGames, [game]);
        profile.favoriteGames = removeGameByIdentifier(profile.favoriteGames, game);
      }
    }

    if (feedback.notes) {
      profile.notes = mergeStringLists(profile.notes, [feedback.notes]);
    }

    if (reasons.length > 0 && game) {
      profile.notes = mergeStringLists(profile.notes, [
        `${game.name}: ${reasons.join('; ')}`,
      ]);
    }

    if (feedback.inferredPreferences && feedback.inferredPreferences.length > 0) {
      const inferred = feedback.inferredPreferences.map((preference, index) => ({
        ...preference,
        id: `${userId}:feedback:${now}:${index}:${normalizePreferenceKey({
          id: '',
          kind: preference.kind,
          value: preference.value,
          signal: preference.signal,
          weight: preference.weight ?? 1,
          source: preference.source ?? 'inferred',
          note: preference.note,
          observedAt: now,
          updatedAt: now,
        })}`,
        weight: preference.weight ?? 1,
        source: preference.source ?? 'inferred',
        observedAt: now,
        updatedAt: now,
      }));

      profile.preferences = mergePreferenceLists(profile.preferences, inferred);
    }

    profile.updatedAt = now;
    await this.repository.save(profile);
    return cloneSteamProfile(profile) as SteamProfile;
  }

  async recommendGames(
    userId: string,
    candidates: Game[],
    options: RecommendationOptions = {},
  ): Promise<Recommendation[]> {
    const profile = await this.getProfile(userId);
    const limit = options.limit ?? DEFAULT_RECOMMENDATION_LIMIT;
    const filtered = this.filterRecommendationCandidates(profile, candidates, options);
    const scored = filtered.map((game) => this.scoreCandidate(profile, game));

    scored.sort((left, right) => right.score - left.score || right.confidence - left.confidence);
    return scored.slice(0, limit);
  }

  async buildRecommendationContext(
    userId: string,
    candidates: Game[] = [],
    options: RecommendationOptions = {},
  ): Promise<RecommendationContext> {
    const profile = await this.getProfile(userId);
    const recommendations = candidates.length > 0
      ? await this.recommendGames(userId, candidates, options)
      : [];

    return {
      profile,
      summary: this.buildProfileSummary(profile),
      preferenceSummary: this.summarizePreferences(profile),
      librarySummary: this.summarizeLibrary(profile),
      exclusionSummary: this.buildExclusionSummary(profile),
      recommendationRules: this.recommendationRules(),
      candidateRecommendations: recommendations,
    };
  }

  async buildReviewContext(userId: string, game: Game): Promise<ReviewContext> {
    const profile = await this.getProfile(userId);
    const keyMatches = this.findPreferenceMatches(profile, game);
    const highlightPoints = this.buildReviewHighlights(profile, game, keyMatches);
    const cautionPoints = this.buildReviewCautions(profile, game, keyMatches);

    return {
      profile,
      game,
      summary: this.buildReviewSummary(profile, game, keyMatches),
      highlightPoints,
      cautionPoints,
      reviewAngles: this.buildReviewAngles(game, keyMatches),
      spoilerGuardrails: [
        'Keep spoilers light unless the user asks for them.',
        'Avoid plot reveals that are not necessary to explain the recommendation.',
        'If the game is story-heavy, mention that the review stays spoiler-aware.',
      ],
    };
  }

  async buildLibraryOverviewContext(
    userId: string,
    games: Game[],
    options: SteamLibraryOverviewOptions = {},
  ): Promise<SteamLibraryOverviewContext> {
    const profile = await this.getProfile(userId);
    const sorted = this.sortByPlaytime(games);
    const totalGames = sorted.length;
    const playedCount = sorted.filter((game) => this.playtimeMinutes(game) >= DEFAULT_ABANDONED_THRESHOLD_MINUTES).length;
    const abandonedCount = sorted.filter((game) => {
      const minutes = this.playtimeMinutes(game);
      return minutes >= DEFAULT_UNPLAYED_THRESHOLD_MINUTES && minutes < DEFAULT_ABANDONED_THRESHOLD_MINUTES;
    }).length;
    const unplayedCount = sorted.filter((game) => this.playtimeMinutes(game) < DEFAULT_UNPLAYED_THRESHOLD_MINUTES).length;
    const totalLifetimeHours = this.roundHours(sorted.reduce((sum, game) => sum + this.playtimeMinutes(game), 0));
    const topLimit = options.topLimit ?? 10;
    const recentLimit = options.recentLimit ?? 5;
    const recentlyActiveGames = sorted
      .filter((game) => (game.playtime2WeeksMinutes ?? 0) > 0)
      .sort((left, right) => (right.playtime2WeeksMinutes ?? 0) - (left.playtime2WeeksMinutes ?? 0) || left.name.localeCompare(right.name))
      .slice(0, recentLimit);

    return {
      profile,
      summary: totalGames > 0
        ? `Library overview for ${profile.displayName ?? profile.userId}: ${playedCount} played, ${abandonedCount} abandoned, ${unplayedCount} unplayed, ${totalLifetimeHours} total hours.`
        : `No public library data is available yet for ${profile.displayName ?? profile.userId}.`,
      totalGames,
      playedCount,
      abandonedCount,
      unplayedCount,
      totalLifetimeHours,
      topPlayedGames: sorted.slice(0, topLimit),
      backlog: sorted.filter((game) => this.playtimeMinutes(game) < DEFAULT_UNPLAYED_THRESHOLD_MINUTES),
      abandonedGames: sorted.filter((game) => {
        const minutes = this.playtimeMinutes(game);
        return minutes >= DEFAULT_UNPLAYED_THRESHOLD_MINUTES && minutes < DEFAULT_ABANDONED_THRESHOLD_MINUTES;
      }),
      recentlyActiveGames,
      nextActions: this.buildLibraryNextActions(totalGames, unplayedCount, recentlyActiveGames.length),
    };
  }

  async buildDiscoveryContext(
    userId: string,
    candidates: Game[] = [],
    options: SteamDiscoveryOptions = {},
  ): Promise<SteamDiscoveryContext> {
    const profile = await this.getProfile(userId);
    const recommendations = candidates.length > 0
      ? await this.recommendGames(userId, candidates, options)
      : [];
    const focusSignals = uniqueStrings([
      options.mood ? `Mood: ${options.mood}` : '',
      options.timeAvailable ? `Time available: ${options.timeAvailable}` : '',
      profile.favoriteGames.length > 0 ? `Favorites: ${previewList(profile.favoriteGames.map((game) => game.name))}` : '',
      profile.dislikedGames.length > 0 ? `Avoid: ${previewList(profile.dislikedGames.map((game) => game.name))}` : '',
    ]);

    return {
      profile,
      summary: this.buildDiscoverySummary(profile, options, recommendations.length),
      mood: options.mood,
      timeAvailable: options.timeAvailable,
      focusSignals,
      recommendationRules: uniqueStrings([
        ...this.recommendationRules(),
        options.mood ? `Optimize for the requested mood: ${options.mood}.` : '',
        options.timeAvailable ? `Respect the requested time budget: ${options.timeAvailable}.` : '',
      ]),
      candidateRecommendations: recommendations,
    };
  }

  async buildWishlistContext(
    userId: string,
    saleItems: SteamWishlistSaleItem[] = [],
    wishlist: WishlistItem[] = [],
    options: SteamWishlistContextOptions = {},
  ): Promise<SteamWishlistContext> {
    const profile = await this.getProfile(userId);
    const limit = options.limit ?? 5;
    const trackedWishlist = wishlist.length > 0 ? wishlist : profile.wishlist;
    const sortedSaleItems = [...saleItems].sort((left, right) => right.discountPercent - left.discountPercent || left.name.localeCompare(right.name));
    const sortedWishlist = [...trackedWishlist].sort((left, right) => {
      const priorityOrder: Record<string, number> = { high: 3, medium: 2, low: 1 };
      return (priorityOrder[right.priority] ?? 0) - (priorityOrder[left.priority] ?? 0) || right.addedAt.localeCompare(left.addedAt);
    });

    return {
      profile,
      summary: sortedSaleItems.length > 0
        ? `${sortedSaleItems.length} wishlist game(s) are discounted right now out of ${trackedWishlist.length} tracked item(s).`
        : `Wishlist context for ${profile.displayName ?? profile.userId}: ${trackedWishlist.length} tracked item(s), no active sale data.`,
      totalWishlistCount: trackedWishlist.length,
      saleItems: sortedSaleItems.slice(0, limit),
      topWishlisted: sortedWishlist.slice(0, limit),
      nextActions: [
        sortedSaleItems.length > 0 ? 'Lead with the biggest discounts.' : 'Ask for store wishlist data or a fresh sale snapshot.',
        'Call out review score and original price when available.',
        'Prefer high-priority wishlist items when no sale is active.',
      ],
    };
  }

  async buildAchievementContext(
    userId: string,
    game: Game,
    progress: SteamAchievementProgress,
  ): Promise<SteamAchievementContext> {
    const profile = await this.getProfile(userId);

    return {
      profile,
      game,
      summary: this.buildAchievementSummary(profile, game, progress),
      progress,
      highlightPoints: this.buildAchievementHighlights(progress),
      cautionPoints: this.buildAchievementCautions(game, progress),
      nextGoals: this.buildAchievementGoals(progress),
      spoilerGuardrails: [
        'Keep hidden achievements spoiler-light unless the user asks.',
        'Do not claim exact totals when achievement data is private or incomplete.',
        'Mention progress and next targets before listing individual unlocks.',
      ],
    };
  }

  async buildGameLookupContext(
    userId: string,
    game: Game,
    options: SteamGameLookupOptions = {},
  ): Promise<SteamGameLookupContext> {
    const profile = await this.getProfile(userId);
    const sourceNotes = uniqueStrings([
      ...(options.source ? [`Source: ${options.source}`] : []),
      ...(options.sourceNotes ?? []),
    ]);

    return {
      profile,
      game,
      summary: this.buildLookupSummary(profile, game),
      highlights: this.buildLookupHighlights(game),
      cautions: this.buildLookupCautions(game),
      sourceNotes,
    };
  }

  async buildSetupContext(userId: string, check: SteamSetupCheck): Promise<SteamSetupContext> {
    const profile = await this.getProfile(userId);

    return {
      profile,
      summary: this.buildSetupSummary(profile, check),
      checks: this.buildSetupChecks(check),
      nextSteps: this.buildSetupNextSteps(check),
      troubleshooting: this.buildSetupTroubleshooting(check),
    };
  }

  private applyProfilePatch(profile: SteamProfile, patch: SteamProfilePatch): SteamProfile {
    const nextProfile = cloneSteamProfile(profile) as SteamProfile;

    if (patch.displayName !== undefined) {
      nextProfile.displayName = patch.displayName;
    }

    if (patch.notes) {
      nextProfile.notes = mergeStringLists(nextProfile.notes, patch.notes);
    }

    if (patch.favoriteGames) {
      nextProfile.favoriteGames = mergeGameLists(nextProfile.favoriteGames, patch.favoriteGames);
    }

    if (patch.ownedGames) {
      nextProfile.ownedGames = mergeGameLists(nextProfile.ownedGames, patch.ownedGames);
    }

    if (patch.dislikedGames) {
      nextProfile.dislikedGames = mergeGameLists(nextProfile.dislikedGames, patch.dislikedGames);
    }

    if (patch.wishlist) {
      nextProfile.wishlist = mergeWishlistLists(nextProfile.wishlist, patch.wishlist);
    }

    if (patch.preferences) {
      nextProfile.preferences = mergePreferenceLists(nextProfile.preferences, patch.preferences);
    }

    nextProfile.updatedAt = this.now();
    return nextProfile;
  }

  private filterRecommendationCandidates(
    profile: SteamProfile,
    candidates: Game[],
    options: RecommendationOptions,
  ): Game[] {
    const ownedKeys = new Set(profile.ownedGames.map((game) => normalizeGameKey(game)));
    const favoriteKeys = new Set(profile.favoriteGames.map((game) => normalizeGameKey(game)));
    const dislikedKeys = new Set(profile.dislikedGames.map((game) => normalizeGameKey(game)));
    const wishlistKeys = new Set(profile.wishlist.map((item) => normalizeGameKey(item.game)));
    const seen = new Set<string>();
    const output: Game[] = [];

    for (const candidate of candidates) {
      const key = normalizeGameKey(candidate);
      if (seen.has(key)) {
        continue;
      }

      seen.add(key);

      if (!options.includeOwned && ownedKeys.has(key)) {
        continue;
      }

      if (!options.includeFavorites && favoriteKeys.has(key)) {
        continue;
      }

      if (!options.includeDisliked && dislikedKeys.has(key)) {
        continue;
      }

      if (!options.includeWishlist && wishlistKeys.has(key)) {
        continue;
      }

      output.push(candidate);
    }

    return output;
  }

  private scoreCandidate(profile: SteamProfile, game: Game): Recommendation {
    const matchedPreferences = this.findPreferenceMatches(profile, game);
    const reasons: string[] = [];
    const tradeoffs: string[] = [];
    let score = 0;

    if (this.containsGame(profile.ownedGames, game)) {
      score += RECOMMENDATION_WEIGHTS.ownedPenalty;
      tradeoffs.push('Already owned');
    }

    if (this.containsGame(profile.favoriteGames, game)) {
      score += RECOMMENDATION_WEIGHTS.favoritePenalty;
      tradeoffs.push('Already a favorite');
    }

    if (this.containsGame(profile.dislikedGames, game)) {
      score += RECOMMENDATION_WEIGHTS.dislikedPenalty;
      tradeoffs.push('Previously disliked');
    }

    if (this.containsWishlistItem(profile.wishlist, game)) {
      score += RECOMMENDATION_WEIGHTS.wishlistMatch;
      reasons.push('Matches a saved wishlist interest');
    }

    for (const preference of matchedPreferences) {
      const weight = this.preferenceWeightForMatch(preference, game);
      score += weight;
      reasons.push(this.describePreferenceMatch(preference));
    }

    if (game.playtimeHours !== undefined) {
      const lengthPreference = this.findPreference(profile, 'length');
      if (lengthPreference) {
        const lengthScore = this.scoreLengthPreference(lengthPreference, game.playtimeHours);
        if (lengthScore !== 0) {
          score += lengthScore;
          reasons.push(this.describePreferenceMatch(lengthPreference));
        }
      }
    }

    if (game.priceCents !== undefined) {
      const pricePreference = this.findPreference(profile, 'price');
      if (pricePreference) {
        const priceScore = this.scorePricePreference(pricePreference, game.priceCents);
        if (priceScore !== 0) {
          score += priceScore;
          reasons.push(this.describePreferenceMatch(pricePreference));
        }
      }
    }

    if (this.hasAnyTag(game, ['multiplayer', 'co-op', 'coop', 'online co-op'])) {
      score += RECOMMENDATION_WEIGHTS.cooperativeMatch;
      reasons.push('Supports cooperative play');
    }

    if (this.hasAnyTag(game, ['competitive', 'pvp', 'ranked'])) {
      score += RECOMMENDATION_WEIGHTS.competitiveMatch;
      reasons.push('Supports competitive play');
    }

    if (score <= 0) {
      score += RECOMMENDATION_WEIGHTS.noveltyPenalty;
      tradeoffs.push('Weak overlap with the current profile');
    }

    const normalizedScore = Math.max(
      0,
      Math.min(DEFAULT_MAX_RECOMMENDATION_SCORE, Math.round(score + this.preferenceLift(profile, game))),
    );
    const confidence = Math.max(
      0.1,
      Math.min(0.98, 0.25 + (matchedPreferences.length * 0.1) + (normalizedScore / 220)),
    );

    return {
      game,
      score: normalizedScore,
      confidence,
      reasons: uniqueStrings(reasons),
      tradeoffs: uniqueStrings(tradeoffs),
      matchedPreferences,
    };
  }

  private preferenceLift(profile: SteamProfile, game: Game): number {
    const genreMatches = new Set<string>();
    const tagMatches = new Set<string>();
    const searchSpace = [
      ...game.genres,
      ...game.tags,
      ...game.platforms,
      game.name,
    ];

    for (const favorite of profile.favoriteGames) {
      for (const genre of favorite.genres) {
        if (hasTextMatch(searchSpace, genre)) {
          genreMatches.add(genre);
        }
      }

      for (const tag of favorite.tags) {
        if (hasTextMatch(searchSpace, tag)) {
          tagMatches.add(tag);
        }
      }
    }

    return (genreMatches.size * RECOMMENDATION_WEIGHTS.favoriteMatch)
      + (tagMatches.size * RECOMMENDATION_WEIGHTS.explicitLikeMatch);
  }

  private findPreferenceMatches(profile: SteamProfile, game: Game): UserPreference[] {
    const matches: UserPreference[] = [];

    for (const preference of profile.preferences) {
      if (this.matchesPreference(preference, game)) {
        matches.push(preference);
      }
    }

    return matches;
  }

  private matchesPreference(preference: UserPreference, game: Game): boolean {
    const values = [
      game.name,
      ...game.genres,
      ...game.tags,
      ...game.platforms,
    ];

    const normalizedValue = preference.value.trim().toLowerCase();
    if (!normalizedValue) {
      return false;
    }

    switch (preference.kind) {
      case 'genre':
      case 'mood':
      case 'mechanic':
      case 'narrative':
      case 'pace':
      case 'platform':
      case 'coop':
      case 'competitive':
      case 'difficulty':
      case 'playerCount':
      case 'note':
        return hasTextMatch(values, normalizedValue);
      case 'length':
      case 'price':
        return false;
      default:
        return hasTextMatch(values, normalizedValue);
    }
  }

  private preferenceWeightForMatch(preference: UserPreference, game: Game): number {
    switch (preference.signal) {
      case 'like':
        return preference.weight > 0 ? preference.weight * 4 : 4;
      case 'neutral':
        return 1;
      case 'dislike':
        return preference.weight < 0 ? preference.weight * 4 : -preference.weight * 2;
      default:
        return 1;
    }
  }

  private describePreferenceMatch(preference: UserPreference): string {
    const verb = preference.signal === 'dislike' ? 'avoids' : 'matches';
    return `${verb} ${preference.kind} preference "${preference.value}"`;
  }

  private scoreLengthPreference(preference: UserPreference, hours: number): number {
    const parsed = extractNumber(preference.value);
    if (parsed === null) {
      return 0;
    }

    const lower = preference.value.trim().toLowerCase();
    if (lower.includes('under') || lower.includes('short') || lower.includes('below') || lower.includes('less than')) {
      return hours <= parsed ? RECOMMENDATION_WEIGHTS.lengthMatch : -RECOMMENDATION_WEIGHTS.lengthMatch;
    }

    if (lower.includes('over') || lower.includes('long') || lower.includes('more than')) {
      return hours >= parsed ? RECOMMENDATION_WEIGHTS.lengthMatch : -RECOMMENDATION_WEIGHTS.lengthMatch;
    }

    const difference = Math.abs(hours - parsed);
    if (difference <= 3) {
      return RECOMMENDATION_WEIGHTS.lengthMatch;
    }

    return 0;
  }

  private scorePricePreference(preference: UserPreference, priceCents: number): number {
    const parsed = extractNumber(preference.value);
    if (parsed === null) {
      return 0;
    }

    const lower = preference.value.trim().toLowerCase();
    if (lower.includes('under') || lower.includes('cheap') || lower.includes('budget') || lower.includes('below')) {
      return priceCents <= parsed * 100 ? RECOMMENDATION_WEIGHTS.priceMatch : -RECOMMENDATION_WEIGHTS.priceMatch;
    }

    if (lower.includes('over') || lower.includes('premium') || lower.includes('high')) {
      return priceCents >= parsed * 100 ? RECOMMENDATION_WEIGHTS.priceMatch : 0;
    }

    return Math.abs(priceCents - parsed * 100) <= 500 ? RECOMMENDATION_WEIGHTS.priceMatch : 0;
  }

  private containsGame(games: Game[], candidate: Game): boolean {
    const key = normalizeGameKey(candidate);
    return games.some((game) => normalizeGameKey(game) === key);
  }

  private containsWishlistItem(items: WishlistItem[], candidate: Game): boolean {
    const key = normalizeGameKey(candidate);
    return items.some((item) => normalizeGameKey(item.game) === key);
  }

  private findPreference(profile: SteamProfile, kind: string): UserPreference | undefined {
    return profile.preferences.find((preference) => preference.kind === kind);
  }

  private hasAnyTag(game: Game, candidates: string[]): boolean {
    const pool = [
      game.name,
      ...game.genres,
      ...game.tags,
      ...game.platforms,
    ];

    return candidates.some((candidate) => hasTextMatch(pool, candidate));
  }

  private buildProfileSummary(profile: SteamProfile): string {
    const favorites = previewList(profile.favoriteGames.map((game) => game.name));
    const owned = previewList(profile.ownedGames.map((game) => game.name));
    const disliked = previewList(profile.dislikedGames.map((game) => game.name));
    const wishlist = previewList(profile.wishlist.map((item) => item.game.name));

    return [
      profile.displayName ? `Profile for ${profile.displayName}.` : `Profile for ${profile.userId}.`,
      `Favorites: ${favorites}.`,
      `Owned: ${owned}.`,
      `Disliked: ${disliked}.`,
      `Wishlist: ${wishlist}.`,
    ].join(' ');
  }

  private summarizePreferences(profile: SteamProfile): string[] {
    const lines: string[] = [];
    const grouped = new Map<string, UserPreference[]>();

    for (const preference of profile.preferences) {
      const bucket = grouped.get(preference.kind) ?? [];
      bucket.push(preference);
      grouped.set(preference.kind, bucket);
    }

    for (const [kind, preferences] of grouped.entries()) {
      const likeValues = preferences.filter((item) => item.signal === 'like').map((item) => item.value);
      const dislikeValues = preferences.filter((item) => item.signal === 'dislike').map((item) => item.value);

      if (likeValues.length > 0) {
        lines.push(`${kind}: likes ${previewList(likeValues)}`);
      }

      if (dislikeValues.length > 0) {
        lines.push(`${kind}: avoids ${previewList(dislikeValues)}`);
      }
    }

    if (lines.length === 0) {
      lines.push('No explicit preference memory yet.');
    }

    return lines;
  }

  private summarizeLibrary(profile: SteamProfile): string[] {
    return [
      `Owned games: ${profile.ownedGames.length}`,
      `Favorite games: ${profile.favoriteGames.length}`,
      `Disliked games: ${profile.dislikedGames.length}`,
      `Wishlist items: ${profile.wishlist.length}`,
    ];
  }

  private buildExclusionSummary(profile: SteamProfile): string[] {
    return [
      `Avoid recommending games already owned (${profile.ownedGames.length} entries).`,
      `Avoid games already marked as disliked (${profile.dislikedGames.length} entries).`,
      `Avoid repeating favorites unless the user explicitly asks for similar titles.`,
      'Treat wishlist items as signals of interest, not as fresh discovery targets unless requested.',
    ];
  }

  private recommendationRules(): string[] {
    return [
      'Lead with the strongest fit first.',
      'Mention one or two reasons that are grounded in stored memory.',
      'Include a tradeoff if the fit is only partial.',
      'Avoid claiming certainty when the profile is sparse.',
      'Prefer concise, honest, and actionable guidance.',
    ];
  }

  private buildReviewSummary(profile: SteamProfile, game: Game, matchedPreferences: UserPreference[]): string {
    const preferenceSummary = matchedPreferences.length > 0
      ? `Matched preferences: ${previewList(matchedPreferences.map((preference) => `${preference.kind}:${preference.value}`))}.`
      : 'No strong preference overlap was found.';

    return [
      profile.displayName ? `${profile.displayName}'s review context for ${game.name}.` : `Review context for ${game.name}.`,
      preferenceSummary,
      `Known tags: ${previewList([...game.genres, ...game.tags, ...game.platforms])}.`,
    ].join(' ');
  }

  private buildReviewHighlights(profile: SteamProfile, game: Game, matchedPreferences: UserPreference[]): string[] {
    const highlights = [
      `${game.name} appears to fit the player's memory because ${matchedPreferences.length > 0 ? previewList(matchedPreferences.map((preference) => preference.value)) : 'it matches the available library signals'}.`,
    ];

    if (profile.favoriteGames.length > 0) {
      highlights.push(`Compare it with favorites such as ${previewList(profile.favoriteGames.map((item) => item.name))}.`);
    }

    if (game.playtimeHours !== undefined) {
      highlights.push(`Estimated playtime signal: about ${game.playtimeHours} hours.`);
    }

    if (game.priceCents !== undefined) {
      highlights.push(`Price signal: ${formatMoney(game.priceCents, game.currency)}.`);
    }

    return uniqueStrings(highlights);
  }

  private buildReviewCautions(profile: SteamProfile, game: Game, matchedPreferences: UserPreference[]): string[] {
    const cautions = [
      'Do not overstate quality if the profile does not strongly match the game.',
    ];

    if (profile.dislikedGames.length > 0) {
      cautions.push(`Note potential friction with disliked titles such as ${previewList(profile.dislikedGames.map((item) => item.name))}.`);
    }

    if (matchedPreferences.length === 0) {
      cautions.push('The review should avoid pretending the fit is obvious.');
    }

    if (game.notes) {
      cautions.push('Use game metadata carefully and do not invent unsupported facts.');
    }

    return uniqueStrings(cautions);
  }

  private buildReviewAngles(game: Game, matchedPreferences: UserPreference[]): string[] {
    const angles = [
      'Value for money',
      'Core loop and pacing',
      'Replayability',
      'Difficulty and accessibility',
      'Story, tone, or mood',
    ];

    if (this.hasAnyTag(game, ['co-op', 'coop', 'multiplayer'])) {
      angles.unshift('Co-op and social play');
    }

    if (this.hasAnyTag(game, ['competitive', 'pvp', 'ranked'])) {
      angles.unshift('Competitive depth');
    }

    if (matchedPreferences.length > 0) {
      angles.unshift('Fit with the player profile');
    }

    return uniqueStrings(angles);
  }

  private buildDiscoverySummary(profile: SteamProfile, options: SteamDiscoveryOptions, recommendationCount: number): string {
    const moodPart = options.mood ? `Mood: ${options.mood}.` : 'No mood target was supplied.';
    const timePart = options.timeAvailable ? `Time budget: ${options.timeAvailable}.` : 'No time budget was supplied.';
    const resultPart = recommendationCount > 0
      ? `${recommendationCount} candidate recommendation(s) are ready.`
      : 'No candidate recommendations were supplied.';

    return [
      profile.displayName ? `Discovery context for ${profile.displayName}.` : `Discovery context for ${profile.userId}.`,
      moodPart,
      timePart,
      resultPart,
    ].join(' ');
  }

  private buildLibraryNextActions(totalGames: number, unplayedCount: number, recentCount: number): string[] {
    const actions = [
      'Lead with backlog and most-played rankings.',
      'Call out deck compatibility, reviews, or tags when the source data includes them.',
    ];

    if (totalGames === 0) {
      actions.unshift('Warn that the library may be private or unavailable.');
    }

    if (unplayedCount > 0) {
      actions.push(`Surface the ${Math.min(10, unplayedCount)} most interesting backlog picks first.`);
    }

    if (recentCount > 0) {
      actions.push('Include a recently active section to show what the player is touching now.');
    }

    return uniqueStrings(actions);
  }

  private buildAchievementSummary(profile: SteamProfile, game: Game, progress: SteamAchievementProgress): string {
    const owner = profile.displayName ?? profile.userId;
    const privacy = progress.privateData ? 'Achievement data is private or partially hidden.' : 'Achievement data is available.';
    return `${owner} progress for ${game.name}: ${progress.unlockedCount}/${progress.totalCount} (${progress.completionPct}%). ${privacy}`;
  }

  private buildAchievementHighlights(progress: SteamAchievementProgress): string[] {
    const highlights = [
      `${progress.unlockedCount} achievement(s) unlocked out of ${progress.totalCount}.`,
    ];

    if (progress.recentUnlocked.length > 0) {
      highlights.push(`Most recent unlocks: ${previewList(progress.recentUnlocked.map((achievement) => achievement.displayName))}.`);
    }

    if (progress.completionPct >= 90) {
      highlights.push('The player is close to completionist territory.');
    }

    return uniqueStrings(highlights);
  }

  private buildAchievementCautions(game: Game, progress: SteamAchievementProgress): string[] {
    const cautions = [
      'Avoid over-sharing hidden achievement names unless the user asks for spoilers.',
    ];

    if (progress.privateData) {
      cautions.push('Do not infer exact progress from incomplete or private achievement data.');
    }

    if (!game.summary) {
      cautions.push('Use only the provided achievement metadata; do not invent game-specific facts.');
    }

    return uniqueStrings(cautions);
  }

  private buildAchievementGoals(progress: SteamAchievementProgress): string[] {
    const goals = progress.locked
      .filter((achievement) => !achievement.hidden)
      .slice(0, 5)
      .map((achievement) => achievement.displayName);

    if (progress.hiddenLockedCount > 0) {
      goals.push(`${progress.hiddenLockedCount} hidden achievement(s) remain.`);
    }

    if (goals.length === 0) {
      goals.push('No visible locked achievements were supplied.');
    }

    return uniqueStrings(goals);
  }

  private buildLookupSummary(profile: SteamProfile, game: Game): string {
    const owner = profile.displayName ?? profile.userId;
    return `${owner} lookup context for ${game.name}.`;
  }

  private buildLookupHighlights(game: Game): string[] {
    const highlights = [
      game.summary ? game.summary : `No summary was provided for ${game.name}.`,
    ];

    if (game.reviewScore !== undefined || game.reviewDescription !== undefined) {
      highlights.push(`Reviews: ${game.reviewDescription ?? 'n/a'}${game.reviewScore !== undefined ? ` (${game.reviewScore})` : ''}.`);
    }

    if (game.deckCompatibility) {
      highlights.push(`Steam Deck: ${game.deckCompatibility}.`);
    }

    const metadata = previewList([
      ...game.genres,
      ...game.tags,
      ...game.platforms,
    ]);
    highlights.push(`Metadata: ${metadata}.`);

    return uniqueStrings(highlights);
  }

  private buildLookupCautions(game: Game): string[] {
    const cautions = [
      'Treat unsupported fields as unknown rather than inferred.',
    ];

    if (!game.storeUrl) {
      cautions.push('No store URL was provided, so link handling should stay generic.');
    }

    if (!game.developer && !game.publisher) {
      cautions.push('Developer and publisher are missing; avoid asserting them.');
    }

    return uniqueStrings(cautions);
  }

  private buildSetupSummary(profile: SteamProfile, check: SteamSetupCheck): string {
    const owner = profile.displayName ?? profile.userId;
    const configured = [
      check.steamApiKeyConfigured ? 'Steam API key' : null,
      check.libraryAccessible ? 'library access' : null,
      check.wishlistAccessible ? 'wishlist access' : null,
      check.achievementsAccessible ? 'achievement access' : null,
      check.igdbConfigured ? 'IGDB access' : null,
    ].filter(Boolean) as string[];

    return `${owner} setup check: ${configured.length > 0 ? configured.join(', ') : 'no integrations verified yet'}.`;
  }

  private buildSetupChecks(check: SteamSetupCheck): string[] {
    return uniqueStrings([
      check.steamApiKeyConfigured ? 'Steam API key is configured.' : 'Steam API key is missing or unavailable.',
      check.libraryAccessible ? 'Library data can be read.' : 'Library data is not available yet.',
      check.wishlistAccessible ? 'Wishlist data can be read.' : 'Wishlist data is private or unavailable.',
      check.achievementsAccessible ? 'Achievement data can be read.' : 'Achievement data is private or unavailable.',
      check.igdbConfigured ? 'IGDB enrichment is available.' : 'IGDB enrichment is unavailable.',
      ...(check.notes ?? []),
    ]);
  }

  private buildSetupNextSteps(check: SteamSetupCheck): string[] {
    const steps = [
      !check.steamApiKeyConfigured ? 'Set the Steam API key first.' : null,
      !check.libraryAccessible ? 'Retry after making the profile/library public if needed.' : null,
      !check.wishlistAccessible ? 'Make the wishlist public if sale checks are needed.' : null,
      !check.achievementsAccessible ? 'Make game details public if achievement tracking is needed.' : null,
      !check.igdbConfigured ? 'Add IGDB credentials if richer game lookup is desired.' : null,
    ].filter(Boolean) as string[];

    return steps.length > 0 ? steps : ['Everything looks configured.'];
  }

  private buildSetupTroubleshooting(check: SteamSetupCheck): string[] {
    const troubleshooting = [
      'Double-check privacy settings if Steam returns empty payloads.',
      'Use the source data as-is; do not fabricate missing library or wishlist entries.',
    ];

    if (!check.steamApiKeyConfigured) {
      troubleshooting.unshift('Missing credentials usually mean the runtime has not loaded the required secrets yet.');
    }

    return uniqueStrings([...troubleshooting, ...(check.notes ?? [])]);
  }

  private playtimeMinutes(game: Game): number {
    if (typeof game.playtimeMinutes === 'number') {
      return game.playtimeMinutes;
    }

    if (typeof game.playtimeHours === 'number') {
      return Math.round(game.playtimeHours * 60);
    }

    return 0;
  }

  private sortByPlaytime(games: Game[]): Game[] {
    return [...games].sort((left, right) => {
      const diff = this.playtimeMinutes(right) - this.playtimeMinutes(left);
      return diff !== 0 ? diff : left.name.localeCompare(right.name);
    });
  }

  private roundHours(minutes: number): number {
    return Math.round((minutes / 60) * 10) / 10;
  }

  private createPreferenceId(preference: UserPreference): string {
    return [
      'preference',
      normalizePreferenceKey(preference),
      this.now(),
    ].join(':');
  }

  private createWishlistItemId(item: WishlistItem): string {
    return [
      'wishlist',
      normalizeGameKey(item.game),
      this.now(),
    ].join(':');
  }

  private resolveGameFeedbackTarget(feedback: SteamFeedback): Game | null {
    if (feedback.game) {
      if ('genres' in feedback.game) {
        return feedback.game;
      }

      return {
        appId: feedback.game.appId,
        name: feedback.game.name,
        genres: [],
        tags: [],
        platforms: [],
      };
    }

    if (feedback.gameName) {
      return {
        name: feedback.gameName,
        genres: [],
        tags: [],
        platforms: [],
      };
    }

    return null;
  }

  private now(): string {
    return (this.options.clock ?? (() => new Date()))().toISOString();
  }
}

function extractNumber(value: string): number | null {
  const match = value.match(/(\d+(?:\.\d+)?)/);
  if (!match) {
    return null;
  }

  return Number(match[1]);
}

function hasTextMatch(values: string[], needle: string): boolean {
  const normalizedNeedle = needle.trim().toLowerCase();
  if (!normalizedNeedle) {
    return false;
  }

  return values.some((value) => value.trim().toLowerCase().includes(normalizedNeedle));
}

function previewList(values: string[], limit = 3): string {
  const unique = uniqueStrings(values.filter((value) => value.trim().length > 0));
  if (unique.length === 0) {
    return 'none';
  }

  if (unique.length <= limit) {
    return unique.join(', ');
  }

  return `${unique.slice(0, limit).join(', ')}, and ${unique.length - limit} more`;
}

function uniqueStrings(values: string[]): string[] {
  const seen = new Set<string>();
  const output: string[] = [];

  for (const value of values) {
    const normalized = value.trim().toLowerCase();
    if (!normalized || seen.has(normalized)) {
      continue;
    }

    seen.add(normalized);
    output.push(value.trim());
  }

  return output;
}

function formatMoney(priceCents: number, currency?: string): string {
  const amount = (priceCents / 100).toFixed(2);
  return currency ? `${currency} ${amount}` : `$${amount}`;
}
