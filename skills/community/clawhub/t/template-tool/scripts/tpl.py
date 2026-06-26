#!/usr/bin/env python3
"""Template Tool - Process text templates."""

import argparse
import json
import re
import sys
import os


def process_template(template: str, variables: dict) -> str:
    """Process template with variables."""
    result = template
    
    # Simple variable substitution {{variable}}
    def replace_var(match):
        var_name = match.group(1).strip()
        
        # Check for default value
        if '|' in var_name:
            var_name, default = var_name.split('|', 1)
            var_name = var_name.strip()
            default = default.strip()
        
        value = variables.get(var_name, default if 'default' in locals() else '')
        return str(value)
    
    result = re.sub(r'\{\{([^}]+)\}\}', replace_var, result)
    
    # Simple conditionals {{#if variable}}...{{/if}}
    def replace_if(match):
        var_name = match.group(1).strip()
        content = match.group(2)
        
        if variables.get(var_name):
            return content
        return ''
    
    result = re.sub(r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}', replace_if, result, flags=re.DOTALL)
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Template processing tool')
    parser.add_argument('template', nargs='?', help='Template string or file')
    parser.add_argument('--vars', '-v', nargs='+', help='Variables (key=value)')
    parser.add_argument('--var-file', '-f', help='JSON file with variables')
    parser.add_argument('--list', '-l', action='store_true', help='List templates')
    parser.add_argument('--init', metavar='NAME', help='Create template file')
    
    args = parser.parse_args()
    
    # List templates
    if args.list:
        print("Available templates:")
        print("  email - Basic email template")
        print("  html - HTML page template")
        print("  json - JSON template")
        return
    
    # Initialize template
    if args.init:
        templates = {
            'email': '''Subject: {{subject}}
To: {{to}}
From: {{from}}

{{body}}
''',
            'html': '''<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
</head>
<body>
    <h1>{{heading}}</h1>
    {{content}}
</body>
</html>
''',
            'json': '''{
    "name": "{{name}}",
    "value": {{value}},
    "enabled": {{enabled}}
}
'''
        }
        
        if args.init in templates:
            with open(f"{args.init}.txt", 'w') as f:
                f.write(templates[args.init])
            print(f"Created template: {args.init}.txt")
        else:
            print(f"Unknown template: {args.init}", file=sys.stderr)
            print("Use --list to see available templates", file=sys.stderr)
        return
    
    # Parse variables
    variables = {}
    
    if args.vars:
        for var in args.vars:
            if '=' in var:
                key, value = var.split('=', 1)
                variables[key] = value
    
    if args.var_file:
        try:
            with open(args.var_file, 'r') as f:
                file_vars = json.load(f)
                variables.update(file_vars)
        except Exception as e:
            print(f"Error reading variable file: {e}", file=sys.stderr)
            sys.exit(1)
    
    if not args.template:
        parser.print_help()
        return
    
    # Read template
    if os.path.isfile(args.template):
        with open(args.template, 'r') as f:
            template = f.read()
    else:
        template = args.template
    
    # Process
    result = process_template(template, variables)
    print(result)


if __name__ == '__main__':
    main()
