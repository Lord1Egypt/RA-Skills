# Alipay+ Signature Guide

## Overview

Alipay+ uses RSA2 signature algorithm to ensure the security of requests and notifications. All API requests and asynchronous notifications require signature verification.

---

## Signature Algorithm

- **Algorithm**: RSA2 (RSA with SHA-256)
- **Key Length**: 2048 bits or higher
- **Character Encoding**: UTF-8
- **Signature Format**: Base64Url

---

## Request Signature Process

### Step 1: Build Content To Be Signed

**Syntax:**
```
<HTTP-METHOD> <Request-URI>
<Client-Id>.<Request-Time>.<Request-Body>
```

**Components:**
| Component | Description |
|-----------|-------------|
| `HTTP-METHOD` | HTTP method (GET, POST, PUT, DELETE, etc.) |
| `Request-URI` | Request path (e.g., `/aps/api/v1/payments/pay`) |
| `Client-Id` | Your Client ID (e.g., `SANDBOX_5YC47N2ZQHJ004124`) |
| `Request-Time` | ISO 8601 timestamp (e.g., `2025-02-20T08:51:49.09Z`) |
| `Request-Body` | Raw JSON request body (no whitespace/line breaks) |

**Example:**

Request details:
- **Request-URI**: `/aps/api/v1/payments/pay`
- **Client-Id**: `SANDBOX_5YC47N2ZQHJ004124`
- **Request-Time**: `2025-02-20T08:51:49.09Z`
- **Request-Body**:
```json
{
 "order":{
 "orderId":"OrderID_0101010101",
 "orderDescription":"sample_order",
 "orderAmount":{
 "value":"100",
 "currency":"JPY"
 }
 },
 "paymentAmount":{
 "value":"100",
 "currency":"JPY"
 },
 "paymentFactor": {
 "isInStorePayment": "true"
 } 
}
```

**Content To Be Signed:**
```
POST /aps/api/v1/payments/pay
SANDBOX_5YC47N2ZQHJ004124.2025-02-20T08:51:49.09Z.{"order":{"orderId":"OrderID_0101010101","orderDescription":"sample_order","orderAmount":{"value":"100","currency":"JPY"}},"paymentAmount":{"value":"100","currency":"JPY"},"paymentFactor":{"isInStorePayment":"true"}}
```

**Important Notes:**
1. The request body must be compact JSON (no extra whitespace or line breaks)
2. The format is exactly: `<METHOD> <URI>\n<ClientId>.<Time>.<Body>`
3. There is a newline character (`\n`) between the URI line and the Client-Id line
4. Request-Time must be in ISO 8601 format with timezone (Z for UTC)

### Step 2: Generate Signature

```
generatedSignature = base64UrlEncode(sha256withrsa(<Content_To_Be_Signed>, <privateKey>))
```

**Using OpenSSL:**
```bash
# Sign the content
echo -n "<Content_To_Be_Signed>" | openssl dgst -sha256 -sign private_key.pem | base64 | tr '+/' '-_' | tr -d '='
```

**Using Java:**
```java
import java.security.*;
import java.nio.file.*;
import java.util.Base64;

public class SignatureUtil {
    
    public static String generateSignature(String content, String privateKeyPath) throws Exception {
        String privateKey = new String(Files.readAllBytes(Paths.get(privateKeyPath)));
        Signature sign = Signature.getInstance("SHA256withRSA");
        sign.initSign(getPrivateKey(privateKey));
        sign.update(content.getBytes("UTF-8"));
        byte[] signatureBytes = sign.sign();
        // Convert to Base64Url
        return Base64.getUrlEncoder().withoutPadding().encodeToString(signatureBytes);
    }
    
    private static PrivateKey getPrivateKey(String privateKey) throws Exception {
        String pem = privateKey.replace("-----BEGIN PRIVATE KEY-----", "")
                               .replace("-----END PRIVATE KEY-----", "")
                               .replaceAll("\\s", "");
        KeySpec keySpec = new PKCS8EncodedKeySpec(Base64.getDecoder().decode(pem));
        return KeyFactory.getInstance("RSA").generatePrivate(keySpec);
    }
}
```

### Step 3: Add Signature to Request Headers

```http
POST /aps/api/v1/payments/pay HTTP/1.1
Host: openapi.alipayplus.com
Content-Type: application/json
Client-Id: SANDBOX_5YC47N2ZQHJ004124
Request-Time: 2025-02-20T08:51:49.09Z
Signature: algorithm=RSA256,keyVersion=1,signature=<Base64Url-encoded signature>
```

