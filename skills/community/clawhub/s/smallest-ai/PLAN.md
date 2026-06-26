# Plan: Add Smallest AI as a Native TTS Provider in OpenClaw

## Context

**What:** Add Smallest AI (Lightning v3.1 TTS, Pulse STT) as a first-class provider in OpenClaw's TTS system, alongside the existing providers: ElevenLabs, OpenAI, and Edge TTS.

**Why:** Smallest AI offers sub-100ms latency TTS with 30+ language support, making it competitive with existing providers. Adding it natively means users can set `provider: "smallestai"` in their `openclaw.json` config rather than relying on the external skill/script approach.

**Repository:** https://github.com/openclaw/openclaw (TypeScript, pnpm, vitest)

**Build/Test commands:**
```bash
pnpm build && pnpm check && pnpm test
```

---

## Architecture Overview

### How OpenClaw's TTS System Works

OpenClaw's TTS is NOT a plugin/adapter pattern with a common interface. Instead, it is a **monolithic module** with provider-specific code paths handled inline via `if/else` branches. The key insight: there is no `TtsProvider` base class or interface to implement. Each provider is wired directly into the core functions.

**Flow: text -> audio -> delivery**

```
1. User/agent reply text arrives
2. maybeApplyTtsToPayload() in tts.ts decides if TTS should run
3. Text is cleaned (strip markdown), optionally summarized
4. parseTtsDirectives() extracts inline [[tts:...]] overrides
5. textToSpeech() is called:
   a. Resolves provider order (primary + fallbacks)
   b. For each provider, calls the provider-specific function:
      - "edge"       -> edgeTTS()         in tts-core.ts
      - "elevenlabs" -> elevenLabsTTS()   in tts-core.ts
      - "openai"     -> openaiTTS()       in tts-core.ts
      - "smallestai" -> smallestaiTTS()   NEW
   c. Audio buffer is written to a temp file
   d. TtsResult returned with audioPath, provider, format info
6. Audio file path is attached to the reply payload (mediaUrl)
7. Channel delivers the audio file to the user
```

**Fallback behavior:** When the primary provider fails, OpenClaw iterates through `TTS_PROVIDERS` in order. The new provider must be added to this list.

**Telephony path:** `textToSpeechTelephony()` is a separate function that returns raw PCM buffers for voice-call use cases. Smallest AI can support this via `sample_rate=8000` or `sample_rate=24000` with `add_wav_header=false` (raw PCM).

---

## Smallest AI API Details

### TTS: Lightning v3.1

```
POST https://api.smallest.ai/waves/v1/lightning-v3.1/get_speech
Authorization: Bearer <SMALLEST_API_KEY>
Content-Type: application/json
```

Request body:
```json
{
  "text": "Hello world",
  "voice_id": "diana",
  "sample_rate": 24000,
  "speed": 1.0,
  "language": "en",
  "output_format": "wav"
}
```

Response: Binary audio data (WAV when `add_wav_header: true`, raw PCM otherwise).

**Parameters:**
| Param           | Type   | Default | Range/Values                        |
|-----------------|--------|---------|-------------------------------------|
| text            | string | --      | Required. Max ~5000 chars           |
| voice_id        | string | --      | Required. emily, jasmine, arman, arnav, mithali |
| sample_rate     | int    | 24000   | 8000, 16000, 24000, 48000          |
| speed           | float  | 1.0     | 0.5 - 2.0                          |
| language        | string | "en"    | ISO 639-1 code (30+ languages)     |
| add_wav_header  | bool   | false   | true = playable WAV file            |

**Voices:**
| Voice ID  | Gender | Style                | Best For                    |
|-----------|--------|----------------------|-----------------------------|
| diana     | Female | Neutral, clear (American)  | General use (default)       |
| vincent   | Male   | Conversational (American)  | Announcements, briefings    |
| advika    | Female | Native Hindi (Indian)      | Hindi content, code-switch  |
| vivaan    | Male   | Indian English/Hindi       | Bilingual content           |
| camilla   | Female | Mexican/Latin Spanish      | Spanish content             |

