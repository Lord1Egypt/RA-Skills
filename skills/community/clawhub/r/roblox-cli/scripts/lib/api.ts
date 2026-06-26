import { deflateSync } from 'zlib';
import type {
  CLIResult,
  CLIError,
  Game,
  GamesListResponse,
  GamePass,
  GamePassListResponse,
  DeveloperProduct,
  DeveloperProductListResponse,
  JwtParseResult,
  CreateGamePassRequest,
  UpdateGamePassRequest,
  CreateDeveloperProductRequest,
  UpdateDeveloperProductRequest,
} from './types.js';

const RETRY_STATUS_CODES = [429, 500, 502, 503, 504];
const MAX_RETRIES = 3;
const BASE_DELAY_MS = 1000;

function getCrcTable(): number[] {
  const table: number[] = [];
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table[n] = c;
  }
  return table;
}

function crc32(data: Buffer): number {
  let crc = 0xffffffff;
  const table = getCrcTable();
  for (let i = 0; i < data.length; i++) {
    const byte = data[i] ?? 0;
    const idx = (crc ^ byte) & 0xff;
    crc = (crc >>> 8) ^ (table[idx] ?? 0);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

export function parseRobloxApiKeyJwt(apiKey: string): JwtParseResult {
  try {
    const normalized = apiKey.replace(/-/g, '+').replace(/_/g, '/');
    const decoded = Buffer.from(normalized, 'base64').toString('utf-8');
    
    const jwtMatch = decoded.match(/eyJ[A-Za-z0-9_-]+\.([A-Za-z0-9_-]+)\./);
    if (!jwtMatch?.[1]) return { ownerId: null, exp: null };
    
    const payloadB64 = jwtMatch[1].replace(/-/g, '+').replace(/_/g, '/');
    const payload = JSON.parse(Buffer.from(payloadB64, 'base64').toString('utf-8'));
    
    return { 
      ownerId: payload.ownerId || null,
      exp: payload.exp || null
    };
  } catch {
    return { ownerId: null, exp: null };
  }
}

export function generatePlaceholderIcon(): Buffer {
  const width = 150;
  const height = 150;
  
  const ihdrData = Buffer.alloc(13);
  ihdrData.writeUInt32BE(width, 0);
  ihdrData.writeUInt32BE(height, 4);
  ihdrData.writeUInt8(8, 8);
  ihdrData.writeUInt8(2, 9);
  ihdrData.writeUInt8(0, 10);
  ihdrData.writeUInt8(0, 11);
  ihdrData.writeUInt8(0, 12);
  
  const rawData: number[] = [];
  for (let y = 0; y < height; y++) {
    rawData.push(0);
    for (let x = 0; x < width; x++) {
      rawData.push(76, 175, 80);
    }
  }
  
  const rawBuffer = Buffer.from(rawData);
  const compressedData = deflateSync(rawBuffer);
  
  const signature = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
  
  const createChunk = (type: string, data: Buffer): Buffer => {
    const length = Buffer.alloc(4);
    length.writeUInt32BE(data.length, 0);
    const typeBuffer = Buffer.from(type, 'ascii');
    const crcData = Buffer.concat([typeBuffer, data]);
    const crc = Buffer.alloc(4);
    crc.writeUInt32BE(crc32(crcData), 0);
    return Buffer.concat([length, typeBuffer, data, crc]);
  };
  
  const ihdrChunk = createChunk('IHDR', ihdrData);
  const idatChunk = createChunk('IDAT', compressedData);
  const iendChunk = createChunk('IEND', Buffer.alloc(0));
  
  return Buffer.concat([signature, ihdrChunk, idatChunk, iendChunk]);
}

export function buildMultipartBody(fields: Record<string, string | Buffer>, boundary: string): Buffer {
  const parts: Buffer[] = [];
  
  for (const [name, value] of Object.entries(fields)) {
    if (Buffer.isBuffer(value)) {
      parts.push(Buffer.from(
        `--${boundary}\r\nContent-Disposition: form-data; name="${name}"; filename="icon.png"\r\nContent-Type: image/png\r\n\r\n`
      ));
      parts.push(value);
      parts.push(Buffer.from('\r\n'));
    } else {
      parts.push(Buffer.from(
        `--${boundary}\r\nContent-Disposition: form-data; name="${name}"\r\n\r\n${value}\r\n`
      ));
    }
  }
  
  parts.push(Buffer.from(`--${boundary}--\r\n`));
  return Buffer.concat(parts);
}

function makeError(code: string, message: string): CLIError {
  return { success: false, error: { code, message } };
}

function mapHttpStatusToError(status: number, context: 'list' | 'get' | 'create' | 'update'): CLIError {
  switch (status) {
    case 400:
      return makeError('INVALID_ARGS', 'Invalid request parameters');
    case 401:
      return makeError('API_ERROR', 'Invalid or expired API key');
    case 403:
      return makeError('API_ERROR', 'API key lacks access to this universe');
    case 404:
      if (context === 'list') {
        return makeError('API_ERROR', 'Universe not found');
      }
      return makeError('NOT_FOUND', 'Resource not found');
    case 429:
      return makeError('RATE_LIMITED', 'Rate limit exceeded');
    default:
      return makeError('API_ERROR', `API request failed with status ${status}`);
  }
}

async function fetchWithRetry(
  url: string,
  options: RequestInit,
  context: 'list' | 'get' | 'create' | 'update'
): Promise<Response | CLIError> {
  let lastError: CLIError | null = null;
  
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    try {
      const response = await fetch(url, options);
      
      if (response.ok) {
        return response;
      }
      
      if (!RETRY_STATUS_CODES.includes(response.status) || attempt === MAX_RETRIES) {
        return mapHttpStatusToError(response.status, context);
      }
      
      let delayMs = BASE_DELAY_MS * Math.pow(2, attempt);
      
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After');
        if (retryAfter) {
          const retrySeconds = parseInt(retryAfter, 10);
          if (!isNaN(retrySeconds)) {
            delayMs = retrySeconds * 1000;
          }
        }
      }
      
      const jitter = delayMs * 0.1 * (Math.random() * 2 - 1);
      await new Promise(resolve => setTimeout(resolve, delayMs + jitter));
      
      lastError = mapHttpStatusToError(response.status, context);
    } catch (err) {
      if (attempt === MAX_RETRIES) {
        return makeError('NETWORK_ERROR', `Network error: ${err instanceof Error ? err.message : 'Unknown error'}`);
      }
      
      const delayMs = BASE_DELAY_MS * Math.pow(2, attempt);
      const jitter = delayMs * 0.1 * (Math.random() * 2 - 1);
      await new Promise(resolve => setTimeout(resolve, delayMs + jitter));
      
      lastError = makeError('NETWORK_ERROR', `Network error: ${err instanceof Error ? err.message : 'Unknown error'}`);
    }
  }
  
  return lastError ?? makeError('API_ERROR', 'Request failed after retries');
}

