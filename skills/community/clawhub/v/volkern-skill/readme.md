# Volkern MCP Server (v1.1.0)

Servidor MCP (Model Context Protocol) para integrar Volkern CRM con agentes de IA como Claude, GPT, y otros clientes compatibles con MCP.

## Novedades v1.1.0 - Catálogo Mejorado

### Nuevas Herramientas de Catálogo
- `volkern_list_catalogo` - Listar ítems con filtros avanzados (tipo, categoría, etiqueta)
- `volkern_get_catalogo_item` - Obtener detalle completo de un ítem
- `volkern_create_catalogo_item` - Crear ítem con campos personalizados, categorías, media y precios flexibles
- `volkern_update_catalogo_item` - Actualizar cualquier campo de un ítem
- `volkern_search_catalogo` - Búsqueda por texto en nombre, descripción y SKU

### Funcionalidades Soportadas
- **Campos personalizados**: Atributos dinámicos por ítem (metros², habitaciones, idioma, etc.)
- **Categorías multinivel**: Organización jerárquica (Inmuebles > Oficina > Lujo)
- **Etiquetas**: Tags para filtrado rápido (vip, oportunidad, nuevo)
- **Galería multimedia**: Imágenes, video tours, documentos técnicos, tours 360°
- **Precios flexibles**: Pago único, recurrente o por hora con descuentos por volumen

## Instalación

### Opción 1: Instalación global desde NPM (Recomendado)

```bash
npm install -g volkern-mcp-server
```

### Opción 2: Usando npx (sin instalación)

```bash
npx volkern-mcp-server
```

### Opción 3: Desde código fuente

```bash
git clone https://github.com/volkern/mcp-server.git
cd mcp-server
npm install
npm run build
```

## Configuración

El servidor requiere las siguientes variables de entorno:

```bash
export VOLKERN_API_KEY="tu_api_key_aqui"
export VOLKERN_API_URL="https://volkern.app/api"  # Opcional, usa este valor por defecto
```

## Uso con Claude Desktop

Agrega la siguiente configuración a tu archivo `claude_desktop_config.json`:

### Si instalaste con NPM (Recomendado)

```json
{
  "mcpServers": {
    "volkern": {
      "command": "volkern-mcp",
      "env": {
        "VOLKERN_API_KEY": "tu_api_key_aqui"
      }
    }
  }
}
```

### Si usas npx

```json
{
  "mcpServers": {
    "volkern": {
      "command": "npx",
      "args": ["volkern-mcp-server"],
      "env": {
        "VOLKERN_API_KEY": "tu_api_key_aqui"
      }
    }
  }
}
```

### Si instalaste desde código fuente

**macOS/Linux:**
```json
{
  "mcpServers": {
    "volkern": {
      "command": "node",
      "args": ["/ruta/a/volkern-mcp-server/dist/index.js"],
      "env": {
        "VOLKERN_API_KEY": "tu_api_key_aqui"
      }
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "volkern": {
      "command": "node",
      "args": ["C:\\ruta\\a\\volkern-mcp-server\\dist\\index.js"],
      "env": {
        "VOLKERN_API_KEY": "tu_api_key_aqui"
      }
    }
  }
}
```

## Herramientas Disponibles

### Gestión de Leads
| Herramienta | Descripción |
|-------------|-------------|
| `volkern_list_leads` | Listar leads con filtros opcionales |
| `volkern_get_lead` | Obtener detalles de un lead por ID |
| `volkern_create_lead` | Crear un nuevo lead |
| `volkern_update_lead` | Actualizar un lead existente |

### Citas/Appointments
| Herramienta | Descripción |
|-------------|-------------|
| `volkern_check_disponibilidad` | Consultar horarios disponibles |
| `volkern_list_citas` | Listar citas con filtros |
| `volkern_create_cita` | Crear una nueva cita |
| `volkern_update_cita` | Actualizar una cita |
| `volkern_cita_accion` | Confirmar, cancelar o reprogramar |

### Servicios
| Herramienta | Descripción |
|-------------|-------------|
| `volkern_list_servicios` | Listar servicios del catálogo |
| `volkern_get_servicio` | Obtener detalles de un servicio |

### Tareas
| Herramienta | Descripción |
|-------------|-------------|
| `volkern_create_task` | Crear tarea de seguimiento |
| `volkern_list_tasks` | Listar tareas de un lead |
| `volkern_complete_task` | Marcar tarea como completada |

### Mensajería
| Herramienta | Descripción |
|-------------|-------------|
| `volkern_send_whatsapp` | Enviar mensaje de WhatsApp |
| `volkern_list_conversaciones` | Listar conversaciones |

### Interacciones
| Herramienta | Descripción |
|-------------|-------------|
| `volkern_list_interactions` | Listar interacciones de un lead |
| `volkern_create_interaction` | Registrar llamada, email, reunión |

### Notas
| Herramienta | Descripción |
|-------------|-------------|
| `volkern_list_notes` | Listar notas de un lead |
| `volkern_create_note` | Agregar nota a un lead |

## Ejemplos de Uso

### Crear un lead y agendar cita

```
Usuario: Crea un lead para Juan Pérez, email juan@example.com, y agenda una cita para mañana a las 10am

Agente:
1. volkern_create_lead(nombre: "Juan Pérez", email: "juan@example.com")
2. volkern_check_disponibilidad(fecha: "2026-02-09")
3. volkern_create_cita(leadId: "...", fechaHora: "2026-02-09T10:00:00Z", titulo: "Reunión inicial")
```

### Consultar disponibilidad

```
Usuario: ¿Qué horarios hay disponibles para el lunes?

Agente:
1. volkern_check_disponibilidad(fecha: "2026-02-10")
```

### Crear tarea de seguimiento

```
Usuario: Crea un recordatorio para llamar a Juan mañana

Agente:
1. volkern_list_leads(search: "Juan")
2. volkern_create_task(leadId: "...", tipo: "llamada", titulo: "Llamar a Juan", fechaVencimiento: "2026-02-09T09:00:00Z")
```

## Desarrollo

```bash
# Ejecutar en modo desarrollo
npm run dev

# Compilar
npm run build

# Ejecutar compilado
npm start
```

## Troubleshooting

### Error: VOLKERN_API_KEY not set
Asegúrate de configurar la variable de entorno antes de iniciar el servidor.

### Error 401: No autorizado
Verifica que tu API key tenga los permisos necesarios en Volkern (Configuración → API Keys).

### Error 409: Conflicto de horario
El slot solicitado ya está ocupado. Consulta disponibilidad con `volkern_check_disponibilidad`.

## Licencia

MIT
