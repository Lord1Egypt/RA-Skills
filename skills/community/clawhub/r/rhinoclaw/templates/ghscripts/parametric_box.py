# Parametric Box with optional fillet
# Inputs: Width, Height, Depth, FilletRadius (all numbers)
# Outputs: Geometry

import Rhino.Geometry as rg

# Create centered box
plane = rg.Plane.WorldXY
interval_x = rg.Interval(-Width / 2.0, Width / 2.0)
interval_y = rg.Interval(-Depth / 2.0, Depth / 2.0)
interval_z = rg.Interval(0, Height)

box = rg.Box(plane, interval_x, interval_y, interval_z)
brep = box.ToBrep()

# Apply fillet if radius > 0
if FilletRadius > 0:
    edges = [i for i in range(brep.Edges.Count)]
    radii = [FilletRadius] * len(edges)
    filleted = rg.Brep.CreateFilletEdges(brep, edges, radii, radii, 
                                          rg.BlendType.Fillet, 
                                          rg.RailType.DistanceFromEdge, 0.01)
    if filleted and len(filleted) > 0:
        brep = filleted[0]

Geometry = brep
