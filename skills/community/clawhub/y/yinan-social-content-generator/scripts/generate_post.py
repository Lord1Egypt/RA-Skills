#!/usr/bin/env python3
"""
Social Media Post Generator
Generate platform-optimized posts with optional AI images.

Usage:
    python generate_post.py --platform twitter --topic "AI tools" --tone professional --include-image
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Try to import openai for image generation
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Platform configurations
PLATFORM_CONFIG = {
    'twitter': {
        'max_length': 280,
        'image_ratios': ['16:9', '1:1'],
        'hashtag_count': (2, 3),
        'emoji_style': 'moderate',
        'template': 'hook_body_cta_hashtags'
    },
    'instagram': {
        'max_length': 2200,
        'image_ratios': ['1:1', '4:5', '9:16'],
        'hashtag_count': (5, 15),
        'emoji_style': 'abundant',
        'template': 'emoji_opener_story_benefits_cta_hashtags'
    },
    'linkedin': {
        'max_length': 3000,
        'image_ratios': ['1.91:1', '1:1'],
        'hashtag_count': (3, 5),
        'emoji_style': 'minimal',
        'template': 'professional_hook_story_takeaway_question_hashtags'
    },
    'facebook': {
        'max_length': 63206,
        'image_ratios': ['1.91:1', '1:1'],
        'hashtag_count': (1, 3),
        'emoji_style': 'moderate',
        'template': 'friendly_hook_content_cta_hashtags'
    }
}

# Tone configurations
TONE_PROMPTS = {
    'professional': 'Write in a professional, authoritative tone. Use clear, concise language.',
    'casual': 'Write in a friendly, conversational tone. Use contractions and informal language.',
    'funny': 'Write in a humorous, witty tone. Include jokes or playful observations.',
    'inspirational': 'Write in an uplifting, motivational tone. Use empowering language.',
    'educational': 'Write in an informative, teaching tone. Break down complex concepts clearly.',
    'controversial': 'Write in a bold, provocative tone. Challenge conventional wisdom.'
}

def generate_post_text(topic, platform, tone, use_ai=True):
    """Generate post text for the specified platform."""
    config = PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG['twitter'])
    tone_prompt = TONE_PROMPTS.get(tone, TONE_PROMPTS['professional'])
    
    if use_ai and HAS_OPENAI:
        # Use OpenAI for text generation
        try:
            client = OpenAI()
            prompt = f"""Generate a {platform} post about "{topic}".

{tone_prompt}

Platform requirements:
- Maximum {config['max_length']} characters
- Include {config['hashtag_count'][0]}-{config['hashtag_count'][1]} relevant hashtags
- Follow the template: {config['template']}
- Use emojis appropriately ({config['emoji_style']})

Generate only the post content, no explanations."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"AI generation failed: {e}, falling back to template...")
    
    # Fallback: Template-based generation
    return generate_template_post(topic, platform, tone, config)

def generate_template_post(topic, platform, tone, config):
    """Generate post using templates (fallback when AI unavailable)."""
    import random
    
    # Simple templates based on platform
    hooks = {
        'twitter': [
            f"🚀 {topic} is changing everything.",
            f"Hot take: {topic} > everything else.",
            f"Nobody talks about {topic} but they should."
        ],
        'instagram': [
            f"✨ {topic} ✨",
            f"POV: You just discovered {topic}",
            f"Let's talk about {topic} 👇"
        ],
        'linkedin': [
            f"The future of {topic} is here.",
            f"What I learned about {topic}:",
            f"Unpopular opinion about {topic}:"
        ],
        'facebook': [
            f"Hey friends! Let's discuss {topic}.",
            f"Thoughts on {topic}?",
            f"Just discovered something cool about {topic}!"
        ]
    }
    
    hashtags = {
        'twitter': ['#Tech', '#Innovation', '#Future'],
        'instagram': ['#TechLife', '#Innovation', '#DigitalLife', '#TechTrends', '#FutureIsNow'],
        'linkedin': ['#Technology', '#Innovation', '#Business', '#Leadership'],
        'facebook': ['#Tech', '#Innovation']
    }
    
    hook = random.choice(hooks.get(platform, hooks['twitter']))
    tags = ' '.join(random.sample(hashtags.get(platform, hashtags['twitter']), 
                                   min(config['hashtag_count'][1], len(hashtags.get(platform, [])))))
    
    return f"{hook}\n\nWhat are your thoughts?\n\n{tags}"

def generate_image_prompt(topic, platform):
    """Generate image prompt for DALL-E."""
    config = PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG['twitter'])
    ratio = config['image_ratios'][0]
    
    return f"Professional, modern image about {topic}. Clean design, vibrant colors, suitable for {platform} social media post. Aspect ratio {ratio}. High quality, eye-catching."

def generate_image(prompt, output_path):
    """Generate image using OpenAI DALL-E."""
    if not HAS_OPENAI:
        print("OpenAI not available, skipping image generation.")
        return None
    
    try:
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Download the image
        import requests
        img_data = requests.get(image_url).content
        with open(output_path, 'wb') as f:
            f.write(img_data)
        
        print(f"✓ Image saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None

def save_post(content, image_path, metadata, output_dir):
    """Save generated post to files."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save text
    text_path = Path(output_dir) / 'post.txt'
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Post saved to {text_path}")
    
    # Save metadata
    meta_path = Path(output_dir) / 'metadata.json'
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"✓ Metadata saved to {meta_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate social media posts')
    parser.add_argument('--platform', required=True, 
                        choices=['twitter', 'instagram', 'linkedin', 'facebook'],
                        help='Target platform')
    parser.add_argument('--topic', required=True, help='Post topic/theme')
    parser.add_argument('--tone', default='professional',
                        choices=['professional', 'casual', 'funny', 'inspirational', 'educational', 'controversial'],
                        help='Writing tone')
    parser.add_argument('--include-image', action='store_true', help='Generate accompanying image')
    parser.add_argument('--image-prompt', help='Custom image prompt (auto-generated if not provided)')
    parser.add_argument('--output', default='.', help='Output directory')
    parser.add_argument('--no-ai', action='store_true', help='Use templates instead of AI')
    args = parser.parse_args()
    
    print(f"Generating {args.platform} post about: {args.topic}")
    print(f"Tone: {args.tone}")
    print()
    
    # Generate text
    post_text = generate_post_text(
        args.topic, 
        args.platform, 
        args.tone,
        use_ai=not args.no_ai
    )
    
    print("Generated post:")
    print("-" * 50)
    print(post_text)
    print("-" * 50)
    print(f"Character count: {len(post_text)}")
    print()
    
    # Generate image if requested
    image_path = None
    if args.include_image:
        image_prompt = args.image_prompt or generate_image_prompt(args.topic, args.platform)
        print(f"Generating image: {image_prompt[:50]}...")
        image_filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image_path = Path(args.output) / image_filename
        generate_image(image_prompt, image_path)
    
    # Save results
    metadata = {
        'platform': args.platform,
        'topic': args.topic,
        'tone': args.tone,
        'generated_at': datetime.now().isoformat(),
        'character_count': len(post_text),
        'has_image': image_path is not None
    }
    
    save_post(post_text, image_path, metadata, args.output)
    
    print("\n✅ Post generation complete!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
