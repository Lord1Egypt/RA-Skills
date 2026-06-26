#!/bin/bash
# reconciliation.sh
# Alipay+ Reconciliation File Parsing and Discrepancy Detection Script
# Usage: ./reconciliation.sh

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
RECONCILE_DIR="$HOME/.openclaw/workspace/alipayplus-reconciliation"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ========== Function Definitions ==========

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if file exists and is readable
check_file() {
    local file=$1
    if [ ! -f "$file" ]; then
        print_error "File does not exist: $file"
        return 1
    fi
    if [ ! -r "$file" ]; then
        print_error "File is not readable: $file"
        return 1
    fi
    return 0
}

# Parse transaction file
parse_transaction_file() {
    local file=$1
    local output_file=$2
    
    print_info "Parsing transaction file: $file"
    
    if ! check_file "$file"; then
        return 1
    fi
    
    # Extract key fields: tradeNo, outTradeNo, amount, status
    awk -F',' 'NR>1 {print $2","$3","$5","$9}' "$file" > "$output_file"
    
    local count=$(wc -l < "$output_file" | tr -d ' ')
    print_success "Parsed $count transaction records"
}

# Parse fee file
parse_fee_file() {
    local file=$1
    local output_file=$2
    
    print_info "Parsing fee file: $file"
    
    if ! check_file "$file"; then
        return 1
    fi
    
    # Extract key fields: tradeNo, outTradeNo, feeAmount
    awk -F',' 'NR>1 {print $2","$3","$4}' "$file" > "$output_file"
    
    local count=$(wc -l < "$output_file" | tr -d ' ')
    print_success "Parsed $count fee records"
}

# Compare with local orders
compare_orders() {
    local transaction_file=$1
    local local_order_file=$2
    
    print_info "Comparing with local orders..."
    
    if ! check_file "$transaction_file"; then
        return 1
    fi
    
    if [ ! -f "$local_order_file" ]; then
        print_warning "Local order file does not exist: $local_order_file"
        print_info "Creating empty local order file..."
        touch "$local_order_file"
    fi
    
    # Find orders that exist locally but not in Alipay+ (missing transactions)
    print_info "Finding missing transactions..."
    comm -23 <(sort "$local_order_file") <(sort "$transaction_file") > "${RECONCILE_DIR}/missing_in_alipay.txt"
    
    # Find orders that exist in Alipay+ but not locally (extra transactions)
    print_info "Finding extra transactions..."
    comm -13 <(sort "$local_order_file") <(sort "$transaction_file") > "${RECONCILE_DIR}/extra_in_alipay.txt"
    
    # Find orders with amount discrepancies
    print_info "Finding amount discrepancies..."
    join -t',' -j 2 <(sort -t',' -k2 "$local_order_file") <(sort -t',' -k2 "$transaction_file") | \
        awk -F',' '$3 != $5 {print $0}' > "${RECONCILE_DIR}/amount_mismatch.txt"
    
    # Generate statistics
    echo ""
    print_header "Reconciliation Results"
    
    local missing_count=$(wc -l < "${RECONCILE_DIR}/missing_in_alipay.txt" | tr -d ' ')
    local extra_count=$(wc -l < "${RECONCILE_DIR}/extra_in_alipay.txt" | tr -d ' ')
    local mismatch_count=$(wc -l < "${RECONCILE_DIR}/amount_mismatch.txt" | tr -d ' ')
    
    echo "Missing in Alipay+:  $missing_count"
    echo "Extra in Alipay+:    $extra_count"
    echo "Amount mismatch:     $mismatch_count"
    echo ""
    
    if [ $missing_count -gt 0 ] || [ $extra_count -gt 0 ] || [ $mismatch_count -gt 0 ]; then
        print_warning "Discrepancies detected! Please review the reports."
    else
        print_success "All orders reconciled successfully!"
    fi
}

# Generate reconciliation report
generate_report() {
    local report_date=$1
    local report_file="${RECONCILE_DIR}/reconciliation_report_${report_date}.txt"
    
    print_info "Generating reconciliation report..."
    
    {
        echo "========================================"
        echo "Alipay+ Reconciliation Report"
        echo "========================================"
        echo "Report Date: $(date)"
        echo "Reconciliation Date: $report_date"
        echo ""
        echo "----------------------------------------"
        echo "Summary"
        echo "----------------------------------------"
        echo "Missing in Alipay+: $(wc -l < "${RECONCILE_DIR}/missing_in_alipay.txt" | tr -d ' ')"
        echo "Extra in Alipay+: $(wc -l < "${RECONCILE_DIR}/extra_in_alipay.txt" | tr -d ' ')"
        echo "Amount Mismatch: $(wc -l < "${RECONCILE_DIR}/amount_mismatch.txt" | tr -d ' ')"
        echo ""
        
        if [ -s "${RECONCILE_DIR}/missing_in_alipay.txt" ]; then
            echo "----------------------------------------"
            echo "Missing in Alipay+ (Top 10)"
            echo "----------------------------------------"
            head -10 "${RECONCILE_DIR}/missing_in_alipay.txt"
            echo ""
        fi
        
        if [ -s "${RECONCILE_DIR}/extra_in_alipay.txt" ]; then
            echo "----------------------------------------"
            echo "Extra in Alipay+ (Top 10)"
            echo "----------------------------------------"
            head -10 "${RECONCILE_DIR}/extra_in_alipay.txt"
            echo ""
        fi
        
        if [ -s "${RECONCILE_DIR}/amount_mismatch.txt" ]; then
            echo "----------------------------------------"
            echo "Amount Mismatch (Top 10)"
            echo "----------------------------------------"
            head -10 "${RECONCILE_DIR}/amount_mismatch.txt"
            echo ""
        fi
        
        echo "========================================"
        echo "End of Report"
        echo "========================================"
    } > "$report_file"
    
    print_success "Report generated: $report_file"
    echo ""
    cat "$report_file"
}

