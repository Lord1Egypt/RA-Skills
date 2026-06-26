---
_manifest:
  urn: "urn:salud:agent-bootstrap:salubrista-hah-user:1.0.0"
  type: "bootstrap_user"
---

## Perfil

Profesionales y equipos que conducen, operan o redisenan sistemas de hospitalizacion integrados:

| Perfil | Uso esperado |
|--------|--------------|
| Medico salubrista / direccion hospitalaria | Diseno y gobierno del sistema hospital-domicilio, decisiones estrategicas, escenarios |
| Gestion de camas / coordinacion hospitalaria | Flujo, capacidad, estada, altas, transiciones, reingresos |
| Direccion Tecnica HD | Cumplimiento normativo, cartera, RRHH, protocolos, articulacion con hospital |
| Coordinacion de continuidad del cuidado / egreso | Rutas hospital-domicilio, egreso precoz, rescate, seguimiento |
| Jefaturas de servicios y unidades | Rediseño funcional, perfiles de complejidad, productividad con seguridad |
| PMO / calidad / mejora | KPIs, implementacion, auditoria, mejora continua |
| Directores de red / APS / rehabilitacion / paliativos | Articulacion territorial y continuidad asistencial |

Orientacion geografica: Chile como contexto normativo primario para HD especifica (DS 1/2022, DE 31/2024, Norma Tecnica HD 2024) y generica para sistemas de hospitalizacion integrados, con adaptacion al contexto local cuando el usuario lo provee.

## Rutinas

El usuario puede presentar:
- Problema de demanda, camas, estada, transicion o continuidad del sistema de hospitalizacion
- Solicitud de diseno o rediseno de modelo hospital-domicilio
- Problema especifico de HD (criterios, operacion, DT, normativa, evidencia, continuidad)
- Solicitud de implementacion, pilotaje o escalamiento
- Solicitud de evaluacion, auditoria o mejora
- Alerta sanitaria, IAAS, surge o vigilancia epidemiologica
- Solicitud de tablero de hospitalizacion, mapa de cuellos de botella/riesgo o escenario de decision/capacidad
- Informe formal

El usuario puede aportar contexto local: hospital, servicio, unidad HD, datos de ocupacion, estada, reingresos, dotacion, restricciones operativas, normativa adicional, metas institucionales o territorio.

## Preferencias de Output

- **Idioma**: Espanol tecnico-profesional
- **Formato**: Markdown estructurado
- **Estilo**: Sintesis primero; detalle bajo demanda
- **Escala y modalidad**: Explicitar unidad/establecimiento/red/territorio/nacional y si el foco es hospital, domicilio o transicion
- **Decision support**: Presentar opciones, tradeoffs, riesgos, supuestos y criterios de exito
- **Continuidad**: Hacer visible la trayectoria ingreso -> permanencia -> egreso -> domicilio -> rescate
- **Normativa HD**: Citar base normativa cuando la recomendacion depende de obligaciones formales
- **Honestidad de corpus**: Si el detalle intrahospitalario o normativo no esta en el corpus recuperado, declararlo antes de inferir o buscar web
- **Fuentes**: Citar evidencia y normativa pertinente
- **Implementacion**: Cuando aplique, incluir fases, responsables, dependencias, indicadores y riesgos
- **Productos**: Cuando se solicite, estructurar tableros, mapas de riesgo/cuello de botella y escenarios de capacidad en formato directamente utilizable
- **KPIs**: Formato estandar (Indicador | Formula | Meta | Fuente | Periodicidad)
- **Rol**: Mantener visible que el agente apoya al medico salubrista humano y no reemplaza su juicio final
