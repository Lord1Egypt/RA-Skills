---
name: stayforge-api
description: "Hotel booking and accommodation search using StayForge API - hotel booking, hotel search, accommodation booking, hotel reservation, find hotels, book hotels, travel booking, lodging search, accommodation finder, hotel deals, hotel prices, hotel availability, vacation rentals, business travel, leisure travel, hotel comparison, best hotel rates, cheap hotels, luxury hotels, budget accommodation, hotel rooms, travel accommodation, hospitality booking, stay booking, overnight accommodation, travel lodging, hotel inventory, property booking, guest accommodation, and comprehensive travel accommodation search and booking services."
---

# StayForge API Skill

Professional hotel booking and accommodation search using VCG's StayForge API - access to 180,000+ properties worldwide with real-time availability and competitive rates.

## Quick Start

1. **Get API Key**: Help user sign up for free StayForge API key
2. **Store Key**: Save the key securely 
3. **Search & Book**: Find hotels, check availability, make reservations

## API Key Signup

### Step 1: Get User's Email  
Ask the user for their email address to create a free StayForge account.

### Step 2: Sign Up via API
```bash
curl -X POST https://stayforge.vosscg.com/v1/keys \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

**Expected Response:**
```json
{
  "api_key": "stay_1a2b3c4d5e6f7890",
  "message": "API key created successfully", 
  "tier": "free",
  "properties_available": 180000,
  "daily_search_limit": 1000
}
```

### Step 3: Store the API Key
Save the API key securely for future use. Instruct the user to keep it safe.

## Core Hotel Search Features

### Hotel Search by Location
```bash
curl -X GET "https://stayforge.vosscg.com/v1/hotels/search" \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -G \
  -d "location=New York City" \
  -d "checkin=2024-06-15" \
  -d "checkout=2024-06-18" \
  -d "guests=2" \
  -d "rooms=1"
```

**Expected Response:**
```json
{
  "search_id": "search_12345",
  "location": "New York City, NY",
  "checkin": "2024-06-15",
  "checkout": "2024-06-18",
  "total_hotels": 1247,
  "hotels": [
    {
      "hotel_id": "hotel_abc123",
      "name": "Grand Manhattan Hotel",
      "address": "123 Broadway, New York, NY 10001",
      "star_rating": 4,
      "guest_rating": 8.7,
      "location_score": 9.2,
      "price": {
        "total": 450.00,
        "per_night": 150.00,
        "currency": "USD",
        "includes_taxes": true
      },
      "amenities": ["WiFi", "Fitness Center", "Restaurant", "Business Center"],
      "images": ["https://images.stayforge.com/hotel_abc123_1.jpg"],
      "availability": "available",
      "cancellation": "free_until_24h"
    }
  ],
  "filters": {
    "price_range": {"min": 89, "max": 2500},
    "star_ratings": [1, 2, 3, 4, 5],
    "amenities": ["WiFi", "Parking", "Pool", "Spa", "Gym"]
  }
}
```

### Search by Coordinates
```bash
curl -X GET "https://stayforge.vosscg.com/v1/hotels/search" \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -G \
  -d "lat=40.7589" \
  -d "lng=-73.9851" \
  -d "radius=5km" \
  -d "checkin=2024-06-15" \
  -d "checkout=2024-06-18" \
  -d "guests=1"
```

### Advanced Search with Filters
```bash
curl -X POST https://stayforge.vosscg.com/v1/hotels/search/advanced \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Paris, France",
    "checkin": "2024-07-01", 
    "checkout": "2024-07-05",
    "guests": 2,
    "rooms": 1,
    "filters": {
      "price_range": {"min": 100, "max": 400},
      "star_rating": [4, 5],
      "amenities": ["WiFi", "Breakfast", "Parking"],
      "guest_rating_min": 8.0,
      "property_types": ["hotel", "boutique"],
      "location_preference": "city_center"
    },
    "sort_by": "price_low_to_high"
  }'
```

### Hotel Details
```bash
curl -X GET "https://stayforge.vosscg.com/v1/hotels/hotel_abc123/details" \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -G \
  -d "checkin=2024-06-15" \
  -d "checkout=2024-06-18" \
  -d "guests=2"
