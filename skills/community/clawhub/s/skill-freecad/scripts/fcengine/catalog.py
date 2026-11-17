"""Operation catalog: the single source of truth for every operation.

Used for request validation, the ``describe`` command and generated docs.
Pure Python: must not import FreeCAD.

Conventions: lengths in millimetres, angles in degrees, right-handed XYZ.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# Parameter types understood by ``validate``:
#   number   int/float (bool rejected); with expr=True also "=<FreeCAD expression>"
#   integer  int
#   string   str
#   bool     true/false
#   name     reference to an existing object (Name or Label)
#   names    non-empty list of object references
#   newname  identifier for a new object: [A-Za-z_][A-Za-z0-9_]*
#   label    free-form display text (no control characters, max 100 chars)
#   vector   [x, y, z]
#   points   list of >=3 points, each [a, b] or [x, y, z]
#   enum     one of ``choices``
#   selector edge/face selector: "all", a 1-based index, a list of indices,
#            or a selector expression such as ">Z", "|Z and %LINE", "face(>Z)"
#   rotation {"axis": [x, y, z], "angle": degrees}
#   number_or_vector  number or [x, y, z]
#   shapes   list of closed profile shapes (see profiles.py)
#   centers  list of >=1 distinct [a, b] points
#   views    list of render view names
#   expect   expectations object (see EXPECT_KEYS)
#   loads    list of FEM loads (see fem_static)
#   parts    assembly parts: [{"object": name, "name"?, "position"?, "rotation"?, "ground"?}]
#   jointref {"part": name, "face" | "edge": selector}
#   object   JSON object (free-form, checked by the op)
#   path     relative file path inside the workspace


@dataclass(frozen=True)
class Param:
    name: str
    type: str
    doc: str
    required: bool = False
    default: Any = None
    choices: Tuple[str, ...] = ()
    gt: Optional[float] = None  # exclusive minimum
    ge: Optional[float] = None  # inclusive minimum
    le: Optional[float] = None  # inclusive maximum
    expr: bool = False  # accepts "=expression"
    min_items: Optional[int] = None  # for list types

    def describe(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"type": self.type, "doc": self.doc}
        if self.required:
            d["required"] = True
        if self.default is not None:
            d["default"] = self.default
        if self.choices:
            d["choices"] = list(self.choices)
        for key, value in (("gt", self.gt), ("ge", self.ge), ("le", self.le), ("min_items", self.min_items)):
            if value is not None:
                d[key] = value
        if self.expr:
            d["accepts_expression"] = True
        return d


@dataclass(frozen=True)
class Op:
    name: str
    category: str
    summary: str
    params: Tuple[Param, ...]
    mutates: bool = True
    notes: str = ""
    example: Dict[str, Any] = field(default_factory=dict)
    # Groups where exactly one / at least one parameter must be given.
    one_of: Tuple[Tuple[str, ...], ...] = ()

    def param(self, name: str) -> Optional[Param]:
        for p in self.params:
            if p.name == name:
                return p
        return None

    def describe(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "op": self.name,
            "category": self.category,
            "summary": self.summary,
            "params": {p.name: p.describe() for p in self.params},
        }
        if self.one_of:
            d["exactly_one_of"] = [list(g) for g in self.one_of]
        if self.notes:
            d["notes"] = self.notes
        if self.example:
            d["example"] = self.example
        return d


# ---------------------------------------------------------------- shared params


def _name(default_hint: str) -> Param:
    return Param(
        "name",
        "newname",
        f"Name of the new object (identifier). Default: auto ('{default_hint}', '{default_hint}001', ...).",
    )


POSITION = Param("position", "vector", "Placement position [x, y, z] in mm.", default=[0, 0, 0])
ROTATION = Param(
    "rotation", "rotation", 'Orientation as {"axis": [x,y,z], "angle": deg}, applied about the position point.'
)
DIRECTION = Param(
    "direction",
    "vector",
    "Axis direction of the solid (alternative to 'rotation'). Default +Z.",
)
TARGET = Param("target", "name", "Object to operate on.", required=True)
PD_PATTERN_NOTE = (
    "If 'target' is a feature of a PartDesign body (a pad, pocket, hole, ...), the feature is repeated natively "
    "inside the body, in body coordinates; 'fuse' does not apply. A pattern or mirror can't be repeated again: "
    "name the original feature."
)
SHAPES = Param(
    "shapes",
    "shapes",
    'Profile as closed shapes (builds an editable Sketch): {"rect": [x0, y0, x1, y1], "corner_radius": r}, '
    '{"circle": [cx, cy], "radius": r}, {"slot": [[x1, y1], [x2, y2]], "radius": r}, '
    '{"polygon": [[x, y], ...], "corner_radius": r} (or "radii": [...] per corner), '
    '{"spline": [[x, y], ...]} (smooth closed curve through >=3 points), '
    '{"path": [[x, y], [x, y], {"arc_to": [x, y], "center": [cx, cy], "clockwise": false}, '
    '{"spline_to": [x, y], "through": [[x, y], ...], "start_tangent": [dx, dy], "end_tangent": [dx, dy]}, ...]}. '
    "Shapes inside another shape become holes. Splines pass exactly through their points and can bulge between "
    "them; use a path with straight segments and spline_to for flat sides.",
)
OFFSET = Param(
    "offset",
    "number",
    "With 'shapes': distance of the profile plane from the origin along its normal. "
    "In a body this can be an expression that follows the part, e.g. '=Base.Length'.",
    default=0,
    expr=True,
)
BODY = Param(
    "body", "name", "PartDesign body to add this feature to (see op 'body'). Omit for a stand-alone Part solid."
)
MODE = Param(
    "mode",
    "enum",
    "In a body: 'add' material (Pad/Revolution) or 'remove' it (Pocket/Groove).",
    default="add",
    choices=("add", "remove"),
)
REVERSED = Param(
    "reversed",
    "bool",
    "In a body: flip the direction (add goes along the plane normal, remove goes against it).",
    default=False,
)
PROFILE_NOTES = (
    "Give 'height' (or 'direction' outside a body; or 'through_all' when removing in a body). "
    "Plane normals (extrusion direction): XY -> +Z, XZ -> +Y, YZ -> +X. Use 'points' for a quick straight-edged polygon "
    "(closed automatically; do not repeat the first point) or 'shapes' for arcs, rounded corners, circles, slots and holes. "
    "Shapes must be disjoint or fully nested; a path closes back to its start."
)

# ---------------------------------------------------------------- operations

OPS: List[Op] = [
    # ------------------------------------------------------------ solids
    Op(
        "box",
        "solid",
        "Parametric box (Part::Box). 'position' is the minimum corner; the box extends along +X/+Y/+Z.",
        (
            Param("length", "number", "Size along X.", required=True, gt=0, expr=True),
            Param("width", "number", "Size along Y.", required=True, gt=0, expr=True),
            Param("height", "number", "Size along Z.", required=True, gt=0, expr=True),
            _name("Box"),
            POSITION,
            ROTATION,
        ),
        example={"op": "box", "name": "Plate", "length": 100, "width": 60, "height": 8},
    ),
    Op(
        "cylinder",
        "solid",
        "Parametric cylinder (Part::Cylinder). 'position' is the centre of the bottom face; the axis points along 'direction' (default +Z).",
        (
            Param("radius", "number", "Radius.", required=True, gt=0, expr=True),
            Param("height", "number", "Height along the axis.", required=True, gt=0, expr=True),
            _name("Cylinder"),
            POSITION,
            DIRECTION,
            ROTATION,
        ),
        example={"op": "cylinder", "name": "Hole", "radius": 3, "height": 20, "position": [10, 10, -5]},
    ),
    Op(
        "sphere",
        "solid",
        "Parametric sphere (Part::Sphere) centred on 'position'.",
        (
            Param("radius", "number", "Radius.", required=True, gt=0, expr=True),
            _name("Sphere"),
            POSITION,
        ),
    ),
    Op(
        "cone",
        "solid",
        "Parametric cone or frustum (Part::Cone). 'position' is the centre of the bottom face (radius1).",
        (
            Param("radius1", "number", "Bottom radius.", required=True, ge=0, expr=True),
            Param("radius2", "number", "Top radius (0 for a pointed cone).", required=True, ge=0, expr=True),
            Param("height", "number", "Height along the axis.", required=True, gt=0, expr=True),
            _name("Cone"),
            POSITION,
            DIRECTION,
            ROTATION,
        ),
    ),
    Op(
        "torus",
        "solid",
        "Parametric torus (Part::Torus) centred on 'position', ring in the plane normal to 'direction'.",
        (
            Param("radius1", "number", "Major radius: axis to tube centre.", required=True, gt=0, expr=True),
            Param("radius2", "number", "Minor radius: tube radius. Must be < radius1.", required=True, gt=0, expr=True),
            _name("Torus"),
            POSITION,
            DIRECTION,
            ROTATION,
        ),
    ),
    Op(
        "prism",
        "solid",
        "Parametric regular polygonal prism (Part::Prism). 'position' is the centre of the bottom face.",
        (
            Param("sides", "integer", "Number of polygon sides.", required=True, ge=3),
            Param(
                "circumradius", "number", "Distance from centre to a polygon corner.", required=True, gt=0, expr=True
            ),
            Param("height", "number", "Height along the axis.", required=True, gt=0, expr=True),
            _name("Prism"),
            POSITION,
            DIRECTION,
            ROTATION,
        ),
    ),
    # ------------------------------------------------------------ profiles
    Op(
        "extrude",
        "profile",
        "Extrude a closed polygon (Part::Polygon + Part::Extrusion). Points are editable afterwards.",
        (
            Param(
                "points",
                "points",
                "Quick polygon: corners in order, >=3. [a, b] are 2D coordinates in 'plane'; [x, y, z] are absolute.",
            ),
            SHAPES,
            Param(
                "plane",
                "enum",
                "Plane of 2D coordinates: XY -> (x, y, 0), XZ -> (x, 0, z), YZ -> (0, y, z).",
                default="XY",
                choices=("XY", "XZ", "YZ"),
            ),
            OFFSET,
            Param("height", "number", "Extrusion distance along the plane normal (see notes).", gt=0, expr=True),
            Param("direction", "vector", "Explicit extrusion vector; its length is the distance."),
            Param("symmetric", "bool", "Extrude half the distance to each side of the plane.", default=False),
            BODY,
            MODE,
            Param(
                "through_all",
                "bool",
                "In a body with mode 'remove': cut through the whole part instead of 'height'.",
                default=False,
            ),
            REVERSED,
            _name("Extrude"),
        ),
        one_of=(("points", "shapes"),),
        notes=PROFILE_NOTES,
        example={
            "op": "extrude",
            "name": "Plate",
            "height": 6,
            "shapes": [
                {"rect": [0, 0, 80, 50], "corner_radius": 5},
                {"circle": [10, 10], "radius": 3.25},
                {"slot": [[30, 25], [50, 25]], "radius": 4},
            ],
        },
    ),
    Op(
        "revolve",
        "profile",
        "Revolve a closed polygon around an axis (Part::Polygon + Part::Revolution).",
        (
            Param("points", "points", "Quick polygon profile (see 'extrude'). The profile must not cross the axis."),
            SHAPES,
            Param("plane", "enum", "Plane of 2D coordinates.", default="XY", choices=("XY", "XZ", "YZ")),
            OFFSET,
            Param("axis", "vector", "Revolution axis direction.", default=[0, 1, 0]),
            Param("center", "vector", "A point on the revolution axis.", default=[0, 0, 0]),
            Param("angle", "number", "Sweep angle in degrees.", default=360, gt=0, le=360, expr=True),
            BODY,
            MODE,
            _name("Revolve"),
        ),
        one_of=(("points", "shapes"),),
        notes=PROFILE_NOTES,
        example={
            "op": "revolve",
            "name": "Bushing",
            "points": [[10, 0], [20, 0], [20, 5], [14, 5], [14, 30], [10, 30]],
            "axis": [0, 1, 0],
        },
    ),
    Op(
        "loft",
        "profile",
        "Smooth solid through cross-sections (Part::Loft; in a body AdditiveLoft/SubtractiveLoft). For organic "
        "shapes: mouse shells, handles, bottles, transitions between a square and a round end.",
        (
            Param(
                "sections",
                "sections",
                'Cross-sections in order, >=2: {"shape": one closed shape (see extrude '
                '\'shapes\', no holes), "plane": "XY"|"XZ"|"YZ", "offset": distance along the plane normal (number or '
                "'=expression')}.",
                required=True,
            ),
            Param("ruled", "bool", "Straight faces between sections instead of a smooth surface.", default=False),
            Param("closed", "bool", "Loop back from the last section to the first (a ring).", default=False),
            BODY,
            Param(
                "mode", "enum", "In a body: 'add' material or 'remove' it.", default="add", choices=("add", "remove")
            ),
            _name("Loft"),
        ),
        notes="Each section is drawn in its plane like an extrude profile (XY: (x, y) at z = offset; XZ: (x, z) at "
        "y = offset; YZ: (y, z) at x = offset). Sections usually share a plane type with increasing offsets. "
        "Smooth lofts can bulge between sections; add sections where the shape must be controlled. "
        'Edit with set: {"sections": [...]} (same number of sections).',
        example={
            "op": "loft",
            "name": "Shell",
            "sections": [
                {"shape": {"rect": [-20, -15, 20, 15], "corner_radius": 4}, "plane": "XY", "offset": 0},
                {"shape": {"circle": [0, 0], "radius": 12}, "plane": "XY", "offset": 30},
                {"shape": {"circle": [0, 0], "radius": 6}, "plane": "XY", "offset": 50},
            ],
        },
    ),
    Op(
        "sweep",
        "profile",
        "Sweep a profile along a path (Part::Sweep; in a body AdditivePipe/SubtractivePipe): tubes, handles, rails, "
        "springs and threads.",
        (
            Param(
                "shapes",
                "shapes",
                "Profile: one closed outline, optionally with holes (a tube), drawn in 2D around "
                "the start of the path (see notes). Same shape syntax as extrude.",
                required=True,
            ),
            Param("path", "path3d", "Path through [x, y, z] points (>=2), absolute (in a body: body coordinates)."),
            Param(
                "smooth",
                "bool",
                "With 'path': a smooth curve through the points instead of straight segments.",
                default=False,
            ),
            Param(
                "corner_radius", "number", "With 'path': round the corners between straight segments (bent tube).", ge=0
            ),
            Param(
                "helix",
                "helix",
                'Helical path: {"radius": r, "pitch": p, "height": h, "left_handed": false, '
                '"center": [x, y, z], "axis": [0, 0, 1]}. Starts at center + radius along the local X.',
            ),
            Param(
                "up",
                "vector",
                "Direction of the profile's y axis at the start (default +Z, or +X when the path starts "
                "vertically; the helix axis for a helix).",
            ),
            BODY,
            Param(
                "mode", "enum", "In a body: 'add' material or 'remove' it.", default="add", choices=("add", "remove")
            ),
            _name("Sweep"),
        ),
        one_of=(("path", "helix"),),
        notes="The profile is placed at the start of the path, perpendicular to it: profile (0, 0) sits on the path, "
        "its y axis points along 'up' and x points to the right when looking along the path (on a helix: radially outward). The response "
        "reports this 'profile_frame'. A spring is a circle swept along a helix; a thread is a triangle swept "
        "along a helix with mode remove or add. Edit with set: path, smooth, corner_radius, helix, up, shapes.",
        example={
            "op": "sweep",
            "name": "Handle",
            "shapes": [{"circle": [0, 0], "radius": 6}, {"circle": [0, 0], "radius": 4}],
            "path": [[0, 0, 0], [0, 0, 40], [60, 0, 40], [60, 0, 0]],
            "corner_radius": 12,
        },
    ),
    # ------------------------------------------------------------ PartDesign
    Op(
        "text",
        "profile",
        "Text as a solid: letters from a font (Draft ShapeString), extruded along the plane normal. Fuse it onto a "
        "part for raised lettering, or cut it from the part to engrave it.",
        (
            Param("text", "label", "The text (one line, up to 100 characters).", required=True),
            Param("size", "number", "Height of capital letters, in mm.", required=True, gt=0),
            Param(
                "height",
                "number",
                "Extrusion distance along the plane normal (letter depth).",
                required=True,
                gt=0,
                expr=True,
            ),
            Param(
                "position",
                "vector",
                "Where the 'align' point of the text goes (absolute [x, y, z]).",
                default=[0, 0, 0],
            ),
            Param(
                "plane",
                "enum",
                "Plane the text lies in: XY reads from above (+Z), XZ from the front (-Y), YZ from the right (+X).",
                default="XY",
                choices=("XY", "XZ", "YZ"),
            ),
            Param(
                "align",
                "enum",
                "Which point of the text lands on 'position' (bottom = baseline, top = cap height).",
                default="bottom_left",
                choices=(
                    "bottom_left",
                    "bottom_center",
                    "bottom_right",
                    "middle_left",
                    "center",
                    "middle_right",
                    "top_left",
                    "top_center",
                    "top_right",
                ),
            ),
            Param("angle", "number", "Rotation in the plane, counter-clockwise as read, in degrees.", default=0),
            Param("reversed", "bool", "Extrude against the plane normal instead of along it.", default=False),
            Param(
                "font",
                "path",
                "A .ttf/.otf font file in the workspace. Default: FreeCAD's bundled osifont (a plain technical font).",
            ),
            _name("Text"),
        ),
        notes="Extrusion goes along the plane normal: XY -> +Z, XZ -> +Y, YZ -> +X ('reversed' flips it). To engrave "
        "a top face at z = 10 by 1 mm: text at z = 9 with height 2, then cut it (the extra 1 mm passes through the "
        "face). For raised text, start it inside the face (z = 9.9) and fuse. Each letter is a separate solid until "
        "fused or cut. Edit with set: text, size, font, align, height.",
        example={
            "op": "text",
            "name": "Label",
            "text": "V2.1",
            "size": 8,
            "height": 2,
            "position": [40, 25, 5],
            "align": "center",
        },
    ),
    Op(
        "body",
        "partdesign",
        "Create a PartDesign body: a single solid built feature by feature (pad, pocket, hole, fillet, ...), the way "
        "FreeCAD users model parts. Add features with extrude/revolve/hole using 'body', and dress-ups with fillet/chamfer/shell on the body.",
        (_name("Body"), POSITION, ROTATION),
        notes="Sketches are attached to the body's origin planes, so profile coordinates are always body coordinates. "
        "Use 'offset' expressions (e.g. '=Base.Length') to keep features on faces when dimensions change.",
        example={"op": "body", "name": "Bracket"},
    ),
    Op(
        "hole",
        "partdesign",
        "Drill one or more holes into a body (PartDesign::Hole): simple, counterbored or countersunk, sized from metric "
        "screw tables or an explicit diameter. Holes start at the profile plane and go against its normal.",
        (
            Param("body", "name", "Body to drill.", required=True),
            Param(
                "at", "centers", "Hole centres as [a, b] in 'plane' (one hole per point); >= 1 point.", required=True
            ),
            Param("plane", "enum", "Plane of the 'at' coordinates.", default="XY", choices=("XY", "XZ", "YZ")),
            Param(
                "offset",
                "number",
                "Distance of the starting plane along its normal, usually the face the hole starts on, e.g. '=Base.Length'.",
                default=0,
                expr=True,
            ),
            Param(
                "size",
                "enum",
                "Metric screw size; sets the diameter from 'fit' and the seat from 'type'.",
                choices=("M2", "M2.5", "M3", "M4", "M5", "M6", "M8", "M10", "M12", "M14", "M16", "M20"),
            ),
            Param(
                "fit",
                "enum",
                "With 'size': 'clearance' (ISO 273 medium) for a screw to pass, 'tap' for a tap drill (an unthreaded "
                "bore at the tap drill size). Ignored when 'threaded'.",
                default="clearance",
                choices=("clearance", "tap"),
            ),
            Param("diameter", "number", "Explicit hole diameter (instead of 'size').", gt=0, expr=True),
            Param(
                "threaded",
                "bool",
                "With 'size' and type 'simple': model the ISO metric coarse thread (class 6H) in the hole, over its "
                "whole depth, e.g. for a threaded hole in a printed part or a model that shows the thread.",
                default=False,
            ),
            Param("type", "enum", "Hole seat.", default="simple", choices=("simple", "counterbore", "countersink")),
            Param("cut_diameter", "number", "Counterbore/countersink diameter (default from 'size').", gt=0),
            Param("cut_depth", "number", "Counterbore depth (default from 'size').", gt=0),
            Param("depth", "number", "Hole depth; omit to drill through all.", gt=0, expr=True),
            Param("reversed", "bool", "Drill along the plane normal instead of against it.", default=False),
            _name("Hole"),
        ),
        one_of=(("size", "diameter"),),
        notes="Counterbores fit ISO 4762 socket head screws (DIN 974-1); countersinks fit ISO 10642 (90 degrees). "
        "A 'threaded' hole is bored at the thread's minor diameter and the thread is real geometry (slower to "
        "compute and export than a plain hole; give 'depth' for blind tapped holes).",
        example={
            "op": "hole",
            "body": "Bracket",
            "at": [[10, 10], [70, 10]],
            "offset": "=Base.Length",
            "size": "M5",
            "type": "counterbore",
        },
    ),
    # ------------------------------------------------------------ assemblies
    Op(
        "assembly",
        "assembly",
        "Create an assembly (native Assembly workbench) whose parts are links to existing solids or bodies. "
        "The first part is grounded (fixed in place) unless others are marked 'ground'. Then connect parts with 'joint'.",
        (
            Param(
                "parts",
                "parts",
                'Parts: [{"object": "Base"}, {"object": "Pin", "name": "Pin1", "position": [x, y, z], "ground": false}, ...]. '
                "The same object can be added several times under different names.",
                required=True,
            ),
            _name("Assembly"),
        ),
        notes="Each part is a link: editing the original object updates every instance. The originals become intermediates; "
        "the assembly is the result (export/render/measure it). Overlapping parts are reported as 'interferences'.",
        example={"op": "assembly", "name": "Hinge", "parts": [{"object": "Base"}, {"object": "Pin"}]},
    ),
    Op(
        "joint",
        "assembly",
        "Connect two parts of an assembly with a joint and solve. Each side names a part and exactly one face or edge "
        "(selector). Every joint is checked to be satisfied after solving, and part overlaps are reported.",
        (
            Param("assembly", "name", "Assembly to add the joint to.", required=True),
            Param(
                "type",
                "enum",
                "fixed: rigid; revolute: hinge (shared axis and point); cylindrical: rotate + slide on an axis; "
                "slider: slide on an axis without rotation; ball: shared point; parallel / perpendicular: axes only.",
                required=True,
                choices=("fixed", "revolute", "cylindrical", "slider", "ball", "parallel", "perpendicular"),
            ),
            Param(
                "a",
                "jointref",
                'First side: {"part": "Base", "face": ">Z"} or {"part": "Base", "edge": "%CIRCLE and >Z"}.',
                required=True,
            ),
            Param("b", "jointref", "Second side (this part moves to meet the first).", required=True),
            Param(
                "offset",
                "number",
                "Distance of part b from side a along the joint axis: positive moves it away from a's surface "
                "(out of the material), negative into it (e.g. -10 sinks a pin 10 mm into a hole).",
                default=0,
            ),
            _name("Joint"),
        ),
        notes="A face gives a frame at its centre with Z along its normal; a circular edge gives its centre and axis. "
        "Faces touching face-to-face (e.g. a block on a plate) usually need type 'fixed'.",
        example={
            "op": "joint",
            "assembly": "Hinge",
            "type": "revolute",
            "a": {"part": "Base", "edge": "%CIRCLE and >Z"},
            "b": {"part": "Pin", "edge": "%CIRCLE and <Z"},
        },
    ),
    # ------------------------------------------------------------ booleans
    Op(
        "cut",
        "boolean",
        "Subtract tool(s) from a base (Part::Cut). Inputs stay editable; the result is checked to have actually removed material.",
        (
            Param("base", "name", "Object to cut from.", required=True),
            Param("tool", "name", "Single cutting object."),
            Param("tools", "names", "Several cutting objects (fused automatically)."),
            Param("refine", "bool", "Merge coplanar faces in the result (recommended before fillets).", default=True),
            _name("Cut"),
        ),
        one_of=(("tool", "tools"),),
        notes="Tip: make cutting tools extend past the faces they cut (e.g. a hole cylinder 1 mm above and below a plate) to avoid coincident-face failures.",
        example={"op": "cut", "name": "DrilledPlate", "base": "Plate", "tool": "Hole"},
    ),
    Op(
        "fuse",
        "boolean",
        "Union of two or more objects (Part::MultiFuse). Warns if the result is not one connected solid.",
        (
            Param("objects", "names", "Objects to unite (>=2).", required=True, min_items=2),
            Param("refine", "bool", "Merge coplanar faces in the result.", default=True),
            _name("Fusion"),
        ),
    ),
    Op(
        "common",
        "boolean",
        "Intersection of two or more objects (Part::MultiCommon). Fails if the objects do not overlap.",
        (
            Param("objects", "names", "Objects to intersect (>=2).", required=True, min_items=2),
            Param("refine", "bool", "Merge coplanar faces in the result.", default=True),
            _name("Common"),
        ),
    ),
    # ------------------------------------------------------------ dress-up features
    Op(
        "fillet",
        "feature",
        "Round edges (Part::Fillet). Selector-based edge choices are re-evaluated when upstream dimensions change.",
        (
            TARGET,
            Param("radius", "number", "Fillet radius.", required=True, gt=0),
            Param(
                "edges",
                "selector",
                "Edges to round: 'all', 1-based indices, or a selector like '|Z', '>Z', 'face(>Z)'. Use inspect with topology=true to see edges.",
                default="all",
            ),
            _name("Fillet"),
        ),
        example={"op": "fillet", "target": "Plate", "radius": 2, "edges": "|Z"},
    ),
    Op(
        "chamfer",
        "feature",
        "Bevel edges with equal setback (Part::Chamfer).",
        (
            TARGET,
            Param("size", "number", "Chamfer setback distance.", required=True, gt=0),
            Param("edges", "selector", "Edges to chamfer (see 'fillet').", default="all"),
            _name("Chamfer"),
        ),
    ),
    Op(
        "shell",
        "feature",
        "Hollow a solid leaving walls of 'thickness' (Part::Thickness), removing 'open_faces'.",
        (
            TARGET,
            Param("thickness", "number", "Wall thickness.", required=True, gt=0),
            Param(
                "open_faces",
                "selector",
                "Faces to remove, e.g. '>Z' for an open-top box. Required: at least one face.",
                required=True,
            ),
            Param("outward", "bool", "Grow walls outward instead of inward (keeps inner dimensions).", default=False),
            Param("join", "enum", "Corner join type.", default="arc", choices=("arc", "intersection")),
            _name("Shell"),
        ),
        example={"op": "shell", "target": "Housing", "thickness": 2, "open_faces": ">Z"},
    ),
    # ------------------------------------------------------------ patterns
    Op(
        "linear_array",
        "pattern",
        "Repeat an object 'count' times, each copy offset by 'step' (parametric Draft array).",
        (
            TARGET,
            Param(
                "count", "integer", "Total number of instances, including the original.", required=True, ge=2, le=1000
            ),
            Param("step", "vector", "Offset between consecutive instances.", required=True),
            Param("fuse", "bool", "Fuse touching instances into one solid.", default=True),
            _name("LinearArray"),
        ),
        notes=PD_PATTERN_NOTE,
        example={"op": "linear_array", "target": "Hole", "count": 4, "step": [20, 0, 0]},
    ),
    Op(
        "grid_array",
        "pattern",
        "Rectangular grid of an object along X and Y (optionally Z) (parametric Draft array).",
        (
            TARGET,
            Param("count_x", "integer", "Instances along X.", required=True, ge=1, le=1000),
            Param("count_y", "integer", "Instances along Y.", required=True, ge=1, le=1000),
            Param("step_x", "number", "Spacing along X.", required=True),
            Param("step_y", "number", "Spacing along Y.", required=True),
            Param("count_z", "integer", "Instances along Z.", default=1, ge=1, le=1000),
            Param("step_z", "number", "Spacing along Z.", default=0),
            Param("fuse", "bool", "Fuse touching instances into one solid.", default=True),
            _name("GridArray"),
        ),
        notes=PD_PATTERN_NOTE + " In a body, the grid is one MultiTransform feature.",
        example={"op": "grid_array", "target": "Vent", "count_x": 5, "count_y": 3, "step_x": 8, "step_y": 8},
    ),
    Op(
        "polar_array",
        "pattern",
        "Repeat an object around an axis (parametric Draft polar array).",
        (
            TARGET,
            Param(
                "count", "integer", "Total number of instances, including the original.", required=True, ge=2, le=1000
            ),
            Param(
                "angle",
                "number",
                "Total angle. 360 spaces instances evenly around the circle; less than 360 puts the first and last instance at the ends of the arc.",
                default=360,
                gt=0,
                le=360,
            ),
            Param("axis", "vector", "Rotation axis direction.", default=[0, 0, 1]),
            Param("center", "vector", "A point on the rotation axis.", default=[0, 0, 0]),
            Param("fuse", "bool", "Fuse touching instances into one solid.", default=True),
            _name("PolarArray"),
        ),
        notes=PD_PATTERN_NOTE,
    ),
    # ------------------------------------------------------------ transforms
    Op(
        "move",
        "transform",
        "Translate an object by an offset (edits its Placement; the feature tree stays parametric).",
        (TARGET, Param("offset", "vector", "Translation [dx, dy, dz].", required=True)),
        notes="Moving an input of a boolean moves it inside the boolean result.",
    ),
    Op(
        "rotate",
        "transform",
        "Rotate an object about an axis through 'center' (edits its Placement).",
        (
            TARGET,
            Param("angle", "number", "Rotation angle in degrees (right-hand rule).", required=True),
            Param("axis", "vector", "Rotation axis direction.", default=[0, 0, 1]),
            Param("center", "vector", "Point the axis passes through.", default=[0, 0, 0]),
        ),
    ),
    Op(
        "place",
        "transform",
        "Set an object's absolute position and/or rotation (replaces its Placement components).",
        (TARGET, Param("position", "vector", "New absolute position."), ROTATION),
    ),
    Op(
        "mirror",
        "transform",
        "Create a mirrored copy of an object (Part::Mirroring). The original is kept. For a feature of a "
        "PartDesign body (pad, pocket, hole...), mirrors the feature inside the body (PartDesign::Mirrored).",
        (
            TARGET,
            Param("plane", "enum", "Mirror plane through 'point'.", choices=("XY", "XZ", "YZ")),
            Param("normal", "vector", "Mirror plane normal (alternative to 'plane')."),
            Param("point", "vector", "A point on the mirror plane.", default=[0, 0, 0]),
            _name("Mirror"),
        ),
        one_of=(("plane", "normal"),),
        notes="For a body feature, 'point' and 'normal' are body coordinates, and the mirrored copy must touch the "
        "part (a body stays one solid). 'fuse' does not apply. A pattern or mirror can't be mirrored again: name "
        "the original feature.",
        example={"op": "mirror", "target": "Slot", "plane": "YZ", "point": [40, 0, 0]},
    ),
    Op(
        "copy",
        "transform",
        "Create a linked copy (Draft clone) that follows changes to the original, optionally offset.",
        (TARGET, Param("offset", "vector", "Translation of the copy.", default=[0, 0, 0]), _name("Copy")),
    ),
    Op(
        "scale",
        "transform",
        "Create a scaled version of an object (Draft clone with Scale), about the origin. The original becomes an intermediate.",
        (
            TARGET,
            Param("factor", "number_or_vector", "Uniform factor, or [sx, sy, sz].", required=True),
            _name("Scaled"),
        ),
    ),
    # ------------------------------------------------------------ editing
    Op(
        "set",
        "edit",
        "Change properties of an existing object and recompute everything downstream. Use 'inspect' to see editable properties.",
        (
            TARGET,
            Param(
                "properties",
                "object",
                'Property values, e.g. {"Height": 12, "Radius": "=Params.bore / 2"}. Use null to clear an expression. Also accepts "position" and "rotation", and for fillets/chamfers/shells the op parameters (radius, size, edges, thickness, open_faces).',
                required=True,
            ),
        ),
        example={"op": "set", "target": "Plate", "properties": {"Height": 12}},
    ),
    Op(
        "set_params",
        "edit",
        "Create or update named parameters in the 'Params' spreadsheet. Reference them in numeric parameters as '=Params.<name>'.",
        (
            Param(
                "values",
                "object",
                'Parameter values, e.g. {"wall": 2, "bore": 8}. Numbers are millimetres unless a unit string is given ("15 deg").',
                required=True,
            ),
        ),
        example={"op": "set_params", "values": {"plate_t": 8, "hole_d": 6.5}},
    ),
    Op(
        "delete",
        "edit",
        "Delete objects. Refuses to delete objects other objects depend on, unless 'with_dependents' is true.",
        (
            Param("targets", "names", "Objects to delete."),
            Param("all", "bool", "Delete every object in the document.", default=False),
            Param("with_dependents", "bool", "Also delete objects that depend on the targets.", default=False),
        ),
    ),
    Op(
        "rename",
        "edit",
        "Change an object's label. Its internal Name never changes; both can be used as references.",
        (
            TARGET,
            Param("label", "label", "New label: any text, e.g. 'Base plate' (unique in the document).", required=True),
        ),
    ),
    # ------------------------------------------------------------ query
    Op(
        "inspect",
        "query",
        "Describe the document (no target) or one object in detail: properties, dependencies, geometry and optionally faces/edges.",
        (
            Param("target", "name", "Object to inspect. Omit for the whole document tree."),
            Param(
                "topology", "bool", "Include per-face and per-edge descriptors (indices for selectors).", default=False
            ),
        ),
        mutates=False,
    ),
    Op(
        "check",
        "query",
        "Assert geometric expectations on an object; fails with EXPECTATION_FAILED if they do not hold.",
        (
            TARGET,
            Param(
                "expect",
                "expect",
                "Expectations: volume, bbox_size, bbox_min, bbox_max, solids, valid, self_intersecting (false holds only when the check ran and passed), tolerance (mm, default 0.01), volume_tolerance (relative, default 0.001).",
                required=True,
            ),
        ),
        mutates=False,
    ),
    Op(
        "import",
        "solid",
        "Import a solid from a STEP/IGES/BREP/FCStd file or a closed mesh (STL/OBJ/3MF/PLY/OFF) in the workspace, "
        "or a ready-made part from the official "
        "FreeCAD library (bearings, motors, fasteners, profiles, electronics...). Find library parts with "
        "'fcskill.py library <keywords>'.",
        (
            Param(
                "library",
                "string",
                "Library part, as given by 'fcskill.py library' ('part'), e.g. "
                "'Mechanical Parts/Bearings/608ZZ_Ball_Bearing'. Downloaded on first use.",
            ),
            Param(
                "file",
                "path",
                "A .step/.stp, .iges/.igs, .brep or .FCStd file, or a .stl/.obj/.3mf/.ply/.off mesh, in the workspace.",
            ),
            Param(
                "refine",
                "bool",
                "Meshes: merge coplanar triangles into larger faces (cleaner, faster booleans). Skipped above 10000 triangles.",
                default=True,
            ),
            Param(
                "anchor",
                "enum",
                "Which point of the part's bounding box lands on 'position': as modelled ('origin'), "
                "'center', 'bottom_center' or 'min_corner'.",
                default="origin",
                choices=("origin", "center", "bottom_center", "min_corner"),
            ),
            Param("position", "vector", "Where the anchor goes.", default=[0, 0, 0]),
            Param("rotation", "rotation", "Rotation about the anchor point, after anchoring."),
            _name("Imported"),
        ),
        one_of=(("library", "file"),),
        notes="The result is a fixed shape: place, cut, fuse, measure, give it a material or add it to an assembly, but its "
        "dimensions are not editable. Check the reported bbox: library parts keep their author's orientation. "
        "Library parts are CC-BY 3.0: pass the reported 'attribution' on to the user. A mesh becomes a solid made of "
        "its triangles (flat facets, no true cylinders), so cut, fuse, measure and export work, but fillets on its "
        "edges and FEM are unreliable. Meshes must be closed and manifold (repair them first otherwise), up to 20000 "
        "triangles, and are slow to work with (booleans take seconds per few thousand triangles); mesh files carry no units, so check the reported bbox (CHECK_UNITS warns when the size is implausible).",
        example={
            "op": "import",
            "library": "Mechanical Parts/Bearings/608ZZ_Ball_Bearing",
            "name": "Bearing",
            "anchor": "center",
            "position": [0, 0, 20],
        },
    ),
    Op(
        "material",
        "edit",
        "Give finished parts a material (FreeCAD material: density, mechanical data, appearance) and/or a colour. "
        "Shown when the file is opened in FreeCAD and in render images; measure uses the density for masses.",
        (
            Param(
                "targets",
                "names",
                "Parts to set (solids, bodies, or assembly parts: the material goes to their source).",
                required=True,
            ),
            Param(
                "material",
                "string",
                "Preset: steel, steel_s235, steel_s355, stainless_steel, stainless_304, cast_iron, aluminium, "
                "aluminium_6061, aluminium_7075, aluminium_5754, titanium, copper, brass, bronze, gold, silver, chrome, "
                "pla, abs, petg, nylon, nylon_pa12, pom, polypropylene, polycarbonate, acrylic, ptfe, pvc, rubber, "
                "glass, wood, concrete, default; or any FreeCAD library material name (e.g. 'Steel-C45E'). Grades "
                "(steel_s235, aluminium_6061, ...) also carry the strength data 'fem_static' uses.",
            ),
            Param(
                "color",
                "color",
                "Custom colour, '#RRGGBB' or [r, g, b] in 0..1 (e.g. a filament colour); overrides the material's look.",
            ),
            Param("transparency", "integer", "Transparency in percent.", ge=0, le=100),
        ),
        notes="Give 'material', 'color' or both. Plastic presets come with a neutral default colour; give 'color' for the "
        "real one. Colour alone keeps the material set before.",
        example={"op": "material", "targets": ["Rim"], "material": "aluminium"},
    ),
    Op(
        "measure",
        "query",
        "Clearance and interference between objects (minimum distance, closest points, overlap volume), and each "
        "object's mass properties: volume, area, centre of mass and inertia tensor, plus mass with a material. "
        "Use it to check that parts fit together and what they weigh.",
        (
            Param(
                "objects",
                "names",
                "Objects to compare pairwise (default: all result objects). An assembly stands for "
                "its parts, measured where they are assembled; name a single part by its link (e.g. Pin_Part).",
            ),
            Param(
                "require",
                "object",
                'Assertions that fail the step: {"min_clearance": mm} and/or {"no_interference": true}.',
            ),
            Param(
                "material",
                "string",
                "Material for mass (g): a preset or FreeCAD library material name, as in the 'material' op "
                "(e.g. 'steel', 'pla', 'rubber'). Without it, materials assigned with 'material' are used.",
            ),
            Param("density", "number", "Explicit density in g/cm3 (instead of 'material').", gt=0),
        ),
        mutates=False,
        notes="Status per pair: 'clear' (distance > 0), 'touching' (distance 0, no overlap) or 'interfering' (overlap volume > 0). "
        "'properties' gives, per object, the inertia tensor about its centre of mass along the global axes: in "
        "g*mm2 ('inertia_g_mm2', with its principal moments) when a density is known, otherwise geometric "
        "('inertia_mm5': multiply by the density in g/mm3). With masses for every object, 'total' gives the "
        "combined mass and centre of mass.",
        example={"op": "measure", "objects": ["Lid", "Box"], "require": {"min_clearance": 0.3}},
    ),
    Op(
        "export",
        "output",
        "Export objects to STEP, IGES, BREP, STL, OBJ or 3MF, or as a flat 2D outline (DXF, SVG) for laser/CNC cutting, "
        "and verify the written file by reading it back. STEP files carry each part's name, and an assembly "
        "as a product structure (every part once, placed as often as it is used).",
        (
            Param(
                "filename",
                "path",
                "Output path relative to the workspace; the extension sets the format (.step/.stp, .iges/.igs, "
                ".brep, .stl, .obj, .3mf, .dxf, .svg).",
                required=True,
            ),
            Param(
                "view",
                "enum",
                "DXF/SVG: direction of the flat projection, in model millimetres (1:1).",
                default="top",
                choices=("top", "bottom", "front", "back", "right", "left"),
            ),
            Param("targets", "names", "Objects to export. Default: all result objects."),
            Param("tolerance", "number", "Mesh formats: max chordal deviation in mm.", default=0.05, gt=0),
            Param(
                "angular_tolerance",
                "number",
                "Mesh formats: max angular deviation in degrees.",
                default=15,
                gt=0,
                le=90,
            ),
        ),
        mutates=False,
    ),
    Op(
        "fem_static",
        "query",
        "Linear static stress analysis (Gmsh + CalculiX, 2nd-order elements): fixed faces, forces/pressures with units. "
        "Reports max displacement and von Mises stress with locations, safety factor against yield, an equilibrium check "
        "(reactions vs loads) and mesh convergence (a second solve on a 0.7x finer mesh).",
        (
            TARGET,
            Param(
                "material",
                "string",
                "Material grade with strength data (E, Poisson, density, yield): steel_s235, steel_s355, "
                "stainless_304, aluminium_6061, aluminium_7075, aluminium_5754, titanium, brass, pla, petg, abs, "
                "nylon_pa12. Default: the material assigned to the part with the 'material' op. Generic "
                "materials (steel, aluminium) are refused: their yield strength depends on the grade.",
            ),
            Param("fixed", "selector", "Faces held fixed, e.g. '<X' (the bolted face).", required=True),
            Param(
                "loads",
                "loads",
                'List of {"faces": selector, "force": "500 N", "direction": [0, 0, -1]} (total force spread over the faces) '
                'or {"faces": selector, "pressure": "0.5 MPa"} (pushes into planar faces).',
                required=True,
            ),
            Param(
                "mesh_size",
                "number",
                "Element size in mm. Default: about the wall thickness (estimated as 2 x volume / area), which "
                "suits deflection; give a smaller size for stresses near holes and corners (see convergence).",
                gt=0,
            ),
            Param(
                "convergence",
                "bool",
                "Solve twice (mesh size and 0.7x) and report how much the results change.",
                default=True,
            ),
            Param(
                "require",
                "object",
                'Assertions that fail the step: {"min_safety_factor": 2} and/or {"max_displacement": 0.5} (mm).',
            ),
            Param("report", "path", "Write a PNG stress map (4 views)."),
            Param(
                "keep",
                "bool",
                "Keep the analysis (mesh, results) in the document for review in the FreeCAD GUI.",
                default=False,
            ),
        ),
        mutates=False,
        notes="Estimates only: linear elastic, small deformations, no contact. Printed plastics are weaker between layers. "
        "Peak stress at sharp inner corners is mesh-dependent (STRESS_CONCENTRATION warning): add fillets. "
        "A check that could not run is a warning (NO_CONVERGENCE_CHECK, NO_EQUILIBRIUM_CHECK): the result is then unverified.",
        example={
            "op": "fem_static",
            "target": "Bracket",
            "material": "aluminium_6061_t6",
            "fixed": "<X",
            "loads": [{"faces": ">X", "force": "200 N", "direction": [0, 0, -1]}],
            "require": {"min_safety_factor": 2},
            "report": "stress.png",
        },
    ),
    Op(
        "drawing",
        "output",
        "Make a 2D technical drawing (TechDraw page): front, plan and side views at a standard scale, overall and hole "
        "dimensions checked against the model, ISO title block; written as DXF. The page is kept in the .FCStd for PDF export in the GUI.",
        (
            Param("filename", "path", "Output .dxf path relative to the workspace.", required=True),
            Param("targets", "names", "Objects to draw. Default: all solid result objects."),
            Param("sheet", "enum", "Paper size (landscape).", default="A4", choices=("A4", "A3")),
            Param(
                "projection",
                "enum",
                "View arrangement: ISO first angle (plan below, left view on the right) or third angle.",
                default="first_angle",
                choices=("first_angle", "third_angle"),
            ),
            Param(
                "scale", "number", "Fixed scale (e.g. 0.5 for 1:2). Default: largest standard scale that fits.", gt=0
            ),
            Param(
                "dimensions",
                "enum",
                "Dimensions to add.",
                default="overall_and_holes",
                choices=("none", "overall", "overall_and_holes"),
            ),
            Param("iso", "bool", "Add a small isometric view.", default=False),
            Param("title", "string", "Title block: title (default: the part's label)."),
            Param("author", "string", "Title block: creator."),
            Param("material", "string", "Title block: material."),
            Param("number", "string", "Title block: drawing number."),
            Param(
                "preview",
                "path",
                "Also write a PNG preview rendered from the DXF (geometry and dimension lines; no text).",
            ),
            _name("Drawing"),
        ),
        notes="Re-running with the same name regenerates the page (do this after editing the model). PDF/SVG pages need the FreeCAD GUI. "
        "For a flat 1:1 outline for laser/CNC cutting, use 'export' with a .dxf or .svg filename instead.",
        example={
            "op": "drawing",
            "filename": "bracket.dxf",
            "title": "Bracket",
            "author": "ACME",
            "material": "Aluminium 6061",
        },
    ),
    Op(
        "render",
        "output",
        "Render shaded PNG views of the model for a visual check (headless, no GUI needed). Look at the image to confirm features are where you intended.",
        (
            Param("filename", "path", "Output .png path relative to the workspace.", required=True),
            Param(
                "views",
                "views",
                "Views in reading order (2 per row). Choices: iso, front, back, left, right, top, bottom.",
                default=["iso", "front", "top", "right"],
            ),
            Param("targets", "names", "Objects to render. Default: all result objects."),
            Param(
                "size",
                "integer",
                "Pixel size of each square view (the sheet adds 2 px separators between views).",
                default=400,
                ge=64,
                le=2048,
            ),
        ),
        mutates=False,
        notes="All views share one scale (see mm_per_pixel in the result). front looks along +Y, right along -X, top along -Z; "
        "iso looks from the front-right-top corner. Each view has an axis triad bottom-left: X red, Y green, Z blue.",
        example={"op": "render", "filename": "preview.png", "views": ["iso", "top"]},
    ),
]

OPS_BY_NAME: Dict[str, Op] = {op.name: op for op in OPS}

# Keys allowed on every step in addition to the op's own parameters.
STEP_KEYS = ("op", "expect", "comment")

# Request envelope keys.
REQUEST_KEYS = ("doc", "new", "steps", "dry_run", "brief")

EXPECT_KEYS = (
    "volume",
    "bbox_size",
    "bbox_min",
    "bbox_max",
    "solids",
    "valid",
    "self_intersecting",
    "tolerance",
    "volume_tolerance",
)

CATEGORIES = (
    "solid",
    "profile",
    "partdesign",
    "assembly",
    "boolean",
    "feature",
    "pattern",
    "transform",
    "edit",
    "query",
    "output",
)


def describe(names: Optional[List[str]] = None) -> Dict[str, Any]:
    """Machine-readable catalog, optionally restricted to some ops."""
    ops = OPS if not names else [OPS_BY_NAME[n] for n in names if n in OPS_BY_NAME]
    return {
        "units": {"length": "mm", "angle": "deg"},
        "request": {
            "doc": "FreeCAD document path relative to the workspace (default 'model.FCStd'). Created if missing.",
            "new": "true to start from an empty document, discarding the existing file's content.",
            "steps": "Ordered list of operations. All-or-nothing: on any error nothing is saved or exported.",
            "dry_run": "true to execute and report without saving or exporting anything.",
            "brief": "true to leave volume and bounding box out of the per-step entries (long requests); "
            "results, warnings and errors are reported as usual.",
        },
        "step_keys": {
            "op": "Operation name.",
            "expect": "Optional expectations checked on the step's result object (see op 'check').",
            "comment": "Free text, ignored.",
        },
        "ops": [op.describe() for op in ops],
    }