**Required Headers:**
| Header | Description |
|--------|-------------|
| `Client-Id` | Your Client ID |
| `Request-Time` | Request timestamp (ISO 8601) |
| `Signature` | Composite signature header with format: `algorithm=<algorithm>,keyVersion=<key-version>,signature=<Base64Url-encoded signature>` |

**Signature Header Components:**
| Component | Description | Example |
|-----------|-------------|---------|
| `algorithm` | Signature algorithm | `RSA256` |
| `keyVersion` | Key version number | `1` |
| `signature` | Base64Url-encoded signature | `abc123...` |

---

## Response/Webhook Verification

### Step 1: Get Response Content

Get the raw JSON content from the HTTP response body.

### Step 2: Extract Signature

Extract the signature from the response header:
```http
Signature: algorithm=RSA256,keyVersion=0,signature=<target_signature>
```

**Parse the Signature Header:**
```java
// Parse Signature header value
String signatureHeader = "algorithm=RSA256,keyVersion=0,signature=abc123...";
String[] parts = signatureHeader.split(",");
Map<String, String> signatureObj = new HashMap<>();
for (String part : parts) {
    String[] kv = part.split("=", 2);
    if (kv.length == 2) {
        signatureObj.put(kv[0], kv[1]);
    }
}
// signatureObj = { algorithm=RSA256, keyVersion=0, signature=abc123... }

String targetSignature = signatureObj.get("signature"); // This is the signature to be validated
```

### Step 3: Build Content To Be Validated

**Syntax:**
```
<HTTP-METHOD> <Response-URI>
<Client-Id>.<Response-Time>.<Response-Body>
```

**Components:**
| Component | Description |
|-----------|-------------|
| `HTTP-METHOD` | HTTP method (GET, POST, PUT, DELETE, etc.) |
| `Response-URI` | Response path (e.g., `/aps/api/v1/payments/inquiryPayment`) |
| `Client-Id` | Your Client ID (e.g., `SANDBOX_5YC47N2ZQHJ004124`) |
| `Response-Time` | ISO 8601 timestamp from response |
| `Response-Body` | Raw JSON response body (no whitespace/line breaks) |

**Example:**

Response details:
- **HTTP Method**: `POST`
- **Response-URI**: `/aps/api/v1/payments/inquiryPayment`
- **Client-Id**: `SANDBOX_5YC47N2ZQHJ004124`
- **Response-Time**: `2025-02-21T05:43:09Z`
- **Response-Body**:
```json
{
 "result":{
 "resultCode":"ORDER_NOT_EXIST",
 "resultMessage":"Order does not exist.",
 "resultStatus":"F"
 }
}
```

**Content To Be Validated:**
```
POST /aps/api/v1/payments/inquiryPayment
SANDBOX_5YC47N2ZQHJ004124.2025-02-21T05:43:09Z.{"result":{"resultCode":"ORDER_NOT_EXIST","resultMessage":"Order does not exist.","resultStatus":"F"}}
```

**Important Notes:**
1. The response body must be compact JSON (no extra whitespace or line breaks)
2. The format is exactly: `<METHOD> <URI>\n<ClientId>.<Time>.<Body>`
3. There is a newline character (`\n`) between the URI line and the Client-Id line
4. Response-Time must be in ISO 8601 format with timezone (Z for UTC)

### Step 4: Validate the Signature

Use the `sha256withrsa_verify` method to validate the signature:

**Syntax:**
```
IS_SIGNATURE_VALID = sha256withrsa_verify(
  base64UrlDecode(<target_signature>),
  <Content_To_Be_Validated>,
  <serverPublicKey>
)
```

**Using OpenSSL:**
```bash
# Validate the signature
echo -n "<Content_To_Be_Validated>" | openssl dgst -sha256 -verify server_public_key.pem -signature <(echo "<target_signature>" | base64 -d)
```

**Using Java:**
```java
import java.security.*;
import java.util.Base64;

public class SignatureUtil {
    
    public static boolean validateSignature(String targetSignature, String content, String serverPublicKey) throws Exception {
        // Convert Base64Url to Base64
        String base64Sig = targetSignature.replace("-", "+").replace("_", "/");
        
        Signature verify = Signature.getInstance("SHA256withRSA");
        verify.initVerify(getPublicKey(serverPublicKey));
        verify.update(content.getBytes("UTF-8"));
        
        return verify.verify(Base64.getDecoder().decode(base64Sig));
    }
    
    private static PublicKey getPublicKey(String publicKey) throws Exception {
        String pem = publicKey.replace("-----BEGIN PUBLIC KEY-----", "")
                              .replace("-----END PUBLIC KEY-----", "")
                              .replaceAll("\\s", "");
        KeySpec keySpec = new X509EncodedKeySpec(Base64.getDecoder().decode(pem));
        return KeyFactory.getInstance("RSA").generatePublic(keySpec);
    }
}
```

