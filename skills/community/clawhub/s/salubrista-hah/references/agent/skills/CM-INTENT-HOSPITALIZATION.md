---
_manifest:
  urn: urn:salud:skill:salubrista-hah-intent-hospitalization:1.0.0
  type: lazy_load_endofunctor
---

# CM-INTENT-HOSPITALIZATION

## Proposito
Clasificar semanticamente la solicitud para un agente especializado en sistemas de hospitalizacion integrados con enfasis en HD. Hereda la escala multi-nivel del agente salubrista base y determina escala, modalidad dominante y tipo de tarea sin decidir transiciones FSM ni continuidad conversacional.

## Input/Output
- **Input:** consulta: string
- **Output:** IntentResult { escala: "unidad"|"establecimiento"|"red"|"territorio"|"nacional"|"multi"|"na", modalidad: "hospital"|"domicilio"|"transicion"|"integrada"|"na", intencion_primaria: string, objeto: string, tipo_producto: string|null, escalas_secundarias: string[], modalidades_secundarias: string[], clarificacion_requerida: bool, motivo_ambiguedad: string? }

## Procedimiento
1. LEER la consulta completa e identificar el problema principal.
2. CLASIFICAR la intencion dominante:
   - IF objeto = camas, estada, flujo, reingresos, altas, saturacion, accesibilidad, uso evitable -> `hospital_analysis`
   - IF objeto = diseno de rutas, criterios, cartera, unidades de transicion, programas HD, gobernanza -> `hospital_design`
   - IF objeto = criterios de ingreso/egreso HD, operacion HD, direccion tecnica, normativa HD, continuidad hospital-domicilio -> `hah`
   - IF objeto = implementacion, pilotaje, escalamiento, roadmap, gestion del cambio -> `implementation`
   - IF objeto = evaluacion, auditoria, desempeno, calidad, seguridad, KPIs -> `evaluation`
   - IF objeto = brote, IAAS, surge de demanda, vigilancia, RAM, evento sanitario -> `vigilance`
   - IF objeto = tablero de hospitalizacion, mapa de cuellos de botella, mapa de riesgos de continuidad, brief de politica/gestion o escenario de capacidad/decision -> `product`
   - IF objeto = informe formal narrativo o reporte ejecutivo -> `report`
   - IF objeto = cierre explicito de sesion -> `cierre_sesion`
3. IDENTIFICAR escala: unidad / establecimiento / red / territorio / nacional / multi.
4. IDENTIFICAR modalidades y escala secundarias si el problema es multi-nivel o mixto.
5. IDENTIFICAR modalidad dominante: hospital / domicilio / transicion / integrada / na.
6. IDENTIFICAR objeto operativo: camas, unidad HD, servicio, hospital, red, ruta de transicion, gobernanza, otro.
7. IF `intencion_primaria = product`, IDENTIFICAR `tipo_producto`:
   - `hospitalization_dashboard`
   - `continuity_risk_map`
   - `capacity_bottleneck_map`
   - `policy_brief`
   - `decision_scenarios`
8. VERIFICAR ambiguedad: IF la consulta no permite distinguir intencion, escala o modalidad -> emitir `clarify` con motivo explicito.
9. OUTPUT: devolver escala, modalidad, intencion primaria, objeto, tipo de producto si aplica y necesidad de clarificacion.

## Signature Output
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| escala | string | unidad / establecimiento / red / territorio / nacional / multi / na |
| modalidad | string | hospital / domicilio / transicion / integrada / na |
| intencion_primaria | string | `hospital_analysis` / `hospital_design` / `hah` / `implementation` / `evaluation` / `vigilance` / `product` / `report` / `cierre_sesion` / `clarify` |
| objeto | string | Objeto operativo dominante |
| tipo_producto | string? | `hospitalization_dashboard` / `continuity_risk_map` / `capacity_bottleneck_map` / `policy_brief` / `decision_scenarios` |
| escalas_secundarias | string[] | Escalas adicionales si el problema es multi-nivel |
| modalidades_secundarias | string[] | Modalidades adicionales si el problema es mixto |
| clarificacion_requerida | bool | True si la consulta es ambigua |
| motivo_ambiguedad | string? | Solo si clarificacion_requerida = true |
