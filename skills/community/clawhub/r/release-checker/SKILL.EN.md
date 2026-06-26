---
name: release-checker
description: "All-in-one release compatibility checking tool. Automatically analyzes Git diff to detect release compatibility, intelligently identifies Push Center/Gateway/Configuration changes through code analysis, automatically detects SQL script compatibility and generates multi-database versions, outputs complete TODO list and Markdown report."
category: development
risk: safe
source: custom
date_added: "2026-04-07"
author: user
tags: [release, compatibility, java, sql, dml, ddl, config, git-diff, multi-db, mybatis, push-center, Gateway, nacos]
tools: [git, python, glob, grep, read, write, bash]
compatibility: opencode
---

# Release Checker - All-in-One Release Compatibility Tool

## Overview

**Fully automated release compatibility checking tool**, integrating the following core features:

1. **Git Diff Analysis** - Automatically analyzes changed files and categorizes statistics
2. **Intelligent Component Recognition** - Automatically identifies Push Center, Gateway, and Configuration changes through code content analysis
3. **Release Component Confirmation** - Combines automatic recognition results for final user confirmation
4. **SQL Compatibility Check** - Detects MySQL/PostgreSQL/Oracle compatibility issues
5. **SQL Multi-Database Conversion** - Built-in conversion logic to transform MySQL SQL to PostgreSQL/Oracle versions
6. **TODO List Confirmation** - Generates complete to-do list and obtains final user confirmation
7. **Markdown Report Generation** - Outputs comprehensive release compatibility report

Applicable to:
- **MyBatis-Plus Projects** (SQL in code)
- **Spring Cloud Projects** (Feign calls, Nacos configuration)
- **Traditional Java Projects** (Java code + SQL scripts)
- **Multi-Database Projects** (MySQL/PostgreSQL/Oracle)

## When to Use This Skill

- Use when user says "check release compatibility", "release check", or "发版检查"
- Use when user wants to analyze code and script changes in git diff
- Use when user needs to generate release TODO list
- Use when user needs to generate Markdown format compatibility report
- Use when user needs to convert MySQL SQL to multi-database versions
- **Do not** use for general code review; use appropriate code review skills instead

## How It Works

### Mode Detection

Before execution, first determine whether it's single-project or batch mode:

- **Single-Project Mode**: User provides a single project path and comparison branch
- **Batch Mode**: User provides multiple project paths, or uses configuration file

### Step 1: Git Diff Analysis (Automatic)

**Single-Project Mode:**
Execute `git diff <base-branch>..HEAD --name-only` to get all changed files.

**Batch Mode:**
Execute git diff analysis for each project in parallel, collecting change information from all projects.

Identifies:
- Changed Java files (added/modified/deleted)
- Changed SQL scripts (DML/DDL)
- Changed configuration files (yml/properties)
- Changed MyBatis Mapper XML files

### Step 2: Intelligent Component Recognition (Automatic)

**This step automatically detects the following components through code content analysis:**

#### 2.1 Push Center Configuration Recognition

Detects whether changed Java files contain the following content:

- **Push-related logs/comments**: Contains keywords like "推送", "push", "spush", "发送消息", etc.
- **EVENT definitions**: Classes with `extends ApplicationEvent` or `@EventListener`, and class name contains "Push" or related terms
- **Push Feign calls**: Contains `@FeignClient` annotation, and value or url contains "push", "spush" keywords

Detection patterns:
```
// Log/comment detection
推送|push|spush|发送消息|消息推送

// EVENT detection
extends ApplicationEvent
@EventListener
*PushEvent*
*Push*Event*

// Feign detection
@FeignClient.*[Pp]ush
value.*=.*"\$\{[^}]*push
url.*=.*"\$\{[^}]*push
```

If related files are detected, display "Push Center related changes automatically detected" during subsequent user confirmation.

#### 2.2 Gateway Configuration Recognition

Detects whether changed Java files contain the following content:

- **New Feign definitions**: Interfaces with `@FeignClient` annotation
- **Service name through annotation**: value attribute uses `${openfeign.xxx.name:}` format
- **Service name contains spush**: Detects `spush` or similar push service names

Detection patterns:
```
// Feign Client detection
@FeignClient

// Service name detection
value\s*=\s*"\$\{openfeign\.[^}]+name:
value\s*=\s*"\$\{[^}]*spush
url\s*=\s*"\$\{openfeign\.[^}]+url:
```

