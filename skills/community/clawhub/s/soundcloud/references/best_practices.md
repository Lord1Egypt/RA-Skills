# SoundCloud API Best Practices

## Performance Optimization

### 1. Efficient Request Patterns

#### Batch Operations
```bash
# Instead of individual requests
curl /tracks/123
curl /tracks/456
curl /tracks/789

# Use batch processing
./scripts/batch_operations.sh download-metadata track_ids.txt
```

#### Pagination Strategy
```bash
# Start with reasonable limit
GET /tracks?q=genre&limit=50

# Use next_href for subsequent pages
# instead of calculating offsets manually
```

#### Field Selection
```bash
# Request only needed fields
GET /tracks/123?fields=id,title,duration,genre
```

### 2. Caching Strategies

#### Response Caching
```bash
# Cache responses based on endpoint
# Tracks: 5-10 minutes (plays/likes update frequently)
# User profiles: 30-60 minutes
# Playlists: 15-30 minutes
```

#### Local Cache Implementation
```python
# Example Python cache decorator
import functools
import time
import json
from pathlib import Path

def cache_response(ttl_seconds=300):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{args}_{kwargs}"
            cache_file = Path(f"cache/{cache_key}.json")
            
            # Check cache
            if cache_file.exists():
                cache_data = json.loads(cache_file.read_text())
                if time.time() - cache_data['timestamp'] < ttl_seconds:
                    return cache_data['response']
            
            # Make API call
            response = func(*args, **kwargs)
            
            # Save to cache
            cache_data = {
                'timestamp': time.time(),
                'response': response
            }
            cache_file.parent.mkdir(exist_ok=True)
            cache_file.write_text(json.dumps(cache_data))
            
            return response
        return wrapper
    return decorator
```

### 3. Rate Limit Management

#### Exponential Backoff
```python
import time
import random

def make_request_with_backoff(url, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 429:  # Rate limited
                wait_time = (2 ** attempt) + random.random()
                time.sleep(wait_time)
                continue
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + random.random()
            time.sleep(wait_time)
```

#### Request Throttling
```bash
# Add delay between requests
DELAY=1  # seconds between requests

while read track_id; do
    curl "https://api.soundcloud.com/tracks/$track_id"
    sleep $DELAY
done < track_ids.txt
```

## Error Handling

### 1. Comprehensive Error Recovery

#### Retry Logic
```bash
#!/bin/bash
# retry_request.sh

MAX_RETRIES=3
RETRY_DELAY=2

for i in $(seq 1 $MAX_RETRIES); do
    response=$(curl -s -w "%{http_code}" -o response.json "$URL")
    http_code=${response: -3}
    
    case $http_code in
        200|201)
            # Success
            cat response.json
            break
            ;;
        429)
            # Rate limited
            echo "Rate limited, retrying in $RETRY_DELAY seconds..."
            sleep $RETRY_DELAY
            RETRY_DELAY=$((RETRY_DELAY * 2))
            ;;
        5*)
            # Server error
            echo "Server error, retrying..."
            sleep $RETRY_DELAY
            ;;
        *)
            # Client error, don't retry
            echo "Error $http_code"
            exit 1
            ;;
    esac
done
```

#### Graceful Degradation
```bash
# If API fails, provide fallback data
if ! ./scripts/search_tracks.sh "query"; then
    echo "Using cached results..."
    cat cached_results.json
fi
```

### 2. Input Validation

#### Track ID Validation
```bash
validate_track_id() {
    local track_id="$1"
    
    # Check if numeric
    if ! [[ "$track_id" =~ ^[0-9]+$ ]]; then
        echo "Error: Track ID must be numeric"
        return 1
    fi
    
    # Check reasonable range
    if [ "$track_id" -lt 1 ] || [ "$track_id" -gt 9999999999 ]; then
        echo "Error: Track ID out of valid range"
        return 1
    fi
    
    return 0
}
```

