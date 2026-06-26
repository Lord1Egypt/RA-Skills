---
_manifest:
  urn: "urn:salud:kb:hodom-manual-alta-complejidad"
  provenance:
    created_by: "Codex"
    created_at: "2026-03-10"
    source: "source/pro/hodom/manual-general-hodom-2026.md"
version: "1.1.1"
status: published
tags: [hodom, hospitalizacion-domiciliaria, alta-complejidad, hospital-at-home, gestion-clinica]
lang: es
extensions:
  kora:
    family: generic
---

# Manual de Hospitalizacion Domiciliaria de Alta Complejidad

## Fundamentos del modelo Hospital at Home

### Definicion y taxonomia

- `Hospital at Home` (`HaH`) = servicio agudo que sustituye hospitalizacion tradicional trasladando personal, equipos, tecnologia, medicacion y capacidades hospitalarias al domicilio.
- No equivale a:
  - `home health` de baja complejidad
  - cuidado ambulatorio esporadico
  - paliativos tradicionales sin soporte agudo equivalente a sala
- Rasgos distintivos:
  - evaluacion medica y de enfermeria diaria
  - terapias intravenosas
  - diagnostico movil
  - monitorizacion continua
- Distincion central:
  - el "hospital" se define por intensidad clinica, tratamientos y outcomes
  - no por infraestructura fisica `brick-and-mortar`

### Evolucion historica y adopcion global

- Primeros ensayos:
  - Reino Unido
  - fines de la decada de `1970`
- Adopcion consolidada:
  - Australia
  - Canada
  - Israel
- Victoria, Australia:
  - todos los hospitales regionales y metropolitanos con programa HaH
  - gestion aproximada de `6%` de los dias-cama del estado
- Estados Unidos:
  - programa fundacional en Johns Hopkins
  - decada de `1990`
  - referencia operativa `1995`
  - liderazgo: Bruce Leff
- Vias clinicas fundacionales:
  - neumonia adquirida en la comunidad
  - insuficiencia cardiaca congestiva
  - `EPOC`
  - celulitis

### Triple objetivo y valor sanitario

| Dimension           | Hechos anclados                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------ |
| Experiencia         | Mayor confort, mejor sueno, mayor dignidad, mayor apoyo emocional                                      |
| Resultados clinicos | Delirium `24%` a `9%`; readmision a `30` dias `23%` a `7%`; mortalidad menor o no inferior             |
| Funcion             | Sedentarismo `78.0%` vs `86.0%`; tiempo en cama `18%` vs `55%`; pasos diarios `834` vs `120`           |
| Economia            | Ahorro por episodio entre `19%` y mas de `30%`; Johns Hopkins `32%` menos costo (`$5,081` vs `$7,480`) |

## Vias clinicas, triaje y seleccion

### Arquitectura de admision

| Modelo                | Descripcion                                                                      | Ventaja principal                                              | Riesgo principal                                                    |
| --------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------- |
| Evitacion de ingreso  | Admision directa desde urgencias, clinicas comunitarias o derivacion ambulatoria | Menor mortalidad, mayor ahorro, alivio de congestion           | Sobreutilizacion o admision inapropiada                             |
| Alta temprana apoyada | Traslado al hogar tras estancia corta intrahospitalaria                          | Menor riesgo de admision inadecuada; facilita adopcion inicial | Ahorro mas atenuado por costos iniciales y duplicacion transicional |

- Variante emergente:
  - `Inpatient-at-Home`
  - triaje directo desde atencion primaria o comunidad
  - evita incluso el paso por urgencias
- Diseno operativo recomendado:
  - iniciar con `step-down` para consolidar confianza y logistica
  - expandir luego a `step-up` para maximizar retorno y liberacion de camas

### Criterios de inclusion y exclusion medica

#### Inclusion

- Requisito basal:
  - necesidad documentada de cuidados agudos de nivel hospitalario
- Validacion de utilizacion:
  - `InterQual`
  - `MCG Health`
  - `Dragonfly`
- Condiciones de ingreso:
  - estabilidad hemodinamica suficiente para manejo seguro en domicilio
  - ausencia de necesidad de resucitacion o soporte vital continuo
  - plan terapeutico definido
  - trayectoria clinica previsible
- Perfil frecuente:
  - pacientes de `65` anos o mas
  - multimorbilidad
  - alto riesgo de delirium, infeccion nosocomial, caidas o declive funcional si permanecen hospitalizados

#### Exclusiones y contraindicaciones absolutas

- shock
- infarto agudo de miocardio
- necesidad de `UCI` o atencion intensiva previsible
- reintervencion quirurgica inminente
- procedimientos invasivos recurrentes:
  - punciones lumbares
  - biopsias multiples
