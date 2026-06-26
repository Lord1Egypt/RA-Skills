#!/bin/bash
#
# uniapp-vue-analyzer - Smart Project Analysis Tool
# Supports uni-app and Vue projects
# Cross-platform version for Linux/macOS
#

set -e

# Default values
PROJECT_PATH="."
PROJECT_NAME=""
PROJECT_TYPE="auto"
OUTPUT_DIR=""
PREVIEW=false
SKIP_CONFIRM=false
CUSTOM_CONFIG=""
MAX_FILE_SIZE=0
SAVE_CONFIG=false
DEEP_ANALYSIS=false
HELP=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
DARK_GRAY='\033[1;30m'
NC='\033[0m' # No Color

# Show help
show_help() {
    cat << EOF
${CYAN}uniapp-vue-analyzer - Smart Project Analysis Tool${NC}

Usage:
  ./analyze-project.sh [options]

Options:
  -p, --project-path    Project path (default: current directory)
  -n, --project-name    Project name (default: directory name)
  -t, --project-type    Project type: auto|uniapp|vue (default: auto)
  -o, --output-dir      Output directory (default: ./analysis-output)
  --preview             Preview files to be analyzed without running analysis
  -y, --yes             Skip confirmation prompt
  -c, --custom-config   Path to custom configuration file
  --max-file-size       Max file size in MB (default: 1)
  --save-config         Save current settings as user default
  -d, --deep-analysis   Enable deep analysis with manifest/pages.json parsing
  -h, --help            Show this help message

Examples:
  # Analyze current directory (auto-detect type)
  ./analyze-project.sh

  # Analyze specific uni-app project
  ./analyze-project.sh -p /path/to/my-uniapp-project -t uniapp

  # Preview files to be analyzed
  ./analyze-project.sh -p /path/to/my-vue-project --preview

  # Enable deep analysis
  ./analyze-project.sh -p /path/to/project -d

  # Skip confirmation
  ./analyze-project.sh -p /path/to/project -y
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--project-path)
            PROJECT_PATH="$2"
            shift 2
            ;;
        -n|--project-name)
            PROJECT_NAME="$2"
            shift 2
            ;;
        -t|--project-type)
            PROJECT_TYPE="$2"
            shift 2
            ;;
        -o|--output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --preview)
            PREVIEW=true
            shift
            ;;
        -y|--yes)
            SKIP_CONFIRM=true
            shift
            ;;
        -c|--custom-config)
            CUSTOM_CONFIG="$2"
            shift 2
            ;;
        --max-file-size)
            MAX_FILE_SIZE="$2"
            shift 2
            ;;
        --save-config)
            SAVE_CONFIG=true
            shift
            ;;
        -d|--deep-analysis)
            DEEP_ANALYSIS=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR/config"

# Check skill-seekers availability
check_skill_seekers() {
    if command -v skill-seekers &> /dev/null; then
        echo "skill-seekers"
        return 0
    fi
    
    # Check common paths
    local paths=(
        "$HOME/.local/bin/skill-seekers"
        "$HOME/.pyenv/shims/skill-seekers"
        "/usr/local/bin/skill-seekers"
        "/opt/homebrew/bin/skill-seekers"
    )
    
    for path in "${paths[@]}"; do
        if [[ -x "$path" ]]; then
            echo "$path"
            return 0
        fi
    done
    
    return 1
}

# Install skill-seekers
install_skill_seekers() {
    echo ""
    echo -e "${YELLOW}skill-seekers is not installed.${NC}"
    echo ""
    echo -e "${CYAN}To install skill-seekers, run one of the following commands:${NC}"
    echo ""
    echo -e "${GRAY}  # Using pip (requires Python)${NC}"
    echo "  pip install skill-seekers"
    echo ""
    echo -e "${GRAY}  # Or with specific Python version${NC}"
    echo "  python3 -m pip install skill-seekers"
    echo ""
    
    if [[ "$SKIP_CONFIRM" == false ]]; then
        read -p "Would you like to attempt automatic installation? (y/N) " response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Attempting to install skill-seekers...${NC}"
            if pip install skill-seekers 2>/dev/null || python3 -m pip install skill-seekers 2>/dev/null; then
                echo -e "${GREEN}skill-seekers installed successfully!${NC}"
                return 0
            else
                echo -e "${RED}Automatic installation failed. Please install manually.${NC}"
                return 1
            fi
        fi
    fi
    
    return 1
}

