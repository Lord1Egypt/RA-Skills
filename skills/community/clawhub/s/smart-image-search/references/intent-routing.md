# Intent routing

Route image search by likely user intent before ranking.

## Supported intents

### 1. meme
Typical query words:
- meme
- reaction image
- funny image
- emoji
- joke image

Preferred sources and ranking:
- prefer meme, emoji, and funny-image pages
- tolerate lower image quality if semantic match is strong
- de-prioritize official sites

### 2. official
Typical query words:
- official
- logo
- emblem
- mascot
- brand mark
- poster

Preferred sources and ranking:
- prefer official domains, reference pages, and institutional pages
- penalize meme sites and noisy galleries
- when possible, infer a subtype and route more specifically:
  - `campus`: campus, map, gate, landscape
  - `emblem`: emblem, logo, crest, mark, badge
  - `mascot`: mascot, character, official character, IP character
  - `poster`: poster, promotional art, campaign art

### 3. portrait
Typical query words:
- a person or character name only
- portrait
- photo
- image
- picture

Preferred sources and ranking:
- prefer clear portrait or representative photos
- prioritize semantically matched titles and cleaner pages

### 4. wallpaper
Typical query words:
- wallpaper
- hd
- high resolution
- 4k
- landscape
- portrait orientation

Preferred sources and ranking:
- prefer larger images and wallpaper-like pages
- penalize tiny thumbnails and icons

### 5. avatar
Typical query words:
- avatar
- profile picture
- icon

Preferred sources and ranking:
- prefer square or avatar-oriented results when detectable
- tolerate gallery sources if the semantic match is strong

## Decision rule

- If explicit cue words appear, trust them.
- Otherwise default to `portrait` for person/entity names.
- If the entity looks institutional and includes logo/mascot/school words, lean `official`.
- If confidence is mixed, keep `portrait` as the safe default.
