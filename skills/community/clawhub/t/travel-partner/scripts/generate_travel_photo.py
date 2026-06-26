#!/usr/bin/env python3
"""
AI Travel Photo Generator
Generate virtual travel check-in photos using AI image generation technology
"""

import json
import sys
import base64
from pathlib import Path


def generate_photo_prompt(destination, location_type, vibe, time_of_day=None):
    """
    Generate photo prompt for AI image generation

    Args:
        destination: Destination (e.g., Paris, Japan, Maldives)
        location_type: Scene type (e.g., Eiffel Tower, temple, beach, cafe)
        vibe: Atmosphere (e.g., romantic, adventurous, cozy, vibrant)
        time_of_day: Time (e.g., sunrise, sunset, night)

    Returns:
        Detailed prompt string
    """
    base_prompt = f"A stunning, high-quality travel photo of {location_type} in {destination}"

    # Add time
    if time_of_day:
        base_prompt += f", captured during {time_of_day}"

    # Add atmosphere
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

    # Add technical details
    base_prompt += ", professional photography, 8K resolution, ultra-realistic, sharp details, cinematic composition"

    return base_prompt


def generate_itinerary_photo_prompts(destination, day_activities):
    """
    Generate photo prompts for day's activities

    Args:
        destination: Destination
        day_activities: Activity list, each activity includes time, location, type

    Returns:
        Prompt list
    """
    prompts = []

    # Morning activities
    morning_activities = [a for a in day_activities if a.get('time', '').lower() in ['morning', 'am', '09:00']]
    if morning_activities:
        act = morning_activities[0]
        prompt = generate_photo_prompt(
            destination=destination,
            location_type=act.get('location'),
            vibe=act.get('vibe', 'peaceful'),
            time_of_day='sunrise'
        )
        prompts.append({
            'activity': act.get('name'),
            'time': 'Morning',
            'prompt': prompt
        })

    # Day activities
    day_activities_list = [a for a in day_activities if a.get('time', '').lower() in ['afternoon', 'noon', '12:00', '14:00']]
    if day_activities_list:
        act = day_activities_list[0]
        prompt = generate_photo_prompt(
            destination=destination,
            location_type=act.get('location'),
            vibe=act.get('vibe', 'vibrant')
        )
        prompts.append({
            'activity': act.get('name'),
            'time': 'Afternoon',
            'prompt': prompt
        })

    # Evening/sunset activities
    evening_activities = [a for a in day_activities if a.get('time', '').lower() in ['evening', 'sunset', '17:30']]
    if evening_activities:
        act = evening_activities[0]
        prompt = generate_photo_prompt(
            destination=destination,
            location_type=act.get('location'),
            vibe=act.get('vibe', 'romantic'),
            time_of_day='sunset'
        )
        prompts.append({
            'activity': act.get('name'),
            'time': 'Sunset',
            'prompt': prompt
        })

    # Night activities
    night_activities = [a for a in day_activities if a.get('time', '').lower() in ['night', 'pm', '20:00']]
    if night_activities:
        act = night_activities[0]
        prompt = generate_photo_prompt(
            destination=destination,
            location_type=act.get('location'),
            vibe=act.get('vibe', 'cozy'),
            time_of_day='night'
        )
        prompts.append({
            'activity': act.get('name'),
            'time': 'Night',
            'prompt': prompt
        })

    return prompts


def generate_landmark_photo_prompt(destination, landmark):
    """
    Generate photo prompt for famous landmarks

    Args:
        destination: Destination
        landmark: Landmark name

    Returns:
        Detailed prompt
    """
    landmark_prompts = {
        'paris': {
            'eiffel_tower': 'Eiffel Tower in Paris with Champ de Mars green lawn in foreground',
            'louvre': 'Louvre Museum with iconic glass pyramid architecture',
            'montmartre': 'colorful Montmartre streets with Sacre-Coeur Basilica in background',
            'seine_river': 'Seine River cruise scene with historic bridges and Parisian buildings'
        },
        'tokyo': {
            'senso_ji': 'Senso-ji Temple with Kaminarimon gate and traditional Japanese architecture',
            'shibuya_crossing': 'famous Shibuya Crossing with crowds and neon lights',
            'teamlab': 'immersive digital art installation at TeamLab Borderless',
            'skytree': 'Tokyo SkyTree tower with panoramic city view'
        },
        'barcelona': {
            'sagrada_familia': 'Sagrada Familia basilica with stunning Gothic architecture',
            'park_guell': 'Park Guell with colorful Gaudi mosaic benches and Barcelona skyline',
            'gothic_quarter': 'narrow medieval streets of Barcelona Gothic Quarter',
            'la_boqueria': 'vibrant La Boqueria Market with colorful food stalls'
        },
        'new_york': {
            'statue_of_liberty': 'Statue of Liberty with New York Harbor skyline',
            'central_park': 'Central Park scenic view with city skyline in background',
            'brooklyn_bridge': 'Brooklyn Bridge with Manhattan skyline at sunset',
            'times_square': 'Times Square with bright neon lights and billboards'
        },
        'santorini': {
            'oia_sunset': 'famous blue domed churches in Oia with stunning sunset',
            'red_beach': 'Red Beach with dramatic red volcanic cliffs',
            'caldera_view': 'caldera cliff view with white buildings and blue domes',
            'amoudi_bay': 'Amoudi Bay fishing village with crystal clear water'
        }
    }

    dest_key = destination.lower().replace(' ', '_')
    landmark_key = landmark.lower().replace(' ', '_').replace("'", '').replace('-', '_')

    if dest_key in landmark_prompts and landmark_key in landmark_prompts[dest_key]:
        base = landmark_prompts[dest_key][landmark_key]
    else:
        base = f"{landmark} in {destination}"

    prompt = f"A stunning travel photo of {base}, professional photography, 8K resolution, ultra-realistic, cinematic lighting, perfect composition"
    return prompt


def create_photo_manifest(prompts, output_file="travel_photo_manifest.json"):
    """
    Create photo generation manifest

    Args:
        prompts: Prompt list or dictionary
        output_file: Output file path
    """
    manifest = {
        'version': '1.0',
        'description': 'AI Travel Photo Generation Prompts',
        'photos': prompts if isinstance(prompts, list) else [prompts]
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"✅ Photo manifest saved to: {output_file}")
    print(f"📸 Total photo prompts: {len(manifest['photos'])}")


def main():
    """
    Command line usage example
    """
    if len(sys.argv) < 3:
        print("Usage:")
        print("  generate_travel_photo.py <destination> <location_type> [vibe] [time_of_day]")
        print("\nExamples:")
        print("  generate_travel_photo.py Paris 'Eiffel Tower' romantic sunset")
        print("  generate_travel_photo.py Tokyo 'Senso-ji Temple' cultural sunrise")
        sys.exit(1)

    destination = sys.argv[1]
    location_type = sys.argv[2]
    vibe = sys.argv[3] if len(sys.argv) > 3 else 'scenic'
    time_of_day = sys.argv[4] if len(sys.argv) > 4 else None

    prompt = generate_photo_prompt(destination, location_type, vibe, time_of_day)
    print(f"\n📸 Photo Prompt for {destination}:")
    print(f"{'='*80}")
    print(f"{prompt}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
