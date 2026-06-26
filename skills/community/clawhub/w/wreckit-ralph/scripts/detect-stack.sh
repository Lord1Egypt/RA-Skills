#!/usr/bin/env bash
# wreckit — detect language, framework, test runner, type checker
# Usage: ./detect-stack.sh [project-path]
# Outputs JSON to stdout

set -euo pipefail
PROJECT="${1:-.}"
PROJECT="$(cd "$PROJECT" && pwd)"
cd "$PROJECT"

lang=""
framework=""
test_runner=""
type_checker=""
build_cmd=""
test_cmd=""
type_cmd=""

# TypeScript / JavaScript
if [ -f "tsconfig.json" ]; then
  lang="typescript"
  type_checker="tsc"
  type_cmd="npx tsc --noEmit"
  if [ -f "package.json" ]; then
    if grep -q '"next"' package.json 2>/dev/null; then framework="nextjs"
    elif grep -q '"express"' package.json 2>/dev/null; then framework="express"
    elif grep -q '"fastify"' package.json 2>/dev/null; then framework="fastify"
    elif grep -q '"react"' package.json 2>/dev/null; then framework="react"
    elif grep -q '"vue"' package.json 2>/dev/null; then framework="vue"
    elif grep -q '"svelte"' package.json 2>/dev/null; then framework="svelte"
    fi
    if grep -q '"vitest"' package.json 2>/dev/null; then test_runner="vitest"; test_cmd="npx vitest run"
    elif grep -q '"jest"' package.json 2>/dev/null; then test_runner="jest"; test_cmd="npx jest"
    elif grep -q '"mocha"' package.json 2>/dev/null; then test_runner="mocha"; test_cmd="npx mocha"
    elif grep -q 'node --test' package.json 2>/dev/null; then test_runner="node-test"; test_cmd="npm test"
    fi
  fi
elif [ -f "package.json" ] && [ ! -f "tsconfig.json" ]; then
  lang="javascript"
  if grep -q '"vitest"' package.json 2>/dev/null; then test_runner="vitest"; test_cmd="npx vitest run"
  elif grep -q '"jest"' package.json 2>/dev/null; then test_runner="jest"; test_cmd="npx jest"
  elif grep -q 'node --test' package.json 2>/dev/null; then test_runner="node-test"; test_cmd="npm test"
  fi
fi

# Python
if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
  lang="python"
  if [ -f "pyproject.toml" ]; then
    if grep -q "django" pyproject.toml 2>/dev/null; then framework="django"
    elif grep -q "fastapi" pyproject.toml 2>/dev/null; then framework="fastapi"
    elif grep -q "flask" pyproject.toml 2>/dev/null; then framework="flask"
    fi
    if grep -q "pytest" pyproject.toml 2>/dev/null; then test_runner="pytest"; test_cmd="pytest"
    fi
  fi
  if command -v mypy &>/dev/null; then type_checker="mypy"; type_cmd="mypy --strict ."
  elif command -v pyright &>/dev/null; then type_checker="pyright"; type_cmd="pyright"
  fi
  [ -z "$test_runner" ] && test_runner="pytest" && test_cmd="pytest"
fi

# Rust
if [ -f "Cargo.toml" ]; then
  lang="rust"
  type_checker="rustc"
  type_cmd="cargo check"
  test_runner="cargo"
  test_cmd="cargo test"
  if grep -q "actix" Cargo.toml 2>/dev/null; then framework="actix"
  elif grep -q "axum" Cargo.toml 2>/dev/null; then framework="axum"
  elif grep -q "rocket" Cargo.toml 2>/dev/null; then framework="rocket"
  fi
fi

# Go
if [ -f "go.mod" ]; then
  lang="go"
  type_checker="go"
  type_cmd="go vet ./..."
  test_runner="go"
  test_cmd="go test ./..."
  if grep -q "gin-gonic" go.mod 2>/dev/null; then framework="gin"
  elif grep -q "echo" go.mod 2>/dev/null; then framework="echo"
  elif grep -q "fiber" go.mod 2>/dev/null; then framework="fiber"
  fi
