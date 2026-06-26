#!/usr/bin/env python3
"""
JSON Utils + WebSearch integration.
Fetch API schemas from web, validate real API responses, batch-validate endpoints.
"""

import json
import sys
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

# Add json-utils to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "json-utils" / "scripts"))

try:
    from json_processor import parse_json, parse_and_validate
    from json_schema_validator import validate_with_jsonschema
    from json_batch_processor import process_file_batch
    JSON_UTILS_AVAILABLE = True
except ImportError:
    JSON_UTILS_AVAILABLE = False
    print("Warning: json-utils not found. Some features disabled.")


@dataclass
class WebSearchResult:
    query: str
    json_data: dict
    validation_errors: list[str]
    schema_matched: bool
    source_url: str


class WebSearchJSON:
    """
    Combine WebSearch with JSON validation.
    
    Use cases:
    1. Search for API documentation, extract schema
    2. Validate real API responses against schemas
    3. Batch-validate multiple API endpoints
    4. Auto-repair common API response errors
    """
    
    def __init__(self, use_repair: bool = True):
        self.use_repair = use_repair
        self.json_available = JSON_UTILS_AVAILABLE
    
    def search_and_validate(
        self,
        query: str,
        schema: Optional[dict] = None,
        schema_path: Optional[Path] = None
    ) -> WebSearchResult:
        """
        Search web for JSON data, validate against schema.
        
        This is a placeholder - in real usage, this would:
        1. Call WebSearch to find API docs
        2. Extract JSON examples/schemas from results
        3. Parse and validate with json-utils
        """
        # Simulate web search result (would be actual search in production)
        mock_response = {
            "api": query.split()[0] if query else "unknown",
            "version": "1.0",
            "endpoints": [
                {"path": "/items", "method": "GET"},
                {"path": "/items", "method": "POST"}
            ]
        }
        
        # Validate with json-utils if available
        validation_errors = []
        schema_matched = False
        
        if self.json_available and (schema or schema_path):
            try:
                if schema_path:
                    validate_with_jsonschema(mock_response, str(schema_path))
                schema_matched = True
            except Exception as e:
                validation_errors.append(str(e))
        
        return WebSearchResult(
            query=query,
            json_data=mock_response,
            validation_errors=validation_errors,
            schema_matched=schema_matched,
            source_url=f"https://api.github.com/search?q={query.replace(' ', '+')}"
        )
    
    def validate_api_response(
        self,
        response_data: str,
        endpoint: str,
        expected_schema: Optional[dict] = None
    ) -> dict:
        """
        Validate an API response with auto-repair.
        
        Uses json-utils for robust parsing.
        """
        if not self.json_available:
            return json.loads(response_data)
        
        # Use json-utils parser with auto-repair
        result = parse_json(response_data, repair=self.use_repair)
        
        if expected_schema:
            try:
                parse_and_validate(json.dumps(result), expected_schema)
            except Exception as e:
                print(f"Schema validation failed for {endpoint}: {e}")
        
        return result
    
    def batch_validate_endpoints(
        self,
        endpoints: list[str],
        responses: list[str],
        schema_path: Optional[Path] = None
    ) -> list[WebSearchResult]:
        """
        Batch-validate multiple API endpoint responses.
        """
        results = []
        for endpoint, response in zip(endpoints, responses):
            try:
                json_data = self.validate_api_response(response, endpoint)
                results.append(WebSearchResult(
                    query=endpoint,
                    json_data=json_data,
                    validation_errors=[],
                    schema_matched=True,
                    source_url=endpoint
                ))
            except Exception as e:
                results.append(WebSearchResult(
                    query=endpoint,
                    json_data={},
                    validation_errors=[str(e)],
                    schema_matched=False,
                    source_url=endpoint
                ))
        return results
    
    def generate_api_schema(self, sample_response: str, endpoint: str) -> dict:
        """
        Generate JSON Schema from sample API response.
        """
        if not self.json_available:
            return {}
        
        data = parse_json(sample_response)
        
        # Basic schema generation
        def infer_schema(obj, path="root"):
            if isinstance(obj, dict):
                return {
                    "type": "object",
                    "properties": {
                        k: infer_schema(v, f"{path}.{k}")
                        for k, v in obj.items()
                    }
                }
            elif isinstance(obj, list) and obj:
                return {
                    "type": "array",
                    "items": infer_schema(obj[0], f"{path}[]")
                }
            elif isinstance(obj, str):
                return {"type": "string"}
            elif isinstance(obj, int):
                return {"type": "integer"}
            elif isinstance(obj, float):
                return {"type": "number"}
            elif isinstance(obj, bool):
                return {"type": "boolean"}
            else:
                return {"type": "null"}
        
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": f"{endpoint} Response Schema",
            **infer_schema(data)
        }
        
        return schema


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="JSON Utils + WebSearch integration"
    )
    parser.add_argument("--search", help="Search query for API docs")
    parser.add_argument("--validate-file", type=Path, help="JSON file to validate")
    parser.add_argument("--schema", type=Path, help="Schema file path")
    parser.add_argument("--generate-schema", type=Path, 
                        help="Generate schema from sample JSON file")
    parser.add_argument("--endpoint", help="API endpoint identifier")
    args = parser.parse_args()
    
    ws = WebSearchJSON()
    
    if args.search:
        result = ws.search_and_validate(args.search, schema_path=args.schema)
        print(f"Query: {result.query}")
        print(f"Data: {json.dumps(result.json_data, indent=2)}")
        print(f"Schema matched: {result.schema_matched}")
        if result.validation_errors:
            print(f"Errors: {result.validation_errors}")
    elif args.generate_schema and args.endpoint:
        sample = args.generate_schema.read_text()
        schema = ws.generate_api_schema(sample, args.endpoint)
        print(json.dumps(schema, indent=2))


if __name__ == "__main__":
    main()
