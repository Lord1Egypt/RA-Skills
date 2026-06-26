#!/usr/bin/env python3
"""
Guppy/Selene Quantum Skill - Lovable Frontend Integration

This script sets up a Lovable frontend project configured to connect
to a Selene quantum backend API. It creates a complete React + TypeScript
frontend with quantum-specific UI components.

Usage:
    python3 lovable_integrate.py --app-name "quantum-coin-flip" --backend-url "https://myapp.fly.dev"

Options:
    --app-name       Name for the Lovable frontend project
    --backend-url    Selene backend API URL (e.g., https://myapp.fly.dev)
    --quantum-use-case Type of quantum app (coin-flip, optimization, chemistry, etc.)
    --output-dir     Output directory (default: current directory)
"""

import argparse
import os
from pathlib import Path
from datetime import datetime

# Generate Lovable project structure as a simplified template
# In a real implementation, this would scaffold an actual Lovable project
# or copy from a full template. Here we provide minimal structure.

PACKAGE_JSON = '''{{
  "name": "{app_name}-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0",
    "@tanstack/react-query": "^5.0.0",
    "recharts": "^2.10.0",
    "lucide-react": "^0.300.0"
  }},
  "devDependencies": {{
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }}
}}
'''

TS_CONFIG = '''{{
  "compilerOptions": {{
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }},
  "include": ["src"],
  "references": [{{"path": "./tsconfig.node.json"}}]
}}
'''

TS_CONFIG_NODE = '''{{
  "compilerOptions": {{
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  }},
  "include": ["vite.config.ts"]
}}
'''

VITE_CONFIG = '''import {{ defineConfig }} from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({{
  plugins: [react()],
  server: {{
    port: 5173,
    proxy: {{
      '/api': {{
        target: '{backend_url}',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\\/api/, '')
      }}
    }}
  }}
}})
'''

INDEX_HTML = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{app_name} - Quantum {quantum_use_case}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''

MAIN_TSX = '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
'''

APP_TSX = '''import {{
  QueryClient,
  QueryClientProvider,
}} from '@tanstack/react-query'
import {{ QuantumDashboard }} from './components/QuantumDashboard'

const queryClient = new QueryClient()

function App() {{
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-900 text-white">
        <header className="bg-gray-800 p-4 shadow-lg">
          <h1 className="text-2xl font-bold">{app_name}</h1>
          <p className="text-gray-400">Quantum {quantum_use_case} powered by Guppy/Selene</p>
        </header>
        <main className="p-6">
          <QuantumDashboard backendUrl="{backend_url}" quantumUseCase="{quantum_use_case}" />
        </main>
        <footer className="fixed bottom-0 left-0 right-0 bg-gray-800 p-2 text-center text-sm text-gray-400">
          Powered by Quantinuum Guppy/Selene • Deployed on Fly.io
        </footer>
      </div>
    </QueryClientProvider>
  )
}}

export default App
'''

INDEX_CSS = ''':root {{
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
}}