- necesidad continua o repetida de imagenologia avanzada no movilizable:
  - tomografia computarizada
  - resonancia magnetica
- requerimiento rutinario de sustancias controladas no aptas para el domicilio
- dependencia funcional que exige mas de una persona para transferencias basicas

- Exigencia transversal:
  - evaluar la trayectoria probable de la enfermedad
  - anticipar escalamiento o necesidad de reoperacion
  - mantener protocolo de retorno expedito al hospital fisico

### Condiciones clinicas prevalentes

### Insuficiencia cardiaca congestiva

- Triaje:
  - sobrecarga de volumen aguda
  - necesidad de diureticos IV
  - sin shock cardiogenico
  - sin isquemia aguda
  - sin necesidad de telemetria intensiva o `UCI`
- Monitorizacion:
  - peso diario
  - presion arterial
  - frecuencia cardiaca
  - oximetria
- Intervenciones:
  - diureticos de asa IV
  - titulacion segun respuesta
  - control de electrolitos con flebotomia domiciliaria
  - restriccion de sodio y fluidos

### EPOC y asma

- Triaje:
  - disnea, tos o esputo con necesidad de intensificacion terapeutica
  - sin intubacion
  - sin ventilacion mecanica no invasiva de soporte vital continuo
- Monitorizacion:
  - `SpO2`
  - frecuencia respiratoria
  - cuestionarios de sintomas
  - nivel de actividad
- Intervenciones:
  - corticosteroides sistemicos
  - antibioticos si hay sospecha bacteriana
  - broncodilatadores nebulizados
  - titulacion dinamica de oxigenoterapia

### Neumonia adquirida en la comunidad

- Triaje:
  - requiere oxigenoterapia y antibioterapia parenteral
  - con estabilidad hemodinamica
  - excluye hipoxemia refractaria severa, sepsis con hipotension o soporte ventilatorio
- Diagnostico y monitoreo:
  - oximetria
  - temperatura
  - frecuencia cardiaca
  - rayos X portatiles con transmision radiologica segura
- Intervenciones:
  - fluidoterapia IV
  - antibioticos IV
  - desescalada rapida a via oral cuando exista respuesta y tolerancia

### ITU complicada y pielonefritis

- Triaje:
  - dolor incontrolable
  - hiperemesis o intolerancia oral
  - necesidad de antibioticos IV por resistencia microbiana
  - posible alta comorbilidad, sin shock septico
- Monitorizacion:
  - temperatura
  - presion arterial
  - frecuencia cardiaca
  - funcion renal
- Intervenciones:
  - antimicrobianos IV
  - fluidoterapia
  - laboratorios seriados domiciliarios
- Referencia de seguridad:
  - Mayo Clinic reporta resultados equivalentes a sala

### Celulitis e infecciones de piel y tejidos blandos

- Triaje:
  - fracaso de tratamiento ambulatorio
  - sintomatologia sistemica moderada
  - excluye fascitis necrotizante o necesidad inminente de desbridamiento
- Monitorizacion:
  - temperatura
  - evaluacion visual directa
  - fotografia clinica o videollamada
- Intervenciones:
  - antibioticos parenterales
  - en algunos protocolos, autoadministracion guiada
  - curaciones complejas in situ

### Expansion a cirugia y oncologia

#### Readmisiones posoperatorias y vertical quirurgica

- Justificacion:
  - libera camas quirurgicas de alta demanda
  - aumenta `backfill margin`
- Vias clinicas elegibles:
  - infeccion de sitio quirurgico y espacios profundos
  - ileo paralitico
  - obstruccion intestinal
  - cuidado de sonda nasogastrica a succion
  - deshidratacion por nausea intratable o ileostomia de alto debito
  - cuidado de ostomias
  - recuperacion posquirurgica temprana:
    - bariatrica
    - colectomia laparoscopica
    - reversion de ileostomia
- Requisitos operativos:
  - exclusion absoluta si existe necesidad de reintervencion quirurgica
  - re-triaje y traslado rapido ante sepsis severa o cirugia de rescate
  - derivacion directa desde clinicas quirurgicas con apoyo de navegadores/enfermeras avanzadas

#### Manejo agudo en oncologia

- Alcance emergente:
  - quimioterapia domiciliaria
  - soporte agudo post trasplante de celulas madre hematopoyeticas
  - modelos tipo `Home Sweet Home`
- Requisitos:
  - cuidado experto de lineas venosas centrales
  - prevencion de `CLABSI`
  - contencion y manejo de derrames citotoxicos
- Continuidad:
  - puente fluido hacia paliativos domiciliarios de alta intensidad

### Vivienda, determinantes sociales y conectividad

#### Idoneidad estructural y geografica

- Servicios basicos obligatorios:
  - electricidad estable
  - agua corriente
  - climatizacion adecuada:
    - aire acondicionado
    - calefaccion
