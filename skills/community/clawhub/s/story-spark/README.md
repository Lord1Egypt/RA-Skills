# Story Spark

**Generate creative writing prompts from your own life. Transform photos, journal entries, and notes into fiction seeds across multiple genres.**

## The Real-World Problem

Every writer knows writer's block. You stare at a blank page, and every idea feels generic, flat, or borrowed. Generic writing prompt books offer "write about your happiest memory" — but that's not specific enough to spark real fiction.

The best fiction comes from **specific, emotionally charged moments** — the weird conversation you overheard on the train, the photo from that strange afternoon, the half-remembered dream. But most writers don't have a system for mining their own lives for these moments.

**Story Spark** solves this by scanning your photos and journals, finding the moments with narrative potential, and transforming them into detailed fiction prompts with characters, conflicts, and twists.

## Who Needs This

- **Fiction writers** experiencing writer's block
- **Aspiring authors** who want to write but don't know where to start
- **Creative writing students** and teachers
- **Journalers** who want to do something creative with their entries
- **Photographers** looking for narrative uses of their images
- **NaNoWriMo participants** needing daily prompts
- **Anyone who wants to write fiction but thinks their life is "too boring"** — it isn't

## How It Works

1. **Scan**: Reads EXIF metadata from photos (GPS location, date/time, camera settings) and/or text from journal entries and notes
2. **Extract moments**: Identifies emotionally interesting elements — unusual times (3 AM photos), solitary places, seasonal moods, evocative words in journals
3. **Genre transform**: Applies genre lenses (mystery, sci-fi, romance, horror, literary) to reimagine each moment as fiction
4. **Generate prompts**: Creates detailed prompts with premise, character, conflict, and twist
5. **Export**: Outputs as JSON, markdown, or plain text for your writing workflow

## Quick Start

```bash
# Generate prompts from photos
python scripts/story_spark.py photos ~/Pictures/vacation/ --count 5

# From journal entries
python scripts/story_spark.py text ~/journal/ --count 5

# Try the built-in demo (no files needed!)
python scripts/story_spark.py demo --count 5
```

## Example Scenario

**Emma** hasn't written fiction in months. She has 3,000 photos on her phone and a year of journal entries.

1. **Scan**: `python scripts/story_spark.py photos ~/Pictures/ --count 10 --genre mystery`
   - The tool finds a photo taken at 3:17 AM in a hospital parking lot (EXIF: GPS + timestamp)
2. **Prompt generated**:
   > **Source**: Hospital parking lot, 3:17 AM, winter
   > **Genre**: Mystery
   > **Premise**: A night-shift nurse finds a car running in the parking lot — engine on, lights off, driver's seat empty. The car is still warm.
   > **Character**: The nurse, 15 years on the night shift, who's seen everything — until now
   > **Conflict**: Hospital security says call the police. The nurse recognizes the car.
   > **Twist**: The car belongs to someone who died in the hospital three days ago.

3. **Emma writes**: The specific details (hospital, 3 AM, winter) give her story texture that a generic prompt never could. She writes 2,000 words in one sitting.

## Why It Works

- **Specificity sparks creativity**: "A hospital parking lot at 3 AM" is more evocative than "a dark place"
- **Personal connection**: Writing from your own moments adds emotional authenticity
- **Genre variety**: The same moment becomes six different stories — you discover which genre fits your voice
- **Low barrier**: You don't need ideas — you need moments, and you already have thousands

## Installation

```bash
git clone https://github.com/voronindenis5/story-spark.git
cd story-spark
# For photo EXIF reading: pip install Pillow
# Text/journal features need no dependencies
```

## License

MIT — free for personal and creative use.
