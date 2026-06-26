import { describe, expect, test } from "bun:test";
import { selectBackend } from "../../../src/twitter/backends/factory";

describe("selectBackend", () => {
  test("returns null when no credentials", () => {
    const result = selectBackend({} as NodeJS.ProcessEnv);
    expect(result).toBeNull();
  });

  test("uses twitterapiio when TWITTERAPI_IO_KEY is set", () => {
    const result = selectBackend({ TWITTERAPI_IO_KEY: "test-key" } as NodeJS.ProcessEnv);
    expect(result).not.toBeNull();
    expect(typeof result?.fetch).toBe("function");
  });

  test("uses official when only X_BEARER_TOKEN is set", () => {
    const result = selectBackend({ X_BEARER_TOKEN: "test-token" } as NodeJS.ProcessEnv);
    expect(result).not.toBeNull();
    expect(typeof result?.fetch).toBe("function");
  });

  test("prefers twitterapiio when both credentials present (auto)", () => {
    const result = selectBackend({
      TWITTERAPI_IO_KEY: "test-key",
      X_BEARER_TOKEN: "test-token",
    } as NodeJS.ProcessEnv);
    expect(result).not.toBeNull();
  });

  test("explicit twitterapiio backend with missing key returns null", () => {
    const result = selectBackend({ TWITTER_API_BACKEND: "twitterapiio" } as NodeJS.ProcessEnv);
    expect(result).toBeNull();
  });

  test("explicit official backend with missing token returns null", () => {
    const result = selectBackend({ TWITTER_API_BACKEND: "official" } as NodeJS.ProcessEnv);
    expect(result).toBeNull();
  });
});