- Inspeccion del hogar:
  - cableado electrico
  - habitabilidad del dormitorio
  - acceso y seguridad del bano
  - riesgos arquitectonicos de caidas
- Riesgos ambientales a descartar:
  - moho
  - humedad
  - acumulacion de polvo
  - roedores
  - toxinas o alergenos severos
- Cobertura geografica:
  - radio delimitado por tiempo de conduccion
  - referencia frecuente: `30` minutos desde hospital base
- Conectividad:
  - banda ancha o red celular confiable
  - `hotspot` si se requiere
  - respaldo electrico local para equipos medicos

#### Determinantes sociales de la salud

- Evaluar:
  - hacinamiento
  - seguridad del vecindario
  - seguridad alimentaria
  - acceso a dieta adecuada para restricciones clinicas
  - alfabetizacion en salud
  - idioma primario
  - competencia tecnologica
- Respuesta programatica:
  - articular recursos comunitarios
  - entrega de comidas
  - mitigacion de brecha digital

### Red de apoyo social y rol del cuidador informal

- Inclusion prioriza:
  - familiares, conyuge o amigos con presencia constante
  - capacidad para apoyar actividades basicas e instrumentales
- Evaluacion de idoneidad:
  - capacidad fisica
  - capacidad cognitiva
  - disposicion emocional
- Tareas esperadas del cuidador:
  - administracion guiada de medicacion pautada
  - reporte de sintomas
  - supervision de equipos simples
- Limite critico:
  - no transferir enfermeria especializada ni procedimientos invasivos
- Vigilancia del programa:
  - monitorizar estres, ansiedad y fatiga del cuidador
  - educacion continua para sostener la red de apoyo

## Operaciones clinicas y logistica 24/7

### Centro de comando virtual

- Rol:
  - nucleo clinico-operativo del programa
  - equivalente funcional de estacion de enfermeria centralizada
- Cobertura:
  - `24/7`
  - medicos y enfermeria de forma continua
- Arquitectura:
  - plataforma en nube segura
  - interoperabilidad bidireccional con `EHR`
  - `dashboard` unico para tendencias fisiologicas, alertas `IA`, priorizacion de riesgo y documentacion
- Tecnologia desplegada en domicilio:
  - tableta para videoconferencias
  - telefono de marcacion directa al centro
  - extensores Wi-Fi o conectividad celular `4G/LTE`
  - pulsera o collar de alerta de emergencia
- Funciones:
  - recepcion de datos `RPM`
  - vigilancia de adherencia al envio de datos
  - contacto proactivo si faltan transmisiones
  - coordinacion interdisciplinaria
  - programacion de visitas presenciales

### Equipo multidisciplinario y frecuencia minima

#### Medicos hospitalistas y `APPs`

- Responsables de:
  - admision
  - plan de cuidados
  - triaje de agudeza
- Cobertura:
  - disponibilidad `24/7`
- Modelo maduro:
  - visita medica diaria virtual
  - puede ser sincrona con enfermeria presente al lado del paciente

#### Enfermeria de atencion directa

- Ejecuta:
  - medicamentos IV
  - oxigenoterapia
  - curaciones complejas
  - flebotomia
  - pruebas en punto de atencion
  - `ECG`
- Carga tipica descrita:
  - cerca de `3` horas totales al dia
  - distribuidas en multiples visitas

#### Paramedicos comunitarios / `MIH`

- Funcion:
  - extension de medicina y enfermeria
  - evaluacion presencial
  - tratamientos protocolizados
  - respuesta inmediata ante deterioro
- Regla `AHCAH`:
  - pueden contar para visitas presenciales diarias
  - solo bajo supervision clinica de enfermera registrada o medico
- Barrera regulatoria:
  - ajuste de normativas locales que restringen practica al sistema `911`

#### Farmaceuticos clinicos

- Funciones:
  - conciliacion de medicamentos
  - prevencion de interacciones
  - supervision de dispensacion
  - educacion virtual al paciente y red de apoyo

#### Trabajo social y gestion de casos

- Funciones:
  - evaluar seguridad del domicilio
  - confirmar soporte social
  - coordinar equipos medicos duraderos
  - conectar con servicios comunitarios
- Transicion:
  - seguimiento posalta de `30` dias en la referencia citada

#### Protocolo minimo de contacto

- `1` evaluacion diaria por medico, `NP` o `PA`
- minimo `2` visitas presenciales diarias por enfermeria o personal clinico habilitado
- capacidad de respuesta presencial ante crisis en hasta `30` minutos
- frecuencia titulable segun via clinica y agudeza

### Cadena de suministro y ultima milla

