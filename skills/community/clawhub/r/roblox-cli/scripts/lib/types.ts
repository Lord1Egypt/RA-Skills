export interface GameCreator {
  id: number;
  type: string;
  name: string;
}

export interface Game {
  id: number;
  name: string;
  rootPlaceId: number;
  creator: GameCreator;
}

export interface GamesListResponse {
  data: Game[];
  nextPageCursor?: string;
}

export interface GamePassPriceInformation {
  defaultPriceInRobux?: number;
  enabledFeatures?: string[];
}

export interface GamePass {
  gamePassId: number;
  name: string;
  description?: string;
  isForSale?: boolean;
  iconImageAssetId?: number;
  priceInformation?: GamePassPriceInformation;
}

export interface GamePassListResponse {
  gamePasses: GamePass[];
  nextPageToken?: string;
}

export interface DeveloperProductPriceInformation {
  defaultPriceInRobux?: number;
  enabledFeatures?: string[];
}

export interface DeveloperProduct {
  productId: number;
  name: string;
  description?: string;
  isForSale?: boolean;
  iconImageAssetId?: number;
  storePageEnabled?: boolean;
  priceInformation?: DeveloperProductPriceInformation;
}

export interface DeveloperProductListResponse {
  developerProducts: DeveloperProduct[];
  nextPageToken?: string;
}

export interface RobloxError {
  code: string;
  message: string;
}

export interface RobloxErrorResponse {
  errors?: RobloxError[];
}

export interface CLISuccess<T> {
  success: true;
  data: T;
}

export interface CLIError {
  success: false;
  error: {
    code: string;
    message: string;
  };
}

export type CLIResult<T> = CLISuccess<T> | CLIError;

export interface CreateGamePassRequest {
  name: string;
  description?: string;
  price?: number;
  isForSale?: boolean;
  iconFile?: Buffer;
}

export interface UpdateGamePassRequest {
  name?: string;
  description?: string;
  price?: number;
  isForSale?: boolean;
}

export interface CreateDeveloperProductRequest {
  name: string;
  description?: string;
  price?: number;
  isForSale?: boolean;
  iconFile?: Buffer;
}

export interface UpdateDeveloperProductRequest {
  name?: string;
  description?: string;
  price?: number;
  isForSale?: boolean;
}

export interface JwtParseResult {
  ownerId: string | null;
  exp: number | null;
}

export type ErrorCode =
  | 'INVALID_ARGS'
  | 'API_ERROR'
  | 'NOT_FOUND'
  | 'RATE_LIMITED'
  | 'NETWORK_ERROR';
