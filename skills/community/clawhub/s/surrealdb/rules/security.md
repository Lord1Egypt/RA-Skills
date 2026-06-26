# SurrealDB Security

SurrealDB has a layered security model built into the database itself, eliminating the need for separate middleware or application-level permission checks in many cases. Authentication, authorization, and row-level security are all defined in SurrealQL and enforced by the database engine.

---

## Authentication Hierarchy

SurrealDB uses a four-level authentication hierarchy. Each level has access to its scope and everything beneath it.

```
Root User
  |-- Full system access (all namespaces, databases, tables)
  |
  +-- Namespace User
       |-- Access to all databases within a namespace
       |
       +-- Database User
            |-- Access to all tables within a database
            |
            +-- Record User
                 |-- Access governed by table PERMISSIONS
                 |-- Authenticated via DEFINE ACCESS ... TYPE RECORD
```

### Root Users

Root users have unrestricted access to the entire SurrealDB instance. Use them only for administrative operations.

```surrealql
-- Define a root user (requires existing root access)
DEFINE USER admin ON ROOT PASSWORD 'strong-password-here' ROLES OWNER;
DEFINE USER operator ON ROOT PASSWORD 'another-password' ROLES EDITOR;
DEFINE USER readonly ON ROOT PASSWORD 'readonly-pass' ROLES VIEWER;

-- Roles:
-- OWNER: full control (create/drop namespaces, manage users)
-- EDITOR: read/write data, manage schemas
-- VIEWER: read-only access
```

### Namespace Users

Namespace users can access all databases within their namespace but cannot access other namespaces.

```surrealql
USE NS production;

DEFINE USER ns_admin ON NAMESPACE PASSWORD 'ns-password' ROLES OWNER;
DEFINE USER ns_dev ON NAMESPACE PASSWORD 'dev-password' ROLES EDITOR;
DEFINE USER ns_reader ON NAMESPACE PASSWORD 'reader-pass' ROLES VIEWER;
```

### Database Users

Database users can access tables and data within a single database.

```surrealql
USE NS production DB app_main;

DEFINE USER db_admin ON DATABASE PASSWORD 'db-password' ROLES OWNER;
DEFINE USER db_writer ON DATABASE PASSWORD 'writer-pass' ROLES EDITOR;
DEFINE USER db_reader ON DATABASE PASSWORD 'reader-pass' ROLES VIEWER;
```

### `DEFINE USER` Advanced Clauses (`PASSHASH`, `DURATION`)

`DEFINE USER` supports two clauses beyond `PASSWORD` / `ROLES` /
`COMMENT` that matter for production deployments. Both are
verified against the v3.0.5 parser at
`core/src/syn/parser/stmt/define.rs:310-413` (`parse_define_user`)
and the test fixtures at `core/src/syn/parser/test/stmt.rs:291`,
`:318`, `:344`, `:373`.

#### `PASSHASH '<phc-string>'` — Provide a Pre-Hashed Password

