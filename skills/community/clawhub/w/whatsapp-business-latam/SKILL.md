---
name: whatsapp-business-latam
description: >
  Configuración completa de WhatsApp Business API (oficial Meta) para PyMEs de Argentina
  y LATAM. Actívate cuando el usuario mencione: WhatsApp Business, WA API, Meta Business
  Manager, webhook de WhatsApp, templates HSM, mensajes de WhatsApp automatizados,
  integrar WhatsApp con OpenClaw, configurar WhatsApp para el agente, o cuando pregunte
  cómo enviar mensajes de WhatsApp desde el agente. Cubre setup end-to-end, templates
  listos en español para los casos de uso más comunes de PyMEs (turnos, pagos, vencimientos,
  notificaciones), compliance para evitar bloqueos de cuenta, y guía de integración con
  openclaw.config.json. Solo API oficial de Meta — nunca librerías no oficiales.
version: 1.0.0
metadata:
  openclaw:
    emoji: "💬"
    requires:
      bins:
        - curl
      env: []
    always: false
    homepage: https://centriqs.io
---

# WhatsApp Business LATAM

Guía de configuración completa de la **WhatsApp Business API oficial de Meta** para PyMEs en Argentina y LATAM. Integración con OpenClaw, templates HSM en español, compliance, y guía anti-ban.

> ⚠️ **Solo API oficial.** Este skill cubre exclusivamente la API oficial de Meta (WhatsApp
> Business Platform). Nunca usar librerías no oficiales como Baileys, whatsapp-web.js,
> WPPConnect, o similares en producción — violan los Términos de Servicio de WhatsApp y
> resultan en baneo permanente del número. Ver sección "Anti-ban" al final.

---

## Comandos

```
wa setup                        # Guía de setup paso a paso desde cero
wa setup <paso>                 # Paso específico (ej: "wa setup meta-business")
wa template <tipo>              # Template HSM listo para copiar (ver lista abajo)
wa templates                    # Lista todos los templates disponibles
wa checklist                    # Checklist anti-ban completo
wa config                       # Muestra el bloque de config para openclaw.json
wa webhook                      # Instrucciones de configuración del webhook
wa test                         # Cómo enviar un mensaje de prueba con curl
wa compliance                   # Reglas de compliance Meta para no perder la cuenta
wa costos                       # Estimación de costos de la API para PyMEs argentinas
wa ayuda                        # Este menú
```

---

## Workspace

```
~/centriqs/whatsapp/
├── config.md           # Tokens, números, IDs (ver nota de seguridad)
├── templates/          # Templates HSM personalizados del usuario
│   └── aprobados.md    # Templates aprobados por Meta con sus IDs
└── logs/               # Log de envíos (opcional)
```

> 🔒 **Seguridad:** `~/centriqs/whatsapp/config.md` puede contener tokens de acceso.
> Asegurar que el directorio tenga permisos `chmod 700 ~/centriqs/whatsapp/`.
> Nunca compartir el contenido de este archivo en canales públicos o grupos.

### config.md — Completar durante el setup

```markdown
# Configuración WhatsApp Business API

## Credenciales (completar después del setup)
phone_number_id: ""          # ID del número en Meta Business Manager
whatsapp_business_account_id: ""  # WABA ID
access_token: ""             # Token de acceso permanente (System User)
webhook_verify_token: ""     # Token de verificación del webhook (elegido por vos)
app_id: ""                   # App ID en Meta for Developers

## Número
numero_whatsapp: ""          # Formato: +5491112345678
nombre_display: ""           # Nombre que verán los contactos

## Estado
cuenta_verificada: false     # true cuando Meta aprueba la cuenta de negocio
templates_aprobados: 0       # Cantidad de templates aprobados
```

---

## Setup completo — paso a paso

### Paso 1: Cuenta de Facebook Business (Meta Business Suite)

**Prerequisito obligatorio.** Si ya tenés una cuenta empresarial de Facebook/Meta, saltar al paso 2.

1. Ir a `business.facebook.com`
2. Crear cuenta de negocio con:
   - Nombre real de la empresa (no cambiar después — afecta la verificación)
   - Email empresarial (usar `hola@tudominio.com`, no Gmail personal)
   - País: Argentina (o el país del negocio)
