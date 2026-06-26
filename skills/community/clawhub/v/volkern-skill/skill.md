---
name: volkern-crm
description: "Automate Volkern CRM operations including lead management, appointment scheduling, task tracking, service catalog, WhatsApp messaging, sales pipeline, quotations, and contracts. Requires API key authentication."
requires:
  api_key: volkern
---

# Volkern CRM Automation

Automate CRM operations including lead lifecycle management, appointment scheduling with availability checks, task creation, service catalog queries, WhatsApp communication, sales pipeline management, quotation/proposal generation, and contract handling through Volkern's REST API.

## Prerequisites

- Volkern API Key with appropriate permissions
- Base URL: `https://volkern.app/api` (or your custom domain)
- All requests require `Authorization: Bearer {API_KEY}` header
- Timestamps must be in ISO 8601 format (UTC): `yyyy-MM-ddTHH:mm:ss.fffZ`

## Setup

1. Log into Volkern dashboard
2. Navigate to **Configuración → API Keys**
3. Create a new API key with required permissions:
   - `leads:read`, `leads:write` for lead management
   - `citas:read`, `citas:write` for appointments
   - `servicios:read` for service catalog
   - `mensajes:write` for WhatsApp messaging
4. Copy the API key (shown only once)
5. Use the key in the `Authorization` header for all requests

## Core Workflows

### 1. Lead Management

**When to use**: Create, update, search, or manage leads in the CRM

**Tool sequence**:
1. `VOLKERN_LIST_LEADS` - Search and filter existing leads [Optional]
2. `VOLKERN_GET_LEAD` - Get detailed lead information by ID [Optional]
3. `VOLKERN_CREATE_LEAD` - Create a new lead [Required for new leads]
4. `VOLKERN_UPDATE_LEAD` - Update lead properties [Required for updates]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/leads` | GET | `estado`, `canal`, `etiqueta`, `search`, `page`, `limit` |
| `/api/leads/{id}` | GET | `id` (path) |
| `/api/leads` | POST | `nombre`*, `email`, `telefono`, `empresa`, `canal`, `estado`, `etiquetas`, `notas`, `contextoProyecto` |
| `/api/leads/{id}` | PATCH | Any lead field to update |

**Lead estados (stages)**:
- `nuevo` - New lead, not contacted
- `contactado` - Initial contact made
- `calificado` - Qualified lead
- `negociacion` - In negotiation
- `cliente` - Converted to customer
- `perdido` - Lost opportunity

**Pitfalls**:
- `nombre` is the only required field for lead creation
- Email is validated for format but not uniqueness (upsert behavior: existing email updates the lead)
- `canal` should match predefined values: `web`, `referido`, `whatsapp`, `telefono`, `email`, `otro`
- `etiquetas` is an array of strings: `["vip", "urgente"]`

---

### 2. Appointment Scheduling

**When to use**: Book appointments, check availability, manage calendar

**Tool sequence**:
1. `VOLKERN_LIST_SERVICIOS` - Get available services with durations [Prerequisite]
2. `VOLKERN_CHECK_DISPONIBILIDAD` - Query available time slots [Required]
3. `VOLKERN_CREATE_CITA` - Book the appointment [Required]
4. `VOLKERN_LIST_CITAS` - List existing appointments [Optional]
5. `VOLKERN_UPDATE_CITA` - Reschedule or modify [Optional]
6. `VOLKERN_CANCEL_CITA` - Cancel appointment [Optional]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/citas/disponibilidad` | GET | `fecha`* (YYYY-MM-DD), `duracion` (minutes, default 60) |
| `/api/citas` | GET | `estado`, `tipo`, `fecha`, `fechaInicio`, `fechaFin` |
| `/api/citas` | POST | `leadId`*, `fechaHora`*, `tipo`, `titulo`, `descripcion`, `duracion`, `servicioId` |
| `/api/citas/{id}` | PATCH | `fechaHora`, `estado`, `duracion`, `descripcion` |
| `/api/citas/accion` | POST | `citaId`*, `accion`* (`confirmar`\|`cancelar`\|`reprogramar`) |

