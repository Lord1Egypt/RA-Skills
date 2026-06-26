---
name: text-to-sql
description: Support generating SQL queries through natural language; use when users need to configure Text-to-SQL database, manage data topics, or generate SQL with natural language questions
dependency:
  python:
    - pyyaml>=6.0
    - sqlalchemy>=2.0.0
---

# Text-to-SQL Intelligent Query Skill

## Task Objectives

- This Skill is used for: Generating SQL query statements through natural language, supporting multi-topic database configuration and table structure management
- Capabilities include: Database configuration, topic management, table structure reading, natural language to SQL
- Trigger conditions: User needs to configure Text-to-SQL database, create data topics, select data tables, or generate SQL with natural language questions

## Prerequisites

### Dependency Description

Required packages and versions for scripts:

```
pyyaml>=6.0
sqlalchemy>=2.0.0
```

### API Service Description

This Skill generates SQL through the HTTP API `/api/sql_for_skill/` endpoint:

- Default API address: `https://asksql.ucap.com.cn/`
- Service needs to be started before calling
- Supports custom API address (via `--api-url` parameter)

**API Interface Specification**:

- Endpoint path: `POST /api/sql_for_skill/`
- Request format: `multipart/form-data`
- Request parameters:
  - `question`: User's natural language question (string)
  - `yaml_file`: YAML configuration file (uploaded as file)
- Response format: JSON array
- Response example:
  ```json
  [
    {
      "STATUS": "ok",
      "MESSAGE": "",
      "SQL": "SELECT SUM(total_amount) AS total_sales FROM orders WHERE YEAR(signing_date) = 2026",
      "SQL_NO_PERM": "SELECT SUM(total_amount) AS total_sales FROM orders WHERE YEAR(signing_date) = 2026",
      "QUESTION": "This year's total sales"
    }
  ]
  ```
- Return value: Extract the `SQL` field from the first element of the response array

## Data Configuration Methods

### Two Configuration Methods Explained

When the agent guides users through data configuration, it must clearly explain the following two methods:

**Method 1: Database URL Configuration (Highly Recommended)**
- Read table structure directly through database connection
- Real-time data synchronization, ensuring accuracy
- Supports complete database semantic understanding

**Method 2: Excel File Configuration**
- Suitable for scenarios where direct database connection is not possible
- Configure through Excel file with specific format requirements

**Excel File Format (Must Strictly Follow):**

```
┌─────────────────────────────────────────────────────────────────┐
│ Excel File: products.xlsx                                       │
├─────────────────────────────────────────────────────────────────┤
│ Sheet: orders (Sheet name = Table name)                         │
├──────────┬──────────┬────────────┬───────────┬─────────────────┤
│ order_id │ customer │ order_date │  amount   │ status          │
│ (Column) │ (Column) │  (Column)  │ (Column)  │ (Column)        │
├──────────┼──────────┼────────────┼───────────┼─────────────────┤
│   1001   │  John    │ 2024-01-15 │  1500.00  │ completed       │
│   1002   │  Mary    │ 2024-01-16 │  2300.50  │ pending         │
│   ...    │  ...     │    ...     │    ...    │ ...             │
└──────────┴──────────┴────────────┴───────────┴─────────────────┘
         ↑ First row = Column names (field names)
         ↑ Data starts from second row
```

**Format Requirements:**
1. **File naming**: Excel filename must match database name (e.g., `products.xlsx` for `products` database)
2. **Sheet naming**: Each sheet name must exactly match the table name (e.g., `orders` sheet for `orders` table)
3. **First row**: Must contain column names (field names), cannot be empty
4. **Second row onwards**: Actual data rows (optional, used for understanding data types)

**The agent should clearly recommend users to prioritize the database URL configuration method.** Only use the Excel file method when users cannot provide a database connection.

### Method 1: Database URL Configuration

#### Configuration Steps

1. Guide the user to provide database connection information
2. Call the configuration script to save database information:

```bash
python scripts/config_db.py --db-url <database URL> --db-password <password> --config-file ./output/text-to-sql-config.json
```

This script saves the configuration to `./output/text-to-sql-config.json` file.

#### Database URL Format

```
database_type://username:password@host:port/database_name
```

