export type ServerConfig = {
  host: string;
  port: number;
  baseUrl: string;
  publicBaseUrl?: string;
  sessionCookie: string;
  upstreamApiKey?: string;
  accessKeys: Set<string>;
  mongoUri?: string;
  mongoDbName: string;
  knowledgeModelApiBase: string;
  knowledgeModelApiKey?: string;
  knowledgeModelName: string;
  knowledgeEvaluationModelName: string;
};

const DEFAULT_KNOWLEDGE_MODEL_API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1";
const DEFAULT_KNOWLEDGE_MODEL_NAME = "qwen-plus";

function isLocalHostname(hostname: string): boolean {
  const normalized = hostname.trim().toLowerCase();
  return normalized === "localhost" || normalized === "127.0.0.1" || normalized === "::1";
}

function parseAbsoluteUrl(value: string, envName: string): URL {
  let parsed: URL;
  try {
    parsed = new URL(value);
  } catch {
    throw new Error(`${envName} must be a valid absolute URL.`);
  }
  if (!["http:", "https:"].includes(parsed.protocol)) {
    throw new Error(`${envName} must use http or https.`);
  }
  return parsed;
}

function requireHttpsForRemoteUrl(parsed: URL, envName: string): void {
  if (parsed.protocol !== "https:" && !isLocalHostname(parsed.hostname)) {
    throw new Error(`${envName} must use https outside local development.`);
  }
}

export function getConfig(): ServerConfig {
  const configuredBaseUrl = process.env.VIDEOMP3WORD_BASE_URL?.trim() || "https://videomp3word.com";
  const sessionCookie = process.env.VIDEOMP3WORD_SESSION_COOKIE?.trim();
  if (!sessionCookie) {
    throw new Error("VIDEOMP3WORD_SESSION_COOKIE is required. Use a dedicated upstream videomp3word account for this deployment.");
  }
  if (!sessionCookie.includes("=")) {
    throw new Error("VIDEOMP3WORD_SESSION_COOKIE must be a valid cookie header value such as session=your-cookie.");
  }

  const parsedBaseUrl = parseAbsoluteUrl(configuredBaseUrl, "VIDEOMP3WORD_BASE_URL");
  requireHttpsForRemoteUrl(parsedBaseUrl, "VIDEOMP3WORD_BASE_URL");

  const allowedUpstreamHosts = new Set(
    String(process.env.VIDEOMP3WORD_ALLOWED_UPSTREAM_HOSTS || "videomp3word.com,www.videomp3word.com")
      .split(",")
      .map((value) => value.trim().toLowerCase())
      .filter(Boolean)
  );
  const upstreamHost = parsedBaseUrl.hostname.toLowerCase();
  if (!allowedUpstreamHosts.has(upstreamHost)) {
    throw new Error(`VIDEOMP3WORD_BASE_URL host "${upstreamHost}" is not allowed. Configure VIDEOMP3WORD_ALLOWED_UPSTREAM_HOSTS to permit it.`);
  }

  // Keep the MCP defaults aligned with the original videomp3word deployment.
  const knowledgeModelApiBase = parseAbsoluteUrl(
    process.env.KNOWLEDGE_MODEL_API_BASE?.trim() || DEFAULT_KNOWLEDGE_MODEL_API_BASE,
    "KNOWLEDGE_MODEL_API_BASE",
  );
  requireHttpsForRemoteUrl(knowledgeModelApiBase, "KNOWLEDGE_MODEL_API_BASE");

  const publicBaseUrl = process.env.PUBLIC_BASE_URL?.trim();
  if (publicBaseUrl) {
    parseAbsoluteUrl(publicBaseUrl, "PUBLIC_BASE_URL");
  }

  const portValue = Number(process.env.PORT || 3000);
  if (!Number.isInteger(portValue) || portValue < 0 || portValue > 65535) {
    throw new Error("PORT must be an integer between 0 and 65535.");
  }

  const accessKeys = new Set(
    String(process.env.MCP_ACCESS_KEYS || "")
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean)
  );
  const nodeEnv = String(process.env.NODE_ENV || "").trim().toLowerCase();
  if (nodeEnv === "production" && accessKeys.size === 0) {
    throw new Error("MCP_ACCESS_KEYS must be configured in production.");
  }

  return {
    host: process.env.HOST || "0.0.0.0",
    port: portValue,
    baseUrl: parsedBaseUrl.toString().replace(/\/+$/, ""),
    publicBaseUrl: publicBaseUrl?.replace(/\/+$/, ""),
    sessionCookie,
    upstreamApiKey: process.env.VIDEOMP3WORD_API_KEY?.trim(),
    accessKeys,
    mongoUri: process.env.MONGO_URI?.trim(),
    mongoDbName: process.env.MONGO_DB_NAME?.trim() || "videomp3word_mcp",
    knowledgeModelApiBase: knowledgeModelApiBase.toString().replace(/\/+$/, ""),
    knowledgeModelApiKey: process.env.KNOWLEDGE_MODEL_API_KEY?.trim() || process.env.DASHSCOPE_API_KEY?.trim(),
    knowledgeModelName: process.env.KNOWLEDGE_MODEL_NAME?.trim() || DEFAULT_KNOWLEDGE_MODEL_NAME,
    knowledgeEvaluationModelName:
      process.env.KNOWLEDGE_EVALUATION_MODEL_NAME?.trim() ||
      process.env.KNOWLEDGE_MODEL_NAME?.trim() ||
      DEFAULT_KNOWLEDGE_MODEL_NAME,
  };
}

export const serverConfig = getConfig();
