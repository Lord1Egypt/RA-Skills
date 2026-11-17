// Textos del reporte (es / en). Se mantienen juntos para que ambos idiomas digan lo mismo.
import { fmtInt, fmtUsd } from './util.mjs';

const nf = (n, lang) => fmtInt(n, lang);
const usd = (n) => fmtUsd(n);
const range = (a, b) => (Math.round(a) === Math.round(b) ? usd(a) : `${usd(a)}–${usd(b)}`);
const every = (min) => {
  if (!Number.isFinite(min)) return '?';
  const m = Math.round(min * 10) / 10;
  return m % 60 === 0 && m >= 60 ? `${m / 60} h` : `${m} min`;
};
const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
const list = (arr, max = 8) => (arr.length > max ? `${arr.slice(0, max).join(', ')}…` : arr.join(', '));
const files = (items) => [...new Set(items.map((i) => i.data.file))];

const SIGNAL = {
  es: {
    'exfiltrate-secrets': 'pide enviar credenciales',
    'conceal-from-owner': 'pide ocultarle algo al dueño',
    'remote-exec': 'descarga y ejecuta código remoto',
    'override-rules': 'intenta anular reglas anteriores',
    'override-persona': 'intenta cambiar la identidad del agente',
    'fake-system-block': 'imita un bloque de instrucciones del sistema',
    'hidden-characters': 'caracteres invisibles',
  },
  en: {
    'exfiltrate-secrets': 'asks to send credentials out',
    'conceal-from-owner': 'asks to hide something from the owner',
    'remote-exec': 'downloads and runs remote code',
    'override-rules': 'tries to override earlier rules',
    'override-persona': 'tries to change the agent identity',
    'fake-system-block': 'imitates a system-instructions block',
    'hidden-characters': 'invisible characters',
  },
};

// Cómo espaciar o abaratar una tarea programada en cada plataforma.
const SCHEDULE_FIX = {
  es: {
    hermes: (d) => `Espacia esa tarea con hermes cron edit (por ejemplo "every 2h") o pásala a un modelo barato con hermes config set cron.model <modelo>.`,
    nanobot: (d) => (d.kind === 'heartbeat' ? 'En config.json sube gateway.heartbeat.intervalS (3600 = cada hora) o quita de HEARTBEAT.md las tareas que ya no necesitas.' : 'Espacia o borra esa tarea desde tu chat con la herramienta cron.'),
    picoclaw: () => 'En config.json sube heartbeat.interval (en minutos; 60 = cada hora) o deja en HEARTBEAT.md solo las tareas que sigues necesitando.',
    zeroclaw: () => 'En config.toml, en [heartbeat], sube interval_minutes (60 = cada hora) o activa adaptive = true.',
    default: () => 'Espacia esa tarea o pásala a un modelo más barato.',
  },
  en: {
    hermes: () => 'Space that job out with hermes cron edit (for example "every 2h") or move it to a cheap model with hermes config set cron.model <model>.',
    nanobot: (d) => (d.kind === 'heartbeat' ? 'In config.json raise gateway.heartbeat.intervalS (3600 = hourly) or remove from HEARTBEAT.md the tasks you no longer need.' : 'Space out or delete that job from your chat with the cron tool.'),
    picoclaw: () => 'In config.json raise heartbeat.interval (minutes; 60 = hourly) or keep only the tasks you still need in HEARTBEAT.md.',
    zeroclaw: () => 'In config.toml, under [heartbeat], raise interval_minutes (60 = hourly) or set adaptive = true.',
    default: () => 'Space that job out or move it to a cheaper model.',
  },
};

const PLATFORM_LIST = 'OpenClaw, Hermes Agent, nanobot, PicoClaw, ZeroClaw, NanoClaw';

