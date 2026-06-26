---
name: fashion-model-photography
description: Generate professional fashion photography with models wearing products, including pose direction, styling, lighting, and composition for editorial and commercial use. Use for garment shoots, accessory photography, and high-end fashion content.
license: Apache-2.0
metadata:
  author: ShopOS
  version: "1.0"
  category: image-generation
  source: workflow_accessories_shoot/usecases/jewellery_photoshoot.py
  requires: image-generation-tool
---

# Fashion Model Photography

## When to Use This Skill

Use this skill when you need to:
- Create professional fashion photography for campaigns
- Generate editorial-style product imagery
- Produce high-end fashion content for marketing
- Create lookbook and catalog photography
- Generate model shots for jewelry, accessories, or garments
- Produce fashion content with specific styling and mood
- Create aspirational brand imagery

## Core Concepts

### Fashion Photography vs Product Photography

**Fashion Photography:**
- Model as integral part of composition
- Emphasis on styling, mood, and brand story
- Editorial quality with artistic direction
- Sophisticated lighting and composition
- Aspirational and emotionally engaging

**Product Photography:**
- Product as sole focus
- Clean, clear product representation
- Functional, informational purpose
- Straightforward lighting
- Purchase decision support

This skill focuses on **fashion photography** where model and styling create brand narrative.

### Key Elements

1. **Model Direction**: Pose, expression, body language
2. **Styling**: Complete look including garments, accessories, hair, makeup
3. **Lighting**: Professional editorial lighting setups
4. **Composition**: Sophisticated framing and visual hierarchy
5. **Mood**: Emotional tone and brand personality
6. **Technical Excellence**: Professional photography standards

## Step-by-Step Instructions

### Step 1: Define Model Specifications

**Demographics:**
- Origin/Ethnicity (specific, not generic)
- Gender
- Age range (specific, e.g., "24-28 years")
- Body type (athletic, slim, curvy, plus-size, muscular)
- Height category (petite, average, tall)

**Appearance:**
- Skin tone (specific description with undertones)
- Hair (color, style, length, texture)
- Facial features (natural, defined, soft, angular)
- Expression (genuine warmth, contemplative, confident, serene)
- Makeup level (natural, elevated natural, editorial)

### Step 2: Direct Pose and Body Language

**Pose Principles:**
- Asymmetrical posture (weight on one leg)
- Organic head angles (non-frontal, three-quarter)
- Natural gestures implying movement
- Loose, relaxed body language
- Product-appropriate positioning
- "Mid-breath" authentic moments

**For Garments:**
- Hands in pockets, adjusting collar, natural arm positions
- Walking stride, standing with weight shift, seated casual
- Dynamic movement, turning, mid-step

**For Accessories:**
- Delicate hand positioning for jewelry
- Natural carrying for bags
- Graceful neck articulation for necklaces/earrings
- Casual stance for footwear

**Avoid:**
- Rigid, symmetrical poses
- Forced, unnatural expressions
- Overly styled catalog positions
- Blank stares or fake smiles

### Step 3: Style the Complete Look

**Garment Coordination:**
- Featured product as hero piece
- Complementary garments based on product analysis
- Premium fabrics (silk, cashmere, linen, quality cotton)
- Modern sophisticated cuts
- Muted elegant tones that don't compete

**Accessories:**
- Minimal, statement, or none (based on product)
- Jewelry-first or product-first approach
- Appropriate to styling concept

**Hair and Makeup:**
- Elevated natural for most fashion photography
- Subtle luminous glow, defined features
- Visible healthy skin texture (not over-smoothed)
- Hair styled to complement product (updos for earrings, down for necklaces)

**Fabric Behavior:**
- Organic folds with drape tension
- Natural movement and flow
- Realistic wrinkles and texture

### Step 4: Design Lighting Setup

**Lighting Styles:**
- Directional editorial with nuanced gradients
- Soft diffused for natural beauty
- Hard directional for drama and edge
- Natural outdoor for authentic feel
- Studio with controlled shadows

**Key Light:**
- Angled for face and product contouring
- Creates dimension and depth
- Preserves skin texture
- Enhances product details without flare

**Shadow Behavior:**
- Soft-edged for natural feel
- Hard-edged for dramatic impact
- Volumetric shadows suggesting depth
- Implies recent motion or dimension

**Avoid:**
- Flat frontal lighting
- Perfectly even illumination
- Harsh backlighting washing out details
- Glare on product surfaces

### Step 5: Compose the Frame

**Framing:**
- Product-led composition (not head-biased)
- Intimate/closer framing for jewelry emphasis
- Medium shot for garments (model fills 60-70%)
- Full body for complete looks
- Minimize distant environmental shots