If new Feign definitions with service name configuration are detected, display "Gateway related changes automatically detected" during subsequent user confirmation.

#### 2.3 Configuration Change Recognition

**Detection methods:**

- **Local configuration file changes**: Detects whether yml/properties files have changes
- **Annotation-based configuration properties**: Detects whether Java files contain:
  - `@Value("${xxx}")` annotation
  - `@ConfigurationProperties` annotation
  - `@PropertySource` annotation
- **Configuration class changes**: Detects whether classes with `@Configuration` or `@Bean` have changes

Detection patterns:
```
// Configuration property injection
@Value("${

// Configuration property classes
@ConfigurationProperties

// Configuration classes
@Configuration
@Bean
```

If configuration property related code changes are detected, display "Configuration changes automatically detected (annotation/configuration class)" during subsequent user confirmation.

#### 2.4 Other Component Recognition

- **ES Changes**: Detects ES entity classes, ES annotations, ES Repository changes
- **SQL Scripts**: Detects .sql file changes
- **Dictionary Changes**: Detects enum classes, dictionary configuration class changes
- **Redis Configuration**: Detects Redis related configuration, RedisTemplate, @Cacheable, etc.
- **MQ Messages**: Detects MQ annotations, Listener, Producer related changes
- **File Storage**: Detects file upload, storage path related changes
- **API Interfaces**: Detects Controller, @RequestMapping related changes
- **Java Code**: Other Java code changes

### Step 3: Release Component Confirmation (User Interaction - Round 1)

Use Question tool, **must set multiple=true** to allow users to select multiple components at once.

Display automatic recognition results for user reference:

**options parameter**:
```json
[
  {"label": "Push Center Configuration", "description": "Push Center service related configuration changes (Auto-detected: related code found)"},
  {"label": "Gateway Configuration", "description": "Unified Gateway related configuration (Auto-detected: new Feign definition found)"},
  {"label": "ES Changes", "description": "Elasticsearch index or query changes"},
  {"label": "SQL Scripts", "description": "Database script changes (DML/DDL)"},
  {"label": "Dictionary Changes", "description": "Data dictionary or enum configuration changes"},
  {"label": "Configuration File Changes", "description": "Application configuration file changes (Auto-detected: annotation/configuration class found)"},
  {"label": "Redis Configuration", "description": "Redis cache or data structure changes"},
  {"label": "MQ Messages", "description": "Message queue topic or message format changes"},
  {"label": "File Storage", "description": "File upload, storage path changes"},
  {"label": "API Interfaces", "description": "External API interface changes"},
  {"label": "Java Code", "description": "Java code changes"}
]
```

### Step 4: SQL Conversion Inquiry (User Interaction)

**Only execute when user selects "SQL Scripts":**

#### 4.1 Ask if conversion is needed

Use Question tool to ask:

**Question**: "SQL script changes detected. Do you need to convert existing SQL scripts to multi-database versions (MySQL → PostgreSQL/Oracle)?"

**options**: 
```json
[
  {"label": "Yes, I need to generate multi-database versions", "description": "Convert MySQL SQL to PostgreSQL and Oracle versions"},
  {"label": "No, SQL scripts are ready", "description": "Already have complete multi-database SQL scripts, no conversion needed"}
]
```

#### 4.2 Ask for file path (must execute after user selects "Yes")

**⚠️ Important: This step must use Question tool, cannot be skipped, cannot use plain text inquiry.**

If user selects "Yes, I need to generate multi-database versions", **immediately use Question tool to ask for file path**:

**Question**: "Please provide the MySQL SQL file path(s) to convert (multiple files separated by comma or newline)"

**options**: 
```json
[
  {"label": "Use SQL files detected by git diff", "description": "Automatically use SQL file paths from changed files"},
  {"label": "Manually input file paths", "description": "Input the file paths to convert yourself"}
]
```

**If user selects "Use SQL files detected by git diff":**
- Automatically use SQL changed file paths detected in Step 1
- List file paths for user confirmation
- Proceed directly to Step 5 after confirmation

**If user selects "Manually input file paths":**
- Let user input file paths directly (supports multiple, separated by comma or newline)
- Example input:
  ```
  scripts/db/v1.0.0/mysql-ddl.sql,
  scripts/db/v1.0.0/mysql-dml.sql
  ```
