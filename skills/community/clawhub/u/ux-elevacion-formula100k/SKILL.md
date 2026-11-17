---
name: ux-elevacion-formula100k
description: "Skill de elevación de UI/UX para el stack F100K (Next.js 16, Tailwind CSS, shadcn/ui). Activa cuando alguien dice /polish, /craft, /animate, /typeset, /audit-ux, /landing, o frases como \"mejora el diseño\", \"este UI se ve muy AI-looking\", \"anima esta interacción\", \"el spacing se ve raro\", \"el diseño se ve genérico\", \"añade microinteracciones\", \"quiero que se vea profesional\", \"agrega animaciones\", \"construye una landing\", \"hazlo hiper profesional\", \"necesito scroll animations\", \"agrega glow/glass/depth\", \"quiero un hero impactante\". Combina principios de Emil Kowalski (animaciones físicas), Paul Bakaus / Impeccable (7 dominios), anti-slop rules, y patterns avanzados de landings: scroll reveal, bento grid, profundidad visual."
allowed-tools: "Bash, Read, Write, Edit"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Es para mejorar el diseño de una app o landing (Next.js, Tailwind, shadcn). Solo aplica si la usuaria tiene el código en este servidor o te pasa los archivos.
> - Si pide revisar una página publicada, pide capturas o el link y responde con la lista de cambios concretos; no despliegues nada ni hagas push sin su ✅.

---

# UX Elevación — F100K Stack

Principios de diseño de producción para Next.js 16 + Tailwind CSS + shadcn/ui. Estos no son
sugerencias: son invariantes que separan UI mediocre de UI que comunica confianza y craftmanship.

---

## Cuándo activar

### Comandos explícitos
- `/polish` — revisión pre-commit/pre-deploy de un componente o página
- `/craft` — construir un componente nuevo con máxima calidad desde cero
- `/animate` — agregar o mejorar animaciones en un componente existente
- `/typeset` — auditar y corregir la tipografía
- `/audit-ux` — auditoría completa de la UI actual (todos los dominios)
- `/landing` — checklist completo de alto impacto para landing pages

### Frases naturales (activación implícita)
- "mejora el diseño de este componente"
- "este UI se ve muy AI-looking" / "se ve genérico" / "parece un template"
- "anima esta interacción" / "agrega microinteracciones"
- "el spacing se ve raro" / "hay demasiado/poco espacio"
- "la tipografía no está bien" / "los textos no tienen jerarquía"
- "algo en este diseño se siente mal"
- "revisa antes de hacer el PR"
- "quiero que se vea hiper profesional" / "que impresione"
- "agrega scroll animations" / "que los elementos entren al hacer scroll"
- "agrega glow" / "quiero profundidad visual" / "hazlo menos plano"
- "necesito un hero impactante" / "construye la landing"
- "agrega contadores animados" / "que los números aparezcan con animación"

---

## Guía para alumnas — Cómo pedir sin saber diseño

Si no sabes los términos técnicos, usa esta sección. Describe lo que sientes y encuentra
el prompt exacto que debes escribirle a Claude.

### "Se ve feo / genérico / parece hecho por IA"

```
"Mejora el diseño de esta página. Se ve muy genérico, como un template de IA.
Quiero que se vea profesional y con personalidad propia."
```

### "Se ve muy simple / le falta algo / muy plano"

```
"Esta página se ve muy plana. Agrega profundidad visual: sombras, capas,
efectos de fondo. Que se sienta que hay dimensión, no todo al mismo nivel."
```

### "No se ve moderno / parece de hace 10 años"

```
"Moderniza el diseño. Quiero que se vea como una app/landing de 2025:
oscura, con bordes sutiles, tipografía grande y animaciones suaves."
```

### "Los botones / elementos no se sienten bien"

```
"Mejora los botones y elementos interactivos. Que cuando haga hover o clic
se sientan responsivos y con vida, no estáticos."
```

### "Quiero que impresione desde el primer segundo"

```
"Rediseña el hero (la primera pantalla que ve el usuario). Quiero que impresione
inmediatamente: headline poderoso, fondo con profundidad, animaciones de entrada.
Que en 3 segundos quede claro qué es y por qué me importa."
```

### "Los textos no se ven bien / no hay jerarquía"

```
"El texto no tiene jerarquía visual. El título debería verse como título,
el subtítulo como subtítulo, y el cuerpo como cuerpo. Corrígelo con
tamaños, pesos y espaciados correctos."
```

### "Quiero agregar animaciones pero no sé cuáles"

```
"Agrega animaciones profesionales a esta página/componente. Que los elementos
entren suavemente al hacer scroll, que los botones respondan al toque,
y que las transiciones se sientan físicas y naturales."
```

### "Quiero que los elementos aparezcan mientras hago scroll"

```
"Agrega scroll animations: que cada sección y sus elementos aparezcan
con una animación suave cuando el usuario llega a esa parte de la página.
Efecto de fade+slide hacia arriba, escalonado entre elementos."
```

### "Quiero mostrar mis números / stats de forma llamativa"

```
"Crea una sección de estadísticas con contadores animados. Que los números
cuenten desde 0 hasta el valor real cuando el usuario llega a esa sección.
Usar: [tus números reales aquí]"
```

### "Quiero una sección que muestre mis features de forma visual"

```
"Crea una sección de features en formato bento grid: cards de distintos
tamaños que muestren cada función del producto con un visual dentro.
Estilo oscuro, bordes sutiles, hover effect."
```

### "Quiero agregar testimonios / reviews de mis clientes"

```
"Diseña una sección de testimonios profesional. Cards con el texto del
testimonio, foto, nombre y cargo. Estilo oscuro, sobrio, que transmita
confianza. Los testimonios son: [pega tus testimonios reales]"
```

