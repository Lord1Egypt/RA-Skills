#!/bin/bash
# Serverless Template Generator

NAME="${1:-my-function}"
PLATFORM="${2:-vercel}"
LANGUAGE="${3:-js}"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

if [ -z "$NAME" ]; then
    echo "Usage: serverless-template-generator <name> [platform] [language]"
    exit 1
fi

echo -e "${BLUE}☁️ Generating Serverless template: $NAME${NC}"
echo "Platform: $PLATFORM"
echo ""

case "$PLATFORM" in
  vercel)
    mkdir -p "$PLATFORM"/api
    cat > "$PLATFORM/api/$NAME.js" << 'JS'
export default async function handler(req, res) {
  return res.json({
    message: 'Hello from Vercel!',
    platform: 'vercel',
    timestamp: new Date().toISOString()
  });
}
JS
    cat > "$PLATFORM/vercel.json" << 'JSON'
{
  "functions": {
    "api/*.js": {
      "runtime": "nodejs18.x"
    }
  }
}
JSON
    ;;

  netlify)
    mkdir -p "$PLATFORM"/netlify/functions
    cat > "$PLATFORM/netlify/functions/$NAME.js" << 'JS'
exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    body: JSON.stringify({
      message: 'Hello from Netlify!',
      platform: 'netlify'
    })
  };
};
JS
    cat > "$PLATFORM/netlify.toml" << 'TOML'
[build]
  command = ""
  functions = "netlify/functions"
TOML
    ;;

  cloudflare)
    mkdir -p "$PLATFORM"/src
    cat > "$PLATFORM/src/index.js" << 'JS'
export default {
  async fetch(request, env, ctx) {
    return new Response(JSON.stringify({
      message: 'Hello from Cloudflare Workers!',
      platform: 'cloudflare'
    }), {
      headers: { 'content-type': 'application/json' }
    });
  }
};
JS
    cat > "$PLATFORM/wrangler.toml" << 'TOML'
name = "WORKER_NAME"
main = "src/index.js"
compatibility_date = "2023-01-01"
TOML
    sed -i "s/WORKER_NAME/$NAME/g" "$PLATFORM/wrangler.toml"
    ;;
esac

# Generate package.json
cat > "$PLATFORM/package.json" << JSON
{
  "name": "$NAME-$PLATFORM",
  "version": "1.0.0",
  "scripts": {
    "dev": "$PLATFORM dev",
    "deploy": "$PLATFORM deploy --prod"
  }
}
JSON

# Generate README
cat > "$PLATFORM/README.md" << README
# $NAME

Serverless function for $PLATFORM

## Development

\`\`\`bash
# Install dependencies
npm install

# Local development
npm run dev

# Deploy
npm run deploy
\`\`\`

## Usage

\`\`\`javascript
// API call example
const response = await fetch('/api/$NAME');
const data = await response.json();
\`\`\`
README

echo -e "${GREEN}✅ Serverless template generated!${NC}"
echo "📁 Location: ./$PLATFORM"
echo ""
echo "Next steps:"
echo "1. cd $PLATFORM"
echo "2. npm install"
echo "3. npm run dev"
echo "4. npm run deploy"
