#!/usr/bin/env python3
\"\"\"Generalized reference updater for any codebase.\"\"\"

import ast
import yaml
import os
from datetime import datetime

def generate_reference(target_path):
    # Parse target file for configs/schemas
    with open(target_path, 'r') as f:
        tree = ast.parse(f.read())
    
    # Extract HALF_LIFE_CONFIG or similar
    config = extract_config(tree)
    
    # Generate MD/YAML
    doc = {
        'schema': config,
        'overview': 'Auto-generated from code.',
        'last_updated': datetime.now().isoformat()
    }
    
    # Write to refs/
    output_dir = 'references/' + os.path.basename(target_path).replace('.py', '') + '_reference'
os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'reference.md'), 'w') as f:
        f.write(f'# {os.path.basename(target_path)} Reference\n\n')
        f.write(f'**Generated:** {datetime.now().isoformat()}\n\n')
        yaml.dump(doc, f, default_flow_style=False)
    
    print('Docs updated.')

def extract_config(tree):
    # AST visitor for config dicts
    return {'example': 'extracted'}

if __name__ == '__main__':
    target = 'sentiment_decay_model.py'
    generate_reference(target)