- Dominio logistico:
  - medicamentos
  - terapias de infusion
  - `DME`
  - oxigeno
  - conectividad
  - alimentacion
- Riesgo estructural:
  - cadena no lineal, descentralizada y dependiente de multiples proveedores
- Exigencias:
  - despliegue en horas
  - trazabilidad completa
  - coordinacion de proveedores centralizada

#### Logistica farmaceutica

- Riesgos:
  - inestabilidad termica
  - errores de preparacion
  - quiebres de continuidad
- Mitigaciones:
  - indicadores termicos y registradores continuos
  - lotes preparados para ciclos de `24` horas
  - minima manipulacion a la cabecera
  - kits redundantes con medicacion urgente
- Sustancias controladas:
  - cadena de custodia documentada
  - embalaje `tamper-evident`
  - baja visibilidad del contenido

#### `DME`, soporte respiratorio y nutricion

- Entrega inmediata de:
  - camas articuladas
  - sillas de ducha
  - concentradores y sistemas de oxigeno
  - nebulizacion
  - tabletas y dispositivos `RPM`
- Requisito:
  - todo instalado, calibrado y operativo al arribo del paciente
- Soporte nutricional:
  - articulacion con recursos comunitarios
  - convenios directos de distribucion
  - referencia operativa: `Meals on Wheels`

#### Logistica inversa

- Recoleccion y eliminacion segura de:
  - residuos biologicos
  - insumos de vias intravenosas
  - material de curaciones
- Cumplimiento:
  - normativas de bioseguridad y salud publica

### FMEA, subcontratistas y control de calidad

- Riesgos de tercerizacion:
  - brechas de competencia
  - variabilidad del cuidado
  - capacidad insuficiente `24/7`
  - deficit de gobernanza
  - retraso de un solo proveedor compromete el plan total
- Metodo `FMEA`:
  1. mapear procesos y subprocesos criticos
  2. identificar modos de fallo y calcular `RPN`
  3. intervenir primero sobre eventos de mayor impacto clinico
- Ejemplos de fallos de alto riesgo:
  - retraso de antibioticos IV
  - falla de soporte respiratorio
  - errores de calibracion `RPM`
- Politicas contractuales obligatorias:
  - redundancia sistemica
  - auditoria de competencias y licencias
  - rutas de escalamiento integradas al centro de comando
  - `SLA`, `KPI` logisticos y clinicos
  - mejora continua posterior a la firma del contrato

## Infraestructura tecnologica y salud digital

### Monitorizacion remota de pacientes

- Pilar tecnologico del modelo:
  - sustituye rondas y telemetria hospitalaria con datos fisiologicos en tiempo real
- Exigencia regulatoria:
  - dispositivos autorizados, p. ej. `FDA 510(k)`
  - clase II en la referencia citada
  - diferenciacion explicita frente a `wellness apps`
- Kit biometrico posible:
  - presion arterial
  - frecuencia cardiaca
  - `ECG`
  - oximetria `SpO2`
  - peso
  - glucosa capilar o `CGM`
  - termometria
- Riesgos de uso:
  - mala colocacion del oximetro
  - lecturas espurias
  - necesidad de educacion estructurada y calibracion
- Conectividad recomendada:
  - `4G/LTE/5G`
  - `hub` o tableta central
  - extensores de senal
  - respaldo electrico
- Seguridad:
  - cifrado en transito y reposo
  - autenticacion robusta
  - actualizacion segura de firmware
  - trazabilidad por auditoria

### IA, analitica predictiva y fatiga de alertas

- Problema:
  - sobrecarga de datos y desgaste profesional
  - solo `6.6%` de transmisiones o alertas requiere accion clinica real en cohortes monitorizadas citadas por la fuente
- Rol de la `IA`:
  - convertir datos brutos en `actionable insights`
  - detectar descompensacion preclinica
  - automatizar decisiones rutinarias
  - integrar marcadores conductuales:
    - patrones de sueno
    - uso de smartphone
- Jerarquia de escalamiento:
  - Nivel `1`: filtro algoritmico y recordatorios automatizados
  - Nivel `2`: evaluacion contextual e intervencion protocolizada por enfermeria
  - Nivel `3`: escalamiento medico ante incertidumbre o deterioro refractario
- Regla operacional:
  - umbrales individualizados por fisiologia y trayectoria del paciente
  - ejemplo: `SpO2` basal mas baja en `EPOC` severo

### Diagnostico movil en el domicilio

#### Rayos X portatiles

- Equipos digitales compactos:
  - rango referido de `5 kg` a `45 kg`
  - generadores de alta frecuencia
  - baterias de ion-litio
- Requisitos:
  - dosis radiologica baja
  - protocolos de `shielding`
- Usos:
  - neumonia
  - redistribucion de flujo en insuficiencia cardiaca
  - fracturas tras caidas
  - verificacion de vias y sondas
