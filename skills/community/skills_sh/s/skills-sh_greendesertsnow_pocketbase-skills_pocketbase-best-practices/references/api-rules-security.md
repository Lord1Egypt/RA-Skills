# API Rules & Security

**Impact: CRITICAL**

Access control rules, filter expressions, request context usage, and security patterns. Critical for protecting data and enforcing authorization.

---

## 1. Understand API Rule Types and Defaults

**Impact: CRITICAL (Prevents unauthorized access, data leaks, and security vulnerabilities)**

PocketBase uses five collection-level rules to control access. Understanding the difference between locked (null), open (""), and expression rules is critical for security.

**Incorrect (leaving rules open unintentionally):**

```javascript
// Collection with overly permissive rules
const collection = {
  name: 'messages',
  listRule: '',      // Anyone can list all messages!
  viewRule: '',      // Anyone can view any message!
  createRule: '',    // Anyone can create messages!
  updateRule: '',    // Anyone can update any message!
  deleteRule: ''     // Anyone can delete any message!
};
// Complete security bypass - all data exposed
```

**Correct (explicit, restrictive rules):**

```javascript
// Collection with proper access control
const collection = {
  name: 'messages',
  // null = locked, only superusers can access
  listRule: null,    // Default: locked to superusers

  // '' (empty string) = open to everyone (use sparingly)
  viewRule: '@request.auth.id != ""',  // Any authenticated user

  // Expression = conditional access
  createRule: '@request.auth.id != ""',  // Must be logged in
  updateRule: 'author = @request.auth.id',  // Only author
  deleteRule: 'author = @request.auth.id'   // Only author
};
```

**Rule types explained:**

| Rule Value | Meaning | Use Case |
|------------|---------|----------|
| `null` | Locked (superusers only) | Admin-only data, system tables |
| `''` (empty string) | Open to everyone | Public content, no auth required |
| `'expression'` | Conditional access | Most common - check auth, ownership |

**Common patterns:**

```javascript
// Public read, authenticated write (enforce ownership on create)
listRule: '',
viewRule: '',
createRule: '@request.auth.id != "" && @request.body.author = @request.auth.id',
updateRule: 'author = @request.auth.id',
deleteRule: 'author = @request.auth.id'

// Private to owner only
listRule: 'owner = @request.auth.id',
viewRule: 'owner = @request.auth.id',
createRule: '@request.auth.id != ""',
updateRule: 'owner = @request.auth.id',
deleteRule: 'owner = @request.auth.id'

// Read-only public data
listRule: '',
viewRule: '',
createRule: null,
updateRule: null,
deleteRule: null
```

**Error responses by rule type:**
- List rule fail: 200 with empty items
- View/Update/Delete fail: 404 (hides existence)
- Create fail: 400
- Locked rule violation: 403