- Proceed to Step 5 after confirmation

#### 4.3 Handling when user does not select "SQL Scripts"

If user does not select "SQL Scripts" but .sql file changes are detected in git diff:
- List detected SQL changed files
- Proactively ask: "Detected the following SQL file changes, do you need to generate multi-database versions for these files?"
- If user confirms, return to Step 4.2

### Step 5: SQL Compatibility Analysis (Python Script Automatic Execution)

Call Python script to perform compatibility analysis on detected SQL files:

```bash
python scripts/release_checker.py \
  --project <project-path> \
  --branch <comparison-branch> \
  --report <report-output-path>
```

Python script automatically detects the following compatibility issues:

| Compatibility Issue | Detection Pattern | Suggested Solution |
|---------------------|-------------------|--------------------|
| NOW() not supported | `NOW\(\)` | Use SYSTIMESTAMP (Oracle) |
| LIMIT not supported | `LIMIT \d+` | Use OFFSET...ROWS FETCH NEXT |
| IF NOT EXISTS | `IF NOT EXISTS` | Not supported by Oracle, manual handling required |
| AUTO_INCREMENT | `AUTO_INCREMENT` | Use SERIAL (PG) or SEQUENCE (Oracle) |
| ENUM type | `ENUM\(` | Use VARCHAR + CHECK |
| IFNULL | `IFNULL\(` | Use NVL or COALESCE |
| TINYINT | `TINYINT` | PostgreSQL: SMALLINT, Oracle: NUMBER(3) |
| DATETIME | `DATETIME` | PostgreSQL: TIMESTAMP, Oracle: TIMESTAMP |
| Backticks | `` ` `` | PostgreSQL/Oracle: Double quotes |

### Step 6: SQL Multi-Database Conversion (Python Script Automatic Execution)

**Execute when user selects "Yes" in Step 4.**

Call Python script `scripts/release_checker.py` for SQL conversion (using SQLGlot):

```bash
python scripts/release_checker.py --convert-sql \
  --sql-files <MySQL-SQL-file-paths> \
  --output-dir <output-directory>
```

Python script uses **SQLGlot** library for professional SQL parsing and conversion, supporting:
- MySQL → PostgreSQL conversion
- MySQL → Oracle conversion
- Automatic SEQUENCE + TRIGGER generation (Oracle auto-increment)
- Automatic conversion result validation

### Step 6.5: SQL Conversion Validation (Python Script Automatic Execution + Manual Confirmation)

**Python script automatically executes validation (10+ rules) after conversion to ensure generated SQL is executable.**

#### 6.5.1 Python Automatic Syntax Validation

After conversion, Python script automatically executes the following syntax checks (integrated in `--convert-sql` mode):

**PostgreSQL Syntax Validation Rules (10 items):**
- ✅ Backtick check
- ✅ AUTO_INCREMENT check
- ✅ ENGINE check
- ✅ NOW() function check
- ✅ IFNULL function check
- ✅ TINYINT type check
- ✅ DATETIME type check
- ✅ DEFAULT CHARSET check
- ✅ UNSIGNED check
- ✅ COMMENT syntax check

**Oracle Syntax Validation Rules (11 items):**
- ✅ Backtick check
- ✅ AUTO_INCREMENT check
- ✅ ENGINE check
- ✅ NOW() function check
- ✅ IFNULL function check
- ✅ TINYINT type check
- ✅ DATETIME type check
- ✅ IF NOT EXISTS check
- ✅ LIMIT check
- ✅ DEFAULT CHARSET check
- ✅ UNSIGNED check

Python script outputs validation result summary, showing pass/fail/warning counts.

#### 6.5.2 Manual Review Checklist

**After conversion, display the following validation reminders requiring user confirmation:**

```
┌─────────────────────────────────────────────────────────────┐
│  ⚠️  AI-generated SQL requires manual review                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Validation Checklist:                                      │
│  □ Confirm target table structure matches converted fields  │
│  □ Confirm field order and constraints                      │
│  □ Execute in test environment first to verify compatibility│
│  □ Check index and view definitions are correct             │
│  □ Confirm Oracle SEQUENCE/TRIGGER syntax                   │
│  □ Confirm PostgreSQL SERIAL type is correct                │
│  □ Confirm field types in views are compatible with target DB│
│  □ Confirm index syntax is correct (PostgreSQL/Oracle diff) │
│                                                             │
│  Testing Recommendations:                                   │
│  1. Create temporary tables in test environment to verify DDL│
│  2. Execute DESCRIBE/DESC to confirm field structure        │
│  3. Insert test data to verify constraints                  │
│  4. Execute queries to verify views and indexes             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 6.5.3 Validation Confirmation (User Interaction)

