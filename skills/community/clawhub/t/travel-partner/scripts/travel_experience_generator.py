#!/usr/bin/env python3
"""
Travel Experience & Story Generator
Generate travel experiences, guides, and interesting stories
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class TravelExperienceGenerator:
    def __init__(self, destination, persona="romantic_companion"):
        """
        Initialize travel experience generator

        Args:
            destination: Destination
            persona: Character persona (romantic_companion, adventure_seeker, foodie, cultural_explorer)
        """
        self.destination = destination
        self.persona = persona

    def generate_daily_journal(self, day_num, activities):
        """
        Generate diary-style travel experience

        Args:
            day_num: Day number
            activities: Daily activity list

        Returns:
            Journal text
        """
        date = self._calculate_date(day_num)

        # Select tone based on persona
        persona_styles = {
            'romantic_companion': {
                'opening': f"My love, day {day_num} in {self.destination}, every moment reminds me of you...",
                'style': 'tender, romantic, full of longing',
                'closing': "I wish you were here to see this world with me 💕"
            },
            'adventure_seeker': {
                'opening': f"Day {day_num} in {self.destination} - today is filled with adrenaline and surprises!",
                'style': 'energetic, enthusiastic, adventurous spirit',
                'closing': "Every moment is a new adventure, can't wait for tomorrow!"
            },
            'foodie': {
                'opening': f"Food tour day {day_num} in {self.destination} - culinary adventure begins!",
                'style': 'enthusiastic, detailed food description',
                'closing': "Taste memories that will never fade 😋"
            },
            'cultural_explorer': {
                'opening': f"Deep exploration of {self.destination} cultural heritage day {day_num}...",
                'style': 'intellectual, profound, cultural insight',
                'closing': "The power of culture lies in understanding and respect 📚"
            }
        }

        style = persona_styles.get(self.persona, persona_styles['romantic_companion'])

        journal = f"""# {self.destination} Travel Journal - Day {day_num}

📅 **Date**: {date}
📍 **Location**: {self.destination}
👤 **Writer**: {style['opening']}

---

## 🌅 Morning

{activities[0]['time']} - **{activities[0]['name']}**

{self._generate_activity_story(activities[0], 'morning', style['style'])}

📸 **Check-in Photo**: {activities[0]['photo_spot']}
💭 **Feeling**: {self._generate_emotion(activities[0], 'morning')}

---

## ☀️ Afternoon

{activities[1]['time']} - **{activities[1]['name']}**

{self._generate_activity_story(activities[1], 'afternoon', style['style'])}

📸 **Check-in Photo**: {activities[1]['photo_spot']}
💭 **Feeling**: {self._generate_emotion(activities[1], 'afternoon')}

---

## 🌆 Evening

{activities[2]['time']} - **{activities[2]['name']}**

{self._generate_activity_story(activities[2], 'evening', style['style'])}

📸 **Check-in Photo**: {activities[2]['photo_spot']}
💭 **Feeling**: {self._generate_emotion(activities[2], 'evening')}

---

## 🌙 Night

{activities[3]['time']} - **{activities[3]['name']}**

{self._generate_activity_story(activities[3], 'night', style['style'])}

📸 **Check-in Photo**: {activities[3]['photo_spot']}
💭 **Feeling**: {self._generate_emotion(activities[3], 'night')}

---

## 📝 Daily Summary

{self._generate_day_summary(activities)}

{style['closing']}
"""

        return journal

    def generate_travel_guide(self, destination_info):
        """
        Generate travel guide

        Args:
            destination_info: Destination information dictionary

        Returns:
            Guide text
        """
        guide = f"""# {self.destination} Travel Guide 🌍

> **Carefully prepared by your AI companion** | Last updated: {datetime.now().strftime('%Y-%m-%d')}

---

## 📍 Basic Information

**Location**: {destination_info.get('location', '')}
**Best Travel Time**: {destination_info.get('best_season', 'Suitable year-round')}
**Recommended Stay**: {destination_info.get('recommended_days', '3-5 days')}
**Language**: {destination_info.get('language', 'English')}
**Currency**: {destination_info.get('currency', '')}

