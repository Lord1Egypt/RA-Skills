import type { ServerConfig } from "../config.js";
import { MemoryRepository } from "./memoryRepository.js";
import { MongoRepository } from "./mongoRepository.js";
import type { PlatformRepository } from "./types.js";

export function createRepository(config: ServerConfig): PlatformRepository {
  if (config.mongoUri) {
    return new MongoRepository(config.mongoUri, config.mongoDbName);
  }
  return new MemoryRepository();
}
