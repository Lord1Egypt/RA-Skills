# Alipay+ Webhook Configuration Guide

## Overview

Alipay+ delivers payment results in real-time via Webhooks (asynchronous notifications). Proper Webhook configuration is critical for ensuring order status synchronization. This is for ACQP integration only.

---

## Webhook Types

### 1. Payment Notification (payment.notify)
- **Trigger**: Payment success/failure
- **Delivery**: Immediate push + retry mechanism
- **Priority**: High (basis for order status updates)

---

## Configuration Steps

### Step 1: Prepare Webhook Server

**Requirements:**
- Publicly accessible HTTPS endpoint
- Valid SSL certificate
- POST request support
- Response time < 5 seconds

**Example Configuration (Nginx):**
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location /alipayplus/notify {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 2: Configure Webhook URL

1. **Specify the paymentNotifyUrl parameter in the pay API.**
2. **Edit the Notification URL in the Applications > Settings section in Alipay+ Developer Center.**

- **Notify URL**: `https://your-domain.com/alipayplus/notify`

### Step 3: Implement Webhook Receiving Interface

**Java Spring Boot Example:**

See complete implementation in [Java Webhook Implementation](#java-webhook-implementation)

---

## Notification Format

### Payment Notification Example

```json
{
 "acquirerId": "1111088000000000000",
 "pspId": "1022172000000000000",
 "paymentResult": {
 "resultCode": "SUCCESS",
 "resultStatus": "S",
 "resultMessage": "success"
 },
 "paymentRequestId": "pay_1089760038715669_102775745070000",
 "paymentId": "20200101234567890130000",
 "mppPaymentId": "pay_1089760038715670_102775745070001",
 "paymentTime": "2020-01-01T12:01:01+08:30",
 "paymentAmount": {
 "value": "100",
 "currency": "JPY"
 },
 "customerId": "1230000",
 "walletBrandName": "walletName",
 "settlementAmount": {
 "value": "74",
 "currency": "USD"
 },
 "settlementQuote": {
 "quoteCurrencyPair": "USD/JPY",
 "quoteExpiryTime": "2021-06-02T13:15:48+08:00",
 "quoteId": "046793306919858814",
 "quotePrice": "1.35",
 "quoteStartTime": "2021-05-30T13:15:48+08:00"
 }
}
```

### Field Descriptions

| Field | Type | Description |
|------|------|------|
| `acquirerId` | String | Acquirer ID |
| `pspId` | String | Payment Service Provider ID |
| `paymentResult` | Object | Payment result |
| `paymentResult.resultCode` | String | Result code (SUCCESS/FAIL) |
| `paymentResult.resultStatus` | String | Result status (S/F) |
| `paymentResult.resultMessage` | String | Result message |
| `paymentRequestId` | String | Payment request ID |
| `paymentId` | String | Payment ID |
| `mppPaymentId` | String | MPP Payment ID |
| `paymentTime` | String | Payment time (ISO 8601) |
| `paymentAmount` | Object | Payment amount |
| `paymentAmount.value` | String | Amount value |
| `paymentAmount.currency` | String | Currency code |
| `customerId` | String | Customer ID |
| `walletBrandName` | String | Wallet brand name |
| `settlementAmount` | Object | Settlement amount |
| `settlementQuote` | Object | Settlement exchange rate info |

---

## Java Webhook Implementation

### Complete Spring Boot Example

```java
import org.springframework.web.bind.annotation.*;
import org.springframework.http.*;
import org.springframework.stereotype.*;
import com.fasterxml.jackson.databind.*;
import com.fasterxml.jackson.annotation.*;
import lombok.extern.slf4j.*;
import lombok.*;

import java.security.*;
import java.security.spec.*;
import java.util.*;
import java.util.concurrent.*;
import java.nio.charset.*;
import java.time.*;
import java.util.Base64;

@RestController
@RequestMapping("/alipayplus")
@Slf4j
public class AlipayPlusWebhookController {
    
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final PublicKey alipayPublicKey;
    private final ConcurrentHashMap<String, Boolean> processedEvents = new ConcurrentHashMap<>();
    
    // Webhook notification model
    @JsonIgnoreProperties(ignoreUnknown = true)
    @Data
    public static class WebhookNotification {
        private String eventId;
        private String eventType;
        private String eventTime;
        private String notifyTime;
        private String acquirerId;
        private String pspId;
        private PaymentResult paymentResult;
        private String paymentRequestId;
        private String paymentId;
        private String mppPaymentId;
        private String paymentTime;
        private PaymentAmount paymentAmount;
        private String customerId;
        private String walletBrandName;
        private PaymentAmount settlementAmount;
        private SettlementQuote settlementQuote;
    }
    
    @JsonIgnoreProperties(ignoreUnknown = true)
    @Data
    public static class PaymentResult {
        private String resultCode;
        private String resultStatus;
        private String resultMessage;
    }
    
    @JsonIgnoreProperties(ignoreUnknown = true)
    @Data
    public static class PaymentAmount {
        private String value;
        private String currency;
    }
    
    @JsonIgnoreProperties(ignoreUnknown = true)
    @Data
    public static class SettlementQuote {
        private String quoteCurrencyPair;
        private String quoteExpiryTime;
        private String quoteId;
        private String quotePrice;
        private String quoteStartTime;
    }
    
    // Signature header model
    @Data
    public static class SignatureHeader {
        private String algorithm;
        private String keyVersion;
        private String signature;
    }
    
    public AlipayPlusWebhookController(
            @Value("${alipayplus.public-key-path}") String publicKeyPath) throws Exception {
        this.alipayPublicKey = loadPublicKey(publicKeyPath);
    }
    
    /**
     * Handle payment notification
     */
    @PostMapping("/notify/payment")
    public ResponseEntity<String> handlePaymentNotification(
            @RequestBody String requestBody,
            @RequestHeader("Client-Id") String clientId,
            @RequestHeader("Request-Time") String requestTime,
            @RequestHeader("Signature") String signatureHeader,
            HttpServletRequest request) {
        
        try {
            // 1. Parse signature header
            SignatureHeader sigHeader = parseSignatureHeader(signatureHeader);
            
            // 2. Verify signature
            String requestUri = request.getRequestURI();
            String contentToValidate = buildContentToValidate(
                request.getMethod(), requestUri, clientId, requestTime, requestBody);
            
            boolean isValid = verifySignature(
                sigHeader.getSignature(), 
                contentToValidate, 
                alipayPublicKey);
            
            if (!isValid) {
                log.error("❌ Signature verification failed");
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body("FAIL: Invalid signature");
            }
            
            // 3. Parse notification
            WebhookNotification notification = objectMapper.readValue(
                requestBody, WebhookNotification.class);
            
            // 4. Check idempotency
            if (processedEvents.containsKey(notification.getEventId())) {
                log.info("⚠️  Duplicate notification, eventId: {}", notification.getEventId());
                return ResponseEntity.ok("SUCCESS");
            }
            
            // 5. Validate basic fields
            if (!"SUCCESS".equals(notification.getPaymentResult().getResultCode()) ||
                !"S".equals(notification.getPaymentResult().getResultStatus())) {
                log.warn("⚠️  Payment failed: {}", 
                    notification.getPaymentResult().getResultMessage());
                // Still return SUCCESS to prevent retry, handle failure asynchronously
                markAsProcessed(notification.getEventId());
                return ResponseEntity.ok("SUCCESS");
            }
            
            // 6. Process notification asynchronously
            processPaymentAsync(notification);
            
            // 7. Mark as processed and return success
            markAsProcessed(notification.getEventId());
            log.info("✅ Payment notification processed successfully: {}", 
                notification.getPaymentRequestId());
            
            return ResponseEntity.ok("SUCCESS");
            
        } catch (Exception e) {
            log.error("❌ Error processing webhook", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("FAIL: " + e.getMessage());
        }
    }
    
    /**
     * Parse signature header
     * Format: algorithm=RSA256,keyVersion=0,signature=<signature>
     */
    private SignatureHeader parseSignatureHeader(String signatureHeader) {
        SignatureHeader header = new SignatureHeader();
        String[] parts = signatureHeader.split(",");
        
        for (String part : parts) {
            String[] kv = part.split("=", 2);
            if (kv.length == 2) {
                switch (kv[0].trim()) {
                    case "algorithm":
                        header.setAlgorithm(kv[1].trim());
                        break;
                    case "keyVersion":
                        header.setKeyVersion(kv[1].trim());
                        break;
                    case "signature":
                        header.setSignature(kv[1].trim());
                        break;
                }
            }
        }
        
        return header;
    }
    
    /**
     * Build content to be validated
     * Format: <HTTP-METHOD> <Request-URI>\n<Client-Id>.<Request-Time>.<Request-Body>
     */
    private String buildContentToValidate(String method, String uri, 
                                          String clientId, String requestTime, 
                                          String requestBody) {
        return method + " " + uri + "\n" + clientId + "." + requestTime + "." + requestBody;
    }
    
    /**
     * Verify RSA256 signature
     */
    private boolean verifySignature(String signature, String content, PublicKey publicKey) 
            throws Exception {
        try {
            Signature sig = Signature.getInstance("SHA256withRSA");
            sig.initVerify(publicKey);
            sig.update(content.getBytes(StandardCharsets.UTF_8));
            
            byte[] signatureBytes = Base64.getDecoder().decode(signature);
            return sig.verify(signatureBytes);
            
        } catch (Exception e) {
            log.error("Signature verification error", e);
            return false;
        }
    }
    
    /**
     * Load RSA public key from file
     */
    private PublicKey loadPublicKey(String publicKeyPath) throws Exception {
        String publicKeyPEM = new String(Files.readAllBytes(Paths.get(publicKeyPath)))
            .replace("-----BEGIN PUBLIC KEY-----", "")
            .replace("-----END PUBLIC KEY-----", "")
            .replaceAll("\\s+", "");
        
        byte[] publicKeyBytes = Base64.getDecoder().decode(publicKeyPEM);
        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(publicKeyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        return keyFactory.generatePublic(keySpec);
    }
    
    /**
     * Mark event as processed
     */
    private void markAsProcessed(String eventId) {
        processedEvents.put(eventId, true);
        log.debug("Marked event as processed: {}", eventId);
    }
    
    /**
     * Process payment notification asynchronously
     */
    private void processPaymentAsync(WebhookNotification notification) {
        // Use async executor or message queue in production
        CompletableFuture.runAsync(() -> {
            try {
                log.info("🔄 Processing payment: {}", notification.getPaymentRequestId());
                
                // Business logic here:
                // 1. Update order status in database
                // 2. Send confirmation email/SMS
                // 3. Trigger fulfillment process
                // 4. Update inventory
                // 5. Log for auditing
                
                log.info("✅ Payment processed: {}", notification.getPaymentRequestId());
                
            } catch (Exception e) {
                log.error("❌ Error in async payment processing", e);
                // Implement retry logic or alerting here
            }
        });
    }
    
    /**
     * Cleanup old processed events (call periodically)
     */
    @Scheduled(fixedRate = 3600000) // Every hour
    public void cleanupProcessedEvents() {
        int initialSize = processedEvents.size();
        // Keep only last 24 hours of events
        processedEvents.entrySet().removeIf(entry -> {
            // In production, store timestamp with eventId
            return false; // Simplified for example
        });
        log.info("Cleaned up processed events: {} -> {}", initialSize, processedEvents.size());
    }
}
```

### Application Configuration

```yaml
# application.yml
alipayplus:
  public-key-path: /path/to/alipayplus_public_key.pem
  webhook:
    endpoint: /alipayplus/notify/payment
    timeout-seconds: 5

server:
  port: 8080
  servlet:
    context-path: /
```

### Maven Dependencies

```xml
<dependencies>
    <!-- Spring Boot Web -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <version>3.2.3</version>
    </dependency>
    
    <!-- Lombok -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>1.18.30</version>
        <scope>provided</scope>
    </dependency>
    
    <!-- Jackson for JSON -->
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.16.1</version>
    </dependency>
</dependencies>
```

---

## Retry Mechanism

### Alipay+ Retry Policy

If Alipay+ does not receive the required response (**`result.resultStatus = S`** and **`result.resultCode = SUCCESS`**), Alipay+ will resend the asynchronous notifications within **24 hours 22 minutes** for up to **7 times** until the correct response is received.

**Retry Intervals:**

| Retry Attempt | Interval | Cumulative Time |
|---------|---------|---------|
| 1 | Immediate | 0 minutes |
| 2 | 2 minutes | 2 minutes |
| 3 | 10 minutes | 12 minutes |
| 4 | 10 minutes | 22 minutes |
| 5 | 1 hour | 1 hour 22 minutes |
| 6 | 2 hours | 3 hours 22 minutes |
| 7 | 6 hours | 9 hours 22 minutes |
| 8 | 15 hours | 24 hours 22 minutes |

### Success Response Requirements

All of the following conditions must be met for Alipay+ to consider the notification successfully delivered:

- **HTTP Status Code**: `200`
- **Response Body**: Contains `SUCCESS`
- **Response Time**: < 5 seconds

### Conditions That Trigger Retry

- HTTP status code is not 200
- Response timeout (> 5 seconds)
- Connection failure
- Response body does not contain `SUCCESS`

### ⚠️ Important Notes

1. **Idempotency Must Be Implemented**: Due to the retry mechanism, the same notification may be pushed multiple times. You must deduplicate using `eventId` or `paymentRequestId`
2. **Fast Response**: Return `SUCCESS` first, then process business logic asynchronously to avoid timeout
3. **24-Hour Window**: Alipay+ will stop retrying after 24 hours 22 minutes if no successful response is received

---

## Security Recommendations

### 1. Signature Verification
**Must verify** signatures on all Webhook notifications to prevent forged requests.

**Verification Steps:**

1. **Construct the Content_To_Be_Validated:**
   ```
   Content_To_Be_Validated = <HTTP-METHOD> <Request-URI>\n<Client-Id>.<Request-Time>.<Request-Body>
   ```
   - `Request-URI`: Webhook API endpoint path

2. **Extract target_signature from notify request header:**
   ```
   Signature: algorithm=RSA256,keyVersion=0,signature=<target_signature>
   ```

3. **Validate the signature:**
   ```
   IS_SIGNATURE_VALID = sha256withrsa_verify(
     base64UrlDecode(<target_signature>),
     <Content_To_Be_Validated>,
     <serverPublicKey>
   )
   ```

**Code Example:**
```java
// Must verify signature
SignatureHeader sigHeader = parseSignatureHeader(signatureHeader);
String contentToValidate = buildContentToValidate(method, uri, clientId, requestTime, requestBody);
boolean isValid = verifySignature(sigHeader.getSignature(), contentToValidate, alipayPublicKey);

if (!isValid) {
    log.error("❌ Signature verification failed");
    return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("FAIL: Invalid signature");
}
```

### 2. Idempotency Handling
**Must implement** idempotency to prevent duplicate processing.

**Java Example:**
```java
// Check if already processed
if (processedEvents.containsKey(eventId)) {
    log.info("⚠️  Duplicate notification, eventId: {}", eventId);
    return ResponseEntity.ok("SUCCESS");
}

// Process notification
processPaymentAsync(notification);

// Mark as processed
markAsProcessed(eventId);
```

**Database-backed Idempotency (Production):**
```java
@Service
public class IdempotencyService {
    
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    public boolean isProcessed(String eventId) {
        String sql = "SELECT COUNT(*) FROM webhook_events WHERE event_id = ?";
        Integer count = jdbcTemplate.queryForObject(sql, Integer.class, eventId);
        return count != null && count > 0;
    }
    
    public void markAsProcessed(String eventId, String payload) {
        String sql = "INSERT INTO webhook_events (event_id, payload, created_at) VALUES (?, ?, NOW())";
        jdbcTemplate.update(sql, eventId, payload);
    }
}
```

### 3. Rate Limiting
Prevent malicious requests:

**Java Spring Boot Example:**
```java
import org.springframework.web.bind.annotation.*;
import io.github.bucket4j.*;

@RestController
@RequestMapping("/alipayplus")
public class RateLimitedController {
    
    private final Bandwidth limit = Bandwidth.classic(100, Refill.intervally(100, Duration.ofMinutes(1)));
    private final ConcurrentHashMap<String, Bucket> buckets = new ConcurrentHashMap<>();
    
    private Bucket getBucket(String ip) {
        return buckets.computeIfAbsent(ip, k -> Bucket4j.builder()
            .addLimit(limit)
            .build());
    }
    
    @PostMapping("/notify/payment")
    public ResponseEntity<String> handleNotification(
            @RequestBody String body,
            HttpServletRequest request) {
        
        String ip = request.getRemoteAddr();
        Bucket bucket = getBucket(ip);
        
        if (!bucket.tryConsume(1)) {
            log.warn("⚠️  Rate limit exceeded for IP: {}", ip);
            return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS).body("FAIL: Rate limit exceeded");
        }
        
        // Process notification...
        return ResponseEntity.ok("SUCCESS");
    }
}
```

**Maven Dependency:**
```xml
<dependency>
    <groupId>com.github.vladimir-bukhtoyarov</groupId>
    <artifactId>bucket4j-core</artifactId>
    <version>7.6.0</version>
</dependency>
```


### 4. IP Whitelist
If Alipay+ provides fixed IPs, configure firewall whitelist.

**Java Example:**
```java
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    
    @Value("${alipayplus.allowed-ips}")
    private List<String> allowedIps;
    
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .antMatcher("/alipayplus/**")
            .authorizeRequests()
            .requestMatchers(new IpAddressMatcher("192.168.1.0/24")).permitAll()
            .anyRequest().denyAll();
    }
}
```

### 5. Logging
Log all Webhook requests for auditing and troubleshooting:

**Java Example (with SLF4J + Logback):**
```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

@Slf4j
@RestController
@RequestMapping("/alipayplus")
public class WebhookController {
    
    private static final Logger logger = LoggerFactory.getLogger(WebhookController.class);
    
    @PostMapping("/notify/payment")
    public ResponseEntity<String> handleNotification(
            @RequestBody WebhookNotification notification,
            @RequestHeader("Client-Id") String clientId) {
        
        // Add MDC context for structured logging
        MDC.put("eventId", notification.getEventId());
        MDC.put("paymentRequestId", notification.getPaymentRequestId());
        MDC.put("clientId", clientId);
        
        try {
            logger.info("📨 Webhook received: eventType={}, paymentRequestId={}", 
                notification.getEventType(), 
                notification.getPaymentRequestId());
            
            // Process notification...
            
            logger.info("✅ Webhook processed successfully");
            return ResponseEntity.ok("SUCCESS");
            
        } catch (Exception e) {
            logger.error("❌ Webhook processing failed", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("FAIL");
            
        } finally {
            MDC.clear();
        }
    }
}
```

**Logback Configuration (logback-spring.xml):**
```xml
<configuration>
    <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="net.logstash.logback.encoder.LogstashEncoder">
            <includeMdc>true</includeMdc>
            <mdcFieldNames>
                <eventId>eventId</eventId>
                <paymentRequestId>paymentRequestId</paymentRequestId>
            </mdcFieldNames>
        </encoder>
    </appender>
    
    <logger name="com.yourcompany.alipayplus" level="INFO"/>
    
    <root level="INFO">
        <appender-ref ref="JSON"/>
    </root>
</configuration>
```

**Maven Dependency for JSON Logging:**
```xml
<dependency>
    <groupId>net.logstash.logback</groupId>
    <artifactId>logstash-logback-encoder</artifactId>
    <version>7.4</version>
</dependency>
```

---

## Debugging Tools

### Local Testing (ngrok)

```bash
# Start ngrok
ngrok http 8080

# Configure the generated URL as notify_url
# Example: https://abc123.ngrok.io/alipayplus/notify
```

### Using Debug Scripts

```bash
# Start local Webhook server
bash ~/.openclaw/skills/alipayplus-integration/scripts/debug-notify.sh

# Select option 1: Start local Webhook server
# Or option 2: Start tunnel
```

### Replay Testing

```bash
# Select option 3: Replay test notification
# Enter target URL and notification content for testing
```

---

## FAQ

### Q1: Not receiving notifications?

**Troubleshooting Steps:**
1. Check if notify_url is publicly accessible
2. Check if HTTPS certificate is valid
3. Check if firewall rules allow traffic
4. Check Alipay+ platform notification logs
5. Test using ngrok

### Q2: Signature verification failed?

**Troubleshooting Steps:**
1. Confirm the correct public key is used
2. Confirm Content_To_Be_Validated format is correct: `<HTTP-METHOD> <Request-URI>\n<Client-Id>.<Request-Time>.<Request-Body>`
3. Confirm target_signature is correctly extracted from `Signature` header
4. Confirm `Client-Id` and `Request-Time` headers are correctly retrieved
5. Confirm Request-URI is the webhook API endpoint path
6. Use debugging tools to verify

### Q3: Duplicate notifications?

**Solution:**
- Implement idempotency handling, deduplicate using eventId
- Record processed eventId
- Return SUCCESS directly for duplicate notifications

### Q4: Response timeout?

**Solution:**
- Optimize processing logic for faster response
- Process notifications asynchronously, return SUCCESS first
- Increase server resources

---

## Monitoring and Alerts

### Monitoring Metrics
- Webhook reception success rate
- Average response time
- Signature failure count
- Duplicate notification count

### Alert Configuration
- Signature failures > 10 per hour
- Response timeouts > 5 per hour
- Notification backlog > 100

---

**Last Updated**: 2026-03-31  
**Status**: Draft
