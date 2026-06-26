#!/bin/bash
#
# audit-skill.sh - Perform security audit on a skill
# Usage: ./audit-skill.sh <skill-path> [--verbose] [--output report.json]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${AUDIT_DATA_DIR:-$SKILL_DIR/data}"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
TARGET_SKILL=""
VERBOSE=false
OUTPUT_FILE=""
SCAN_TYPES="all"

while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose)
            VERBOSE=true
            shift
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --types)
            SCAN_TYPES="$2"
            shift 2
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            if [[ -z "$TARGET_SKILL" ]]; then
                TARGET_SKILL="$1"
            fi
            shift
            ;;
    esac
done

if [[ -z "$TARGET_SKILL" ]]; then
    echo "Usage: $0 <skill-path> [--verbose] [--output report.json] [--types secrets,injection,permissions]"
    exit 1
fi

if [[ ! -d "$TARGET_SKILL" ]]; then
    echo -e "${RED}❌ Error: Skill directory not found: $TARGET_SKILL${NC}"
    exit 1
fi

# Create data directory
mkdir -p "$DATA_DIR"

# Generate audit ID
DATE=$(date +%Y%m%d)
COUNTER=1
while [[ -f "$DATA_DIR/AUDIT-${DATE}-$(printf "%03d" $COUNTER).json" ]]; do
    COUNTER=$((COUNTER + 1))
done
AUDIT_ID="AUDIT-${DATE}-$(printf "%03d" $COUNTER)"
REPORT_FILE="$DATA_DIR/$AUDIT_ID.json"

SKILL_NAME=$(basename "$TARGET_SKILL")
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo -e "${BLUE}🔍 Starting security audit: $SKILL_NAME${NC}"
echo "================================"

# Initialize counters
CRITICAL=0
HIGH=0
MEDIUM=0
LOW=0
INFO=0
FINDINGS=()

# Function to add finding
add_finding() {
    local severity="$1"
    local type="$2"
    local file="$3"
    local line="$4"
    local description="$5"
    local recommendation="$6"
    
    local finding="{\"id\":\"SEC-$(printf "%03d" $((${#FINDINGS[@]} + 1)))\",\"severity\":\"$severity\",\"type\":\"$type\",\"file\":\"$file\",\"line\":$line,\"description\":\"$description\",\"recommendation\":\"$recommendation\"}"
    FINDINGS+=("$finding")
    
    case $severity in
        critical) CRITICAL=$((CRITICAL + 1)) ;;
        high) HIGH=$((HIGH + 1)) ;;
        medium) MEDIUM=$((MEDIUM + 1)) ;;
        low) LOW=$((LOW + 1)) ;;
        info) INFO=$((INFO + 1)) ;;
    esac
    
    if [[ "$VERBOSE" == true ]]; then
        local color=$NC
        case $severity in
            critical) color=$RED ;;
            high) color=$RED ;;
            medium) color=$YELLOW ;;
        esac
        echo -e "${color}[$severity] $type: $description${NC}"
        echo "  File: $file:$line"
        echo "  Recommendation: $recommendation"
        echo ""
    fi
}

# Check 1: SKILL.md exists
if [[ ! -f "$TARGET_SKILL/SKILL.md" ]]; then
    add_finding "high" "structure" "SKILL.md" 0 "SKILL.md not found" "Create SKILL.md with proper documentation"
else
    [[ "$VERBOSE" == true ]] && echo -e "${GREEN}✅ SKILL.md exists${NC}"
fi

# Check 2: Secrets detection (if enabled)
if [[ "$SCAN_TYPES" == "all" ]] || [[ "$SCAN_TYPES" == *"secrets"* ]]; then
    [[ "$VERBOSE" == true ]] && echo "Scanning for secrets..."
    
    # Patterns to check
    PATTERNS=(
        "api[_-]?key.*=.*['\"][a-zA-Z0-9]{16,}['\"]"
        "password.*=.*['\"][^'\"]+['\"]"
        "token.*=.*['\"][a-zA-Z0-9]{20,}['\"]"
        "secret.*=.*['\"][a-zA-Z0-9]{16,}['\"]"
        "private[_-]?key"
        "AKIA[0-9A-Z]{16}"
        "ghp_[a-zA-Z0-9]{36}"
    )
    
    for pattern in "${PATTERNS[@]}"; do
        while IFS= read -r match; do
            if [[ -n "$match" ]]; then
                file=$(echo "$match" | cut -d: -f1)
                # Skip the audit script itself (it contains the patterns)
                if [[ "$file" == *"audit-skill.sh" ]] || [[ "$file" == *"quick-scan.sh" ]]; then
                    continue
                fi
                line=$(echo "$match" | cut -d: -f2)
                add_finding "critical" "secrets" "$file" "$line" "Potential hardcoded secret detected" "Move secrets to environment variables or secure vault"
            fi
        done < <(grep -rn -E "$pattern" "$TARGET_SKILL" --include="*.js" --include="*.ts" --include="*.sh" --include="*.json" 2>/dev/null || true)
    done
fi