---

## ✈️ Travel Preparation

### Visa Requirements
{destination_info.get('visa_info', 'Please confirm visa requirements based on nationality')}

### Transportation
- **Flight**: {destination_info.get('flight_info', 'Direct flights or connections recommended')}
- **Local Transport**: {destination_info.get('local_transport', '')}

### Essential Items
- Passport and visa copies
- Credit cards and cash
- Phone and charger
- Camera/spare battery
- Comfortable walking shoes
- Weather-appropriate clothing

---

## 🏨 Accommodation Recommendations

**Budget**: $80-120/night
- Hostels, budget hotels
- Convenient location, complete facilities

**Comfort**: $150-250/night
- Three-star hotels, boutique guesthouses
- Great value, quality service

**Luxury**: $300+/night
- Five-star hotels, resorts
- Full service, exceptional experience

---

## 🗺️ Must-Visit Attractions

{self._generate_attractions_list(destination_info.get('attractions', []))}

---

## 🍽️ Food Recommendations

{self._generate_food_recommendations(destination_info.get('food', []))}

---

## 💡 Practical Tips

### Cultural Etiquette
- {self._generate_cultural_tips()}

### Safety Reminders
- {self._generate_safety_tips()}

### Money-Saving Tips
- {self._generate_money_tips()}

---

## 📷 Photo Check-in Spots

{self._generate_photo_spots()}

---

## 💬 Local Language

### Common Phrases
- Hello: {destination_info.get('hello', 'Hello')}
- Thank you: {destination_info.get('thank_you', 'Thank you')}
- Excuse me: {destination_info.get('excuse_me', 'Excuse me')}
- How much: {destination_info.get('how_much', 'How much?')}

---

## 🆘 Emergency Information

- **Police**: {destination_info.get('emergency_police', 'Please check local emergency number')}
- **Ambulance**: {destination_info.get('emergency_ambulance', 'Please check local emergency number')}
- **Chinese Embassy**: {destination_info.get('embassy_info', 'Please check Chinese embassy contact')}

---

## 💰 Budget Reference

- **Economy**: $80-120/day
- **Comfort**: $150-250/day
- **Luxury**: $300+/day

Budget includes: accommodation, dining, transportation, tickets, shopping, etc.

---

## 🎒 Itinerary Suggestions

{self._generate_itinerary_suggestions()}

---

**Have a wonderful trip! Feel free to ask me anything 💕**
"""

        return guide

    def generate_interesting_stories(self):
        """
        Generate interesting travel stories

        Returns:
            Story text
        """
        stories = f"""# {self.destination} Fun Facts & Stories 📖

---

## 😂 Funny Misunderstandings

**Humorous moments of language barriers**

Today in {self.destination} I wanted to order food, gestured for a long time, and the waiter brought something completely different from what I wanted. But this dish turned out surprisingly delicious! Sometimes the best discoveries come from accidents...

---

## 😲 Unexpected Surprises

**Surprise around the corner...**

{self._generate_surprise_story()}

---

## 🤔 Local Secrets

**Places only locals know**

{self._generate_local_secret()}

---

## 🌟 Beautiful Moments

**Most unforgettable moment**

{self._generate_memorable_moment()}

---

## 🎭 Culture Shock

**First time experiencing...**

{self._generate_culture_shock()}

---