# Check for skill-seekers
SKILL_SEEKERS_PATH=$(check_skill_seekers)
if [[ -z "$SKILL_SEEKERS_PATH" ]]; then
    if ! install_skill_seekers; then
        echo ""
        echo -e "${RED}Error: skill-seekers is required but not installed.${NC}"
        echo -e "${YELLOW}Please install it manually and try again.${NC}"
        exit 1
    fi
    SKILL_SEEKERS_PATH=$(check_skill_seekers)
fi

echo -e "${GRAY}Using skill-seekers: $SKILL_SEEKERS_PATH${NC}"

# Resolve project path
PROJECT_PATH=$(cd "$PROJECT_PATH" && pwd)
if [[ ! -d "$PROJECT_PATH" ]]; then
    echo -e "${RED}Error: Project path does not exist: $PROJECT_PATH${NC}"
    exit 1
fi

# Set default output directory
if [[ -z "$OUTPUT_DIR" ]]; then
    OUTPUT_DIR="$PROJECT_PATH/analysis-output"
fi

# Set default project name
if [[ -z "$PROJECT_NAME" ]]; then
    PROJECT_NAME=$(basename "$PROJECT_PATH")
fi

echo ""
echo -e "${CYAN}Project Analyzer${NC}"
echo -e "${GRAY}========================================${NC}"
echo -e "Project Path: ${WHITE}$PROJECT_PATH${NC}"
echo -e "Project Name: ${WHITE}$PROJECT_NAME${NC}"

# Detect project type
detect_project_type() {
    local path="$1"
    local uniapp_score=0
    local vue_score=0
    
    # Check uni-app indicators
    [[ -f "$path/manifest.json" ]] && uniapp_score=$((uniapp_score + 1))
    [[ -f "$path/pages.json" ]] && uniapp_score=$((uniapp_score + 1))
    [[ -f "$path/uni.scss" ]] && uniapp_score=$((uniapp_score + 1))
    
    # Check manifest.json content
    if [[ -f "$path/manifest.json" ]]; then
        if grep -q '"appid"\|uni-app\|dcloudio' "$path/manifest.json" 2>/dev/null; then
            uniapp_score=$((uniapp_score + 2))
        fi
    fi
    
    if [[ $uniapp_score -ge 2 ]]; then
        echo "uniapp"
        return
    fi
    
    # Check Vue indicators
    [[ -f "$path/vue.config.js" ]] && vue_score=$((vue_score + 1))
    [[ -f "$path/vite.config.js" ]] && vue_score=$((vue_score + 1))
    [[ -f "$path/vite.config.ts" ]] && vue_score=$((vue_score + 1))
    [[ -f "$path/nuxt.config.js" ]] && vue_score=$((vue_score + 1))
    [[ -f "$path/nuxt.config.ts" ]] && vue_score=$((vue_score + 1))
    
    # Check package.json
    if [[ -f "$path/package.json" ]]; then
        if grep -q '"vue"\|"@vue/' "$path/package.json" 2>/dev/null; then
            vue_score=$((vue_score + 2))
        fi
    fi
    
    # Check for Vue files in src
    if [[ -d "$path/src" ]]; then
        local vue_files=$(find "$path/src" -name "*.vue" -type f 2>/dev/null | head -5 | wc -l)
        if [[ $vue_files -gt 0 ]]; then
            vue_score=$((vue_score + 2))
        fi
    fi
    
    if [[ $vue_score -ge 2 ]]; then
        echo "vue"
        return
    fi
    
    echo "unknown"
}

# Auto-detect project type
if [[ "$PROJECT_TYPE" == "auto" ]]; then
    echo -e "${YELLOW}Detecting project type...${NC}"
    DETECTED_TYPE=$(detect_project_type "$PROJECT_PATH")
    
    if [[ "$DETECTED_TYPE" == "unknown" ]]; then
        echo -e "${YELLOW}Warning: Could not auto-detect project type, using Vue config as default${NC}"
        PROJECT_TYPE="vue"
    else
        PROJECT_TYPE="$DETECTED_TYPE"
        echo -e "${GREEN}Detected project type: $PROJECT_TYPE${NC}"
    fi