#### URL Resolution
```bash
resolve_soundcloud_url() {
    local url="$1"
    
    # Validate URL format
    if [[ ! "$url" =~ ^https?://soundcloud\.com/ ]]; then
        echo "Error: Not a SoundCloud URL"
        return 1
    fi
    
    # Resolve through API
    local resolved=$(curl -s "https://api.soundcloud.com/resolve?url=$url&client_id=$CLIENT_ID")
    
    if echo "$resolved" | jq -e '.id' >/dev/null 2>&1; then
        echo "$resolved" | jq -r '.id'
        return 0
    else
        echo "Error: Could not resolve URL"
        return 1
    fi
}
```

## Data Management

### 1. Efficient Data Storage

#### JSON Structure Optimization
```json
{
  "tracks": {
    "metadata": {
      "fetched_at": "2024-01-15T10:30:00Z",
      "source": "soundcloud_api"
    },
    "data": [
      {
        "id": 123,
        "title": "Track Title",
        "essential": true,  // Core fields always included
        "extended": false   // Extended fields fetched on demand
      }
    ]
  }
}
```

#### Database Schema
```sql
-- Efficient track storage
CREATE TABLE soundcloud_tracks (
    id BIGINT PRIMARY KEY,
    title TEXT NOT NULL,
    artist_id BIGINT,
    duration_ms INTEGER,
    genre TEXT,
    bpm INTEGER,
    plays INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    fetched_at TIMESTAMP,
    updated_at TIMESTAMP,
    raw_json JSONB  -- Store full response for reference
);

-- Indexes for common queries
CREATE INDEX idx_genre ON soundcloud_tracks(genre);
CREATE INDEX idx_bpm ON soundcloud_tracks(bpm);
CREATE INDEX idx_plays ON soundcloud_tracks(plays DESC);
```

### 2. Data Synchronization

#### Incremental Updates
```bash
#!/bin/bash
# sync_tracks.sh

LAST_SYNC=$(cat last_sync.txt 2>/dev/null || echo "1970-01-01T00:00:00Z")

# Only fetch tracks updated since last sync
curl -X GET "https://api.soundcloud.com/tracks?created_at[from]=$LAST_SYNC&limit=200"

# Update last sync time
date -u +"%Y-%m-%dT%H:%M:%SZ" > last_sync.txt
```

#### Change Detection
```python
def detect_changes(old_data, new_data):
    changes = []
    
    for track_id, new_track in new_data.items():
        old_track = old_data.get(track_id)
        
        if not old_track:
            changes.append(('created', track_id, new_track))
        elif old_track['plays'] != new_track['plays'] or \
             old_track['likes'] != new_track['likes']:
            changes.append(('updated', track_id, new_track))
    
    # Check for deletions
    for track_id in old_data:
        if track_id not in new_data:
            changes.append(('deleted', track_id, None))
    
    return changes
```

## Security Best Practices

### 1. Credential Management

#### Environment-Based Configuration
```bash
#!/bin/bash
# config.sh

# Load environment-specific config
ENV=${ENV:-development}

case $ENV in
    production)
        CONFIG_FILE=".env.production"
        ;;
    staging)
        CONFIG_FILE=".env.staging"
        ;;
    *)
        CONFIG_FILE=".env.development"
        ;;
esac

# Load config
if [ -f "$CONFIG_FILE" ]; then
    export $(grep -v '^#' "$CONFIG_FILE" | xargs)
fi

# Set defaults
export SOUNDCLOUD_CLIENT_ID=${SOUNDCLOUD_CLIENT_ID:-""}
export SOUNDCLOUD_ACCESS_TOKEN=${SOUNDCLOUD_ACCESS_TOKEN:-""}
```

