# Volcengine Skills Update Log

## Update Date: 2026-04-15

### Summary
Updated volcengine skills based on official API Reference PDF extraction and validation.

## Files Updated

### 1. configuration.md

#### Added: Security Considerations Section
- **API Quotas and Limits**
  - Each main account supports up to 50 API Keys
  - API Keys can be restricted to specific Model IDs or IP addresses
  - Project space isolation: Keys only work within their project
  - Rate limiting best practices

#### Added: Error Handling Section
- Complete error code reference table
- 400 Bad Request errors (sensitive content, missing parameters)
- 429 Too Many Requests errors (RPM, TPM, IPM limits)
- 401/403 Authentication errors
- Best practices for error handling

#### Updated: Troubleshooting Section
- Added "Cross-project access denied" issue and solution

### 2. SKILL.md

#### Updated: Best Practices Section
- Enhanced API Key Security with quota limits and permission control
- Added project isolation information
- Improved error handling guidance with specific HTTP status codes
- Added Authentication Methods section (API Key vs Access Key)

#### Added: API Architecture Section
- Data Plane API description and Base URL
- Control Plane API description and Base URL
- API version information (2024-01-01)

#### Updated: Resources Section
- Added documentation update timestamp

### 3. models.md

#### Added: Token Usage Details
- Detailed token usage response format
- Explanation of prompt_tokens, completion_tokens, reasoning_tokens
- Reasoning tokens tracking for reasoning models

#### Added: Streaming Responses
- Streaming configuration example
- Response format description

## Key Information Added from PDF

### Authentication
- **API Key Authentication**: Bearer token in Authorization header
- **Access Key Authentication**: HMAC-SHA256 signature-based (enterprise use)
- **Base URLs**:
  - Data Plane: `https://ark.cn-beijing.volces.com/api/v3`
  - Control Plane: `https://ark.cn-beijing.volcengineapi.com/`

### Quotas and Limits
- 50 API Keys per main account
- Permission control (Model ID, IP address restrictions)
- Project space isolation (no cross-project access)

### Error Codes
- Sensitive content detection errors (400 series)
- Rate limit errors (429 series): RPM, TPM, IPM
- Quota exceeded errors (429 series)
- Authentication errors (401/403 series)

### Token Usage
- Reasoning tokens tracking for reasoning models
- Streaming response support

## Validation Status

### ✅ Verified Against Official PDF
- API Key format and configuration
- Base URL structure
- Authentication methods
- Error code categories
- Quota limits

### ⚠️ Pending Further Verification
- Complete Base URL for all regions
- Detailed parameter documentation
- SDK-specific implementation details

## Next Steps

1. **Extract more pages** for complete API documentation
2. **Verify region-specific Base URLs** (Shanghai, Guangzhou)
3. **Add SDK integration guides** for Python, Java, Go
4. **Create troubleshooting flowcharts** based on error codes

## Impact

### User Benefits
- More accurate configuration guidance
- Better error handling and debugging
- Clearer security best practices
- Official quota and limit information

### Skill Improvements
- Enhanced documentation completeness
- Better alignment with official API documentation
- Improved troubleshooting capabilities

---
*Updated by: OpenClaw AI Assistant*
*Source: Volcano Engine API Reference PDF*
*Extracted pages: 28 (high-priority sections)*