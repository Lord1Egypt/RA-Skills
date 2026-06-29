# Edge Function Development

Use this reference when the user needs Supabase Edge Function examples or old-skill-compatible deployment. Current `ve aidap` does not deploy Supabase Edge Functions; use the preserved data-plane command.

## Basic Deno Function

```typescript
Deno.serve(async (req) => {
  const { pathname } = new URL(req.url);
  if (pathname === "/health") {
    return Response.json({ ok: true });
  }
  return new Response("not found", { status: 404 });
});
```

Deploy from a file:

```bash
python3 scripts/supabase_dataplane.py deploy-edge-function --workspace-id ws-xxxx --function-name health --source-file ./index.ts
```

Deploy a public endpoint without JWT verification:

```bash
python3 scripts/supabase_dataplane.py deploy-edge-function --workspace-id ws-xxxx --function-name webhook --source-file ./webhook.ts --no-verify-jwt
```

## CORS

```typescript
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }
  return Response.json({ ok: true }, { headers: corsHeaders });
});
```

## Auth-Aware Database Access

```typescript
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

Deno.serve(async (req) => {
  const authHeader = req.headers.get("Authorization") ?? "";
  const client = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_ANON_KEY")!,
    { global: { headers: { Authorization: authHeader } } },
  );

  const { data, error } = await client.from("posts").select("*").limit(20);
  if (error) {
    return Response.json({ error: error.message }, { status: 500 });
  }
  return Response.json({ data });
});
```

Use anon-key clients when user identity and RLS should apply. Keep service-role keys server-side and only use them for trusted administrative logic.

## Management Commands

```bash
python3 scripts/supabase_dataplane.py list-edge-functions --workspace-id ws-xxxx
python3 scripts/supabase_dataplane.py get-edge-function --workspace-id ws-xxxx --function-name health
python3 scripts/supabase_dataplane.py delete-edge-function --workspace-id ws-xxxx --function-name health
```

## Runtime Notes

- Default runtime is `native-node20/v1`.
- Supported compatibility runtimes also include `native-python3.9/v1`, `native-python3.10/v1`, and `native-python3.12/v1`.
- Node functions that export a default handler are wrapped with a generated `Deno.serve` entrypoint, matching the old skill behavior.
- Keep functions small and avoid long blocking work; Edge Function execution has time limits.