export class RobloxApiClient {
  private apiKey: string;
  
  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }
  
  async listGames(userId: string): Promise<CLIResult<Game[]>> {
    const allGames: Game[] = [];
    let cursor: string | undefined;
    
    do {
      const url = new URL(`https://games.roblox.com/v2/users/${userId}/games`);
      if (cursor) {
        url.searchParams.set('cursor', cursor);
      }
      
      const result = await fetchWithRetry(url.toString(), { method: 'GET' }, 'list');
      
      if ('success' in result && result.success === false) {
        return result;
      }
      
      const response = result as Response;
      const data: GamesListResponse = await response.json();
      
      allGames.push(...data.data);
      cursor = data.nextPageCursor;
    } while (cursor);
    
    return { success: true, data: allGames };
  }
  
  async listGamePasses(universeId: string): Promise<CLIResult<GamePass[]>> {
    const allPasses: GamePass[] = [];
    let pageToken: string | undefined;
    
    do {
      const url = new URL(`https://apis.roblox.com/game-passes/v1/universes/${universeId}/game-passes/creator`);
      if (pageToken) {
        url.searchParams.set('pageToken', pageToken);
      }
      
      const result = await fetchWithRetry(
        url.toString(),
        {
          method: 'GET',
          headers: { 'x-api-key': this.apiKey },
        },
        'list'
      );
      
      if ('success' in result && result.success === false) {
        return result;
      }
      
      const response = result as Response;
      const data: GamePassListResponse = await response.json();
      
      allPasses.push(...data.gamePasses);
      pageToken = data.nextPageToken;
    } while (pageToken);
    
    return { success: true, data: allPasses };
  }
  
  async getGamePass(universeId: string, passId: string): Promise<CLIResult<GamePass>> {
    const listResult = await this.listGamePasses(universeId);
    
    if (!listResult.success) {
      return listResult as CLIError;
    }
    
    const pass = listResult.data.find(p => p.gamePassId.toString() === passId);
    
    if (!pass) {
      return makeError('NOT_FOUND', `Game pass ${passId} not found in universe ${universeId}`);
    }
    
    return { success: true, data: pass };
  }
  
  async createGamePass(universeId: string, data: CreateGamePassRequest): Promise<CLIResult<GamePass>> {
    const boundary = `----FormBoundary${Date.now()}_${Math.random().toString(36).slice(2)}`;
    const iconFile = data.iconFile ?? generatePlaceholderIcon();
    
    const fields: Record<string, string | Buffer> = {
      Name: data.name,
      Description: data.description ?? '',
      UniverseId: universeId,
      price: (data.price ?? 0).toString(),
      isForSale: (data.isForSale ?? false).toString(),
      File: iconFile,
    };
    
    const body = buildMultipartBody(fields, boundary);
    
    const result = await fetchWithRetry(
      `https://apis.roblox.com/game-passes/v1/universes/${universeId}/game-passes`,
      {
        method: 'POST',
        headers: {
          'x-api-key': this.apiKey,
          'Content-Type': `multipart/form-data; boundary=${boundary}`,
        },
        body: new Uint8Array(body),
      },
      'create'
    );
    
    if ('success' in result && result.success === false) {
      return result;
    }
    
    const response = result as Response;
    const responseData: GamePass = await response.json();
    
    return { success: true, data: responseData };
  }
  
  async updateGamePass(universeId: string, passId: string, data: UpdateGamePassRequest): Promise<CLIResult<GamePass>> {
    const boundary = `----FormBoundary${Date.now()}_${Math.random().toString(36).slice(2)}`;
    
    const fields: Record<string, string> = {};
    if (data.name !== undefined) fields.name = data.name;
    if (data.description !== undefined) fields.description = data.description;
    if (data.price !== undefined) fields.price = data.price.toString();
    if (data.isForSale !== undefined) fields.isForSale = data.isForSale.toString();
    
    const body = buildMultipartBody(fields, boundary);
    
    const result = await fetchWithRetry(
      `https://apis.roblox.com/game-passes/v1/universes/${universeId}/game-passes/${passId}`,
      {
        method: 'PATCH',
        headers: {
          'x-api-key': this.apiKey,
          'Content-Type': `multipart/form-data; boundary=${boundary}`,
        },
        body: new Uint8Array(body),
      },
      'update'
    );
    
    if ('success' in result && result.success === false) {
      return result;
    }
    
    const response = result as Response;
    const responseData: GamePass = await response.json();
    
    return { success: true, data: responseData };
  }
  
  async listProducts(universeId: string): Promise<CLIResult<DeveloperProduct[]>> {
    const allProducts: DeveloperProduct[] = [];
    let pageToken: string | undefined;
    
    do {
      const url = new URL(`https://apis.roblox.com/developer-products/v2/universes/${universeId}/developer-products/creator`);
      if (pageToken) {
        url.searchParams.set('pageToken', pageToken);
      }
      
      const result = await fetchWithRetry(
        url.toString(),
        {
          method: 'GET',
          headers: { 'x-api-key': this.apiKey },
        },
        'list'
      );
      
      if ('success' in result && result.success === false) {
        return result;
      }
      
      const response = result as Response;
      const data: DeveloperProductListResponse = await response.json();
      
      allProducts.push(...data.developerProducts);
      pageToken = data.nextPageToken;
    } while (pageToken);
    
    return { success: true, data: allProducts };
  }
  
  async getProduct(universeId: string, productId: string): Promise<CLIResult<DeveloperProduct>> {
    const url = `https://apis.roblox.com/developer-products/v2/universes/${universeId}/developer-products/${productId}/creator`;
    
    const result = await fetchWithRetry(
      url,
      {
        method: 'GET',
        headers: { 'x-api-key': this.apiKey },
      },
      'get'
    );
    
    if ('success' in result && result.success === false) {
      return result;
    }
    
    const response = result as Response;
    const data: DeveloperProduct = await response.json();
    
    return { success: true, data };
  }
  
  async createProduct(universeId: string, data: CreateDeveloperProductRequest): Promise<CLIResult<DeveloperProduct>> {
    const boundary = `----FormBoundary${Date.now()}_${Math.random().toString(36).slice(2)}`;
    const iconFile = data.iconFile ?? generatePlaceholderIcon();
    
    const fields: Record<string, string | Buffer> = {
      name: data.name,
      description: data.description ?? '',
      price: (data.price ?? 0).toString(),
      isForSale: (data.isForSale ?? false).toString(),
      File: iconFile,
    };
    
    const body = buildMultipartBody(fields, boundary);
    
    const result = await fetchWithRetry(
      `https://apis.roblox.com/developer-products/v2/universes/${universeId}/developer-products`,
      {
        method: 'POST',
        headers: {
          'x-api-key': this.apiKey,
          'Content-Type': `multipart/form-data; boundary=${boundary}`,
        },
        body: new Uint8Array(body),
      },
      'create'
    );
    
    if ('success' in result && result.success === false) {
      return result;
    }
    
    const response = result as Response;
    const responseData: DeveloperProduct = await response.json();
    
    return { success: true, data: responseData };
  }
  
  async updateProduct(universeId: string, productId: string, data: UpdateDeveloperProductRequest): Promise<CLIResult<DeveloperProduct>> {
    const boundary = `----FormBoundary${Date.now()}_${Math.random().toString(36).slice(2)}`;
    
    const fields: Record<string, string> = {};
    if (data.name !== undefined) fields.name = data.name;
    if (data.description !== undefined) fields.description = data.description;
    if (data.price !== undefined) fields.price = data.price.toString();
    if (data.isForSale !== undefined) fields.isForSale = data.isForSale.toString();
    
    const body = buildMultipartBody(fields, boundary);
    
    const result = await fetchWithRetry(
      `https://apis.roblox.com/developer-products/v2/universes/${universeId}/developer-products/${productId}`,
      {
        method: 'PATCH',
        headers: {
          'x-api-key': this.apiKey,
          'Content-Type': `multipart/form-data; boundary=${boundary}`,
        },
        body: new Uint8Array(body),
      },
      'update'
    );
    
    if ('success' in result && result.success === false) {
      return result;
    }
    
    const response = result as Response;
    const responseData: DeveloperProduct = await response.json();
    
    return { success: true, data: responseData };
  }
}