### "La paleta de colores se ve mal / no combina"

```
"La paleta de colores no funciona. Quiero un sistema coherente:
un color de acento principal [di qué color quieres], neutros oscuros para
el fondo, y blancos/grises para el texto. Aplícalo a todo el componente."
```

### Plantilla universal — cuando no sabes qué decir exactamente

Si no encuentras tu caso arriba, usa esta plantilla y rellena los espacios:

```
"Este [componente/página/sección] se ve [problema que percibes].
Quiero que [resultado que buscas].
El estilo debe ser [oscuro/claro/moderno/profesional/minimalista].
La paleta de colores es [colores principales que ya tienes]."
```

---

## Los 3 Diales de Calidad

Antes de cualquier intervención de diseño, calibra estos tres diales según el contexto del
producto. No hay valores correctos absolutos — hay valores coherentes con el propósito.

### VARIANCE — Contraste visual del layout
¿Cuánto contraste hay entre elementos? Un dial bajo crea uniformidad (apropiado para apps de
productividad, dashboards densos). Un dial alto crea drama visual (apropiado para landing pages,
marketing, hero sections).

| Dial | Cuándo | Señales |
|------|--------|---------|
| Bajo | Dashboards, forms, tablas de datos | Mismo tamaño tipográfico, poco contraste entre secciones |
| Medio | Apps SaaS, páginas de feature | 2-3 tamaños tipográficos, 1 elemento featured |
| Alto | Landings, hero, onboarding | Contraste extremo de tamaño, 1 elemento dominante por pantalla |

### MOTION — Intensidad de animación
¿Cuánta vida tienen los elementos? Motion bajo = austero, professional. Motion alto = expresivo,
memorable. El error más común es motion alto en contextos que piden bajo.

| Dial | Cuándo |
|------|--------|
| Bajo | Forms, tablas, dashboards de datos, acciones críticas |
| Medio | Apps de productividad, modales, transiciones de estado |
| Alto | Landings, onboarding, celebraciones, confirmaciones de éxito |

### DENSITY — Espaciado / contenido
¿Cuánto respira el diseño? Density alto = información densa (apropiado para power users, tablas).
Density bajo = espaciado premium (apropiado para marketing, landings, primera impresión).

**Regla:** cuando tengas duda, aumenta el espaciado. Casi siempre hay poco, nunca demasiado.

---

## Comando `/polish`

Checklist de 15 puntos para revisión pre-deploy. Primero lee todos los archivos del componente
señalado, luego produce un reporte con ✅/❌ por punto + fixes específicos en diff de código.

### Protocolo de ejecución
```
1. Lee el archivo del componente con Read
2. Si hay un archivo de estilos global o tailwind.config, léelo también
3. Ejecuta el checklist completo
4. Reporta: ítem, estado (✅/❌), y si es ❌, el fix exacto como diff
```

### Checklist completo

**1. Spacing scale — ¿usa el grid de 4px?**
Todos los valores de `padding`, `margin`, `gap` deben ser múltiplos de 4px. En Tailwind: `p-1`(4)
`p-2`(8) `p-3`(12) `p-4`(16) `p-5`(20) `p-6`(24) `p-8`(32) `p-12`(48) `p-16`(64).
❌ Flag: `p-[13px]`, `mt-[7px]`, valores arbitrarios que no son múltiplos de 4.

**2. Jerarquía tipográfica real**
¿Hay al menos 2 niveles de font-weight diferente? ¿El heading es visiblemente más grande que el
body? ¿El label/caption es distinguible del body sin depender solo del color?
❌ Flag: todo en `text-sm text-muted-foreground` — es la marca de diseño genérico.

**3. Paleta de colores — máx 3 + neutros**
¿El componente usa más de 3 colores no-neutros? ¿Hay colores que no pertenecen al sistema?
❌ Flag: mezcla de `violet`, `purple`, `blue`, `indigo` sin sistema claro.

**4. Contraste WCAG AA**
Texto sobre fondo: mínimo 4.5:1 para texto normal, 3:1 para texto grande (≥18px bold).
❌ Flag: `text-muted-foreground` sobre `bg-muted` — frecuentemente falla AA.

**5. Animaciones ≤300ms**
Cualquier transition/animation que supere 300ms se siente lenta.
❌ Flag: `duration-500`, `duration-700`, `transition-all duration-300 ease-in`.

**6. Solo transform y opacity animados**
NUNCA animar `width`, `height`, `margin`, `padding`, `top`, `left` — causan reflow.
❌ Flag: `transition-all` (anima todo, incluyendo propiedades que hacen reflow).

**7. Easing correcto**
- Entrada de pantalla: `ease-out`
- Elementos interactivos: spring (Framer) o `cubic-bezier(0.34, 1.56, 0.64, 1)` aproximado
- NUNCA `ease-in` para UI (se siente que el elemento "entra arrastrándose")
❌ Flag: `ease-in` en cualquier animación de entrada o modal.

**8. Hover/focus states en TODOS los interactivos**
Cada `button`, `a`, `[role="button"]`, input, select debe tener hover visible y focus-visible ring.
❌ Flag: `outline-none` sin reemplazo de focus visible.

**9. Tap targets ≥44px en mobile**
Botones, links y elementos interactivos deben tener al menos 44×44px de área táctil.
❌ Flag: `h-6 w-6` en un botón sin padding adicional (24px < 44px).

**10. Mobile 390px funcional**
El componente debe funcionar en viewport de 390px sin overflow horizontal ni texto truncado
incorrectamente.
❌ Flag: `min-w-[500px]`, `w-[800px]` sin responsive override.

**11. Slop check — purple/pink gradients**
❌ Flag: `bg-gradient-to-r from-purple-500 to-pink-500` — el gradient más usado en UI genérico.
Fix: un solo color sólido con hover en variación de lightness.

