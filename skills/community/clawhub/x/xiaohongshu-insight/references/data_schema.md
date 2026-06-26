# Xiaohongshu Viral Post Data Field Descriptions

## Basic Post Information (note_base)

| Field | Type | Description |
|-------|------|-------------|
| note_id | string | Unique post identifier |
| title | string | Post title (max 100 characters) |
| content | string | Post body content (max 1000 characters, summary) |
| cover_url | string | Cover image URL |
| publish_time | datetime | Publish time (ISO 8601 format) |
| category | string | Category classification |
| tags | array | List of hashtags |

## Engagement Data (engagement)

| Field | Type | Description |
|-------|------|-------------|
| likes | int | Number of likes |
| collections | int | Number of saves |
| comments | int | Number of comments |
| shares | int | Number of shares |
| total_engagement | int | Total interactions (likes + saves + comments + shares) |
| engagement_rate | float | Engagement rate (total interactions / followers) |
| likes_growth_24h | int | 24-hour like growth |
| likes_growth_7d | int | 7-day like growth |
| growth_rate | float | Growth rate (daily average) |

## Author Information (author)

| Field | Type | Description |
|-------|------|-------------|
| author_id | string | Unique author identifier |
| author_name | string | Author nickname |
| avatar_url | string | Avatar URL |
| followers | int | Number of followers |
| following | int | Number of accounts following |
| notes_count | int | Total number of posts |
| avg_engagement | float | Average interactions per post |
| author_level | string | Author tier (Newbie / Beginner / Intermediate / Advanced / KOL) |

## Viral Tags (viral_tags)

| Field | Type | Description |
|-------|------|-------------|
| is_low_fan_viral | bool | Whether it qualifies as a low-follower viral post |
| is_period_high_like | bool | Whether it qualifies as periodic high-engagement |
| is_daily_spike | bool | Whether it qualifies as a single-day interaction spike |
| is_continuous_growth | bool | Whether it qualifies as sustained interaction growth |
| viral_score | float | Composite viral score (0-100) |
| viral_reason | string | Explanation of viral reason |

## Content Features (content_features)

| Field | Type | Description |
|-------|------|-------------|
| title_keywords | array | Extracted title keywords |
| cover_style | string | Cover style (Solid color / Collage / Contrast / Scene / Portrait) |
| content_type | string | Content type (Tutorial / Review / Recommendation / Tips / Story / Vlog) |
| word_count | int | Body word count |
| image_count | int | Number of images |
| has_video | bool | Whether video is included |
| video_duration | int | Video duration (seconds) |

## Traffic Curve (traffic_curve)

| Field | Type | Description |
|-------|------|-------------|
| likes_1h | int | Likes 1 hour after publishing |
| likes_6h | int | Likes 6 hours after publishing |
| likes_24h | int | Likes 24 hours after publishing |
| likes_48h | int | Likes 48 hours after publishing |
| likes_72h | int | Likes 72 hours after publishing |
| likes_7d | int | Likes 7 days after publishing |
| peak_time | datetime | Peak traffic time |
| decay_rate | float | Decay rate |

## Categories

- Beauty & Skincare (beauty)
- Fashion & Styling (fashion)
- Food & Dining (food)
- Travel Guides (travel)
- Home & Lifestyle (home)
- Parenting & Childcare (parenting)
- Career & Growth (career)
- Relationships & Psychology (emotion)
- Knowledge & Education (knowledge)
- Entertainment & Gossip (entertainment)
- Sports & Fitness (fitness)
- Tech & Gadgets (tech)
- Pets & Animals (pets)
- Photography Tips (photography)
- Handmade & DIY (diy)

## Data Update Frequency

| Data Type | Update Frequency | Description |
|-----------|------------------|-------------|
| Basic Post Information | Real-time | Indexed within 5 minutes of new post publication |
| Engagement Data | Hourly | Engagement metrics updated every hour |
| Viral Tags | Daily | Recalculated daily at 2:00 AM |
| Traffic Curve | Daily | Updated daily at 3:00 AM |
| Trend Analysis | Daily | Generated daily at 4:00 AM |

## Data Quality Metrics

- Indexing Rate: > 95%
- Accuracy Rate: > 98%
- Timeliness: New posts visible within 5 minutes
- Completeness: Core field coverage > 99%