Use Question tool to let user confirm validation results:

**Question**: "SQL conversion completed, please confirm the following validation status:"

**options**:
```json
[
  {"label": "Validated, can generate report", "description": "Already validated in test environment, SQL is executable"},
  {"label": "Needs modification", "description": "Found syntax or logic issues, needs adjustment"},
  {"label": "Skip validation, generate directly", "description": "Trust AI conversion results, generate report directly"}
]
```

If user selects "Needs modification":
- Ask about specific issues
- Manually adjust converted SQL
- Re-execute validation step

### Step 7: TODO Generation (Automatic)

Automatically generate structured TODO list based on user-confirmed release components.

### Step 8: TODO List Confirmation (User Interaction - Round 2)

**Must execute this step for final user confirmation of TODO list:**

Use Question tool to display generated TODO list:

**Question**: "Please confirm the following release TODO list, adjust if needed:"

**options**:
```json
[
  {"label": "Confirm TODO list", "description": "Confirm current TODO list, start generating report"},
  {"label": "Needs modification", "description": "Need to add or remove certain TODO items"}
]
```

If user selects "Needs modification", then:
- Ask user which TODO items need to be added or removed
- Regenerate list and confirm again

### Step 9: Markdown Report Generation (Automatic)

**Single-Project Mode:**
Generate complete Markdown format report, containing:
- Release component confirmation status (including automatic recognition results)
- Changed files summary
- SQL compatibility analysis
- SQL multi-database conversion results (if applicable)
- Java code change description
- Pending TODO list (confirmed version)

**Batch Mode:**
1. Generate independent project-level report for each project
2. Summarize all project results, generate global batch report, containing:
   - Project summary table (change statistics for each project)
   - Global change statistics
   - SQL compatibility analysis summary for each project
   - Global TODO list (grouped by project)
   - Links to each project report file

## Usage

### Command Mode

**Single-Project Mode:**
```
release-checker --project <path> --branch <comparison-branch>
```

**Batch Mode (Multiple Projects):**
```
release-checker --projects <path1> --branches <branch1> --projects <path2> --branches <branch2>
```

Or use configuration file:
```
release-checker --config <configuration-file-path>
```

### Parameter Description

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| --project | -p | Project path (required for single-project mode) | None |
| --branch | -b | Comparison branch (required for single-project mode) | None |
| --projects | -P | Multiple project paths (batch mode, repeatable) | None |
| --branches | -B | Multiple comparison branches (batch mode, corresponds to projects) | None |
| --config | -c | Batch configuration file path (JSON/YAML) | None |
| --report | -r | Markdown report output path | release-check-report.md |

### Batch Configuration File Format

**JSON Format:**
```json
{
  "projects": [
    {
      "path": "/path/to/your/project-a",
      "branch": "release/v1.0.0",
      "report": "report-project-a.md"
    },
    {
      "path": "/path/to/your/project-b",
      "branch": "release/v1.0.0",
      "report": "report-project-b.md"
    },
    {
      "path": "/path/to/your/project-c",
      "branch": "release/v1.0.0",
      "report": "report-project-c.md"
    }
  ],
  "global_report": "batch-release-report.md",
  "parallel": true
}
```

**YAML Format:**
```yaml
projects:
  - path: "/path/to/your/project-a"
    branch: "release/v1.0.0"
    report: "report-project-a.md"
  - path: "/path/to/your/project-b"
    branch: "release/v1.0.0"
    report: "report-project-b.md"
  - path: "/path/to/your/project-c"
    branch: "release/v1.0.0"
    report: "report-project-c.md"
global_report: "batch-release-report.md"
parallel: true
```

### Usage Examples

**Example 1: Single Project**
```
release-checker -p /path/to/your/project -b release/v1.0.0
```

