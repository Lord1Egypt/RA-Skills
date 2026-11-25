#!/usr/bin/env python3
"""Review explicit Klipper/Orca extrusion centerlines; never execute G-code.

Feature-colored toolpath review is inspired by bbolinger/snapmaker-u1-toolkit.
See references/licenses/snapmaker-u1-toolkit-MIT.txt. No toolkit runtime is used.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import tempfile

import numpy as np

EPS = 1e-6
NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)"
PARAM = re.compile(r"([A-Z])\s*(" + NUMBER + r")", re.I)
SCOPE = "Explicit extrusion centerlines in millimeters, all slicer features/layers except TYPE:Custom. Firmware macros, homing, offsets from the printer, bead width and toolhead clearance are not simulated."


def _polygon(value, name):
    try:
        points = np.asarray([[float(v) for v in p.split('x')] for p in value], dtype=float)
    except (TypeError, ValueError, AttributeError) as exc:
        raise ValueError(f'{name} must contain finite x/y coordinate strings') from exc
    if points.ndim != 2 or points.shape[1] != 2 or not np.isfinite(points).all():
        raise ValueError(f'{name} must contain finite x/y coordinates')
    if len(points) > 1 and np.array_equal(points[0], points[-1]):
        points = points[:-1]
    if len(points) < 3:
        raise ValueError(f'{name} needs at least three vertices')
    area = sum(np.linalg.det(np.array([a, b])) for a, b in zip(points, np.roll(points, -1, axis=0)))
    if abs(area) < EPS or np.any(np.linalg.norm(points - np.roll(points, 1, axis=0), axis=1) < EPS):
        raise ValueError(f'{name} has zero area or duplicate adjacent vertices')
    # Reject self-crossing profiles rather than choosing a winding interpretation.
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if j == i + 1 or (i == 0 and j == len(points) - 1):
                continue
            a, b = points[i], points[(i + 1) % len(points)]
            c, d = points[j], points[(j + 1) % len(points)]
            dx, dy = b - a
            collinear = all(abs(dx * (p[1] - a[1]) - dy * (p[0] - a[0])) <= EPS for p in (c, d))
            overlap = collinear and np.all(np.maximum(np.minimum(a, b), np.minimum(c, d)) <= np.minimum(np.maximum(a, b), np.maximum(c, d)) + EPS)
            if overlap or _cuts(np.array([a]), np.array([b]), c, d)[0].size:
                raise ValueError(f'{name} is self-intersecting')
    return points


def machine_region(machine):
    if not isinstance(machine, dict):
        raise ValueError('machine settings must be a JSON object')
    bed = _polygon(machine.get('printable_area'), 'printable_area')
    try:
        height = float(machine['printable_height'])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError('printable_height must be finite and positive') from exc
    if not math.isfinite(height) or height <= 0:
        raise ValueError('printable_height must be finite and positive')
    excluded = machine.get('bed_exclude_area', [])
    holes = [] if excluded in ([], ['0x0']) else [_polygon(excluded, 'bed_exclude_area')]
    edges = np.roll(bed, -1, axis=0) - bed
    turns = edges[:, 0] * np.roll(edges, -1, axis=0)[:, 1] - edges[:, 1] * np.roll(edges, -1, axis=0)[:, 0]
    convex = bool(np.all(turns >= -EPS) or np.all(turns <= EPS))
    angles = [math.atan2(-dx, dy) % math.tau for dx, dy in edges]
    angles += [(a + math.pi) % math.tau for a in angles]
    return bed, height, holes, convex, angles


def _cuts(starts, ends, a, b):
    direction = ends - starts
    edge = b - a
    denominator = direction[:, 0] * edge[1] - direction[:, 1] * edge[0]
    nonparallel = np.abs(denominator) > 1e-12
    safe = np.where(nonparallel, denominator, 1.)
    offset = a - starts
    t = (offset[:, 0] * edge[1] - offset[:, 1] * edge[0]) / safe
    u = (offset[:, 0] * direction[:, 1] - offset[:, 1] * direction[:, 0]) / safe
    indices = np.flatnonzero(nonparallel & (t >= 0) & (t <= 1) & (u >= 0) & (u <= 1))
    return indices, t[indices]


def _inside(points, polygon):
    x, y = points[:, 0], points[:, 1]
    inside = np.zeros(len(points), dtype=bool)
    boundary = inside.copy()
    for a, b in zip(polygon, np.roll(polygon, -1, axis=0)):
        dx, dy = b - a
        cross = (x - a[0]) * dy - (y - a[1]) * dx
        boundary |= (np.abs(cross) <= EPS * math.hypot(dx, dy)) & (x >= min(a[0], b[0]) - EPS) & (x <= max(a[0], b[0]) + EPS) & (y >= min(a[1], b[1]) - EPS) & (y <= max(a[1], b[1]) + EPS)
        if dy:
            inside ^= ((a[1] > y) != (b[1] > y)) & (x < a[0] + (y - a[1]) * dx / dy)
    return inside | boundary


def _arc(start, end, params, clockwise, critical_angles):
    if 'R' in params or 'K' in params or not any(params.get(k, 0) for k in ['I', 'J']):
        raise ValueError('only XY I/J-center arcs are supported; Klipper R arcs are unsupported')
    center = start[:2] + [params.get('I', 0), params.get('J', 0)]
    radius = float(np.linalg.norm(start[:2] - center))
    if not math.isclose(radius, float(np.linalg.norm(end[:2] - center)), abs_tol=.01, rel_tol=1e-4):
        raise ValueError('arc endpoint is inconsistent with its I/J radius')
    a = math.atan2(start[1] - center[1], start[0] - center[0])
    b = math.atan2(end[1] - center[1], end[0] - center[0])
    direction = -1 if clockwise else 1
    sweep = ((b - a) * direction) % math.tau
    if sweep < 1e-10:
        sweep = math.tau
    count = max(2, math.ceil(sweep * radius / .5), math.ceil(sweep / math.radians(5)))
    if count > 10000:
        raise ValueError('arc exceeds the supported subdivision limit')
    fractions = list(np.linspace(0, 1, count + 1))
    for angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2, *critical_angles]:
        distance = ((angle - a) * direction) % math.tau
        if 0 < distance < sweep:
            fractions.append(distance / sweep)
    fractions = np.array(sorted(set(fractions)))
    angles = a + direction * sweep * fractions
    points = np.column_stack([center[0] + radius * np.cos(angles), center[1] + radius * np.sin(angles), start[2] + (end[2] - start[2]) * fractions])
    points[0], points[-1] = start, end
    return points


def parse_gcode(text, critical_angles=()):
    """Track Klipper coordinates and extrusion modes; preserve every scoped segment."""
    position = np.array([np.nan, np.nan, np.nan, 0.])
    offset = np.zeros(4)
    absolute_xyz = absolute_e = True
    role, tool, plane = 'Unclassified', 0, 'G17'
    segments, features, lines, tools, errors = [], [], [], [], []
    macros = set()
    arc_moves = custom_moves = 0
    for number, raw in enumerate(text.splitlines(), 1):
        if raw.startswith(';TYPE:'):
            role = raw[6:].strip() or 'Unclassified'
        code = re.sub(r'\([^)]*\)', '', raw.split(';', 1)[0]).strip()
        if not code:
            continue
        match = re.match(r'^([GMT]\d+(?:\.\d+)?)(?=\s|[A-Z]|$)', code, re.I)
        if not match:
            if re.match(r'^(?:[GMT]\d|N\d)', code, re.I):
                errors.append(f'line {number}: malformed or unsupported numbered command')
                continue
            macros.add(code.split()[0])
            if code.startswith(('SET_GCODE_OFFSET', 'RESTORE_GCODE_STATE')):
                errors.append(f'line {number}: unsupported coordinate-state macro')
            continue
        command = match[1].upper()
        if command.startswith('T'):
            if not command[1:].isdigit():
                errors.append(f'line {number}: invalid tool index')
                continue
            tool = int(command[1:])
            if not absolute_e:
                continue
            position[3] = np.nan
            continue
        relevant = command in {'G0', 'G1', 'G2', 'G3', 'G90', 'G91', 'G92', 'M82', 'M83', 'G17', 'G18', 'G19', 'G20', 'G21', 'G90.1', 'G91.1', 'G28', 'G4'}
        if command == 'G28':
            position[:3] = np.nan
            continue
        if command == 'G4':
            continue
        if not relevant:
            if command.startswith('G') or command in {'M206', 'M428'}:
                errors.append(f'line {number}: unsupported geometry/state command {command}')
            continue
        try:
            tail = code[match.end():]
            params = {key.upper(): float(value) for key, value in PARAM.findall(tail)}
            if PARAM.sub('', tail).strip() or not all(math.isfinite(v) for v in params.values()):
                raise ValueError('malformed or non-finite numeric parameter')
            allowed = 'XYZEF' if command in {'G0', 'G1'} else 'XYZEFIJKRP'
            if command in {'G0', 'G1', 'G2', 'G3'} and set(params) - set(allowed):
                raise ValueError('unsupported motion axis/parameter')
            if command in {'G2', 'G3'} and params.get('P', 1) != 1:
                raise ValueError('only single-turn arcs (P1) are supported')
            if command in {'G90', 'G91'}:
                absolute_xyz = command == 'G90'
            elif command in {'M82', 'M83'}:
                absolute_e = command == 'M82'
            elif command in {'G17', 'G18', 'G19'}:
                plane = command
            elif command in {'G20', 'G90.1', 'G91.1'}:
                raise ValueError(f'unsupported units/arc mode {command}')
            elif command == 'G28':
                position[:3] = np.nan
            elif command == 'G92':
                for i, axis in enumerate('XYZE'):
                    if axis in params or not params:
                        value = params.get(axis, 0)
                        if i < 3 and not math.isfinite(position[i]):
                            raise ValueError('XYZ reset before a known coordinate')
                        if i == 3:
                            position[i], offset[i] = value, 0
                        else:
                            offset[i] = position[i] - value
            elif command in {'G0', 'G1', 'G2', 'G3'}:
                start = position.copy()
                for i, axis in enumerate('XYZE'):
                    if axis in params:
                        relative = not absolute_xyz or (i == 3 and not absolute_e)
                        position[i] = position[i] + params[axis] if relative else params[axis] + offset[i]
                delta_e = params.get('E', 0) if not absolute_xyz or not absolute_e else position[3] - start[3]
                if 'E' in params and not math.isfinite(delta_e):
                    raise ValueError('absolute extrusion needs G92 E after tool selection')
                if delta_e <= 0 or 'E' not in params:
                    continue
                if role.lower() == 'custom':
                    custom_moves += 1
                    continue
                if not np.isfinite(start[:3]).all() or not np.isfinite(position[:3]).all():
                    raise ValueError('extrusion starts before XYZ coordinates are established')
                if command in {'G2', 'G3'}:
                    if plane != 'G17' or not absolute_xyz:
                        raise ValueError('only absolute XYZ / XY-plane arcs are supported')
                    points = _arc(start[:3], position[:3], params, command == 'G2', critical_angles)
                    arc_moves += 1
                else:
                    points = np.array([start[:3], position[:3]])
                for a, b in zip(points, points[1:]):
                    if np.linalg.norm(b - a) > 1e-12:
                        segments.append([a.tolist(), b.tolist()]);features.append(role);lines.append(number);tools.append(tool)
        except ValueError as exc:
            errors.append(f'line {number}: {exc}')
    return {'segments': np.array(segments, dtype=float).reshape((-1, 2, 3)), 'features': features, 'lines': lines, 'tools': tools, 'errors': errors, 'arc_moves': arc_moves, 'skipped_custom_extrusions': custom_moves, 'unmodeled_macros': sorted(macros)}


def validate_paths(paths, machine):
    bed, height, holes, convex, _ = machine_region(machine)
    segments = paths['segments']
    errors = paths['errors'].copy()
    if not len(segments):
        errors.append('no scoped extrusion segments found')
    if paths['arc_moves'] and (holes or not convex):
        # shortcut: arc checks require a convex bed without holes; add exact arc/polygon intersection before accepting other profiles.
        errors.append('arc validation requires a convex printable polygon without excluded areas')
    invalid = set()
    if len(segments):
        points = segments.reshape((-1, 3))
        good = _inside(points[:, :2], bed) & (points[:, 2] >= -EPS) & (points[:, 2] <= height + EPS)
        invalid.update((np.flatnonzero(~good) // 2).tolist())
        # Split straight paths at boundary crossings to catch concave notches and holes.
        for polygon in ([bed] if not convex else []) + holes:
            candidates = {}
            for a, b in zip(polygon, np.roll(polygon, -1, axis=0)):
                indices, cuts = _cuts(segments[:, 0, :2], segments[:, 1, :2], a, b)
                for index, cut in zip(indices.tolist(), cuts.tolist()):
                    candidates.setdefault(index, [0., 1.]).append(cut)
            if polygon is not bed:
                inside = _inside(points[:, :2], polygon).reshape((-1, 2)).any(axis=1)
                invalid.update(np.flatnonzero(inside).tolist())
            for index, cuts in candidates.items():
                ordered = sorted(set(cuts))
                mid = np.array([(a + b) / 2 for a, b in zip(ordered, ordered[1:])])
                sample = segments[index, 0, :2] + mid[:, None] * (segments[index, 1, :2] - segments[index, 0, :2])
                inside = _inside(sample, polygon)
                if (polygon is bed and not inside.all()) or (polygon is not bed and inside.any()):
                    invalid.add(index)
    violations = sorted({paths['lines'][i] for i in invalid})
    return {'passed': not errors and not invalid, 'scope': SCOPE, 'segments_checked': len(segments), 'arc_moves': paths['arc_moves'], 'bounds_mm': [segments.min(axis=(0, 1)).tolist(), segments.max(axis=(0, 1)).tolist()] if len(segments) else None, 'printable_polygon_mm': bed.tolist(), 'printable_height_mm': height, 'excluded_polygons_mm': [p.tolist() for p in holes], 'violation_count': len(violations), 'violation_lines': violations[:30], 'errors': errors[:30], 'error_count': len(errors), 'skipped_custom_extrusions': paths['skipped_custom_extrusions'], 'unmodeled_macros': paths['unmodeled_macros'], 'features': {name: paths['features'].count(name) for name in sorted(set(paths['features']))}, 'tools': sorted(set(paths['tools'])), 'ready_to_print': False}


def render_paths(paths, report, output):
    previous = os.environ.get('MPLCONFIGDIR')
    with tempfile.TemporaryDirectory(prefix='u1-gcode-mpl-') as cache:
        os.environ['MPLCONFIGDIR'] = cache
        try:
            import matplotlib
            matplotlib.use('Agg', force=True)
            from matplotlib import pyplot as plt
            from matplotlib.collections import LineCollection
            from matplotlib.lines import Line2D
            try:
                from .u1_preview import camera_basis
            except ImportError:
                from u1_preview import camera_basis
            output = Path(output)
            output.mkdir(parents=True, exist_ok=True)
            total = len(paths['segments'])
            if not total:
                raise ValueError('no extrusion paths to preview')
            # Sample per feature so small support/interface/brim sets remain visible.
            indices = []
            names = sorted(set(paths['features']))
            minimum = min(1000, 100000 // len(names))
            remaining = 100000 - minimum * len(names)
            feature_array = np.asarray(paths['features'])
            for name in names:
                found = np.flatnonzero(feature_array == name)
                quota = max(1, minimum + int(remaining * len(found) / total))
                indices.extend(found[np.linspace(0, len(found) - 1, min(quota, len(found)), dtype=int)].tolist())
            indices = np.asarray(sorted(indices))
            segments = paths['segments'][indices]
            palette = {'support': '#e87924', 'brim': '#8756b2', 'outer': '#226f7b', 'top': '#347ddd', 'other': '#a8afb6'}
            def category(name):
                value = name.lower()
                return 'support' if 'support' in value else 'brim' if value in {'brim', 'skirt'} else 'outer' if value in {'outer wall', 'overhang wall'} else 'top' if value == 'top surface' else 'other'
            colors = np.array([palette[category(paths['features'][i])] for i in indices])
            files = {}
            label = 'PASS: centerline bounds' if report['passed'] else 'REVIEW FAILED / INCOMPLETE'
            with plt.rc_context({'figure.facecolor': '#f7f7f5'}):
                for name in ['top', '3d']:
                    if name == 'top':
                        projected = segments[:, :, :2]
                        bed = np.asarray(report['printable_polygon_mm'])
                    else:
                        right, up, eye = camera_basis([1., -1., 1.3])
                        projected = np.stack([segments @ right, segments @ up], axis=-1)
                        order = np.argsort((segments @ eye).mean(axis=1), kind='stable')
                        projected, draw_colors = projected[order], colors[order]
                        bed3 = np.column_stack([report['printable_polygon_mm'], np.zeros(len(report['printable_polygon_mm']))])
                        bed = np.column_stack([bed3 @ right, bed3 @ up])
                    if name == 'top':draw_colors = colors
                    fig, ax = plt.subplots(figsize=(9, 8))
                    ax.add_collection(LineCollection(projected, colors=draw_colors, linewidths=.45, alpha=.85))
                    ax.plot(*np.vstack([bed, bed[0]]).T, color='#243b31', linewidth=1.2)
                    for polygon in report['excluded_polygons_mm']:
                        points = np.asarray(polygon)
                        if name == '3d':
                            points = np.column_stack([points, np.zeros(len(points))]);points = np.column_stack([points @ right, points @ up])
                        ax.fill(*points.T, color='#d44b4b', alpha=.3)
                    ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Actual G-code extrusion paths — {name.upper()}\n{label}')
                    if name == '3d':
                        # Keep the top view as plate context and the isometric view readable for small parts.
                        low, high = projected.min(axis=(0, 1)), projected.max(axis=(0, 1))
                        padding = max(float(np.max(high - low)) * .12, 1.)
                        ax.set_xlim(low[0] - padding, high[0] + padding)
                        ax.set_ylim(low[1] - padding, high[1] + padding)
                    ax.legend(handles=[Line2D([0], [0], color=c, label=n) for n, c in palette.items()],loc='upper right')
                    fig.text(.5,.02,f'{len(indices):,} of {total:,} segments shown; ALL checked. Custom blocks/macros excluded. No bead-width or collision certification.',ha='center',fontsize=8)
                    path = output / f'toolpaths-{name}.png';fig.savefig(path,dpi=130);plt.close(fig);files[name] = str(path.resolve())
            return {'files': files, 'segments_displayed': len(indices), 'segments_total': total, 'sampled': len(indices) < total}
        finally:
            if previous is None:
                os.environ.pop('MPLCONFIGDIR', None)
            else:
                os.environ['MPLCONFIGDIR'] = previous


def review_gcode(text, machine, output):
    output = Path(output);output.mkdir(parents=True, exist_ok=True)
    region = machine_region(machine)
    paths = parse_gcode(text, region[4]);report = validate_paths(paths, machine)
    try:
        report['previews'] = render_paths(paths, report, output)
    except (ValueError, OSError, ImportError) as exc:
        report['preview_error'] = str(exc)
    report['review_completed'] = report['passed'] and 'previews' in report
    (output/'toolpath-review.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--machine-json',type=Path,required=True,help='Resolved machine settings with printable_area and printable_height')
    parser.add_argument('--output-dir',type=Path,required=True)
    args = parser.parse_args()
    try:
        if args.output_dir.exists():raise ValueError('output directory must be fresh')
        machine = json.loads(args.machine_json.read_text());machine_region(machine)
        report = review_gcode(args.input.read_text(),machine,args.output_dir)
        print(json.dumps(report,indent=2,allow_nan=False));return 0 if report['review_completed'] else 1
    except (ValueError,OSError) as exc:
        print(json.dumps({'error':str(exc),'ready_to_print':False}));return 2


if __name__ == '__main__':
    raise SystemExit(main())
