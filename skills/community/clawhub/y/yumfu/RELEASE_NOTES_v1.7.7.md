# YumFu v1.7.7 - Clearer Choices + Quieter Gameplay 🎮

## What changed

This release tightens YumFu's actual play experience based on direct user feedback from live gameplay.

### ✅ Choices are now clearer across all worlds
- Gameplay turns should render choices in a separate, easy-to-scan block
- Prefer:
  - Chinese gameplay → `1 / 2 / 3`
  - English gameplay → `A / B / C` or `1 / 2 / 3`
- Choices should no longer be buried inside a dense story paragraph
- Default turn structure now favors:
  1. story consequence
  2. blank line
  3. clear `你现在可以：` / `Choose your next move:`
  4. separate listed options

### ✅ YumFu now prefers silent execution
- YumFu is a game, not an AI process log
- The skill now defaults to quiet execution during gameplay operations
- It should do the work and deliver the finished turn, instead of narrating internal steps like:
  - “I’ll continue this turn now”
  - “I’m sending image + TTS”
  - “I’m updating the save”

### ✅ TTS restricted to player-facing story content
- TTS still stays on by default for gameplay saves unless disabled
- But TTS must now only cover the actual player-facing narration/story text
- Meta execution chatter, progress updates, and assistant-side workflow commentary should not be voiced

### ✅ Gameplay delivery feels more like a real game session
- Less AI self-talk
- Cleaner pacing
- Better readability when choosing actions
- Stronger separation between story content and behind-the-scenes execution

## Why this release

The user feedback was blunt and correct:
- choice formatting should be easier to scan
- YumFu should feel like playing a game, not watching the AI talk about itself
- TTS should only read the content worth hearing

This release turns those preferences into explicit product behavior.

## Result

Future YumFu sessions should now feel:
- cleaner
- faster
- less cluttered
- easier to play turn by turn
- more like an illustrated narrative RPG and less like a verbose assistant workflow
