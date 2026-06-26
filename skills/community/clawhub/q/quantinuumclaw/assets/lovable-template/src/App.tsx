import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { QuantumDashboard } from './components/QuantumDashboard'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 0,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-900 text-white">
        <header className="bg-gray-800 p-6 shadow-lg">
          <h1 className="text-3xl font-bold">Quantum Optimizer</h1>
          <p className="text-gray-400 mt-2">
            Portfolio optimization powered by quantum computing
          </p>
        </header>
        <main className="p-6">
          <QuantumDashboard useCase="optimization" />
        </main>
        <footer className="mt-12 py-4 border-t border-gray-800 text-center text-sm text-gray-500">
          Powered by Quantinuum Guppy/Selene • Deployed on Fly.io
        </footer>
      </div>
    </QueryClientProvider>
  )
}

export default App
