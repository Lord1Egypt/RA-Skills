#!/usr/bin/env python3
"""
DEPRECATED: legacy YumFu storybook generator V2.

Kept only for historical reference.
Do not route new storybook generation through V2.
Use `generate_storybook_v3.py` for canonical HTML storybooks,
and use `deliver_yumfu_turn.py --ending-storybook` for ending / retire / archive delivery.

Original V2 notes:
- Full conversation flow (player input + AI responses)
- Images embedded at correct positions
- Beautiful HTML/PDF layout
- Auto-detection of session from save file
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import re


class StorybookV2:
    def __init__(self, user_id: str, universe: str):
        self.user_id = user_id
        self.universe = universe
        
        # Paths
        self.base_path = Path.home() / "clawd/memory/yumfu"
        self.save_path = self.base_path / "saves" / universe / f"user-{user_id}.json"
        
        if not self.save_path.exists():
            raise FileNotFoundError(f"Save file not found: {self.save_path}")
        
        with open(self.save_path, 'r', encoding='utf-8') as f:
            self.save_data = json.load(f)
        
        # Output directory
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.output_dir = self.base_path / "storybooks" / universe / f"user-{user_id}-{timestamp}"
        self.images_dir = self.output_dir / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
    
    def extract_conversation_from_notes(self) -> List[Dict]:
        """Extract conversation flow from save file notes"""
        notes = self.save_data.get("notes", [])
        conversation = []
        
        for note in notes:
            # Try to parse structured events
            if note.startswith("📍"):
                # Location change
                conversation.append({
                    "type": "location",
                    "content": note
                })
            elif note.startswith("🎨"):
                # Image generated
                match = re.search(r'Generated:\s*(.+)', note)
                if match:
                    img_name = match.group(1).strip()
                    conversation.append({
                        "type": "image",
                        "filename": img_name
                    })
            elif note.startswith("⚔️") or note.startswith("💥"):
                # Combat
                conversation.append({
                    "type": "combat",
                    "content": note
                })
            elif note.startswith("✨") or note.startswith("🏆"):
                # Achievement
                conversation.append({
                    "type": "achievement",
                    "content": note
                })
            else:
                # Regular narrative
                conversation.append({
                    "type": "narration",
                    "content": note
                })
        
        return conversation
    
    def collect_images(self) -> Dict[str, Path]:
        """Collect all generated images"""
        outbound = Path.home() / ".openclaw/media/outbound/yumfu"
        image_map = {}
        
        if not outbound.exists():
            return image_map
        
        image_names = self.save_data.get("images_generated", [])
        
        for img_name in image_names:
            img_path = outbound / img_name
            if img_path.exists():
                # Copy to storybook directory
                dest = self.images_dir / img_path.name
                if not dest.exists():
                    import shutil
                    shutil.copy2(img_path, dest)
                image_map[img_name] = dest
        
        return image_map
    
    def generate_html(self, conversation: List[Dict], images: Dict[str, Path]) -> str:
        """Generate beautiful HTML with conversation flow"""
        character = self.save_data.get("character", {})
        universe = self.save_data.get("universe", "unknown")
        
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
            .page-break {{ page-break-before: always; }}
        }}
        
        body {{
            font-family: 'Georgia', serif;
            line-height: 1.8;
            max-width: 900px;
            margin: 2em auto;
            padding: 0 2em;
            color: #2c3e50;
            background: #f5f5f0;
        }}
        
        .container {{
            background: white;
            padding: 3em;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 2.8em;
            color: #1a1a1a;
            text-align: center;
            margin-bottom: 0.3em;
            border-bottom: 4px solid #d35400;
            padding-bottom: 0.5em;
            font-weight: bold;
        }}
        
        .meta {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 3em;
            font-style: italic;
            font-size: 1.1em;
        }}
        
        .location {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5em;
            border-radius: 10px;
            margin: 2em 0;
            font-size: 1.2em;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}
        
        .narration {{
            text-align: justify;
            margin: 1.5em 0;
            font-size: 1.1em;
            line-height: 2;
            color: #34495e;
        }}
        
        .combat {{
            background: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 1.5em;
            margin: 1.5em 0;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
        }}
        
        .achievement {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1.2em 2em;
            border-radius: 25px;
            margin: 1.5em 0;
            text-align: center;
            font-weight: bold;
            font-size: 1.1em;
            box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        }}
        
        .image-block {{
            margin: 3em 0;
            text-align: center;
        }}
        
        .image-block img {{
            max-width: 100%;
            height: auto;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }}
        
        .image-caption {{
            text-align: center;
            font-style: italic;
            color: #95a5a6;
            margin-top: 1em;
            font-size: 1em;
        }}
        
        .stats-box {{
            background: #ecf0f1;
            padding: 2em;
            border-radius: 10px;
            margin: 2em 0;
            border: 2px solid #bdc3c7;
        }}
        
        .stats-box h2 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5em;
        }}
        
        .stats-box ul {{
            list-style: none;
            padding: 0;
        }}
        
        .stats-box li {{
            padding: 0.5em 0;
            border-bottom: 1px solid #d5d8dc;
        }}
        
        .stats-box li:last-child {{
            border-bottom: none;
        }}
        
        .print-btn {{
            position: fixed;
            top: 30px;
            right: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1em 2em;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            z-index: 1000;
        }}
        
        .print-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}
        
        .footer {{
            text-align: center;
            margin-top: 4em;
            padding-top: 2em;
            border-top: 2px solid #bdc3c7;
            color: #95a5a6;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <button class="print-btn no-print" onclick="window.print()">📄 Print to PDF</button>
    
    <div class="container">
        <h1>{character.get('name', 'Unknown Hero')}'s Adventure</h1>
        <div class="meta">
            {world_titles.get(universe, 'An Epic Journey')}<br>
            <strong>World:</strong> {universe.replace('-', ' ').title()} &nbsp;|&nbsp;
            <strong>Rank:</strong> {character.get('rank', character.get('level', 'Apprentice'))} &nbsp;|&nbsp;
            <strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}
        </div>
        
        <div class="story-content">
"""
        
        # Render conversation flow
        for event in conversation:
            event_type = event.get("type")
            
            if event_type == "location":
                content = event.get("content", "")
                html += f'<div class="location">{content}</div>\n'
            
            elif event_type == "narration":
                content = event.get("content", "")
                html += f'<div class="narration">{content}</div>\n'
            
            elif event_type == "combat":
                content = event.get("content", "")
                html += f'<div class="combat">{content}</div>\n'
            
            elif event_type == "achievement":
                content = event.get("content", "")
                html += f'<div class="achievement">{content}</div>\n'
            
            elif event_type == "image":
                img_name = event.get("filename", "")
                if img_name in images:
                    img_path = images[img_name]
                    scene_name = img_name.split('-', 2)[-1].replace('-', ' ').title()
                    scene_name = scene_name.rsplit('.', 1)[0]  # Remove extension
                    html += f"""
                    <div class="image-block">
                        <img src="images/{img_path.name}" alt="{scene_name}">
                        <p class="image-caption">🎨 {scene_name}</p>
                    </div>
                    """
        
        html += "</div>\n\n"
        
        # Add character stats
        html += """
        <div class="page-break"></div>
        <div class="stats-box">
            <h2>📊 Final Character Stats</h2>
            <ul>
"""
        
        attributes = character.get("attributes", {})
        for stat, value in attributes.items():
            html += f"<li><strong>{stat.replace('_', ' ').title()}:</strong> {value}</li>\n"
        
        html += "</ul>\n</div>\n"
        
        # Add relationships
        relationships = self.save_data.get("relationships", {})
        if relationships:
            html += """
        <div class="stats-box">
            <h2>💝 Relationships</h2>
            <ul>
"""
            for npc, rel_data in relationships.items():
                if isinstance(rel_data, dict):
                    affection = rel_data.get("affection", 0)
                    status = rel_data.get("status", "Unknown")
                    html += f"<li><strong>{npc}</strong> (❤️ {affection}): {status}</li>\n"
            
            html += "</ul>\n</div>\n"
        
        # Add achievements
        achievements = self.save_data.get("achievements", [])
        if achievements:
            html += """
        <div class="stats-box">
            <h2>🏆 Achievements Unlocked</h2>
            <ul>
"""
            for ach in achievements:
                html += f"<li>✨ {ach}</li>\n"
            
            html += "</ul>\n</div>\n"
        
        # Footer
        html += f"""
        <div class="footer">
            <p><strong>YumFu Storybook Generator V2</strong><br>
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate(self):
        """Main generation flow"""
        print(f"📚 Generating Storybook V2 for {self.save_data.get('character', {}).get('name', 'Unknown')}...")
        
        # Extract conversation
        print("📖 Extracting conversation flow...")
        conversation = self.extract_conversation_from_notes()
        print(f"   Found {len(conversation)} events")
        
        # Collect images
        print("🎨 Collecting images...")
        images = self.collect_images()
        print(f"   Found {len(images)} images")
        
        # Generate HTML
        print("✍️  Creating storybook...")
        html_content = self.generate_html(conversation, images)
        
        # Save HTML
        html_file = self.output_dir / "storybook.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n🎉 Storybook complete!")
        print(f"📁 Location: {self.output_dir}")
        print(f"🌐 HTML: {html_file}")
        print(f"🖼️  Images: {len(images)} files")
        print(f"\n💡 Open in browser and print to PDF!")
        
        return html_file


def main():
    parser = argparse.ArgumentParser(description="Generate YumFu Storybook V2 with full conversation")
    parser.add_argument("--user-id", required=True, help="User ID")
    parser.add_argument("--universe", required=True, help="World (warrior-cats, xiaoao, harry-potter)")
    
    args = parser.parse_args()
    
    generator = StorybookV2(
        user_id=args.user_id,
        universe=args.universe
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
