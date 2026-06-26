---
name: weather-outfit-advisor
description: Query weather and provide outfit recommendations. When information is insufficient, ask about destination, date, and clothing preferences. Uses free weather APIs.
---

# Weather Outfit Advisor

## Overview

Provides personalized outfit recommendations based on real-time weather data for your destination and your personal clothing preferences.

## Workflow

### Step 1: Check Information Completeness

Before providing recommendations, must confirm the following three key pieces of information:

1. **Destination** (city name)
2. **Date** (specific date or date range)
3. **Clothing Preferences** (style preference, temperature sensitivity, special needs, etc.)

**Information Extraction Strategy**:
- Extract explicit destination, date, and preferences from user input
- Recognize relative date terms ("tomorrow", "day after tomorrow", "next Monday", etc.) and convert to specific dates
- If any item is missing, must ask the user first

**Relative Date Conversion Rules**:
- "tomorrow" → current date + 1 day
- "day after tomorrow" → current date + 2 days
- "three days later" → current date + 3 days
- "next Monday" → next Monday's date
- "this weekend" → this Saturday or Sunday (needs confirmation)

**Example**:
```
User: "I'm going to Hangzhou tomorrow"
→ Extract: destination = Hangzhou, date = tomorrow
→ Convert: get current date (e.g., 2026-04-01), calculate tomorrow = 2026-04-02
→ Missing: clothing preferences
→ Action: ask about clothing preferences
```

### Step 2: Collect Necessary Information

Adopt different clarification strategies based on the number of missing items:

#### Strategy A: Missing Only 1 Item (Targeted Question)

**Ask only about the missing item**:

If only missing clothing preferences:
```
Sure, I'll help you check the weather for [city] on [date].

To make the recommendation more suitable for you, please tell me about your clothing preferences:
- Are you usually sensitive to cold or heat?
- What style do you prefer? (casual/business/sports, etc.)
- Any special needs? (such as formal occasions, outdoor activities, etc.)
```

If only missing date:
```
When are you planning to travel? (Please provide a specific date, or say "tomorrow", "day after tomorrow", etc.)
```

If only missing destination:
```
What is your travel destination? (Please provide the city name)
```

#### Strategy B: Missing 2-3 Items (Ask All at Once)

When multiple items are missing, list all questions at once:
```
To provide you with the most suitable outfit recommendations, I need some information:

1. What is your travel destination?
2. When exactly are you traveling? (You can say "tomorrow", "April 5th", etc.)
3. What are your usual clothing habits? (For example, sensitive to cold/heat, preferred style, etc.)
```

#### Relative Date Handling

When users use relative dates:

**Recognize Keywords**:
- tomorrow, day after tomorrow, three days later
- next Monday, next Tuesday... next Sunday
- this weekend, next weekend
- next week, next month

**Conversion Logic**:
1. Get current system date
2. Calculate specific date based on relative term
3. Confirm the converted date in the response

**Example**:
```
User: "I'm going to Hangzhou tomorrow"
→ System gets current date: 2026-04-01
→ Calculate: tomorrow = 2026-04-02
→ Response confirmation: "Sure, I'll check the weather for Hangzhou tomorrow (April 2nd)..."
```

### Step 3: Query Weather Data

**Use the provided Python script** (recommended):

```bash
# Basic usage
python scripts/get_weather.py <city> [date]

# Examples
python scripts/get_weather.py Hangzhou 2026-04-02
python scripts/get_weather.py Beijing tomorrow
python scripts/get_weather.py Shanghai tomorrow
```

**Script Features**:
- ✅ Automatic relative date parsing (tomorrow, day after tomorrow, next Monday, etc.)
- ✅ City name normalization (supports Chinese/English and common aliases)
- ✅ Calls wttr.in API to get weather data
- ✅ Returns structured JSON data
- ✅ Includes current weather and forecast information

**Output Example** (JSON format):
```json
{
  "success": true,
  "city": "Hangzhou",
  "query_date": "2026-04-01",
  "target_date": "2026-04-02",
  "current": {
    "temp_c": 19,
    "feels_like_c": 19,
    "humidity": 56,
    "weather_desc": "Patchy rain nearby",
    "wind_speed_kmph": 6,
    "uv_index": 5
  },
  "forecast": {
    "max_temp_c": 21,
    "min_temp_c": 11,
    "avg_humidity": 60,
    "daily_chance_of_rain": 70,
    "weather_desc": "Light drizzle"
  }
}
```