```

**Expected Response:**
```json
{
  "hotel_id": "hotel_abc123",
  "name": "Grand Manhattan Hotel",
  "description": "Elegant 4-star hotel in the heart of Manhattan...",
  "address": {
    "street": "123 Broadway",
    "city": "New York",
    "state": "NY", 
    "postal_code": "10001",
    "country": "USA"
  },
  "contact": {
    "phone": "+1-212-555-0123",
    "email": "info@grandmanhattan.com"
  },
  "ratings": {
    "star_rating": 4,
    "guest_rating": 8.7,
    "location_score": 9.2,
    "cleanliness": 8.9,
    "service": 8.5
  },
  "room_types": [
    {
      "room_type": "standard_double",
      "name": "Standard Double Room", 
      "size": "25 sqm",
      "beds": "1 Double Bed",
      "max_guests": 2,
      "price": 150.00,
      "available_rooms": 5
    },
    {
      "room_type": "deluxe_suite",
      "name": "Deluxe Suite",
      "size": "45 sqm", 
      "beds": "1 King Bed + Sofa Bed",
      "max_guests": 4,
      "price": 280.00,
      "available_rooms": 2
    }
  ],
  "amenities": {
    "property": ["WiFi", "Fitness Center", "Restaurant", "24h Front Desk"],
    "room": ["Air Conditioning", "TV", "Safe", "Mini Bar", "Coffee Maker"]
  },
  "policies": {
    "checkin": "15:00",
    "checkout": "11:00", 
    "cancellation": "Free cancellation until 24 hours before checkin",
    "pets": "No pets allowed",
    "smoking": "Non-smoking property"
  }
}
```

## Booking Management

### Create Booking
```bash
curl -X POST https://stayforge.vosscg.com/v1/bookings/create \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -H "Content-Type: application/json" \
  -d '{
    "hotel_id": "hotel_abc123",
    "room_type": "standard_double",
    "checkin": "2024-06-15",
    "checkout": "2024-06-18", 
    "guests": 2,
    "rooms": 1,
    "guest_details": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@email.com",
      "phone": "+1-555-123-4567"
    },
    "special_requests": "Late checkout if possible",
    "payment_method": "credit_card"
  }'
```

**Expected Response:**
```json
{
  "booking_id": "book_xyz789",
  "confirmation_number": "STAY-123456",
  "status": "confirmed",
  "hotel": {
    "name": "Grand Manhattan Hotel",
    "address": "123 Broadway, New York, NY"
  },
  "booking_details": {
    "checkin": "2024-06-15",
    "checkout": "2024-06-18",
    "nights": 3,
    "room_type": "Standard Double Room",
    "guests": 2
  },
  "pricing": {
    "room_rate": 150.00,
    "nights": 3,
    "subtotal": 450.00,
    "taxes": 54.00,
    "total": 504.00,
    "currency": "USD"
  },
  "cancellation_deadline": "2024-06-14T15:00:00Z",
  "voucher_url": "https://stayforge.vosscg.com/voucher/book_xyz789"
}
```

### Booking Status Check
```bash
curl -X GET "https://stayforge.vosscg.com/v1/bookings/book_xyz789/status" \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890"
```

### Cancel Booking
```bash
curl -X POST https://stayforge.vosscg.com/v1/bookings/book_xyz789/cancel \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -H "Content-Type: application/json" \
  -d '{
    "cancellation_reason": "Change of plans",
    "refund_requested": true
  }'
```

### Modify Booking
```bash
curl -X PUT https://stayforge.vosscg.com/v1/bookings/book_xyz789/modify \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -H "Content-Type: application/json" \
  -d '{
    "new_checkout": "2024-06-19",
    "modification_reason": "Extended stay"
  }'
```

## Location & Discovery Features

### Popular Destinations
```bash
curl -X GET "https://stayforge.vosscg.com/v1/destinations/popular" \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -G \
  -d "region=north_america" \
  -d "category=business"
```

### Hotel Deals & Offers
```bash
curl -X GET "https://stayforge.vosscg.com/v1/deals" \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -G \
  -d "location=Las Vegas" \
  -d "deal_type=weekend_special" \
  -d "checkin=2024-06-15"
```

### Location Suggestions
```bash
curl -X GET "https://stayforge.vosscg.com/v1/locations/suggest" \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -G \
  -d "query=Times Square"
```

**Expected Response:**
```json
{
  "suggestions": [
    {
      "location_id": "loc_times_square",
      "name": "Times Square, New York",
      "type": "landmark",
      "coordinates": {"lat": 40.7589, "lng": -73.9851},
      "nearby_hotels": 156
    },
    {
      "location_id": "loc_midtown_manhattan", 
      "name": "Midtown Manhattan, New York",
      "type": "district",
      "coordinates": {"lat": 40.7549, "lng": -73.9840},
      "nearby_hotels": 234
    }
  ]
}
```

## Advanced Features

### Business Travel Integration
```bash
curl -X POST https://stayforge.vosscg.com/v1/business/search \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Chicago, IL",
    "checkin": "2024-06-10",
    "checkout": "2024-06-12",
    "business_filters": {
      "meeting_rooms": true,
      "business_center": true,
      "airport_shuttle": true,
      "corporate_rates": true
    },
    "company_id": "corp_12345"
  }'
