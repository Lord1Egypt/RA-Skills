---
name: translateflow-api
description: "AI-powered translation services using TranslateFlow API - translation, translate text, language conversion, multilingual translation, language translation, document translation, website translation, content localization, real-time translation, batch translation, professional translation, machine translation, neural translation, automatic translation, text translation, instant translation, multi-language support, localization services, international content, global content, cross-language communication, foreign language translation, language conversion tool, translation automation, and intelligent language processing for any text or content translation needs."
---

# TranslateFlow API Skill

Professional AI-powered translation services using VCG's TranslateFlow API - high-quality neural translation supporting 100+ languages with context awareness and domain specialization.

## Quick Start

1. **Get API Key**: Help user sign up for free TranslateFlow API key
2. **Store Key**: Save the key securely 
3. **Translate Content**: Single text, batch documents, or real-time translation

## API Key Signup

### Step 1: Get User's Email
Ask the user for their email address to create a free TranslateFlow account.

### Step 2: Sign Up via API
```bash
curl -X POST https://translateflow.vosscg.com/v1/keys \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

**Expected Response:**
```json
{
  "api_key": "tf_fedcba0987654321",
  "message": "API key created successfully",
  "tier": "free",
  "supported_languages": 120,
  "daily_limit": "10000 characters"
}
```

### Step 3: Store the API Key
Save the API key securely for future use. Instruct the user to keep it safe.

## Core Translation Features

### Simple Text Translation
```bash
curl -X POST https://translateflow.vosscg.com/v1/translate \
  -H "X-API-Key: tf_fedcba0987654321" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you today?",
    "source_language": "en",
    "target_language": "es",
    "quality": "high"
  }'
```

**Expected Response:**
```json
{
  "translated_text": "Hola, ¿cómo estás hoy?",
  "source_language": "en",
  "target_language": "es",
  "confidence": 0.98,
  "characters_used": 25,
  "remaining_daily": 9975
}
```

### Auto-Detect Language
```bash
curl -X POST https://translateflow.vosscg.com/v1/translate \
  -H "X-API-Key: tf_fedcba0987654321" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bonjour, comment allez-vous?",
    "source_language": "auto",
    "target_language": "en"
  }'
```

**Expected Response:**
```json
{
  "translated_text": "Hello, how are you?",
  "source_language_detected": "fr",
  "target_language": "en",
  "confidence": 0.96,
  "detection_confidence": 0.99
}
```

### Batch Translation
```bash
curl -X POST https://translateflow.vosscg.com/v1/translate/batch \
  -H "X-API-Key: tf_fedcba0987654321" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Welcome to our website",
      "Contact us for more information",
      "Thank you for your purchase"
    ],
    "source_language": "en",
    "target_language": "de",
    "preserve_formatting": true
  }'
```

**Expected Response:**
```json
{
  "translations": [
    {
      "index": 0,
      "original": "Welcome to our website",
      "translated": "Willkommen auf unserer Website",
      "confidence": 0.97
    },
    {
      "index": 1,
      "original": "Contact us for more information", 
      "translated": "Kontaktieren Sie uns für weitere Informationen",
      "confidence": 0.95
    },
    {
      "index": 2,
      "original": "Thank you for your purchase",
      "translated": "Vielen Dank für Ihren Kauf",
      "confidence": 0.98
    }
  ],
  "total_characters": 89,
  "batch_processing_time": "1.2s"
}
```

### Document Translation
```bash
curl -X POST https://translateflow.vosscg.com/v1/documents/translate \
  -H "X-API-Key: tf_fedcba0987654321" \
  -F "file=@document.pdf" \
  -F "source_language=en" \
  -F "target_language=fr" \
  -F "preserve_layout=true"
```

**Expected Response:**
```json
{
  "document_id": "doc_12345",
  "status": "processing",
  "estimated_completion": "2-5 minutes",
  "download_url": "https://translateflow.vosscg.com/v1/documents/doc_12345/download",
  "original_pages": 5,
  "detected_language": "en"
}
```

### Specialized Domain Translation
```bash
curl -X POST https://translateflow.vosscg.com/v1/translate/specialized \
  -H "X-API-Key: tf_fedcba0987654321" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The patient presents with acute myocardial infarction requiring immediate intervention.",
    "source_language": "en",
    "target_language": "es",
    "domain": "medical",
    "terminology": "technical"
  }'
```

**Expected Response:**
```json
{
  "translated_text": "El paciente presenta infarto agudo de miocardio que requiere intervención inmediata.",
  "domain": "medical",
  "technical_terms_translated": 3,
  "confidence": 0.99,
  "medical_accuracy_score": 0.97
}
```

## Supported Languages

### Get Language List
```bash
curl -X GET https://translateflow.vosscg.com/v1/languages \
  -H "X-API-Key: tf_fedcba0987654321"
```

**Popular Language Pairs:**
- English ↔ Spanish (en ↔ es)
- English ↔ French (en ↔ fr)  
- English ↔ German (en ↔ de)
- English ↔ Chinese (en ↔ zh)
- English ↔ Japanese (en ↔ ja)
- English ↔ Portuguese (en ↔ pt)
- English ↔ Italian (en ↔ it)
- English ↔ Russian (en ↔ ru)
- English ↔ Arabic (en ↔ ar)
- And 100+ more languages

## Advanced Features

### Context-Aware Translation
```bash
curl -X POST https://translateflow.vosscg.com/v1/translate/contextual \
  -H "X-API-Key: tf_fedcba0987654321" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Book the flight",
    "source_language": "en",
    "target_language": "es",
    "context": {
      "domain": "travel",
      "situation": "booking_travel",
      "tone": "formal"
    }
  }'
