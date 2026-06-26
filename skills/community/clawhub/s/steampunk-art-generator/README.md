# Steampunk Art Generator

Generate stunning steampunk artwork from text descriptions — Victorian portraits with brass gears, clockwork machinery, ornate goggles, leather-and-copper aesthetics, and industrial fantasy scenes. Describe your vision and receive a high-quality AI-generated image in seconds.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/steampunk-art-generator
```

**Via ClawHub:**
```bash
clawhub install steampunk-art-generator
```

---

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage Examples

**Default steampunk portrait:**
```bash
node steampunkartgenerator.js "steampunk inventor with clockwork arm" --token "$NETA_TOKEN"
```

**Landscape scene:**
```bash
node steampunkartgenerator.js "steampunk city skyline with airships and factory smokestacks" --token "$NETA_TOKEN" --size landscape
```

**Tall portrait format:**
```bash
node steampunkartgenerator.js "Victorian lady with ornate brass goggles and corset, steampunk fashion" --token "$NETA_TOKEN" --size tall
```

**Square format:**
```bash
node steampunkartgenerator.js "steampunk clockwork cat, mechanical gears, copper and bronze" --token "$NETA_TOKEN" --size square
```

**With style reference:**
```bash
node steampunkartgenerator.js "steampunk knight in full brass armor" --token "$NETA_TOKEN" --ref <picture_uuid>
```

**Output:** Returns a direct image URL.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | *(required)* | Your Neta API token |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--ref` | UUID string | *(none)* | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width | Height |
|------|-------|--------|
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `square` | 1024 | 1024 |
| `tall` | 704 | 1408 |

---

## Prompt Tips

- Be descriptive: include materials (brass, copper, leather), lighting (gaslight, candlelight), and mood (dramatic, mysterious)
- Mention specific steampunk elements: clockwork gears, steam engines, airships, top hats, goggles, mechanical limbs
- Add era details: Victorian, Edwardian, industrial revolution
- Include artistic style cues: cinematic, illustration, oil painting, concept art

**Example prompts:**
- `"steampunk explorer, pith helmet with brass compass, leather coat covered in pockets and gadgets, dramatic lighting"`
- `"steampunk laboratory interior, bubbling alchemical apparatus, copper pipes and gauges, warm amber gaslight"`
- `"Victorian steampunk duchess, elaborate clockwork jewelry, silk and gears, aristocratic setting"`