### STT: Pulse (future scope, not in initial PR)

```
POST https://api.smallest.ai/waves/v1/pulse/get_text
Content-Type: audio/wav
Authorization: Bearer <SMALLEST_API_KEY>
```

---

## Files to Modify (with exact paths)

All paths relative to the OpenClaw repo root.

### 1. Type definitions

**File: `src/config/types.tts.ts`**

Add `"smallestai"` to the `TtsProvider` union type.

```typescript
// BEFORE:
export type TtsProvider = "elevenlabs" | "openai" | "edge";

// AFTER:
export type TtsProvider = "elevenlabs" | "openai" | "edge" | "smallestai";
```

Add the `SmallestaiTtsConfig` section to `TtsConfig`:

```typescript
// Add inside TtsConfig type, after the edge section:
/** Smallest AI (Lightning) configuration. */
smallestai?: {
  apiKey?: SecretInput;
  baseUrl?: string;
  voiceId?: string;
  model?: string;
  sampleRate?: number;
  speed?: number;
  language?: string;
};
```

### 2. Zod validation schema

**File: `src/config/zod-schema.core.ts`**

Update the `TtsProviderSchema` enum and add a `smallestai` section to `TtsConfigSchema`.

```typescript
// BEFORE (line ~356):
export const TtsProviderSchema = z.enum(["elevenlabs", "openai", "edge"]);

// AFTER:
export const TtsProviderSchema = z.enum(["elevenlabs", "openai", "edge", "smallestai"]);
```

Add inside the `TtsConfigSchema` `.object({...})`, after the `edge` section:

```typescript
smallestai: z
  .object({
    apiKey: SecretInputSchema.optional().register(sensitive),
    baseUrl: z.string().optional(),
    voiceId: z.string().optional(),
    model: z.string().optional(),
    sampleRate: z.number().int().min(8000).max(48000).optional(),
    speed: z.number().min(0.5).max(2).optional(),
    language: z.string().optional(),
  })
  .strict()
  .optional(),
```

### 3. Core TTS module -- config resolution

**File: `src/tts/tts.ts`**

**3a. Add defaults (near top, around line 53-68):**

```typescript
const DEFAULT_SMALLESTAI_BASE_URL = "https://api.smallest.ai";
const DEFAULT_SMALLESTAI_VOICE_ID = "diana";
const DEFAULT_SMALLESTAI_MODEL = "lightning-v3.1";
const DEFAULT_SMALLESTAI_SAMPLE_RATE = 24000;
const DEFAULT_SMALLESTAI_LANGUAGE = "en";
```

**3b. Add import of `smallestaiTTS` from tts-core.ts (line ~32):**

```typescript
import {
  // ... existing imports ...
  smallestaiTTS,
} from "./tts-core.js";
```

**3c. Expand `ResolvedTtsConfig` type (after the `edge` block, around line 136):**

```typescript
smallestai: {
  apiKey?: string;
  baseUrl: string;
  voiceId: string;
  model: string;
  sampleRate: number;
  speed: number;
  language: string;
};
```

**3d. Expand `resolveTtsConfig()` function (around line 261-330) to include smallestai resolution:**

Inside `resolveTtsConfig()`, after the `edge: { ... }` block:

```typescript
smallestai: {
  apiKey: normalizeResolvedSecretInputString({
    value: raw.smallestai?.apiKey,
    path: "messages.tts.smallestai.apiKey",
  }),
  baseUrl: raw.smallestai?.baseUrl?.trim() || DEFAULT_SMALLESTAI_BASE_URL,
  voiceId: raw.smallestai?.voiceId?.trim() || DEFAULT_SMALLESTAI_VOICE_ID,
  model: raw.smallestai?.model?.trim() || DEFAULT_SMALLESTAI_MODEL,
  sampleRate: raw.smallestai?.sampleRate ?? DEFAULT_SMALLESTAI_SAMPLE_RATE,
  speed: raw.smallestai?.speed ?? 1.0,
  language: raw.smallestai?.language?.trim() || DEFAULT_SMALLESTAI_LANGUAGE,
},
```

