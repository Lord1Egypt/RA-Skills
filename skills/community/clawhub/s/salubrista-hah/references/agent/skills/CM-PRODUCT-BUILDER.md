---
_manifest:
  urn: urn:salud:skill:salubrista-hah-product-builder:1.0.0
  type: lazy_load_endofunctor
---

# CM-PRODUCT-BUILDER

## Proposito
Construir productos estructurados para decisiones sobre sistemas de hospitalizacion integrados: tableros de hospitalizacion, mapas de cuellos de botella o riesgos de continuidad, briefs de politica/gestion y escenarios de capacidad o decision.

## Input/Output
- **Input:** contenido_analisis: object, tipo_producto: "hospitalization_dashboard"|"continuity_risk_map"|"capacity_bottleneck_map"|"policy_brief"|"decision_scenarios", audiencia: string
- **Output:** Product { escala: string, tipo_producto, estructura, componentes: string[], criterios_uso: string[], trazabilidad: string[], disclaimer }

## Procedimiento
1. RECIBIR el contenido acumulado desde analisis del sistema, HD, implementacion, evaluacion o vigilancia.
2. IDENTIFICAR escala, modalidad dominante y decision objetivo.
3. IF `tipo_producto = hospitalization_dashboard`:
   - estructurar KPIs de ocupacion, estada, rotacion, altas, rescates, reingresos, continuidad y seguridad
4. IF `tipo_producto = continuity_risk_map`:
   - organizar riesgos de transicion por probabilidad, impacto, modalidad, responsable y mitigacion
5. IF `tipo_producto = capacity_bottleneck_map`:
   - ordenar cuellos de botella por nodo, causa, impacto sobre camas/HD, dependencia y accion sugerida
6. IF `tipo_producto = policy_brief`:
   - estructurar problema, contexto, opciones, tradeoffs, recomendacion e implicancias de implementacion
7. IF `tipo_producto = decision_scenarios`:
   - construir alternativas comparables con supuestos, beneficios, riesgos, carga operativa y condiciones de exito
8. VERIFICAR:
   - el producto hace visible la trayectoria hospital-domicilio
   - los supuestos y limites del corpus intrahospitalario son explicitos cuando aplica
   - la decision final no se presenta como resuelta por el agente
9. OUTPUT: producto estructurado, componentes, criterios de uso, trazabilidad y disclaimer.

## Signature Output
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| escala | string | unidad / establecimiento / red / territorio / nacional / multi / na |
| tipo_producto | string | hospitalization_dashboard / continuity_risk_map / capacity_bottleneck_map / policy_brief / decision_scenarios |
| estructura | string | Forma general del producto |
| componentes | string[] | Campos o secciones del producto |
| criterios_uso | string[] | Como leer o usar el producto |
| trazabilidad | string[] | Evidencia y normativa citada |
| disclaimer | string | Producto de apoyo tecnico; la decision final corresponde a la conduccion humana |
