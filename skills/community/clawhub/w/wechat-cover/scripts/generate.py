#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "openai>=1.12.0",
#     "pillow>=10.0.0",
#     "google-genai>=0.8.0",
# ]
# ///
"""
WeChat Cover Image Generator

Generates cover images optimized for WeChat official accounts (2.35:1 aspect ratio)
using a provider-agnostic client architecture.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Literal


# Settings file path (relative to generate.py)
SETTINGS_PATH = Path(__file__).parent.parent / "settings.json"


def load_settings() -> dict:
    """Load settings from settings.json if it exists."""
    if SETTINGS_PATH.exists():
        try:
            with open(SETTINGS_PATH) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


SETTINGS = load_settings()


from openai_client import OpenAIImageClient
from gemini_client import GeminiImageClient
from image_client import ImageClient, ImageGenerationError


# Style variants — Claude-like aesthetic with specific color palettes and composition
STYLE_VARIANTS: dict[str, str] = {
    "default": (
        "Warm minimalist aesthetic inspired by Anthropic's Claude design language. "
        "Color palette: cream white (#FAF9F6), warm beige (#F5F0EB), soft coral (#E8A87C), "
        "muted sage (#B5C4B1), warm gray (#C4C1BE). "
        "Clean organic shapes and subtle gradients. "
        "Soft diffused natural lighting with no harsh shadows. "
        "Generous negative space, balanced asymmetric composition. "
        "Smooth matte textures, no gloss or reflective surfaces. "
        "Evokes calm intelligence and understated sophistication."
    ),
    "tech": (
        "Modern tech aesthetic inspired by Anthropic's Claude design language. "
        "Color palette: cool off-white (#F4F6F8), soft slate blue (#94A3B8), "
        "misty lavender (#C7D2FE), pale cyan (#A5F3FC), warm silver (#D1D5DB). "
        "Abstract geometric lines and flowing data-inspired curves. "
        "Subtle glass morphism and soft glowing edges. "
        "Cool diffused lighting with gentle gradients. "
        "Clean grid-based composition with breathing room. "
        "Evokes quiet innovation and thoughtful technology."
    ),
    "business": (
        "Professional aesthetic inspired by Anthropic's Claude design language. "
        "Color palette: warm white (#FEFDFB), navy accent (#1E3A5F), "
        "charcoal (#374151), amber accent (#D4A574), cool gray (#9CA3AF). "
        "Clean architectural lines and structured geometric shapes. "
        "Natural window lighting with soft directional shadows. "
        "Centered or rule-of-thirds composition with clear hierarchy. "
        "Matte finishes, subtle paper textures. "
        "Evokes trustworthiness, clarity, and calm authority."
    ),
    "lifestyle": (
        "Warm lifestyle aesthetic inspired by Anthropic's Claude design language. "
        "Color palette: warm cream (#FFF8F0), blush pink (#F9E4D4), "
        "soft sage (#D4E2D0), golden hour (#F5D89A), terracotta (#D4956A). "
        "Organic natural textures, soft rounded shapes, gentle curves. "
        "Warm golden-hour lighting with soft bokeh-like depth. "
        "Relaxed off-center composition with natural framing. "
        "Hand-crafted tactile quality, linen and paper textures. "
        "Evokes warmth, comfort, and authentic living."
    ),
    "creative": (
        "Refined creative aesthetic inspired by Anthropic's Claude design language. "
        "Color palette: crisp white (#FFFFFF), coral red (#E06C5C), "
        "deep teal (#2D6A6A), golden yellow (#E9B44C), soft purple (#9B8EC2). "
        "Bold yet restrained abstract geometric composition. "
        "Dynamic asymmetric layout with strong focal point. "
        "Bright even lighting, vivid but not oversaturated colors. "
        "Mix of sharp edges and organic curves, paper-cut aesthetic. "
        "Evokes creative energy and artistic confidence."
    ),
}

# Topic keyword → visual metaphor mapping
_TOPIC_VISUAL_HINTS: list[tuple[list[str], str]] = [
    (
        ["ai", "artificial intelligence", "machine learning", "deep learning", "llm", "gpt", "claude", "agent"],
        "neural network patterns, interconnected glowing nodes, abstract brain topology, flowing data streams",
    ),
    (
        ["tech", "software", "programming", "code", "developer", "engineering", "api", "cloud"],
        "abstract circuit patterns, clean geometric grids, floating code symbols, digital layers",
    ),
    (
        ["business", "startup", "entrepreneur", "growth", "revenue", "profit", "scale"],
        "upward growth lines, clean bar chart abstractions, architectural perspective, structured layouts",
    ),
    (
        ["finance", "invest", "stock", "crypto", "blockchain", "defi", "trading"],
        "abstract chart curves, flowing data lines, geometric coin shapes, clean number patterns",
    ),
    (
        ["lifestyle", "food", "travel", "nature", "health", "fitness", "cooking"],
        "natural organic textures, warm ambient scenes, botanical elements, handcrafted objects",
    ),
    (
        ["design", "creative", "art", "aesthetic", "ui", "ux", "brand"],
        "color swatches, abstract geometric composition, design tools, playful shapes",
    ),
    (
        ["productivity", "tool", "app", "workflow", "automation", "efficiency"],
        "clean workflow diagrams, connected modules, streamlined shapes, organized spaces",
    ),
    (
        ["education", "learn", "course", "tutorial", "book", "reading", "study"],
        "open book silhouettes, geometric learning paths, stacked layers, clean knowledge symbols",
    ),
]

# Table-driven keyword matching: (keywords, style_name)
_TOPIC_STYLE_CHECKS: list[tuple[list[str], str]] = [
    (["tech", "ai", "software", "programming", "code", "computer", "digital", "data"], "tech"),
    (["business", "startup", "entrepreneur", "finance", "investment", "market"], "business"),
    (["life", "lifestyle", "food", "travel", "nature", "health", "fitness", "fashion"], "lifestyle"),
    (["creative", "art", "design", "photo", "video", "music"], "creative"),
]


def get_style(topic: str | None, style_arg: str | None) -> str:
    """
    Resolve the style to use based on topic and explicit style argument.

    Args:
        topic: The article topic/category
        style_arg: Explicit style variant name or custom style string

    Returns:
        Style description string
    """
    # If explicit style variant provided, use it
    if style_arg is not None:
        if style_arg in STYLE_VARIANTS:
            return STYLE_VARIANTS[style_arg]
        return style_arg

    if topic is None:
        return STYLE_VARIANTS["default"]

    topic_lower = topic.lower()
    for keywords, style_name in _TOPIC_STYLE_CHECKS:
        if any(kw in topic_lower for kw in keywords):
            return STYLE_VARIANTS[style_name]

    return STYLE_VARIANTS["default"]


def get_visual_hints(topic: str | None) -> str:
    """Get visual metaphor hints based on topic keywords."""
    if not topic:
        return ""
    topic_lower = topic.lower()
    hints: list[str] = []
    for keywords, hint in _TOPIC_VISUAL_HINTS:
        if any(kw in topic_lower for kw in keywords):
            hints.append(hint)
    return "; ".join(hints) if hints else "abstract visual metaphor representing the topic"


def build_prompt(title: str, topic: str | None, style: str | None = None) -> str:
    """
    Build the image generation prompt for WeChat cover.

    Uses a 6-section structured prompt for consistent, high-quality output
    aligned with Claude's design aesthetic.

    Args:
        title: Article title
        topic: Article topic/category
        style: Optional style override

    Returns:
        Formatted prompt string
    """
    resolved_style = get_style(topic, style)
    visual_hints = get_visual_hints(topic)

    prompt = f"""Article: "{title}"