Reference: [PocketBase API Rules](https://pocketbase.io/docs/api-rules-and-filters/)

## 2. Use @collection for Cross-Collection Lookups

**Impact: HIGH (Enables complex authorization without denormalization)**

The `@collection` reference allows rules to query other collections, enabling complex authorization patterns like role-based access, team membership, and resource permissions.

**Incorrect (denormalizing data for access control):**

```javascript
// Duplicating team membership in every resource
const documentsSchema = [
  { name: 'title', type: 'text' },
  { name: 'team', type: 'relation' },
  // Duplicated member list for access control - gets out of sync!
  { name: 'allowedUsers', type: 'relation', options: { maxSelect: 999 } }
];

// Rule checks duplicated data
listRule: 'allowedUsers ?= @request.auth.id'
// Problem: must update allowedUsers whenever team membership changes
```

**Correct (using @collection lookup):**

```javascript
// Clean schema - no duplication
const documentsSchema = [
  { name: 'title', type: 'text' },
  { name: 'team', type: 'relation', options: { collectionId: 'teams' } }
];

// Check team membership via @collection lookup
listRule: '@collection.team_members.user ?= @request.auth.id && @collection.team_members.team ?= team'

// Alternative: check if user is in team's members array
listRule: 'team.members ?= @request.auth.id'

// Role-based access via separate roles collection
listRule: '@collection.user_roles.user = @request.auth.id && @collection.user_roles.role = "admin"'
```

**Common patterns:**

```javascript
// Team-based access
// teams: { name, members (relation to users) }
// documents: { title, team (relation to teams) }
viewRule: 'team.members ?= @request.auth.id'

// Organization hierarchy
// orgs: { name }
// org_members: { org, user, role }
// projects: { name, org }
listRule: '@collection.org_members.org = org && @collection.org_members.user = @request.auth.id'

// Permission-based access
// permissions: { resource, user, level }
updateRule: '@collection.permissions.resource = id && @collection.permissions.user = @request.auth.id && @collection.permissions.level = "write"'

// Using aliases for complex queries
listRule: '@collection.memberships:m.user = @request.auth.id && @collection.memberships:m.team = team'
```

**Performance considerations:**
- Cross-collection lookups add query complexity
- Ensure referenced fields are indexed
- Consider caching for frequently accessed permissions
- Test performance with realistic data volumes

Reference: [PocketBase Collection Reference](https://pocketbase.io/docs/api-rules-and-filters/#collection-fields)

## 3. Master Filter Expression Syntax

**Impact: CRITICAL (Enables complex access control and efficient querying)**

PocketBase filter expressions use a specific syntax for both API rules and client-side queries. Understanding operators and composition is essential.

**Incorrect (invalid filter syntax):**

```javascript
// Wrong operator syntax
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'status == "published"'  // Wrong: == instead of =
});

// Missing quotes around strings
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'status = published'  // Wrong: unquoted string
});

// Wrong boolean logic
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'status = "published" AND featured = true'  // Wrong: AND instead of &&
});
```

**Correct (proper filter syntax):**

```javascript
// Equality and comparison operators
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'status = "published"'           // Equals
});
filter: 'views != 0'                        // Not equals
filter: 'views > 100'                       // Greater than
filter: 'views >= 100'                      // Greater or equal
filter: 'price < 50.00'                     // Less than
filter: 'created <= "2024-01-01 00:00:00"'  // Less or equal

// String operators
filter: 'title ~ "hello"'   // Contains (case-insensitive)
filter: 'title !~ "spam"'   // Does not contain

// Logical operators
filter: 'status = "published" && featured = true'   // AND
filter: 'category = "news" || category = "blog"'    // OR
filter: '(status = "draft" || status = "review") && author = "abc"'  // Grouping

// Array/multi-value operators (for select, relation fields)
filter: 'tags ?= "featured"'    // Any tag equals "featured"
filter: 'tags ?~ "tech"'        // Any tag contains "tech"

// Null checks
filter: 'deletedAt = null'      // Is null
filter: 'avatar != null'        // Is not null

// Date comparisons
filter: 'created > "2024-01-01 00:00:00"'
filter: 'created >= @now'       // Current timestamp
filter: 'expires < @today'      // Start of today (UTC)
```

**Available operators:**

| Operator | Description |
|----------|-------------|
| `=` | Equal |
| `!=` | Not equal |
| `>` `>=` `<` `<=` | Comparison |
| `~` | Contains (LIKE %value%) |
| `!~` | Does not contain |
| `?=` `?!=` `?>` `?~` | Any element matches |
| `&&` | AND |
| `\|\|` | OR |
| `()` | Grouping |

**Date macros:**
- `@now` - Current UTC datetime
- `@today` - Start of today UTC
- `@month` - Start of current month UTC
- `@year` - Start of current year UTC

**Filter functions:**
- `strftime(fmt, datetime)` - Format/extract datetime parts (v0.36+). E.g. `strftime('%Y-%m', created) = "2026-03"`. See `rules-strftime.md` for the full format specifier list.
- `length(field)` - Element count of a multi-value field (file, relation, select). E.g. `length(tags) > 0`.
- `each(field, expr)` - Iterate a multi-value field: `each(tags, ? ~ "urgent")`.
- `issetIf(field, val)` - Conditional presence check for complex rules.

Reference: [PocketBase Filters](https://pocketbase.io/docs/api-rules-and-filters/#filters-syntax)

## 4. Default to Locked Rules, Open Explicitly

**Impact: CRITICAL (Defense in depth, prevents accidental data exposure)**

New collections should start with locked (null) rules and explicitly open only what's needed. This prevents accidental data exposure and follows the principle of least privilege.

**Incorrect (starting with open rules):**

```javascript
// Dangerous: copying rules from examples without thinking
const collection = {
  name: 'user_settings',
  listRule: '',      // Open - leaks all user settings!
  viewRule: '',      // Open - anyone can view any setting
  createRule: '',    // Open - no auth required
  updateRule: '',    // Open - anyone can modify!
  deleteRule: ''     // Open - anyone can delete!
};

// Also dangerous: using auth check when ownership needed
const collection = {
  name: 'private_notes',
  listRule: '@request.auth.id != ""',  // Any logged-in user sees ALL notes
  viewRule: '@request.auth.id != ""',
  updateRule: '@request.auth.id != ""',  // Any user can edit ANY note!
};
```

**Correct (locked by default, explicitly opened):**

```javascript
// Step 1: Start locked
const collection = {
  name: 'user_settings',
  listRule: null,    // Locked - superusers only
  viewRule: null,
  createRule: null,
  updateRule: null,
  deleteRule: null
};

// Step 2: Open only what's needed with proper checks
const collection = {
  name: 'user_settings',
  // Users can only see their own settings
  listRule: 'user = @request.auth.id',
  viewRule: 'user = @request.auth.id',
  // Users can only create settings for themselves
  createRule: '@request.auth.id != "" && @request.body.user = @request.auth.id',
  // Users can only update their own settings
  updateRule: 'user = @request.auth.id',
  // Prevent deletion or restrict to owner
  deleteRule: 'user = @request.auth.id'
};

// For truly public data, document why it's open
const collection = {
  name: 'public_announcements',
  // Intentionally public - these are site-wide announcements
  listRule: '',
  viewRule: '',
  // Only admins can manage (using custom "role" field on auth collection)
  // IMPORTANT: Prevent role self-assignment in the users collection updateRule:
  //   updateRule: 'id = @request.auth.id && @request.body.role:isset = false'
  createRule: '@request.auth.role = "admin"',
  updateRule: '@request.auth.role = "admin"',
  deleteRule: '@request.auth.role = "admin"'
};
```

**Rule development workflow:**

1. **Start locked** - All rules `null`
2. **Identify access needs** - Who needs what access?
3. **Write minimal rules** - Open only required operations
4. **Test thoroughly** - Verify both allowed and denied cases
5. **Document decisions** - Comment why rules are set as they are

**Security checklist:**
- [ ] No empty string rules without justification
- [ ] Ownership checks on personal data
- [ ] Auth checks on write operations
- [ ] Admin-only rules for sensitive operations
- [ ] Tested with different user contexts

Reference: [PocketBase API Rules](https://pocketbase.io/docs/api-rules-and-filters/)

## 5. Use @request Context in API Rules

**Impact: CRITICAL (Enables dynamic, user-aware access control)**

The `@request` object provides access to the current request context including authenticated user, request body, query parameters, and headers. Use it to build dynamic access rules.

**Incorrect (hardcoded or missing auth checks):**

```javascript
// No authentication check
const collection = {
  listRule: '',  // Anyone can see everything
  createRule: ''  // Anyone can create
};

// Hardcoded user ID (never do this)
const collection = {
  listRule: 'owner = "specific_user_id"'  // Only one user can access
};
```

**Correct (using @request context):**

```javascript
// Check if user is authenticated
createRule: '@request.auth.id != ""'

// Check ownership via auth record
listRule: 'owner = @request.auth.id'
viewRule: 'owner = @request.auth.id'
updateRule: 'owner = @request.auth.id'
deleteRule: 'owner = @request.auth.id'

// Access auth record fields
// IMPORTANT: If using custom role fields, ensure update rules prevent
// users from modifying their own role: @request.body.role:isset = false
listRule: '@request.auth.role = "admin"'
listRule: '@request.auth.verified = true'

// Validate request body on create/update
createRule: '@request.auth.id != "" && @request.body.owner = @request.auth.id'

// Prevent changing certain fields
updateRule: 'owner = @request.auth.id && @request.body.owner:isset = false'

// WARNING: Query parameters are user-controlled and should NOT be used
// for authorization decisions. Use them only for optional filtering behavior
// where the fallback is equally safe.
// listRule: '@request.query.publicOnly = "true" || owner = @request.auth.id'
// The above is UNSAFE - users can bypass ownership by adding ?publicOnly=true
// Instead, use separate endpoints or server-side logic for public vs. private views.
listRule: 'owner = @request.auth.id || public = true'  // Use a record field, not query param

// Access nested auth relations
listRule: 'team.members ?= @request.auth.id'
```

**Available @request fields:**

| Field | Description |
|-------|-------------|
| `@request.auth.id` | Authenticated user's ID (empty string if not authenticated) |
| `@request.auth.*` | Any field from auth record (role, verified, email, etc.) |
| `@request.body.*` | Request body fields (create/update only) |
| `@request.query.*` | URL query parameters |
| `@request.headers.*` | Request headers |
| `@request.method` | HTTP method (GET, POST, etc.) |
| `@request.context` | Request context: `default`, `oauth2`, `otp`, `password`, `realtime`, `protectedFile` |

**Body field modifiers:**

```javascript
// Check if field is being set
updateRule: '@request.body.status:isset = false'  // Can't change status

// Check if field changed from current value
updateRule: '@request.body.owner:changed = false'  // Can't change owner

// Get length of array/string
createRule: '@request.body.tags:length <= 5'  // Max 5 tags
```

Reference: [PocketBase API Rules](https://pocketbase.io/docs/api-rules-and-filters/#available-fields)

## 6. Use strftime() for Date Arithmetic in Filter Expressions

**Impact: MEDIUM (strftime() (added in v0.36) replaces brittle string prefix comparisons on datetime fields)**

PocketBase v0.36 added the `strftime()` function to the filter expression grammar. It maps directly to SQLite's [strftime](https://sqlite.org/lang_datefunc.html) and is the correct way to bucket, compare, or extract parts of a datetime field. Before v0.36 people worked around this with `~` (substring) matches against the ISO string; those workarounds are fragile (they break at midnight UTC, ignore timezones, and can't handle ranges).

**Incorrect (substring match on the ISO datetime string):**

```javascript
// ❌ "matches anything whose ISO string contains 2026-04-08" - breaks as soon
//    as your DB stores sub-second precision or you cross a month boundary
const todayPrefix = new Date().toISOString().slice(0, 10);
const results = await pb.collection("orders").getList(1, 50, {
    filter: `created ~ "${todayPrefix}"`, // ❌
});
```

**Correct (strftime with named format specifiers):**

```javascript
// "all orders created today (UTC)"
const results = await pb.collection("orders").getList(1, 50, {
    filter: `strftime('%Y-%m-%d', created) = strftime('%Y-%m-%d', @now)`,
});

// "all orders from March 2026"
await pb.collection("orders").getList(1, 50, {
    filter: `strftime('%Y-%m', created) = "2026-03"`,
});

// "orders created this hour"
await pb.collection("orders").getList(1, 50, {
    filter: `strftime('%Y-%m-%d %H', created) = strftime('%Y-%m-%d %H', @now)`,
});
```

```javascript
// Same function is available inside API rules:
//   collection "orders" - List rule:
//      @request.auth.id != "" &&
//      user = @request.auth.id &&
//      strftime('%Y-%m-%d', created) = strftime('%Y-%m-%d', @now)
```

**Common format specifiers:**

| Specifier | Meaning |
|---|---|
| `%Y` | 4-digit year |
| `%m` | month (01-12) |
| `%d` | day of month (01-31) |
| `%H` | hour (00-23) |
| `%M` | minute (00-59) |
| `%S` | second (00-59) |
| `%W` | ISO week (00-53) |
| `%j` | day of year (001-366) |
| `%w` | day of week (0=Sunday) |

**Other filter functions worth knowing:**

| Function | Use |
|---|---|
| `strftime(fmt, datetime)` | Format/extract datetime parts (v0.36+) |
| `length(field)` | Count elements in a multi-value field (file, relation, select) |
| `each(field, expr)` | Iterate over multi-value fields: `each(tags, ? ~ "urgent")` |
| `issetIf(field, val)` | Conditional presence check used in complex rules |

Reference: [Filter Syntax - Functions](https://pocketbase.io/docs/api-rules-and-filters/#filters) · [v0.36.0 release](https://github.com/pocketbase/pocketbase/releases/tag/v0.36.0)

