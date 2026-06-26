---
_manifest:
  urn: "urn:salud:kb:hodom-situacion-chile-2026"
  provenance:
    created_by: "Codex"
    created_at: "2026-03-10"
    source: "source/pro/hodom/situacion-hodom-chile-2026.md"
version: "1.0.1"
status: published
tags: [hodom, hospitalizacion-domiciliaria, chile, salud-publica, analisis-situacional]
lang: es
extensions:
  kora:
    family: generic
---

# Situacion de la Hospitalizacion Domiciliaria en Chile 2024-2026

## 1. Resumen ejecutivo

### 1.1 Sintesis de situacion actual

- La hospitalizacion domiciliaria (`HD`) paso de contingencia SARS-CoV-2 a pilar estructural de alta complejidad `2024-2026`.
- Opera como alternativa a la atencion cerrada:
  - cuidados de rango hospitalario en domicilio
  - equivalencia funcional en calidad y cantidad
  - equipo multiprofesional
  - monitorizacion e intervenciones complejas
- Valor sistemico central:
  - optimizacion de cama fisica
  - evitacion de ingreso
  - alta precoz
  - menor exposicion a infecciones intrahospitalarias
- Soporte normativo clave:
  - `DS N° 1/2022`
  - Norma Tecnica `2024` para establecimientos de HD
  - Norma Tecnica `N° 243` de mayo `2025`
- La HD se consolida como proceso transversal de red:
  - Hospitales Comunitarios
  - Hospitales Provinciales
  - Hospitales Regionales o Institutos
- Cobertura asistencial potencial:
  - adultos
  - pediatria
  - salud mental
  - ginecoobstetricia
  - cuidados paliativos

### 1.2 Hallazgos epidemiologicos, operativos y financieros

#### Hallazgos epidemiologicos

- Presion asistencial por:
  - envejecimiento poblacional acelerado
  - aumento de enfermedades cronicas no transmisibles
  - mayor costo tecnologico de terapias
  - amenaza persistente de eventos epidemicos o desastres
- Deficit estructural en atencion cerrada:
  - `2` a `2.1` camas por `1.000` habitantes en Chile
  - `4.7` camas por `1.000` habitantes en OCDE
- Brecha de recurso humano:
  - `2.5` medicos por `1.000` habitantes en Chile vs `3.5` OCDE
  - `2.7` enfermeras por `1.000` habitantes en Chile vs `8.8` OCDE
- Perfiles clinicos frecuentes en HD:
  - infecciones agudas con terapia endovenosa
  - cronicos descompensados
  - pacientes terminales subsidiarios de paliativos `GES-4`

#### Hallazgos operativos

- Produccion nacional DEIS:
  - `70.687` pacientes atendidos en `2019`
  - `166.707` pacientes atendidos en `2024`
  - crecimiento: `135%`
- Produccion `2024`:
  - mas de `1.4` millones de dias-cama HD
  - equivalencia diaria: `3.923` camas virtuales
- Evidencia local `SSMOc`:
  - ocupacion promedio: `91%`
  - reingreso a hospitalizacion tradicional: `4.1%`
  - distribucion `2024`: `50%` de atenciones complejas
- Lectura:
  - la HD ya maneja casuistica de alta demanda de recursos
  - valida su rol como extension autentica de atencion cerrada

#### Hallazgos financieros

- Sector publico:
  - transicion progresiva a `GRD`
  - proyeccion `2026`: `80` hospitales bajo ese esquema
  - ventaja: menor estancia intrahospitalaria y mejor eficiencia por egreso equivalente
- Innovacion publica `2024-2025`:
  - `MCC`
  - Norma Tecnica `N° 238`
  - codigo `0201408`: "Dia Cama de Hospitalizacion Domiciliaria de Baja Complejidad"
- Sector privado:
  - cobertura via planes complementarios
  - `CAEC` generalmente excluye HD
  - excepciones calificadas restringidas por Superintendencia de Salud

### 1.3 Recomendaciones estrategicas

1. Integracion sociosanitaria obligatoria entre unidades HD, `Chile Cuida` y programa domiciliario `SENAMA`.
2. Mitigacion de brecha territorial con telemedicina, `Hospital Digital` y destinacion de `PAO` a zonas aisladas.
3. Escalamiento nacional de georreferenciacion dinamica, FHIR, fichas moviles e `IoT`.
4. Validacion multicentrica de un score nacional de complejidad para alinear lenguaje clinico y financiamiento.

## 2. Contexto epidemiologico y estructural del sistema de salud

### 2.1 Transicion demografica y carga de cronicidad

- El sistema de salud chileno enfrenta aumento persistente de costos por:
  - transicion epidemiologica
  - transicion demografica
  - avance tecnologico terapeutico
- Marco poblacional descrito por `OMS` y `OPS`:
  - envejecimiento acelerado
  - determinantes socioeconomicos estructurales
  - mayor carga de morbimortalidad por cronicos no transmisibles
  - persistencia de amenazas infecciosas con potencial epidemico
- Efecto sanitario:
  - presion sostenida sobre camas cerradas
  - necesidad de respuestas mas complejas y prolongadas
  - exigencia de mecanismos alternativos para atencion intrahospitalaria

### 2.2 Deficit historico de camas hospitalarias

| Indicador                         | Chile       | OCDE  | Lectura                    |
| --------------------------------- | ----------- | ----- | -------------------------- |
| Camas por `1.000` habitantes      | `2` a `2.1` | `4.7` | Deficit estructural        |
| Medicos por `1.000` habitantes    | `2.5`       | `3.5` | Brecha profesional         |
| Enfermeras por `1.000` habitantes | `2.7`       | `8.8` | Brecha mayor en enfermeria |

- Dotacion aproximada de camas:
  - total pais: `37.548`
  - publicas: `24.983` (`67%`)
  - privadas: `12.565` (`33%`)
