import sys
import json
import traceback
import os
import contextlib

@contextlib.contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def inject_freecad_path():
    try:
        import FreeCAD
        return
    except ImportError:
        pass
    
    fc_path = os.environ.get("FREECAD_PATH")
    paths = [fc_path] if fc_path else []
    
    if sys.platform == "win32":
        import glob
        for prog in [os.environ.get("ProgramFiles"), os.environ.get("ProgramW6432"), os.environ.get("ProgramFiles(x86)")]:
            if prog:
                paths += glob.glob(os.path.join(prog, "FreeCAD*", "bin"))
    elif sys.platform == "darwin":
        paths += ["/Applications/FreeCAD.app/Contents/Resources/lib", "/Applications/FreeCAD.app/Contents/Resources/bin"]
    else:
        paths += ["/usr/lib/freecad/lib", "/usr/lib/freecad/Ext/freecad/lib", "/usr/lib/freecad-daily/lib"]

    for p in paths:
        if p and os.path.isdir(p):
            sys.path.append(p)
            try:
                import FreeCAD
                return
            except ImportError:
                sys.path.pop()

inject_freecad_path()

# Load ops inside suppression to avoid noisy FreeCAD init logs
with suppress_stdout():
    from ops import utils, primitive, boolean, transform, export, inspect, modifier, array, profile

def execute_op(op, params, doc):
    if op == "create_primitive":
        return primitive.run(params, doc)
    elif op == "boolean":
        return boolean.run(params, doc)
    elif op == "transform":
        return transform.run(params, doc)
    elif op == "export":
        return export.run(params, doc)
    elif op == "inspect":
        return inspect.run(params, doc)
    elif op == "modifier":
        return modifier.run(params, doc)
    elif op == "array":
        return array.run(params, doc)
    elif op == "profile":
        return profile.run(params, doc)
    else:
        raise ValueError(f"Unknown operation: {op}")

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Missing JSON input"}))
        sys.exit(1)

    try:
        cmd = json.loads(sys.argv[1])
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Invalid JSON input: {e}"}))
        sys.exit(1)

    result = {}
    try:
        with suppress_stdout():
            doc = utils.load_or_create_doc("model.FCStd")
            
            if cmd.get("operation") == "batch":
                steps = cmd.get("parameters", {}).get("steps", [])
                for step in steps:
                    execute_op(step["operation"], step["parameters"], doc)
            else:
                execute_op(cmd["operation"], cmd["parameters"], doc)
                
            utils.save_and_export(doc, "model.FCStd", "model.step")
            
            state = utils.get_document_state(doc)
            
        result = {
            "status": "success",
            "objects": state
        }
    except Exception as e:
        result = {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }

    # Emit clean JSON for OpenClaw
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
