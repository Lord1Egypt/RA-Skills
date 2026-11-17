#!/usr/bin/env python3
"""
build_overlays.py — Paso 5 de trial-reels-lab-f100k.

Lee variantes.json y arma una composición HyperFrames por variante, lista
para renderizar con alfa real. Cada composición vive en su propia carpeta con
el pack tipográfico F100K copiado dentro (Chrome bloquea file:// absoluto, así
que las fuentes tienen que ser rutas relativas).

Un layout por celda de la matriz:
    claim     — bloque de texto grande, palabra de acento resaltada
    visual    — asset (logo intervenido / captura / pop culture) + texto corto
    conflicto — texto con el verbo de ruptura en caja de acento
    prueba    — cifra enorme + subtexto, con captura opcional

Uso:
    python3 build_overlays.py <carpeta_TRIAL_REELS>
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import re
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
FONTS_DIR = SKILL_DIR / "fonts"

# Paleta validada: blanco + acento amarillo neón, siempre con contorno negro.
ACENTO = "#FFE03D"
CONTORNO = "#000000"

# Referencia de diseño. Todo se escala proporcionalmente a la altura real.
REF_ALTO = 1920
# El overlay inferior apoya a la altura del pecho, nunca sobre la barbilla.
BOTTOM_INFERIOR_REF = 520
# Si no se midió el hairline mirando el frame, se asume el 42% desde arriba.
HAIRLINE_FRAC = 0.42

CELDAS_VALIDAS = {"claim", "visual", "conflicto", "prueba"}

# Ancho medio de un carácter en la display (Anton) en mayúsculas, como
# fracción del font-size. Medido con margen para no quedarse corto.
RATIO_DISPLAY = 0.52
RATIO_SANS = 0.58
# Margen horizontal a cada lado del bloque de texto.
PADDING_REF = 72


# Caracteres por línea que mantienen la display en un cuerpo legible.
MAX_CHARS_LINEA = 20
# Por debajo de esto el gancho no se lee en el primer segundo.
MIN_LEGIBLE_REF = 64


def equilibrar_lineas(texto: str, max_chars: int = MAX_CHARS_LINEA) -> str:
    """
    Reparte el texto en líneas cortas respetando los saltos ya escritos.

    Encoger la fuente hasta que quepa todo en una línea deja el gancho
    ilegible; es mejor repartirlo en dos o tres líneas y conservar el cuerpo.

    El reparto es EQUILIBRADO, no codicioso: `textwrap` llenaría la primera
    línea al máximo y dejaría una huérfana ("…en 4 / minutos"), que se lee
    peor justo en el segundo que decide si te ven.
    """
    import math
    import textwrap

    salida: list[str] = []
    for original in texto.split("\n"):
        if not original.strip():
            continue
        if len(original) <= max_chars:
            salida.append(original)
            continue
        n_lineas = math.ceil(len(original) / max_chars)
        ancho_equilibrado = math.ceil(len(original) / n_lineas)
        # Se sube el ancho hasta que quepa en el nº de líneas previsto: una
        # palabra larga puede forzar una línea extra si se aprieta demasiado.
        for w in range(ancho_equilibrado, max_chars + 1):
            trozos = textwrap.wrap(original, width=w, break_long_words=False,
                                   break_on_hyphens=False)
            if len(trozos) <= n_lineas:
                break
        salida.extend(trozos)
    return "\n".join(salida) or texto


def ajustar_font_size(texto: str, ancho_disponible: int, maximo: int,
                      ratio: float, minimo: int = 40) -> int:
    """
    Baja el tamaño hasta que la línea más larga entre en el ancho disponible.

    Red de seguridad después de `equilibrar_lineas`: si aun así no cabe, es
    que el gancho es demasiado largo para el primer segundo.
    """
    lineas = [l for l in texto.split("\n") if l.strip()]
    if not lineas:
        return maximo
    mas_larga = max(len(l) for l in lineas)
    if mas_larga == 0:
        return maximo
    cabe = int(ancho_disponible / (mas_larga * ratio))
    return max(minimo, min(maximo, cabe))


def esc(texto: str) -> str:
    """Escapa y convierte saltos de línea del JSON en <br>."""
    return "<br>".join(html.escape(l) for l in texto.split("\n"))


def partir_por_acento(texto: str, acento: str | None) -> tuple[str, str, str] | None:
    """
    Localiza el acento tolerando que el reparto en líneas haya metido un salto
    donde antes había un espacio. Devuelve (antes, acento_real, despues).
    """
    if not acento or not acento.strip():
        return None
    patron = r"\s+".join(re.escape(p) for p in acento.split())
    m = re.search(patron, texto)
    if not m:
        return None
    return texto[:m.start()], m.group(0), texto[m.end():]


def resaltar(texto: str, acento: str | None) -> str:
    """Envuelve el fragmento de acento en un <span> resaltado."""
    partes = partir_por_acento(texto, acento)
    if partes is None:
        return esc(texto)
    antes, real, despues = partes
    return f"{esc(antes)}<span class='acento'>{esc(real)}</span>{esc(despues)}"


def data_uri(ruta: Path) -> str:
    """Los assets se embeben para que la composición sea autocontenida."""
    mime = mimetypes.guess_type(ruta.name)[0] or "image/png"
    b64 = base64.b64encode(ruta.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def css_base(ancho: int, alto: int, escala: float) -> str:
    px = lambda v: round(v * escala)
    return f"""
