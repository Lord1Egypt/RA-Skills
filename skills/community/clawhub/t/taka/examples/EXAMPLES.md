# Taka CLI Examples

## Quick Examples

### Generate an Image
```bash
taka generate-image --prompt "minimalist logo for a coffee brand"
```

### Generate with Aspect Ratio
```bash
taka generate-image --prompt "Instagram story background" --aspect-ratio 9:16
```

### Generate a Video
```bash
taka generate-video --prompt "ocean waves at sunset" --duration 7
```

### Create Instagram Post (One Command)
```bash
taka create-creative --name "Beach Day" --type instagram --prompt "tropical beach with crystal clear water"
```

## Script Examples

| Script | Description |
|--------|-------------|
| [instagram-post.sh](./instagram-post.sh) | Create an Instagram post with image and caption |
| [email-campaign.sh](./email-campaign.sh) | Build a complete email with hero image |
| [promotional-flyer.sh](./promotional-flyer.sh) | Create a promotional flyer with AI hero image |
| [video-reel.sh](./video-reel.sh) | Generate short videos for Reels/TikTok |

## Parsing Output with jq

All commands output JSON. Use `jq` to extract values:

```bash
# Get creative ID after creation
ID=$(taka create-creative --name "Test" --type instagram | jq -r '.creative.id')

# Get image URL after generation
URL=$(taka generate-image --prompt "test" | jq -r '.imageUrl')

# List creative names
taka list-creatives | jq '.[].name'
```

## Batch Operations

```bash
#!/bin/bash
# Generate multiple images with different prompts
PROMPTS=("sunrise over mountains" "city skyline at night" "forest path in autumn")

for prompt in "${PROMPTS[@]}"; do
  echo "Generating: $prompt"
  taka generate-image --prompt "$prompt" --aspect-ratio 1:1
done
```