Examples:
- MySQL: `mysql://root:password@localhost:3306/mydb` (will auto-convert to use pymysql driver)
- MySQL with explicit driver: `mysql+pymysql://root:password@localhost:3306/mydb`
- SQL Server: `mssql://sa:password@localhost:1433/mydb`

**Note**: For MySQL connections, the system automatically converts `mysql://` to `mysql+pymysql://` for better compatibility. You can also explicitly specify the driver.

#### Reading Table Structure

After configuration, use the following command to read table structure:

```bash
python scripts/read_tables.py --config-file ./output/text-to-sql-config.json
```

### Method 2: Excel File Configuration

#### Applicable Scenarios

When users cannot provide a database connection, the Excel file method can be used for configuration.

#### Configuration Steps

1. Guide the user to provide the Excel file path
2. Remind user to follow the Excel file format requirements described above
3. After the user provides the file, **no parsing operation is needed**, directly call the `read_tables.py` script:

```bash
python scripts/read_tables.py --excel-file <Excel file path>
```

Example:
```bash
python scripts/read_tables.py --excel-file data_file.xlsx
```

- Parameter description:
  - `--excel-file`: Complete path to the Excel file

## Operation Steps

### Step 0: Configuration Check (Must Execute on First Call)

**Important: The agent must check the configuration status before performing any operation**

The agent needs to check whether yaml configuration files exist in the `./output/` directory:

**Check Method**:

```bash
# Check if .yaml files exist in ./output/ directory
ls ./output/*.yaml 2>/dev/null
```

**Check Result Handling**:

**Scenario A: yaml configuration files exist**

- Indicates user has completed configuration in advance
- Agent skips all configuration steps (Step 1 and Step 2)
- Proceed directly to Step 3 (Query with natural language)
- Agent informs user: "Detected existing topic configuration, you can ask questions directly."
- List configured topic names for user reference

**Scenario B: No yaml configuration files**

- Indicates user has not completed configuration
- Agent proceeds to execute Step 1 (Database Configuration) and Step 2 (Topic Setup)
- Guide user through the standard configuration process

### Standard Configuration Process

#### Step 1: Database Configuration

**The agent must clearly explain the two configuration methods:**

1. **Method 1: Database URL Configuration (Highly Recommended)**
   - Read table structure directly through database connection
   - Real-time data synchronization, ensuring accuracy
   - Supports complete database semantic understanding

2. **Method 2: Excel File Configuration**
   - Suitable for scenarios where direct database connection is not possible
   - Configure through Excel file schema description

**The agent should clearly recommend users to prioritize the database URL configuration method.**

**If user chooses database URL configuration:**
Guide user to provide database URL and password, save to local configuration file:

```bash
python scripts/config_db.py --db-url <database URL> --db-password <password>
```

This script saves the configuration to `text-to-sql-config.json` file.

**If user chooses Excel file configuration:**
1. Guide user to provide Excel file path
2. Remind user to follow the **Excel File Format** requirements described in the "Two Configuration Methods Explained" section above
3. After user provides file, **no parsing operation needed**, directly call:

```bash
python scripts/read_tables.py --excel-file <Excel file path>
```

#### Step 2: Topic Setup

**Important: The agent must mandatorily guide users to set up topics, table selection step cannot be skipped**

The agent should guide users through the following process:

**2.1 Clearly inform user that topic setup is mandatory**

- Agent clearly states: "Topic setup is a mandatory step, it will help you get more accurate SQL generation results and better query performance."
- Explain benefits of setting up topics: more accurate SQL generation, faster query speed, better business semantic understanding

**2.2 Execute topic setup process**

- Agent must guide user to create topics and select tables, **table selection step cannot be skipped**
- Multiple topics can be created
- Execution steps:
  1. Call script to read all table structures and generate knowledge
     ```bash
     # Method 1: Use database connection (recommended)
     python scripts/read_tables.py --config-file ./output/text-to-sql-config.json --output-dir ./output

     # Method 2: Use Excel file
     python scripts/read_tables.py --excel-file data_file.xlsx
     ```
     This script generates `table_info.json` (table name list) and `column_info.json` (table structure information) files.
  2. **Agent reads table list from** **`table_info.json`** **file, displays all tables to user completely**, provides clear table descriptions
  3. **Key emphasis: Table selection is a critical step in topic creation, directly affects SQL generation accuracy and query effectiveness, must be autonomously selected by user based on actual business needs**
  4. Ask user: "Please tell me the topic name you want to create (e.g., sales topic, human resources topic)"
  5. **Agent is strictly prohibited from selecting tables for topics itself**, must require user to explicitly specify needed tables
  6. Agent can provide brief table descriptions and recommendations, but final selection must be completely left to user
  7. Generate topic configuration file
     ```bash
     python scripts/generate_yaml.py --topic-name <topic name> --tables <table list comma-separated> --output-path ./output/
     ```
  8. Ask user: "Do you want to continue creating other topics?"
  9. User can repeat to create multiple topics (no need to re-read table structure, use existing `./output/column_info.json` directly)

