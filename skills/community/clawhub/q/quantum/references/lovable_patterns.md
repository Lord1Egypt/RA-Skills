# Lovable Frontend Patterns for Quantum Apps

This document provides patterns, components, and best practices for building frontend interfaces for quantum computing applications using Lovable (React + TypeScript). Designed specifically for the Guppy/Selene backend integration.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Core Components](#core-components)
3. [Quantum Dashboard Pattern](#quantum-dashboard-pattern)
4. [State Management](#state-management)
5. [Real-Time Updates](#real-time-updates)
6. [Result Visualization](#result-visualization)
7. [Error Handling](#error-handling)
8. [Performance Optimization](#performance-optimization)
9. [Responsive Design](#responsive-design)
10. [Deployment](#deployment)

## Project Structure

```
quantum-app-frontend/
├── src/
│   ├── components/
│   │   ├── QuantumDashboard.tsx  # Main dashboard component
│   │   ├── QuantumResult.tsx     # Result display component
│   │   ├── ParameterEditor.tsx   # Parameter input form
│   │   ├── JobStatus.tsx         # Job status tracker (async)
│   │   └── ui/                   # Reusable UI components
│   │       ├── Card.tsx
│   │       ├── Button.tsx
│   │       └── Input.tsx
│   ├── lib/
│   │   ├── api.ts                # API client configuration
│   │   ├── quantumClient.ts      # Quantum API wrapper
│   │   └── types.ts              # TypeScript type definitions
│   ├── App.tsx
│   └── main.tsx
├── public/
└── package.json
```

## Core Components

### API Client Setup

`src/lib/api.ts`:
```typescript
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8080';

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth (if needed)
api.interceptors.request.use(
  (config) => {
    const apiKey = import.meta.env.VITE_API_KEY;
    if (apiKey) {
      config.headers.Authorization = `Bearer ${apiKey}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 429) {
      const retryAfter = error.response.headers['retry-after'];
      console.warn(`Rate limited. Retry after ${retryAfter}s`);
    }
    return Promise.reject(error);
  }
);
```

### Quantum API Wrapper

`src/lib/quantumClient.ts`:
```typescript
import { api } from './api';

export interface QuantumParams {
  shots?: number;
  precision?: number;
  [key: string]: any;
}

export interface QuantumResult<T = any> {
  application: string;
  use_case: string;
  timestamp: string;
  status: 'success' | 'error';
  result: T;
  statistics: {
    shots: number;
    execution_time_ms: number;
    hardware_used: string;
  };
}

export interface JobStatus {
  job_id: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  created_at: string;
  progress: number;
  queue_position?: number;
  error?: { code: string; message: string };
}

class QuantumClient {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || API_BASE;
  }

  // Synchronous execution (wait=true)
  async compute<T = any>(useCase: string, params: QuantumParams): Promise<QuantumResult<T>> {
    const response = await api.post<QuantumResult<T>>(`/api/${useCase}/compute`, {
      params,
      wait: true,
      timeout_ms: 30000,
    });
    return response.data;
  }

  // Asynchronous execution (wait=false)
  async submitJob(useCase: string, params: QuantumParams): Promise<{ job_id: string }> {
    const response = await api.post<{ job_id: string }>(`/api/${useCase}/compute`, {
      params,
      wait: false,
    });
    return response.data;
  }

  async getJobStatus(jobId: string): Promise<JobStatus> {
    const response = await api.get<JobStatus>(`/api/jobs/${jobId}`);
    return response.data;
  }

  async getJobResult<T = any>(jobId: string): Promise<QuantumResult<T>> {
    const response = await api.get<QuantumResult<T>>(`/api/jobs/${jobId}/result`);
    return response.data;
  }

  async pollJob<T = any>(
    jobId: string,
    onProgress?: (status: JobStatus) => void,
    maxAttempts = 120
  ): Promise<QuantumResult<T>> {
    for (let i = 0; i < maxAttempts; i++) {
      const status = await this.getJobStatus(jobId);

      if (onProgress) {
        onProgress(status);
      }

      if (status.status === 'completed') {
        return await this.getJobResult<T>(jobId);
      } else if (status.status === 'failed') {
        throw new Error(status.error?.message || 'Job failed');
      }

      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    throw new Error('Job timeout');
  }

  async health(): Promise<{ status: string; guppy_available: boolean }> {
    const response = await api.get('/health');
    return response.data;
  }

  async info(): Promise<any> {
    const response = await api.get('/api/info');
    return response.data;
  }
}

export const quantumClient = new QuantumClient();
```

## Quantum Dashboard Pattern

The main dashboard component that provides a complete interface for quantum computation:

`src/components/QuantumDashboard.tsx`:
```typescript
import { useState } from 'react';
import { quantumClient, QuantumParams, QuantumResult } from '../lib/quantumClient';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Button } from './ui/Button';
import { Activity, Cpu } from 'lucide-react';

interface QuantumDashboardProps {
  useCase: string;
  defaultParams?: QuantumParams;
  onResult?: (result: QuantumResult) => void;
}

export function QuantumDashboard({
  useCase,
  defaultParams = { shots: 1000 },
  onResult
}: QuantumDashboardProps) {
  const [params, setParams] = useState<QuantumParams>(defaultParams);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QuantumResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runComputation = async () => {
    setLoading(true);
    setError(null);
    try {
      const computedResult = await quantumClient.compute(useCase, params);
      setResult(computedResult);
      onResult?.(computedResult);
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || err.message;
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-5 h-5" />
            Quantum Computation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ParameterEditor
            params={params}
            onChange={setParams}
            useCase={useCase}
          />
          <Button
            onClick={runComputation}
            disabled={loading}
            className="w-full mt-4"
          >
            {loading ? (
              <>
                <Cpu className="w-4 h-4 mr-2 animate-spin" />
                Running Quantum Algorithm...
              </>
            ) : (
              'Run Quantum Computation'
            )}
          </Button>
          {error && (
            <div className="mt-4 p-4 bg-red-900 border border-red-700 rounded text-red-200">
              {error}
            </div>
          )}
          {result && <QuantumResult result={result} />}
        </CardContent>
      </Card>
    </div>
  );
}
```

### Parameter Editor Component

`src/components/ParameterEditor.tsx`:
```typescript
import { QuantumParams } from '../lib/quantumClient';

interface ParameterEditorProps {
  params: QuantumParams;
  onChange: (params: QuantumParams) => void;
  useCase: string;
}

const PARAM_DEFINITIONS: Record<string, Array<{
  name: keyof QuantumParams;
  label: string;
  type: 'number' | 'range' | 'select';
  min?: number;
  max?: number;
  step?: number;
  options?: Array<{ value: number; label: string }>;
}>> = {
  optimization: [
    { name: 'shots', label: 'Shots', type: 'number', min: 100, max: 10000, step: 100 },
    { name: 'precision', label: 'Precision', type: 'range', min: 0.001, max: 0.1, step: 0.001 },
  ],
  random: [
    { name: 'bits', label: 'Bits', type: 'number', min: 1, max: 64, step: 1 },
    { name: 'shots', label: 'Shots', type: 'number', min: 1, max: 1000, step: 10 },
  ],
  chemistry: [
    { name: 'shots', label: 'Shots', type: 'number', min: 1000, max: 100000, step: 1000 },
    { name: 'molecule', label: 'Molecule', type: 'select',
      options: [
        { value: 0, label: 'H2' },
        { value: 1, label: 'LiH' },
        { value: 2, label: 'BeH2' },
      ]
    },
  ],
};

export function ParameterEditor({ params, onChange, useCase }: ParameterEditorProps) {
  const definitions = PARAM_DEFINITIONS[useCase] || [];

  if (definitions.length === 0) {
    return (
      <div className="text-gray-400 p-4 border border-gray-700 rounded">
        <p>No configurable parameters for this quantum use case.</p>
        <p className="text-sm mt-2">Click "Run Quantum Computation" to execute.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <p className="text-sm font-medium text-gray-300">Parameters:</p>
      {definitions.map(({ name, label, type, min, max, step, options }) => {
        const value = params[name] ?? (type === 'range' ? 0.01 : undefined);

        return (
          <div key={name} className="space-y-2">
            <label className="block text-sm font-medium text-gray-300">
              {label}
            </label>
            {type === 'number' && (
              <input
                type="number"
                min={min}
                max={max}
                step={step}
                value={value}
                onChange={(e) => onChange({ ...params, [name]: Number(e.target.value) })}
                className="w-full p-2 bg-gray-800 border border-gray-700 rounded text-white"
              />
            )}
            {type === 'range' && (
              <input
                type="range"
                min={min}
                max={max}
                step={step}
                value={value}
                onChange={(e) => onChange({ ...params, [name]: Number(e.target.value) })}
                className="w-full"
              />
            )}
            {type === 'select' && options && (
              <select
                value={value}
                onChange={(e) => onChange({ ...params, [name]: Number(e.target.value) })}
                className="w-full p-2 bg-gray-800 border border-gray-700 rounded text-white"
              >
                {options.map(opt => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            )}
            <p className="text-xs text-gray-500">
              {type === 'number' && `Range: ${min} - ${max}`}
              {type === 'range' && `Value: ${value}`}
            </p>
          </div>
        );
      })}
      <div className="text-xs text-gray-400 mt-2">
        Adjust parameters then run computation.
      </div>
    </div>
  );
}
```

### Quantum Result Display

`src/components/QuantumResult.tsx`:
```typescript
import { QuantumResult } from '../lib/quantumClient';
import { Card, CardHeader, CardTitle, CardContent } from './ui/Card';
import { Clock, Cpu, BarChart3 } from 'lucide-react';

interface QuantumResultProps {
  result: QuantumResult;
}

export function QuantumResult({ result }: QuantumResultProps) {
  const { result: data, statistics } = result;

  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle>Computation Results</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Execution stats */}
          <div className="grid grid-cols-3 gap-4 p-4 bg-gray-800 rounded">
            <div className="text-center">
              <Clock className="w-5 h-5 mx-auto text-blue-400" />
              <div className="text-2xl font-bold">{statistics.execution_time_ms}ms</div>
              <div className="text-xs text-gray-400">Execution Time</div>
            </div>
            <div className="text-center">
              <Cpu className="w-5 h-5 mx-auto text-green-400" />
              <div className="text-2xl font-bold">{statistics.shots.toLocaleString()}</div>
              <div className="text-xs text-gray-400">Shots</div>
            </div>
            <div className="text-center">
              <BarChart3 className="w-5 h-5 mx-auto text-purple-400" />
              <div className="text-2xl font-bold">{statistics.hardware_used}</div>
              <div className="text-xs text-gray-400">Hardware</div>
            </div>
          </div>

          {/* Result data */}
          <div>
            <h4 className="font-semibold mb-2">Result:</h4>
            <pre className="p-4 bg-gray-900 border border-gray-700 rounded overflow-x-auto text-sm">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>

          {/* Timestamp */}
          <div className="text-xs text-gray-500">
            Generated: {new Date(result.timestamp).toLocaleString()}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

## State Management

For simpler apps, React's built-in `useState` is sufficient. For complex apps with many quantum parameters and results, consider using TanStack Query or Zustand.

### Using TanStack Query

```typescript
// src/lib/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 0,
      retry: 1,
    },
  },
});
```

Wrap your app:

```typescript
// App.tsx
import {{ QueryClientProvider }} from '@tanstack/react-query';
import {{ queryClient }} from './lib/queryClient';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <QuantumDashboard useCase="optimization" />
    </QueryClientProvider>
  );
}
```

## Real-Time Updates

For long-running quantum jobs, implement progress tracking:

### Job Status Tracker

`src/components/JobStatus.tsx`:
```typescript
import { useEffect, useState } from 'react';
import { JobStatus as JobStatusType } from '../lib/quantumClient';
import { Progress } from './ui/Progress';

interface JobStatusProps {
  jobId: string;
  onComplete?: (result: any) => void;
}

export function JobStatus({ jobId, onComplete }: JobStatusProps) {
  const [status, setStatus] = useState<JobStatusType | null>(null);
  const [result, setResult] = useState(null);

  useEffect(() => {
    let mounted = true;
    let interval: NodeJS.Timeout;

    const poll = async () => {
      try {
        const currentStatus = await quantumClient.getJobStatus(jobId);
        if (mounted) {
          setStatus(currentStatus);

          if (currentStatus.status === 'completed' && !result) {
            const finalResult = await quantumClient.getJobResult(jobId);
            setResult(finalResult);
            onComplete?.(finalResult);
            clearInterval(interval);
          } else if (currentStatus.status === 'failed') {
            clearInterval(interval);
          }
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    };

    // Initial poll
    poll();

    // Poll every second
    interval = setInterval(poll, 1000);

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, [jobId, onComplete, result]);

  if (!status) return <div>Loading...</div>;

  return (
    <div className="space-y-4">
      <div className="flex justify-between">
        <span>Status: {status.status}</span>
        <span>{Math.round(status.progress * 100)}%</span>
      </div>
      <Progress value={status.progress * 100} />
      {status.queue_position && (
        <p className="text-sm text-gray-400">
          Queue position: {status.queue_position}
        </p>
      )}
    </div>
  );
}
```

## Result Visualization

### Simple Bar Chart

Use Recharts for quantum probability distributions:

```typescript
import {{ BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer }} from 'recharts';

interface ProbabilityChartProps {
  data: Array<{{ state: string; probability: number }}>
}

export function ProbabilityChart({{ data }}: ProbabilityChartProps) {{
  return (
    <ResponsiveContainer width="100%" height={{300}}>
      <BarChart data={{data}}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="state" />
        <YAxis label={{ value: 'Probability', angle: -90, position: 'insideLeft' }} />
        <Tooltip formatter={(value) => [`${{value.toFixed(4)}}`, 'Probability']} />
        <Bar dataKey="probability" fill="#3b82f6" />
      </BarChart>
    </ResponsiveContainer>
  );
}}
```

Usage in `QuantumResult`:

```typescript
// If result contains probability distribution
if (result.result.probabilities) {
  const chartData = Object.entries(result.result.probabilities).map(
    ([state, prob]) => ({ state, probability: prob as number })
  );
  return <ProbabilityChart data={chartData} />;
}
```

## Error Handling

### Global Error Boundary

`src/components/ErrorBoundary.tsx`:
```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
    // Send to error tracking service
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="p-6 bg-red-900 border border-red-700 rounded">
          <h2 className="text-xl font-bold mb-2">Something went wrong</h2>
          <p className="text-red-200 mb-4">
            {this.state.error?.message || 'An unexpected error occurred'}
          </p>
          <button
            className="px-4 py-2 bg-blue-600 rounded"
            onClick={() => window.location.reload()}
          >
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### API Error Handling Hook

`src/hooks/useQuantumApi.ts`:
```typescript
import { useState } from 'react';
import { quantumClient, QuantumResult } from '../lib/quantumClient';

export function useQuantumApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runComputation = async (useCase: string, params: any): Promise<QuantumResult | null> => {
    setLoading(true);
    setError(null);
    try {
      const result = await quantumClient.compute(useCase, params);
      return result;
    } catch (err: any) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { runComputation, loading, error, clearError: () => setError(null) };
}
```

## Performance Optimization

### Lazy Loading Components

```typescript
import { lazy, Suspense } from 'react';

const QuantumDashboard = lazy(() => import('./components/QuantumDashboard'));

function App() {
  return (
    <Suspense fallback={<div>Loading quantum interface...</div>}>
      <QuantumDashboard useCase="optimization" />
    </Suspense>
  );
}
```

### Memoize Expensive Calculations

```typescript
import { useMemo } from 'react';

function QuantumResult({ result }: QuantumResultProps) {
  const processedData = useMemo(() => {
    // Expensive data transformation
    return processQuantumResult(result);
  }, [result]);

  return <div>{/* render processedData */}</div>;
}
```

### Virtual Scrolling for Large Results

If displaying thousands of quantum samples, use virtual scrolling:

```typescript
import { FixedSizeList as List } from 'react-window';

const Row = ({ index, style }: any) => (
  <div style={style}>Sample {index}: {data[index]}</div>
);

function SampleList({ samples }: { samples: string[] }) {
  return (
    <List height={400} itemCount={samples.length} itemSize={35} width="100%">
      {Row}
    </List>
  );
}
```

## Responsive Design

Tailwind CSS for responsive layouts:

```typescript
// Grid adapts to screen size
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// Responsive typography
<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">

// Mobile-first button
<button className="w-full md:w-auto px-4 py-2">
```

## Deployment

### Environment Variables

Create `.env` file:

```
VITE_API_URL=https://your-app.fly.dev
VITE_API_KEY=your_optional_api_key
```

### Build and Deploy to Lovable

1. Install dependencies:
   ```bash
   npm install
   ```

2. Test locally:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

4. Deploy to Lovable:
   - Import project into Lovable workspace
   - Set environment variables in Lovable dashboard
   - Deploy to Lovable hosting

### Deploy to Vercel/Netlify (Alternative)

```bash
# Vercel
vercel --prod

# Netlify
netlify deploy --prod --dir dist
```

Ensure API URL is set in hosting platform environment variables.

---

**For Selene API reference, see [selene_api.md](./selene_api.md)**
**For Fly.io configuration, see [flyio_config.md](./flyio_config.md)**
