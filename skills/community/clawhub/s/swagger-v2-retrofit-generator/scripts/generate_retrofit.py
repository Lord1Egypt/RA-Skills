#!/usr/bin/env python3
"""
Generate Retrofit (Kotlin) client code from Swagger v2 API documentation.
Supports filtering by path, HTTP method, tags, and summary search.
"""

import argparse
import json
import sys
import re
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class Property:
    name: str
    type_name: str
    nullable: bool = True
    description: Optional[str] = None


@dataclass
class ModelClass:
    name: str
    properties: List[Property]
    description: Optional[str] = None


@dataclass
class Endpoint:
    path: str
    method: str
    operation_id: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    tags: List[str]
    parameters: List[Dict[str, Any]]
    responses: Dict[str, Any]
    consumes: Optional[List[str]]
    produces: Optional[List[str]]
    
    @property
    def full_path(self) -> str:
        """Return method + path format like 'POST /users'."""
        return f"{self.method.upper()} {self.path}"
    
    def matches_search(self, query: str, search_fields: Optional[List[str]] = None) -> bool:
        """
        Check if endpoint matches search query across specified fields.
        
        Args:
            query: Search string (case-insensitive)
            search_fields: List of fields to search ['path', 'summary', 'description', 
                        'operationId', 'tags']. Default: all fields.
        """
        if not query:
            return True
        
        query_lower = query.lower()
        fields = search_fields or ['path', 'summary', 'description', 'operationId', 'tags']
        
        for field in fields:
            if field == 'path' and query_lower in self.path.lower():
                return True
            if field == 'summary' and self.summary and query_lower in self.summary.lower():
                return True
            if field == 'description' and self.description and query_lower in self.description.lower():
                return True
            if field == 'operationId' and self.operation_id and query_lower in self.operation_id.lower():
                return True
            if field == 'tags':
                for tag in self.tags:
                    if query_lower in tag.lower():
                        return True
        
        return False


