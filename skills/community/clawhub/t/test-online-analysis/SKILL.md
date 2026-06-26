---
name: test-online-analysis
description: Online (real-time) data analysis, rule extraction, and pattern recognition for testing scenarios. Activate when user mentions test online analysis, real-time data rule extraction, testing scenario pattern recognition, or log/stream data analysis for testing.
---

# Test Online Analysis 测试实时分析技能

## Overview

This skill provides real-time data analysis capabilities, including rule extraction from online streaming data, pattern recognition for testing scenarios, log analysis, and anomaly detection. It helps automate the process of identifying business rules, testing patterns, and abnormal behaviors from live data streams or log files.

## Core Capabilities

### 1. Rule Extraction
- Automatically extract business rules from online data streams
- Identify implicit logic and constraints from real-time transaction data
- Generate structured rule documentation for testing reference

### 2. Pattern Recognition
- Recognize common testing scenarios from log data
- Identify recurring patterns in user behavior and system responses
- Classify data patterns to simplify test case design

### 3. Anomaly Detection
- Real-time detection of abnormal data points and system behaviors
- Compare current data against historical patterns to identify outliers
- Generate anomaly reports with severity levels

### 4. Testing Scenario Generation
- Automatically generate test cases based on extracted rules and patterns
- Map real-world scenarios to test coverage requirements
- Identify edge cases and boundary conditions from live data



## Workflow

### Step 1: Data Ingestion
1. Accept input data sources: log files, real-time API streams, database queries
2. Validate data format and structure
3. Preprocess data (cleaning, normalization, filtering)

### Step 2: Analysis Execution
1. Run rule extraction algorithm on processed data
2. Apply pattern recognition models to identify testing scenarios
3. Perform anomaly detection against baseline patterns

### Step 3: Result Generation
1. Generate structured rule documentation in markdown format
2. Create test case suggestions based on extracted patterns
3. Produce anomaly reports with actionable insights

### Step 4: Output Delivery
1. Present summary of key findings to user
2. Offer to export full analysis results to files
3. Suggest follow-up actions for testing optimization

## Usage Examples

### Example 1: Extract Rules from Transaction Logs
**User Request:** "Analyze these transaction logs and extract business rules for testing"
**Skill Action:**
1. Ingest and parse log files
2. Extract transaction validation rules, amount limits, and processing logic
3. Generate structured rule document with test case suggestions
4. Output summary of key rules and potential testing scenarios

### Example 2: Detect Anomalies in Real-time Data
**User Request:** "Monitor this data stream and find anomalies"
**Skill Action:**
1. Connect to real-time data source
2. Establish baseline pattern from historical data
3. Alert on anomalous data points as they appear
4. Generate anomaly report with severity assessment

## Resources

### scripts/
- `rule_extractor.py`: Core algorithm for extracting business rules from structured data
- `pattern_recognizer.py`: Machine learning model for identifying testing scenarios
- `anomaly_detector.py`: Real-time anomaly detection utility
- `test_case_generator.py`: Automatically generate test cases from extracted rules

### references/
- `rule_extraction_standards.md`: Guidelines for consistent rule documentation
- `pattern_catalog.md`: Catalog of common testing patterns and scenarios
- `anomaly_severity_matrix.md`: Severity classification framework for anomalies

## Installation

### Local Installation
1. Clone or copy the `online-analysis` directory to your OpenClaw skills folder:
   ```bash
   # User workspace skills
   cp -r online-analysis ~/.openclaw/workspace/skills/
   
   # Or global system skills
   cp -r online-analysis /usr/local/lib/node_modules/openclaw/skills/
   ```
2. Restart OpenClaw to load the new skill

### Dependencies
```bash
pip install numpy
```

## Usage

### Command Line
```bash
# Extract rules from log files
python scripts/rule_extractor.py transaction_logs.txt > extracted_rules.md

# Detect anomalies in numeric data
python scripts/anomaly_detector.py performance_metrics.json > anomaly_report.md
```

### Skill Trigger
The skill automatically activates when you mention:
- "online analysis"
- "rule extraction"
- "real-time data analysis"
- "log analysis for testing"
- "anomaly detection"

## License
MIT