**Composition Rules:**
- Rule of thirds for dynamic balance
- Off-kilter balance for interest
- Negative space for breathing room
- Golden ratio for organic flow
- Centered for minimalist impact

**Camera Specs:**
- Professional DSLR or medium format
- 50mm, 85mm, or 35mm lens (based on shot type)
- f/2.8 to f/5.6 for depth control
- Eye-level or intentional angle variation

### Step 6: Set Environment and Background

**Studio:**
- Textured backdrops (not plain white/grey)
- Materials: marble, terracotta, linen, wood, botanical
- Color: complementary to product and model
- Sophisticated, curated environments

**Lifestyle:**
- Urban, indoor, or outdoor contexts
- Architectural elements and textures
- Natural materials and surfaces
- Atmospheric depth

### Step 7: Construct Fashion Photography Prompt

```
Professional fashion photography of [MODEL DESCRIPTION] wearing [PRODUCT].

SCENE: [Environment with specific details and atmosphere]

MODEL SPECIFICATIONS:
- Origin: [Specific ethnicity]
- Gender: [Male/Female/Non-binary]
- Age: [Specific range]
- Body Type: [Specific description]
- Height: [Petite/Average/Tall with specifics]
- Skin Tone: [Detailed description with undertones]
- Hair: [Color, style, length, texture]
- Expression: [Specific emotional quality - genuine, not forced]
- Appearance: [Facial features, natural characteristics]
- Makeup: [Elevated natural/editorial with specific details]

POSE AND BODY LANGUAGE:
[Detailed asymmetrical pose description]
[Specific positioning for product visibility]
[Natural gesture or implied movement]
[Head angle and gaze direction]

STYLING:
- Main Product: [Exact product from reference image]
- [Complementary garments with specific details]
- Footwear: [Specific style and color]
- Accessories: [Minimal/statement/none with specifics]
- Fabric Behavior: [How garments drape and move]

PHOTOGRAPHY TECHNICAL:
- Camera: [Professional setup - DSLR/medium format]
- Lens: [Specific focal length]
- Aperture: [f-stop for desired depth]
- Lighting: [Specific setup - direction, quality, color temp]
- Composition: [Framing approach and rule application]
- Angle: [Eye-level/low/high with specifics]
- Background: [Specific environment with materials and colors]

MOOD AND ATMOSPHERE:
[Specific emotional qualities]
[Brand personality traits]
[Energy level and sophistication]

Professional fashion photography, editorial quality, [specific style keywords],
photorealistic, natural skin texture, authentic moment, 8K resolution.
```

## Examples

### Example 1: Jewelry Editorial

**Input:**
- Product: Gold chandelier earrings
- Style: Elegant, sophisticated
- Use: Editorial campaign

**Prompt:**
```
Professional fashion photography of a 28-year-old South Asian female model wearing gold chandelier earrings.

SCENE: Modern minimalist interior with warm plaster wall, soft diffused window light creating gentle gradient.

MODEL SPECIFICATIONS:
- Origin: South Asian descent
- Gender: Female
- Age: 28 years
- Body Type: Slim, elegant proportions
- Height: 5'7", graceful stature
- Skin Tone: Warm medium brown with golden undertones, natural healthy glow
- Hair: Dark brown, swept back in elegant low bun exposing neck and ears completely
- Expression: Serene confidence, contemplative gaze with subtle smile, genuine warmth
- Appearance: Refined features, defined brows, high cheekbones, natural beauty
- Makeup: Elevated natural - subtle luminous glow, defined brows and lashes, nude-rose lips, visible skin texture

POSE AND BODY LANGUAGE:
Three-quarter profile with head turned to showcase right earring prominently. Neck naturally extended with graceful articulation emphasizing earring drop. Right hand delicately touching collarbone, left arm relaxed at side. Shoulders slightly angled creating elegant diagonal line. Weight shifted to left leg, creating subtle asymmetry.

STYLING:
- Main Product: Gold chandelier drop earrings with crystal accents (from reference image)
- Garment: Off-shoulder silk charmeuse top in champagne tone, draping elegantly
- Accessories: No necklace (earrings are statement), simple gold bangle on left wrist
- Fabric Behavior: Silk drapes softly with natural sheen, gentle folds at shoulder

PHOTOGRAPHY TECHNICAL:
- Camera: Medium format digital
- Lens: 85mm portrait lens
- Aperture: f/4 for balanced depth, earrings sharp with soft background
- Lighting: Soft directional key light from left at 45 degrees, subtle fill from right, creating dimension on face and earring sparkle
- Composition: Medium shot, chest-up, model positioned on right third, negative space left
- Angle: Eye-level, slight three-quarter view
- Background: Warm plaster wall with subtle texture, soft focus, muted tones

MOOD AND ATMOSPHERE:
Elegant, sophisticated, refined, timeless grace, serene confidence, luxury without ostentation, editorial sophistication.

Professional fashion photography, editorial quality, luxury jewelry aesthetic, 
photorealistic, natural skin texture, poised authentic moment, 8K resolution.
```

