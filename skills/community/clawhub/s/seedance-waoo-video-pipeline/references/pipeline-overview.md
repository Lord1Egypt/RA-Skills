# Pipeline Overview

## Purpose

This pipeline combines **Seedance** for story pre-production and **waoowaoo** for downstream media production.

- Seedance standardizes the story into a production-ready pack.
- waoowaoo consumes that pack and produces real deliverables.

## Layers

### 1. Story Pack Layer
Produces:
- script document
- asset list
- storyboard document
- continuity hints
- tail-frame hints when needed

### 2. Production Layer
Consumes story pack and resolves:
- episode
- panel
- source image
- video prompt
- subtitle text
- video task state

### 3. Delivery Layer
Builds:
- subtitled clip
- subtitle + TTS clip
- subtitle + TTS + ambience final clip
- delivery manifest

## Operating Philosophy

- one main clip before many partial clips
- real DB/task state beats assumptions
- probe tasks are diagnostic only
- narration must align with subtitle text
- ambience should behave like environment, not generic music

## Trigger Summary

### Auto-trigger
- story / novel / bridge scene → short video
- script → storyboard → video requests
- one sentence / 一句文案 from scratch

### Conditional trigger
- existing script / storyboard / panel / raw clip exists
- continue from the highest reliable completed stage

### Do not trigger
- format conversion only
- manual editing only
- pure technical maintenance

## Recommended Default Flow

### Default start rule

If the user only provides a topic /一句文案 and does not provide existing script, storyboard, panel ids, or approved images, the pipeline must start from Seedance-side pre-production first.

Required start order:
1. build Story Intent Brief
2. build script line / story intent
3. build or normalize story pack
4. build storyboard / panel plan
5. surface the formal Seedance four-pack to the user and wait for confirmation
6. after confirmation, generate the first-image confirmation pack and send it to the user
7. approve first image / first frame
8. only then resolve current main clip in waoowaoo
9. generate or download source video
10. validate subtitle text
11. generate aligned narration
12. prepare ambience
13. mix final delivery clip
14. send and archive outputs
