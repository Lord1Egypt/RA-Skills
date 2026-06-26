name: video-generator
description: AI video production workflow using Remotion. Use when creating videos, short films, commercials, motion graphics, product demos, social media videos, or any programmatic video content. Produces professional motion graphics using React + Remotion.
version: 1.0.0

# Video Generator (OpenClaw Skill)

This skill builds professional motion graphics videos using Remotion.

## Workflow

1. If product/company is mentioned → scrape brand using Firecrawl
2. Create project in output/<project-name>/
3. Build scenes using Remotion architecture
4. Install dependencies (npm install)
5. Run dev server (Remotion Studio)
6. Expose via Cloudflare tunnel
7. Share public URL
8. Iterate based on user feedback
9. Render only when explicitly requested

## Key Rules

- NEVER use emoji icons, always Lucide icons
- Avoid slideshow-style transitions
- Use motion graphics principles (overlap, spring physics, layered scenes)
- Use brand colors from scraped data
- Keep text minimal and cinematic

## Commands

- npm run dev → start studio
- npm run build → bundle project
- npx remotion render → export video

## Output Structure

output/<project-name>/