**3e. Update `resolveTtsApiKey()` (around line 521-532):**

```typescript
// Add before the final `return undefined;`:
if (provider === "smallestai") {
  return config.smallestai.apiKey || process.env.SMALLEST_API_KEY;
}
```

**3f. Update `TTS_PROVIDERS` constant (line 534):**

```typescript
// BEFORE:
export const TTS_PROVIDERS = ["openai", "elevenlabs", "edge"] as const;

// AFTER:
export const TTS_PROVIDERS = ["openai", "elevenlabs", "edge", "smallestai"] as const;
```

**3g. Update `isTtsProviderConfigured()` (around line 540-545):**

The existing logic already handles this correctly -- `smallestai` is not `"edge"`, so it falls through to the `return Boolean(resolveTtsApiKey(config, provider))` path. No change needed here.

**3h. Update `textToSpeech()` function (around line 562-730):**

Inside the `for (const provider of providers)` loop, after the `edge` block and after the `apiKey` check, add a `smallestai` branch. The current structure handles `elevenlabs` and `openai` as the two API-key providers. We need to add `smallestai` as a third.

After the `if (!apiKey)` check (line ~665), before the existing `if (provider === "elevenlabs")` block:

```typescript
if (provider === "smallestai") {
  audioBuffer = await smallestaiTTS({
    text: params.text,
    apiKey,
    baseUrl: config.smallestai.baseUrl,
    voiceId: config.smallestai.voiceId,
    model: config.smallestai.model,
    sampleRate: config.smallestai.sampleRate,
    speed: config.smallestai.speed,
    language: config.smallestai.language,
    addWavHeader: true,
    timeoutMs: config.timeoutMs,
  });
} else if (provider === "elevenlabs") {
```

Note: the `output.extension` for Smallest AI will be `.wav` since we use `add_wav_header: true`. The output format constants need updating:

```typescript
// Add to TELEGRAM_OUTPUT (for voice-bubble channels):
const TELEGRAM_OUTPUT = {
  openai: "opus" as const,
  elevenlabs: "opus_48000_64",
  smallestai: { sampleRate: 24000, addWavHeader: true },
  extension: ".opus",
  voiceCompatible: true,
};
```

Actually, the simpler approach: Smallest AI returns WAV. For Telegram/WhatsApp voice bubbles (which need opus), the audio won't be directly voice-compatible, so `voiceCompatible` will be `false` for Smallest AI in voice-bubble channels. This is fine -- the audio still plays as an attachment. The return value should use `.wav` extension:

```typescript
// Inside the smallestai branch, after getting audioBuffer:
const latencyMs = Date.now() - providerStart;
const tempRoot = resolvePreferredOpenClawTmpDir();
mkdirSync(tempRoot, { recursive: true, mode: 0o700 });
const tempDir = mkdtempSync(path.join(tempRoot, "tts-"));
const audioPath = path.join(tempDir, `voice-${Date.now()}.wav`);
writeFileSync(audioPath, audioBuffer);
scheduleCleanup(tempDir);

return {
  success: true,
  audioPath,
  latencyMs,
  provider,
  outputFormat: "wav",
  voiceCompatible: false,
};
```

**3i. Update `textToSpeechTelephony()` (around line 732-819):**

Add a `smallestai` branch in the telephony provider loop. Smallest AI supports raw PCM output when `add_wav_header: false`:

