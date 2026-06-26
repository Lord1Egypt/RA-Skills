import type { TwitterBackend } from "./types";
import { createTwitterApiIoBackend } from "./twitterapiio";
import { createOfficialBackend } from "./official";

export function selectBackend(env: NodeJS.ProcessEnv, fetcher: typeof fetch = fetch): TwitterBackend | null {
  const explicit = env.TWITTER_API_BACKEND;

  if (explicit === "twitterapiio") {
    const key = env.TWITTERAPI_IO_KEY;
    if (!key) {
      console.warn("[twitter/factory] TWITTER_API_BACKEND=twitterapiio but TWITTERAPI_IO_KEY is missing");
      return null;
    }
    return createTwitterApiIoBackend(key, fetcher);
  }

  if (explicit === "official") {
    const token = env.X_BEARER_TOKEN;
    if (!token) {
      console.warn("[twitter/factory] TWITTER_API_BACKEND=official but X_BEARER_TOKEN is missing");
      return null;
    }
    return createOfficialBackend(token, env, fetcher);
  }

  // auto
  if (env.TWITTERAPI_IO_KEY) {
    return createTwitterApiIoBackend(env.TWITTERAPI_IO_KEY, fetcher);
  }

  if (env.X_BEARER_TOKEN) {
    return createOfficialBackend(env.X_BEARER_TOKEN, env, fetcher);
  }

  return null;
}
