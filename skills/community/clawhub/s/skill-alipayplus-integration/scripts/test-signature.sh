#!/bin/bash
# Alipay+ Signature Testing Tool

set -e

echo "🔐 Alipay+ Signature Testing Tool"
echo "================================="
echo ""

# Check OpenSSL
if ! command -v openssl &> /dev/null; then
  echo "✗ OpenSSL not installed. Please install:"
  echo "  macOS: brew install openssl"
  echo "  Ubuntu: sudo apt-get install openssl"
  exit 1
fi

echo "✓ OpenSSL installed"
echo ""

# Select test type
echo "Please select test type:"
echo "1. Generate test signature"
echo "2. Verify asynchronous notification signature"
echo "3. Generate RSA key pair (for testing)"
echo "4. Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
  1)
    echo ""
    echo "=== Generate Test Signature ==="
    echo ""
    read -p "Enter the string to be signed: " sign_content
    read -p "Enter private key file path (or press Enter to use default): " private_key_file
    private_key_file=${private_key_file:-$HOME/.openclaw/workspace/alipayplus_private_key.pem}

    if [ ! -f "$private_key_file" ]; then
      echo "✗ Private key file does not exist: $private_key_file"
      echo "  Please run option 3 first to generate test keys, or specify the correct private key file path"
      exit 1
    fi

    # Generate signature
    signature=$(echo -n "$sign_content" | openssl dgst -sha256 -sign "$private_key_file" | base64 -w 0)

    echo ""
    echo "✅ Signature result:"
    echo "$signature"
    echo ""
    echo "📝 Please add the signature to the X-Alipayplus-Signature header field"
    ;;
    
  2)
    echo ""
    echo "=== Verify Asynchronous Notification Signature ==="
    echo ""
    read -p "Enter the original asynchronous notification content: " notify_content
    read -p "Enter the signature value: " signature
    read -p "Enter Alipay+ public key file path (or press Enter to use default): " public_key_file
    public_key_file=${public_key_file:-$HOME/.openclaw/workspace/alipayplus_public_key.pem}

    if [ ! -f "$public_key_file" ]; then
      echo "✗ Public key file does not exist: $public_key_file"
      echo "  Please specify the correct public key file path"
      exit 1
    fi

    # Verify signature
    echo "$signature" | base64 -d > /tmp/verify_signature.bin
    verify_result=$(echo -n "$notify_content" | openssl dgst -sha256 -verify "$public_key_file" -signature /tmp/verify_signature.bin 2>&1) || true

    rm -f /tmp/verify_signature.bin

    if [[ "$verify_result" == *"Verified OK"* ]]; then
      echo ""
      echo "✅ Signature verification passed!"
    else
      echo ""
      echo "✗ Signature verification failed"
      echo "  Error message: $verify_result"
      echo ""
      echo "🔍 Possible causes:"
      echo "  1. Incorrect public key"
      echo "  2. Signature content has been tampered with"
      echo "  3. Incorrect signature format"
    fi
    ;;
    
  3)
    echo ""
    echo "=== Generate RSA Key Pair (for testing) ==="
    echo ""

    private_key_file="$HOME/.openclaw/workspace/alipayplus_private_key.pem"
    public_key_file="$HOME/.openclaw/workspace/alipayplus_public_key.pem"

    # Generate private key
    openssl genrsa -out "$private_key_file" 2048
    echo "✅ Private key generated: $private_key_file"

    # Generate public key
    openssl rsa -in "$private_key_file" -pubout -out "$public_key_file"
    echo "✅ Public key generated: $public_key_file"

    echo ""
    echo "⚠️  Note: This key pair is for testing only. For production, please use the official keys issued by Alipay+."
    echo ""
    echo "📝 Private key content (please keep it secure):"
    echo "----------------------------------------"
    cat "$private_key_file"
    echo "----------------------------------------"
    echo ""
    echo "📝 Public key content (for configuration):"
    echo "----------------------------------------"
    cat "$public_key_file"
    echo "----------------------------------------"
    ;;
    
  4)
    echo "Exiting"
    exit 0
    ;;

  *)
    echo "✗ Invalid choice"
    exit 1
    ;;
esac

echo ""
