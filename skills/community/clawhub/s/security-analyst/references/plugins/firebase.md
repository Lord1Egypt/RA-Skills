---
name: Firebase
detect:
  files: ["firebase.json", "firestore.rules", ".firebaserc", "database.rules.json"]
  dependencies: ["firebase-admin", "firebase-functions", "@firebase/app", "@firebase/auth", "@firebase/firestore"]
  keywords: ["Firebase", "Firestore", "Cloud Functions for Firebase"]
---

## attack-surface-http

**Cloud Tasks & Background Function Authentication:**
1. Are Cloud Tasks endpoints validating OIDC tokens from the task queue service account?
   - Grep for `onTaskDispatched`, `onDispatch`, Cloud Tasks handler patterns
   - Check: is the OIDC audience verified? Can an attacker call the endpoint directly without a valid task token?
2. Can an attacker enqueue arbitrary Cloud Tasks by calling the task creation API directly?
   - Check: are task creation permissions restricted to the correct service account?

**Firestore Trigger Data Injection:**
3. For each `onDocumentCreated`, `onDocumentWritten`, `onDocumentUpdated` trigger:
   - Can a client write to the triggering collection with attacker-controlled data?
   - Does the trigger function trust the document data without validation?
   - Can the trigger be used to escalate privileges? (e.g., writing a document that triggers admin-level processing)

**Pub/Sub Message Authentication:**
4. For each `onMessagePublished` handler:
   - Is the Pub/Sub subscription authenticated?
   - Can an attacker publish messages directly to the topic?
   - Is message data validated in the handler?

**Recursive Trigger Detection (Self-DoS Risk):**
5. Can a function trigger cause a loop? (Function A writes to Firestore -> triggers Function B -> writes back -> triggers Function A)
   - Check for write operations inside Firestore trigger handlers that target the same or related collections
   - Per Firebase checklist: test functions locally with the emulator suite before deploying to catch infinite trigger-write loops
   - If a self-DoS occurs, the fix is to undeploy the function by removing it from `index.js` and running `firebase deploy --only functions`

**Callable Function Auth:**
6. For each `onCall` / `onRequest` handler:
   - Is `context.auth` checked before processing?
   - For `onRequest`: is auth handled manually? (Firebase Auth is NOT automatic for HTTP functions)
   - Can an unauthenticated request reach processing logic?

**Defensive Function Design:**
7. Per Firebase checklist: where real-time responsiveness is less important, are functions structured defensively?
   - Are results published to Pub/Sub and processed in batches via scheduled functions (to mitigate abusive traffic)?
   - Are simple functions preferred over complex ones? (complexity leads to hard-to-spot bugs — consider Cloud Run for complex logic)

## attack-surface-authz

**Firestore Security Rules — Existence and Mode:**
1. Do Firestore security rules actually exist?
   - Glob for `firestore.rules`, `*.rules` in the project root
   - If no rules file exists: **Critical** — the database may be using default open rules
   - Read `firebase.json` and check if `firestore.rules` is referenced — if not, rules may not be deployed
2. Were rules initialized in **production mode** (deny all by default)?
   - Per Firebase checklist: rules should deny all access by default, with specific allow rules added per resource
   - Check: does the root have `allow read, write: if false;`? Or is there a wide-open `allow read, write: if true;` or `allow read, write: if request.auth != null;` at the top level?
   - A rule like `allow read, write: if request.auth != null;` at the root is almost as bad as no rules — any authenticated user can read/write anything

**Firestore Security Rules Deep Analysis:**
3. Read `firestore.rules` completely and analyze:
   - **`rules_version`**: Is `rules_version = '2';` declared at the top? Version 1 is legacy with different wildcard and recursive behavior — version 2 is required for collection group queries and recommended for all new projects
   - **Wildcard paths**: Are `{document=**}` wildcards used? These match all subcollections and can create overly permissive rules
   - **Collection group queries**: Are there `match /{path=**}/collectionName/{doc}` rules? These apply to collection group queries across all parent documents — verify the ownership check is correct
   - **`request.resource.data` vs `resource.data`**: `request.resource.data` is what the client is trying to write; `resource.data` is the current document state. Confusing these is a common source of write bypass
   - **Field-level validation**: Are rules checking specific fields the client can set? Or just checking auth?
   - **Server-enforced fields**: Can a client write to fields that should only be set server-side (timestamps, counters, status)?