- Flujo:
  - posicionamiento de `DR panel`
  - adquisicion instantanea
  - sin revelado quimico

#### `POCUS`

- Equipos:
  - transductores de mano
  - consolas ligeras o dispositivos inteligentes de grado medico
- Usos:
  - ecocardiograma dirigido
  - descarte de `TVP`
  - derrame pleural
  - ascitis
  - tejidos blandos en celulitis y abscesos
  - guiado de accesos venosos perifericos o lineas medias

#### `ECG` y telemetria de alta resolucion

- `ECG` de `12` derivaciones:
  - calidad hospitalaria
  - arritmias
  - isquemia aguda
  - seguimiento de `QTc`
- Monitores Holter y parches biometricos:
  - vigilancia continua de `24` horas a varios dias
  - menor carga funcional para el paciente

#### Transmision e interoperabilidad diagnostica

- Requisito:
  - encriptacion in situ
  - transmision inmediata por red celular propia del equipo
- Lectura remota:
  - radiologia y cardiologia prioritaria
  - plataformas tipo `MediMatrix` o `PACS` hospitalario
  - informes en `EHR` el mismo dia o en horas

### Interoperabilidad, `EHR` y facturacion `CPT`

#### Arquitectura y gobernanza

- Estandares:
  - `FHIR`
  - `HL7`
  - `RESTful APIs`
- Reglas de datos `PGHD`:
  - definir si ingresan automaticamente al `EHR`
  - o si requieren validacion previa
- Requisito de interfaz:
  - distinguir metricas tomadas en domicilio vs mediciones presenciales
- Documentacion automatizada:
  - `time-stamp`
  - `audit logs`
  - control de acceso por roles
  - cumplimiento `HIPAA`

#### Codigos `CPT`

| Codigo  | Hecho operativo preservado                                                                        |
| ------- | ------------------------------------------------------------------------------------------------- |
| `99453` | Configuracion inicial del dispositivo y educacion estructurada al paciente                        |
| `99454` | Provision del dispositivo y transmision diaria; requiere al menos `16` dias de datos en `30` dias |
| `99457` | Primeros `20` minutos mensuales de comunicacion interactiva y gestion clinica                     |
| `99458` | Cada bloque adicional de `20` minutos                                                             |
| `99091` | Recoleccion, analisis e interpretacion de datos fisiologicos continuos                            |

- Capacidad minima del sistema:
  - reportes de fin de mes
  - dias monitorizados
  - tendencias
  - minutos documentados
  - justificacion clinica continua

## Calidad, seguridad y outcomes

### Mortalidad y morbilidad iatrogenica

- Metaanalisis:
  - `61` ensayos controlados aleatorizados
  - `OR 0.81`
  - `IC 95% 0.69-0.95`
  - `P = 0.008`
  - `NNT = 50`
- `CMS` / `AHCAH`:
  - mortalidad inferior en los `25` `MS-DRG` mas frecuentes
  - diferencia estadisticamente significativa en `11` de esos `25`
- Cohortes especificas:
  - `0.93%` en HaH vs `3.4%` hospitalario
- Infecciones asociadas a la atencion:
  - tasas inferiores frente a hospital fisico
  - menor exposicion a patogenos nosocomiales y multirresistentes
- Delirium:
  - `24%` en hospital tradicional
  - `9%` en HaH

### Readmisiones, urgencias y `SNF`

| Indicador                                | Hospital tradicional | HaH     | Nota                                |
| ---------------------------------------- | -------------------- | ------- | ----------------------------------- |
| Readmision a `30` dias                   | `23%`                | `7%`    | Ensayo pivotal de Brigham           |
| Readmision a `30` dias                   | `15.60%`             | `8.60%` | `MACT` Mount Sinai                  |
| Visitas a urgencias                      | `13%`                | `7%`    | Menor uso posalta                   |
| Visitas a urgencias                      | `11.70%`             | `5.80%` | Resultado institucional concordante |
| Derivacion a `SNF`                       | `10.40%`             | `1.70%` | Menor institucionalizacion          |
| Riesgo relativo de ingreso a largo plazo | `1`                  | `0.16`  | Menor dependencia institucional     |

- Metaanalisis:
  - riesgo relativo de readmision a `30` dias: `0.74`
- Matiz `CMS`:
  - cohorte analizada: mas de `11,000` pacientes bajo `AHCAH`
  - resultados de readmision varian por `MS-DRG`
  - hubo `2` `MS-DRG` con readmision significativamente mas alta en HaH
  - y `3` `MS-DRG` con tasas muy altas en hospital fisico
- Implicacion:
  - el beneficio depende de seleccion rigurosa por patologia

### Estado funcional y movilidad