**Example 2: Batch Mode (Command Line)**
```
release-checker -P /path/to/project-a -B release/v1.0.0 -P /path/to/project-b -B release/v1.0.0
```

**Example 3: Batch Mode (Configuration File)**
```
release-checker -c release-config.json
```

**Example 4: Natural Language Trigger (Batch)**
```
User: Check release compatibility for the following projects, all comparing against release/v1.0.0:
- /path/to/your/project-a
- /path/to/your/project-b
- /path/to/your/project-c
```

### Batch Execution Flow

```
1. AI parses batch configuration (command line parameters or configuration file)
2. For each project execute in parallel/serial:
   a. git diff analysis
   b. intelligent component recognition
   c. release component confirmation (batch confirm or individual confirm)
   d. SQL conversion (if needed)
   e. SQL syntax validation
   f. generate project-level report
3. Summarize all project results
4. Generate global batch report (containing summary of all projects)
```

### Batch Confirmation Mode

**Question**: "Detected N projects to check, please select confirmation mode:"

**options**:
```json
[
  {"label": "Batch confirmation (all projects use same components)", "description": "All projects select the same release components"},
  {"label": "Individual confirmation", "description": "Each project selects release components separately"},
  {"label": "Use intelligent recognition results", "description": "Directly use AI automatically recognized components, no manual confirmation needed"}
]
```

### Usage Example

```
User: Check release compatibility for /path/to/your/project between current next branch and last release/v1.0.0 branch

AI automatically executes:
1. git diff release/v1.0.0..next --name-only
2. Analyze changed files, intelligently recognize Push Center/Gateway/Configuration changes
3. Use Question to let user select involved components (Round 1)
4. If user selects "SQL Scripts", ask if conversion to multi-database versions is needed
5. If user needs conversion, ask for SQL file paths
6. Analyze SQL compatibility, generate multi-database versions (if needed)
7. **Execute SQL syntax validation (automatic)**
8. **Display manual review checklist, require user confirmation**
9. Generate preliminary TODO list
10. Use Question to let user confirm TODO list (Round 2)
11. Generate complete Markdown report
```

### Interaction Flow

```
1. AI analyzes git diff, displays changed file statistics
2. AI automatically recognizes Push Center, Gateway, Configuration changes and other components
3. AI pops up Question to let user select release components (Round 1, includes automatic recognition results)
4. If user selects "SQL Scripts":
   - AI asks if conversion to multi-database versions is needed
   - If yes, asks for SQL file paths
   - Generates PostgreSQL and Oracle versions
5. AI analyzes SQL compatibility
6. AI executes SQL syntax validation (automatic check)
7. AI displays manual review checklist, requires user confirmation
8. AI generates preliminary TODO list
9. AI pops up Question to let user confirm TODO list (Round 2)
10. After user confirmation, AI generates complete Markdown report
```

## Intelligent Recognition Details

### Push Center Recognition Flow

```
1. Get git diff changed Java file list
2. For each file execute content detection:
   a) Detect if contains push-related keywords (推送, push, spush)
   b) Detect if defines EVENT class (extends ApplicationEvent)
   c) Detect if contains Push related Feign Client
3. If any item is detected, mark as "Push Center Configuration"
4. Display automatic recognition results and basis during user confirmation phase
```

### Gateway Recognition Flow

```
1. Get git diff changed Java file list
2. For each file execute content detection:
   a) Detect if contains new @FeignClient annotation
   b) Detect if value attribute uses ${xxx.xxx.name:} format
   c) Detect if service name contains spush or other service identifiers
3. If new Feign definition with service configuration is detected, mark as "Gateway Configuration"
4. Display automatic recognition results and basis during user confirmation phase
```

### Configuration Change Recognition Flow

```
1. Get git diff changed file list
2. Detect configuration file changes:
   a) Detect if yml/properties files have changes
3. Detect annotation-based configuration:
   a) For Java files detect @Value, @ConfigurationProperties, @PropertySource
   b) For Java files detect @Configuration, @Bean classes
4. Comprehensive determination, mark as "Configuration File Changes"
5. Display automatic recognition results during user confirmation phase (distinguish between local config and annotation config)
```

## SQL Conversion Built-in Logic

### Python Script Execution

**This skill uses Python script for SQL conversion and validation to ensure reliability.**