fi

# Swift / Xcode
# Detect: Package.swift (SPM), *.xcodeproj, *.xcworkspace, Podfile (CocoaPods), Cartfile (Carthage)
SWIFT_DETECTED=0
build_system=""
type_check_confidence=""
mutation_support="false"  # No production mutation testing tool exists for Swift

HAS_SPM=0; [ -f "Package.swift" ] && HAS_SPM=1
HAS_XCODEPROJ=0; find . -name "*.xcodeproj" -maxdepth 2 2>/dev/null | head -1 | grep -q . && HAS_XCODEPROJ=1
HAS_XCWORKSPACE=0; find . -name "*.xcworkspace" -maxdepth 2 -not -path "*/xcodeproj/*" 2>/dev/null | head -1 | grep -q . && HAS_XCWORKSPACE=1
HAS_PODFILE=0; [ -f "Podfile" ] && HAS_PODFILE=1
HAS_CARTFILE=0; [ -f "Cartfile" ] && HAS_CARTFILE=1

if [ "$HAS_SPM" -eq 1 ] || [ "$HAS_XCODEPROJ" -eq 1 ] || [ "$HAS_XCWORKSPACE" -eq 1 ] || [ "$HAS_PODFILE" -eq 1 ] || [ "$HAS_CARTFILE" -eq 1 ]; then
  SWIFT_DETECTED=1
  lang="swift"

  # Determine build system
  SYSTEMS=0
  [ "$HAS_SPM" -eq 1 ] && SYSTEMS=$((SYSTEMS + 1))
  [ "$HAS_XCODEPROJ" -eq 1 ] && SYSTEMS=$((SYSTEMS + 1))
  [ "$HAS_PODFILE" -eq 1 ] && SYSTEMS=$((SYSTEMS + 1))
  [ "$HAS_CARTFILE" -eq 1 ] && SYSTEMS=$((SYSTEMS + 1))

  if [ "$SYSTEMS" -gt 1 ]; then
    build_system="mixed"
    type_check_confidence="medium"
  elif [ "$HAS_SPM" -eq 1 ]; then
    build_system="spm"
    type_check_confidence="high"
  elif [ "$HAS_PODFILE" -eq 1 ]; then
    build_system="cocoapods"
    type_check_confidence="medium"
  elif [ "$HAS_CARTFILE" -eq 1 ]; then
    build_system="carthage"
    type_check_confidence="medium"
  elif [ "$HAS_XCODEPROJ" -eq 1 ] || [ "$HAS_XCWORKSPACE" -eq 1 ]; then
    build_system="xcodebuild"
    type_check_confidence="medium"
  fi

  # Set type check command based on build system
  if [ "$HAS_SPM" -eq 1 ]; then
    type_checker="swift"
    type_cmd="swift build"
    build_cmd="swift build"
  elif [ "$HAS_XCODEPROJ" -eq 1 ] || [ "$HAS_XCWORKSPACE" -eq 1 ]; then
    type_checker="xcodebuild"
    # Try to detect a scheme; graceful fallback
    SCHEME=$(xcodebuild -list 2>/dev/null | sed -n '/Schemes:/,/^$/p' | grep -m1 '^\s' | xargs 2>/dev/null || echo "")
    if [ -n "$SCHEME" ]; then
      type_cmd="xcodebuild build -scheme $SCHEME -quiet"
      build_cmd="xcodebuild build -scheme $SCHEME -quiet"
    else
      type_cmd="xcodebuild build -quiet"
      build_cmd="xcodebuild build -quiet"
    fi
  fi

  # Test runner
  if [ "$HAS_SPM" -eq 1 ]; then
    test_runner="swift"
    test_cmd="swift test"
  else
    test_runner="xcodebuild"
    SCHEME=$(xcodebuild -list 2>/dev/null | sed -n '/Schemes:/,/^$/p' | grep -m1 '^\s' | xargs 2>/dev/null || echo "")
    if [ -n "$SCHEME" ]; then
      test_cmd="xcodebuild test -scheme $SCHEME -quiet"
    else
      test_cmd="xcodebuild test -quiet"
    fi
  fi

  # Framework detection
  if [ -f "Package.swift" ]; then
    if grep -q "Vapor" Package.swift 2>/dev/null; then framework="vapor"
    elif grep -q "Kitura" Package.swift 2>/dev/null; then framework="kitura"
    elif grep -q "Perfect" Package.swift 2>/dev/null; then framework="perfect"
    fi
  fi
  if [ "$HAS_PODFILE" -eq 1 ] && [ -z "$framework" ]; then
    if grep -q "Alamofire" Podfile 2>/dev/null; then framework="alamofire"; fi
  fi