```typescript
if (provider === "smallestai") {
  const sampleRate = 24000;
  const audioBuffer = await smallestaiTTS({
    text: params.text,
    apiKey,
    baseUrl: config.smallestai.baseUrl,
    voiceId: config.smallestai.voiceId,
    model: config.smallestai.model,
    sampleRate,
    speed: config.smallestai.speed,
    language: config.smallestai.language,
    addWavHeader: false,
    timeoutMs: config.timeoutMs,
  });

  return {
    success: true,
    audioBuffer,
    latencyMs: Date.now() - providerStart,
    provider,
    outputFormat: "pcm",
    sampleRate,
  };
}
```

**3j. Expand `TtsDirectiveOverrides` type (around line 163-178) and directive parsing:**

Add `smallestai` overrides:

```typescript
export type TtsDirectiveOverrides = {
  ttsText?: string;
  provider?: TtsProvider;
  openai?: { voice?: string; model?: string };
  elevenlabs?: {
    voiceId?: string;
    modelId?: string;
    seed?: number;
    applyTextNormalization?: "auto" | "on" | "off";
    languageCode?: string;
    voiceSettings?: Partial<ResolvedTtsConfig["elevenlabs"]["voiceSettings"]>;
  };
  smallestai?: {
    voiceId?: string;
    language?: string;
    speed?: number;
    sampleRate?: number;
  };
};
```

### 4. Core TTS module -- API call implementation

**File: `src/tts/tts-core.ts`**

Add the `smallestaiTTS()` function. Follow the exact same pattern as `elevenLabsTTS()` and `openaiTTS()`.

**Add these constants near the top:**

```typescript
const DEFAULT_SMALLESTAI_BASE_URL = "https://api.smallest.ai";

const SMALLESTAI_VOICES = [
  "diana",
  "vincent",
  "advika",
  "vivaan",
  "camilla",
  "zara",
  "melody",
  "stella",
  "robert",
  "arjun",
] as const;

export function isValidSmallestaiVoice(voice: string): boolean {
  return SMALLESTAI_VOICES.includes(voice as (typeof SMALLESTAI_VOICES)[number]);
}
```

**Add the main TTS function:**

```typescript
export async function smallestaiTTS(params: {
  text: string;
  apiKey: string;
  baseUrl: string;
  voiceId: string;
  model: string;
  sampleRate: number;
  speed: number;
  language: string;
  addWavHeader: boolean;
  timeoutMs: number;
}): Promise<Buffer> {
  const {
    text,
    apiKey,
    baseUrl,
    voiceId,
    model,
    sampleRate,
    speed,
    language,
    addWavHeader,
    timeoutMs,
  } = params;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const normalizedBaseUrl = baseUrl.trim().replace(/\/+$/, "") || DEFAULT_SMALLESTAI_BASE_URL;
    const url = `${normalizedBaseUrl}/waves/v1/${model}/get_speech`;

    const response = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
        voice_id: voiceId,
        sample_rate: sampleRate,
        speed,
        language,
        output_format: addWavHeader ? "wav" : "pcm",
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new Error(`Smallest AI TTS API error (${response.status})`);
    }

    return Buffer.from(await response.arrayBuffer());
  } finally {
    clearTimeout(timeout);
  }
}
```

**Export from tts-core.ts:** Add `smallestaiTTS` and `isValidSmallestaiVoice` to the module's exports.

### 5. Directive parsing updates

**File: `src/tts/tts-core.ts`** (in `parseTtsDirectives()`)

Add handling for `smallestai` voice directives in the switch statement (around line 154-332). Add cases:

```typescript
case "smallestai_voice":
case "smallestaivoice":
  if (!policy.allowVoice) {
    break;
  }
  if (isValidSmallestaiVoice(rawValue)) {
    overrides.smallestai = { ...overrides.smallestai, voiceId: rawValue };
  } else {
    warnings.push(`invalid Smallest AI voice "${rawValue}"`);
  }
  break;
```

Also update the `provider` case to accept `"smallestai"`:

```typescript
case "provider":
  if (!policy.allowProvider) {
    break;
  }
  if (
    rawValue === "openai" ||
    rawValue === "elevenlabs" ||
    rawValue === "edge" ||
    rawValue === "smallestai"
  ) {
    overrides.provider = rawValue;
  } else {
    warnings.push(`unsupported provider "${rawValue}"`);
  }
  break;
```

### 6. Secret registry

**File: `src/secrets/target-registry-data.ts`**

Add an entry for the Smallest AI API key. Insert after the `messages.tts.openai.apiKey` entry (around line 627):

```typescript
{
  id: "messages.tts.smallestai.apiKey",
  targetType: "messages.tts.smallestai.apiKey",
  configFile: "openclaw.json",
  pathPattern: "messages.tts.smallestai.apiKey",
  secretShape: SECRET_INPUT_SHAPE,
  expectedResolvedValue: "string",
  includeInPlan: true,
  includeInConfigure: true,
  includeInAudit: true,
},
```

Also add entries for Discord voice TTS if you want full parity:

```typescript
{
  id: "channels.discord.voice.tts.smallestai.apiKey",
  targetType: "channels.discord.voice.tts.smallestai.apiKey",
  configFile: "openclaw.json",
  pathPattern: "channels.discord.voice.tts.smallestai.apiKey",
  secretShape: SECRET_INPUT_SHAPE,
  expectedResolvedValue: "string",
  includeInPlan: true,
  includeInConfigure: true,
  includeInAudit: true,
},
{
  id: "channels.discord.accounts.*.voice.tts.smallestai.apiKey",
  targetType: "channels.discord.accounts.*.voice.tts.smallestai.apiKey",
  configFile: "openclaw.json",
  pathPattern: "channels.discord.accounts.*.voice.tts.smallestai.apiKey",
  secretShape: SECRET_INPUT_SHAPE,
  expectedResolvedValue: "string",
  includeInPlan: true,
  includeInConfigure: true,
  includeInAudit: true,
},
```

### 7. Secret collectors for TTS

**File: `src/secrets/runtime-config-collectors-tts.ts`**

Add a `smallestai` API key collector block alongside `elevenlabs` and `openai`:

```typescript
const smallestai = params.tts.smallestai;
if (isRecord(smallestai)) {
  collectSecretInputAssignment({
    value: smallestai.apiKey,
    path: `${params.pathPrefix}.smallestai.apiKey`,
    expected: "string",
    defaults: params.defaults,
    context: params.context,
    active: params.active,
    inactiveReason: params.inactiveReason,
    apply: (value) => {
      smallestai.apiKey = value;
    },
  });
}
```

### 8. Gateway server methods

**File: `src/gateway/server-methods/tts.ts`**

**8a. Update `tts.providers` handler** (around line 124-156) to list Smallest AI:

```typescript
{
  id: "smallestai",
  name: "Smallest AI",
  configured: Boolean(resolveTtsApiKey(config, "smallestai")),
  models: ["lightning-v3.1"],
  voices: ["diana", "vincent", "advika", "vivaan", "camilla"],
},
```

**8b. Update `tts.setProvider` handler** (around line 101-123) to accept `"smallestai"`:

```typescript
// BEFORE:
if (provider !== "openai" && provider !== "elevenlabs" && provider !== "edge") {

// AFTER:
if (
  provider !== "openai" &&
  provider !== "elevenlabs" &&
  provider !== "edge" &&
  provider !== "smallestai"
) {
```

And update the error message:

```typescript
"Invalid provider. Use openai, elevenlabs, edge, or smallestai.",
```

**8c. Update `tts.status` handler** to include Smallest AI key status:

Add after `hasElevenLabsKey`:
```typescript
hasSmallestaiKey: Boolean(resolveTtsApiKey(config, "smallestai")),
```

### 9. Chat command handler

**File: `src/auto-reply/reply/commands-tts.ts`**

