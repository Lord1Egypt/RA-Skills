import { useState } from 'react'
import { QuantumParams, QuantumResult, quantumClient } from '../lib/api'
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card'
import { Button } from './ui/Button'
import { Activity, Cpu } from 'lucide-react'

interface QuantumDashboardProps {
  useCase: string
  defaultParams?: QuantumParams
  onResult?: (result: QuantumResult) => void
}

const PARAM_DEFINITIONS: Record<
  string,
  Array<{
    name: keyof QuantumParams
    label: string
    type: 'number' | 'range'
    min?: number
    max?: number
    step?: number
  }>
> = {
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
  ],
}

export function QuantumDashboard({
  useCase,
  defaultParams = { shots: 1000 },
  onResult,
}: QuantumDashboardProps) {
  const [params, setParams] = useState<QuantumParams>(defaultParams)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<QuantumResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const runComputation = async () => {
    setLoading(true)
    setError(null)
    try {
      const computedResult = await quantumClient.compute(useCase, params)
      setResult(computedResult)
      onResult?.(computedResult)
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.error?.message || err.message
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

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
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">
                Parameters:
              </label>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {PARAM_DEFINITIONS[useCase]?.map(
                  ({ name, label, type, min, max, step }) => {
                    const value = params[name] ?? (type === 'range' ? 0.01 : undefined)
                    return (
                      <div key={name} className="space-y-2">
                        <label className="text-sm text-gray-400">{label}</label>
                        {type === 'number' && (
                          <input
                            type="number"
                            min={min}
                            max={max}
                            step={step}
                            value={value}
                            onChange={(e) =>
                              setParams({
                                ...params,
                                [name]: Number(e.target.value),
                              })
                            }
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
                            onChange={(e) =>
                              setParams({
                                ...params,
                                [name]: Number(e.target.value),
                              })
                            }
                            className="w-full"
                          />
                        )}
                      </div>
                    )
                  }
                ) || (
                  <p className="text-gray-400 text-sm">
                    No configurable parameters for this use case.
                  </p>
                )}
              </div>
            </div>
            <Button
              onClick={runComputation}
              disabled={loading}
              className="w-full"
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
              <div className="p-4 bg-red-900 border border-red-700 rounded text-red-200">
                {error}
              </div>
            )}
            {result && <QuantumResult result={result} />}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function QuantumResult({ result }: { result: QuantumResult }) {
  const { result: data, statistics } = result

  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle>Computation Results</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-4 p-4 bg-gray-800 rounded">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400">
                {statistics.execution_time_ms}ms
              </div>
              <div className="text-xs text-gray-400">Execution Time</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">
                {statistics.shots.toLocaleString()}
              </div>
              <div className="text-xs text-gray-400">Shots</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-400">
                {statistics.hardware_used}
              </div>
              <div className="text-xs text-gray-400">Hardware</div>
            </div>
          </div>

          <div>
            <h4 className="font-semibold mb-2">Result:</h4>
            <pre className="p-4 bg-gray-900 border border-gray-700 rounded overflow-x-auto text-sm font-mono">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>

          <div className="text-xs text-gray-500">
            Generated: {new Date(result.timestamp).toLocaleString()}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
