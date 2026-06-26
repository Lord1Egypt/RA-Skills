import { RobloxApiClient } from '../lib/api.js';
import type {
  CLIResult,
  DeveloperProduct,
  CreateDeveloperProductRequest,
  UpdateDeveloperProductRequest,
} from '../lib/types.js';

export async function list(
  apiKey: string,
  universeId: string
): Promise<CLIResult<DeveloperProduct[]>> {
  const client = new RobloxApiClient(apiKey);
  return await client.listProducts(universeId);
}

export async function get(
  apiKey: string,
  universeId: string,
  productId: string
): Promise<CLIResult<DeveloperProduct>> {
  const client = new RobloxApiClient(apiKey);
  return await client.getProduct(universeId, productId);
}

export async function create(
  apiKey: string,
  universeId: string,
  data: CreateDeveloperProductRequest
): Promise<CLIResult<DeveloperProduct>> {
  // Validate required fields
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
  return await client.createProduct(universeId, data);
}

export async function update(
  apiKey: string,
  universeId: string,
  productId: string,
  data: UpdateDeveloperProductRequest
): Promise<CLIResult<DeveloperProduct>> {
  // At least one field required
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

  // If isForSale provided without price, fetch current price
  if (data.isForSale !== undefined && data.price === undefined) {
    const currentResult = await get(apiKey, universeId, productId);
    if (!currentResult.success) {
      return currentResult;
    }
    data.price = currentResult.data.priceInformation?.defaultPriceInRobux;
  }

  const client = new RobloxApiClient(apiKey);
  return await client.updateProduct(universeId, productId, data);
}
