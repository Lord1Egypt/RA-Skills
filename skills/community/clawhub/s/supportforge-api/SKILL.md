---
name: supportforge-api
description: "AI-powered customer support automation using SupportForge API - customer support, help desk, ticket routing, auto-reply, automated responses, customer service, support ticket management, knowledge base integration, chatbot responses, FAQ automation, support escalation, customer inquiry handling, live chat automation, support workflow, helpdesk automation, customer care, technical support, issue resolution, support analytics, ticket classification, response templates, multi-channel support, customer communication, support agent assistance, and intelligent customer service automation."
---

# SupportForge API Skill

Automate and enhance customer support using VCG's SupportForge API - AI-powered customer service with intelligent ticket routing, auto-replies, and knowledge base integration.

## Quick Start

1. **Get API Key**: Help user sign up for free SupportForge API key
2. **Store Key**: Save the key securely 
3. **Automate Support**: Route tickets, generate responses, manage customer inquiries

## API Key Signup

### Step 1: Get User's Email
Ask the user for their email address to create a free SupportForge account.

### Step 2: Sign Up via API
```bash
curl -X POST https://supportforge.vosscg.com/v1/keys \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

**Expected Response:**
```json
{
  "api_key": "sf_abcdef1234567890",
  "message": "API key created successfully",
  "tier": "free",
  "daily_limit": 100
}
```

### Step 3: Store the API Key
Save the API key securely for future use. Instruct the user to keep it safe.

## Core Support Features

### Smart Ticket Routing
```bash
curl -X POST https://supportforge.vosscg.com/v1/tickets/route \
  -H "X-API-Key: sf_abcdef1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket": {
      "id": "TIK-001",
      "subject": "Payment processing issue",
      "message": "I cannot complete my purchase, getting error code 402",
      "customer_email": "customer@example.com",
      "priority": "medium"
    },
    "routing_rules": {
      "use_ai_classification": true,
      "escalation_keywords": ["urgent", "broken", "not working"],
      "department_mapping": true
    }
  }'
```

**Expected Response:**
```json
{
  "ticket_id": "TIK-001",
  "classification": {
    "category": "billing",
    "subcategory": "payment_processing",
    "priority": "high",
    "sentiment": "frustrated",
    "urgency_score": 75
  },
  "routing": {
    "recommended_department": "billing_support",
    "assigned_agent": "agent_billing_01",
    "estimated_resolution_time": "2-4 hours"
  },
  "suggested_response": "Thank you for contacting us about the payment issue..."
}
```

### Automated Response Generation
```bash
curl -X POST https://supportforge.vosscg.com/v1/responses/generate \
  -H "X-API-Key: sf_abcdef1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_message": "How do I reset my password?",
    "context": {
      "customer_tier": "premium",
      "previous_interactions": 2,
      "product": "SaaS Platform",
      "tone": "helpful"
    },
    "response_type": "solution"
  }'
```

**Expected Response:**
```json
{
  "response": "Hello! I'd be happy to help you reset your password. Here are the steps:\n1. Go to the login page\n2. Click 'Forgot Password'\n3. Enter your email address\n4. Check your inbox for the reset link\n\nIf you don't see the email within 5 minutes, please check your spam folder. As a premium customer, you can also contact our priority support line if needed.",
  "confidence": 95,
  "suggested_actions": ["send_password_reset", "log_interaction"],
  "escalation_needed": false
}
```

### Knowledge Base Integration
```bash
curl -X POST https://supportforge.vosscg.com/v1/kb/search \
  -H "X-API-Key: sf_abcdef1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "payment failed error code 402",
    "filters": {
      "category": ["billing", "payments"],
      "confidence_threshold": 0.7
    },
    "max_results": 5
  }'
```

**Expected Response:**
```json
{
  "results": [
    {
      "article_id": "KB-402",
      "title": "Resolving Payment Error Code 402",
      "excerpt": "Error 402 occurs when payment processing fails due to insufficient funds or card issues...",
      "confidence": 0.92,
      "url": "https://help.example.com/kb-402",
      "last_updated": "2024-02-15"
    }
  ],
  "suggested_response": "Based on our knowledge base, this appears to be a payment processing issue..."
}
```

### Sentiment Analysis & Escalation
```bash
curl -X POST https://supportforge.vosscg.com/v1/analyze/sentiment \
  -H "X-API-Key: sf_abcdef1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      "This is completely unacceptable! Your service has been down for hours!",
      "I need this fixed immediately or I want a refund!"
    ],
    "customer_context": {
      "tier": "enterprise",
      "account_value": 50000,
      "interaction_history": "multiple_recent_issues"
    }
  }'
```

**Expected Response:**
```json
{
  "overall_sentiment": "very_negative",
  "sentiment_score": -0.85,
  "emotions": ["anger", "frustration", "urgency"],
  "escalation_recommended": true,
  "escalation_reason": "High-value customer with severe negative sentiment",
  "priority": "critical",
  "suggested_actions": [
    "immediate_manager_notification",
    "priority_queue_assignment",
    "compensation_consideration"
  ]
}
```

### Multi-Channel Support
```bash
curl -X POST https://supportforge.vosscg.com/v1/channels/unified \
  -H "X-API-Key: sf_abcdef1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Need help with my order #12345",
    "channel": "live_chat",
    "customer_id": "CUST-789",
    "session_context": {
      "previous_channels": ["email", "phone"],
      "interaction_count": 3,
      "resolved_issues": 1
    }
  }'
