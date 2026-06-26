# Travel Mapify Troubleshooting Guide

## Common Issues and Solutions

### 1. HTML Files Display as Source Code Instead of Rendered Webpage

#### Problem
When opening generated HTML files directly (using `file://` protocol), the browser displays raw HTML/JavaScript code instead of rendering the interactive map.

#### Root Cause
- **Browser Security Restrictions**: Modern browsers block external JavaScript resources (like AMap API) when loaded from local files (`file://` protocol)
- **CORS Policy**: Cross-Origin Resource Sharing restrictions prevent loading external APIs from local files
- **JavaScript Execution Blocked**: Browser security policies disable JavaScript execution for local files in some cases

#### Solutions

##### ✅ Recommended: Use Local HTTP Server
```bash
# Navigate to your workspace directory
cd /Users/xuandu/.openclaw/workspace

# Start a simple HTTP server (Python 3)
python3 -m http.server 8081

# Access your map via:
# http://localhost:8081/your-travel-map.html
```

##### ✅ Alternative: Configure Browser Security (Not Recommended for Production)
- **Chrome**: Launch with `--allow-file-access-from-files` flag (security risk)
- **Firefox**: Set `security.fileuri.strict_origin_policy` to `false` in `about:config`

##### ✅ Best Practice: Always Test via HTTP Server
- Never rely on `file://` protocol for web applications with external dependencies
- Use local development servers for testing
- Deploy to proper web hosting for production use

### 2. Map Not Loading or Blank Screen

#### Problem
Map container appears but no map tiles or markers are displayed.

#### Root Causes and Solutions

##### A. AMap API Key Issues
- **Domain Restrictions**: AMap API keys are often restricted to specific domains
- **Solution**: 
  - Add `localhost`, `127.0.0.1`, and your deployment domain to AMap Console whitelist
  - Use a valid, unrestricted API key for development

##### B. Network Connectivity
- **Firewall/Proxy**: Corporate networks may block external APIs
- **Solution**: 
  - Test API connectivity: `curl "https://webapi.amap.com/maps?v=2.0&key=YOUR_KEY"`
  - Ensure network allows access to `webapi.amap.com`

##### C. JavaScript Errors
- **Console Errors**: Check browser developer tools (F12) for JavaScript errors
- **Solution**:
  - Open Developer Tools → Console tab
  - Look for CORS, syntax, or API errors
  - Fix identified issues in HTML/JavaScript code

### 3. localStorage Data Corruption

#### Problem
Map fails to load POI data due to corrupted or incompatible localStorage data.

#### Root Cause
- Previous versions stored different data formats in localStorage
- Manual modifications or browser extensions may corrupt data
- Cross-browser compatibility issues

#### Solutions

##### A. Clear localStorage
```javascript
// In browser console (F12)
localStorage.removeItem('travelMapPois');
localStorage.removeItem('chongqingTravelPlan');
location.reload();
```

##### B. Implement Fallback Logic
Always include fallback POI data in your HTML templates:
```javascript
var poiList = JSON.parse(localStorage.getItem('travelMapPois')) || [
    // Default/fallback POIs here
    {
        name: "Default Location",
        location: [106.575329, 29.557253],
        address: "Fallback address"
    }
];
```

##### C. Validate Data Structure
Add data validation before using localStorage data:
```javascript
function isValidPOI(poi) {
    return poi && 
           typeof poi.name === 'string' && 
           Array.isArray(poi.location) && 
           poi.location.length === 2;
}

var storedData = JSON.parse(localStorage.getItem('travelMapPois'));
var poiList = Array.isArray(storedData) && storedData.every(isValidPOI) 
    ? storedData 
    : DEFAULT_POIS;
```

### 4. Poor OCR Quality from Input Images

#### Problem
OCR extraction fails to identify POIs correctly from travel planning images.

#### Root Causes
- Low image quality or resolution
- Handwritten text or stylized fonts
- Complex backgrounds interfering with text recognition
- Mixed languages without proper OCR configuration

#### Solutions

##### A. Image Preprocessing
- Convert to high-contrast black and white
- Increase resolution if possible
- Crop to focus on text areas only
- Remove background noise

##### B. OCR Configuration
Use appropriate language settings:
```bash
# For Chinese + English mixed content
tesseract input.jpg output -l chi_sim+eng --psm 6

# For better layout analysis
tesseract input.jpg output -l chi_sim+eng --psm 1
```

##### C. Manual POI Entry
When automatic extraction fails:
- Provide manual search functionality in the interface
- Allow users to add POIs by name through search
- Implement drag-and-drop marker placement for unknown locations

### 5. Performance Issues with Large POI Lists

#### Problem
Map becomes slow or unresponsive with many POIs (>20).

#### Solutions

##### A. Optimize Marker Rendering
- Use simple marker icons instead of complex HTML
- Limit info window content size
- Implement marker clustering for dense areas

##### B. Efficient Route Drawing
- Simplify polyline paths for long routes
- Use requestAnimationFrame for smooth updates
- Debounce reordering operations

##### C. Memory Management
- Remove unused markers when POIs are deleted
- Clean up event listeners properly
- Use efficient data structures for POI storage

## Development Best Practices

### 1. Always Test via HTTP Server
```bash
# Good practice for local development
cd /your/project/directory
python3 -m http.server 8000
# Then visit http://localhost:8000
```

### 2. Implement Robust Error Handling
```javascript
// Wrap API calls in try-catch
try {
    var map = new AMap.Map('container', config);
} catch (error) {
    console.error('Map initialization failed:', error);
    showErrorMessage('地图加载失败，请检查网络连接');
}
```

### 3. Provide User Feedback
- Show loading indicators during API calls
- Display clear error messages for common issues
- Offer alternative actions when automatic processes fail

### 4. Validate All Inputs
- Sanitize user inputs before API calls
- Validate coordinate ranges before processing
- Check data structure integrity before use

### 5. Document Dependencies
Clearly document all external dependencies:
- AMap Web API key requirements
- Local proxy server setup (port 8769)
- Browser compatibility requirements
- Network connectivity needs

## Debugging Checklist

When maps don't work as expected:

1. **Check Browser Console** (F12) for JavaScript errors
2. **Verify Network Tab** for failed API requests
3. **Test API Key** independently with curl/wget
4. **Clear localStorage** to eliminate data corruption
5. **Use HTTP Server** instead of file:// protocol
6. **Validate HTML Structure** with W3C validator
7. **Test in Multiple Browsers** to isolate browser-specific issues

## Emergency Recovery

If all else fails:

1. **Use the Working Template**: Copy from `cq-travel-map-working.html`
2. **Hard-code POI Data**: Remove localStorage dependency temporarily  
3. **Simplify Map Configuration**: Use basic AMap.Map() without advanced layers
4. **Manual Testing**: Test each component separately (markers, polylines, etc.)

This troubleshooting guide should help resolve 95% of common issues encountered when using the travel-mapify skill.