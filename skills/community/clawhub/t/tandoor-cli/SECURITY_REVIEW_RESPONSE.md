# Response to OlawHub Security Review

This document summarizes the changes made to address security concerns raised in the OlawHub skill review.

## Review Date
May 4, 2026

## Summary of Changes

All security concerns have been addressed through documentation updates, explicit approval gates, and security best practices guidance.

---

## 1. Tool Misuse and Exploitation (HIGH SEVERITY)

### Original Concern
> The skill exposes destructive, bulk, and account-administration operations to the agent, but the instructions do not add explicit approval gates or limits for these high-impact actions.

### Resolution

**Files Modified:**
- `SKILL.md`
- `references/SETUP.md`

**Changes Made:**

1. **Command Classification System**
   - All commands now categorized by risk level:
     - Read operations (safe, no approval)
     - Write operations (require user confirmation)
     - Destructive operations (require explicit confirmation)
     - Administrative operations (require privileged token + explicit confirmation)

2. **Explicit Approval Gates**
   - Added "Approval Required" column to command tables
   - Documented specific confirmation messages for each destructive operation
   - Examples:
     - `delete <id>`: "This will permanently delete recipe X. Cannot be undone. Confirm?"
     - `shopping check --all`: "This will mark ALL shopping items as checked. Confirm?"
     - `household users assign`: "This will move user X to household Y. Confirm?"

3. **Agent Behavior Rules Section**
   - Clear instructions on when to proceed vs. when to ask
   - Explicit prohibition on using `--force` without user instruction
   - Requirement to explain impact before destructive operations

4. **Security Warning Banner**
   - Added prominent warning at top of SKILL.md
   - States: "This skill provides mutation authority over your Tandoor instance"
   - Directs users to only install if they want agent mutation authority

**User Impact:** Agents can no longer execute destructive operations without explicit user approval. Users maintain full control over high-impact actions.

---

## 2. Agentic Supply Chain Vulnerabilities (LOW SEVERITY)

### Original Concern
> The skill relies on an external npm package that is not included in the reviewed artifact set; npx may download and run package code on demand.

### Resolution

**Files Modified:**
- `SKILL.md`
- `SECURITY.md`

**Changes Made:**

1. **Version Awareness**
   - Documentation acknowledges the npm package dependency
   - Recommends version pinning for production use

2. **Verification Links**
   - Added direct links to npm package: https://www.npmjs.com/package/tandoor-cli
   - Added direct link to source repository: https://github.com/dcenatiempo/tandoor-cli
   - Included in "Before first use" checklist

3. **Pre-Installation Checklist**
   - Verify the npm package
   - Review the source code
   - Consider using a test instance first

4. **Supply Chain Security Section**
   - Added to SKILL.md under "Security & Permission Model"
   - Recommends reviewing package before use with privileged credentials
   - Suggests monitoring npm security advisories

**User Impact:** Users can verify the package source and pin to known-good versions before granting access to their Tandoor instance.

---

## 3. Identity and Privilege Abuse - Space Owner Token (HIGH SEVERITY)

### Original Concern
> The skill directs use of a highly privileged Tandoor identity for household invite management, which is broader than ordinary recipe and shopping-list management.

### Resolution

**Files Modified:**
- `SKILL.md`
- `SECURITY.md`
- `references/SETUP.md`

**Changes Made:**

1. **Least Privilege Principle**
   - Added "Token Security" section emphasizing least-privileged tokens
   - Guidance on token scoping:
     - Read-only tokens for queries
     - Standard user tokens for recipe management
     - Admin tokens only for household management
     - Space-owner tokens only for invite creation

2. **Command-Level Permission Documentation**
   - Each administrative command now states required permission level
   - Example: "household invite create" explicitly states "Space-owner token + explicit confirmation"

3. **Permission Error Guidance**
   - Users directed to contact administrators if lacking permissions
   - Clear explanation that 403 errors indicate insufficient privileges

4. **Token Scoping Examples**
   - SECURITY.md provides three token configuration examples:
     - Read-only (safest)
     - Recipe management (standard)
     - Administrative tasks (restricted)

**User Impact:** Users can create appropriately scoped tokens for their use case, avoiding over-privileged access.

---

## 4. Identity and Privilege Abuse - Long-Lived Tokens (MEDIUM SEVERITY)

