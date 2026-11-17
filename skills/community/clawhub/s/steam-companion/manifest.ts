import { STEAM_COMPANION_CAPABILITIES, STEAM_COMPANION_DISPLAY_NAME, STEAM_COMPANION_SKILL_NAME, STEAM_COMPANION_VERSION } from './constants.js';
import { steamCompanionPromptCatalog } from './prompts.js';
import { steamCompanionToolCatalog } from './tools.js';
import type { SteamCompanionManifest } from './types.js';

export const steamCompanionManifest: SteamCompanionManifest = {
  name: STEAM_COMPANION_SKILL_NAME,
  displayName: STEAM_COMPANION_DISPLAY_NAME,
  description: 'Reusable Steam gaming companion for profiles, library insights, recommendations, wishlist tracking, achievement context, game lookups, reviews, setup verification, and preference memory.',
  version: STEAM_COMPANION_VERSION,
  capabilities: [...STEAM_COMPANION_CAPABILITIES],
  exportedTools: steamCompanionToolCatalog,
  exportedPrompts: steamCompanionPromptCatalog,
};