**The meaning of travel lies not only in reaching the destination, but in every story along the way 🌍✨**
"""

        return stories

    def _generate_activity_story(self, activity, time_of_day, style):
        """Generate activity story"""
        time_descriptions = {
            'morning': 'Morning sunlight shines on',
            'afternoon': 'Afternoon time at',
            'evening': 'Sunset time',
            'night': 'Night'
        }

        activity_stories = {
            'Explore Louvre': f'{time_descriptions[time_of_day]} the Louvre glass pyramid, I walked into this art palace. The Mona Lisa\'s smile reminds me of your smile, equally mysterious and beautiful.',
            'Visit Eiffel Tower': f'{time_descriptions[time_of_day]} the Eiffel Tower, I looked up at this iron giant. Every floor upward, the city panorama became more magnificent, really wish I could see this angle with you.',
            'Senso-ji Temple visit': f'{time_descriptions[time_of_day]} amidst Senso-ji Temple incense, I felt Tokyo\'s tradition and tranquility. The Kaminarimon red lantern sways in the wind, telling ancient legends.',
            'TeamLab Borderless': f'{time_descriptions[time_of_day]} stepping into TeamLab\'s digital world, light and shadow interweave into a dreamlike scene. Every corner is a new surprise, like every encounter in life.',
            'Visit Sagrada Familia': f'{time_descriptions[time_of_day]} Sagrada Familia\'s spires point to the sky, Gaudi\'s genius shocked me. This unfinished cathedral seems to tell a story about dreams and persistence.',
            'Statue of Liberty': f'{time_descriptions[time_of_day]} the Statue of Liberty shone in the morning light, the torch in hand symbolizes hope. Climbing the crown to overlook New York, feeling the city\'s pulse.',
            'Oia Village': f'{time_descriptions[time_of_day]} wandering through Oia\'s alleyways, white walls and blue domed churches are scattered. Every corner is a perfect photo spot, like a fairy tale world.'
        }

        base_story = activity_stories.get(
            activity['name'],
            f'{time_descriptions[time_of_day]} {activity["location"]}, experiencing the unique charm of {activity["name"]}.'
        )

        if 'romantic' in style.lower():
            base_story += " Every moment makes me miss you..."

        return base_story

    def _generate_emotion(self, activity, time_of_day):
        """Generate emotion description"""
        emotions = {
            'morning': 'Beginning full of anticipation, new adventures await us',
            'afternoon': 'Immersed in the joy of exploration, time seems to stand still',
            'evening': 'Sunset time, heart full of peace and gratitude',
            'night': 'Night romance, stars are blinking'
        }
        return emotions.get(time_of_day, 'Beautiful experience')

    def _generate_day_summary(self, activities):
        """Generate daily summary"""
        return f"""
Today was a day full of discoveries. From {activities[0]['name']} to {activities[3]['name']}, every activity made me love this world more.
The beauty of {self.destination} lies not only in the scenery but in people\'s warm smiles and deep history and culture.
Four check-in photos recorded today\'s bits and pieces. Behind every photo is a story,
and the best story is sharing all this with you...
"""

    def _generate_attractions_list(self, attractions):
        """Generate attraction list"""
        if not attractions:
            return "• Attraction 1 - Description\n• Attraction 2 - Description\n• Attraction 3 - Description"

        return "\n".join([f"### {a['name']}\n{a['description']}\n" for a in attractions])

    def _generate_food_recommendations(self, foods):
        """Generate food recommendations"""
        if not foods:
            return "• Must-try food 1 - Price range\n• Must-try food 2 - Price range\n• Must-try food 3 - Price range"

        return "\n".join([f"### {f['name']}\n{f['description']} - {f['price']}\n" for f in foods])

    def _generate_cultural_tips(self):
        """Generate cultural tips"""
        tips = [
            "Greet locals appropriately",
            "Follow local customs and etiquette",
            "Respect religious site regulations",
            "Keep appropriate volume in public places"
        ]
        return "\n- ".join(tips)

    def _generate_safety_tips(self):
        """Generate safety tips"""
        tips = [
            "Keep passport and important documents safe",
            "Avoid carrying large amounts of cash",
            "Choose legitimate accommodation and transportation",
            "Know local emergency contact information",
            "Keep in touch with family"
        ]
        return "\n- ".join(tips)

    def _generate_money_tips(self):
        """Generate money-saving tips"""
        tips = [
            "Use public transport instead of taxis",
            "Buy food at local markets",
            "Choose student discounts or city cards",
            "Free attractions and activities",
            "Book tickets in advance for discounts"
        ]
        return "\n- ".join(tips)

    def _generate_photo_spots(self):
        """Generate photo spots"""
        return f"""
### Sunrise/Sunset Spots
• Landmark best viewpoint - {self.destination} iconic location
• High observation deck - Panoramic view