3. Completar perfil de negocio: dirección, sitio web, categoría

> ⚠️ Usar datos reales del negocio. Las cuentas con datos falsos o inconsistentes
> son marcadas como spam por los algoritmos de Meta y pueden ser suspendidas.

---

### Paso 2: Meta for Developers — Crear la App

1. Ir a `developers.facebook.com`
2. Click en **"My Apps"** → **"Create App"**
3. Seleccionar tipo: **"Business"**
4. Completar:
   - App name: `[NombreEmpresa] WA Bot` (ej: `Centriqs WA Bot`)
   - Contact email: email empresarial
   - Business account: seleccionar la cuenta del Paso 1
5. En el dashboard de la app, buscar **"WhatsApp"** y click en **"Set up"**

**Guardar en `config.md`:** el `App ID` que aparece en el dashboard de la app.

---

### Paso 3: WhatsApp Business Account (WABA) y número

1. Dentro de la app en Meta for Developers, ir a **WhatsApp → Getting Started**
2. Meta provee un número de prueba gratuito para testing (solo para 5 contactos)
3. Para producción: agregar un número real dedicado
   - El número **no puede estar registrado** en ninguna app de WhatsApp (ni personal ni Business)
   - Si el número ya tiene WhatsApp, primero borrarlo de WhatsApp en el teléfono
   - Puede ser: línea móvil, línea fija con capacidad de recibir SMS/llamadas, VoIP

4. Proceso de verificación del número:
   - Ingresar el número en formato internacional: `+5491112345678`
   - Recibir código por SMS o llamada
   - Ingresar código → número verificado

**Guardar en `config.md`:**
- `phone_number_id` (aparece en la sección del número)
- `whatsapp_business_account_id` (WABA ID)

---

### Paso 4: Token de acceso permanente (System User)

El token temporal de prueba expira en 24 horas. Para producción, crear un **System User** con token permanente:

1. Ir a **Meta Business Suite → Configuración del negocio → Usuarios → Usuarios del sistema**
2. Click **"Agregar"** → tipo: **"Admin"**
3. Asignar activos: seleccionar la app de WhatsApp creada en el Paso 2
4. Generar token:
   - Click en el System User creado → **"Generar nuevo token"**
   - App: seleccionar tu app
   - Permisos mínimos necesarios:
     - `whatsapp_business_messaging`
     - `whatsapp_business_management`
   - Expiración: **"Nunca"**
5. Copiar y guardar el token de inmediato (no se puede recuperar después)

**Guardar en `config.md`:** `access_token`

> 🔒 Este token tiene acceso completo al número de WhatsApp. Tratar como una contraseña.
> Rotarlo si se sospecha que fue comprometido desde Meta Business Suite.

---

### Paso 5: Webhook — recibir mensajes entrantes

El webhook es la URL donde Meta envía los mensajes que recibe tu número. OpenClaw necesita exponerse como servidor para recibirlos.

**Opción A — Vercel (recomendada para Centriqs):**

Crear un endpoint en tu proyecto de Vercel en `centriqs.io/api/whatsapp`:

```javascript
// api/whatsapp.js (Next.js / Vercel serverless function)
export default function handler(req, res) {
  if (req.method === 'GET') {
    // Verificación inicial del webhook por Meta
    const mode = req.query['hub.mode'];
    const token = req.query['hub.verify_token'];
    const challenge = req.query['hub.challenge'];

    if (mode === 'subscribe' && token === process.env.WEBHOOK_VERIFY_TOKEN) {
      return res.status(200).send(challenge);
    }
    return res.status(403).end();
  }

  if (req.method === 'POST') {
    // Reenviar el payload a OpenClaw (webhook local o túnel)
    // Implementar según arquitectura: ngrok en dev, VPS en producción
    console.log('Mensaje entrante:', JSON.stringify(req.body, null, 2));
    return res.status(200).json({ status: 'ok' });
  }
}
```

**Variable de entorno en Vercel:** `WEBHOOK_VERIFY_TOKEN=<tu_token_elegido>`

**Opción B — VPS del cliente (producción):**

Para clientes en managed services, el webhook apunta al VPS del cliente. OpenClaw escucha en el puerto configurado (por defecto 3000 o el que definas).

