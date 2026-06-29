---
name: work-productivity-nano-banana-workflow-helper
description: >-
  Build practical AI image generation and editing workflows inspired by Nano Banana Pro demand. Use when a user needs prompt sets, reference-image planning, iteration rules, output QA, cost controls, or deployment hardening for image generation workflows.
---

# Nano Banana Image Workflow Helper

## Requirement

Use this skill when a user is building, operating, or debugging an AI image generation workflow and needs repeatable help turning a visual goal into prompts, references, checks, and retry decisions.

The validated demand came from popular Nano Banana Pro-style ClawHub workflows plus recent complaints about AI image and video generation cost, waiting time, failed outputs, and first-deployment misconfiguration. This skill focuses on making those workflows reliable rather than adding another generic prompt template.

## Workflow

1. Identify the intended output: subject, format, audience, aspect ratio, required text, brand constraints, reference images, and any prohibited changes.
2. Convert the goal into a prompt pack: base prompt, negative prompt, style anchors, camera/composition notes, edit mask instructions, and variation prompts.
3. Define the iteration budget before generation: maximum attempts, stop conditions, fallback model/tool, and what counts as an acceptable output.
4. Add visual QA checks for composition, anatomy, text rendering, object count, brand consistency, background artifacts, and safety or licensing concerns.
5. When output fails, classify the failure as prompt ambiguity, reference mismatch, model limitation, asset quality, queue/cost issue, or deployment/configuration issue.
6. Produce a revised prompt or workflow patch, then record the change in an iteration log so future runs can reuse the learning.

## Expected Outputs

- A ready-to-run prompt pack for image generation or editing.
- A compact QA checklist tailored to the requested image type.
- A retry plan that controls cost, wait time, and failed-output loops.
- A deployment or configuration checklist when the user is packaging the workflow as a skill or tool.

## Validation

- Prompts include concrete subject, style, composition, constraints, and negative guidance.
- The QA checklist catches visual, brand, safety, and export issues before handoff.
- Retry decisions are bounded by a clear budget and do not depend on cloud-only assumptions.
- The final answer names any model/tool limits that cannot be solved by prompting alone.

## Triggers

Keywords: `nano banana`, `nano-banana-pro`, `AI image generation`, `image editing`, `prompt pack`, `reference image`, `visual QA`, `Gemini image`, `generation failure`.

Example trigger sentences:

- `Use $work-productivity-nano-banana-workflow-helper to build prompts for this product image set.`
- `My AI image workflow keeps producing unusable outputs; diagnose the prompt and retry plan.`
- `Create a QA checklist for publishing a Nano Banana-style image generation skill.`
