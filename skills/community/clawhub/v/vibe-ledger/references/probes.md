# Probes

Deterministic checks that run during `start`. Each finding has a `level`: `certain` (the code says so), `hint` (likely, confirm in the code) or `fact` (a neutral observation). A probe that does not apply to the project is skipped and listed in the report; a probe that crashes is listed too.

| Probe | Runs for | Checks | Blind spots |
|---|---|---|---|
| `secrets_exposed` | every project | env vars starting with `NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`, `REACT_APP_` that hold a real secret or are named SECRET/SERVICE_ROLE/PRIVATE/PASSWORD; OpenAI/Anthropic/Stripe/AWS/GitHub/Slack keys and service-role JWTs written in code; `.env` files tracked by git | keys set in a hosting dashboard; secrets in formats it does not know. Supabase anon keys and Stripe publishable keys are public by design and not reported. |
| `supabase_rls` | Supabase projects | tables created without enabling row level security, RLS switched off, policies with `using (true)`, tables used in code but missing from migrations, the service-role key in browser code | anything changed in the Supabase dashboard rather than in migrations: a table created without RLS here may have it switched on there (so that finding fills no access cells) |
| `firebase_rules` | Firebase projects | rules that allow everything (`if true`), test-mode rules (`request.time < timestamp.date(...)`), Realtime Database rules set to `true` | rules deployed from the console and not in the repo |
| `cors_wildcard` | every project | `origin: '*'`, `Access-Control-Allow-Origin: *`, `cors()` with no options; notes when credentials are allowed too | CORS set on a proxy or hosting platform |
| `paid_api_unauthed` | Next.js, Express | server endpoints that import a paid SDK (OpenAI, Anthropic, Replicate, Stripe, Twilio, Resend, Google AI, Groq, Cohere, ElevenLabs) directly or through one local import, with no login check in the file | login enforced by middleware in another file (a false alarm — hence `hint`); rate limits are not checked |
| `routes` | Next.js, Express | pages (`PAGE /x`), API routes (`API /api/x`, `POST /api/x`) and Express routes | routes built dynamically |

Stacks with no probes (Flask, Django, FastAPI, Rails, Go, PHP, …) are named in the report as "not covered"; their promises can still be checked by reading the code.
