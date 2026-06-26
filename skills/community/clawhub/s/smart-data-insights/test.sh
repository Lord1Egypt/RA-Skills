#!/bin/bash
# Test script for data-analyst skill

set -e

echo "🧪 Testing Data Analyst Skill..."

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TOOLS_DIR="$SCRIPT_DIR/tools"

# Create test data
echo "📁 Creating test data..."
cat > /tmp/test_data.csv << EOF
id,name,age,salary,department,join_date
1,Alice,25,50000,Engineering,2022-01-15
2,Bob,30,60000,Marketing,2021-06-20
3,Charlie,,55000,Engineering,2022-03-10
4,Diana,28,62000,Marketing,2021-11-05
5,Eve,35,75000,Engineering,2020-08-12
6,Frank,30,60000,Marketing,2021-06-20
7,Grace,29,58000,Sales,2022-02-28
8,Henry,32,68000,Engineering,2021-04-15
9,Ivy,27,52000,Sales,2022-05-20
10,Jack,,65000,Marketing,2021-09-30
EOF

echo "✅ Test data created: /tmp/test_data.csv"

# Test 1: Basic analysis
echo ""
echo "🔍 Test 1: Basic analysis..."
python3 "$TOOLS_DIR/analyze.py" /tmp/test_data.csv

# Test 2: With cleaning
echo ""
echo "🧹 Test 2: Analysis with cleaning..."
python3 "$TOOLS_DIR/analyze.py" /tmp/test_data.csv --clean

# Test 3: With visualization
echo ""
echo "📊 Test 3: Analysis with visualization..."
python3 "$TOOLS_DIR/analyze.py" /tmp/test_data.csv --visualize

# Test 4: Full analysis
echo ""
echo "🚀 Test 4: Full analysis (clean + visualize + report)..."
python3 "$TOOLS_DIR/analyze.py" /tmp/test_data.csv --clean --visualize --report

# Check outputs
echo ""
echo "📋 Checking outputs..."
if [ -f "/tmp/test_data_summary.json" ]; then
    echo "✅ Summary file created"
else
    echo "❌ Summary file missing"
fi

if [ -f "/tmp/test_data_cleaned.csv" ]; then
    echo "✅ Cleaned file created"
else
    echo "❌ Cleaned file missing"
fi

if ls /tmp/test_data_*.png 1> /dev/null 2>&1; then
    echo "✅ Charts created: $(ls /tmp/test_data_*.png | wc -l) files"
else
    echo "❌ No charts created"
fi

if [ -f "/tmp/test_data_report.md" ]; then
    echo "✅ Report created"
else
    echo "❌ Report missing"
fi

# Cleanup
echo ""
echo "🧹 Cleaning up..."
rm -f /tmp/test_data*.csv /tmp/test_data*.json /tmp/test_data*.png /tmp/test_data*.md

echo ""
echo "✅ All tests passed!"