### Example 2: Streetwear Fashion

**Input:**
- Product: Oversized hoodie
- Style: Urban, authentic
- Use: Social media campaign

**Prompt:**
```
Professional fashion photography of a 24-year-old African American female model wearing an oversized grey hoodie.

SCENE: Urban street setting with graffiti wall, natural overcast daylight creating even soft lighting.

MODEL SPECIFICATIONS:
- Origin: African American
- Gender: Female
- Age: 24 years
- Body Type: Athletic, strong build
- Height: 5'8", confident stature
- Skin Tone: Deep brown with warm undertones, natural healthy skin, visible texture
- Hair: Natural textured afro, full volume, authentic styling
- Expression: Confident, direct gaze with subtle attitude, genuine self-assurance
- Appearance: Strong features, natural brows, clear skin, authentic beauty
- Makeup: Minimal - natural brows, clear skin, subtle lip color, no heavy makeup

POSE AND BODY LANGUAGE:
Mid-stride walking towards camera, left foot forward, right arm swinging naturally. Hood up, hands emerging from sleeves. Dynamic movement captured mid-motion, creating energy. Head slightly tilted, direct eye contact with camera. Asymmetrical stance with weight shifting forward, implying motion and confidence.

STYLING:
- Main Product: Oversized grey cotton hoodie with drawstrings (from reference image)
- Garment: Black joggers with tapered fit, partially visible
- Footwear: High-top white sneakers, clean and fresh
- Accessories: Gold hoop earrings visible under hood, minimal
- Fabric Behavior: Hoodie drapes loosely, natural movement folds, relaxed oversized fit

PHOTOGRAPHY TECHNICAL:
- Camera: Professional DSLR, street photography style
- Lens: 35mm for environmental context
- Aperture: f/4 for subject focus with urban background context
- Lighting: Natural overcast daylight, even soft illumination, no harsh shadows
- Composition: Medium-full shot, model fills 70% of frame, dynamic diagonal
- Angle: Eye-level, straight-on with slight tilt for energy
- Background: Urban graffiti wall with vibrant colors, slightly out of focus, authentic street context

MOOD AND ATMOSPHERE:
Urban, energetic, authentic street style, confident, unapologetic, raw energy, contemporary youth culture, genuine attitude.

Professional street fashion photography, editorial quality, urban authentic aesthetic,
photorealistic, natural skin texture, captured mid-movement, dynamic energy, 8K resolution.
```

### Example 3: Luxury Fashion

**Input:**
- Product: Tailored blazer
- Style: Sophisticated, premium
- Use: Lookbook

**Prompt:**
```
Professional fashion photography of a 32-year-old European male model wearing a navy blue tailored blazer.

SCENE: Modern architectural interior with clean lines, natural light from large windows, sophisticated minimalist environment.

MODEL SPECIFICATIONS:
- Origin: European descent (Scandinavian features)
- Gender: Male
- Age: 32 years
- Body Type: Athletic, lean build with defined shoulders
- Height: 6'1", commanding presence
- Skin Tone: Fair with neutral undertones, healthy complexion, visible skin texture
- Hair: Dark blonde, short textured style with natural movement
- Expression: Confident sophistication, subtle intensity, contemplative gaze
- Appearance: Strong jawline, defined features, light stubble, refined masculine beauty
- Makeup: None (natural male grooming)

POSE AND BODY LANGUAGE:
Standing with weight on right leg, left leg slightly forward creating subtle asymmetry. Left hand in trouser pocket, right arm relaxed at side. Shoulders back, confident posture without stiffness. Head turned to three-quarter angle, gaze directed slightly off-camera with thoughtful expression. Blazer worn open, showing shirt and creating vertical lines.

STYLING:
- Main Product: Navy blue tailored blazer with modern slim fit (from reference image)
- Garment: Crisp white dress shirt, top button undone, relaxed sophistication
- Bottomwear: Charcoal grey tailored trousers, slim fit
- Footwear: Black leather oxford shoes, polished
- Accessories: Simple silver watch on left wrist, no other jewelry
- Fabric Behavior: Blazer drapes perfectly with structured shoulders, natural break at sleeves, professional tailoring visible

PHOTOGRAPHY TECHNICAL:
- Camera: Medium format digital
- Lens: 85mm portrait lens
- Aperture: f/2.8 for subject isolation with soft background
- Lighting: Natural window light from left creating soft directional illumination, subtle fill maintaining detail in shadows
- Composition: Three-quarter length shot, model fills 65% of frame, positioned on right third
- Angle: Eye-level, slight low angle adding authority
- Background: Modern architectural elements, clean lines, soft focus, neutral tones

MOOD AND ATMOSPHERE:
Sophisticated, confident, refined masculinity, contemporary luxury, understated elegance, professional authority, timeless style.

Professional fashion photography, editorial quality, luxury menswear aesthetic,
photorealistic, natural skin texture, sophisticated composition, 8K resolution.
```

