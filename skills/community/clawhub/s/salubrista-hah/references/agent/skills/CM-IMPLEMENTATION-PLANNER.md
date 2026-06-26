---
_manifest:
  urn: urn:salud:skill:salubrista-hah-implementation-planner:1.0.0
  type: lazy_load_endofunctor
---

# CM-IMPLEMENTATION-PLANNER

## Proposito
Traducir disenos o mejoras del sistema de hospitalizacion integrado en planes de implementacion reales. Atiende pilotaje, escalamiento, protocolos, coordinacion interservicios, gestion del cambio y monitoreo de la continuidad hospital-domicilio.

## Input/Output
- **Input:** propuesta: string, contexto: object
- **Output:** ImplementationPlan { escala: string, objetivo_operativo, supuestos: string[], fases: string[], responsables: string[], riesgos: string[], indicadores: string[], continuidad_asegurada: string }

## Procedimiento
1. Resolver `kb_route` hacia gestion-redes general, unidades u herramientas y recuperar el contenido con `knowledge_retrieval`.
2. SI la propuesta involucra HD o transicion hospital-domicilio -> sumar el URN HaH pertinente.
3. DEFINIR el objetivo operativo del cambio.
4. EVALUAR factibilidad:
   - capacidad instalada
   - dotacion y roles
   - madurez del equipo
   - dependencias interservicios
   - restricciones normativas o institucionales
   - soporte territorial
5. ESTRUCTURAR fases:
   - preparacion
   - piloto
   - escalamiento
   - estabilizacion
6. DEFINIR responsables y nodos de coordinacion:
   - hospital
   - HD
   - APS
   - rehabilitacion / paliativos / red de apoyo
7. GESTION DEL CAMBIO:
   - comunicacion
   - capacitacion
   - soporte en terreno
   - feedback y ajuste
8. IDENTIFICAR riesgos:
   - sobrecarga de camas o del equipo HD
   - fallas de transicion
   - rescate insuficiente
   - desalineacion hospital-red
   - resistencia organizacional
9. DEFINIR monitoreo:
   - indicadores de proceso, continuidad, seguridad y resultado
   - hitos de revision
   - gatillos de correccion o rollback
10. OUTPUT: objetivo operativo, supuestos, fases, responsables, riesgos, indicadores y criterio de continuidad asegurada.

## Signature Output
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| escala | string | unidad / establecimiento / red / territorio / nacional / multi / na |
| objetivo_operativo | string | Resultado operativo buscado |
| supuestos | string[] | Condiciones necesarias |
| fases | string[] | Secuencia de implementacion |
| responsables | string[] | Roles o actores responsables |
| riesgos | string[] | Riesgos principales y mitigaciones |
| indicadores | string[] | KPIs o hitos de seguimiento |
| continuidad_asegurada | string | Como se protege la continuidad hospital-domicilio |