```

### Real-time Translation
```bash
curl -X POST https://translateflow.vosscg.com/v1/translate/realtime \
  -H "X-API-Key: tf_fedcba0987654321" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Can you help me find the nearest restaurant?",
    "source_language": "en",
    "target_language": "it",
    "speed_priority": true,
    "conversation_id": "conv_789"
  }'
```

### Quality Levels
```bash
# Economy (fast, good for basic content)
curl -X POST https://translateflow.vosscg.com/v1/translate \
  -d '{"text":"Hello world", "quality":"economy"}'

# Standard (balanced speed and quality)
curl -X POST https://translateflow.vosscg.com/v1/translate \
  -d '{"text":"Hello world", "quality":"standard"}'

# Premium (highest quality, best for professional content)
curl -X POST https://translateflow.vosscg.com/v1/translate \
  -d '{"text":"Hello world", "quality":"premium"}'
```

### Translation Memory
```bash
curl -X POST https://translateflow.vosscg.com/v1/memory/store \
  -H "X-API-Key: tf_fedcba0987654321" \
  -H "Content-Type: application/json" \
  -d '{
    "source_text": "Thank you for your order",
    "translated_text": "Gracias por su pedido",
    "source_language": "en",
    "target_language": "es",
    "domain": "ecommerce"
  }'
```

### Glossary Integration
```bash
curl -X POST https://translateflow.vosscg.com/v1/translate \
  -H "X-API-Key: tf_fedcba0987654321" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Our SaaS platform provides comprehensive analytics.",
    "source_language": "en",
    "target_language": "fr",
    "glossary": {
      "SaaS": "SaaS (logiciel en tant que service)",
      "analytics": "analytiques"
    }
  }'
```

## Website & Content Localization

### Website Translation
```bash
curl -X POST https://translateflow.vosscg.com/v1/websites/translate \
  -H "X-API-Key: tf_fedcba0987654321" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "target_languages": ["es", "fr", "de"],
    "elements_to_translate": ["text", "alt_text", "meta_tags"],
    "preserve_html": true
  }'
```

### Content Management Integration
```bash
curl -X POST https://translateflow.vosscg.com/v1/cms/translate \
  -H "X-API-Key: tf_fedcba0987654321" \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "blog_post",
    "title": "10 Tips for Better SEO",
    "body": "Search engine optimization is crucial...",
    "target_languages": ["es", "pt", "it"],
    "seo_optimize": true
  }'
```

## Error Handling

Common error responses:
- `401 Unauthorized` - Invalid or missing API key
- `429 Too Many Requests` - Daily character limit exceeded
- `400 Bad Request` - Invalid language code or empty text
- `413 Payload Too Large` - Text exceeds maximum length (10,000 characters per request)
- `422 Unprocessable Entity` - Unsupported language pair

## Pricing & Limits

**Free Tier:**
- 10,000 characters per day
- 120+ supported languages
- Standard quality translations
- Basic document support

**Paid Plans:**
- Upgrade at https://vosscg.com/forges for higher limits
- Premium neural translation models
- Document translation (PDF, DOCX, PPTX)
- Translation memory and glossaries
- Priority processing
- Custom domain models

## Best Practices

1. **Language Detection**: Use auto-detection when source language is uncertain
2. **Domain Specialization**: Specify domain for technical/professional content
3. **Batch Processing**: Use batch endpoints for multiple texts (more efficient)
4. **Context Matters**: Provide context for ambiguous terms
5. **Quality Selection**: Choose appropriate quality level for use case
6. **Character Optimization**: Remove unnecessary formatting before translation

## Common Use Cases

### E-commerce Product Descriptions
```bash
curl -X POST https://translateflow.vosscg.com/v1/translate/batch \
  -H "X-API-Key: [API_KEY]" \
  -d '{
    "texts":["High-quality leather wallet", "Free shipping worldwide"],
    "target_language":"es",
    "domain":"ecommerce"
  }'
```

### Customer Support Messages
```bash
curl -X POST https://translateflow.vosscg.com/v1/translate \
  -H "X-API-Key: [API_KEY]" \
  -d '{
    "text":"Thank you for contacting us. We will respond within 24 hours.",
    "target_language":"fr",
    "context":{"domain":"customer_service", "tone":"professional"}
  }'
```

### Marketing Content
```bash
curl -X POST https://translateflow.vosscg.com/v1/translate/specialized \
  -H "X-API-Key: [API_KEY]" \
  -d '{
    "text":"Limited time offer! 50% off all premium features.",
    "target_language":"de",
    "domain":"marketing",
    "preserve_formatting":true
  }'
```

### Legal Document Translation  
```bash
curl -X POST https://translateflow.vosscg.com/v1/documents/translate \
  -H "X-API-Key: [API_KEY]" \
  -F "file=@contract.pdf" \
  -F "target_language=es" \
  -F "domain=legal" \
  -F "quality=premium"
```

## Integration Examples

### OpenClaw Agent Workflow
```bash
# Help user get API key
curl -X POST https://translateflow.vosscg.com/v1/keys -d '{"email":"user@domain.com"}'

# Translate user's text/content
curl -X POST https://translateflow.vosscg.com/v1/translate \
  -H "X-API-Key: [USER_API_KEY]" \
  -d '{"text":"[USER_TEXT]", "target_language":"[TARGET_LANG]"}'

# Return translated content to user
```

When users need text translation, content localization, document translation, or multi-language support, use this skill to leverage TranslateFlow's professional AI translation capabilities with context awareness and domain specialization.