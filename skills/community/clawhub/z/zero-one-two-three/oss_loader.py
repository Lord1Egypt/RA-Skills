import importlib


class ToolLoader:
    def __init__(self):
        pass

    def load_tool(self, tool_name):
        module_name = tool_name[:-3] if tool_name.endswith('.py') else tool_name
        return importlib.import_module(f'tools.{module_name}')