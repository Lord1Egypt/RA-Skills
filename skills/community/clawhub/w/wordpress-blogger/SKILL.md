---
name: wordpress-blogger
description: >
  Publish articles to WordPress blogs via REST API. Handles post creation, category/tag management,
  and SEO-friendly English slug generation. Use when user asks to publish blog posts, create WordPress
  articles, or post content to their blog. TRIGGER this skill whenever user mentions publishing to
  blog, WordPress posting, or creating articles on their WordPress site.
license: MIT
allowed-tools: Bash
---

# WordPress Blog Publisher

Publish articles to WordPress blogs safely with automatic category/tag management and English URL slugs.

---

## Prerequisites

WordPress credentials must be configured in the workspace `.env` file:

```bash
# WordPress Blog Credentials
WP_BLOG_URL="https://blog.example.com"      # Blog base URL (no trailing slash)
WP_USERNAME="your_username"                  # WordPress admin username
WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx"   # Application password
```

**How to create an Application Password:**
1. Log in to WordPress admin dashboard
2. Go to Users → Profile
3. Scroll to "Application Passwords" section
4. Click "Add New Application Password"
5. Copy the generated password

---

## Step 1 — Read Credentials

Read credentials from workspace `.env`:

```bash
# Load credentials from .env file
source /root/.openclaw/workspace/.env

WP_URL="${WP_BLOG_URL:-https://blog.example.com}"
WP_USER="${WP_USERNAME:-admin}"
WP_PASS="${WP_APP_PASSWORD}"

# Verify credentials exist
if [ -z "$WP_PASS" ]; then
  echo "❌ Error: WP_APP_PASSWORD not found in .env file"
  exit 1
fi
```

---

## Step 2 — Analyze Content & Generate Metadata

Before publishing, analyze the article content to generate appropriate metadata:

### Generate English Slug

Create a URL-friendly English slug from the article title or content:

- Use lowercase with hyphens as separators
- Keep it under 50 characters when possible
- Include main keywords
- Remove stop words (a, an, the, and, or, etc.)

**Examples:**
- "AMD Ryzen 9 7950X vs Intel Core i9-13900K: A Detailed Benchmark Comparison" → `ryzen-7950x-vs-i9-13900k-benchmark-comparison`
- "How to Optimize Database Performance in Production" → `optimize-database-performance-production`
- "Understanding Container Orchestration with Kubernetes" → `understanding-container-orchestration-kubernetes`

### Suggest Categories & Tags

Based on article content, suggest appropriate WordPress categories and tags:

| Content Type | Suggested Categories | Suggested Tags |
|-------------|---------------------|----------------|
| Hardware reviews | Hardware, Reviews | CPU, benchmark, performance, AMD, Intel |
| Software development | Development, Programming | coding, best-practices, architecture |
| AI/LLM related | AI, Technology | machine-learning, LLM, artificial-intelligence |
| Career development | Career | career-growth, soft-skills, productivity |
| DevOps/Infrastructure | DevOps, Infrastructure | docker, kubernetes, ci-cd, cloud |

If user doesn't specify, use these reasonable defaults:
- **Category**: Based on content topic (create if not exists)
- **Tags**: Extract 2-4 keywords from content

---

## Step 3 — Create Category (if needed)

Check if category exists, create if not:

```bash
CATEGORY_NAME="Hardware"  # Use suggested or user-specified category

# Try to find existing category
CAT_ID=$(curl -s "${WP_URL}/wp-json/wp/v2/categories?search=${CATEGORY_NAME}&per_page=1" \
  -u "${WP_USER}:${WP_PASS}" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)

# Create if not exists
if [ -z "$CAT_ID" ]; then
  CAT_RESULT=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/categories" \
    -u "${WP_USER}:${WP_PASS}" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"${CATEGORY_NAME}\"}")
  CAT_ID=$(echo "$CAT_RESULT" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
fi

echo "Category ID: $CAT_ID"
```

---

## Step 4 — Create Tags (if needed)

For each tag, check existence and create if needed:

```bash
TAGS=("CPU" "Benchmark" "AMD" "Performance")  # Use suggested or user-specified tags
TAG_IDS=""

for TAG in "${TAGS[@]}"; do
  # Try to find existing tag
  TID=$(curl -s "${WP_URL}/wp-json/wp/v2/tags?search=${TAG}&per_page=1" \
    -u "${WP_USER}:${WP_PASS}" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
  
  # Create if not exists
  if [ -z "$TID" ]; then
    TAG_RESULT=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/tags" \
      -u "${WP_USER}:${WP_PASS}" \
      -H "Content-Type: application/json" \
      -d "{\"name\": \"${TAG}\"}")
    TID=$(echo "$TAG_RESULT" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
  fi
  
  TAG_IDS="${TAG_IDS},${TID}"
done

# Remove leading comma
TAG_IDS=$(echo "$TAG_IDS" | sed 's/^,//')
echo "Tag IDs: $TAG_IDS"
```

---

## Step 5 — Create or Update Post

### Create New Post

```bash
TITLE="AMD Ryzen 9 7950X vs Intel Core i9-13900K: A Detailed Benchmark Comparison"
CONTENT="<p>In this comprehensive benchmark analysis...</p>"  # Convert markdown to HTML
SLUG="ryzen-7950x-vs-i9-13900k-benchmark-comparison"
EXCERPT="We compare two flagship processors across gaming, productivity, and power efficiency."

# Create post
POST_RESULT=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/posts" \
  -u "${WP_USER}:${WP_PASS}" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"${TITLE}\",
    \"content\": \"${CONTENT}\",
    \"slug\": \"${SLUG}\",
    \"status\": \"publish\",
    \"categories\": [${CAT_ID}],
    \"tags\": [${TAG_IDS}],
    \"excerpt\": \"${EXCERPT}\"
  }")

POST_ID=$(echo "$POST_RESULT" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
echo "Created post ID: $POST_ID"
```

