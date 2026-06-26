#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema, } from "@modelcontextprotocol/sdk/types.js";
// ============================================
// Configuration
// ============================================
const VOLKERN_API_URL = process.env.VOLKERN_API_URL || "https://volkern.app/api";
const VOLKERN_API_KEY = process.env.VOLKERN_API_KEY || "";
if (!VOLKERN_API_KEY) {
    console.error("Error: VOLKERN_API_KEY environment variable is required");
    process.exit(1);
}
// ============================================
// API Helper
// ============================================
async function volkernRequest(endpoint, method = "GET", body) {
    const url = `${VOLKERN_API_URL}${endpoint}`;
    const options = {
        method,
        headers: {
            "Authorization": `Bearer ${VOLKERN_API_KEY}`,
            "Content-Type": "application/json",
        },
    };
    if (body && method !== "GET") {
        options.body = JSON.stringify(body);
    }
    const response = await fetch(url, options);
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`Volkern API Error (${response.status}): ${JSON.stringify(errorData)}`);
    }
    return response.json();
}
// ============================================
// Tool Definitions
// ============================================
const tools = [
    // === LEADS ===
    {
        name: "volkern_list_leads",
        description: "List leads with optional filters. Returns paginated results.",
        inputSchema: {
            type: "object",
            properties: {
                estado: {
                    type: "string",
                    enum: ["nuevo", "contactado", "calificado", "negociacion", "cliente", "perdido"],
                    description: "Filter by lead status"
                },
                canal: {
                    type: "string",
                    enum: ["web", "referido", "whatsapp", "telefono", "email", "otro"],
                    description: "Filter by acquisition channel"
                },
                search: {
                    type: "string",
                    description: "Search by name, email, or phone"
                },
                page: { type: "number", description: "Page number (default: 1)" },
                limit: { type: "number", description: "Results per page (default: 50, max: 100)" }
            }
        }
    },
    {
        name: "volkern_get_lead",
        description: "Get detailed information about a specific lead by ID",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "The lead's unique ID" }
            },
            required: ["leadId"]
        }
    },
    {
        name: "volkern_create_lead",
        description: "Create a new lead in the CRM. If email already exists, updates the existing lead.",
        inputSchema: {
            type: "object",
            properties: {
                nombre: { type: "string", description: "Lead's full name (required)" },
                email: { type: "string", description: "Email address" },
                telefono: { type: "string", description: "Phone number with country code (e.g., +34612345678)" },
                empresa: { type: "string", description: "Company name" },
                canal: {
                    type: "string",
                    enum: ["web", "referido", "whatsapp", "telefono", "email", "otro"],
                    description: "Acquisition channel"
                },
                estado: {
                    type: "string",
                    enum: ["nuevo", "contactado", "calificado", "negociacion", "cliente", "perdido"],
                    description: "Initial status (default: nuevo)"
                },
                etiquetas: {
                    type: "array",
                    items: { type: "string" },
                    description: "Tags for categorization"
                },
                notas: { type: "string", description: "Initial notes" },
                contextoProyecto: { type: "string", description: "Project context or requirements" }
            },
            required: ["nombre"]
        }
    },
    {
        name: "volkern_update_lead",
        description: "Update an existing lead's information",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "The lead's unique ID" },
                nombre: { type: "string" },
                email: { type: "string" },
                telefono: { type: "string" },
                empresa: { type: "string" },
                canal: { type: "string" },
                estado: { type: "string" },
                etiquetas: { type: "array", items: { type: "string" } },
                notas: { type: "string" }
            },
            required: ["leadId"]
        }
    },
    // === APPOINTMENTS ===
    {
        name: "volkern_check_disponibilidad",
        description: "Check available time slots for a specific date. Always call this before booking.",
        inputSchema: {
            type: "object",
            properties: {
                fecha: { type: "string", description: "Date in YYYY-MM-DD format" },
                duracion: { type: "number", description: "Duration in minutes (default: 60)" }
            },
            required: ["fecha"]
        }
    },
    {
        name: "volkern_list_citas",
        description: "List appointments with optional filters",
        inputSchema: {
            type: "object",
            properties: {
                estado: {
                    type: "string",
                    enum: ["Pendiente", "Confirmada", "Completada", "Cancelada", "Pagada"],
                    description: "Filter by appointment status"
                },
                tipo: {
                    type: "string",
                    enum: ["reunion", "servicio", "llamada", "otro"],
                    description: "Filter by appointment type"
                },
                fecha: { type: "string", description: "Filter by specific date (YYYY-MM-DD)" },
                fechaInicio: { type: "string", description: "Start of date range (ISO 8601)" },
                fechaFin: { type: "string", description: "End of date range (ISO 8601)" }
            }
        }
    },
    {
        name: "volkern_create_cita",
        description: "Create a new appointment. Check availability first with volkern_check_disponibilidad.",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "ID of the lead for this appointment" },
                fechaHora: { type: "string", description: "Appointment date/time in ISO 8601 UTC (e.g., 2026-02-10T10:00:00Z)" },
                tipo: {
                    type: "string",
                    enum: ["reunion", "servicio", "llamada", "otro"],
                    description: "Appointment type (default: reunion)"
                },
                titulo: { type: "string", description: "Appointment title" },
                descripcion: { type: "string", description: "Appointment description or notes" },
                duracion: { type: "number", description: "Duration in minutes (default: 60)" },
                servicioId: { type: "string", description: "Service ID (required if tipo is 'servicio')" }
            },
            required: ["leadId", "fechaHora"]
        }
    },
    {
        name: "volkern_update_cita",
        description: "Update an existing appointment",
        inputSchema: {
            type: "object",
            properties: {
                citaId: { type: "string", description: "The appointment's unique ID" },
                fechaHora: { type: "string", description: "New date/time in ISO 8601 UTC" },
                estado: { type: "string", enum: ["Pendiente", "Confirmada", "Completada", "Cancelada"] },
                descripcion: { type: "string" },
                duracion: { type: "number" }
            },
            required: ["citaId"]
        }
    },
    {
        name: "volkern_cita_accion",
        description: "Perform an action on an appointment (confirm, cancel, or reschedule)",
        inputSchema: {
            type: "object",
            properties: {
                citaId: { type: "string", description: "The appointment's unique ID" },
                accion: {
                    type: "string",
                    enum: ["confirmar", "cancelar", "reprogramar"],
                    description: "Action to perform"
                },
                nuevaFecha: { type: "string", description: "New date/time for reschedule (ISO 8601)" },
                motivo: { type: "string", description: "Reason for cancellation" }
            },
            required: ["citaId", "accion"]
        }
    },
    // === CATALOG (ENHANCED) ===
    {
        name: "volkern_list_catalogo",
        description: "List catalog items (products, services, appointments, courses) with advanced filters",
        inputSchema: {
            type: "object",
            properties: {
                tipo: {
                    type: "string",
                    enum: ["producto", "servicio", "cita", "academia"],
                    description: "Filter by item type"
                },
                activo: { type: "boolean", description: "Filter only active items (default: true)" },
                categoria: { type: "string", description: "Filter by category name" },
                etiqueta: { type: "string", description: "Filter by tag" },
                search: { type: "string", description: "Search by name, description or SKU" },
                page: { type: "number", description: "Page number (default: 1)" },
                limit: { type: "number", description: "Results per page (default: 50)" }
            }
        }
    },
    {
        name: "volkern_get_catalogo_item",
        description: "Get detailed information about a specific catalog item including custom fields, pricing, and media",
        inputSchema: {
            type: "object",
            properties: {
                itemId: { type: "string", description: "The catalog item's unique ID" }
            },
            required: ["itemId"]
        }
    },
    {
        name: "volkern_create_catalogo_item",
        description: "Create a new catalog item with full support for custom fields, categories, tags, media, and flexible pricing",
        inputSchema: {
            type: "object",
            properties: {
                nombre: { type: "string", description: "Item name (required)" },
                descripcion: { type: "string", description: "Detailed description" },
                sku: { type: "string", description: "Internal SKU/code" },
                tipo: {
                    type: "string",
                    enum: ["producto", "servicio", "cita", "academia"],
                    description: "Item type (default: servicio)"
                },
                precioBase: { type: "number", description: "Base price (required)" },
                moneda: { type: "string", description: "Currency code (EUR, USD, MXN, GBP)" },
                categoriaFiscal: { type: "string", enum: ["general", "reducido", "superreducido", "exento"] },
                tasaImpuestoId: { type: "string", description: "Tax rate ID" },
                duracionMinutos: { type: "number", description: "Duration in minutes (for services/appointments)" },
                modalidad: { type: "string", enum: ["presencial", "virtual", "hibrido"] },
                unidad: { type: "string", description: "Unit (unidad, hora, servicio, mes, sesion, paquete)" },
                activo: { type: "boolean", description: "Is active (default: true)" },
                destacado: { type: "boolean", description: "Is featured (default: false)" },
                customFields: {
                    type: "array",
                    description: "Custom fields array [{key, label, type, value, unit?, options?}]",
                    items: {
                        type: "object",
                        properties: {
                            key: { type: "string" },
                            label: { type: "string" },
                            type: { type: "string", enum: ["text", "number", "select", "date", "boolean"] },
                            value: { type: ["string", "number", "boolean"] },
                            unit: { type: "string" },
                            options: { type: "array", items: { type: "string" } }
                        }
                    }
                },
                categorias: {
                    type: "array",
                    items: { type: "string" },
                    description: "Categories array (e.g., ['Inmuebles', 'Oficina', 'Lujo'])"
                },
                etiquetas: {
                    type: "array",
                    items: { type: "string" },
                    description: "Tags array (e.g., ['vip', 'oportunidad', 'nuevo'])"
                },
                metadata: {
                    type: "object",
                    description: "Additional metadata (e.g., {industria: 'real-estate', prioridad: 3})"
                },
                media: {
                    type: "object",
                    description: "Media gallery {imagenes: [], video_tour, documento_tecnico, tour_360}",
                    properties: {
                        imagenes: { type: "array", items: { type: "string" } },
                        video_tour: { type: "string" },
                        documento_tecnico: { type: "string" },
                        tour_360: { type: "string" }
                    }
                },
                pricing: {
                    type: "object",
                    description: "Flexible pricing {tipo, descuentos[], impuestos}",
                    properties: {
                        tipo: { type: "string", enum: ["unico", "recurrente", "por_hora"] },
                        descuentos: {
                            type: "array",
                            items: {
                                type: "object",
                                properties: {
                                    tipo: { type: "string" },
                                    min: { type: "number" },
                                    descuento: { type: "number" }
                                }
                            }
                        },
                        impuestos: {
                            type: "object",
                            properties: {
                                iva: { type: "number" },
                                incluido: { type: "boolean" }
                            }
                        }
                    }
                }
            },
            required: ["nombre", "precioBase"]
        }
    },
    {
        name: "volkern_update_catalogo_item",
        description: "Update an existing catalog item. Supports partial updates of any field including custom fields, categories, tags, media, and pricing",
        inputSchema: {
            type: "object",
            properties: {
                itemId: { type: "string", description: "The catalog item's unique ID" },
                nombre: { type: "string" },
                descripcion: { type: "string" },
                sku: { type: "string" },
                tipo: { type: "string", enum: ["producto", "servicio", "cita", "academia"] },
                precioBase: { type: "number" },
                moneda: { type: "string" },
                categoriaFiscal: { type: "string" },
                tasaImpuestoId: { type: "string" },
                duracionMinutos: { type: "number" },
                modalidad: { type: "string" },
                unidad: { type: "string" },
                activo: { type: "boolean" },
                destacado: { type: "boolean" },
                customFields: { type: "array", description: "Replace custom fields" },
                categorias: { type: "array", items: { type: "string" }, description: "Replace categories" },
                etiquetas: { type: "array", items: { type: "string" }, description: "Replace tags" },
                metadata: { type: "object", description: "Replace metadata" },
                media: { type: "object", description: "Replace media gallery" },
                pricing: { type: "object", description: "Replace pricing configuration" }
            },
            required: ["itemId"]
        }
    },
    {
        name: "volkern_search_catalogo",
        description: "Search catalog items by text across name, description and SKU. Returns items matching the query with their categories and tags.",
        inputSchema: {
            type: "object",
            properties: {
                query: { type: "string", description: "Search query" },
                tipo: { type: "string", enum: ["producto", "servicio", "cita", "academia"] },
                limit: { type: "number", description: "Max results (default: 20)" }
            },
            required: ["query"]
        }
    },
    // === SERVICES (LEGACY - uses catalog) ===
    {
        name: "volkern_list_servicios",
        description: "List available services from the catalog (legacy endpoint, use volkern_list_catalogo with tipo='servicio' instead)",
        inputSchema: {
            type: "object",
            properties: {
                activo: { type: "boolean", description: "Filter only active services (default: true)" }
            }
        }
    },
    {
        name: "volkern_get_servicio",
        description: "Get detailed information about a specific service (legacy endpoint)",
        inputSchema: {
            type: "object",
            properties: {
                servicioId: { type: "string", description: "The service's unique ID" }
            },
            required: ["servicioId"]
        }
    },
    // === TASKS ===
    {
        name: "volkern_create_task",
        description: "Create a follow-up task for a lead",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "ID of the lead" },
                tipo: {
                    type: "string",
                    enum: ["llamada", "email", "reunion", "recordatorio"],
                    description: "Task type"
                },
                titulo: { type: "string", description: "Task title" },
                descripcion: { type: "string", description: "Task description/context" },
                fechaVencimiento: { type: "string", description: "Due date in ISO 8601 UTC" },
                asignadoA: { type: "string", description: "User ID to assign the task to" }
            },
            required: ["leadId", "tipo", "titulo", "fechaVencimiento"]
        }
    },
    {
        name: "volkern_list_tasks",
        description: "List tasks for a specific lead",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "ID of the lead" }
            },
            required: ["leadId"]
        }
    },
    {
        name: "volkern_complete_task",
        description: "Mark a task as completed",
        inputSchema: {
            type: "object",
            properties: {
                taskId: { type: "string", description: "The task's unique ID" }
            },
            required: ["taskId"]
        }
    },
    // === MESSAGING ===
    {
        name: "volkern_send_whatsapp",
        description: "Send a WhatsApp message to a lead. Requires active WhatsApp integration.",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "ID of the lead to message" },
                mensaje: { type: "string", description: "Message content" },
                tipo: {
                    type: "string",
                    enum: ["texto", "imagen", "documento"],
                    description: "Message type (default: texto)"
                }
            },
            required: ["leadId", "mensaje"]
        }
    },
    {
        name: "volkern_list_conversaciones",
        description: "List WhatsApp conversations, optionally filtered by lead",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "Filter by lead ID" },
                page: { type: "number" },
                limit: { type: "number" }
            }
        }
    },
    // === INTERACTIONS ===
    {
        name: "volkern_list_interactions",
        description: "List all interactions for a specific lead",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "ID of the lead" }
            },
            required: ["leadId"]
        }
    },
    {
        name: "volkern_create_interaction",
        description: "Log an interaction (call, email, meeting) with a lead",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "ID of the lead" },
                tipo: {
                    type: "string",
                    enum: ["llamada", "email", "whatsapp", "reunion", "nota", "otro"],
                    description: "Interaction type"
                },
                contenido: { type: "string", description: "Interaction summary/content" },
                resultado: {
                    type: "string",
                    enum: ["positivo", "neutro", "negativo"],
                    description: "Outcome of the interaction"
                },
                metadatos: {
                    type: "object",
                    description: "Additional metadata (e.g., call duration, meeting attendees)"
                }
            },
            required: ["leadId", "tipo", "contenido"]
        }
    },
    // === NOTES ===
    {
        name: "volkern_list_notes",
        description: "List all notes for a specific lead",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "ID of the lead" }
            },
            required: ["leadId"]
        }
    },
    {
        name: "volkern_create_note",
        description: "Create a note for a lead",
        inputSchema: {
            type: "object",
            properties: {
                leadId: { type: "string", description: "ID of the lead" },
                contenido: { type: "string", description: "Note content" },
                titulo: { type: "string", description: "Optional note title" }
            },
            required: ["leadId", "contenido"]
        }
    }
];
// ============================================
// Tool Handlers
// ============================================
async function handleToolCall(name, args) {
    switch (name) {
        // LEADS
        case "volkern_list_leads": {
            const params = new URLSearchParams();
            if (args.estado)
                params.append("estado", String(args.estado));
            if (args.canal)
                params.append("canal", String(args.canal));
            if (args.search)
                params.append("search", String(args.search));
            if (args.page)
                params.append("page", String(args.page));
            if (args.limit)
                params.append("limit", String(args.limit));
            return volkernRequest(`/leads?${params.toString()}`);
        }
        case "volkern_get_lead":
            return volkernRequest(`/leads/${args.leadId}`);
        case "volkern_create_lead":
            return volkernRequest("/leads", "POST", args);
        case "volkern_update_lead": {
            const { leadId, ...data } = args;
            return volkernRequest(`/leads/${leadId}`, "PATCH", data);
        }
        // APPOINTMENTS
        case "volkern_check_disponibilidad": {
            const params = new URLSearchParams();
            params.append("fecha", String(args.fecha));
            if (args.duracion)
                params.append("duracion", String(args.duracion));
            return volkernRequest(`/citas/disponibilidad?${params.toString()}`);
        }
        case "volkern_list_citas": {
            const params = new URLSearchParams();
            if (args.estado)
                params.append("estado", String(args.estado));
            if (args.tipo)
                params.append("tipo", String(args.tipo));
            if (args.fecha)
                params.append("fecha", String(args.fecha));
            if (args.fechaInicio)
                params.append("fechaInicio", String(args.fechaInicio));
            if (args.fechaFin)
                params.append("fechaFin", String(args.fechaFin));
            return volkernRequest(`/citas?${params.toString()}`);
        }
        case "volkern_create_cita":
            return volkernRequest("/citas", "POST", args);
        case "volkern_update_cita": {
            const { citaId, ...data } = args;
            return volkernRequest(`/citas/${citaId}`, "PATCH", data);
        }
        case "volkern_cita_accion":
            return volkernRequest("/citas/accion", "POST", args);
        // CATALOG (ENHANCED)
        case "volkern_list_catalogo": {
            const params = new URLSearchParams();
            if (args.tipo)
                params.append("tipo", String(args.tipo));
            if (args.activo !== undefined)
                params.append("activo", String(args.activo));
            if (args.categoria)
                params.append("categoria", String(args.categoria));
            if (args.etiqueta)
                params.append("etiqueta", String(args.etiqueta));
            if (args.search)
                params.append("search", String(args.search));
            if (args.page)
                params.append("page", String(args.page));
            if (args.limit)
                params.append("limit", String(args.limit));
            return volkernRequest(`/catalogo?${params.toString()}`);
        }
        case "volkern_get_catalogo_item":
            return volkernRequest(`/catalogo/${args.itemId}`);
        case "volkern_create_catalogo_item":
            return volkernRequest("/catalogo", "POST", args);
        case "volkern_update_catalogo_item": {
            const { itemId, ...data } = args;
            return volkernRequest(`/catalogo/${itemId}`, "PATCH", data);
        }
        case "volkern_search_catalogo": {
            const params = new URLSearchParams();
            params.append("search", String(args.query));
            if (args.tipo)
                params.append("tipo", String(args.tipo));
            if (args.limit)
                params.append("limit", String(args.limit));
            return volkernRequest(`/catalogo?${params.toString()}`);
        }
        // SERVICES (LEGACY)
        case "volkern_list_servicios": {
            const params = new URLSearchParams();
            if (args.activo !== undefined)
                params.append("activo", String(args.activo));
            return volkernRequest(`/servicios?${params.toString()}`);
        }
        case "volkern_get_servicio":
            return volkernRequest(`/servicios/${args.servicioId}`);
        // TASKS
        case "volkern_create_task": {
            const { leadId, ...taskData } = args;
            return volkernRequest(`/leads/${leadId}/tasks`, "POST", taskData);
        }
        case "volkern_list_tasks":
            return volkernRequest(`/leads/${args.leadId}/tasks`);
        case "volkern_complete_task":
            return volkernRequest(`/tasks/${args.taskId}`, "PATCH", { completada: true });
        // MESSAGING
        case "volkern_send_whatsapp":
            return volkernRequest("/mensajes/enviar", "POST", args);
        case "volkern_list_conversaciones": {
            const params = new URLSearchParams();
            if (args.leadId)
                params.append("leadId", String(args.leadId));
            if (args.page)
                params.append("page", String(args.page));
            if (args.limit)
                params.append("limit", String(args.limit));
            return volkernRequest(`/mensajes/conversaciones?${params.toString()}`);
        }
        // INTERACTIONS
        case "volkern_list_interactions":
            return volkernRequest(`/leads/${args.leadId}/interactions`);
        case "volkern_create_interaction": {
            const { leadId, ...interactionData } = args;
            return volkernRequest(`/leads/${leadId}/interactions`, "POST", interactionData);
        }
        // NOTES
        case "volkern_list_notes":
            return volkernRequest(`/leads/${args.leadId}/notes`);
        case "volkern_create_note": {
            const { leadId: noteLeadId, ...noteData } = args;
            return volkernRequest(`/leads/${noteLeadId}/notes`, "POST", noteData);
        }
        default:
            throw new Error(`Unknown tool: ${name}`);
    }
}
// ============================================
// Server Setup
// ============================================
const server = new Server({
    name: "volkern-mcp-server",
    version: "1.0.0",
}, {
    capabilities: {
        tools: {},
    },
});
// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools };
});
// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    try {
        const result = await handleToolCall(name, args);
        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify(result, null, 2),
                },
            ],
        };
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return {
            content: [
                {
                    type: "text",
                    text: `Error: ${errorMessage}`,
                },
            ],
            isError: true,
        };
    }
});
// Start server
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Volkern MCP Server running on stdio");
}
main().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
});