### Unique Angles
• Street corner scenes - Capture local life
• Colorful architecture - Visual impact

### Romantic Couple Photos
• {self.destination} classic background - Eternal memory
• Couple exclusive spot - Private and romantic
"""

    def _generate_itinerary_suggestions(self):
        """Generate itinerary suggestions"""
        return """
### Day 1: First Impressions
- Arrive, check in
- Walk around city, adapt to environment
- Taste local cuisine

### Day 2: Deep Exploration
- Visit main attractions
- Cultural experience activities
- Night view

### Day 3: Special Experience
- Special activity or day trip
- Shopping or leisure
- Farewell dinner
"""

    def _generate_surprise_story(self):
        """Generate surprise story"""
        return """
Today I got lost in an alleyway in {self.destination}, thought I would be anxious, but unexpectedly discovered a hidden treasure shop. The owner was a kind old grandmother. She chatted with me in local language. Although we had a language barrier, her smile and warmth made me feel at home. This made me understand that sometimes the best scenery is often in the most unexpected places.
"""

    def _generate_local_secret(self):
        """Generate local secret"""
        return """
Did you know? {self.destination} has a small park only locals know, with few tourists but absolutely stunning scenery. There you can avoid crowds and quietly admire the city panorama. This was accidentally told to me by a local. It seems the most authentic travel often comes from communicating with people.
"""

    def _generate_memorable_moment(self):
        """Generate memorable moment"""
        return """
The most unforgettable moment was at a sunset in {self.destination}. The sunset dyed the sky golden, the whole city bathed in warm afterglow. I stood high, looking at all this, suddenly felt the world is so beautiful, every moment is worth cherishing. In that moment, really wanted to share this beauty with you.
"""

    def _generate_culture_shock(self):
        """Generate culture shock"""
        return """
The first time I tried local etiquette in {self.destination}, I was nervous. Locals were very friendly to correct my mistakes, and smiled at my effort as a "foreigner." This made me understand that cultural differences are not obstacles but bridges of understanding and learning.
"""

    def _calculate_date(self, day_num):
        """Calculate date"""
        from datetime import datetime, timedelta
        start_date = datetime.now() + timedelta(days=7)
        target_date = start_date + timedelta(days=day_num-1)
        return target_date.strftime('%Y-%m-%d')


def save_content_to_file(content, output_file):
    """Save content to file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Content saved to: {output_file}")


def main():
    """Command line usage"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  travel_experience_generator.py <destination> [persona]")
        print("\nPersonas:")
        print("  romantic_companion - Romantic companion")
        print("  adventure_seeker - Adventurer")
        print("  foodie - Foodie")
        print("  cultural_explorer - Cultural explorer")
        sys.exit(1)

    destination = sys.argv[1]
    persona = sys.argv[2] if len(sys.argv) > 2 else "romantic_companion"

    generator = TravelExperienceGenerator(destination, persona)

    # Generate sample content
    sample_activities = [
        {'time': '09:00', 'name': 'Explore Louvre', 'location': 'Musee du Louvre', 'photo_spot': 'Louvre Pyramid'},
        {'time': '14:00', 'name': 'Seine River Cruise', 'location': 'Seine River', 'photo_spot': 'Seine River Cruise'},
        {'time': '17:30', 'name': 'Visit Eiffel Tower', 'location': 'Eiffel Tower', 'photo_spot': 'Eiffel Tower Sunset'},
        {'time': '20:00', 'name': 'French Dinner', 'location': 'Restaurant', 'photo_spot': 'Romantic Restaurant'}
    ]

    # Generate journal
    journal = generator.generate_daily_journal(1, sample_activities)
    save_content_to_file(journal, f"{destination.lower()}_journal_day1.md")

    # Generate guide
    guide = generator.generate_travel_guide({})
    save_content_to_file(guide, f"{destination.lower()}_guide.md")

    # Generate stories
    stories = generator.generate_interesting_stories()
    save_content_to_file(stories, f"{destination.lower()}_stories.md")

    print(f"\n📝 Generated travel experience content for {destination}")
    print(f"💑 Persona: {persona}")


if __name__ == "__main__":
    main()