### Update Existing Post

If updating an existing post (e.g., adding categories/tags to a draft):

```bash
POST_ID="123"  # Existing post ID

UPDATE_RESULT=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/posts/${POST_ID}" \
  -u "${WP_USER}:${WP_PASS}" \
  -H "Content-Type: application/json" \
  -d "{
    \"categories\": [${CAT_ID}],
    \"tags\": [${TAG_IDS}],
    \"slug\": \"${SLUG}\"
  }")
```

---

## Step 6 — Generate Public URL

Construct the public viewing URL (not the API endpoint):

```bash
# WordPress permalink structure: /{slug}/
PUBLIC_URL="${WP_URL}/${SLUG}/"

# If slug not set, use post ID format
if [ -z "$SLUG" ]; then
  PUBLIC_URL="${WP_URL}/?p=${POST_ID}"
fi

echo "✅ Article published successfully!"
echo ""
echo "📄 Title: ${TITLE}"
echo "🔗 URL: ${PUBLIC_URL}"
echo "📁 Category: ${CATEGORY_NAME}"
echo "🏷️ Tags: ${TAGS[*]}"
```

---

## Content Conversion

### Markdown to HTML

WordPress content field requires HTML. Convert markdown:

| Markdown | HTML |
|----------|------|
| `# Title` | `<h1>Title</h1>` |
| `## Subtitle` | `<h2>Subtitle</h2>` |
| `### H3` | `<h3>H3</h3>` |
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `- list item` | `<ul><li>list item</li></ul>` |
| `1. item` | `<ol><li>item</li></ol>` |
| `[text](url)` | `<a href="url">text</a>` |
| `` `code` `` | `<code>code</code>` |
| ````code block```` | `<pre><code>code block</code></pre>` |

### Handling Special Characters

Escape double quotes in content when building JSON:

```bash
# Escape quotes for JSON
ESCAPED_CONTENT=$(echo "$CONTENT" | sed 's/"/\\"/g')
```

---

## Complete Workflow Example

```bash
#!/bin/bash

# Load credentials
source /root/.openclaw/workspace/.env
WP_URL="${WP_BLOG_URL:-https://blog.example.com}"
WP_USER="${WP_USERNAME:-admin}"
WP_PASS="${WP_APP_PASSWORD}"

# Article content - CPU Benchmark example
TITLE="AMD Ryzen 9 7950X vs Intel Core i9-13900K: A Detailed Benchmark Comparison"
SLUG="ryzen-7950x-vs-i9-13900k-benchmark-comparison"
CATEGORY="Hardware"
TAGS=("CPU" "Benchmark" "AMD" "Intel" "Performance")

CONTENT="<p>The battle for desktop CPU supremacy continues...</p><h2>Test Methodology</h2><p>All tests were conducted on identical platforms...</p>"

# Step 1: Create/Get Category
CAT_RESULT=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/categories" \
  -u "${WP_USER}:${WP_PASS}" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"${CATEGORY}\"}")
CAT_ID=$(echo "$CAT_RESULT" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)

# Step 2: Create/Get Tags
TAG_IDS=""
for TAG in "${TAGS[@]}"; do
  TAG_RESULT=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/tags" \
    -u "${WP_USER}:${WP_PASS}" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"${TAG}\"}")
  TID=$(echo "$TAG_RESULT" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
  TAG_IDS="${TAG_IDS},${TID}"
done
TAG_IDS=$(echo "$TAG_IDS" | sed 's/^,//')

# Step 3: Create Post
POST_RESULT=$(curl -s -X POST "${WP_URL}/wp-json/wp/v2/posts" \
  -u "${WP_USER}:${WP_PASS}" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"${TITLE}\",
    \"content\": \"${CONTENT}\",
    \"slug\": \"${SLUG}\",
    \"status\": \"publish\",
    \"categories\": [${CAT_ID}],
    \"tags\": [${TAG_IDS}]
  }")

POST_ID=$(echo "$POST_RESULT" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
PUBLIC_URL="${WP_URL}/${SLUG}/"

echo "✅ Published: ${PUBLIC_URL}"
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid credentials | Check username and app password |
| `403 Forbidden` | Insufficient permissions | Use admin account or check user capabilities |
| `rest_cannot_create` | Missing edit_posts capability | Verify user has publishing permissions |
| `term_exists` | Category/tag already exists | Fetch existing ID instead of creating |

### API Response Check

Always check API responses for errors:

```bash
if echo "$RESULT" | grep -q '"code":"'; then
  ERROR_CODE=$(echo "$RESULT" | grep -o '"code":"[^"]*"' | head -1)
  ERROR_MSG=$(echo "$RESULT" | grep -o '"message":"[^"]*"' | head -1)
  echo "❌ API Error: $ERROR_CODE - $ERROR_MSG"
  exit 1
fi
```

---

## Safety Rules

- ✅ Always generate English slug for SEO-friendly URLs
- ✅ Create reasonable category/tags if user doesn't specify
- ✅ Return public viewing URL, not API endpoint
- ✅ Escape content properly for JSON payload
- ✅ Verify credentials before attempting API calls
- ❌ Never hardcode credentials in scripts
- ❌ Never return API URLs (with /wp-json/) as the result

---

## Response Format

After successful publication, respond with:

```
✅ Article published successfully!

📄 Title: [Article Title]
🔗 URL: [Public Viewing URL]
📁 Category: [Category Name]
🏷️ Tags: [Tag List]
```
