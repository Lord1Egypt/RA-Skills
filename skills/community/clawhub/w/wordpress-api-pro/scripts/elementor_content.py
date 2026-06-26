#!/usr/bin/env python3
"""Manage Elementor page content via REST API"""
import argparse, json, os, sys, urllib.request
from base64 import b64encode
from security import warn_insecure_wp_url

def get_elementor_data(url, username, password, post_id):
    """Get Elementor data for a page"""
    api_url = f"{url.rstrip('/')}/wp-json/wp/v2/pages/{post_id}?_fields=id,title,meta"
    credentials = f"{username}:{password}".encode('utf-8')
    auth_header = b64encode(credentials).decode('ascii')
    
    request = urllib.request.Request(api_url)
    request.add_header('Authorization', f'Basic {auth_header}')
    
    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            # Extract _elementor_data from meta
            elementor_data = result.get('meta', {}).get('_elementor_data', '')
            
            if elementor_data:
                # Parse JSON string
                try:
                    parsed_data = json.loads(elementor_data)
                    result['elementor_data_parsed'] = parsed_data
                except json.JSONDecodeError:
                    result['elementor_data_raw'] = elementor_data
            
            return result
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

def update_elementor_data(url, username, password, post_id, elementor_data):
    """Update Elementor data for a page"""
    api_url = f"{url.rstrip('/')}/wp-json/wp/v2/pages/{post_id}"
    credentials = f"{username}:{password}".encode('utf-8')
    auth_header = b64encode(credentials).decode('ascii')
    
    # Prepare meta update
    data = {
        'meta': {
            '_elementor_data': json.dumps(elementor_data) if isinstance(elementor_data, (dict, list)) else elementor_data
        }
    }
    
    request = urllib.request.Request(api_url, data=json.dumps(data).encode('utf-8'), method='POST')
    request.add_header('Authorization', f'Basic {auth_header}')
    request.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

def find_widget_in_elements(elements, widget_id):
    """Recursively find a widget by ID in Elementor data structure"""
    if not isinstance(elements, list):
        return None
    
    for element in elements:
        if element.get('id') == widget_id:
            return element
        
        # Search in nested elements
        if 'elements' in element:
            found = find_widget_in_elements(element['elements'], widget_id)
            if found:
                return found
    
    return None

def update_widget_content(elements, widget_id, content):
    """Update widget content in Elementor data structure"""
    if not isinstance(elements, list):
        return False
    
    for element in elements:
        if element.get('id') == widget_id:
            # Update based on widget type
            widget_type = element.get('widgetType', '')
            
            if widget_type in ['heading', 'text-editor']:
                if 'settings' not in element:
                    element['settings'] = {}
                
                if widget_type == 'heading':
                    element['settings']['title'] = content
                elif widget_type == 'text-editor':
                    element['settings']['editor'] = content
            
            elif widget_type == 'button':
                if 'settings' not in element:
                    element['settings'] = {}
                element['settings']['text'] = content
            
            else:
                # Generic fallback - try to set content in settings
                if 'settings' not in element:
                    element['settings'] = {}
                element['settings']['content'] = content
            
            return True
        
        # Search in nested elements
        if 'elements' in element:
            if update_widget_content(element['elements'], widget_id, content):
                return True
    
    return False

parser = argparse.ArgumentParser(description='Manage Elementor page content')
parser.add_argument('--url', default=os.getenv('WP_URL'))
parser.add_argument('--username', default=os.getenv('WP_USERNAME'))
parser.add_argument('--app-password', default=os.getenv('WP_APP_PASSWORD'))
parser.add_argument('--post-id', type=int, required=True, help='Page ID')
parser.add_argument('--action', choices=['get', 'update'], required=True, help='Action to perform')
parser.add_argument('--widget-id', help='Widget ID to target (for update)')
parser.add_argument('--content', help='New content (for update)')

args = parser.parse_args()

if not all([args.url, args.username, args.app_password]):
    print(json.dumps({"error": "Missing credentials"}), file=sys.stderr)
    sys.exit(1)
warn_insecure_wp_url(args.url)

if args.action == 'get':
    result = get_elementor_data(args.url, args.username, args.app_password, args.post_id)
    print(json.dumps(result, indent=2))

elif args.action == 'update':
    if not args.widget_id or not args.content:
        print(json.dumps({"error": "Both --widget-id and --content required for update"}), file=sys.stderr)
        sys.exit(1)
    
    # First, get current data
    page_data = get_elementor_data(args.url, args.username, args.app_password, args.post_id)
    
    if 'elementor_data_parsed' not in page_data:
        print(json.dumps({"error": "No Elementor data found for this page"}), file=sys.stderr)
        sys.exit(1)
    
    elementor_data = page_data['elementor_data_parsed']
    
    # Update the widget
    if update_widget_content(elementor_data, args.widget_id, args.content):
        # Save back
        result = update_elementor_data(args.url, args.username, args.app_password, args.post_id, elementor_data)
        print(json.dumps({"success": True, "widget_id": args.widget_id, "updated": True}, indent=2))
    else:
        print(json.dumps({"error": f"Widget ID '{args.widget_id}' not found"}), file=sys.stderr)
        sys.exit(1)
