# Parametric Door Frame (Türzarge)
# Inputs: Lichthoehe, Lichtbreite, Zargenbreite, Zargentiefe, Falzbreite, Falztiefe
# Outputs: Geometry

import Rhino.Geometry as rg

# All dimensions in mm
lh = Lichthoehe    # Clear opening height
lb = Lichtbreite   # Clear opening width  
zb = Zargenbreite  # Frame width (visible face)
zt = Zargentiefe   # Frame depth (into wall)
fb = Falzbreite    # Rabbet width
ft = Falztiefe     # Rabbet depth

geometries = []

# Left jamb (Zarge links)
left_outer = rg.Box(
    rg.Plane.WorldXY,
    rg.Interval(-zb, 0),
    rg.Interval(0, zt),
    rg.Interval(0, lh + zb)
)
geometries.append(left_outer.ToBrep())

# Left rabbet (Falz links)
if fb > 0 and ft > 0:
    left_falz = rg.Box(
        rg.Plane.WorldXY,
        rg.Interval(0, fb),
        rg.Interval(zt - ft, zt),
        rg.Interval(0, lh + zb)
    )
    geometries.append(left_falz.ToBrep())

# Right jamb (Zarge rechts)
right_outer = rg.Box(
    rg.Plane.WorldXY,
    rg.Interval(lb, lb + zb),
    rg.Interval(0, zt),
    rg.Interval(0, lh + zb)
)
geometries.append(right_outer.ToBrep())

# Right rabbet (Falz rechts)
if fb > 0 and ft > 0:
    right_falz = rg.Box(
        rg.Plane.WorldXY,
        rg.Interval(lb - fb, lb),
        rg.Interval(zt - ft, zt),
        rg.Interval(0, lh + zb)
    )
    geometries.append(right_falz.ToBrep())

# Head (Kopfstück oben)
head = rg.Box(
    rg.Plane.WorldXY,
    rg.Interval(-zb, lb + zb),
    rg.Interval(0, zt),
    rg.Interval(lh, lh + zb)
)
geometries.append(head.ToBrep())

# Head rabbet (Falz oben)
if fb > 0 and ft > 0:
    head_falz = rg.Box(
        rg.Plane.WorldXY,
        rg.Interval(0, lb),
        rg.Interval(zt - ft, zt),
        rg.Interval(lh - fb, lh)
    )
    geometries.append(head_falz.ToBrep())

# Union all parts
result = rg.Brep.CreateBooleanUnion(geometries, 0.01)
if result and len(result) > 0:
    Geometry = result[0]
else:
    # Fallback: return all parts separately
    Geometry = geometries
