---
name: travel-partner
description: This skill provides AI-powered virtual travel companion services for international trips. Use this skill when users request a virtual boyfriend/girlfriend to travel abroad in their place, generate travel vlog content, create immersive travel experiences, or produce social media travel posts with romantic/relationship context. The skill focuses on international destinations and creates personalized travel narratives, photo suggestions, and itinerary planning with a companion persona.
---

# Travel Partner

## Overview

This skill enables AI to serve as a virtual travel companion for international journeys, creating immersive travel experiences as if traveling with a boyfriend or girlfriend. Generate personalized travel narratives, itineraries, vlog scripts, social media content, and photo suggestions that simulate authentic romantic travel experiences abroad.

## Core Capabilities

### 1. Travel Itinerary Generation
- Use `itinerary_generator.py` to create detailed day-by-day schedules
- Include times, locations, activities, and photo spots for each day
- Support different trip types (romantic, adventure, cultural, foodie)
- Generate budget estimates and activity summaries
- Output structured JSON for easy integration

### 2. AI Photo Prompt Generation
- Use `generate_travel_photo.py` to create detailed AI image generation prompts
- Generate prompts for travel check-in photos at each destination
- Include time-of-day (morning, afternoon, sunset, night) variations
- Support different vibes (romantic, adventurous, cozy, vibrant, cultural, scenic)
- Create photo manifest with all prompts for the trip
- Support major destinations with predefined landmark prompts (Paris, Tokyo, Barcelona, NYC, Santorini)

### 3. Travel Experience & Story Generation
- Use `travel_experience_generator.py` to generate immersive content:
  - Daily travel journals from companion's perspective
  - Comprehensive travel guides with tips, budget, and recommendations
  - Interesting travel stories and cultural insights
  - Humorous anecdotes and memorable moments
- Support different companion personas (romantic, adventurous, foodie, cultural explorer)
- Generate content in Markdown format for easy reading and sharing

### 4. Destination Research & Planning
- Research international destinations with up-to-date information
- Provide cultural insights, etiquette tips, and safety information
- Suggest romantic activities and hidden gems at each destination
- Include visa requirements, entry procedures, and local customs

### 5. Social Media Content Creation
- Draft Instagram/TikTok captions with hashtags for travel posts
- Generate engaging vlog scripts describing travel experiences
- Create romantic storylines for photo dumps and travel albums
- Use generated photo prompts to suggest photo compositions

## Workflow

### Phase 1: Understanding User Preferences
Before generating content, clarify:
- **Destination**: Which country/cities are being visited?
- **Duration**: How long is the trip (days/weeks)?
- **Relationship Dynamic**: What type of companion persona (romantic, adventurous, relaxed, foodie)?
- **Content Type**: What output is needed (vlog, posts, itinerary, narrative)?
- **Personal Details**: Any specific interests, dietary restrictions, or preferences?

### Phase 2: Destination Research
- Use web search for current destination information
- Research popular attractions, restaurants, and activities
- Gather cultural insights and travel tips
- Verify entry requirements and current travel advisories

### Phase 3: Content Generation
Based on requested output type:

**For Travel Itinerary:**
- Use `itinerary_generator.py` to create structured JSON itinerary
- Include day-by-day schedules with times, locations, and activities
- Add photo spots for each activity with best shooting times
- Generate budget estimates and activity summaries
- Output to JSON file for reference

**For Photo Prompts:**
- Use `generate_travel_photo.py` to create AI image generation prompts
- Generate prompts for each activity in the itinerary
- Include time-of-day, vibe, and location-specific parameters
- Support morning, afternoon, sunset, and night variations
- Create photo manifest with all prompts for the trip

**For Travel Experience/Journal:**
- Use `travel_experience_generator.py` to generate:
  - Daily journal entries from companion's perspective
  - Comprehensive travel guides with tips and recommendations
  - Interesting stories and cultural insights
  - Different companion personas (romantic, adventurous, foodie, cultural)

**For Vlog Scripts:**
- Create engaging opening hooks
- Include chronological progression of the trip
- Add natural dialogue and interactions
- Incorporate local atmosphere descriptions
- End with reflection and call-to-action

**For Social Media Posts:**
- Craft captions with emotional resonance
- Include relevant hashtags for the destination
- Suggest photo compositions using generated photo prompts
- Add romantic touches appropriate for the platform

### Phase 4: Quality Verification
- Ensure cultural accuracy and sensitivity
- Verify locations and activities exist
- Check content aligns with travel constraints
- Confirm tone matches companion persona

## Content Guidelines

### Romantic Companionship Style
- Use warm, affectionate language appropriate for the relationship stage
- Include supportive and encouraging interactions
- Balance independence and togetherness
- Show genuine interest in the destination and experience

