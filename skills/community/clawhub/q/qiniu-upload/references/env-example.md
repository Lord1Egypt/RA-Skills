# Qiniu environment variables

Required:

- `QINIU_ACCESS_KEY`
- `QINIU_SECRET_KEY`
- `QINIU_BUCKET`
- `QINIU_DOMAIN`

Optional:

- `QINIU_ZONE=z2`
- `QINIU_PRIVATE_BUCKET=false`
- `QINIU_PRIVATE_EXPIRE_SECONDS=3600`

Example PowerShell session:

```powershell
$env:QINIU_ACCESS_KEY = 'your-access-key'
$env:QINIU_SECRET_KEY = 'your-secret-key'
$env:QINIU_BUCKET = 'your-bucket'
$env:QINIU_DOMAIN = 'https://cdn.example.com'
$env:QINIU_ZONE = 'z2'
```