# Download reconciliation files
download_reconciliation() {
    # Check if download script exists
    local download_script="$SCRIPT_DIR/download-reconciliation.sh"
    
    if [ -x "$download_script" ]; then
        print_info "Calling automated download script..."
        echo ""
        "$download_script" "$@"
    else
        print_warning "Download script not found or not executable: $download_script"
        echo ""
        print_info "Manual download instructions:"
        echo "   - Alipay+ SFTP Server"
        echo "   - Alipay+ Partner Workspace (https://workspace.alipayplus.com)"
        echo ""
        echo "Or run:"
        echo "  $download_script"
        echo ""
    fi
}

# Show main menu
show_menu() {
    echo ""
    echo "========================================"
    echo "Alipay+ Reconciliation Tool"
    echo "========================================"
    echo ""
    echo "  1) Download reconciliation files"
    echo "  2) Parse reconciliation files"
    echo "  3) Compare with local orders"
    echo "  4) Generate reconciliation report"
    echo "  5) View discrepancy details"
    echo "  0) Exit"
    echo ""
    echo "========================================"
}

# ========== Main Program ==========

main() {
    # Create working directory
    mkdir -p "$RECONCILE_DIR"
    
    while true; do
        show_menu
        
        read -p "Select an option (0-5): " choice
        
        case $choice in
            1)
                print_header "Download Reconciliation Files"
                
                read -p "Enter reconciliation date (YYYYMMDD, press Enter for yesterday): " date_arg
                
                if [ -z "$date_arg" ]; then
                    download_reconciliation
                else
                    download_reconciliation "$date_arg"
                fi
                ;;
                
            2)
                print_header "Parse Reconciliation Files"
                
                read -p "Enter date directory (YYYYMMDD): " date_dir
                local file_path="${RECONCILE_DIR}/${date_dir}"
                
                # List available files
                echo ""
                print_info "Available files in $file_path:"
                ls -1 "$file_path" 2>/dev/null || print_error "Directory not found"
                echo ""
                
                read -p "Enter transaction file name: " trans_file
                read -p "Enter fee file name (or press Enter to skip): " fee_file
                
                parse_transaction_file "${file_path}/${trans_file}" "${RECONCILE_DIR}/parsed_transactions.csv"
                
                if [ -n "$fee_file" ]; then
                    parse_fee_file "${file_path}/${fee_file}" "${RECONCILE_DIR}/parsed_fees.csv"
                fi
                ;;
                
            3)
                print_header "Compare with Local Orders"
                
                read -p "Enter parsed transaction file path: " trans_file
                read -p "Enter local order file path: " local_file
                
                compare_orders "$trans_file" "$local_file"
                ;;
                
            4)
                print_header "Generate Reconciliation Report"
                
                read -p "Enter reconciliation date (YYYYMMDD): " report_date
                generate_report "$report_date"
                ;;
                
            5)
                print_header "View Discrepancy Details"
                
                echo ""
                echo "  1) Missing in Alipay+"
                echo "  2) Extra in Alipay+"
                echo "  3) Amount Mismatch"
                echo ""
                read -p "Select discrepancy type (1-3): " dtype
                
                case $dtype in
                    1)
                        echo ""
                        print_info "Missing in Alipay+:"
                        cat "${RECONCILE_DIR}/missing_in_alipay.txt"
                        ;;
                    2)
                        echo ""
                        print_info "Extra in Alipay+:"
                        cat "${RECONCILE_DIR}/extra_in_alipay.txt"
                        ;;
                    3)
                        echo ""
                        print_info "Amount Mismatch:"
                        cat "${RECONCILE_DIR}/amount_mismatch.txt"
                        ;;
                    *)
                        print_error "Invalid option"
                        ;;
                esac
                ;;
                
            0)
                print_info "Exiting..."
                exit 0
                ;;
                
            *)
                print_error "Invalid option. Please select 0-5."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
