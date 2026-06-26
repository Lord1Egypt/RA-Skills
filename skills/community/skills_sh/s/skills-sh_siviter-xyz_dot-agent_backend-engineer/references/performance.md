# Backend Performance

Caching, query optimization, load balancing, and scaling strategies.

## Caching Strategies

### Cache-Aside Pattern
1. Check cache for data
2. If miss, fetch from database
3. Store in cache for future requests
4. Return data

### Write-Through Caching
1. Write to cache and database simultaneously
2. Ensures consistency
3. Higher write latency

### Write-Back Caching
1. Write to cache immediately
2. Write to database asynchronously
3. Risk of data loss on cache failure

### Redis Caching
- 90% database load reduction
- Sub-millisecond latency
- Use for session storage, rate limiting, leaderboards
- Set appropriate TTLs

## Database Query Optimization

### Indexing
- Add indexes to frequently queried columns
- Composite indexes for multi-column queries
- Monitor index usage
- 30% I/O reduction with proper indexing

### Query Optimization
- Use EXPLAIN to analyze queries
- Avoid N+1 queries (use eager loading)
- Limit result sets
- Use pagination for large datasets

### Connection Pooling
- Reuse database connections
- 5-10x performance boost
- Configure pool size based on load
- Monitor connection usage

## Load Balancing

### Strategies
- Round-robin - Distribute evenly
- Least connections - Route to least busy
- IP hash - Sticky sessions
- Geographic - Route by location

### Health Checks
- Monitor backend health
- Remove unhealthy instances
- Automatic failover
- Graceful degradation

## Scaling Strategies

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Simple but limited
- Use for moderate growth

### Horizontal Scaling
- Add more servers
- Requires load balancing
- Stateless application design
- Better for high growth

### Database Scaling
- Read replicas for read-heavy workloads
- Sharding for very large datasets
- Caching layer to reduce DB load
- Connection pooling

## CDN (Content Delivery Network)

- 50%+ latency reduction
- Cache static assets at edge
- Reduce origin server load
- Global distribution

## Monitoring & Profiling

### Key Metrics
- Response time (p50, p95, p99)
- Throughput (requests/second)
- Error rate
- Resource utilization (CPU, memory)

### Profiling Tools
- Application Performance Monitoring (APM)
- Database query profilers
- Memory profilers
- CPU profilers

### Best Practices
- Set up alerts for critical metrics
- Monitor error rates
- Track slow queries
- Profile regularly
- Optimize bottlenecks
