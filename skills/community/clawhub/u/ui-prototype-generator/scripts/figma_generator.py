#!/usr/bin/env python3
"""
Figma Prototype Generator
Generates Figma designs via API from HTML or reference images
"""

import json
import os
import sys
from pathlib import Path
import base64

# Note: In real implementation, use requests library
# import requests

class FigmaPrototypeGenerator:
    """Generate Figma prototypes via API"""
    
    def __init__(self, access_token=None):
        self.access_token = access_token or self._load_token()
        self.base_url = "https://api.figma.com/v1"
        
    def _load_token(self):
        """Load Figma token from auth-profiles.json"""
        auth_paths = [
            Path.home() / ".openclaw" / "agents" / "main" / "agent" / "auth-profiles.json",
            Path.home() / ".openclaw" / "auth-profiles.json",
            Path.cwd() / "auth-profiles.json"
        ]
        
        for auth_path in auth_paths:
            if auth_path.exists():
                try:
                    with open(auth_path, 'r') as f:
                        auth_data = json.load(f)
                        
                    # Try different structures
                    if 'profiles' in auth_data:
                        figma_auth = auth_data['profiles'].get('figma')
                    elif 'figma' in auth_data:
                        figma_auth = auth_data['figma']
                    else:
                        figma_auth = auth_data
                    
                    if figma_auth and 'access_token' in figma_auth:
                        print(f"✓ Loaded Figma token from {auth_path}")
                        return figma_auth['access_token']
                        
                except Exception as e:
                    print(f"Warning: Could not read {auth_path}: {e}")
                    continue
        
        return None
    
    def check_auth(self):
        """Check if Figma authentication is available"""
        if not self.access_token:
            print("❌ Figma access token not found")
            print("\nTo set up Figma authentication:")
            print("1. Go to https://www.figma.com/settings")
            print("2. Scroll to 'Personal Access Tokens'")
            print("3. Click 'Create new token'")
            print("4. Copy the token (starts with 'figd_')")
            print("5. Save it to auth-profiles.json:")
            print("""
{
  "profiles": {
    "figma": {
      "provider": "figma",
      "access_token": "YOUR_TOKEN_HERE",
      "token_type": "Bearer"
    }
  }
}
            """)
            return False
        
        print("✓ Figma authentication ready")
        return True
    
    def create_prototype(self, name, nodes, file_key=None):
        """Create or update Figma prototype"""
        if not self.check_auth():
            return None
        
        print(f"\n🎨 Creating Figma prototype: {name}")
        print(f"   Nodes: {len(nodes)}")
        
        # In real implementation, this would call Figma API
        # For now, generate a JSON file that can be imported
        
        figma_data = {
            "name": name,
            "type": "DOCUMENT",
            "version": "1.0",
            "children": [
                {
                    "name": "Page 1",
                    "type": "CANVAS",
                    "children": nodes
                }
            ]
        }
        
        # Save to file
        output_file = f"{name.lower().replace(' ', '_')}_figma.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(figma_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Figma prototype data saved: {output_file}")
        print(f"\nTo import into Figma:")
        print("1. Open Figma")
        print("2. Install the 'JSON to Figma' plugin")
        print("3. Run plugin and import the JSON file")
        print("\nOr use the bundled plugin:")
        print("1. Open Figma → Plugins → Development")
        print("2. Import plugin from manifest.json")
        print("3. Run 'UI Prototype Importer'")
        
        return output_file
    
    def convert_html_to_figma(self, html_file):
        """Convert HTML prototype to Figma nodes"""
        print(f"\n📄 Converting HTML: {html_file}")
        
        # Read HTML file
        html_content = Path(html_file).read_text(encoding='utf-8')
        
        # Extract CSS styles
        css_styles = self._extract_css(html_content)
        
        # Parse structure and create nodes
        nodes = self._parse_html_to_nodes(html_content, css_styles)
        
        print(f"✓ Converted {len(nodes)} top-level nodes")
        
        return nodes
    
    def _extract_css(self, html_content):
        """Extract CSS from HTML"""
        import re
        
        styles = {}
        
        # Extract from <style> tags
        style_pattern = r'<style[^>]*>(.*?)</style>'
        style_matches = re.findall(style_pattern, html_content, re.DOTALL)
        
        for style_block in style_matches:
            # Parse CSS rules
            rule_pattern = r'([^{]+)\{([^}]+)\}'
            rules = re.findall(rule_pattern, style_block)
            
            for selector, properties in rules:
                selector = selector.strip()
                styles[selector] = {}
                
                for prop in properties.split(';'):
                    if ':' in prop:
                        key, value = prop.split(':', 1)
                        styles[selector][key.strip()] = value.strip()
        
        return styles
    
    def _parse_html_to_nodes(self, html_content, css_styles):
        """Parse HTML and create Figma nodes"""
        nodes = []
        
        # Simplified parsing - identify common patterns
        import re
        
        # Header pattern
        if 'header' in html_content.lower():
            header_node = {
                "type": "FRAME",
                "name": "Header",
                "x": 0,
                "y": 0,
                "width": 1440,
                "height": 50,
                "fills": [{"type": "SOLID", "color": {"r": 0, "g": 0.08, "b": 0.16}}],
                "children": []
            }
            nodes.append(header_node)
        
        # Sidebar pattern
        if 'sidebar' in html_content.lower():
            sidebar_node = {
                "type": "FRAME",
                "name": "Sidebar",
                "x": 0,
                "y": 50,
                "width": 200,
                "height": 800,
                "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
                "children": []
            }
            nodes.append(sidebar_node)
        
        # Modal pattern
        if 'modal' in html_content.lower():
            modal_node = {
                "type": "FRAME",
                "name": "Modal",
                "x": 420,
                "y": 100,
                "width": 600,
                "height": 500,
                "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
                "cornerRadius": 8,
                "effects": [{
                    "type": "DROP_SHADOW",
                    "color": {"r": 0, "g": 0, "b": 0, "a": 0.15},
                    "offset": {"x": 0, "y": 4},
                    "radius": 12
                }],
                "children": []
            }
            nodes.append(modal_node)
        
        # Table pattern
        if 'table' in html_content.lower():
            table_node = {
                "type": "FRAME",
                "name": "Data Table",
                "x": 220,
                "y": 150,
                "width": 1200,
                "height": 400,
                "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
                "children": []
            }
            nodes.append(table_node)
        
        return nodes
    
    def create_component_library(self):
        """Create Figma component library"""
        components = [
            {
                "type": "COMPONENT",
                "name": "Button/Primary",
                "width": 120,
                "height": 40,
                "fills": [{"type": "SOLID", "color": {"r": 0.094, "g": 0.565, "b": 1}}],
                "cornerRadius": 4
            },
            {
                "type": "COMPONENT",
                "name": "Button/Default",
                "width": 120,
                "height": 40,
                "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
                "strokes": [{"type": "SOLID", "color": {"r": 0.85, "g": 0.85, "b": 0.85}}],
                "cornerRadius": 4
            },
            {
                "type": "COMPONENT",
                "name": "Input/Text",
                "width": 200,
                "height": 35,
                "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
                "strokes": [{"type": "SOLID", "color": {"r": 0.85, "g": 0.85, "b": 0.85}}],
                "cornerRadius": 4
            },
            {
                "type": "COMPONENT",
                "name": "Card",
                "width": 300,
                "height": 200,
                "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1}}],
                "cornerRadius": 8,
                "effects": [{
                    "type": "DROP_SHADOW",
                    "color": {"r": 0, "g": 0, "b": 0, "a": 0.1},
                    "offset": {"x": 0, "y": 2},
                    "radius": 8
                }]
            }
        ]
        
        return components

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Figma prototypes')
    parser.add_argument('--input', '-i', help='Input HTML file')
    parser.add_argument('--name', '-n', default='UI Prototype', help='Prototype name')
    parser.add_argument('--check-auth', action='store_true', help='Check authentication only')
    parser.add_argument('--components', action='store_true', help='Generate component library')
    
    args = parser.parse_args()
    
    generator = FigmaPrototypeGenerator()
    
    if args.check_auth:
        if generator.check_auth():
            print("\n✅ Authentication ready")
            sys.exit(0)
        else:
            print("\n❌ Authentication required")
            sys.exit(1)
    
    elif args.components:
        components = generator.create_component_library()
        output_file = "figma_components.json"
        with open(output_file, 'w') as f:
            json.dump({"components": components}, f, indent=2)
        print(f"✓ Component library saved: {output_file}")
    
    elif args.input:
        # Convert HTML to Figma nodes
        nodes = generator.convert_html_to_figma(args.input)
        
        # Create prototype
        result = generator.create_prototype(args.name, nodes)
        
        if result:
            print(f"\n✅ Success! Output: {result}")
        else:
            print("\n❌ Failed to create prototype")
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()