4. **Granular CRUD Operation Splitting:**
   - Are rules using broad `allow read` / `allow write` instead of granular operations?
   - `read` should be split into `get` (single document) and `list` (collection queries) where different access levels are needed — a user may be allowed to `get` their own document but should not `list` the entire collection
   - `write` should be split into `create`, `update`, and `delete` — each has different security implications:
     - `create`: validate all required fields are present, ownership field matches `request.auth.uid`
     - `update`: prevent ownership transfer — check BOTH `request.resource.data.author_uid == request.auth.uid` AND `resource.data.author_uid == request.auth.uid` to prevent a user from changing the owner field
     - `delete`: may need stricter conditions than update (e.g., only admins can delete)
   - Overly broad `allow write: if request.auth.uid != null` gives authenticated users create + update + delete on everything

5. **Data Type and Schema Validation in Rules:**
   - Are rules validating the **types** of incoming fields? (e.g., `request.resource.data.amount is number`, `request.resource.data.name is string`)
   - Are rules enforcing **required fields**? (e.g., `request.resource.data.keys().hasAll(['name', 'email', 'createdAt'])`)
   - Are rules preventing **extra fields**? (e.g., checking `request.resource.data.keys().hasOnly(['name', 'email', 'createdAt', 'updatedAt'])` to prevent clients from adding arbitrary fields like `role` or `isAdmin`)
   - Are rules validating **field value constraints**? (e.g., string length limits with `request.resource.data.name.size() < 100`, numeric ranges)
   - Are rules enforcing **immutable fields**? (e.g., on update, `request.resource.data.createdAt == resource.data.createdAt` to prevent clients from changing creation timestamps)

6. **Time-Based Access Rules:**
   - Are `request.time` checks used for temporal access controls? (e.g., `allow read: if resource.data.publishDate <= request.time` for embargoed content)
   - Are there time-limited tokens or expiring access patterns that use timestamps in rules?
   - Can an attacker exploit stale timestamp comparisons? (Firestore server timestamps are authoritative but `request.resource.data` timestamps can be client-provided — always use `request.time` for server-authoritative time)

7. **Role-Based Access via `get()` Calls in Rules:**
   - Do rules use `get()` or `exists()` to check roles/permissions from other documents? (e.g., `get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == "admin"`)
   - Each `get()` or `exists()` call in a rule counts as a **billed document read** — can an attacker cause excessive billing by triggering many rule evaluations?
   - Rules are limited to 10 `get()` calls per request — are complex role checks approaching this limit?
   - Can the referenced role document be modified by the user themselves? (if `users/{uid}` is user-writable and rules read roles from it, the user can self-escalate)

8. **Rules as Schema (Firebase Checklist Best Practice):**
   - Are security rules written alongside the data model? (not as a pre-launch afterthought)
   - Does every document type/path have a corresponding rule?
   - Are there paths that lack explicit rules? (in Firestore, unmatched paths are denied by default, but verify no wildcard rule grants unintended access)

9. **Security Rules Testing:**
   - Are there unit tests for security rules using the Firebase Emulator Suite? (Glob for test files with `@firebase/rules-unit-testing` or `firebase/testing` imports)
   - Are rules tests part of the CI pipeline?
   - Per Firebase checklist: untested rules are a significant risk — every rule path should have test coverage

**Realtime Database Rules (if applicable):**
10. If the project uses Realtime Database (check for `database.rules.json` or `"database"` in `firebase.json`):
    - Were rules initialized in **locked mode**? (`".read": false, ".write": false`)
    - Are there `".read": true` or `".write": true` at any level? (wide-open access)
    - Is `auth != null` the only check? (any authenticated user can read/write)
    - **Rule Cascade Gotcha**: RTDB rules cascade downward — a `.read: true` at a parent path **cannot be revoked** by `.read: false` at a child path. The child rule is silently ignored. Check for parent rules that are too permissive, since child rules can only GRANT additional access, never restrict it
    - Are there `$wildcard` variables used for path-delineated access? (e.g., `"$uid": { ".read": "auth.uid === $uid" }`)
    - Is `.validate` used for data shape enforcement? (`.validate` only runs on write, not on read — it cannot restrict read access)

**Cloud Storage Rules (if applicable):**
11. If the project uses Cloud Storage (check for `storage.rules` or `"storage"` in `firebase.json`):
    - Do rules default to deny? Per Firebase checklist, start with:
      ```
      allow read, write: if false;
      ```
    - Are upload size limits enforced in rules? (`request.resource.size < maxSize`)
    - Are content types validated? (`request.resource.contentType.matches('image/.*')`)
    - **Metadata-based ownership**: If `resource.metadata` is used for group/owner access control (e.g., `resource.metadata.owner == request.auth.token.groupId`), can an attacker set their own metadata on upload to claim ownership?
    - Are there path-based ownership rules? (e.g., `/user/{userId}/` prefix) — verify that `request.auth.uid == userId` is enforced and the user cannot write outside their path
    - Note: files may still be accessible via App Engine or Google Cloud Storage APIs even if Firebase Storage rules deny access — check for alternative access paths