export const STR = {
  es: {
    lang: 'es',
    sev: { high: 'ALTO', medium: 'MEDIO', low: 'BAJO', info: 'INFO' },
    header: (v) => `PSYSEAL SCAN v${v} — revisión local: lee tus archivos, no sube nada y no modifica nada`,
    installLine: (inst, billing) =>
      inst.platform === 'openclaw'
        ? `${inst.name} · config: ${inst.configPath} (${inst.configFound ? 'leída' : 'no encontrada; uso valores por defecto'}) · Anthropic se factura: ${{ api: 'por API', subscription: 'por suscripción', mixed: 'mixto', unknown: 'sin datos (asumo API)' }[billing] || 'sin datos'}`
        : `${inst.platform === 'generic' ? 'Carpeta de agente' : inst.name} · ${inst.root}`,
    agentLine: (a) => `Agente: ${a.id} (${a.platform === 'generic' ? 'Carpeta de agente' : a.platformName}) · Modelo: ${a.model || 'sin definir'} · Carpeta: ${a.workspace}`,
    secBoot: '1) Lo que tu agente carga en cada mensaje',
    secBootGeneric: '1) Archivos de instrucciones y memoria encontrados',
    colFile: 'Archivo',
    colChars: 'Caracteres',
    colTokens: '≈Tokens',
    colCap: 'Tope',
    colState: 'Estado',
    stOk: 'ok',
    stMissing: '—',
    stNotEveryTurn: 'no en cada mensaje',
    stFill: (pct) => `${pct}% lleno`,
    stTrunc: (lost) => `RECORTADO (se pierden ${lost})`,
    stCutTotal: 'recortado por tope total',
    stNear: 'cerca del tope',
    noBootFiles: 'sin archivos de instrucciones ni memoria',
    bootTotal: (tok, chars) => `Total que entra ≈ ${tok} tokens (${chars} caracteres) en cada mensaje. El prompt del sistema, las herramientas y las skills suman más.`,
    bootTotalGeneric: (n) => `${plural(n, 'archivo revisado', 'archivos revisados')}. Sin conocer la plataforma no sé cuáles entran en cada mensaje, así que no estimo costos.`,
    secHb: '2) Latido (heartbeat)',
    secSchedules: '2) Tareas programadas',
    noSchedules: 'Sin tareas programadas activas.',
    scheduleSqlite: 'Las tareas programadas de esta plataforma viven en su base de datos; no se revisan.',
    scheduleLine: (s) => {
      const name = s.kind === 'heartbeat' ? 'Latido' : `Tarea "${s.name}"`;
      if (!s.active) return `${name} · cada ${every(s.everyMin)} · sin tareas pendientes: hoy no despierta al agente.`;
      const money = s.cost.monthUsd !== null ? ` · ≈ ${usd(s.cost.monthUsd)} al mes (sin contar caché)` : '';
      return `${name} · cada ${every(s.everyMin)} (${s.runsPerDay} al día) · ≈ ${nf(s.cost.perRunTokens, 'es')} tokens por corrida${money}`;
    },
    scheduleNote: 'Estimación por corrida: lo que entra en cada mensaje + ≈3,000 tokens de sistema y herramientas. Las tareas que leen conversación o archivos grandes cuestan más.',
    hbOff: {
      'not-owner': 'Este agente no corre latidos (otro agente tiene bloque heartbeat, o no es el agente dueño).',
      'cron-disabled': 'Los latidos programados están apagados (cron.enabled=false).',
      'every-zero': 'Latido desactivado (every: 0m).',
      'zero-width-window': 'activeHours tiene inicio igual a fin: el latido nunca corre.',
    },
    hbLine: (p, e) =>
      `Corre cada ${every(p.everyMin)} (${p.runsPerDay} veces al día) con ${e.modelRef || 'modelo sin definir'} · caché: ${e.retention.value ?? 'desconocido'}${e.retention.explicit ? '' : e.retention.viaEnv ? ' (OPENCLAW_CACHE_RETENTION)' : ' (por defecto)'}`,
    hbNow: (e) =>
      e.state.isolatedSession
        ? `Hoy cada latido corre aislado${e.state.lightContext ? ' y ligero: ya estás en lo más barato.' : ' pero aún carga los archivos de arranque.'}`
        : 'Hoy cada latido reenvía la conversación completa de tu sesión principal.' + (e.retention.value === 'short' && e.everyMin > 5 ? ' Como el caché dura 5 min, cada vez se reescribe.' : ''),
    hbTableHead: (priced) => (priced ? ['Tu sesión principal', 'Hoy / mes', 'A) aislar', 'B) caché largo'] : ['Tu sesión principal', 'Tokens por latido hoy', 'Con A) aislar', '']),
    hbTokens: (n) => `${nf(n, 'es')} tokens`,
    hbNoteLevers: 'A y B se solapan: elige una (no se suman). Son estimaciones con supuestos, no promesas.',
    hbNoteSession: 'Si no pasas --session-tokens, muestro 3 tamaños posibles. Para tu número real corre /context en tu chat y usa --session-tokens <n>.',
    hbSubscription: 'Pagas por suscripción: no hay costo por token, pero el latido sí gasta tu cuota; la columna muestra tokens, no dólares.',
    hbUnpriced: (m) => `No conozco el precio de ${m || 'tu modelo'}: muestro tokens, no dólares (puedes pasar --price entrada,salida,lectura,escritura en USD por millón).`,
    secFindings: '3) Hallazgos',
    noFindings: 'Sin hallazgos importantes.',
    secFirst: '4) Qué haría primero',
    secUsage: '5) Tu gasto real registrado',
    usageUnrecognized: 'No reconocí el formato del archivo de uso. Genera uno con: openclaw gateway usage-cost --days 30 --json > uso.json',
    usageLine: (u) => `Últimos ${u.days || '?'} días: $${u.totalCost.toFixed(2)}${u.monthlyProjection !== null ? ` → ≈ ${usd(u.monthlyProjection)} al mes` : ''}`,
    usageMix: (s) => `Reparto: entrada ${Math.round(s.input * 100)}% · salida ${Math.round(s.output * 100)}% · lectura de caché ${Math.round(s.cacheRead * 100)}% · escritura de caché ${Math.round(s.cacheWrite * 100)}%`,
    usageCacheWrite: 'Más de la mitad del gasto son ESCRITURAS de caché: el contexto se reescribe en vez de reutilizarse. Suele pasar con latidos largos y caché de 5 min.',
    usageHit: (r) => `Solo ${Math.round(r * 100)}% de tu prompt viene del caché.`,
    usageMissing: (n) => `${n} registros no tienen precio: el total real es mayor.`,
    usageIncomplete: (s) => `OpenClaw marca los totales como ${s}: vuelve a correr el comando en un rato.`,
    footerEstimates: (date) => `Estimaciones: ~4 caracteres por token; precios de lista públicos del proveedor del modelo al ${date}.`,
    footerVerify: 'Para verificar con tus números: /context list, /usage cost, openclaw gateway usage-cost --json.',
    footerVerifyGeneric: 'Para verificar con tus números, compáralo con el panel de uso de tu proveedor.',
    footerPrivacy: 'Privacidad: este escaneo no usa red, no escribe archivos y nunca imprime el contenido de tu memoria ni tus credenciales (solo archivo, línea y tipo).',
    notFound: (d) => [
      `No encontré ningún agente en esta computadora (busqué ${PLATFORM_LIST}).`,
      'Si lo usas en otro lugar:',
      ...(d.platform === 'win32'
        ? ['  - Dentro de WSL2: corre el escáner dentro de esa distribución de Linux. Desde Windows, esa carpeta se ve como \\\\wsl.localhost\\<distro>\\home\\<usuario>.']
        : []),
      '  - En un servidor (VPS): corre el escáner en ese servidor; así tus archivos no salen de ahí.',
      '  - Si está en otra carpeta: pasa --path <carpeta de tu agente>. Si es otra plataforma, el escáner revisa credenciales, instrucciones sospechosas y memoria inflada.',
    ],
    cta: (name, url, fixable) =>
      fixable > 0
        ? `${name} puede arreglar ${plural(fixable, 'de estos hallazgos', 'de estos hallazgos')} por ti, con respaldo y tu aprobación en cada cambio: ${url}`
        : `Tu agente salió bien. Muéstralo con el sello firmado de ${name}: ${url}`,
    f: {
      'secret.exposed': (items) => ({
        head: `${items.length} credencial(es) en texto plano en ${list(files(items), 4)}: ${list(items.map((i) => `${i.data.file}:${i.data.line} (${i.data.type})`), 6)}`,
        fix: 'Rota AHORA, en el proveedor, las claves marcadas (si estuvieron en un archivo que el agente lee, asúmelas comprometidas), borra esas líneas y guarda las claves donde tu plataforma guarda credenciales (.env o variables de entorno).',
      }),
      'config.secret_plaintext': (items) => ({
        head: `Credencial(es) en texto plano dentro de la configuración: ${list(items.map((i) => `${i.data.path} (${i.data.type})`), 6)}`,
        fix: 'En openclaw.json, sustituye esos valores en texto plano por ${NOMBRE_DE_VARIABLE} o un SecretRef.',
      }),
      'inject.critical': (items) => ({
        head: `Texto que parece una orden peligrosa en ${list(items.map((i) => `${i.data.file}:${i.data.line} (${SIGNAL.es[i.data.signal] || i.data.signal})`), 5)}`,
        fix: 'Abre las líneas marcadas. Si no las escribiste tú, bórralas y averigua por dónde entraron (página web, mensaje, herramienta). Este escaneo no muestra el texto para no reinyectarlo en tu agente.',
      }),
      'inject.override': (items) => ({
        head: `Texto que intenta reescribir las reglas del agente en ${list(items.map((i) => `${i.data.file}:${i.data.line}`), 6)}`,
        fix: 'Revisa el texto marcado: si lo escribiste tú, déjalo; si vino de contenido externo, bórralo (es la forma típica de "envenenar" la memoria).',
      }),
      'inject.hidden': (items) => ({
        head: `Caracteres invisibles (se usan para esconder instrucciones) en ${list(items.map((i) => `${i.data.file}:${i.data.line}`), 6)}`,
        fix: 'Reescribe a mano o borra las líneas con caracteres invisibles: no se ven al abrir el archivo.',
      }),
      'bootstrap.file_truncated': (items) => ({
        head: items.map((i) => `${i.data.file} mide ${nf(i.data.chars, 'es')} caracteres y el tope es ${nf(i.data.cap, 'es')}: al agente solo le llegan los primeros ${nf(i.data.cap, 'es')}; se pierden ${nf(i.data.lostChars, 'es')}`).join('\n    '),
        fix: 'Resume lo duradero y mueve el detalle a un archivo que el agente consulte cuando lo necesite. Subir el tope también sube el costo de cada mensaje.',
      }),
      'bootstrap.file_cut_by_total': (items) => ({
        head: `Entran recortados por el tope total de arranque: ${list(files(items))}`,
        fix: 'Acorta los archivos más grandes o sube agents.defaults.bootstrapTotalMaxChars sabiendo que cuesta tokens en cada mensaje.',
      }),
      'bootstrap.near_cap': (items) => ({
        head: `Cerca del tope (empezarán a recortarse): ${list(items.map((i) => `${i.data.file} ${nf(i.data.chars, 'es')}/${nf(i.data.cap, 'es')}`))}`,
        fix: 'Resume los archivos cercanos al tope antes de que se corten sin avisar.',
      }),
      'bootstrap.leftover': (items) => ({
        head: `BOOTSTRAP.md sigue en el workspace (≈${nf(items[0].data.tokens, 'es')} tokens por mensaje): es el ritual de primer arranque.`,
        fix: 'Si ya terminaste la configuración inicial, borra BOOTSTRAP.md.',
      }),
      'bootstrap.legacy_files': (items) => ({
        head: `Archivos de versiones anteriores: ${list(items[0].data.files)}`,
        fix: 'Corre openclaw doctor --fix. En OpenClaw 2026.9+ HEARTBEAT.md ya no se lee en ejecución, memory.md en minúscula nunca se inyecta y TOOLS.md se mezcla en la sección ## Tools de AGENTS.md.',
      }),
      'weight.heavy_file': (items) => ({
        head: `Archivos grandes que entran completos en cada mensaje: ${list(items.map((i) => `${i.data.file} (≈${nf(i.data.tokens, 'es')} tokens)`))}`,
        fix: 'Deja en esos archivos solo lo que el agente necesita siempre; el resto muévelo a un archivo que consulte cuando haga falta.',
      }),
      'memory.near_full': (items) => ({
        head: `Memoria casi llena: ${list(items.map((i) => `${i.data.file} ${i.data.pct}% (${nf(i.data.chars, 'es')}/${nf(i.data.cap, 'es')})`))}. Al llenarse, el agente gasta turnos borrando para poder guardar.`,
        fix: 'Junta entradas parecidas y borra las que ya no sirven para dejar espacio.',
      }),
      'memory.over_limit': (items) => ({
        head: `Memoria por encima de su límite: ${list(items.map((i) => `${i.data.file} ${nf(i.data.chars, 'es')}/${nf(i.data.cap, 'es')}`))}`,
        fix: 'Recorta ese archivo por debajo del límite; si no, el agente no podrá guardar nada nuevo.',
      }),
      'perm.secret_file_open': (items) => ({
        head: `Archivos con credenciales que otros usuarios de la máquina pueden leer: ${list(items.map((i) => `${i.data.file} (permisos ${i.data.mode})`))}`,
        fix: 'Déjalos solo para tu usuario: chmod 600 <archivo>.',
      }),
      'schedule.frequent': (items) => ({
        head: items
          .map((i) => {
            const d = i.data;
            const money = d.monthUsd !== null && d.monthUsd !== undefined ? `, ≈ ${usd(d.monthUsd)} al mes` : '';
            return `${d.kind === 'heartbeat' ? 'El latido' : `La tarea "${d.name}"`} corre ${d.runsPerDay} veces al día (≈ ${nf(d.perRunTokens, 'es')} tokens por corrida${money}).`;
          })
          .join('\n    '),
        fix: (SCHEDULE_FIX.es[items[0].data.platform] || SCHEDULE_FIX.es.default)(items[0].data),
      }),
      'schedule.unreadable': (items) => ({ head: `No pude leer ${items[0].data.file}; no revisé esas tareas.`, fix: null }),
      'memory.bloat': (items) => {
        const d = items[0].data;
        const val = d.perThousandCalls ? ` Quitarlo ahorra ≈${usd(d.perThousandCalls.per1000Hit)}–${usd(d.perThousandCalls.per1000Miss)} por cada 1,000 llamadas.` : '';
        return {
          head: `${d.file} tiene ≈${nf(d.reclaimableTokens, 'es')} tokens recuperables (${plural(d.dupLines, 'línea repetida', 'líneas repetidas')}, ${plural(d.blobLines, 'línea gigante', 'líneas gigantes')}, ${plural(d.bigFences, 'bloque de código largo', 'bloques de código largos')}).${val}`,
          fix: 'Deja en la memoria solo hechos duraderos: borra lo repetido y saca los volcados largos a un archivo aparte.',
        };
      },
      'heartbeat.full_history': (items) => {
        const d = items[0].data;
        const save = d.priced && d.savingHigh > 0 ? ` Ahorro posible ≈${range(d.savingLow, d.savingHigh)} al mes (según el tamaño de tu sesión).` : '';
        return {
          head: `Cada latido (cada ${every(d.everyMin)}, ${d.runsPerDay} al día) viaja con toda la conversación de tu sesión principal.${save}`,
          fix: 'En openclaw.json: agents.defaults.heartbeat = { isolatedSession: true, lightContext: true }. Efecto: el latido ya no ve la conversación reciente ni los archivos de arranque; si tu latido los necesita, no lo actives. Verifica después con openclaw system heartbeat last.',
        };
      },
      'heartbeat.cache_expires': (items) => {
        const d = items[0].data;
        return {
          head: `El caché de 5 min${d.explicit ? '' : ' (por defecto)'} caduca entre latidos de ${every(d.everyMin)}: cada latido reescribe todo el contexto (a 1.25× el precio de entrada).`,
          fix: d.canFix
            ? 'Prueba cacheRetention: "long" (1 h) para ese modelo: agents.defaults.models["proveedor/modelo"].params.cacheRetention. Escribir cuesta 2× la entrada, pero se amortiza porque el latido lo renueva antes de que expire.'
            : 'Con una cadencia mayor a 1 h el caché largo tampoco sirve; baja heartbeat.every a 55m o menos si quieres mantenerlo tibio, o aísla el latido.',
        };
      },
      'heartbeat.bootstrap_each_run': (items) => ({
        head: `Cada latido aislado aún carga ≈${nf(items[0].data.tokens, 'es')} tokens de archivos de arranque.`,
        fix: 'Con heartbeat.lightContext: true los latidos omiten los archivos de arranque.',
      }),
      'heartbeat.expensive_model': (items) => ({
        head: `El latido usa ${items[0].data.model}; ${items[0].data.cheaper} cuesta ≈${items[0].data.ratio}× menos por token de entrada.`,
        fix: 'El latido casi siempre responde NO_REPLY. Si tu tarea de latido es simple, define agents.defaults.heartbeat.model con un modelo barato y prueba que siga funcionando.',
      }),
      'heartbeat.no_active_hours': (items) => ({
        head: `El latido corre las 24 h (${items[0].data.runsPerDay} al día).`,
        fix: 'Con heartbeat.activeHours = { start: "08:00", end: "22:00" } corres ≈40% menos latidos.',
      }),
      'heartbeat.invalid_every': () => ({ head: 'heartbeat.every no es una duración válida; asumí 30 min.', fix: 'Usa un valor como "30m" o "1h".' }),
      'heartbeat.price_unknown': () => ({ head: null, fix: null }),
      'heartbeat.disabled': () => ({ head: null, fix: null }),
      'harness.codex': () => ({ head: 'Este agente usa el arnés nativo de Codex: MEMORY.md puede no pegarse en cada mensaje, así que los tokens de arranque son un máximo.', fix: null }),
      'agent.not_found': (items) => ({ head: `No existe el agente "${items[0].data.id}". Agentes disponibles: ${items[0].data.available.join(', ') || '(ninguno)'}.`, fix: 'Usa --agent con uno de esos ids, o quita --agent para revisar todos.' }),
      'config.missing': (items) => ({ head: `No encontré ${items[0].data.path}; usé los valores por defecto de OpenClaw.`, fix: 'Si tu config está en otro lado, pasa --config <ruta> o define OPENCLAW_CONFIG_PATH.' }),
      'config.error': (items) => ({ head: `No pude leer ${items[0].data.path}: ${items[0].data.error}`, fix: 'Revisa la sintaxis del archivo (JSON5).' }),
      'config.include_warnings': (items) => ({ head: `Avisos al resolver $include: ${list(items[0].data.warnings, 5)}`, fix: null }),
      'platform.generic': () => ({ head: 'No reconocí la plataforma de esta carpeta: reviso credenciales, instrucciones sospechosas y memoria inflada, sin estimar costos.', fix: null }),
      'platform.no_agents': (items) => ({ head: `Encontré ${items[0].data.platform} en ${items[0].data.root}, pero sin agentes configurados.`, fix: null }),
      'platform.read_error': (items) => ({ head: `No pude leer ${items[0].data.platform} en ${items[0].data.root}: ${items[0].data.error}`, fix: null }),
    },
  },
  en: {
    lang: 'en',
    sev: { high: 'HIGH', medium: 'MEDIUM', low: 'LOW', info: 'INFO' },
    header: (v) => `PSYSEAL SCAN v${v} — local review: reads your files, uploads nothing, changes nothing`,
    installLine: (inst, billing) =>
      inst.platform === 'openclaw'
        ? `${inst.name} · config: ${inst.configPath} (${inst.configFound ? 'read' : 'not found; using defaults'}) · Anthropic billing: ${{ api: 'API', subscription: 'subscription', mixed: 'mixed', unknown: 'unknown (assuming API)' }[billing] || 'unknown'}`
        : `${inst.platform === 'generic' ? 'Agent folder' : inst.name} · ${inst.root}`,
    agentLine: (a) => `Agent: ${a.id} (${a.platform === 'generic' ? 'Agent folder' : a.platformName}) · Model: ${a.model || 'unset'} · Folder: ${a.workspace}`,
    secBoot: '1) What your agent loads on every message',
    secBootGeneric: '1) Instruction and memory files found',
    colFile: 'File',
    colChars: 'Characters',
    colTokens: '≈Tokens',
    colCap: 'Cap',
    colState: 'Status',
    stOk: 'ok',
    stMissing: '—',
    stNotEveryTurn: 'not every message',
    stFill: (pct) => `${pct}% full`,
    stTrunc: (lost) => `TRUNCATED (${lost} lost)`,
    stCutTotal: 'cut by total cap',
    stNear: 'near the cap',
    noBootFiles: 'no instruction or memory files',
    bootTotal: (tok, chars) => `Total injected ≈ ${tok} tokens (${chars} characters) on every message. The system prompt, tools and skills add more.`,
    bootTotalGeneric: (n) => `${plural(n, 'file reviewed', 'files reviewed')}. Without knowing the platform I cannot tell which ones load on every message, so I do not estimate costs.`,
    secHb: '2) Heartbeat',
    secSchedules: '2) Scheduled tasks',
    noSchedules: 'No active scheduled tasks.',
    scheduleSqlite: "This platform keeps its scheduled tasks in its database; they are not reviewed.",
    scheduleLine: (s) => {
      const name = s.kind === 'heartbeat' ? 'Heartbeat' : `Job "${s.name}"`;
      if (!s.active) return `${name} · every ${every(s.everyMin)} · no pending tasks: it does not wake the agent today.`;
      const money = s.cost.monthUsd !== null ? ` · ≈ ${usd(s.cost.monthUsd)} per month (cache not counted)` : '';
      return `${name} · every ${every(s.everyMin)} (${s.runsPerDay} a day) · ≈ ${nf(s.cost.perRunTokens, 'en')} tokens per run${money}`;
    },
    scheduleNote: 'Per-run estimate: what loads on every message + ≈3,000 tokens of system prompt and tools. Jobs that read conversation or large files cost more.',
    hbOff: {
      'not-owner': 'This agent does not run heartbeats (another agent has a heartbeat block, or it is not the owner agent).',
      'cron-disabled': 'Scheduled heartbeats are off (cron.enabled=false).',
      'every-zero': 'Heartbeat disabled (every: 0m).',
      'zero-width-window': 'activeHours has start equal to end: the heartbeat never runs.',
    },
    hbLine: (p, e) =>
      `Runs every ${every(p.everyMin)} (${p.runsPerDay} times a day) with ${e.modelRef || 'unset model'} · cache: ${e.retention.value ?? 'unknown'}${e.retention.explicit ? '' : e.retention.viaEnv ? ' (OPENCLAW_CACHE_RETENTION)' : ' (default)'}`,
    hbNow: (e) =>
      e.state.isolatedSession
        ? `Today each heartbeat runs isolated${e.state.lightContext ? ' and light: you are already on the cheapest setup.' : ' but still loads the startup files.'}`
        : 'Today each heartbeat resends the full conversation of your main session.' + (e.retention.value === 'short' && e.everyMin > 5 ? ' Since the cache lasts 5 min, it is rewritten every time.' : ''),
    hbTableHead: (priced) => (priced ? ['Your main session', 'Today / month', 'A) isolate', 'B) long cache'] : ['Your main session', 'Tokens per heartbeat today', 'With A) isolate', '']),
    hbTokens: (n) => `${nf(n, 'en')} tokens`,
    hbNoteLevers: 'A and B overlap: pick one (they do not add up). These are estimates with stated assumptions, not promises.',
    hbNoteSession: 'Without --session-tokens I show 3 possible sizes. For your real number run /context in your chat and pass --session-tokens <n>.',
    hbSubscription: 'You pay by subscription: no per-token cost, but heartbeats do spend your quota; the column shows tokens, not dollars.',
    hbUnpriced: (m) => `I do not know the price of ${m || 'your model'}: showing tokens, not dollars (you can pass --price input,output,read,write in USD per million).`,
    secFindings: '3) Findings',
    noFindings: 'No significant findings.',
    secFirst: '4) What I would do first',
    secUsage: '5) Your recorded real spend',
    usageUnrecognized: 'I could not recognize the usage file format. Generate one with: openclaw gateway usage-cost --days 30 --json > usage.json',
    usageLine: (u) => `Last ${u.days || '?'} days: $${u.totalCost.toFixed(2)}${u.monthlyProjection !== null ? ` → ≈ ${usd(u.monthlyProjection)} per month` : ''}`,
    usageMix: (s) => `Mix: input ${Math.round(s.input * 100)}% · output ${Math.round(s.output * 100)}% · cache reads ${Math.round(s.cacheRead * 100)}% · cache writes ${Math.round(s.cacheWrite * 100)}%`,
    usageCacheWrite: 'More than half of the spend is cache WRITES: the context is rewritten instead of reused. Typical with long heartbeats and a 5-minute cache.',
    usageHit: (r) => `Only ${Math.round(r * 100)}% of your prompt comes from the cache.`,
    usageMissing: (n) => `${n} records have no price: the real total is higher.`,
    usageIncomplete: (s) => `OpenClaw marks the totals as ${s}: run the command again in a while.`,
    footerEstimates: (date) => `Estimates: ~4 characters per token; the model provider's public list prices as of ${date}.`,
    footerVerify: 'To verify with your numbers: /context list, /usage cost, openclaw gateway usage-cost --json.',
    footerVerifyGeneric: "To verify with your numbers, compare with your provider's usage dashboard.",
    footerPrivacy: 'Privacy: this scan uses no network, writes no files and never prints your memory content or credentials (only file, line and type).',
    notFound: (d) => [
      `I could not find any agent on this computer (looked for ${PLATFORM_LIST}).`,
      'If you use it somewhere else:',
      ...(d.platform === 'win32' ? ['  - Inside WSL2: run the scanner inside that Linux distribution. From Windows, that folder appears as \\\\wsl.localhost\\<distro>\\home\\<user>.'] : []),
      '  - On a server (VPS): run the scanner on that server, so your files never leave it.',
      '  - If it lives in another folder: pass --path <your agent folder>. For other platforms the scanner checks credentials, suspicious instructions and memory bloat.',
    ],
    cta: (name, url, fixable) =>
      fixable > 0
        ? `${name} can fix ${plural(fixable, 'of these findings', 'of these findings')} for you, with a backup and your approval on every change: ${url}`
        : `Your agent came out fine. Show it with a signed ${name} seal: ${url}`,
    f: {
      'secret.exposed': (items) => ({
        head: `${items.length} plaintext credential(s) in ${list(files(items), 4)}: ${list(items.map((i) => `${i.data.file}:${i.data.line} (${i.data.type})`), 6)}`,
        fix: 'Rotate NOW, at the provider, the flagged keys (if they sat in a file your agent reads, assume they are compromised), delete those lines and keep keys where your platform stores credentials (.env or environment variables).',
      }),
      'config.secret_plaintext': (items) => ({
        head: `Plaintext credential(s) inside the config: ${list(items.map((i) => `${i.data.path} (${i.data.type})`), 6)}`,
        fix: 'In openclaw.json, replace those plaintext values with ${VARIABLE_NAME} or a SecretRef.',
      }),
      'inject.critical': (items) => ({
        head: `Text that looks like a dangerous order in ${list(items.map((i) => `${i.data.file}:${i.data.line} (${SIGNAL.en[i.data.signal] || i.data.signal})`), 5)}`,
        fix: 'Open the flagged lines. If you did not write them, delete them and find out how they got in (web page, message, tool). This scan does not print the text so it cannot re-inject it into your agent.',
      }),
      'inject.override': (items) => ({
        head: `Text that tries to rewrite the agent rules in ${list(items.map((i) => `${i.data.file}:${i.data.line}`), 6)}`,
        fix: 'Review the flagged text: if you wrote it, keep it; if it came from external content, delete it (this is the classic way to poison memory).',
      }),
      'inject.hidden': (items) => ({
        head: `Invisible characters (used to hide instructions) in ${list(items.map((i) => `${i.data.file}:${i.data.line}`), 6)}`,
        fix: 'Retype or delete the lines with invisible characters: they are not visible when you open the file.',
      }),
      'bootstrap.file_truncated': (items) => ({
        head: items.map((i) => `${i.data.file} is ${nf(i.data.chars, 'en')} characters and the cap is ${nf(i.data.cap, 'en')}: the agent only gets the first ${nf(i.data.cap, 'en')}; ${nf(i.data.lostChars, 'en')} are lost`).join('\n    '),
        fix: 'Summarize durable facts and move detail to a file the agent looks up when needed. Raising the cap also raises the cost of every message.',
      }),
      'bootstrap.file_cut_by_total': (items) => ({
        head: `Cut by the total startup cap: ${list(files(items))}`,
        fix: 'Shorten the largest files or raise agents.defaults.bootstrapTotalMaxChars knowing it costs tokens on every message.',
      }),
      'bootstrap.near_cap': (items) => ({
        head: `Near the cap (will start getting cut): ${list(items.map((i) => `${i.data.file} ${nf(i.data.chars, 'en')}/${nf(i.data.cap, 'en')}`))}`,
        fix: 'Summarize the files near the cap before they get cut silently.',
      }),
      'bootstrap.leftover': (items) => ({
        head: `BOOTSTRAP.md is still in the workspace (≈${nf(items[0].data.tokens, 'en')} tokens per message): it is the first-run ritual.`,
        fix: 'If initial setup is done, delete BOOTSTRAP.md.',
      }),
      'bootstrap.legacy_files': (items) => ({
        head: `Files from earlier versions: ${list(items[0].data.files)}`,
        fix: 'Run openclaw doctor --fix. In OpenClaw 2026.9+ HEARTBEAT.md is no longer read at runtime, lowercase memory.md is never injected and TOOLS.md is merged into the ## Tools section of AGENTS.md.',
      }),
      'weight.heavy_file': (items) => ({
        head: `Large files loaded in full on every message: ${list(items.map((i) => `${i.data.file} (≈${nf(i.data.tokens, 'en')} tokens)`))}`,
        fix: 'Keep only what the agent always needs in those files; move the rest to a file it looks up when needed.',
      }),
      'memory.near_full': (items) => ({
        head: `Memory almost full: ${list(items.map((i) => `${i.data.file} ${i.data.pct}% (${nf(i.data.chars, 'en')}/${nf(i.data.cap, 'en')})`))}. Once full, the agent spends turns deleting so it can save.`,
        fix: 'Merge similar entries and delete the ones that no longer help, to free space.',
      }),
      'memory.over_limit': (items) => ({
        head: `Memory above its limit: ${list(items.map((i) => `${i.data.file} ${nf(i.data.chars, 'en')}/${nf(i.data.cap, 'en')}`))}`,
        fix: 'Trim that file below the limit; otherwise the agent cannot save anything new.',
      }),
      'perm.secret_file_open': (items) => ({
        head: `Credential files other users on this machine can read: ${list(items.map((i) => `${i.data.file} (mode ${i.data.mode})`))}`,
        fix: 'Restrict them to your user: chmod 600 <file>.',
      }),
      'schedule.frequent': (items) => ({
        head: items
          .map((i) => {
            const d = i.data;
            const money = d.monthUsd !== null && d.monthUsd !== undefined ? `, ≈ ${usd(d.monthUsd)} per month` : '';
            return `${d.kind === 'heartbeat' ? 'The heartbeat' : `Job "${d.name}"`} runs ${d.runsPerDay} times a day (≈ ${nf(d.perRunTokens, 'en')} tokens per run${money}).`;
          })
          .join('\n    '),
        fix: (SCHEDULE_FIX.en[items[0].data.platform] || SCHEDULE_FIX.en.default)(items[0].data),
      }),
      'schedule.unreadable': (items) => ({ head: `Could not read ${items[0].data.file}; those jobs were not reviewed.`, fix: null }),
      'memory.bloat': (items) => {
        const d = items[0].data;
        const val = d.perThousandCalls ? ` Removing it saves ≈${usd(d.perThousandCalls.per1000Hit)}–${usd(d.perThousandCalls.per1000Miss)} per 1,000 calls.` : '';
        return {
          head: `${d.file} has ≈${nf(d.reclaimableTokens, 'en')} reclaimable tokens (${plural(d.dupLines, 'repeated line', 'repeated lines')}, ${plural(d.blobLines, 'giant line', 'giant lines')}, ${plural(d.bigFences, 'long code block', 'long code blocks')}).${val}`,
          fix: 'Keep only durable facts in memory: delete repeats and move long dumps to a separate file.',
        };
      },
      'heartbeat.full_history': (items) => {
        const d = items[0].data;
        const save = d.priced && d.savingHigh > 0 ? ` Possible savings ≈${range(d.savingLow, d.savingHigh)} per month (depends on your session size).` : '';
        return {
          head: `Each heartbeat (every ${every(d.everyMin)}, ${d.runsPerDay} a day) carries the whole conversation of your main session.${save}`,
          fix: 'In openclaw.json: agents.defaults.heartbeat = { isolatedSession: true, lightContext: true }. Effect: the heartbeat no longer sees recent conversation or startup files; if yours needs them, do not enable it. Check afterwards with openclaw system heartbeat last.',
        };
      },
      'heartbeat.cache_expires': (items) => {
        const d = items[0].data;
        return {
          head: `The 5-minute cache${d.explicit ? '' : ' (default)'} expires between ${every(d.everyMin)} heartbeats: each one rewrites the whole context (at 1.25× the input price).`,
          fix: d.canFix
            ? 'Try cacheRetention: "long" (1 h) for that model: agents.defaults.models["provider/model"].params.cacheRetention. Writing costs 2× input, but it pays off because the heartbeat refreshes it before it expires.'
            : 'With a cadence above 1 h the long cache does not help either; lower heartbeat.every to 55m or less to keep it warm, or isolate the heartbeat.',
        };
      },
      'heartbeat.bootstrap_each_run': (items) => ({
        head: `Each isolated heartbeat still loads ≈${nf(items[0].data.tokens, 'en')} tokens of startup files.`,
        fix: 'With heartbeat.lightContext: true, heartbeats skip the startup files.',
      }),
      'heartbeat.expensive_model': (items) => ({
        head: `The heartbeat uses ${items[0].data.model}; ${items[0].data.cheaper} costs ≈${items[0].data.ratio}× less per input token.`,
        fix: 'The heartbeat almost always answers NO_REPLY. If your heartbeat task is simple, set agents.defaults.heartbeat.model to a cheap model and test that it still works.',
      }),
      'heartbeat.no_active_hours': (items) => ({
        head: `The heartbeat runs 24 h a day (${items[0].data.runsPerDay} a day).`,
        fix: 'With heartbeat.activeHours = { start: "08:00", end: "22:00" } you run ≈40% fewer heartbeats.',
      }),
      'heartbeat.invalid_every': () => ({ head: 'heartbeat.every is not a valid duration; I assumed 30 min.', fix: 'Use a value like "30m" or "1h".' }),
      'heartbeat.price_unknown': () => ({ head: null, fix: null }),
      'heartbeat.disabled': () => ({ head: null, fix: null }),
      'harness.codex': () => ({ head: 'This agent uses the native Codex harness: MEMORY.md may not be pasted every message, so startup tokens are a maximum.', fix: null }),
      'agent.not_found': (items) => ({ head: `There is no agent "${items[0].data.id}". Available agents: ${items[0].data.available.join(', ') || '(none)'}.`, fix: 'Use --agent with one of those ids, or drop --agent to review them all.' }),
      'config.missing': (items) => ({ head: `Could not find ${items[0].data.path}; used OpenClaw defaults.`, fix: 'If your config lives elsewhere, pass --config <path> or set OPENCLAW_CONFIG_PATH.' }),
      'config.error': (items) => ({ head: `Could not read ${items[0].data.path}: ${items[0].data.error}`, fix: 'Check the file syntax (JSON5).' }),
      'config.include_warnings': (items) => ({ head: `Warnings while resolving $include: ${list(items[0].data.warnings, 5)}`, fix: null }),
      'platform.generic': () => ({ head: 'I did not recognize the platform of this folder: I check credentials, suspicious instructions and memory bloat, without estimating costs.', fix: null }),
      'platform.no_agents': (items) => ({ head: `Found ${items[0].data.platform} at ${items[0].data.root}, but no configured agents.`, fix: null }),
      'platform.read_error': (items) => ({ head: `Could not read ${items[0].data.platform} at ${items[0].data.root}: ${items[0].data.error}`, fix: null }),
    },
  },
};
