# POI Validation Rules

## Overview

This document defines the rules and heuristics for validating Points of Interest (POIs) extracted from travel planning images.

## Validation Criteria

### 1. Name Validation

#### Required Characteristics
- **Non-empty**: Must contain at least 2 characters
- **Readable**: Should not be pure numbers or special characters
- **Location-like**: Should contain location indicators or be a known place name

#### Valid Name Patterns
- Chinese location names: `解放碑`, `洪崖洞`, `十八梯`
- English location names: `Jiefangbei`, `Hongyadong`, `Shibati`
- Mixed names: `Chongqing Hongyadong`, `重庆来福士`

#### Invalid Name Patterns
- Pure numbers: `123`, `456789`
- Single characters: `A`, `中`
- Generic terms: `here`, `there`, `location`
- Contact info: `13800138000`, `contact@example.com`

### 2. Coordinate Validation

#### Valid Coordinate Ranges
- **Longitude**: -180 to 180 degrees
- **Latitude**: -90 to 90 degrees
- **China-specific**: Longitude 73-136, Latitude 18-54

#### Coordinate Format
- Must be array of exactly 2 numbers: `[lng, lat]`
- Both values must be valid floats
- Cannot be null or undefined

### 3. Confidence Scoring

#### High Confidence (0.8-1.0)
- Exact match from Amap API with valid coordinates
- Known landmark names with verified locations
- Multiple validation sources agree

#### Medium Confidence (0.5-0.7)
- Partial match from Amap API
- Reasonable location name but coordinates approximate
- Single validation source

#### Low Confidence (0.2-0.4)
- No geocoding result, using fallback coordinates
- Ambiguous location name
- Requires manual verification

#### Very Low Confidence (<0.2)
- Invalid or missing data
- Clearly not a location
- Should be filtered out

## Filtering Rules

### Automatic Filtering
POIs are automatically filtered out if they:
- Have confidence < 0.3 (configurable threshold)
- Lack both name and coordinates
- Contain only contact information
- Are clearly not locations (e.g., "lunch", "dinner", "hotel")

### Manual Verification Required
POIs require manual verification if they:
- Have confidence between 0.3-0.6
- Have ambiguous names with multiple possible matches
- Are missing coordinates but have valid names
- Are in unexpected geographic areas

## Processing Pipeline

### Step 1: OCR Extraction
- Extract all text from image
- Split into individual lines/words
- Remove obvious non-location text

### Step 2: Initial Filtering
- Remove lines shorter than 2 characters
- Remove lines containing only numbers
- Remove lines with contact information patterns

### Step 3: Location Classification
- Apply keyword matching for location indicators
- Use language detection (Chinese vs English)
- Assign initial confidence scores

### Step 4: Geocoding
- Query Amap API for each candidate POI
- Validate returned coordinates
- Update confidence based on API response quality

### Step 5: Final Validation
- Apply coordinate validation rules
- Filter by final confidence threshold
- Flag ambiguous results for user review

## Special Cases

### 1. Transportation Hubs
- **Airports**: `重庆江北国际机场`, `Chongqing Jiangbei International Airport`
- **Train Stations**: `重庆北站`, `Chongqing North Railway Station`
- **Metro Stations**: `小什字站`, `Xiaoshizi Station`

### 2. Landmarks vs Addresses
- **Landmarks**: Prefer well-known names (`洪崖洞` over `嘉陵江滨江路88号`)
- **Addresses**: Use when landmark name is unavailable
- **Hybrid**: Combine both when possible (`洪崖洞 (嘉陵江滨江路88号)`)

### 3. Duplicate Detection
- **Exact duplicates**: Remove identical entries
- **Fuzzy duplicates**: Merge similar names (`解放碑` and `解放碑步行街`)
- **Coordinate proximity**: Merge POIs within 100m of each other

## Quality Assurance

### Validation Checks
1. **Name sanity**: Does it look like a real place name?
2. **Coordinate validity**: Are coordinates in reasonable ranges?
3. **Geographic consistency**: Are all POIs in the same general area?
4. **Completeness**: Do we have enough POIs for a meaningful route?

### Error Recovery
- **Missing POIs**: Allow manual addition through search interface
- **Wrong coordinates**: Enable drag-and-drop marker adjustment
- **Incorrect order**: Provide reordering tools (drag + arrow buttons)
- **Poor image quality**: Request higher resolution or manual input

## Performance Considerations

### Processing Time Targets
- **OCR extraction**: < 5 seconds per image
- **Geocoding**: < 2 seconds per POI (with caching)
- **Total pipeline**: < 30 seconds for typical travel plan (5-10 POIs)

### Resource Usage
- **Memory**: Keep processed images in memory only during processing
- **API calls**: Implement rate limiting and caching
- **Storage**: Clean up temporary files after processing

## User Experience Guidelines

### Feedback Messages
- **Success**: "Successfully extracted X locations from your image"
- **Partial success**: "Found X locations, Y need verification"
- **Failure**: "Could not extract locations. Please try a clearer image"

### Manual Override Options
- Add missing POIs through search
- Remove incorrect POIs
- Adjust POI order manually
- Fine-tune coordinates by dragging markers

### Accessibility
- Ensure generated HTML is keyboard navigable
- Provide clear error messages
- Support screen readers with proper ARIA labels
- Maintain color contrast for readability