class SwaggerParser:
    """Parse Swagger v2 specification."""
    
    SWAGGER_TYPES_TO_KOTLIN = {
        'string': 'String',
        'integer': 'Int',
        'number': 'Double',
        'boolean': 'Boolean',
        'array': 'List',
        'object': 'Any',
        'file': 'MultipartBody.Part',
    }
    
    # 常见中文词汇到英文的映射（用于类名转换）
    # 按长度降序排列，确保长词先被替换
    CHINESE_TO_ENGLISH = {
        # 复合词汇（优先匹配）
        '详情信息对象': 'DetailInfoObject',
        '详情信息': 'DetailInfo',
        '商品列表': 'GoodsList',
        '用户列表': 'UserList',
        '绘本详情': 'PictureBookDetail',
        # 基础词汇
        '口语课': 'OralClass',
        '绘本': 'PictureBook',
        '结果': 'Result',
        '数据': 'Data',
        '信息': 'Info',
        '对象': 'Object',
        '列表': 'List',
        '详情': 'Detail',
        '商品': 'Goods',
        '用户': 'User',
        '订单': 'Order',
        '首页': 'Home',
        '请求': 'Request',
        '响应': 'Response',
        '参数': 'Param',
        '配置': 'Config',
        '记录': 'Record',
        '翻译': 'Translation',
        '单词': 'Word',
    }
    
    def __init__(self, swagger_data: dict):
        self.data = swagger_data
        self.base_path = swagger_data.get('basePath', '')
        self.host = swagger_data.get('host', '')
        self.definitions = swagger_data.get('definitions', {})
        self.tags = {tag.get('name', ''): tag for tag in swagger_data.get('tags', [])}
        # 建立原始类名到清理后类名的映射
        self._class_name_map: Dict[str, str] = {}
        self._build_class_name_map()
        
    def _build_class_name_map(self):
        """Build mapping from original class names to sanitized class names."""
        for name in self.definitions.keys():
            self._class_name_map[name] = self.sanitize_class_name(name)
    
    def sanitize_class_name(self, name: str) -> str:
        """
        Convert any string to a valid Kotlin class name.
        """
        if not name:
            return 'UnknownClass'
        
        # Step 1: Remove special characters like « » 《 》 < >
        name = re.sub(r'[«»《》<>]', '', name)
        
        # Step 2: Try to translate common Chinese terms to English
        # Sort by length descending to match longer phrases first
        sorted_items = sorted(self.CHINESE_TO_ENGLISH.items(), key=lambda x: len(x[0]), reverse=True)
        for cn, en in sorted_items:
            name = name.replace(cn, en)
        
        # Step 3: Replace remaining Chinese characters with 'X' (placeholder)
        name = re.sub(r'[\u4e00-\u9fff]', 'X', name)
        
        # Step 4: Replace special characters with underscores
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        
        # Step 5: Remove consecutive underscores
        name = re.sub(r'_+', '_', name)
        
        # Step 6: Split by underscore and capitalize each part (PascalCase)
        parts = name.split('_')
        pascal_parts = []
        for part in parts:
            if part:
                # If part is already camelCase (contains uppercase letters after first char),
                # only capitalize the first letter
                if any(c.isupper() for c in part[1:]):
                    pascal_parts.append(part[0].upper() + part[1:])
                else:
                    pascal_parts.append(part[0].upper() + part[1:].lower())
        
        result = ''.join(pascal_parts)
        
        # Step 7: Ensure it starts with a letter
        if result and not result[0].isalpha():
            result = 'Class' + result
        
        return result or 'UnknownClass'
    
    def get_sanitized_class_name(self, original_name: str) -> str:
        """Get sanitized class name from original name."""
        return self._class_name_map.get(original_name, self.sanitize_class_name(original_name))
        
    def get_type(self, schema: dict, fallback_name: str = 'Any') -> str:
        """Convert Swagger type to Kotlin type."""
        if not schema:
            return 'Any'
        
        # Handle $ref - use sanitized class name
        if '$ref' in schema:
            ref = schema['$ref']
            original_name = ref.split('/')[-1]
            return self.get_sanitized_class_name(original_name)
        
        swagger_type = schema.get('type', 'object')
        format_type = schema.get('format', '')
        
        # Special handling for date/datetime
        if format_type in ['date', 'date-time']:
            return 'String'
        
        # Special handling for integer formats
        if swagger_type == 'integer' and format_type == 'int64':
            return 'Long'
        
        if swagger_type == 'array':
            items = schema.get('items', {})
            item_type = self.get_type(items, 'Any')
            return f'List<{item_type}>'
        
        return self.SWAGGER_TYPES_TO_KOTLIN.get(swagger_type, 'Any')
    
    def parse_model(self, name: str, definition: dict) -> ModelClass:
        """Parse a Swagger definition into a ModelClass."""
        properties = []
        required_props = set(definition.get('required', []))
        
        # Use sanitized class name
        sanitized_name = self.get_sanitized_class_name(name)
        
        props = definition.get('properties', {})
        for prop_name, prop_schema in props.items():
            is_required = prop_name in required_props
            prop_type = self.get_type(prop_schema, 'Any')
            
            # Add nullable marker if optional
            type_name = f'{prop_type}?' if not is_required else prop_type
            
            properties.append(Property(
                name=prop_name,
                type_name=type_name,
                nullable=not is_required,
                description=prop_schema.get('description')
            ))
        
        return ModelClass(
            name=sanitized_name,
            properties=properties,
            description=definition.get('description')
        )
    
    def parse_all_models(self) -> List[ModelClass]:
        """Parse all model definitions."""
        models = []
        for name, definition in self.definitions.items():
            if definition.get('type') == 'object' or 'properties' in definition:
                models.append(self.parse_model(name, definition))
        return models
    
    def parse_endpoints(self, 
                        path_filters: Optional[List[str]] = None, 
                        method_filter: Optional[str] = None,
                        search_query: Optional[str] = None,
                        search_fields: Optional[List[str]] = None,
                        tag_filter: Optional[List[str]] = None) -> List[Endpoint]:
        """
        Parse API endpoints from paths with optional filters.
        
        Args:
            path_filters: List of path patterns to include (e.g., ['/users', '/picture/*'])
                         Supports wildcards: * matches any characters
            method_filter: HTTP method to filter by (e.g., 'POST', 'GET')
            search_query: Search string to match against summary, path, description, etc.
            search_fields: Fields to search in ['path', 'summary', 'description', 'operationId', 'tags']
            tag_filter: List of tags to filter by (e.g., ['用户相关API', '绘本接口'])
        """
        endpoints = []
        paths = self.data.get('paths', {})
        
        for path, path_item in paths.items():
            # Check path filter first
            if path_filters and not self._matches_path_filter(path, path_filters):
                continue
            
            for method in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
                if method in path_item:
                    # Check method filter
                    if method_filter and method.upper() != method_filter.upper():
                        continue
                    
                    operation = path_item[method]
                    
                    # Extract tags
                    tags = operation.get('tags', [])
                    
                    # Check tag filter
                    if tag_filter:
                        if not any(t in tags for t in tag_filter):
                            continue
                    
                    endpoint = Endpoint(
                        path=path,
                        method=method.upper(),
                        operation_id=operation.get('operationId'),
                        summary=operation.get('summary'),
                        description=operation.get('description'),
                        tags=tags,
                        parameters=operation.get('parameters', []),
                        responses=operation.get('responses', {}),
                        consumes=operation.get('consumes'),
                        produces=operation.get('produces')
                    )
                    
                    # Check search query
                    if search_query and not endpoint.matches_search(search_query, search_fields):
                        continue
                    
                    endpoints.append(endpoint)
        
        return endpoints
    
    def _matches_path_filter(self, path: str, filters: List[str]) -> bool:
        """Check if path matches any of the filter patterns."""
        for pattern in filters:
            # Convert wildcard pattern to regex
            regex_pattern = ''
            for char in pattern:
                if char == '*':
                    regex_pattern += '.*'
                elif char in '.+?^${}()|[]\\':
                    regex_pattern += '\\' + char
                else:
                    regex_pattern += char
            
            # Add anchors for exact matching
            regex_pattern = f'^{regex_pattern}$'
            
            if re.match(regex_pattern, path, re.IGNORECASE):
                return True
        
        return False
    
    def get_referenced_models(self, endpoints: List[Endpoint]) -> Set[str]:
        """
        Get all model names referenced by the given endpoints.
        This helps generate only necessary data classes.
        """
        referenced = set()
        
        for endpoint in endpoints:
            # Check parameters for body schema references
            for param in endpoint.parameters:
                if param.get('in') == 'body' and 'schema' in param:
                    self._collect_schema_refs(param['schema'], referenced)
            
            # Check responses for schema references
            for response in endpoint.responses.values():
                if 'schema' in response:
                    self._collect_schema_refs(response['schema'], referenced)
        
        return referenced
    
    def _collect_schema_refs(self, schema: dict, refs: Set[str]):
        """Recursively collect $ref references from a schema."""
        if not schema:
            return
        
        if '$ref' in schema:
            ref_name = schema['$ref'].split('/')[-1]
            # Use sanitized class name
            sanitized_name = self.get_sanitized_class_name(ref_name)
            if sanitized_name not in refs:
                refs.add(sanitized_name)
                # Also check if this model references other models
                if ref_name in self.definitions:
                    self._collect_schema_refs(self.definitions[ref_name], refs)
        
        # Check nested schemas
        if 'items' in schema:
            self._collect_schema_refs(schema['items'], refs)
        
        if 'properties' in schema:
            for prop_schema in schema['properties'].values():
                self._collect_schema_refs(prop_schema, refs)
    
    def get_all_tags(self) -> List[Tuple[str, Optional[str]]]:
        """Get all tags with descriptions."""
        tags = []
        for tag_name, tag_info in self.tags.items():
            desc = tag_info.get('description', '') if isinstance(tag_info, dict) else ''
            tags.append((tag_name, desc))
        return sorted(tags)