- `HAD`:
  - prevalencia cercana a `30%` en adultos mayores hospitalizados
- Acelerometria:
  - sedentarismo `78.0%` vs `86.0%`
  - tiempo en cama `18%` vs `55%`
  - pasos diarios `834` vs `120`
  - actividad ligera `21.25%` vs `13.92%`
- Cohortes asiaticas:
  - `79.7%` reporta menos tiempo en cama
  - `73.2%` aumenta deambulacion
- Efecto clinico:
  - preservacion de `AVD` y `AIVD`
  - menor necesidad de `SNF`
  - menor cascada de dependencia institucional

### Seguridad del paciente y escalamiento clinico

#### Medicacion

- Riesgos criticos:
  - errores de medicacion
  - polifarmacia
  - preparacion compleja en domicilio
- Mitigaciones:
  - prescripcion integrada con `EHR`
  - lotes de `24` horas
  - minima preparacion a la cabecera
  - escaneo de codigos de barras en punto de atencion
  - evaluacion formal de capacidad de autoadministracion
  - pastilleros bicolores cuando aplique
  - enfermeria virtual para supervisar tomas

#### Transporte y almacenamiento de farmacos

- Requisitos:
  - monitoreo termico activo
  - contenedores de cadena de frio
  - condiciones de almacenamiento domiciliario validadas
  - kits de rescate en vivienda para farmacos urgentes

#### Sustancias controladas

- Reglas:
  - cadena de custodia ininterrumpida
  - empaque `tamper-evident`
  - baja visibilidad en transporte
  - `lock boxes` en domicilio

#### Tasas de escalamiento

- Definicion:
  - retorno no planificado al hospital por deterioro, fracaso terapeutico o complicacion no manejable en casa
- Datos:
  - `AHCAH`: `7.2%` en cohorte de mas de `11,000` pacientes
  - cohorte de pielonefritis aguda: `4.8%`
- Lectura operacional:
  - tasas inferiores a `10%` confirman soporte remoto efectivo
  - una tasa demasiado cercana a `0%` puede indicar triaje excesivamente conservador
- Respaldo reglamentario:
  - capacidad de desplegar respuesta presencial en hasta `30` minutos
  - articulacion con `911` y paramedicos comunitarios

## Economia de la salud, capacidad y reembolso

### Costos directos e indirectos

| Hallazgo            | Magnitud                                                                      |
| ------------------- | ----------------------------------------------------------------------------- |
| Johns Hopkins       | `32%` menos costo total (`$5,081` vs `$7,480`)                                |
| Presbyterian        | `19%` menos costo medio                                                       |
| Brigham and Women's | `38%` menos costo ajustado por episodio                                       |
| Singapur            | `42%` menos costo por dia-cama; `24%` menos por episodio; ahorro de `\$1,665` |

- Impulsores del ahorro:
  - menor `overhead`
  - menos laboratorios: mediana `3` vs `15`
  - menor uso de imagenes: `14%` vs `44%`
  - menos interconsultas: `2%` vs `31%`
  - menor estancia media en datos fundacionales: `3.2` vs `4.9` dias
  - menor utilizacion posaguda costosa
- Extension del beneficio:
  - a `30` dias, la brecha total puede ampliarse hasta `25%`

### Capacidad instalada y `backfill margin`

- Premisa:
  - HaH funciona como valvula de escape para sistemas saturados
- Dato contextual:
  - hospitales con programas HaH muestran ocupacion media `20` puntos porcentuales mayor que hospitales tradicionales
- Mecanismo:
  - trasladar casos medicos de baja o moderada agudeza al hogar
  - liberar cama fisica
  - rellenar con casos mas rentables:
    - quirurgicos
    - alta complejidad
- Tension financiera:
  - dificil reemplazar una admision de `$10,000` o `$12,000` si no existe certeza de `backfill`

#### Casos cuantificados

- Readmisiones quirurgicas elegibles:
  - `30.1%` a `60` dias
- Dias-cama liberados:
  - `4,152`
- Margen potencial por nueva capacidad:
  - `\$8.8` millones
- Expansion virtual:
  - `250` camas
  - ahorro de capital cercano a `\$500` millones
  - supuesto: `\$2` millones por cama fisica nueva
- Programas maduros:
  - Advocate Health: `33,000` dias-cama liberados tras mas de `9,400` pacientes desde `2020`
  - Contessa: mas de `32,000` dias-cama liberados desde `2016`
  - Atrium Health: proyeccion de liberar `10%` de sus camas al tratar `100` pacientes diarios para `2025`

### Marco regulatorio y reembolso en Estados Unidos

- Programa:
  - `Acute Hospital Care at Home` (`AHCAH`) de `CMS`