**2.3 Agent Guidance Recommendations**

- **Agent is prohibited from making assumptions or guessing user intent**
- Agent must mandatorily guide user to set up topics, cannot allow skipping
- **Agent is strictly prohibited from setting topics or selecting tables for topics itself**, must display all table lists to user after reading table structure, let user completely autonomously select relevant tables based on actual business needs
- Agent can provide brief table descriptions and recommendations, but final selection must be completely left to user
- **Key emphasis: Table selection step cannot be skipped, this is a key link to ensure topic configuration accuracy**
- **Prioritize recommending database connection method to users**, only use Excel file method when user cannot provide database connection

#### Step 3: Query with Natural Language (Includes Topic Selection Logic)

**Important: Step 3 can be executed directly (when Step 0 detects existing configuration)**

After configuration is complete (or when existing configuration is detected), users can ask questions in natural language, the agent needs to select topic and generate SQL according to the following logic:

##### 3.1 Topic Selection Logic

**Scenario: One or more topics exist (user has completed topic setup)**

**Case A: User question explicitly mentions topic**

- Agent identifies topic keywords in user question (e.g., "sales", "human resources", "inventory", etc.)
- Matches corresponding `<topic name>.yaml` file in `./output/` directory
- If match is successful, directly use that yaml file to call script
- If match fails, prompt user that topic does not exist and list available topics

**Case B: User question does not explicitly mention topic**

- Agent analyzes question content, selects most relevant topic from all topics
- Agent informs user: "Based on your question, I suggest using [topic name] topic, continue?"
- If user confirms, use that topic; if user declines, list all topics for user to select

##### 3.2 Call SQL Generation Script

After determining topic, call API to generate SQL:

```bash
python scripts/query_sql.py --api-url https://asksql.ucap.com.cn/ --question "user question" --config ./output/<topic name>.yaml
```

The script calls the API's `/api/sql_for_skill/` endpoint and returns the generated SQL statement.

### Optional Branches

- When user wants to modify topic configuration: Re-call `generate_yaml.py` to overwrite original configuration file
- When user wants to reconfigure database: Re-call `config_db.py` to overwrite configuration file
- When user wants to view configured topics: Agent lists yaml files in `./output/` directory
- When user question is ambiguous and cannot determine topic: Agent actively asks user or lists all topics for selection
- When API service is not at default address: Use `--api-url` parameter to specify custom API address

## Resource Index

### Required Scripts

- [scripts/config_db.py](scripts/config_db.py) - Save database configuration to local file
- [scripts/read_tables.py](scripts/read_tables.py) - Read database table structure (supports both database connection and Excel file methods)
- [scripts/generate_yaml.py](scripts/generate_yaml.py) - Generate topic configuration file (supports all parameter)
- [scripts/query_sql.py](scripts/query_sql.py) - Generate SQL by calling generate_sql API endpoint

### Output Files

All generated files are stored in `./output/` directory:
- `table_info.json` - Table name list
- `column_info.json` - Table structure information
- `<topic_name>.yaml` - Topic configuration files
- [references/open_semantic_interchange_description.md](references/open_semantic_interchange_description.md) - YAML file format specification and field definitions (refer to this document when users ask about YAML format, field meanings, or configuration details)

## Notes

- All scripts are pure functional tools without interaction logic, all inputs are passed through parameters
- Database URL and password are saved in local configuration file `./output/text-to-sql-config.json`
- Topic configuration files are stored in yaml format for easy version management and viewing
- Only `query_sql.py` calls API, other scripts are all executed locally
- If database connection fails, check if URL and password are correct
- If API service connection fails, check if service is started and address is correct
- **Prioritize database connection method**, only use Excel file method when database connection cannot be provided
- **When users ask about YAML file format, field definitions, or configuration details**, refer to the [open_semantic_interchange_description.md](references/open_semantic_interchange_description.md) document which contains complete specification of the semantic model YAML structure