- Distribucion territorial desigual:
  - en `RM`, casi `50%` de la dotacion se concentra en privado
  - fuera de `RM`, la participacion privada baja a `21%`
  - en Aysen, disponibilidad privada puede ser `0%`
- Estres sociosanitario ejemplificado en `SSMOc`:
  - inicio `2021`: `1.1` camas por `1.000` habitantes
- Lectura:
  - margen operativo entre camas demandadas y camas liberadas es estrecho
  - la HD emerge como via alternativa impostergable

### 2.3 Evolucion del modelo HD

- La HD se expandio en pandemia como estrategia de emergencia:
  - evitar colapso de urgencias y unidades criticas
  - expandir virtualmente capacidad instalada
  - abrir unidades en hospitales que no las tenian
- Con el cierre de la urgencia pandemica, la HD paso a modelo estructural.
- Dos logicas operativas dominantes:
  - evitacion de ingreso
  - alta precoz
- Beneficios directos:
  - mejor experiencia y recuperacion del paciente
  - menor exposicion a infecciones y complicaciones intrahospitalarias
  - mejora de eficiencia hospitalaria
- Prueba estadistica:
  - crecimiento nacional `135%` entre `2019` y `2024`

## 3. Marco regulatorio y normativo vigente

### 3.1 Definicion tecnico-juridica

- La HD es modalidad asistencial alternativa a la hospitalizacion tradicional.
- Requisito juridico central:
  - si HD no existiera, el paciente habria requerido internacion hospitalaria
- Diferencia estructural frente a atencion domiciliaria basica:
  - indicacion medica estricta
  - control medico diario
  - alta medica formal del episodio
- Poblaciones definidas:
  - paciente agudo
  - paciente cronico reagudizado
- Condicion clinica exigida:
  - estabilidad suficiente para manejo seguro en domicilio

### 3.2 `DS N° 1/2022` del MINSAL

- Primer reglamento especifico para establecimientos, unidades o servicios de HD.
- Aplica a prestadores publicos y privados.
- Ejes:
  - continuidad de la atencion
  - estandares de tratamiento y seguimiento
  - recurso humano calificado
  - gobernanza clinica especializada
- Exigencias criticas:
  - direccion tecnica a cargo de medico cirujano
  - postitulo o postgrado en gestion en salud
  - curso `IAAS` de al menos `80` horas
  - permanencia minima: `22` horas semanales
- Coordinacion operativa:
  - profesional de salud; enfermeria como perfil predominante en la fuente
  - experiencia minima: `5` anos
  - competencias en gestion sanitaria
  - `RCP/DEA`
  - `IAAS`

### 3.3 Norma Tecnica para establecimientos de HD (`2024`)

- Operativiza el `DS N° 1/2022`.
- Fija requisitos minimos de:
  - infraestructura
  - equipamiento
  - procesos
  - trazabilidad
- Exigencias de unidad base:
  - dependencias administrativas y logisticas
  - sistema telefonico o radial con grabacion continua o registro auditable
  - soporte informatico
  - respaldo electrico
  - area transitoria para `REAS`
  - bodega con control de temperatura y cadena de frio
- Equipamiento movil minimo:
  - presion arterial
  - frecuencia cardiaca
  - frecuencia respiratoria
  - saturacion de oxigeno
- Protocolos obligatorios:
  - evaluacion e ingreso
  - programacion de rutas vehiculares
  - contingencia por descompensacion
  - agresiones al equipo de salud

### 3.4 Norma Tecnica `N° 243` de mayo `2025`

- Reordena la taxonomia hospitalaria:
  - primer nivel: Hospitales Comunitarios
  - segundo nivel: Hospitales Provinciales
  - tercer nivel: Hospitales Regionales o Institutos
- La HD pasa a ser proceso asistencial transversal.
- Disponible en los tres niveles de atencion.
- Opera como extension in situ del hospital.
- Polivalencia estructural:
  - integra especialidades y subespecialidades segun cartera del hospital base
- Areas explicitamente abarcables:
  - adultos
  - pediatria
  - ginecoobstetricia
  - salud mental
  - cuidados paliativos

### 3.5 Derechos, deberes y datos sensibles

- `Ley N° 20.584`:
  - consentimiento informado expreso y firmado
  - entrega de carta de derechos y deberes
  - informacion sobre mecanismo formal de reclamos
  - habilitacion de resumen clinico fisico o digital en domicilio
- El resumen clinico debe contener:
  - diagnosticos
  - planes terapeuticos
  - telefonos de emergencia
- `Ley N° 19.628`:
  - ficha clinica, diagnosticos y tratamientos domiciliarios son datos sensibles
- Deber del prestador:
  - sistemas encriptados e interoperables
  - registro en tiempo real por equipo en terreno
  - acceso oportuno para continuidad del cuidado
  - proteccion frente a terceros no autorizados
- Custodia medico-legal:
  - la ficha clinica debe resguardarse por al menos `15` anos
  - no exige duplicados si ya existen informes originales de procedimientos

## 4. Criterios de elegibilidad y modelo operativo

### 4.1 Criterios clinicos de inclusion

- Dirigido a pacientes que requieren cuidados de rango hospitalario sin riesgo vital inminente.
- Incluye:
  - cuadros agudos
  - cuadros subagudos
  - cronicos reagudizados
- Condicion obligatoria:
  - estabilidad clinica
  - equilibrio de funciones vitales
- Requisitos de ingreso:
  - diagnostico medico definido
  - plan terapeutico acotado y cuantificable
- Estada tipica:
  - promedio `5` a `10` dias
  - maximo operativo citado: `30` dias
- Perfiles frecuentes:
  - infecciones respiratorias
  - infecciones urinarias
  - infecciones de tejidos blandos
  - `EPOC`
  - insuficiencia cardiaca
  - diabetes descompensada
  - postquirurgicos
  - paliativos de fin de vida