fi

# Java / Kotlin
if [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
  if find . -name "*.kt" -maxdepth 3 2>/dev/null | head -1 | grep -q .; then
    lang="kotlin"
  else
    lang="java"
  fi
  type_checker="gradle"
  type_cmd="./gradlew compileJava"
  test_runner="gradle"
  test_cmd="./gradlew test"
  if grep -q "spring" build.gradle* 2>/dev/null; then framework="spring"; fi
elif [ -f "pom.xml" ]; then
  lang="java"
  type_checker="maven"
  type_cmd="mvn compile"
  test_runner="maven"
  test_cmd="mvn test"
fi

# Shell (fallback — detect if there are .sh files with a run_tests.sh or similar)
if [ -z "$lang" ]; then
  SH_COUNT=$(find . -name '*.sh' -not -path '*/.git/*' -not -path '*/node_modules/*' 2>/dev/null | wc -l | tr -d ' ')
  if [ "$SH_COUNT" -gt 0 ]; then
    lang="shell"
    # Look for a test runner script
    if [ -f "tests/run_tests.sh" ]; then test_cmd="bash tests/run_tests.sh"; test_runner="bash"
    elif [ -f "test/run_tests.sh" ]; then test_cmd="bash test/run_tests.sh"; test_runner="bash"
    elif [ -f "run_tests.sh" ]; then test_cmd="bash run_tests.sh"; test_runner="bash"
    elif find . -name "run_tests.sh" -not -path '*/.git/*' 2>/dev/null | head -1 | grep -q .; then
      RUNNER=$(find . -name "run_tests.sh" -not -path '*/.git/*' 2>/dev/null | head -1)
      test_cmd="bash $RUNNER"; test_runner="bash"
    fi
    if command -v shellcheck &>/dev/null; then type_checker="shellcheck"; type_cmd="shellcheck *.sh"; fi
  fi
fi

# Build JSON output — use Python to ensure valid JSON (handles special chars in commands)
python3 - <<PYEOF
import json
data = {
    "language": "${lang:-unknown}",
    "framework": "${framework:-none}",
    "testRunner": "${test_runner:-none}",
    "typeChecker": "${type_checker:-none}",
    "commands": {
        "typeCheck": "${type_cmd:-none}",
        "test": "${test_cmd:-none}",
        "build": "${build_cmd:-none}"
    }
}
# Swift-specific fields
if "${lang:-unknown}" == "swift":
    data["buildSystem"] = "${build_system:-unknown}"
    data["typeCheckConfidence"] = "${type_check_confidence:-medium}"
    data["mutationSupport"] = False  # No production mutation testing tool for Swift
    data["swiftIndicators"] = {
        "spm": ${HAS_SPM:-0} == 1,
        "xcodeproj": ${HAS_XCODEPROJ:-0} == 1,
        "xcworkspace": ${HAS_XCWORKSPACE:-0} == 1,
        "cocoapods": ${HAS_PODFILE:-0} == 1,
        "carthage": ${HAS_CARTFILE:-0} == 1
    }
print(json.dumps(data, indent=2))
PYEOF