**Availability response structure**:
```json
{
  "fecha": "2026-02-10",
  "dia": "lunes",
  "diaActivo": true,
  "horarioLaboral": {
    "rangos": [{"inicio": "09:00", "fin": "13:00"}, {"inicio": "15:00", "fin": "18:00"}],
    "resumen": "09:00-13:00, 15:00-18:00"
  },
  "disponibles": {
    "total": 12,
    "slots": ["2026-02-10T09:00:00.000Z", "2026-02-10T09:30:00.000Z", ...]
  },
  "ocupados": {
    "total": 2,
    "slots": [{"hora": "...", "cita": {"id": "...", "titulo": "..."}}]
  }
}
```

**Cita tipos**:
- `reunion` - General meeting (default)
- `servicio` - Service appointment (requires `servicioId`)
- `llamada` - Phone call
- `otro` - Other

**Cita estados**:
- `Pendiente` - Awaiting confirmation
- `Confirmada` - Confirmed by client
- `Completada` - Meeting completed
- `Cancelada` - Cancelled
- `Pagada` - Paid (for paid services)

**Pitfalls**:
- Always check `diaActivo` before attempting to book - inactive days return 0 slots
- `duracion` must be an integer (minutes), not a string
- `fechaHora` must be ISO 8601 UTC format
- Booking on an occupied slot returns `409 Conflict` with suggested alternatives
- Weekend availability depends on tenant configuration in **Configuración → Horarios**

---

### 3. Task Management

**When to use**: Create follow-up tasks, reminders, or activities for leads

**Tool sequence**:
1. `VOLKERN_GET_LEAD` - Verify lead exists [Prerequisite]
2. `VOLKERN_CREATE_TASK` - Create task for the lead [Required]
3. `VOLKERN_LIST_TASKS` - Get lead's pending tasks [Optional]
4. `VOLKERN_COMPLETE_TASK` - Mark task as done [Optional]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/leads/{leadId}/tasks` | GET | `leadId` (path) |
| `/api/leads/{leadId}/tasks` | POST | `tipo`*, `titulo`*, `fechaVencimiento`*, `descripcion`, `asignadoA` |
| `/api/tasks/{taskId}` | PATCH | `completada`, `fechaCompletado` |

**Task tipos**:
- `llamada` - Phone call to make
- `email` - Email to send
- `reunion` - Meeting to schedule
- `recordatorio` - General reminder

**Pitfalls**:
- `tipo` must be lowercase and one of the valid values
- `fechaVencimiento` is required and must be a future date
- Tasks are automatically associated with the tenant via the API key

---

### 4. Service Catalog

**When to use**: Query available services for booking or pricing information

**Tool sequence**:
1. `VOLKERN_LIST_SERVICIOS` - Get all services [Required]
2. `VOLKERN_GET_SERVICIO` - Get specific service details [Optional]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/servicios` | GET | `activo` (boolean) |
| `/api/servicios/{id}` | GET | `id` (path) |

**Service response structure**:
```json
{
  "id": "clxyz...",
  "nombre": "Consultoría Inicial",
  "descripcion": "Sesión de 60 minutos...",
  "duracionMinutos": 60,
  "precio": 150.00,
  "moneda": "EUR",
  "modalidad": "virtual",
  "activo": true
}
```

**Modalidades**:
- `presencial` - In-person
- `virtual` - Online/video call
- `hibrido` - Hybrid (generates Google Meet link if connected)

**Pitfalls**:
- Only `activo: true` services should be offered for booking
- `duracionMinutos` determines the slot blocking duration
- Prices are in the tenant's configured currency

---

### 5. WhatsApp Messaging

**When to use**: Send WhatsApp messages to leads via connected integration

**Tool sequence**:
1. `VOLKERN_GET_LEAD` - Get lead's phone number [Prerequisite]
2. `VOLKERN_SEND_WHATSAPP` - Send message [Required]
3. `VOLKERN_LIST_CONVERSACIONES` - View conversation history [Optional]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/mensajes/enviar` | POST | `leadId`*, `mensaje`*, `tipo` |
| `/api/mensajes/conversaciones` | GET | `leadId`, `page`, `limit` |
| `/api/mensajes/conversaciones/{id}` | GET | `id` (path) |

**Message tipos**:
- `texto` - Plain text message
- `imagen` - Image with optional caption
- `documento` - Document attachment

**Pitfalls**:
- Requires active WhatsApp integration (Evolution API or Anytimebot)
- Lead must have a valid `telefono` field with country code
- Message delivery is async; check conversation history for status
- Rate limits apply based on WhatsApp Business policies

---

### 6. Lead Interactions

**When to use**: Record calls, meetings, or other activities with leads

**Tool sequence**:
1. `VOLKERN_GET_LEAD` - Verify lead exists [Prerequisite]
2. `VOLKERN_LIST_INTERACTIONS` - View existing interactions [Optional]
3. `VOLKERN_CREATE_INTERACTION` - Log the interaction [Required]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/leads/{id}/interactions` | GET | `id` (path) - Returns all interactions for the lead |
| `/api/leads/{id}/interactions` | POST | `tipo`*, `contenido`*, `resultado`, `metadatos` |

