---
name: websocket-tester
description: Test WebSocket connections, message flows, and real-time features. Connect to endpoints, send/receive messages, test reconnection logic, measure latency, validate message schemas, and load test concurrent connections.
---

# WebSocket Tester

Test WebSocket endpoints without a browser. Connect, send messages, validate responses, test reconnection, measure latency, and load test concurrent connections — for chat, real-time updates, game servers, IoT, and streaming APIs.

Use when: "test websocket", "websocket not connecting", "debug real-time", "ws connection issues", "websocket load test", "test socket.io", "chat server testing", or when building/debugging real-time features.

## Commands

### 1. `connect` — Test WebSocket Connection

```bash
# Basic connection test with wscat (Node.js)
npx wscat -c "wss://$HOST/ws" 2>&1 &
WSCAT_PID=$!
sleep 3
kill $WSCAT_PID 2>/dev/null

# Or with websocat (Rust)
echo "test" | websocat "wss://$HOST/ws" 2>&1

# Or with Python
python3 -c "
import asyncio, websockets, time, json

async def test_connection():
    url = 'wss://$HOST/ws'
    start = time.time()
    try:
        async with websockets.connect(url, close_timeout=5) as ws:
            latency = (time.time() - start) * 1000
            print(f'✅ Connected in {latency:.0f}ms')
            print(f'Protocol: {ws.subprotocol or \"none\"}')
            print(f'Headers: {dict(ws.response_headers)}')

            # Test ping/pong
            pong = await ws.ping()
            await pong
            print('✅ Ping/Pong working')

            # Listen for initial messages (server hello, auth challenge)
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=3)
                print(f'Server sent: {msg[:200]}')
            except asyncio.TimeoutError:
                print('No initial message from server (normal for some protocols)')

    except websockets.exceptions.InvalidStatusCode as e:
        print(f'❌ Connection rejected: HTTP {e.status_code}')
    except ConnectionRefusedError:
        print(f'❌ Connection refused — server not listening on WebSocket endpoint')
    except Exception as e:
        print(f'❌ Error: {e}')

asyncio.run(test_connection())
" 2>&1
```

### 2. `test-messages` — Send and Validate Messages

```python
import asyncio, websockets, json, time

async def test_messages():
    async with websockets.connect('wss://$HOST/ws') as ws:
        # Test 1: Send and receive
        test_msg = json.dumps({'type': 'ping', 'data': 'hello'})
        await ws.send(test_msg)
        print(f'→ Sent: {test_msg}')

        response = await asyncio.wait_for(ws.recv(), timeout=5)
        print(f'← Received: {response[:200]}')

        # Validate response schema
        try:
            data = json.loads(response)
            assert 'type' in data, 'Missing type field'
            print('✅ Response is valid JSON with type field')
        except json.JSONDecodeError:
            print('⚠️ Response is not JSON — might be binary or plain text')
        except AssertionError as e:
            print(f'❌ Schema validation: {e}')

        # Test 2: Measure round-trip latency
        latencies = []
        for i in range(10):
            start = time.time()
            await ws.send(json.dumps({'type': 'ping', 'seq': i}))
            await asyncio.wait_for(ws.recv(), timeout=5)
            latencies.append((time.time() - start) * 1000)

        avg = sum(latencies) / len(latencies)
        p95 = sorted(latencies)[int(len(latencies) * 0.95)]
        print(f'\\nLatency (10 round-trips): avg={avg:.1f}ms, p95={p95:.1f}ms')

asyncio.run(test_messages())
```

### 3. `reconnect` — Test Reconnection Logic

```python
async def test_reconnection():
    """Simulate connection drops and verify client reconnects"""

    # Test 1: Server closes connection
    async with websockets.connect('wss://$HOST/ws') as ws:
        print('Connected. Sending close frame...')
        await ws.close(1001, 'Testing reconnection')
        print(f'Close code: {ws.close_code}, reason: {ws.close_reason}')

    # Test 2: Reconnect and verify state
    async with websockets.connect('wss://$HOST/ws') as ws:
        print('✅ Reconnected successfully')
        # Check if server restored session state
        await ws.send(json.dumps({'type': 'get_state'}))
        state = await asyncio.wait_for(ws.recv(), timeout=5)
        print(f'State after reconnect: {state[:200]}')

    # Test 3: Connection with auth token
    async with websockets.connect(
        'wss://$HOST/ws',
        extra_headers={'Authorization': f'Bearer {TOKEN}'}
    ) as ws:
        print('✅ Authenticated connection')
```

### 4. `load-test` — Concurrent Connection Load Test

```python
import asyncio, websockets, time, statistics

async def load_test(url, num_connections, duration_sec, messages_per_sec):
    """Load test WebSocket endpoint"""
    results = {
        'connected': 0,
        'failed': 0,
        'messages_sent': 0,
        'messages_received': 0,
        'latencies': [],
        'errors': [],
    }

    async def client(client_id):
        try:
            async with websockets.connect(url, close_timeout=5) as ws:
                results['connected'] += 1
                end_time = time.time() + duration_sec

                while time.time() < end_time:
                    start = time.time()
                    await ws.send(json.dumps({
                        'type': 'message',
                        'client': client_id,
                        'ts': start
                    }))
                    results['messages_sent'] += 1

                    try:
                        await asyncio.wait_for(ws.recv(), timeout=5)
                        results['messages_received'] += 1
                        results['latencies'].append((time.time() - start) * 1000)
                    except asyncio.TimeoutError:
                        results['errors'].append(f'Client {client_id}: timeout')

                    await asyncio.sleep(1.0 / messages_per_sec)

        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f'Client {client_id}: {e}')

    tasks = [client(i) for i in range(num_connections)]
    await asyncio.gather(*tasks)

    # Report
    lats = results['latencies']
    print(f'\\n=== WebSocket Load Test Results ===')
    print(f'Connections: {results["connected"]}/{num_connections} ({results["failed"]} failed)')
    print(f'Messages: {results["messages_sent"]} sent, {results["messages_received"]} received')
    if lats:
        print(f'Latency: avg={statistics.mean(lats):.1f}ms, '
              f'p50={statistics.median(lats):.1f}ms, '
              f'p95={sorted(lats)[int(len(lats)*0.95)]:.1f}ms, '
              f'p99={sorted(lats)[int(len(lats)*0.99)]:.1f}ms')
    if results['errors']:
        print(f'Errors ({len(results["errors"])}):')
        for e in results['errors'][:5]:
            print(f'  - {e}')

# Run: 100 concurrent connections, 60s, 1 msg/sec each
asyncio.run(load_test('wss://$HOST/ws', 100, 60, 1))
```

### 5. `diagnose` — Common WebSocket Issues

**Connection failures:**
- HTTP 101 upgrade rejected → check server supports WebSocket
- 403 on connect → CORS or auth issue
- Connection timeout → firewall blocking WS, or wrong port
- SSL/TLS error → certificate issue on wss://

**Message issues:**
- Messages not received → check subscription/room join logic
- Duplicate messages → missing deduplication, reconnect replay
- Out-of-order → add sequence numbers, reorder buffer
- Large messages rejected → check server max frame size

**Performance:**
- High latency → check server-side processing time
- Connection drops → heartbeat/ping interval too long
- Memory growth → connection leak (not closing on client disconnect)