**12. Slop check — side border accent (left-border tabs)**
❌ Flag: `border-l-4 border-blue-500` como único diferenciador visual de un item seleccionado.
Fix: `bg-accent/10` con `text-accent` — background tonal es más sofisticado.

**13. Slop check — bounce exagerado**
❌ Flag: `animate-bounce`, spring con stiffness muy bajo y damping muy bajo (ej: stiffness:100
damping:5), `cubic-bezier` con overshoot >1.8.
Fix: spring stiffness:300 damping:30 — bounce controlado, no cartoon.

**14. Scale de press correcto**
❌ Flag: `hover:scale-110`, `active:scale-90` — muy exagerado.
Fix: `active:scale-[0.97]` o `active:scale-[0.98]` — casi imperceptible pero se siente bien.

**15. Skeleton en lugar de spinners para loading estructural**
Si el componente tiene un loading state que afecta layout (cards, listas, tablas):
❌ Flag: `<Spinner />` centrado que colapsa el layout.
Fix: skeleton que preserve exactamente el shape del contenido final.

---

## Comando `/animate`

### Qué animar — lista de patrones válidos
1. **Entrada de modales, sheets, drawers** — scale+opacity spring desde el origen
2. **Entrada de dropdowns, popovers** — scale+opacity desde el trigger point
3. **Hover states de cards interactivas** — translateY sutil + shadow
4. **Button press** — scale down en active
5. **Loading → contenido** — fade in del contenido cuando resuelve
6. **Transición de tab** — fade + translate lateral del panel activo
7. **Stagger de lista** — delay incremental en items de una lista que aparece
8. **Toast/notification entrada** — slide desde borde + fade
9. **Confirmación de éxito** — scale up breve + color flash

### Qué NUNCA animar
- Typing / input de texto (teclado)
- Scroll position (performance y accessibility)
- `width` / `height` / `margin` / `padding` (reflow)
- Colores en hover de texto (usar opacity o lightness, no color transition)
- Toda una página en page transitions a menos que sea un requisito explícito
- Loading spinners que giran infinitamente en acciones ≤500ms

### Spring values recomendados

```typescript
// Estándar — la mayoría de UI elements
{ stiffness: 300, damping: 30 }

// Suave — drawers, sheets que entran desde fuera
{ stiffness: 250, damping: 28 }

// Rígido — tooltips, dropdowns que deben aparecer rápido
{ stiffness: 400, damping: 40 }

// Celebración — success states únicamente
{ stiffness: 200, damping: 15, mass: 0.8 }
```

### Patrón 1: Button Press

```tsx
// CSS puro (sin dependencias)
<button className="transition-transform duration-75 active:scale-[0.97] active:duration-[50ms]">
  Click me
</button>

// Tailwind variant personalizado en tailwind.config
// theme.extend.scale: { '97': '0.97', '98': '0.98' }

// Framer Motion
import { motion } from "framer-motion";
<motion.button
  whileTap={{ scale: 0.97 }}
  transition={{ type: "spring", stiffness: 400, damping: 40 }}
>
  Click me
</motion.button>
```

### Patrón 2: Modal Entrance

```tsx
// Framer Motion — modal que entra con scale+opacity
const modalVariants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { type: "spring", stiffness: 300, damping: 30 },
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    transition: { duration: 0.15, ease: "easeIn" },
  },
};

<AnimatePresence>
  {isOpen && (
    <motion.div
      variants={modalVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="fixed inset-0 z-50 flex items-center justify-center"
    >
      {/* modal content */}
    </motion.div>
  )}
</AnimatePresence>

// CSS puro con @keyframes (sin Framer)
// globals.css
@keyframes modal-in {
  from { opacity: 0; transform: scale(0.95); }
  to   { opacity: 1; transform: scale(1); }
}
.modal-enter {
  animation: modal-in 200ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
```

### Patrón 3: Sheet slide-in desde abajo

```tsx
const sheetVariants = {
  hidden: { opacity: 0, y: "100%" },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring", stiffness: 250, damping: 28 },
  },
  exit: {
    opacity: 0,
    y: "100%",
    transition: { duration: 0.2, ease: "easeIn" },
  },
};

// La salida usa ease-in porque el elemento se va — el usuario ya no necesita seguirlo
```

### Patrón 4: Hover card — sutil lift

```tsx
// CSS con Tailwind
<div className="transition-[transform,box-shadow] duration-200 ease-out hover:-translate-y-0.5 hover:shadow-md">
  {/* card content */}
</div>

// Regla: translateY máximo -4px (-translate-y-1), shadow solo un nivel arriba del estado base
// Si la card ya tiene shadow-md, el hover es shadow-lg — no shadow-2xl

// Framer Motion
<motion.div
  whileHover={{ y: -2, boxShadow: "0 8px 25px rgba(0,0,0,0.12)" }}
  transition={{ type: "spring", stiffness: 300, damping: 30 }}
>
```

### Patrón 5: Stagger list animation

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06, // 60ms entre cada item — más que esto se siente lento
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 8 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { type: "spring", stiffness: 300, damping: 30 },
  },
};

<motion.ul variants={containerVariants} initial="hidden" animate="visible">
  {items.map((item) => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.content}
    </motion.li>
  ))}
</motion.ul>

