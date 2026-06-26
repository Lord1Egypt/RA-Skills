# TeraBox Troubleshooting

## Common Issues

### Login Failed

**Problem:** Browser opens after `terabox login` but authorization fails

**Solutions:**
1. Check network connection
2. Confirm TeraBox account is in good standing
3. Try clearing browser cache and retry
4. Use manual authorization code input mode

**Problem:** Callback server fails to start

**Solutions:**
1. Check if port 8787 is in use: `lsof -i :8787`
2. Change port and retry
3. Use manual input mode

---

### Token Expired

**Problem:** Commands report Token expired

**Solution:**
```bash
# Re-login
bash scripts/login.sh
```

---

### Path Errors

**Problem:** "Path outside sandbox" error

**Cause:** TeraBox OpenAPI applications can only access designated sandbox directory

**Solutions:**
- Ensure all paths are within sandbox directory
- Do not use `../` path traversal
- Use relative paths instead of absolute paths

---

### Upload Failed

**Problem:** Large file upload interrupted

**Solutions:**
1. Check network stability
2. Use `--progress` to monitor upload progress
3. Re-execute upload command (supports resume)

**Problem:** File already exists

**Solutions:**
- Delete or rename existing file first
- Or upload to a different path

---

### Share Link Invalid

**Problem:** Share link reported as invalid or expired

**Solutions:**
1. Confirm link format is correct
2. Confirm extraction code is correct
3. Contact sharer to verify link is still valid

---

### Share Download Issues

**Problem:** `share-download` fails with errno 112

**Cause:** Invalid signature or timestamp for share API

**Solutions:**
1. Retry the command
2. Make sure you're using the latest version of the tool
3. Check if the share link is still valid

**Problem:** File list is empty

**Cause:** May need extraction code or share has expired

**Solutions:**
1. Provide extraction code with `--pwd`
2. Check if share has expired with `share-info`

---

## Error Code Reference

| Error Code | Description | Solution |
|------------|-------------|----------|
| -3 | Password required | Provide extraction code with --pwd |
| -6 | Token expired | Re-login |
| -7 | Access denied | Check permissions |
| -8 | File already exists | Delete or rename |
| -9 | File not found | Check path |
| -10 | Path error | Check path format |
| 112 | Invalid sign/timestamp | Retry the operation |
| 100505 | API error | Use alternative API endpoint |

---

## Logging and Debugging

### View Configuration

```bash
cat ~/.config/terabox/config.json
```

### Check Login Status

```bash
terabox whoami
```

### JSON Output Debugging

```bash
terabox ls --json 2>&1 | jq .
```

### Check Share Status

```bash
# View share details
terabox share-info "https://terabox.com/s/1xxxxx"

# Check if files are accessible
terabox share-list "https://terabox.com/s/1xxxxx" --pwd abcd --json
```

---

## Getting Help

```bash
# View all commands
terabox --help

# View specific command help
terabox upload --help
terabox share-download --help
```
