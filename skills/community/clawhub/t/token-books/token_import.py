#!/usr/bin/env python3
"""
TokenBooks - Provider Import Parsers
Import billing data from various AI providers.

Author: Shadow Rose
License: MIT
"""

import csv
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class UsageRecord:
    """Single API usage record."""
    timestamp: str  # ISO format
    provider: str
    model: str
    task: str  # Optional task label
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float


class ImportParser:
    """Base class for import parsers."""
    
    @staticmethod
    def parse(file_path: str) -> List[UsageRecord]:
        """Parse import file into usage records."""
        raise NotImplementedError


class OpenAIParser(ImportParser):
    """Parser for OpenAI CSV exports."""
    
    @staticmethod
    def parse(file_path: str) -> List[UsageRecord]:
        """
        Parse OpenAI CSV export.
        
        Expected columns:
        - Timestamp
        - Model
        - Input Tokens (or Prompt Tokens)
        - Output Tokens (or Completion Tokens)
        - Cost
        """
        records = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Try different column name variants
                timestamp = row.get('Timestamp') or row.get('timestamp') or row.get('Date')
                model = row.get('Model') or row.get('model')
                input_tokens = int(row.get('Input Tokens', 0) or row.get('Prompt Tokens', 0) or 0)
                output_tokens = int(row.get('Output Tokens', 0) or row.get('Completion Tokens', 0) or 0)
                cost = float(row.get('Cost', 0) or row.get('cost', 0) or 0)
                task = row.get('Task', '') or row.get('task', '') or ''
                
                if not timestamp or not model:
                    continue
                
                records.append(UsageRecord(
                    timestamp=timestamp,
                    provider='openai',
                    model=model,
                    task=task,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=input_tokens + output_tokens,
                    cost_usd=cost
                ))
        
        return records