**Configurar el webhook en Meta:**

1. En Meta for Developers → tu App → WhatsApp → Configuration
2. **Webhook URL:** `https://centriqs.io/api/whatsapp` (o la URL de tu VPS)
3. **Verify Token:** el valor de `webhook_verify_token` en tu `config.md`
4. Click **"Verify and Save"**
5. Suscribir a los campos: `messages`, `message_deliveries`, `message_reads`

---

### Paso 6: Integración con openclaw.json

Agregar el canal de WhatsApp en la configuración de OpenClaw:

```json
// ~/.openclaw/openclaw.json — sección "channels"
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "provider": "meta-cloud-api",
      "phoneNumberId": "<phone_number_id_de_config.md>",
      "accessToken": "<access_token_de_config.md>",
      "webhookVerifyToken": "<webhook_verify_token_de_config.md>",
      "webhookPath": "/webhook/whatsapp",
      "wabaId": "<whatsapp_business_account_id_de_config.md>"
    }
  }
}
```

> ⚠️ No hardcodear tokens directamente en `openclaw.json` si el archivo es accesible
> desde el repositorio. Usar variables de entorno y referenciarlas con `${VAR_NAME}`.

---

### Paso 7: Verificación de la cuenta de negocio (Meta Business Verification)

Para desbloquear límites de mensajes y poder enviar mensajes de plantilla a cualquier número (no solo a los 5 de prueba), es necesario verificar la empresa ante Meta.

1. Ir a **Meta Business Suite → Configuración → Verificación del negocio**
2. Seleccionar país: Argentina
3. Documentos necesarios (uno de los siguientes):
   - **DNI/CUIT + constancia de inscripción AFIP** (monotributistas y autónomos)
   - **Contrato de sociedad + inscripción en IGJ** (SRL, SA)
   - **Extracto bancario** a nombre de la empresa (últimos 3 meses)
4. La verificación tarda 2-5 días hábiles
5. Una vez verificada: límite inicial de **1,000 conversaciones de negocio por día**

> La verificación desbloquea también la posibilidad de usar el nombre de display
> personalizado (en vez del número de teléfono) en los chats.

---

## Templates HSM — Listos para usar

Los **HSM (Highly Structured Messages)** son plantillas pre-aprobadas por Meta para enviar mensajes fuera de la ventana de 24 horas. Son obligatorios para iniciar conversaciones o para mensajes automatizados (recordatorios, alertas, notificaciones).

**Cómo enviar un template aprobado:**

```bash
curl -X POST \
  "https://graph.facebook.com/v23.0/<PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "5491112345678",
    "type": "template",
    "template": {
      "name": "<NOMBRE_DEL_TEMPLATE>",
      "language": { "code": "es_AR" },
      "components": [
        {
          "type": "body",
          "parameters": [
            { "type": "text", "text": "<VALOR_VARIABLE_1>" },
            { "type": "text", "text": "<VALOR_VARIABLE_2>" }
          ]
        }
      ]
    }
  }'
```

---

### TEMPLATE 1 — Confirmación de turno

**Nombre sugerido:** `confirmacion_turno_v1` **Categoría Meta:** `UTILITY` **Idioma:** `es_AR`

```
Hola {{1}}, tu turno está confirmado para el {{2}} a las {{3}} hs.

Dirección: {{4}}

Si necesitás reprogramar, respondé este mensaje o llamanos al {{5}}.

— {{6}}
```

**Variables:**
1. Nombre del cliente
2. Fecha (DD/MM/AAAA)
3. Hora (HH:MM)
4. Dirección del negocio
5. Teléfono de contacto
6. Nombre del negocio

**Ejemplo de uso real:**
> "Hola María, tu turno está confirmado para el 15/04/2026 a las 10:30 hs.
> Dirección: Av. Corrientes 1234, CABA.
> Si necesitás reprogramar, respondé este mensaje o llamanos al 11-4444-5555.
> — Estudio Pérez & Asociados"

---

### TEMPLATE 2 — Recordatorio de turno (24hs antes)

**Nombre sugerido:** `recordatorio_turno_24hs_v1` **Categoría Meta:** `UTILITY` **Idioma:** `es_AR`

