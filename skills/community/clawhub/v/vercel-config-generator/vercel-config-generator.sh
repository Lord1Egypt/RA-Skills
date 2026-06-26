#!/bin/bash
TYPE="${1:-serverless}"

cat > vercel.json << 'JSON'
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": null,
  "functions": {
    "api/**/*.js": {
      "runtime": "nodejs18.x"
    }
  }
}
JSON

echo "✅ Vercel config generated!"