class AnthropicParser(ImportParser):
    """Parser for Anthropic usage JSON."""
    
    @staticmethod
    def parse(file_path: str) -> List[UsageRecord]:
        """
        Parse Anthropic usage JSON.
        
        Expected format:
        {
          "data": [
            {
              "timestamp": "2026-02-21T10:00:00Z",
              "model": "claude-3-opus",
              "input_tokens": 1000,
              "output_tokens": 500
            }
          ]
        }
        """
        records = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both {"data": [...]} and [...] formats
        usage_list = data.get('data', data) if isinstance(data, dict) else data
        
        for item in usage_list:
            timestamp = item.get('timestamp') or item.get('created_at')
            model = item.get('model')
            input_tokens = int(item.get('input_tokens', 0))
            output_tokens = int(item.get('output_tokens', 0))
            task = item.get('task', '')
            
            if not timestamp or not model:
                continue
            
            # Anthropic pricing (as of 2026)
            cost = AnthropicParser._calculate_cost(model, input_tokens, output_tokens)
            
            records.append(UsageRecord(
                timestamp=timestamp,
                provider='anthropic',
                model=model,
                task=task,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                cost_usd=cost
            ))
        
        return records
    
    @staticmethod
    def _calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on Anthropic pricing."""
        # Prices per 1M tokens (2026 estimates)
        pricing = {
            'claude-3-opus': {'input': 15.0, 'output': 75.0},
            'claude-3-sonnet': {'input': 3.0, 'output': 15.0},
            'claude-3-haiku': {'input': 0.25, 'output': 1.25},
        }
        
        # Find matching model
        for model_name, prices in pricing.items():
            if model_name in model.lower():
                input_cost = (input_tokens / 1_000_000) * prices['input']
                output_cost = (output_tokens / 1_000_000) * prices['output']
                return input_cost + output_cost
        
        # Unknown model - return 0
        return 0.0


class CustomCSVParser(ImportParser):
    """Parser for custom CSV format."""
    
    @staticmethod
    def parse(file_path: str, column_mapping: Dict[str, str] = None) -> List[UsageRecord]:
        """
        Parse custom CSV with column mapping.
        
        Args:
            file_path: Path to CSV file
            column_mapping: Dict mapping standard names to CSV columns
                {
                    'timestamp': 'Date',
                    'provider': 'API_Provider',
                    'model': 'Model_Name',
                    'input_tokens': 'Prompt_Tokens',
                    'output_tokens': 'Response_Tokens',
                    'cost': 'Cost_USD'
                }
        """
        if column_mapping is None:
            column_mapping = {}
        
        records = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                timestamp = row.get(column_mapping.get('timestamp', 'timestamp'))
                provider = row.get(column_mapping.get('provider', 'provider'), 'unknown')
                model = row.get(column_mapping.get('model', 'model'))
                input_tokens = int(row.get(column_mapping.get('input_tokens', 'input_tokens'), 0) or 0)
                output_tokens = int(row.get(column_mapping.get('output_tokens', 'output_tokens'), 0) or 0)
                cost = float(row.get(column_mapping.get('cost', 'cost'), 0) or 0)
                task = row.get(column_mapping.get('task', 'task'), '')
                
                if not timestamp or not model:
                    continue
                
                records.append(UsageRecord(
                    timestamp=timestamp,
                    provider=provider.lower(),
                    model=model,
                    task=task,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=input_tokens + output_tokens,
                    cost_usd=cost
                ))
        
        return records


class ImportManager:
    """Manager for importing from multiple sources."""
    
    def __init__(self):
        """Initialize import manager."""
        self.records: List[UsageRecord] = []
    
    def import_openai(self, file_path: str):
        """Import OpenAI CSV."""
        records = OpenAIParser.parse(file_path)
        self.records.extend(records)
        return len(records)
    
    def import_anthropic(self, file_path: str):
        """Import Anthropic JSON."""
        records = AnthropicParser.parse(file_path)
        self.records.extend(records)
        return len(records)
    
    def import_custom_csv(self, file_path: str, column_mapping: Dict[str, str] = None):
        """Import custom CSV."""
        records = CustomCSVParser.parse(file_path, column_mapping)
        self.records.extend(records)
        return len(records)
    
    def get_all_records(self) -> List[UsageRecord]:
        """Get all imported records."""
        return self.records
    
    def export_json(self, output_path: str):
        """Export all records to JSON."""
        data = [
            {
                'timestamp': r.timestamp,
                'provider': r.provider,
                'model': r.model,
                'task': r.task,
                'input_tokens': r.input_tokens,
                'output_tokens': r.output_tokens,
                'total_tokens': r.total_tokens,
                'cost_usd': r.cost_usd
            }
            for r in self.records
        ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)


def main():
    """CLI interface for import."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description='TokenBooks Import - Import billing data'
    )
    parser.add_argument(
        'input',
        help='Input file path'
    )
    parser.add_argument(
        '--provider',
        required=True,
        choices=['openai', 'anthropic', 'custom'],
        help='Provider type'
    )
    parser.add_argument(
        '--output',
        help='Output JSON file (optional)'
    )
    parser.add_argument(
        '--column-map',
        help='Column mapping JSON for custom CSV (optional)'
    )
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = ImportManager()
    
    try:
        if args.provider == 'openai':
            count = manager.import_openai(args.input)
        elif args.provider == 'anthropic':
            count = manager.import_anthropic(args.input)
        elif args.provider == 'custom':
            column_map = None
            if args.column_map:
                with open(args.column_map, 'r') as f:
                    column_map = json.load(f)
            count = manager.import_custom_csv(args.input, column_map)
        
        print(f"✅ Imported {count} records from {args.provider}")
        
        # Export if requested
        if args.output:
            manager.export_json(args.output)
            print(f"✅ Exported to {args.output}")
        else:
            # Print summary
            records = manager.get_all_records()
            total_cost = sum(r.cost_usd for r in records)
            total_tokens = sum(r.total_tokens for r in records)
            
            print(f"\nSummary:")
            print(f"  Total cost: ${total_cost:.2f}")
            print(f"  Total tokens: {total_tokens:,}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