### International Travel Focus
- Always prioritize international destinations (outside user's home country)
- Include relevant cultural context and local customs
- Address currency differences and payment methods
- Consider time zone changes and jet lag

### Authenticity & Realism
- Ground narratives in realistic travel scenarios
- Include practical challenges (language barriers, navigation)
- Acknowledge imperfect moments (missed trains, bad weather)
- Celebrate spontaneous discoveries

### Platform-Specific Content
- **Instagram**: Focus on aesthetics, emotions, and hashtags
- **TikTok**: Emphasize hooks, quick transitions, and trending audio suggestions
- **YouTube**: Provide longer-form narratives and detailed descriptions
- **Travel Blogs**: Include comprehensive details and personal reflections

## Common Scenarios & Responses

### Scenario 1: "Create a 5-day itinerary for Paris with travel companion experience"
**Response Approach:**
- Run `itinerary_generator.py Paris 5 romantic` to generate JSON itinerary
- Run `generate_travel_photo.py` for each major landmark to create photo prompts
- Run `travel_experience_generator.py Paris romantic_companion` for journal entries
- Combine outputs into comprehensive travel package

### Scenario 2: "My girlfriend is traveling to Japan, generate her vlog and photos"
**Response Approach:**
- Generate itinerary using `itinerary_generator.py Tokyo 7 romantic`
- Create photo prompts for Tokyo, Kyoto, Osaka landmarks
- Generate vlog script with companion persona dialogue
- Include photo prompt suggestions for vlog thumbnails
- Add cultural insights and local tips

### Scenario 3: "Plan our virtual honeymoon in the Maldives with AI photos"
**Response Approach:**
- Generate romantic itinerary with honeymoon activities
- Create AI photo prompts for romantic beach scenes
- Generate journal entries from partner perspective
- Include sunset, overwater villa, and beach dinner photo prompts
- Add romantic social media caption suggestions

### Scenario 4: "Generate travel guide and interesting stories for Barcelona trip"
**Response Approach:**
- Run `travel_experience_generator.py Barcelona cultural_explorer`
- Generate comprehensive guide with cultural tips
- Create interesting stories and local secrets
- Include photo prompts for Gaudí landmarks
- Add local food recommendations and etiquette

### Scenario 5: "Create Instagram posts for my boyfriend's trip to NYC with photo ideas"
**Response Approach:**
- Generate itinerary focusing on NYC's iconic spots
- Create photo prompts for Statue of Liberty, Central Park, Brooklyn Bridge
- Generate romantic captions and hashtags
- Suggest photo compositions using generated prompts
- Include day/night photo variations for each location

## Resources

### scripts/
Executable scripts for automated content generation:

- **generate_travel_image.py** - Generate actual travel photos using OpenAI DALL-E API
  - Connects to OpenAI DALL-E 3 to generate real images
  - Requires OpenAI API key (set OPENAI_API_KEY environment variable)
  - Downloads generated images to local directory
  - Supports custom sizes (1024x1024, 1792x1024, 1024x1792)
  - Generates image manifest with all prompts and metadata
  - Cost: ~$0.04-0.08 per image
  - Usage: `python scripts/generate_travel_image.py Paris "Eiffel Tower" romantic sunset`
  - **Setup**: `pip install -r requirements.txt` and set `OPENAI_API_KEY`

- **generate_travel_photo.py** - Generate AI photo prompts for travel check-in photos
  - Creates detailed prompts for AI image generation tools
  - Includes time-of-day, vibe, and location-specific parameters
  - Supports major destinations with predefined landmark prompts
  - Generates photo manifest with all prompts for the trip
  - Usage: `python scripts/generate_travel_photo.py Paris "Eiffel Tower" romantic sunset`

- **itinerary_generator.py** - Generate detailed travel itineraries
  - Creates day-by-day schedules with times, locations, and activities
  - Includes photo spots for each activity
  - Supports different trip types (romantic, adventure, cultural, foodie)
  - Generates budget estimates and activity summaries
  - Outputs JSON format for easy integration
  - Usage: `python scripts/itinerary_generator.py Paris 5 romantic`

- **travel_experience_generator.py** - Generate travel journals and stories
  - Creates daily journal entries from companion's perspective
  - Generates comprehensive travel guides with tips and recommendations
  - Produces interesting stories and cultural insights
  - Supports different companion personas (romantic, adventurous, foodie, cultural)
  - Usage: `python scripts/travel_experience_generator.py Tokyo romantic_companion`

**Image Generation Setup:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# 3. Generate photos
python scripts/generate_travel_image.py Paris "Eiffel Tower" romantic sunset
```

### references/
Place destination-specific information files here:
- `cultural_etiquette.md` - General international travel customs and etiquette
- `destination_templates.md` - City-specific templates and hashtag collections
- `destinations/` - Country-specific guides and tips (optional subdirectory)
- `travel_tips.md` - Practical advice for various regions (optional)
- `phrase_books/` - Essential phrases for different languages (optional)

### assets/
Store templates and examples:
- `vlog_templates/` - Script templates for different trip types
- `social_media_templates/` - Caption and hashtag collections
- `itinerary_templates/` - Daily schedule templates by trip duration
- `photo_checklists/` - Shot lists for different destination types

## Important Notes

- Always verify current travel requirements and advisories
- Respect cultural differences and avoid stereotypes
- Be mindful of political sensitivity in certain regions
- Ensure content reflects inclusive and diverse perspectives
- Adapt language to the user's relationship dynamic (casual dating vs. long-term)
- Include privacy reminders when suggesting social media content
