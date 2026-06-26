# Security Best Practices Reference

Comprehensive security guidance for development, deployment, and operations.

---

## Secure Development Lifecycle

### Design Phase
- Threat modeling for new features
- Security requirements defined
- Architecture review for sensitive data flows
- Privacy by design (data minimization)

### Implementation Phase
- Secure coding standards followed
- Code review includes security checks
- Static analysis (SAST) in CI/CD
- Dependency scanning enabled
- Unit tests include security cases

### Testing Phase
- Dynamic analysis (DAST) on staging
- Penetration testing before production
- Security regression tests
- Fuzzing for input parsers

### Deployment Phase
- Security hardening applied
- Secrets rotated on deploy
- Monitoring/alerting enabled
- Incident response plan ready

---

## Authentication Best Practices

### Password Policies
- Minimum length: 12 characters
- No complexity requirements (NIST guidance)
- Check against breached password lists
- Allow password managers (paste-friendly)
- No password hints or security questions

### Session Management
- Secure random session IDs
- Timeout: 30 minutes (sensitive apps)
- Absolute timeout: 8-12 hours
- Invalidate on password change
- HttpOnly + Secure + SameSite cookies

### MFA Implementation
- TOTP (RFC 6238) for time-based codes
- WebAuthn/FIDO2 for hardware keys
- Backup codes for recovery
- SMS only as last resort (SIM swapping risk)

---

## Authorization Best Practices

### RBAC (Role-Based Access Control)
```
Roles: admin, user, viewer
Permissions: create, read, update, delete
Assign permissions to roles, roles to users
```

### ABAC (Attribute-Based Access Control)
```
Policy: user.department == resource.department
Policy: user.level >= resource.classification
Policy: request.ip in allowed_ranges
```

### Principle of Least Privilege
- Default deny
- Grant minimum necessary access
- Time-limited permissions when possible
- Regular access reviews (quarterly)

---

## Data Protection

### Encryption at Rest
- Database: TDE or application-layer encryption
- Files: AES-256
- Backups: encrypted before storage
- Keys: HSM or cloud KMS

### Encryption in Transit
- TLS 1.3 preferred, 1.2 minimum
- Strong cipher suites (AEAD)
- Certificate validation (no self-signed in prod)
- HSTS enabled

### Data Classification
- Public: no restrictions
- Internal: employee access only
- Confidential: need-to-know, encrypted
- Restricted: highest protection, audit access

---

## Secure Configuration

### Server Hardening
```bash
# Disable unused services
systemctl disable --now <service>

# Remove unnecessary users
userdel <unused-account>

# Set secure umask
echo "umask 027" >> /etc/profile
```

### Network Security
- Firewall: deny-by-default inbound
- Security groups: minimal open ports
- NAT Gateway for outbound (hide internal IPs)
- WAF for web applications
- DDoS protection enabled

### Container Hardening
- Read-only root filesystem
- Drop capabilities: `--cap-drop=ALL`
- No privilege escalation: `--security-opt=no-new-privileges`
- User namespace remapping
- Seccomp profiles

---

## Monitoring & Detection

### Security Events to Log
- Authentication success/failure
- Authorization denials
- Privilege escalations
- Data exports (bulk downloads)
- Configuration changes
- Admin actions
- API rate limit hits

### Alerting Rules
- Multiple failed logins (5+ in 5 min)
- Privilege escalation attempts
- Unusual data access patterns
- Geographic anomalies (impossible travel)
- New admin account created
- Security group changes

### Log Management
- Centralized log aggregation
- Immutable log storage
- Retention: 90 days minimum
- Access restricted to security team
- Real-time search capability

---

## Vulnerability Management

### Scanning Schedule
- SAST: Every commit
- DAST: Weekly on staging
- Dependency scan: Daily
- Container scan: Every build
- Infrastructure scan: Monthly

### Prioritization (CVSS)
- Critical (9.0+): Patch within 24 hours
- High (7.0-8.9): Patch within 7 days
- Medium (4.0-6.9): Patch within 30 days
- Low (<4.0): Patch in next maintenance window

### Patching Process
1. Identify vulnerable systems
2. Test patch in staging
3. Schedule maintenance window
4. Deploy with rollback plan
5. Verify fix applied
6. Document in change log

---

## Incident Response

### Preparation
- Incident response plan documented
- Roles assigned (IC, comms, technical)
- Contact list maintained
- Tools ready (forensics, containment)
- Regular tabletop exercises

### Detection & Analysis
- Triage: Confirm incident is real
- Classification: Type, severity, scope
- Escalation: Notify stakeholders
- Documentation: Timeline, evidence

### Containment & Eradication
- Short-term: Stop the bleeding
- Long-term: Remove attacker access
- Evidence preservation: Forensics
- Root cause: How they got in

### Recovery
- Restore from clean backups
- Rotate all credentials
- Patch vulnerabilities
- Enhanced monitoring
- Gradual return to normal

### Post-Incident
- Post-mortem within 1 week
- Blameless review
- Action items assigned
- Process improvements
- Lessons learned documented

---

## Compliance Frameworks

### SOC 2
- Security, availability, confidentiality
- Access controls, encryption, monitoring
- Annual audit required

### GDPR
- Data subject rights (access, deletion)
- Consent management
- Data processing agreements
- Breach notification (72 hours)

### HIPAA
- PHI protection
- Access controls
- Audit trails
- Business associate agreements

### PCI-DSS
- Cardholder data protection
- Network segmentation
- Encryption requirements
- Quarterly scans

---

## Developer Security Training

### Required Topics
- OWASP Top 10
- Secure coding patterns
- Threat modeling basics
- Incident response roles
- Compliance requirements

### Frequency
- Onboarding: Security fundamentals
- Annual: Refresher training
- New threats: Ad-hoc updates
- Role-specific: Advanced topics

### Metrics
- Training completion rates
- Phishing test results
- Secure code review quality
- Vulnerability introduction rates

---

## Third-Party Risk Management

### Vendor Assessment
- Security questionnaire (SIG, CAIQ)
- SOC 2 report review
- Penetration test results
- Data processing agreement
- Incident notification SLA

### Ongoing Monitoring
- Annual reassessment
- Breach notifications
- Service level monitoring
- Contract compliance

### Integration Security
- API authentication required
- Rate limiting enforced
- Data minimization (only what's needed)
- Audit logging on integration points

---

*Use this reference for security strategy and implementation guidance.*