- Patron frecuente de complejidad hospitalaria: `2` o mas intervenciones activas
  - terapia intravenosa o subcutanea diaria
  - kinesioterapia motora o respiratoria
  - oxigenoterapia
  - curaciones avanzadas
  - ajuste diario de farmacos

### 4.2 Criterios sociales de inclusion

- Factor mas restrictivo frecuente: soporte psicosocial.
- Requisito insoslayable:
  - red familiar
  - red comunitaria
  - o tutor responsable
- El cuidador informal opera como co-terapeuta.
- Debe poder:
  - comprender instrucciones
  - administrar medicamentos por via oral
  - vigilar cambios de temperatura o conciencia
  - contactar al equipo frente a descompensacion
- Exigencia etica y normativa:
  - consentimiento informado del paciente o representante

### 4.3 Entorno domiciliario

- El hogar asume funcion de unidad clinica terapeutica.
- Debe cumplir condiciones minimas de:
  - saneamiento
  - habitabilidad
  - limpieza
  - ventilacion
  - ausencia de riesgos estructurales
- Servicios basicos obligatorios:
  - agua potable
  - energia electrica
- Conectividad obligatoria o progresiva:
  - acceso telefonico operativo
  - internet para telemedicina y telemonitorizacion
- Restriccion geografica:
  - domicilio dentro del radio de cobertura y factibilidad de acceso del prestador

### 4.4 Exclusiones absolutas

- En esfera clinica:
  - inestabilidad
  - ausencia de diagnostico claro
  - ausencia de plan terapeutico definido
  - cirugia mayor exclusiva de recinto
  - vigilancia intensiva continua
  - monitorizacion hemodinamica invasiva
  - patologias psiquiatricas severas descompensadas
  - dolor cronico dificil sin patologia aguda corregible
  - insuficiencias organicas terminales fuera de capacidad del equipo
  - nivel de estabilidad tan alto que corresponderia manejo ambulatorio
- En esfera social:
  - ausencia de cuidador efectivo
  - ausencia de red de apoyo
  - negativa a firmar consentimiento
  - no adherencia de paciente o tutor
  - incumplimiento de condiciones sanitarias
  - incumplimiento de condiciones electricas
  - domicilio fuera de cobertura geografica

## 5. Indicadores de produccion y gestion clinica `2019-2024`

### 5.1 Evolucion del volumen asistencial

| Ano    | Pacientes atendidos | Lectura                     |
| ------ | ------------------- | --------------------------- |
| `2019` | `70.687`            | Base pre consolidacion      |
| `2024` | `166.707`           | Modelo estructural nacional |

- Fuente:
  - `DEIS`
  - `REM`
- Crecimiento del periodo: `135%`.

### 5.2 Impacto en gestion de camas

- Produccion `2024`:
  - mas de `1.4` millones de dias persona atendidos
- Formula:
  - `dias persona atendidos / 365`
- Resultado:
  - `3.923` camas virtuales diarias
- Significado sanitario:
  - capacidad equivalente de multiples hospitales de alta complejidad
  - menor costo operacional
  - menor riesgo de infeccion intrahospitalaria

### 5.3 Score de categorizacion de complejidad

- Experiencia destacada: `SSMOc`.
- Variables consideradas:
  - visitas clinicas
  - procedimientos invasivos
  - vias venosas
  - sondas
  - oxigenoterapia
- Niveles:
  - basico: `0` a `2`
  - intermedio: `3` a `5`
  - complejo: `6` o mas
- Distribucion `2018`:
  - `39%` basico
  - `31%` intermedio
  - `30%` complejo
- Distribucion `2024`:
  - `9%` basico
  - `42%` intermedio
  - `50%` complejo
- Lectura:
  - aumento objetivo de agudeza
  - validacion de HD como extension de atencion cerrada

### 5.4 Eficacia y seguridad clinica

- Reingreso a hospitalizacion tradicional en `SSMOc` `2018-2024`:
  - `4.1%`
  - `41` pacientes por cada `1.000`
- Variacion segun hospital base:
  - `2±2` a `6±1` reingresos
- Mortalidad intra-programa del periodo:
  - `3.683` fallecimientos
  - `5%` del total de personas atendidas
- Lectura:
  - perfil epidemiologico mixto
  - incluye agudos, cronicos reagudizados y paliativos

### 5.5 Dias de estada y flujo desde urgencias

- Pilares operativos:
  - evitacion de ingreso
  - alta precoz
- Promedio de estada en redes como `SSMOc`:
  - `11±3` dias
- Ocupacion promedio de plazas HD:
  - `91%±3`
- Correlacion:
  - menor hospitalizacion prolongada en urgencias
  - mejor ciclado de pacientes
  - mejora costo-efectiva de eficiencia global

## 6. Recursos humanos, infraestructura y bioseguridad

### 6.1 Direccion tecnica

- Debe ser medico cirujano.
- Requisitos:
  - experiencia clinica minima de `2` anos
  - postitulo o postgrado en gestion en salud
  - curso `IAAS` de al menos `80` horas
  - vigencia `IAAS`: `5` anos
  - `RCP` basica y uso de desfibrilador
- Permanencia presencial minima:
  - `22` horas semanales
- Debe existir reemplazante formal con los mismos requisitos minimos.

### 6.2 Coordinacion operativa

- Recae en profesional de la salud; enfermeria como perfil predominante en la fuente.
- Requisitos:
  - experiencia clinica minima de `5` anos
  - formacion en gestion en salud
  - curso `IAAS` de `80` horas
  - soporte vital basico
- Funciones de hecho:
  - gestion diaria del flujo de pacientes
  - asignacion de rutas
  - articulacion del equipo
  - educacion continua al grupo familiar
  - trazabilidad de indicaciones

### 6.3 Especializacion del equipo multiprofesional

- Todo el personal debe:
  - estar habilitado legalmente
  - estar inscrito en Superintendencia de Salud cuando corresponda
- Induccion institucional obligatoria:
  - minimo `44` horas
  - componentes teoricos y practicos
