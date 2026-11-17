# Anti-Slop Patterns — Lista Expandida

Referencia técnica para la skill `ux-elevacion-formula100k`. Cada entry tiene:
- Pattern (qué hacer mal)
- Por qué se usa (la trampa mental)
- Alternativa correcta
- Código de ejemplo cuando aplica

---

## CATEGORÍA: Gradientes

### ❌ Purple-to-pink gradient
**Pattern:** `bg-gradient-to-r from-purple-500 to-pink-500` (o variantes: violet-to-fuchsia, blue-to-purple)
**Por qué se usa:** Parece dinámico, "moderno", y lo genera cualquier AI de UI por default.
**Problema:** Es el gradient más usado en templates de IA desde 2022. Comunica "hecho en 5 minutos".
**Alternativa:** Color sólido con hover en lightness ajustada. Si necesitas gradient, monocromático:
```tsx
// Monocromático sutil — casi imperceptible pero añade profundidad
bg-gradient-to-b from-violet-600 to-violet-700

// Sólido con hover correcto
bg-violet-600 hover:bg-violet-700
```

### ❌ Rainbow gradient como decoración
**Pattern:** Borders o textos con gradients multi-color tipo `from-pink-500 via-yellow-500 to-cyan-500`
**Alternativa:** Un solo color de acento aplicado con intención. El arcoíris no es un sistema de color.

### ❌ Gradient en texto (gradient text)
**Pattern:** `bg-clip-text text-transparent bg-gradient-to-r from-X to-Y` en headings
**Problema:** Rompe selectabilidad de texto en algunos browsers, bajo contraste en muchos contextos.
**Alternativa:** Color sólido de alta contrast. Si necesitas énfasis, usa font-weight, no color gradient.
**Excepción:** Válido solo en display copy de landing page donde el texto no es cuerpo principal.

---

## CATEGORÍA: Borders y Separadores

### ❌ Side-border accent (el "tab" lateral colorido)
**Pattern:** `border-l-4 border-blue-500 pl-3` para indicar item seleccionado o destacado
**Por qué se usa:** Fácil de implementar, "soluciona" la selección visual rápido.
**Problema:** Herencia visual de Bootstrap 3 / UI de 2014. Comunica que el diseño no evolucionó.
**Alternativa:**
```tsx
// Background tonal — más sofisticado
className="bg-blue-50 dark:bg-blue-950/20 rounded-md px-3 py-2"

// Combinado con texto en acento
className="bg-accent/10 text-accent-foreground font-medium rounded-md px-3 py-2"
```

### ❌ Dividers innecesarios
**Pattern:** `<hr className="my-4" />` entre cada sección, o `border-b` en cada row de lista.
**Problema:** El espaciado debería crear la separación visual. Dividers encima de espaciado = ruido.
**Alternativa:** `space-y-6` o `gap-6` — el espacio crea la separación sin líneas adicionales.
**Excepción:** Dividers en tablas de datos donde la densidad lo requiere, o en separaciones semánticas reales (tipo `<hr>` en dropdown entre grupos).

### ❌ Border en todos los lados de una card
**Pattern:** `border border-border rounded-lg` en cards sobre fondos blancos/gris muy claro.
**Alternativa:**
```tsx
// Shadow sutil en lugar de border — se lee mejor como card
className="shadow-sm rounded-lg bg-card"

// O: fondo levemente diferente sin border
className="bg-muted/30 rounded-lg"
```

---

## CATEGORÍA: Tipografía

### ❌ Todo en text-sm text-muted-foreground
**Pattern:** Usar la misma clase para heading, body, label, y caption.
**Síntoma:** La UI se ve "flat", todo tiene el mismo peso, no hay donde anclar la vista.
**Alternativa:** Ver type scale en SKILL.md — mínimo 2 pesos y 2 tamaños por componente con contenido real.

### ❌ uppercase sin tracking
**Pattern:** `uppercase text-xs` sin `tracking-widest` o similar.
**Problema:** Uppercase en texto pequeño sin tracking extra es ilegible.
**Fix:** `uppercase text-xs tracking-widest font-medium` — los tres siempre juntos.

### ❌ Font-size arbitrario sin sistema
**Pattern:** `text-[13px]`, `text-[17px]`, `text-[22px]` — valores fuera de la scale.
**Fix:** Mapear al valor más cercano de la type scale del proyecto. Si hace falta un valor, agregarlo
al config de Tailwind de forma consistente.

