# Score Analysis Framework

## 1. Analysis Dimensions Overview

### 1.1 Horizontal Comparison (Peer Classes)
- Total score average comparison
- Subject average comparison
- Score segment distribution comparison
- Special control line / undergraduate line pass rate comparison
- Top student distribution comparison

### 1.2 Vertical Comparison (Time Dimension)
- Class average score trends
- Pass count changes
- Student ranking fluctuations
- Subject score changes

### 1.3 Individual Analysis
- Student score volatility (stability)
- Subject imbalance diagnosis
- Progress/regression attribution
- Critical student identification (within X points of pass line)

## 2. Detailed Analysis Metrics

### 2.1 Class Overall Situation

#### Basic Statistics
- Number of students
- Total score average, median, standard deviation
- Subject averages, medians, standard deviations
- Maximum, minimum scores
- Average ranking (school/district level)

#### Pass Line Situation
- Special control line (first-tier) pass count and rate
- Undergraduate line (second-tier) pass count and rate
- Subject-specific pass counts
- Pass match rate (subject pass vs total pass correlation)

### 2.2 Score Distribution

| Score Segment | Count | Percentage | Peer Class |
|---------------|-------|------------|------------|
| 600+          |       |            |            |
| 550-600       |       |            |            |
| 500-550       |       |            |            |
| 450-500       |       |            |            |
| 400-450       |       |            |            |
| 350-400       |       |            |            |
| Below 350     |       |            |            |

### 2.3 Subject Analysis

#### Subject Balance
- Subject average comparison
- Subject standard deviation (lower = more balanced)
- Strongest vs weakest subject
- Subject range (strongest - weakest)

#### Subject Contribution
- Correlation between each subject and total score
- Most impactful subject
- Least impactful subject
- Score improvement cost-effectiveness

### 2.4 Individual Student Analysis

#### Subject Imbalance Diagnosis
- Calculate standard deviation of student's subject scores
- Higher imbalance index = more imbalanced development
- Identify severely imbalanced students (index > threshold)

#### Stability Analysis
- Standard deviation across multiple exams
- Ranking fluctuation amplitude
- Stable/volatile classification

#### Progress/Regression Attribution
- Ranking change cause analysis
- Subject contribution calculation
- Identify primary driving subjects

### 2.5 Critical Student Analysis

#### Special Control Line Critical Students
- Students within 10 points of special control line
- Identify weak subjects
- Provide improvement suggestions

#### Undergraduate Line Critical Students
- Students within 10 points of undergraduate line
- Identify weak subjects
- Provide improvement suggestions

## 3. Visualization Charts

### 3.1 Grouped Radar Charts (by student type)
- **Special Control Line Critical Students**: Show subject abilities (max 5 students)
- **Undergraduate Line Critical Students**: Show subject abilities (max 5 students)
- **Subject-Imbalanced Students**: Show highest imbalance index (max 5 students)

### 3.2 Other Charts
- Subject average bar chart
- Class average comparison chart
- Score segment distribution chart

## 4. Report Output Structure

### 4.1 Cover Page
- School logo (optional)
- School name
- Class name
- Exam name
- Analysis date

### 4.2 Table of Contents

### 4.3 Class Overall Situation
- Basic statistics table (three-line table)
- Pass line situation table
- Subject average comparison chart

### 4.4 Peer Class Comparison
- Total score comparison table
- Score distribution table
- Class average comparison chart
- Highlight box (key conclusions)

### 4.5 Critical Student Analysis
- Special control line critical students table + radar chart
- Undergraduate line critical students table + radar chart

### 4.6 Subject Imbalance Diagnosis
- Imbalanced students table + radar chart

### 4.7 Core Conclusions & Recommendations
- Strengths
- Weaknesses
- Teaching recommendations

## 5. Data Processing Notes

### 5.1 Header Detection
- Support Chinese/English mixed headers
- Handle merged cells
- Skip empty rows and title rows
- Detect adjusted/raw scores

### 5.2 Data Cleaning
- Handle absence marks (e.g., "/", "Absent", "Makeup")
- Handle anomalies (e.g., 0 scores, negative scores)
- Unified score format (string to number)

### 5.3 Special Cases
- Adjusted vs raw score distinction
- Different full scores per subject
- Bonus points handling
- Absent student marking

## 6. Style Specifications

### 6.1 Color Scheme (Customizable)
- Primary: Teal #006B6B
- Secondary: Medium Teal #2E8686
- Accent: Dark Red #C0392B (use sparingly)
- Decoration: Gold #B8860B

### 6.2 Table Style
- Research-style three-line table
- Teal header background
- Alternating row gray background

### 6.3 Chart Style
- Title: 16pt, teal color
- Labels: 12pt, dark gray
- Data labels: 12pt, bold

### 6.4 Document Style
- Body: Times New Roman, 12pt
- Headings: Bold, 16/14/12pt
- Line spacing: 1.5x
- First line indent: 2 characters