**9a. Update `ttsUsage()` function** (around line 43-68) to list Smallest AI:

Add to the Providers section:
```typescript
`• smallestai -- Ultra-fast, sub-100ms (requires API key)\n` +
```

**9b. Update `/tts provider` handler** (around line 159-189):

Add key check:
```typescript
const hasSmallestai = Boolean(resolveTtsApiKey(config, "smallestai"));
```

Add to the display:
```typescript
`Smallest AI key: ${hasSmallestai ? "check" : "x"}\n` +
```

Update the validation check:
```typescript
// BEFORE:
if (requested !== "openai" && requested !== "elevenlabs" && requested !== "edge") {

// AFTER:
if (
  requested !== "openai" &&
  requested !== "elevenlabs" &&
  requested !== "edge" &&
  requested !== "smallestai"
) {
```

And update the Usage line:
```typescript
`Usage: /tts provider openai | elevenlabs | edge | smallestai`,
```

### 10. Schema help metadata

**File: `src/config/schema.help.ts`**

Add help text for `messages.tts.smallestai` fields. Find the TTS section (around line 1350) and add entries for the new fields:

```typescript
"messages.tts.smallestai":
  "Smallest AI (Lightning) TTS provider configuration for ultra-fast voice synthesis. Requires a Smallest AI API key from waves.smallest.ai.",
"messages.tts.smallestai.apiKey":
  "Smallest AI API key for authenticating TTS requests. Obtain from https://waves.smallest.ai.",
"messages.tts.smallestai.baseUrl":
  "Custom base URL for Smallest AI API requests. Override only for on-premise or proxy deployments.",
"messages.tts.smallestai.voiceId":
  "Voice identifier for Smallest AI TTS. Available voices: emily, jasmine, arman, arnav, mithali.",
"messages.tts.smallestai.model":
  "Smallest AI TTS model identifier. Default: lightning-v3.1.",
"messages.tts.smallestai.sampleRate":
  "Audio sample rate in Hz for Smallest AI TTS output. Supported: 8000, 16000, 24000, 48000.",
"messages.tts.smallestai.speed":
  "Playback speed for Smallest AI TTS (0.5-2.0, default 1.0).",
"messages.tts.smallestai.language":
  "ISO 639-1 language code for Smallest AI TTS (default: en). Supports 30+ languages.",
```

### 11. Schema labels

**File: `src/config/schema.labels.ts`**

Add around line 686:
```typescript
"messages.tts.smallestai": "Smallest AI TTS",
```

---

## Configuration Example

After implementation, users configure Smallest AI in `openclaw.json`:

```json
{
  "messages": {
    "tts": {
      "provider": "smallestai",
      "smallestai": {
        "apiKey": { "$env": "SMALLEST_API_KEY" },
        "voiceId": "emily",
        "speed": 1.0,
        "language": "en",
        "sampleRate": 24000
      }
    }
  }
}
```

Or minimally (with env var fallback):
```json
{
  "messages": {
    "tts": {
      "provider": "smallestai"
    }
  }
}
```
With `SMALLEST_API_KEY` set in the environment.

---

## Testing Approach

### Unit Tests to Add

**File: `src/tts/tts.test.ts`**