- Marco legislativo referido en la fuente:
  - Ley de Asignaciones Consolidadas de `2026`
  - paridad de pago `DRG`
  - extension de exenciones hasta `30 de septiembre de 2030`
- Exigencia operativa:
  - documentacion robusta
  - codificacion correcta
  - capacidad de auditoria

### Atencion basada en valor

- Sinergias:
  - `ACO`
  - pagos capitados
  - `Medicare Advantage`
  - pagadores privados alineados con valor
- Logica economica:
  - evita urgencias y hospitalizaciones fisicas costosas
  - reduce uso posagudo y `SNF`
  - alinea incentivos clinicos y financieros

## Experiencia del paciente, cuidador y equidad

### Satisfaccion del paciente

| Indicador                                  | Hospital tradicional | HaH     |
| ------------------------------------------ | -------------------- | ------- |
| `Picker`                                   | `11.0`               | `13.4`  |
| `NPS`                                      | `45.5`               | `88.4`  |
| Disposicion a reutilizar servicio          | n/a                  | `97.5%` |
| Pacientes "extremadamente" o "muy" comodos | `60.9%`              | `84.4%` |

- Calidad del sueno:
  - `74.8%` reporta sueno superior en domicilio
- Beneficios percibidos:
  - privacidad
  - flexibilidad de rutina
  - mayor dignidad
  - cercania con familia y mascotas
  - menor ansiedad y depresion asociadas al ingreso

### Carga del cuidador

- Riesgos:
  - ansiedad
  - alteracion del sueno
  - carga de vigilancia
  - descuido del autocuidado
  - ocultamiento del estres por temor a institucionalizacion
- Aceptabilidad poblacional:
  - `47.2%` considera aceptable el modelo
  - `16.6%` lo considera inaceptable por preocupacion de sobrecarga familiar
- Delimitacion obligatoria:
  - `ADL` y soporte emocional = rol del cuidador
  - vias IV, medicacion compleja, interpretacion de datos y decisiones = rol exclusivo del equipo clinico
- Soportes requeridos:
  - entrenamiento en dispositivos
  - planes de contingencia y primeros auxilios
  - centro de comando `24/7`
  - videoconferencia o contacto de un solo toque
  - `Zarit Burden Interview` para monitoreo de sobrecarga

### Consideraciones culturales

- Integrar valores que priorizan el cuidado familiar
- Mitigar resistencia a la impersonalidad tecnologica
- Hallazgos referidos en comunidades asiaticas y latinas
- Presentar apoyos y tecnologia como complemento del cuidado familiar, no como reemplazo

### Equidad, diversidad y acceso en areas rurales

#### Contexto estructural

- `14%` de la poblacion de EE. UU. vive en areas rurales
- `23%` reporta el acceso a salud como problema mayor
- tiempo medio hacia hospital fisico: `34` minutos
- mas de `150` hospitales rurales cerrados desde `2010`

#### Resultados de equidad

- No se observan diferencias estadisticamente significativas en:
  - mortalidad
  - escalamiento
  - readmision
  - entre grupos etnicos o raciales historicamente marginados
- Pacientes con discapacidad o elegibilidad dual:
  - resultados comparables a hospital fisico
- Beneficio adicional:
  - el hogar permite detectar `SDOH` ocultos durante una hospitalizacion convencional

#### Ruralidad y hospitales de acceso critico

- Aceptabilidad:
  - rechazo urbano previo hasta `63%`
  - rechazo rural `31%`
  - satisfaccion superior al `90%` en sistemas como Marshfield Clinic
- Resultados:
  - paridad clinica y de costos frente a hospital fisico
  - pacientes rurales menos sedentarios y mas activos
- Adaptaciones necesarias:
  - medicina predominantemente remota tras evaluacion inicial
  - apoyo presencial de enfermeria o `MIH`
  - traslado intermitente al hospital para imagenes avanzadas o accesos complejos cuando sea necesario

## Barreras estructurales de implementacion

### Resistencia cultural, profesional y medico-legal

- Barrera central:
  - percepcion de que el hogar es clinicamente inferior al hospital fisico
- Foco de resistencia:
  - medicos de urgencias
  - especialistas derivadores
- Causas:
  - temor a deterioro subito fuera del hospital
  - mayor carga de decision y coordinacion en urgencias
  - ambiguedad sobre responsabilidad legal en `RPM`
  - preocupacion por mala praxis y cobertura de seguro
- Mitigaciones:
  - presentar HaH como unidad hospitalaria integrada, no como servicio domiciliario ambulatorio
  - demostrar cobertura `24/7` y algoritmos claros de escalamiento
  - retroalimentar resultados del programa en reuniones clinicas
  - generar publicaciones e informes internos
  - incorporar formacion sobre medicina aguda en el hogar en pregrado y residencia

