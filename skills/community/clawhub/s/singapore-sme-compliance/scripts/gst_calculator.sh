#!/bin/bash
# Singapore GST Calculator
# Usage: ./gst_calculator.sh <amount> [rate]

AMOUNT=${1:-0}
RATE=${2:-0.09}

if [ "$AMOUNT" = "0" ]; then
    echo "Usage: ./gst_calculator.sh <amount> [rate]"
    echo "Example: ./gst_calculator.sh 1000 0.09"
    exit 1
fi

# Calculate GST
GST=$(echo "$AMOUNT * $RATE" | bc -l)
TOTAL=$(echo "$AMOUNT + $GST" | bc -l)

echo "================================"
echo "Singapore GST Calculator"
echo "================================"
echo "Amount (excl. GST): S$ $(printf "%.2f" $AMOUNT)"
echo "GST Rate: $(echo "$RATE * 100" | bc -l)%"
echo "GST Amount: S$ $(printf "%.2f" $GST)"
echo "--------------------------------"
echo "Total (incl. GST): S$ $(printf "%.2f" $TOTAL)"
echo "================================"
