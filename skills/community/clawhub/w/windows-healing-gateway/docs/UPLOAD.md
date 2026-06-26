# Upload Guide

## ClawHub Upload

### Step 1: Prepare Files

Ensure all files are in place:

```
windows-healing-gateway/
├── scripts/
│   ├── openclaw-fix.ps1
│   ├── openclaw-monitor.ps1
│   ├── openclaw-gateway-starter.ps1
│   ├── OpenClaw-Gateway-AutoStart.xml
│   ├── OpenClaw-Monitor-Service.xml
│   └── deploy-windows-healing.ps1
├── SKILL.md
├── skill.json
├── README.md
└── LICENSE
```

### Step 2: Upload to ClawHub

1. Visit https://clawhub.ai/upload
2. Drag and drop the `windows-healing-gateway` folder
3. Fill in the form:
   - **Slug**: `windows-healing-gateway`
   - **Display Name**: `Windows Healing Gateway`
   - **Version**: `1.0.0`
   - **Tags**: `windows, healing, gateway, monitoring, task-scheduler`
4. Check MIT-0 license agreement
5. Click **Publish**

### Step 3: Verify

After upload, install via:

```powershell
clawhub install windows-healing-gateway
```

## GitHub Upload

### Create Repository

1. Go to https://github.com/new
2. Repository name: `windows-healing-gateway`
3. Description: `OpenClaw Gateway self-healing system for Windows`
4. Make it Public
5. Click **Create repository**

### Push Code

```powershell
cd skills/windows-healing-gateway
git init
git add .
git commit -m "Initial commit: Windows Healing Gateway v1.0.0"
git remote add origin https://github.com/YOUR_USERNAME/windows-healing-gateway.git
git push -u origin main
```

### Create Release

1. Go to GitHub repository
2. Click **Releases** → **Create a new release**
3. Tag: `v1.0.0`
4. Title: `Windows Healing Gateway v1.0.0`
5. Description: Copy from README.md
6. Click **Publish release**

## Post-Upload

### Test Installation

```powershell
# Via ClawHub
clawhub install windows-healing-gateway

# Via GitHub
clawhub install https://github.com/YOUR_USERNAME/windows-healing-gateway
```

### Verify Deployment

```powershell
# Run deployment
python skills/windows-healing-gateway/scripts/deploy-windows-healing.ps1

# Check status
schtasks /Query /TN "OpenClaw\*" /FO LIST
```

## Troubleshooting

### Upload Fails

- Ensure SKILL.md exists
- Check skill.json is valid JSON
- Verify no sensitive data in scripts

### Installation Fails

- Check PowerShell execution policy
- Verify Windows version compatibility
- Ensure Task Scheduler access

## Support

- GitHub Issues: https://github.com/YOUR_USERNAME/windows-healing-gateway/issues
- ClawHub: https://clawhub.ai/skills/windows-healing-gateway