Script location: `scripts/release_checker.py`

#### Conversion Function

```
python release_checker.py --convert-sql --sql-files <file1> <file2> ... [--output-dir <output-directory>]
```

**Parameter Description:**
| Parameter | Description |
|-----------|-------------|
| --convert-sql | Enable SQL conversion mode |
| --sql-files | MySQL SQL files to convert (multiple allowed) |
| --output-dir | Output directory (default same as source file directory) |

#### Validation Function

Python script automatically executes the following validations:

**PostgreSQL Validation Rules (10 items):**
- ✅ Backtick check
- ✅ AUTO_INCREMENT check
- ✅ ENGINE check
- ✅ NOW() function check
- ✅ IFNULL function check
- ✅ TINYINT type check
- ✅ DATETIME type check
- ✅ DEFAULT CHARSET check
- ✅ UNSIGNED check
- ✅ COMMENT syntax check

**Oracle Validation Rules (11 items):**
- ✅ Backtick check
- ✅ AUTO_INCREMENT check
- ✅ ENGINE check
- ✅ NOW() function check
- ✅ IFNULL function check
- ✅ TINYINT type check
- ✅ DATETIME type check
- ✅ IF NOT EXISTS check
- ✅ LIMIT check
- ✅ DEFAULT CHARSET check
- ✅ UNSIGNED check

#### Conversion Function Implementation

Python script has the following built-in conversion functions:

```
SQLConverter.convert_to_postgresql(sql_content):
    - Replace AUTO_INCREMENT → SERIAL
    - Replace NOW() → CURRENT_TIMESTAMP
    - Replace DATETIME → TIMESTAMP
    - Replace TINYINT → SMALLINT
    - Replace backticks → double quotes
    - Remove ENGINE=InnoDB
    - Remove DEFAULT CHARSET
    - Remove UNSIGNED

SQLConverter.convert_to_oracle(sql_content):
    - Replace DATETIME → TIMESTAMP
    - Replace TINYINT → NUMBER(3)
    - Replace backticks → double quotes
    - Replace LIMIT → manual handling required
    - Remove AUTO_INCREMENT, create SEQUENCE + TRIGGER
    - Replace NOW() → SYSTIMESTAMP
    - Remove ENGINE=InnoDB
    - Remove DEFAULT CHARSET
    - Remove UNSIGNED
```

### Conversion Output

After conversion generates:
- `<original-filename>-postgres.sql`
- `<original-filename>-oracle.sql`

Each file header contains conversion notes comments.

**Python Script Execution Flow:**
```
1. Read MySQL SQL file
2. Execute PostgreSQL conversion → Output .postgres.sql
3. Execute Oracle conversion → Output .oracle.sql
4. Validate PostgreSQL version (10 rules)
5. Validate Oracle version (11 rules)
6. Display validation result summary
7. Save converted files
```

## Output Examples

### Intelligent Recognition Results

```
🔍 Intelligent Recognition Results
===========================================================
Push Center Configuration: ✅ Automatically detected
  - Detected file: XXXXEvent.java (contains EVENT definition)
  - Detected file: PushFeignClient.java (contains push related Feign)

Gateway Configuration: ✅ Automatically detected
  - Detected new Feign definition: PushFeignClient
  - Service name configuration: ${xxx.xxx.name:xxxx-server}

Configuration File Changes: ✅ Automatically detected
  - Detected annotation config: @Value("${xxx}")
  - Detected configuration class: XxxProperties.java
```

### User Confirmation (Round 1)

```
Please confirm which components are involved in this release? (Automatic recognition results for reference only)

[ ] Push Center Configuration - Push Center service related configuration changes (Auto-detected: related code found)
[✓] Gateway Configuration - Unified Gateway related configuration (Auto-detected: new Feign definition found)
[ ] ES Changes - Elasticsearch index or query changes
[✓] SQL Scripts - Database script changes (DML/DDL)
[ ] Dictionary Changes - Data dictionary or enum configuration changes
[✓] Configuration File Changes - Application configuration file changes (Auto-detected: annotation/configuration class found)
[ ] Redis Configuration - Redis cache or data structure changes
[ ] MQ Messages - Message queue topic or message format changes
[ ] File Storage - File upload, storage path changes
[✓] API Interfaces - External API interface changes
[✓] Java Code - Java code changes
```