Topic: {topic or "general"}

STYLE: {resolved_style}

COMPOSITION:
Ultra-wide 2.35:1 cinematic aspect ratio. Place the main subject in the center-left third, leaving the right third as clean breathing space for title overlay. Use rule-of-thirds grid. Maintain generous margins — do not fill edge-to-edge. The image should feel spacious, not crowded. Single clear focal point, no secondary competing elements.

VISUAL ELEMENTS:
{visual_hints}. Render as clean, stylized illustration — NOT photorealistic. Use simplified geometric forms and smooth gradients. The composition should feel designed, not photographed. Layer 2-3 visual elements maximum with clear depth hierarchy: one dominant foreground element and subtle background texture.

LIGHTING & TEXTURE:
Soft diffused lighting with no harsh shadows or high contrast. Matte surface finish throughout. If gradients are used, make them gentle and nearly imperceptible. The overall feel should be warm, calm, and inviting — like a premium print advertisement.

AVOID:
No text, no letters, no numbers, no watermarks, no logos, no UI elements, no people's faces, no photorealistic rendering, no dark backgrounds, no neon colors, no cluttered compositions, no heavy shadows, no 3D perspective distortion. The image must be clean enough to serve as a professional magazine cover."""

    return prompt.strip()


def generate_filename(title: str) -> str:
    """
    Generate filename based on title and timestamp.

    Handles both Chinese and English titles by extracting key words
    and transliterating where needed.

    Args:
        title: Article title

    Returns:
        Generated filename string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d")
    # Remove punctuation, keep alphanumeric and CJK characters
    cleaned = re.sub(r'[^\w\u4e00-\u9fff]', ' ', title)
    # Split into words (works for both Chinese and English)
    words = cleaned.split()[:4]
    short_title = "-".join(words).lower()
    # Remove any remaining non-ASCII/non-hyphen characters for filesystem safety
    short_title = "".join(
        c for c in short_title if c.isalnum() or c in "-\u4e00-\u9fff"
    )[:40]
    if not short_title:
        short_title = "untitled"
    return f"{timestamp}-wechat-cover-{short_title}.png"


def resolve_provider(
    provider: Literal["openai", "gemini"],
    base_url: str | None,
    model: str | None,
) -> ImageClient:
    """
    Resolve the image generation provider to a client instance.

    Priority: CLI argument > settings.json > hardcoded default

    Args:
        provider: Provider name ("openai" or "gemini")
        base_url: Optional base URL for OpenAI-compatible APIs
        model: Optional model override

    Returns:
        An ImageClient implementation instance

    Raises:
        ValueError: If provider is unknown
    """
    # Get defaults from settings.json
    provider_settings = SETTINGS.get(provider, {})

    if provider == "openai":
        model_name = model or provider_settings.get("model", "dall-e-3")
        resolved_base_url = base_url or provider_settings.get("base_url")
        return OpenAIImageClient(model=model_name, base_url=resolved_base_url)
    elif provider == "gemini":
        model_name = model or provider_settings.get("model", "gemini-3-pro-image-preview")
        return GeminiImageClient(model=model_name)
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_api_key_for_provider(provider: Literal["openai", "gemini"], api_key: str | None) -> str:
    """
    Get the API key for the specified provider.

    Priority: CLI argument > settings.json > environment variable

    Args:
        provider: Provider name
        api_key: Explicitly provided API key

    Returns:
        API key string

    Raises:
        ValueError: If no API key is available
    """
    if api_key:
        return api_key

    # Check settings.json first
    provider_settings = SETTINGS.get(provider, {})
    if provider_settings.get("api_key"):
        return provider_settings["api_key"]

    # Check environment variables
    env_vars = {
        "openai": ["OPENAI_API_KEY", "OPENAI_API_KEY_1"],
        "gemini": ["GEMINI_API_KEY", "GEMINI_API_KEY_1"],
    }

    for env_var in env_vars.get(provider, []):
        key = os.environ.get(env_var)
        if key:
            return key

    raise ValueError(
        f"No API key provided for {provider}. "
        f"Set it in settings.json, {env_vars[provider][0]} environment variable, or use --api-key argument."
    )


def retry_with_backoff(
    func,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> None:
    """
    Retry a function with exponential backoff.

    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay after each retry

    Returns:
        The return value of func if successful

    Raises:
        The last exception if all retries fail
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= backoff_factor

    raise last_exception


