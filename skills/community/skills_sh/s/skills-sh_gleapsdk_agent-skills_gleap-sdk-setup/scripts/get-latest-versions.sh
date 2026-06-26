#!/bin/bash
# Fetches the latest Gleap SDK versions from all package registries.
# Output is structured for easy parsing by Claude.

# Helper: extract a JSON string value by key (handles both compact and pretty JSON)
json_val() {
  grep -o "\"$1\" *: *\"[^\"]*\"" | head -1 | sed 's/.*: *"//;s/"$//'
}

echo "=== Gleap SDK Latest Versions ==="
echo ""

# JavaScript (npm)
JS_VERSION=$(curl -sf https://registry.npmjs.org/gleap/latest | json_val version)
echo "JavaScript (npm: gleap): ${JS_VERSION:-unknown}"

# React Native (npm)
RN_VERSION=$(curl -sf https://registry.npmjs.org/react-native-gleapsdk/latest | json_val version)
echo "React Native (npm: react-native-gleapsdk): ${RN_VERSION:-unknown}"

# Ionic/Capacitor (npm)
CAP_VERSION=$(curl -sf https://registry.npmjs.org/capacitor-gleap-plugin/latest | json_val version)
echo "Ionic/Capacitor (npm: capacitor-gleap-plugin): ${CAP_VERSION:-unknown}"

# Android (Maven Central)
ANDROID_VERSION=$(curl -sf "https://search.maven.org/solrsearch/select?q=g:io.gleap+AND+a:gleap-android-sdk&rows=1&wt=json" | json_val latestVersion)
echo "Android (Maven: io.gleap:gleap-android-sdk): ${ANDROID_VERSION:-unknown}"

# iOS (GitHub tags for SPM / CocoaPods)
IOS_VERSION=$(curl -sf https://api.github.com/repos/GleapSDK/Gleap-iOS-SDK/tags | json_val name)
echo "iOS (GitHub/CocoaPods: Gleap): ${IOS_VERSION:-unknown}"

# Flutter (pub.dev)
FLUTTER_VERSION=$(curl -sf https://pub.dev/api/packages/gleap_sdk | json_val version)
echo "Flutter (pub.dev: gleap_sdk): ${FLUTTER_VERSION:-unknown}"

# Cordova (npm)
CORDOVA_VERSION=$(curl -sf https://registry.npmjs.org/cordova-plugin-gleap/latest | json_val version)
echo "Cordova (npm: cordova-plugin-gleap): ${CORDOVA_VERSION:-unknown}"

echo ""
echo "Use these versions in install commands instead of hardcoded values."
