# AI Game Art Generation

## Patterns


---
  #### **Id**
comfyui-game-asset-pipeline
  #### **Name**
ComfyUI Game Asset Pipeline
  #### **Description**
Production workflow for consistent game assets
  #### **When To Use**
Any AI-generated game art project
  #### **Structure**
    1. Define style reference (existing art or trained LoRA)
    2. Configure ControlNet for structure control
    3. Set up IP-Adapter for consistency
    4. Batch process with Image Grid node
    5. Auto background removal
    6. Export to game engine format
    
  #### **Code Example**
    # ComfyUI workflow structure (conceptual)
    workflow = {
      "LoadImage": "reference_character.png",
      "IPAdapterLoader": "ip-adapter-plus-face_sd15.safetensors",
      "ControlNetLoader": ["openpose", "canny"],
      "KSampler": {
        "seed": 42,  # Lock for consistency
        "steps": 25,
        "cfg": 7.5
      },
      "BackgroundRemoval": True,
      "ImageGrid": {"columns": 4, "rows": 4}  # Spritesheet
    }
    
  #### **Benefits**
    - Reproducible results
    - Batch capability
    - Consistent style across assets
  #### **Pitfalls**
    - Complex setup - save workflows
    - VRAM requirements (12GB+ recommended)

---
  #### **Id**
lora-training-for-games
  #### **Name**
LoRA Training for Game Styles
  #### **Description**
Train custom models for perfect style matching
  #### **When To Use**
Need exact style consistency across many assets
  #### **Structure**
    1. Collect 30-50 images for art styles (15-30 for characters)
    2. Caption with rare tokens: "drawing in skw style"
    3. Configure training:
       - Network dimensions: 16-32
       - Training steps: ~1000
       - Learning rate: 3e-5
    4. Test with sample prompts
    5. Iterate on dataset quality
    
  #### **Code Example**
    # Kohya SS LoRA training config
    training_config = {
      "pretrained_model": "stabilityai/sdxl-base-1.0",
      "output_dir": "./lora_output",
      "instance_prompt": "game asset in mygamestyle style",
      "max_train_steps": 1000,
      "learning_rate": 3e-5,
      "network_dim": 32,
      "network_alpha": 16,
      "resolution": 1024,
      "train_batch_size": 1,
    }
    
  #### **Benefits**
    - Perfect style consistency
    - Fast generation once trained
    - Unique, ownable aesthetic
  #### **Pitfalls**
    - Quality > quantity in training data
    - Overfitting if too few diverse samples

---
  #### **Id**
tileable-texture-workflow
  #### **Name**
Tileable Texture Generation
  #### **Description**
Create seamless, game-ready textures with PBR maps
  #### **When To Use**
Environment textures, materials, terrain
  #### **Structure**
    1. Enable tiling in model settings
    2. Use prompts: "seamless, tileable, repeating pattern"
    3. Generate at 512-1024px
    4. Use Seamless Stitcher for 4x resolution
    5. Generate PBR maps with Poly AI or similar
    
  #### **Code Example**
    # Tileable texture prompt template
    prompt = """
    seamless tileable {material} texture,
    photorealistic, highly detailed,
    even pattern, perfectly aligned,
    game ready, PBR material
    """
    
    # Post-process for PBR
    pbr_maps = generate_pbr_maps(
      base_color=texture,
      outputs=["normal", "height", "roughness", "ao", "metalness"]
    )
    
  #### **Benefits**
    - Infinite texture variety
    - Consistent quality
    - Full PBR pipeline
  #### **Pitfalls**
    - Check for visible seams at tile boundaries
    - Verify scale matches game world

---
  #### **Id**
character-consistency-pipeline
  #### **Name**
Character Consistency Pipeline
  #### **Description**
Generate consistent characters across multiple poses/angles
  #### **When To Use**
Character sprites, turnarounds, animation frames
  #### **Structure**
    1. Generate or select reference image
    2. Load into IP-Adapter (starting_control_step: 0.5)
    3. Use ControlNet for pose variation
    4. Seed lock for facial features
    5. Batch generate all needed poses
    6. Verify consistency, regenerate outliers
    
  #### **Code Example**
    # Scenario.com Dual Reference approach
    dual_reference_config = {
      "image_to_image_slot": "character_ref.png",  # Controls color/style
      "controlnet_slot": "character_ref.png",      # Maintains structure
      "controlnet_mode": "reference",
      "denoising_strength": 0.5  # Balance consistency vs variation
    }
    
  #### **Benefits**
    - Same character, different poses
    - Suitable for animation
    - Maintainable quality
  #### **Pitfalls**
    - Some drift inevitable - verify manually
    - Complex poses may break consistency

