# Security Guidelines for Tandoor CLI Skill

This document addresses security concerns and best practices for using the tandoor-cli skill with AI agents.

## Overview

The tandoor-cli skill provides programmatic access to your Tandoor Recipe Manager instance. Like any tool with write access to your data, it requires careful configuration and usage to maintain security.

## Addressed Security Concerns

### 1. Tool Misuse and Exploitation (HIGH SEVERITY)

**Concern:** The skill exposes destructive, bulk, and account-administration operations without explicit approval gates.

**Mitigation:**
- **Command Classification:** All commands are now classified by risk level (read, write, destructive, administrative)
- **Approval Gates:** The SKILL.md explicitly requires user confirmation before:
  - Any write operation (add, update, import)
  - Any destructive operation (delete, clear, bulk operations)
  - Any administrative operation (household management, user assignment)
- **Agent Behavior Rules:** Clear instructions prevent agents from executing high-risk commands without explicit user approval
- **No Automatic --force:** Agents are forbidden from using `--force` flags without explicit user instruction

**User Action Required:**
- Review the command classification table in SKILL.md
- Only install this skill if you want the agent to have mutation authority
- Monitor agent behavior and revoke access if misuse is detected

### 2. Agentic Supply Chain Vulnerabilities (LOW SEVERITY)

**Concern:** The skill relies on an external npm package that could be compromised.

**Mitigation:**
- **Version Pinning:** The skill explicitly uses `npx tandoor-cli@0.3.1` to pin to a known version
- **Verification Links:** SKILL.md provides direct links to:
  - npm package: https://www.npmjs.com/package/tandoor-cli
  - Source repository: https://github.com/dcenatiempo/tandoor-cli
- **Pre-Installation Checklist:** Users are instructed to verify the package before first use
- **No Auto-Updates:** Using `@version` syntax prevents automatic updates to potentially compromised versions

**User Action Required:**
- Verify the npm package and repository before first installation
- Review the package source code if using privileged credentials
- Monitor npm security advisories for the tandoor-cli package
- Update to newer versions only after reviewing changelogs

### 3. Identity and Privilege Abuse - Space Owner Token (HIGH SEVERITY)

**Concern:** The skill directs use of a highly privileged space-owner token for household invite management.

**Mitigation:**
- **Least Privilege Principle:** SKILL.md now emphasizes using the least-privileged token possible
- **Token Scoping Guidance:**
  - Read-only tokens for query operations
  - Standard user tokens for recipe management
  - Admin tokens only when household management is required
  - Space-owner tokens only for invite link creation
- **Explicit Warnings:** Administrative commands clearly state they require privileged tokens
- **Permission Errors:** Users are directed to contact administrators if they lack necessary permissions

**User Action Required:**
- Create separate tokens for different use cases
- Use read-only tokens when possible
- Avoid providing space-owner tokens unless invite management is truly needed
- Revoke privileged tokens immediately after administrative tasks

### 4. Identity and Privilege Abuse - Long-Lived Tokens (MEDIUM SEVERITY)

**Concern:** The setup guide demonstrates creating long-lived (10-year) read/write OAuth2 tokens.

**Mitigation:**
- **Token Lifetime Guidance:** SKILL.md now recommends short-lived tokens (days/weeks) instead of long-lived tokens (years)
- **Security Best Practices Section:** Added explicit guidance on:
  - Token rotation schedules
  - Secure token storage
  - Immediate revocation if compromised
  - Regular token audits
- **Alternative Approaches:** Users are encouraged to:
  - Generate tokens on-demand for specific tasks
  - Revoke tokens after use
  - Use environment-specific tokens (dev vs. production)

**User Action Required:**
- Modify the token generation command to use shorter expiry periods:
  ```python
  expires=timezone.now() + timedelta(days=7)  # 7 days instead of 3650
  ```
- Implement a token rotation schedule
- Store tokens securely (environment variables, secret managers, not in code)
- Revoke unused tokens regularly

## Recommended Token Configuration

### For Read-Only Use (Safest)

If you only need to query recipes, create a read-only token:

```python
token = AccessToken.objects.create(
    user=user,
    application=app,
    token=secrets.token_hex(20),
    expires=timezone.now() + timedelta(days=7),  # 7 days
    scope='read',  # Read-only
)
```

### For Recipe Management (Standard)

For adding/editing recipes but not administrative tasks:

```python
token = AccessToken.objects.create(
    user=user,
    application=app,
    token=secrets.token_hex(20),
    expires=timezone.now() + timedelta(days=30),  # 30 days
    scope='read write',
)
```

Use a standard user account (not admin/staff).

### For Administrative Tasks (Restricted)

Only when household management is required:

```python
token = AccessToken.objects.create(
    user=admin_user,  # Must be admin/staff
    application=app,
    token=secrets.token_hex(20),
    expires=timezone.now() + timedelta(days=1),  # 1 day
    scope='read write',
)
```

Revoke immediately after completing administrative tasks.

## Token Storage Best Practices

### ✅ Secure Methods

- **Environment variables:** `export TANDOOR_API_TOKEN=...` (session-only)
- **Secret managers:** AWS Secrets Manager, HashiCorp Vault, 1Password CLI
- **Encrypted config files:** `~/.config/tandoor-cli/config.json` with `0600` permissions
- **CI/CD secrets:** GitHub Secrets, GitLab CI/CD variables

### ❌ Insecure Methods

- **Plain text in code:** Never commit tokens to version control
- **Shared config files:** Avoid world-readable files
- **Chat logs:** Don't paste tokens in Slack, Discord, etc.
- **Browser history:** Be careful with tokens in URLs

## Monitoring and Auditing

### Regular Security Checks

1. **List active tokens:**
   ```python
   docker exec <container> /opt/recipes/venv/bin/python /opt/recipes/manage.py shell -c "
   from oauth2_provider.models import AccessToken
   from django.utils import timezone
   
   active = AccessToken.objects.filter(expires__gt=timezone.now())
   for token in active:
       print(f'{token.user.username}: {token.scope} (expires {token.expires})')
   "
   ```

2. **Revoke unused tokens:**
   ```python
   docker exec <container> /opt/recipes/venv/bin/python /opt/recipes/manage.py shell -c "
   from oauth2_provider.models import AccessToken
   
   # Revoke all tokens for tandoor-cli app
   AccessToken.objects.filter(application__name='tandoor-cli').delete()
   "
   ```

3. **Review Tandoor audit logs:** Check for unexpected API activity

### Incident Response

If a token is compromised:

1. **Immediately revoke the token** using the command above
2. **Review recent API activity** in Tandoor logs
3. **Generate a new token** with a different value
4. **Update all systems** using the old token
5. **Investigate** how the token was exposed

## Agent-Specific Security

### For AI Agent Users

When using this skill with AI agents (Kiro, Claude, etc.):

1. **Start with read-only tokens** to test agent behavior
2. **Monitor agent commands** before granting write access
3. **Use approval hooks** to review destructive operations
4. **Limit token scope** to the minimum required for the task
5. **Revoke tokens** when the agent task is complete

### Agent Behavior Validation

Test that your agent follows the security rules:

```bash
# This should prompt for confirmation, not execute immediately
"Delete recipe 42"

# This should refuse without explicit user approval
"Clear all shopping items"

# This should warn about privilege requirements
"Create a new household"
```

If your agent executes these without confirmation, the skill is not being used correctly.

## Compliance and Governance

### For Organizations

If deploying this skill in a team or organization:

- **Access Control:** Limit who can generate API tokens
- **Token Policies:** Enforce maximum token lifetimes
- **Audit Logging:** Enable and monitor Tandoor API logs
- **Incident Response:** Have a plan for token compromise
- **Training:** Ensure users understand the security model

### For Personal Use

Even for personal Tandoor instances:

- **Principle of Least Privilege:** Use the minimum permissions needed
- **Defense in Depth:** Don't rely solely on token security
- **Regular Reviews:** Audit tokens and agent behavior periodically
- **Backup Strategy:** Maintain backups in case of accidental deletion

## Reporting Security Issues

If you discover a security vulnerability in:

- **tandoor-cli package:** Report to https://github.com/dcenatiempo/tandoor-cli/security
- **Tandoor Recipe Manager:** Report to https://github.com/TandoorRecipes/recipes/security
- **This skill:** Open an issue at your repository with `[SECURITY]` prefix

Do not disclose security vulnerabilities publicly until they are patched.

## Version History

- **v0.4.0** (May 2026): Added comprehensive security documentation and approval gates
- **v0.3.0** (Earlier): Initial skill release

## Additional Resources

- [Tandoor Security Documentation](https://docs.tandoor.dev/security/)
- [OAuth2 Best Practices](https://oauth.net/2/oauth-best-practice/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Agent Skills Security Guidelines](https://agentskills.io/security)
