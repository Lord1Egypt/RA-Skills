---
title: Use GeoPoint Fields for Location Data
impact: MEDIUM
impactDescription: Built-in geographic queries, distance calculations
tags: collections, geopoint, location, geographic, maps
---

## Use GeoPoint Fields for Location Data

PocketBase provides a dedicated GeoPoint field type for storing geographic coordinates with built-in distance query support via `geoDistance()`.

**Incorrect (storing coordinates as separate fields):**

```javascript
// Separate lat/lon fields - no built-in distance queries
const placesSchema = [
  { name: 'name', type: 'text' },
  { name: 'latitude', type: 'number' },
  { name: 'longitude', type: 'number' }
];

// Manual distance calculation - complex and slow
async function findNearby(lat, lon, maxKm) {
  const places = await pb.collection('places').getFullList();

  // Calculate distance for every record client-side
  return places.filter(place => {
    const dist = haversine(lat, lon, place.latitude, place.longitude);
    return dist <= maxKm;
  });
}
```

**Correct (using GeoPoint field):**

```javascript
// GeoPoint field stores coordinates as { lon, lat } object
const placesSchema = [
  { name: 'name', type: 'text' },
  { name: 'location', type: 'geopoint' }
];

// Creating a record with GeoPoint
await pb.collection('places').create({
  name: 'Coffee Shop',
  location: { lon: -73.9857, lat: 40.7484 }  // Note: lon first!
});

// Or using "lon,lat" string format
await pb.collection('places').create({
  name: 'Restaurant',
  location: '-73.9857,40.7484'  // String format also works
});

// Query nearby locations using geoDistance()
async function findNearby(lon, lat, maxKm) {
  // geoDistance returns distance in kilometers
  const places = await pb.collection('places').getList(1, 50, {
    filter: pb.filter(
      'geoDistance(location, {:point}) <= {:maxKm}',
      {
        point: { lon, lat },
        maxKm: maxKm
      }
    ),
    sort: pb.filter('geoDistance(location, {:point})', { point: { lon, lat } })
  });

  return places;
}

// Find places within 5km of Times Square
const nearbyPlaces = await findNearby(-73.9857, 40.7580, 5);

// Use in API rules for location-based access
// listRule: geoDistance(location, @request.query.point) <= 10
```

**geoDistance() function:**

```javascript
// Syntax: geoDistance(geopointField, referencePoint)
// Returns: distance in kilometers

// In filter expressions
filter: 'geoDistance(location, "-73.9857,40.7484") <= 5'

// With parameter binding (recommended)
filter: pb.filter('geoDistance(location, {:center}) <= {:radius}', {
  center: { lon: -73.9857, lat: 40.7484 },
  radius: 5
})

// Sorting by distance
sort: 'geoDistance(location, "-73.9857,40.7484")'  // Closest first
sort: '-geoDistance(location, "-73.9857,40.7484")' // Farthest first
```

**GeoPoint data format:**

```javascript
// Object format (recommended)
{ lon: -73.9857, lat: 40.7484 }

// String format
"-73.9857,40.7484"  // "lon,lat" order

// Important: longitude comes FIRST (GeoJSON convention)
```

**Use cases:**
- Store-locator / find nearby
- Delivery radius validation
- Geofencing in API rules
- Location-based search results

**Limitations:**
- Spherical Earth calculation (accurate to ~0.3%)
- No polygon/area containment queries
- Single point per field (use multiple fields for routes)

Reference: [PocketBase GeoPoint](https://pocketbase.io/docs/collections/#geopoint)
