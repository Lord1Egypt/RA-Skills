# Writing NSFW prompts that work

## Recipe

```
[Who: adult + age range + look] + [one main action] + [one secondary motion]
+ [setting] + [light sources] + [camera move] + [style]
```

- **Image-to-video:** the first frame already shows the subject, wardrobe and setting. Describe what *changes*: "She turns slowly from the window toward camera, the silk catching the city light."
- **Say who is in shot** when it matters: `Cast: one woman.` / `Cast: an adult man and an adult woman.`
- **Pin the camera:** `static camera`, `locked-off`, `slow push-in`, `orbit left`, `tilt up`.
- **Give motion a cause:** a draught pulls the silk, steam fogs the glass, wind lifts the hair.
- **One main action per 5 seconds.** Chain clips (`last_image_url`, `video-extend`) for longer scenes.
- **Always state adult age** ("in her 30s", "an adult man in his 40s"). Never add youthful descriptors (school settings, "petite", "young-looking", childlike anime proportions), even if the user asks.

## Reliability ladder (most → least reliable)

breathing, blinking → hair and fabric in wind → water, steam, smoke, candle flicker → slow head turn, look over the shoulder → walking toward or away from the camera → stretching, rolling over → dancing → two-person contact → fast or acrobatic action.

## Couples

Different outfit colours per person, side or back angles, slow actions, 5 seconds, a stronger model (Seedance 2.0/2.5 Spicy).

## Text-to-image first frames

Subject large in frame, relaxed hands, simple background, lighting that matches the video mood, resolution ≥ the video resolution. Z-Image Spicy for photoreal, Prefect Pony XL for anime (tags: `score_9, score_8_up, anime style, 1woman, adult, mature female, ...`).

## Negative prompts (Wan 2.6 / 2.7 Spicy only)

```
blurry, low quality, watermark, text, deformed, bad anatomy, extra limbs, extra fingers,
plastic skin, flickering, morphing, identity change, extra person
```

## Expanding a one-line idea

Use `spicy.py chat` with a text model and this system prompt:

```
You write prompts for adult image-to-video models. Every character is an adult aged 21+;
never use descriptors that suggest youth and never depict real, identifiable people.
Return ONE prompt of 40–80 words: only what changes from the first frame, one main action,
one secondary motion, one camera move, the light sources, a short style phrase.
```

More than 100 ready prompts: https://github.com/Spicy-API/nsfw-ai-video-prompts
