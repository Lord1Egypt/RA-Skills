# OpenClaw Backup Skill

Automated encrypted backup and restore for OpenClaw Agent workspace files using Claude Code.

**NEW in v2.0.0**: Auto-generates a unique random password for each backup (never reuse passwords).

## Quick Start

### 1. Install Dependencies

```bash
# Install Python requests library
pip install requests

# Verify system tools (macOS/Linux usually have these built-in)
tar --version
openssl version
```

### 2. Install Skill

Copy this directory to Claude Code Skills directory:

```bash
# Copy to Claude Code Skills directory
cp -r openclaw-backup ~/.cursor/skills/

# Or create a symbolic link
ln -s /path/to/openclaw-backup ~/.cursor/skills/openclaw-backup
```

### 3. Use Skill

In Claude Code, use the following commands to trigger the skill:

```
# Backup workspace files
"Back up my workspace files"
"Upload SOUL.md to soul-upload"

# Restore backup
"Restore my last backup"
"Download backup <backup-id>"

# Delete backup
"Delete my backup"
"Remove backup <backup-id>"
```

## Features

✅ **AES-256-CBC Encryption** - Military-grade encryption using openssl
✅ **Auto-Generated Passwords** - Unique 32-char random password for each backup (v2.0.0)
✅ **Auto File Collection** - Default backup of SOUL.md, MEMORY.md, and other key files
✅ **Recovery Info Management** - Auto-save backup records to `.openclaw-backup-recovery.txt`
✅ **Error Handling** - Friendly error messages and recovery suggestions
✅ **Size Limit Check** - Auto-check 20MB file limit
✅ **Temp File Cleanup** - Auto-cleanup of sensitive temporary files

## Directory Structure

```
openclaw-backup/
├── README.md              # This file
├── SKILL.md               # Skill definition and workflow instructions
└── scripts/
    └── backup.py          # Python backup script (core logic)
```

## Manual Script Usage

You can also use the Python script directly (without Claude Code):

### Upload Backup

```bash
# Auto-generate password (recommended)
python3 scripts/backup.py upload \
  --files "SOUL.md MEMORY.md IDENTITY.md"

# Or specify custom password
python3 scripts/backup.py upload \
  --files "SOUL.md MEMORY.MD IDENTITY.md" \
  --password "your-custom-password"
```

Output example:
```json
{
  "backupId": "3f8a2b1c-1234-5678-90ab-cdef12345678",
  "downloadUrl": "https://soul-upload.com/backup/3f8a2b1c-...",
  "sizeBytes": 45678,
  "sha256": "abc123def456...",
  "password": "auto-generated-32-char-password"
}
```

### Download Backup

```bash
python3 scripts/backup.py download \
  --backup-id "3f8a2b1c-1234-5678-90ab-cdef12345678" \
  --password "password-from-recovery-file" \
  --output-dir "./restored"
```

Output example:
```json
{
  "success": true,
  "extractedFiles": ["SOUL.md", "MEMORY.md", "IDENTITY.md"],
  "outputDir": "/absolute/path/to/restored"
}
```

### Delete Backup

```bash
python3 scripts/backup.py delete \
  --backup-id "3f8a2b1c-1234-5678-90ab-cdef12345678"
```

Output example:
```json
{
  "success": true,
  "backupId": "3f8a2b1c-1234-5678-90ab-cdef12345678"
}
```

## Security Notes

⚠️ **Password Policy (v2.0.0)**
- Auto-generates unique 32-character random password for each backup
- Never reuse passwords across backups (per soul-upload.com policy)
- Password stored in `.openclaw-backup-recovery.txt` (CRITICAL for restoration)

⚠️ **Recovery File**
- `.openclaw-backup-recovery.txt` contains backup metadata INCLUDING password
- **CRITICAL**: Recovery file is the ONLY place password is stored
- Without recovery file, backup CANNOT be restored
- Recommendation: Back up recovery file to separate secure location
- Consider: Add to `.gitignore` if sensitive OR commit for team access

⚠️ **Encryption**
- Uses AES-256-CBC symmetric encryption
- openssl automatically adds salt for enhanced security
- Encryption done locally, only encrypted file uploaded

## File Size Limits

- **Maximum Backup Size**: 20 MB (compressed and encrypted)
- **Limit Handling**: Script auto-checks and prompts
- **Recommendation**: Remove large files (logs, caches) or split backup

## API Endpoints

This skill uses soul-upload.com Backup API:

| Endpoint | Method | Function |
|----------|--------|----------|
| `/backup` | POST | Upload encrypted backup |
| `/backup/:backupId` | GET | Download backup |
| `/backup/:backupId` | DELETE | Delete backup |

## Troubleshooting

### Missing Dependencies

```bash
# macOS
brew install openssl
pip3 install requests

# Ubuntu/Debian
sudo apt-get install tar openssl python3-pip
pip3 install requests
```

### Recovery File Lost

- Recovery file is CRITICAL - contains the only copy of password
- Without it, backup CANNOT be restored
- Always back up recovery file to separate secure location
- If lost, backup is permanently inaccessible

### Network Issues

- Check network connection
- Script default timeout is 5 minutes
- Can retry failed operations

## Development and Testing

### Run Tests

```bash
# Create test files
echo "Test SOUL content" > test-SOUL.md
echo "Test MEMORY content" > test-MEMORY.md

# Test upload (auto-generate password)
python3 scripts/backup.py upload \
  --files "test-SOUL.md test-MEMORY.md"

# Save returned backupId and password

# Test download
mkdir restored
python3 scripts/backup.py download \
  --backup-id "<your-backup-id>" \
  --password "<password-from-output>" \
  --output-dir "./restored"

# Verify files
diff test-SOUL.md restored/test-SOUL.md

# Test delete
python3 scripts/backup.py delete \
  --backup-id "<your-backup-id>"

# Cleanup test files
rm -rf test-*.md restored
```

### Code Structure

- `scripts/backup.py` - Core logic
  - `generate_password()` - Generate random password (NEW)
  - `upload_backup()` - Encrypt and upload
  - `download_backup()` - Download and decrypt
  - `delete_backup()` - Delete remote backup
  - `check_dependencies()` - Verify system dependencies

## Best Practices

1. **Regular Backups** - Weekly or after important changes
2. **Recovery File Management** - Keep `.openclaw-backup-recovery.txt` safe and backed up
3. **Verify Restoration** - Regularly test restoration process
4. **Clean Old Backups** - Delete unneeded old backups
5. **Multiple Copies** - Keep recovery file in multiple secure locations

## Contributing

Issues and Pull Requests welcome!

## License

MIT License

## Related Links

- [soul-upload.com](https://soul-upload.com)
- [Backup Guide](https://soul-upload.com/guides/how-to-backup-soul-md)
- [Restore Guide](https://soul-upload.com/guides/how-to-restore-soul-md)
- [Claude Code Documentation](https://claude.ai/claude-code)

---

**Version**: 2.0.0
**Last Updated**: 2025-02-15
**Password Policy**: Auto-generated unique password per backup (NEW in v2.0.0)
