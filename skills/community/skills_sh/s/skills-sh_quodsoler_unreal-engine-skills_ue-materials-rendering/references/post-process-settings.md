# Post-Process Settings Reference

`FPostProcessSettings` fields accessible from C++, grouped by category. Every field requires its paired `bOverride_*` bool to be `true` to take effect when set on a `APostProcessVolume` or `UPostProcessComponent`.

Source: `Engine/Source/Runtime/Engine/Classes/Engine/Scene.h`

---

## Usage Pattern

```cpp
// Always set the override bool alongside the value:
PPV->Settings.bOverride_BloomIntensity = true;
PPV->Settings.BloomIntensity = 1.5f;

// Setting the value without the override has no effect.
PPV->Settings.BloomIntensity = 1.5f; // silent no-op if bOverride_BloomIntensity is false
```

---

## Bloom

Controls the glow around bright light sources.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_BloomMethod` | bool | false | Enable method override |
| `BloomMethod` | EBloomMethod | `BM_SOG` | `BM_SOG` (Gaussian Sum) or `BM_FFT` (Convolution) |
| `bOverride_BloomIntensity` | bool | false | |
| `BloomIntensity` | float | 0.675 | Overall bloom brightness multiplier. 0 = off |
| `bOverride_BloomThreshold` | bool | false | |
| `BloomThreshold` | float | -1.0 | Luminance threshold for bloom. -1 = all pixels |
| `bOverride_BloomSizeScale` | bool | false | |
| `BloomSizeScale` | float | 4.0 | Scale for all Gaussian bloom kernel sizes |

**Visual effect:** Increasing `BloomIntensity` above 1.0 creates a dreamy glow around bright elements (windows, neon signs, fire). Setting `BloomThreshold` to 1.0 restricts bloom to pixels brighter than 1.0 linear, which is more physically accurate.

---

## Exposure (Auto Exposure / Eye Adaptation)

Controls how the camera adapts to scene brightness.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_AutoExposureMethod` | bool | false | |
| `AutoExposureMethod` | EAutoExposureMethod | `AEM_Histogram` | `AEM_Histogram` (high quality) or `AEM_Basic` (faster) |
| `bOverride_AutoExposureMinBrightness` | bool | false | |
| `AutoExposureMinBrightness` | float | 0.03 | Minimum scene luminance exposure adapts to (EV100 units) |
| `bOverride_AutoExposureMaxBrightness` | bool | false | |
| `AutoExposureMaxBrightness` | float | 8.0 | Maximum scene luminance exposure adapts to (EV100 units) |
| `bOverride_AutoExposureBias` | bool | false | |
| `AutoExposureBias` | float | 0.0 | Manual exposure offset in EV (exposure value). Positive = brighter |
| `bOverride_AutoExposureSpeedUp` | bool | false | |
| `AutoExposureSpeedUp` | float | 3.0 | Adaptation speed when moving to brighter scene (EV/sec) |
| `bOverride_AutoExposureSpeedDown` | bool | false | |
| `AutoExposureSpeedDown` | float | 1.0 | Adaptation speed when moving to darker scene (EV/sec) |
| `bOverride_AutoExposureLowPercent` | bool | false | |
| `AutoExposureLowPercent` | float | 80.0 | Histogram low percentile for metering (0–100) |
| `bOverride_AutoExposureHighPercent` | bool | false | |
| `AutoExposureHighPercent` | float | 98.3 | Histogram high percentile for metering (0–100) |

**Fixed exposure (override eye adaptation):**
```cpp
// Lock exposure to a fixed EV100 value — disables adaptation
PPV->Settings.bOverride_AutoExposureMethod = true;
PPV->Settings.AutoExposureMethod = AEM_Manual;
PPV->Settings.bOverride_AutoExposureBias = true;
PPV->Settings.AutoExposureBias = 0.0f; // EV100 = 0 is "neutral" daylight
```