- Exigencias especificas:
  - HD pediatrica y psiquiatrica:
    - medico especialista respectivo
    - o medico general con `2` anos demostrables en servicios afines
  - rehabilitacion motora y respiratoria:
    - kinesilogos con `2` anos de experiencia
    - entrenamiento en soporte vital basico
    - manejo de secreciones, oxigenoterapia y rehabilitacion precoz

### 6.4 Riesgos, `REAS` y emergencias

- `REAS`:
  - manual de recepcion, manejo, retiro y eliminacion
  - ajuste a `DS N° 6/2009`
  - bodega con control de temperatura
  - cadena de frio
  - disposicion transitoria de residuos clinicos
- Bioseguridad:
  - mismas precauciones estandar y de aislamiento que atencion cerrada
- Prevencion de eventos adversos:
  - instruccion al cuidador
  - adaptacion del entorno
  - prevencion de caidas
  - prevencion de ulceras por presion
  - barandillas laterales
  - iluminacion nocturna adecuada
  - higiene y lubricacion de piel
- Respuesta a emergencias:
  - protocolo de actuacion ante emergencia clinica
  - comunicacion telefonica o radial continua con grabacion
  - rescate medico y derivacion inmediata
  - ambulancias propias o alianzas privadas
  - articulacion con `SAMU` en red publica
- Seguridad del personal:
  - protocolo de actuacion frente a agresiones al equipo de salud

## 7. Arquitectura financiera, mecanismos de pago y aseguramiento

### 7.1 Sistema publico (`FONASA`)

#### 7.1.1 Financiamiento tradicional `MAI`

- Historicamente, la HD publica se financia via `MAI`.
- Cobertura sin copago:
  - tramos `A` y `B`
  - personas mayores de `60` anos
- Limitacion:
  - presupuesto historico centralizado refleja mal el aumento de volumen y agudeza
- Riesgo:
  - tension sobre sostenibilidad de unidades de alta complejidad

#### 7.1.2 Transicion a `GRD`

- Proyeccion `2026`:
  - `80` hospitales bajo `GRD`
- Incorporaciones recientes citadas:
  - Traiguen
  - Puerto Aysen
  - Penaflor
  - Ancud
- `GRD` relaciona tipo de paciente y consumo real de recursos via Peso Relativo.
- Rol estrategico de HD:
  - reduce estancia media intrahospitalaria
  - favorece alta precoz para completar tratamiento en domicilio
  - evita `Outliers Superiores`
  - promueve `Inliers` u `Outliers Inferiores`
  - optimiza pago por egreso equivalente
  - libera cama fisica para demanda de urgencia

#### 7.1.3 `MCC` y codigo `0201408`

- Cambio regulatorio mas trascendental:
  - `MCC`
  - Ley `N° 21.674`
  - Norma Tecnica `N° 238`
- Poblacion objetivo:
  - afiliados `FONASA` tramos `B`, `C` y `D`
  - prima complementaria voluntaria
- Arancel incorporado:
  - codigo `0201408`
  - "Dia Cama de Hospitalizacion Domiciliaria de Baja Complejidad"
- Prestacion integral incluida:
  - visita medica
  - enfermeria
  - kinesiologia
  - insumos
  - medicamentos generales de estabilizacion
- Efectos:
  - menor gasto de bolsillo
  - incentivo a oferta privada de cupos HD
  - alivio de saturacion publica

### 7.2 Sistema privado (`ISAPRES`)

#### 7.2.1 Bonificaciones y auditoria de pertinencia

- La cobertura depende del contrato complementario del afiliado.
- La mayoria de las Isapres bonifica HD si:
  - es alternativa real a hospitalizacion convencional
  - existe pertinencia clinica documentada
- Hay auditoria medica estricta para validar equivalencia en calidad e intensidad.

#### 7.2.2 Restriccion `CAEC`

- La `CAEC` financia `100%` del gasto tras superar deducible.
- Regla general:
  - la atencion y hospitalizacion domiciliaria esta excluida "en todas sus formas"

#### 7.2.3 Excepciones calificadas `CAEC`

- Base:
  - Circular `IF N° 7`
- Requisitos copulativos:
  1. Hospitalizacion convencional previa con necesidad de continuidad de tratamiento activo.
  2. Medico tratante prescriptor distinto e independiente del supervisor o director tecnico del prestador HD.
  3. Autorizacion y derivacion formal de la Isapre a prestador de su red `CAEC`.
- Finalidad regulatoria:
  - evitar riesgo moral
  - impedir financiamiento de cuidados cronicos de larga data
  - impedir residencias geriatricas encubiertas
  - impedir enfermeria basica bajo seguro catastrofico

### 7.3 Presupuesto fiscal `2026`

- Respaldo macro:
  - aumento real del presupuesto MINSAL: `5.6%`
  - partida superior a `30` billones de pesos
  - aumento acumulado desde `2022`: `30%`
- En `PPI`, el presupuesto impacta capacidad instalada y resolutiva HD.
- Glosas destacadas:
  - Plan de Normalizacion Presupuestaria
  - financiamiento protegido para dias cama
  - ventilacion domiciliaria
- Impacto:
  - soporte a pacientes cronicos complejos
  - soporte a electrodependientes
  - financiamiento estatal de insumos y monitorizacion
  - liberacion de cupos `UCI`

## 8. Rol del sector privado y prestadores independientes

### 8.1 Evolucion de la oferta privada especializada

- El sector privado transito desde enfermeria basica a manejo de:
  - alta complejidad
  - mediana complejidad
  - baja complejidad
- Incorporo:
  - tecnologias avanzadas
  - monitorizacion remota
  - equipos multidisciplinarios
