---
title: Default to Locked Rules, Open Explicitly
impact: CRITICAL
impactDescription: Defense in depth, prevents accidental data exposure
tags: api-rules, security, defaults, best-practices
---

## Default to Locked Rules, Open Explicitly

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