```

### Group Bookings
```bash
curl -X POST https://stayforge.vosscg.com/v1/groups/quote \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Orlando, FL",
    "checkin": "2024-08-01",
    "checkout": "2024-08-05",
    "rooms_needed": 15,
    "total_guests": 30,
    "group_type": "conference",
    "special_requirements": ["meeting space", "group dining"]
  }'
```

### Hotel Reviews & Ratings
```bash
curl -X GET "https://stayforge.vosscg.com/v1/hotels/hotel_abc123/reviews" \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -G \
  -d "limit=10" \
  -d "sort=recent"
```

### Price Tracking
```bash
curl -X POST https://stayforge.vosscg.com/v1/price-alerts/create \
  -H "X-API-Key: stay_1a2b3c4d5e6f7890" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Miami, FL",
    "checkin": "2024-12-20",
    "checkout": "2024-12-25", 
    "target_price": 200,
    "email": "user@example.com"
  }'
```

## Error Handling

Common error responses:
- `401 Unauthorized` - Invalid or missing API key
- `429 Too Many Requests` - Daily search limit exceeded (1000 searches/day free)
- `400 Bad Request` - Invalid dates or location
- `404 Not Found` - Hotel not found or unavailable
- `409 Conflict` - Room no longer available (booking conflict)
- `422 Unprocessable Entity` - Invalid guest details or booking parameters

## Pricing & Limits

**Free Tier:**
- 1000 hotel searches per day
- Access to 180,000+ properties worldwide
- Basic booking management
- Standard customer support

**Paid Plans:**
- Upgrade at https://vosscg.com/forges for higher limits
- Corporate booking tools and rates
- Group booking management
- Advanced analytics and reporting
- Priority customer support
- Custom integration support

## Best Practices

1. **Date Validation**: Always validate checkin/checkout dates
2. **Availability Check**: Check real-time availability before booking
3. **Guest Details**: Collect complete guest information for bookings
4. **Price Comparison**: Show multiple options with different price points
5. **Location Context**: Provide location suggestions and nearby attractions
6. **Cancellation Policies**: Always display cancellation terms clearly

## Common Use Cases

### Vacation Planning
```bash
# Search beach hotels in Cancun
curl -X GET "https://stayforge.vosscg.com/v1/hotels/search" \
  -H "X-API-Key: [API_KEY]" \
  -G -d "location=Cancun, Mexico" -d "amenities=beach,pool"
```

### Business Travel
```bash
# Find airport hotels with meeting facilities
curl -X POST https://stayforge.vosscg.com/v1/business/search \
  -H "X-API-Key: [API_KEY]" \
  -d '{"location":"LAX Airport", "business_filters":{"meeting_rooms":true}}'
```

### Last-Minute Booking
```bash
# Tonight's availability
curl -X GET "https://stayforge.vosscg.com/v1/hotels/search" \
  -H "X-API-Key: [API_KEY]" \
  -G -d "location=current" -d "checkin=today" -d "checkout=tomorrow"
```

### Event Accommodation
```bash
# Hotels near convention center
curl -X GET "https://stayforge.vosscg.com/v1/hotels/search" \
  -H "X-API-Key: [API_KEY]" \
  -G -d "lat=34.0522" -d "lng=-118.2437" -d "radius=2km"
```

## Integration Examples  

### OpenClaw Agent Workflow
```bash
# Help user get API key
curl -X POST https://stayforge.vosscg.com/v1/keys -d '{"email":"user@domain.com"}'

# Search hotels based on user requirements  
curl -X GET "https://stayforge.vosscg.com/v1/hotels/search" \
  -H "X-API-Key: [USER_API_KEY]" \
  -G -d "location=[DESTINATION]" -d "checkin=[DATE]" -d "checkout=[DATE]"

# Show options and help with booking if requested
curl -X POST https://stayforge.vosscg.com/v1/bookings/create \
  -H "X-API-Key: [USER_API_KEY]" \
  -d '{"hotel_id":"[SELECTED_HOTEL]", ...}'
```

When users need hotel accommodations, want to search for hotels, make travel bookings, find vacation rentals, or need help with business travel arrangements, use this skill to leverage StayForge's extensive hotel inventory and booking capabilities.