- Prestadores destacados:
  - `Home Medical Clinic`:
    - mas de `25` anos de experiencia
    - mas de `27.000` pacientes atendidos
    - ficha electronica en domicilio conectada `24/7` a Central de Enfermeria
    - unidad pediatrica intensiva `Medical Hilfe`
    - alianza de rescate con `HELP S.A.`
  - `GrupoSalud CHBS`:
    - cobertura nacional
    - equipos medicos en todas las capitales regionales
    - implementacion en hasta `4` dias habiles
    - oferta para terminales, ventilacion y clinica neurologica domiciliaria
    - foco en `ACV`, `TEC` y lesiones medulares
  - `Clinica Universidad de los Andes`:
    - extension directa de centro institucional privado
    - pionera en Chile
    - foco postquirurgico y medico en `RM`
    - comunas citadas:
      - Las Condes
      - Lo Barnechea
      - Vitacura
    - estada promedio: `10` dias
    - maximo: `30` dias
    - exclusion de salud mental descompensada y dependencia severa sin cuidador
  - `Domihealth`:
    - foco en adulto mayor
    - patologias respiratorias y geriatricas
    - demencia
    - `EPOC`
    - radiografias portatiles, ecografias y Doppler en domicilio

### 8.2 Reputacion corporativa y estandares de calidad

- Referencia externa:
  - Ranking `Merco Salud Chile 2025`
  - auditoria `KPMG`
- Metodologia:
  - combina indicadores objetivos de desempeno clinico
  - percepcion de medicos, directivos y equipos de salud
- Hallazgos citados:
  - Clinica Alemana de Santiago lider en `18` servicios clinicos
  - ortopedia y traumatologia como servicios con alta derivacion a HD postquirurgica
  - reconocimiento a red `Clinicas RedSalud`
  - centros destacados:
    - Clinica RedSalud Elqui
    - Clinica RedSalud Mayor Temuco
- Lectura:
  - reputacion y calidad importan como nodos derivadores hacia HD

### 8.3 Alianzas estrategico-publicas

- La falta de camas publicas vuelve a los privados socios estrategicos del Estado.
- Mecanismos:
  - licitaciones
  - compras estrategicas
  - descompresion de hospitales
  - apoyo a listas de espera
- Ley de Presupuestos `2026`:
  - glosa de continuidad por mas de `$57.804` millones
  - destino:
    - prestaciones `NO GES`
    - Sistema de Acceso Priorizado (`SAP`)
  - compra estimada:
    - aproximadamente `15.000` cirugias al sector privado
- Tras cirugias mayores, la HD privada absorbe manejo postoperatorio temprano.
- `MCC` y codigo `0201408` consolidan financieramente esta alianza.
- En oncologia `GES-4`:
  - privados cumplen rol de soporte vital
  - ejemplo citado: `Oncovida`
  - prestaciones:
    - analgesia compleja
    - hidratacion parenteral
    - soporte multidisciplinario
  - inicio garantizado:
    - maximo `5` dias desde confirmacion diagnostica

## 9. Salud digital, interoperabilidad y logistica clinica

### 9.1 Telemedicina y telemonitorizacion

- Proyeccion `2026`:
  - la telemedicina podria representar casi `30%` de las interacciones sanitarias
- Base tecnologica:
  - `IoT`
  - wearables
  - fichas clinicas electronicas moviles
- Variables monitorizables:
  - frecuencia cardiaca
  - saturacion de oxigeno
  - presion arterial
  - deteccion de caidas
- Los datos viajan en tiempo real y permiten evaluacion:
  - asincronica
  - sincronica
- En `MCC`, codigo `0201408` ya incorpora:
  - teleconsultas medicas
  - teleconsultas de enfermeria
  - telerehabilitacion kinesiologica
- Referencia privada:
  - `Home Medical Clinic`
  - ficha electronica en domicilio conectada `24/7` a central de enfermeria

### 9.2 Logistica dinamica: piloto Hospital Sotero del Rio

- Uno de los principales cuellos de botella HD:
  - gestion del recurso humano en terreno
  - gestion de flota vehicular
- Caso citado:
  - Hospital Sotero del Rio
  - mas de `156.000` atenciones HD en `2024`
- Problema previo:
  - planificacion manual de rutas
  - menor adaptabilidad
  - mayor riesgo laboral
- Solucion piloto iniciada a fines de `2025`:
  - programa "Juegatela por la Innovacion e Impulsa el Cambio en Salud"
  - apoyo de `MINSAL`, `Corfo`, `CENS` y `Pro Salud Chile`
  - plataforma `Raylex`
- Variables integradas:
  - tiempo de desplazamiento
  - trafico
  - clima
  - seguridad de ruta
  - especialidad requerida
  - tipo de intervencion
- Resultado:
  - mayor visibilidad operativa
  - menor tiempo de traslado
  - mayor seguridad del equipo
  - cambio de paradigma escalable a `2026`

### 9.3 Interoperabilidad y `HL7 FHIR`

- Imperativo sanitario y legal:
  - HD debe comportarse como extension real del hospital
- Base normativa:
  - Norma Tecnica `N° 243`
  - `Ley N° 21.688` sobre interoperabilidad de fichas clinicas
- Exigencia:
  - profesionales de especialidad en `APS` y hospitales comunitarios deben acceder a ficha del hospital de referencia
- Eje tecnologico `2025-2026`:
  - soberania tecnologica
  - interoperabilidad bajo `HL7 FHIR`
- Beneficios:
  - acceso de equipos en terreno a antecedentes del paciente
  - registro en tiempo real desde dispositivos moviles
  - continuidad asistencial conectada
  - compatibilidad con resguardo de datos sensibles

### 9.4 Inteligencia Artificial

- Rol dual:
  - clinico
  - logistico
- En logistica:
  - asignacion y ajuste dinamico de rutas
  - maximizacion de atenciones por movil
- En clinica:
  - procesamiento de datos de wearables
  - analisis de tendencias y patrones
  - diagnostico predictivo de crisis respiratorias o cardiovasculares
  - alertas anticipadas a central de monitoreo
