# Scoring Dimension Details

Complete guide for evaluating each dimension.

## 1. Transportation (交通可达性) - Weight: 25%

### Key Metrics

| Metric | Data Points | Scoring Criteria |
|--------|-------------|------------------|
| Flight Price | Round-trip economy | 9-10: <1,500; 7-8: 1,500-3,000; 5-6: 3,000-5,000; <5: >5,000 |
| Flight Frequency | Daily flights | 9-10: 5+/day; 7-8: 2-4/day; 5-6: 1/day; <5: <1/day |
| Ground Transport | Airport to court | 9-10: <30min; 7-8: 30-60min; 5-6: 1-2h; <5: >2h |

### Data Sources
- Flights: flyai-skill, Ctrip, Trip.com
- Ground transport: Google Maps, local transport apps

### Example Assessment
```
Shanghai  Sanya:
- Flight: 1,800 (Score: 7/10)
- Frequency: 10/day (Score: 9/10)
- Ground: 45min (Score: 7/10)
- Transport Score: 7.5/10
```

---

## 2. Accommodation (住宿条件) - Weight: 25%

### Key Metrics

| Metric | Data Points | Scoring Criteria |
|--------|-------------|------------------|
| Price | Mid-range hotel/night | 9-10: <500; 7-8: 500-1,000; 5-6: 1,000-2,000; <5: >2,000 |
| Proximity | Distance to courts | 9-10: On-site; 7-8: <10min; 5-6: 10-30min; <5: >30min |
| Rating | Platform scores | 9-10: 4.5+; 7-8: 4.0-4.5; 5-6: 3.5-4.0; <5: <3.5 |

### Data Sources
- Hotels: Booking.com, Agoda, TripAdvisor
- Reviews: Platform ratings + user comments

### Example Assessment
```
Sanya Haitang Bay:
- Price: 1,200/night (Score: 6/10)
- Proximity: On-site (Score: 10/10)
- Rating: 4.6/5 (Score: 9/10)
- Accommodation Score: 8.0/10
```

---

## 3. Weather (天气适宜度) - Weight: 20%

### Key Metrics

| Metric | Data Points | Scoring Criteria |
|--------|-------------|------------------|
| Temperature | Daily average | 9-10: 18-26C; 7-8: 15-28C; 5-6: 10-32C; <5: <10C or >32C |
| Precipitation | Rain days/month | 9-10: <3 days; 7-8: 3-7 days; 5-6: 7-14 days; <5: >14 days |
| Sunlight | Daylight hours | 9-10: >10h; 7-8: 8-10h; 5-6: 6-8h; <5: <6h |

### Data Sources
- Weather: Weather Spark, historical climate data
- Seasonal patterns: Tourism boards, local guides

### Example Assessment
```
Bali in May:
- Temperature: 27C (Score: 8/10)
- Rain: 2 days/month (Score: 9/10)
- Sunlight: 11h/day (Score: 9/10)
- Weather Score: 9.0/10
```

### Best Seasons by Region

| Region | Best Months | Avoid Months |
|--------|-------------|--------------|
| Southeast Asia | Nov-Mar | Jun-Oct (monsoon) |
| Europe | May-Sep | Nov-Feb (cold) |
| Australia | Dec-Feb | Jun-Aug (winter) |
| US (Florida) | Oct-Apr | Jun-Sep (hot/humid) |

---

## 4. Facilities (球场质量) - Weight: 30%

### Key Metrics

| Metric | Data Points | Scoring Criteria |
|--------|-------------|------------------|
| Court Quality | Surface, maintenance | 9-10: Pro-level; 7-8: Well-maintained; 5-6: Average; <5: Poor |
| Court Fees | Hourly rate | 9-10: <100; 7-8: 100-200; 5-6: 200-400; <5: >400 |
| Amenities | Locker, shower, rental | 9-10: Full service; 7-8: Basic amenities; 5-6: Limited; <5: Minimal |
| Coaching | Pro availability | 9-10: Multiple pros; 7-8: Some coaches; 5-6: Limited; <5: None |

### Data Sources
- Courts: Official websites, user reviews
- Prices: Direct inquiry, user reports
- Coaching: Club websites, tennis forums

### Example Assessment
```
Bali Tennis Club:
- Quality: Hard courts, good maintenance (Score: 8/10)
- Fees: 150/hour (Score: 8/10)
- Amenities: Locker, shower, rental (Score: 8/10)
- Coaching: 3 pro coaches (Score: 9/10)
- Facilities Score: 8.5/10
```

### Court Surface Guide

| Surface | Characteristics | Best For |
|---------|-----------------|----------|
| Hard | Consistent bounce, medium pace | All levels |
| Clay | Slower, high bounce, sliding | Endurance training |
| Grass | Fast, low bounce | Serve/volley style |

---

## Scoring Formula

### Default Weights
```
Total Score = Transportation0.25 + Accommodation0.25 + Weather0.20 + Facilities0.30
```

### Custom Weights (User Priority)
If user prioritizes 2 dimensions:
```
Total Score = Priority10.35 + Priority20.35 + Other10.15 + Other20.15
```

### Rating Scale

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9.0-10 | Excellent | Highly Recommended |
| 8.0-8.9 | Very Good | Recommended |
| 7.0-7.9 | Good | Worth Considering |
| 6.0-6.9 | Average | Okay if convenient |
| <6.0 | Below Average | Not Recommended |

---

## Data Quality Guidelines

###  Do
- Use real data from reliable sources
- Mark prices as "参考价" (reference only)
- Label missing data as "待补充"
- Cite data sources in report

###  Don't
- Invent prices or ratings
- Guess when data unavailable
- Assume without verification
- Copy unverified user claims