**Interaction tipos**:
- `llamada` - Phone call
- `email` - Email sent/received
- `whatsapp` - WhatsApp message
- `reunion` - Meeting held
- `nota` - Internal note
- `otro` - Other interaction type

**Resultado values**:
- `positivo` - Positive outcome
- `neutro` - Neutral
- `negativo` - Negative outcome

**Response structure**:
```json
{
  "success": true,
  "interaction": {
    "id": "clxyz...",
    "leadId": "clxyz...",
    "tipo": "llamada",
    "contenido": "Discussed pricing options...",
    "resultado": "positivo",
    "metadatos": { "duracion": "15min" },
    "fechaCreacion": "2026-02-09T10:00:00Z",
    "creador": { "id": "...", "name": "John", "email": "john@example.com" }
  }
}
```

**Pitfalls**:
- `tipo` must be lowercase
- Interactions automatically update lead's `fechaUltimaActividad`
- Triggers `interaccion_creada` automation event

---

### 7. Lead Notes

**When to use**: Add internal notes or observations about leads

**Tool sequence**:
1. `VOLKERN_GET_LEAD` - Verify lead exists [Prerequisite]
2. `VOLKERN_LIST_NOTES` - View existing notes [Optional]
3. `VOLKERN_CREATE_NOTE` - Add a new note [Required]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/leads/{id}/notes` | GET | `id` (path) - Returns all notes for the lead |
| `/api/leads/{id}/notes` | POST | `contenido`*, `titulo` (optional) |

**Response structure**:
```json
{
  "success": true,
  "note": {
    "id": "clxyz...",
    "leadId": "clxyz...",
    "contenido": "**Important**\n\nClient prefers morning calls...",
    "fechaCreacion": "2026-02-09T10:00:00Z",
    "creador": { "id": "...", "name": "John", "email": "john@example.com" }
  }
}
```

**Pitfalls**:
- If `titulo` is provided, it's prepended to `contenido` as bold markdown
- Notes automatically update lead's `fechaUltimaActividad`
- Triggers `nota_creada` automation event

---

### 8. Contacts & Companies

**When to use**: Manage business contacts (persons) and companies separately from leads

**Tool sequence**:
1. `VOLKERN_LIST_CONTACTS` - Search and filter contacts [Optional]
2. `VOLKERN_GET_CONTACT` - Get detailed contact information [Optional]
3. `VOLKERN_CREATE_CONTACT` - Create a new contact or company [Required for new]
4. `VOLKERN_UPDATE_CONTACT` - Update contact properties [Required for updates]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/contacts` | GET | `tipo` (person/company), `search`, `page`, `limit` |
| `/api/contacts/{id}` | GET | `id` (path) |
| `/api/contacts` | POST | `nombre`*, `email`, `telefono`, `tipo`, `cargo`, `ubicacion`, `companyId`, `linkedin`, `notas`, `tags` |
| `/api/contacts/{id}` | PATCH | Any contact field to update |

**Contact tipos**:
- `person` - Individual person (default)
- `company` - Business/organization

**Response structure**:
```json
{
  "id": "clxyz...",
  "nombre": "María García",
  "email": "maria@empresa.com",
  "telefono": "+34612345678",
  "tipo": "person",
  "cargo": "Directora de Marketing",
  "ubicacion": "Madrid, España",
  "company": { "id": "...", "nombre": "Empresa S.L." },
  "linkedin": "https://linkedin.com/in/mariagarcia",
  "tags": ["VIP", "Decision Maker"],
  "deals": [{ "id": "...", "titulo": "..." }],
  "fechaCreacion": "2026-02-09T10:00:00Z"
}
```

**Pitfalls**:
- `nombre` is the only required field
- `companyId` links a person to their company
- Companies can have multiple associated contacts
- Use `tipo=company` to list only companies

---

### 9. Sales Pipeline (Deals)

**When to use**: Manage sales opportunities through pipeline stages

