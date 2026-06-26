import { callRapidApi } from "./lib/engine.js";
import {
  loadRegistry,
  requireAction,
  extractParams,
  applyParamMapping,
  applyPathParams
} from "./lib/registry.js";
import { getByPath } from "./lib/normalize.js";
import { toErrorResult, HttpError } from "./lib/errors.js";

export async function createRapidApiSkill(options = {}) {
  const primaryEnv = options.primaryEnv || "RAPIDAPI_KEY";
  const injectedEnv = options.env || {};
  const config = options.config || {};
  const rapidApiKey =
    options.apiKey ||
    options.rapidApiKey ||
    config.rapidApiKey ||
    injectedEnv[primaryEnv] ||
    process.env[primaryEnv];
  const templatesDir =
    options.templatesDir || config.templatesDir || "./templates";
  const allowNonRapidApiHosts =
    typeof options.allowNonRapidApiHosts === "boolean"
      ? options.allowNonRapidApiHosts
      : typeof config.allowNonRapidApiHosts === "boolean"
      ? config.allowNonRapidApiHosts
      : String(process.env.ALLOW_NON_RAPIDAPI_HOSTS || "true").toLowerCase() === "true";
  const timeoutMs =
    typeof options.timeoutMs === "number"
      ? options.timeoutMs
      : typeof config.timeoutMs === "number"
      ? config.timeoutMs
      : process.env.RAPIDAPI_TIMEOUT_MS
      ? Number(process.env.RAPIDAPI_TIMEOUT_MS)
      : 15000;

  if (!rapidApiKey) {
    throw new Error(`${primaryEnv} is required`);
  }

  const registry = await loadRegistry(templatesDir);

  async function callAction(name, input = {}) {
    const action = requireAction(registry, name);
    const meta = {
      host: action.template.host,
      path: action.template.path,
      method: action.template.method || "GET"
    };

    try {
      if (input && typeof input !== "object") {
        throw new HttpError(400, "Input must be an object");
      }

      const mapping = applyParamMapping(input, action.template.paramMapping);

      const query = {
        ...extractParams(input, action.template.querySchema),
        ...mapping.query
      };
      const body = {
        ...extractParams(input, action.template.bodySchema),
        ...mapping.body
      };
      const pathParams = {
        ...extractParams(input, action.template.pathParams),
        ...mapping.path
      };
      const headers = {
        ...(action.template.headers || {}),
        ...extractParams(input, action.template.headerSchema),
        ...mapping.header
      };

      const finalPath = applyPathParams(action.template.path, pathParams);

      const result = await callRapidApi(
        {
          host: action.template.host,
          path: finalPath,
          method: action.template.method,
          query,
          body,
          headers,
          timeoutMs: action.template.timeoutMs,
          responseType: action.template.response?.type || "json"
        },
        rapidApiKey,
        allowNonRapidApiHosts,
        timeoutMs
      );

      const errorPath = action.template.response?.errorPath;
      if (errorPath) {
        const maybeError = getByPath(result.data, errorPath);
        if (maybeError) {
          throw new HttpError(502, "RapidAPI error payload", maybeError);
        }
      }

      if (action.template.response?.normalize) {
        const normalized = {};
        for (const [key, pathValue] of Object.entries(
          action.template.response.normalize
        )) {
          normalized[key] = getByPath(result.data, pathValue);
        }
        result.data = normalized;
      } else if (action.template.response?.dataPath) {
        result.data = getByPath(result.data, action.template.response.dataPath);
      }

      return result;
    } catch (err) {
      return toErrorResult(err, meta);
    }
  }

  async function callRapidApiDirect(input) {
    const meta = { host: input?.host || "unknown", path: input?.path || "unknown", method: input?.method || "unknown" };
    try {
      return await callRapidApi(
        input,
        rapidApiKey,
        allowNonRapidApiHosts,
        timeoutMs
      );
    } catch (err) {
      return toErrorResult(err, meta);
    }
  }

  return {
    listActions: () => registry.list(),
    callAction,
    callRapidApi: callRapidApiDirect
  };
}
