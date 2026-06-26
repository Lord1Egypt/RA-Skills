#!/bin/bash
PRESET="${1:-strict}"

cat > tsconfig.json << JSON
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": $([ "$PRESET" = "strict" ] && echo "true" || echo "false"),
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
JSON

echo "✅ TypeScript config generated: $PRESET"