```
Recordatorio: {{1}}, mañana {{2}} tenés turno a las {{3}} hs en {{4}}.

Confirmá respondiendo SÍ o comunicate si necesitás cancelar.

— {{5}}
```

**Variables:**
1. Nombre del cliente
2. Fecha (ej: "martes 14/04")
3. Hora
4. Nombre del lugar/consultorio/estudio
5. Nombre del negocio

---

### TEMPLATE 3 — Recordatorio de pago pendiente

**Nombre sugerido:** `recordatorio_pago_pendiente_v1` **Categoría Meta:** `UTILITY` **Idioma:** `es_AR`

```
Hola {{1}}, te recordamos que tenés un pago pendiente por ${{2}} con vencimiento el {{3}}.

Podés abonar por transferencia al CBU {{4}} a nombre de {{5}}, o respondé este mensaje para coordinar.

— {{6}}
```

**Variables:**
1. Nombre del cliente
2. Monto (sin símbolo de moneda en la variable — el $ va en el template)
3. Fecha de vencimiento (DD/MM/AAAA)
4. CBU de la empresa
5. Titular del CBU
6. Nombre del negocio

---

### TEMPLATE 4 — Alerta de vencimiento AFIP/ARCA

**Nombre sugerido:** `alerta_vencimiento_arca_v1` **Categoría Meta:** `UTILITY` **Idioma:** `es_AR`

```
📋 Recordatorio fiscal: {{1}}, el {{2}} vence {{3}}.

{{4}}

Consultá con tu contador si necesitás asistencia. Respondé este mensaje para más información.

— {{5}}
```

**Variables:**
1. Nombre del cliente o empresa
2. Fecha de vencimiento (DD/MM/AAAA)
3. Nombre de la obligación (ej: "IVA período marzo 2026")
4. Nota adicional (ej: "CUIT terminados en 0 y 1" o "Todos los contribuyentes")
5. Nombre del estudio/agente que envía

**Uso típico:** estudios contables que quieren recordar a sus clientes los vencimientos del mes sin llamar uno por uno.

---

### TEMPLATE 5 — Notificación de entrega / pedido listo

**Nombre sugerido:** `pedido_listo_v1` **Categoría Meta:** `UTILITY` **Idioma:** `es_AR`

```
Hola {{1}}, tu pedido #{{2}} está listo para {{3}}.

{{4}}

Ante cualquier consulta respondé este mensaje.

— {{5}}
```

**Variables:**
1. Nombre del cliente
2. Número de pedido o referencia
3. `retiro en tienda` / `envío a domicilio` / `descarga disponible`
4. Instrucciones adicionales (ej: dirección, link de descarga, código de retiro)
5. Nombre del negocio

---

### TEMPLATE 6 — Bienvenida / primer contacto

**Nombre sugerido:** `bienvenida_v1` **Categoría Meta:** `MARKETING` **Idioma:** `es_AR`

```
¡Hola {{1}}! Bienvenido/a a {{2}} 👋

Soy el asistente virtual. Puedo ayudarte con:
• {{3}}
• {{4}}
• {{5}}

¿En qué puedo ayudarte hoy?
```

**Variables:**
1. Nombre del contacto (si está disponible)
2. Nombre del negocio
3, 4, 5. Servicios principales (ej: "Consultas sobre turnos", "Estado de pedidos", "Información de precios")

> ℹ️ Los templates de categoría `MARKETING` tienen costo por conversación más alto
> que los de `UTILITY`. Usar solo cuando es el primer contacto o para campañas activas.

---

### Cómo enviar templates desde OpenClaw

El agente puede ejecutar el envío de templates usando el comando `curl` (declarado en `requires.bins`). Ejemplo de función reutilizable:

```bash
# Función de envío de template WhatsApp
# Uso: wa_send_template <numero> <template_name> <var1> <var2> ...

wa_send_template() {
  local numero="$1"
  local template_name="$2"
  shift 2
  local params=""

  for var in "$@"; do
    params="${params}{\"type\":\"text\",\"text\":\"${var}\"},"
  done
  params="${params%,}"  # Quitar última coma

  curl -s -X POST \
    "https://graph.facebook.com/v23.0/${PHONE_NUMBER_ID}/messages" \
    -H "Authorization: Bearer ${WA_ACCESS_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{
      \"messaging_product\": \"whatsapp\",
      \"to\": \"${numero}\",
      \"type\": \"template\",
      \"template\": {
        \"name\": \"${template_name}\",
        \"language\": {\"code\": \"es_AR\"},
        \"components\": [{
          \"type\": \"body\",
          \"parameters\": [${params}]
        }]
      }
    }"
}
```

