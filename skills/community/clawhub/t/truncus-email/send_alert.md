# Send a Monitoring Alert

Deliver an urgent system alert to the operations team.

## User Prompt

> "Alert the ops team at oncall@acme.com that the payments API error rate spiked above 5%."

## Agent Action

```bash
curl -X POST https://truncus.co/api/v1/emails/send \
  -H "Authorization: Bearer $TRUNCUS_API_KEY" \
  -H "Idempotency-Key: alert-payments-error-rate-2026-03-11T1430Z" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "oncall@acme.com",
    "from": "alerts@yourapp.com",
    "subject": "[ALERT] Payments API error rate above 5%",
    "html": "<div style=\"font-family: sans-serif;\"><h2 style=\"color: #d32f2f;\">Payments API Error Rate Alert</h2><p><strong>Metric:</strong> Error rate<br><strong>Current value:</strong> 7.3%<br><strong>Threshold:</strong> 5%<br><strong>Detected at:</strong> 2026-03-11 14:28 UTC</p><p>The payments API error rate has exceeded the 5% threshold for the past 5 minutes. Check the <a href=\"https://dashboard.yourapp.com/metrics/payments\">metrics dashboard</a> for details.</p><hr><p style=\"color: #666; font-size: 12px;\">This is an automated alert from your monitoring system.</p></div>",
    "text": "[ALERT] Payments API Error Rate\n\nMetric: Error rate\nCurrent value: 7.3%\nThreshold: 5%\nDetected at: 2026-03-11 14:28 UTC\n\nThe payments API error rate has exceeded the 5% threshold for the past 5 minutes.",
    "metadata": {
      "alert_type": "error_rate",
      "service": "payments-api",
      "severity": "high",
      "current_value": "7.3%",
      "threshold": "5%"
    }
  }'
```

## Expected Response

```json
{
  "status": "sent",
  "message_id": "cm3mno6pqr7stu",
  "provider_message_id": "0100018e-ijkl-9012-3456-example"
}
```

## Agent Reply

> Sent alert to oncall@acme.com: "Payments API error rate above 5%" (currently 7.3%). Message ID: `cm3mno6pqr7stu`.