class RetrofitGenerator:
    """Generate Retrofit/Kotlin code."""
    
    HTTP_METHOD_ANNOTATIONS = {
        'GET': '@GET',
        'POST': '@POST',
        'PUT': '@PUT',
        'DELETE': '@DELETE',
        'PATCH': '@PATCH',
        'HEAD': '@HEAD',
        'OPTIONS': '@OPTIONS',
    }
    
    # 常见中文词汇到英文的映射（用于类名转换）
    # 常见中文词汇到英文的映射（用于类名转换）
    # 按长度降序排列，确保长词先被替换
    CHINESE_TO_ENGLISH = {
        # 复合词汇（优先匹配）
        '详情信息对象': 'DetailInfoObject',
        '详情信息': 'DetailInfo',
        '商品列表': 'GoodsList',
        '用户列表': 'UserList',
        '绘本详情': 'PictureBookDetail',
        # 基础词汇
        '口语课': 'OralClass',
        '绘本': 'PictureBook',
        '结果': 'Result',
        '数据': 'Data',
        '信息': 'Info',
        '对象': 'Object',
        '列表': 'List',
        '详情': 'Detail',
        '商品': 'Goods',
        '用户': 'User',
        '订单': 'Order',
        '首页': 'Home',
        '请求': 'Request',
        '响应': 'Response',
        '参数': 'Param',
        '配置': 'Config',
        '记录': 'Record',
        '翻译': 'Translation',
        '单词': 'Word',
    }
    
    def __init__(self, package_name: str = 'com.example.api'):
        self.package_name = package_name
        
    def sanitize_class_name(self, name: str) -> str:
        """
        Convert any string to a valid Kotlin class name.
        
        Rules:
        - Must start with a letter or underscore
        - Can contain letters, digits, and underscores
        - Should be in PascalCase
        - Chinese characters will be translated or replaced
        """
        if not name:
            return 'UnknownClass'
        
        # Step 1: Remove special characters like « » 《 》 < >
        name = re.sub(r'[«»《》<>]', '', name)
        
        # Step 2: Try to translate common Chinese terms to English
        # Sort by length descending to match longer phrases first
        sorted_items = sorted(self.CHINESE_TO_ENGLISH.items(), key=lambda x: len(x[0]), reverse=True)
        for cn, en in sorted_items:
            name = name.replace(cn, en)
        
        # Step 3: Replace remaining Chinese characters with 'X' (placeholder)
        # This is a fallback - ideally all Chinese should be translated
        name = re.sub(r'[\u4e00-\u9fff]', 'X', name)
        
        # Step 4: Replace special characters with underscores
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        
        # Step 5: Remove consecutive underscores
        name = re.sub(r'_+', '_', name)
        
        # Step 6: Split by underscore and capitalize each part (PascalCase)
        parts = name.split('_')
        pascal_parts = []
        for part in parts:
            if part:
                # If part is already camelCase (contains uppercase letters after first char),
                # only capitalize the first letter
                if any(c.isupper() for c in part[1:]):
                    pascal_parts.append(part[0].upper() + part[1:])
                else:
                    pascal_parts.append(part[0].upper() + part[1:].lower())
        
        result = ''.join(pascal_parts)
        
        # Step 7: Ensure it starts with a letter
        if result and not result[0].isalpha():
            result = 'Class' + result
        
        # Step 8: Handle empty result
        if not result:
            return 'UnknownClass'
        
        return result
        
    def sanitize_method_name(self, name: str) -> str:
        """Convert operationId or path to valid Kotlin method name."""
        if not name:
            return 'unknownMethod'
        
        # Replace special characters
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        
        # Ensure starts with lowercase
        if name[0].isupper():
            name = name[0].lower() + name[1:]
        
        # Remove consecutive underscores
        name = re.sub(r'_+', '_', name)
        
        # Remove trailing underscore
        name = name.rstrip('_')
        
        return name or 'unknownMethod'
    
    def generate_model_class(self, model: ModelClass) -> str:
        """Generate Kotlin data class for a model."""
        lines = []
        
        # Doc comment
        if model.description:
            lines.append(f'/**')
            lines.append(f' * {model.description}')
            lines.append(f' */')
        
        lines.append(f'data class {model.name}(')
        
        # Properties
        props = []
        for prop in model.properties:
            doc = f' // {prop.description}' if prop.description else ''
            props.append(f'    val {prop.name}: {prop.type_name}{doc}')
        
        lines.append(',\n'.join(props))
        lines.append(')')
        
        return '\n'.join(lines)
    
    def generate_service_method(self, endpoint: Endpoint, parser: SwaggerParser) -> str:
        """Generate Retrofit service method for an endpoint."""
        lines = []
        
        # Doc comment
        doc_parts = []
        if endpoint.summary:
            doc_parts.append(endpoint.summary)
        if endpoint.description and endpoint.description != endpoint.summary:
            doc_parts.append(endpoint.description)
        if endpoint.tags:
            doc_parts.append(f"Tags: {', '.join(endpoint.tags)}")
        
        if doc_parts:
            lines.append(f'    /**')
            for part in doc_parts:
                lines.append(f'     * {part}')
            lines.append(f'     */')
        
        # HTTP method annotation
        annotation = self.HTTP_METHOD_ANNOTATIONS.get(endpoint.method, '@GET')
        lines.append(f'    {annotation}("{endpoint.path}")')
        
        # Method signature
        method_name = self.sanitize_method_name(
            endpoint.operation_id or f'{endpoint.method.lower()}_{endpoint.path}'
        )
        
        # Build parameters
        params = []
        body_param = None
        
        for param in endpoint.parameters:
            param_name = param.get('name', '')
            param_in = param.get('in', '')
            required = param.get('required', False)
            
            if param_in == 'path':
                params.append(f'@Path("{param_name}") {param_name}: {parser.get_type(param)}')
            elif param_in == 'query':
                param_type = parser.get_type(param)
                if not required:
                    param_type = f'{param_type}? = null'
                params.append(f'@Query("{param_name}") {param_name}: {param_type}')
            elif param_in == 'header':
                param_type = parser.get_type(param)
                if not required:
                    param_type = f'{param_type}? = null'
                params.append(f'@Header("{param_name}") {param_name}: {param_type}')
            elif param_in == 'body':
                body_param = param
        
        # Determine return type from 200 response
        return_type = 'ResponseBody'  # Default
        if '200' in endpoint.responses:
            response = endpoint.responses['200']
            if 'schema' in response:
                return_type = parser.get_type(response['schema'])
        
        # Add body parameter last
        if body_param:
            body_type = parser.get_type(body_param.get('schema', {}))
            params.append(f'@Body body: {body_type}')
        
        # Build full method signature
        if params:
            lines.append(f'    suspend fun {method_name}(')
            lines.append('        ' + ',\n        '.join(params))
            lines.append(f'    ): {return_type}')
        else:
            lines.append(f'    suspend fun {method_name}(): {return_type}')
        
        return '\n'.join(lines)
    
    def generate_service_interface(self, name: str, endpoints: List[Endpoint], parser: SwaggerParser) -> str:
        """Generate Retrofit service interface."""
        lines = []
        
        lines.append(f'interface {name} {{')
        lines.append('')
        
        for i, endpoint in enumerate(endpoints):
            method_code = self.generate_service_method(endpoint, parser)
            lines.append(method_code)
            if i < len(endpoints) - 1:
                lines.append('')
        
        lines.append('}')
        
        return '\n'.join(lines)
    
    def generate_full_code(self, parser: SwaggerParser, 
                           service_name: str = 'ApiService',
                           endpoints: Optional[List[Endpoint]] = None,
                           include_all_models: bool = True) -> str:
        """
        Generate complete Kotlin file with imports, models and service.
        
        Args:
            parser: SwaggerParser instance
            service_name: Name for the service interface
            endpoints: Specific endpoints to generate (if None, all endpoints)
            include_all_models: If False, only generate models referenced by endpoints
        """
        lines = []
        
        # Package and imports
        lines.append(f'package {self.package_name}')
        lines.append('')
        lines.append('import retrofit2.http.*')
        lines.append('import okhttp3.ResponseBody')
        lines.append('')
        
        # Get endpoints
        if endpoints is None:
            endpoints = parser.parse_endpoints()
        
        # Models
        if include_all_models:
            # Generate all models
            models = parser.parse_all_models()
        else:
            # Generate only referenced models
            referenced_names = parser.get_referenced_models(endpoints)
            models = []
            for sanitized_name in referenced_names:
                # Find original name by looking up in the reverse mapping
                original_name = None
                for orig, sanitized in parser._class_name_map.items():
                    if sanitized == sanitized_name:
                        original_name = orig
                        break
                if original_name and original_name in parser.definitions:
                    models.append(parser.parse_model(original_name, parser.definitions[original_name]))
        
        for model in models:
            lines.append(self.generate_model_class(model))
            lines.append('')
        
        # Service interface
        lines.append(self.generate_service_interface(service_name, endpoints, parser))
        
        return '\n'.join(lines)