**Variables de entorno requeridas** (inyectar en `openclaw.json` bajo `skills.entries`):

```json
{
  "skills": {
    "entries": {
      "whatsapp-business-latam": {
        "env": {
          "PHONE_NUMBER_ID": "<phone_number_id>",
          "WA_ACCESS_TOKEN": "<access_token>"
        }
      }
    }
  }
}
```

---

## Compliance — Reglas para no perder la cuenta

### Ventana de servicio de 24 horas (Customer Service Window)

Cuando un usuario te escribe un mensaje, se abre automáticamente una **Customer Service Window (CSW) de 24 horas**. Cada mensaje que el usuario envía reinicia el contador.

**Qué podés hacer dentro de la CSW (todo gratis):**
- Enviar cualquier cantidad de mensajes de texto libre
- Enviar imágenes, documentos, audios, ubicaciones
- Enviar **templates de utility** (sin costo, desde julio 2025)

**Qué NO podés hacer dentro de la CSW:**
- Enviar templates de marketing o autenticación (siempre tienen costo)

**Fuera de la CSW (más de 24hs desde el último mensaje del usuario):**
- Solo podés enviar templates aprobados
- Cada template delivered se cobra según su categoría (ver sección Costos)

**Regla práctica para PyMEs:** mantener la conversación activa es gratis. Si un cliente escribe una consulta, el agente puede responder todo lo necesario sin costo, incluso enviar confirmaciones o recordatorios con templates de utility — siempre que sea dentro de las 24hs desde el último mensaje del cliente.

### Opt-in obligatorio

Meta exige que los contactos hayan dado **consentimiento explícito** para recibir mensajes de WhatsApp de tu empresa antes de que les envíes el primer template.

Formas válidas de opt-in:
- Formulario web con checkbox específico para WhatsApp
- Mensaje de confirmación por SMS previo al primer WA
- Confirmación verbal documentada (en el momento del turno, por ejemplo)

Lo que NO es opt-in válido:
- Tener el número de teléfono del cliente
- Que el cliente te haya comprado algo
- Un contrato genérico de servicios

> Guardar evidencia del opt-in por cliente. Si Meta audita tu cuenta y no podés demostrar
> el consentimiento, el número puede ser baneado.

### Rate limits — Messaging Tiers

Meta limita la cantidad de **usuarios únicos** a los que podés iniciar conversaciones por día (los mensajes entrantes y respuestas dentro de CSW no cuentan contra el límite).

| Tier | Usuarios únicos / 24hs |
|------|------------------------|
| Sin verificar | 250 |
| Tier 1 (cuenta verificada) | 1,000 |
| Tier 2 | 10,000 |
| Tier 3 | 100,000 |
| Tier 4 | Ilimitado |

**Cómo se sube de tier:**
- Mantener quality rating en **Verde** durante 7 días consecutivos
- Enviar al menos el 50% del volumen del tier actual durante esos 7 días
- El upgrade es automático (no requiere solicitud)

**Cómo se baja de tier:**
- Quality rating en **Rojo** durante 7 días → bajás un tier
- Quality rating en **Rojo** persistente → suspensión del número

### Quality Rating

Meta mide la calidad de tu cuenta según:
- Tasa de bloqueos de contactos
- Reportes de spam
- Tasa de respuesta a mensajes entrantes
- Relevancia de los templates enviados

**Si cae a "Amarillo":** recibís una advertencia. Reducir volumen de envíos inmediatamente. **Si cae a "Rojo":** el número queda en pausa. Puede resultar en baneo si no mejora.

---

## Free Entry Points — la ventana de 72 horas

Meta abre una ventana especial de **72 horas de mensajes completamente gratis** cuando el usuario entra a tu WhatsApp a través de:

- **Click-to-WhatsApp Ads** (anuncios en Facebook/Instagram que abren el chat)
- **Facebook Page CTA button** ("Enviar mensaje" en tu página de Facebook)
- Anuncios de WhatsApp Flow

