# Criterio de gancho — de dónde sale "lo que funciona"

Tres capas, en orden de autoridad. Cuando se contradicen, **gana la de arriba**.

---

## Capa 1 — Los datos de la cuenta (máxima autoridad)

Lo que ganó **en esta cuenta** vence a cualquier estudio general.

**Si usas esta skill en tu propia cuenta:** la Capa 1 son *tus* datos, no los del usuario. Antes de escribir las variantes, mira tus 5 reels con más alcance y tus 5 peores de los últimos 30 días y contesta: ¿qué carga el gancho en los buenos —texto, imagen o lo que dices—? ¿Abren declarando o preguntando? ¿Sale objeto en mano? Eso manda sobre todo lo demás. Si no tienes historial suficiente, salta a la Capa 2 y **dilo** — es justamente lo que los trial reels vienen a resolver.

**Para la cuenta del usuario:** leer `cerebro/memoria/patterns_ig_<handle>.md` (lo actualiza `patron-ig-f100k` cada semana). Leer patrones VIRALES (repetir) y NEGATIVOS (evitar). Si ese archivo no existe, **decirlo en voz alta** y seguir con la Capa 2 — no inventar patrones de cuenta.

**Ejemplo de una Capa 1 ya construida (auditoría de los reels de una cuenta de nicho marketing)** — sirve de ejemplo de cómo se ve una Capa 1 bien hecha:

- La brecha entre su mejor reel y el peor es de **cientos de veces**, y no la explica la duración, ni el CTA, ni que el contenido "no guste" — los peores tienen *más* likes por vista. La explica el gancho y su ejecución en el segundo 1.
- **Textual:** promesa + NÚMERO desde el frame 0, que cambia cada 2-3s. Nunca texto-etiqueta ("Lista de formatos").
- **Visual:** ojos clavados a cámara + objeto en mano + gesto + buena luz. Nunca manos entrelazadas, mirada al teléfono, prop irrelevante, ni grabado en el auto.
- **Verbal:** primera frase = dato, cifra o conflicto. Hablar de *tú*, no de "mis/yo". Vender el resultado, no la función. Cero "Ok…" / "Así es como…".
- **Contradicción importante:** en ESA cuenta el carrier **visual rindió peor** y el textual/verbal ganó. No fue estadísticamente significativo (muestra chica) pero la dirección fue consistente. → **No forzar gancho visual como default.** La celda B de la matriz existe justamente para poner esto a prueba sin costo, que es lo que un trial reel permite.

**Ganchos visuales que sí le funcionaron a esa cuenta:** referencia de cultura pop + promesa concreta, logo de una app intervenido con símbolo emocional (💔 ⚠️ ✓ X), "Terminé con [APP]" + logo + 💔, "Principiante / Pro" con burbujas de chat. El logo **limpio, sin intervenir, no funcionó**.

---

## Capa 2 — Las 300 fichas re-observadas

Observación honesta de los primeros 3 segundos de 300 virales en español, hecha sobre **frames reales** (no reconstruida).

El dataset crudo no viene en este paquete; si la usuaria lo tiene, estaría en:

```
cerebro/1000-ganchos/data/fichas_observadas/fichas300.json
```

**Si ese archivo no existe** (caso normal en este agente), no pasa nada: los hallazgos que importan están resumidos abajo y son suficientes para llenar la matriz. Lo que **no** se puede hacer es inventar cortes por nicho que no estén en esta lista — si hace falta un número que solo salga del JSON y el JSON no está, se dice y se sigue.

Lo que aporta:

- **88%** abre con texto en pantalla · **77%** muestra cara · **~73%** cámara fija · **41%** objeto en mano · **30%** tiene un corte dentro de los 3s.
- **El carrier se invierte por nicho.** En nichos de dinero (ventas, negocios, marca personal, emprendimiento, finanzas, mindset; n=175) el gancho lo carga el **texto 66%** vs visual 28%. En cocina/belleza/relaciones el visual sube a 44% y en cocina domina. → El nicho decide qué celda de la matriz es el *default* y cuál es la *apuesta*.
- **El movimiento lo pone el cuerpo, no la edición:** plano fijo 73% + cuerpo que entra al cuadro 62%, y solo 2% corta el plano dentro de los 3s.
- El modelo dejó campos en `null` cuando no se veía (12% del texto, 16% del objeto). Ese `null` es un dato, no un hueco que rellenar.

**Techo de este dato:** es descriptivo, no causal. No hay grupo de control limpio. Se usa para **elegir qué probar**, nunca para prometer un resultado.

---

## Capa 3 — Los tipos de gancho como rotación

La taxonomía de tipos de gancho (vacío de información, de resultado, de conflicto, filtrante, etc.) sirve para **variar** —no repetir siempre el mismo— pero el tipo por sí solo **no discrimina** entre viral y flop: dentro de los virales explica el 0.34% de la varianza (Kruskal p=0.159). El carrier —*quién* carga el gancho— explica 7.5× más.

Traducción práctica: no gastar la corrida buscando "el tipo correcto". Gastarla variando **quién carga el gancho** y **cómo se ejecuta el segundo 1**. Eso es exactamente lo que hace la matriz de 4 celdas.

---

## REGLA DE HONESTIDAD (no negociable)

Una auditoría de 5 lentes (17-jul-2026) encontró que **la mitad de los hallazgos del estudio original no existían** — eran cadenas de texto escritas a mano en el código, nunca calculadas. El plan de propagarlos a 6 skills se canceló. Esta skill hereda la regla:

**Prohibido citar, en cualquier salida al usuario o al editor:**

- ❌ "+42% por usar un número" → medido de verdad: +0% (Mann-Whitney p=0.718)
- ❌ "abrir declarando 4.6% vs 9.3%" → nunca se calculó; al medir contra control se invierte
- ❌ "mediana 11 palabras" → contaminado con metadata del anotador. Limpio: **8 palabras**
- ❌ Cualquier "×N" del estudio original. `outlier_sc` es número de MADs en escala log, **no** un multiplicador de vistas. Hay controles negativos, imposible para un "×"
- ❌ Todo el bloque "viral vs flop" (pilar emocional, zona flop, matriz nicho×gancho): el control se eligió tomando los peores por outlier → circular por construcción

**Prohibido además:**

- Llamar "fórmula que se repite" a un ranking de medianas sin test de significancia. Las muestras por plantilla son chicas.
- Pintar de rojo / marcar como ley cualquier diferencia que no pase un test. Ejemplo real: "sin cara rinde más" salió de filtrar un subconjunto de n=26 — al medir bien, p=0.87 y si acaso rinde *menos*.
- Inventar patrones de la cuenta cuando no hay archivo de patrones. Se dice que no se pudo leer y se sigue.

**Permitido:** los números de la Capa 1 (son mediciones directas de la cuenta), los porcentajes descriptivos de la Capa 2 presentados **como descripción**, y decir "no lo sabemos, por eso lo testeamos" — que es literalmente el propósito de esta skill.

Cuando haya duda sobre si un número es citable: **no citarlo.** El trial reel existe para generar el dato, no para adornarlo.