- Efecto:
  - ajustes terapeuticos en tiempo real
  - prevencion de traslados de urgencia y reingresos

## 10. Poblaciones especiales y continuidad socioclinica

### 10.1 Oncologia y cuidados paliativos

- La HD es entorno preferente para muerte digna y humanizada.
- Problema garantizado:
  - `GES N° 4`
  - "Alivio del dolor y cuidados paliativos por cancer avanzado"
- Cobertura:
  - cualquier edad
  - diagnostico confirmado
  - independiente del estadio clinico
- Oportunidad:
  - inicio maximo en `5` dias desde confirmacion diagnostica
- Proteccion financiera:
  - `FONASA`: `0%` copago
  - `Isapres`: `20%` copago
- Prestaciones:
  - analgesia compleja
  - opioides
  - hidratacion parenteral
  - insumos
  - examenes
  - equipo multiprofesional con medicos, enfermeras, psicologos y trabajadores sociales
- Enfoque:
  - control de sintomas
  - maxima calidad de vida
  - autonomia del paciente en rutinas, alimentacion y acompanamiento espiritual
- Tecnica recomendada al cuidador:
  - `COPE`
  - Creatividad
  - Optimismo
  - Planificacion
  - Informacion de Expertos
- El modelo incluye soporte estructurado al duelo.
- Riesgo priorizado:
  - prevenir duelo patologico si sintomas incapacitantes persisten mas alla de `6` meses

### 10.2 Geriatria y dependencia severa

- El envejecimiento eleva cronicos no transmisibles y dependencia funcional.
- El exito HD en geriatria depende del cuidador informal.
- Ausencia de red de apoyo efectiva:
  - exclusion absoluta
- Sinergia sociosanitaria requerida con `Chile Cuida`.
- Presupuesto `2026`:
  - Red Local de Apoyos y Cuidados: `$54.801` millones
  - crecimiento vs `2025`: `23.6%`
  - operacion garantizada de `100` Centros Comunitarios de Cuidados
- Continuidad de programa:
  - "Chile te Cuida"
  - foco en capacitacion y respiro de cuidadoras no remuneradas
- Programa Cuidados Domiciliarios `SENAMA`:
  - presupuesto `2026`: `$3.580` millones
  - crecimiento acumulado del ultimo cuatrienio: `94%`
  - poblacion objetivo:
    - personas de `60+`
    - dependencia moderada o severa
    - `60%` mas vulnerable del `RSH`
    - sin cuidador principal
- Impacto:
  - retrasa institucionalizacion
  - complementa intervenciones clinicas HD
  - ayuda a prevenir sindrome del cuidador

### 10.3 Infanto-juvenil

- La HD pediatrica exige mayor especializacion tecnica y logistica.
- Requisito normativo:
  - medico pediatra
  - o medico general con al menos `2` anos demostrables en servicios pediatricos cerrados
- Nicho privado ultra-especializado citado:
  - `Medical Hilfe` de `Home Medical Clinic`
- Prestaciones descritas:
  - infecciones respiratorias agudas estacionales
  - neurorehabilitacion pediatrica
  - ventilacion mecanica invasiva domiciliaria
- Rehabilitacion en infantes:
  - kinesilogos entrenados
  - aspiracion de secreciones
  - ajuste de parametros ventilatorios
- Rol del cuidador primario:
  - co-terapeuta permanente
  - capacitacion exhaustiva
  - certificacion informal en:
    - reanimacion basica
    - manejo de ostomias
    - administracion de farmacos intravenosos
- Si existe familiar en fase terminal:
  - se requiere orientacion psicologica adaptada al desarrollo del nino o adolescente
  - objetivo: prevenir ansiedad o depresion secundaria

## 11. Conclusiones, brechas y desafios estrategicos

### 11.1 Inequidad territorial

- Existe brecha estructural en distribucion de camas y servicios.
- Asimetria relevante:
  - `RM`: casi `50%` de camas privadas
  - resto del pais: `21%`
  - Aysen: `0%` camas privadas
- Extrapolacion al modelo HD:
  - zonas urbanas cuentan con HD publica y privada de alta complejidad
  - regiones rurales y extremas quedan mas limitadas a baja complejidad
- Brechas concretas:
  - neurorehabilitacion
  - cuidados intensivos pediatricos
  - ventilacion mecanica domiciliaria
- Respuesta propuesta en Presupuesto `2026`, Glosa `52`:
  - informe tecnico sobre formacion, retencion y distribucion de especialistas
  - fortalecimiento de `PAO`
  - uso intensivo de telemedicina especializada

### 11.2 Sobrecarga del cuidador informal

- La HD depende criticamente del cuidador principal.
- Su ausencia es exclusion absoluta.
- Riesgo:
  - claudicacion familiar
  - sindrome del cuidador
- Integracion sociosanitaria requerida con apoyo estatal formal.
- Base operativa y financiera ya consolidada en [-> 10.2 Geriatria y dependencia severa].
- Efecto esperado:
  - complementar HD
  - retrasar institucionalizacion
  - sostener viabilidad del cuidado de alta complejidad en hogar

### 11.3 Estandarizacion clinica nacional

- El score de complejidad `SSMOc` fue innovacion relevante.
- Pero sigue en fase inicial desde perspectiva de salud publica.
- Requiere:
  - validacion tecnica externa
  - estudios multicentricos
  - confiabilidad interobservador
  - sensibilidad a cambios clinicos
  - aplicabilidad en zonas rurales, sector privado y baja complejidad
- Correlaciones necesarias:
  - reingreso
  - mortalidad
  - dias de estada
- Finalidad:
  - definir dotacion minima
  - diferenciar financiamiento segun intensidad real de cuidados

### 11.4 Trazabilidad financiera bajo `GRD`

- La transicion `GRD` impactara `80` hospitales en `2026`.
- Nuevos recintos citados:
  - Traiguen
  - Puerto Aysen
  - Penaflor
  - Ancud
