import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8080'

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for auth
api.interceptors.request.use(
  (config) => {
    const apiKey = import.meta.env.VITE_API_KEY
    if (apiKey) {
      config.headers.Authorization = `Bearer ${apiKey}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 429) {
      const retryAfter = error.response.headers['retry-after']
      console.warn(`Rate limited. Retry after ${retryAfter}s`)
    }
    return Promise.reject(error)
  }
)

export interface QuantumParams {
  shots?: number
  precision?: number
  [key: string]: any
}

export interface QuantumResult<T = any> {
  application: string
  use_case: string
  timestamp: string
  status: 'success' | 'error'
  result: T
  statistics: {
    shots: number
    execution_time_ms: number
    hardware_used: string
  }
}

export interface JobStatus {
  job_id: string
  status: 'queued' | 'running' | 'completed' | 'failed'
  created_at: string
  progress: number
  queue_position?: number
  error?: { code: string; message: string }
}

export class QuantumClient {
  async compute<T = any>(useCase: string, params: QuantumParams): Promise<QuantumResult<T>> {
    const response = await api.post<QuantumResult<T>>(`/api/${useCase}/compute`, {
      params,
      wait: true,
      timeout_ms: 30000,
    })
    return response.data
  }

  async submitJob(useCase: string, params: QuantumParams): Promise<{ job_id: string }> {
    const response = await api.post<{ job_id: string }>(`/api/${useCase}/compute`, {
      params,
      wait: false,
    })
    return response.data
  }

  async getJobStatus(jobId: string): Promise<JobStatus> {
    const response = await api.get<JobStatus>(`/api/jobs/${jobId}`)
    return response.data
  }

  async getJobResult<T = any>(jobId: string): Promise<QuantumResult<T>> {
    const response = await api.get<QuantumResult<T>>(`/api/jobs/${jobId}/result`)
    return response.data
  }

  async pollJob<T = any>(
    jobId: string,
    onProgress?: (status: JobStatus) => void,
    maxAttempts = 120
  ): Promise<QuantumResult<T>> {
    for (let i = 0; i < maxAttempts; i++) {
      const status = await this.getJobStatus(jobId)

      if (onProgress) {
        onProgress(status)
      }

      if (status.status === 'completed') {
        return await this.getJobResult<T>(jobId)
      } else if (status.status === 'failed') {
        throw new Error(status.error?.message || 'Job failed')
      }

      await new Promise((resolve) => setTimeout(resolve, 1000))
    }
    throw new Error('Job timeout')
  }

  async health() {
    const response = await api.get('/health')
    return response.data
  }

  async info() {
    const response = await api.get('/api/info')
    return response.data
  }
}

export const quantumClient = new QuantumClient()
