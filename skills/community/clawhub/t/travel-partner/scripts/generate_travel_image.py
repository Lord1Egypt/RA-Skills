#!/usr/bin/env python3
"""
AI Travel Image Generator
Generate actual travel photos using OpenAI DALL-E API
"""

import json
import sys
import os
import base64
from pathlib import Path
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class TravelImageGenerator:
    def __init__(self, api_key=None):
        """
        Initialize image generator

        Args:
            api_key: OpenAI API key (optional, can use OPENAI_API_KEY env variable)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI library not installed. Please install it first:\n"
                "pip install openai"
            )

        # Get API key from parameter or environment
        api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please:\n"
                "1. Set OPENAI_API_KEY environment variable, or\n"
                "2. Pass api_key parameter when creating generator"
            )

        self.client = OpenAI(api_key=api_key)

    def generate_photo_prompt(self, destination, location_type, vibe, time_of_day=None):
        """
        Generate photo prompt

        Args:
            destination: Destination (e.g., Paris, Tokyo)
            location_type: Location (e.g., Eiffel Tower, temple, beach)
            vibe: Atmosphere (romantic, adventurous, cozy, vibrant)
            time_of_day: Time (sunrise, sunset, night)

        Returns:
            Prompt string
        """
        base_prompt = f"A stunning, high-quality travel photo of {location_type} in {destination}"

        if time_of_day:
            base_prompt += f", captured during {time_of_day}"

        vibe_keywords = {
            'romantic': 'soft warm lighting, dreamy atmosphere, golden hour, intimate feeling, pastel colors',
            'adventurous': 'dynamic composition, vibrant energy, dramatic clouds, sense of movement, bold colors',
            'cozy': 'warm inviting atmosphere, soft diffused light, comfortable setting, peaceful mood, warm tones',
            'vibrant': 'bright vivid colors, energetic atmosphere, clear sharp details, lively scene, saturated hues',
            'cultural': 'authentic atmosphere, traditional elements, rich cultural details, heritage feel, warm earthy tones',
            'scenic': 'breathtaking landscape, panoramic view, crystal clear sky, perfect lighting, majestic scenery'
        }

        if vibe in vibe_keywords:
            base_prompt += f", {vibe_keywords[vibe]}"

        base_prompt += ", professional photography, 8K resolution, ultra-realistic, sharp details, cinematic composition"

        return base_prompt

    def generate_image(self, prompt, size="1024x1024", quality="standard", n=1):
        """
        Generate image using DALL-E

        Args:
            prompt: Image prompt
            size: Image size (1024x1024, 1792x1024, 1024x1792)
            quality: Image quality (standard, hd)
            n: Number of images (1-4)

        Returns:
            Image URL(s)
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=n
            )

            return response.data

        except Exception as e:
            raise Exception(f"Error generating image: {str(e)}")

    def download_image(self, url, output_path):
        """
        Download image from URL

        Args:
            url: Image URL
            output_path: Local file path
        """
        import requests

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                f.write(response.content)

            return True

        except Exception as e:
            raise Exception(f"Error downloading image: {str(e)}")

    def generate_travel_photo(
        self,
        destination,
        location_type,
        vibe="scenic",
        time_of_day=None,
        size="1024x1024",
        output_dir="travel_photos"
    ):
        """
        Complete workflow: generate prompt, create image, download

        Args:
            destination: Destination
            location_type: Location
            vibe: Atmosphere
            time_of_day: Time
            size: Image size
            output_dir: Output directory

        Returns:
            Dictionary with prompt, image path, and metadata
        """
        # Generate prompt
        prompt = self.generate_photo_prompt(destination, location_type, vibe, time_of_day)

        print(f"🎨 Generating photo for: {location_type} in {destination}")
        print(f"📝 Prompt: {prompt}\n")

        # Generate image
        images = self.generate_image(prompt, size=size, n=1)
        image_url = images[0].url

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_destination = destination.replace(' ', '_').lower()
        safe_location = location_type.replace(' ', '_').lower()
        filename = f"{safe_destination}_{safe_location}_{timestamp}.png"
        file_path = output_path / filename

        # Download image
        print(f"📥 Downloading image to: {file_path}")
        self.download_image(image_url, file_path)

        print(f"✅ Image saved successfully!\n")

        return {
            'prompt': prompt,
            'image_path': str(file_path),
            'image_url': image_url,
            'metadata': {
                'destination': destination,
                'location': location_type,
                'vibe': vibe,
                'time_of_day': time_of_day,
                'size': size,
                'created_at': datetime.now().isoformat()
            }
        }

    def generate_itinerary_photos(
        self,
        destination,
        activities,
        output_dir="travel_photos"
    ):
        """
        Generate photos for itinerary activities

        Args:
            destination: Destination
            activities: List of activities with time, name, location
            output_dir: Output directory

        Returns:
            List of generated photo info
        """
        results = []

        for activity in activities:
            if 'location' not in activity:
                continue

            # Determine time of day
            time_of_day = None
            time_str = activity.get('time', '')

            if '09:00' in time_str or 'morning' in time_str.lower():
                time_of_day = 'sunrise'
            elif '17:30' in time_str or 'evening' in time_str.lower() or 'sunset' in time_str.lower():
                time_of_day = 'sunset'
            elif '20:00' in time_str or 'night' in time_str.lower():
                time_of_day = 'night'

            # Generate photo
            try:
                result = self.generate_travel_photo(
                    destination=destination,
                    location_type=activity['location'],
                    vibe='romantic',
                    time_of_day=time_of_day,
                    size="1024x1024",
                    output_dir=output_dir
                )
                results.append(result)
            except Exception as e:
                print(f"❌ Error generating photo for {activity['location']}: {e}")

        return results


