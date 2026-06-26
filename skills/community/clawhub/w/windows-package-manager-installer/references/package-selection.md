# Package Manager Selection Notes

Use these heuristics when choosing between winget and Chocolatey.

## Prefer winget when
- the package is a mainstream desktop application
- the user wants the closest-to-native Windows installation path
- App Installer is already present and `winget` is working

## Prefer Chocolatey when
- `winget` is missing or broken
- the package is a CLI/developer utility often maintained in Chocolatey
- the user explicitly asks for `choco`
- you want one consistent package-manager flow after Chocolatey has already been installed

## Fallback logic
1. Check `winget`
2. Check `choco`
3. If neither is available, install the missing package manager environment first
4. If the package is not likely to be available in either manager, explain that and switch to manual vendor-install guidance