Durante esas 72 horas:
- Podés enviar cualquier cantidad de mensajes de cualquier categoría (incluido marketing)
- **Sin costo** para ninguno de ellos
- El contador se reinicia con cada nuevo mensaje del usuario dentro de la ventana

**Por qué es importante para PyMEs argentinas:**

Si hacés campañas pagas en Meta Ads con CTA a WhatsApp, el costo de los mensajes posteriores queda incluido en el costo del ad. Esto cambia la matemática del customer acquisition: lo que pagás es solo el ad, no los mensajes de follow-up.

**Estrategia recomendada:**
1. Correr campaña de Click-to-WhatsApp Ads con presupuesto definido
2. Responder rápido (ventana de 72hs empieza con el click)
3. Cerrar la venta o agendar reunión dentro de las 72hs
4. A partir de la 73ª hora, si necesitás re-engagement, usar utility templates (paid)

---

## Checklist anti-ban

Antes de enviar el primer mensaje de producción, verificar que:

```
[ ] El número usado es EXCLUSIVO para WhatsApp Business API
    (no está ni estuvo en la app de WhatsApp personal o Business App)

[ ] La cuenta de Meta Business está verificada con documentación real

[ ] Todos los contactos dieron opt-in explícito antes del primer envío

[ ] Los templates fueron aprobados por Meta antes de enviarlos
    (no enviar templates "pendientes de revisión")

[ ] El nombre de display del número coincide con el nombre legal del negocio
    o una variación reconocible

[ ] No se está usando ninguna librería no oficial:
    ❌ Baileys
    ❌ whatsapp-web.js
    ❌ WPPConnect
    ❌ venom-bot
    ❌ Chat-API
    ✅ Meta Cloud API (graph.facebook.com)

[ ] El token de acceso es de un System User, no de una cuenta personal

[ ] Los mensajes tienen un propósito claro y valor para el receptor
    (no spam, no mensajes masivos sin segmentación)

[ ] El webhook responde con HTTP 200 en menos de 5 segundos
    (si Meta no recibe 200, reintenta y puede marcar la cuenta como problemática)

[ ] El número tiene habilitado el desvío de llamadas o puede recibir SMS
    (necesario para renovar la verificación del número si caduca)
```

---

## Costos estimados para PyMEs argentinas

> ⚠️ **Cambio importante — julio 2025:** Meta migró de un modelo de pricing
> "per-conversation" (24hs) a un modelo **per-message**. Todo este skill está
> actualizado al nuevo modelo. Referencia oficial: `business.whatsapp.com/products/platform-pricing`

### Qué es gratis en el modelo per-message (muy importante para PyMEs)

| Categoría | Costo |
|-----------|-------|
| Service messages (cualquier mensaje dentro de la Customer Service Window) | GRATIS sin límite |
| Utility templates enviados dentro de la CSW | GRATIS sin límite |
| Free Entry Points — usuarios que entran via Click-to-WhatsApp Ads o CTA de Facebook Page | 72hs de mensajes gratis (incluido marketing) |

Esto es un cambio estructural: **una PyME con tráfico entrante orgánico (clientes que inician la conversación) puede operar con costo casi nulo**.

### Qué se paga (modelo per-message, por template delivered)

| Categoría | Cuándo aplica |
|-----------|---------------|
| Utility template | Enviado fuera de la CSW (recordatorio proactivo sin conversación previa reciente) |
| Marketing template | Campañas, promociones, bienvenidas sin conversación previa |
| Authentication template | Códigos de verificación, OTPs, 2FA |

Las tarifas exactas por país y categoría están en el sitio oficial de Meta. Meta ajusta precios periódicamente — no hardcodear valores en integraciones productivas.

### Volume tiers (descuentos por volumen)

Desde julio 2025, Meta aplica **tiered pricing** para utility y authentication: cuanto más envíes, menor es el costo unitario. Los tiers se definen por mercado y se calculan mensualmente según el volumen acumulado del mes.

### Estimación de costo mensual (escenarios reales)

