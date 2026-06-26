# Query Patterns

## Raw curl examples

### Search events by keyword and country

```bash
curl --get "https://app.ticketmaster.com/discovery/v2/events.json" \
  --data-urlencode "apikey=$TM_API_KEY" \
  --data-urlencode "keyword=adele" \
  --data-urlencode "countryCode=GB" \
  --data-urlencode "size=5"
```

### Search events by city and classification

```bash
curl --get "https://app.ticketmaster.com/discovery/v2/events.json" \
  --data-urlencode "apikey=$TM_API_KEY" \
  --data-urlencode "city=Madrid" \
  --data-urlencode "classificationName=music" \
  --data-urlencode "startDateTime=2026-04-01T00:00:00Z" \
  --data-urlencode "size=10"
```

### Fetch one event by ID

```bash
curl --get "https://app.ticketmaster.com/discovery/v2/events/E123456.json" \
  --data-urlencode "apikey=$TM_API_KEY"
```

### Search venues

```bash
curl --get "https://app.ticketmaster.com/discovery/v2/venues.json" \
  --data-urlencode "apikey=$TM_API_KEY" \
  --data-urlencode "keyword=Madison Square Garden" \
  --data-urlencode "countryCode=US" \
  --data-urlencode "size=3"
```

### Search attractions

```bash
curl --get "https://app.ticketmaster.com/discovery/v2/attractions.json" \
  --data-urlencode "apikey=$TM_API_KEY" \
  --data-urlencode "keyword=Coldplay" \
  --data-urlencode "size=3"
```

## Helper commands with `ticketmaster.sh`

```bash
./ticketmaster.sh events "coldplay" --city Madrid --country ES --size 5
./ticketmaster.sh event E123456
./ticketmaster.sh venues "madison square garden" --country US --size 3
./ticketmaster.sh attractions "fc barcelona" --size 5
./ticketmaster.sh classifications
```

## Good inspection order

1. Search with minimal filters.
2. Add city or country.
3. Add date window or classification.
4. Capture event or venue IDs.
5. Fetch details by ID before making claims about timing or availability.
