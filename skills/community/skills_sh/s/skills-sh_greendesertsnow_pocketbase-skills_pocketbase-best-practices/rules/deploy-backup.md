---
title: Implement Proper Backup Strategies
impact: LOW-MEDIUM
impactDescription: Prevents data loss, enables disaster recovery
tags: production, backup, disaster-recovery, data-protection
---

## Implement Proper Backup Strategies

Regular backups are essential for production deployments. PocketBase provides built-in backup functionality and supports external S3 storage.

**Incorrect (no backup strategy):**

```javascript
// No backups at all - disaster waiting to happen
// Just running: ./pocketbase serve

// Manual file copy while server running - can corrupt data
// cp pb_data/data.db backup/

// Only backing up database, missing files
// sqlite3 pb_data/data.db ".backup backup.db"
```

**Correct (comprehensive backup strategy):**

```javascript
// 1. Using PocketBase Admin API for backups
const adminPb = new PocketBase('http://127.0.0.1:8090');
await adminPb.collection('_superusers').authWithPassword(admin, password);

// Create backup (includes database and files)
async function createBackup(name = '') {
  const backup = await adminPb.backups.create(name);
  console.log('Backup created:', backup.key);
  return backup;
}

// List available backups
async function listBackups() {
  const backups = await adminPb.backups.getFullList();
  backups.forEach(b => {
    console.log(`${b.key} - ${b.size} bytes - ${b.modified}`);
  });
  return backups;
}

// Download backup
async function downloadBackup(key) {
  const token = await adminPb.files.getToken();
  const url = adminPb.backups.getDownloadURL(token, key);
  // url can be used to download the backup file
  return url;
}

// Restore from backup (CAUTION: overwrites current data!)
async function restoreBackup(key) {
  await adminPb.backups.restore(key);
  console.log('Restore initiated - server will restart');
}

// Delete old backups
async function cleanupOldBackups(keepCount = 7) {
  const backups = await adminPb.backups.getFullList();

  // Sort by date, keep newest
  const sorted = backups.sort((a, b) =>
    new Date(b.modified) - new Date(a.modified)
  );

  const toDelete = sorted.slice(keepCount);
  for (const backup of toDelete) {
    await adminPb.backups.delete(backup.key);
    console.log('Deleted old backup:', backup.key);
  }
}
```

**Automated backup script (cron job):**

```bash
#!/bin/bash
# backup.sh - Run daily via cron

POCKETBASE_URL="http://127.0.0.1:8090"
ADMIN_EMAIL="admin@example.com"
ADMIN_PASSWORD="your-secure-password"
BACKUP_DIR="/path/to/backups"
KEEP_DAYS=7

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup via API
curl -X POST "${POCKETBASE_URL}/api/backups" \
  -H "Authorization: $(curl -s -X POST "${POCKETBASE_URL}/api/collections/_superusers/auth-with-password" \
    -d "identity=${ADMIN_EMAIL}&password=${ADMIN_PASSWORD}" | jq -r '.token')" \
  -d "name=backup_${TIMESTAMP}"

# Clean old local backups
find "${BACKUP_DIR}" -name "*.zip" -mtime +${KEEP_DAYS} -delete

echo "Backup completed: backup_${TIMESTAMP}"
```

**Configure S3 for backup storage:**

```javascript
// In Admin UI: Settings > Backups > S3
// Or via API:
await adminPb.settings.update({
  backups: {
    s3: {
      enabled: true,
      bucket: 'my-pocketbase-backups',
      region: 'us-east-1',
      endpoint: 's3.amazonaws.com',
      accessKey: process.env.AWS_ACCESS_KEY,
      secret: process.env.AWS_SECRET_KEY
    }
  }
});
```

**Backup best practices:**

| Aspect | Recommendation |
|--------|---------------|
| Frequency | Daily minimum, hourly for critical apps |
| Retention | 7-30 days of daily backups |
| Storage | Off-site (S3, separate server) |
| Testing | Monthly restore tests |
| Monitoring | Alert on backup failures |

**Pre-backup checklist:**
- [ ] S3 or external storage configured
- [ ] Automated schedule set up
- [ ] Retention policy defined
- [ ] Restore procedure documented
- [ ] Restore tested successfully

Reference: [PocketBase Backups](https://pocketbase.io/docs/going-to-production/#backups)