### ❌ Line-height en headings grandes igual que body
**Pattern:** `text-4xl leading-normal` — `leading-normal` (1.5) en un heading grande es demasiado
abierto, se ve incohesivo.
**Fix:** `text-4xl leading-tight` o `leading-[1.1]` — headings grandes necesitan line-height más apretado.

### ❌ Body text en font-semibold o bold
**Pattern:** `font-semibold` en párrafos de más de 2 líneas.
**Problema:** El peso alto en texto de cuerpo largo hace la lectura más difícil.
**Fix:** `font-normal` para body. El énfasis puntual usa `font-medium` o `<strong>`.

---

## CATEGORÍA: Spacing y Layout

### ❌ Spacing inconsistente (no en grid de 4px)
**Pattern:** `mt-[13px]`, `gap-[7px]`, `p-[18px]`
**Fix:** `mt-3`(12px), `gap-2`(8px), `p-4`(16px) — siempre en la scale de 4px.

### ❌ Grid de cards perfectamente idénticas (mismo tamaño, mismo peso)
**Pattern:**
```tsx
<div className="grid grid-cols-3 gap-4">
  {items.map(item => <Card key={item.id} className="h-32" {...item} />)}
</div>
```
**Problema:** La uniformidad comunica que ningún item es más importante que otro. El ojo no sabe
dónde ir.
**Alternativa:** Un item featured que rompe la grilla:
```tsx
<div className="grid grid-cols-3 gap-4">
  <Card featured className="col-span-2" {...items[0]} />
  <Card {...items[1]} />
  {items.slice(2).map(item => <Card key={item.id} {...item} />)}
</div>
```

### ❌ Padding insuficiente en containers principales
**Pattern:** `p-4` como padding de un container de página o sección principal.
**Regla:** Containers de página: `px-6 md:px-8 lg:px-12`. Secciones: `py-12 md:py-16 lg:py-24`.
El espaciado en desktop debe sentirse "premium" — más del que crees necesitar.

### ❌ Max-width demasiado ancho para reading content
**Pattern:** Columnas de texto que van de borde a borde en desktop.
**Fix:** `max-w-prose` (65ch) para texto largo. `max-w-2xl` para content con imágenes.
Un texto de 100 caracteres por línea destruye la legibilidad.

---

## CATEGORÍA: Animaciones

### ❌ Bounce exagerado (animate-bounce, spring cartoon)
**Pattern:** `animate-bounce`, o spring con `stiffness: 80, damping: 8`
**Problema:** Bounce de más de 2-3% del valor original se siente cartoon, no físico.
**Fix:**
```tsx
// Spring controlado — bounce mínimo
{ type: "spring", stiffness: 300, damping: 30 }

// Sin ningún bounce
{ type: "spring", stiffness: 300, damping: 40 }
```

### ❌ transition-all
**Pattern:** `className="transition-all duration-200"`
**Problema:** Anima TODAS las propiedades CSS, incluyendo width, height, margin que causan reflow.
**Fix:**
```tsx
// Solo las propiedades necesarias
className="transition-[transform,opacity] duration-200"
className="transition-[transform,box-shadow] duration-200 ease-out"
```

### ❌ ease-in en entradas
**Pattern:** `transition={{ ease: "easeIn", duration: 0.3 }}`
**Problema:** ease-in empieza lento y termina rápido — para una entrada, el elemento "llega"
abruptamente. La percepción es de lag seguido de pop.
**Fix:** ease-out para entradas, spring para interactivos.

### ❌ Duración >300ms en UI elements
**Pattern:** `duration-500`, `duration-700`, `transition-all duration-1000`
**Regla:** ≤150ms para micro-interactions (hover, button press), ≤300ms para transiciones de
estado (modales, drawers, tab switches). >300ms solo en animaciones de pantalla completa o
celebraciones explícitas.

### ❌ Stagger en listas largas
**Pattern:** Stagger animation en listas de 20+ items.
**Problema:** El último item tarda `n * staggerDelay` ms en aparecer. Con 20 items a 60ms = 1.2s.
**Fix:** Stagger solo en listas de ≤12 items. Para listas más largas, todos los items entran juntos.

---

## CATEGORÍA: Componentes interactivos

### ❌ Hover scale de 1.05+
**Pattern:** `hover:scale-105`, `hover:scale-110`
**Problema:** Scale de 5%+ es perceptiblemente grande — la card "salta" visualmente. Comunica
"template de Themeforest" inmediatamente.
**Fix:**
```tsx
// Lift sutil — el correcto para cards
hover:-translate-y-0.5 hover:shadow-md transition-[transform,box-shadow] duration-200 ease-out

// Para buttons: scale en active, no hover
active:scale-[0.97] transition-transform duration-75
```