#### Secret Rotation
```bash
#!/bin/bash
# rotate_token.sh

# Check token expiration
TOKEN_AGE=$(( $(date +%s) - $(stat -c %Y token.txt) ))

if [ $TOKEN_AGE -gt 2592000 ]; then  # 30 days
    echo "Token is 30+ days old, refreshing..."
    
    # Refresh token
    NEW_TOKEN=$(curl -s -X POST "https://api.soundcloud.com/oauth2/token" \
      -d "client_id=$CLIENT_ID" \
      -d "client_secret=$CLIENT_SECRET" \
      -d "grant_type=refresh_token" \
      -d "refresh_token=$REFRESH_TOKEN" | jq -r '.access_token')
    
    # Update environment
    echo "$NEW_TOKEN" > token.txt
    export SOUNDCLOUD_ACCESS_TOKEN="$NEW_TOKEN"
fi
```

### 2. Request Security

#### Input Sanitization
```bash
sanitize_input() {
    local input="$1"
    
    # Remove potentially dangerous characters
    input=$(echo "$input" | tr -d ';|&$`')
    
    # Limit length
    input=$(echo "$input" | cut -c1-100)
    
    echo "$input"
}

# Usage
SAFE_QUERY=$(sanitize_input "$USER_QUERY")
```

#### HTTPS Enforcement
```bash
# Always use HTTPS
API_BASE="https://api.soundcloud.com"

# Verify SSL certificates
curl --ssl-verify "$API_BASE/..."
```

## Monitoring & Logging

### 1. Comprehensive Logging

#### Structured Logging
```bash
#!/bin/bash
# log_helper.sh

log_api_call() {
    local endpoint="$1"
    local status="$2"
    local duration="$3"
    
    echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") | \
          ENDPOINT=$endpoint | \
          STATUS=$status | \
          DURATION=${duration}ms | \
          CLIENT_ID=${SOUNDCLOUD_CLIENT_ID:0:8}..." >> api.log
}

# Usage
START=$(date +%s%N)
response=$(curl -s "$URL")
END=$(date +%s%N)
DURATION=$(( (END - START) / 1000000 ))

log_api_call "$URL" "$?" "$DURATION"
```

#### Performance Metrics
```bash
#!/bin/bash
# collect_metrics.sh

collect_metrics() {
    echo "=== SoundCloud API Metrics ==="
    echo "Timestamp: $(date)"
    echo ""
    
    # API response times
    echo "Response Times (ms):"
    grep "DURATION" api.log | tail -10 | awk -F'|' '{print $4}' | \
        awk -F'=' '{print $2}' | sort -n | \
        awk 'NR==1{min=$1} NR==NF{max=$1} {sum+=$1} END{print "  Min:", min, "Max:", max, "Avg:", sum/NR}'
    
    # Success rate
    total=$(grep -c "ENDPOINT" api.log 2>/dev/null || echo 0)
    errors=$(grep -c "STATUS=[1-9]" api.log 2>/dev/null || echo 0)
    if [ $total -gt 0 ]; then
        success_rate=$(( 100 * (total - errors) / total ))
        echo "Success Rate: ${success_rate}%"
    fi
    
    # Rate limit status
    echo "Rate Limit Headers from last request:"
    grep -i "x-ratelimit" last_response_headers.txt 2>/dev/null || echo "  Not available"
}
```

### 2. Alerting

#### Error Threshold Alerts
```bash
#!/bin/bash
# check_errors.sh

ERROR_THRESHOLD=5  # Errors per hour
CURRENT_HOUR=$(date +%Y-%m-%d-%H)

ERROR_COUNT=$(grep "$CURRENT_HOUR" api.log | grep -c "STATUS=[1-9]")

if [ $ERROR_COUNT -ge $ERROR_THRESHOLD ]; then
    echo "ALERT: High error rate detected"
    echo "Hour: $CURRENT_HOUR"
    echo "Errors: $ERROR_COUNT"
    echo "Threshold: $ERROR_THRESHOLD"
    
    # Send alert (example: email, Slack, etc.)
    # send_alert "SoundCloud API High Error Rate"
