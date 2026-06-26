#!/usr/bin/env python3
"""
RedactKit - Pattern Library
Built-in and custom pattern definitions for PII/secret detection.

Author: Shadow Rose
License: MIT
"""

import re
from typing import Dict, List, Tuple, Pattern
from dataclasses import dataclass


@dataclass
class RedactionPattern:
    """A pattern for detecting sensitive data."""
    name: str
    pattern: Pattern
    category: str  # 'pii', 'secrets', 'financial', 'network'
    sensitivity: str  # 'low', 'medium', 'high'
    description: str
    placeholder_template: str  # e.g., '[EMAIL-{index}]'


class PatternLibrary:
    """Library of built-in patterns for sensitive data detection."""
    
    # Email patterns
    EMAIL = RedactionPattern(
        name='email',
        pattern=re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        category='pii',
        sensitivity='medium',
        description='Email addresses',
        placeholder_template='[EMAIL-{index}]'
    )
    
    # Phone numbers (US and international formats)
    PHONE = RedactionPattern(
        name='phone',
        pattern=re.compile(
            r'(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})|'
            r'\+[0-9]{1,3}[-.\s]?[0-9]{1,14}'
        ),
        category='pii',
        sensitivity='medium',
        description='Phone numbers',
        placeholder_template='[PHONE-{index}]'
    )
    
    # Social Security Numbers (US)
    SSN = RedactionPattern(
        name='ssn',
        pattern=re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        category='pii',
        sensitivity='high',
        description='Social Security Numbers',
        placeholder_template='[SSN-{index}]'
    )
    
    # Credit card numbers
    CREDIT_CARD = RedactionPattern(
        name='credit_card',
        pattern=re.compile(
            r'\b(?:4[0-9]{12}(?:[0-9]{3})?|'  # Visa
            r'5[1-5][0-9]{14}|'  # MasterCard
            r'3[47][0-9]{13}|'  # American Express
            r'3(?:0[0-5]|[68][0-9])[0-9]{11}|'  # Diners Club
            r'6(?:011|5[0-9]{2})[0-9]{12}|'  # Discover
            r'(?:2131|1800|35\d{3})\d{11})\b'  # JCB
        ),
        category='financial',
        sensitivity='high',
        description='Credit card numbers',
        placeholder_template='[CC-{index}]'
    )
    
    # IP addresses (IPv4)
    IP_ADDRESS = RedactionPattern(
        name='ip_address',
        pattern=re.compile(
            r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ),
        category='network',
        sensitivity='low',
        description='IPv4 addresses',
        placeholder_template='[IP-{index}]'
    )
    
    # API keys (generic pattern)
    API_KEY = RedactionPattern(
        name='api_key',
        pattern=re.compile(
            r'\b[A-Za-z0-9_-]{32,}\b|'  # Generic long alphanumeric
            r'(?:api[_-]?key|apikey|token|secret)["\']?\s*[:=]\s*["\']?([A-Za-z0-9_-]{16,})'
        ),
        category='secrets',
        sensitivity='high',
        description='API keys and tokens',
        placeholder_template='[API-KEY-{index}]'
    )
    
    # URLs
    URL = RedactionPattern(
        name='url',
        pattern=re.compile(
            r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&/=]*'
        ),
        category='network',
        sensitivity='low',
        description='URLs',
        placeholder_template='[URL-{index}]'
    )
    
    # AWS Access Key
    AWS_KEY = RedactionPattern(
        name='aws_access_key',
        pattern=re.compile(r'\b(AKIA[0-9A-Z]{16})\b'),
        category='secrets',
        sensitivity='high',
        description='AWS Access Keys',
        placeholder_template='[AWS-KEY-{index}]'
    )
    
    # Private keys (PEM format headers)
    PRIVATE_KEY = RedactionPattern(
        name='private_key',
        pattern=re.compile(r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----'),
        category='secrets',
        sensitivity='high',
        description='Private keys (PEM format)',
        placeholder_template='[PRIVATE-KEY-{index}]'
    )
    
    # Passwords in common formats
    PASSWORD = RedactionPattern(
        name='password',
        pattern=re.compile(
            r'(?:password|passwd|pwd)["\']?\s*[:=]\s*["\']?([^\s"\']{8,})',
            re.IGNORECASE
        ),
        category='secrets',
        sensitivity='high',
        description='Passwords',
        placeholder_template='[PASSWORD-{index}]'
    )
    
    # Person names (simple heuristic: capitalized words)
    # NOTE: This has false positives, but good for high-sensitivity mode
    PERSON_NAME = RedactionPattern(
        name='person_name',
        pattern=re.compile(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'),
        category='pii',
        sensitivity='low',
        description='Potential person names (may have false positives)',
        placeholder_template='[NAME-{index}]'
    )
    
    @classmethod
    def get_all_patterns(cls) -> List[RedactionPattern]:
        """Get all built-in patterns."""
        return [
            cls.EMAIL,
            cls.PHONE,
            cls.SSN,
            cls.CREDIT_CARD,
            cls.IP_ADDRESS,
            cls.API_KEY,
            cls.URL,
            cls.AWS_KEY,
            cls.PRIVATE_KEY,
            cls.PASSWORD,
            cls.PERSON_NAME,
        ]
    
    @classmethod
    def get_by_category(cls, category: str) -> List[RedactionPattern]:
        """Get patterns by category."""
        return [p for p in cls.get_all_patterns() if p.category == category]
    
    @classmethod
    def get_by_sensitivity(cls, min_sensitivity: str) -> List[RedactionPattern]:
        """
        Get patterns meeting minimum sensitivity level.
        
        Args:
            min_sensitivity: 'low', 'medium', or 'high'
        
        Returns:
            List of patterns at or above the sensitivity level
        """
        sensitivity_order = ['low', 'medium', 'high']
        min_level = sensitivity_order.index(min_sensitivity)
        
        return [
            p for p in cls.get_all_patterns()
            if sensitivity_order.index(p.sensitivity) >= min_level
        ]


class CustomPatternManager:
    """Manager for user-defined custom patterns."""
    
    def __init__(self):
        """Initialize custom pattern manager."""
        self.custom_patterns: List[RedactionPattern] = []
    
    def add_pattern(self, name: str, regex: str, category: str,
                   sensitivity: str, description: str,
                   placeholder_template: str = None):
        """
        Add a custom pattern.
        
        Args:
            name: Pattern name (unique identifier)
            regex: Regular expression pattern
            category: Category ('pii', 'secrets', 'financial', 'network', 'custom')
            sensitivity: Sensitivity level ('low', 'medium', 'high')
            description: Human-readable description
            placeholder_template: Template for replacement (default: [CUSTOM-{name}-{index}])
        
        Raises:
            ValueError: If regex is invalid
        """
        try:
            pattern = re.compile(regex)
        except re.error as e:
            raise ValueError(f"Invalid regex: {e}")
        
        if placeholder_template is None:
            placeholder_template = f'[CUSTOM-{name.upper()}-{{index}}]'
        
        redaction_pattern = RedactionPattern(
            name=name,
            pattern=pattern,
            category=category,
            sensitivity=sensitivity,
            description=description,
            placeholder_template=placeholder_template
        )
        
        # Remove existing pattern with same name
        self.custom_patterns = [p for p in self.custom_patterns if p.name != name]
        
        # Add new pattern
        self.custom_patterns.append(redaction_pattern)
    
    def remove_pattern(self, name: str):
        """Remove a custom pattern by name."""
        self.custom_patterns = [p for p in self.custom_patterns if p.name != name]
    
    def get_all(self) -> List[RedactionPattern]:
        """Get all custom patterns."""
        return self.custom_patterns.copy()
    
    def load_from_config(self, config: List[Dict]):
        """
        Load custom patterns from config.
        
        Args:
            config: List of pattern dicts with keys: name, regex, category, sensitivity, description
        """
        for pattern_config in config:
            self.add_pattern(
                name=pattern_config['name'],
                regex=pattern_config['regex'],
                category=pattern_config.get('category', 'custom'),
                sensitivity=pattern_config.get('sensitivity', 'medium'),
                description=pattern_config.get('description', ''),
                placeholder_template=pattern_config.get('placeholder_template')
            )


def main():
    """CLI for testing patterns."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='RedactKit Pattern Tester')
    parser.add_argument('text', nargs='?', help='Text to test (or stdin)')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--sensitivity', default='low', choices=['low', 'medium', 'high'])
    
    args = parser.parse_args()
    
    # Get text
    if args.text:
        text = args.text
    else:
        text = sys.stdin.read()
    
    # Get patterns
    if args.category:
        patterns = PatternLibrary.get_by_category(args.category)
    else:
        patterns = PatternLibrary.get_by_sensitivity(args.sensitivity)
    
    # Test each pattern
    print(f"Testing {len(patterns)} patterns...\n")
    
    for pattern in patterns:
        matches = pattern.pattern.findall(text)
        if matches:
            print(f"✓ {pattern.name} ({pattern.category}, {pattern.sensitivity})")
            print(f"  {pattern.description}")
            print(f"  Found {len(matches)} matches:")
            for match in matches[:3]:  # Show first 3
                match_str = match if isinstance(match, str) else str(match)
                print(f"    - {match_str[:50]}")
            print()


if __name__ == '__main__':
    main()