## Key Principles

1. **Unposed Authenticity**: Mid-breath moments, not rigid catalog poses
2. **Product Priority**: Composition led by product, not just model's face
3. **Asymmetry**: Avoid symmetrical, frontal, rigid positioning
4. **Natural Expression**: Genuine emotion, not forced or blank
5. **Elevated Natural**: Sophisticated but not over-styled
6. **Skin Texture**: Visible pores, natural gradients, healthy glow
7. **Fashion-Forward Language**: Editorial terminology, specific details

## Common Mistakes to Avoid

- ❌ Rigid, symmetrical catalog poses
- ❌ Overly styled, artificial appearance
- ❌ Plain white/grey backgrounds (use textured)
- ❌ Flat, even lighting with no dimension
- ❌ Generic model descriptions
- ❌ Competing styling that distracts from product
- ❌ Forced product display with unnatural positioning

## Integration Pattern

```typescript
// TypeScript tool call implementation
interface FashionPhotoParams {
  productImage: string;
  productType: 'garment' | 'accessory' | 'jewelry' | 'footwear';
  modelDemographics: {
    age: number;
    gender: string;
    ethnicity: string;
    bodyType: string;
  };
  styleDirection: 'editorial' | 'commercial' | 'luxury' | 'streetwear' | 'minimalist';
  environment: 'studio' | 'urban' | 'indoor' | 'outdoor';
}

async function generateFashionPhoto(params: FashionPhotoParams) {
  // 1. Analyze product
  const productAnalysis = await analyzeProduct(params.productImage);
  
  // 2. Define model specifications
  const modelSpecs = defineModelSpecs(
    params.modelDemographics,
    productAnalysis
  );
  
  // 3. Create pose direction
  const poseDirection = createPoseDirection(
    params.productType,
    params.styleDirection
  );
  
  // 4. Design styling
  const styling = designStyling(
    productAnalysis,
    params.styleDirection
  );
  
  // 5. Set lighting and composition
  const photography = setPhotographySpecs(
    params.styleDirection,
    params.environment
  );
  
  // 6. Construct fashion prompt
  const prompt = constructFashionPrompt({
    product: productAnalysis,
    model: modelSpecs,
    pose: poseDirection,
    styling: styling,
    photography: photography
  });
  
  // 7. Generate image
  const result = await imageGenTool({
    prompt: prompt,
    images: [{ url: params.productImage, name: 'Product' }],
    aspectRatio: '2:3', // Portrait for fashion
    outputFormat: 'jpeg'
  });
  
  return result;
}
```

## Tool Definition

```typescript
// For Claude tool calling
const fashionModelPhotoTool = {
  name: 'generate_fashion_model_photo',
  description: 'Generate professional fashion photography with models wearing products, including pose direction, styling, and editorial quality',
  input_schema: {
    type: 'object',
    properties: {
      product_image: {
        type: 'string',
        description: 'URL of the product image'
      },
      product_type: {
        type: 'string',
        enum: ['garment', 'accessory', 'jewelry', 'footwear'],
        description: 'Type of product being photographed'
      },
      model_demographics: {
        type: 'object',
        properties: {
          age: { type: 'number', description: 'Model age' },
          gender: { type: 'string', description: 'Model gender' },
          ethnicity: { type: 'string', description: 'Specific ethnicity' },
          body_type: { type: 'string', description: 'Body type description' }
        },
        required: ['age', 'gender', 'ethnicity', 'body_type']
      },
      style_direction: {
        type: 'string',
        enum: ['editorial', 'commercial', 'luxury', 'streetwear', 'minimalist'],
        description: 'Fashion photography style direction'
      },
      environment: {
        type: 'string',
        enum: ['studio', 'urban', 'indoor', 'outdoor'],
        description: 'Photography environment setting'
      }
    },
    required: ['product_image', 'product_type', 'model_demographics', 'style_direction', 'environment']
  }
};
```

## References

- Source: `workflow_accessories_shoot/implementation/usecases/jewellery_photoshoot.py`
- Related Skills: product-analysis-styling, garment-lifestyle-photography
- Fashion Photography Standards: See references/fashion-standards.md
