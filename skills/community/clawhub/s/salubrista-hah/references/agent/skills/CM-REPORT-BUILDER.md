---
_manifest:
  urn: urn:salud:skill:salubrista-hah-report-builder:1.0.0
  type: lazy_load_endofunctor
---

# CM-REPORT-BUILDER

## Proposito
Construir informes estructurados para apoyar decisiones sobre sistemas de hospitalizacion integrados. Integra analisis del sistema, diseno, continuidad del cuidado, HD, capacidad, implementacion, KPIs y trazabilidad normativa en un formato util para la conduccion humana.

## Input/Output
- **Input:** contenido_analisis: object, tipo_informe: string, audiencia: string
- **Output:** Report { tipo_informe: string, audiencia: string, resumen_ejecutivo: string, escala: string, modalidad: string, analisis: string, opciones: string[], implementacion: string[], kpis: string[], riesgos: string[], trazabilidad: string[], disclaimer: string }

## Procedimiento
1. RECIBIR contenido acumulado desde analisis del sistema, HD, implementacion, evaluacion o vigilancia.
2. IDENTIFICAR tipo de informe:
   - diagnostico del sistema de hospitalizacion
   - propuesta de rediseño hospital-domicilio
   - plan de implementacion
   - evaluacion de desempeno
   - cumplimiento normativo HD
   - alerta o vigilancia
3. IDENTIFICAR audiencia: medico salubrista, direccion hospitalaria, DT HD, coordinacion de camas, red territorial, regulador u otra autoridad.
4. ESTRUCTURAR informe:
   - problema, escala y modalidad dominante
   - trayectoria asistencial involucrada
   - hallazgos principales
   - opciones de decision o rediseño
   - riesgos y continuidad del cuidado
   - implicancias de implementacion
   - KPIs y criterios de seguimiento
   - trazabilidad de evidencia y normativa
   - disclaimer de rol de copiloto
5. VERIFICAR coherencia:
   - hospital y domicilio no aparecen como silos
   - la modalidad esta justificada
   - la decision final queda en la conduccion humana
6. SI `web_search` fue necesario para evidencia faltante o vigencia normativa -> integrar y citar.

## Signature Output
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| tipo_informe | string | Tipo de producto generado |
| audiencia | string | Destinatario principal |
| resumen_ejecutivo | string | Sintesis para decision |
| escala | string | unidad / establecimiento / red / territorio / nacional / multi / na |
| modalidad | string | Modalidad dominante |
| analisis | string | Analisis principal |
| opciones | string[] | Opciones o cursos de accion |
| implementacion | string[] | Implicancias operativas o siguientes pasos |
| kpis | string[] | Indicadores de seguimiento |
| riesgos | string[] | Riesgos, tradeoffs y dependencias |
| trazabilidad | string[] | Evidencia y normativa citada |
| disclaimer | string | Apoyo tecnico; la conduccion y decision final permanecen en la persona responsable |
