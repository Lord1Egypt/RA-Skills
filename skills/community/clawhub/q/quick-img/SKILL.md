---
name: quick-img
description: "Generate images using curl and the SkillBoss API."
allowed-tools: Bash
metadata: {"clawdbot":{"requires":{"env":["SKILLBOSS_API_KEY"]},"primaryEnv":"SKILLBOSS_API_KEY"}}
---

# Quick Image Generator

Generate images from text prompts using curl.

## Generate

```bash
curl -s -X POST https://api.heybossai.com/v1/run \
  -H "Content-Type: application/json" \
  -d "{\"api_key\":\"$SKILLBOSS_API_KEY\",\"model\":\"mm/img\",\"inputs\":{\"prompt\":\"A sunset\"}}" \
  | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const j=JSON.parse(d);console.log(j.image_url||JSON.stringify(j))})"
```

## Check IP

```bash
node {baseDir}/scripts/hello.mjs
```

Notes:
- Get SKILLBOSS_API_KEY at https://www.skillboss.co
