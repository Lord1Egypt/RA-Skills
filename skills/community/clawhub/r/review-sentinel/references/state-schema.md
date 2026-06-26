# State Schema

## config.json
```json
{
  "businesses": [
    {
      "name": "string — Display name",
      "placeId": "string — Google Maps Place ID (optional)",
      "location": "string — City/address for context",
      "searchQuery": "string — Search term for Google Maps lookup",
      "competitors": ["string — competitor search queries"],
      "lastChecked": "ISO 8601 timestamp or null",
      "reviewCount": "number — last known review count",
      "rating": "number — last known average rating",
      "responseStyle": "medical|retail|service — tone for drafting responses"
    }
  ]
}
```

## state/<business-slug>.json
```json
{
  "businessName": "string",
  "lastFetched": "ISO 8601 timestamp",
  "currentRating": 4.4,
  "totalReviews": 723,
  "ratingBreakdown": {
    "5": 603,
    "4": 8,
    "3": 10,
    "2": 21,
    "1": 81
  },
  "recentReviews": [
    {
      "author": "string",
      "rating": 5,
      "text": "string — review body",
      "date": "string — relative or absolute date",
      "replied": false,
      "responseText": null,
      "topics": ["service", "staff", "wait"],
      "sentiment": "positive|neutral|negative"
    }
  ],
  "history": [
    {
      "date": "YYYY-MM-DD",
      "rating": 4.4,
      "totalReviews": 723,
      "breakdown": { "5": 603, "4": 8, "3": 10, "2": 21, "1": 81 }
    }
  ],
  "alerts": [
    {
      "date": "ISO 8601",
      "type": "new_negative|rating_drop|review_spike",
      "message": "string",
      "acknowledged": false
    }
  ]
}
```
