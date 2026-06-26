#!/bin/bash
# Alipay+ Configuration Generation Script
# Generates configuration files consistent with the references/config-template.json structure

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$HOME/.openclaw/workspace"

echo "🔧 Alipay+ Configuration Generation Tool"
echo "========================================"
echo ""

# Select role
echo "Please select role type:"
echo "1. ACQP (Acquirer Service Provider)"
echo "2. MPP (Mobile Payment Provider)"
read -p "Enter your choice (1/2): " role_choice

case $role_choice in
  1)
    role="ACQP"
    echo "✓ Selected: ACQP (Acquirer Service Provider)"
    ;;
  2)
    role="MPP"
    echo "✓ Selected: MPP (Mobile Payment Provider)"
    ;;
  *)
    echo "✗ Invalid choice, defaulting to ACQP"
    role="ACQP"
    ;;
esac

# Select environment
echo ""
echo "Please select environment:"
echo "1. Sandbox"
echo "2. Production"
read -p "Enter your choice (1/2): " env_choice

case $env_choice in
  1)
    environment="sandbox"
    baseUrl="https://open-sea-global.alipayplus.com"
    echo "✓ Selected: Sandbox environment"
    ;;
  2)
    environment="production"
    baseUrl="https://open-sea-global.alipayplus.com"
    echo "✓ Selected: Production environment"
    ;;
  *)
    echo "✗ Invalid choice, defaulting to Sandbox"
    environment="sandbox"
    baseUrl="https://open-sea-global.alipayplus.com"
    ;;
esac

# Get user input
echo ""
echo "Please enter configuration information (press Enter to use default values):"
echo ""
read -p "Partner ID: " partner_id
partner_id=${partner_id:-YOUR_PARTNER_ID}

read -p "Client ID: " client_id
client_id=${client_id:-YOUR_CLIENT_ID}

echo ""
echo "📝 Key Configuration:"
echo "  Tip: You can replace with actual keys in the configuration file later"
echo "  Private key file path (optional): "
read -p "  Private key file path: " private_key_path

