# Unsplash Skill - Usage Examples

Detailed examples for common use cases.

## Table of Contents

- [Basic Search](#basic-search)
- [Advanced Search with Filters](#advanced-search-with-filters)
- [Random Photos](#random-photos)
- [Pagination](#pagination)
- [Download Tracking](#download-tracking)
- [Attribution Examples](#attribution-examples)
- [Complete Workflows](#complete-workflows)
- [Error Handling](#error-handling)

## Basic Search

### Simple Keyword Search

```bash
./scripts/search.sh "sunset"
```

Returns 10 sunset photos with full metadata and attribution.

### Multi-word Search

```bash
./scripts/search.sh "mountain landscape"
```

Searches for photos matching both "mountain" and "landscape".

### Specific Count

```bash
./scripts/search.sh "coffee" 1 5
```

Returns 5 coffee-related photos (page 1, 5 results per page).

## Advanced Search with Filters

### Landscape Orientation Only

```bash
./scripts/search.sh "nature" 1 10 relevant landscape
```

Returns 10 landscape-oriented nature photos.

### Portrait Photos

```bash
./scripts/search.sh "portrait photography" 1 8 relevant portrait
```

### Filter by Color

```bash
# Black and white photos
./scripts/search.sh "architecture" 1 5 relevant "" black_and_white

# Blue-toned photos
./scripts/search.sh "ocean" 1 5 relevant landscape blue

# Red-toned photos
./scripts/search.sh "flower" 1 5 relevant "" red
```

### Latest Photos

```bash
./scripts/search.sh "technology" 1 10 latest
```

Sort by newest uploads instead of relevance.

## Random Photos

### Single Random Photo

```bash
./scripts/random.sh
```

Returns one completely random photo from Unsplash.

### Random by Topic

```bash
./scripts/random.sh "nature"
```

Returns one random nature-related photo.

### Multiple Random Photos

```bash
./scripts/random.sh "architecture" 5
```

Returns 5 random architecture photos (great for galleries).

### Random with Orientation

```bash
./scripts/random.sh "travel" 10 landscape
```

Returns 10 random landscape-oriented travel photos.

## Pagination

### First Page

```bash
./scripts/search.sh "workspace" 1 10
```

### Second Page

```bash
./scripts/search.sh "workspace" 2 10
```

### Custom Page Size

```bash
./scripts/search.sh "workspace" 1 20
```

Returns 20 results per page (max: 30).

## Download Tracking

### Basic Tracking

```bash
# 1. Search for a photo
result=$(./scripts/search.sh "sunset" 1 1)

# 2. Extract photo ID
photo_id=$(echo "$result" | jq -r '.id')

# 3. User decides to download
# 4. Track the download
download_url=$(./scripts/track.sh "$photo_id")

echo "Download URL: $download_url"
```

### Only Track Actual Downloads

```bash
# DON'T track when just displaying
./scripts/search.sh "coffee"
# Show images to user

# ONLY track when user actually downloads
# User clicks "Download" button
./scripts/track.sh "$photo_id"
```

## Attribution Examples

### Plain Text Attribution

```bash
result=$(./scripts/search.sh "mountain" 1 1)
echo "$result" | jq -r '.attribution_text'
```

Output:
```
Photo by John Doe on Unsplash
```

Place this near the image in blog posts, documents, or captions.

### HTML Attribution

```bash
result=$(./scripts/search.sh "coffee" 1 1)
echo "$result" | jq -r '.attribution_html'
```

Output:
```html
Photo by <a href="https://unsplash.com/@johndoe?utm_source=claude_skill&utm_medium=referral">John Doe</a> on <a href="https://unsplash.com/?utm_source=claude_skill&utm_medium=referral">Unsplash</a>
```

Use this in HTML content, websites, or web applications.

### Complete Photo Card (HTML)

```bash
result=$(./scripts/search.sh "workspace" 1 1)
photo_url=$(echo "$result" | jq -r '.urls.regular')
attribution=$(echo "$result" | jq -r '.attribution_html')

cat << EOF
<figure>
  <img src="$photo_url" alt="Workspace photo">
  <figcaption>$attribution</figcaption>
</figure>
EOF
```

## Complete Workflows

### Blog Post Hero Image Selection

```bash
#!/bin/bash

# Search for relevant images
echo "Searching for blog post images..."
results=$(./scripts/search.sh "technology coding" 1 5 latest landscape)

# Display options
echo "$results" | jq -c '.' | while read -r photo; do
    id=$(echo "$photo" | jq -r '.id')
    desc=$(echo "$photo" | jq -r '.alt_description')
    photographer=$(echo "$photo" | jq -r '.photographer_name')
    url=$(echo "$photo" | jq -r '.urls.small')

    echo "ID: $id"
    echo "Description: $desc"
    echo "Photographer: $photographer"
    echo "Preview: $url"
    echo "---"
done

# User selects photo ID
selected_id="abc123xyz"

# Extract full details
selected=$(echo "$results" | jq -c ". | select(.id == \"$selected_id\")")
image_url=$(echo "$selected" | jq -r '.urls.regular')
attribution=$(echo "$selected" | jq -r '.attribution_html')

echo "Using image: $image_url"
echo "Attribution: $attribution"
```

### Gallery of Random Images

```bash
#!/bin/bash

# Get variety of travel images
echo "Creating travel photo gallery..."
photos=$(./scripts/random.sh "travel" 12 landscape)

# Generate HTML gallery
cat << 'HTML_START'
<!DOCTYPE html>
<html>
<head>
    <title>Travel Photo Gallery</title>
    <style>
        .gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .photo { text-align: center; }
        .photo img { width: 100%; height: auto; }
        .attribution { font-size: 12px; margin-top: 8px; }
    </style>
</head>
<body>
    <div class="gallery">
HTML_START

echo "$photos" | jq -c '.' | while read -r photo; do
    url=$(echo "$photo" | jq -r '.urls.regular')
    alt=$(echo "$photo" | jq -r '.alt_description')
    attribution=$(echo "$photo" | jq -r '.attribution_html')

    cat << EOF
        <div class="photo">
            <img src="$url" alt="$alt">
            <div class="attribution">$attribution</div>
        </div>
EOF
done

cat << 'HTML_END'
    </div>
</body>
</html>
HTML_END
```

### Brand Color Matching

```bash
#!/bin/bash

# Search for images matching brand colors
brand_color="blue"
echo "Finding images with $brand_color tones..."

results=$(./scripts/search.sh "abstract background" 1 10 relevant "" "$brand_color")

echo "$results" | jq -c '.' | while read -r photo; do
    id=$(echo "$photo" | jq -r '.id')
    color=$(echo "$photo" | jq -r '.color')
    url=$(echo "$photo" | jq -r '.urls.small')

    echo "ID: $id | Color: $color | Preview: $url"
done
```

### Social Media Content

```bash
#!/bin/bash

# Get square/squarish photos for Instagram
echo "Finding Instagram-ready photos..."
photos=$(./scripts/random.sh "lifestyle" 9 squarish)

# Save each photo's details
echo "$photos" | jq -c '.' | while read -r photo; do
    id=$(echo "$photo" | jq -r '.id')
    url=$(echo "$photo" | jq -r '.urls.regular')
    attribution=$(echo "$photo" | jq -r '.attribution_text')

    echo "Photo ID: $id"
    echo "URL: $url"
    echo "Caption: $attribution"
    echo "---"
done
```

## Error Handling

### Check API Key Before Running

```bash
#!/bin/bash

if [ -z "$UNSPLASH_ACCESS_KEY" ]; then
    echo "ERROR: Please set UNSPLASH_ACCESS_KEY"
    echo "export UNSPLASH_ACCESS_KEY='your_key_here'"
    exit 1
fi

# Proceed with search
./scripts/search.sh "nature"
```

### Handle Empty Results

```bash
#!/bin/bash

results=$(./scripts/search.sh "veryrareuncommonphrase12345")

if [ "$results" == "[]" ]; then
    echo "No photos found. Try a different search term."
    exit 0
fi

echo "Found photos!"
echo "$results" | jq -r '.[] | .id'
```

### Handle API Errors

```bash
#!/bin/bash

# Capture both stdout and stderr
output=$(./scripts/search.sh "nature" 2>&1)
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "Search failed!"
    echo "$output"
    exit 1
fi

echo "Search successful!"
echo "$output"
```

### Rate Limit Handling

```bash
#!/bin/bash

search_with_retry() {
    local query="$1"
    local max_retries=3
    local retry=0

    while [ $retry -lt $max_retries ]; do
        output=$(./scripts/search.sh "$query" 2>&1)
        exit_code=$?

        if [ $exit_code -eq 0 ]; then
            echo "$output"
            return 0
        fi

        if echo "$output" | grep -q "Rate limit exceeded"; then
            retry=$((retry + 1))
            echo "Rate limited. Waiting 60 seconds... (Retry $retry/$max_retries)" >&2
            sleep 60
        else
            echo "$output" >&2
            return $exit_code
        fi
    done

    echo "Failed after $max_retries retries" >&2
    return 1
}

# Use with retry
results=$(search_with_retry "sunset")
```

## Processing Output

### Extract Specific Fields

```bash
# Get just the image URLs
./scripts/search.sh "coffee" | jq -r '.urls.regular'

# Get photographer names
./scripts/search.sh "nature" | jq -r '.photographer_name'

# Get photo IDs
./scripts/search.sh "workspace" | jq -r '.id'
```

### Filter by Dimensions

```bash
# Find photos wider than 4000px
./scripts/search.sh "landscape" 1 20 | jq 'select(.width > 4000)'

# Find square-ish photos (aspect ratio close to 1:1)
./scripts/search.sh "minimal" 1 20 | jq 'select((.width / .height) > 0.9 and (.width / .height) < 1.1)'
```

### Save to JSON File

```bash
# Save search results
./scripts/search.sh "mountain" 1 20 > mountains.json

# Save random photos
./scripts/random.sh "nature" 10 > nature_random.json

# Append to existing file
./scripts/search.sh "sunset" >> all_photos.json
```

## Testing Setup

### Test with Your API Key

```bash
# Set your API key
export UNSPLASH_ACCESS_KEY="your_key_here"

# Run test search
./scripts/search.sh "test" 1 1

# Check if it works
if [ $? -eq 0 ]; then
    echo "✓ Setup successful!"
else
    echo "✗ Setup failed"
fi
```

### Verify Attribution Format

```bash
# Check that attribution is included
result=$(./scripts/search.sh "test" 1 1)

if echo "$result" | jq -e '.attribution_text' > /dev/null; then
    echo "✓ Attribution text present"
else
    echo "✗ Attribution text missing"
fi

if echo "$result" | jq -e '.attribution_html' > /dev/null; then
    echo "✓ Attribution HTML present"
else
    echo "✗ Attribution HTML missing"
fi
```

## Performance Tips

### Cache Search Results

```bash
#!/bin/bash

cache_dir="$HOME/.cache/unsplash"
mkdir -p "$cache_dir"

search_cached() {
    local query="$1"
    local cache_key=$(echo "$query" | md5)
    local cache_file="$cache_dir/$cache_key.json"

    # Check if cached and less than 1 hour old
    if [ -f "$cache_file" ]; then
        if [ $(($(date +%s) - $(stat -f %m "$cache_file"))) -lt 3600 ]; then
            cat "$cache_file"
            return 0
        fi
    fi

    # Fetch fresh results
    results=$(./scripts/search.sh "$query")
    echo "$results" | tee "$cache_file"
}

# Use cached search
search_cached "nature"
```

### Batch Processing

```bash
#!/bin/bash

# Process multiple search terms efficiently
search_terms=("nature" "technology" "food" "travel" "architecture")

for term in "${search_terms[@]}"; do
    echo "Searching: $term"
    ./scripts/search.sh "$term" 1 5 > "${term}_results.json"
    sleep 1  # Rate limit protection
done

echo "All searches complete!"
```

## Advanced Filtering

### Combine Search with jq Filtering

```bash
# Search and filter for specific colors
./scripts/search.sh "abstract" 1 20 | \
    jq 'select(.color | test("#[0-9a-f]{2}[0-9a-f]{2}ff"; "i"))'  # Blue-ish colors

# Filter by photographer
./scripts/search.sh "landscape" 1 20 | \
    jq 'select(.photographer_username == "johndoe")'

# Filter by description keyword
./scripts/search.sh "animal" 1 20 | \
    jq 'select(.alt_description | contains("cat"))'
```

## Integration Examples

### Markdown Document Generation

```bash
#!/bin/bash

query="workspace"
output_file="workspace-images.md"

cat > "$output_file" << EOF
# Workspace Inspiration

Beautiful workspace photos from Unsplash.

EOF

./scripts/search.sh "$query" 1 5 | jq -c '.' | while read -r photo; do
    desc=$(echo "$photo" | jq -r '.alt_description')
    url=$(echo "$photo" | jq -r '.urls.regular')
    attribution=$(echo "$photo" | jq -r '.attribution_text')

    cat >> "$output_file" << EOF
## $desc

![${desc}](${url})

*${attribution}*

---

EOF
done

echo "Generated: $output_file"
```

This examples file provides practical, copy-paste-ready code for common scenarios.
