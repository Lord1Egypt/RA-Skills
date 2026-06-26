import { resolveAppState } from "./config.js";
import { exitWithError, normalizePath, printJson, sanitizeForOutput } from "./utils.js";

export async function performRequest(state, config, request) {
  const appState = resolveAppState(state, config);
  if (!appState.apiKey && !state.dryRun) {
    const guidance = [
      "Use --api-key, set TWEXAPI_KEY, or configure an app with auth apps add.",
      "Get an API key here: https://twexapi.io/dashboard",
      'Example: twexapi auth apps add --name prod --api-key "twitterx_..."',
    ].join("\n");
    exitWithError("Missing API key.", guidance);
  }

  const target = normalizePath(request.path);
  const url = /^https?:\/\//i.test(target) ? target : `${appState.baseUrl}${target}`;
  const headers = {
    Accept: "application/json",
    ...state.headers,
    ...request.headers,
  };

  if (appState.apiKey) {
    headers.Authorization = `Bearer ${appState.apiKey}`;
  }

  let body;
  if (request.body !== undefined) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
    body = headers["Content-Type"].includes("application/json")
      ? JSON.stringify(request.body)
      : String(request.body);
  }

  if (state.dryRun) {
    const preview = sanitizeForOutput({
      method: request.method,
      url,
      headers,
      ...(body
        ? {
            body: headers["Content-Type"]?.includes("application/json") ? JSON.parse(body) : body,
          }
        : {}),
    });
    printJson(preview);
    return { dryRun: true, data: preview };
  }

  const response = await fetch(url, {
    method: request.method,
    headers,
    body,
  });

  const text = await response.text();
  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  let data = text;

  if (isJson && text) {
    try {
      data = JSON.parse(text);
    } catch (error) {
      exitWithError("Failed to parse JSON response.", error.message);
    }
  }

  if (!response.ok) {
    if (isJson) {
      console.error(JSON.stringify(data, null, 2));
    } else {
      console.error(text);
    }
    process.exit(response.status || 1);
  }

  if (!request.silent) {
    if (state.raw || !isJson) {
      process.stdout.write(text);
      if (!text.endsWith("\n")) {
        process.stdout.write("\n");
      }
    } else {
      printJson(data);
    }
  }

  return {
    response,
    text,
    isJson,
    data,
  };
}