**Firebase Auth Custom Claims:**
12. Are custom claims used for authorization? (Grep for `token.admin`, `token.role`, custom claim fields in rules)
    - Can a client influence their own custom claims? (Check if there's a callable function that sets claims based on user input)
    - Are claims propagated correctly? (Claims are set on the token and only refresh on token refresh — stale claims window)

13. **Cross-User Access:**
    - For each user-scoped collection (`users/{userId}/...`), verify rules enforce `request.auth.uid == userId`
    - For subcollections: do nested rules inherit the parent ownership check or do they need their own?
    - Are there admin bypass paths? How are admin users identified in rules? (custom claim? specific UID list?)

14. **Anonymous Auth in Rules:**
    - Per Firebase checklist: anonymous accounts are easy to create — protect non-public data with rules requiring specific sign-in providers or verified email
    - Check for rules that only check `request.auth != null` without verifying the sign-in provider or email verification
    - Look for: `request.auth.token.firebase.sign_in_provider != "anonymous"` or `request.auth.token.email_verified == true` on sensitive resources

## attack-surface-frontend

**Firebase API Keys:**
1. Firebase client config (`apiKey`, `authDomain`, `projectId`, etc.) is **public by design** and NOT a vulnerability — mark as Informational if found
   - Per Firebase checklist: API keys for Firebase services only identify the project, not control access
2. However, check:
   - Are there OTHER API keys mixed in with Firebase config that are NOT meant to be public? (FCM server keys, service account keys)
   - Per Firebase checklist: **FCM server keys** (legacy HTTP API) ARE sensitive and must be kept secret
   - Per Firebase checklist: **Service account private keys** (Admin SDK) ARE sensitive and must be kept secret
3. **API Key Restrictions:**
   - Are API key restrictions configured in the Google Cloud console? (app restrictions, API restrictions)
   - Per Firebase checklist: set up API key restrictions to scope keys to your app clients and the APIs you use

**Firebase Auth UI:**
4. If using Firebase Auth UI or `signInWithRedirect`/`signInWithPopup`:
   - Is the `authDomain` configured correctly? (custom domain vs default `.firebaseapp.com`)
   - Can the redirect URL be manipulated? (check `continueUrl` parameter handling)
   - Is `signInSuccessUrl` validated against an allowlist?

5. **Authentication Provider Security:**
   - Per Firebase checklist: OAuth 2.0 / OpenID Connect providers (Google, Facebook, etc.) are the most secure option
   - If using email-password auth: is the quota on `identitytoolkit.googleapis.com` endpoints tightened to prevent brute force?
   - If using email-password auth: is email enumeration protection enabled?
   - Is multi-factor authentication supported? (upgrade to Cloud Identity Platform)

6. **Anonymous Authentication:**
   - Per Firebase checklist: only use anonymous auth for warm onboarding, not as a replacement for user sign-in
   - Are anonymous users converted to permanent accounts before data needs to persist across devices?
   - Are security rules properly restricting what anonymous users can access?

**Firestore Client-Side Access:**
7. Are there client-side Firestore reads/writes? (Grep for `getDoc`, `setDoc`, `updateDoc`, `addDoc`, `onSnapshot`)
   - Is all client-side data access protected by Firestore rules?
   - Are there client-side writes that should only be server-side?

## config-infrastructure

**Firebase Hosting Configuration:**
1. Read `firebase.json` and analyze:
   - **Rewrites**: Do rewrite rules send unauthenticated requests to Cloud Functions? (rewrites bypass function-level auth checks if the function doesn't verify auth itself)
   - **Headers**: Is the `headers` section restrictive? Check for overly broad CORS (`Access-Control-Allow-Origin: *` on all paths)
   - **`cleanUrls` and `trailingSlash`**: These can create unexpected path resolution that bypasses path-based security checks
   - **Security headers**: Are CSP, HSTS, X-Frame-Options configured in firebase.json `headers`?

2. **Emulator Detection:**
   - Grep for `FIREBASE_EMULATOR`, `connectFirestoreEmulator`, `connectAuthEmulator`, `useEmulator`
   - Is there any code path that connects to emulators based on environment variables in production?
   - Can an attacker set environment variables to redirect traffic to a malicious endpoint?

3. **Firebase App Check:**
   - Is App Check enabled? (Grep for `appCheck`, `AppCheck`, attestation providers)
   - Per Firebase checklist: enable App Check for every service that supports it
   - Are Cloud Functions enforcing App Check? (Grep for `app-check` context)
   - Can App Check be bypassed by debug tokens left in production?

4. **Cloud Functions Secrets Management:**
   - Per Firebase checklist: **never put sensitive information in environment variables** for Cloud Functions (environments are reused between invocations)
   - Are secrets stored using Secret Manager? (Grep for `defineSecret`, `SecretManagerServiceClient`, `secret-manager`)
   - Are there hardcoded API keys, tokens, or private keys in function code?
   - If calling Google APIs: is the Admin SDK using automatic credential acquisition (no explicit service account key)?
   - If non-Google credentials are needed: are they accessed via Secret Manager, not env vars?
   - Per Firebase checklist: if sensitive information must be passed to functions, encrypt it with a custom solution

5. **Environment Separation:**
   - Per Firebase checklist: are there separate Firebase projects for development, staging, and production?
   - Can development credentials access production resources?
   - Is team access to the production project limited? (check predefined IAM roles or custom IAM roles)

6. **Monitoring and Budget Alerting:**
   - Per Firebase checklist: set up monitoring and alerting for Cloud Firestore, Realtime Database, Cloud Storage, and Hosting
   - Are budget alerts configured on the GCP project to detect unusual resource usage?
   - Is the Usage and billing dashboard monitored?

7. **IAM and Service Accounts:**
   - Are Cloud Functions using the default service account with overly broad permissions?
   - Are there custom service accounts with least-privilege permissions for each function?
   - Are there service account keys downloaded and stored insecurely? (service account private keys must be kept secret)

## dependency-audit

**Firebase Library Supply Chain:**
1. Per Firebase checklist: watch out for library misspellings or new maintainers when adding dependencies
   - Are Firebase SDK packages from the official `firebase` or `@firebase/` scope?
   - Are there similarly-named packages that could be typosquat attacks?
2. Per Firebase checklist: don't update libraries without understanding the changes
   - Check changelogs for Firebase SDK updates before upgrading
3. Per Firebase checklist: install watchdog libraries (Snyk, npm audit) as dev dependencies to scan for insecure dependencies
4. Is the Cloud Functions logger SDK used? (`firebase-functions/logger`)
   - Per Firebase checklist: set up monitoring after library updates to detect unusual behavior caused by dependency changes

## logic-race-conditions

**Firestore Transaction Specifics:**
1. Are Firestore transactions used for check-then-update operations?
   - Firestore transactions retry up to 5 times by default on contention — can this be exploited?
   - Is the transaction read set minimal? (reading unnecessary documents increases contention)
2. Does `FieldValue.increment()` provide sufficient atomicity for the use case?
   - Increment is atomic for a single field, but NOT for read-then-conditional-increment patterns
   - If the counter check + increment are separate operations, there's a race window

**Cloud Functions Cold Start Races:**
3. Are there global variables initialized on cold start that could be accessed before initialization completes?
4. If multiple instances start simultaneously, do they race on shared resources? (e.g., initializing a singleton, writing to a shared document)

## logic-dos

**Cloud Functions Scaling (Firebase Checklist):**
1. Per Firebase checklist: configure Cloud Functions to scale for **normal traffic**, not unlimited
   - Is `maxInstances` configured for each function? (prevents runaway scaling and billing attacks)
   - Are `minInstances` set appropriately? (too many wastes money, too few causes cold start latency)
2. Set up alerting to be notified when concurrent instance limits are nearly reached
3. Can an attacker trigger function invocations that scale indefinitely?
4. Are there recursive trigger chains that cause unbounded function invocations?
   - Per Firebase checklist: test with the emulator suite to catch self-DoS patterns before deploying

**Firestore Write Limits:**
5. Firestore batched writes are limited to 500 operations per batch
   - Can an attacker trigger an operation that tries to write > 500 documents? (causes failure)
   - Are batch sizes validated before processing?

6. **Firestore Rate Limits:**
   - Maximum 1 write per second per document — can an attacker trigger rapid writes to the same document to cause failures?
   - Maximum 10,000 writes per second per database — can an attacker approach this via amplification?

**Firebase Auth Rate Limits:**
7. Firebase Auth has built-in rate limits for sign-up, sign-in, and password reset — are there custom endpoints that bypass these by calling Admin SDK directly?
8. Per Firebase checklist: for email-password auth, tighten the default quota on `identitytoolkit.googleapis.com` endpoints to prevent brute force attacks
