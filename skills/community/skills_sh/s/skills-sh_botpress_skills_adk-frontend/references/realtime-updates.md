# Real-Time Updates

Learn how to keep your ADK frontend UI in sync with backend data using polling strategies.

## Polling vs WebSockets

### When to Use Polling (Most Cases)

**Polling is the recommended approach for most ADK frontends** because:

- **Simpler Implementation**: No connection management, reconnection logic, or WebSocket server setup
- **More Reliable**: Works through firewalls, proxies, and corporate networks
- **Easier to Debug**: Standard HTTP requests visible in DevTools
- **Better Resource Control**: You control exactly when and how often to fetch
- **Sufficient for Most Use Cases**: 1-3 second updates feel real-time to users

### When to Consider WebSockets (Rare)

Only use WebSockets if you absolutely need:

- **Sub-second updates** (<1s) for critical real-time features
- **Bi-directional push** from server (though server-sent events are simpler)
- **Multiplayer/collaborative** features with many concurrent users

For ADK applications, polling with TanStack Query is almost always the right choice.

---

## TanStack Query refetchInterval

TanStack Query provides built-in polling through the `refetchInterval` option. The simplest approach uses `useQuery` directly:

### Basic Pattern with useQuery

```typescript
import { useQuery } from "@tanstack/react-query";
import { listTickets } from "../services/tickets";

function ActiveTickets() {
  const { data, isLoading } = useQuery({
    queryKey: ["tickets", "active"],
    queryFn: () => listTickets({
      filter: { state: { $in: ["open", "snoozed"] } },
      limit: 1000,
      orderBy: "updatedAt",
      orderDirection: "desc",
    }),
    refetchInterval: 1000 * 3, // 3 seconds
  });

  if (isLoading) return <LoadingSpinner />;
  return <TicketList tickets={data?.rows ?? []} />;
}
```

### Different Intervals for Different Data

Not all data needs the same refresh rate. Choose intervals based on:

1. **How frequently the data changes**
2. **How critical updates are to the user**
3. **The cost of fetching (network, battery, server load)**

---

## Recommended Polling Intervals

Here are production-tested intervals for common data types:

### 1. Messages (1 second)

**The most critical real-time data** — messages in an active conversation:

```typescript
function useMessages(ticketId?: string) {
  return useQuery({
    queryKey: ['messages', ticketId],
    enabled: !!ticketId,
    queryFn: () => {
      if (!ticketId) return { rows: [] }
      return listMessages(ticketId, {
        limit: 1000,
        orderBy: 'createdAt',
        orderDirection: 'asc',
      })
    },
    refetchInterval: 1000, // 1 second
  })
}
```

**Why 1 second**: When viewing a specific conversation, users expect near-instant updates. 1 second is the fastest practical polling interval without overwhelming the network.

### 2. Active Items (3 seconds)

**User-facing critical data** — items the user is actively monitoring:

```typescript
function useActiveTickets() {
  return useQuery({
    queryKey: ['tickets', 'active'],
    queryFn: () =>
      listTickets({
        filter: { state: { $in: ['open', 'snoozed'] } },
        limit: 1000,
        orderBy: 'updatedAt',
        orderDirection: 'desc',
      }),
    refetchInterval: 1000 * 3, // 3 seconds
  })
}
```

**Why 3 seconds**: Active items are the main focus of the UI. 3 seconds feels real-time while being network-friendly.

### 3. Analysis/Computed Data (5 seconds)

**Background processing results** — analysis or computed data:

```typescript
function useAnalysis(ticketId?: string) {
  return useQuery({
    queryKey: ['analysis', ticketId],
    enabled: !!ticketId,
    queryFn: () => {
      if (!ticketId) return { rows: [] }
      return listAnalysisResults(ticketId, {
        limit: 1000,
        orderBy: 'updatedAt',
        orderDirection: 'desc',
      })
    },
    refetchInterval: 1000 * 5, // 5 seconds
  })
}
```

