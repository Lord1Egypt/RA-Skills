# Recipes

Copy-paste patterns. Vendor-neutral: open protocols (SMTP, S3 API, standard webhooks) over proprietary SDKs. Swap providers via config, not code.

## 1. Current User Helper

Centralises the lookup so every handler returns the same `NotFound` when the session outlives the user. `DbConn` runs in both queries (non-transactional) and mutations (transactional).

Inverted calling convention: `db.fetch_optional(query)`, not `query.fetch_optional(db)` — `DbConn` is not a sqlx `Executor`.

```rust
// src/utils/current_user.rs
use forge::prelude::*;

pub async fn current_user(db: DbConn<'_>, user_id: Uuid) -> Result<User> {
    db.fetch_optional(
        sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", user_id)
    )
    .await?
    .ok_or_else(|| ForgeError::NotFound(format!("user {user_id}")))
}
```

Use from a query or mutation — both expose `ctx.db_conn()`:

```rust
#[forge::query]
pub async fn my_profile(ctx: &QueryContext) -> Result<User> {
    current_user(ctx.db_conn(), ctx.user_id()?).await
}

#[forge::mutation]
pub async fn update_profile(ctx: &MutationContext, name: String) -> Result<User> {
    let user = current_user(ctx.db_conn(), ctx.user_id()?).await?;
    // ... the DbConn call above participated in the same transaction as ctx.conn()
    Ok(user)
}
```

## 2. Plan Gating Helper

