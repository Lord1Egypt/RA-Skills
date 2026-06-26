# Ai Game Art Generation - Sharp Edges

## Stability AI $1M Revenue License Trap

### **Id**
stability-ai-license-trap
### **Severity**
critical
### **Description**
  Free use of Stable Diffusion is only for annual revenue under $1M. Enterprise license required above that threshold. Many indie devs don't realize this until they're successful.
  
### **Detection Pattern**
stabilityai|stable.*diffusion|sdxl
### **Symptoms**
  - Cease and desist letter
  - Steam store removal threat
  - Legal liability
### **Solution**
  1. Document revenue projections
  2. If expecting > $1M, contact Stability AI for enterprise license
  3. Consider FLUX or other alternatives for commercial work
  4. Maintain clear documentation of all AI tool usage
  
### **References**
  - https://stability.ai/license

## Midjourney Commercial Use Requires Paid Plan

### **Id**
midjourney-commercial-confusion
### **Severity**
high
### **Description**
  Free tier Midjourney images cannot be used commercially. Pro/Mega required if company revenue exceeds $1M. All images are PUBLIC by default (competitors see your assets).
  
### **Detection Pattern**
midjourney|mj.*prompt
### **Symptoms**
  - Copyright claim on game assets
  - Competitors copying revealed concepts
### **Solution**
  1. Never use free tier for commercial projects
  2. Enable Stealth Mode (Pro/Mega only) for confidential work
  3. Pro plan minimum for commercial game development
  4. Document license tier used for each asset
  
### **References**
  - https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service

## Steam Now Requires AI Content Disclosure

### **Id**
steam-ai-disclosure-required
### **Severity**
high
### **Description**
  As of 2024, Steam requires disclosure of ALL AI-generated content. Failure to disclose can result in store removal. ~7% of games now have AI disclosures.
  
### **Detection Pattern**
steam|publish|release
### **Symptoms**
  - Store page rejection
  - Post-launch takedown
  - Negative reviews from disclosure omission
### **Solution**
  1. Complete AI Content section in Steam Content Survey
  2. Classify as Pre-Generated or Live-Generated
  3. Describe guardrails for live generation
  4. NEVER use Adult Only Sexual Content with live AI
  
### **References**
  - https://store.steampowered.com/news/group/4145017/view/3862463747997849618

## Character Consistency Drift Across Batches

### **Id**
consistency-drift-across-batches
### **Severity**
high
### **Description**
  AI models don't maintain perfect consistency. Characters drift in appearance, especially facial features, across separate generation sessions or batches.
  
### **Detection Pattern**
character|sprite|batch|multiple
### **Symptoms**
  - Same character looks different in different scenes
  - Players notice "multiple twins" effect
  - Art feels inconsistent, amateur
### **Solution**
  1. Train custom LoRA on character reference art
  2. Use IP-Adapter with starting_control_step: 0.5
  3. Seed lock for reproducibility
  4. Generate ALL poses/expressions in single session
  5. Manual QA pass to catch outliers
  6. Keep master reference sheet for verification
  
### **Technical Detail**
  IP-Adapter acts as "single image fine-tuning" - maintains consistency better than prompt-only approaches
  

## Anatomical Failures (Six Fingers, Impossible Poses)

### **Id**
six-finger-anatomy-fails
### **Severity**
medium
### **Description**
  AI models frequently produce anatomically incorrect outputs: extra fingers, merged limbs, impossible joint angles. MIT research shows 90% of humans can detect these errors.
  
### **Detection Pattern**
character|human|hand|pose
### **Symptoms**
  - Extra or missing fingers
  - Merged limbs
  - Impossible body proportions
  - Uncanny valley effect
### **Solution**
  1. Use ControlNet with OpenPose for structured poses
  2. Generate hands separately and composite
  3. Use negative prompts: "extra fingers, deformed hands, bad anatomy"
  4. Always manually review character outputs
  5. Consider stylization that hides anatomical details
  
### **Technical Detail**
  Hand-specific LoRAs exist on Civitai that significantly improve hand generation quality
  

## Pixel Art Anti-Aliasing Artifacts

### **Id**
pixel-art-anti-aliasing-artifacts
### **Severity**
medium
### **Description**
  Standard diffusion models produce varying pixel sizes, inconsistent outlines, and anti-aliasing that destroys pixel art aesthetic. "Nearly all pixel art models have this issue."
  