**Tool sequence**:
1. `VOLKERN_LIST_PIPELINE_STAGES` - Get configured stages [Prerequisite]
2. `VOLKERN_LIST_DEALS` - Search and filter deals [Optional]
3. `VOLKERN_CREATE_DEAL` - Create a new opportunity [Required for new]
4. `VOLKERN_UPDATE_DEAL` - Move stage, update value, close deal [Required for updates]
5. `VOLKERN_GET_SALES_FORECAST` - Get pipeline analytics [Optional]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/pipeline/stages` | GET | - |
| `/api/deals` | GET | `etapa`, `estado`, `prioridad`, `search`, `page`, `limit` |
| `/api/deals/{id}` | GET | `id` (path) |
| `/api/deals` | POST | `titulo`*, `valor`, `moneda`, `etapa`, `prioridad`, `probabilidad`, `fechaEstimadaCierre`, `leadId`, `contactId`, `companyId`, `descripcion` |
| `/api/deals/{id}` | PATCH | Any deal field to update |
| `/api/deals/forecast` | GET | `periodo` (mes/trimestre/año) |

**Deal estados**:
- `abierto` - Active opportunity (default)
- `ganado` - Won deal
- `perdido` - Lost deal

**Deal prioridades**:
- `baja` - Low priority
- `media` - Medium priority
- `alta` - High priority

**Default pipeline stages** (probability in %):
| Stage | Probability |
|-------|-------------|
| Calificación | 10% |
| Contacto Inicial | 25% |
| Propuesta | 50% |
| Negociación | 75% |
| Cierre | 90% |
| Ganado | 100% |
| Perdido | 0% |

**Forecast response structure**:
```json
{
  "basicForecast": { "total": 125000, "ponderado": 45000 },
  "adjustedForecast": { "total": 42000, "confianza": 0.85 },
  "conversionRates": { "Calificación": { "teorica": 10, "real": 8.5 } },
  "cycleTime": { "promedioDias": 45 },
  "projection6Months": [{ "mes": "Feb 2026", "estimado": 15000 }],
  "historicalSales": [{ "mes": "Jan 2026", "total": 12000 }],
  "funnel": [{ "etapa": "Calificación", "cantidad": 10, "valor": 50000 }],
  "topDeals": [{ "id": "...", "titulo": "...", "valorPonderado": 15000 }]
}
```

**Pitfalls**:
- `titulo` is the only required field
- `etapa` must match exact stage name (case-sensitive)
- `probabilidad` auto-updates when changing `etapa`
- Moving to "Ganado" auto-sets `estado: ganado` and `probabilidad: 100`
- Moving to "Perdido" auto-sets `estado: perdido` and `probabilidad: 0`

---

### 10. Quotations (Cotizaciones)

**When to use**: Create and send price quotes/proposals to clients

**Tool sequence**:
1. `VOLKERN_GET_LEAD` or `VOLKERN_GET_DEAL` - Get client info [Prerequisite]
2. `VOLKERN_LIST_COTIZACIONES` - View existing quotes [Optional]
3. `VOLKERN_CREATE_COTIZACION` - Create new quote with items [Required]
4. `VOLKERN_UPDATE_COTIZACION` - Edit quote (only in borrador status) [Optional]
5. `VOLKERN_SEND_COTIZACION` - Email quote to client [Optional]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/cotizaciones` | GET | `estado`, `search`, `page`, `limit` |
| `/api/cotizaciones/{id}` | GET | `id` (path) |
| `/api/cotizaciones` | POST | `leadId`, `dealId`, `validezDias`, `notas`, `items`* |
| `/api/cotizaciones/{id}` | PATCH | `estado`, `validezDias`, `notas`, `items` |
| `/api/cotizaciones/{id}/send` | POST | `mensaje` (optional email text) |

**Item structure**:
```json
{
  "concepto": "Consultoría inicial",
  "cantidad": 2,
  "precioUnitario": 150.00,
  "descuento": 10
}
```

**Cotización estados**:
- `borrador` - Draft (editable)
- `enviada` - Sent to client
- `aceptada` - Accepted by client
- `rechazada` - Rejected
- `expirada` - Validity expired

**Response structure**:
```json
{
  "id": "clxyz...",
  "numero": "COT-2026-0001",
  "estado": "borrador",
  "subtotal": 270.00,
  "iva": 56.70,
  "total": 326.70,
  "validezDias": 30,
  "fechaExpiracion": "2026-03-11",
  "items": [...],
  "lead": { "nombre": "...", "email": "..." },
  "urlPublica": "https://volkern.app/cotizacion/abc123"
}
```

