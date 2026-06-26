# Python MCP Server Implementation Guide

## Overview

This document provides Python-specific best practices and examples for implementing MCP servers using FastMCP.

---

## Quick Reference

### Key Imports
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
```

### Server Initialization
```python
mcp = FastMCP("service_mcp")
```

### Tool Registration Pattern
```python
@mcp.tool(name="tool_name", annotations={...})
async def tool_function(params: InputModel) -> str:
    # Implementation
    pass
```

---

## Server Naming Convention

Python MCP servers: `{service}_mcp` (lowercase with underscores)
- Examples: `github_mcp`, `jira_mcp`, `stripe_mcp`

---

## Pydantic Models for Input Validation

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict

class UserSearchInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    query: str = Field(..., description="Search string", min_length=2, max_length=200)
    limit: Optional[int] = Field(default=20, ge=1, le=100)
    offset: Optional[int] = Field(default=0, ge=0)

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()
```

---

## Response Format Options

```python
from enum import Enum

class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"

class SearchInput(BaseModel):
    query: str = Field(..., description="Search query")
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )
```

---

## Complete Example

```python
#!/usr/bin/env python3
from typing import Optional
from enum import Enum
import httpx
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("example_mcp")

class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"

class UserSearchInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    query: str = Field(..., min_length=2, max_length=200)
    limit: Optional[int] = Field(default=20, ge=1, le=100)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN)

@mcp.tool(
    name="example_search_users",
    annotations={
        "title": "Search Users",
        "readOnlyHint": True,
        "destructiveHint": False
    }
)
async def example_search_users(params: UserSearchInput) -> str:
    '''Search for users in the system.'''
    # Implementation here
    pass

if __name__ == "__main__":
    mcp.run()
```

---

## Quality Checklist

- [ ] All tools have descriptive names and documentation
- [ ] All tools use Pydantic BaseModel for input validation
- [ ] All Fields have explicit types and descriptions
- [ ] All async functions properly defined
- [ ] Error handling implemented for all external calls
- [ ] Server name follows format: `{service}_mcp`
