# Licensing Errors and Solutions

## Table of Contents
- [License Key Not Registered](#license-key-not-registered-error)
- [Invalid License Key](#invalid-license-key-error)
- [Trial License Expired](#trial-license-expired-error)
- [Platform Mismatch](#platform-mismatch-error)
- [Version Mismatch](#version-mismatch-error)
- [NPX Command Errors](#npx-command-errors)

## Overview

Syncfusion licensing errors appear in browser console when license key is missing, invalid, or improperly configured. **All errors are non-blocking** - application continues to work normally with console warnings only.

## License Key Not Registered Error

### Error Message
```
This application was built using a trial version of Syncfusion Essential Studio.
Please include a valid license key in the application.
```

### Cause
Syncfusion license key not registered in the application.

### Solution

Generate license key from [Syncfusion Portal](https://www.syncfusion.com/account/downloads).

**Step 1:** Set the environment variable:

```bash
# Windows
setx SYNCFUSION_LICENSE "Your_License_Key_Here"

# Mac/Linux
export SYNCFUSION_LICENSE='Your_License_Key_Here'
```

**Step 2:** Activate the license using NPX command:

```bash
npx syncfusion-license activate
```

## Invalid License Key Error

### Error Message
```
The included Syncfusion license key is invalid.
```

### Common Causes
1. Malformed key (spaces/line breaks)
2. Wrong platform (v30.x.x and earlier)
3. Wrong version
4. Wrong edition (v31.1.17+)

### Solution: Malformed Key

Key must be single line, 100-150 characters, no spaces or line breaks. Re-copy license key from portal carefully and ensure entire key is copied.

### Solution: Wrong Platform (v30.x.x)

1. Go to [License Portal](https://www.syncfusion.com/account/downloads)
2. Select version 30.x.x or earlier
3. Select platform: **React**
4. Generate and replace key

### Solution: Wrong Edition (v31.1.17+)

1. Go to [License Portal](https://www.syncfusion.com/account/downloads)
2. Select version 31.x.x or higher
3. Select **all 5 editions/SDKs** (UI Edition, Document SDK, DOCX Editor SDK, PDF Viewer SDK, Spreadsheet Editor SDK)
4. Generate Enterprise Edition key
5. Replace old key

### Solution: Wrong Version

Check version:
```bash
npm list @syncfusion/ej2-react-grids
```

Generate key matching exact version from [License Portal](https://www.syncfusion.com/account/downloads).

## Trial License Expired Error

**Error Message**
```
Your Syncfusion trial license has expired.
```

**Causes**

**Primary** - 30-day trial period ended
**Secondary** - configuration npm package mismatch

### 30-day Trial Period Solutions

**Option 1: Purchase License**  
Visit [Syncfusion Sales](https://www.syncfusion.com/sales/products)
- Community License (Free for <$1M revenue)
- Commercial License (Paid)

**Option 2: Community License**  
Apply at [Community License](https://www.syncfusion.com/products/communitylicense) (approval in 1-2 days)

**Option 3: Extend Trial**  
Email [support@syncfusion.com](mailto:support@syncfusion.com) (case-by-case)

### Configuration Mismatch Solutions

#### Explicit @syncfusion/ej2-base Dependency

Remove `@syncfusion/ej2-base` from package.json (auto-installed with other packages):

```json
{
  "dependencies": {
    "@syncfusion/ej2-react-grids": "25.1.35"
    // ✅ @syncfusion/ej2-base installed automatically
  }
}
```

Then: Delete node_modules, package-lock.json → `npm install` → Clear cache

#### Major Version Conflict with ^ Symbol

Use `~` (tilde) instead of `^` (caret) to prevent major version upgrades:

```json
{
  "dependencies": {
    "@syncfusion/ej2-react-grids": "~25.1.35",  // ✅ Only 25.1.x patches
    "@syncfusion/ej2-react-buttons": "~25.1.35"
  }
}
```

Version symbols:
- `^25.1.35` - Allows 25.x.x ❌
- `~25.1.35` - Only 25.1.x ✅
- `25.1.35` - Exact version ✅

## Platform Mismatch Error

### Error Message
```
The included Syncfusion license key is not valid for this platform.
```

### Cause (v30.x.x and Earlier)

License key generated for one platform but used in another (e.g., Angular key in React project).

### Solution

**Verify platform:**
```bash
cat package.json | grep "@syncfusion"
# Expected for React: "@syncfusion/ej2-react-*"
```

**Generate correct platform key:**
1. Go to [License Portal](https://www.syncfusion.com/account/downloads)
2. Select version 30.x.x or earlier
3. Select platform: **React**
4. Generate key

**Note:** For v31.1.17+, platform mismatch errors don't occur - UI Edition/Enterprise Edition keys work across all platforms.

## Version Mismatch Error

### Error Message
```
The included Syncfusion license key is not valid for version {installed_version}.
```

### Cause

License key version doesn't match installed package version.

### Solution

**Step 1:** Check all Syncfusion package versions
```bash
npm list | grep @syncfusion

# Expected (all same version):
# @syncfusion/ej2-react-grids@25.1.35
# @syncfusion/ej2-react-buttons@25.1.35
# @syncfusion/ej2-base@25.1.35
```

**Step 2:** Update all packages to same version if mixed
```bash
npm install @syncfusion/ej2-react-grids@26.1.35 @syncfusion/ej2-react-buttons@26.1.35
```

**Step 3:** Generate new license key for exact version from [License Portal](https://www.syncfusion.com/account/downloads)

**Step 4:** Clear cache
```bash
rm -rf node_modules/.cache
npm start
```

### Version Update Workflow

```bash
# 1. Update packages
npm install @syncfusion/ej2-react-grids@26.1.35

# 2. Verify versions match
npm list | grep @syncfusion

# 3. Generate new license key for v26.1.35 from portal

# 4. Update environment variable with new key

# 5. Clear cache
rm -rf node_modules/.cache

# 6. Restart
npm start
```

## NPX Command Errors

### Error: Invalid License Key Structure
```
Error: Invalid license key structure.
```

**Solution:**
```bash
echo "YOUR_COMPLETE_LICENSE_KEY" > syncfusion-license.txt
npx syncfusion-license activate
```

### Error: Version Mismatch
```
Error: License key version (25.1.35) does not match installed package version (26.1.35).
```

**Solution:**
1. Check version: `npm list @syncfusion/ej2-base`
2. Generate new key for that version
3. Update `syncfusion-license.txt`
4. Run: `npx syncfusion-license activate`

### Error: Platform Mismatch
```
Error: License key platform (Angular) does not match detected platform (React).
```

**Solution (v30.x.x):**
1. Generate React platform key
2. Update `syncfusion-license.txt`
3. Run: `npx syncfusion-license activate`

### Error: Trial License Expired
```
Error: Trial license has expired.
```

**Solution:**
1. Purchase or apply for community license
2. Generate new paid license key
3. Update `syncfusion-license.txt`
4. Run: `npx syncfusion-license activate`

### Error: License File Not Found
```
Error: License file not found.
```

**Solution Option 1:**
```bash
echo "YOUR_LICENSE_KEY" > syncfusion-license.txt
npx syncfusion-license activate
```

**Solution Option 2:**
```bash
# Windows
$env:SYNCFUSION_LICENSE="YOUR_LICENSE_KEY"
npx syncfusion-license activate

# macOS/Linux
export SYNCFUSION_LICENSE="YOUR_LICENSE_KEY"
npx syncfusion-license activate
```
