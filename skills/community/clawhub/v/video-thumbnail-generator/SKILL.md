---
name: video-thumbnail-generator
description: Generate thumbnail candidates from video frames so creators, ecommerce teams, and operators can choose cleaner covers for social, storefronts, and internal sharing. Use when a video needs a stronger preview image or cover frame.
---

# Video Thumbnail Generator

Turn video frames into usable thumbnail candidates.

## Problem it solves
A strong preview image often determines whether a video gets clicked, watched, or even noticed. But teams usually grab random frames manually. This skill helps extract and evaluate better thumbnail candidates from the video itself.

## Use when
- A social or product video needs a better cover image
- A team wants several frame options instead of one random grab
- A storefront, gallery, ad, or internal review asset needs a clearer preview
- The user wants a simple thumbnail workflow without full design work

## Do not use when
- The user needs full graphic design for a polished thumbnail
- The source video is too low quality to produce usable stills
- The better answer is a custom static image, not a frame grab

## Inputs
- Source video file
- Target platform or use case
- Preferred frame qualities: face, product, motion-free, readable text, bright frame, etc.
- Optional desired count of thumbnail candidates

## Workflow
1. Identify what makes a useful thumbnail for the target platform.
2. Extract candidate frames from visually strong moments.
3. Prefer frames with clarity, focus, and clean composition.
4. Avoid blur-heavy, transition, or awkward-expression frames.
5. Return a shortlist of thumbnail candidates with rationale.

## Output
Return:
1. Candidate thumbnail frames
2. Why each is viable
3. Best recommended option
4. Risks if the video is weak for frame-based thumbnails

## Quality bar
- Avoid motion blur, half-blinks, and awkward facial expressions
- Prefer clear product visibility or recognizable subject framing
- Match the thumbnail style to the platform use case
- Don’t oversell mediocre candidates as strong

## Resource
See `references/output-template.md`.
