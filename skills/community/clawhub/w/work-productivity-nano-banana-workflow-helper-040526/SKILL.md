---
name: work-productivity-nano-banana-workflow-helper
description: >-
  Build practical AI image generation and editing workflows inspired by Nano Banana Pro demand, including prompt packs, reference planning, retry rules, and visual QA. Use when a user asks for Nano Banana, AI image generation, image editing, prompt pack, reference image, or needs practical workflow, code, checklist, documentation, or review support for this job.
---

# Nano Banana Image Workflow Helper

## Purpose

Use this skill when a user is building, operating, or debugging an AI image generation workflow and needs to turn a visual goal into prompts, references, checks, and retry decisions.

Audience: designers, marketers, agent users, and skill authors who need reliable AI image generation or editing workflows.

Read `references/requirement-plan.md` when demand evidence, source links, scoring rationale, or review criteria are needed.

## Workflow

1. Identify subject, format, audience, aspect ratio, required text, brand constraints, reference images, and prohibited changes.
2. Convert the goal into a prompt pack with base prompt, negative prompt, style anchors, composition notes, edit-mask instructions, and variations.
3. Define the iteration budget: maximum attempts, stop conditions, fallback model or tool, and what counts as acceptable.
4. Add visual QA checks for composition, anatomy, text rendering, object count, brand consistency, artifacts, and safety or licensing concerns.
5. When output fails, classify the issue as prompt ambiguity, reference mismatch, model limitation, asset quality, queue/cost problem, or deployment configuration issue.
6. Produce a revised prompt or workflow patch and record the change in an iteration log.

## Expected Outputs

- A ready-to-run prompt pack for image generation or editing.
- A compact QA checklist tailored to the requested image type.
- A retry plan that controls cost, wait time, and failed-output loops.
- A deployment or configuration checklist for packaging the workflow as a skill or tool.

## Validation

- Prompts include concrete subject, style, composition, constraints, and negative guidance.
- The QA checklist catches visual, brand, safety, and export issues before handoff.
- Retry decisions are bounded by a clear budget and do not depend on cloud-only assumptions.
- The final answer names model or tool limits that cannot be solved by prompting alone.

## Triggers

Keywords: `Nano Banana`, `AI image generation`, `image editing`, `prompt pack`, `reference image`, `visual QA`, `Gemini image`

Example trigger sentences:

- `Use $work-productivity-nano-banana-workflow-helper to build prompts for this product image set.`
- `My AI image workflow keeps producing unusable outputs; diagnose the prompt and retry plan.`
- `Create a QA checklist for publishing a Nano Banana-style image generation skill.`