def main() -> None:
    """CLI entry point."""
    # Get defaults from settings.json
    default_provider = SETTINGS.get("default_provider", "openai")
    default_resolution = SETTINGS.get("default_resolution", "2K")
    default_style = SETTINGS.get("default_style", "default")
    default_base_url = SETTINGS.get("openai", {}).get("base_url") or os.environ.get("OPENAI_BASE_URL")

    parser = argparse.ArgumentParser(
        description="Generate WeChat cover images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--topic", required=True, help="Topic/category")
    parser.add_argument(
        "--provider",
        default=default_provider,
        choices=["openai", "gemini"],
        help=f"Image generation provider (default: {default_provider})",
    )
    parser.add_argument(
        "--base-url",
        default=default_base_url,
        help="Base URL for OpenAI-compatible API (default: from settings.json or OPENAI_BASE_URL env var)",
    )
    parser.add_argument(
        "--model",
        help="Model override (e.g., dall-e-3, gemini-3-pro-image-preview)",
    )
    parser.add_argument(
        "--style",
        default=default_style,
        help=f"Style variant (default, tech, business, lifestyle, creative) or custom style string (default: {default_style})",
    )
    parser.add_argument(
        "--filename",
        help="Output filename (auto-generated if not provided)",
    )
    parser.add_argument(
        "--resolution",
        default=default_resolution,
        choices=["1K", "2K", "4K"],
        help=f"Image resolution (default: {default_resolution})",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "--api-key",
        help="API key (or set in settings.json / environment variable)",
    )

    args = parser.parse_args()

    # Resolve API key
    try:
        api_key = get_api_key_for_provider(args.provider, args.api_key)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Resolve provider client
    try:
        client = resolve_provider(args.provider, args.base_url, args.model)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Generate filename and output path
    filename = args.filename or generate_filename(args.title)
    output_dir = Path(args.output_dir)
    output_path = output_dir / filename

    # Build prompt
    prompt = build_prompt(args.title, args.topic, args.style)

    # Print summary
    print(f"Generating WeChat cover for: {args.title}")
    print(f"Topic: {args.topic}")
    print(f"Style: {get_style(args.topic, args.style)[:60]}...")
    print(f"Provider: {args.provider}")
    print(f"Resolution: {args.resolution}")
    print(f"Output: {output_path}")
    print()

    # Generate image with retry
    def generate_image() -> None:
        client.generate(
            prompt=prompt,
            filename=str(output_path),
            resolution=args.resolution,
            api_key=api_key,
        )

    try:
        retry_with_backoff(generate_image)
        print(f"Successfully generated: {output_path}")
    except ImageGenerationError as e:
        print(f"Error generating image: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()