- Riesgo central:
  - subvaloracion de egresos HD
- Punto critico:
  - codificacion correcta del `CMBD`
  - `CIE-10`
  - `CIE-9MC`
  - marcador `POA`
  - diagnosticos secundarios
  - comorbilidades
  - procedimientos realizados en domicilio
- Consecuencia de mala trazabilidad:
  - desfinanciamiento de hospitales comunitarios
- Requerimiento estrategico:
  - integrar score de complejidad y sistemas de informacion `GRD`

### 11.5 Plan de accion gubernamental `2026-2030`

1. Transformacion digital y logistica clinica:
   - escalar georreferenciacion dinamica y asignacion algoritmica de rutas como el piloto del Hospital Sotero del Rio
2. Integracion de telemedicina y monitorizacion remota:
   - estandarizar wearables e `IA` para signos vitales y prediccion de descompensaciones
3. Fortalecimiento de cobertura financiera mixta:
   - potenciar `MCC`, codigo `0201408` y auditar excepciones `CAEC`
4. Interoperabilidad total de datos:
   - exigir `HL7 FHIR` y comunicacion bidireccional entre HD, `APS` y hospitales de referencia

## Anexo A. Fichas de indicadores `REM` para HD

### Ficha 1. Personas atendidas

- Indicador:
  - Personas Atendidas en HD
- Definicion:
  - total de pacientes atendidos en un periodo, incluyendo continuidad desde mes previo e ingresos del mes
- Fuente:
  - `DEIS`
  - `REM A21`, seccion `C`
- Utilidad:
  - mide cobertura real y evolucion longitudinal
- Hito:
  - `70.687` en `2019`
  - `166.707` en `2024`

### Ficha 2. Dias persona atendidos

- Indicador:
  - Dias Persona Atendidos
  - Dias Cama HD
- Definicion:
  - suma de dias de hospitalizacion domiciliaria consumidos por los pacientes del periodo
- Fuente:
  - `DEIS`
  - Manual `REM 2025-2026`
  - `REM A21`, seccion `C`
- Utilidad:
  - refleja carga asistencial directa territorial
- Dato `2024`:
  - `1.432.000` dias persona atendidos

### Ficha 3. Capacidad operativa equivalente

- Indicador:
  - Numero de Camas Estimadas
- Definicion:
  - estimacion de camas fisicas que la red habria debido disponer sin HD
- Formula:
  - `total de dias persona atendidos en el ano / 365`
- Dimension:
  - eficiencia y gestion de redes
- Resultado `2024`:
  - `3.923` camas virtuales diarias

### Ficha 4. Tasa de reingreso

- Indicador:
  - Porcentaje de reingresos a hospitalizacion tradicional
- Definicion:
  - proporcion de pacientes HD que requieren reingreso a cama cerrada
- Formula:
  - `(reingresos del ano / personas atendidas en HD del ano) * 100`
- Dimension:
  - eficacia
- Sentido:
  - descendente
- Referencia:
  - `4.1%` en redes exigentes como `SSMOc`

### Ficha 5. Intensidad del cuidado

- Indicador:
  - promedio de visitas domiciliarias efectuadas por equipo HD por paciente
- Definicion:
  - densidad de atenciones presenciales por episodio
- Formula:
  - `visitas totales del equipo HD / personas atendidas por la unidad`
- Dimension:
  - eficiencia
- Sentido:
  - ascendente
- Utilidad:
  - auditar si el programa sostiene estandar de rango hospitalario
- Referencia operativa citada:
  - promedio esperado aproximado: `13` visitas por caso

### Ficha 6. Indicadores complementarios locales

- Las orientaciones tecnicas exigen registro local continuo de:
  - porcentaje de ocupacion
  - promedio de dias de estada
  - numero de fallecidos no esperados
- Referencia de alta complejidad:
  - promedio de estada: `11±3` dias

## Anexo B. Consentimiento informado y protocolos de urgencia domiciliaria

### I. Modelo estructural de consentimiento informado

- La firma informada es requisito clinico y legal.
- La negativa a firmar excluye ingreso a HD.
- Dominios minimos:
  - identificacion del paciente:
    - nombre
    - `RUT`
    - fecha de nacimiento
    - domicilio exacto
    - prevision
  - identificacion del cuidador o tutor:
    - nombre
    - `RUT`
    - parentesco o relacion
  - declaracion de informacion clinica:
    - diagnostico principal
    - condicion actual
    - plan terapeutico
    - estada estimada
    - riesgos, beneficios y alternativas
  - compromisos del cuidador y paciente:
    - mantener habitabilidad, luz, agua y conectividad
    - presencia continua del cuidador
    - apoyo en medicamentos basicos
    - alerta precoz al equipo
    - autorizacion de ingreso del equipo clinico
  - certificacion de entrega normativa:
    - carta de derechos y deberes
    - mecanismo formal de reclamos
    - resumen clinico en domicilio con diagnosticos, evolucion breve, cuidados a seguir y telefonos de contacto para emergencia
  - firmas:
    - paciente
    - cuidador o tutor
    - profesional de ingreso
    - lugar, fecha y hora

### II. Protocolos de urgencia domiciliaria

#### 1. Emergencia clinica

- Sistema de alerta continua:
  - telefonico o radial
  - registro auditable de llamadas
  - fecha, hora, motivo, emisor y derivacion
- Triage y teleasistencia:
  - evaluacion de riesgo vital inminente
- Activacion de rescate medico:
  - traslado basico o avanzado a urgencias
  - hospitales comunitarios sin unidades criticas deben estabilizar transitoriamente con oxigenoterapia, soporte ventilatorio y farmacos de reanimacion hasta concretar traslado efectivo
- Manejo de caidas:
  - evaluacion de contusiones
  - riesgo de fractura
  - tecnicas seguras de levantamiento

#### 2. Adecuacion del esfuerzo terapeutico y ordenes de no reanimar