@import url("./fonts/fonts.css");

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

/* Fondo transparente: el render sale con alfa real, sin chroma. */
body {{ background: transparent; }}

#root {{
  position: relative;
  width: {ancho}px;
  height: {alto}px;
  overflow: hidden;
  background: transparent;
}}

.zona {{
  position: absolute;
  left: 0;
  right: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: {px(24)}px;
  padding: 0 {px(72)}px;
}}

/* El borde INFERIOR del bloque superior descansa al ras del cabello. */
.zona.superior {{ bottom: var(--desde-abajo); }}
.zona.inferior {{ bottom: {px(BOTTOM_INFERIOR_REF)}px; }}

.linea {{
  font-family: "F100K Display", Anton, Impact, sans-serif;
  font-size: {px(112)}px;
  line-height: 1.02;
  letter-spacing: -0.01em;
  text-transform: uppercase;
  text-align: center;
  color: #FFFFFF;
  -webkit-text-stroke: {px(6)}px {CONTORNO};
  paint-order: stroke fill;
  text-shadow: 0 {px(8)}px {px(24)}px rgba(0,0,0,.45);
}}

.acento {{ color: {ACENTO}; }}

.caja-acento {{
  display: inline-block;
  background: {ACENTO};
  color: #000000;
  -webkit-text-stroke: 0;
  padding: {px(6)}px {px(22)}px {px(12)}px;
  border-radius: {px(12)}px;
  text-shadow: none;
}}

.cifra {{
  font-family: "F100K Display", Anton, Impact, sans-serif;
  font-size: {px(220)}px;
  line-height: 0.92;
  color: {ACENTO};
  -webkit-text-stroke: {px(8)}px {CONTORNO};
  paint-order: stroke fill;
  text-align: center;
}}

.subtexto {{
  font-family: "F100K Sans", Inter, system-ui, sans-serif;
  font-weight: 800;
  font-size: {px(56)}px;
  line-height: 1.15;
  text-align: center;
  color: #FFFFFF;
  -webkit-text-stroke: {px(4)}px {CONTORNO};
  paint-order: stroke fill;
}}

.asset-wrap {{ position: relative; display: inline-block; }}

/* Los assets con transparencia nunca van fullscreen: dejarían ver la cara
   por los huecos. Se acotan a un bloque. */
.asset {{
  display: block;
  max-width: {px(560)}px;
  max-height: {px(560)}px;
  filter: drop-shadow(0 {px(10)}px {px(28)}px rgba(0,0,0,.5));
}}

.asset.captura {{
  max-width: {px(760)}px;
  border-radius: {px(20)}px;
  border: {px(5)}px solid #FFFFFF;
}}