`PASSWORD '<plaintext>'` hashes the value with argon2 at define
time
(`core/src/sql/statements/define/user.rs:96` —
`Argon2::default().hash_password(p.as_bytes(), &SaltString::generate(&mut OsRng))`).
`PASSHASH '<phc-string>'` instead accepts an
[argon2 PHC string](https://en.wikipedia.org/wiki/PHC_string_format)
that you have hashed yourself (or migrated from another system),
and stores it as-is. The two clauses are mutually exclusive — the
parser bails with "Can't set both a passhash and a password" at
`define.rs:348-349` / `:355-356`.

> **PHC validation runs at signin time, not define time.** The
> parser stores whatever string you pass verbatim
> (`define.rs:353-358` assigns `PassType::Hash(self.parse_string_lit()?)`
> with no format check, and `core/src/expr/statements/define/user.rs:97-103`
> persists `hash: self.hash.clone()`). The first time the value
> is interpreted is during signin at
> `core/src/iam/verify.rs:947-948` — `PasswordHash::new(hash)`
> rejects malformed PHC strings inside `verify_pass`. So
> `DEFINE USER alice ON ROOT PASSHASH 'not-actually-a-phc-string'`
> succeeds at define time and fails on first signin attempt with
> "Invalid password hash". Treat `PASSHASH` as a "store as-is,
> validate-on-use" clause; do not rely on define-time syntax
> checking.

Use `PASSHASH` when:

- Migrating users from an external system that already stores
  argon2-hashed passwords (e.g. an existing identity provider's
  database dump). `PASSWORD` would re-hash an already-hashed
  string and lock those users out.
- Provisioning users from infrastructure-as-code where you do
  not want plaintext passwords ever to touch the SurrealQL
  source file (hash externally, commit the PHC string).

```surrealql
-- Migrate an existing argon2-hashed user. The hash must be a
-- valid argon2 PHC string at the time of the user's first
-- signin (starts with $argon2id$ / $argon2i$ / $argon2d$);
-- bare hex digests will store successfully but fail signin.
DEFINE USER alice ON ROOT
    PASSHASH '$argon2id$v=19$m=19456,t=2,p=1$<salt-b64>$<hash-b64>'
    ROLES EDITOR
    COMMENT 'imported from legacy IdP 2026-05-06';
```

`crypto::argon2::generate($plaintext)` produces a PHC string of
exactly the shape `PASSHASH` expects — useful for an
ad-hoc hash on the SurrealDB side before committing it to source
control:

```surrealql
-- One-off shell to obtain a PHC string for a known plaintext:
RETURN crypto::argon2::generate('the-temporary-password');
-- Then paste the result into the PASSHASH clause.
```

#### `DURATION FOR { TOKEN | SESSION } <expr>` — Per-User Token / Session Limits

System users (root, namespace, database) issue both a JWT access
token and a server-side session on signin. By default the token
lives for **1 hour** and the session has **no upper bound** until
the user signs out or the server restarts (default token = 3600s
at `define.rs:336`; default session = `Literal::None` at
`core/src/sql/statements/define/user.rs:43`). The `DURATION`
clause overrides those defaults per user. Both
`FOR TOKEN <dur>` and `FOR SESSION <dur>` are accepted, in either
order, comma-separated; either one alone is also valid. The
parser also accepts `NONE` as an expiry value (the parser parses
through `parse_expr_field()` which evaluates `NONE` to a sentinel
value the runtime treats as no-expiry). The v3.0.5 test suite
contains `DURATION FOR TOKEN NONE` anti-fixtures across **three
commented regions** at `core/src/syn/parser/test/stmt.rs:398-407`
(one DEFINE USER block), `:623-631` (one DEFINE ACCESS TYPE JWT
block), and `:1250-1276` (three DEFINE ACCESS TYPE RECORD blocks
at DB / ROOT / NS levels) — five anti-fixtures total, all gated
by `/* ... */` wrappers and calling `unwrap_err()` on the parse.
They exist to document why the syntax was suppressed during a
parameterization refactor (see the `// TODO: Parameterization
broke the guarantee that token duration is not none.` note at
stmt.rs:1252). So direct positive-fixture provenance for
`DURATION FOR TOKEN NONE` does not exist in v3.0.5; the syntax
flows through `parse_expr_field()` and the runtime treats
`Literal::None` as no-expiry, but consumers who need the
behaviour should validate against an actual signin/authenticate
round-trip rather than relying on parse-only confirmation.

Apply at signin time at
`core/src/iam/signin.rs:481` / `:502` (token + session expiry
respectively for system users) and `core/src/iam/verify.rs:106`
(session re-evaluation on subsequent verifications).

```surrealql
-- High-security operator: short tokens, bounded session
DEFINE USER pager ON ROOT
    PASSWORD 'rotated-weekly-via-ops-runbook'
    ROLES OWNER
    DURATION FOR TOKEN 5m, FOR SESSION 1h;

-- CI runner: longer token to ride out long-running migrations,
-- bounded session so a leaked CI host eventually loses access
DEFINE USER ci_runner ON DATABASE
    PASSWORD 'redacted'
    ROLES EDITOR
    DURATION FOR TOKEN 2h, FOR SESSION 8h;

-- Read-only analyst dashboard: opt out of token expiry entirely
-- (NOT recommended for write roles — kept here as an example of
-- the syntax)
DEFINE USER dashboard_viewer ON DATABASE
    PASSWORD 'redacted'
    ROLES VIEWER
    DURATION FOR TOKEN NONE, FOR SESSION 24h;
```

Combining clauses in a single statement:

```surrealql
-- A migrated, role-scoped, bounded-duration user
DEFINE USER service_account ON DATABASE
    PASSHASH '$argon2id$v=19$m=19456,t=2,p=1$<salt>$<hash>'
    ROLES EDITOR
    DURATION FOR TOKEN 15m, FOR SESSION 12h
    COMMENT 'migrated 2026-05-06; rotates with infra refresh cycle';
```

### Record Users

Record users are end-user accounts authenticated via `DEFINE ACCESS ... TYPE RECORD`. They are the most granular level and are subject to table-level PERMISSIONS clauses.

```surrealql
-- See DEFINE ACCESS section below for full details
DEFINE ACCESS account ON DATABASE TYPE RECORD
    SIGNUP (CREATE user SET email = $email, pass = crypto::argon2::generate($pass))
    SIGNIN (SELECT * FROM user WHERE email = $email AND crypto::argon2::compare(pass, $pass))
    DURATION FOR TOKEN 15m, FOR SESSION 12h;
```

---

## DEFINE ACCESS

The `DEFINE ACCESS` statement configures how users authenticate with SurrealDB. There are three access types: **RECORD** (signup/signin against records in the DB), **JWT** (validate externally-issued tokens), and **BEARER** (long-lived token grants for users or records).

### Record-Based Authentication (End Users)

Record access allows end users to sign up and sign in. The `SIGNUP` and `SIGNIN` clauses define SurrealQL expressions that execute during authentication.

```surrealql
-- Basic email/password authentication
DEFINE ACCESS account ON DATABASE TYPE RECORD
    SIGNUP (
        CREATE user SET
            email = $email,
            pass = crypto::argon2::generate($pass),
            created_at = time::now(),
            role = 'member'
    )
    SIGNIN (
        SELECT * FROM user
        WHERE email = $email
        AND crypto::argon2::compare(pass, $pass)
    )
    DURATION FOR TOKEN 15m, FOR SESSION 12h;
```

After successful authentication, `$auth` contains the authenticated user record and `$access` contains the access method name. These are available in PERMISSIONS clauses.

```surrealql
-- Advanced record access with validation
DEFINE ACCESS secure_account ON DATABASE TYPE RECORD
    SIGNUP (
        -- Validate email format
        IF string::is_email($email) THEN
            CREATE user SET
                email = string::lowercase($email),
                pass = crypto::argon2::generate($pass),
                name = $name,
                created_at = time::now(),
                verified = false,
                role = 'member'
        ELSE
            THROW "Invalid email format"
        END
    )
    SIGNIN (
        SELECT * FROM user
        WHERE email = string::lowercase($email)
        AND crypto::argon2::compare(pass, $pass)
    )
    DURATION FOR TOKEN 15m, FOR SESSION 12h;
```

```surrealql
-- Multi-tenant record access
DEFINE ACCESS tenant_account ON DATABASE TYPE RECORD
    SIGNUP (
        -- Verify tenant exists before creating user
        LET $tenant = SELECT * FROM tenant WHERE id = $tenant_id;
        IF count($tenant) > 0 THEN
            CREATE user SET
                email = $email,
                pass = crypto::argon2::generate($pass),
                tenant = $tenant_id,
                role = 'member'
        ELSE
            THROW "Invalid tenant"
        END
    )
    SIGNIN (
        SELECT * FROM user
        WHERE email = $email
        AND crypto::argon2::compare(pass, $pass)
    )
    DURATION FOR TOKEN 30m, FOR SESSION 24h;
```

#### Refresh Tokens (`WITH REFRESH`)

`TYPE RECORD` access can issue a **refresh token** alongside the
short-lived access token. The refresh token is itself a single-use
bearer grant: the client exchanges it for a fresh access token
(plus a fresh refresh token) without re-running `SIGNIN`. Verified
against the v3.0.5 parser at `core/src/syn/parser/stmt/define.rs`
lines 492-500 (the `WITH REFRESH` arm of the `TYPE RECORD` parser
loop, which constructs a `BearerAccess { kind: Refresh, subject:
Record, jwt: <inherited from WITH JWT> }`) and exercised by the
parser test fixtures at `core/src/syn/parser/test/stmt.rs:911`,
`:1108`, `:1163`. Runtime behaviour is split across two ranges:

- **Initial issuance** (`core/src/iam/signin.rs:279-295` for the
  refresh-var dispatch + `:352-364` for the
  `create_refresh_token_record(...)` call after a successful
  `SIGNIN`).
- **Rotation on subsequent renewals** (`core/src/iam/signin.rs:893-917`
  inside `signin_bearer`'s `BearerAccessType::Refresh` arm —
  `revoke_refresh_token_record(old_grant)` followed by
  `create_refresh_token_record(new_grant)`, returning a new
  bearer key).

Helpers used by both phases live at `core/src/iam/access.rs:107-170`
(`create_refresh_token_record` / `revoke_refresh_token_record`).

Key semantics:

- `WITH REFRESH` is only valid on `TYPE RECORD`. The parser
  rejects it on `TYPE JWT` and `TYPE BEARER`.
- The refresh token's lifetime comes from `DURATION FOR GRANT` on
  the same access definition. `FOR TOKEN` still controls the
  access-token lifetime; `FOR SESSION` still controls the session
  ceiling.
- Refresh tokens are **single-use**: each successful refresh
  invalidates the prior token and returns a new one (verified at
  `core/src/iam/signin.rs:893-917`). Reusing a consumed refresh
  token is rejected.
- The refresh value the client sees is the full bearer key with
  the prefix `surreal-refresh-<id>-<secret>`. Construction
  chain: `core/src/iam/access.rs:107-170`
  (`create_refresh_token_record`) calls into `create_grant` at
  `core/src/expr/statements/access.rs:181+`, which constructs
  the literal key in `new_grant_bearer` at `:121-126`
  (`format!("{prefix}-{id}-{secret}")`); the `Base::Db`
  enforcement guard for record-subject grants is at
  `:231-234` (`ensure!(matches!(base, Base::Db),
  Error::DbEmpty);` inside the `Subject::Record(_)` match arm,
  rejecting Base::Ns / Root even though parser-level `ACCESS …
  ON NAMESPACE GRANT FOR RECORD` is accepted). The bearer-
  presence check + `new_grant_bearer` invocation that follows
  the guard sits at `:237-242`. Signin validates four
  dash-separated parts (prefix-type / `refresh` / id / secret)
  inside `validate_grant_bearer` at
  `core/src/iam/signin.rs:1042-1056`. The integration test at
  `signin.rs:1582-1584` asserts the `surreal-refresh-…` regex
  on the returned plaintext — that reference is a test, not a
  production code path. Persist the entire string SurrealDB
  hands back verbatim — do not strip the `surreal-refresh-`
  prefix or split on `-` client-side.
- `WITH REFRESH` and `WITH JWT` can coexist in either order; the
  parser loop accepts repeated `WITH` clauses (test fixtures
  `:1108` shows `WITH REFRESH WITH JWT …`; `:1163` shows
  `WITH JWT … WITH REFRESH`).

```surrealql
-- Record access with refresh-token rotation. Access token is
-- short-lived (15m); refresh token lives 30 days and rotates on
-- every renewal.
DEFINE ACCESS account ON DATABASE TYPE RECORD
    SIGNUP (
        CREATE user SET
            email = $email,
            pass = crypto::argon2::generate($pass)
    )
    SIGNIN (
        SELECT * FROM user
        WHERE email = $email
        AND crypto::argon2::compare(pass, $pass)
    )
    WITH REFRESH
    DURATION
        FOR GRANT 30d,    -- refresh-token lifetime
        FOR TOKEN 15m,    -- access-token lifetime
        FOR SESSION 12h;
```

Client-side renewal (JavaScript SDK):

```javascript
// Initial sign-in returns BOTH an access token and a refresh token
// when the access method has WITH REFRESH.
const tokens = await db.signin({
    access: 'account',
    variables: { email, pass }
});
// tokens shape with WITH REFRESH:
//   { access: '<jwt>', refresh: 'surreal-refresh-<id>-<secret>' }
// The refresh value SurrealDB returns is the complete bearer key
// (literal 'surreal-refresh-' prefix + id + secret, four
// dash-separated parts total). Persist it verbatim; do NOT strip
// the prefix or split on '-' client-side.

// Later, when the access token is near expiry, exchange the refresh
// token for a fresh pair WITHOUT prompting for credentials again.
const renewed = await db.signin({
    access: 'account',
    variables: { refresh: tokens.refresh }
});
// renewed.refresh is a NEW token; the old one is now invalid.
// Persist `renewed.refresh` for the next renewal.
```

### JWT-Based Authentication

JWT access allows external identity providers to authenticate users with SurrealDB.

> **`TYPE JWT` is a verification-only access method.** The parser
> accepts `DURATION FOR TOKEN` and `DURATION FOR SESSION` (verified
> against test fixtures in `core/src/syn/parser/test/stmt.rs:558`
> for inline-key `TYPE JWT ALGORITHM HS256 KEY … DURATION FOR
> TOKEN 10s`, `:762` and `:823` for `TYPE JWT URL … WITH ISSUER …
> DURATION FOR TOKEN 10s [, FOR SESSION 2d]` patterns), but the
> issuance story is narrower than parser acceptance suggests:
>
> - **`signin` does NOT mint tokens for `AccessType::Jwt`.** The
>   `db_access` / `ns_access` / `root_access` signin paths only
>   match `Record` and `Bearer` access types; everything else falls
>   through to `Error::AccessMethodMismatch`
>   (`core/src/iam/signin.rs:449 / :550 / :686`, plus the
>   `signin_bearer` fallthrough at `:739` for bearer access methods
>   without a configured `at.jwt.issue` key). `WITH ISSUER ALGORITHM
>   <alg> KEY <key>` on a pure `TYPE JWT` is parser-accepted and
>   persisted but currently has no signin entry point that consumes
>   it for issuance — it only matters when the same access
>   definition is nested inside `TYPE RECORD WITH JWT` (where
>   `signin.rs:275-318` does mint a token using `at.jwt.issue.key` /
>   `expiration(av.token_duration)`).
> - **`FOR TOKEN` is unused on the `authenticate` path.** Incoming
>   third-party JWTs are validated against the access method's
>   verification key (or JWKS) and the JWT's own `exp` claim
>   controls token lifetime; `verify.rs` reads `de.session_duration`
>   for session expiry but does not consume `de.token_duration` for
>   `AccessType::Jwt` (grep of `token_duration` in `verify.rs`
>   surfaces only test fixtures).
> - **`FOR SESSION` IS applied** to JWT-authenticated sessions —
>   the DB-namespace branch sets `session.exp =
>   expiration(de.session_duration)` at `verify.rs:394`.
>
> If you need SurrealDB to *mint* tokens (not just validate
> external ones), use `TYPE RECORD WITH JWT … WITH ISSUER
> ALGORITHM <alg> KEY <key>` rather than `TYPE JWT … WITH ISSUER
> ALGORITHM <alg> KEY <key>` (the `ALGORITHM` token in `WITH
> ISSUER` is REQUIRED for JWKS / URL verifier paths only —
> inline asymmetric verifiers inherit the verifier algorithm
> from `define.rs:1697`, so bare `WITH ISSUER KEY '<priv>'`
> works there; see "Issuer key defaults" below for the full
> rubric). Pre-v1.6.2 revisions of this rule incorrectly
> described pure `TYPE JWT` as a first-class issuance path.

```surrealql
-- HMAC-based JWT (symmetric key)
DEFINE ACCESS jwt_auth ON DATABASE TYPE JWT
    ALGORITHM HS256
    KEY 'your-256-bit-secret-key-here'
    DURATION FOR SESSION 12h;

-- RSA-based JWT (asymmetric key, more secure)
DEFINE ACCESS jwt_rsa ON DATABASE TYPE JWT
    ALGORITHM RS256
    KEY '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
-----END PUBLIC KEY-----'
    DURATION FOR SESSION 12h;

-- ECDSA-based JWT
DEFINE ACCESS jwt_ecdsa ON DATABASE TYPE JWT
    ALGORITHM ES256
    KEY '-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcD...
-----END PUBLIC KEY-----'
    DURATION FOR SESSION 12h;

-- JWT with record binding (map JWT claims to a user record).
-- Inside a `TYPE RECORD WITH JWT` definition, the `WITH JWT KEY`
-- clause is the *verification* key (used to validate incoming
-- tokens the access method accepts). To also let SurrealDB *issue*
-- record-bound tokens, add a separate `WITH ISSUER` clause
-- holding the signing-side credential. SurrealDB then consumes
-- `at.jwt.issue.key` at `core/src/iam/signin.rs:275-318` when
-- minting a token after SIGNUP/SIGNIN.
--
-- ISSUER KEY DEFAULTS (verified at `core/src/syn/parser/stmt/define.rs:1696-1708`
-- + `:1726-1762`). The issuer's algorithm — `iss.alg` —
-- propagates as follows:
--   • Inline `ALGORITHM <alg> KEY <key>` verifier (HMAC, RSA,
--     ECDSA, EdDSA): line 1697 unconditionally sets `iss.alg =
--     <verifier-alg>` BEFORE the WITH ISSUER block runs. So a
--     bare `WITH ISSUER KEY '<priv>'` (no ALGORITHM) inherits
--     RS256 / HS256 / etc. from the verifier — works correctly
--     for asymmetric pairs as long as the verifier alg is set.
--   • SYMMETRIC inline verifiers (HS256/HS384/HS512) ALSO copy
--     the verifier key into `iss.key` automatically (line 1703;
--     full block at lines 1702-1708 sets `iss.key = key` then
--     `res.issue = Some(iss.clone())`) — `WITH ISSUER` is
--     optional for those; you can mint with just the inline
--     `ALGORITHM HS256 KEY '<secret>'`.
--   • `URL '<jwks>'` (JWKS) verifier: parser does NOT set
--     `iss.alg` (the URL arm at lines 1716-1722 has no
--     `iss.alg = ...` line). `iss.alg` stays at
--     `JwtAccessIssue::default()` — `Algorithm::Hs512` from
--     `core/src/sql/access_type.rs:181-191`. If you need to mint
--     RSA / ECDSA tokens alongside JWKS verification, you MUST
--     specify `WITH ISSUER ALGORITHM <alg> KEY '<priv>'` —
--     omitting ALGORITHM there will treat your private-key PEM
--     as an HMAC secret at `core/src/iam/issue.rs:10-28`.
--   • If no `WITH ISSUER` clause and no symmetric inline
--     auto-population, `at.jwt.issue` is `None`; signin's
--     "check if record access supports issuing tokens" guard at
--     `signin.rs:275-278` bails with `AccessMethodMismatch`.
--
-- A pure `TYPE JWT … WITH ISSUER ALGORITHM … KEY …` (no
-- enclosing `TYPE RECORD`) is parser-accepted but currently has
-- NO runtime signin path that consumes it — see the
-- "verification-only" callout above.
--
-- The two flows below are SEPARATE PATTERNS — each access
-- definition supports one entry path, not both. The earlier
-- v1.5.x / v1.6.2-pre-rev-5 single-definition "hybrid" pattern
-- (a TYPE RECORD with WITH ISSUER + AUTHENTICATE that tries to
-- handle BOTH credential SIGNIN and inbound JWT) is broken
-- because:
--   • Credential SIGNIN mints a token whose claims object
--     contains `$token.ID` (uppercase) — the record id from
--     `Claims { id: Some(rid.to_sql()), .. }` at
--     `core/src/iam/signin.rs:314-324`, serialised by
--     `into_claims_object` at `core/src/iam/token.rs:289-345`.
--     The minted token has NO `sub` claim (Claims::default sets
--     sub: None at `token.rs:243`).
--   • Inbound third-party JWTs typically carry `$token.sub` (the
--     IdP-assigned subject) but no `$token.ID`.
-- A single AUTHENTICATE clause would have to branch on which
-- claim is present; cleaner to define two access methods.
--
-- For runtime semantics: when `AUTHENTICATE` is omitted, record
-- access against an inbound JWT requires the token to carry
-- SurrealDB's own `id` claim — `verify.rs:177-245` reads `id`
-- from claims to bind the record directly; if `id` is absent
-- AND there's no AUTHENTICATE, `verify.rs:464` bails
-- `AccessMethodMismatch`. (Inbound IdP JWTs almost never carry
-- a SurrealDB record id, so AUTHENTICATE is effectively
-- required for IdP integration.)
--
-- ROUTING-CLAIM REQUIREMENT (verified at
-- `core/src/iam/verify.rs:292-297` + `core/src/iam/token.rs:248-275`).
-- Inbound JWTs MUST carry `ns`, `db`, and `ac` claims for
-- SurrealDB to route them to an access method. The `token`
-- entry point `fn token` at `verify.rs:155` calls
-- `decode_claims_unverified(token)?` at `:159` (with a
-- describing comment at `:158`) to decode
-- the JWT WITHOUT verifying it first (the actual signature
-- verification runs later, inside the access-method-specific
-- branch); the resulting `token_data.claims` is then matched
-- against the database-access arm at `:292-297`
-- (the prior arm's closing brace + `Ok(())` sit on `:288-291`):
--     Claims { ns: Some(ns), db: Some(db), ac: Some(ac), .. }
-- Tokens missing any of those three fall through to
-- `_ => Err(InvalidAuth)` at `verify.rs:825` (the entire
-- arm — pattern + body — sits on :825; :826 is the closing
-- brace of the surrounding match). The
-- serde
-- aliases at `token.rs:248-275` accept any of these spellings:
-- `ns` / `NS` / `https://surrealdb.com/ns` /
-- `https://surrealdb.com/namespace`; same shape for `db` /
-- `DB` / `…/database` and `ac` / `AC` / `…/access`. Configure
-- your IdP to mint custom claims for these three fields (most
-- enterprise IdPs — Auth0 Actions, Okta inline hooks, AWS
-- Cognito pre-token-generation Lambda, Azure AD claim mapping
-- — support this). Without them, validation fails before the
-- access method even runs.

-- Pattern A — Inbound third-party JWT verification.
-- For when an external IdP (Auth0 / Okta / Cognito) issues
-- JWTs that carry `sub` and you want SurrealDB to map them to
-- a user record. NO SIGNIN clause: clients call
-- `db.authenticate(externalJwt)` directly. WITH ISSUER KEY is
-- omitted because there is no SurrealDB-side minting in this
-- pattern.
DEFINE ACCESS external_jwt_auth ON DATABASE TYPE RECORD
    -- Clause order matters: parser at
    -- `core/src/syn/parser/stmt/define.rs:456-507` consumes
    -- TYPE RECORD's SIGNUP/SIGNIN inner loop and WITH JWT/REFRESH
    -- inner loop before returning to the outer parse_define_access
    -- loop where AUTHENTICATE / DURATION are matched (line 545+).
    -- Putting AUTHENTICATE before WITH would leave WITH unconsumed
    -- by the outer loop and fail the parse. Canonical fixture
    -- order at `core/src/iam/verify.rs:2029-2037`.
    WITH JWT
        ALGORITHM RS256 KEY '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
-----END PUBLIC KEY-----'
    AUTHENTICATE (
        -- $token.sub is the IdP's subject claim; map it to the
        -- local user record. `sess.tk` (the source of $token) is
        -- populated by the authenticate path BEFORE this
        -- AUTHENTICATE clause runs:
        --   • Typical IdP-`sub` JWTs (no SurrealDB `id` claim)
        --     hit the claims-without-id arm at
        --     `core/src/iam/verify.rs:432-440` — this is the
        --     usual path for Pattern A.
        --   • If the inbound JWT happens to also carry a
        --     SurrealDB `id` claim, the with-id arm at
        --     `verify.rs:256-263` populates `sess.tk` instead
        --     and SurrealDB binds the record directly.
        -- Neither path involves SIGNIN-mint at signin.rs:340-345
        -- — this access method has no SIGNIN clause.
        SELECT id FROM user WHERE external_id = $token.sub
    )
    DURATION FOR SESSION 12h;
-- Note: `DURATION FOR TOKEN` is NOT applied on the
-- AccessType::Record authenticate path — the IdP's own `exp`
-- claim governs token lifetime. `DURATION FOR SESSION` IS applied
-- (`verify.rs:457` for the no-id claims arm where AUTHENTICATE
-- runs; `:282` for the with-id claims arm) to bound the
-- SurrealDB session.

-- Pattern B — Credential SIGNIN with SurrealDB-minted JWT.
-- For a classic email/password flow where SurrealDB issues a
-- JWT after credentials validate. Inline ALGORITHM RS256 KEY on
-- the verifier means iss.alg = RS256 (from define.rs:1697),
-- which the bare `WITH ISSUER KEY '<priv>'` then inherits
-- correctly; the issued token is round-trippable because
-- `verify.rs:177-245` reads SurrealDB's `id` claim and binds
-- the record directly (no `kid` lookup required for inline-KEY
-- verifiers).
DEFINE ACCESS credential_auth ON DATABASE TYPE RECORD
    SIGNIN (
        SELECT * FROM user
        WHERE email = $email
        AND crypto::argon2::compare(pass, $pass)
    )
    WITH JWT
        ALGORITHM RS256 KEY '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
-----END PUBLIC KEY-----'
    -- The verifier sets iss.alg = RS256 at parse time
    -- (define.rs:1697), so bare `WITH ISSUER KEY '<priv>'`
    -- correctly inherits RS256 here.
    WITH ISSUER KEY '-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQ...
-----END PRIVATE KEY-----'
    DURATION FOR TOKEN 1h, FOR SESSION 12h;
-- Without an AUTHENTICATE clause, the issued token's `id`
-- claim (set to `rid.to_sql()` at signin.rs:323) is what
-- subsequent `db.authenticate(token)` calls use to re-bind
-- the record (verify.rs:177-245). $auth.id stays populated
-- across calls — no token-only-permissions trap.
```

### Supported JWT Algorithms

| Algorithm | Type | Key |
|---|---|---|
| HS256, HS384, HS512 | HMAC (symmetric) | Shared secret key |
| RS256, RS384, RS512 | RSA (asymmetric) | Public key for verification |
| ES256, ES384 | ECDSA (asymmetric) | Public key for verification |
| ES512 | ECDSA (asymmetric) | **Maps to ES384 at runtime** — see caveat below |
| PS256, PS384, PS512 | RSA-PSS (asymmetric) | Public key for verification |
| EdDSA | EdDSA (asymmetric) | Public key for verification |

> **ES512 caveat.** The parser accepts `ALGORITHM ES512` but
> v3.0.5 maps `catalog::Algorithm::Es512` to
> `jsonwebtoken::Algorithm::ES384` in both the
> `Validation::new` constructed during inbound-token verification
> (`core/src/iam/verify.rs:47-48`) and the
> algorithm-to-jwt-algorithm helper used during issuance
> (`core/src/iam/mod.rs:46-47`). Practical effect: an access
> method configured with `ALGORITHM ES512` actually verifies
> incoming tokens against ES384 and emits ES384-signed tokens.
> Whether `jsonwebtoken::decode` accepts an inbound `alg: ES512`
> header at all depends on the upstream `jsonwebtoken` crate
> behaviour and is outside what this v3.0.5 source check can
> verify (`core/src/iam/verify.rs:956-957` calls into the crate
> with the rebuilt ES384 validation). Use `ES384` directly
> (or one of the other ECDSA / EdDSA algorithms) if you want
> truthful algorithm advertising and avoid the silent rewrite.

### JWKS-Backed JWT (`URL` clause)

Instead of pinning a single inline `KEY`, JWT access can resolve
verification keys at request time from a remote
[JSON Web Key Set](https://datatracker.ietf.org/doc/html/rfc7517#section-5)
endpoint. This is the standard pattern for integrating with
external identity providers (Auth0, Okta, AWS Cognito, Google,
Azure AD) that publish a JWKS document and rotate signing keys on
their own schedule. The parser accepts `URL '<jwks-uri>'` as an
alternative to `ALGORITHM <alg> KEY '<key>'` on both `TYPE JWT`
and the nested `WITH JWT` clause inside `TYPE RECORD` (the same
`parse_jwt()` function is invoked from both call sites at
`core/src/syn/parser/stmt/define.rs:454` and `:484`).

> **JWKS verification requires the `jwks` Cargo feature at
> build time.** The parser accepts `URL '<jwks-uri>'`
> unconditionally, but every runtime arm that handles
> `JwtAccessVerify::Jwks` is gated `#[cfg(feature = "jwks")]`
> in `core/src/iam/verify.rs` (lines 228-240, 340-352, 412-424,
> 573-585, 725-737). Without the feature, the JWKS arm is
> replaced by a `_ => bail!(Error::AccessMethodMismatch)`
> branch and the verification path no longer authenticates
> incoming JWTs.
>
> The `jwks` feature is **NOT** in the default
> `surrealdb-server` feature set (`server/Cargo.toml:19-30` —
> default = `[allocator, allocation-tracking, storage-mem,
> storage-surrealkv, storage-rocksdb, scripting, http,
> surrealism, graphql, cli]`); it is declared at
> `server/Cargo.toml:32` as `jwks = ["surrealdb-core/jwks"]`,
> which transitively gates `core/src/iam/jwks.rs` itself
> (`core/Cargo.toml:45` makes the `jwks` core feature pull in
> `dep:reqwest`).
>
> If you build SurrealDB from source, pass `--features jwks` to
> `cargo build`. If you consume an official binary, verify
> against the release notes that JWKS is enabled before relying
> on `URL '<jwks-uri>'` for production verification.
>
> **The gate scopes to incoming-JWT verification, not all
> signin paths.** For a `TYPE RECORD WITH JWT URL '<jwks>'
> WITH ISSUER ALGORITHM <alg> KEY '<priv>'` definition that has
> a `SIGNIN`/`SIGNUP` clause, credential-based signin still
> works (it goes through `db_access` at
> `core/src/iam/signin.rs:245-410`, which never invokes the
> JWKS verifier arms). Only **incoming third-party JWTs** —
> tokens presented to the `authenticate` path that route
> through `verify.rs` — fail when the feature is off.
>
> **JWKS round-trip limitation.** Tokens that SurrealDB *mints*
> from this hybrid (after a successful signin) cannot
> subsequently re-authenticate through the same access
> method's JWKS verifier. SurrealDB encodes minted JWTs with
> bare `Header::new(...)` at
> `core/src/iam/signin.rs:369 / :938` and
> `core/src/iam/signup.rs:268`, which omits the `kid` claim;
> the JWKS verifier requires `token_data.header.kid` to look
> up the verification key (`verify.rs:230-237` etc., bailing
> with "Missing token header 'kid'" otherwise). The hybrid
> pattern is therefore appropriate for **one-way** validation
> of third-party-issued JWTs (which carry their own `kid`),
> not for round-tripping SurrealDB-issued tokens. If you need
> SurrealDB-issued tokens to be re-validatable, use
> `TYPE RECORD WITH JWT ALGORITHM <alg> KEY '<pub>' WITH ISSUER
> ALGORITHM <alg> KEY '<priv>'` (inline KEY on the verifier
> side, NOT URL) so verification is keyed by the static public
> key rather than a JWKS lookup.

Verified against:

- Parser branch: `core/src/syn/parser/stmt/define.rs:1716-1722`
  inside `parse_jwt()` — `URL` is one of the two valid first
  tokens after the JWT type marker (alternative is `ALGORITHM`).
- Verifier path: `core/src/iam/jwks.rs` (HTTP fetch, in-memory
  cache keyed by URL, JWK lookup by `kid` header). Compiled out
  unless `--features jwks` is enabled per the callout above.
- Test fixtures: `core/src/syn/parser/test/stmt.rs:703`, `:731`,
  `:762`, `:792`, `:823` exercising `TYPE JWT URL '…/jwks.json'`
  with and without `WITH ISSUER`, `DURATION FOR TOKEN`, and
  `DURATION FOR SESSION` clauses. **No dedicated parser fixture
  covers `TYPE RECORD WITH JWT URL` directly**, but the runtime
  verifier exercises the shape via the
  `#[cfg(feature = "jwks")]` test at
  `core/src/iam/verify.rs:1495-1497` (definition at `:1560-1564`,
  end-to-end JWT validation at `:1607-1623`). Combined with the
  shared `parse_jwt()` call from both `t!("JWT")` (line 454,
  standalone) and the `WITH JWT` arm of TYPE RECORD (line 484),
  the nested form is fully supported.

Operational notes:

- The JWKS document is fetched lazily on the first verification
  request and cached. Cache TTL is governed by environment
  variables read at `core/src/iam/jwks.rs:31-66`:
  `SURREAL_JWKS_CACHE_EXPIRATION_SECONDS` (default 12h),
  `SURREAL_JWKS_CACHE_COOLDOWN_SECONDS` (default 5m, throttles
  re-fetch after any cache miss including expired-cache + `kid`
  miss), and `SURREAL_JWKS_REMOTE_TIMEOUT_MILLISECONDS` (default
  1000ms).
- Network access to the JWKS URL must be permitted by the
  capabilities allowlist at server start (e.g. `--allow-net
  '<jwks-host>'` or a broader policy). Otherwise verification
  fails with "Network access to JWKS location is not allowed"
  (`core/src/iam/jwks.rs:238`). Only the original URL host is
  capability-checked; redirect targets are handled by the
  underlying `reqwest` client without an additional
  capabilities check (do not assume capability enforcement
  applies to redirect chains — keep your IdP under a stable
  hostname, or run JWKS through a proxy you control).
- `WITH ISSUER` on a pure `TYPE JWT` is **not** a runtime
  issuance hybrid — see the verification-only callout at the
  top of "JWT-Based Authentication" above. For setups that
  need both JWKS-backed validation of third-party tokens AND
  SurrealDB-minted credential signin tokens, define **two
  separate access methods** — one with `WITH JWT URL '<jwks>'`
  + `AUTHENTICATE` for inbound IdP tokens (`jwks_inbound`
  pattern below) and one with `WITH JWT ALGORITHM <alg> KEY
  '<pub>'` (inline KEY, NOT URL) + `SIGNIN` + `WITH ISSUER`
  for credential minting (`credential_mint` pattern below).
  Do NOT compose them into a single `TYPE RECORD WITH JWT URL
  … WITH ISSUER …` definition: the anti-pattern callout under
  the example block documents two source-verified failure
  modes (kid round-trip + sub-vs-ID predicate split). If a
  consumer insists on the combined shape and only uses it for
  one entry path at a time, the `ALGORITHM` token in `WITH
  ISSUER` is REQUIRED because the URL/JWKS verifier branch at
  `core/src/syn/parser/stmt/define.rs:1716-1722` does NOT set
  `iss.alg` (the inline-key branch at `:1697` does); without
  explicit `ALGORITHM <alg>` the issuer side falls back to
  `JwtAccessIssue::default()` (Hs512 from
  `sql/access_type.rs:181-191`) and treats an asymmetric
  private key as an HMAC secret at `iam/issue.rs:10-28`.

```surrealql
-- Validate JWTs issued by an external IdP (e.g. Auth0). No
-- inline KEY: SurrealDB fetches the JWK Set at request time and
-- caches it for SURREAL_JWKS_CACHE_EXPIRATION_SECONDS. Inbound
-- JWTs MUST carry NS/DB/AC routing claims (or aliases per
-- token.rs:248-275) — see the ROUTING-CLAIM REQUIREMENT block
-- in JWT-Based Authentication above; this applies to TYPE JWT
-- the same way it applies to TYPE RECORD WITH JWT.
DEFINE ACCESS auth0_jwt ON DATABASE TYPE JWT
    URL 'https://your-tenant.auth0.com/.well-known/jwks.json'
    DURATION FOR SESSION 12h;

-- The TYPE RECORD WITH JWT URL shape — third-party JWTs sign
-- in record users via AUTHENTICATE — is shown below as
-- Pattern A (`jwks_inbound`). AUTHENTICATE is required because
-- inbound IdP JWTs typically don't carry the SurrealDB `id`
-- claim (verify.rs:401-462 + :464). The two patterns
-- (`jwks_inbound` + `credential_mint`) below cover the full
-- combinatorial space of JWKS-backed verification + optional
-- SurrealDB-side minting.

-- TYPE JWT + WITH ISSUER is parser-accepted but currently has no
-- signin entry point that mints tokens — see the "TYPE JWT is a
-- verification-only access method" callout above. The two
-- patterns below show how to combine JWKS-backed inbound JWT
-- verification with SurrealDB-side flows; they are SEPARATE
-- access definitions because the claim shape after credential
-- SIGNIN ($token.ID) differs from the inbound IdP JWT shape
-- ($token.sub) — see the "JWT with record binding" comment in
-- the JWT-Based Authentication section above for the
-- claim-shape walkthrough.

-- Pattern A — JWKS-verify inbound third-party JWTs only.
-- Clients call db.authenticate(externalJwt). NO SIGNIN, NO
-- WITH ISSUER. AUTHENTICATE maps the IdP's $token.sub to a
-- local record. This is the natural shape for federated IdP
-- integration (Auth0 / Okta / Cognito) where SurrealDB
-- never mints tokens itself.
DEFINE ACCESS jwks_inbound ON DATABASE TYPE RECORD
    -- Same clause-order constraint as external_jwt_auth above.
    -- NS/DB/AC routing claims must be present on the inbound
    -- JWT — see the ROUTING-CLAIM REQUIREMENT block in
    -- JWT-Based Authentication above.
    WITH JWT
        URL 'https://your-tenant.auth0.com/.well-known/jwks.json'
    AUTHENTICATE (
        SELECT id FROM user WHERE external_id = $token.sub
    )
    DURATION FOR SESSION 12h;
-- DURATION FOR TOKEN is omitted: on the AccessType::Record
-- authenticate path without SurrealDB-side minting, the IdP's
-- own `exp` claim governs token lifetime. `DURATION FOR
-- SESSION` IS applied at `verify.rs:457` (no-id claims arm,
-- where AUTHENTICATE runs — the typical IdP-`sub` path) or
-- `:282` (with-id claims arm, when the inbound JWT happens
-- to carry SurrealDB's own `id` claim). `de.token_duration`
-- is not consumed in either arm.

-- Pattern B — SurrealDB-side credential mint, round-trippable.
-- Use INLINE KEY (not URL) on the verifier so SurrealDB-minted
-- tokens can be re-validated by the same access method. The
-- minted token (from SIGNIN at signin.rs:275-318) ships without
-- a `kid` header (Header::new at signin.rs:369), which would
-- fail JWKS verification at verify.rs:230-237 ("Missing token
-- header 'kid'") — the inline-KEY path doesn't lookup by `kid`,
-- so round-trip works.
DEFINE ACCESS credential_mint ON DATABASE TYPE RECORD
    SIGNIN (
        SELECT * FROM user
        WHERE email = $email
        AND crypto::argon2::compare(pass, $pass)
    )
    WITH JWT
        ALGORITHM RS256 KEY '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
-----END PUBLIC KEY-----'
    WITH ISSUER KEY '-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQ...
-----END PRIVATE KEY-----'
    DURATION FOR TOKEN 1h, FOR SESSION 12h;
-- Bare `WITH ISSUER KEY '<priv>'` is correct here because the
-- verifier ALGORITHM RS256 sets iss.alg = RS256 at define.rs:1697
-- before the WITH ISSUER block runs. Subsequent
-- db.authenticate(token) calls re-bind the record via the `id`
-- claim at verify.rs:177-245.

-- ANTI-PATTERN: TYPE RECORD WITH JWT URL '<jwks>' WITH ISSUER
-- ALGORITHM <alg> KEY '<priv>' (single definition combining
-- JWKS-verify inbound + credential-mint round-trip) is what
-- v1.6.2-pre-rev-5 documented as `hybrid_record`. Source
-- verification surfaced two reasons that pattern is broken:
-- (1) credential SIGNIN mints tokens without a kid header, so
-- the round-trip path through the JWKS verifier fails
-- ("Missing token header 'kid'" at verify.rs:230-237);
-- (2) the AUTHENTICATE clause cannot share predicates between
-- the two entry paths because $token.sub (inbound IdP) and
-- $token.ID (SurrealDB mint, see token.rs:289-345) are
-- different keys. Use Pattern A OR Pattern B; do not try to
-- compose them into a single access definition.
```

When deploying with capabilities locked down, allow the JWKS
host explicitly. Pin the IdP under one stable hostname rather
than relying on capability enforcement of redirect chains
(`core/src/iam/jwks.rs:268-313` only checks the original URL
host before issuing the `reqwest` request):

```bash
surreal start \
    --allow-net 'your-tenant.auth0.com' \
    rocksdb:///var/data/surreal.db
```

Build with the `jwks` feature for `URL` to actually authenticate
incoming tokens:

```bash
# If building from source
cargo build --release --features 'jwks,storage-rocksdb,storage-mem'
```

### Bearer-Token Authentication

SurrealDB v3 has no `TYPE API KEY` access -- pre-v1.5.1 revisions of
this rule documented that as a third access type, but it is not in
the v3 grammar. The intended functionality (long-lived token grants
for service accounts or background workers) is provided by `TYPE
BEARER`.

```surrealql
-- Bearer access for an existing user (typical "service account
-- with a long-lived token" pattern). The token is issued via
-- `ACCESS <name> GRANT FOR USER <username>` after the access is
-- defined.
DEFINE ACCESS service_tokens ON DATABASE TYPE BEARER FOR USER
    DURATION FOR GRANT 30d, FOR TOKEN 1h, FOR SESSION 12h;

-- Bearer access tied to a record (e.g. one record per integration
-- partner, with the bearer token bound to that record).
DEFINE ACCESS partner_tokens ON DATABASE TYPE BEARER FOR RECORD
    AUTHENTICATE {
        IF $auth.id THEN RETURN $auth ELSE THROW "no auth record" END
    }
    DURATION FOR GRANT 90d, FOR TOKEN 1h, FOR SESSION 24h;

-- Issue a token under the access method:
ACCESS service_tokens GRANT FOR USER ci_runner;
```

`TYPE BEARER` accepts `DURATION FOR GRANT`, `DURATION FOR TOKEN`,
and `DURATION FOR SESSION`. `FOR GRANT` controls how long the issued
bearer token remains usable; `FOR TOKEN` and `FOR SESSION` follow
the same shape as `TYPE RECORD`.

### Bearer-Grant Lifecycle (`ACCESS GRANT / SHOW / REVOKE / PURGE`)

`DEFINE ACCESS … TYPE BEARER` defines the access *method*; the
actual long-lived tokens are minted by a separate top-level
`ACCESS` statement. SurrealDB v3 ships four `ACCESS` subcommands
for managing the lifecycle of bearer grants. Verified against
the v3.0.5 parser at `core/src/syn/parser/stmt/mod.rs:108-271`
(`parse_access` dispatches on `GRANT | SHOW | REVOKE | PURGE`)
and the test fixtures at `core/src/syn/parser/test/stmt.rs:2604`
(GRANT FOR USER), `:2621` (GRANT FOR RECORD), `:2645-2683`
(SHOW), `:2703-2741` (REVOKE), `:2761-2853` (PURGE).

#### `ACCESS … GRANT FOR { USER | RECORD }`

Issues a new bearer grant under a `TYPE BEARER` access method.
The grant token is returned to the caller exactly once; SurrealDB
stores only the hash, so a lost token cannot be recovered and
must be re-issued.

```surrealql
-- 1. Define the access method
DEFINE ACCESS service_tokens ON DATABASE TYPE BEARER FOR USER
    DURATION FOR GRANT 30d, FOR TOKEN 1h, FOR SESSION 12h;

-- 2. Issue a grant for an existing user
ACCESS service_tokens ON DATABASE GRANT FOR USER ci_runner;
-- Returns the bearer token (only shown once); persist it in the
-- consumer's secret store.

-- Record-bound grants for FOR RECORD bearer access
DEFINE ACCESS partner_tokens ON DATABASE TYPE BEARER FOR RECORD
    DURATION FOR GRANT 90d, FOR TOKEN 1h, FOR SESSION 24h;

ACCESS partner_tokens ON DATABASE GRANT FOR RECORD partner:acme;
```

#### `ACCESS … SHOW { ALL | GRANT <id> | WHERE <cond> }`

Lists existing grants without revealing token material (the
stored hash is opaque). Useful for auditing what tokens exist
and which subjects they bind to.

```surrealql
-- All grants under an access method
ACCESS service_tokens ON DATABASE SHOW ALL;

-- A specific grant by id
ACCESS service_tokens ON DATABASE SHOW GRANT abc123;

-- Filter with a WHERE condition (predicate runs against grant
-- metadata; expired and revoked grants are included unless you
-- filter them out yourself)
ACCESS service_tokens ON DATABASE SHOW WHERE expiration < time::now();
```

#### `ACCESS … REVOKE { ALL | GRANT <id> | WHERE <cond> }`

Marks a grant as revoked. Revoked grants stop authenticating
immediately but are NOT deleted; they remain visible to `SHOW`
until purged. Use this to invalidate a leaked token, kick a
former employee's CI runner, or force-rotate a partner's
credentials.

```surrealql
-- Revoke every grant under this access method (kill switch)
ACCESS service_tokens ON DATABASE REVOKE ALL;

-- Revoke one grant by id
ACCESS service_tokens ON DATABASE REVOKE GRANT abc123;

-- Conditional revoke
ACCESS service_tokens ON DATABASE REVOKE
    WHERE subject.user = 'former_employee';
```

#### `ACCESS … PURGE { EXPIRED | REVOKED | EXPIRED, REVOKED } [ FOR <duration> ]`

Physically deletes grants from the catalog. Always required as a
follow-up to `REVOKE` — without `PURGE`, revoked grants
accumulate in the catalog forever. Both keywords can be combined
and the `FOR <duration>` grace period requires the grant to be
**older than** the duration (strict greater-than: runtime test
is `elapsed_seconds > stmt.grace.secs()` at
`core/src/expr/statements/access.rs:878-887`); use it to keep a
forensic window before permanently erasing audit evidence.

```surrealql
-- Delete all grants whose expiration has already passed
ACCESS service_tokens ON DATABASE PURGE EXPIRED;

-- Delete revoked grants but keep them around for 90 days first
ACCESS service_tokens ON DATABASE PURGE REVOKED FOR 90d;

-- Sweep both classes in one statement
ACCESS service_tokens ON DATABASE PURGE EXPIRED, REVOKED FOR 30d;
```

The parser order between `EXPIRED` and `REVOKED` is irrelevant
(verified at `core/src/syn/parser/stmt/mod.rs:228-256`). Pass the
`FOR <duration>` clause to require grants be older than that
duration before they purge; omit it for an immediate sweep.

#### Operational Pattern: Rotation Workflow

Combine the four subcommands for a credential-rotation playbook:

```surrealql
-- 1. Issue a fresh grant for the new key
ACCESS service_tokens ON DATABASE GRANT FOR USER ci_runner;
-- (deliver the returned token to the consumer)

-- 2. Once the consumer is on the new token, revoke the old one
ACCESS service_tokens ON DATABASE REVOKE GRANT <old-grant-id>;

-- 3. Periodically purge revoked + expired grants, keeping a
-- 30-day window for incident response
ACCESS service_tokens ON DATABASE PURGE EXPIRED, REVOKED FOR 30d;
```

**Base scoping (`ON DATABASE` / `ON NAMESPACE` / `ON ROOT`):**

- `ON …` is **optional** on every `ACCESS` subcommand
  (`core/src/syn/parser/stmt/mod.rs:131`:
  `self.eat(t!("ON")).then(|| self.parse_base())`); when omitted,
  execution resolves the base from the current session context
  via `opt.selected_base()`
  (`core/src/expr/statements/access.rs:836-848`). The examples
  above use explicit `ON DATABASE` for clarity, but `ACCESS
  service_tokens SHOW ALL` is equivalent inside a `USE NS … DB
  …` context.
- `SHOW`, `REVOKE`, and `PURGE` accept whichever base the access
  method was defined on. `DEFINE ACCESS … TYPE BEARER FOR USER`
  and `TYPE JWT` are valid on `ROOT`, `NAMESPACE`, and
  `DATABASE`, so their lifecycle subcommands work at the same
  bases.
- `GRANT FOR RECORD` is **database-only** at runtime
  (`core/src/expr/statements/access.rs:231-234` for the
  AccessType::Record arm + `:353-355` for the
  AccessType::Bearer arm — both call `ensure!(matches!(base,
  Base::Db), Error::DbEmpty);` for record subjects). The corresponding
  `DEFINE ACCESS … TYPE BEARER FOR RECORD` and `TYPE RECORD`
  are also DB-only at parse time
  (`core/src/syn/parser/stmt/define.rs:457-461, :521-526`). The
  parser will accept `ACCESS … ON NAMESPACE GRANT FOR RECORD …`
  syntactically (test SQL string at
  `core/src/syn/parser/test/stmt.rs:2621`; the harness wrapper
  begins on the previous line at `:2620`), but execution will
  fail at runtime because no record-typed access method can
  exist on a namespace.
- Match the `ON …` clause to the base the corresponding `DEFINE
  ACCESS` was created on.

### Token Duration Configuration

```surrealql
-- Duration controls how long tokens and sessions last
DEFINE ACCESS account ON DATABASE TYPE RECORD
    SIGNUP (...)
    SIGNIN (...)
    -- Token: short-lived, used for individual requests
    -- Session: longer-lived, maintains authenticated state
    DURATION FOR TOKEN 15m, FOR SESSION 12h;

-- Very short tokens for high-security environments
DEFINE ACCESS high_sec ON DATABASE TYPE RECORD
    SIGNUP (...)
    SIGNIN (...)
    DURATION FOR TOKEN 5m, FOR SESSION 1h;

-- Longer durations for less sensitive applications
DEFINE ACCESS relaxed ON DATABASE TYPE RECORD
    SIGNUP (...)
    SIGNIN (...)
    DURATION FOR TOKEN 1h, FOR SESSION 7d;
```

---

## Row-Level Security (Table Permissions)

Permissions are defined on tables and control what record users can do. They are enforced automatically by the database engine -- there is no way for a record user to bypass them.

### Basic Permissions

```surrealql
DEFINE TABLE post SCHEMALESS
    PERMISSIONS
        FOR select WHERE published = true OR user = $auth.id
        FOR create WHERE $auth.id IS NOT NONE
        FOR update WHERE user = $auth.id
        FOR delete WHERE user = $auth.id OR $auth.role = 'admin';
```

### Granular Permission Examples

```surrealql
-- Public read, authenticated write
DEFINE TABLE article SCHEMALESS
    PERMISSIONS
        FOR select FULL       -- anyone can read (including unauthenticated)
        FOR create, update, delete WHERE $auth.id IS NOT NONE;

-- Owner-only access
DEFINE TABLE private_note SCHEMALESS
    PERMISSIONS
        FOR select, update, delete WHERE owner = $auth.id
        FOR create WHERE $auth.id IS NOT NONE;

-- No access for record users (admin-only table)
DEFINE TABLE system_config SCHEMALESS
    PERMISSIONS
        FOR select, create, update, delete NONE;

-- Role-based permissions
DEFINE TABLE order SCHEMAFULL
    PERMISSIONS
        FOR select WHERE
            customer = $auth.id
            OR $auth.role IN ['admin', 'support']
        FOR create WHERE $auth.id IS NOT NONE
        FOR update WHERE
            customer = $auth.id AND status = 'draft'
            OR $auth.role = 'admin'
        FOR delete WHERE $auth.role = 'admin';
```

### Multi-Tenant Permissions

```surrealql
-- Tenant isolation: users can only see data in their tenant
DEFINE TABLE customer SCHEMAFULL
    PERMISSIONS
        FOR select WHERE tenant = $auth.tenant
        FOR create WHERE tenant = $auth.tenant
        FOR update WHERE tenant = $auth.tenant AND $auth.role IN ['admin', 'editor']
        FOR delete WHERE tenant = $auth.tenant AND $auth.role = 'admin';

DEFINE TABLE invoice SCHEMAFULL
    PERMISSIONS
        FOR select WHERE
            tenant = $auth.tenant
            AND (
                created_by = $auth.id
                OR $auth.role IN ['admin', 'finance']
            )
        FOR create WHERE tenant = $auth.tenant
        FOR update WHERE
            tenant = $auth.tenant
            AND (created_by = $auth.id OR $auth.role = 'admin')
            AND status != 'finalized'
        FOR delete NONE;  -- invoices cannot be deleted
```

### Complex Permission Conditions

```surrealql
-- Time-based permissions
DEFINE TABLE submission SCHEMAFULL
    PERMISSIONS
        FOR select FULL
        FOR create WHERE
            $auth.id IS NOT NONE
            AND time::now() < d'2026-03-01T00:00:00Z'  -- submission deadline
        FOR update WHERE
            author = $auth.id
            AND status = 'draft'
            AND time::now() < d'2026-03-01T00:00:00Z'
        FOR delete WHERE author = $auth.id AND status = 'draft';

-- Permissions based on related records
DEFINE TABLE comment SCHEMAFULL
    PERMISSIONS
        FOR select WHERE
            -- Can see comments on posts you can see
            (SELECT VALUE published FROM ONLY post WHERE id = $parent.post) = true
            OR $auth.id IS NOT NONE
        FOR create WHERE $auth.id IS NOT NONE
        FOR update WHERE author = $auth.id
        FOR delete WHERE
            author = $auth.id
            OR $auth.role = 'moderator';

-- Access-method-specific permissions
DEFINE TABLE user SCHEMAFULL
    PERMISSIONS
        FOR select WHERE
            $access = 'account' AND id = $auth.id  -- record users see only themselves
            OR $access = 'admin_access'              -- admin access sees all
        FOR update WHERE id = $auth.id
        FOR delete NONE;
```

---

## Field-Level Permissions

> **v3.1.4 security fix (GHSA-8rw6-p7m8-63jp):** array element-level
> `PERMISSIONS FOR select WHERE …` on fields such as `items[*]` could leak
> denied elements on 3.1.0–3.1.3. Upgrade to **v3.1.4+** before relying on
> per-element array permissions in production.

### PERMISSIONS on DEFINE FIELD

```surrealql
-- Restrict field visibility and mutability
DEFINE TABLE user SCHEMAFULL
    PERMISSIONS FOR select, create, update WHERE $auth.id = id OR $auth.role = 'admin';

DEFINE FIELD email ON TABLE user TYPE string
    PERMISSIONS
        FOR select WHERE id = $auth.id OR $auth.role = 'admin'
        FOR update WHERE id = $auth.id;

DEFINE FIELD pass ON TABLE user TYPE string
    PERMISSIONS
        FOR select NONE  -- password hash is never returned
        FOR update WHERE id = $auth.id;

DEFINE FIELD role ON TABLE user TYPE string
    PERMISSIONS
        FOR select FULL
        FOR update WHERE $auth.role = 'admin';  -- only admins can change roles

DEFINE FIELD salary ON TABLE user TYPE option<decimal>
    PERMISSIONS
        FOR select WHERE id = $auth.id OR $auth.role IN ['admin', 'hr']
        FOR update WHERE $auth.role IN ['admin', 'hr'];

DEFINE FIELD internal_notes ON TABLE user TYPE option<string>
    PERMISSIONS
        FOR select WHERE $auth.role IN ['admin', 'hr']
        FOR update WHERE $auth.role = 'admin';
```

### Computed Field Security

```surrealql
-- Computed fields can enforce derived security values
DEFINE FIELD created_by ON TABLE document TYPE record<user>
    DEFAULT $auth.id
    READONLY;  -- cannot be overwritten after creation

DEFINE FIELD tenant ON TABLE document TYPE record<tenant>
    DEFAULT $auth.tenant
    READONLY;

-- Computed field that masks sensitive data based on viewer
DEFINE FIELD display_email ON TABLE user VALUE
    IF $auth.role = 'admin' OR $auth.id = id THEN
        email
    ELSE
        string::concat(
            string::slice(email, 0, 2),
            '***@',
            string::split(email, '@')[1]
        )
    END;
```

### Sensitive Data Masking

```surrealql
-- Credit card masking
DEFINE TABLE payment_method SCHEMAFULL;
DEFINE FIELD card_number ON TABLE payment_method TYPE string
    PERMISSIONS FOR select NONE;  -- raw number never returned
DEFINE FIELD masked_card ON TABLE payment_method VALUE
    string::concat('****-****-****-', string::slice(card_number, -4));
DEFINE FIELD cardholder ON TABLE payment_method TYPE string;
DEFINE FIELD expiry ON TABLE payment_method TYPE string;

-- SSN/sensitive ID masking
DEFINE FIELD ssn ON TABLE employee TYPE string
    PERMISSIONS
        FOR select WHERE $auth.role = 'hr_admin'
        FOR update WHERE $auth.role = 'hr_admin';
DEFINE FIELD masked_ssn ON TABLE employee VALUE
    string::concat('***-**-', string::slice(ssn, -4));
```

---

## Security Best Practices

### Principle of Least Privilege

```surrealql
-- Start with NONE and explicitly grant access
DEFINE TABLE sensitive_data SCHEMAFULL
    PERMISSIONS
        FOR select, create, update, delete NONE;

-- Then open up only what is needed
-- Better: grant specific access to specific roles
DEFINE TABLE project SCHEMAFULL
    PERMISSIONS
        FOR select WHERE
            team_member = $auth.id
            OR $auth.role IN ['admin', 'project_manager']
        FOR create WHERE $auth.role IN ['admin', 'project_manager']
        FOR update WHERE
            lead = $auth.id
            OR $auth.role = 'admin'
        FOR delete WHERE $auth.role = 'admin';
```

### Password Hashing

SurrealDB provides built-in cryptographic hashing functions. Always use argon2 for password storage.

```surrealql
-- Argon2 (recommended -- memory-hard, resistant to GPU attacks)
crypto::argon2::generate($password)
crypto::argon2::compare($hash, $password)

-- Bcrypt (acceptable alternative)
crypto::bcrypt::generate($password)
crypto::bcrypt::compare($hash, $password)

-- Scrypt (another memory-hard option)
crypto::scrypt::generate($password)
crypto::scrypt::compare($hash, $password)

-- SHA-256/512 (NOT suitable for passwords, use for data integrity only)
crypto::sha256($data)
crypto::sha512($data)

-- PBKDF2 (acceptable but argon2 is preferred)
crypto::pbkdf2::generate($password)
crypto::pbkdf2::compare($hash, $password)

-- NEVER store plaintext passwords
-- BAD:
CREATE user SET pass = $pass;
-- GOOD:
CREATE user SET pass = crypto::argon2::generate($pass);
```

### Token Duration Guidelines

| Use Case | Token Duration | Session Duration |
|---|---|---|
| Banking/financial | 5m | 30m |
| Enterprise SaaS | 15m | 8h |
| Consumer web app | 30m | 24h |
| Mobile app | 1h | 30d |
| Internal tool | 1h | 12h |
| IoT device | 24h | 90d |

```surrealql
-- High-security pattern: short tokens, moderate sessions
DEFINE ACCESS banking ON DATABASE TYPE RECORD
    SIGNUP (...)
    SIGNIN (...)
    DURATION FOR TOKEN 5m, FOR SESSION 30m;
```

### CORS Configuration

CORS is configured at the server level when starting SurrealDB, not in SurrealQL.

```bash
# Allow specific origins. The flag is `--allow-origin` (singular) in
# v3 — verified against `surrealdb/server/src/cli/start.rs`. Pass it
# multiple times (or use a comma-separated list) to allow multiple
# origins.
surreal start --allow-origin "https://app.example.com" \
              --allow-origin "https://admin.example.com"

# Allow all origins (development only)
surreal start --allow-origin "*"

# Full server startup with security flags. NOTE: in v3, strictness
# is no longer a server-startup flag — `--strict` is deprecated and
# silently ignored. v3 only accepts STRICT on `DEFINE DATABASE` (NOT
# on `DEFINE NAMESPACE` — verified against `core/src/sql/statements/
# define/namespace.rs`, which has no `strict` field). For namespace-
# wide coverage, define each database within the namespace as STRICT:
#   USE NS prod;
#   DEFINE DATABASE app STRICT;
#   DEFINE DATABASE analytics STRICT;
# To restrict server-level surface, use the capabilities flags
# (`--deny-guests`, `--deny-arbitrary-query`, `--deny-funcs <list>`,
# etc.) — see the network-security and CORS sections below.
surreal start \
    --bind 0.0.0.0:8000 \
    --user root \
    --pass "strong-root-password" \
    --allow-origin "https://app.example.com" \
    --deny-guests \
    rocksdb:///var/data/surreal.db
```

### TLS/SSL Configuration

```bash
# Start with TLS
surreal start \
    --web-crt /etc/ssl/certs/server.crt \
    --web-key /etc/ssl/private/server.key \
    --bind 0.0.0.0:8000

# Client connections should use wss:// or https://
# wss://db.example.com:8000/rpc  (WebSocket with TLS)
# https://db.example.com:8000    (HTTP with TLS)
```

### Network Security for Distributed Deployments

```bash
# Bind only to private network interfaces
surreal start --bind 10.0.1.5:8000

# For TiKV distributed deployments, ensure:
# 1. TiKV nodes communicate over private network
# 2. PD (Placement Driver) is not exposed publicly
# 3. SurrealDB compute nodes connect to TiKV over private network
surreal start --kvs-ca /etc/tikv/ca.pem --kvs-crt /etc/tikv/client.crt --kvs-key /etc/tikv/client.key tikv://10.0.1.10:2379

# In v3, `--strict` is deprecated and silently ignored. Enforce
# strict mode per-database at runtime (STRICT is NOT valid on
# DEFINE NAMESPACE in v3 — only on DEFINE DATABASE):
#   DEFINE DATABASE app STRICT;
# For namespace-wide coverage, define each database within the
# namespace as STRICT. To require authentication for all connections,
# deny guest access at the server level via the capabilities flag
# below.
surreal start --deny-guests --deny-arbitrary-query
```

### Audit Logging Patterns

```surrealql
-- Create an append-only audit log table
DEFINE TABLE audit_log SCHEMAFULL
    PERMISSIONS
        FOR select WHERE $auth.role = 'admin'
        FOR create FULL
        FOR update, delete NONE;  -- immutable records

DEFINE FIELD action ON TABLE audit_log TYPE string;
DEFINE FIELD table_name ON TABLE audit_log TYPE string;
DEFINE FIELD record_id ON TABLE audit_log TYPE option<record>;
DEFINE FIELD actor ON TABLE audit_log TYPE option<record<user>>;
DEFINE FIELD timestamp ON TABLE audit_log TYPE datetime DEFAULT time::now();
DEFINE FIELD details ON TABLE audit_log TYPE option<object>;

-- Attach audit events to sensitive tables
DEFINE EVENT audit_user_changes ON TABLE user WHEN $event IN ["CREATE", "UPDATE", "DELETE"] THEN {
    CREATE audit_log SET
        action = $event,
        table_name = 'user',
        record_id = $after.id ?? $before.id,
        actor = $auth.id,
        details = {
            before: IF $event != "CREATE" THEN $before ELSE NONE END,
            after: IF $event != "DELETE" THEN $after ELSE NONE END
        };
};

DEFINE EVENT audit_permission_changes ON TABLE system_config
    WHEN $event IN ["CREATE", "UPDATE", "DELETE"] THEN {
    CREATE audit_log SET
        action = $event,
        table_name = 'system_config',
        record_id = $after.id ?? $before.id,
        actor = $auth.id,
        details = { event: $event };
};
```

### Common Security Pitfalls

1. Using `PERMISSIONS FOR select FULL` on tables with sensitive data. This allows unauthenticated access.

2. Forgetting that `$auth` is NONE for unauthenticated requests. Always check `$auth.id IS NOT NONE` where authentication is required.

3. Not setting PERMISSIONS at all. By default, tables without PERMISSIONS allow full access to all authenticated system users (root, namespace, database) but deny access to record users.

4. Storing plaintext passwords. Always use `crypto::argon2::generate()`.

5. Using overly long token durations. Keep tokens short (5-30 minutes) and sessions reasonable.

6. Relying on `--strict` for production hardening. The flag is deprecated in v3 and silently ignored at startup. Enforce strict mode at the schema layer with `DEFINE DATABASE <db> STRICT;` (STRICT is only valid on `DEFINE DATABASE` in v3 — not on `DEFINE NAMESPACE`; for namespace-wide coverage, define each database within the namespace as STRICT), and lock down server-level surface with `--deny-guests` and `--deny-arbitrary-query`.

7. Exposing SurrealDB directly to the internet without TLS. Always use TLS in production.

8. Using HS256 JWT with a weak secret key. Use at least 256 bits of entropy or prefer asymmetric algorithms (RS256, ES256).

---

## Authentication Flows

### Signup/Signin Flow for Web Applications

```surrealql
-- 1. Define the access method
DEFINE ACCESS account ON DATABASE TYPE RECORD
    SIGNUP (
        CREATE user SET
            email = string::lowercase($email),
            pass = crypto::argon2::generate($pass),
            name = $name,
            created_at = time::now(),
            role = 'member'
    )
    SIGNIN (
        SELECT * FROM user
        WHERE email = string::lowercase($email)
        AND crypto::argon2::compare(pass, $pass)
    )
    DURATION FOR TOKEN 15m, FOR SESSION 12h;

-- 2. User table with permissions
DEFINE TABLE user SCHEMAFULL
    PERMISSIONS
        FOR select WHERE id = $auth.id OR $auth.role = 'admin'
        FOR update WHERE id = $auth.id
        FOR delete WHERE $auth.role = 'admin'
        FOR create NONE;  -- users are created only through SIGNUP

DEFINE FIELD email ON TABLE user TYPE string ASSERT string::is_email($value);
DEFINE FIELD pass ON TABLE user TYPE string PERMISSIONS FOR select NONE;
DEFINE FIELD name ON TABLE user TYPE string;
DEFINE FIELD role ON TABLE user TYPE string DEFAULT 'member';
DEFINE FIELD created_at ON TABLE user TYPE datetime;
```

Client-side flow (using the JavaScript SDK):

```javascript
import Surreal from 'surrealdb';

const db = new Surreal();
await db.connect('wss://db.example.com/rpc');
await db.use({ namespace: 'production', database: 'app' });

// Sign up
const signupToken = await db.signup({
    access: 'account',
    variables: {
        email: 'user@example.com',
        pass: 'secure-password',
        name: 'Alice'
    }
});

// Sign in
const signinToken = await db.signin({
    access: 'account',
    variables: {
        email: 'user@example.com',
        pass: 'secure-password'
    }
});

// Authenticate with existing token
await db.authenticate(signinToken);

// All subsequent queries are scoped to this user
const myProfile = await db.select('user');
// Returns only the authenticated user's record (due to PERMISSIONS)
```

### JWT Token Integration with External Identity Providers

```surrealql
-- Define JWT access that maps external IdP tokens to a SurrealDB
-- record. `WITH JWT KEY` is the verification key (validates
-- inbound third-party JWTs). AUTHENTICATE binds the token's
-- subject claim to a local record; without AUTHENTICATE, the
-- inbound JWT must carry SurrealDB's own `id` claim or
-- verification bails `AccessMethodMismatch` at
-- `core/src/iam/verify.rs:464`. WITH ISSUER KEY is omitted
-- because this access method is authenticate-only — there is
-- no SIGNIN clause that would trigger SurrealDB-side minting,
-- and on the authenticate path SurrealDB does not mint tokens
-- (the AccessType::Record arm at `verify.rs:401-462` for
-- claims-without-`id` calls `authenticate_record` to bind the
-- record from $token.* but never invokes `encode` — issuance
-- is reserved for the signin flow).
DEFINE ACCESS external_idp ON DATABASE TYPE RECORD
    -- Clause order: WITH JWT must precede AUTHENTICATE (the
    -- TYPE RECORD subparser at define.rs:456-507 consumes WITH
    -- JWT/REFRESH before returning to the outer access-define
    -- loop where AUTHENTICATE is matched).
    WITH JWT
        ALGORITHM RS256 KEY '-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
-----END PUBLIC KEY-----'
    AUTHENTICATE (
        SELECT id FROM user WHERE external_id = $token.sub
    )
    DURATION FOR SESSION 12h;

-- The JWT payload MUST include `ns`, `db`, `ac` routing claims
-- (or aliases per `core/src/iam/token.rs:248-275`) — without
-- them, `core/src/iam/verify.rs:292-297` cannot match the
-- database-access arm and falls through to InvalidAuth at
-- :825-826. Example JWT payload (issued by the IdP, NOT by
-- SurrealDB; configure the IdP to mint these custom claims via
-- Auth0 Actions / Okta inline hooks / Cognito pre-token Lambda
-- / Azure AD claim mapping):
-- {
--   "ns": "production",
--   "db": "app",
--   "ac": "external_idp",
--   "sub": "auth0|12345",
--   "email": "user@example.com",
--   "roles": ["editor"],
--   "tenant_id": "tenant:acme",
--   "exp": 1700000000
-- }
-- (The serde aliases also accept "NS"/"DB"/"AC" or
-- "https://surrealdb.com/ns" full-URI forms if your IdP
-- requires namespaced claim keys.)

-- Access JWT claims in permissions via $token. Permissions can
-- read $token.* on EVERY query after authenticate; AUTHENTICATE
-- only runs once at session establishment. Use $token.* for
-- claim-driven row filtering as below.
DEFINE TABLE document SCHEMAFULL
    PERMISSIONS
        FOR select WHERE tenant = $token.tenant_id
        FOR create WHERE 'editor' IN $token.roles
        FOR update WHERE 'editor' IN $token.roles AND tenant = $token.tenant_id
        FOR delete WHERE 'admin' IN $token.roles;
```

### Session Management

```surrealql
-- Define explicit session tracking
DEFINE TABLE session SCHEMAFULL
    PERMISSIONS
        FOR select WHERE user = $auth.id
        FOR create WHERE $auth.id IS NOT NONE
        FOR update, delete WHERE user = $auth.id;

DEFINE FIELD user ON TABLE session TYPE record<user>;
DEFINE FIELD device ON TABLE session TYPE string;
DEFINE FIELD ip_address ON TABLE session TYPE string;
DEFINE FIELD created_at ON TABLE session TYPE datetime DEFAULT time::now();
DEFINE FIELD last_active ON TABLE session TYPE datetime DEFAULT time::now();
DEFINE FIELD expires_at ON TABLE session TYPE datetime;

-- Create session on signin
DEFINE EVENT track_signin ON TABLE user WHEN $event = "UPDATE"
    AND $after.last_signin != $before.last_signin THEN {
    CREATE session SET
        user = $after.id,
        device = $after.current_device,
        ip_address = $after.current_ip,
        expires_at = time::now() + 12h;
};

-- Clean expired sessions (run periodically via application or cron)
DELETE session WHERE expires_at < time::now();
```

### Multi-Tenant Security with Namespaces

```surrealql
-- Strategy 1: One namespace per tenant (strongest isolation)
-- Each tenant gets their own namespace with identical schema

-- Tenant A
USE NS tenant_a DB main;
DEFINE ACCESS account ON DATABASE TYPE RECORD
    SIGNUP (CREATE user SET email = $email, pass = crypto::argon2::generate($pass))
    SIGNIN (SELECT * FROM user WHERE email = $email AND crypto::argon2::compare(pass, $pass))
    DURATION FOR TOKEN 15m, FOR SESSION 12h;

-- Tenant B (completely isolated)
USE NS tenant_b DB main;
DEFINE ACCESS account ON DATABASE TYPE RECORD
    SIGNUP (CREATE user SET email = $email, pass = crypto::argon2::generate($pass))
    SIGNIN (SELECT * FROM user WHERE email = $email AND crypto::argon2::compare(pass, $pass))
    DURATION FOR TOKEN 15m, FOR SESSION 12h;
```

```surrealql
-- Strategy 2: Shared database with tenant column (simpler, less isolation)
USE NS production DB shared;

DEFINE TABLE tenant SCHEMAFULL
    PERMISSIONS FOR select, create, update, delete NONE;  -- admin only

DEFINE TABLE user SCHEMAFULL
    PERMISSIONS
        FOR select WHERE tenant = $auth.tenant
        FOR update WHERE id = $auth.id
        FOR create, delete NONE;
DEFINE FIELD tenant ON TABLE user TYPE record<tenant> READONLY;

DEFINE TABLE data SCHEMAFULL
    PERMISSIONS
        FOR select WHERE tenant = $auth.tenant
        FOR create WHERE tenant = $auth.tenant
        FOR update WHERE tenant = $auth.tenant
        FOR delete WHERE tenant = $auth.tenant AND $auth.role = 'admin';
DEFINE FIELD tenant ON TABLE data TYPE record<tenant> DEFAULT $auth.tenant READONLY;

-- The READONLY + DEFAULT ensures the tenant field is automatically set
-- and cannot be tampered with by the user
```

---

## Security Checklist for Production

Before deploying SurrealDB to production:

- Use `--deny-guests` and `--deny-arbitrary-query` to require authentication for all connections (the legacy `--strict` flag is deprecated and silently ignored in v3); enforce schema strictness via `DEFINE DATABASE <db> STRICT;` (STRICT is only valid on `DEFINE DATABASE` in v3, not on `DEFINE NAMESPACE` — for namespace-wide coverage, define each database within the namespace as STRICT)
- Enable TLS with valid certificates (`--web-crt`, `--web-key`)
- Set strong root passwords (minimum 20 characters, random)
- Define PERMISSIONS on every table that record users access
- Use `PERMISSIONS FOR select NONE` on password/secret fields
- Use `crypto::argon2::generate()` for all password storage
- Set appropriate token and session durations
- Restrict CORS to specific origins (not `*`)
- Bind to private network interfaces where possible
- Enable audit logging on sensitive tables
- Review all `FULL` permissions for unintended public access
- Ensure `$auth.id IS NOT NONE` checks where authentication is required
- Use SCHEMAFULL tables to prevent schema injection
- Set `READONLY` on fields that should not be user-modifiable (tenant, created_by)
- Use asymmetric JWT algorithms (RS256, ES256) over symmetric (HS256) when possible
- Regularly rotate JWT signing keys
- Test permissions thoroughly with different user roles
