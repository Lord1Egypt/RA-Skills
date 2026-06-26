#!/usr/bin/env python3
"""Template Tool - Generate code templates."""

import argparse
import os
import sys
from pathlib import Path


TEMPLATES = {
    'python': {
        'description': 'Python package structure',
        'files': {
            '__init__.py': '# {name}\n',
            'main.py': '''#!/usr/bin/env python3
"""Main module for {name}."""

def main():
    print("Hello from {name}!")

if __name__ == '__main__':
    main()
''',
            'requirements.txt': '# Add your dependencies here\nrequests>=2.28.0\n',
            'setup.py': '''from setuptools import setup, find_packages

setup(
    name="{name}",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
)
''',
            'README.md': '''# {name}

A Python project.

## Installation

```bash
pip install {name}
```

## Usage

```python
import {name}
```
'''
        }
    },
    'javascript': {
        'description': 'Node.js project',
        'files': {
            'package.json': '''{{
  "name": "{name}",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {{
    "start": "node index.js",
    "test": "echo \\"Error: no test specified\\" && exit 1"
  }},
  "keywords": [],
  "author": "",
  "license": "ISC"
}}
''',
            'index.js': '''const main = () => {{
  console.log("Hello from {name}!");
}};

main();
''',
            'README.md': '''# {name}

A Node.js project.

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```
'''
        }
    },
    'api': {
        'description': 'REST API project',
        'files': {
            'main.py': '''#!/usr/bin/env python3
"""REST API for {name}."""

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({{"message": "Welcome to {name} API"}})

@app.route('/health')
def health():
    return jsonify({{"status": "ok"}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
''',
            'requirements.txt': '''flask>=2.0.0
flask-cors>=3.0.0
''',
            'README.md': '''# {name} API

REST API built with Flask.

## Running

```bash
pip install -r requirements.txt
python main.py
```

## Endpoints

- GET / - Root
- GET /health - Health check
'''
        }
    },
    'docker': {
        'description': 'Docker Compose project',
        'files': {
            'docker-compose.yml': '''version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
''',
            'Dockerfile': '''FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8000

CMD ["npm", "start"]
''',
            'README.md': '''# {name}

Docker Compose project.

## Running

```bash
docker-compose up
```
'''
        }
    },
    'readme': {
        'description': 'README.md file',
        'files': {
            'README.md': '''# {name}

> A short description

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
# Add installation steps
```

## Usage

```bash
# Add usage examples
```

## License

MIT
'''
        }
    },
    'gitignore': {
        'description': '.gitignore file',
        'files': {
            '.gitignore': '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
'''
        }
    },
    'dockerfile': {
        'description': 'Dockerfile',
        'files': {
            'Dockerfile': '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
'''
        }
    },
    'class': {
        'description': 'Python class template',
        'files': {
            '{name}.py': '''class {Name}:
    """A class that does something."""
    
    def __init__(self, param1, param2=None):
        self.param1 = param1
        self.param2 = param2
    
    def do_something(self):
        """Do something."""
        pass
    
    def __str__(self):
        return f"{self.__class__.__name__}(param1={self.param1})"
'''
        }
    },
    'function': {
        'description': 'JavaScript function',
        'files': {
            'index.js': '''/**
 * {name} - A function that does something
 * @param {string} param1 - Description
 * @param {number} param2 - Description
 * @returns {string} Result
 */
function {Name}(param1, param2 = 10) {{
  // Implementation
  return `Result: ${{param1}}`;
}}

module.exports = {Name};
'''
        }
    },
    'react': {
        'description': 'React component',
        'files': {
            '{name}.jsx': '''import React from 'react';

const {Name} = ({{ title = 'Default' }}) => {{
  return (
    <div className="{name}">
      <h1>{{title}}</h1>
    </div>
  );
}};

export default {Name};
''',
            'index.js': '''export { default } from './{Name}';
'''
        }
    }
}


def list_templates():
    """List available templates."""
    print("Available templates:")
    print("-" * 40)
    for name, info in TEMPLATES.items():
        print(f"  {name:15} - {info['description']}")


def create_template(template_name: str, name: str, output_dir: str = "."):
    """Create a template."""
    if template_name not in TEMPLATES:
        print(f"Error: Unknown template '{template_name}'")
        print("Use --list to see available templates")
        return False
    
    template = TEMPLATES[template_name]
    output_path = Path(output_dir)
    
    # Convert name to appropriate format
    safe_name = name.replace(' ', '_').replace('-', '_')
    class_name = ''.join(word.capitalize() for word in name.replace('-', ' ').split())
    
    print(f"Creating {template['description']} in {output_dir}/")
    
    for filename, content in template['files'].items():
        # Replace placeholders
        filename = filename.format(name=safe_name, Name=class_name)
        content = content.format(name=safe_name, Name=class_name)
        
        file_path = output_path / filename
        
        # Create parent directories
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"  Created: {filename}")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Code template generator')
    parser.add_argument('template', nargs='?', help='Template to use')
    parser.add_argument('--name', '-n', help='Project/component name')
    parser.add_argument('--output', '-o', default='.', help='Output directory')
    parser.add_argument('--list', '-l', action='store_true', help='List templates')
    
    args = parser.parse_args()
    
    if args.list:
        list_templates()
        return
    
    if not args.template:
        parser.print_help()
        print("\nExamples:")
        print("  template-tool --list")
        print("  template-tool python --name myproject")
        print("  template-tool api --name users-api")
        print("  template-tool readme --name 'My Project'")
        return
    
    if not args.name:
        print("Error: --name is required")
        return
    
    create_template(args.template, args.name, args.output)


if __name__ == '__main__':
    main()
