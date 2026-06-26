#!/usr/bin/env python3
"""
Generate travel maps using the generic template with unique map ID for localStorage isolation.
This replaces the Shanghai template with a clean generic version that has:
- No city-specific references
- Unique map ID based on POI names to prevent localStorage conflicts
- Proper placeholder replacement for dynamic content
- Real FlyAI hotel search integration
- Professional UX improvements
"""

import os
import sys
import json
import argparse
import re

# Import configuration
try:
    from .config import WORKSPACE_DIR
except ImportError:
    # Fallback for standalone execution
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, SCRIPT_DIR)
    from config import WORKSPACE_DIR

def load_generic_template():
    """Load the generic template with unique map ID support"""
    template_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', 'main-generic-template-with-unique-id.html')
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Generic template with unique ID not found: {template_path}")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_poi_js_array(pois):
    """Generate JavaScript POI array from POI list"""
    js_lines = []
    
    for poi in pois:
        name = poi.get('name', 'Unnamed Location')
        address = poi.get('address', '')
        rating = poi.get('rating', '')
        poi_id = poi.get('id', '')
        
        # Handle location coordinates
        if isinstance(poi.get('location'), list) and len(poi['location']) == 2:
            lng, lat = poi['location'][0], poi['location'][1]
        else:
            # Use approximate coordinates if not available (shouldn't happen with proper geocoding)
            lng, lat = 116.4074, 39.9042  # Beijing default
        
        js_lines.append('            {')
        js_lines.append(f'                name: "{name}",')
        js_lines.append(f'                location: [{lng}, {lat}],')
        js_lines.append(f'                address: "{address}",')
        js_lines.append(f'                rating: "{rating}",')
        js_lines.append(f'                id: "{poi_id}"')
        js_lines.append('            },')
    
    # Remove trailing comma from last item if exists
    if len(js_lines) > 0:
        js_lines[-1] = '            }'
    
    return '\n'.join(js_lines)

def replace_placeholders(template_content, pois):
    """Replace placeholders in the template with actual content"""
    if not pois:
        raise ValueError("No POIs provided")
    
    # Get first POI coordinates for map center
    first_poi = pois[0]
    if isinstance(first_poi.get('location'), list) and len(first_poi['location']) == 2:
        first_lng, first_lat = first_poi['location'][0], first_poi['location'][1]
    else:
        first_lng, first_lat = 116.4074, 39.9042  # Beijing default
    
    # Replace map center coordinates
    template_content = template_content.replace('[FIRST_POI_LNG, FIRST_POI_LAT]', f'[{first_lng}, {first_lat}]')
    
    # Generate POI list
    poi_js = generate_poi_js_array(pois)
    
    # Replace POI list placeholder
    template_content = template_content.replace('        var poiList = [\n            // POI_LIST_PLACEHOLDER - will be replaced with actual POIs\n        ];', f'        var poiList = [\n{poi_js}\n        ];')
    
    # Ensure hotel port placeholder exists (for main script to replace later)
    if 'HOTEL_SEARCH_PORT_PLACEHOLDER' not in template_content:
        # If no placeholder found, add a comment indicating it should be there
        print("Warning: HOTEL_SEARCH_PORT_PLACEHOLDER not found in template")
    
    return template_content

def main():
    parser = argparse.ArgumentParser(description='Generate travel map using generic template with unique map ID')
    parser.add_argument('input_file', help='Input JSON file with geocoded POIs')
    parser.add_argument('output_file', help='Output HTML file path')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)
    
    # Load POIs
    with open(args.input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    # Extract POIs
    if isinstance(input_data, list):
        pois = input_data
    elif 'filtered_geocoded_pois' in input_data:
        pois = input_data['filtered_geocoded_pois']
    elif 'geocoded_pois' in input_data:
        pois = input_data['geocoded_pois']
    else:
        print("Error: Input file must contain POIs in 'filtered_geocoded_pois', 'geocoded_pois', or as root array", file=sys.stderr)
        sys.exit(1)
    
    if not pois:
        print("Error: No POIs found in input file", file=sys.stderr)
        sys.exit(1)
    
    # Load template
    try:
        template_content = load_generic_template()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Replace placeholders
    try:
        updated_content = replace_placeholders(template_content, pois)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Write output
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Travel map generated using generic template with unique map ID: {args.output_file}")
    print(f"\n💡 IMPORTANT: To view the map properly, start a local HTTP server:")
    print(f"   cd {WORKSPACE_DIR}")
    print(f"   python3 -m http.server 9999")
    print(f"   Then open: http://localhost:9999/{os.path.basename(args.output_file)}")

if __name__ == '__main__':
    main()