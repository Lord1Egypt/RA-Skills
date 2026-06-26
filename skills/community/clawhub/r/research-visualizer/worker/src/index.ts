interface Env {
  BUCKET: R2Bucket;
}

const RATE_LIMIT_MAX = 30;
const RATE_LIMIT_WINDOW_MS = 60 * 60 * 1000;
const MAX_BODY_SIZE = 2 * 1024 * 1024;

const ipCounts = new Map<string, { count: number; resetAt: number }>();

function checkRateLimit(ip: string): boolean {
  const now = Date.now();
  const entry = ipCounts.get(ip);
  if (!entry || now > entry.resetAt) {
    ipCounts.set(ip, { count: 1, resetAt: now + RATE_LIMIT_WINDOW_MS });
    return true;
  }
  if (entry.count >= RATE_LIMIT_MAX) return false;
  entry.count++;
  return true;
}

function generateSlug(): string {
  const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
  let slug = "";
  const bytes = crypto.getRandomValues(new Uint8Array(8));
  for (const b of bytes) slug += chars[b % chars.length];
  return slug;
}

function corsHeaders(): HeadersInit {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    const url = new URL(request.url);

    // Serve files from R2
    if (request.method === "GET" && url.pathname.startsWith("/r/")) {
      const key = url.pathname.slice(1); // "r/slug.html"
      const obj = await env.BUCKET.get(key);
      if (!obj) return new Response("Not found", { status: 404 });
      return new Response(obj.body, {
        headers: {
          "Content-Type": "text/html; charset=utf-8",
          ...corsHeaders(),
        },
      });
    }

    if (request.method !== "POST" || url.pathname !== "/api/upload") {
      return new Response("Not found", { status: 404, headers: corsHeaders() });
    }

    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    if (!checkRateLimit(ip)) {
      return Response.json(
        { error: "Rate limit exceeded. Max 30 uploads per hour." },
        { status: 429, headers: corsHeaders() }
      );
    }

    const contentLength = parseInt(request.headers.get("content-length") || "0");
    if (contentLength > MAX_BODY_SIZE) {
      return Response.json(
        { error: "Body too large. Max 2MB." },
        { status: 413, headers: corsHeaders() }
      );
    }

    let body: { html?: string; slug?: string };
    try {
      body = await request.json();
    } catch {
      return Response.json(
        { error: "Invalid JSON" },
        { status: 400, headers: corsHeaders() }
      );
    }

    if (!body.html || typeof body.html !== "string") {
      return Response.json(
        { error: "Missing 'html' field" },
        { status: 400, headers: corsHeaders() }
      );
    }

    if (new TextEncoder().encode(body.html).length > MAX_BODY_SIZE) {
      return Response.json(
        { error: "HTML content too large. Max 2MB." },
        { status: 413, headers: corsHeaders() }
      );
    }

    const slug = body.slug && /^[a-z0-9_-]+$/i.test(body.slug) ? body.slug : generateSlug();
    const key = `r/${slug}.html`;

    await env.BUCKET.put(key, body.html, {
      httpMetadata: { contentType: "text/html; charset=utf-8" },
    });

    return Response.json(
      { url: `https://r.a2ui.me/r/${slug}.html` },
      { status: 200, headers: corsHeaders() }
    );
  },
} satisfies ExportedHandler<Env>;
