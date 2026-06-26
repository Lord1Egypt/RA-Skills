---
_manifest:
  urn: urn:salud:skill:salubrista-hah-hospital-system-analyst:1.0.0
  type: lazy_load_endofunctor
---

# CM-HOSPITAL-SYSTEM-ANALYST

## Proposito
Analizar o disenar sistemas de hospitalizacion integrados. Su foco es la trayectoria asistencial completa entre hospital, transicion y domicilio, incluyendo capacidad instalada, continuidad del cuidado, reingresos y articulacion con la red.

## Input/Output
- **Input:** mode: "analysis"|"design", problema: string, contexto: object
- **Output:** HospitalSystemResult { escala: string, modalidad_dominante: string, analisis: string, recomendaciones: string[], kpis_propuestos: string[], riesgos: string[], componente_hah_requerido: bool, implementacion_requerida: bool }

## Procedimiento
1. Resolver `kb_route` hacia el corpus de hospitalizacion integrada mas pertinente y recuperar el contenido con `knowledge_retrieval`.
2. IF el problema involucra continuidad hospital-domicilio, egreso precoz o HD -> sumar el URN HaH pertinente antes de continuar.
3. SI el problema exige detalle intrahospitalario no cubierto por `gestion-redes-*` -> declararlo como limite del corpus y complementar con `web_search`.
4. POSICIONAR la escala: unidad / establecimiento / red / territorio / nacional / multi.
5. IDENTIFICAR modalidad dominante: hospital / domicilio / transicion / integrada.
6. IF mode = `analysis`:
   - mapear demanda, accesibilidad, gestion de camas, estada media, rotacion, altas demoradas y reingresos
   - identificar cuellos de botella, descoordinacion hospital-red y oportunidad de sustitucion o extension domiciliaria
   - explicitar continuidad del cuidado, rescate y efectos no intencionales del sistema
7. IF mode = `design`:
   - definir objetivo sanitario y funcional
   - proponer criterios de ingreso y permanencia, rutas de transicion, programas HD, egreso precoz o unidades de transicion
   - definir gobernanza, nodos, roles y articulacion con APS, rehabilitacion, paliativos u otras redes
8. VERIFICAR modality fit:
   - no usar HD como descarga indiscriminada
   - justificar la modalidad segun seguridad, complejidad, estabilidad, entorno y capacidad operativa
9. PROPONER KPIs:
   - ocupacion, estada media, rotacion, altas oportunas, reingresos, rescates, eventos adversos, continuidad, experiencia usuaria, uso de capacidad
10. MARCAR salidas:
   - IF el problema requiere aterrizaje especifico en HD -> `componente_hah_requerido = true`
   - IF la propuesta exige fases, responsables o pilotaje -> `implementacion_requerida = true`
11. OUTPUT: analisis o diseno, recomendaciones, KPIs, riesgos y banderas de continuidad.

## Signature Output
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| escala | string | unidad / establecimiento / red / territorio / nacional / multi / na |
| modalidad_dominante | string | hospital / domicilio / transicion / integrada |
| analisis | string | Diagnostico o propuesta del sistema |
| recomendaciones | string[] | Recomendaciones accionables |
| kpis_propuestos | string[] | Indicadores sugeridos |
| riesgos | string[] | Riesgos y efectos no intencionales |
| componente_hah_requerido | bool | True si hace falta profundizar en HD |
| implementacion_requerida | bool | True si hace falta plan operativo detallado |
