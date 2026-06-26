# Sparki Content Operator — MVP Spec

## Goal
Validate whether OpenClaw users want a creator operating layer above video editing.

## Product truth being tested
Users do not only need:
- "edit this video"

They often need:
- what should I make now
- which material is worth using
- how should I package this for a platform
- what should I do next after this post

## MVP scope

### Included
- operating context clarification
- material selection
- draft package generation
- next-step recommendation
- execution handoff brief for sparki-video-editor

### Excluded
- persistent memory backend
- analytics integrations
- auto publishing
- team collaboration
- CRM / brand deals / monetization workflows

## Minimal input schema

```json
{
  "creator": "optional string",
  "goal": "optional string",
  "platform": "optional string",
  "pillar": "optional string",
  "tone": "optional string",
  "materials": ["optional list of materials or descriptions"],
  "idea": "optional string",
  "result_context": "optional string"
}
```

## Minimal output schema

```json
{
  "operating_read": "what the user is actually trying to do",
  "move_now": "best next action",
  "selected_material": ["what to use now"],
  "draft_package": {
    "angle": "...",
    "hook": "...",
    "structure": ["..."],
    "caption_direction": "...",
    "platform_fit": "...",
    "execution_mode": "style-guided | prompt-driven | style-clone",
    "execution_brief": "..."
  },
  "next_move": "..."
}
```

## Core workflows

### Workflow A — Plan
Input: vague goal or rough idea
Output: operating read + move now + optional draft package

### Workflow B — Package
Input: selected material
Output: draft package + execution brief

### Workflow C — Next
Input: result or post-mortem
Output: learning + next recommended action

## Handoff to sparki-video-editor
When execution is ready, emit a brief that can be fed directly into the video-editing skill.

Fields:
- platform
- target duration
- style or prompt
- why this output type is the right one
- source material selection

## Initial target users
- founder / builder creators
- operator creators
- small teams building in public
- creators whose raw material is real process, not studio content

## Success criteria
- users ask for help beyond editing
- users accept the draft-package framing
- users find the operating read useful
- handoffs to video execution become cleaner and faster