- Riesgo critico:
  - intervencion de urgencias externas en paliativos terminales
- Requisitos:
  - voluntades anticipadas o directrices medicas claras en ficha domiciliaria
  - evitar obstinacion terapeutica
  - coordinar informacion con `SAMU` o agencias de rescate
  - priorizar analgesia y confort sobre maniobras invasivas

#### 3. Agresiones al equipo de salud

- Riesgos:
  - violencia verbal
  - violencia fisica
  - presencia de armas
- Medidas:
  - evaluacion previa del entorno
  - mecanismos de escape y alerta
  - evacuacion inmediata si procede
  - georreferenciacion y monitoreo satelital de vehiculos

## Anexo C. Mapas de georreferenciacion y brechas territoriales

### 1. Fundamentacion metodologica y epidemiologica

- La georreferenciacion permite analizar:
  - distribucion geografica de oferta de camas
  - correlacion con demanda poblacional
  - accesibilidad al hospital base del cual depende HD
- El modelo espacial usa tres niveles de cobertura:
  - Cobertura `1`:
    - misma comuna del hospital base
  - Cobertura `2`:
    - comunas adyacentes
  - Cobertura `3`:
    - comunas no adyacentes o derivaciones distantes

### 2. Macro-gestion: brechas estructurales

- El mapa nacional confirma deficit historico:
  - `2.1` camas por `1.000` habitantes
- De `37.548` camas:
  - privado aporta `33%` (`12.565`)
- Desigualdad territorial:
  - `RM`: `50%` de dotacion en sector privado
  - resto del pais: promedio `21%`
  - Aysen: `0%` privado
- Lectura:
  - la carga asistencial recae en la red publica de macrozonas extremas
  - la HD debe asumir rol de soporte vital en atencion cerrada

### 3. Tipologia de cobertura territorial

Base metodologica: analisis cluster `K-Means` sobre `177` hospitales publicos.

| Clase | N     | Cobertura observada              | Lectura operativa                                                |
| ----- | ----- | -------------------------------- | ---------------------------------------------------------------- |
| `1`   | `32`  | `57.6%` local, `23.7%` adyacente | Alta y mediana complejidad urbana; radio domiciliario provincial |
| `2`   | `15`  | `64.4%` local, `23.6%` adyacente | Alta complejidad regional con mayor capacidad de derivacion a HD |
| `3`   | `112` | `81.9%` local                    | Hospitales Comunitarios; alta ruralidad; brecha de especialistas |
| `4`   | `4`   | Alta variabilidad                | Centros de referencia con gestion de altas a comunas distantes   |
| `5`   | `14`  | Muy alta variabilidad            | Referencia nacional, alta carga adyacente y no adyacente         |

- Clases `4` y `5`:
  - cobertura local minoritaria entre `41.2%` y `47.1%`
  - proporcion de pacientes adyacentes y no adyacentes hasta `16.5%`
- Lectura:
  - los Hospitales Comunitarios son frontera de atencion cerrada en zonas extremas
  - los centros de referencia requieren articulacion inter-redes y telecomunicaciones robustas

### 4. Micro-gestion y logistica clinica dinamica

- El piloto del Hospital Sotero del Rio muestra que mapas de isocronas y georreferenciacion en tiempo real son imperativos operativos.
- Variables integradas:
  - accesibilidad y trafico
  - condiciones climaticas
  - seguridad en ruta
  - distribucion espacial de pacientes
  - requerimiento de especialidad
  - score de complejidad
  - tipo de atencion
- Resultado:
  - reconfiguracion de rutas ante imprevistos
  - oportunidad asistencial
  - mayor integridad del personal clinico

### 5. Implicancias para planificacion y reduccion de brechas

1. Focalizar telemedicina sincronica y asincronica en los `112` hospitales de Clase `3`.
2. Priorizar `PAO` en macrozonas con baja densidad de camas y alta ruralidad.
3. Estandarizar georreferenciacion y coordinacion de traslados a nivel nacional con escalamiento del modelo `Raylex`/Sotero del Rio.

## Anexo D. Glosario de terminos tecnicos y acronimos

| Termino                                | Definicion compacta                                                                                                                                   |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CAEC`                                 | Cobertura adicional de `ISAPRES` para eventos de alto costo; por regla general excluye HD y solo admite excepciones calificadas con derivacion formal |
| `CMBD`                                 | Conjunto Minimo Basico de Datos; base de clasificacion del episodio y financiamiento bajo `GRD`; exige codificacion completa `CIE-10` y `CIE-9MC`     |
| `GES`                                  | Regimen legal de garantias explicitas; en HD destaca `GES-4` para alivio del dolor y cuidados paliativos por cancer avanzado                          |
| `GRD`                                  | Grupos Relacionados por el Diagnostico; mecanismo principal de pago por resolucion integral del episodio; en Chile usa familia `IR-GRD`               |
| `HD`                                   | Modalidad alternativa a atencion cerrada para pacientes agudos o cronicos reagudizados con cuidados hospitalarios en domicilio                        |
| `IAAS`                                 | Infecciones Asociadas a la Atencion de Salud; control critico en HD; direccion tecnica y coordinacion deben acreditar curso de `80` horas             |
| `Inliers` y `Outliers`                 | Clasificacion de duracion del episodio bajo `GRD`; `Outliers Superiores` generan carencias o deducibles perjudiciales                                 |
| `IoT` y wearables                      | Dispositivos conectados que transmiten constantes vitales a ficha clinica electronica para telemonitorizacion continua                                |
| `MCC`                                  | Modalidad de Cobertura Complementaria de `FONASA`; permite acceso a red privada definida mediante prima voluntaria e incluye arancel HD `0201408`     |
| Score de Categorizacion de Complejidad | Herramienta objetiva para clasificar atenciones HD en basicas, intermedias y complejas segun visitas, oxigenoterapia y procedimientos invasivos       |