**Pitfalls**:
- `items` array is required with at least one item
- Only `borrador` status quotes can be edited
- Quote number is auto-generated (COT-YYYY-####)
- `validezDias` defaults to 30 if not specified
- Client can accept quote via public URL
- Accepted quotes can be converted to contracts

---

### 11. Contracts (Contratos)

**When to use**: Create formal contracts from accepted quotes or manually

**Tool sequence**:
1. `VOLKERN_LIST_COTIZACIONES` - Find accepted quote [Optional]
2. `VOLKERN_CREATE_CONTRATO_FROM_COTIZACION` - Convert quote to contract [Option A]
3. `VOLKERN_CREATE_CONTRATO` - Create contract manually [Option B]
4. `VOLKERN_LIST_CONTRATOS` - View existing contracts [Optional]
5. `VOLKERN_SEND_CONTRATO` - Send for client signature [Required]

**Key parameters**:

| Endpoint | Method | Parameters |
|----------|--------|------------|
| `/api/contratos` | GET | `estado`, `tipo`, `search`, `page`, `limit` |
| `/api/contratos/{id}` | GET | `id` (path) |
| `/api/contratos` | POST | `titulo`*, `tipo`, `leadId`, `dealId`, `cotizacionId`, `fechaInicio`, `fechaFin`, `metodoPago`, `clausulas`, `items` |
| `/api/contratos/from-cotizacion/{cotizacionId}` | POST | `fechaInicio`, `fechaFin`, `metodoPago`, `clausulas` |
| `/api/contratos/{id}/send` | POST | `mensaje` (optional email text) |

**Contrato tipos**:
- `servicios` - Service agreement
- `productos` - Product sale
- `suscripcion` - Subscription
- `proyecto` - Project-based
- `otro` - Other

**Contrato estados**:
- `borrador` - Draft
- `enviado` - Sent for signature
- `firmado_cliente` - Signed by client
- `firmado_empresa` - Signed by company
- `activo` - Both signatures, active
- `completado` - Fulfilled
- `cancelado` - Cancelled

**Método de pago**:
- `unico` - Single payment
- `mensual` - Monthly payments
- `trimestral` - Quarterly payments
- `anual` - Annual payments

**Response structure**:
```json
{
  "id": "clxyz...",
  "numero": "CONT-2026-0001",
  "titulo": "Contrato de Servicios",
  "tipo": "servicios",
  "estado": "enviado",
  "total": 12000.00,
  "fechaInicio": "2026-02-15",
  "fechaFin": "2027-02-14",
  "metodoPago": "mensual",
  "firmadoPorCliente": false,
  "firmadoPorEmpresa": false,
  "items": [...],
  "pagos": [...],
  "urlPublica": "https://volkern.app/contrato/xyz789"
}
```

**Pitfalls**:
- Contract number is auto-generated (CONT-YYYY-####)
- Creating from cotización copies items automatically
- Client signs via public URL (no login required)
- Payment schedule is auto-generated based on `metodoPago`
- `activo` status requires both signatures
- Digital signatures include timestamp and IP

---

## Common Patterns

### ID Resolution
Volkern uses CUID format for all entity IDs:
- Example: `clxyz123abc456def789`
- Always retrieve IDs from list/create responses
- Never construct IDs manually

### Pagination
List endpoints support pagination:
```
GET /api/leads?page=1&limit=50
```
- Default `limit`: 50
- Maximum `limit`: 100
- Response includes `total` count for pagination UI

### Time Handling
- All timestamps are in **UTC**
- Format: `yyyy-MM-ddTHH:mm:ss.fffZ`
- Availability queries use date only: `YYYY-MM-DD`
- Frontend displays in tenant's configured timezone

### Error Handling
Standard HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (invalid/missing API key)
- `404` - Not Found
- `409` - Conflict (e.g., scheduling conflict)
- `500` - Server Error

Error response format:
```json
{
  "error": "Descriptive error message",
  "details": "Additional context",
  "hint": "How to fix the issue"
}
```

---

## Quick Reference

| Task | Endpoint | Method | Key Params |
|------|----------|--------|------------|
| **LEADS** | | | |
| List leads | `/api/leads` | GET | `estado`, `search`, `page` |
| Get lead | `/api/leads/{id}` | GET | `id` |
| Create lead | `/api/leads` | POST | `nombre`*, `email`, `telefono` |
| Update lead | `/api/leads/{id}` | PATCH | Any field |
| **APPOINTMENTS** | | | |
| Check availability | `/api/citas/disponibilidad` | GET | `fecha`*, `duracion` |
| List appointments | `/api/citas` | GET | `estado`, `fecha` |
| Create appointment | `/api/citas` | POST | `leadId`*, `fechaHora`*, `tipo` |
| Update appointment | `/api/citas/{id}` | PATCH | `estado`, `fechaHora` |
| Confirm/Cancel | `/api/citas/accion` | POST | `citaId`*, `accion`* |
| **SERVICES** | | | |
| List services | `/api/servicios` | GET | `activo` |
| Get service | `/api/servicios/{id}` | GET | `id` |
| **TASKS** | | | |
| Create task | `/api/leads/{id}/tasks` | POST | `tipo`*, `titulo`*, `fechaVencimiento`* |
| List tasks | `/api/leads/{id}/tasks` | GET | - |
| Complete task | `/api/tasks/{id}` | PATCH | `completada: true` |
| **MESSAGING** | | | |
| Send WhatsApp | `/api/mensajes/enviar` | POST | `leadId`*, `mensaje`* |
| List conversations | `/api/mensajes/conversaciones` | GET | `leadId` |
| **INTERACTIONS** | | | |
| List interactions | `/api/leads/{id}/interactions` | GET | - |
| Create interaction | `/api/leads/{id}/interactions` | POST | `tipo`*, `contenido`*, `resultado` |
| **NOTES** | | | |
| List notes | `/api/leads/{id}/notes` | GET | - |
| Add note | `/api/leads/{id}/notes` | POST | `contenido`*, `titulo` |
| **CONTACTS** | | | |
| List contacts | `/api/contacts` | GET | `tipo`, `search`, `page` |
| Get contact | `/api/contacts/{id}` | GET | `id` |
| Create contact | `/api/contacts` | POST | `nombre`*, `email`, `tipo` |
| Update contact | `/api/contacts/{id}` | PATCH | Any field |
| **DEALS** | | | |
| List pipeline stages | `/api/pipeline/stages` | GET | - |
| List deals | `/api/deals` | GET | `etapa`, `estado`, `search` |
| Get deal | `/api/deals/{id}` | GET | `id` |
| Create deal | `/api/deals` | POST | `titulo`*, `valor`, `etapa` |
| Update deal | `/api/deals/{id}` | PATCH | `etapa`, `estado`, `valor` |
| Sales forecast | `/api/deals/forecast` | GET | `periodo` |
| **QUOTATIONS** | | | |
| List quotes | `/api/cotizaciones` | GET | `estado`, `search` |
| Get quote | `/api/cotizaciones/{id}` | GET | `id` |
| Create quote | `/api/cotizaciones` | POST | `items`*, `leadId`, `dealId` |
| Update quote | `/api/cotizaciones/{id}` | PATCH | `items`, `notas` |
| Send quote | `/api/cotizaciones/{id}/send` | POST | `mensaje` |
| **CONTRACTS** | | | |
| List contracts | `/api/contratos` | GET | `estado`, `tipo`, `search` |
| Get contract | `/api/contratos/{id}` | GET | `id` |
| Create contract | `/api/contratos` | POST | `titulo`*, `tipo`, `items` |
| Create from quote | `/api/contratos/from-cotizacion/{id}` | POST | `fechaInicio`, `metodoPago` |
| Send contract | `/api/contratos/{id}/send` | POST | `mensaje` |

\* = Required field

---

## Known Pitfalls

### Authentication
- API keys are tenant-scoped; one key per organization
- Keys can have granular permissions; check scope if getting 401/403
- Never expose API keys in client-side code

### Data Validation
- Phone numbers should include country code: `+34612345678`
- Email validation is strict; malformed emails are rejected
- Dates in the past may be rejected for appointments

### Scheduling Conflicts
- The system validates overlapping appointments
- Use `disponibilidad` endpoint before booking
- 409 responses include suggested alternative slots

### WhatsApp Integration
- Requires pre-configured integration (Evolution API)
- First message to new number requires template approval
- Media messages have size limits (16MB for images)

### Rate Limits
- Standard: 100 requests/minute per API key
- Bulk operations: 10 requests/minute
- WhatsApp: Subject to Meta's messaging limits