### SQL Conversion Inquiry

```
SQL script changes detected. Do you need to convert existing SQL scripts to multi-database versions?

[ ] Yes, I need to generate multi-database versions
[✓] No, SQL scripts are ready
```

**After user selects "Yes", Python script automatically executes:**

```bash
# Execute SQL conversion
python scripts/release_checker.py \
  --convert-sql \
  --sql-files scripts/db/v1.0.0/mysql-ddl.sql \
  --output-dir scripts/db/v1.0.0/
```

**Python script output example:**

```
🔄 SQL Multi-Database Conversion
===========================================================

📄 Processing file: scripts/db/v1.0.0/mysql-ddl.sql
  ✅ PostgreSQL conversion completed (8 changes)
    - Backticks → Double quotes
    - AUTO_INCREMENT → SERIAL
    - NOW() → CURRENT_TIMESTAMP
    - DATETIME → TIMESTAMP
    - TINYINT → SMALLINT
    - IFNULL() → COALESCE()
    - Remove ENGINE=InnoDB
    - Remove DEFAULT CHARSET

  ✅ Oracle conversion completed (8 changes)
    - Backticks → Double quotes
    - NOW() → SYSTIMESTAMP
    - DATETIME → TIMESTAMP
    - TINYINT → NUMBER(3)
    - IFNULL() → NVL()
    - AUTO_INCREMENT → SEQUENCE + TRIGGER
    - Remove ENGINE=InnoDB
    - Remove DEFAULT CHARSET

  🔍 PostgreSQL validation:
    Pass: 8/10, Fail: 0, Warning: 2
    ⚠️  NOW() function check: Suggest using CURRENT_TIMESTAMP instead of NOW()
    ⚠️  COMMENT syntax check: PostgreSQL supports COMMENT ON COLUMN syntax

  🔍 Oracle validation:
    Pass: 9/11, Fail: 0, Warning: 2
    ⚠️  IF NOT EXISTS check: Oracle does not support IF NOT EXISTS, manual handling required
    ⚠️  LIMIT check: Manual conversion to ROWNUM or FETCH FIRST required

  💾 PostgreSQL saved: scripts/db/v1.0.0/mysql-ddl-postgres.sql
  💾 Oracle saved: scripts/db/v1.0.0/mysql-ddl-oracle.sql

✅ SQL conversion completed
```

### User Confirmation (Round 2) - TODO List Confirmation

```
Please confirm the following release TODO list:

## 📋 Release TODO List

### SQL Scripts Related
- [ ] Execute Oracle DDL script: scripts/db/v1.0.0/oracle-ddl.sql
- [ ] Execute PostgreSQL DDL script: scripts/db/v1.0.0/postgres-ddl.sql
- [ ] Validate SQL compatibility (Oracle: IF NOT EXISTS needs manual handling)

### Push Center Configuration
- [ ] Validate Push API client configuration
- [ ] Check Push event handling logic

### Gateway Configuration
- [ ] Validate API interface changes
- [ ] Check interface permission configuration

### Configuration File Changes
- [ ] Check @Value annotation configuration
- [ ] Validate configuration class loading

### Java Code
- [ ] Execute unit tests: mvn test
- [ ] Compile validation: mvn compile

[✓] Confirm TODO list
[ ] Needs modification
```

### Markdown Report

```markdown
# 📋 Release Compatibility Check Report

> Project: /path/to/your/project
> Comparison Branch: release/v1.0.0 → feature/next
> Generation Time: 2026-04-07 12:00:00

---

## 1. Intelligent Recognition Results

| Component | Auto-Detected | User Confirmed |
|-----------|---------------|----------------|
| Push Center Configuration | ✅ Related code detected | ✅ Yes |
| Gateway Configuration | ✅ New Feign detected | ✅ Yes |
| Configuration File Changes | ✅ Annotation/config class detected | ✅ Yes |
| SQL Scripts | - | ✅ Yes |
| Java Code | - | ✅ Yes |

## 2. Changed Files Summary

| Type | Count |
|------|-------|
| Java Code | 32 |
| SQL Scripts | 2 |
| Others | 1 |

## 3. SQL Compatibility Analysis

### Changed SQL Files
- scripts/db/v1.0.0/oracle-ddl.sql
- scripts/db/v1.0.0/postgres-ddl.sql

### Compatibility Issues
- ⚠️ [LOW] IF NOT EXISTS not supported in Oracle

## 4. Pending TODO (Confirmed)

- [ ] SQL Scripts: Execute DDL, validate compatibility
- [ ] Push Center Configuration: Validate Push API
- [ ] Gateway Configuration: Validate interface changes
- [ ] Configuration Changes: Check annotation configuration
- [ ] Java Code: Execute tests and compile validation

---

*Report generated by: release-checker*
```

