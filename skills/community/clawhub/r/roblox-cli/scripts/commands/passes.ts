import { RobloxApiClient } from '../lib/api.js';
import type {
  CLIResult,
  GamePass,
  CreateGamePassRequest,
  UpdateGamePassRequest,
} from '../lib/types.js';

/**
 * List all game passes for a universe (paginated)
 */
export async function list(
  apiKey: string,
  universeId: string
): Promise<CLIResult<GamePass[]>> {
  const client = new RobloxApiClient(apiKey);
  return await client.listGamePasses(universeId);
}

/**
 * Get a specific game pass by ID (uses list + filter pattern)
 */
export async function get(
  apiKey: string,
  universeId: string,
  passId: string
): Promise<CLIResult<GamePass>> {
  const listResult = await list(apiKey, universeId);

  if (!listResult.success) {
    return listResult;
  }

  const pass = listResult.data.find(
    (p) => p.gamePassId === parseInt(passId, 10)
  );

  if (!pass) {
    return {
      success: false,
      error: {
        code: 'NOT_FOUND',
        message: `Game pass ${passId} not found in universe ${universeId}`,
      },
    };
  }

  return { success: true, data: pass };
}

/**
 * Create a new game pass
 * Required: name, price
 * Optional: description, isForSale
 */
export async function create(
  apiKey: string,
  universeId: string,
  data: CreateGamePassRequest
): Promise<CLIResult<GamePass>> {
  if (!data.name || data.price === undefined) {
    return {
      success: false,
      error: {
        code: 'INVALID_ARGS',
        message: 'Missing required flags: --name and --price are required',
      },
    };
  }

  const client = new RobloxApiClient(apiKey);
  return await client.createGamePass(universeId, data);
}

/**
 * Update an existing game pass
 * At least one field required: name, description, price, or isForSale
 * If isForSale is provided without price, fetches current price
 */
export async function update(
  apiKey: string,
  universeId: string,
  passId: string,
  data: UpdateGamePassRequest
): Promise<CLIResult<GamePass>> {
  if (
    !data.name &&
    !data.description &&
    data.price === undefined &&
    data.isForSale === undefined
  ) {
    return {
      success: false,
      error: {
        code: 'INVALID_ARGS',
        message:
          'At least one update flag required: --name, --description, --price, or --for-sale',
      },
    };
  }

  if (data.isForSale !== undefined && data.price === undefined) {
    const currentResult = await get(apiKey, universeId, passId);
    if (!currentResult.success) {
      return currentResult;
    }
    data.price = currentResult.data.priceInformation?.defaultPriceInRobux;
  }

  const client = new RobloxApiClient(apiKey);
  return await client.updateGamePass(universeId, passId, data);
}