### Original Concern
> The setup guide demonstrates creating a long-lived read/write OAuth2 access token, which would let the CLI perform both read and mutation operations for up to a year if not revoked.

### Resolution

**Files Modified:**
- `references/SETUP.md`
- `SECURITY.md`

**Changes Made:**

1. **Token Lifetime Recommendations**
   - Changed default example from 365 days (1 year) to 7-30 days
   - Added "Token Lifetime Recommendations" section:
     - AI agents / automation: 7-30 days
     - Personal CLI use: 30-90 days
     - Testing / development: 1-7 days
     - Administrative tasks: 1 day (revoke after use)

2. **Multiple Token Examples**
   - SETUP.md now provides separate examples for:
     - Read-only token (7 days, `scope='read'`)
     - Read-write token (30 days, `scope='read write'`)
   - Users choose appropriate example for their use case

3. **Token Security Best Practices**
   - Store tokens securely (environment variables, secret managers)
   - Never commit tokens to version control
   - Revoke tokens immediately if compromised
   - Rotate tokens regularly
   - Use read-only tokens when possible

4. **Token Management Commands**
   - SECURITY.md includes commands to:
     - List active tokens
     - Revoke unused tokens
     - Audit token usage

**User Impact:** Users create shorter-lived tokens appropriate for their use case, reducing exposure window if tokens are compromised.

---

## New Documentation

### SECURITY.md (New File)

Comprehensive security documentation covering:

1. **Overview of Security Model**
2. **Detailed Mitigation for Each Concern**
3. **Recommended Token Configurations**
   - Read-only, standard, and administrative examples
4. **Token Storage Best Practices**
   - Secure vs. insecure methods
5. **Monitoring and Auditing**
   - Commands to list and revoke tokens
   - Incident response procedures
6. **Agent-Specific Security**
   - Guidance for AI agent users
   - Agent behavior validation tests
7. **Compliance and Governance**
   - Organizational policies
   - Personal use guidelines
8. **Reporting Security Issues**

---

## Testing Recommendations

To verify the security improvements:

### 1. Test Agent Approval Gates

```bash
# Should prompt for confirmation, not execute immediately:
"Delete recipe 42"
"Clear all shopping items"
"Create a new household"

# Should proceed without confirmation:
"List all recipes"
"Search for pasta recipes"
```

### 2. Test Token Scoping

```bash
# Create a read-only token and verify write operations fail:
export TANDOOR_API_TOKEN=<read-only-token>
tandoor list  # Should work
tandoor add --json recipe.json  # Should fail with 403
```

### 3. Test Version Awareness

```bash
# Verify the CLI version:
tandoor --version
```

---

## Compliance Summary

| Concern | Severity | Status | Mitigation |
|---------|----------|--------|------------|
| Tool Misuse and Exploitation | HIGH | ✅ Resolved | Explicit approval gates, command classification, agent behavior rules |
| Agentic Supply Chain | LOW | ✅ Resolved | Verification links, pre-installation checklist, version awareness |
| Space Owner Token Privilege | HIGH | ✅ Resolved | Least privilege guidance, token scoping examples, permission documentation |
| Long-Lived Tokens | MEDIUM | ✅ Resolved | Shorter default lifetimes, token rotation guidance, security best practices |

---

## Recommendations for Users

### Before Installation

1. ✅ Read `SECURITY.md` to understand the security model
2. ✅ Verify the npm package at https://www.npmjs.com/package/tandoor-cli
3. ✅ Review the source code at https://github.com/dcenatiempo/tandoor-cli
4. ✅ Decide what level of access you want to grant the agent

### During Setup

1. ✅ Create a token with the minimum required permissions
2. ✅ Use short token lifetimes (7-30 days for agents)
3. ✅ Store tokens securely (environment variables, secret managers)
4. ✅ Test with a non-production Tandoor instance first

### After Installation

1. ✅ Monitor agent behavior for unexpected commands
2. ✅ Verify agents request approval for destructive operations
3. ✅ Rotate tokens regularly
4. ✅ Revoke tokens immediately if compromised

---

## Contact

For questions about these security improvements:
- Open an issue in the repository
- Tag issues with `[SECURITY]` for priority handling

For security vulnerabilities:
- Report privately via GitHub Security Advisories
- Do not disclose publicly until patched

---

## Version History

- **v0.4.0** (May 2026): Security improvements addressing OlawHub review
- **v0.3.0** (Earlier): Initial skill release