fi
```

#### Rate Limit Alerts
```bash
check_rate_limit() {
    local remaining=$(grep -i "x-ratelimit-remaining" last_response_headers.txt | tail -1 | awk '{print $2}')
    
    if [ -n "$remaining" ] && [ "$remaining" -lt 100 ]; then
        echo "WARNING: Rate limit getting low"
        echo "Remaining requests: $remaining"
    fi
}
```

## Development Workflow

### 1. Testing Strategy

#### Unit Tests for API Calls
```python
# test_soundcloud_api.py
import unittest
from unittest.mock import patch, Mock
import soundcloud_api

class TestSoundCloudAPI(unittest.TestCase):
    
    @patch('soundcloud_api.requests.get')
    def test_search_tracks(self, mock_get):
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = [
            {'id': 123, 'title': 'Test Track'}
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test function
        results = soundcloud_api.search_tracks('test')
        
        # Assertions
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 123)
        mock_get.assert_called_once()
```

#### Integration Tests
```bash
#!/bin/bash
# integration_test.sh

set -e

echo "Running SoundCloud API integration tests..."
echo ""

# Test 1: Search tracks
echo "Test 1: Track search"
if ./scripts/search_tracks.sh "test" --limit 1 --json > /dev/null; then
    echo "✓ Passed"
else
    echo "✗ Failed"
    exit 1
fi

# Test 2: Get track details
echo "Test 2: Track analysis"
if ./scripts/analyze_track.sh "293" > /dev/null 2>&1; then
    echo "✓ Passed"
else
    echo "✗ Failed (may need valid track ID)"
fi

echo ""
echo "All tests completed"
```

### 2. Development Environment

#### Docker Configuration
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install jq for JSON processing
RUN apt-get update && apt-get install -y jq curl

# Copy scripts
COPY scripts/ ./scripts/
RUN chmod +x scripts/*.sh

# Set environment
ENV SOUNDCLOUD_CLIENT_ID=""
ENV SOUNDCLOUD_ACCESS_TOKEN=""

# Entry point
CMD ["bash"]
```

#### Makefile for Common Tasks
```makefile
# Makefile

.PHONY: test lint format clean

test:
	./integration_test.sh

lint:
	shellcheck scripts/*.sh

format:
	shfmt -w scripts/*.sh

clean:
	rm -f *.log *.json *.csv cache/*

deploy:
	./scripts/package_skill.sh
	cp soundcloud.skill /path/to/deployment/
```

## Production Readiness Checklist

### Before Deployment
- [ ] Rate limiting implemented with exponential backoff
- [ ] Comprehensive error handling and logging
- [ ] Input validation and sanitization
- [ ] Secure credential storage
- [ ] Caching strategy defined
- [ ] Monitoring and alerting configured
- [ ] Backup and recovery plan
- [ ] Documentation updated

### Performance Checklist
- [ ] API calls batched where possible
- [ ] Pagination implemented efficiently
- [ ] Response caching enabled
- [ ] Database indexes optimized
- [ ] CDN configured for static assets

### Security Checklist
- [ ] HTTPS enforced for all requests
- [ ] API tokens rotated regularly
- [ ] Input validation prevents injection
- [ ] Access controls implemented
- [ ] Security headers configured

### Maintenance Checklist
- [ ] Regular token rotation scheduled
- [ ] Cache invalidation strategy
- [ ] Database cleanup scheduled
- [ ] Log rotation configured
- [ ] Backup verification automated

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. "API returning 401 Unauthorized"
- Check client ID is valid and not expired
- Verify access token hasn't been revoked
- Ensure proper authentication header format

#### 2. "Slow response times"
- Implement caching for frequent requests
- Batch multiple requests together
- Check network latency and DNS resolution

#### 3. "Missing data in responses"
- Some fields require specific permissions
- Check if user has access to private content
- Verify API version compatibility

#### 4. "Inconsistent pagination"
- Use `linked_partitioning=true` for consistent results
- Handle `next_href` instead of manual offset calculation
- Account for tracks being added/deleted during pagination

#### 5. "Rate limiting issues"
- Implement exponential backoff
- Cache responses to reduce