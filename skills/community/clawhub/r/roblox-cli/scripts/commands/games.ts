import { RobloxApiClient, parseRobloxApiKeyJwt } from '../lib/api.js';
import type { CLIResult, Game } from '../lib/types.js';

export async function list(apiKey: string): Promise<CLIResult<Game[]>> {
  // 1. Parse JWT to get ownerId
  const { ownerId } = parseRobloxApiKeyJwt(apiKey);
  
  // 2. If ownerId is null, return INVALID_API_KEY error
  if (!ownerId) {
    return {
      success: false,
      error: {
        code: 'INVALID_API_KEY',
        message: 'Could not parse API key. Ensure you copied the full key from Roblox Creator Hub.'
      }
    };
  }
  
  // 3. Create API client and call listGames
  const client = new RobloxApiClient(apiKey);
  return await client.listGames(ownerId);
}