### Integracion de flujos de trabajo

- Cuellos de botella:
  - identificar candidatos a tiempo
  - explicar modelo a la familia
  - coordinar transicion en entornos de urgencias saturados
- Hallazgo operativo:
  - el compromiso del medico de urgencias es el factor mas critico
- Mitigaciones:
  - estrategias `push-pull`
  - alertas automatizadas e `IA` en el `EHR`
  - rol de navegador clinico para recibir referencias y asumir la coordinacion
- Carga de coordinacion:
  - red fragmentada de proveedores
  - cientos de domicilios unicos
  - dependencia de `ultima milla`
- Dato anclado:
  - hasta `20.5%` del tiempo fuera de las visitas puede destinarse a coordinacion no reembolsable
- Ecosistema hibrido:
  - comunicacion en tiempo real entre centro virtual y equipo presencial
  - reglas estrictas sobre que alerta exige visita, ajuste remoto o escalamiento medico
  - interoperabilidad bidireccional `RPM` + logistica + `EHR`

### Brecha digital, alfabetizacion e idioma

- Riesgos:
  - falta de banda ancha
  - conectividad celular insuficiente
  - baja alfabetizacion digital
  - baja literacidad en salud
  - barreras idiomaticas
- Mitigaciones de infraestructura:
  - no depender de internet del paciente
  - kits con conectividad celular integrada
  - `hotspots`
  - dispositivos sin costo para el paciente
- Mitigaciones de usabilidad:
  - equipos de un solo toque o `plug-and-play`
  - herramientas por voz para discapacidad visual o motora
  - `onboarding` estructurado para paciente y cuidador
  - soporte tecnico continuo
- Mitigaciones idiomaticas:
  - software e instrucciones multilingues
  - personal multilingue en centro de comando
  - interpretacion simultanea `24/7`
  - soporte de lengua de senas
  - confirmacion por `teach-back`

## Perspectivas 2026-2030

### Inpatient-at-Home

- Evolucion:
  - elimina dependencia estructural del departamento de urgencias
  - desplaza el triaje aguas arriba hacia comunidad y atencion primaria
- Mecanismo:
  - el paciente es evaluado in situ por `PCP` o equipos moviles
  - si requiere nivel hospitalario, ingresa directo a HaH
  - sin cruzar las puertas del hospital
- Requisitos para APS y grupos medicos:
  - acceso `24/7`
  - triaje de descompensaciones complejas
  - logistica expedita de laboratorio e imagen portatil
  - entrega oportuna de tratamientos agudos
  - personal para visitas domiciliarias de alto contacto
- Barrera financiera:
  - HaH hospitalario retiene ingresos `DRG` superiores a `\$8,000` por episodio
  - `IAH` puro sustituye eso por honorarios profesionales cercanos a `\$717`
- Implicacion:
  - su expansion depende del crecimiento de `VBC`, capitacion y riesgo compartido

### Innovacion biomedica y analitica

- Evolucion esperada:
  - de monitorizacion fisiologica a monitorizacion bioquimica en tiempo real
  - biosensores portatiles
  - `lab-on-a-patch`
  - marcadores metabolicos
  - `IA` predictiva

### Ecosistema ampliado de atencion en hogar

- Horizonte:
  - hasta `25%` de la atencion posaguda y a largo plazo podria entregarse en domicilio
- Verticales proyectadas:
  - quimioterapia domiciliaria
  - `SNF-at-home`
  - rehabilitacion intensiva en el hogar
  - paliativos domiciliarios avanzados
- Fundamentos operativos:
  - reutiliza `RPM`
  - reutiliza logistica de ultima milla
  - permite transicion continua sin cambiar de entorno fisico
- Oncologia:
  - menor exposicion a patogenos nosocomiales
  - deteccion temprana de neutropenia febril o sepsis con monitorizacion continua
- Paliativos:
  - proyeccion demografica `2050`: `1` de cada `6` personas tendra `65` anos o mas
  - cerca de `80%` de adultos mayores vive con `2` o mas enfermedades cronicas
  - `advance care planning` en los primeros `30` dias facilita transicion oportuna a hospicio
- Sinergia organizacional:
  - portafolio combinado `HaH` + `SNF-at-home` + rehabilitacion + paliativos
  - alineacion directa con `ACO` y `bundled payments`

## Tesis operativa del manual

- `HaH` no es simplificacion de cuidados domiciliarios; es extension de hospitalizacion aguda al hogar.
- La fidelidad del modelo depende de:
  - elegibilidad estricta
  - centro de comando virtual `24/7`
  - minimo `1` evaluacion diaria de alto nivel + `2` visitas presenciales
  - logistica de ultima milla robusta
  - interoperabilidad auditable
  - capacidad de escalamiento rapido al hospital fisico
