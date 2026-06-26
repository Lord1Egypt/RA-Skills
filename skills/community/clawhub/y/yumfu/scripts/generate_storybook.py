#!/usr/bin/env python3
"""
DEPRECATED: legacy YumFu storybook generator.

Do not use this for new flows.
Use `generate_storybook_v3.py` for canonical HTML storybooks,
and use `deliver_yumfu_turn.py --ending-storybook` for ending / retire / archive delivery.
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class StorybookGenerator:
    def __init__(self, user_id: str, universe: str, session_id: str = None):
        self.user_id = user_id
        self.universe = universe
        self.session_id = session_id or datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # Paths
        self.base_path = Path.home() / "clawd/memory/yumfu"
        self.storybook_dir = self.base_path / "storybooks" / universe / f"user-{user_id}-{self.session_id}"
        self.images_dir = self.storybook_dir / "images"
        self.html_file = self.storybook_dir / "storybook.html"
        
        # Create directories
        self.storybook_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        
    def load_save_file(self) -> Dict:
        """Load user's save file"""
        save_path = self.base_path / "saves" / self.universe / f"user-{self.user_id}.json"
        if not save_path.exists():
            raise FileNotFoundError(f"Save file not found: {save_path}")
        
        with open(save_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def collect_images(self) -> List[Path]:
        """Collect all images generated in this session"""
        outbound = Path.home() / ".openclaw/media/outbound/yumfu"
        if not outbound.exists():
            return []
        
        save_data = self.load_save_file()
        image_names = save_data.get("images_generated", [])
        
        images = []
        for img_name in image_names:
            img_path = outbound / img_name
            if img_path.exists():
                # Copy to storybook images directory
                dest = self.images_dir / img_path.name
                if not dest.exists():
                    import shutil
                    shutil.copy2(img_path, dest)
                images.append(dest)
        
        return images
    
    def generate_html(self, save_data: Dict, images: List[Path]) -> str:
        """Generate beautiful HTML storybook"""
        character = save_data.get("character", {})
        universe = save_data.get("universe", "unknown")
        
        # World-specific titles
        world_titles = {
            "warrior-cats": "A Warrior Cats Tale",
            "xiaoao": "笑傲江湖传奇",
            "harry-potter": "A Hogwarts Adventure"
        }
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{character.get('name', 'Hero')}'s Adventure</title>
    <style>
        @media print {{
            body {{ margin: 0.5in; }}
            .no-print {{ display: none; }}
        }}
        
        body {{
            font-family: 'Georgia', serif;
            line-height: 1.8;
            max-width: 800px;
            margin: 2em auto;
            padding: 0 2em;
            color: #333;
            background: #f9f9f9;
        }}
        
        .container {{
            background: white;
            padding: 3em;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 2.5em;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 0.5em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.5em;
        }}
        
        .meta {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 2em;
            font-style: italic;
        }}
        
        h2 {{
            font-size: 1.8em;
            color: #34495e;
            margin-top: 2em;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 0.3em;
        }}
        
        h3 {{
            font-size: 1.3em;
            color: #7f8c8d;
            margin-top: 1.5em;
        }}
        
        p {{
            text-align: justify;
            margin-bottom: 1em;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 2em auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .caption {{
            text-align: center;
            font-style: italic;
            color: #7f8c8d;
            margin-top: -1em;
            margin-bottom: 2em;
        }}
        
        ul, ol {{
            margin-left: 2em;
        }}
        
        li {{
            margin-bottom: 0.5em;
        }}
        
        .stats {{
            background: #ecf0f1;
            padding: 1.5em;
            border-radius: 8px;
            margin: 1.5em 0;
        }}
        
        .achievement {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 0.5em 1em;
            border-radius: 20px;
            margin: 0.5em;
            font-size: 0.9em;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 3em;
            padding-top: 2em;
            border-top: 1px solid #bdc3c7;
            color: #95a5a6;
            font-size: 0.9em;
        }}
        
        .print-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #3498db;
            color: white;
            border: none;
            padding: 1em 2em;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}
        
        .print-btn:hover {{
            background: #2980b9;
        }}
    </style>