echo ""
echo "🔔 Webhook Configuration (ACQP mode):"
# ACQP receives notify URL at its own address, this is a sample
if [ "$role" = "ACQP" ]; then
  echo "  ACQP mode requires configuring the Webhook receiving address"
  read -p "  Webhook Notify URL: " webhook_notify_url
  webhook_notify_url=${webhook_notify_url:-https://your-domain.com/alipayplus/acqp/notifyPayment}
else
  webhook_notify_url=""
fi

echo ""
echo "🚪 Gateway Configuration:"
read -p "  Partner Base URL: " partner_base_url
partner_base_url=${partner_base_url:-YOUR_BASE_URL}

# MPP mode: Generate full URLs for each mppEndpoints API; MPP endpoints are configured by MPP itself, this is a sample
if [ "$role" = "MPP" ]; then
  echo ""
  echo "📍 MPP Gateway Endpoints (based on Partner Base URL):"

  mpp_pay_url="${partner_base_url}/alipayplus/mpp/pay"
  mpp_inquiry_payment_url="${partner_base_url}/alipayplus/mpp/inquiryPayment"
  mpp_cancel_payment_url="${partner_base_url}/alipayplus/mpp/cancelPayment"
  mpp_refund_url="${partner_base_url}/alipayplus/mpp/refund"
  mpp_apply_token_url="${partner_base_url}/alipayplus/mpp/applyToken"

  echo "  ✓ mpp.pay: $mpp_pay_url"
  echo "  ✓ mpp.inquiryPayment: $mpp_inquiry_payment_url"
  echo "  ✓ mpp.cancelPayment: $mpp_cancel_payment_url"
  echo "  ✓ mpp.refund: $mpp_refund_url"
  echo "  ✓ mpp.applyToken: $mpp_apply_token_url"
fi

echo ""
echo "💱 Business Configuration:"
read -p "  Default currency (default: USD): " currency
currency=${currency:-USD}

read -p "  Request timeout (milliseconds, default: 30000): " timeout
timeout=${timeout:-30000}

read -p "  Retry times (default: 3): " retry_times
retry_times=${retry_times:-3}

# 生成配置文件
config_file="$WORKSPACE_DIR/alipayplus-config.json"

cat > "$config_file" << EOF
{
  "alipayplus": {
    "environment": "$environment",
    "role": "$role",
    "partnerId": "$partner_id",
    "clientId": "$client_id",
    "credentials": {
      "privateKey": "-----BEGIN RSA PRIVATE KEY-----\\nYOUR_PRIVATE_KEY_HERE\\n-----END RSA PRIVATE KEY-----",
      "alipayPlusPublicKey": "-----BEGIN PUBLIC KEY-----\\nALIPAY_PLUS_PUBLIC_KEY_HERE\\n-----END PUBLIC KEY-----"
    },
    "endpoints": {
      "baseUrl": "$baseUrl",
      "acqp": {
        "payments": {
          "pay": "/aps/api/v1/payments/pay",
          "inquiryPayment": "/aps/api/v1/payments/inquiryPayment",
          "cancelPayment": "/aps/api/v1/payments/cancelPayment",
          "refund": "/aps/api/v1/payments/refund"
        },
        "merchants": {
          "registration": "/aps/api/v1/merchants/registration",
          "inquiryRegistrationStatus": "/aps/api/v1/merchants/inquiryRegistrationStatus"
        },
        "disputes": {
          "responseRetrieval": "/aps/api/v1/disputes/responseRetrieval",
          "responseEscalation": "/aps/api/v1/disputes/responseEscalation"
        }
      },
      "mpp": {
        "payments": {
          "notifyPayment": "/aps/api/v1/payments/notifyPayment",
          "userInitiatedPay": "/aps/api/v1/payments/userInitiatedPay"
        },
        "codes": {
          "getPaymentCode": "/aps/api/v1/codes/getPaymentCode"
        }
      }
    },
    "webhooks": {
      "acqp": {
        "notifyPayment": "/alipayplus/acqp/notifyPayment",
        "notifyRegistrationStatus": "/alipayplus/acqp/notifyRegistrationStatus",
        "initiateRetrieval": "/alipayplus/acqp/initiateRetrieval",
        "initiateEscalation": "/alipayplus/acqp/initiateEscalation"
      },
      "verifySignature": true
    },
    "gateway": {
      "partnerBaseUrl": "$partner_base_url",
      "mpp": {
        "pay": "${partner_base_url}/alipayplus/mpp/pay",
        "inquiryPayment": "${partner_base_url}/alipayplus/mpp/inquiryPayment",
        "cancelPayment": "${partner_base_url}/alipayplus/mpp/cancelPayment",
        "refund": "${partner_base_url}/alipayplus/mpp/refund",
        "applyToken": "${partner_base_url}/alipayplus/mpp/applyToken"
      },
      "verifySignature": true
    },
    "signConfig": {
      "signType": "RSA2",
      "signAlgorithm": "SHA256withRSA",
      "charset": "UTF-8",
      "format": "JSON",
      "version": "1.0",
      "signatureFormat": "Base64Url",
      "keyLength": 2048
    },
    "business": {
      "currency": "$currency",
      "timeout": $timeout,
      "retryTimes": $retry_times
    }
  }
}
EOF

echo ""
echo "✅ Configuration file generated: $config_file"
echo ""
echo "⚠️  Pending tasks:"
echo "  1. Replace YOUR_PRIVATE_KEY_HERE with your application private key"
echo "  2. Replace ALIPAY_PLUS_PUBLIC_KEY_HERE with the Alipay+ public key"
if [ -n "$private_key_path" ] && [ "$private_key_path" != "" ]; then
  echo "  3. Private key file recorded: $private_key_path"
fi
echo ""
echo "📚 Next steps:"
echo "  - Run test-signature.sh to test signatures"
echo "  - Run debug-notify.sh to test asynchronous notifications"
echo ""
echo "📖 Reference materials:"
echo "  - references/config-template.json (configuration template)"
echo "  - references/signature-reference.md (signature documentation)"
echo "  - references/webhook-reference.md (webhook documentation, ACQP only)"
echo ""