**Visual effect:** `AutoExposureBias` of +1 doubles perceived brightness; -1 halves it. Narrowing the Min/Max range prevents wild brightness swings in high-contrast scenes.

---

## Depth of Field (Cinematic DOF)

Blurs out-of-focus objects to simulate camera aperture. Requires Cinematic DOF method.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_DepthOfFieldFstop` | bool | false | |
| `DepthOfFieldFstop` | float | 4.0 | Aperture in f-stops. Lower = more blur (f/1.4 = very shallow DOF) |
| `bOverride_DepthOfFieldMinFstop` | bool | false | |
| `DepthOfFieldMinFstop` | float | 1.2 | Minimum aperture clamp |
| `bOverride_DepthOfFieldBladeCount` | bool | false | |
| `DepthOfFieldBladeCount` | int32 | 5 | Aperture blade count (affects bokeh shape) |
| `bOverride_DepthOfFieldFocalDistance` | bool | false | |
| `DepthOfFieldFocalDistance` | float | 1000.0 | In-focus distance from camera (cm) |
| `bOverride_DepthOfFieldSensorWidth` | bool | false | |
| `DepthOfFieldSensorWidth` | float | 24.576 | Sensor width in mm (affects DOF calculation) |
| `bOverride_DepthOfFieldDepthBlurRadius` | bool | false | |
| `DepthOfFieldDepthBlurRadius` | float | 0.0 | Gaussian blur radius at 1m distance (0 = off) |
| `bOverride_DepthOfFieldDepthBlurAmount` | bool | false | |
| `DepthOfFieldDepthBlurAmount` | float | 1.0 | Blur amount multiplier for DepthBlurRadius |
| `bOverride_DepthOfFieldNearTransitionRegion` | bool | false | |
| `DepthOfFieldNearTransitionRegion` | float | 300.0 | Distance in front of focal plane for blur transition (cm) |
| `bOverride_DepthOfFieldFarTransitionRegion` | bool | false | |
| `DepthOfFieldFarTransitionRegion` | float | 500.0 | Distance behind focal plane for blur transition (cm) |

**Visual effect:** `DepthOfFieldFstop = 1.4` with `DepthOfFieldFocalDistance = 200` (2m) creates a very cinematic portrait-style shallow depth of field. `Fstop = 22` produces near-infinite focus.

---

## Color Grading

Adjusts the final image colors. Applied in linear light before tonemapping.

| Field | Type | Description |
|-------|------|-------------|
| `bOverride_ColorSaturation` | bool | |
| `ColorSaturation` | FVector4 | Per-channel saturation (RGBA). Default = (1,1,1,1) |
| `bOverride_ColorContrast` | bool | |
| `ColorContrast` | FVector4 | Per-channel contrast. Default = (1,1,1,1) |
| `bOverride_ColorGamma` | bool | |
| `ColorGamma` | FVector4 | Gamma correction per channel. Default = (1,1,1,1) |
| `bOverride_ColorGain` | bool | |
| `ColorGain` | FVector4 | Multiplier per channel. Default = (1,1,1,1) |
| `bOverride_ColorOffset` | bool | |
| `ColorOffset` | FVector4 | Additive offset per channel. Default = (0,0,0,0) |
| `bOverride_ColorSaturationShadows` | bool | Shadow-region saturation |
| `ColorSaturationShadows` | FVector4 | Affects only shadow tones |
| `bOverride_ColorSaturationMidtones` | bool | Midtone-region saturation |
| `ColorSaturationMidtones` | FVector4 | Affects only midtones |
| `bOverride_ColorSaturationHighlights` | bool | Highlight-region saturation |
| `ColorSaturationHighlights` | FVector4 | Affects only highlights |

```cpp
// Desaturate shadows (classic film noir / horror look)
PPV->Settings.bOverride_ColorSaturationShadows = true;
PPV->Settings.ColorSaturationShadows = FVector4(0.5f, 0.5f, 0.5f, 1.0f);