def list_endpoints(swagger_data: dict, 
                   search_query: Optional[str] = None,
                   search_fields: Optional[List[str]] = None,
                   tag_filter: Optional[List[str]] = None) -> List[Tuple[str, str, Optional[str], List[str]]]:
    """List all available endpoints for user selection."""
    endpoints = []
    paths = swagger_data.get('paths', {})
    
    for path, path_item in paths.items():
        for method in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
            if method in path_item:
                operation = path_item[method]
                tags = operation.get('tags', [])
                summary = operation.get('summary', operation.get('operationId', ''))
                
                # Check tag filter
                if tag_filter and not any(t in tags for t in tag_filter):
                    continue
                
                # Check search query
                if search_query:
                    query_lower = search_query.lower()
                    fields = search_fields or ['path', 'summary', 'description', 'operationId', 'tags']
                    
                    match = False
                    for field in fields:
                        if field == 'path' and query_lower in path.lower():
                            match = True
                            break
                        if field == 'summary' and summary and query_lower in summary.lower():
                            match = True
                            break
                        if field == 'description':
                            desc = operation.get('description', '')
                            if desc and query_lower in desc.lower():
                                match = True
                                break
                        if field == 'operationId':
                            op_id = operation.get('operationId', '')
                            if op_id and query_lower in op_id.lower():
                                match = True
                                break
                        if field == 'tags':
                            for tag in tags:
                                if query_lower in tag.lower():
                                    match = True
                                    break
                    
                    if not match:
                        continue
                
                endpoints.append((
                    method.upper(),
                    path,
                    summary,
                    tags
                ))
    
    return sorted(endpoints, key=lambda x: x[1])