**Why 5 seconds**: Analysis runs in the background. 5 seconds balances freshness with cost.

### 4. Background Data (30 seconds)

**Secondary data** — closed items users aren't actively viewing:

```typescript
function useClosedTickets() {
  return useQuery({
    queryKey: ['tickets', 'closed'],
    queryFn: () =>
      listTickets({
        filter: { state: 'closed' },
        limit: 1000,
        orderBy: 'updatedAt',
        orderDirection: 'desc',
      }),
    refetchInterval: 1000 * 30, // 30 seconds
  })
}
```

**Why 30 seconds**: Closed items rarely change. Keeps data fresh without wasting resources.

### 5. Static/Config Data (5 minutes)

**Rarely changes** — admin lists, configuration data:

```typescript
function useAdminList() {
  return useQuery({
    queryKey: ['admins'],
    queryFn: () => listAdmins(),
    refetchInterval: 1000 * 60 * 5, // 5 minutes
  })
}
```

**Why 5 minutes**: Admin lists change very rarely. Minimizes network overhead.

---

## Choosing the Right Interval

| Data Type                | Interval   | Use Case                                          |
| ------------------------ | ---------- | ------------------------------------------------- |
| **User-facing critical** | 1-3s       | Active items, live messages, real-time dashboards |
| **Secondary/contextual** | 5-10s      | Analysis results, background processing status    |
| **Background data**      | 30s-1min   | Closed items, historical data, secondary lists    |
| **Static/config data**   | 5+ minutes | User lists, settings, configuration               |

### Cost vs UX Trade-off

**Faster intervals**:

- Better user experience
- More real-time feel
- Higher network costs, more server load, battery drain on mobile

**Slower intervals**:

- Lower network/server costs, better battery life
- Less responsive feel, users may miss updates

**Best Practice**: Start with conservative intervals (5-10s) and only optimize to faster intervals where it measurably improves UX.

---

## Conditional Refetching

### The `enabled` Pattern

Only fetch data when it's actually needed:

```typescript
function useMessages(ticketId?: string) {
  return useQuery({
    queryKey: ['messages', ticketId],
    enabled: !!ticketId, // Only fetch if ticketId exists
    queryFn: () => {
      if (!ticketId) return { rows: [] }
      return listMessages(ticketId)
    },
    refetchInterval: 1000,
  })
}
```

**Why this matters**:

- Saves network requests when no item is selected
- Prevents errors from invalid API calls
- Improves performance

### Pausing Queries When Not Needed

```typescript
const messagesQuery = useQuery({
  queryKey: ['messages', ticketId],
  enabled: isActive && !!ticketId, // Multiple conditions
  refetchInterval: isActive ? 1000 : false, // Stop polling when paused
  // ...
})
```

**Use cases**:

- User switches tabs (pause background tab queries)
- Modal/dialog is closed (pause modal-specific queries)
- Component is hidden (pause until visible)

---

## Visibility-Based Polling

### Slow Down for Background Tabs

Detect tab visibility and adjust intervals:

```typescript
function useActiveTickets() {
  const [isVisible, setIsVisible] = useState(!document.hidden)

  useEffect(() => {
    const handleVisibilityChange = () => setIsVisible(!document.hidden)
    document.addEventListener('visibilitychange', handleVisibilityChange)
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange)
  }, [])

  return useQuery({
    queryKey: ['tickets', 'active'],
    queryFn: () => listTickets({ filter: { state: { $in: ['open', 'snoozed'] } } }),
    refetchInterval: isVisible ? 1000 * 3 : 1000 * 30,
  })
}
```

### Pause/Resume with visibilitychange

```typescript
useEffect(() => {
  const handleVisibilityChange = () => {
    if (document.hidden) {
      queryClient.setQueryDefaults(['messages'], {
        refetchInterval: false,
      })
    } else {
      queryClient.setQueryDefaults(['messages'], {
        refetchInterval: 1000,
      })
    }
  }

  document.addEventListener('visibilitychange', handleVisibilityChange)
  return () => document.removeEventListener('visibilitychange', handleVisibilityChange)
}, [])
```