// Regla: stagger solo en listas de ≤12 items. Listas más largas deben entrar todas juntas
// o usar virtualización — el stagger de 50 items es tortura visual.
```

---

## Comando `/typeset`

### Type scale recomendada para apps F100K (Tailwind)

```tsx
// tailwind.config.ts — extend fontSize con line-height y letter-spacing integrados
fontSize: {
  "display": ["3.5rem",  { lineHeight: "1.05", letterSpacing: "-0.04em" }], // 56px — hero
  "h1":      ["2.25rem", { lineHeight: "1.1",  letterSpacing: "-0.03em" }], // 36px
  "h2":      ["1.75rem", { lineHeight: "1.15", letterSpacing: "-0.02em" }], // 28px
  "h3":      ["1.375rem",{ lineHeight: "1.2",  letterSpacing: "-0.01em" }], // 22px
  "h4":      ["1.125rem",{ lineHeight: "1.3",  letterSpacing: "-0.01em" }], // 18px
  "body-lg": ["1rem",    { lineHeight: "1.6",  letterSpacing: "0" }],       // 16px
  "body":    ["0.9375rem",{ lineHeight: "1.55", letterSpacing: "0" }],      // 15px
  "body-sm": ["0.875rem",{ lineHeight: "1.5",  letterSpacing: "0" }],       // 14px
  "label":   ["0.8125rem",{ lineHeight: "1.2", letterSpacing: "0.04em" }],  // 13px
  "caption": ["0.75rem", { lineHeight: "1.3",  letterSpacing: "0.03em" }],  // 12px
}
```

### Reglas de font-weight — uso obligatorio

| Peso | Tailwind | Cuándo usar |
|------|----------|-------------|
| 800 | `font-extrabold` | Hero display único por página. NUNCA en más de un elemento |
| 700 | `font-bold` | H1, H2 de sección. Máx 2-3 por pantalla |
| 600 | `font-semibold` | H3, H4, labels de form, nombres en cards |
| 500 | `font-medium` | Sub-labels, captions importantes, precios |
| 400 | `font-normal` | Body text, descripciones, párrafos |

❌ Nunca usar 700+ en texto de más de 2 líneas — la densidad del peso aplasta el aire.
❌ Nunca usar el mismo weight para heading y body en el mismo bloque visual.

### Reglas de line-height

```
Títulos display/h1:    line-height: 1.05 – 1.1   (muy apretado, looks powerful)
Headings h2/h3:        line-height: 1.15 – 1.2
Subtítulos/h4/labels:  line-height: 1.2 – 1.3
Body text:             line-height: 1.5 – 1.6    (mínimo para legibilidad)
Caption/metadata:      line-height: 1.3 – 1.4
```

### Reglas de letter-spacing

```
Display/H1:   -0.03em a -0.04em   (tracking tight — headings grandes siempre van apretados)
H2/H3:        -0.01em a -0.02em
Body:         0                   (tracking normal — nunca ajustar body text)
Labels:       +0.03em a +0.05em   (tracking amplio — legibilidad en tamaño pequeño)
Caps labels:  +0.06em a +0.1em    (uppercase + tracking amplio = combinación correcta)
```

❌ Nunca usar `tracking-wide` o `tracking-widest` en headings grandes — en texto grande el
spacing amplio se ve como karate chop al diseño.

### Jerarquía visual — el test de squint

Mira el componente con los ojos entrecerrados hasta que todo se vuelva borroso. ¿Puedes
identificar el elemento más importante? ¿El segundo más importante? Si la respuesta es no,
la jerarquía tipográfica es insuficiente.

Herramienta rápida de diagnóstico:
```bash
# Busca si todos los textos tienen la misma clase base
grep -n "text-sm text-muted-foreground" src/components/MiComponente.tsx
# Si aparece 5+ veces, hay un problema de jerarquía
```

---

## Comando `/craft`

Para construir un nuevo componente con máxima calidad.

### Paso 1: Leer el contexto del proyecto

```bash
# Antes de escribir una línea de código, leer:
cat tailwind.config.ts          # paleta y escala tipográfica
cat src/styles/globals.css      # variables CSS, tokens
ls src/components/ui/           # componentes shadcn disponibles
# Leer 2-3 componentes existentes para entender el patrón de la codebase
```

No inventar un sistema de diseño desde cero — extender el existente.

### Paso 2: Calibrar los 3 diales

Antes de escribir JSX, definir:

```
VARIANCE: [bajo | medio | alto]
Razón: ___

MOTION: [bajo | medio | alto]
Razón: ___

DENSITY: [bajo | medio | alto]
Razón: ___
```

Un dashboard de métricas = VARIANCE bajo, MOTION bajo, DENSITY alto.
Una card de pricing en landing = VARIANCE medio, MOTION medio, DENSITY bajo.
Un hero de onboarding = VARIANCE alto, MOTION medio-alto, DENSITY bajo.

### Paso 3: Construir

Orden de construcción:
1. **Layout y estructura** — grid, flex, spacing
2. **Tipografía** — aplicar la jerarquía antes que el color
3. **Color** — aplicar paleta después de que la estructura sea sólida
4. **Estados interactivos** — hover, focus, active, disabled
5. **Animaciones** — último, una vez que la estructura sea correcta
6. **Responsive** — verificar 390px antes de considerar terminado

### Paso 4: Checklist de calidad antes de terminar

```
□ ¿El componente funciona sin JS? (estructura semántica correcta)
□ ¿Tiene todos los aria-labels necesarios?
□ ¿Los estados de loading/error/empty están manejados?
□ ¿El spacing usa el grid de 4px?
□ ¿Hay jerarquía tipográfica real (mínimo 2 pesos diferentes)?
□ ¿Las animaciones usan solo transform/opacity?
□ ¿Funciona en 390px?
□ ¿Pasaría el slop check de 7 puntos?
```

---

## Anti-slop Rules — Lista definitiva

Ver `references/anti-slop-patterns.md` para la lista expandida. Aquí los 7 más críticos:

### ❌ 1. Purple-to-pink gradient genérico
```tsx
// MAL — el gradient más usado en templates de IA
className="bg-gradient-to-r from-purple-500 to-pink-500"

