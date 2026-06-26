"""
Social Media Content Generator for OpenClaw
"""

import os
import json
import argparse
from PIL import Image, ImageDraw
from datetime import datetime

BRANDS = {
    "leveluplove": {
        "colors": {"primary": "#FF6B9D", "secondary": "#C084FC"},
        "vibe": "romantic"
    },
    "paylesstax": {
        "colors": {"primary": "#2563EB", "secondary": "#10B981"},
        "vibe": "professional"
    }
}

SPECS = {
    "carousel": {"width": 1080, "height": 1080, "panels": 4},
    "infographic": {"width": 1080, "height": 1350},
    "image": {"width": 1080, "height": 1080},
    "oneliner": {"width": 1080, "height": 1080}
}

class Generator:
    def __init__(self, brand, content_type):
        self.brand = brand
        self.content_type = content_type
        self.config = BRANDS[brand]
        self.specs = SPECS[content_type]

    def generate(self, data, output_path):
        width, height = self.specs["width"], self.specs["height"]
        colors = self.config["colors"]

        if self.content_type == "carousel":
            panels = self.specs["panels"]
            img = Image.new('RGB', (width, height * panels), "#FFFFFF")
            draw = ImageDraw.Draw(img)
            for i in range(panels):
                y = i * height
                draw.rectangle([0, y, width, y + height], fill=colors["primary"])
                text = data.get("panels", [{}])[i].get("text", f"Panel {i+1}") if i < len(data.get("panels", [])) else f"Panel {i+1}"
                draw.text((50, y + 50), text[:50], fill="#FFFFFF")
        else:
            img = Image.new('RGB', (width, height), colors["primary"])
            draw = ImageDraw.Draw(img)
            headline = data.get("headline", "Headline")
            draw.text((100, height//2 - 50), headline[:60], fill="#FFFFFF")

        ts = datetime.now().strftime("%s")
        fn = f"{self.brand}_{self.content_type}_{ts}.png"
        fp = os.path.join(output_path, fn)
        img.save(fp)
        return fp

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--brand', choices=['leveluplove', 'paylesstax'], required=True)
    p.add_argument('--type', choices=['carousel', 'infographic', 'image', 'oneliner'], required=True)
    p.add_argument('--template', help='JSON template path')
    p.add_argument('--output', default='./output')
    p.add_argument('--headline', default='Headline')
    args = p.parse_args()

    data = json.load(open(args.template)) if args.template and os.path.exists(args.template) else {"headline": args.headline}
    os.makedirs(args.output, exist_ok=True)
    result = Generator(args.brand, args.type).generate(data, args.output)
    print(f"Generated: {result}")
