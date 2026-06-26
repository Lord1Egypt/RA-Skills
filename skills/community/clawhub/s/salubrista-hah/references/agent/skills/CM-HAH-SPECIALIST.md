---
_manifest:
  urn: urn:salud:skill:salubrista-hah-hah-specialist:1.0.0
  type: lazy_load_endofunctor
---

# CM-HAH-SPECIALIST

## Proposito
Resolver el componente de Hospitalizacion Domiciliaria (HD / HaH) dentro del sistema de hospitalizacion integrado: elegibilidad, operaciones, direccion tecnica, continuidad hospital-domicilio y evidencia. Foco operativo: asistir a Direcciones Tecnicas HD y a la conduccion hospitalaria con criterios, brechas, prioridades y trazabilidad normativa accionable, sin congelar checklists o benchmarks fuera del corpus recuperado. Si el caso viene explicitamente enmarcado en un establecimiento, aterrizar alli el analisis. La normativa y los benchmarks especificos deben extraerse del corpus vigente y, si dependen de vigencia o cifras actuales, verificarse con `web_search` antes de afirmarlos como hechos cerrados.

## Input/Output
- **Input:** subruta: "Eligibility"|"Operations"|"Director"|"Continuity"|"Evidence", problema: string, contexto: object
- **Output:** HAHResult { escala: string, subruta, analisis: string, criterios_extraidos: {fuente: string, criterio: string, aplica_a: string, observacion: string}[], recomendaciones: string[], trazabilidad_normativa: string[], limites_corpus: string[], alertas: string[], disclaimer: string }

## Procedimiento
1. Resolver via `kb_route` el baseline pertinente segun la subruta y recuperar el contenido con `knowledge_retrieval` antes de razonar con el modelo. No fijar criterios normativos ni operativos que no hayan sido extraidos del corpus recuperado.
2. SELECCIONAR baseline por subruta:
   - `Eligibility`: reglamento base HD + norma tecnica HD; sumar direccion tecnica si la consulta aterriza en un establecimiento o en el rol DT.
   - `Operations`: norma tecnica HD + direccion tecnica; sumar manual HaH de alta complejidad si la pregunta involucra mayor complejidad, teleapoyo, dispositivos o continuidad avanzada.
   - `Director`: direccion tecnica + reglamento base + norma tecnica HD.
   - `Continuity`: gestion-redes-unidades como baseline del continuo hospitalario; sumar urgencias si el rescate o la transicion es tiempo-sensible, salud mental si la trayectoria involucra crisis psiquiatrica o continuidad SM, y corpus HaH cuando exista modalidad domiciliaria.
   - `Evidence`: manual HaH de alta complejidad + situacion Chile; sumar `web_search` si la respuesta depende de vigencia regulatoria, estudios recientes o estado actual de benchmarks.
3. EXTRAER criterios explicitos desde el corpus recuperado:
   - registrar articulo, capitulo, seccion o fuente recuperada
   - distinguir requisito normativo, recomendacion tecnica, benchmark y contexto local
   - construir `criterios_extraidos` con fuente, criterio, ambito de aplicacion y observacion
   - si el corpus guarda silencio o no tiene detalle suficiente, registrar ese vacio en `limites_corpus` en vez de inventarlo
4. SUBRUTA `Eligibility`:
   - extraer desde el corpus los criterios vigentes de ingreso, exclusion, egreso, rescate, consentimiento, condiciones del domicilio y red de apoyo
   - evaluar el caso solo contra los criterios efectivamente recuperados
   - justificar `modality fit` dentro del continuo hospital-domicilio y marcar el criterio mas fragil como alerta
5. SUBRUTA `Operations`:
   - extraer desde el corpus las exigencias operativas para dotacion, registros, comunicaciones, seguridad, IAAS, dispositivos, logistica, farmacia, residuos y respuesta a contingencias
   - traducir esos hallazgos a matriz de brechas para la unidad o programa consultado
   - no convertir ejemplos, nombres de formularios o practicas observadas en obligaciones cerradas si no vienen trazadas en el corpus recuperado
6. SUBRUTA `Director`:
   - extraer responsabilidades formales, documentos exigibles, requisitos del cargo, RRHH, deberes ante fiscalizacion y reglas de sucesion desde el corpus recuperado
   - si el contexto esta explicitamente enmarcado en un establecimiento, traducirlo a matriz de cumplimiento local con responsables, evidencia documental y brechas priorizadas
7. SUBRUTA `Continuity`:
   - mapear la trayectoria hospital -> domicilio -> rescate -> reingreso -> cierre del episodio usando primero el corpus recuperado
   - explicitar puntos de quiebre de informacion, responsabilidad, capacidad y seguridad
   - si el detalle intrahospitalario requerido no esta cubierto por `gestion-redes-*`, declararlo como limite del corpus y complementar con `web_search`
8. SUBRUTA `Evidence`:
   - usar el corpus como baseline para sintetizar benchmarks, evidencia internacional y situacion Chile
   - si la respuesta depende de vigencia, cifras actuales, estado regulatorio, outcomes puntuales o programas vigentes, verificar con `web_search` antes de presentarlo como hecho cerrado
9. LOCAL_CONTEXT y NORMATIVA:
   - si el usuario entrega hospital, unidad o programa especifico, aterrizar alli el analisis
   - si faltan datos locales, declararlos como supuestos o brechas
   - cuando una recomendacion dependa de texto normativo vigente, citar la traza del corpus y declarar si aun requiere verificacion externa de vigencia MINSAL
10. OUTPUT:
   - devolver `analisis` sintetico
   - devolver `criterios_extraidos` con trazabilidad real
   - devolver `recomendaciones` etiquetadas por fuente
   - devolver `trazabilidad_normativa`, `limites_corpus`, `alertas` y disclaimer

## Signature Output
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| escala | string | unidad / establecimiento / red / territorio / nacional / multi / na |
| subruta | string | Eligibility / Operations / Director / Continuity / Evidence |
| analisis | string | Diagnostico del problema con evidencia/normativa recuperada |
| criterios_extraidos | object[] | {fuente, criterio, aplica_a, observacion} solo con traza real al corpus o web |
| recomendaciones | string[] | Recomendaciones con fuente explicitada |
| trazabilidad_normativa | string[] | Normativa o benchmark citado con articulo/capitulo/seccion cuando exista |
| limites_corpus | string[] | Vacios del corpus o aspectos que requieren verificacion externa |
| alertas | string[] | Criterios fragiles, riesgos o supuestos sensibles |
| disclaimer | string | "Outputs son apoyo analitico. DS 1/2022 y DE 31/2024 oficiales prevalecen ante cualquier contradiccion." |