---

## Best Practices

### 1. Use Appropriate Intervals

Match polling frequency to data importance:

```typescript
// Critical data polls frequently
refetchInterval: 1000 * 1 // Messages: 1 second

// Background data polls slowly
refetchInterval: 1000 * 60 * 5 // Admin list: 5 minutes

// Don't poll everything at 1 second!
```

### 2. Combine Polling + Optimistic Updates

Get the best of both worlds:

- **Optimistic updates**: Make UI feel instant for user actions
- **Polling**: Catches updates from other users and external events

```typescript
// User action — instant feedback via optimistic update
await closeTicket({ ticketId, agentId })

// Polling — catches updates from other agents
refetchInterval: 1000 * 3 // Background sync
```

### 3. Pause Inactive Queries

Save resources when data isn't visible:

```typescript
const messagesQuery = useQuery({
  queryKey: ['messages', ticketId],
  enabled: isTicketOpen, // Pause when closed
  refetchInterval: isTicketOpen ? 1000 : false,
  queryFn: () => listMessages(ticketId),
})
```

### 4. Handle Connection Errors

Polling continues even if requests fail. Handle errors gracefully:

```typescript
const { data, error, isLoading, refetch } = useQuery({
  queryKey: ["tickets"],
  queryFn: () => listTickets({ state: "open" }),
  refetchInterval: 3000,
});

if (error) {
  return <ErrorBanner error={error} onRetry={() => refetch()} />;
}
```

### 5. Show Loading/Stale Indicators

Let users know when data might be outdated:

```typescript
const { data, isFetching, isStale } = useQuery({
  queryKey: ["tickets"],
  queryFn: fetchTickets,
  refetchInterval: 3000,
});

return (
  <div>
    {isFetching && <Spinner />}
    {isStale && <StaleDataBadge />}
    <TicketList tickets={data?.rows ?? []} />
  </div>
);
```

---

## Performance Considerations

### Network Cost of Polling

**Example**: 10 active users polling at 1-second intervals

- 10 requests/second
- 600 requests/minute
- 36,000 requests/hour

**Mitigation**:

- Use slower intervals for non-critical data
- Pause queries when not visible
- Consider WebSockets only if costs become prohibitive (rare)

### Battery Impact on Mobile

Frequent polling drains mobile device batteries:

**Best practices**:

- Use 5+ second intervals on mobile
- Pause polling when app is in background
- Use `visibilitychange` events to pause/resume

### Use Longer Intervals for Background Tabs

```typescript
const refetchInterval =
  document.visibilityState === 'visible'
    ? 1000 * 3 // Active tab: 3 seconds
    : 1000 * 30 // Background tab: 30 seconds
```

---

## Summary

**Polling Strategy**:

- Use `refetchInterval` on `useQuery` for most real-time needs
- Match intervals to data importance (1s–5min range)
- WebSockets are rarely needed for ADK frontends

**Performance**:

- Pause queries when not needed (`enabled` flag)
- Slow down for background tabs (`visibilitychange`)
- Show loading/stale indicators
- Handle errors gracefully
- Consider battery/network costs

**Production Intervals**:

- Messages: 1 second
- Active items: 3 seconds
- Analysis: 5 seconds
- Closed items: 30 seconds
- Config data: 5 minutes

This approach provides a responsive, real-time feel while being network-efficient and battery-friendly.

---

## See Also

- **[Data Fetching](./data-fetching.md)** — TanStack Query setup, mutations, and Collections
- **[Calling Actions](./calling-actions.md)** — Optimistic update patterns with actions
- **[State Management](./state-management.md)** — Zustand vs TanStack Query decision
- **[Service Layer](./service-layer.md)** — Service functions used by queries
- **[Overview](./overview.md)** — Architecture and synchronization concepts
