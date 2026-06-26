#!/bin/bash
# QR Code Tool - Generate and read QR codes
# Version: 1.0.0

QR_DIR="$(cd "$(dirname "$0")/../../.." && pwd)/qrcodes"
mkdir -p "$QR_DIR"

# Generate timestamp
get_timestamp() {
    date "+%Y%m%d_%H%M%S"
}

# Check dependencies
check_deps() {
    local missing=0
    
    if ! command -v qrencode &> /dev/null; then
        echo "⚠️  qrencode not installed"
        echo "   Install: brew install qrencode (Mac) or apt-get install qrencode (Linux)"
        missing=1
    fi
    
    if ! command -v zbarimg &> /dev/null; then
        echo "⚠️  zbar-tools not installed (for reading QR)"
        echo "   Install: brew install zbar (Mac) or apt-get install zbar-tools (Linux)"
        # Not critical, only needed for reading
    fi
    
    return $missing
}

# Generate QR code
generate_qr() {
    local content="$1"
    local output="$2"
    
    if [ -z "$content" ]; then
        echo "❌ No content provided"
        return 1
    fi
    
    if [ -z "$output" ]; then
        output="$QR_DIR/qr_$(get_timestamp).png"
    fi
    
    check_deps || return 1
    
    qrencode -o "$output" -s 10 -l M "$content"
    
    if [ $? -eq 0 ]; then
        echo "✅ QR Code Generated"
        echo "   Content: $content"
        echo "   File: $output"
        echo "   Size: 300x300 (approx)"
    else
        echo "❌ Failed to generate QR code"
        return 1
    fi
}

# Generate WiFi QR
generate_wifi_qr() {
    local ssid="$1"
    local password="$2"
    local encryption="${3:-WPA}"
    
    if [ -z "$ssid" ] || [ -z "$password" ]; then
        echo "❌ SSID and password required"
        return 1
    fi
    
    local content="WIFI:T:$encryption;S:$ssid;P:$password;;"
    local output="$QR_DIR/wifi_${ssid}_$(get_timestamp).png"
    
    generate_qr "$content" "$output"
    echo "   Type: WiFi ($encryption)"
}

# Generate vCard QR
generate_vcard() {
    local name="$1"
    local phone="$2"
    local email="$3"
    
    if [ -z "$name" ]; then
        echo "❌ Name required"
        return 1
    fi
    
    local content="BEGIN:VCARD
VERSION:3.0
N:$name
TEL:$phone
EMAIL:$email
END:VCARD"
    
    local output="$QR_DIR/contact_$(get_timestamp).png"
    generate_qr "$content" "$output"
    echo "   Type: vCard Contact"
}

# Read QR code
read_qr() {
    local image="$1"
    
    if [ ! -f "$image" ]; then
        echo "❌ Image not found: $image"
        return 1
    fi
    
    if ! command -v zbarimg &> /dev/null; then
        echo "❌ zbarimg not installed"
        echo "   Install: brew install zbar (Mac) or apt-get install zbar-tools (Linux)"
        return 1
    fi
    
    echo "📱 QR Code Content:"
    zbarimg -q "$image" 2>/dev/null
}

# Batch generate
batch_generate() {
    local input="$1"
    local output_dir="${2:-$QR_DIR}"
    
    if [ ! -f "$input" ]; then
        echo "❌ Input file not found: $input"
        return 1
    fi
    
    mkdir -p "$output_dir"
    
    local count=0
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        local output="$output_dir/qr_$(echo "$line" | md5sum | cut -c1-8).png"
        qrencode -o "$output" -s 10 -l M "$line" 2>/dev/null && ((count++))
    done < "$input"
    
    echo "✅ Batch Complete"
    echo "   Generated: $count QR codes"
    echo "   Output: $output_dir"
}

# Show help
show_help() {
    echo "QR Code Tool - Generate and read QR codes"
    echo ""
    echo "Usage:"
    echo "  qr.sh generate \"<text>\" [--output file.png]"
    echo "  qr.sh wifi \"<ssid>\" \"<password>\" [--encryption WPA]"
    echo "  qr.sh vcard \"<name>\" \"<phone>\" \"<email>\""
    echo "  qr.sh read \"<image.png>\""
    echo "  qr.sh batch \"<input.txt>\" [--output-dir ./qrcodes]"
    echo ""
}

# Main
case "$1" in
    generate)
        shift
        content=""
        output=""
        while [ $# -gt 0 ]; do
            case "$1" in
                --output)
                    output="$2"
                    shift 2
                    ;;
                *)
                    content="$content $1"
                    shift
                    ;;
            esac
        done
        content=$(echo "$content" | sed 's/^ *//')
        generate_qr "$content" "$output"
        ;;
    wifi)
        shift
        ssid=""
        password=""
        encryption="WPA"
        while [ $# -gt 0 ]; do
            case "$1" in
                --encryption)
                    encryption="$2"
                    shift 2
                    ;;
                *)
                    [ -z "$ssid" ] && ssid="$1" || [ -z "$password" ] && password="$1"
                    shift
                    ;;
            esac
        done
        generate_wifi_qr "$ssid" "$password" "$encryption"
        ;;
    vcard)
        generate_vcard "$2" "$3" "$4"
        ;;
    read)
        read_qr "$2"
        ;;
    batch)
        shift
        input=""
        output_dir="$QR_DIR"
        while [ $# -gt 0 ]; do
            case "$1" in
                --output-dir)
                    output_dir="$2"
                    shift 2
                    ;;
                *)
                    input="$1"
                    shift
                    ;;
            esac
        done
        batch_generate "$input" "$output_dir"
        ;;
    *)
        show_help
        ;;
esac