// BIEN — un color sólido con variación de lightness
className="bg-violet-600 hover:bg-violet-700"
// o: un gradient monocromático sutil
className="bg-gradient-to-b from-violet-600 to-violet-700"
```

### ❌ 2. Side-border como único accent visual
```tsx
// MAL — ese tab lateral colorido que grita "Bootstrap 3"
className="border-l-4 border-blue-500 pl-4"

// BIEN — background tonal
className="bg-blue-50 dark:bg-blue-950/30 px-4 py-2 rounded-md"
// o: texto en color accent + ningún borde
className="text-blue-600 font-semibold"
```

### ❌ 3. Todo en text-sm text-muted-foreground
```tsx
// MAL — diseño flat donde todo tiene la misma importancia
<p className="text-sm text-muted-foreground">Título</p>
<p className="text-sm text-muted-foreground">Descripción</p>
<p className="text-sm text-muted-foreground">Metadata</p>

// BIEN — jerarquía real
<h3 className="text-base font-semibold text-foreground">Título</h3>
<p className="text-sm text-foreground/80 leading-relaxed">Descripción</p>
<span className="text-xs text-muted-foreground tracking-wide">Metadata</span>
```

### ❌ 4. Grid de cards perfectamente idénticas
```tsx
// MAL — todos los items tienen el mismo peso visual
<div className="grid grid-cols-3 gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>

// BIEN — un item featured rompe la monotonía
<div className="grid grid-cols-3 gap-4">
  <Card {...items[0]} featured className="col-span-2 row-span-2" />
  {items.slice(1).map(item => <Card key={item.id} {...item} />)}
</div>
```

### ❌ 5. Loading spinner que colapsa el layout
```tsx
// MAL — el spinner destruye el layout, el contenido "salta" al cargar
{isLoading ? <Spinner /> : <ContentList items={items} />}

// BIEN — skeleton que preserva el shape exacto
{isLoading ? (
  <div className="space-y-3">
    {Array.from({ length: 5 }).map((_, i) => (
      <Skeleton key={i} className="h-16 w-full rounded-lg" />
    ))}
  </div>
) : (
  <ContentList items={items} />
)}
```

### ❌ 6. Modal con ease-in
```tsx
// MAL — la entrada se siente lenta y torpe
transition={{ duration: 0.3, ease: "easeIn" }}

// BIEN — spring que se siente físico
transition={{ type: "spring", stiffness: 300, damping: 30 }}
// o sin Framer:
// animation: modal-in 200ms cubic-bezier(0.34, 1.56, 0.64, 1)
```

### ❌ 7. Hover scale exagerado
```tsx
// MAL — la card "salta" al hover, se siente cheap
className="hover:scale-105 transition-transform"

// BIEN — lift sutil casi imperceptible pero se siente correcto
className="hover:-translate-y-0.5 hover:shadow-md transition-[transform,box-shadow] duration-200 ease-out"
// o para buttons:
className="active:scale-[0.97] transition-transform duration-75"
```

---

## Principios de Emil Kowalski — Resumen operativo

1. **Max 300ms** para cualquier animación de UI. Más que eso y el usuario se pregunta si rompió algo.
2. **Solo `transform` y `opacity`**. Son las únicas propiedades que el navegador puede animar sin reflow (compositor-only).
3. **Scale en press: 0.97-0.98**. No 0.9 (exagerado), no 0.99 (imperceptible). El punto dulce es 0.97.
4. **`clip-path` para transiciones sofisticadas** — modales que revelan desde un punto, dropdowns que se expanden desde el trigger.
5. **Spring > cubic-bezier** para elementos interactivos. Spring se siente físico porque modela inercia real.
6. **Easing cheatsheet**: spring/ease-out para entrada, ease-in para salida, ease-in-out para loops.
7. **NUNCA ease-in para entrada**. Se siente como el elemento "se cuela" en vez de "llegar".
8. **NUNCA animar keyboard actions**. El input de texto no debe tener transiciones.
9. **Animaciones confirman acciones, no entretienen**. Si una animación es lo primero que notas, probablemente está mal.
10. **Bounce controlado**. `stiffness: 300, damping: 30` tiene overshoot mínimo. Ajusta damping hacia arriba (40-50) para eliminar bounce completamente.

---

## Principios de Paul Bakaus / Impeccable — 7 dominios

### 1. Tipografía (`/typeset`)
Hierarchy first. Sizing, weight, y spacing deben crear una escala legible antes de agregar color.
La jerarquía tipográfica es la base de todo diseño legible.

### 2. Color/Contraste (`/colorize`)
Paleta coherente: 1 color de acento que realmente acente (no decora — jerarquiza), neutros grises
bien definidos, WCAG AA como mínimo absoluto. El acento debe aparecer en ≤20% de la UI.

### 3. Espaciado (`/layout`)
Grid de 4px base. Visual rhythm = que el ojo pueda "leer" el espaciado como una melodía, no ruido.
Más espacio del que crees necesitar. Siempre.

### 4. Movimiento (`/animate`)
Intencional, físico, coherente. Cada animación debe tener una razón de existir: confirmar una
acción, guiar la atención, o comunicar estado.

### 5. Interacción (`/delight`)
Todos los interactivos tienen hover. Todos los focusables tienen focus-visible ring. Los estados
disabled son visualmente distintos. Los estados de éxito/error son inconfundibles.

### 6. Responsive (`/adapt`)
Mobile-first. 390px es el breakpoint de referencia, no el afterthought. Breakpoints coherentes
que tienen razón de existir (no `md:` porque sí).

### 7. UX Writing (`/distill`)
Copy claro, accionable, sin jerga. Los labels de botones deben describir acciones, no estados.
"Guardar cambios" no "Submit". "Cancelar suscripción" no "Proceder con cancelación".

### `/polish` = los 7 dominios en una sola pasada
Cuando ejecutas `/polish`, estás ejecutando los 7 dominios de forma simultánea sobre un
componente específico. El output es un reporte accionable con diffs, no sugerencias vagas.

---

## Comando `/landing` — Landings de Alto Impacto

Para cuando construyes una landing page de producto, programa, o servicio. Este nivel está
por encima del `/craft` estándar: aquí el objetivo es impresión inmediata y conversión.

### Anatomía del Hero Perfecto

El hero debe resolver 3 preguntas en ≤3 segundos: ¿Qué es? ¿Para quién? ¿Por qué ahora?

```tsx
// Estructura canónica de hero
<section className="relative min-h-screen flex flex-col items-center justify-center pt-20 pb-32 overflow-hidden">

  {/* 1. Fondo con profundidad — NO un color plano */}
  <HeroBackground />  {/* ver sección Profundidad Visual */}

  {/* 2. Pill badge — novedad / credibilidad */}
  <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-sm text-white/70 backdrop-blur-sm">
    <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
    <span>Nuevo — Versión 2.0 disponible</span>
  </div>

  {/* 3. Headline — máximo 8 palabras, font extrabold, tracking tight */}
  <h1 className="max-w-4xl text-center text-5xl font-extrabold leading-[1.05] tracking-[-0.04em] text-white md:text-7xl">
    La única plataforma que{" "}
    <span className="gradient-text">convierte seguidores en ventas</span>
  </h1>

  {/* 4. Subheadline — 1-2 líneas, NO repite el headline */}
  <p className="mt-6 max-w-2xl text-center text-lg text-white/60 leading-relaxed">
    Breve descripción del mecanismo único. Cómo funciona, no qué hace.
  </p>

  {/* 5. CTAs — primario + secundario, nunca 3 */}
  <div className="mt-10 flex flex-col items-center gap-3 sm:flex-row">
    <PrimaryButton>Comenzar gratis — sin tarjeta</PrimaryButton>
    <GhostButton>Ver demo en 2 min →</GhostButton>
  </div>

  {/* 6. Trust signal inline — debajo de CTAs */}
  <p className="mt-4 text-sm text-white/40">
    +2,400 emprendedores ya generan ventas con esto
  </p>

  {/* 7. Mockup del producto — siempre visible above the fold */}
  <HeroMockup className="mt-20" />

