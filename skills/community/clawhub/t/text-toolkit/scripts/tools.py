from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def case_to_camel(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to camelCase
    
    Args:
        text: The text to transform to camelCase
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_camel", arguments)

def case_to_pascal(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to PascalCase
    
    Args:
        text: The text to transform to PascalCase
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_pascal", arguments)

def case_to_snake(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to snake_case
    
    Args:
        text: The text to transform to snake_case
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_snake", arguments)

def case_to_kebab(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to kebab-case
    
    Args:
        text: The text to transform to kebab-case
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_kebab", arguments)

def case_to_constant(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to CONSTANT_CASE
    
    Args:
        text: The text to transform to CONSTANT_CASE
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_constant", arguments)

def case_to_dot(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to dot.case
    
    Args:
        text: The text to transform to dot.case
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_dot", arguments)

def case_to_no(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to no case
    
    Args:
        text: The text to transform to no case
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_no", arguments)

def case_to_pascal_snake(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to Pascal_Snake_Case
    
    Args:
        text: The text to transform to Pascal_Snake_Case
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_pascal_snake", arguments)

def case_to_path(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to path/case
    
    Args:
        text: The text to transform to path/case
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_path", arguments)

def case_to_sentence(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to Sentence case
    
    Args:
        text: The text to transform to Sentence case
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_sentence", arguments)

def case_to_train(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to Train-Case
    
    Args:
        text: The text to transform to Train-Case
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_train", arguments)

def case_to_capital(
    text: str,
    delimiter: Optional[str] = None,
    locale: Optional[null] = None,
    mergeAmbiguousCharacters: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Convert text to Capital Case
    
    Args:
        text: The text to transform to Capital Case
        delimiter: The character to use between words (optional)
        locale: Locale for case conversion (optional)
        mergeAmbiguousCharacters: Whether to merge ambiguous characters (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "locale": locale,
        "mergeAmbiguousCharacters": mergeAmbiguousCharacters
    }
    
    return call_api("1777316659720195", "case_to_capital", arguments)

def encode_base64(
    text: str
) -> Dict[str, Any]:
    """
    Encode text to Base64
    
    Args:
        text: The text to encode or decode
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "encode_base64", arguments)

def decode_base64(
    text: str
) -> Dict[str, Any]:
    """
    Decode Base64 to text
    
    Args:
        text: The text to encode or decode
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "decode_base64", arguments)

def encode_url(
    text: str
) -> Dict[str, Any]:
    """
    Encode text for URLs
    
    Args:
        text: The text to encode or decode
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "encode_url", arguments)

def decode_url(
    text: str
) -> Dict[str, Any]:
    """
    Decode URL-encoded text
    
    Args:
        text: The text to encode or decode
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "decode_url", arguments)

def encode_html(
    text: str
) -> Dict[str, Any]:
    """
    Encode HTML entities
    
    Args:
        text: The text to encode or decode
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "encode_html", arguments)

def decode_html(
    text: str
) -> Dict[str, Any]:
    """
    Decode HTML entities
    
    Args:
        text: The text to encode or decode
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "decode_html", arguments)

def format_json(
    text: str,
    indent_size: Optional[int] = 2.0
) -> Dict[str, Any]:
    """
    Format and beautify JSON
    
    Args:
        text: The text to format
        indent_size: Number of spaces for indentation (1-8)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "indent_size": indent_size
    }
    
    return call_api("1777316659720195", "format_json", arguments)

def format_xml(
    text: str,
    indent_size: Optional[int] = 2.0
) -> Dict[str, Any]:
    """
    Format and beautify XML
    
    Args:
        text: The text to format
        indent_size: Number of spaces for indentation (1-8)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "indent_size": indent_size
    }
    
    return call_api("1777316659720195", "format_xml", arguments)

def format_sql(
    text: str,
    indent_size: Optional[int] = 2.0
) -> Dict[str, Any]:
    """
    Format and beautify SQL
    
    Args:
        text: The text to format
        indent_size: Number of spaces for indentation (1-8)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "indent_size": indent_size
    }
    
    return call_api("1777316659720195", "format_sql", arguments)

def format_html(
    text: str,
    indent_size: Optional[int] = 2.0
) -> Dict[str, Any]:
    """
    Format and beautify HTML
    
    Args:
        text: The text to format
        indent_size: Number of spaces for indentation (1-8)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "indent_size": indent_size
    }
    
    return call_api("1777316659720195", "format_html", arguments)

def count_characters(
    text: str
) -> Dict[str, Any]:
    """
    Count characters in text
    
    Args:
        text: The text to analyze
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "count_characters", arguments)

def count_words(
    text: str
) -> Dict[str, Any]:
    """
    Count words in text
    
    Args:
        text: The text to analyze
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "count_words", arguments)

def count_lines(
    text: str
) -> Dict[str, Any]:
    """
    Count lines in text
    
    Args:
        text: The text to analyze
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "count_lines", arguments)

def analyze_readability(
    text: str
) -> Dict[str, Any]:
    """
    Calculate readability metrics
    
    Args:
        text: The text to analyze
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "analyze_readability", arguments)

def string_trim(
    text: str,
    trim_type: Optional[str] = "both"
) -> Dict[str, Any]:
    """
    Trim whitespace from text
    
    Args:
        text: The text to trim
        trim_type: Type of trimming to perform
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "trim_type": trim_type
    }
    
    return call_api("1777316659720195", "string_trim", arguments)

def string_substring(
    text: str,
    start: Optional[int] = 0.0,
    end: Optional[int] = None
) -> Dict[str, Any]:
    """
    Extract a substring
    
    Args:
        text: The text to extract a substring from
        start: Starting index (inclusive)
        end: Ending index (exclusive, optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "start": start,
        "end": end
    }
    
    return call_api("1777316659720195", "string_substring", arguments)

def string_replace(
    text: str,
    search: str,
    replace: str,
    replace_all: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Replace text
    
    Args:
        text: The text to perform replacements on
        search: The string to search for
        replace: The string to replace with
        replace_all: Whether to replace all occurrences
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "search": search,
        "replace": replace,
        "replace_all": replace_all
    }
    
    return call_api("1777316659720195", "string_replace", arguments)

def string_split(
    text: str,
    delimiter: Optional[str] = " ",
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Split text into an array
    
    Args:
        text: The text to split
        delimiter: The delimiter to split by
        limit: Maximum number of splits (optional)
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "delimiter": delimiter,
        "limit": limit
    }
    
    return call_api("1777316659720195", "string_split", arguments)

def string_join(
    parts: null,
    delimiter: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Join an array into text
    
    Args:
        parts: The array of strings to join
        delimiter: The delimiter to join with
    
    Returns:
        
    """
    arguments = {
        "parts": parts,
        "delimiter": delimiter
    }
    
    return call_api("1777316659720195", "string_join", arguments)

def generate_uuid(
    version: Optional[str] = "v4",
    namespace: Optional[str] = None,
    name: Optional[str] = None,
    uppercase: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Generate a UUID
    
    Args:
        version: UUID version to generate
        namespace: Namespace for v5 UUID (required for v5)
        name: Name for v5 UUID (required for v5)
        uppercase: Whether to return the UUID in uppercase
    
    Returns:
        
    """
    arguments = {
        "version": version,
        "namespace": namespace,
        "name": name,
        "uppercase": uppercase
    }
    
    return call_api("1777316659720195", "generate_uuid", arguments)

def validate_uuid(
    uuid: str
) -> Dict[str, Any]:
    """
    Validate a UUID
    
    Args:
        uuid: The UUID to validate
    
    Returns:
        
    """
    arguments = {
        "uuid": uuid
    }
    
    return call_api("1777316659720195", "validate_uuid", arguments)

def generate_md5(
    text: str
) -> Dict[str, Any]:
    """
    Generate MD5 hash
    
    Args:
        text: The text to hash
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "generate_md5", arguments)

def generate_sha1(
    text: str
) -> Dict[str, Any]:
    """
    Generate SHA-1 hash
    
    Args:
        text: The text to hash
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "generate_sha1", arguments)

def generate_sha256(
    text: str
) -> Dict[str, Any]:
    """
    Generate SHA-256 hash
    
    Args:
        text: The text to hash
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "generate_sha256", arguments)

def generate_sha512(
    text: str
) -> Dict[str, Any]:
    """
    Generate SHA-512 hash
    
    Args:
        text: The text to hash
    
    Returns:
        
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659720195", "generate_sha512", arguments)

def generate_hmac(
    text: str,
    key: str,
    algorithm: Optional[str] = "SHA256"
) -> Dict[str, Any]:
    """
    Generate HMAC hash
    
    Args:
        text: The text to hash
        key: The secret key for HMAC
        algorithm: The hashing algorithm to use
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "key": key,
        "algorithm": algorithm
    }
    
    return call_api("1777316659720195", "generate_hmac", arguments)

def generate_lorem_ipsum(
    count: Optional[int] = 5.0,
    units: Optional[str] = "sentences",
    paragraphLowerBound: Optional[int] = 3.0,
    paragraphUpperBound: Optional[int] = 7.0,
    sentenceLowerBound: Optional[int] = 5.0,
    sentenceUpperBound: Optional[int] = 15.0,
    format: Optional[str] = "plain"
) -> Dict[str, Any]:
    """
    Generate lorem ipsum text
    
    Args:
        count: Number of units to generate
        units: Type of units to generate
        paragraphLowerBound: Minimum sentences per paragraph
        paragraphUpperBound: Maximum sentences per paragraph
        sentenceLowerBound: Minimum words per sentence
        sentenceUpperBound: Maximum words per sentence
        format: Output format
    
    Returns:
        
    """
    arguments = {
        "count": count,
        "units": units,
        "paragraphLowerBound": paragraphLowerBound,
        "paragraphUpperBound": paragraphUpperBound,
        "sentenceLowerBound": sentenceLowerBound,
        "sentenceUpperBound": sentenceUpperBound,
        "format": format
    }
    
    return call_api("1777316659720195", "generate_lorem_ipsum", arguments)

def regex_test(
    text: str,
    pattern: str,
    flags: Optional[str] = "g"
) -> Dict[str, Any]:
    """
    Test a regex pattern against text
    
    Args:
        text: The text to test against the pattern
        pattern: The regex pattern to test
        flags: Regex flags (e.g., 'g', 'i', 'gi')
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "pattern": pattern,
        "flags": flags
    }
    
    return call_api("1777316659720195", "regex_test", arguments)

def regex_replace(
    text: str,
    pattern: str,
    replacement: str,
    flags: Optional[str] = "g"
) -> Dict[str, Any]:
    """
    Replace text using a regex pattern
    
    Args:
        text: The text to perform replacements on
        pattern: The regex pattern to match
        replacement: The replacement string
        flags: Regex flags (e.g., 'g', 'i', 'gi')
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "pattern": pattern,
        "replacement": replacement,
        "flags": flags
    }
    
    return call_api("1777316659720195", "regex_replace", arguments)

def regex_extract(
    text: str,
    pattern: str,
    flags: Optional[str] = "g"
) -> Dict[str, Any]:
    """
    Extract matches using a regex pattern
    
    Args:
        text: The text to extract from
        pattern: The regex pattern with capture groups
        flags: Regex flags (e.g., 'g', 'i', 'gi')
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "pattern": pattern,
        "flags": flags
    }
    
    return call_api("1777316659720195", "regex_extract", arguments)

def regex_split(
    text: str,
    pattern: str,
    flags: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Split text using a regex pattern
    
    Args:
        text: The text to split
        pattern: The regex pattern to split by
        flags: Regex flags (e.g., 'i')
    
    Returns:
        
    """
    arguments = {
        "text": text,
        "pattern": pattern,
        "flags": flags
    }
    
    return call_api("1777316659720195", "regex_split", arguments)

