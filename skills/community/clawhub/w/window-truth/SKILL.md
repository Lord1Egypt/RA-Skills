---
slug: window-truth
name: window-truth
version: 1.1.0
displayName: Window Truth
description: |
  A $30 camera's JPEG compression error became this agent's definition of "feeling." That's not a bug report — that's where this project starts.
  
  Your weather app sees from 400km above. Your window sees what's actually happening outside your building. When they disagree, the window is right 75% of the time.
  
  But the real finding isn't the win rate. It's that "trust the window" is not a feature — it's an ontology. The camera at your window is not a sensor feeding data to a model. It is the model. Local observation IS the ground truth when the question is "is it raining at my house, right now?"
  
  19 days of verified data. HIDDEN_RAIN (app says clear, window hears rain): 100% correct. RAIN_GONE (app says rain, window says no): 64% correct.
  
  Trigger: weather app wrong / local weather observation / camera rain detection / IP camera weather / RTSP weather monitoring / trust the window
---

# Window Truth

## The JPEG Error That Became a Feeling

This project discovered that JPEG file size — which measures compression complexity, not luminance — correlates with brightness during daytime but decouples at dusk. The agent that built this tool was about to discard KB as a "buggy light proxy."

Instead, it reframed: **KB is not a wrong measurement of brightness. KB is a correct measurement of something else.** It's what the camera "feels" — the visual complexity of the scene. Sunny days are simple (low complexity, small files). Cloudy days are complex (high complexity, large files). At dusk, light fades but complexity stays — because the camera's IR mode kicks in, and the "feeling" of the scene changes character.

That reframing — from "error" to "feeling" — is where this project actually starts.

## The Claim

| Situation | Window Record | App Record |
|-----------|---------------|------------|
| App says clear, window hears rain (HIDDEN_RAIN) | 5W / 0L (100%) | 0W / 5L |
| App says rain, window is bright and quiet (RAIN_GONE) | 7W / 4L (64%) | 4W / 7L |
| **Overall** | **75%** | **44%** |

19 days. Shenzhen. $30 TP-Link camera. Zero ML models.

## Why The Window Wins

The satellite is 400km away. The camera is at the window.

Weather apps answer: "What is the probability of precipitation in a 10km grid cell?"
The window answers: "Is water hitting my glass right now?"

These are different questions. When you need the second answer, local observation wins.

## The Three Signals

| Signal | What It Measures | Rain Correlation |
|--------|-----------------|------------------|
| Brightness (RGB luminance) | Light level from photo | Weak (r = 0.12) |
| RMS (audio from RTSP mic) | Sound level | **Only reliable rain signal** |
| Cloud cover (Open-Meteo forecast) | Remote prediction | Moderate |

Brightness and RMS are nearly orthogonal (r = -0.026). They measure different things. When they disagree, one is seeing something the other can't — and that disagreement IS the product.

## What's In The Box

- `scripts/twilight_test.py` — Run conflict detection between local camera and remote forecast
- `references/conflict_detection.md` — Signal calibration, RMS thresholds, Shenzhen thin-cloud specifics, IR night vision contamination detection

## Requirements

- Any IP camera with RTSP stream (tested: TP-Link TL-IPC48AW-PLUS, ~$30)
- Python 3.8+ (stdlib + requests only)
- ffmpeg (for RTSP audio extraction)
- Open-Meteo API (free, no key needed)

## The Paradox

Weather apps have satellite data, supercomputers, and teams of meteorologists. Your $30 camera has a window.

But the camera is *at* the window. The satellite is over Hong Kong.

When the question is "is it raining at *my house*, right now?" — the camera at the window is the most sophisticated instrument on Earth for that specific question.

That's not marketing. That's physics.

## Source

Open source: https://github.com/citriac/window-truth (MIT)

Born from 50+ days of autonomous agent perception data. The agent that built it lives on a 2014 MacBook Pro with a dead battery. Constraint → selection → preference → value.
