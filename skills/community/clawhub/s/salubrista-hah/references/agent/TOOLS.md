---
_manifest:
  urn: "urn:salud:agent-bootstrap:salubrista-hah-tools:1.0.0"
  type: "bootstrap_tools"
---

## kb_route

- **Firma:** topic: string -> urn: string
- **Cuando usar:** Primer paso semantico para resolver el corpus rector antes del analisis. Usar en problemas de hospitalizacion integrada, gestion de camas, continuidad del cuidado, hospitalizacion domiciliaria, implementacion, evaluacion y aterrizajes psiquiatricos vinculados a HD.
- **Cuando NO usar:** Si el mismo tema ya fue resuelto y recuperado en el turno actual.
- **Routing map hospitalizacion integrada:**

| Topic | URN |
|-------|-----|
| Gobernanza hospitalaria, procesos transversales, calidad, RRHH, gestion del cambio, operacion de establecimientos | `urn:salud:kb:gestion-redes-general` |
| Unidades hospitalarias, hospitalizacion, articulacion de modalidades, HaH, continuidad funcional entre dispositivos | `urn:salud:kb:gestion-redes-unidades` |
| Red de urgencias, ingresos hospitalarios, SAMU, descompensaciones, rescate y transiciones tiempo-sensibles | `urn:salud:kb:gestion-redes-urgencias` |
| Crisis de salud mental, continuidad psiquiatrica o articulacion con COSAM/rehabilitacion en trayectorias hospital-domicilio | `urn:salud:kb:gestion-redes-salud-mental` |
| KPIs, BPMN, simulacion, plantillas operativas, madurez digital y soporte instrumental | `urn:salud:kb:gestion-redes-herramientas` |
| Indice general, glosario, normativa y contextualizacion local | `urn:salud:kb:gestion-redes-indice` |

- **Nota:** Este bloque es el baseline del componente intrahospitalario. Cobertura limitada a los URNs listados.


- **Routing map HD / hospital-domicilio:**

| Topic | URN |
|-------|-----|
| Reglamento base HD: autorizacion, direccion tecnica, ingreso/egreso, articulado central | `urn:salud:kb:hodom-reglamento-ds1-2022` |
| Decreto aprobatorio y fundamento juridico de la norma tecnica HD 2024 | `urn:salud:kb:hodom-decreto-exento-31-2024` |
| Norma tecnica HD 2024: personal, infraestructura, equipamiento, registros, protocolos, PAC, seguridad | `urn:salud:kb:hodom-norma-tecnica-2024` |
| Direccion Tecnica HD: art. 7-10, RRHH, manuales, fiscalizacion, sucesion, operacion local del DT | `urn:salud:kb:hodom-direccion-tecnica` |
| Modelo HaH de alta complejidad: benchmarks, operaciones, RPM/IoT, pathways, backfill y continuidad | `urn:salud:kb:hodom-manual-alta-complejidad` |
| Situacion de Chile 2024-2026: DEIS, financiamiento, GRD/MCC, brechas de red | `urn:salud:kb:hodom-situacion-chile-2026` |

- **Routing map salud publica aplicada:**

| Topic | URN |
|-------|-----|
| Epidemiologia aplicada, riesgos, brotes, razonamiento sanitario integrado y pensamiento sistemico | `urn:salud:kb:firs-framework-integrado-razonamiento-salud` |

## knowledge_retrieval

- **Firma:** urn: string -> content: string
- **Cuando usar:** Recuperar el contenido del corpus inmediatamente despues de `kb_route`. En problemas de hospitalizacion integrada, recuperar primero gestion-redes y sumar corpus HD cuando la trayectoria hospital-domicilio o la normativa sean relevantes.
- **Cuando NO usar:** Si el contenido ya esta en contexto de turno actual.
- **Nota OpenClaw:** Los corpus estan montados en `/home/node/knowledge/salud/`. Para recuperar, leer el archivo correspondiente al URN usando las herramientas de filesystem.

### Mapeo URN -> Ruta de archivo