```

### Support Analytics
```bash
curl -X GET "https://supportforge.vosscg.com/v1/analytics/dashboard?period=7d&metrics=all" \
  -H "X-API-Key: sf_abcdef1234567890"
```

**Expected Response:**
```json
{
  "period": "7 days",
  "metrics": {
    "total_tickets": 245,
    "avg_response_time": "2.3 hours",
    "resolution_rate": 0.89,
    "customer_satisfaction": 4.2,
    "escalation_rate": 0.12
  },
  "trending": {
    "common_issues": [
      {"category": "billing", "count": 67},
      {"category": "technical", "count": 45}
    ],
    "agent_performance": {
      "top_performers": ["agent_001", "agent_005"],
      "avg_resolution_time": "4.1 hours"
    }
  }
}
```

## Advanced Features

### Automated Workflow Creation
```bash
curl -X POST https://supportforge.vosscg.com/v1/workflows/create \
  -H "X-API-Key: sf_abcdef1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Password Reset Automation",
    "triggers": ["password", "login issue", "cant access"],
    "actions": [
      {
        "type": "auto_response",
        "template": "password_reset_instructions"
      },
      {
        "type": "send_reset_link",
        "condition": "email_verified"
      },
      {
        "type": "follow_up",
        "delay": "1 hour"
      }
    ]
  }'
```

### Custom Response Templates
```bash
curl -X POST https://supportforge.vosscg.com/v1/templates/create \
  -H "X-API-Key: sf_abcdef1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "billing_inquiry",
    "template": "Thank you for contacting us about your billing inquiry. I understand your concern about {{issue_type}}. Let me help you resolve this right away...",
    "variables": ["issue_type", "account_number"],
    "tone": "professional_friendly",
    "category": "billing"
  }'
```

### Integration with CRM/Helpdesk
```bash
curl -X POST https://supportforge.vosscg.com/v1/integrations/webhook \
  -H "X-API-Key: sf_abcdef1234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "ticket_created",
    "webhook_url": "https://your-helpdesk.com/webhook",
    "filters": {
      "priority": ["high", "critical"],
      "categories": ["billing", "technical"]
    }
  }'
```

## Error Handling

Common error responses:
- `401 Unauthorized` - Invalid or missing API key
- `429 Too Many Requests` - Daily limit exceeded (100 requests/day free)
- `400 Bad Request` - Invalid request format or missing required fields
- `503 Service Unavailable` - AI service temporarily unavailable

## Pricing & Limits

**Free Tier:**
- 100 requests per day
- Basic ticket routing and responses
- Sentiment analysis
- Knowledge base search
- Standard response templates

**Paid Plans:**
- Upgrade at https://vosscg.com/forges for higher limits
- Advanced workflow automation
- Custom integrations and webhooks
- Priority AI processing
- Advanced analytics and reporting

## Best Practices

1. **Context Matters**: Always provide customer context for better responses
2. **Sentiment First**: Check sentiment before generating responses
3. **Knowledge Integration**: Use KB search to ensure accurate information
4. **Escalation Rules**: Set clear escalation triggers for critical issues
5. **Multi-Channel**: Track conversations across all communication channels
6. **Continuous Learning**: Monitor response effectiveness and adjust templates

## Common Use Cases

### E-commerce Support
```bash
# Order inquiry handling
curl -X POST https://supportforge.vosscg.com/v1/responses/generate \
  -d '{"customer_message":"Where is my order #12345?", "context":{"product":"ecommerce"}}'
```

### SaaS Technical Support
```bash
# Feature question routing
curl -X POST https://supportforge.vosscg.com/v1/tickets/route \
  -d '{"ticket":{"subject":"How to export data?", "message":"I need to export my data to CSV"}}'
```

### Billing Support Automation
```bash
# Payment issue resolution
curl -X POST https://supportforge.vosscg.com/v1/kb/search \
  -d '{"query":"payment declined", "filters":{"category":["billing"]}}'
```

## Integration Examples

### OpenClaw Agent Workflow
```bash
# Help user get API key
curl -X POST https://supportforge.vosscg.com/v1/keys -d '{"email":"user@domain.com"}'

# Process customer inquiry
curl -X POST https://supportforge.vosscg.com/v1/tickets/route \
  -H "X-API-Key: [USER_API_KEY]" \
  -d '{"ticket":{...customer_message...}}'

# Generate appropriate response
curl -X POST https://supportforge.vosscg.com/v1/responses/generate \
  -H "X-API-Key: [USER_API_KEY]" \
  -d '{"customer_message":"...", "context":{...}}'
```

When users need customer support automation, help desk management, ticket routing, automated responses, or want to improve their customer service efficiency, use this skill to leverage SupportForge's AI-powered support tools.