**Escenario A — Estudio contable con 50 clientes, solo recordatorios ARCA:**
- Clientes escriben consultas durante el mes (genera CSW): service messages gratis
- ~50 recordatorios proactivos de vencimiento por mes (utility fuera de CSW)
- **Costo estimado: USD 1-3/mes** (solo los utility fuera de CSW)

**Escenario B — E-commerce chico con 500 pedidos/mes:**
- Cliente compra y recibe confirmación (dentro de la CSW si preguntó algo antes): gratis
- Actualización de envío (utility, mayoría dentro de CSW): gratis
- Recordatorio de carrito abandonado (marketing, fuera de CSW): paid
- **Costo estimado: USD 5-20/mes** según mix

**Escenario C — PyME con estrategia de CTWA Ads:**
- Leads llegan via Click-to-WhatsApp Ads → **72hs gratis** para vender
- Mensajes de seguimiento post-72hs: utility paid
- **Costo estimado: USD 10-30/mes** (pero con ROI muy alto por cost-per-lead bajo)

> **Factor clave:** el costo real depende de la proporción entre mensajes dentro y fuera
> de la CSW. Una PyME que fomenta que el cliente inicie la conversación (respondiendo
> rápido, usando CTWA Ads, mostrando el número en redes) paga muy poco.

---

## Mensaje de respuesta libre (dentro de ventana de 24hs)

Cuando el usuario escribe al número, el agente puede responder con texto libre durante las siguientes 24 horas. Ejemplo de respuesta automática vía API:

```bash
curl -X POST \
  "https://graph.facebook.com/v23.0/${PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer ${WA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "5491112345678",
    "type": "text",
    "text": {
      "body": "¡Hola! Recibimos tu mensaje y te respondemos en breve. — Equipo Centriqs"
    }
  }'
```

---

## Prueba de envío — verificar que todo funciona

Una vez completado el setup, enviar un mensaje de prueba:

```bash
# Reemplazar con tus valores reales
PHONE_NUMBER_ID="tu_phone_number_id"
ACCESS_TOKEN="tu_access_token"
NUMERO_DESTINO="549XXXXXXXXXX"  # Tu propio número para prueba

curl -X POST \
  "https://graph.facebook.com/v23.0/${PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"messaging_product\": \"whatsapp\",
    \"to\": \"${NUMERO_DESTINO}\",
    \"type\": \"text\",
    \"text\": {\"body\": \"Prueba de conexión exitosa — OpenClaw + WhatsApp Business API ✓\"}
  }"
```

**Respuesta esperada:**

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "549XXXXXXXXXX", "wa_id": "549XXXXXXXXXX"}],
  "messages": [{"id": "wamid.XXXXXXXXXX"}]
}
```

Si obtenés `"error"` en la respuesta, verificar: token válido, `PHONE_NUMBER_ID` correcto, número de destino en formato internacional sin `+` (ej: `5491112345678` no `+5491112345678`).

---

## Privacidad y seguridad

- El `access_token` de System User tiene acceso completo al número. Nunca incluirlo en
código que se suba a repositorios públicos (GitHub, GitLab, etc.).
- Usar variables de entorno o el sistema de secrets de OpenClaw (`skills.entries.*.env`).
- Los mensajes de los usuarios son datos personales sujetos a la **Ley 25.326** de Argentina
(Protección de Datos Personales). No almacenar conversaciones sin consentimiento explícito.
- El log de envíos en `~/centriqs/whatsapp/logs/` debe tener permisos restringidos
(`chmod 600`) si contiene nombres o números de clientes.
- Ante una brecha de seguridad que exponga el token, rotarlo inmediatamente desde
Meta Business Suite → Usuarios del sistema → Generar nuevo token.

---

## Related skills

| Skill | Relación |
|-------|---------|
| latam-timezone-briefing | Puede disparar envíos de WhatsApp como canal de entrega del briefing |
| argentina-fiscal-calendar | Provee los datos de vencimientos que el agente puede notificar por WhatsApp |
| whatsapp-business-latam-pro *(paid — ClawMart, próximamente)* | Automatización avanzada: menú interactivo, respuestas con botones, flows, integración con Tiendanube y MercadoPago |

---

*Desarrollado por [Centriqs](https://centriqs.io) — Center of your operations* *MIT License — Libre uso, modificación y redistribución con atribución*