</section>
```

### Reglas de jerarquía en hero

| Elemento | Tamaño | Peso | Opacidad texto |
|----------|--------|------|----------------|
| Pill badge | 14px | 400 | 70% |
| Headline | 56–72px | 800 | 100% |
| Subheadline | 18px | 400 | 60% |
| CTA primario | 16px | 600 | 100% (bg sólido) |
| CTA secundario | 16px | 500 | 70% |
| Trust signal | 14px | 400 | 40% |

❌ Nunca headline de más de 2 líneas en desktop.
❌ Nunca 3 CTAs — el usuario tiene que elegir y no elige.
❌ Nunca subheadline que repita las mismas palabras del headline.

---

## Profundidad Visual — Glow, Glass y Sombras Avanzadas

### Glow effects correctos (no excess)

El glow sirve para anclar elementos flotantes y crear profundidad. Mal usado es la señal
#1 de diseño AI-generated.

```tsx
// ✅ BIEN — glow como luz de fondo, no como borde
<div className="relative">
  {/* Glow blob detrás del elemento principal */}
  <div
    className="absolute inset-0 -z-10 blur-[120px] opacity-30"
    style={{ background: "radial-gradient(ellipse at center, #6366f1 0%, transparent 70%)" }}
  />
  <HeroContent />
</div>

// ✅ BIEN — glow en botón primario (solo el primario)
<button className="relative bg-indigo-600 hover:bg-indigo-500 transition-colors">
  <span className="absolute inset-0 rounded-[inherit] shadow-[0_0_20px_rgba(99,102,241,0.5)] opacity-0 transition-opacity hover:opacity-100" />
  Comenzar
</button>

