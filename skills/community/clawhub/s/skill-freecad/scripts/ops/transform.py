import FreeCAD as App
from . import utils

def run(p, doc=None):
    if doc is None:
        doc = App.ActiveDocument

    target_name = p.get("target")
    if not target_name:
        raise ValueError("Transform operation requires a 'target' object name")

    obj = utils.find_object(doc, target_name)
    if not obj:
        raise ValueError(f"Could not find target object: {target_name}")

    # Translation
    translate = p.get("translate")
    if translate:
        vec = App.Vector(*translate)
        obj.Placement.Base = obj.Placement.Base.add(vec)

    # Rotation (Roll, Pitch, Yaw in degrees)
    rotate = p.get("rotate")
    if rotate:
        rot = App.Rotation(*rotate)
        obj.Placement.Rotation = obj.Placement.Rotation.multiply(rot)

    # Scale uniformly or non-uniformly
    scale = p.get("scale")
    if scale is not None:
        if isinstance(scale, (int, float)):
            # Uniform
            obj.Shape = obj.Shape.scale(float(scale))
        elif isinstance(scale, list) and len(scale) == 3:
            # Non-uniform scaling requires matrix operation
            mat = App.Matrix()
            mat.scale(scale[0], scale[1], scale[2])
            obj.Shape = obj.Shape.transformShape(mat)