Never use `ForgeError::Forbidden` for billing state — it logs the user out. Use `InvalidArgument` or a custom error mapped through the frontend error handler. See [Pitfalls](./pitfalls.md#7-authentication).

Plan gating runs from mutations, so take `&mut ForgeConn` (the one from `ctx.conn().await?`). It reuses the active transaction and supports every sqlx macro — including `query_scalar!`, which `DbConn` doesn't wrap.

```rust
// src/utils/plan.rs
pub async fn require_plan(
    conn: &mut ForgeConn<'_>,
    user_id: Uuid,
    min_plan: Plan,
) -> Result<()> {
    let current = sqlx::query_scalar!(
        r#"SELECT plan as "plan: Plan" FROM subscriptions
           WHERE user_id = $1 AND status = 'active'"#,
        user_id
    )
    .fetch_optional(&mut *conn)
    .await?
    .unwrap_or(Plan::Free);

    if current < min_plan {
        return Err(ForgeError::InvalidArgument(format!(
            "feature requires {min_plan:?} plan, current: {current:?}"
        )));
    }
    Ok(())
}
```

Call site:

```rust
#[forge::mutation]
pub async fn start_export(ctx: &MutationContext) -> Result<Uuid> {
    let mut conn = ctx.conn().await?;
    require_plan(&mut conn, ctx.user_id()?, Plan::Pro).await?;
    // ... proceed with premium work, all in the same transaction
    Ok(Uuid::new_v4())
}
```

## 3. Pagination

Two patterns — pick by collection size and sort stability.

**LIMIT/OFFSET** for small, user-bounded lists with acceptable page numbers:

```rust
#[forge::query]
pub async fn list_items(ctx: &QueryContext, args: PageArgs) -> Result<Page<Item>> {
    let limit = args.limit.clamp(1, 100);
    let offset = args.page.saturating_mul(limit);
    let items = sqlx::query_as!(
        Item,
        "SELECT * FROM items WHERE user_id = $1 \
         ORDER BY created_at DESC LIMIT $2 OFFSET $3",
        ctx.user_id()?, limit as i64, offset as i64,
    )
    .fetch_all(ctx.db())
    .await?;
    let has_more = items.len() as i64 == limit as i64;
    Ok(Page { items, has_more })
}
```

**Cursor** for infinite scroll and stable ordering under concurrent inserts:

```rust
#[forge::query]
pub async fn feed(ctx: &QueryContext, args: CursorArgs) -> Result<CursorPage<Post>> {
    let items = sqlx::query_as!(
        Post,
        "SELECT * FROM posts
         WHERE user_id = $1 AND ($2::TIMESTAMPTZ IS NULL OR created_at < $2)
         ORDER BY created_at DESC LIMIT $3",
        ctx.user_id()?, args.cursor, args.limit.clamp(1, 50) as i64,
    )
    .fetch_all(ctx.db())
    .await?;
    let next = items.last().map(|p| p.created_at);
    Ok(CursorPage { items, next_cursor: next })
}
```

## 4. Transactional Email (Askama + SMTP)

[`askama`](https://docs.rs/askama) for compile-checked templates, [`lettre`](https://docs.rs/lettre) for vendor-neutral SMTP. Works with SES, SendGrid, Postmark, Mailgun, self-hosted Postfix.

```rust
// src/email.rs
use askama::Template;

#[derive(Template)]
#[template(path = "welcome.html")]
struct WelcomeEmail<'a> {
    name: &'a str,
    login_url: &'a str,
}

#[forge::job(retry(max_attempts = 5), idempotent, key = "args.user_id")]
pub async fn send_welcome(ctx: &JobContext, args: SendWelcomeArgs) -> Result<()> {
    let user = current_user(ctx.db_conn(), args.user_id).await?;

    let login_url = ctx.env_require("APP_URL")?;
    let html = WelcomeEmail { name: &user.name, login_url: &login_url }
        .render()
        .map_err(|e| ForgeError::Internal(e.to_string()))?;

    let smtp_url = ctx.env_require("SMTP_URL")?;
    // ... build lettre transport from smtp_url and send `html` ...
    Ok(())
}

#[derive(Debug, serde::Serialize, serde::Deserialize)]
pub struct SendWelcomeArgs { pub user_id: Uuid }
```

- **Dispatch from a mutation**: `ctx.dispatch_job("send_welcome", SendWelcomeArgs { user_id }).await?` inside a mutation so the email is only queued if the transaction commits (transactions are on by default). See [Patterns](./patterns.md#background-jobs).
- **Idempotency**: the `key = "args.user_id"` attribute names a path into the args struct. Combined with the job's retry policy, it prevents a duplicate send when a worker crashes after sending but before marking the job complete.

## 5. File Upload to S3-Compatible Storage

S3 is a protocol, not a vendor. [`aws-sdk-s3`](https://docs.rs/aws-sdk-s3) with a custom `endpoint_url` talks to AWS S3, Cloudflare R2, Backblaze B2, MinIO, Wasabi, Tigris, DigitalOcean Spaces.

```rust
// src/storage.rs — one helper initialised from env
pub async fn s3_client(ctx: &MutationContext) -> Result<aws_sdk_s3::Client> {
    let endpoint = ctx.env_require("S3_ENDPOINT")?;
    let region = ctx.env_or("S3_REGION", "auto");
    // Credentials from S3_ACCESS_KEY_ID / S3_SECRET_ACCESS_KEY
    // Build and return client...
}

#[forge::mutation]
pub async fn upload_avatar(ctx: &MutationContext, file: Upload) -> Result<String> {
    let key = format!("avatars/{}/{}", ctx.user_id()?, Uuid::new_v4());
    let bucket = ctx.env_require("S3_BUCKET")?;
    s3_client(ctx).await?
        .put_object()
        .bucket(&bucket)
        .key(&key)
        .body(file.into_stream().into())
        .send().await
        .map_err(|e| ForgeError::Internal(format!("upload failed: {e}")))?;

    let mut conn = ctx.conn().await?;
    sqlx::query!("UPDATE users SET avatar_key = $1 WHERE id = $2", key, ctx.user_id()?)
        .execute(&mut conn).await?;
    Ok(key)
}
```

`Upload` is codegen-recognised: frontend clients switch to `multipart/form-data` automatically when given `File` / `Blob`.

## 6. Payment Webhook → Job → Mutation

Stripe, Polar, Paddle, LemonSqueezy all follow the same shape: signed webhook → validate → ack fast → do heavy work asynchronously. Isolate provider-specific decoding at the webhook boundary.

```rust
#[forge::webhook(
    path = "/webhooks/payments",
    signature = WebhookSignature::standard_webhooks("PAYMENTS_WEBHOOK_SECRET"),
    idempotency = "header:webhook-id"
)]
pub async fn payments_webhook(ctx: &WebhookContext, event: PaymentEvent) -> Result<WebhookResult> {
    ctx.dispatch_job("process_payment_event", event).await?;
    Ok(WebhookResult::Accepted)
}

#[forge::job(retry(max_attempts = 5, backoff = "exponential"), idempotent, key = "args.id")]
pub async fn process_payment_event(ctx: &JobContext, args: PaymentEvent) -> Result<()> {
    match args.kind {
        PaymentEventKind::SubscriptionUpdated => update_subscription(ctx, args).await?,
        PaymentEventKind::InvoicePaid => mark_invoice_paid(ctx, args).await?,
        _ => {} // Unknown event types are logged and ignored
    }
    Ok(())
}
```

- **Race with checkout confirmation**: the webhook and the synchronous checkout return can arrive in any order. Use `COALESCE($1, column)` in updates so a slow webhook cannot clobber data set by the faster path. See [Patterns](./patterns.md#webhooks).
- **Provider swap**: to move from one provider to another, change the signature constructor and the event decoder. Handler logic stays identical.

## 7. AI Features via Jobs + Progress + Subscriptions

Forge ships no LLM abstraction — existing primitives cover it. `#[job]` for long generations, `ctx.progress()` for streaming updates, `#[query]` subscriptions for the UI. `#[workflow]` for durable multi-turn flows.

`ctx.http()` buffers the full response (right for RPC JSON). For SSE-style token streaming, use `ctx.raw_http()` to get the underlying `reqwest::Client` and `.bytes_stream()`.

```rust
use futures_util::StreamExt;

#[forge::mutation]
pub async fn ask_question(ctx: &MutationContext, args: AskArgs) -> Result<Uuid> {
    let mut conn = ctx.conn().await?;
    let id = sqlx::query_scalar!(
        "INSERT INTO llm_calls (user_id, prompt, status) \
         VALUES ($1, $2, 'pending') RETURNING id",
        ctx.user_id()?, args.prompt,
    )
    .fetch_one(&mut conn).await?;

    ctx.dispatch_job("run_completion", RunArgs { call_id: id }).await?;
    Ok(id)
}

#[forge::job(timeout = "5m")]
pub async fn run_completion(ctx: &JobContext, args: RunArgs) -> Result<()> {
    let prompt = load_prompt(ctx, args.call_id).await?;
    let api_key = ctx.env_require("OPENAI_API_KEY")?;

    // raw_http() is reqwest::Client — use bytes_stream() for streaming responses.
    let response = ctx.raw_http()
        .post("https://api.openai.com/v1/chat/completions")
        .bearer_auth(api_key)
        .json(&serde_json::json!({
            "model": "gpt-4o-mini",
            "stream": true,
            "messages": [{ "role": "user", "content": prompt }],
        }))
        .send().await
        .map_err(|e| ForgeError::Internal(e.to_string()))?;

    let mut stream = response.bytes_stream();
    let mut buf = String::new();
    while let Some(chunk) = stream.next().await {
        let bytes = chunk.map_err(|e| ForgeError::Internal(e.to_string()))?;
        for delta in parse_sse_deltas(&bytes) {
            buf.push_str(&delta);
            ctx.progress(0, &buf)?;   // partial text flows to the UI via subscription
            ctx.check_cancelled().await?;
        }
    }

    sqlx::query!(
        "UPDATE llm_calls SET status = 'completed', response = $1 WHERE id = $2",
        buf, args.call_id,
    )
    .execute(ctx.db())
    .await?;
    Ok(())
}

#[forge::query]
pub async fn get_call(ctx: &QueryContext, id: Uuid) -> Result<LlmCall> {
    sqlx::query_as!(
        LlmCall,
        "SELECT * FROM llm_calls WHERE id = $1 AND user_id = $2",
        id, ctx.user_id()?,
    )
    .fetch_optional(ctx.db()).await?
    .ok_or_else(|| ForgeError::NotFound(format!("call {id}")))
}
```

Frontend subscribes to `getCall$({ id })` — SSE delivers each `UPDATE` as a new snapshot. No custom WebSocket plumbing. For in-flight token streaming, skip the DB write-side entirely: have the query re-run on a separate event table you `UPDATE` inside the while-loop. Swap providers by changing URL + payload shape; the handler pattern is identical.

- **Cost tracking**: add `input_tokens`, `output_tokens`, `cost_usd` columns on `llm_calls` for per-user billing — no separate service needed.
- **Conversation memory**: `#[forge::workflow]` + `ctx.step()` persists turn state across days. See [Patterns](./patterns.md#durable-workflows).