else
    echo -e "Using specified project type: ${WHITE}$PROJECT_TYPE${NC}"
fi

# Load configuration
load_config() {
    local type="$1"
    local base_config="$CONFIG_DIR/base.json"
    local type_config="$CONFIG_DIR/$type.json"
    
    # Start with base config
    if [[ -f "$base_config" ]]; then
        cat "$base_config"
    else
        echo '{}'
    fi
}

echo -e "${YELLOW}Loading configuration...${NC}"
CONFIG=$(load_config "$PROJECT_TYPE")

# Generate skill-seekers config
generate_skill_seekers_config() {
    local config="$1"
    local project_path="$2"
    local project_name="$3"
    
    # Parse exclude directories from config
    local exclude_dirs="[]"
    local exclude_files="[]"
    local exclude_patterns="[]"
    local include_extensions="[]"
    local max_file_size=1048576
    
    if command -v jq &> /dev/null; then
        exclude_dirs=$(echo "$config" | jq -c '.exclude.directories // []')
        exclude_files=$(echo "$config" | jq -c '.exclude.files // []')
        exclude_patterns=$(echo "$config" | jq -c '.exclude.patterns // []')
        include_extensions=$(echo "$config" | jq -c '.file_filters.include_extensions // []')
        max_file_size=$(echo "$config" | jq -r '.file_filters.max_file_size // 1048576')
    fi
    
    cat << EOF
{
    "name": "$project_name",
    "description": "$PROJECT_TYPE project: $project_name",
    "base_path": "$project_path",
    "exclude": {
        "directories": $exclude_dirs,
        "files": $exclude_files,
        "patterns": $exclude_patterns
    },
    "file_filters": {
        "max_file_size": $max_file_size,
        "min_file_size": 10,
        "include_extensions": $include_extensions
    },
    "analysis_options": {
        "include_tests": false,
        "include_docs": true,
        "include_config": true,
        "max_files": 1000,
        "max_depth": 10
    }
}
EOF
}

# Generate config
SKILL_SEEKERS_CONFIG=$(generate_skill_seekers_config "$CONFIG" "$PROJECT_PATH" "$PROJECT_NAME")

# Save temporary config (with restricted permissions)
TEMP_CONFIG=$(mktemp /tmp/project-analyzer-XXXXXX.json)
chmod 600 "$TEMP_CONFIG"  # Restrict permissions to owner only
echo "$SKILL_SEEKERS_CONFIG" > "$TEMP_CONFIG"

echo -e "${GREEN}Configuration loaded${NC}"
echo ""

# Show exclusion summary
echo -e "${CYAN}Exclusion Rules Summary${NC}"
echo -e "${GRAY}========================================${NC}"

if command -v jq &> /dev/null; then
    local exclude_dirs_count=$(echo "$SKILL_SEEKERS_CONFIG" | jq '.exclude.directories | length')
    local exclude_patterns_count=$(echo "$SKILL_SEEKERS_CONFIG" | jq '.exclude.patterns | length')
    local include_extensions_count=$(echo "$SKILL_SEEKERS_CONFIG" | jq '.file_filters.include_extensions | length')
    
    echo -e "Excluded directories: ${GRAY}$exclude_dirs_count${NC}"
    echo -e "Excluded patterns: ${GRAY}$exclude_patterns_count${NC}"
    echo -e "Included extensions: ${GRAY}$include_extensions_count types${NC}"
fi

echo ""