// ❌ MAL — glow en todos los elementos (pierden significado)
// ❌ MAL — glow con blur muy pequeño (<40px) — queda como halo feo
// ❌ MAL — glow de color diferente al acento de la paleta
```

### Gradient text — solo para headlines

```tsx
// globals.css
.gradient-text {
  background: linear-gradient(135deg, #fff 0%, rgba(255,255,255,0.6) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

// Variante con acento de color
.gradient-text-accent {
  background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

// ❌ NUNCA gradient text en body, labels, o más de 1 elemento por sección
// ❌ NUNCA gradient con más de 3 stops de colores distintos (se ve karate-chop)
```

### Glassmorphism correcto

```tsx
// ✅ Glass auténtico: necesita fondo con contenido detrás para funcionar
<div
  className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-6"
  // backdrop-blur SOLO funciona si hay elementos visuales detrás del glass
  // Si el fondo es un color plano, es mentira glass — usar bg-white/10 sin blur
>
  <CardContent />
</div>

// ❌ MAL — glass sobre fondo plano negro sin contenido detrás
// ❌ MAL — backdrop-blur muy alto (>20px) enlentece móvil — usar backdrop-blur-sm en mobile
// ❌ MAL — border blanco muy opaco (border-white/30) se ve plástico
```

### Dark surface hierarchy — 5 niveles

Nunca diseñar en dark mode con un solo `bg-black`. La profundidad viene de capas:

```tsx
// tokens CSS en globals.css
:root {
  --surface-0: #000000;     // Fondo base — lo más profundo
  --surface-1: #0A0A10;     // Contenedores principales (sidebar, panels)
  --surface-2: #0E0E18;     // Cards, secciones
  --surface-3: #141422;     // Cards hover, elementos elevados
  --surface-4: #1A1A2E;     // Tooltips, dropdowns
  --surface-border: rgba(255,255,255,0.06); // Borde entre superficies
}

// Uso:
// bg-[var(--surface-0)] — fondo de página
// bg-[var(--surface-1)] — nav, sidebar
// bg-[var(--surface-2)] — cards
// bg-[var(--surface-3)] — card en hover state
// Los bordes entre capas: border-white/[0.06]
```

### Spotlight / beam effect (efecto de cono de luz)

```tsx
// Efecto beam de luz en hero — se mueve con el mouse o es estático
// Versión estática (sin JS):
<div className="absolute inset-0 overflow-hidden">
  <div
    className="absolute -top-1/2 left-1/2 -translate-x-1/2 w-[800px] h-[600px] opacity-20"
    style={{
      background: "conic-gradient(from 270deg at 50% 0%, transparent 0deg, #6366f1 90deg, transparent 180deg)",
      filter: "blur(60px)",
    }}
  />
</div>

// Grid de puntos (dot pattern) de fondo:
<div
  className="absolute inset-0 opacity-[0.15]"
  style={{
    backgroundImage: "radial-gradient(circle, rgba(255,255,255,0.3) 1px, transparent 1px)",
    backgroundSize: "32px 32px",
  }}
/>
```

---

## Scroll Animations — Reveal al hacer scroll

Estas animaciones SOLO se usan en landings y páginas de marketing. NUNCA en app UIs o dashboards.

### Setup con Framer Motion `useInView`

```tsx
// Componente reutilizable para cualquier elemento con reveal
"use client"
import { motion, useInView } from "framer-motion"
import { useRef } from "react"

function FadeIn({
  children,
  delay = 0,
  direction = "up", // "up" | "down" | "left" | "right" | "none"
  className,
}: {
  children: React.ReactNode
  delay?: number
  direction?: "up" | "down" | "left" | "right" | "none"
  className?: string
}) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-80px" })

  const directionOffset = {
    up: { y: 24 },
    down: { y: -24 },
    left: { x: 24 },
    right: { x: -24 },
    none: {},
  }

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, ...directionOffset[direction] }}
      animate={isInView ? { opacity: 1, x: 0, y: 0 } : {}}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 30,
        delay,
      }}
      className={className}
    >
      {children}
    </motion.div>
  )
}
```

### Patrón: Sección con stagger al entrar en viewport

```tsx
// Features section — cada card entra con delay incremental
<div className="grid grid-cols-3 gap-6">
  {features.map((feature, i) => (
    <FadeIn key={feature.id} delay={i * 0.08} direction="up">
      <FeatureCard {...feature} />
    </FadeIn>
  ))}
</div>

// Regla: delay máximo 0.08 * n — nunca acumular más de 0.5s de total
// Si hay más de 6 items, eliminar el delay (stagger de >6 items es tortura)
```

### Patrón: Contador animado al entrar en viewport

```tsx
"use client"
import { useEffect, useRef } from "react"
import { useInView, useMotionValue, useSpring } from "framer-motion"

function AnimatedCounter({ target, suffix = "" }: { target: number; suffix?: string }) {
  const ref = useRef<HTMLSpanElement>(null)
  const motionValue = useMotionValue(0)
  const spring = useSpring(motionValue, { duration: 1500, bounce: 0 })
  const isInView = useInView(ref, { once: true })

  useEffect(() => {
    if (isInView) motionValue.set(target)
  }, [isInView, motionValue, target])

  useEffect(() => {
    spring.on("change", (v) => {
      if (ref.current) ref.current.textContent = `${Math.round(v).toLocaleString()}${suffix}`
    })
  }, [spring, suffix])

  return <span ref={ref}>0{suffix}</span>
}

// Uso en Stats section:
<AnimatedCounter target={2400} suffix="+" />  // → "+2,400"
<AnimatedCounter target={98} suffix="%" />     // → "98%"
```

### Patrón: Text reveal por palabras (headline de impact)

```tsx
function WordReveal({ text, delay = 0 }: { text: string; delay?: number }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true })
  const words = text.split(" ")

  return (
    <span ref={ref} className="inline">
      {words.map((word, i) => (
        <motion.span
          key={i}
          className="inline-block"
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{
            type: "spring",
            stiffness: 300,
            damping: 30,
            delay: delay + i * 0.05,
          }}
        >
          {word}&nbsp;
        </motion.span>
      ))}
    </span>
  )
}

// ⚠️ Solo para headlines de hero o secciones de impacto. Nunca en body text.
```

---

## Bento Grid — Layouts Heterogéneos

El bento grid (grid de cards de distintos tamaños) es el pattern más efectivo para mostrar
features de producto. Funciona porque rompe la monotonía del grid uniforme.

### Estructura base

```tsx
// grid de 12 columnas — las cards ocupan distintos spans
<div className="grid grid-cols-12 gap-4 auto-rows-[180px]">

  {/* Card grande — feature principal */}
  <BentoCard className="col-span-7 row-span-2">
    <MainFeatureVisual />
  </BentoCard>

  {/* Card alta — métrica o stat */}
  <BentoCard className="col-span-5 row-span-2">
    <StatsVisual />
  </BentoCard>

  {/* Cards pequeñas — features secundarias */}
  <BentoCard className="col-span-4">
    <MiniFeature1 />
  </BentoCard>
  <BentoCard className="col-span-4">
    <MiniFeature2 />
  </BentoCard>
  <BentoCard className="col-span-4">
    <MiniFeature3 />
  </BentoCard>

</div>

