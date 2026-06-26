# Token Usage Monitor Integration Guide

## Overview

This guide explains how to integrate the Token Usage Monitor with OpenClaw sessions to automatically track token consumption for all AI model interactions.

## Automatic Integration

### Step 1: Modify OpenClaw Session Startup

Add the following code to your OpenClaw session startup script to automatically track token usage:

```python
from skills.token-usage-monitor.scripts.token_usage_tracker import TokenUsageTracker

def track_token_usage(session_id, model, prompt_tokens, completion_tokens):
    """Track token usage for each AI model call"""
    tracker = TokenUsageTracker()
    tracker.track_usage(session_id, model, prompt_tokens, completion_tokens)

# Example usage in a model call wrapper
def call_ai_model(prompt, model="doubao-seed"):
    # Call the AI model
    response = openclaw.call_model(prompt, model=model)
    
    # Extract token counts from response metadata
    prompt_tokens = response.metadata.get("prompt_tokens", 0)
    completion_tokens = response.metadata.get("completion_tokens", 0)
    
    # Track usage
    track_token_usage(openclaw.session_id, model, prompt_tokens, completion_tokens)
    
    return response
```

### Step 2: Add Heartbeat Check

Update your HEARTBEAT.md to include periodic token usage checks:

```markdown
# HEARTBEAT.md

## Periodic Checks
- Check token usage thresholds hourly
- Generate daily usage report at 9:00 AM
```

Add this to your heartbeat processing logic:

```python
from skills.token-usage-monitor.scripts.token_usage_tracker import TokenUsageTracker
from datetime import datetime

def process_heartbeat():
    tracker = TokenUsageTracker()
    
    # Check thresholds every hour
    now = datetime.now()
    if now.minute == 0:
        # This will trigger alerts if thresholds are exceeded
        for model in tracker.usage_data["thresholds"]:
            date_str = now.strftime("%Y-%m-%d")
            if date_str in tracker.usage_data["daily_totals"] and model in tracker.usage_data["daily_totals"][date_str]:
                daily_total = tracker.usage_data["daily_totals"][date_str][model]["total_tokens"]
                tracker._check_thresholds(model, daily_total)
    
    # Generate daily report at 9:00 AM
    if now.hour == 9 and now.minute == 0:
        report = tracker.get_daily_report()
        # Send report to user
        openclaw.send_message(f"📅 Daily Token Usage Report:\n{json.dumps(report, indent=2)}")
```

## Manual Usage

### Tracking Ad-Hoc Requests

You can manually track token usage for individual requests:

```bash
python scripts/token_usage_tracker.py --track --model doubao-seed --prompt-tokens 500 --completion-tokens 1200
```

### Setting Custom Thresholds

```bash
# Set a threshold of 50,000 tokens per day for GPT-4
python scripts/token_usage_tracker.py --set-threshold --model gpt-4 --limit 50000

# Set a threshold of 200,000 tokens per day for Doubao
python scripts/token_usage_tracker.py --set-threshold --model doubao-seed --limit 200000
```

## Customization

### Model Pricing

Edit the `model_pricing` section in the token_usage.json file or modify the script directly:

```python
tracker.usage_data["model_pricing"]["custom-model"] = 0.005 / 1000  # $0.005 per 1000 tokens
tracker._save_data()
```

### Alert Channels

Extend the `_check_thresholds` method in the TokenUsageTracker class to support additional alert channels:

```python
def _check_thresholds(self, model: str, tokens_used: int):
    if model in self.usage_data["thresholds"]:
        threshold = self.usage_data["thresholds"][model]
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
        if date_str in self.usage_data["daily_totals"] and model in self.usage_data["daily_totals"][date_str]:
            daily_total = self.usage_data["daily_totals"][date_str][model]["total_tokens"]
            
            if daily_total >= threshold["limit"] and not threshold.get("alert_sent", False):
                # Send to chat
                print(f"⚠️ ALERT: {model} usage ({daily_total} tokens) exceeds daily threshold of {threshold['limit']} tokens!")
                
                # Send email (requires smtplib setup)
                # send_email_alert(model, daily_total, threshold["limit"])
                
                # Send to webhook
                # send_webhook_alert(model, daily_total, threshold["limit"])
                
                threshold["alert_sent"] = True
                self._save_data()
```

## Troubleshooting

### Data File Location

The usage data is stored at `~/.openclaw/token_usage.json`. If you need to reset your usage data, simply delete this file.

### Permission Issues

If you encounter permission errors when writing to the data file, ensure the OpenClaw user has write access to the `~/.openclaw/` directory:

```bash
chown -R $USER:$USER ~/.openclaw/
chmod -R 700 ~/.openclaw/
```

### Token Count Accuracy

The accuracy of token counts depends on the metadata provided by your AI model provider. If token counts are missing or inaccurate, you may need to:
1. Check if your model supports token counting metadata
2. Implement a local token counter (e.g., using tiktoken for OpenAI models)
3. Adjust the integration to use approximate token counting

## Best Practices

1. **Track All Usage**: Integrate tracking for all AI model calls to get a complete picture of your token consumption
2. **Set Realistic Thresholds**: Start with conservative thresholds and adjust based on actual usage patterns
3. **Review Regularly**: Schedule weekly or monthly reviews of usage reports to identify cost optimization opportunities
4. **Optimize Prompts**: Use the usage data to identify prompts that generate excessive token usage and optimize them
5. **Monitor Costs**: Regularly review estimated costs to ensure they align with your budget