---
  #### **Id**
batch-asset-automation
  #### **Name**
Batch Asset Automation
  #### **Description**
Process hundreds of assets overnight
  #### **When To Use**
Large-scale asset production
  #### **Structure**
    1. Prepare CSV with all prompt variations
    2. Configure Auto Queue in ComfyUI
    3. Set random seed nodes for variation
    4. Background removal + naming pipeline
    5. Auto-export to project folders
    
  #### **Code Example**
    # Batch prompt template CSV
    # type,subject,style,variation
    enemy,goblin,fantasy,aggressive
    enemy,goblin,fantasy,defensive
    enemy,skeleton,fantasy,archer
    enemy,skeleton,fantasy,warrior
    item,sword,fantasy,common
    item,sword,fantasy,rare
    item,sword,fantasy,legendary
    
    # ComfyUI processes each row overnight
    
  #### **Benefits**
    - Unattended production
    - Consistent naming/organization
    - Massive throughput (100+ assets/night)
  #### **Pitfalls**
    - Review for quality issues in morning
    - Don't skip human curation step

---
  #### **Id**
steam-ai-disclosure-workflow
  #### **Name**
Steam AI Disclosure Compliance
  #### **Description**
Proper AI content disclosure for Steam release
  #### **When To Use**
Any Steam game with AI-generated content
  #### **Structure**
    1. Document all AI-generated assets
    2. Complete Steam Content Survey "AI Content" section
    3. Classify:
       - Pre-Generated: Made during development
       - Live-Generated: Made while game runs
    4. Describe guardrails for live generation
    5. Verify no AOSC with live-generated AI
    
  #### **Code Example**
    # Steam AI Disclosure documentation
    AI_CONTENT_DISCLOSURE = {
      "pre_generated": {
        "character_sprites": "Stable Diffusion + custom LoRA",
        "background_art": "Midjourney + manual touch-up",
        "item_icons": "DALL-E 3 + post-processing",
      },
      "live_generated": None,  # No runtime AI generation
      "legal_compliance": "All training data properly licensed",
      "no_infringing_content": True
    }
    
  #### **Benefits**
    - Steam compliance
    - Transparent with players
    - Avoids store removal
  #### **Pitfalls**
    - ~7% of Steam games now disclose AI
    - Players may review-bomb AI games

## Anti-Patterns


---
  #### **Id**
ai-slop-production
  #### **Name**
AI Slop Production
  #### **Description**
Mass-generating without quality curation
  #### **Why Bad**
    Creates generic, recognizable "AI art" that players and critics will immediately identify and criticize. Damages game perception.
    
  #### **Signs**
    - No human review step
    - Using raw generations without touch-up
    - Inconsistent styles across assets
    - Six-fingered characters, impossible anatomy
  #### **Better Approach**
    Quality over quantity. 50 curated assets beat 500 AI slop. Always have human artist refinement pass.
    

---
  #### **Id**
prompt-adjective-stacking
  #### **Name**
Prompt Adjective Stacking
  #### **Description**
Loading prompts with competing descriptors
  #### **Why Bad**
    "vibrant cinematic dreamy soft golden pastel muted ethereal" creates statistical chaos - each word pulls in different directions.
    
  #### **Example**
    BAD: "highly detailed ultra realistic dreamy fantasy vintage modern
          cinematic vibrant soft bright dark character sprite"
    
    GOOD: "fantasy warrior character, pixel art style, 32x32,
           limited palette, clean linework"
    
  #### **Better Approach**
Focused, specific prompts with consistent vocabulary

---
  #### **Id**
ignoring-license-terms
  #### **Name**
Ignoring License Terms
  #### **Description**
Using AI tools without checking commercial terms
  #### **Why Bad**
    Stability AI requires enterprise license if revenue > $1M. Midjourney requires paid plan for commercial use. Steam requires disclosure. Violations = legal risk.
    
  #### **Consequences**
    - Takedown notices
    - Store removal
    - Legal action
  #### **Better Approach**
Document all tools, verify licenses, maintain paper trail

---
  #### **Id**
no-version-control-assets
  #### **Name**
No Version Control for AI Assets
  #### **Description**
Not tracking AI assets in Git LFS
  #### **Why Bad**
    AI generation is non-deterministic. Lost assets cannot be exactly regenerated. Prompts + seeds must be documented.
    
  #### **Better Approach**
    - Git LFS for all binary assets
    - Document prompts + seeds + settings
    - Lock files to prevent overwrite
    