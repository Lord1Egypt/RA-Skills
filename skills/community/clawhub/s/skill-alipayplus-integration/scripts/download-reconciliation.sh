#!/bin/bash
# download-reconciliation.sh
# Alipay+ Reconciliation File Auto-Download Script
# Usage: ./download-reconciliation.sh [DATE]

set -e

# ========== Configuration Area ==========
SFTP_USER="${SFTP_USER:-your_username}"
SFTP_HOST="${SFTP_HOST:-sftp.alipayplus.com}"
SFTP_KEY="${SFTP_KEY:-$HOME/.ssh/alipayplus_sftp}"
PARTICIPANT_ID="${PARTICIPANT_ID:-ACQP123}"  # Your Participant ID
SETTLEMENT_CURRENCY="${SETTLEMENT_CURRENCY:-USD}"  # Settlement Currency
ENV="${ENV:-production}"  # production or sandbox
LOCAL_DIR="${LOCAL_DIR:-$HOME/.openclaw/workspace/alipayplus-reconciliation}"

# ========== Function Definitions ==========

usage() {
    echo "Usage: $0 [DATE]"
    echo ""
    echo "Arguments:"
    echo "  DATE    Download date (format: YYYYMMDD), defaults to yesterday"
    echo ""
    echo "Environment Variables:"
    echo "  SFTP_USER         SFTP username (default: your_username)"
    echo "  SFTP_HOST         SFTP host (default: sftp.alipayplus.com)"
    echo "  SFTP_KEY          SSH private key path (default: ~/.ssh/alipayplus_sftp)"
    echo "  PARTICIPANT_ID    Participant ID (default: ACQP123)"
    echo "  SETTLEMENT_CURRENCY Settlement currency (default: USD)"
    echo "  ENV               Environment: production|sandbox (default: production)"
    echo "  LOCAL_DIR         Local save directory (default: ~/alipayplus-reconciliation)"
    echo ""
    echo "Examples:"
    echo "  $0                    # Download yesterday's reconciliation files"
    echo "  $0 20240331            # Download reconciliation files for specified date"
    echo "  ENV=sandbox $0        # Download from sandbox environment"
    exit 1
}

log_info() {
    echo "ℹ️  $1"
}

log_success() {
    echo "✅ $1"
}

log_error() {
    echo "❌ Error: $1" >&2
}

check_dependencies() {
    if ! command -v sftp &> /dev/null; then
        log_error "sftp command not found. Please install openssh-client first."
        exit 1
    fi
    
    if [ ! -f "$SFTP_KEY" ]; then
        log_error "SSH private key not found: $SFTP_KEY"
        echo "Please configure SFTP_KEY environment variable or create the key file."
        exit 1
    fi
}

download_files() {
    local date=$1
    local sftp_root
    
    # Set root directory based on environment
    if [ "$ENV" = "sandbox" ]; then
        sftp_root="/sandbox"
        log_info "Using sandbox environment"
    else
        sftp_root="/v1"
        log_info "Using production environment"
    fi
    
    local date_dir="$LOCAL_DIR/$date"
    mkdir -p "$date_dir"
    
    log_info "Starting reconciliation file download ($date)..."
    echo ""
    
    # Download settlement files
    log_info "  [1/3] Downloading settlement files..."
    if sftp -i "$SFTP_KEY" -b - "$SFTP_USER@$SFTP_HOST" << EOF
cd ${sftp_root}/settlements/settlement/${PARTICIPANT_ID}/${date}
get settlement_${PARTICIPANT_ID}_${SETTLEMENT_CURRENCY}_*.csv ${date_dir}/
bye
EOF
    then
        log_success "Settlement files downloaded"
    else
        log_error "Failed to download settlement files"
    fi
    echo ""
    
    # Download transaction files (detail + summary) and fee files
    log_info "  [2/3] Downloading transaction detail files..."
    if sftp -i "$SFTP_KEY" -b - "$SFTP_USER@$SFTP_HOST" << EOF
cd ${sftp_root}/settlements/clearing/${PARTICIPANT_ID}/${date}
get transactionItems_${PARTICIPANT_ID}_${SETTLEMENT_CURRENCY}_*.csv ${date_dir}/
bye
EOF
    then
        log_success "Transaction detail files downloaded"
    else
        log_error "Failed to download transaction detail files"
    fi
    echo ""
    
    log_info "  [3/3] Downloading transaction summary and fee files..."
    if sftp -i "$SFTP_KEY" -b - "$SFTP_USER@$SFTP_HOST" << EOF
cd ${sftp_root}/settlements/clearing/${PARTICIPANT_ID}/${date}
get summary_${PARTICIPANT_ID}_${SETTLEMENT_CURRENCY}_*.csv ${date_dir}/
get feeItems_${PARTICIPANT_ID}_${SETTLEMENT_CURRENCY}_*.csv ${date_dir}/
bye
EOF
    then
        log_success "Transaction summary and fee files downloaded"
    else
        log_error "Failed to download transaction summary or fee files"
    fi
    echo ""
    
    # Show download results
    log_success "Reconciliation files downloaded to: $date_dir"
    echo ""
    echo "📂 File list:"
    ls -lh "$date_dir"
    echo ""
    
    # Count files
    local file_count=$(find "$date_dir" -name "*.csv" | wc -l | tr -d ' ')
    echo "Total files downloaded: $file_count"
}

# ========== Main Program ==========

main() {
    # Show help
    if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
        usage
    fi
    
    # Check dependencies
    check_dependencies
    
    # Determine download date
    local download_date
    if [ -n "$1" ]; then
        download_date="$1"
        log_info "Using specified date: $download_date"
    else
        download_date=$(date -d "yesterday" +%Y%m%d)
        log_info "Using default date (yesterday): $download_date"
    fi
    
    echo ""
    echo "=========================================="
    echo "Alipay+ Reconciliation File Download"
    echo "=========================================="
    echo "Participant ID: $PARTICIPANT_ID"
    echo "Settlement Currency: $SETTLEMENT_CURRENCY"
    echo "Environment: $ENV"
    echo "Download Date: $download_date"
    echo "Save Directory: $LOCAL_DIR"
    echo "=========================================="
    echo ""
    
    # Download files
    download_files "$download_date"
    
    echo ""
    echo "💡 Tips:"
    echo "  - Use reconciliation.sh script for reconciliation comparison"
    echo "  - File location: $LOCAL_DIR/$download_date"
}

main "$@"