.emoji {{
  position: absolute;
  right: -{px(28)}px;
  bottom: -{px(24)}px;
  font-size: {px(160)}px;
  line-height: 1;
  filter: drop-shadow(0 {px(8)}px {px(18)}px rgba(0,0,0,.5));
}}
"""


def preparar(texto: str, ancho: int, escala: float, maximo_ref: int,
             ratio: float = RATIO_DISPLAY, etiqueta: str = "",
             max_chars: int = MAX_CHARS_LINEA) -> tuple[str, str]:
    """
    Reparte el texto en líneas legibles y calcula su font-size.

    Devuelve (texto_repartido, style). Avisa si el resultado queda por debajo
    del umbral legible: eso significa que el gancho es demasiado largo para
    los primeros segundos, y conviene acortarlo en vez de encogerlo.
    """
    repartido = equilibrar_lineas(texto, max_chars)
    disponible = ancho - 2 * round(PADDING_REF * escala)
    px = ajustar_font_size(
        repartido, disponible, round(maximo_ref * escala), ratio,
        minimo=round(40 * escala),
    )
    # Solo avisa si el texto tuvo que encogerse por debajo del umbral; un
    # subtexto cuyo máximo ya es pequeño por diseño no es un problema.
    umbral = round(min(MIN_LEGIBLE_REF, maximo_ref) * escala)
    if px < umbral:
        print(
            f"⚠ {etiqueta}: el texto queda a {px}px, por debajo del umbral "
            f"legible. Acortar el gancho — el criterio pide 8-12 palabras.",
            file=sys.stderr,
        )
    return repartido, f"font-size:{px}px"


def cuerpo_claim(v: dict, escala: float, ancho: int) -> str:
    texto, estilo = preparar(v["texto"], ancho, escala, 112,
                             etiqueta=f"variante {v['id']}")
    return (f"<div class='linea' id='l1' style='{estilo}'>"
            f"{resaltar(texto, v.get('acento'))}</div>")


def cuerpo_conflicto(v: dict, escala: float, ancho: int) -> str:
    # La caja de acento añade relleno lateral: se descuenta del ancho útil.
    texto, estilo = preparar(v["texto"], ancho - round(60 * escala), escala,
                             96, etiqueta=f"variante {v['id']}", max_chars=17)
    partes = partir_por_acento(texto, v.get("acento"))
    if partes is None:
        interior = esc(texto)
    else:
        antes, real, despues = partes
        interior = (f"{esc(antes)}<span class='caja-acento'>{esc(real)}</span>"
                    f"{esc(despues)}")
    return f"<div class='linea' id='l1' style='{estilo}'>{interior}</div>"


def cuerpo_visual(v: dict, escala: float, ancho: int, base_dir: Path) -> str:
    partes = []
    if v.get("asset"):
        ruta = (base_dir / v["asset"]).resolve()
        if not ruta.exists():
            sys.exit(f"[{v['id']}] falta el asset: {ruta}")
        emoji = (
            f"<span class='emoji'>{html.escape(v['emoji'])}</span>"
            if v.get("emoji") else ""
        )
        partes.append(
            f"<div class='asset-wrap' id='asset'>"
            f"<img class='asset' src='{data_uri(ruta)}' alt=''>{emoji}</div>"
        )
    if v.get("texto"):
        texto, estilo = preparar(v["texto"], ancho, escala, 96,
                                 etiqueta=f"variante {v['id']}", max_chars=18)
        partes.append(
            f"<div class='linea' id='l1' style='{estilo}'>"
            f"{resaltar(texto, v.get('acento'))}</div>"
        )
    return "\n      ".join(partes)


def cuerpo_prueba(v: dict, escala: float, ancho: int, base_dir: Path) -> str:
    partes = []
    if v.get("asset"):
        ruta = (base_dir / v["asset"]).resolve()
        if not ruta.exists():
            sys.exit(f"[{v['id']}] falta el asset: {ruta}")
        partes.append(
            f"<img class='asset captura' id='asset' src='{data_uri(ruta)}' alt=''>"
        )
    # La cifra es corta por definición: no se reparte en líneas.
    cifra, estilo = preparar(v["texto"], ancho, escala, 220,
                             etiqueta=f"variante {v['id']} (cifra)",
                             max_chars=14)
    partes.append(f"<div class='cifra' id='l1' style='{estilo}'>"
                  f"{esc(cifra)}</div>")
    if v.get("subtexto"):
        sub, est2 = preparar(v["subtexto"], ancho, escala, 56, RATIO_SANS,
                             etiqueta=f"variante {v['id']} (subtexto)",
                             max_chars=28)
        partes.append(f"<div class='subtexto' id='l2' style='{est2}'>"
                      f"{esc(sub)}</div>")
    return "\n      ".join(partes)


def timeline_js(v: dict) -> str:
    """
    Entrada rápida — el gancho tiene que estar legible casi desde el frame 0.
    Se usa fromTo, nunca .from con opacity: .from deja el elemento visible si
    el render arranca antes de que el tween corra.
    """
    lineas = [
        'window.__timelines = window.__timelines || {};',
        'const tl = gsap.timeline({ paused: true });',
    ]
    if v["celda"] in ("visual", "prueba") and v.get("asset"):
        lineas.append(
            'tl.fromTo("#asset", { scale: 0.86, opacity: 0 }, '
            '{ scale: 1, opacity: 1, duration: 0.34, ease: "back.out(1.6)" }, 0);'
        )
    lineas.append(
        'tl.fromTo("#l1", { y: 34, opacity: 0 }, '
        '{ y: 0, opacity: 1, duration: 0.30, ease: "power3.out" }, 0.06);'
    )
    if v.get("subtexto"):
        lineas.append(
            'tl.fromTo("#l2", { y: 22, opacity: 0 }, '
            '{ y: 0, opacity: 1, duration: 0.26, ease: "power3.out" }, 0.22);'
        )
    lineas.append(f'window.__timelines["{v["id"].lower()}"] = tl;')
    return "\n      ".join(lineas)


def construir(v: dict, cfg: dict, base_dir: Path, destino: Path) -> None:
    ancho, alto = cfg["resolucion"]
    escala = alto / REF_ALTO
    dur = round(float(v.get("salida", cfg["duracion_overlay"]))
                - float(v.get("entrada", 0.0)), 3)
    if dur <= 0:
        sys.exit(f"[{v['id']}] la duración del overlay es {dur}s.")

    posicion = v.get("posicion", "superior")
    if posicion == "centro":
        sys.exit(f"[{v['id']}] posición 'centro' está prohibida: tapa la cara.")
    if posicion not in ("superior", "inferior"):
        sys.exit(f"[{v['id']}] posición desconocida: {posicion}")

    hairline = cfg.get("hairline_y") or round(alto * HAIRLINE_FRAC)
    desde_abajo = max(0, alto - int(hairline))

    celda = v["celda"]
    if celda == "claim":
        cuerpo = cuerpo_claim(v, escala, ancho)
    elif celda == "conflicto":
        cuerpo = cuerpo_conflicto(v, escala, ancho)
    elif celda == "visual":
        cuerpo = cuerpo_visual(v, escala, ancho, base_dir)
    elif celda == "prueba":
        cuerpo = cuerpo_prueba(v, escala, ancho, base_dir)
    else:
        sys.exit(f"[{v['id']}] celda desconocida: {celda}")

    destino.mkdir(parents=True, exist_ok=True)
    fuentes = destino / "fonts"
    if fuentes.exists():
        shutil.rmtree(fuentes)
    shutil.copytree(FONTS_DIR, fuentes)

    (destino / "styles.css").write_text(
        css_base(ancho, alto, escala), encoding="utf-8"
    )

    doc = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={ancho}, height={alto}" />
    <title>Trial Reels — variante {v['id']} ({celda})</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <div
      id="root"
      data-composition-id="{v['id'].lower()}"
      data-start="0"
      data-width="{ancho}"
      data-height="{alto}"
      data-duration="{dur}"
    >
      <section
        class="zona {posicion}"
        style="--desde-abajo: {desde_abajo}px"
        data-start="0"
        data-duration="{dur}"
        data-track-index="1"
      >
      {cuerpo}
      </section>
    </div>
    <script>
      {timeline_js(v)}
    </script>
  </body>
</html>
"""
    (destino / "index.html").write_text(doc, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("carpeta", type=Path, help="carpeta TRIAL_REELS")
    args = ap.parse_args()

    base = args.carpeta.expanduser().resolve()
    spec = base / "variantes.json"
    if not spec.exists():
        sys.exit(f"Falta {spec}. Escribirlo primero (ver matriz-variantes.md).")

    cfg = json.loads(spec.read_text(encoding="utf-8"))
    variantes = cfg.get("variantes") or []
    if not variantes:
        sys.exit("variantes.json no tiene variantes.")

    # La matriz es forzada: si dos variantes comparten celda, el test no
    # enseña nada y no vale la pena gastar el render.
    celdas = [v.get("celda") for v in variantes]
    desconocidas = set(celdas) - CELDAS_VALIDAS
    if desconocidas:
        sys.exit(f"Celdas desconocidas: {sorted(desconocidas)}")
    repetidas = {c for c in celdas if celdas.count(c) > 1}
    if repetidas:
        sys.exit(
            f"Celdas repetidas: {sorted(repetidas)}. La matriz exige una celda "
            "distinta por variante — si no, el A/B no informa. Ver "
            "matriz-variantes.md."
        )

    cfg.setdefault("resolucion", [1080, 1920])
    cfg.setdefault("duracion_overlay", 3.0)

    for v in variantes:
        destino = base / f"comp_{v['id']}"
        construir(v, cfg, base, destino)
        print(f"✓ {destino}/index.html  ({v['celda']}, {v.get('posicion')})")

    print(f"\nPrevisualizar antes de renderizar:")
    print(f"  hyperframes preview \"{base}/comp_{variantes[0]['id']}\" --frame 1.0")


if __name__ == "__main__":
    main()