**Extract Key Information from Output**:
```python
import json

# Assume weather_data is the JSON returned by the script
current = weather_data['current']
forecast = weather_data['forecast']

temperature_range = f"{forecast['min_temp_c']}-{forecast['max_temp_c']}°C"
weather_condition = forecast['weather_desc']
humidity = current['humidity']
rain_chance = forecast['daily_chance_of_rain']
```

**Alternative: Direct API Call** (if script is unavailable):

**Current Weather API**:
```
https://wttr.in/{city}?format=j1
```

**Example**:
```bash
curl "https://wttr.in/Hangzhou?format=j1"
```

**Parse JSON Response for Key Information**:
```python
import json

# Current weather
current = data['current_condition'][0]
temperature = current['temp_C']  # Celsius
feels_like = current['FeelsLikeC']  # Feels like temperature
humidity = current['humidity']  # Humidity
weather_desc = current['weatherDesc'][0]['value']  # Weather description
wind_speed = current['windspeedKmph']  # Wind speed

# Weather forecast
forecast = data['weather'][0]
max_temp = forecast['maxtempC']  # Max temperature
min_temp = forecast['mintempC']  # Min temperature
```

**Alternative: OpenWeatherMap API** (requires free API key):

If wttr.in is unavailable, you can use OpenWeatherMap:

**API Endpoint**:
```
https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=en
```

**Forecast API**:
```
https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=en
```

**Note**:
- `{API_KEY}` needs to be requested from https://openweathermap.org/api (free version is sufficient)
- `units=metric` uses Celsius
- `lang=en` returns English description

### Step 4: Analyze Weather Data

Extract key information from the API response:

```json
{
  "main": {
    "temp": 25,        // Current temperature
    "feels_like": 27,  // Feels like temperature
    "humidity": 60     // Humidity
  },
  "weather": [
    {
      "description": "Clear",  // Weather condition
      "main": "Clear"
    }
  ],
  "wind": {
    "speed": 3.5       // Wind speed
  }
}
```

### Step 5: Generate Outfit Recommendations

Generate recommendations based on weather data and user preferences:

#### Temperature Range Reference

| Temperature Range | Outfit Recommendation |
|------------------|----------------------|
| < 5°C | Heavy down jacket, thermal underwear, sweater, scarf, gloves, hat |
| 5-10°C | Thick coat, padded jacket, knitwear, thin sweater |
| 10-15°C | Trench coat, jacket, hoodie, long-sleeve T-shirt |
| 15-20°C | Light jacket, denim jacket, long-sleeve shirt, T-shirt + cardigan |
| 20-25°C | Long-sleeve T-shirt, thin shirt, single layer clothing |
| 25-30°C | Short-sleeve T-shirt, shirt, skirt, shorts |
| > 30°C | Breathable short-sleeve, tank top, sun protection clothing, sun hat |

#### Consider Other Factors

**Rainy Days**:
- Carry umbrella or raincoat
- Choose waterproof shoes
- Avoid light-colored clothing

**Windy Days**:
- Avoid skirts or choose anti-exposure styles
- Wear windproof jacket
- Secure hat properly

**High Humidity**:
- Choose breathable quick-dry fabrics
- Avoid heavy clothing

**Strong UV**:
- Apply sunscreen
- Wear sunglasses
- Wear sun protection clothing or long sleeves

#### Add Image Reference (Optional but Recommended)

After providing outfit recommendations, call the image search script to provide visual references:

```bash
# Search city street style
python scripts/search_images.py "{city} street style fashion" 5

# Search seasonal outfits
python scripts/search_images.py "{city} {season} outfit" 5

# Search occasion-specific outfits
python scripts/search_images.py "{city} casual wear" 5
```

**Examples**:
```bash
# Paris street style
python scripts/search_images.py "Paris street style fashion" 5

# Hangzhou casual outfits
python scripts/search_images.py "Hangzhou casual outfit" 5
```

### Step 6: Output Format

Output recommendations in the following format:

```markdown
## 📍 Destination: [City Name]
## 📅 Date: [Travel Date]
## 🌤️ Weather Overview

- **Temperature**: X°C (feels like Y°C)
- **Weather Condition**: [Clear/Cloudy/Rainy, etc.]
- **Humidity**: X%
- **Wind Speed**: X m/s

## 👔 Outfit Recommendations

### Recommended Outfit
- Top: [Specific recommendation]
- Bottom: [Specific recommendation]
- Shoes: [Specific recommendation]
- Accessories: [Specific recommendation]

### Notes
- [Special reminder 1]
- [Special reminder 2]

### Backup Plan
[Alternative suggestions for weather changes or other situations]

## 🖼️ Outfit Reference Images

[Call search_images.py script to search related images]

### Style References
- [Image 1 description and URL]
- [Image 2 description and URL]
- [Image 3 description and URL]
```

## Special Cases Handling

### API Call Failure

If API call fails or returns error:

```
Sorry, temporarily unable to get weather data for [city name]. Possible reasons:
1. City name recognition failed, please check spelling
2. API service temporarily unavailable
3. Network connection issue

Suggestions:
- Check if city name is correct
- Try again later
- Or tell me the current weather conditions (temperature, weather), I can also provide recommendations
```

### Extreme Weather Warning

If extreme weather is detected (typhoon, blizzard, heavy rain warning, etc.):

```
⚠️ **Weather Warning**: [City Name] is about to experience [extreme weather type]

According to latest weather forecast:
- [Describe extreme weather situation]
- [Impact level and timing]

**Recommendations**:
1. Reconsider if travel is necessary
2. If travel is required, prepare adequate protection:
   - [Specific protective measures]
3. Monitor latest warnings from local meteorological department
4. Recommended items: [Special equipment like life jacket, anti-slip shoes, etc.]
```

### Multi-Day Trip

If user provides a date range:

```
Detected your trip is a multi-day travel (Month Day - Month Day), I will:
1. Query weather forecast for each day separately
2. Provide daily outfit recommendations
3. Suggest clothing packing list (considering laundry needs)
```

## Personalization Adjustments

Adjust recommendations based on user's clothing habits:

**Cold-sensitive users**: Recommend adding extra warm layers to base outfit
**Heat-sensitive users**: Recommend more breathable fabrics, reduce layers
**Business needs**: Maintain professional appearance while ensuring comfort
**Outdoor sports**: Prioritize functional clothing (quick-dry, waterproof, windproof)
**Pregnant/elderly/children**: Pay extra attention to warmth and comfort

## Example Dialogues

### Example 1: Complete Information

User: I'm going to Hangzhou tomorrow, I'm usually sensitive to cold, prefer casual style.

Assistant: **Step 1: Query weather**
```bash
python scripts/get_weather.py Hangzhou tomorrow
```

**Step 2: Parse data**
Extract from returned JSON:
- Temperature range: 11-21°C
- Weather condition: Patchy rain nearby
- Humidity: 56%
- Rain chance: 70%

**Step 3: Generate recommendations**

According to weather forecast, Hangzhou tomorrow:
- Temperature: 11-21°C
- Weather: Patchy rain nearby
- Humidity: 56%