1. **Config resolution tests:**
   ```typescript
   describe("resolveTtsConfig smallestai", () => {
     it("resolves smallestai defaults when no config provided", () => {
       const cfg: OpenClawConfig = {
         agents: { defaults: { model: { primary: "openai/gpt-4o-mini" } } },
         messages: { tts: {} },
       };
       const config = resolveTtsConfig(cfg);
       expect(config.smallestai.baseUrl).toBe("https://api.smallest.ai");
       expect(config.smallestai.voiceId).toBe("emily");
       expect(config.smallestai.model).toBe("lightning-v3.1");
       expect(config.smallestai.sampleRate).toBe(24000);
       expect(config.smallestai.language).toBe("en");
     });

     it("resolves smallestai config overrides", () => {
       const cfg: OpenClawConfig = {
         agents: { defaults: { model: { primary: "openai/gpt-4o-mini" } } },
         messages: {
           tts: {
             smallestai: {
               voiceId: "arman",
               speed: 1.5,
               language: "hi",
               sampleRate: 16000,
             },
           },
         },
       };
       const config = resolveTtsConfig(cfg);
       expect(config.smallestai.voiceId).toBe("arman");
       expect(config.smallestai.speed).toBe(1.5);
       expect(config.smallestai.language).toBe("hi");
       expect(config.smallestai.sampleRate).toBe(16000);
     });
   });
   ```

2. **API key resolution tests:**
   ```typescript
   describe("resolveTtsApiKey smallestai", () => {
     it("resolves from config", () => {
       // test with config.smallestai.apiKey set
     });

     it("falls back to SMALLEST_API_KEY env var", () => {
       // test with env var
     });
   });
   ```

3. **Provider auto-detection tests:**
   ```typescript
   it("auto-selects smallestai when SMALLEST_API_KEY is set and no other keys", () => {
     // Need to update getTtsProvider() to include smallestai detection
   });
   ```

4. **Directive parsing tests:**
   ```typescript
   it("accepts smallestai as provider override", () => {
     const policy = resolveModelOverridePolicy({ enabled: true, allowProvider: true });
     const input = "Hello [[tts:provider=smallestai]] world";
     const result = parseTtsDirectives(input, policy);
     expect(result.overrides.provider).toBe("smallestai");
   });
   ```

**File: `src/config/zod-schema.tts.test.ts`**

Add tests for the schema validation:
```typescript
it("accepts smallestai configuration", () => {
  expect(() =>
    TtsConfigSchema.parse({
      provider: "smallestai",
      smallestai: {
        voiceId: "emily",
        speed: 1.0,
        sampleRate: 24000,
        language: "en",
      },
    }),
  ).not.toThrow();
});

it("rejects out-of-range smallestai speed", () => {
  expect(() =>
    TtsConfigSchema.parse({
      smallestai: { speed: 5.0 },
    }),
  ).toThrow();
});

it("rejects out-of-range smallestai sampleRate", () => {
  expect(() =>
    TtsConfigSchema.parse({
      smallestai: { sampleRate: 100 },
    }),
  ).toThrow();
});
```

### Manual Testing

1. Set `SMALLEST_API_KEY` in your environment
2. Configure `openclaw.json` with `provider: "smallestai"`
3. Test via gateway:
   - `/tts status` -- should show `smallestai` as provider
   - `/tts provider smallestai` -- should switch provider
   - `/tts audio Hello from Smallest AI` -- should generate audio
   - `/tts providers` -- should list Smallest AI with configured status
4. Test fallback: remove Smallest AI key, set as primary -- should fall back to other providers
5. Test telephony path if voice-call extension is available

---

## Files Summary (Complete Checklist)

| # | File | Change |
|---|------|--------|
| 1 | `src/config/types.tts.ts` | Add `"smallestai"` to TtsProvider union; add smallestai config type to TtsConfig |
| 2 | `src/config/zod-schema.core.ts` | Add `"smallestai"` to TtsProviderSchema enum; add smallestai Zod object to TtsConfigSchema |
| 3 | `src/tts/tts.ts` | Add defaults, config resolution, API key resolution, provider list, textToSpeech branch, telephony branch, directive override type |
| 4 | `src/tts/tts-core.ts` | Add `smallestaiTTS()` function, voice validation, directive parsing for smallestai, export new functions |
| 5 | `src/secrets/target-registry-data.ts` | Add `messages.tts.smallestai.apiKey` and Discord voice variants |
| 6 | `src/secrets/runtime-config-collectors-tts.ts` | Add smallestai API key collector |
| 7 | `src/gateway/server-methods/tts.ts` | Add Smallest AI to providers list, setProvider validation, status key check |
| 8 | `src/auto-reply/reply/commands-tts.ts` | Add Smallest AI to /tts help, provider command validation and display |
| 9 | `src/config/schema.help.ts` | Add help text for messages.tts.smallestai.* fields |
| 10 | `src/config/schema.labels.ts` | Add label for messages.tts.smallestai |
| 11 | `src/tts/tts.test.ts` | Add unit tests for config resolution, API key resolution, directive parsing |
| 12 | `src/config/zod-schema.tts.test.ts` | Add schema validation tests for smallestai config |