# Preview mode
if [[ "$PREVIEW" == true ]]; then
    echo -e "${CYAN}Preview Mode - Files to be analyzed${NC}"
    echo -e "${GRAY}========================================${NC}"
    
    # Create temp directory for preview
    TEMP_DIR=$(mktemp -d /tmp/project-analyzer-preview-XXXXXX)
    
    # Copy files (apply exclusion rules)
    if command -v jq &> /dev/null; then
        exclude_list=$(echo "$SKILL_SEEKERS_CONFIG" | jq -r '.exclude.directories[]')
        
        for item in "$PROJECT_PATH"/*; do
            local item_name=$(basename "$item")
            local exclude=false
            
            while IFS= read -r dir; do
                if [[ "$item_name" == "$dir" ]]; then
                    exclude=true
                    break
                fi
            done <<< "$exclude_list"
            
            if [[ "$exclude" == false ]]; then
                if [[ -d "$item" ]]; then
                    cp -r "$item" "$TEMP_DIR/"
                else
                    cp "$item" "$TEMP_DIR/"
                fi
            fi
        done
        
        # Count files
        local include_exts=$(echo "$SKILL_SEEKERS_CONFIG" | jq -r '.file_filters.include_extensions[]')
        local file_count=0
        local total_size=0
        
        while IFS= read -r ext; do
            local files=$(find "$TEMP_DIR" -name "*$ext" -type f 2>/dev/null)
            for file in $files; do
                if [[ -f "$file" ]]; then
                    file_count=$((file_count + 1))
                    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
                    total_size=$((total_size + size))
                fi
            done
        done <<< "$include_exts"
        
        echo -e "${GREEN}Preview Statistics${NC}"
        echo -e "   File count: ${WHITE}$file_count${NC}"
        echo -e "   Total size: ${WHITE}$(echo "scale=2; $total_size / 1024" | bc) KB${NC}"
        echo ""
    fi
    
    # Cleanup
    rm -rf "$TEMP_DIR"
    rm -f "$TEMP_CONFIG"
    
    echo -e "${GREEN}Preview complete${NC}"
    echo -e "${YELLOW}Tip: Remove --preview flag to run actual analysis${NC}"
    exit 0
fi

# Confirmation prompt
if [[ "$SKIP_CONFIRM" == false ]]; then
    echo ""
    read -p "Start analysis? (y/n) " confirmation
    if [[ ! "$confirmation" =~ ^[Yy]$ ]]; then
        echo -e "${RED}Analysis cancelled${NC}"
        rm -f "$TEMP_CONFIG"
        exit 0
    fi
fi

# Execute analysis
echo ""
echo -e "${GREEN}Starting project analysis...${NC}"
echo -e "${GRAY}========================================${NC}"

# Create temp directory
TEMP_DIR=$(mktemp -d /tmp/project-analyzer-XXXXXX)

cleanup() {
    rm -rf "$TEMP_DIR"
    rm -f "$TEMP_CONFIG"
}
trap cleanup EXIT

# Copy project files
echo -e "${YELLOW}Copying project files...${NC}"

if command -v jq &> /dev/null; then
    exclude_list=$(echo "$SKILL_SEEKERS_CONFIG" | jq -r '.exclude.directories[]')
    
    for item in "$PROJECT_PATH"/*; do
        local item_name=$(basename "$item")
        local exclude=false
        
        while IFS= read -r dir; do
            if [[ "$item_name" == "$dir" ]]; then
                exclude=true
                break
            fi
        done <<< "$exclude_list"
        
        if [[ "$exclude" == false ]]; then
            if [[ -d "$item" ]]; then
                cp -r "$item" "$TEMP_DIR/"
            else
                cp "$item" "$TEMP_DIR/"
            fi
        fi
    done
fi

# Process Vue files for skill-seekers compatibility
echo -e "${YELLOW}Processing Vue files for compatibility...${NC}"
declare -A VUE_FILE_MAP

while IFS= read -r -d '' vue_file; do
    local new_name="${vue_file}.js"
    mv "$vue_file" "$new_name"
    VUE_FILE_MAP["$new_name"]="$vue_file"
    local basename=$(basename "$vue_file")
    echo -e "  Renamed: ${GRAY}$basename -> $basename.js${NC}"
done < <(find "$TEMP_DIR" -name "*.vue" -type f -print0 2>/dev/null)

# Run skill-seekers analysis
echo -e "${YELLOW}Running skill-seekers analysis...${NC}"

OUTPUT_PATH="$OUTPUT_DIR/$PROJECT_NAME"
mkdir -p "$OUTPUT_PATH"

if $SKILL_SEEKERS_PATH analyze \
    --directory "$TEMP_DIR" \
    --output "$OUTPUT_PATH" \
    --name "$PROJECT_NAME" \
    --description "$PROJECT_TYPE project: $PROJECT_NAME"; then
    
    echo ""
    echo -e "${GREEN}Analysis complete!${NC}"
    echo -e "Output directory: ${CYAN}$OUTPUT_PATH${NC}"
    echo ""
    echo -e "${WHITE}Generated files:${NC}"
    
    [[ -f "$OUTPUT_PATH/SKILL.md" ]] && echo -e "   - ${GRAY}SKILL.md (Project skill documentation)${NC}"
    [[ -f "$OUTPUT_PATH/code_analysis.json" ]] && echo -e "   - ${GRAY}code_analysis.json (Code analysis data)${NC}"
    
    # Fix Vue file references (with proper escaping to prevent command injection)
    if [[ -f "$OUTPUT_PATH/code_analysis.json" ]] && [[ ${#VUE_FILE_MAP[@]} -gt 0 ]]; then
        for renamed in "${!VUE_FILE_MAP[@]}"; do
            local original="${VUE_FILE_MAP[$renamed]}"
            local rel_renamed=$(basename "$renamed")
            local rel_original=$(basename "$original")
            # Escape special characters for sed (prevent command injection)
            local escaped_renamed=$(printf '%s' "$rel_renamed" | sed 's/[[\.*^$+?{|}\[\]()\\]/\\&/g')
            local escaped_original=$(printf '%s' "$rel_original" | sed 's/[[\.*^$+?{|}\[\]()\\]/\\&/g')
            # Use # as delimiter to avoid issues with | in filenames
            sed -i '' "s#${escaped_renamed}#${escaped_original}#g" "$OUTPUT_PATH/code_analysis.json" 2>/dev/null || \
            sed -i "s#${escaped_renamed}#${escaped_original}#g" "$OUTPUT_PATH/code_analysis.json" 2>/dev/null || true
        done
        echo -e "   - ${GRAY}Fixed Vue file references in code_analysis.json${NC}"
    fi
    
    if [[ -d "$OUTPUT_PATH/references" ]]; then
        local ref_count=$(find "$OUTPUT_PATH/references" -type f | wc -l)
        echo -e "   - ${GRAY}references/ (Reference docs, $ref_count files)${NC}"
    fi
else
    echo ""
    echo -e "${RED}Analysis failed, please check error messages${NC}"
    exit 1
fi

# Deep Analysis
if [[ "$DEEP_ANALYSIS" == true ]]; then
    echo ""
    echo -e "${YELLOW}Running deep analysis...${NC}"
    
    PROJECT_METADATA="{}"
    
    if [[ "$PROJECT_TYPE" == "uniapp" ]]; then
        # Parse manifest.json
        if [[ -f "$PROJECT_PATH/manifest.json" ]]; then
            if command -v jq &> /dev/null; then
                PROJECT_METADATA=$(echo "$PROJECT_METADATA" | jq \
                    --arg name "$(jq -r '.name // empty' "$PROJECT_PATH/manifest.json" 2>/dev/null)" \
                    --arg appid "$(jq -r '.id // empty' "$PROJECT_PATH/manifest.json" 2>/dev/null)" \
                    --arg version "$(jq -r '.versionName // empty' "$PROJECT_PATH/manifest.json" 2>/dev/null)" \
                    '.name = $name | .appid = $appid | .version = $version')
                echo -e "  ${GRAY}Parsed manifest.json${NC}"
            fi
        fi
        
        # Parse pages.json
        if [[ -f "$PROJECT_PATH/pages.json" ]]; then
            if command -v jq &> /dev/null; then
                # Remove comments (both // and /* */) and parse
                local pages_content=$(sed -e 's|//.*||g' -e ':a;N;$!ba;s|/\*.*?\*/||g' "$PROJECT_PATH/pages.json" | jq -c '.pages // []' 2>/dev/null)
                PROJECT_METADATA=$(echo "$PROJECT_METADATA" | jq --argjson pages "$pages_content" '.pages = $pages')
                echo -e "  ${GRAY}Parsed pages.json${NC}"
            fi
        fi
    elif [[ "$PROJECT_TYPE" == "vue" ]]; then
        # Parse package.json
        if [[ -f "$PROJECT_PATH/package.json" ]]; then
            if command -v jq &> /dev/null; then
                PROJECT_METADATA=$(echo "$PROJECT_METADATA" | jq \
                    --arg name "$(jq -r '.name // empty' "$PROJECT_PATH/package.json" 2>/dev/null)" \
                    --arg version "$(jq -r '.version // empty' "$PROJECT_PATH/package.json" 2>/dev/null)" \
                    --arg description "$(jq -r '.description // empty' "$PROJECT_PATH/package.json" 2>/dev/null)" \
                    --arg vue_version "$(jq -r '.dependencies.vue // empty' "$PROJECT_PATH/package.json" 2>/dev/null)" \
                    '.name = $name | .version = $version | .description = $description | .vueVersion = $vue_version')
                
                # Detect build tool
                if jq -e '.devDependencies.vite' "$PROJECT_PATH/package.json" &>/dev/null; then
                    PROJECT_METADATA=$(echo "$PROJECT_METADATA" | jq '.buildTool = "Vite"')
                elif jq -e '.devDependencies.webpack' "$PROJECT_PATH/package.json" &>/dev/null; then
                    PROJECT_METADATA=$(echo "$PROJECT_METADATA" | jq '.buildTool = "Webpack"')
                elif jq -e '.devDependencies."@vue/cli-service"' "$PROJECT_PATH/package.json" &>/dev/null; then
                    PROJECT_METADATA=$(echo "$PROJECT_METADATA" | jq '.buildTool = "Vue CLI"')
                fi
                
                echo -e "  ${GRAY}Parsed package.json${NC}"
            fi
        fi
        
        # Parse router
        for router_path in "$PROJECT_PATH/src/router/index.js" "$PROJECT_PATH/src/router/index.ts" \
                          "$PROJECT_PATH/router/index.js" "$PROJECT_PATH/router/index.ts"; do
            if [[ -f "$router_path" ]]; then
                # 使用数组收集路由，兼容无 jq 环境
                local routes_json="[]"
                if command -v jq &> /dev/null; then
                    routes_json=$(grep -oE 'path\s*:\s*["\'\'']([^"\'\'']+)["\'\''']' "$router_path" 2>/dev/null | sed 's/.*["\'\''']\([^"\'\''']*\)["\'\'''].*/\1/' | jq -R . | jq -s .)
                else
                    # 无 jq 时的简单处理：提取所有路径
                    local temp_routes=$(grep -oE 'path\s*:\s*["\'\'']([^"\'\'']+)["\'\''']' "$router_path" 2>/dev/null | sed "s/.*['\'']\([^'\'']*\)['\'].*/\1/" || true)
                    if [[ -n "$temp_routes" ]]; then
                        routes_json="[$(echo "$temp_routes" | tr '\n' ',' | sed 's/,$//' | sed "s/^\(.*\)/\"\\1\"/" | tr '\n' ',')]"
                        routes_json=$(echo "$routes_json" | sed 's/,\]/]/g')
                    fi
                fi
                if [[ -n "$routes_json" ]] && [[ "$routes_json" != "[]" ]]; then
                    if command -v jq &> /dev/null; then
                        PROJECT_METADATA=$(echo "$PROJECT_METADATA" | jq --argjson routes "$routes_json" '.routes = $routes | .routeCount = ($routes | length)')
                    fi
                    echo -e "  ${GRAY}Parsed router configuration${NC}"
                    break
                fi
            fi
        done
    fi
    
    # Save metadata
    if [[ "$PROJECT_METADATA" != "{}" ]]; then
        echo "$PROJECT_METADATA" | jq . > "$OUTPUT_PATH/project_metadata.json"
        echo -e "  ${GRAY}Saved project metadata${NC}"
    fi
fi

# Run code quality analysis
echo ""
echo -e "${YELLOW}Running code quality analysis...${NC}"
QUALITY_ANALYZER="$SCRIPT_DIR/scripts/code-quality-analyzer.sh"
if [[ -f "$QUALITY_ANALYZER" ]]; then
    if bash "$QUALITY_ANALYZER" "$PROJECT_PATH" "$OUTPUT_PATH" "$PROJECT_TYPE" 2>/dev/null; then
        echo -e "  ${GRAY}Code quality report saved${NC}"
    else
        echo -e "  ${YELLOW}Warning: Code quality analysis failed${NC}"
    fi
else
    echo -e "  ${GRAY}Code quality analyzer not found (optional)${NC}"
fi

echo ""
echo -e "${GREEN}All analyses complete!${NC}"
echo -e "Results saved to: ${CYAN}$OUTPUT_PATH${NC}"
