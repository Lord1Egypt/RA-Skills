---
_manifest:
  urn: urn:salud:skill:salubrista-hah-quality-auditor:1.0.0
  type: lazy_load_endofunctor
---

# CM-QUALITY-AUDITOR

## Proposito
Evaluar desempeno, calidad y mejora continua de sistemas de hospitalizacion integrados, incluyendo hospital y HD. Organiza hallazgos, KPIs y acciones de mejora para capacidad, seguridad, continuidad del cuidado y eficiencia del continuo asistencial.

## Input/Output
- **Input:** alcance: string, datos: object
- **Output:** EvaluationReport { escala: string, mode: string, alcance: string, criterios_evaluacion: string[], hallazgos: string[], plan_mejora: string[], kpis_seguimiento: string[], trazabilidad_normativa: string[], resumen_ejecutivo: string }

## Procedimiento
1. DETERMINAR mode segun la intencion del usuario: `evaluation` (desempeno, mejora continua, seguimiento de indicadores) | `audit` (auditoria formal, cumplimiento normativo, fiscalizacion).
2. DEFINIR alcance y escala (per Scale_vocabulary): unidad, establecimiento, red, territorio, nacional, multi o na.
3. Resolver `kb_route` hacia gestion-redes y, si aplica, sumar corpus HaH pertinente. Recuperar baseline con `knowledge_retrieval`.
4. FIJAR criterios de evaluacion segun mode:
   - IF mode = `evaluation`: foco en desempeno, calidad, KPIs, resultados, experiencia usuaria y mejora continua. Criterios: seguridad, oportunidad, eficiencia, continuidad del cuidado, experiencia usuaria y del cuidador, equidad, sostenibilidad.
   - IF mode = `audit`: foco en cumplimiento normativo, fiscalizacion, trazabilidad documental y brechas regulatorias. Criterios: conformidad normativa (DS 1/2022, DE 31/2024, Norma Tecnica HD si aplica), completitud de registros, trazabilidad de procesos, condiciones de autorizacion sanitaria.
5. ORGANIZAR evidencia:
   - IF mode = `evaluation`: ocupacion, estada, rotacion, altas demoradas, reingresos, rescates, eventos adversos, IAAS, continuidad, experiencia
   - IF mode = `audit`: documentos exigibles, protocolos, registros clinicos, cumplimiento de dotacion, condiciones de infraestructura, evidencia de fiscalizacion
6. IDENTIFICAR hallazgos:
   - fortalezas
   - cuellos de botella
   - fallas de transicion
   - brechas de capacidad o coordinacion
   - brechas normativas en HD si aplica
7. CLASIFICAR implicancias:
   - requiere rediseño
   - requiere implementacion de mejoras
   - requiere seguimiento adicional
8. CONSTRUIR plan de mejora:
   - accion
   - responsable
   - plazo
   - indicador
9. OUTPUT: escala, mode, criterios, hallazgos, plan de mejora, KPIs y trazabilidad.

## Signature Output
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| escala | string | unidad / establecimiento / red / territorio / nacional / multi / na |
| mode | string | evaluation / audit (determinado por el CM) |
| alcance | string | Objeto evaluado |
| criterios_evaluacion | string[] | Dimensiones usadas (diferenciadas por mode) |
| hallazgos | string[] | Hallazgos principales |
| plan_mejora | string[] | Acciones priorizadas |
| kpis_seguimiento | string[] | Indicadores de seguimiento |
| trazabilidad_normativa | string[] | Normas o guias citadas |
| resumen_ejecutivo | string | Sintesis para decision |
