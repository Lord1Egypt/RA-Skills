import { promises as fs } from 'node:fs';
import { dirname } from 'node:path';

import type { Game, GameIdentifier, SteamProfile, SteamProfilePatch, UserPreference, WishlistItem } from './types.js';

export interface SteamCompanionRepository {
  get(userId: string): Promise<SteamProfile | null>;
  save(profile: SteamProfile): Promise<void>;
}

export function createEmptySteamProfile(userId: string, displayName?: string): SteamProfile {
  const now = new Date().toISOString();

  return {
    userId,
    displayName,
    favoriteGames: [],
    ownedGames: [],
    dislikedGames: [],
    wishlist: [],
    preferences: [],
    notes: [],
    createdAt: now,
    updatedAt: now,
  };
}

export function cloneSteamProfile(profile: SteamProfile | null): SteamProfile | null {
  return profile === null ? null : JSON.parse(JSON.stringify(profile)) as SteamProfile;
}

export function normalizeGameKey(game: Game | GameIdentifier): string {
  if (typeof game.appId === 'number') {
    return `app:${game.appId}`;
  }

  return `name:${normalizeText(game.name)}`;
}

export function normalizePreferenceKey(preference: UserPreference): string {
  return [
    normalizeText(preference.kind),
    normalizeText(preference.value),
    preference.signal,
  ].join(':');
}

export function normalizeWishlistItemKey(item: WishlistItem): string {
  return normalizeGameKey(item.game);
}

export function mergeGame(base: Game | undefined, next: Game): Game {
  if (!base) {
    return {
      appId: next.appId,
      name: next.name,
      genres: [...next.genres],
      tags: [...next.tags],
      platforms: [...next.platforms],
      playtimeHours: next.playtimeHours,
      playtimeMinutes: next.playtimeMinutes,
      playtime2WeeksMinutes: next.playtime2WeeksMinutes,
      priceCents: next.priceCents,
      currency: next.currency,
      releaseYear: next.releaseYear,
      releaseDate: next.releaseDate,
      storeUrl: next.storeUrl,
      notes: next.notes,
      summary: next.summary,
      reviewScore: next.reviewScore,
      reviewDescription: next.reviewDescription,
      deckCompatibility: next.deckCompatibility,
      developer: next.developer,
      publisher: next.publisher,
    };
  }

  return {
    appId: next.appId ?? base.appId,
    name: next.name || base.name,
    genres: mergeStringLists(base.genres, next.genres),
    tags: mergeStringLists(base.tags, next.tags),
    platforms: mergeStringLists(base.platforms, next.platforms),
    playtimeHours: next.playtimeHours ?? base.playtimeHours,
    playtimeMinutes: next.playtimeMinutes ?? base.playtimeMinutes,
    playtime2WeeksMinutes: next.playtime2WeeksMinutes ?? base.playtime2WeeksMinutes,
    priceCents: next.priceCents ?? base.priceCents,
    currency: next.currency ?? base.currency,
    releaseYear: next.releaseYear ?? base.releaseYear,
    releaseDate: next.releaseDate ?? base.releaseDate,
    storeUrl: next.storeUrl ?? base.storeUrl,
    notes: next.notes ?? base.notes,
    summary: next.summary ?? base.summary,
    reviewScore: next.reviewScore ?? base.reviewScore,
    reviewDescription: next.reviewDescription ?? base.reviewDescription,
    deckCompatibility: next.deckCompatibility ?? base.deckCompatibility,
    developer: next.developer ?? base.developer,
    publisher: next.publisher ?? base.publisher,
  };
}

export function mergeWishlistItem(base: WishlistItem | undefined, next: WishlistItem): WishlistItem {
  if (!base) {
    return JSON.parse(JSON.stringify(next)) as WishlistItem;
  }

  return {
    id: next.id || base.id,
    game: mergeGame(base.game, next.game),
    desiredPriceCents: next.desiredPriceCents ?? base.desiredPriceCents,
    currency: next.currency ?? base.currency,
    priority: next.priority ?? base.priority,
    addedAt: base.addedAt || next.addedAt,
    reason: next.reason ?? base.reason,
  };
}

export function mergePreference(base: UserPreference | undefined, next: UserPreference): UserPreference {
  if (!base) {
    return JSON.parse(JSON.stringify(next)) as UserPreference;
  }

  return {
    id: next.id || base.id,
    kind: next.kind,
    value: next.value || base.value,
    signal: next.signal,
    weight: next.weight ?? base.weight,
    source: next.source ?? base.source,
    note: next.note ?? base.note,
    observedAt: base.observedAt || next.observedAt,
    updatedAt: next.updatedAt || base.updatedAt,
  };
}