**Validation Result:**
- `true` / `Verified OK` - Signature is valid
- `false` / `Verification Failure` - Signature is invalid

---

## Code Examples

### Java - Complete Request with Signature Header

```java
import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.security.*;
import java.security.spec.*;
import java.time.*;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;

public class AlipayPlusClient {
    
    private final String clientId;
    private final String privateKey;
    private final String publicKey;
    private final ObjectMapper objectMapper;
    
    public AlipayPlusClient(String clientId, String privateKeyPath, String publicKeyPath) throws Exception {
        this.clientId = clientId;
        this.privateKey = new String(Files.readAllBytes(Paths.get(privateKeyPath)));
        this.publicKey = new String(Files.readAllBytes(Paths.get(publicKeyPath)));
        this.objectMapper = new ObjectMapper();
    }
    
    // Build content to be signed
    public String buildContent(String method, String uri, String requestTime, Object body) throws Exception {
        String compactBody = objectMapper.writeValueAsString(body);
        return method + " " + uri + "\n" + clientId + "." + requestTime + "." + compactBody;
    }
    
    // Generate Base64Url signature
    public String sign(String method, String uri, String requestTime, Object body) throws Exception {
        String content = buildContent(method, uri, requestTime, body);
        Signature sign = Signature.getInstance("SHA256withRSA");
        sign.initSign(getPrivateKey(privateKey));
        sign.update(content.getBytes("UTF-8"));
        byte[] signatureBytes = sign.sign();
        // Convert to Base64Url
        return Base64.getUrlEncoder().withoutPadding().encodeToString(signatureBytes);
    }
    
    // Build Signature header value
    public String buildSignatureHeader(String signature) {
        return "algorithm=RSA256,keyVersion=1,signature=" + signature;
    }
    
    // Make API request
    public Map<String, Object> request(String method, String uri, Object body) throws Exception {
        String requestTime = Instant.now().toString();
        String signature = sign(method, uri, requestTime, body);
        String signatureHeader = buildSignatureHeader(signature);
        
        URL url = new URL("https://openapi.alipayplus.com" + uri);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod(method);
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setRequestProperty("Client-Id", clientId);
        conn.setRequestProperty("Request-Time", requestTime);
        conn.setRequestProperty("Signature", signatureHeader);
        conn.setDoOutput(true);
        
        // Write request body
        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = objectMapper.writeValueAsString(body).getBytes("UTF-8");
            os.write(input, 0, input.length);
        }
        
        // Read response
        StringBuilder response = new StringBuilder();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(conn.getInputStream(), "UTF-8"))) {
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
        }
        
        // Verify response signature
        String responseSignature = conn.getHeaderField("Signature");
        boolean isValid = verify(method, uri, requestTime, response.toString(), responseSignature);
        
        conn.disconnect();
        
        Map<String, Object> result = new HashMap<>();
        result.put("data", objectMapper.readValue(response.toString(), Map.class));
        result.put("signatureValid", isValid);
        return result;
    }
    
    // Verify signature from response/webhook
    public boolean verify(String method, String uri, String requestTime, String body, String signatureHeader) throws Exception {
        // Parse Signature header
        String[] parts = signatureHeader.split(",");
        Map<String, String> signatureObj = new HashMap<>();
        for (String part : parts) {
            String[] kv = part.split("=", 2);
            if (kv.length == 2) {
                signatureObj.put(kv[0], kv[1]);
            }
        }
        
        String content = buildContent(method, uri, requestTime, body);
        Signature verifier = Signature.getInstance("SHA256withRSA");
        verifier.initVerify(getPublicKey(publicKey));
        verifier.update(content.getBytes("UTF-8"));
        
        // Convert Base64Url back to Base64
        String base64Sig = signatureObj.get("signature").replace("-", "+").replace("_", "/");
        
        return verifier.verify(Base64.getDecoder().decode(base64Sig));
    }
    
    private static PrivateKey getPrivateKey(String privateKey) throws Exception {
        String pem = privateKey.replace("-----BEGIN PRIVATE KEY-----", "")
                               .replace("-----END PRIVATE KEY-----", "")
                               .replaceAll("\\s", "");
        KeySpec keySpec = new PKCS8EncodedKeySpec(Base64.getDecoder().decode(pem));
        return KeyFactory.getInstance("RSA").generatePrivate(keySpec);
    }
    
    private static PublicKey getPublicKey(String publicKey) throws Exception {
        String pem = publicKey.replace("-----BEGIN PUBLIC KEY-----", "")
                              .replace("-----END PUBLIC KEY-----", "")
                              .replaceAll("\\s", "");
        KeySpec keySpec = new X509EncodedKeySpec(Base64.getDecoder().decode(pem));
        return KeyFactory.getInstance("RSA").generatePublic(keySpec);
    }
    
    // Usage
    public static void main(String[] args) {
        try {
            AlipayPlusClient client = new AlipayPlusClient(
                "SANDBOX_5YC47N2ZQHJ004124",
                "./private_key.pem",
                "./alipayplus_public_key.pem"
            );
            
            Map<String, Object> body = new HashMap<>();
            Map<String, Object> order = new HashMap<>();
            order.put("orderId", "OrderID_0101010101");
            order.put("orderDescription", "sample_order");
            Map<String, String> orderAmount = new HashMap<>();
            orderAmount.put("value", "100");
            orderAmount.put("currency", "JPY");
            order.put("orderAmount", orderAmount);
            body.put("order", order);
            
            Map<String, String> paymentAmount = new HashMap<>();
            paymentAmount.put("value", "100");
            paymentAmount.put("currency", "JPY");
            body.put("paymentAmount", paymentAmount);
            
            Map<String, String> paymentFactor = new HashMap<>();
            paymentFactor.put("isInStorePayment", "true");
            body.put("paymentFactor", paymentFactor);
            
            Map<String, Object> response = client.request("POST", "/aps/api/v1/payments/pay", body);
            System.out.println("Response: " + response);
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### Java Signature Example

```java
import java.security.*;
import java.security.spec.*;
import java.util.*;
import javax.crypto.*;
import java.util.Base64;

