/** @jest-environment node */
import { request } from "../http.js";
import type { FetchLike, HttpResponse } from "../http.js";

function res(
  status: number,
  body: string,
  headers: Record<string, string> = {},
): HttpResponse {
  const lower: Record<string, string> = {};
  for (const [k, v] of Object.entries(headers)) lower[k.toLowerCase()] = v;
  return {
    status,
    headers: { get: (name: string) => lower[name.toLowerCase()] ?? null },
    text: async () => body,
  };
}

const RL_HEADERS = {
  "X-RateLimit-Limit": "100",
  "X-RateLimit-Remaining": "97",
  "X-RateLimit-Reset": "1753000000",
};

function fakeFetch(response: HttpResponse | Error): {
  fetchImpl: FetchLike;
  calls: { url: string; init: { method: string; headers: Record<string, string>; body?: string } }[];
} {
  const calls: { url: string; init: { method: string; headers: Record<string, string>; body?: string } }[] = [];
  const fetchImpl: FetchLike = async (url, init) => {
    calls.push({ url, init });
    if (response instanceof Error) throw response;
    return response;
  };
  return { fetchImpl, calls };
}

describe("request", () => {
  const base = { baseUrl: "https://tokei.io", apiKey: "tokei_k_test", path: "/me" };

  it("builds the /api/v1 URL, sends the bearer auth header, and appends query params", async () => {
    const { fetchImpl, calls } = fakeFetch(res(200, JSON.stringify({ ok: true }), RL_HEADERS));
    await request(
      { ...base, path: "/contests", query: { status: "active", per_page: "10" } },
      fetchImpl,
    );
    expect(calls).toHaveLength(1);
    const url = new URL(calls[0].url);
    expect(url.origin + url.pathname).toBe("https://tokei.io/api/v1/contests");
    expect(url.searchParams.get("status")).toBe("active");
    expect(url.searchParams.get("per_page")).toBe("10");
    expect(calls[0].init.method).toBe("GET");
    expect(calls[0].init.headers["Authorization"]).toBe("Bearer tokei_k_test");
  });

  it("augments a success body with a numeric rate_limit object", async () => {
    const { fetchImpl } = fakeFetch(res(200, JSON.stringify({ ok: true, data: 1 }), RL_HEADERS));
    const { payload, exitCode } = await request(base, fetchImpl);
    expect(exitCode).toBe(0);
    expect(payload).toEqual({
      ok: true,
      data: 1,
      rate_limit: { limit: 100, remaining: 97, reset: 1753000000 },
    });
  });

  it("sets rate_limit to null when the headers are absent", async () => {
    const { fetchImpl } = fakeFetch(res(200, JSON.stringify({ ok: true }), {}));
    const { payload } = await request(base, fetchImpl);
    expect(payload).toEqual({ ok: true, rate_limit: null });
  });

  it("passes a non-2xx JSON error body through, augmented, and exits 1", async () => {
    const errBody = { success: false, error: { code: "NOT_FOUND", message: "nope", status: 404 } };
    const { fetchImpl } = fakeFetch(res(404, JSON.stringify(errBody), RL_HEADERS));
    const { payload, exitCode } = await request(base, fetchImpl);
    expect(exitCode).toBe(1);
    expect(payload).toEqual({
      ...errBody,
      rate_limit: { limit: 100, remaining: 97, reset: 1753000000 },
    });
  });

  it("wraps a non-JSON error body as http_error and exits 1", async () => {
    const { fetchImpl } = fakeFetch(res(502, "<html>bad gateway</html>", RL_HEADERS));
    const { payload, exitCode } = await request(base, fetchImpl);
    expect(exitCode).toBe(1);
    expect(payload).toEqual({
      ok: false,
      error: { type: "http_error", status: 502, message: "<html>bad gateway</html>" },
      rate_limit: { limit: 100, remaining: 97, reset: 1753000000 },
    });
  });

  it("returns a network_error envelope (no rate_limit) and exits 1 when fetch throws", async () => {
    const { fetchImpl } = fakeFetch(new Error("ECONNREFUSED"));
    const { payload, exitCode } = await request(base, fetchImpl);
    expect(exitCode).toBe(1);
    expect(payload).toEqual({
      ok: false,
      error: { type: "network_error", message: "ECONNREFUSED" },
    });
  });

  it("strips a trailing slash from the base URL override", async () => {
    const { fetchImpl, calls } = fakeFetch(res(200, JSON.stringify({ ok: true }), {}));
    await request({ ...base, baseUrl: "http://localhost:3000/" }, fetchImpl);
    expect(calls[0].url).toBe("http://localhost:3000/api/v1/me");
  });
});

describe("request — write methods", () => {
  const base = { baseUrl: "https://tokei.io", apiKey: "tokei_k_test", path: "/promotions" };

  it("POST serialises the body as JSON with Content-Type, exit 0 on 201", async () => {
    const created = { success: true, data: { id: "p-1" } };
    const { fetchImpl, calls } = fakeFetch(res(201, JSON.stringify(created), RL_HEADERS));
    const { payload, exitCode } = await request(
      { ...base, method: "POST", body: { title: "Launch", status: "draft" } },
      fetchImpl,
    );
    expect(exitCode).toBe(0);
    expect(calls[0].init.method).toBe("POST");
    expect(calls[0].init.headers["Content-Type"]).toBe("application/json");
    expect(calls[0].init.body).toBe(JSON.stringify({ title: "Launch", status: "draft" }));
    expect(payload).toEqual({
      ...created,
      rate_limit: { limit: 100, remaining: 97, reset: 1753000000 },
    });
  });

  it("PATCH passes a 422 validation body through, augmented, and exits 1", async () => {
    const errBody = {
      success: false,
      error: {
        code: "VALIDATION_ERROR",
        message: "Invalid request body",
        details: [{ field: "end_date", message: "must be in the future" }],
      },
    };
    const { fetchImpl, calls } = fakeFetch(res(422, JSON.stringify(errBody), RL_HEADERS));
    const { payload, exitCode } = await request(
      { ...base, path: "/contests/c-1", method: "PATCH", body: { end_date: "2020-01-01" } },
      fetchImpl,
    );
    expect(exitCode).toBe(1);
    expect(calls[0].init.method).toBe("PATCH");
    expect(payload).toEqual({
      ...errBody,
      rate_limit: { limit: 100, remaining: 97, reset: 1753000000 },
    });
  });

  it("DELETE sends no body and no Content-Type header", async () => {
    const { fetchImpl, calls } = fakeFetch(res(200, JSON.stringify({ success: true }), {}));
    const { exitCode } = await request(
      { ...base, path: "/webhooks/w-1", method: "DELETE" },
      fetchImpl,
    );
    expect(exitCode).toBe(0);
    expect(calls[0].init.method).toBe("DELETE");
    expect(calls[0].init.body).toBeUndefined();
    expect(calls[0].init.headers["Content-Type"]).toBeUndefined();
  });
});
