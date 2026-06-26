#!/usr/bin/env python3
"""
Vadivelu Kaipulla Meme Generator Skill.
Selects random meme image + authentic Vadivelu quote.
"""

import random
import json
import logging
import sys

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Unique Vadivelu meme templates (Imgflip-style URLs; replace with your assets/{})
VADIVELU_MEMES = [
    "https://i.imgflip.com/3v33sx.jpg",  # Classic Kaipulla
    "https://i.imgflip.com/1x057l.jpg",  # Angry Vadivelu
    "https://i.imgflip.com/3uxf0s.jpg",  # Shocked face
    "https://i.imgflip.com/4abcde.jpg",  # Laughing
    "https://i.imgflip.com/5fghij.jpg",  # "Athuvum biotic"
    # Add more: local assets/meme1.jpg via f"{__file__}/../assets/meme1.jpg"
]

# Authentic Vadivelu quotes (Kaipulla style)
VADIVELU_QUOTES = [
    "Kaipulla da!",
    "Athuvum biotic!",
    "Idhu enna thappu?",
    "Super da!",
    "Enna da ivlo aasai?",
    "Ayyo!",
    "Dei poda!",
    "One more time!",
    "Nalla irukku da!",
    "Vida po!"
]

def execute(custom_text: str = None) -> str:
    """
    Main entrypoint for OpenClaw skill execution.
    Args:
        custom_text: Optional user-provided text for meme caption.
    Returns:
        JSON-structured meme response.
    """
    try:
        meme_url = random.choice(VADIVELU_MEMES)
        quote = random.choice(VADIVELU_QUOTES)
        
        response = {
            "status": "success",
            "meme_url": meme_url,
            "quote": quote,
            "custom_text": custom_text or "Random Vadivelu magic! 😂",
            "message": f"😂 **Vadivelu Kaipulla Meme** 😂\n\n![Vadivelu]({meme_url})\n\n**Quote:** \"{quote}\"\n\n**Caption:** {custom_text or 'Pure comedy!'}"
        }
        logger.info(f"Generated meme: {meme_url} with quote '{quote}'")
        return json.dumps(response, indent=2)
    
    except Exception as e:
        error = {"status": "error", "message": f"Vadivelu meme failed: {str(e)}"}
        logger.error(error["message"])
        return json.dumps(error, indent=2)

if __name__ == "__main__":
    # CLI test mode: python agent.py [optional-text]
    args = sys.argv[1:] if len(sys.argv) > 1 else [None]
    print(execute(args[0]))