### **Detection Pattern**
pixel.*art|retro|8.*bit|sprite
### **Symptoms**
  - Blurry pixels instead of crisp edges
  - Inconsistent pixel sizes in same image
  - Random noise patterns
  - Sub-pixel details that shouldn't exist
### **Solution**
  1. Use Retro Diffusion or similar specialized models
  2. Post-process with color quantization
  3. Manual cleanup of edge pixels
  4. Generate at exact target resolution (e.g., 32x32)
  5. Custom downscaling algorithms, not standard bicubic
  
### **References**
  - https://runware.ai/blog/retro-diffusion-creating-authentic-pixel-art-with-ai-at-scale

## Color Palette Chaos from Prompt Stacking

### **Id**
color-palette-chaos
### **Severity**
medium
### **Description**
  AI models interpret descriptive words statistically, not artistically. Stacking adjectives like "vibrant cinematic dreamy soft golden" creates color inconsistency as each term pulls different directions.
  
### **Detection Pattern**
vibrant|cinematic|dreamy|soft.*golden|ethereal
### **Symptoms**
  - Colors don't match across assets
  - Muddy, unfocused color schemes
  - Style feels inconsistent
### **Solution**
  1. Define explicit color palette before generation
  2. Use consistent, focused prompt vocabulary
  3. Train LoRA on reference palette
  4. Post-process to enforce palette compliance
  5. Use color reference image with IP-Adapter
  

## Visible Seams in "Tileable" Textures

### **Id**
tileable-visible-seams
### **Severity**
medium
### **Description**
  Enabling tiling option doesn't guarantee invisible seams. Patterns may technically tile but show obvious repetition when viewed in-game at scale.
  
### **Detection Pattern**
tile|seamless|texture|pattern
### **Symptoms**
  - Obvious grid pattern when tiled
  - Edge artifacts at tile boundaries
  - Player notices repetition
### **Solution**
  1. Use specialized tiling workflow (circular convolution)
  2. Generate 4 similar textures and use Seamless Stitcher
  3. Add variation overlays in-engine
  4. Test at game zoom levels, not just preview
  5. Use larger tile sizes to reduce repetition visibility
  

## VRAM Out of Memory Crashes

### **Id**
vram-oom-crashes
### **Severity**
medium
### **Description**
  Complex ComfyUI workflows with multiple ControlNets, IP-Adapter, and high resolutions can exhaust VRAM. 8GB minimum, 12GB+ recommended.
  
### **Detection Pattern**
comfyui|controlnet|ip.*adapter|batch
### **Symptoms**
  - CUDA out of memory errors
  - System freeze during generation
  - Workflow only works with tiny batch sizes
### **Solution**
  1. Use FP16/FP8 quantized models
  2. Reduce batch size to 1
  3. Lower resolution, upscale after
  4. Enable tiled VAE decode
  5. Close other GPU applications
  6. Consider cloud GPU (RunPod, etc.)
  
### **Technical Detail**
  FLUX.2 with FP8 requires 40% less VRAM than full precision
  

## Lost Assets from Missing Git LFS

### **Id**
git-lfs-missing-assets
### **Severity**
high
### **Description**
  AI generation is non-deterministic. Same prompt + seed doesn't guarantee identical output. Lost assets cannot be regenerated. Without Git LFS, large assets aren't properly tracked.
  
### **Detection Pattern**
git|version.*control|backup
### **Symptoms**
  - Binary files too large for git
  - Assets lost after branch switch
  - Cannot reproduce exact asset
### **Solution**
  1. Set up Git LFS before first generation
  2. Track all binary formats: *.png, *.jpg, *.psd, *.blend
  3. Use lockable files for unmergeable assets
  4. Document prompts + seeds + model versions
  5. Store ComfyUI workflow JSON with assets
  

## AI-Generated Assets May Not Be Copyrightable

### **Id**
copyright-unprotectable-assets
### **Severity**
medium
### **Description**
  US Copyright Office 2025: AI-generated content without meaningful human input is NOT copyrightable. Cannot prevent others from using similar imagery.
  
### **Detection Pattern**
copyright|protect|legal
### **Symptoms**
  - Cannot DMCA takedown similar assets
  - Competitors can legally use similar AI outputs
  - No exclusive ownership of asset designs
### **Solution**
  1. Add significant human modification to establish copyright
  2. Document human creative decisions
  3. Use AI as starting point, not final product
  4. Consider trademark protection for distinctive elements
  5. Protect via trade secret (don't publish prompts/methods)
  