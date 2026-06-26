import FreeCAD as App

# Inspect doesn't need to do anything to the document since cad_engine always prints 
# document state at the end of execution. Calling this operation is just a fast way 
# to trigger a state read.
def run(p, doc=None):
    pass
