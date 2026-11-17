#!/usr/bin/env python3
"""
plan_publicacion.py — Paso 7 de trial-reels-lab-f100k.

Escribe PLAN_PUBLICACION.md con el cronograma exacto de la tanda y, con
--recordatorios, crea los avisos reales en Apple Reminders para los dos
momentos que se pasan solos:

  - el chequeo de las 48 horas (empujar el ganador al grid)
  - el control diario de la regla del 25%

Uso:
    python3 plan_publicacion.py <carpeta_TRIAL_REELS> [--recordatorios]
                                [--inicio "2026-07-23 14:00"] [--lista "Contenido"]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Separación entre publicaciones de una misma tanda: si salen de golpe,
# compiten entre ellas por la misma ventana de distribución.
SEPARACION_MIN = 5
LIMITE_DIARIO = 5
# La ventana de mejor rendimiento de esta cuenta.
FRANJA = "14:00–22:00 hora Colombia"


def redondear_a_hora_util(dt: datetime) -> datetime:
    """Si cae fuera de la franja, empuja al siguiente arranque de franja."""
    if dt.hour < 14:
        return dt.replace(hour=14, minute=0, second=0, microsecond=0)
    if dt.hour >= 22:
        return (dt + timedelta(days=1)).replace(
            hour=14, minute=0, second=0, microsecond=0
        )
    return dt.replace(second=0, microsecond=0)


def crear_recordatorio(titulo: str, nota: str, cuando: datetime,
                       lista: str) -> bool:
    """AppleScript contra Recordatorios. Devuelve False si no se pudo."""
    def q(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    # La fecha se arma por componentes, no como texto: `date "25/07/2026"`
    # se interpreta según el idioma del sistema y falla en otras
    # configuraciones. El `set day to 1` previo evita el desbordamiento al
    # cambiar de mes (día 31 sobre un mes de 30).
    script = f'''
    set d to current date
    set day of d to 1
    set year of d to {cuando.year}
    set month of d to {cuando.month}
    set day of d to {cuando.day}
    set time of d to ({cuando.hour} * hours + {cuando.minute} * minutes)
    tell application "Reminders"
        set destino to missing value
        repeat with L in lists
            if name of L is "{q(lista)}" then set destino to L
        end repeat
        if destino is missing value then set destino to default list
        tell destino
            make new reminder with properties {{name:"{q(titulo)}", body:"{q(nota)}", remind me date:d}}
        end tell
    end tell
    '''
    cp = subprocess.run(["osascript", "-e", script],
                        capture_output=True, text=True)
    if cp.returncode != 0:
        print(f"⚠ No se pudo crear el recordatorio «{titulo}»: "
              f"{cp.stderr.strip()}", file=sys.stderr)
        return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("carpeta", type=Path)
    ap.add_argument("--recordatorios", action="store_true")
    ap.add_argument("--inicio", default=None,
                    help='"AAAA-MM-DD HH:MM"; por defecto, ahora')
    ap.add_argument("--lista", default="Recordatorios",
                    help="lista de Apple Reminders")
    args = ap.parse_args()

    base = args.carpeta.expanduser().resolve()
    cfg = json.loads((base / "variantes.json").read_text(encoding="utf-8"))
    variantes = cfg["variantes"]

    if len(variantes) > LIMITE_DIARIO:
        sys.exit(f"{len(variantes)} variantes superan el límite de "
                 f"{LIMITE_DIARIO} trial reels al día. Partir la tanda en dos.")

    inicio = (datetime.strptime(args.inicio, "%Y-%m-%d %H:%M")
              if args.inicio else datetime.now())
    inicio = redondear_a_hora_util(inicio)

    horarios = [inicio + timedelta(minutes=SEPARACION_MIN * i)
                for i in range(len(variantes))]
    corte_48h = horarios[-1] + timedelta(hours=48)
    control_25 = horarios[-1] + timedelta(hours=24)

    modo = cfg.get("modo", "video")
    archivo = (lambda v: f"VARIANTE_{v['id']}.mp4") if modo == "video" \
        else (lambda v: f"overlay_{v['id']}.mov (montar sobre la base)")

    L = [
        f"# Plan de publicación — {cfg.get('proyecto', 'tanda de trial reels')}",
        "",
        f"Generado el {datetime.now():%d/%m/%Y %H:%M} · "
        f"{len(variantes)} variantes · franja objetivo {FRANJA}",
        "",
        "## Cronograma",
        "",
        "| Hora | Variante | Celda | Archivo | Mutación |",
        "|---|---|---|---|---|",
    ]
    for v, h in zip(variantes, horarios):
        L.append(
            f"| {h:%H:%M} | {v['id']} | {v['celda']} | `{archivo(v)}` | "
            f"{v.get('mutacion', 'none')} |"
        )

    L += [
        "",
        f"Las {len(variantes)} se publican **como trial reels**, con "
        f"{SEPARACION_MIN} minutos de separación. Ninguna va al grid todavía.",
        "",
        f"## Caption (idéntica en las {len(variantes)})",
        "",
        "```",
        cfg.get("caption", "— pendiente —"),
        "```",
        "",
        f"La misma caption en las {len(variantes)} es seguro: no cuenta como "
        "contenido "
        "duplicado. Lo único que debe cambiar son los primeros segundos "
        "visuales.",
        "",
        "## Qué mirar para elegir ganadora",
        "",
        "No basta con las vistas. Comparar, en este orden:",
        "",
        "1. Vistas — la señal gruesa",
        "2. Tiempo promedio de reproducción — más alto, mejor",
        "3. Tasa de skip — más baja, mejor",
        "4. Gráfico de retención — se busca caída inicial que **se aplane**; "
        "si sigue cayendo, el gancho atrajo a quien no era",
        "5. Comentarios — la señal de lead, la que más pesa si hay CTA",
        "",
        "Una variante con menos vistas pero retención plana y más comentarios "
        "puede ser mejor candidata que la de más vistas.",
        "",
        "## Cuándo empujar al grid",
        "",
        f"- **Regla de 48h — antes de {corte_48h:%d/%m %H:%M}.** Empujada dentro "
        "de esa ventana, entra al feed de tus seguidores como post normal y "
        "recibe re-engagement. Funciona aunque el engagement ya se haya "
        "enfriado.",
        f"- **Regla del 25% — control diario desde {control_25:%d/%m %H:%M}.** "
        "Si un día suma menos del 25% de vistas que el día anterior, ya se "
        "pasó el punto: se está muriendo en el algoritmo de trials y empujarla "
        "no rescata nada.",
        "",
        "Vale la que llegue primero.",
        "",
        "## Play A o Play B",
        "",
        "- **Play A** (Administrar trial reels → publicar en el perfil): para "
        "un formato raro o que sirve a otro ICP. Llega al grid con la prueba "
        "social ya puesta.",
        "- **Play B** (subirla fresca al grid): para un hit evidente que encaja "
        "con lo que tus seguidores ya quieren. Quedan dos cohetes a la vez.",
        "",
        "## Después",
        "",
        f"- Reciclar esta tanda a partir del **{horarios[-1] + timedelta(days=60):%d/%m/%Y}** "
        "(60 días), con una mutación distinta.",
        "- Ganadora + 4 ganchos nuevos × 4 mutaciones = 16 publicaciones del "
        "mismo material.",
        "- No superar 5 trial reels al día y mantener 3 posts al grid por semana.",
        "",
        "## Por qué existe cada variante",
        "",
    ]
    for v in variantes:
        L.append(f"- **{v['id']} ({v['celda']}):** {v.get('por_que', '—')}")
    L.append("")

    destino = base / "PLAN_PUBLICACION.md"
    destino.write_text("\n".join(L), encoding="utf-8")
    print(f"✓ {destino}")

    if not args.recordatorios:
        print("  (sin recordatorios; agregar --recordatorios para crearlos)")
        return

    if sys.platform != "darwin":
        print("⚠ Los recordatorios solo funcionan en macOS.", file=sys.stderr)
        return

    proyecto = cfg.get("proyecto", "tanda")
    creados = 0
    creados += crear_recordatorio(
        f"Trial reels — empujar ganadora al grid ({proyecto})",
        f"Vence la regla de 48h. Comparar vistas, retención y comentarios de "
        f"las {len(variantes)} variantes y empujar la ganadora (Play A o B). "
        f"Plan: {destino}",
        corte_48h - timedelta(hours=6),
        args.lista,
    )
    creados += crear_recordatorio(
        f"Trial reels — control del 25% ({proyecto})",
        "Anotar las vistas de cada variante. Si una sumó menos del 25% que "
        "ayer, ya se pasó el punto de empujarla al grid.",
        control_25,
        args.lista,
    )
    print(f"  {creados}/2 recordatorios creados en «{args.lista}»")


if __name__ == "__main__":
    main()
