# Security Audit Checklist

Checklist for evaluating skill security before recommendation.

## Pre-installation Checks

### Author Verification
- [ ] Author has verified identity on clawhub
- [ ] Author has published multiple skills
- [ ] No recent author name changes
- [ ] Author has public profile/contact

### Community Signals
- [ ] Skill has 10+ downloads
- [ ] No critical security issues reported
- [ ] Recent activity (issues/updates within 3 months)
- [ ] Positive rating trend (not declining)

## Code Analysis

### Network Activity
- [ ] No unexpected outbound network calls
- [ ] All API calls are documented
- [ ] No hardcoded API keys or credentials
- [ ] Uses environment variables for secrets

### File System Access
- [ ] Only accesses necessary directories
- [ ] No system-level file modifications
- [ ] No attempts to modify OpenClaw core files
- [ ] Respects workspace boundaries

### Execution Safety
- [ ] No eval() or exec() of untrusted input
- [ ] No shell injection vulnerabilities
- [ ] Input validation present
- [ ] Error handling doesn't leak sensitive info

### Permission Analysis
- [ ] Requested permissions match functionality
- [ ] No overly broad permissions (e.g., "all files")
- [ ] Network permissions justified
- [ ] No request for elevated privileges

## Red Flags (Auto-reject)

Any of these disqualifies a skill:

- Obfuscated or minified code without source
- Requests to disable security features
- Attempts to access credentials or tokens
- Network calls to undocumented endpoints
- File system access outside workspace
- Execution of downloaded code
- Requests for system-level permissions

## Yellow Flags (Manual Review)

These require extra scrutiny:

- New author with no history
- Sudden spike in permissions from previous version
- Network calls to personal/domains
- Binary dependencies without clear purpose
- Complex build processes

## Post-installation Monitoring

After installation, monitor for:

- Unexpected network activity
- File system changes outside expected paths
- Error messages revealing system info
- Performance anomalies

## Reporting Issues

If security issues are found:
1. Do not install/recommend the skill
2. Document the specific issue
3. Report to clawhub security team
4. Notify user of the risk