# Check 3: Injection vulnerabilities (if enabled)
if [[ "$SCAN_TYPES" == "all" ]] || [[ "$SCAN_TYPES" == *"injection"* ]]; then
    [[ "$VERBOSE" == true ]] && echo "Scanning for injection vulnerabilities..."
    
    # Check for eval
    while IFS= read -r match; do
        if [[ -n "$match" ]]; then
            file=$(echo "$match" | cut -d: -f1)
            line=$(echo "$match" | cut -d: -f2)
            add_finding "high" "injection" "$file" "$line" "eval() detected - potential code injection" "Avoid eval(), use safer alternatives"
        fi
    done < <(grep -rn "eval(" "$TARGET_SKILL" --include="*.js" --include="*.ts" 2>/dev/null || true)
    
    # Check for unsafe exec
    while IFS= read -r match; do
        if [[ -n "$match" ]]; then
            file=$(echo "$match" | cut -d: -f1)
            line=$(echo "$match" | cut -d: -f2)
            add_finding "medium" "injection" "$file" "$line" "Child process execution detected" "Validate and sanitize all inputs to shell commands"
        fi
    done < <(grep -rn "exec\|execFile\|spawn" "$TARGET_SKILL" --include="*.js" --include="*.ts" 2>/dev/null | grep -v "node_modules" || true)
fi

# Check 4: File permissions (if enabled)
if [[ "$SCAN_TYPES" == "all" ]] || [[ "$SCAN_TYPES" == *"permissions"* ]]; then
    [[ "$VERBOSE" == true ]] && echo "Checking file permissions..."
    
    # Check for world-writable files
    while IFS= read -r file; do
        if [[ -n "$file" ]]; then
            add_finding "medium" "permissions" "$file" 0 "World-writable file detected" "Remove world-write permission: chmod o-w $file"
        fi
    done < <(find "$TARGET_SKILL" -type f -perm -002 2>/dev/null | grep -v ".git" || true)
fi

# Check 5: Insecure HTTP URLs (if enabled)
if [[ "$SCAN_TYPES" == "all" ]] || [[ "$SCAN_TYPES" == *"network"* ]]; then
    [[ "$VERBOSE" == true ]] && echo "Checking network security..."
    
    while IFS= read -r match; do
        if [[ -n "$match" ]]; then
            file=$(echo "$match" | cut -d: -f1)
            line=$(echo "$match" | cut -d: -f2)
            add_finding "low" "network" "$file" "$line" "Insecure HTTP URL detected" "Use HTTPS instead of HTTP"
        fi
    done < <(grep -rn "http://" "$TARGET_SKILL" --include="*.js" --include="*.ts" --include="*.sh" --include="*.md" 2>/dev/null | grep -v "localhost" | grep -v "127.0.0.1" || true)
fi

# Check 6: Dependency check (if package.json exists)
if [[ "$SCAN_TYPES" == "all" ]] || [[ "$SCAN_TYPES" == *"dependencies"* ]]; then
    if [[ -f "$TARGET_SKILL/package.json" ]]; then
        [[ "$VERBOSE" == true ]] && echo "Checking dependencies..."
        
        # Check for suspicious packages
        SUSPICIOUS_PKGS=("eval" "child_process" "vm")
        for pkg in "${SUSPICIOUS_PKGS[@]}"; do
            if grep -q "$pkg" "$TARGET_SKILL/package.json" 2>/dev/null; then
                add_finding "medium" "dependencies" "package.json" 0 "Potentially dangerous dependency: $pkg" "Review if this dependency is necessary"
            fi
        done
    fi
fi

# Determine pass/fail
PASSED="false"
if [[ $CRITICAL -eq 0 && $HIGH -eq 0 ]]; then
    PASSED="true"
fi

# Generate JSON report
JSON_FINDINGS=$(printf '%s\n' "${FINDINGS[@]}" | paste -sd, -)

cat > "$REPORT_FILE" << EOF
{
  "audit_id": "$AUDIT_ID",
  "skill": "$SKILL_NAME",
  "timestamp": "$TIMESTAMP",
  "summary": {
    "critical": $CRITICAL,
    "high": $HIGH,
    "medium": $MEDIUM,
    "low": $LOW,
    "info": $INFO
  },
  "findings": [$JSON_FINDINGS],
  "passed": $PASSED,
  "recommendations": [
    "Review all findings above medium severity",
    "Fix critical and high severity issues before release",
    "Consider addressing medium severity issues"
  ]
}
EOF

# Also copy to output file if specified
if [[ -n "$OUTPUT_FILE" ]]; then
    cp "$REPORT_FILE" "$OUTPUT_FILE"
fi

# Print summary
echo ""
echo "================================"
echo "Audit Summary for $SKILL_NAME"
echo "================================"
echo "Critical: $CRITICAL"
echo "High: $HIGH"
echo "Medium: $MEDIUM"
echo "Low: $LOW"
echo "Info: $INFO"
echo ""

if [[ "$PASSED" == "true" ]]; then
    echo -e "${GREEN}✅ Audit PASSED${NC}"
else
    echo -e "${RED}❌ Audit FAILED${NC}"
    echo "Please address critical and high severity findings"
fi

echo ""
echo -e "${BLUE}📄 Report saved: $REPORT_FILE${NC}"
[[ -n "$OUTPUT_FILE" ]] && echo -e "${BLUE}📄 Output copied: $OUTPUT_FILE${NC}"

exit $([[ "$PASSED" == "true" ]] && echo 0 || echo 1)