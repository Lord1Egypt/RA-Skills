---
title: Configure Production Settings Properly
impact: LOW-MEDIUM
impactDescription: Secure and optimized production environment
tags: production, configuration, security, environment
---

## Configure Production Settings Properly

Production deployments require proper configuration of URLs, secrets, SMTP, and security settings.

**Incorrect (development defaults in production):**

```bash
# Running with defaults - insecure!
./pocketbase serve

# Hardcoded secrets
./pocketbase serve --encryptionEnv="mySecretKey123"

# Wrong origin for CORS
# Leaving http://localhost:8090 as allowed origin
```

**Correct (production configuration):**

```bash
# Production startup with essential flags
./pocketbase serve \
  --http="0.0.0.0:8090" \
  --origins="https://myapp.com,https://www.myapp.com" \
  --encryptionEnv="PB_ENCRYPTION_KEY"

# Using environment variables
export PB_ENCRYPTION_KEY="your-32-char-encryption-key-here"
export SMTP_HOST="smtp.sendgrid.net"
export SMTP_PORT="587"
export SMTP_USER="apikey"
export SMTP_PASS="your-sendgrid-api-key"

./pocketbase serve --http="0.0.0.0:8090"
```

**Configure SMTP for emails:**

```javascript
// Via Admin UI or API
await adminPb.settings.update({
  smtp: {
    enabled: true,
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT),
    username: process.env.SMTP_USER,
    password: process.env.SMTP_PASS,
    tls: true
  },
  meta: {
    appName: 'My App',
    appURL: 'https://myapp.com',
    senderName: 'My App',
    senderAddress: 'noreply@myapp.com'
  }
});

// Test email configuration
await adminPb.settings.testEmail('users', 'test@example.com', 'verification');
```

**Configure S3 for file storage:**

```javascript
// Move file storage to S3 for scalability
await adminPb.settings.update({
  s3: {
    enabled: true,
    bucket: 'my-app-files',
    region: 'us-east-1',
    endpoint: 's3.amazonaws.com',
    accessKey: process.env.AWS_ACCESS_KEY,
    secret: process.env.AWS_SECRET_KEY,
    forcePathStyle: false
  }
});

// Test S3 connection
await adminPb.settings.testS3('storage');
```

**Systemd service file:**

```ini
# /etc/systemd/system/pocketbase.service
[Unit]
Description=PocketBase
After=network.target

[Service]
Type=simple
User=pocketbase
Group=pocketbase
LimitNOFILE=4096
Restart=always
RestartSec=5s
WorkingDirectory=/opt/pocketbase
ExecStart=/opt/pocketbase/pocketbase serve --http="127.0.0.1:8090"

# Environment variables
EnvironmentFile=/opt/pocketbase/.env

# Security hardening
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/opt/pocketbase/pb_data

[Install]
WantedBy=multi-user.target
```

**Environment file (.env):**

```bash
# /opt/pocketbase/.env
# SECURITY: Set restrictive permissions: chmod 600 /opt/pocketbase/.env
# SECURITY: Add to .gitignore - NEVER commit this file to version control
# For production, consider a secrets manager (Vault, AWS Secrets Manager, etc.)

PB_ENCRYPTION_KEY=  # Generate with: openssl rand -hex 16

# SMTP
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=           # Set your SMTP password here

# S3 (optional)
AWS_ACCESS_KEY=      # Set your AWS access key
AWS_SECRET_KEY=      # Set your AWS secret key

# OAuth (optional)
GOOGLE_CLIENT_ID=    # Set your Google client ID
GOOGLE_CLIENT_SECRET= # Set your Google client secret
```

**Protect your environment file:**

```bash
# Set restrictive permissions (owner read/write only)
chmod 600 /opt/pocketbase/.env
chown pocketbase:pocketbase /opt/pocketbase/.env

# Ensure .env is in .gitignore
echo ".env" >> .gitignore
```

**Production checklist:**

- [ ] HTTPS enabled (via reverse proxy)
- [ ] Strong encryption key set
- [ ] CORS origins configured
- [ ] SMTP configured and tested
- [ ] Superuser password changed
- [ ] S3 configured (for scalability)
- [ ] Backup schedule configured
- [ ] Rate limiting enabled (via reverse proxy)
- [ ] Logging configured

Reference: [PocketBase Going to Production](https://pocketbase.io/docs/going-to-production/)