### ❌ outline-none sin reemplazo
**Pattern:** `className="outline-none focus:outline-none"` sin `focus-visible:ring-2`
**Problema:** Elimina la accesibilidad de navegación por teclado.
**Fix:**
```tsx
className="outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
// shadcn/ui lo aplica por default en sus componentes — usar esos en lugar de elementos nativos directos
```

### ❌ Disabled state visualmente idéntico al normal
**Pattern:** El estado disabled no tiene cambio visual claro.
**Fix:** `disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none`

### ❌ Loading state que colapsa el layout
**Pattern:**
```tsx
{isLoading ? (
  <div className="flex items-center justify-center py-8">
    <Spinner />
  </div>
) : (
  <ul>...</ul>
)}
```
**Problema:** El spinner tiene altura diferente al contenido — cuando carga, el layout "salta".
**Fix:** Skeleton que preserva exactamente la forma del contenido final.

---

## CATEGORÍA: Color

### ❌ Usar color como único diferenciador
**Pattern:** El estado "seleccionado" solo cambia el color del texto.
**Problema:** Falla para usuarios con daltonismo y baja visión.
**Fix:** Color + peso de fuente, o color + background, o color + ícono.

### ❌ Más de 3 colores de acento
**Pattern:** Usar `blue`, `green`, `yellow`, `red`, `purple` todos en la misma pantalla como colores
de acento.
**Fix:** 1 color de acento principal, colores semánticos para estados (success=green, error=red,
warning=amber, info=blue), y todo lo demás en neutros.

### ❌ El acento no acenta
**Pattern:** El color de acento aparece en el 60% de los elementos (backgrounds, borders, texto, icons).
**Fix:** El color de acento debe aparecer en ≤20% de la UI. Si está en todo, no acenta nada.

---

## CATEGORÍA: Dark mode

### ❌ Dark mode como `bg-gray-900` sobre `bg-white`
**Pattern:** Light mode blanco puro, dark mode negro/gris muy oscuro.
**Problema:** El contraste extremo causa fatiga visual.
**Fix para dark:** `bg-zinc-950` como fondo más oscuro, `bg-zinc-900` para cards, `bg-zinc-800`
para inputs — escala de grises con diferencias sutiles entre capas.

### ❌ Colores que no tienen variante dark
**Pattern:** `text-gray-700` hardcoded sin `dark:text-gray-300`
**Fix:** Usar tokens de shadcn/ui (`text-foreground`, `text-muted-foreground`, `bg-background`,
`bg-card`) — ya tienen dark mode integrado.

---

## CATEGORÍA: Mobile

### ❌ Tap targets < 44px
**Pattern:** Ícono de 16px como botón sin padding.
```tsx
// MAL
<button><Icon className="w-4 h-4" /></button>

// BIEN — padding compensa el tamaño del ícono
<button className="p-2.5"><Icon className="w-4 h-4" /></button>
// 10px padding × 2 + 16px icon = 36px — todavía pequeño
// Mejor: p-3 (12px × 2 + 16px = 40px) o p-3.5 (14px × 2 + 16px = 44px) ✓
```

### ❌ Texto que se trunca incorrectamente en mobile
**Pattern:** Texto largo sin `break-words` o con `whitespace-nowrap` en contenedores flex.
**Fix:** `truncate` con `title` attribute para un-line truncation. `line-clamp-2` para multiline.
`break-words` para strings sin espacios (URLs, emails).

---

## CATEGORÍA: UX Writing

### ❌ Labels de botones como estados, no acciones
- ❌ "Submit" → ✅ "Guardar cambios"
- ❌ "Proceed" → ✅ "Continuar al pago"
- ❌ "Confirm" → ✅ "Confirmar eliminación"
- ❌ "OK" → ✅ La acción específica ("Entendido", "Cerrar", "Volver")

### ❌ Placeholder como label
**Pattern:** Solo `placeholder="Escribe tu email"` sin `<label>`.
**Problema:** El placeholder desaparece cuando el usuario empieza a escribir.
**Fix:** `<label>` visible siempre. Placeholder solo para formato de ejemplo ("ej: ana@empresa.com").

### ❌ Mensajes de error técnicos
- ❌ "Error 422: Validation failed on field email" 
- ✅ "El email no tiene un formato válido"
- ❌ "Request failed with status 500"
- ✅ "No se pudo guardar. Intenta de nuevo."
