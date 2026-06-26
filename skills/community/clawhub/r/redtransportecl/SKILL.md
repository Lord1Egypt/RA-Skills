  ---                                                                                                                                                                          
  name: redtransportecl                                                                                                                                                          
  description: Usa la CLI `red-transporte` para consultar paraderos, recorridos, predicciones en tiempo real, GTFS local y utilidades geoespaciales de RED Chile.                
  metadata:                                                                                                                                                                      
    {                                                                                                                                                                            
      "openclaw":                                                                                                                                                                
        {                                                                                                                                                                        
          "requires": { "bins": ["red-transporte"] }                                                                                                                             
        }                                                                                                                                                                        
    }                                                                                                                                                                            
  ---  

# RedTransporteAPI CLI — SKILL

Esta skill esta enfocada exclusivamente en el uso de la CLI `red-transporte`.

## Requisitos

- Python 3.9 o superior
- Instalar dependencias del proyecto
- Descargar GTFS local antes de consultas que usan datos estaticos

```bash
pip install ".[all]"
red-transporte gtfs update
```

## Sintaxis general

```bash
red-transporte [--json] [--verbose|-v] <comando> [opciones]
```

## Flags globales

- `--json`: imprime salida JSON cruda.
- `--verbose` o `-v`: activa logging en nivel debug.

Ejemplo:

```bash
red-transporte --json stop PA433
red-transporte -v predict PA433
```

## Comandos CLI detallados

### 1) `gtfs`

Gestiona datos GTFS locales.

Subcomandos:

- `gtfs update [--force]`
	- Descarga/actualiza el GTFS vigente desde DTPM.
	- `--force`: fuerza re-descarga aunque exista version local.
- `gtfs status`
	- Muestra estado de los datos GTFS locales.

Ejemplos:

```bash
red-transporte gtfs update
red-transporte gtfs update --force
red-transporte --json gtfs status
```

### 2) `stop`

Obtiene informacion completa de un paradero.

Uso:

```bash
red-transporte stop <code>
```

Argumentos:

- `<code>`: codigo del paradero (ejemplo: `PA433`).

Ejemplos:

```bash
red-transporte stop PA433
red-transporte --json stop PA433
```

### 3) `search`

Busca paraderos por texto.

Uso:

```bash
red-transporte search <query> [--limit N]
```

Argumentos y opciones:

- `<query>`: texto de busqueda.
- `--limit`: maximo de resultados (default: `10`).

Ejemplos:

```bash
red-transporte search "providencia"
red-transporte search "macul" --limit 5
```

### 4) `nearby`

Lista paraderos cercanos a una coordenada.

Uso:

```bash
red-transporte nearby <lat> <lon> [--radius KM]
```

Argumentos y opciones:

- `<lat>`: latitud (float).
- `<lon>`: longitud (float).
- `--radius`: radio en kilometros (default: `0.5`).

Ejemplos:

```bash
red-transporte nearby -33.4372 -70.6506
red-transporte nearby -33.4372 -70.6506 --radius 1.0
```

### 5) `station`

Devuelve la estacion de metro/tren mas cercana.

Uso:

```bash
red-transporte station <lat> <lon>
```

Argumentos:

- `<lat>`: latitud (float).
- `<lon>`: longitud (float).

Ejemplo:

```bash
red-transporte station -33.45 -70.65
```

### 6) `route`

Muestra informacion de un recorrido.

Uso:

```bash
red-transporte route <route_id>
```

Argumentos:

- `<route_id>`: ID o nombre corto del recorrido (ejemplo: `506`, `D12`).

Ejemplos:

```bash
red-transporte route 506
red-transporte route D12
```

### 7) `routes`

Lista recorridos, opcionalmente filtrados por modo.

Uso:

```bash
red-transporte routes [--mode bus|metro|rail|tram]
```

Opciones:

- `--mode`: filtra por modo de transporte.

Ejemplos:

```bash
red-transporte routes
red-transporte routes --mode metro
red-transporte routes --mode bus
```

### 8) `predict`

Consulta predicciones en tiempo real para un paradero.

Uso:

```bash
red-transporte predict <code>
```

Argumentos:

- `<code>`: codigo del paradero.

Ejemplos:

```bash
red-transporte predict PA433
red-transporte --json predict PA433
```

### 9) `stats`

Entrega estadisticas globales del sistema.

Uso:

```bash
red-transporte stats
```

Ejemplo:

```bash
red-transporte --json stats
```

### 10) `suggest`

Sugiere recorridos entre dos puntos geograficos (basico, sin tiempos).

Uso:

```bash
red-transporte suggest <from_lat> <from_lon> <to_lat> <to_lon> [--radius KM]
```

Argumentos y opciones:

- `<from_lat>`: latitud origen.
- `<from_lon>`: longitud origen.
- `<to_lat>`: latitud destino.
- `<to_lon>`: longitud destino.
- `--radius`: radio de busqueda en kilometros (default: `0.5`).

Ejemplos:

```bash
red-transporte suggest -33.4372 -70.6506 -33.4189 -70.6024
red-transporte suggest -33.4372 -70.6506 -33.4189 -70.6024 --radius 0.8
```

### 11) `server`

Inicia el servidor HTTP de la API.

Uso:

```bash
red-transporte server
```

Salida esperada:

- API disponible localmente (por defecto) en `http://localhost:8000`.
- Documentacion Swagger en `http://localhost:8000/docs`.

## Flujo recomendado de uso CLI

1. Descargar GTFS: `red-transporte gtfs update`
2. Verificar estado: `red-transporte gtfs status`
3. Consultar paraderos/recorridos: `stop`, `search`, `route`, `routes`
4. Consultar tiempo real: `predict`
5. Consultas geoespaciales: `nearby`, `station`, `suggest`