---

## Provider Auto-Detection Note

In `getTtsProvider()` (tts.ts line ~449-465), the current logic auto-selects providers based on available API keys when no explicit provider is configured:

```typescript
if (resolveTtsApiKey(config, "openai")) return "openai";
if (resolveTtsApiKey(config, "elevenlabs")) return "elevenlabs";
return "edge";
```

We should add Smallest AI detection. The question is priority order. Since Smallest AI is optimized for speed, it could go before or after the existing providers. A reasonable default is after elevenlabs but before edge:

```typescript
if (resolveTtsApiKey(config, "openai")) return "openai";
if (resolveTtsApiKey(config, "elevenlabs")) return "elevenlabs";
if (resolveTtsApiKey(config, "smallestai")) return "smallestai";
return "edge";
```

---

## Output Format Considerations

Smallest AI returns WAV audio. Unlike ElevenLabs/OpenAI which can output mp3/opus directly:

- **Standard channels (Discord, web):** WAV works fine as a media attachment
- **Voice-bubble channels (Telegram, WhatsApp, Feishu):** These prefer opus for compact voice notes. WAV will still work as a regular audio attachment (not as a native voice bubble). If opus voice-bubble support is needed later, a WAV-to-opus transcoding step could be added.
- **Telephony:** Use `add_wav_header: false` to get raw PCM, which is what the telephony pipeline expects.

---

## PR Submission Notes

**Branch naming:** `feat/tts-smallestai-provider`

**PR title:** `feat(tts): add Smallest AI (Lightning) as native TTS provider`

**PR description should include:**
- Summary of the new provider
- Link to Smallest AI docs (https://waves-docs.smallest.ai)
- Config example
- List of all changed files
- Test results
- Note that STT (Pulse) integration is planned for a follow-up PR

**Before submitting:**
```bash
pnpm build && pnpm check && pnpm test
```

**Review considerations per CONTRIBUTING.md:**
- Keep the PR focused on TTS only (no STT in first PR)
- Respond to bot review conversations
- Include test evidence
- Follow alphabetical ordering for providers in docs/UI lists (edge, elevenlabs, openai, smallestai)

**Important codebase patterns to follow:**
- All Zod schemas use `.strict()` to reject unknown keys
- SecretInput fields use `SecretInputSchema.optional().register(sensitive)`
- Error messages follow the pattern `Provider Name API error (STATUS_CODE)`
- Temp files use `resolvePreferredOpenClawTmpDir()` and `scheduleCleanup()`
- Test files are colocated (same directory as source)
- Tests use vitest (`describe`, `it`, `expect`, `vi.mock`)

---

## Future Work (NOT in this PR)

1. **STT (Pulse):** Add Smallest AI as an audio understanding provider under `tools.media.audio.models`
2. **Voice cloning:** Support custom voice IDs from the Smallest AI console
3. **Talk mode:** Add Smallest AI as a Talk (live voice call) provider alongside ElevenLabs
4. **Streaming TTS:** Use the WebSocket endpoint (`wss://api.smallest.ai/waves/v1/lightning-v3.1/get_speech/stream`) for real-time audio streaming in voice calls
5. **Opus output:** Add optional WAV-to-opus transcoding for voice-bubble compatibility on Telegram/WhatsApp
