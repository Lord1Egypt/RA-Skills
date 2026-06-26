#!/bin/bash

# SkillsMP Search - Search skills from SkillsMP marketplace

API_KEY="${SKILLSMP_API_KEY:-}"
LIMIT="${SKILLSMP_LIMIT:-10}"

if [ -z "$API_KEY" ]; then
  echo "Error: SKILLSMP_API_KEY not set"
  echo ""
  echo "Please set your API key:"
  echo "  export SKILLSMP_API_KEY=\"sk_live_xxxxxxxxxxxx\""
  exit 1
fi

QUERY="$1"

if [ -z "$QUERY" ]; then
  echo "Usage: skillsmp-search \"<关键词>\" [--limit N]"
  exit 1
fi

# Parse limit from arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --limit)
      LIMIT="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

# Call SkillsMP API
RESPONSE=$(curl -s -X GET "https://skillsmp.com/api/v1/skills/search?q=${QUERY}&limit=${LIMIT}" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json")

# Check if response is valid
if echo "$RESPONSE" | grep -q '"success":false'; then
  ERROR_MSG=$(echo "$RESPONSE" | grep -oP '"message":\s*"\K[^"]+' | head -1)
  echo "Error: $ERROR_MSG"
  exit 1
fi

# Parse and display results
echo "$RESPONSE" | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
except:
    print('Error: Invalid JSON response')
    sys.exit(1)

skills = data.get('data', {}).get('skills', [])
if not skills:
    print('No results found')
    sys.exit(0)

total = data.get('data', {}).get('pagination', {}).get('total', len(skills))

print('='*60)
print(f'找到 {total} 个 Skills (显示前 {len(skills)} 个):')
print('='*60)

for i, skill in enumerate(skills, 1):
    name = skill.get('name', 'N/A')
    description = skill.get('description', '')[:70]
    author = skill.get('author', 'N/A')
    stars = skill.get('stars', 0)
    url = skill.get('skillUrl', '')
    
    print(f'')
    print(f'{i}. {name}')
    print(f'   作者: {author}')
    print(f'   ⭐: {stars}')
    print(f'   描述: {description}...')
    print(f'   链接: {url}')

print('')
print('='*60)
" 2>/dev/null || echo "$RESPONSE"