</head>
<body>
    <button class="print-btn no-print" onclick="window.print()">📄 Print to PDF</button>
    
    <div class="container">
        <h1>{character.get('name', 'Unknown Hero')}: {world_titles.get(universe, 'An Epic Journey')}</h1>
        
        <div class="meta">
            <strong>Universe:</strong> {universe.replace('-', ' ').title()} &nbsp;|&nbsp;
            <strong>Rank:</strong> {character.get('rank', character.get('level', 'Apprentice'))} &nbsp;|&nbsp;
            <strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}
        </div>
        
        <h2>📖 The Story Begins</h2>
"""
        
        # Add notes as story chapters
        notes = save_data.get("notes", [])
        for i, note in enumerate(notes, 1):
            html += f"<h3>Chapter {i}</h3>\n<p>{note}</p>\n\n"
        
        # Add images with captions
        if images:
            html += f"<h2>🎨 Moments Captured</h2>\n\n"
            for img in images:
                scene_name = img.stem.split('-', 2)[-1].replace('-', ' ').title()
                html += f"""
                <div>
                    <img src="images/{img.name}" alt="{scene_name}">
                    <p class="caption">{scene_name}</p>
                </div>
                """
        
        # Add achievements
        achievements = save_data.get("achievements", [])
        if achievements:
            html += f"<h2>🏆 Achievements Unlocked</h2>\n"
            for ach in achievements:
                html += f'<span class="achievement">✨ {ach}</span>\n'
            html += "\n"
        
        # Add character stats
        html += f"<h2>📊 Final Stats</h2>\n<div class='stats'>\n<ul>\n"
        attributes = character.get("attributes", {})
        for stat, value in attributes.items():
            html += f"<li><strong>{stat.replace('_', ' ').title()}:</strong> {value}</li>\n"
        html += "</ul>\n</div>\n"
        
        # Add relationships
        relationships = save_data.get("relationships", {})
        if relationships:
            html += f"<h2>💝 Bonds Formed</h2>\n<ul>\n"
            for npc, rel_data in relationships.items():
                if isinstance(rel_data, dict):
                    affection = rel_data.get("affection", 0)
                    status = rel_data.get("status", "Unknown")
                    html += f"<li><strong>{npc}</strong> (❤️ {affection}): {status}</li>\n"
            html += "</ul>\n"
        
        # Footer
        html += f"""
        <div class="footer">
            <p>Generated by YumFu Storybook Generator<br>
            Session ID: {self.session_id}</p>
        </div>
        
    </div>
</body>
</html>
"""
        
        return html
    
    def generate(self):
        """Main generation flow"""
        print(f"📚 Generating storybook for session {self.session_id}...")
        
        # Load save data
        print("📖 Loading adventure data...")
        save_data = self.load_save_file()
        
        # Collect images
        print("🎨 Collecting images...")
        images = self.collect_images()
        print(f"   Found {len(images)} images")
        
        # Generate HTML
        print("✍️  Creating storybook...")
        html_content = self.generate_html(save_data, images)
        
        # Save HTML
        with open(self.html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n🎉 Storybook complete!\n")
        print(f"📁 Location: {self.storybook_dir}")
        print(f"🌐 HTML: {self.html_file}")
        print(f"🖼️  Images: {len(images)} files in images/")
        print(f"\n💡 To create PDF: Open HTML in browser and print to PDF")
        
        return self.html_file


def main():
    parser = argparse.ArgumentParser(description="Generate YumFu adventure storybook")
    parser.add_argument("--user-id", required=True, help="User ID")
    parser.add_argument("--universe", required=True, help="World (warrior-cats, xiaoao, harry-potter)")
    parser.add_argument("--session-id", help="Optional session ID")
    
    args = parser.parse_args()
    
    generator = StorybookGenerator(
        user_id=args.user_id,
        universe=args.universe,
        session_id=args.session_id
    )
    
    html_file = generator.generate()
    
    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(f"file://{html_file}")
        print(f"\n🌐 Opened in browser!")
    except:
        print(f"\n💡 Open manually: file://{html_file}")


if __name__ == "__main__":
    main()
