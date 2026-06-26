#!/usr/bin/env python3
"""
Universal Documentation Generator

Extracts system configurations, generates comprehensive references
across multiple programming languages and systems.
"""

import os
import ast
import yaml
import json
import logging
from typing import Dict, Any, List
from datetime import datetime

class UniversalDocGenerator:
    def __init__(self, source_file: str, output_dir: str = 'references'):
        self.source_file = source_file
        self.output_dir = output_dir
        self.logger = self._setup_logging()

    def _setup_logging(self):
        """Configure logging for documentation generation."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - DocGen: %(message)s',
            handlers=[
                logging.FileHandler('doc_generator.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def extract_configuration(self) -> Dict[str, Any]:
        """
        Extract configuration from various source types.
        Supports Python AST parsing, JSON, YAML, and basic language configs.
        """
        ext = os.path.splitext(self.source_file)[1]
        
        extractors = {
            '.py': self._python_config_extract,
            '.json': self._json_config_extract,
            '.yaml': self._yaml_config_extract,
            '.yml': self._yaml_config_extract
        }
        
        extractor = extractors.get(ext, self._default_config_extract)
        return extractor()

    def _python_config_extract(self) -> Dict[str, Any]:
        """Extract configuration from Python files using AST."""
        with open(self.source_file, 'r') as f:
            tree = ast.parse(f.read())
        
        config = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                config[node.name] = {
                    k.id: ast.literal_eval(v) 
                    for k, v in zip(
                        [n for n in node.body if isinstance(n, ast.Name)],
                        [n.value for n in node.body if isinstance(n, ast.Assign)]
                    )
                }
        return config

    def _json_config_extract(self) -> Dict[str, Any]:
        """Extract configuration from JSON files."""
        with open(self.source_file, 'r') as f:
            return json.load(f)

    def _yaml_config_extract(self) -> Dict[str, Any]:
        """Extract configuration from YAML files."""
        with open(self.source_file, 'r') as f:
            return yaml.safe_load(f)

    def _default_config_extract(self) -> Dict[str, Any]:
        """Fallback generic configuration extraction."""
        self.logger.warning(f"Generic extraction for {self.source_file}")
        return {}

    def generate_documentation(self, config: Dict[str, Any]) -> None:
        """
        Generate multi-format documentation.
        
        Outputs:
        - Markdown reference
        - YAML schema
        - JSON details
        """
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Markdown documentation
        output_subdir = os.path.join(self.output_dir, os.path.basename(self.source_file).replace('.py', ''))
        os.makedirs(output_subdir, exist_ok=True)
        with open(os.path.join(output_subdir, 'system_reference.md'), 'w') as md_file:
            md_file.write(f'# System Reference: {os.path.basename(self.source_file)}\n\n')
            md_file.write(f'**Generated:** {datetime.now().isoformat()}\n\n')
            md_file.write('## Configuration\n')
            md_file.write('```yaml\n')
            md_file.write(yaml.dump(config, default_flow_style=False))
            md_file.write('```\n')
        
        # YAML Schema
        with open(os.path.join(self.output_dir, 'system_schema.yaml'), 'w') as yaml_file:
            yaml.dump({
                'source': self.source_file,
                'generated_at': datetime.now().isoformat(),
                'config': config
            }, yaml_file)
        
        # JSON Details
        with open(os.path.join(self.output_dir, 'system_details.json'), 'w') as json_file:
            json.dump({
                'source': self.source_file,
                'generated_at': datetime.now().isoformat(),
                'config': config
            }, json_file, indent=2)
        
        self.logger.info(f"Documentation generated for {self.source_file}")

def main(source_file: str):
    """
    Main entry point for universal documentation generation.
    """
    doc_generator = UniversalDocGenerator(source_file)
    config = doc_generator.extract_configuration()
    doc_generator.generate_documentation(config)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python universal_doc_generator.py <source_file>")
        sys.exit(1)