public class AlipayPlusSignUtil {
    
    // Generate Signature
    public static String sign(String content, String privateKey) throws Exception {
        PrivateKey priKey = getPrivateKey(privateKey);
        Signature signature = Signature.getInstance("SHA256withRSA");
        signature.initSign(priKey);
        signature.update(content.getBytes("UTF-8"));
        return Base64.getEncoder().encodeToString(signature.sign());
    }
    
    // Verify Signature
    public static boolean verify(String content, String signature, String publicKey) throws Exception {
        PublicKey pubKey = getPublicKey(publicKey);
        Signature sig = Signature.getInstance("SHA256withRSA");
        sig.initVerify(pubKey);
        sig.update(content.getBytes("UTF-8"));
        return sig.verify(Base64.getDecoder().decode(signature));
    }
    
    private static PrivateKey getPrivateKey(String privateKey) throws Exception {
        KeySpec keySpec = new PKCS8EncodedKeySpec(
            Base64.getDecoder().decode(privateKey)
        );
        return KeyFactory.getInstance("RSA").generatePrivate(keySpec);
    }
    
    private static PublicKey getPublicKey(String publicKey) throws Exception {
        KeySpec keySpec = new X509EncodedKeySpec(
            Base64.getDecoder().decode(publicKey)
        );
        return KeyFactory.getInstance("RSA").generatePublic(keySpec);
    }
}
```

---

## FAQ

### Q1: Signature Verification Failed?

**Possible Causes:**
1. Key mismatch - Ensure the correct private/public key pair is used
2. Character encoding issue - Ensure UTF-8 encoding is used
3. Parameter sorting error - Ensure parameters are sorted by ASCII code
4. Null parameter handling - Null parameters should not participate in signing
5. Special character escaping - Ensure special characters are handled correctly

**Troubleshooting Steps:**
```bash
# 1. Print the content to be signed
echo "Content to be signed: $sign_string"

# 2. Test signature with OpenSSL
echo -n "$sign_string" | openssl dgst -sha256 -sign private_key.pem | base64

# 3. Compare the generated signature
```

### Q2: How to Debug Signature Issues?

**Debugging Tools:**
```bash
# Test using script
bash ~/.openclaw/skills/alipayplus-integration/scripts/test-signature.sh
```

### Q3: How to handle Certificate Mode?

In certificate mode, you need to include the certificate in the request:
```http
Client-Certificate: <Base64-encoded certificate content>
```

The signature process remains the same, but verification requires validating the certificate first.

---

## Security Best Practices

1. **Private Key Storage**: Never commit private keys to code repositories; use a key management service (KMS)
2. **Key Rotation**: Rotate keys periodically, recommended every 6 months
3. **Certificate Monitoring**: Monitor certificate expiration and renew 30 days in advance
4. **Signature Logging**: Log signature and verification activities for troubleshooting
5. **Alert on Failures**: Trigger alerts on signature verification failures - may indicate security issues

---

**Last Updated**: 2026-03-31  
**Status**: Initial Draft