## Supported Databases

| Database | File Suffix | Features |
|----------|-------------|----------|
| MySQL | `-mysql.sql` / `mysql/*.xml` | AUTO_INCREMENT, NOW(), backticks |
| PostgreSQL | `-postgres.sql` / `postgresql/*.xml` | SERIAL, CURRENT_TIMESTAMP, double quotes |
| Oracle | `-oracle.sql` / `oracle/*.xml` | SEQUENCE+TRIGGER, SYSTIMESTAMP, VARCHAR2 |

## Limitations

- Requires git repository for diff analysis
- **Does not execute actual SQL validation** (AI-generated SQL needs manual validation in test environment)
- Does not execute Java code compilation validation
- Generated scripts require manual review
- MyBatis Mapper conversion requires ensuring corresponding directory structure exists
- Intelligent recognition based on code pattern matching, may have false positives, requires final user confirmation
- **SQL conversion validation rule library only covers common syntax, complex SQL (stored procedures, functions, triggers) requires manual review**
- **AI cannot validate data compatibility and business logic correctness**

## Cross-Platform Compatibility

### Tool Adaptation

This skill is designed to be **platform-independent**, not relying on platform-specific tools.

| Tool | Purpose | Compatibility |
|------|---------|---------------|
| `git` | Git diff analysis | All platforms |
| `bash` | Execute shell commands | All platforms |
| `grep` | Content search | All platforms |
| `glob` | File matching | All platforms |
| `read` | Read files | All platforms |
| `write` | Write files | All platforms |

### Question Tool Degradation Strategy

**Priority use of Question tool** (OpenCode/Claude Code native support), **automatically degrade to text interaction when platform does not support**.

#### Degradation Rules

```
IF Question tool available:
    → Use Question tool (multiple=true)
ELSE:
    → Use text confirmation format, let user reply with numbers or option letters
```

#### Text Confirmation Format (Degradation Solution)

**Single-Project Mode:**
```
Please select components involved in this release (reply with numbers, multiple separated by comma):

  1. Push Center Configuration - Push Center service related configuration changes
  2. Gateway Configuration - Unified Gateway related configuration
  3. ES Changes - Elasticsearch index or query changes
  4. SQL Scripts - Database script changes (DML/DDL)
  5. Dictionary Changes - Data dictionary or enum configuration changes
  6. Configuration File Changes - Application configuration file changes
  7. Redis Configuration - Redis cache or data structure changes
  8. MQ Messages - Message queue topic or message format changes
  9. File Storage - File upload, storage path changes
  10. API Interfaces - External API interface changes
  11. Java Code - Java code changes

Example reply: 1,4,6,11
```

**SQL Conversion Inquiry:**
```
SQL script changes detected. Do you need to convert to multi-database versions?

  1. Yes, I need to generate multi-database versions
  2. No, SQL scripts are ready

Please select (1/2):
```

**TODO List Confirmation:**
```
Please confirm the following release TODO list:

## 📋 Release TODO List
(List TODO items here)

Please select:
  1. Confirm TODO list, start generating report
  2. Needs modification (please specify what needs adjustment)
```

**Batch Confirmation Mode:**
```
Detected 3 projects to check, please select confirmation mode:

  1. Batch confirmation (all projects use same components)
  2. Individual confirmation (each project selects separately)
  3. Use intelligent recognition results (no manual confirmation needed)

Please select (1/2/3):
```

## Best Practices

1. Run checks before each release
2. Carefully confirm intelligent recognition results and user-selected components
3. If there are SQL changes and multi-database support is needed, use built-in conversion function
4. **Execute SQL syntax validation (automatic check)**
5. **Manually validate generated SQL scripts in test environment**
6. Confirm whether generated TODO list meets actual requirements
7. Generate Markdown report for retention
8. Review TODO items before merging to main branch