## Planificador de rutas RAPTOR (API)

El endpoint `/routing/plan` usa el algoritmo RAPTOR para calcular rutas optimas de transporte publico entre dos coordenadas. Este endpoint solo esta disponible via la API HTTP (no via CLI).

### Endpoint

```
GET /routing/plan
```

### Parametros

| Parametro | Tipo | Default | Descripcion |
|-----------|------|---------|-------------|
| `from_lat` | float | (requerido) | Latitud del origen |
| `from_lon` | float | (requerido) | Longitud del origen |
| `to_lat` | float | (requerido) | Latitud del destino |
| `to_lon` | float | (requerido) | Longitud del destino |
| `departure_time` | str | `08:00:00` | Hora de salida en formato HH:MM:SS |
| `day` | str | `L` | Dia: `L`=laboral, `S`=sabado, `D`=domingo |
| `max_results` | int | `3` | Maximo de alternativas (1-5) |
| `max_transfers` | int | `2` | Maximo de transbordos (0-3) |
| `fare_type` | str | `normal` | Tipo tarifa: `normal`, `estudiante`, `adulto_mayor` |

### Ejemplo de uso

```bash
# Estacion Central a Puente Alto, laboral 09:00
curl "http://localhost:8000/routing/plan?from_lat=-33.4525&from_lon=-70.6783&to_lat=-33.586&to_lon=-70.576&departure_time=09:00:00&day=L"

# Plaza Italia a La Moneda, tarifa estudiante
curl "http://localhost:8000/routing/plan?from_lat=-33.4372&from_lon=-70.634&to_lat=-33.4422&to_lon=-70.6537&fare_type=estudiante"

# Sin transbordos (solo rutas directas)
curl "http://localhost:8000/routing/plan?from_lat=-33.4372&from_lon=-70.634&to_lat=-33.5195&to_lon=-70.598&max_transfers=0"
```

### Respuesta

La respuesta contiene una lista de planes de viaje (`plans`), cada uno con:

- `total_time_secs` / `total_time_human`: tiempo total del viaje
- `departure_time` / `arrival_time`: hora de salida y llegada
- `walk_time_secs`, `ride_time_secs`, `wait_time_secs`: desglose de tiempos
- `transfers`: numero de transbordos
- `total_walk_m`: metros caminados en total
- `fare`: tarifa calculada con desglose
- `legs`: lista de tramos del viaje (caminar, bus, metro, etc.)
- `summary`: resumen legible del viaje

Cada leg tiene:
- `mode`: `walk`, `bus`, `metro`, `rail`
- `route_name`: nombre del recorrido (ej: `L1`, `506`, `210`)
- `board_stop_name` / `alight_stop_name`: paradero de subida y bajada
- `num_stops`: cantidad de paradas
- `duration_secs`: duracion del tramo
- `wait_secs`: tiempo de espera antes de abordar
- `walk_distance_m`: distancia caminada (solo para legs de caminata)

### RAPTOR: como funciona

RAPTOR (Round-Based Public Transit Optimized Router) busca rutas por rondas:
- **Ronda 1**: mejor ruta directa (0 transbordos)
- **Ronda 2**: mejor ruta con 1 transbordo
- **Ronda 3**: mejor ruta con 2 transbordos

Solo devuelve una ronda si es estrictamente mas rapida que la anterior (Pareto-optimo). Ejemplo: si con 2 transbordos llegas en 1h09 pero sin transbordos en 1h20, ambas opciones se muestran.

El tiempo de espera se calcula como: headway/2 (promedio) + 30 segundos de penalizacion por abordaje. Los headways vienen de las frecuencias reales del GTFS por hora y dia.

### Tarifa integrada RED

El calculo de tarifa sigue las reglas oficiales de [red.cl](https://www.red.cl/tarifas-y-recargas/conoce-las-tarifas/).

**Tarifas base adulto normal:**

| Modo | Punta (07-09 / 18-20) | Valle (09-18 / 20-20:44 / fds) | Baja (06-07 / 20:45-23) |
|------|----------------------|-------------------------------|------------------------|
| Bus | $795 | $795 | $795 |
| Metro/Tren | $895 | $815 | $735 |

**Reglas de transbordo:**
- Maximo 2 transbordos en ventana de 120 minutos
- Tarifa integrada = maximo entre bus ($795) y metro (segun periodo)
- Bus → Metro: pagas la diferencia hasta tarifa metro
- Metro → Bus: bus incluido ($0 adicional)
- Bus → Bus: segundo bus incluido ($0 adicional)
- Solo el primer tramo paga completo; los demas estan incluidos

**Tarifas especiales:**

| fare_type | Tarifa |
|-----------|--------|
| `normal` | segun tabla de arriba |
| `estudiante` | $260 plana |
| `adulto_mayor` | $390 plana |

**Desglose en respuesta:**
El campo `fare.breakdown` muestra por cada tramo de transporte:
- `mode`: tipo de vehiculo
- `route`: nombre del recorrido
- `fare_mode`: tarifa teorica del modo
- `paid`: monto pagado en ese tramo ($0 si es transbordo incluido)

## Notas operativas CLI

- Si no existe GTFS local, varios comandos fallaran hasta ejecutar `red-transporte gtfs update`.
- `predict` consulta fuentes en tiempo real y puede variar entre llamadas.
- Para integraciones de scripts, usar siempre `--json`.
- El planificador RAPTOR solo esta disponible via la API HTTP (`/routing/plan`), no via CLI.
