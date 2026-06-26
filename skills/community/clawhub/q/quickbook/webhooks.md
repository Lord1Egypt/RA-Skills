# QuickBooks Online Webhooks Reference

## Payload Format (CloudEvents v1.0)
Webhooks are delivered as an array of JSON objects following the CloudEvents specification:
```json
[
  {
    "specversion": "1.0",
    "id": "88cd52aa-33b6-4351-9aa4-47572edbd068",
    "source": "intuit.dsnBgbseACLLRZNxo2dfc4evmEJdxde58xeeYcZliOU=",
    "type": "qbo.invoice.created.v1",
    "datacontenttype": "application/json",
    "time": "2026-05-31T21:31:25.179Z",
    "intuitentityid": "95",
    "intuitaccountid": "310687",
    "data": {}
  }
]
```

## Signature Verification (Python)
Verify the cryptographic signature passed in the `intuit-signature` header using HMAC-SHA256 with your secure Verifier Token.

```python
import hmac
import hashlib
import base64

def verify_webhook_signature(raw_payload: bytes, verifier_token: str, received_signature: str) -> bool:
    """
    Validates the HMAC-SHA256 signature of a QuickBooks Online webhook.
    :param raw_payload: The raw, unparsed UTF-8 request body bytes.
    :param verifier_token: The verifier token from the Intuit Developer Portal.
    :param received_signature: The value of the 'intuit-signature' header.
    :return: True if the signature is valid, False otherwise.
    """
    # Create HMAC-SHA256 hash using the verifier token as the key
    hmac_hash = hmac.new(
        verifier_token.encode('utf-8'),
        raw_payload,
        hashlib.sha256
    ).digest()
    
    # Base64 encode the resulting hash
    calculated_signature = base64.b64encode(hmac_hash).decode('utf-8')
    
    # Securely compare signatures to prevent timing attacks
    return hmac.compare_digest(calculated_signature, received_signature)
```

## Best Practices
1.  **3-Second Timeout:** Your endpoint must respond with an `HTTP 200 OK` status code within **3 seconds** of receiving the payload.
2.  **Asynchronous Processing:** Never perform database operations, API calls, or complex business logic synchronously within your webhook handler. Write the payload to a message queue (e.g., Redis, RabbitMQ, or AWS SQS) and return `200 OK` immediately.
3.  **Idempotency:** Webhook notifications are guaranteed to be delivered *at least once*. Ensure your processing queue tracks the unique `id` of each CloudEvent to prevent duplicate processing.