def save_generation_manifest(results, output_file="image_generation_manifest.json"):
    """
    Save generation manifest

    Args:
        results: List of generation results
        output_file: Output file path
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"📄 Manifest saved to: {output_file}")


def print_usage():
    """Print usage instructions"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                 AI Travel Image Generator                          ║
╚══════════════════════════════════════════════════════════════╝

📝 Setup:

1. Install dependencies:
   pip install openai requests

2. Set your OpenAI API key:
   export OPENAI_API_KEY="your-api-key-here"
   OR pass api_key as parameter

🎯 Usage:

# Generate single photo
python generate_travel_image.py Paris "Eiffel Tower" romantic sunset

# Generate with custom size
python generate_travel_image.py Tokyo "Senso-ji Temple" cultural --size 1792x1024

# Generate from itinerary JSON
python generate_travel_image.py --itinerary paris_itinerary_3days.json

💰 Cost:
- DALL-E 3 Standard (1024x1024): ~$0.04 per image
- DALL-E 3 HD (1024x1024): ~$0.08 per image

📸 Supported Sizes:
- 1024x1024 (Square)
- 1792x1024 (Landscape)
- 1024x1792 (Portrait)

🌅 Supported Times:
- sunrise, sunset, night (or leave empty for natural light)

💫 Supported Vibes:
- romantic, adventurous, cozy, vibrant, cultural, scenic

    """)


def main():
    """Command line interface"""
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print_usage()
        sys.exit(0)

    # Check dependencies
    if not OPENAI_AVAILABLE:
        print("❌ OpenAI library not installed!")
        print("Please install: pip install openai")
        sys.exit(1)

    # Check API key
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key not found!")
        print("Please set OPENAI_API_KEY environment variable:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)

    # Single photo generation
    if len(sys.argv) >= 3 and sys.argv[1] not in ['--itinerary']:
        destination = sys.argv[1]
        location = sys.argv[2]
        vibe = sys.argv[3] if len(sys.argv) > 3 else 'scenic'
        time_of_day = sys.argv[4] if len(sys.argv) > 4 else None

        generator = TravelImageGenerator(api_key=api_key)
        result = generator.generate_travel_photo(
            destination=destination,
            location_type=location,
            vibe=vibe,
            time_of_day=time_of_day
        )

        print(f"\n🎉 Photo generation complete!")
        print(f"📂 Saved to: {result['image_path']}")
        print(f"🔗 URL: {result['image_url']}")

        sys.exit(0)

    # Itinerary photo generation
    if len(sys.argv) > 1 and '--itinerary' in sys.argv:
        itinerary_file = sys.argv[sys.argv.index('--itinerary') + 1]

        # Load itinerary
        with open(itinerary_file, 'r', encoding='utf-8') as f:
            itinerary = json.load(f)

        generator = TravelImageGenerator(api_key=api_key)

        # Generate photos for first 3 activities
        all_activities = []
        for day in itinerary['days'][:1]:  # First day only for demo
            for activity in day['activities'][:3]:  # First 3 activities
                all_activities.append(activity)

        print(f"📸 Generating {len(all_activities)} photos...")
        results = generator.generate_itinerary_photos(
            destination=itinerary['destination'],
            activities=all_activities
        )

        save_generation_manifest(results)

        print(f"\n🎉 Generated {len(results)} photos successfully!")

        sys.exit(0)

    # No valid arguments
    print_usage()
    sys.exit(1)


if __name__ == "__main__":
    main()
