# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it privately by opening an issue on [GitHub](https://github.com/neuhanli/skills/issues).

## Security Best Practices

### Before Installation

1. **Review Source Code**
   - Carefully examine `scripts/tencent_hotsearch.py`
   - Review `requirements.txt` for dependencies
   - Check `config.example.json` for configuration structure

2. **Verify the Repository and Publisher**
   - Confirm the official repository: https://github.com/neuhanli/skills
   - Check for signed releases and commit history
   - Review issues and pull requests for community feedback

3. **Check for Code Integrity**
   - Verify file checksums if provided
   - Compare with official repository before installation
   - Look for any unexpected modifications

### Credential Management

- ✅ **Use Temporary API Keys**: Only use temporary/least-privileged API keys for testing
- ✅ **Rotate Keys Regularly**: Change API keys periodically and after each testing session
- ✅ **Never Commit config.json**: The file is already in `.gitignore` - respect this
- ✅ **Set File Permissions**: Use `chmod 600 config.json` on Linux/macOS
- ✅ **Use Dedicated Keys**: Create separate API keys for this skill, not your production keys
- ✅ **Monitor Usage**: Regularly check API usage in Tencent Cloud console

### Runtime Security

- ✅ **Run in Isolated Environment**: Use container/VM for execution
- ✅ **Non-Sensitive Output Directory**: Do not point `output_dir` to sensitive system paths
- ✅ **Review Dependencies**: Audit `requirements.txt` before running `pip install`
- ✅ **Network Restrictions**: The skill only accesses `wsa.tencentcloudapi.com`
- ✅ **Monitor Network Activity**: Watch for unexpected network connections

### File System Security

- ✅ **Protected Configuration**: `config.json` is excluded from version control
- ✅ **Output Directory Validation**: The skill prevents directory traversal attacks
- ✅ **Secret Masking**: API keys are masked in logs and error messages

## Audit Checklist

Before using this skill, complete the following checklist:

- [ ] **Code Review**: Reviewed `scripts/tencent_hotsearch.py` completely
- [ ] **Dependency Audit**: Reviewed all packages in `requirements.txt`
- [ ] **Source Verified**: Confirmed repository authenticity
- [ ] **Temporary Credentials**: Created dedicated temporary API keys
- [ ] **Isolated Environment**: Set up container/VM for testing
- [ ] **Git Protection**: Verified `.gitignore` includes `config.json`
- [ ] **File Permissions**: Set `chmod 600 config.json`
- [ ] **Output Path**: Configured non-sensitive output directory
- [ ] **Network Monitoring**: Prepared to monitor network activity

## Known Security Features

This skill implements the following security measures:

### ✅ Path Traversal Prevention
The skill validates output paths to prevent directory traversal attacks:
```python
def _validate_output_path(self, output_path: str) -> Path:
    # Ensures output is within configured directory
    # Prevents '../' and other traversal patterns
```

### ✅ Secret Masking
API credentials are masked in all logs and error messages:
```python
def _mask_secret(self, secret: str) -> str:
    # Returns 'AKID...xxxx' instead of full secret
```

### ✅ HTTPS Only
All API requests use encrypted HTTPS connections to official endpoints only.

### ✅ Error Handling
Comprehensive error handling with secure credential management - no secrets exposed in exceptions.

### ✅ Git Protection
`.gitignore` is configured to exclude `config.json` and output files from version control.

## Dependency Information

### Required Packages

**None** - This skill uses only Python standard library modules:
- `urllib.request` - HTTP requests (stdlib)
- `urllib.parse` - URL parsing (stdlib)
- `json`, `os`, `sys`, `hashlib`, `hmac`, `time`, `datetime`, `pathlib`, `typing`, `argparse` - All stdlib

### Optional Packages
- `pandas>=2.0.0` - Only needed if you want to export results to CSV format

### Security Considerations
- No external dependencies required for core functionality
- All HTTP requests use Python's built-in `urllib` (no third-party packages)
- Manual HMAC-SHA256 signing implemented using stdlib `hashlib` and `hmac`
- If CSV export is needed, install pandas from official PyPI: `pip install pandas>=2.0.0`
- Consider using virtual environment for optional dependencies

## Building Trust

### Trust Concerns Addressed

This skill has been updated to address the following trust concerns identified in security assessments:

#### ✅ Registry Metadata Inconsistency Resolved
- **Issue**: Registry metadata claimed "no credentials/config required" while code requires Tencent API credentials
- **Resolution**: SKILL.md now explicitly declares `required_credentials` and `permissions`
- **User Action**: Always verify SKILL.md metadata matches your expectations

#### ✅ Code Transparency Enhanced
- **Issue**: Users need to verify code integrity before providing credentials
- **Resolution**: Added verification steps and GitHub repository links
- **User Action**: Review `scripts/tencent_hotsearch.py` before installation

#### ✅ Security Documentation Comprehensive
- **Issue**: Insufficient guidance on secure credential handling
- **Resolution**: Multi-layered security documentation (SECURITY.md, CONFIG.md, README.md)
- **User Action**: Read all security documentation before use

### For Publishers: Improving Trust

To further improve trust in this skill, publishers should consider:

- **Correct Registry Metadata**: Ensure registry accurately reflects credential requirements
- **Signed Releases**: Provide GPG-signed releases for verification
- **Checksums**: Publish SHA256 checksums for all files
- **Transparent Updates**: Maintain clear version history and changelog
- **Responsive Support**: Address security concerns promptly

### For Users: Verifying Trustworthiness

Before trusting this skill with API credentials:

1. **Code Review**: Verify the source code matches described functionality
2. **Dependency Audit**: Confirm no unexpected dependencies
3. **Network Monitoring**: Watch for unexpected API calls
4. **Credential Testing**: Use temporary keys in isolated environment
5. **Behavior Monitoring**: Check for unexpected file operations

### Trust Indicators

**Positive Indicators:**
- ✅ Uses only Python standard library (no external dependencies)
- ✅ Only accesses official Tencent API endpoint
- ✅ Implements path traversal protection
- ✅ Masks secrets in error messages
- ✅ Provides comprehensive security documentation

**Areas for Improvement:**
- ⚠️ Registry metadata inconsistency (addressed in documentation)
- ⚠️ File-based credential storage (use temporary keys)
- ⚠️ Requires user to verify code integrity

## Contact

For security-related questions or concerns:
- Open an issue on [GitHub](https://github.com/neuhanli/skills/issues)
- Review the main repository for contact information

## Version History

### v1.1.0
- Added comprehensive security policy
- Enhanced trust-building documentation
- Resolved registry metadata inconsistencies in documentation
- Added installation verification checklist

### v1.0.0
- Initial security policy
- Implemented path traversal prevention
- Added secret masking
- Configured .gitignore for credential protection