## Usage Examples

### Example 0: Detected Existing Configuration (Direct Query)

1. User: "Query last month's total sales"
2. Agent: Check ./output/ directory
3. Agent: Detect existing topic configuration files
4. Agent: "Detected existing topic configuration, you can ask questions directly."
5. Agent: Identify topic relevant to the question, use corresponding topic configuration file
6. Agent: Call query_sql.py to generate SQL

### Example 1: Intelligently Guide User to Set Up Topic (Recommended Process)

1. User: "Help me configure Text-to-SQL"
2. Agent: Check ./output/ directory
3. Agent: No yaml configuration files found, need to execute configuration process
4. Agent: "Please provide database URL and password"
5. User: "Database URL is URL"
6. Agent: Call config_db.py to save configuration
7. Agent: "Topic setup is a mandatory step, it will help you get more accurate SQL generation results and better query performance."
8. Agent: Call read_tables.py --config-file ./output/text-to-sql-config.json --output-dir ./output to read all tables
9. Agent: "There are multiple tables in the database, what topic do you want to create?"
10. User: "Create a topic"
11. Agent: "Please select tables to include in this topic from the database tables"
12. User: "Select relevant tables"
13. Agent: Call generate_yaml.py to generate topic configuration file
14. Agent: "Do you want to continue creating other topics?"
15. User: "No need"
16. User: "Query the top 10 products with highest sales last month"
17. Agent: Identify topic relevant to the question, use corresponding topic configuration file to call query_sql.py to generate SQL

### Example 2: Configure with Excel File

1. User: "Help me configure Text-to-SQL, but I don't have a database"
2. Agent: Check ./output/ directory
3. Agent: No yaml configuration files found, need to execute configuration process
4. Agent: "Okay, you can use the Excel file method for configuration. Please provide an Excel file with format requirements: each sheet corresponds to a table name, first row is column names"
5. User: "Provide Excel file path"
6. Agent: Call read_tables.py --excel-file data_file.xlsx to read Excel data
7. Agent: "Topic setup is a mandatory step..."
8. Follow same process as Example 1

### Example 3: Set Up Multiple Topics

1. User: "Help me configure Text-to-SQL"
2. Agent: Check ./output/ directory
3. Agent: No yaml configuration files found, need to execute configuration process
4. Agent: "Please provide database URL and password"
5. User: "Database URL is URL"
6. Agent: Call config_db.py to save configuration
7. Agent: "Topic setup is a mandatory step, it will help you get more accurate SQL generation results and better query performance."
8. Agent: Call read_tables.py --config-file text-to-sql-config.json to read all tables
9. Agent: "There are multiple tables in the database, what topic do you want to create?"
10. User: "Create first topic"
11. Agent: "Please select tables to include in this topic from the database tables"
12. User: "Select relevant tables"
13. Agent: Call generate_yaml.py to generate topic configuration file
14. Agent: "Do you want to continue creating other topics?"
15. User: "Create another topic"
16. Agent: "Please select tables to include in this topic from the database tables"
17. User: "Select relevant tables"
18. Agent: Call generate_yaml.py to generate topic configuration file
19. Agent: "Do you want to continue creating other topics?"
20. User: "No need"
21. User: "Query average salary of technical department"
22. Agent: Identify topic relevant to the question, determine most relevant topic
23. Agent: "Based on your question, I suggest using relevant topic, continue?"
24. User: "Yes"
25. Agent: Call query_sql.py using corresponding topic configuration file to generate SQL

### Example 4: User Explicitly Specifies Topic

1. User configured multiple topics
2. User: "Use a specific topic to query total orders in 2024"
3. Agent: Check ./output/ directory (existing configuration)
4. Agent: Identify topic explicitly specified by user, directly use corresponding topic configuration file
5. Agent: Call query_sql.py to generate SQL

### Example 5: Custom API Address

1. User: "My Text-to-SQL service is deployed at http://127.0.1.100:8080"
2. Agent: All query_sql.py calls use --api-url http://127.0.1.101:8080 parameter
3. User: "Query sales data"
4. Agent: Call query_sql.py --api-url http://127.0.1.101:8080 --config using corresponding topic configuration file to generate SQL
