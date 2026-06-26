# Security Policy

## API Key Management

This skill requires API keys to access TradingView data through RapidAPI. Please follow these security best practices:

### ⚠️ Critical Security Rules

1. **Never commit API keys to version control**
   - Do not include real API keys in configuration files that are tracked by git
   - Use environment variables or secure configuration management tools
   - Add configuration files with keys to `.gitignore`

2. **Keep your API keys private**
   - Do not share your API keys in public forums, chat rooms, or documentation
   - Do not include API keys in screenshots or screen recordings
   - Treat API keys like passwords

3. **Rotate keys regularly**
   - If you suspect your API key has been compromised, regenerate it immediately
   - Consider rotating keys periodically as a security best practice

4. **Use minimal permissions**
   - Only use API keys with the minimum required permissions
   - Monitor your API usage for unexpected activity

## Data Privacy

### What data is sent to external APIs

When using this skill, the following data may be sent to external services:

- **TradingView API**: Stock symbols, market queries, and analysis requests
- **RapidAPI**: Authentication headers and API requests

### What data is NOT sent

- Your local files and code (unless explicitly referenced in queries)
- Personal information beyond what's required for API authentication
- Conversation history (unless you explicitly include it in queries)

## External Dependencies

This skill relies on the following external services:

- **RapidAPI** (https://rapidapi.com) - API gateway and authentication
- **TradingView Data API** (https://example-mcp-server.com) - Market data provider

These services have their own security policies and terms of service. Please review:
- [RapidAPI Terms of Service](https://rapidapi.com/terms/)
- [RapidAPI Privacy Policy](https://rapidapi.com/privacy/)

## Reporting Security Issues

If you discover a security vulnerability in this skill, please report it by:

1. **Do NOT** open a public GitHub issue
2. Contact the maintainer directly through GitHub private message
3. Provide detailed information about the vulnerability
4. Allow reasonable time for the issue to be addressed before public disclosure

## Security Best Practices for Users

### Configuration File Security

When configuring the MCP server, ensure your configuration file is secure:

```bash
# Set appropriate file permissions (Unix/Linux/macOS)
chmod 600 ~/Library/Application\ Support/Cursor/mcp_config.json
```

### Using Environment Variables (Advanced)

For enhanced security, consider using environment variables instead of hardcoded keys:

```json
{
  "mcpServers": {
    "RapidAPI Hub - TradingView Data": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: tradingview-data1.p.rapidapi.com",
        "--header",
        "x-api-key: ${RAPIDAPI_KEY}"
      ]
    }
  }
}
```

Then set the environment variable:
```bash
export RAPIDAPI_KEY="your-actual-key-here"
```

### Monitoring API Usage

Regularly check your RapidAPI dashboard to:
- Monitor API call volume
- Detect unusual activity
- Stay within rate limits
- Review billing (if applicable)

## Rate Limiting and Abuse Prevention

- The free tier has rate limits to prevent abuse
- Excessive requests may result in temporary blocks
- Use caching when possible to reduce API calls
- Implement exponential backoff for retries

## Disclaimer

This skill is provided "as is" without warranty of any kind. Users are responsible for:
- Securing their own API keys
- Complying with terms of service of external APIs
- Understanding the risks of using third-party services
- Any investment decisions made using this tool

**Investment Risk Warning**: This tool is for educational and research purposes only. It does not constitute financial advice. All investment decisions are made at your own risk.

## License

This security policy is part of the TradingView Quantitative Skills project and is licensed under the MIT License.