export function mergeProfile(base: SteamProfile, patch: SteamProfilePatch): SteamProfile {
  const profile: SteamProfile = cloneSteamProfile(base) ?? createEmptySteamProfile(base.userId, base.displayName);

  if (patch.displayName !== undefined) {
    profile.displayName = patch.displayName;
  }

  if (patch.notes !== undefined) {
    profile.notes = mergeStringLists(profile.notes, patch.notes);
  }

  if (patch.favoriteGames) {
    profile.favoriteGames = mergeGameLists(profile.favoriteGames, patch.favoriteGames);
  }

  if (patch.ownedGames) {
    profile.ownedGames = mergeGameLists(profile.ownedGames, patch.ownedGames);
  }

  if (patch.dislikedGames) {
    profile.dislikedGames = mergeGameLists(profile.dislikedGames, patch.dislikedGames);
  }

  if (patch.wishlist) {
    profile.wishlist = mergeWishlistLists(profile.wishlist, patch.wishlist);
  }

  if (patch.preferences) {
    profile.preferences = mergePreferenceLists(profile.preferences, patch.preferences);
  }

  profile.updatedAt = new Date().toISOString();
  return profile;
}

export function mergeGameLists(existing: Game[], incoming: Game[]): Game[] {
  const map = new Map<string, Game>();

  for (const game of existing) {
    map.set(normalizeGameKey(game), JSON.parse(JSON.stringify(game)) as Game);
  }

  for (const game of incoming) {
    const key = normalizeGameKey(game);
    map.set(key, mergeGame(map.get(key), game));
  }

  return [...map.values()];
}

export function mergeWishlistLists(existing: WishlistItem[], incoming: WishlistItem[]): WishlistItem[] {
  const map = new Map<string, WishlistItem>();

  for (const item of existing) {
    map.set(normalizeWishlistItemKey(item), JSON.parse(JSON.stringify(item)) as WishlistItem);
  }

  for (const item of incoming) {
    const key = normalizeWishlistItemKey(item);
    map.set(key, mergeWishlistItem(map.get(key), item));
  }

  return [...map.values()];
}

export function mergePreferenceLists(existing: UserPreference[], incoming: UserPreference[]): UserPreference[] {
  const map = new Map<string, UserPreference>();

  for (const preference of existing) {
    map.set(normalizePreferenceKey(preference), JSON.parse(JSON.stringify(preference)) as UserPreference);
  }

  for (const preference of incoming) {
    const key = normalizePreferenceKey(preference);
    map.set(key, mergePreference(map.get(key), preference));
  }

  return [...map.values()];
}

export function removeGameByIdentifier(items: Game[], target: Game | GameIdentifier): Game[] {
  const key = normalizeGameKey(target);
  return items.filter((item) => normalizeGameKey(item) !== key);
}

export function removeWishlistItemByIdentifier(items: WishlistItem[], target: Game | GameIdentifier): WishlistItem[] {
  const key = normalizeGameKey(target);
  return items.filter((item) => normalizeGameKey(item.game) !== key);
}

export function removePreferenceByIdentifier(items: UserPreference[], target: UserPreference): UserPreference[] {
  const key = normalizePreferenceKey(target);
  return items.filter((item) => normalizePreferenceKey(item) !== key);
}

export function mergeStringLists(existing: string[], incoming: string[]): string[] {
  const seen = new Set<string>();
  const output: string[] = [];

  for (const value of [...existing, ...incoming]) {
    const normalized = normalizeText(value);
    if (!normalized || seen.has(normalized)) {
      continue;
    }

    seen.add(normalized);
    output.push(value.trim());
  }

  return output;
}

export function normalizeText(value: string): string {
  return value.trim().toLowerCase();
}

export class InMemorySteamCompanionRepository implements SteamCompanionRepository {
  private readonly profiles = new Map<string, SteamProfile>();

  async get(userId: string): Promise<SteamProfile | null> {
    return cloneSteamProfile(this.profiles.get(userId) ?? null);
  }

  async save(profile: SteamProfile): Promise<void> {
    this.profiles.set(profile.userId, cloneSteamProfile(profile) as SteamProfile);
  }
}

export class JsonFileSteamCompanionRepository implements SteamCompanionRepository {
  private constructor(
    private readonly filePath: string,
    private readonly profiles: Map<string, SteamProfile>,
  ) {}

  static async create(filePath: string): Promise<JsonFileSteamCompanionRepository> {
    const profiles = new Map<string, SteamProfile>();

    try {
      const raw = await fs.readFile(filePath, 'utf8');
      const parsed = JSON.parse(raw) as { profiles?: SteamProfile[] };
      for (const profile of parsed.profiles ?? []) {
        profiles.set(profile.userId, profile);
      }
    } catch (error) {
      if (!isMissingFileError(error)) {
        throw error;
      }
    }

    return new JsonFileSteamCompanionRepository(filePath, profiles);
  }

  async get(userId: string): Promise<SteamProfile | null> {
    return cloneSteamProfile(this.profiles.get(userId) ?? null);
  }

  async save(profile: SteamProfile): Promise<void> {
    this.profiles.set(profile.userId, cloneSteamProfile(profile) as SteamProfile);
    await this.persist();
  }

  private async persist(): Promise<void> {
    await fs.mkdir(dirname(this.filePath), { recursive: true });

    const payload = {
      profiles: [...this.profiles.values()],
    };

    await fs.writeFile(this.filePath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  }
}

function isMissingFileError(error: unknown): boolean {
  if (typeof error !== 'object' || error === null) {
    return false;
  }

  return 'code' in error && (error as { code?: string }).code === 'ENOENT';
}