// Teal-orange grade — boost blue-greens in shadows, warm up highlights
PPV->Settings.bOverride_ColorOffsetShadows = true;
PPV->Settings.ColorOffsetShadows = FVector4(0.0f, 0.01f, 0.02f, 0.0f); // slight blue push in shadows
PPV->Settings.bOverride_ColorGainHighlights = true;
PPV->Settings.ColorGainHighlights = FVector4(1.05f, 0.98f, 0.9f, 1.0f);  // warm highlights
```

**Visual effect:** `ColorSaturation = FVector4(0,0,0,1)` produces full greyscale. The W (alpha) component of these vectors is a master scale applied equally to RGB.

---

## Vignette

Darkens edges of the screen.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_VignetteIntensity` | bool | false | |
| `VignetteIntensity` | float | 0.4 | 0 = no vignette, 1 = strong dark edges |

---

## Film Grain

Adds photographic grain to the final image.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_FilmGrainIntensity` | bool | false | |
| `FilmGrainIntensity` | float | 0.0 | Overall grain strength |
| `bOverride_FilmGrainIntensityShadows` | bool | false | |
| `FilmGrainIntensityShadows` | float | 1.0 | Grain intensity in shadow regions |
| `bOverride_FilmGrainIntensityMidtones` | bool | false | |
| `FilmGrainIntensityMidtones` | float | 1.0 | Grain intensity in midtone regions |
| `bOverride_FilmGrainIntensityHighlights` | bool | false | |
| `FilmGrainIntensityHighlights` | float | 1.0 | Grain intensity in highlight regions |
| `bOverride_FilmGrainShadowsMax` | bool | false | |
| `FilmGrainShadowsMax` | float | 0.09 | Maximum luminance where shadows grain applies |
| `bOverride_FilmGrainHighlightsMin` | bool | false | |
| `FilmGrainHighlightsMin` | float | 0.5 | Minimum luminance where highlights grain applies |

---

## Ambient Occlusion (SSAO)

Screen-space approximation of ambient occlusion (shadowing in crevices and corners).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_AmbientOcclusionIntensity` | bool | false | |
| `AmbientOcclusionIntensity` | float | 0.5 | 0 = off, 1 = full AO |
| `bOverride_AmbientOcclusionRadius` | bool | false | |
| `AmbientOcclusionRadius` | float | 200.0 | World-space sample radius in cm |
| `bOverride_AmbientOcclusionRadiusInWS` | bool | false | |
| `AmbientOcclusionRadiusInWS` | bool | false | If true, Radius is world-space cm; else view-space |
| `bOverride_AmbientOcclusionBias` | bool | false | |
| `AmbientOcclusionBias` | float | 3.0 | Bias to avoid self-occlusion on surfaces |
| `bOverride_AmbientOcclusionPower` | bool | false | |
| `AmbientOcclusionPower` | float | 2.0 | Power applied to AO result; higher = more contrast |
| `bOverride_AmbientOcclusionQuality` | bool | false | |
| `AmbientOcclusionQuality` | float | 50.0 | 0–100; number of samples |

**Visual effect:** AO adds subtle shadowing where surfaces meet, grounding objects and adding depth. Increase `Radius` for large architectural scenes; decrease for small props.

---

## Lumen Global Illumination and Reflections (UE5)

