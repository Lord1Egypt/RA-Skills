---
name: skill4agent
description: Use this skill when you need to search, read, and install skills from the online skill library. Support by Chinese.
requirements:
  - node.js: ">=16.0.0"
  - npm: "*"
  - npx: "*"
external_dependencies:
  - npm: https://www.npmjs.com/package/skill4agent
  - api: https://skill4agent.com/api
source: https://www.skill4agent.com
---

## Skill Purpose
Use CLI commands or API interfaces provided by the skill4agent platform to implement a complete workflow for searching skills, reading skill details, and installing skills.

## Usage Options
This skill provides two mutually exclusive usage options:
1. **CLI Option**: Requires Node.js environment, uses `npx skill4agent` commands
2. **API Option**: No external dependencies, uses direct HTTPS requests to skill4agent.com

Choose one option based on the available environment. If Node.js is available, prefer the CLI option for convenience. If Node.js is not available, use the API option.

## Three Core Operations

### 1. Search Skills (search)
**Purpose**: Find relevant skills using Chinese, English, or mixed Chinese-English keywords

#### CLI Command (requires Node.js environment)
```bash
# Basic search (recommended to use -j for JSON format output)
npx skill4agent search <keyword> -j

# Control the number of returned results (recommended to use -j for JSON format output)
npx skill4agent search <keyword> -j -l <number>
```

#### API Interface
```
https://skill4agent.com/api/search?keyword=<keyword>
```

**Parameter Description**:
- `keyword` (required): Search keyword (supports Chinese, English, or mixed Chinese-English)
- `limit` (optional): Number of returned results, default 10, maximum 50

**Important Return Fields**:
- `skillId`: Skill ID
- `source`: Skill source repository
- `skill_name`: Skill name
- `description`: Skill description
- `tags`: Skill tags
- `totalInstalls`: Number of installations
- `read_skill_url`: Skill detail URL
- `download_zip_url`: Skill download URL
- `translation`: Translation information (original language, whether translation is available, translated language)
- `script`: Script check information (whether scripts are included, whether sensitive code exists, specific locations of sensitive code)

### 2. Read Skills (read)
**Purpose**: View detailed information and complete content of skill (SKILL.md)

#### CLI Command (requires Node.js environment)
```bash
# Read original content (recommended to use -j for JSON format output)
npx skill4agent read <source> <skill_name> -j

# Read translated content (recommended to use -j for JSON format output)
npx skill4agent read <source> <skill_name> --type translated -j
```

#### API Interface
```
https://skill4agent.com/api/skills/info?source=<source>&skill_name=<skill_name>
```

**Parameter Description**:
- `source` (required): Skill source repository (obtained from search results)
- `skill_name` (required): Skill name (obtained from search results)
- `type` (optional): Content type (`original`/`translated`), default `original`

**Important Return Fields**:
- `skillId`: Skill ID
- `source`: Skill source repository
- `skill_name`: Skill name
- `download_zip_url`: Skill download URL
- `translation`: Translation information (original language, whether translation is available, translated language)
- `script`: Script check information (whether scripts are included, whether sensitive code exists, specific locations of sensitive code)
- `content`: Detailed skill content (complete content of SKILL.md)

### 3. Install Skills (install)
**Purpose**: Install skills to local projects

#### CLI Command (requires Node.js environment)
```bash
# Install original skill
npx skill4agent install <source> <skill_name>

# Install translated skill
npx skill4agent install <source> <skill_name> --type translated
```

#### API Interface
```
https://skill4agent.com/api/download/<skillId>?type=<type>
```

**Parameter Description**:
- `skillId` (required): Skill ID (obtained from search results or skill detail information)
- `type` (optional): Content type (`original`/`translated`), default `original`

#### Installation Instructions
- CLI command: Installs to `.agents/skills/<skill_name>` directory under the current directory
- API interface: Download ZIP file and extract to get `<skill_name>` directory
- To install the skill to other paths (e.g., user-specified or application-required paths), move the skill directory to the target location manually

## Script Security Check
Use the returned `script` field to check whether the skill contains scripts and whether sensitive code exists.

- `has_script`: `true` means the skill contains scripts
- `script_check_result`:
  - `safe`: Script is safe
  - `need attention`: Contains sensitive code
- `script_check_notes`: Specific locations of sensitive code, need to recheck after installation

**Note**: For skills that contain scripts with sensitive code, you must obtain user consent before installation. After installation, recheck the sensitive code locations listed in `script_check_notes` along with the code context to ensure there are no risks of malicious programs, unauthorized access to user private information, modification or deletion of local files, or changes to system configurations.

## Scenario-based Workflows

### Scenario 1: Only understand related skills
- **Action**: Use keywords to search for relevant skills
- **Output**: Summarize search results and wait for user's further instructions

### Scenario 2: Find suitable skills to complete tasks
1. **Search**: Use keywords to search for relevant skills
2. **Filter**: Preliminary filtering based on `description`, `tags`, and `totalInstalls`
3. **Read**: View detailed information about candidate skills, analyze whether the skill meets the task requirements
4. **Recommend**: Recommend the most suitable skills to users (if the skill contains scripts with sensitive code, you must inform the user)

### Scenario 3: Search and install skills
1. **Search**: Use keywords to search for relevant skills
2. **Filter**: Filter suitable skills based on search results
3. **Read** (if needed): Further understand skill details, analyze whether the skill meets the task requirements
4. **Install**: Install the skill to the required directory (for skills containing scripts with sensitive code, do NOT install without user consent - you must obtain user consent before installing)
5. **Script Security Recheck**: If the skill contains scripts with sensitive code, recheck the sensitive code locations listed in `script_check_notes` along with the code context after installation to ensure there are no risks of malicious programs, unauthorized access to user private information, modification or deletion of local files, or changes to system configurations.

## Search Optimization Suggestions
When no results are found:
1. **Optimize keywords**: Use more general or concise keywords
2. **Switch language**:
   - If English search returns no results → Try Chinese or mixed Chinese-English keywords
   - If Chinese search returns no results → Try English or mixed Chinese-English keywords

## Best Practices
- **JSON Format**: Always add `-j` parameter to search and read commands to return JSON format output for easier parsing
- **Language Version Selection**: Choose appropriate version based on user's preferred language (check original and translated languages via `translation` field)