// BentoCard base component:
function BentoCard({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn(
      "group relative overflow-hidden rounded-2xl border border-white/[0.06] bg-[var(--surface-2)] p-6",
      "transition-all duration-300 hover:border-white/[0.12] hover:bg-[var(--surface-3)]",
      className
    )}>
      {/* Gradient spot en hover */}
      <div className="absolute inset-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100"
        style={{ background: "radial-gradient(ellipse at 80% 0%, rgba(99,102,241,0.08) 0%, transparent 60%)" }}
      />
      {children}
    </div>
  )
}
```

### Reglas del bento

- La card más grande debe ocupar ≥50% del ancho del grid.
- Máximo 3 tamaños distintos de card (grande, mediana, pequeña).
- Cada card debe tener un visual único — no solo texto.
- El hover de card = border más visible + subtle glow desde una esquina.
- En mobile: todas las cards pasan a `col-span-12` (full width).

---

## Social Proof — Trust Signals que Convierten

### Anatomía de trust signals efectivos

```tsx
// 1. Avatar stack — muestra personas reales, no íconos
<div className="flex items-center gap-3">
  <div className="flex -space-x-2">
    {avatars.map((src, i) => (
      <img
        key={i}
        src={src}
        className="h-8 w-8 rounded-full border-2 border-[var(--surface-0)] object-cover"
        alt=""
      />
    ))}
  </div>
  <div>
    <div className="flex">
      {[...Array(5)].map((_, i) => (
        <StarIcon key={i} className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
      ))}
    </div>
    <p className="text-xs text-white/50">+2,400 ya dentro</p>
  </div>
</div>

// 2. Logo bar — clientes o apariciones en medios
// Regla: logos en grayscale opacity-40, en hover opacity-70
// Nunca logos a color en esta sección — crea ruido visual
<div className="flex items-center gap-8 opacity-40">
  {logos.map(logo => (
    <img key={logo} src={logo} className="h-6 object-contain grayscale" alt="" />
  ))}
</div>

// 3. Testimonial card — 1 real vence a 10 genéricos
<blockquote className="rounded-2xl border border-white/[0.06] bg-[var(--surface-2)] p-6">
  <p className="text-white/80 leading-relaxed">
    "{texto genuino del usuario, con detalles específicos, no genérico}"
  </p>
  <footer className="mt-4 flex items-center gap-3">
    <img src={avatar} className="h-10 w-10 rounded-full object-cover" />
    <div>
      <p className="text-sm font-semibold text-white">{nombre}</p>
      <p className="text-xs text-white/50">{cargo}, {empresa}</p>
    </div>
  </footer>
</blockquote>
```

### Reglas de trust signals

- Los números deben ser específicos: "2,437 usuarios" vence a "miles de usuarios".
- Nunca inventar métricas — usar las reales aunque sean menores.
- Los testimoniales deben mencionar un resultado concreto, no una emoción genérica.
- Los logos van siempre en grayscale — a color compiten con el acento de la paleta.

---

## Botones de Alto Impacto

El botón primario de una landing es el elemento más importante del diseño. Merece atención.

```tsx
// Botón primario de landing — no es el shadcn/ui Button por default
function PrimaryButton({ children, onClick }: { children: React.ReactNode; onClick?: () => void }) {
  return (
    <motion.button
      onClick={onClick}
      whileTap={{ scale: 0.97 }}
      transition={{ type: "spring", stiffness: 400, damping: 40 }}
      className="group relative inline-flex items-center gap-2 overflow-hidden rounded-xl
                 bg-indigo-600 px-8 py-3.5 text-base font-semibold text-white
                 shadow-[0_0_0_1px_rgba(99,102,241,0.3),0_4px_15px_rgba(99,102,241,0.4)]
                 transition-all duration-200
                 hover:bg-indigo-500
                 hover:shadow-[0_0_0_1px_rgba(99,102,241,0.5),0_8px_25px_rgba(99,102,241,0.5)]"
    >
      {/* Shimmer interno en hover */}
      <span
        className="absolute inset-0 translate-x-[-100%] bg-gradient-to-r from-transparent via-white/10 to-transparent
                   transition-transform duration-500 group-hover:translate-x-[100%]"
      />
      {children}
      <ArrowRightIcon className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5" />
    </motion.button>
  )
}

// El shimmer sweep solo en hover, nunca loop infinito.
// El shadow doble (ring + blur) da profundidad sin exagerar.
// La flecha que se mueve 2px en hover es suficiente — no 8px.
```

---

## Checklist `/landing` — Pre-deploy

Antes de declarar terminada una landing, verificar:

**Above the fold (sin scroll)**
- [ ] El headline responde ¿Qué es? ¿Para quién? en ≤8 palabras
- [ ] Hay un único CTA primario visible
- [ ] El mockup del producto es visible sin scroll en desktop
- [ ] El badge/pill de credibilidad está presente
- [ ] El fondo tiene profundidad (no color plano)

**Animaciones**
- [ ] El hero carga sin animaciones bloqueantes (content visible inmediato)
- [ ] Los elementos de hero tienen entrada con spring (no ease-in)
- [ ] Las secciones de features revelan al hacer scroll (no al cargar todo)
- [ ] Los contadores animados solo corren cuando son visibles
- [ ] El botón primario tiene feedback de press (scale 0.97)

**Profundidad visual**
- [ ] Hay al menos 3 niveles de surface color distintos
- [ ] El glow existe solo en 1-2 elementos, no en todo
- [ ] El gradient text está en ≤1 elemento por sección
- [ ] Los bordes de cards son `border-white/[0.06]` o más sutiles

**Trust signals**
- [ ] Hay números específicos (no "muchos usuarios")
- [ ] Al menos 1 testimonial con nombre real + resultado concreto
- [ ] Los logos están en grayscale

**Performance**
- [ ] Las imágenes tienen `loading="lazy"` excepto el hero fold
- [ ] El video de demo tiene `autoPlay muted loop playsInline`
- [ ] No hay `backdrop-blur` en elementos que se mueven o que son muchos
- [ ] El `blur-[120px]` de glows está en elementos estáticos, no animados
