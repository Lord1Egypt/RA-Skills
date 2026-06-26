# Real-Time Grid Updates

## Table of Contents
- [Overview](#overview)
- [Auto-Refresh Strategy](#auto-refresh-strategy)
- [WebSocket Integration](#websocket-integration)
- [SignalR Integration](#signalr-integration)

---

## Overview

When building production grids, real-time data updates are often required. This guide covers three common patterns:

1. **Polling**: Periodic refreshes (simplest, less efficient)
2. **WebSocket**: True push updates from server
3. **SignalR**: ASP.NET Core real-time communication

Choose based on your backend architecture and latency requirements.

---

## Auto-Refresh Strategy

**Use case**: When you need periodic data syncing without live push.

```tsx
import React, { useRef, useEffect, useState } from 'react';
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-grids';

function GridWithAutoRefresh() {
  const gridRef = useRef(null);
  const [refreshInterval, setRefreshInterval] = useState(5000);  // 5 seconds
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        setIsLoading(true);
        const response = await fetch('/api/orders');
        
        if (!response.ok) throw new Error('Failed to fetch');
        
        const newData = await response.json();
        
        // Update grid data
        if (gridRef.current) {
          gridRef.current.dataSource = newData;
        }
      } catch (error) {
        console.error('Refresh error:', error);
      } finally {
        setIsLoading(false);
      }
    }, refreshInterval);

    return () => clearInterval(interval);
  }, [refreshInterval]);

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <label>Refresh every: </label>
        <select 
          value={refreshInterval} 
          onChange={(e) => setRefreshInterval(parseInt(e.target.value))}
          disabled={isLoading}
        >
          <option value='1000'>1 second</option>
          <option value='5000'>5 seconds</option>
          <option value='10000'>10 seconds</option>
          <option value='30000'>30 seconds</option>
        </select>
        {isLoading && <span> • Refreshing...</span>}
      </div>

      <GridComponent ref={gridRef} dataSource={[]} allowPaging={true}>
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
          <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
          <ColumnDirective field='Freight' headerText='Freight' format='C2' />
        </ColumnsDirective>
        <Inject services={[Page]} />
      </GridComponent>
    </div>
  );
}

export default GridWithAutoRefresh;
```

**Key Points:**
- Set appropriate intervals (don't hammer the server with sub-second refreshes)
- Show loading state to users
- Handle errors gracefully
- Clear interval on component unmount

---

## WebSocket Integration

**Use case**: Near real-time updates from any backend technology.

```tsx
import React, { useRef, useEffect, useState } from 'react';
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';

function GridWithWebSocket() {
  const gridRef = useRef(null);
  const wsRef = useRef(null);
  const [connectionStatus, setConnectionStatus] = useState('Connecting...');

  useEffect(() => {
    try {
      const ws = new WebSocket('url');

      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('Connected');
        wsRef.current = ws;
      };

      ws.onmessage = (event) => {
        try {
          const newData = JSON.parse(event.data);
          
          if (!gridRef.current || !gridRef.current.dataSource) return;
          
          const data = gridRef.current.dataSource;
          const index = data.findIndex(item => item.OrderID === newData.OrderID);
          
          if (index >= 0) {
            // Update existing row
            Object.assign(data[index], newData);
            gridRef.current.setCellValue(index, 'Freight', newData.Freight);
          } else {
            // Add new row
            gridRef.current.addRecord(newData);
          }
        } catch (error) {
          console.error('Error processing message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('Connection Error');
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnectionStatus('Disconnected');
      };

      return () => ws.close();
    } catch (error) {
      console.error('WebSocket setup error:', error);
      setConnectionStatus('Setup Failed');
    }
  }, []);

  return (
    <div>
      <div style={{ marginBottom: '10px', fontSize: '12px', color: '#666' }}>
        Status: <strong>{connectionStatus}</strong>
      </div>

      <GridComponent ref={gridRef} dataSource={[]} allowPaging={true}>
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
          <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
          <ColumnDirective field='Freight' headerText='Freight' format='C2' />
        </ColumnsDirective>
      </GridComponent>
    </div>
  );
}

export default GridWithWebSocket;
```

**Benefits:**
- Minimal latency (true push)
- Efficient (only sends updates, not full grid)
- Works across any backend

**Challenges:**
- Requires WebSocket support on server
- Harder to implement filtering/pagination on real-time flow

---

## SignalR Integration

**Use case**: ASP.NET Core applications with SignalR HubConnections.

```tsx
import React, { useRef, useEffect, useState } from 'react';
import * as signalR from '@microsoft/signalr';
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-grids';

function GridWithSignalR() {
  const gridRef = useRef(null);
  const connectionRef = useRef(null);
  const [connectionState, setConnectionState] = useState('Connecting...');

  useEffect(() => {
    const connection = new signalR.HubConnectionBuilder()
      .withUrl('/orderHub')
      .withAutomaticReconnect([1000, 2000, 5000, 10000, null]) // Exponential backoff
      .build();

    connectionRef.current = connection;

    // Handle OrderUpdated  event
    connection.on('OrderUpdated', (updatedOrder) => {
      if (!gridRef.current || !gridRef.current.dataSource) return;
      
      const data = gridRef.current.dataSource;
      const index = data.findIndex(o => o.OrderID === updatedOrder.OrderID);
      
      if (index >= 0) {
        Object.assign(data[index], updatedOrder);
        // Update specific cells for efficiency
        gridRef.current.setCellValue(index, 'Freight', updatedOrder.Freight);
        gridRef.current.setCellValue(index, 'Status', updatedOrder.Status);
      }
    });

    // Handle OrderAdded event
    connection.on('OrderAdded', (newOrder) => {
      gridRef.current.addRecord(newOrder);
    });

    // Handle OrderDeleted event
    connection.on('OrderDeleted', (orderId) => {
      if (!gridRef.current || !gridRef.current.dataSource) return;
      
      const data = gridRef.current.dataSource;
      const index = data.findIndex(o => o.OrderID === orderId);
      if (index >= 0) {
        gridRef.current.deleteRecord('OrderID', data[index]);
      }
    });

    // Connection state changes
    connection.onreconnecting(() => setConnectionState('Reconnecting...'));
    connection.onreconnected(() => setConnectionState('Connected'));
    connection.onclose(() => setConnectionState('Disconnected'));

    // Start connection
    connection.start()
      .then(() => {
        console.log('SignalR connected');
        setConnectionState('Connected');
      })
      .catch(err => {
        console.error('SignalR connection error:', err);
        setConnectionState('Connection Failed');
      });

    return () => connection.stop();
  }, []);

  return (
    <div>
      <div style={{ marginBottom: '10px', fontSize: '12px', color: '#666' }}>
        SignalR Status: <strong>{connectionState}</strong>
      </div>

      <GridComponent ref={gridRef} dataSource={[]} allowPaging={true}>
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' isPrimaryKey={true} width='100' />
          <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
          <ColumnDirective field='Freight' headerText='Freight' format='C2' />
          <ColumnDirective field='Status' headerText='Status' width='100' />
        </ColumnsDirective>
        <Inject services={[Page]} />
      </GridComponent>
    </div>
  );
}

export default GridWithSignalR;
```

**Benefits:**
- Built-in reconnection handling
- Server manages connection state
- Supports multiple clients
- Easy to implement on ASP.NET Core

---