def list_tags(parser: SwaggerParser) -> None:
    """List all available tags."""
    tags = parser.get_all_tags()
    print(f"Found {len(tags)} tags:\n")
    for name, desc in tags:
        desc_str = f" - {desc}" if desc else ""
        print(f"  - {name}{desc_str}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate Retrofit/Kotlin code from Swagger v2 API docs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate all APIs
  python generate_retrofit.py swagger.json
  
  # Generate specific endpoint: POST /picture/getPictureDetailPage
  python generate_retrofit.py swagger.json --path /picture/getPictureDetailPage --method POST
  
  # Generate all APIs under /picture/
  python generate_retrofit.py swagger.json --path "/picture/*"
  
  # Search and generate (search in path, summary, description, operationId, tags)
  python generate_retrofit.py swagger.json --search "绘本详情"
  python generate_retrofit.py swagger.json --search "getPicture" --search-field path
  
  # Generate by tag
  python generate_retrofit.py swagger.json --tag "绘本接口" --tag "用户相关API"
  
  # List available endpoints with search
  python generate_retrofit.py swagger.json --list
  python generate_retrofit.py swagger.json --list --search "绘本"
  python generate_retrofit.py swagger.json --list --search "getPicture" --search-field path
  python generate_retrofit.py swagger.json --list --tag "绘本接口"
  
  # List all tags
  python generate_retrofit.py swagger.json --list-tags
        '''
    )
    parser.add_argument(
        'input',
        help='Input Swagger JSON file path, or "-" for stdin'
    )
    parser.add_argument(
        '-p', '--package',
        default='com.example.api',
        help='Package name for generated code (default: com.example.api)'
    )
    parser.add_argument(
        '-s', '--service-name',
        default='ApiService',
        help='Service interface name (default: ApiService)'
    )
    parser.add_argument(
        '--path',
        action='append',
        dest='paths',
        help='''Filter by API path. Can be specified multiple times.
                Supports wildcards (*).
                Examples: /users, /picture/*, /api/v1/*/detail'''
    )
    parser.add_argument(
        '-m', '--method',
        help='Filter by HTTP method (GET, POST, PUT, DELETE, PATCH)'
    )
    # Search options
    parser.add_argument(
        '--search',
        help='''Search query to filter endpoints. Searches in path, summary, 
                description, operationId, and tags by default.'''
    )
    parser.add_argument(
        '--search-field',
        action='append',
        dest='search_fields',
        choices=['path', 'summary', 'description', 'operationId', 'tags'],
        help='''Fields to search in. Can be specified multiple times.
                Default: all fields.'''
    )
    # Tag filter
    parser.add_argument(
        '--tag',
        action='append',
        dest='tags',
        help='''Filter by tag. Can be specified multiple times.
                Example: --tag "绘本接口" --tag "用户相关API"'''
    )
    parser.add_argument(
        '--only-used-models',
        action='store_true',
        help='Only generate data classes referenced by the selected endpoints'
    )
    # List options
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List all available endpoints and exit'
    )
    parser.add_argument(
        '--list-tags',
        action='store_true',
        help='List all available tags and exit'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)'
    )
    
    args = parser.parse_args()
    
    # Read input
    if args.input == '-':
        swagger_data = json.load(sys.stdin)
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            swagger_data = json.load(f)
    
    swagger_parser = SwaggerParser(swagger_data)
    
    # List tags mode
    if args.list_tags:
        list_tags(swagger_parser)
        return
    
    # List mode
    if args.list:
        endpoints = list_endpoints(
            swagger_data, 
            search_query=args.search,
            search_fields=args.search_fields,
            tag_filter=args.tags
        )
        print(f"Found {len(endpoints)} endpoints:\n")
        for method, path, summary, tags in endpoints:
            summary_str = f" - {summary}" if summary else ""
            tags_str = f" [{', '.join(tags)}]" if tags else ""
            print(f"  {method:6} {path}{summary_str}{tags_str}")
        return
    
    # Parse and generate
    endpoints = swagger_parser.parse_endpoints(
        path_filters=args.paths,
        method_filter=args.method,
        search_query=args.search,
        search_fields=args.search_fields,
        tag_filter=args.tags
    )
    
    if not endpoints:
        print("No endpoints match the specified filters.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Generating code for {len(endpoints)} endpoint(s)...", file=sys.stderr)
    for ep in endpoints:
        tags_str = f" [{', '.join(ep.tags)}]" if ep.tags else ""
        print(f"  - {ep.full_path}{tags_str}", file=sys.stderr)
    
    generator = RetrofitGenerator(package_name=args.package)
    code = generator.generate_full_code(
        swagger_parser,
        service_name=args.service_name,
        endpoints=endpoints,
        include_all_models=not args.only_used_models
    )
    
    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f'\nCode generated: {args.output}', file=sys.stderr)
    else:
        print(code)


if __name__ == '__main__':
    main()