| URN | Ruta |
|-----|------|
| `urn:salud:kb:gestion-redes-general` | `/home/node/knowledge/salud/salubrista/gestion-redes/01-gestion-redes-general.md` |
| `urn:salud:kb:gestion-redes-unidades` | `/home/node/knowledge/salud/salubrista/gestion-redes/02-unidades-asistenciales.md` |
| `urn:salud:kb:gestion-redes-urgencias` | `/home/node/knowledge/salud/salubrista/gestion-redes/03-urgencias.md` |
| `urn:salud:kb:gestion-redes-salud-mental` | `/home/node/knowledge/salud/salubrista/gestion-redes/04-salud-mental.md` |
| `urn:salud:kb:gestion-redes-herramientas` | `/home/node/knowledge/salud/salubrista/gestion-redes/05-herramientas-anexos.md` |
| `urn:salud:kb:gestion-redes-indice` | `/home/node/knowledge/salud/salubrista/gestion-redes/00-indice.md` |
| `urn:salud:kb:hodom-reglamento-ds1-2022` | `/home/node/knowledge/salud/hodom/normativa/01-reglamento-hodom-ds1-2022.md` |
| `urn:salud:kb:hodom-decreto-exento-31-2024` | `/home/node/knowledge/salud/hodom/normativa/02-decreto-exento-31-2024-aprueba-norma-tecnica.md` |
| `urn:salud:kb:hodom-norma-tecnica-2024` | `/home/node/knowledge/salud/hodom/normativa/03-norma-tecnica-hodom-2024.md` |
| `urn:salud:kb:hodom-direccion-tecnica` | `/home/node/knowledge/salud/hodom/director/01-manual-direccion-tecnica.md` |
| `urn:salud:kb:hodom-manual-alta-complejidad` | `/home/node/knowledge/salud/hodom/director/02-manual-alta-complejidad.md` |
| `urn:salud:kb:hodom-situacion-chile-2026` | `/home/node/knowledge/salud/hodom/director/03-situacion-chile-2026.md` |
| `urn:salud:kb:firs-framework-integrado-razonamiento-salud` | `/home/node/knowledge/salud/salubrista/framework-razonamiento-clinico-epidemiologico-gestion/firs-framework-integrado.md` |

## web_search

- **Firma:** query: string -> SearchResult[]
- **Cuando usar:** Complementar corpus con evidencia actualizada, normativa MINSAL vigente, datos epidemiologicos actuales, benchmarks de hospitalizacion integrada o estudios recientes de HD y continuidad del cuidado. Citar fuente web en output.
- **Cuando NO usar:** Si el corpus ya cubre adecuadamente el tema. No usar web para reemplazar el corpus; solo para extenderlo o verificar vigencia.
- **Notas:** Devuelve resultados web genericos. Preferir fuentes autoritativas: MINSAL, OPS, OMS, IHI, NICE, AHRQ, Cochrane, Johns Hopkins, CMS y journals indexados. Especialmente pertinente cuando el problema requiera detalle intrahospitalario no disponible en gestion-redes o vigencia normativa/benchmark actual.


# Federacion kora — derivacion inter-agente

Este agente es miembro de la federacion kora. Puede derivar casos a otros agentes cuando un problema esta fuera de su dominio.

### Directorio de la federacion

Lee `/home/node/shared/federation/directorio-agentes.md` para saber que agentes existen, que hacen y como contactarlos. Este archivo esta siempre actualizado.

### Como derivar a otro agente

Usa `web_fetch` para enviar un hook al gateway del agente destino:

```
POST http://{gateway_host}:{port}/hooks/agent
Authorization: Bearer 766c9b38b53702cd0c994d7361c25e0bc5e6a3c671d1ac76
Content-Type: application/json

{
  "message": "[Derivacion de {mi-nombre}] {contexto del caso y motivo}",
  "name": "derivacion-{mi-nombre}"
}
```

Agentes disponibles (referencia rapida):

| Agente | Gateway | Hook URL |
|---|---|---|
| korax | kora-personal | `http://kora-personal:18789/hooks/agent` |
| steipete | kora-steipete | `http://kora-steipete:18810/hooks/agent` |
| salubrista-hah | kora-salubrista | `http://kora-salubrista:18830/hooks/agent` |

### Cuando derivar

- Solo cuando el caso esta **fuera de tu dominio** (ver Reglas Duras en AGENTS.md)
- Incluir contexto suficiente para que el destino no necesite preguntar de vuelta
- Informar al usuario que estas derivando y a quien

### Espacio compartido

- Tu directorio propio (lectura/escritura): `/home/node/shared/{mi-id}/`
- Directorio de la federacion (solo lectura): `/home/node/shared/federation/`
- Puedes dejar documentos en tu directorio para que otros agentes los lean si el operador configura visibilidad cruzada
