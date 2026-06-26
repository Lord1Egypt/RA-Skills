"""Tests for stack trace extraction."""

from repro_pack.parser.stack_trace import extract_stack_traces


class TestPythonTrace:
    def test_extracts_python_trace(self, python_stack_trace):
        traces = extract_stack_traces(python_stack_trace)
        assert len(traces) >= 1
        t = traces[0]
        assert t.language == "python"
        assert t.exception_type == "TypeError"
        assert "NoneType" in t.exception_message
        assert len(t.frames) == 3
        assert t.frames[0].file_path == "/app/main.py"
        assert t.frames[0].line_number == 42

    def test_extracts_function_names(self, python_stack_trace):
        traces = extract_stack_traces(python_stack_trace)
        funcs = [f.function_name for f in traces[0].frames]
        assert "handle_request" in funcs
        assert "process_data" in funcs


class TestJavaTrace:
    def test_extracts_java_trace(self, java_stack_trace):
        traces = extract_stack_traces(java_stack_trace)
        assert len(traces) >= 1
        t = traces[0]
        assert t.language == "java"
        assert t.exception_type == "java.lang.NullPointerException"
        assert len(t.frames) >= 2


class TestJSTrace:
    def test_extracts_js_trace(self, js_stack_trace):
        traces = extract_stack_traces(js_stack_trace)
        assert len(traces) >= 1
        t = traces[0]
        assert t.language == "javascript"
        assert t.exception_type == "TypeError"
        assert "map" in t.exception_message
        assert len(t.frames) >= 2
        assert t.frames[0].line_number == 142


class TestNoTrace:
    def test_no_trace_in_normal_text(self):
        traces = extract_stack_traces("Just a normal log message\nNothing to see here")
        assert traces == []