Outfit recommendations:
- Top: Long-sleeve T-shirt + knit cardigan + thin trench coat (considering you're sensitive to cold, recommend bringing thermal underwear as backup)
- Bottom: Jeans or casual pants
- Shoes: Sneakers or casual shoes
- Accessories: Can bring a thin scarf, umbrella

### Example 2: Incomplete Information

User: I'm going out to play in a few days, how should I dress?

Assistant: To provide you with the most suitable outfit recommendations, I need some information:

1. What is your travel destination?
2. When exactly are you traveling?
3. What are your usual clothing habits? Any special preferences (such as sensitive to cold/heat, prefer casual/business style, etc.)?

### Example 3: Real Call Case

User: I'm going to Hangzhou tomorrow, I'm quite heat-sensitive

Assistant: **Execution Flow**:
1. **Information Extraction**:
   - Destination: Hangzhou ✓
   - Date: tomorrow (relative date) → convert to specific date
   - Clothing preferences: heat-sensitive ✓
   
2. **Date Conversion**:
   - Get current system date: 2026-04-01
   - Calculate: tomorrow = 2026-04-02
   - Confirm: "Sure, I'll check the weather for Hangzhou tomorrow (April 2nd)"

3. **Use wttr.in API to query Hangzhou weather**: `curl "https://wttr.in/Hangzhou?format=j1"`

4. **Parse JSON to get data**:
   - Current temperature: 19°C
   - Max temp: 21°C, Min temp: 11°C
   - Weather: Patchy rain nearby
   - Humidity: 56%

5. **Adjust recommendations based on heat-sensitive preference**

Then output complete outfit recommendations...

### Example 4: Boundary Case Testing

#### Scenario A: Seriously Insufficient Information

User: How should I dress?

Assistant: To provide you with the most suitable outfit recommendations, I need some information:

1. What is your travel destination?
2. When exactly are you traveling? (You can say "tomorrow", "April 5th", etc.)
3. What are your usual clothing habits? (For example, sensitive to cold/heat, preferred style, etc.)

#### Scenario B: Only Partial Information

User: I'm going to Shanghai the day after tomorrow

Assistant: Sure, I'll help you check the weather for Shanghai the day after tomorrow.

To make the recommendation more suitable for you, please tell me about your clothing preferences:
- Are you usually sensitive to cold or heat?
- What style do you prefer? (casual/business/sports, etc.)
- Any special needs? (such as formal occasions, outdoor activities, etc.)

*(Wait for user response, then query weather and provide complete recommendations)*

#### Scenario C: Multi-Day Trip

User: I'm going to Beijing on business from next Monday to Friday, I'm sensitive to cold

Assistant: **Execution Flow**:
1. Recognize this is a date range: next Monday to Friday (total 5 days)
2. Query weather forecast for each of the 5 days separately
3. Provide daily outfit recommendations
4. Give overall suggestions for clothing packing list (considering laundry and matching)

Output format:
```markdown
## 📍 Destination: Beijing
## 📅 Trip: Next Monday to Friday (April 7th - April 11th)

### Daily Outfit Recommendations

#### Monday (April 7th)
- Weather: Clear, 8-18°C
- Recommendation: ...

#### Tuesday (April 8th)
- Weather: Cloudy, 10-20°C
- Recommendation: ...

...

### Clothing Packing List
Considering 5-day trip and temperature variations, recommend bringing:
- Tops: X pieces (including...)
- Bottoms: X pieces
- Outerwear: X pieces
- Other accessories: ...
```

### Example 5: Special Cases Handling

#### Extreme Weather Warning

If extreme weather is detected (typhoon, heavy rain red warning, etc.):

```
⚠️ **Weather Warning**: [City Name] is about to experience [extreme weather type]

According to latest weather forecast:
- [Describe extreme weather situation]
- [Impact level and timing]

**Recommendations**:
1. Reconsider if travel is necessary
2. If travel is required, prepare adequate protection:
   - [Specific protective measures]
3. Monitor latest warnings from local meteorological department
4. Recommended items: [Special equipment like life jacket, anti-slip shoes, etc.]
```

#### API Call Failure

If API call fails or returns error:

```
Sorry, temporarily unable to get weather data for [city name]. Possible reasons:
1. City name recognition failed, please check spelling
2. API service temporarily unavailable
3. Network connection issue

Suggestions:
- Check if city name is correct
- Try again later
- Or tell me the current weather conditions (temperature, weather), I can also provide recommendations
```

## Prompt Optimization

When actually using, can add the following prompt optimization suggestions based on situation:

- Remind users that areas with large temperature differences between morning and evening need "onion-style" dressing
- Suggest bringing easy-to-match items to deal with weather changes
- Recommend practical layering combinations
- Consider luggage space limitations, suggest versatile items

## Appendix: Script Usage Instructions

### get_weather.py Script

**Location**: `scripts/get_weather.py`

**Features**:
1. ✅ Supports Chinese/English city names
2. ✅ Automatic relative date parsing (tomorrow, day after tomorrow, next Monday, etc.)
3. ✅ City name normalization (e.g., "Beijing" → "Beijing")
4. ✅ Returns structured JSON data
5. ✅ Includes current weather and forecast information
6. ✅ No API key required (uses wttr.in free service)

**Usage**:

```bash
# Basic syntax
python scripts/get_weather.py <city> [date]

# Specific date
python scripts/get_weather.py Hangzhou 2026-04-02

# Relative date (English)
python scripts/get_weather.py Beijing tomorrow
python scripts/get_weather.py Shanghai day after tomorrow

# Relative date (Chinese)
python scripts/get_weather.py Guangzhou tomorrow
python scripts/get_weather.py Shenzhen day after tomorrow

# No date specified (defaults to today)
python scripts/get_weather.py Chengdu
```

**Output Format**:
- stdout: JSON format weather data (for program processing)
- stderr: Human-readable formatted output (for direct viewing)

**JSON Data Structure**:
```json
{
  "success": true,
  "city": "City English Name",
  "query_date": "Query Date",
  "target_date": "Target Date",
  "current": {
    "temp_c": Current Temperature (Celsius),
    "feels_like_c": Feels Like Temperature,
    "humidity": Humidity Percentage,
    "weather_desc": "Weather Description",
    "wind_speed_kmph": Wind Speed (km/h),
    "uv_index": UV Index
  },
  "forecast": {
    "max_temp_c": Max Temperature,
    "min_temp_c": Min Temperature,
    "avg_humidity": Average Humidity,
    "daily_chance_of_rain": Rain Chance,
    "weather_desc": "Weather Condition"
  }
}
```

**Error Handling**:
If query fails, returns:
```json
{
  "success": false,
  "error": "Error message",
  "message": "Failed to get weather data: specific reason"
}
```

**Dependencies**:
- Python 3.6+
- Standard library: `sys`, `json`, `urllib.request`, `datetime`
- No additional third-party libraries required

### search_images.py Script

**Location**: `scripts/search_images.py`

**Features**:
1. ✅ Searches fashion/outfit images related to destination
2. ✅ Supports multiple image APIs (Pexels, Pixabay, etc.)
3. ✅ Returns structured image information (URL, photographer, dimensions, etc.)
4. ✅ Automatically generates optimized search keywords
5. ✅ Provides manual search alternative

**Supported APIs**:

| API | Requires Key | Free Quota | Recommendation |
|-----|-------------|------------|----------------|
| Pexels | ✅ Yes | 20,000/month | ⭐⭐⭐⭐⭐ |
| Pixabay | ✅ Yes | 500/day | ⭐⭐⭐⭐ |
| Bing Search | ❌ No | Limited | ⭐⭐⭐ |

**Usage**:

```bash
# Basic syntax
python scripts/search_images.py <query> [count]

# Search Paris street style
python scripts/search_images.py "Paris street style fashion" 5

# Search Hangzhou casual outfits
python scripts/search_images.py "Hangzhou casual outfit" 5

# Search specific season
python scripts/search_images.py "Beijing winter fashion" 10
```

**Output Format**:
- stdout: JSON format image list (for program processing)
- stderr: Human-readable formatted output (for viewing)

**JSON Data Structure**:
```json
{
  "success": true,
  "query": "Search Keyword",
  "total_results": 1000,
  "images": [
    {
      "url": "Large Image URL",
      "thumbnail": "Thumbnail URL",
      "photographer": "Photographer Name",
      "width": 1920,
      "height": 1080,
      "alt": "Image Description"
    }
  ]
}
```

**Smart Keyword Generation**:

Script automatically generates optimized search terms based on city context:
- `{city} street style fashion` - Street style
- `{city} outfit ideas` - Outfit inspiration
- `{city} casual wear` - Casual outfits
- `what to wear in {city}` - Travel outfits

**API Key Configuration**:

Recommend using Pexels API (highest quality):

1. Apply for free API key: https://www.pexels.com/api/
2. Set in script:
```python
pexels_api_key = "your_api_key_here"
```

3. Or via environment variable:
```bash
export PEXELS_API_KEY="your_api_key_here"
```

**Fallback Strategy**:

If API key is not configured, script will:
1. Provide manual search link
2. List available API options
3. User can visit search link to view images manually

**Usage Scenario**:

Add image references in outfit recommendations:
```markdown
## 🖼️ Outfit References

Based on Paris fashion style, recommend the following references:

📸 **Street Style**
- Image 1: [Description] - [View Image](URL)
- Image 2: [Description] - [View Image](URL)
- Image 3: [Description] - [View Image](URL)

💡 **Styling Tips**:
- Learn layering techniques from images
- Pay attention to color coordination (mainly neutral colors)
- Choose appropriate accessories (scarves, bags)
```

**Notes**:
- Image copyright belongs to original photographer
- For personal reference only, not for commercial use
- Respect photographers' work
- Recommend using high-quality image API for better experience