Lumen replaces SSAO, SSGI, and SSR for high-quality GI and reflections.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_LumenSceneDetail` | bool | false | |
| `LumenSceneDetail` | float | 1.0 | Surface cache resolution scale. Higher = better quality, higher cost |
| `bOverride_LumenSceneLightingQuality` | bool | false | |
| `LumenSceneLightingQuality` | float | 1.0 | Lighting pass quality. Range 0–4 |
| `bOverride_LumenSceneLightingUpdateSpeed` | bool | false | |
| `LumenSceneLightingUpdateSpeed` | float | 1.0 | How quickly scene lighting updates propagate |
| `bOverride_LumenFinalGatherQuality` | bool | false | |
| `LumenFinalGatherQuality` | float | 1.0 | GI final gather quality. Range 0–4 |
| `bOverride_LumenFinalGatherLightingUpdateSpeed` | bool | false | |
| `LumenFinalGatherLightingUpdateSpeed` | float | 1.0 | Update speed for final gather lighting |
| `bOverride_LumenMaxTraceDistance` | bool | false | |
| `LumenMaxTraceDistance` | float | 20000.0 | Maximum ray trace distance in cm |
| `bOverride_LumenReflectionQuality` | bool | false | |
| `LumenReflectionQuality` | float | 1.0 | Reflection quality. Range 0–4 |
| `bOverride_LumenRayLightingMode` | bool | false | |
| `LumenRayLightingMode` | ELumenRayLightingModeOverride | Default | `Default`, `SurfaceCache`, `HitLighting` |

**Visual effect:**
- Increasing `LumenSceneDetail` to 2–4 improves interior scenes where cache misses cause splotchy GI.
- `LumenReflectionQuality = 2+` with `HitLighting` mode gives accurate mirror-like reflections at higher cost.
- `LumenMaxTraceDistance` controls the effective GI range — reduce for indoor-only scenes to save performance.

---

## Screen Space Global Illumination (SSGI, non-Lumen)

Available when Lumen is disabled. Screen-space only.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_ScreenSpaceReflectionIntensity` | bool | false | |
| `ScreenSpaceReflectionIntensity` | float | 100.0 | SSR strength (0 = off) |
| `bOverride_ScreenSpaceReflectionQuality` | bool | false | |
| `ScreenSpaceReflectionQuality` | float | 50.0 | SSR sample count (0–100) |
| `bOverride_ScreenSpaceReflectionMaxRoughness` | bool | false | |
| `ScreenSpaceReflectionMaxRoughness` | float | 0.6 | Max roughness for SSR (0–1) |

---

## Motion Blur

Blurs moving objects proportional to velocity.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_MotionBlurAmount` | bool | false | |
| `MotionBlurAmount` | float | 0.5 | Blur strength (0 = off) |
| `bOverride_MotionBlurMax` | bool | false | |
| `MotionBlurMax` | float | 5.0 | Maximum blur length as percentage of screen width |
| `bOverride_MotionBlurTargetFPS` | bool | false | |
| `MotionBlurTargetFPS` | int32 | 30 | Target FPS for motion blur normalization |
| `bOverride_MotionBlurPerObjectSize` | bool | false | |
| `MotionBlurPerObjectSize` | float | 0.5 | Threshold for per-object motion blur |

---

## Chromatic Aberration

Simulates lens color fringing (RGB channel separation at screen edges).

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_SceneFringeIntensity` | bool | false | |
| `SceneFringeIntensity` | float | 0.0 | 0 = off, 5.0 = visible fringe |
| `bOverride_ChromaticAberrationStartOffset` | bool | false | |
| `ChromaticAberrationStartOffset` | float | 0.0 | Radial start position (0 = center, 1 = edge) |

---

## Camera Lens (Dirt Mask and Lens Flares)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bOverride_LensFlareIntensity` | bool | false | |
| `LensFlareIntensity` | float | 1.0 | Streak/flare strength around bright sources |
| `bOverride_LensFlareBokehSize` | bool | false | |
| `LensFlareBokehSize` | float | 3.0 | Bokeh lens flare size |
| `bOverride_LensFlareThreshold` | bool | false | |
| `LensFlareThreshold` | float | 8.0 | Luminance threshold for lens flares |
| `bOverride_BloomDirtMaskIntensity` | bool | false | |
| `BloomDirtMaskIntensity` | float | 0.0 | Camera lens dirt over bloom |
| `bOverride_BloomDirtMask` | bool | false | |
| `BloomDirtMask` | `UTexture*` | nullptr | Dirt mask texture |

