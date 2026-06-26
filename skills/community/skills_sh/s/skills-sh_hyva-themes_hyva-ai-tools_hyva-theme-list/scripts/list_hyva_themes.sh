#!/bin/bash
# Lists all Hyvä themes in a Magento 2 project
# Hyvä themes are identified by the presence of web/tailwind/package.json
#
# Searches:
#   - app/design/frontend/ (custom themes)
#   - vendor/ (installed themes from any vendor)
#
# Usage: list_hyva_themes.sh
# Output: One theme path per line (relative to project root)

set -euo pipefail

# Find themes in app/design/frontend/
# Structure: app/design/frontend/Vendor/ThemeName/web/tailwind/package.json
find app/design/frontend -path "*/web/tailwind/package.json" -type f 2>/dev/null | while read -r package_json; do
    theme_path="${package_json%/web/tailwind/package.json}"
    # Only include if it has theme.xml (valid Magento theme)
    if [ -f "$theme_path/theme.xml" ]; then
        echo "$theme_path"
    fi
done

# Find themes in vendor/
# Structure: vendor/vendor-name/package-name/web/tailwind/package.json
find vendor -path "*/web/tailwind/package.json" -type f 2>/dev/null | while read -r package_json; do
    theme_path="${package_json%/web/tailwind/package.json}"
    # Only include if it looks like a theme (has theme.xml)
    if [ -f "$theme_path/theme.xml" ]; then
        echo "$theme_path"
    fi
done
