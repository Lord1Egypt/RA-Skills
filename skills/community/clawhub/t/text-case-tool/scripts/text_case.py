#!/usr/bin/env python3
"""
Text Case Converter - Convert text between different case formats
"""
import argparse
import re

def to_upper(text):
    return text.upper()

def to_lower(text):
    return text.lower()

def to_title(text):
    return text.title()

def to_sentence(text):
    if not text:
        return text
    return text[0].upper() + text[1:].lower()

def to_camel(text):
    # Remove special chars and convert to camelCase
    words = re.split(r'[\s\-_]+', text)
    if not words:
        return text
    return words[0].lower() + ''.join(w.capitalize() for w in words[1:])

def to_pascal(text):
    # PascalCase (UpperCamelCase)
    words = re.split(r'[\s\-_]+', text)
    return ''.join(w.capitalize() for w in words)

def to_snake(text):
    # snake_case
    # Handle camelCase/PascalCase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    # Replace spaces and hyphens
    s3 = re.sub(r'[\s\-]+', '_', s2)
    return s3.lower()

def to_kebab(text):
    # kebab-case
    # Handle camelCase/PascalCase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', text)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1)
    # Replace spaces and underscores
    s3 = re.sub(r'[\s_]+', '-', s2)
    return s3.lower()

def to_constant(text):
    # CONSTANT_CASE
    return to_snake(text).upper()

def main():
    parser = argparse.ArgumentParser(
        description='Convert text between different case formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 text_case.py "hello world" --upper
  python3 text_case.py "HELLO WORLD" --lower
  python3 text_case.py "hello world" --camel
  python3 text_case.py "HelloWorld" --snake
        """
    )
    
    parser.add_argument('text', help='Text to convert')
    parser.add_argument('--upper', action='store_true', help='UPPER CASE')
    parser.add_argument('--lower', action='store_true', help='lower case')
    parser.add_argument('--title', action='store_true', help='Title Case')
    parser.add_argument('--sentence', action='store_true', help='Sentence case')
    parser.add_argument('--camel', action='store_true', help='camelCase')
    parser.add_argument('--pascal', action='store_true', help='PascalCase')
    parser.add_argument('--snake', action='store_true', help='snake_case')
    parser.add_argument('--kebab', action='store_true', help='kebab-case')
    parser.add_argument('--constant', action='store_true', help='CONSTANT_CASE')
    
    args = parser.parse_args()
    
    converters = {
        'upper': to_upper,
        'lower': to_lower,
        'title': to_title,
        'sentence': to_sentence,
        'camel': to_camel,
        'pascal': to_pascal,
        'snake': to_snake,
        'kebab': to_kebab,
        'constant': to_constant,
    }
    
    # Find which converter to use
    for name, func in converters.items():
        if getattr(args, name):
            result = func(args.text)
            print(result)
            return
    
    # Default: show all conversions
    print(f"Input: {args.text}")
    print(f"  upper:      {to_upper(args.text)}")
    print(f"  lower:      {to_lower(args.text)}")
    print(f"  title:      {to_title(args.text)}")
    print(f"  sentence:   {to_sentence(args.text)}")
    print(f"  camel:      {to_camel(args.text)}")
    print(f"  pascal:     {to_pascal(args.text)}")
    print(f"  snake:      {to_snake(args.text)}")
    print(f"  kebab:      {to_kebab(args.text)}")
    print(f"  constant:   {to_constant(args.text)}")

if __name__ == '__main__':
    main()