---

## Post-Process Materials (Blendables)

Post-process materials are added via the volume's blendable array:

```cpp
// Material Domain must be set to "Post Process" in material editor.
PPV->AddOrUpdateBlendable(PostProcessMaterial, 1.0f);

// Via Settings directly (typed):
PPV->Settings.AddBlendable(PostProcessMaterial, 0.5f);

// Weighted blend — weight 0 = invisible, 1 = full effect
// Multiple blendables are composited in array order.
```

Blendable priorities within the post-process pipeline:
1. Scene Color (before tone mapping) — use `Blendable Location: Before Tonemapping`
2. After Tone Mapping — use `Blendable Location: After Tonemapping`
3. SSR input — special location for SSR replacement

---

## Volume Priority and Blending

Multiple overlapping volumes blend based on:

1. **Priority** — higher value wins when fully inside. Undefined order on tie.
2. **BlendWeight** — 0 to 1; partial effect weight.
3. **BlendRadius** — world-space distance from volume boundary where blend transitions.
4. **bUnbound** — if true, volume applies everywhere (lowest effective priority among unbounded volumes unless Priority is set high).

```cpp
// Two volumes overlapping: the one with Priority = 10 overrides Priority = 1
// for all properties both have bOverride set.

PPVBackground->Priority = 1;
PPVDanger->Priority = 10;
```

Blend order from source documentation: the camera's final post-process settings are accumulated from lowest to highest priority, with each higher-priority volume blending over lower-priority settings according to BlendWeight.

---

## Common Presets (C++ Snippets)

### Horror / Dark Atmosphere

```cpp
auto& S = PPV->Settings;

S.bOverride_BloomIntensity = true;       S.BloomIntensity = 0.2f;
S.bOverride_VignetteIntensity = true;    S.VignetteIntensity = 1.0f;
S.bOverride_ColorSaturation = true;      S.ColorSaturation = FVector4(0.6f, 0.6f, 0.6f, 1.0f);
S.bOverride_AutoExposureMinBrightness = true; S.AutoExposureMinBrightness = 0.01f;
S.bOverride_AutoExposureMaxBrightness = true; S.AutoExposureMaxBrightness = 1.0f;
S.bOverride_FilmGrainIntensity = true;   S.FilmGrainIntensity = 0.8f;
```

### High-Contrast Cinematic

```cpp
auto& S = PPV->Settings;

S.bOverride_BloomIntensity = true;       S.BloomIntensity = 0.5f;
S.bOverride_ColorContrast = true;        S.ColorContrast = FVector4(1.3f, 1.3f, 1.3f, 1.0f);
S.bOverride_ColorSaturation = true;      S.ColorSaturation = FVector4(1.2f, 1.2f, 1.2f, 1.0f);
S.bOverride_DepthOfFieldFstop = true;    S.DepthOfFieldFstop = 2.0f;
S.bOverride_DepthOfFieldFocalDistance = true; S.DepthOfFieldFocalDistance = 500.0f;
S.bOverride_MotionBlurAmount = true;     S.MotionBlurAmount = 0.4f;
```

### Sci-Fi / Tech UI Overlay

```cpp
auto& S = PPV->Settings;

S.bOverride_BloomIntensity = true;      S.BloomIntensity = 2.0f;
S.bOverride_SceneFringeIntensity = true; S.SceneFringeIntensity = 2.0f;
S.bOverride_ColorSaturationHighlights = true;
S.ColorSaturationHighlights = FVector4(0.7f, 1.2f, 1.4f, 1.0f); // teal highlights
S.bOverride_VignetteIntensity = true;   S.VignetteIntensity = 0.6f;
```

### Disable All Post-Process (Performance / Mobile)

```cpp
// Set BlendWeight to 0 to suppress all post-process from a volume
PPV->BlendWeight = 0.0f;

// Or disable entirely
PPV->bEnabled = false;
```
