import FreeCAD as App
import Part
import os

def load_or_create_doc(filename="model.FCStd", doc_name="Model"):
    """Loads an existing FreeCAD document or creates a new one."""
    safe_filename = os.path.basename(filename)
    if os.path.exists(safe_filename):
        doc = App.openDocument(safe_filename)
    else:
        doc = App.newDocument(doc_name)
    App.setActiveDocument(doc.Name)
    return doc

def find_object(doc, name):
    """Finds an object by name or label in the document."""
    obj = doc.getObject(name)
    if not obj:
        obj = doc.getObject(name.replace(" ", "_"))
    if not obj:
        # Search by Label
        for o in doc.Objects:
            if o.Label == name:
                return o
    return obj

def save_and_export(doc, fcstd_filename="model.FCStd", step_filename="model.step"):
    """Saves the document and exports all Part features to a STEP file."""
    safe_fcstd = os.path.basename(fcstd_filename)
    safe_step = os.path.basename(step_filename)
    
    doc.recompute()
    doc.saveAs(safe_fcstd)
    
    export_objs = []
    for obj in doc.Objects:
        if hasattr(obj, "Shape") and obj.Shape and not obj.Shape.isNull():
            export_objs.append(obj)
            
    if export_objs:
        Part.export(export_objs, safe_step)

def get_document_state(doc):
    """Returns a dictionary of all relevant shapes and their bounding boxes for the LLM context."""
    objs = []
    for obj in doc.Objects:
        if hasattr(obj, "Shape") and obj.Shape and not obj.Shape.isNull():
            bb = obj.Shape.BoundBox
            objs.append({
                "name": obj.Name,
                "label": obj.Label,
                "volume": obj.Shape.Volume if hasattr(obj.Shape, "Volume") else 0,
                "bounding_box": {
                    "x_min": round(bb.XMin, 3), "x_max": round(bb.XMax, 3),
                    "y_min": round(bb.YMin, 3), "y_max": round(bb.YMax, 3),
                    "z_min": round(bb.ZMin, 3), "z_max": round(bb.ZMax, 3)
                }
            })
    return objs
