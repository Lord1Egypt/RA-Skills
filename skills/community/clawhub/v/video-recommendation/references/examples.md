# Examples

## Example 1: direct recommendation

### User request
"Recommend some videos for me based on what we've been talking about lately."

### Recommended behavior
- infer recent themes from chat
- choose 2-3 angles only
- return 5-8 exact links
- add one short reason per link

### Example output shape
- Andrej Karpathy — "We’re summoning ghosts, not building animals"
  <direct link>
  Why: fits a user thinking about AI capability, meaning, and where intelligence is actually going.

- A.I. ‐ Humanity's Final Invention?
  <direct link>
  Why: strong match for users thinking about civilizational implications, not just products.

## Example 2: links only

### User request
"Just give me 10 video links."

### Recommended behavior
- skip extra framing
- give direct links only, or title + link
- no search URLs unless exact pages are unavailable

## Example 3: project fuel

### User request
"Give me videos that can inspire our AI video product direction."

### Recommended behavior
- bias toward AI filmmaking, creative tooling, founder/product insight
- prioritize workflows, showcases, breakdowns, and signal-rich commentary
- avoid broad entertainment picks

### Example output shape
#### AI filmmaking
- Grizzlies: An AI short film | Runway
  <direct link>
  Why: good taste benchmark for what feels cinematic instead of gimmicky.

#### Product signal
- Why most AI products fail
  <direct link>
  Why: useful for thinking about where user value comes from beyond novelty.

## Example 4: mood rescue

### User request
"I want something fun tonight, but not dumb."

### Recommended behavior
- keep list short
- bias toward delight, surprise, energy, and high production value
- avoid lectures unless they are genuinely entertaining

## Example 5: bilingual user

### User request
"给我一些英文视频，最好不要太水。"

### Recommended behavior
- keep reply in the user's language
- recommendations can still be English-language videos
- prioritize signal density and clarity

## Example 6: strategic taste curation

### User request
"What are 5 videos I probably didn't know I wanted?"

### Recommended behavior
- optimize for delight and precision
- slightly widen the search beyond obvious channels
- avoid random eclecticism; keep an underlying theme
