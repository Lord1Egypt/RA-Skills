# Image Pipeline

## Goal

Turn `imageMode` into an actual pre-publish asset workflow.

## Modes

### stock
- Generate search plan
- Pull watermark-free relevant stock images from allowed providers
- Send chosen images into publish assets directory

### cards-lite
- Generate lightweight visual assets with little or no text
- Use when stock images are not desired

### mixed
- Try stock images first
- If image quality/relevance is weak, fall back to cards-lite
- Publish from the final chosen asset directory

## Current scaffold outputs

- `stock-plan.json`
- `pipeline-plan.json`
- `cards-lite/` (fallback target)
- `publish-assets/` (final target)
