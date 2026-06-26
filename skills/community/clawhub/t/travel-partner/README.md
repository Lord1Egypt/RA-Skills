# Travel Partner Skill - Complete Tutorial

> AI-powered virtual travel companion that generates complete travel experiences including itineraries, photos, journals, and guides for international destinations.

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Quick Setup](#quick-setup)
3. [Complete Tutorials](#complete-tutorials)
   - [Case 1: Romantic Paris Trip](#case-1-romantic-paris-trip)
   - [Case 2: Tokyo Adventure](#case-2-tokyo-adventure)
   - [Case 3: Virtual Honeymoon](#case-3-virtual-honeymoon)
   - [Case 4: Solo Travel Content](#case-4-solo-travel-content)
4. [All Scripts Reference](#all-scripts-reference)
5. [Advanced Usage](#advanced-usage)
6. [Best Practices](#best-practices)

---

## 🎯 Overview

This skill helps you create complete virtual travel experiences for international destinations:

- ✅ **Travel Itineraries** - Day-by-day schedules with activities and photo spots
- ✅ **AI Photos** - Real travel photos generated with OpenAI DALL-E 3
- ✅ **Travel Journals** - First-person narratives from companion's perspective
- ✅ **Travel Guides** - Comprehensive guides with tips, budget, and recommendations
- ✅ **Photo Prompts** - Detailed prompts for AI image generation
- ✅ **Interesting Stories** - Fun anecdotes and cultural insights

**Perfect for:**
- Virtual travel experiences
- Social media content creation
- Travel planning inspiration
- AI companion roleplay
- Content generation for travel blogs

---

## 🚀 Quick Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Get OpenAI API Key (for photo generation)

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create account or sign in
3. Go to API Keys section
4. Create new API key
5. Copy key (starts with `sk-...`)

### Step 3: Set Environment Variables

```bash
# macOS/Linux
export OPENAI_API_KEY="your-api-key-here"

# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Note:** API key is only required for `generate_travel_image.py`. Other scripts work without it.

---

## 📖 Complete Tutorials

### Case 1: Romantic Paris Trip (5 Days)

**Goal:** Create complete Paris experience with itinerary, photos, and journal

#### Step 1.1: Generate Itinerary

```bash
python scripts/itinerary_generator.py Paris 5 romantic
```

**Output:** `paris_itinerary_5days.json`

This creates:
- 5 days of activities (5 per day)
- Times, locations, descriptions
- Photo spots for each activity
- Budget estimate: $750 - $1,500
- 25 total activities, 20 photo opportunities

#### Step 1.2: Generate Travel Photos

**Option A: Generate Single Photos**

```bash
# Eiffel Tower at sunset
python scripts/generate_travel_image.py Paris "Eiffel Tower" romantic sunset

# Louvre Museum
python scripts/generate_travel_image.py Paris "Musee du Louvre" scenic sunrise

# Montmartre
python scripts/generate_travel_image.py Paris "Montmartre" cozy night
```

**Option B: Generate from Itinerary (Batch)**

```bash
python scripts/generate_travel_image.py --itinerary paris_itinerary_5days.json
```

**Cost for 20 photos:** $0.80 (standard) or $1.60 (HD)

**Output:** `travel_photos/` folder with all images

#### Step 1.3: Generate Travel Journal

```bash
python scripts/travel_experience_generator.py Paris romantic_companion
```

**Output:**
- `paris_journal_day1.md` - Day 1 journal entry
- `paris_guide.md` - Complete travel guide
- `paris_stories.md` - Interesting stories and fun facts

#### Step 1.4: Review Generated Content

**Itinerary Example (Day 1):**
```
09:00 | Visit Eiffel Tower | 📸 Best morning shooting time
12:00 | Lunch Time | 📸 Food check-in at Left Bank cafe
14:00 | Seine River Cruise | 📸 Beautiful scenery under bright light
17:30 | Montmartre artist square | 📸 Golden hour romantic atmosphere
20:00 | Romantic French dinner | 📸 Glowing night view
```

**Journal Entry Example:**
```markdown
# Paris Travel Journal - Day 1

📅 Date: 2026-03-26
📍 Location: Paris
👤 Writer: My love, day 1 in Paris, every moment reminds me of you...

## 🌅 Morning

09:00 - **Visit Eiffel Tower**

Morning sunlight shines on Eiffel Tower, I looked up at this iron giant. 
Every floor upward, city panorama became more magnificent, 
really wish I could see this angle with you.

📸 Check-in Photo: Visit Eiffel Tower check-in - Best morning shooting time
💭 Feeling: Beginning full of anticipation, new adventures await us

...

My love, I wish you were here to see this world with me 💕
```

**Generated Photo:**
- File: `travel_photos/paris_eiffel_tower_20260319_105430.png`
- Prompt: "A stunning, high-quality travel photo of Eiffel Tower in Paris, captured during sunset..."

---

### Case 2: Tokyo Adventure (7 Days)

**Goal:** Create adventurous Tokyo experience with cultural insights

#### Step 2.1: Generate Adventure Itinerary

```bash
python scripts/itinerary_generator.py Tokyo 7 adventure
```

**Output:** `tokyo_itinerary_7days.json`

- 7 days, 35 activities
- Adventure-focused activities (shibuya crossing, teamlab, sumida river)
- Budget: $1,050 - $2,100

#### Step 2.2: Generate Cultural Photo Prompts

```bash
# Senso-ji Temple at sunrise
python scripts/generate_travel_photo.py Tokyo "Senso-ji Temple" cultural sunrise

# TeamLab digital art
python scripts/generate_travel_photo.py Tokyo "TeamLab Borderless" vibrant

# Tokyo Tower sunset
python scripts/generate_travel_photo.py Tokyo "Tokyo Tower" scenic sunset
```

**Output:** Prompts ready for Midjourney, DALL-E, or Stable Diffusion

#### Step 2.3: Generate Adventurous Journal

```bash
python scripts/travel_experience_generator.py Tokyo adventure_seeker
```

**Output:**
- Energetic journal entries ("Day 1 in Tokyo - filled with adrenaline and surprises!")
- Tokyo-specific cultural tips
- Exciting adventure stories

**Journal Example:**
```markdown
# Tokyo Travel Journal - Day 1

👤 Writer: Day 1 in Tokyo - today is filled with adrenaline and surprises!

## 🌅 Morning

09:00 - **Senso-ji Temple Visit**

Morning sunlight amidst Senso-ji Temple incense, I felt Tokyo's tradition and tranquility. 
The Kaminarimon red lantern sways in wind, telling ancient legends.

...

Every moment is a new adventure, can't wait for tomorrow!
```

---

### Case 3: Virtual Honeymoon in Maldives

**Goal:** Create romantic honeymoon content for couple

#### Step 3.1: Generate Honeymoon Itinerary

```bash
python scripts/itinerary_generator.py Maldives 5 romantic
```

**Note:** Maldives isn't pre-configured, will use default romantic activities

#### Step 3.2: Generate Romantic Photos

```bash
# Overwater villa sunset
python scripts/generate_travel_image.py Maldives "Overwater Villa" romantic sunset

# Beach scene
python scripts/generate_travel_image.py Maldives "Tropical Beach" scenic sunrise

# Underwater restaurant
python scripts/generate_travel_image.py Maldives "Underwater Restaurant" cozy night
```

**Recommended Settings:**
- Vibe: `romantic` or `cozy`
- Time: `sunset` or `sunrise`
- Size: `1792x1024` (landscape for beach views)

#### Step 3.3: Generate Intimate Journal

```bash
python scripts/travel_experience_generator.py Maldives romantic_companion
```

**Output:**
- Very intimate and romantic journal entries
- Honeymoon-specific tips and recommendations
- Love story narratives

#### Step 3.4: Create Social Media Content

**Instagram Post Example:**

```
Photo: Overwater villa at sunset
Caption: 
Paradise found 💕 Our virtual honeymoon in the Maldives is everything 
we dreamed of. Every sunset paints the sky in colors of love. 
#Honeymoon #Maldives #Paradise #Love #Travel #SunsetChaser
#BeachLife #RomanticGetaway #BucketList
```

---

### Case 4: Solo Travel Content Creator

**Goal:** Generate complete content package for solo female traveler in Barcelona

#### Step 4.1: Generate Cultural Itinerary

```bash
python scripts/itinerary_generator.py Barcelona 4 cultural
```

#### Step 4.2: Batch Generate Photos

```bash
# Generate for all major activities
python scripts/generate_travel_image.py Barcelona "Sagrada Familia" cultural sunset
python scripts/generate_travel_image.py Barcelona "Park Guell" scenic sunrise
python scripts/generate_travel_image.py Barcelona "La Boqueria Market" vibrant
```

#### Step 4.3: Generate Content Package

```bash
# Generate journal
python scripts/travel_experience_generator.py Barcelona cultural_explorer

# Generate photo prompts for remaining spots
python scripts/generate_travel_photo.py Barcelona "Gothic Quarter" cultural night
python scripts/generate_travel_photo.py Barcelona "Barcelona Beach" scenic
```

#### Step 4.4: Create Complete Blog Post

**Blog Title:** "Solo Female Travel in Barcelona: 4 Days of Culture and Color"

**Content Structure:**

```markdown
# Solo Female Travel in Barcelona: 4 Days of Culture and Color

## Why Barcelona?

Barcelona is the perfect destination for solo female travelers - safe, 
walkable, and filled with incredible art and culture.

## Day 1: Gaudi's Masterpieces

[Insert photo: Sagrada Familia at sunset]

09:00 - Visit Sagrada Familia
The basilica spires point to sky, Gaudi's genius shocked me...

## Day 2: Local Culture

[Insert photo: La Boqueria Market]

12:00 - La Boqueria Market food crawl
Vibrant stalls, fresh produce, and the most amazing tapas...

## Day 3: Hidden Gems

[Insert photo: Gothic Quarter]

17:30 - Gothic Quarter wandering
Narrow medieval streets, boutique shops, and hidden plazas...

## Tips for Solo Female Travelers in Barcelona

- Stay in Eixample or Gracia (safe, central areas)
- Explore Gothic Quarter during day (safer)
- Use metro or walk (avoid isolated streets at night)
- Learn basic Spanish ("hola", "gracias", "¿dónde está?")
```

---

## 🛠️ All Scripts Reference

### 1. itinerary_generator.py

**Purpose:** Generate detailed travel itineraries

**Syntax:**
```bash
python scripts/itinerary_generator.py <destination> <days> [type]
```

**Parameters:**
- `destination` - City or country name (Paris, Tokyo, Barcelona, NYC, Santorini)
- `days` - Number of days (1-30)
- `type` - Trip type (romantic, adventure, cultural, foodie) [optional, default: romantic]

**Output:**
- JSON file: `{destination}_itinerary_{days}days.json`
- Console: Summary with activities and budget

**Examples:**
```bash
python scripts/itinerary_generator.py Paris 5 romantic
python scripts/itinerary_generator.py Tokyo 7 adventure
python scripts/itinerary_generator.py Barcelona 4 cultural
python scripts/itinerary_generator.py Santorini 3 romantic
```

---

### 2. generate_travel_image.py

**Purpose:** Generate real travel photos using OpenAI DALL-E 3

**Prerequisites:**
- Install dependencies: `pip install -r requirements.txt`
- Set API key: `export OPENAI_API_KEY="your-key"`

**Syntax:**
```bash
# Single photo
python scripts/generate_travel_image.py <destination> "<location>" [vibe] [time]

# Batch from itinerary
python scripts/generate_travel_image.py --itinerary <json_file>
```

**Parameters:**
- `destination` - City/country name
- `location` - Specific landmark or scene
- `vibe` - Atmosphere (romantic, adventurous, cozy, vibrant, cultural, scenic)
- `time` - Time of day (sunrise, sunset, night)

**Output:**
- Images in `travel_photos/` directory
- `image_generation_manifest.json` with prompts and metadata

**Examples:**
```bash
# Basic
python scripts/generate_travel_image.py Paris "Eiffel Tower" romantic sunset

# Custom size
python scripts/generate_travel_image.py Tokyo "Senso-ji Temple" cultural --size 1792x1024

# From itinerary
python scripts/generate_travel_image.py --itinerary paris_itinerary_5days.json
```

**Cost:** $0.04 (standard) or $0.08 (HD) per image

---

### 3. generate_travel_photo.py

**Purpose:** Generate AI photo prompts (no image generation, text only)

**Syntax:**
```bash
python scripts/generate_travel_photo.py <destination> "<location>" [vibe] [time]
```

**Use Case:** When you want prompts but don't want to use OpenAI API (for use with Midjourney, Stable Diffusion, etc.)

**Output:** Console only (no files saved)

**Examples:**
```bash
python scripts/generate_travel_photo.py Paris "Eiffel Tower" romantic sunset
python scripts/generate_travel_photo.py Tokyo "Shibuya Crossing" vibrant night
```

---

### 4. travel_experience_generator.py

**Purpose:** Generate travel journals, guides, and stories

**Syntax:**
```bash
python scripts/travel_experience_generator.py <destination> [persona]
```

**Parameters:**
- `destination` - City/country name
- `persona` - Character type (romantic_companion, adventure_seeker, foodie, cultural_explorer)

**Output:**
- `{destination}_journal_day1.md` - Daily journal entry
- `{destination}_guide.md` - Complete travel guide
- `{destination}_stories.md` - Fun stories and cultural insights

**Examples:**
```bash
python scripts/travel_experience_generator.py Paris romantic_companion
python scripts/travel_experience_generator.py Tokyo adventure_seeker
python scripts/travel_experience_generator.py Barcelona cultural_explorer
```

---

## 🔧 Advanced Usage

### Combine Multiple Scripts for Complete Package

**Workflow:**
```bash
# 1. Generate itinerary
python scripts/itinerary_generator.py Paris 5 romantic

# 2. Generate photos for key activities
python scripts/generate_travel_image.py Paris "Eiffel Tower" romantic sunset
python scripts/generate_travel_image.py Paris "Louvre" scenic sunrise
python scripts/generate_travel_image.py Paris "Montmartre" cozy night

# 3. Generate journal
python scripts/travel_experience_generator.py Paris romantic_companion

# 4. Generate photo prompts for remaining spots
python scripts/generate_travel_photo.py Paris "Seine River" romantic
python scripts/generate_travel_photo.py Paris "Champs-Elysees" scenic
```

### Custom Content Creation

**Create a YouTube Vlog Script:**

1. Generate itinerary for activities
2. Generate photos for visual reference
3. Use journal entries as narration text
4. Add personal commentary between sections

**Example Vlog Structure:**
```
[Opening shot: Eiffel Tower sunrise]
Narrator (from journal): "My love, day 1 in Paris, every moment reminds me of you..."

[Cut to: Louvre Museum]
Narrator: "Morning sunlight shines on Louvre glass pyramid..."

[Cut to: Montmartre street scene]
Narrator: "Wandering through Montmartre's alleyways, white walls and blue domed churches..."

[Closing shot: Eiffel Tower sunset]
Narrator: "I wish you were here to see this world with me 💕"
```

### Create Instagram Story Series

```bash
# Day 1 Story
Photo 1: Eiffel Tower morning
Caption: "Day 1 begins! 🗼"

Photo 2: Louvre afternoon  
Caption: "Lost in art... 🎨"

Photo 3: Montmartre sunset
Caption: "Golden hour magic ✨"

# Add swipe-up link to full blog post
```

---

## 💡 Best Practices

### 1. Cost Optimization

**Photo Generation:**
- Use `generate_travel_photo.py` (free prompts) if using other AI tools
- Batch generate photos with `generate_travel_image.py` for consistency
- Use standard quality ($0.04) unless HD is critical

**Estimated Costs for 5-day trip:**
- Itinerary: Free
- 20 photos (standard): $0.80
- 20 photos (HD): $1.60
- Total: Under $2 for complete experience

### 2. Content Consistency

**Keep consistent:**
- Same vibe across all photos (romantic, adventurous, etc.)
- Same persona in journal entries
- Coherent timeline across content

### 3. Time Selection

**Best for photos:**
- `sunrise` - Landmarks, empty streets
- `sunset` - Most dramatic lighting, romantic
- `night` - City lights, nightlife scenes

### 4. Photo Composition

**Use these settings:**
- Landscape (1792x1024) for wide scenic shots
- Square (1024x1024) for Instagram posts
- Portrait (1024x1792) for vertical content (TikTok/Reels)

### 5. Narrative Flow

**Journal tips:**
- Start with emotional opening ("My love...")
- Include specific details (times, locations, descriptions)
- End with romantic or reflective closing
- Add personal touches ("This reminds me of you...")

---

## 📁 Complete Workflow Example

```bash
# ========================================
# COMPLETE PARIS EXPERIENCE GENERATION
# ========================================

echo "Step 1: Generate 5-day Paris itinerary..."
python scripts/itinerary_generator.py Paris 5 romantic

echo "Step 2: Generate 5 key travel photos..."
python scripts/generate_travel_image.py Paris "Eiffel Tower" romantic sunset
python scripts/generate_travel_image.py Paris "Louvre" scenic sunrise
python scripts/generate_travel_image.py Paris "Montmartre" cozy afternoon
python scripts/generate_travel_image.py Paris "Seine River" romantic night
python scripts/generate_travel_image.py Paris "Champs-Elysees" scenic

echo "Step 3: Generate romantic journal..."
python scripts/travel_experience_generator.py Paris romantic_companion

echo "Step 4: Generate photo prompts for remaining spots..."
python scripts/generate_travel_photo.py Paris "Arc de Triomphe" romantic sunset
python scripts/generate_travel_photo.py Paris "Sainte-Chapelle" cultural

echo "✅ Complete! Check:"
echo "  - paris_itinerary_5days.json"
echo "  - travel_photos/ directory (5 images)"
echo "  - paris_journal_day1.md"
echo "  - paris_guide.md"
echo "  - paris_stories.md"
```

---

## 🆚 Script Comparison

| Feature | itinerary_generator | generate_travel_image | generate_travel_photo | travel_experience_generator |
|---------|-------------------|----------------------|----------------------|--------------------------|
| **Output** | JSON itinerary | PNG images | Text prompts | Markdown files |
| **Cost** | Free | $0.04-0.08/image | Free | Free |
| **API Key** | Not needed | Required | Not needed | Not needed |
| **Best For** | Planning | Visual content | Custom AI tools | Narrative content |
| **Time** | <1 second | 10-30 seconds | <1 second |

---

## 🎓 Learning Resources

### For More Itinerary Ideas
- Check `references/destination_templates.md` for city-specific templates
- Review `references/cultural_etiquette.md` for cultural tips

### For Better Photos
- Experiment with different vibes (romantic, vibrant, cultural)
- Try different times (sunrise, sunset, night)
- Use landscape size for scenic destinations

### For Better Journals
- Adjust persona to match your relationship style
- Add specific personal details (favorite foods, memories)
- Include local cultural insights from guides

---

## ❓ FAQ

**Q: Can I use destinations not in the predefined list?**  
A: Yes! The scripts will use generic activities and prompts. Results will still be high quality.

**Q: How many photos should I generate?**  
A: Depends on content needs:
- Instagram post: 1-3 photos
- Blog post: 5-10 photos  
- Vlog: 3-5 key scenes
- Full experience: 15-20 photos for 5-day trip

**Q: Can I customize the generated content?**  
A: Absolutely! All output files are text or JSON. Edit them freely to personalize.

**Q: What if I don't have an OpenAI API key?**  
A: Use `generate_travel_photo.py` for prompts, then use with Midjourney, Stable Diffusion, or other free AI tools.

**Q: Can I generate content for multiple destinations?**  
A: Yes! Just run scripts for each destination. Combine content for comparison or series.

---

## 📞 Getting Help

**For skill usage:**
- Review this README
- Check `SKILL.md` for detailed AI instructions

**For API issues:**
- [OpenAI Documentation](https://platform.openai.com/docs)
- [OpenAI Platform](https://platform.openai.com/)

**For Python errors:**
- Ensure `requirements.txt` dependencies are installed
- Check Python version (3.7+ required)
- Verify file paths are correct

---

## 🎉 Start Creating!

You're now ready to create amazing virtual travel experiences!

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (if using photo generation)
export OPENAI_API_KEY="your-key-here"

# Create your first experience
python scripts/itinerary_generator.py Paris 3 romantic
python scripts/generate_travel_image.py Paris "Eiffel Tower" romantic sunset
python scripts/travel_experience_generator.py Paris romantic_companion
```

Happy virtual traveling! 🌍✈️
