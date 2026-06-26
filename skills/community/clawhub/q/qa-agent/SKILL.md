---
name: qa-agent
description: 'Un agente para realizar tareas de control de calidad (QA), incluyendo análisis de código, ejecución de pruebas y reporte de problemas.'
metadata:
  {
    "openclaw": { "emoji": "🧪", "requires": { "linting_tools": true, "testing_frameworks": true } },
  }
---

# Skill: QA Agent (Agente de Control de Calidad)

Esta skill permite a Omen actuar como un agente de QA, ayudando a asegurar la calidad del código y las funcionalidades.

## Capacidades:
- **Análisis Estático de Código (Linting)**: Identificar problemas de estilo, errores potenciales y malas prácticas en el código fuente.
- **Ejecución de Pruebas Unitarias/Integración**: Lanzar y monitorear frameworks de testing para verificar funcionalidades.
- **Generación de Reportes**: Crear resúmenes de los resultados del QA, incluyendo errores detectados y sugerencias.

## Requisitos:
Para un funcionamiento óptimo, se necesitan herramientas o librerías de línea de comandos para:
- **Linters**: `ruff` para Python (venv), `eslint` para JavaScript (sistema).
- **Frameworks de Testing**: `pytest` para Python (venv), `jest` para JavaScript (sistema).

## Consideraciones:
- Se priorizarán soluciones locales y de código abierto que sean fáciles de integrar y ejecutar en un entorno Linux.
- La skill será flexible para soportar diferentes lenguajes de programación y frameworks.

---

## Herramientas Implementadas

Todos los scripts residen en `scripts/` relativo a esta skill. Acepta una ruta objetivo opcional como primer argumento; si se omite, se usa el directorio actual (o todos los tests en el caso de Jest).

---

### 1. Ruff — Python Linter

**Binario**: `venv/bin/ruff` (incluido en el venv de la skill)

**Script**: `scripts/run_ruff.sh`

**Invocación**:
```bash
bash scripts/run_ruff.sh [path] [extra ruff args...]
```

**Ejemplos**:
```bash
# Lint del directorio actual
bash scripts/run_ruff.sh

# Lint de un archivo o carpeta específica
bash scripts/run_ruff.sh src/

# Con flags adicionales de ruff
bash scripts/run_ruff.sh src/ --fix
```

**Salida**: Lista de infracciones con archivo, línea, código de regla y descripción. Código de salida 0 si no hay errores.

---

### 2. pytest — Python Testing Framework

**Binario**: `venv/bin/pytest` (incluido en el venv de la skill)

**Script**: `scripts/run_pytest.sh`

**Invocación**:
```bash
bash scripts/run_pytest.sh [path] [extra pytest args...]
```

**Ejemplos**:
```bash
# Ejecutar todos los tests del directorio actual
bash scripts/run_pytest.sh

# Ejecutar tests de una carpeta o archivo específico
bash scripts/run_pytest.sh tests/

# Con flags adicionales
bash scripts/run_pytest.sh tests/ -k "test_login" --tb=short
```

**Salida**: Reporte de tests con PASSED/FAILED/ERROR por test. Código de salida 0 si todos pasan.

---

### 3. ESLint — JavaScript Linter

**Binario**: `eslint` (instalado en el sistema, `/usr/bin/eslint`)

**Script**: `scripts/run_eslint.sh`

**Invocación**:
```bash
bash scripts/run_eslint.sh [path] [extra eslint args...]
```

**Ejemplos**:
```bash
# Lint del directorio actual
bash scripts/run_eslint.sh

# Lint de un archivo o carpeta específica
bash scripts/run_eslint.sh src/

# Con flags adicionales
bash scripts/run_eslint.sh src/ --fix --ext .js,.ts
```

**Salida**: Lista de advertencias/errores con archivo, línea, regla y descripción. Código de salida 0 si no hay errores.

---

### 4. Jest — JavaScript Testing Framework

**Binario**: `jest` (instalado en el sistema, `/usr/bin/jest`)

**Script**: `scripts/run_jest.sh`

**Invocación**:
```bash
bash scripts/run_jest.sh [path/pattern] [extra jest args...]
```

**Ejemplos**:
```bash
# Ejecutar todos los tests
bash scripts/run_jest.sh

# Ejecutar tests que coincidan con un patrón de ruta
bash scripts/run_jest.sh src/components/

# Con flags adicionales
bash scripts/run_jest.sh src/ --coverage --watchAll=false
```

**Salida**: Reporte de suites y tests con PASS/FAIL. Código de salida 0 si todos los tests pasan.
