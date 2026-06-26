# Send an HTML Report

Agent generates a structured HTML report and delivers it via email.

## User Prompt

> "Build a summary of this week's sales data and email it to reports@acme.com."

## Agent Action

The agent constructs the HTML body from the data, then sends:

```bash
curl -X POST https://truncus.co/api/v1/emails/send \
  -H "Authorization: Bearer $TRUNCUS_API_KEY" \
  -H "Idempotency-Key: weekly-sales-2026-w11" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "reports@acme.com",
    "from": "analytics@yourapp.com",
    "subject": "Weekly Sales Report — Week 11, 2026",
    "html": "<h1>Weekly Sales Report</h1><p>Week 11 (Mar 9 – Mar 15, 2026)</p><table border=\"1\" cellpadding=\"8\" cellspacing=\"0\"><thead><tr><th>Product</th><th>Units</th><th>Revenue</th></tr></thead><tbody><tr><td>Pro Plan</td><td>42</td><td>$798</td></tr><tr><td>Scale Plan</td><td>7</td><td>$693</td></tr></tbody><tfoot><tr><td><strong>Total</strong></td><td><strong>49</strong></td><td><strong>$1,491</strong></td></tr></tfoot></table>",
    "text": "Weekly Sales Report — Week 11, 2026\n\nPro Plan: 42 units, $798\nScale Plan: 7 units, $693\nTotal: 49 units, $1,491",
    "metadata": {
      "report_type": "weekly_sales",
      "week": "2026-W11"
    }
  }'
```

## Expected Response

```json
{
  "status": "sent",
  "message_id": "cm2xyz4abc5def",
  "provider_message_id": "0100018e-efgh-5678-9012-example"
}
```

## Agent Reply

> Sent the weekly sales report to reports@acme.com. 49 total units, $1,491 revenue. Message ID: `cm2xyz4abc5def`.