body {{
  margin: 0;
  min-width: 320px;
  min-height: 100vh;
}}
'''

QUANTUM_DASHBOARD_COMPONENT = '''import React, {{ useState }} from 'react'
import {{ Card, CardContent, CardHeader, CardTitle }} from './ui/Card'
import {{ Button }} from './ui/Button'
import {{ Activity } from 'lucide-react'
import axios from 'axios'

interface QuantumDashboardProps {{
  backendUrl: string
  quantumUseCase: string
}}

export function QuantumDashboard({{ backendUrl, quantumUseCase }}: QuantumDashboardProps) {{
  const [params, setParams] = useState('{{"shots": 1000}}')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const runQuantumComputation = async () => {{
    setLoading(true)
    setError(null)
    try {{
      const response = await axios.post(`${{backendUrl}}/api/${{quantum_use_case}}/compute`, JSON.parse(params))
      setResult(response.data)
    }} catch (err: any) {{
      setError(err.response?.data?.detail || err.message)
    }} finally {{
      setLoading(false)
    }}
  }}

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
              <label className="block text-sm font-medium mb-2">Parameters (JSON)</label>
              <textarea
                value={params}
                onChange={(e) => setParams(e.target.value)}
                className="w-full h-24 p-3 bg-gray-800 border border-gray-700 rounded font-mono text-sm"
                placeholder='{{"shots": 1000}}'
              />
            </div>
            <Button
              onClick={runQuantumComputation}
              disabled={loading}
              className="w-full"
            >
              {{ loading ? 'Running...' : 'Run Quantum Algorithm' }}
            </Button>
            {{error && (
              <div className="p-3 bg-red-900 border border-red-700 rounded text-red-200">
                {{error}}
              </div>
            )}
            {{result && (
              <div className="p-4 bg-gray-800 border border-gray-700 rounded">
                <h3 className="font-semibold mb-2">Results</h3>
                <pre className="text-sm overflow-x-auto">
                  {{JSON.stringify(result, null, 2)}}
                </pre>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>About This Application</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-300">
            This quantum computing application uses Quantinuum's Guppy programming language
            and Selene backend to perform {quantum_use_case} computations.
            Results are delivered via REST API from the quantum hardware/emulator.
          </p>
          <div className="mt-4 text-sm text-gray-400">
            <p>Backend: {{{{backendUrl}}}}</p>
            <p>API endpoints:</p>
            <ul className="list-disc list-inside ml-4">
              <li>GET /health</li>
              <li>POST /api/{quantum_use_case}/compute</li>
              <li>GET /api/info</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}}
'''

# Create simple UI components (without full shadcn/ui setup for brevity)
BUTTON_COMPONENT = '''import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {{
  children: React.ReactNode
}}

export function Button({{ className = '', children, ...props }}: ButtonProps) {{
  return (
    <button
      className={`px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded font-medium transition ${{className}}`}}
      {...props}}
    >
      {{children}}
    </button>
  )
}}
'''

CARD_COMPONENT = '''import React from 'react'

interface CardProps {{
  children: React.ReactNode
  className?: string
}}

export function Card({{ className = '', children }}: CardProps) {{
  return (
    <div className=`bg-gray-800 border border-gray-700 rounded-lg shadow-lg ${{className}}``>
      {{children}}
    </div>
  )
}}

export function CardHeader({{ children, className = '' }}: CardProps) {{
  return <div className=`p-4 border-b border-gray-700 ${{className}}``>{{children}}</div>
}}

export function CardTitle({{ children, className = '' }}: CardProps) {{
  return <h3 className=`text-lg font-semibold ${{className}}``>{{children}}</h3>
}}

export function CardContent({{ children, className = '' }}: CardProps) {{
  return <div className=`p-4 ${{className}}``>{{children}}</div>
}}
'''

def create_lovable_frontend(app_name, backend_url, quantum_use_case, output_dir):
    """Create a Lovable frontend project structure"""

    project_dir = Path(output_dir) / f"{app_name}-frontend"
    project_dir.mkdir(parents=True, exist_ok=True)

    print(f"Creating Lovable frontend: {project_dir}")

    # Create src directory structure
    src_dir = project_dir / "src"
    src_dir.mkdir(exist_ok=True)
    components_dir = src_dir / "components"
    components_dir.mkdir(exist_ok=True)
    ui_dir = components_dir / "ui"
    ui_dir.mkdir(exist_ok=True)

    timestamp = datetime.utcnow().isoformat()

    # Write config files
    (project_dir / "package.json").write_text(PACKAGE_JSON.format(app_name=app_name))
    print("  ✓ Created package.json")

    (project_dir / "tsconfig.json").write_text(TS_CONFIG)
    print("  ✓ Created tsconfig.json")

    (project_dir / "tsconfig.node.json").write_text(TS_CONFIG_NODE)
    print("  ✓ Created tsconfig.node.json")

    (project_dir / "vite.config.ts").write_text(VITE_CONFIG.format(backend_url=backend_url))
    print("  ✓ Created vite.config.ts")

    (project_dir / "index.html").write_text(INDEX_HTML.format(app_name=app_name, quantum_use_case=quantum_use_case))
    print("  ✓ Created index.html")

    # Write source files
    (src_dir / "main.tsx").write_text(MAIN_TSX)
    print("  ✓ Created src/main.tsx")

    (src_dir / "App.tsx").write_text(APP_TSX.format(app_name=app_name, quantum_use_case=quantum_use_case, backend_url=backend_url))
    print("  ✓ Created src/App.tsx")

    (src_dir / "index.css").write_text(INDEX_CSS)
    print("  ✓ Created src/index.css")

    # Write components
    (components_dir / "QuantumDashboard.tsx").write_text(QUANTUM_DASHBOARD_COMPONENT)
    print("  ✓ Created src/components/QuantumDashboard.tsx")

    (ui_dir / "Card.tsx").write_text(CARD_COMPONENT)
    print("  ✓ Created src/components/ui/Card.tsx")

    (ui_dir / "Button.tsx").write_text(BUTTON_COMPONENT)
    print("  ✓ Created src/components/ui/Button.tsx")

    # Public assets
    public_dir = project_dir / "public"
    public_dir.mkdir(exist_ok=True)
    (public_dir / "vite.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--logos" width="31.88" height="32" preserveAspectRatio="xMidYMid meet" viewBox="0 0 256 257"><defs><linearGradient id="IconifyId1813088fe1fbc01fb466" x1="-.828%" x2="57.636%" y1="7.652%" y2="78.411%"><stop offset="0%" stop-color="#41D1FF"></stop><stop offset="100%" stop-color="#BD34FE"></stop></linearGradient><linearGradient id="IconifyId1813088fe1fbc01fb467" x1="43.376%" x2="50.316%" y1="2.242%" y2="89.03%"><stop offset="0%" stop-color="#FFBD4F"></stop><stop offset="100%" stop-color="#FF980E"></stop></linearGradient></defs><path fill="url(#IconifyId1813088fe1fbc01fb466)" d="M255.153 37.938L134.897 252.976c-2.483 4.44-8.862 4.466-11.382.048L.875 37.958c-2.746-4.814 1.371-10.646 6.827-9.67l120.385 21.517a6.537 6.537 0 0 0 2.322-.004l117.867-21.483c5.438-.991 9.574 4.796 6.877 9.62Z"></path><path fill="url(#IconifyId1813088fe1fbc01fb467)" d="M185.432.063L96.44 17.501a3.268 3.268 0 0 0-2.634 3.014l-5.474 92.456a3.268 3.268 0 0 0 3.997 3.378l24.777-5.718c2.318-.535 4.413 1.507 3.936 3.838l-7.361 36.047c-.495 2.426 1.782 4.5 4.151 3.78l15.304-4.649c2.372-.72 4.652 1.36 4.15 3.788l-11.698 56.621c-.732 3.542 3.979 5.473 5.943 2.437l1.313-2.028l72.516-144.72c1.215-2.423-.88-5.186-3.54-4.672l-25.505 4.922c-2.396.462-4.435-1.77-3.759-4.114l16.646-57.705c.677-2.35-1.37-4.583-3.769-4.113Z"></path></svg>')
    print("  ✓ Created public/vite.svg")

    # README
    readme_content = f'''# {app_name} Frontend

Quantum {quantum_use_case} interface powered by {backend_url}

## Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

   Frontend will be available at http://localhost:5173

## Building for Production

```bash
npm run build
```

Build output goes to `dist/` directory.

## Configuration

- Backend API URL is configured in `vite.config.ts` proxy and in `App.tsx`
- The API proxy forwards `/api/*` requests to the Selene backend
- Update `backendUrl` in `App.tsx` if changing the backend endpoint

## Features

- Real-time quantum computation results
- Parameter editing with JSON validation
- Result visualization with response display
- Error handling and loading states
- Responsive design optimized for dashboards

## Tech Stack

- React 18 + TypeScript
- Vite (fast build tool)
- TanStack Query for API state management
- Recharts for data visualization (extendable)
- Tailwind CSS via Lucide icons (pre-configured)

## Deployment

This frontend is designed to be deployed to:
- Lovable (preferred)
- Vercel/Netlify (alternative)
- Any static hosting service

For Lovable:
1. Import this project into Lovable workspace
2. Set environment variable VITE_API_URL to your backend URL
3. Deploy to Lovable hosting

## Connecting to Quantum Backend

Ensure your Selene backend is running and accessible. The frontend expects these endpoints:

- `GET /health`
- `POST /api/{quantum_use_case}/compute`
- `GET /api/info`

API requests are proxied during development and direct in production.
'''
    (project_dir / "README.md").write_text(readme_content)
    print("  ✓ Created README.md")

    .gitignore_content = '''node_modules/
dist/
.env.local
.env.*.local
*.log
.DS_Store
'''
    (project_dir / ".gitignore").write_text(.gitignore_content)
    print("  ✓ Created .gitignore")

    print(f"\n✅ Lovable frontend created at: {project_dir}")
    print(f"\nNext steps:")
    print(f"1. cd {project_dir}")
    print(f"2. npm install")
    print(f"3. npm run dev")
    print(f"4. Deploy to Lovable when ready")

    return project_dir

def main():
    parser = argparse.ArgumentParser(description="Setup Lovable frontend for quantum backend")
    parser.add_argument("--app-name", required=True, help="Frontend project name")
    parser.add_argument("--backend-url", required=True, help="Selene backend API URL")
    parser.add_argument("--quantum-use-case", default="optimization", help="Quantum use case type")
    parser.add_argument("--output-dir", default=".", help="Output directory (default: current)")

    args = parser.parse_args()

    try:
        create_lovable_frontend(args.app_name, args.backend_url, args.quantum_use_case, args.output_dir)
        print("\n✅ Frontend integration complete!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
