# UI5 Development Server Features Complete Reference

**Official Documentation**: [https://ui5.github.io/cli/stable/pages/Server/](https://ui5.github.io/cli/stable/pages/Server/)

This reference provides comprehensive details about the UI5 development server features, middleware, and capabilities.

## Table of Contents

1. [Overview](#overview)
2. [Standard Middleware Stack](#standard-middleware-stack)
3. [HTTP/2 and HTTPS Support](#http2-and-https-support)
4. [Content Security Policy (CSP)](#content-security-policy-csp)
5. [Resource Processing](#resource-processing)
6. [SSL Certificate Management](#ssl-certificate-management)
7. [Server Configuration](#server-configuration)
8. [Testing Integration](#testing-integration)

---

## Overview

The UI5 Server module provides local development infrastructure for UI5 projects. It handles resource serving, theme compilation, testing utilities, and security policies through a middleware-based architecture.

**Key Features**:
- HTTP/2 and HTTPS support with automatic SSL certificates
- Content Security Policy (CSP) enforcement and reporting
- Automatic resource transformations
- Theme compilation (LESS to CSS)
- QUnit test runner integration
- Version info generation
- Custom middleware extensibility

---

## Standard Middleware Stack

The UI5 development server executes middleware in this specific order:

### 1. csp (Content Security Policy)
**Purpose**: Manages CSP headers for security testing

**Features**:
- Enabled by default
- Can send SAP-specific CSP policies
- Collects CSP violation reports

**Configuration**:
```bash
ui5 serve --sap-csp-policies        # Enable SAP CSP policies
ui5 serve --serve-csp-reports       # Collect violation reports
```

**Access Reports**:
```
http://localhost:8080/.ui5/csp/csp-reports.json
```

**See**: [Content Security Policy section](#content-security-policy-csp) below

---

### 2. compression
**Purpose**: Standard Express compression middleware

**Features**:
- Automatic gzip/deflate compression
- Reduces bandwidth usage
- Improves load times

**Headers Added**:
- `Content-Encoding: gzip` (or deflate)

---

### 3. cors (Cross-Origin Resource Sharing)
**Purpose**: Enable cross-origin requests for development

**Features**:
- Allows requests from any origin
- Adds CORS headers automatically

**Headers Added**:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: *`

---

### 4. discovery
**Purpose**: File listing for test suite integration

**Features**:
- Provides JSON file listings
- Used by test runners (Karma, etc.)

**Endpoint**:
```
http://localhost:8080/.ui5/discovery/
```

---

### 5. serveResources
**Purpose**: Main resource serving middleware

**Features**:
- Serves project and dependency resources
- Uses file system abstraction layer
- Applies automatic transformations

**Resource Transformations**:
- Non-ASCII character escaping in `.properties` files
- `manifest.json` enhancement with supported locales

**See**: [Resource Processing section](#resource-processing) below

---

### 6. testRunner
**Purpose**: Provides QUnit test runner interface

**Features**:
- Automatic test discovery
- Test suite execution
- Results reporting

**Endpoint**:
```
http://localhost:8080/test-resources/sap/ui/qunit/testrunner.html
```

**Usage**:
```bash
ui5 serve --open test-resources/sap/ui/qunit/testrunner.html
```

---

### 7. serveThemes
**Purpose**: Dynamic CSS compilation from LESS sources

**Features**:
- On-the-fly LESS to CSS compilation
- Theme parameter resolution
- CSS variable support (experimental)

**How It Works**:
1. Request for `.css` file
2. Checks for corresponding `.less` source
3. Compiles LESS to CSS dynamically
4. Caches compiled result
5. Serves CSS to browser

**Example**:
```
Request:  /resources/my/lib/themes/base/library.css
Compiles: /resources/my/lib/themes/base/library.less
Serves:   Compiled CSS
```

---

### 8. versionInfo
**Purpose**: Generates version info JSON dynamically

**Features**:
- Aggregates version information from all dependencies
- Provides library metadata
- Used by UI5 framework loader

**Endpoint**:
```
http://localhost:8080/resources/sap-ui-version.json
```

**Content Example**:
```json
{
  "name": "my.app",
  "version": "1.0.0",
  "buildTimestamp": "202511211200",
  "scmRevision": "",
  "gav": "",
  "libraries": [
    {
      "name": "sap.ui.core",
      "version": "1.120.0",
      "buildTimestamp": "",
      "scmRevision": ""
    }
  ]
}
```

---

### 9. nonReadRequests
**Purpose**: Block non-read HTTP methods

**Features**:
- Blocks POST, PUT, DELETE requests
- Returns 404 for blocked methods
- Prevents accidental data modification

**Blocked Methods**:
- POST
- PUT
- DELETE
- PATCH

**Response**: `404 Not Found`

---

### 10. serveIndex
**Purpose**: Directory listing HTML generation

**Features**:
- Automatic index page generation for directories
- File and folder navigation
- Simplified mode available

**Configuration**:
```bash
ui5 serve --simple-index           # Use simplified listing
```

**Example Output**:
```html
<!DOCTYPE html>
<html>
<head><title>Index of /resources/my/app/</title></head>
<body>
<h1>Index of /resources/my/app/</h1>
<ul>
  <li><a href="Component.js">Component.js</a></li>
  <li><a href="controller/">controller/</a></li>
  <li><a href="view/">view/</a></li>
</ul>
</body>
</html>
```

---

## HTTP/2 and HTTPS Support

### Overview

The UI5 server supports HTTP/2 protocol with automatic HTTPS configuration.

### Enabling HTTP/2

```bash
ui5 serve --h2                      # Enable HTTP/2 (auto-enables HTTPS)
```

**What Happens**:
1. Server starts with HTTPS on port 8443 (default)
2. HTTP/2 protocol enabled
3. Self-signed SSL certificate auto-generated
4. Certificate stored in `~/.ui5/server/`

### Port Configuration

**Default Ports**:
- HTTP: 8080
- HTTPS: 8443 (when using `--h2`)

**Custom Ports**:
```bash
ui5 serve --port 3000               # HTTP on port 3000
ui5 serve --h2 --port 4000          # HTTPS/HTTP2 on port 4000
```

**Configuration (ui5.yaml)**:
```yaml
server:
  settings:
    httpPort: 8080
    httpsPort: 8443
```

### Benefits of HTTP/2

1. **Multiplexing**: Multiple requests over single connection
2. **Header Compression**: Reduced overhead
3. **Server Push**: Proactive resource sending
4. **Better Performance**: Mimics production CDN behavior

### Best Practices

- **Use HTTP/2 for development** to match production environment
- **Test with HTTPS** to catch mixed content issues early
- **Trust certificates** in browser for best experience

---

## Content Security Policy (CSP)

### Overview

The CSP middleware enables testing of Content Security Policy compliance during development.

### Default Behavior

**Enabled by Default**: CSP middleware is active but permissive.

### SAP CSP Policies

Enable SAP-specific CSP policies for testing:

```bash
ui5 serve --sap-csp-policies
```

**Policies Activated**:
- `sap-target-level-1` (report-only)
- `sap-target-level-3` (report-only)

**Mode**: Report-only (doesn't block, only reports violations)

### CSP Reports Collection

Collect policy violation reports:

```bash
ui5 serve --sap-csp-policies --serve-csp-reports
```

**Access Reports**:
```bash
curl http://localhost:8080/.ui5/csp/csp-reports.json
```

**Report Format**:
```json
[
  {
    "csp-report": {
      "document-uri": "http://localhost:8080/index.html",
      "violated-directive": "script-src",
      "blocked-uri": "inline",
      "line-number": 42,
      "source-file": "http://localhost:8080/index.html"
    },
    "timestamp": "2025-11-21T12:00:00.000Z"
  }
]
```

### CSP Headers Sent

**sap-target-level-1**:
```
Content-Security-Policy-Report-Only:
  default-src 'self';
  script-src 'self' 'unsafe-eval';
  style-src 'self' 'unsafe-inline';
```

**sap-target-level-3**:
```
Content-Security-Policy-Report-Only:
  default-src 'self';
  script-src 'self';
  style-src 'self';
```

### Testing Workflow

1. **Enable CSP policies**:
   ```bash
   ui5 serve --sap-csp-policies --serve-csp-reports
   ```

2. **Test application** in browser

3. **Review violations**:
   ```bash
   curl http://localhost:8080/.ui5/csp/csp-reports.json | jq
   ```

4. **Fix violations** in code

5. **Re-test** until no violations

### Common CSP Violations

**Inline Scripts**:
```html
<!-- Violation -->
<script>console.log('test');</script>

<!-- Fix: Move to external file -->
<script src="script.js"></script>
```

**Inline Styles**:
```html
<!-- Violation -->
<div style="color: red;">Text</div>

<!-- Fix: Use CSS classes -->
<div class="red-text">Text</div>
```

**eval() Usage**:
```javascript
// Violation
eval("console.log('test')");

// Fix: Avoid eval, use alternatives
console.log('test');
```

---

## Resource Processing

The serveResources middleware automatically processes certain resources.

### Properties File Processing

**Non-ASCII Character Escaping**:

**.properties files** with non-ASCII characters are automatically escaped to ensure proper encoding.

**Example**:
```properties
# Source file (UTF-8)
greeting=Grüß Gott

# Served as (escaped)
greeting=Gr\u00FC\u00DF Gott
```

**Why**: Ensures compatibility with ISO-8859-1 parsers.

**Configuration**:
```yaml
resources:
  configuration:
    propertiesFileSourceEncoding: UTF-8  # Source encoding
```

### Manifest.json Enhancement

**Supported Locales Detection**:

The server automatically populates the `supportedLocales` property in `manifest.json` by detecting `.properties` files.

**How It Works**:
1. Scans project for i18n `.properties` files
2. Detects locale variants (e.g., `i18n_de.properties`, `i18n_fr.properties`)
3. Adds `supportedLocales` array to manifest

**Example**:

**File Structure**:
```
webapp/
├── i18n/
│   ├── i18n.properties          # Default
│   ├── i18n_de.properties       # German
│   ├── i18n_fr.properties       # French
│   └── i18n_es.properties       # Spanish
└── manifest.json
```

**Original manifest.json**:
```json
{
  "sap.app": {
    "i18n": "i18n/i18n.properties"
  }
}
```

**Enhanced manifest.json** (served):
```json
{
  "sap.app": {
    "i18n": {
      "bundleUrl": "i18n/i18n.properties",
      "supportedLocales": ["de", "fr", "es", ""]
    }
  }
}
```

**Requirements**:
- Manifest version 1.21.0+
- Resource bundles within project namespace
- Properties files follow naming convention (`name_locale.properties`)

---

## SSL Certificate Management

### Overview

When using `--h2`, UI5 CLI automatically generates self-signed SSL certificates.

### Certificate Location

**Storage**: `~/.ui5/server/` (or custom `ui5DataDir`)

**Files**:
```
~/.ui5/server/
├── server.crt                    # Certificate
└── server.key                    # Private key
```

### Certificate Generation

**Automatic**: Generated on first use of `--h2` flag

**Prompts**: User prompted to trust certificate

**Validity**: Typically 365 days

### Trusting Certificates

#### macOS
```bash
# Add to keychain
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain \
  ~/.ui5/server/server.crt

# Or open in Keychain Access and mark as trusted
open ~/.ui5/server/server.crt
```

#### Windows
```powershell
# Import certificate
certutil -addstore -f "ROOT" %USERPROFILE%\.ui5\server\server.crt
```

#### Linux
```bash
# Copy to trusted certificates (Ubuntu/Debian)
sudo cp ~/.ui5/server/server.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# Or for user only (Firefox)
# Import via Firefox settings
```

#### Browser Only
In browser warning:
1. Click "Advanced"
2. Click "Proceed to localhost (unsafe)"
3. Certificate remembered for session

### Regenerating Certificates

```bash
# Remove existing certificates
rm -rf ~/.ui5/server/

# Re-run server (generates new certificates)
ui5 serve --h2
```

### Using Custom Certificates

Custom HTTPS certificates are supported via CLI flags:

```bash
ui5 serve --h2 --key /path/to/server.key --cert /path/to/server.crt
```

**Default Certificates**: Auto-generated and stored in `~/.ui5/server/` (server.key, server.crt)

**Custom Certificate Options**:
- `--key <path>`: Path to private key file
- `--cert <path>`: Path to certificate file

**Advanced Scenarios**: For dynamic SNI, client certificates, or other complex requirements, use a reverse proxy or custom middleware.

---

## Server Configuration

### Via ui5.yaml

```yaml
server:
  settings:
    httpPort: 8080                # HTTP port
    httpsPort: 8443               # HTTPS port

  customMiddleware:
    - name: my-middleware
      afterMiddleware: compression
      configuration:
        key: value
```

### Via CLI Flags

```bash
ui5 serve \
  --port 3000 \                  # Port (HTTP or HTTPS with --h2)
  --h2 \                         # Enable HTTP/2 and HTTPS
  --key /path/to/key \           # Custom SSL key (optional)
  --cert /path/to/cert \         # Custom SSL certificate (optional)
  --accept-remote-connections \  # Allow non-localhost
  --sap-csp-policies \           # Enable CSP policies
  --serve-csp-reports \          # Collect CSP reports
  --simple-index                 # Simplified directory listing
```

### Remote Access

**Default**: Server only accepts connections from localhost

**Enable Remote Access**:
```bash
ui5 serve --accept-remote-connections
```

**Security Warning**: Only use on trusted networks!

**Access from Other Devices**:
```
http://<your-ip-address>:8080
https://<your-ip-address>:8443  # With --h2
```

**Find Your IP**:
```bash
# macOS/Linux
ifconfig | grep "inet "

# Windows
ipconfig
```

---

## Testing Integration

### QUnit Test Runner

**Access**:
```
http://localhost:8080/test-resources/sap/ui/qunit/testrunner.html
```

**Open Automatically**:
```bash
ui5 serve --open test-resources/sap/ui/qunit/testrunner.html
```

### karma-ui5 Integration

Custom middleware works with karma-ui5's internal server:

**Requirements**:
- Use Connect API only (not Express-specific features)
- Avoid `req.baseUrl`, `req.hostname`, `req.ip`, `req.ips`

**Example karma.conf.js**:
```javascript
module.exports = function(config) {
  config.set({
    frameworks: ['ui5'],
    ui5: {
      configPath: 'ui5.yaml',
      // Custom middleware loaded automatically
    }
  });
};
```

### Test Discovery

The discovery middleware provides file listings for test integration:

**Endpoint**:
```
http://localhost:8080/.ui5/discovery/all.json
```

**Response**:
```json
{
  "files": [
    "/resources/my/app/test/unit/AllTests.js",
    "/resources/my/app/test/integration/AllJourneys.js"
  ]
}
```

---

## Best Practices

1. **Use HTTP/2** during development to match production
2. **Enable CSP early** to catch violations before production
3. **Trust SSL certificates** properly for best developer experience
4. **Use custom middleware** for API proxying and mocking
5. **Test on mobile devices** using `--accept-remote-connections`
6. **Monitor CSP reports** regularly during development
7. **Use QUnit test runner** for comprehensive test execution
8. **Configure ports** via ui5.yaml for team consistency

---

## Common Issues

### Port Already in Use
See troubleshooting.md

### SSL Certificate Warnings
Trust certificates or proceed with warning (development only)

### CSP Violations Blocking App
Disable `--sap-csp-policies` temporarily, fix violations, re-enable

### Remote Connections Not Working
- Check firewall settings
- Verify `--accept-remote-connections` flag
- Ensure correct IP address used

---

**Last Updated**: 2025-11-21
**Official Docs**: [https://ui5.github.io/cli/stable/pages/Server/](https://ui5.github.io/cli/stable/pages/Server/)
