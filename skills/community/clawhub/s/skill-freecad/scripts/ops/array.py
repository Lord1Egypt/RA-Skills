import FreeCAD as App
import Part
import math
from . import utils

def run(p, doc=None):
    if doc is None:
        doc = App.ActiveDocument

    a_type = p.get("type", "linear").lower()
    target_name = p.get("target")
    name = p.get("name", f"{a_type}_array")
    count = p.get("count", 2)
    
    obj = utils.find_object(doc, target_name)
    if not obj or not hasattr(obj, "Shape"):
        raise ValueError(f"Target object '{target_name}' not found")

    base_shape = obj.Shape
    shapes = [base_shape]

    if a_type == "linear":
        vec = App.Vector(*p.get("step", [10, 0, 0]))
        for i in range(1, count):
            copy_shape = base_shape.copy()
            copy_shape.translate(vec.multiply(i))
            shapes.append(copy_shape)
    elif a_type == "polar":
        axis = App.Vector(*p.get("axis", [0, 0, 1]))
        center = App.Vector(*p.get("center", [0, 0, 0]))
        total_angle = p.get("angle", 360)
        step_angle = total_angle / count
        for i in range(1, count):
            copy_shape = base_shape.copy()
            copy_shape.rotate(center, axis, step_angle * i)
            shapes.append(copy_shape)
    else:
        raise ValueError(f"Unknown array type: {a_type}")

    fused = shapes[0]
    for i in range(1, len(shapes)):
        fused = fused.fuse(shapes[i])

    array_obj = doc.addObject("Part::Feature", name)
    array_obj.Label = name
    array_obj.Shape = fused
    return array_obj
