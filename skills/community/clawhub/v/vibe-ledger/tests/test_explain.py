import pytest

import explain
import graph

CLIENT = '''import OpenAI from "openai";

export async function runAnthropic(request) {
  return fetch(request.url);
}

const runOpenAi = async (request) => {
  return request;
};

function helper() {}
const shared = function () {};
const tiny = x => x;

export default class Client {
  static create() {}
  async send(payload) {
    if (payload) {
      return payload;
    }
  }
}

const api = {
  ping() { return 1; },
  pong: async () => 2,
  pang: function () { return 3; },
};
'''
PY = "class Store:\n    def save(self):\n        pass\n\nasync def fetch_all():\n    pass\n\ndef run():\n    pass\n"


def test_definitions_cover_common_forms():
    defs = explain.find_definitions(CLIENT, "js")
    for name, line in (("runAnthropic", 3), ("runOpenAi", 7), ("helper", 11), ("shared", 12), ("tiny", 13),
                       ("Client", 15), ("create", 16), ("send", 17), ("ping", 25), ("pong", 26), ("pang", 27)):
        assert defs.get(name) == [line], (name, defs.get(name))
    assert "if" not in defs and "return" not in defs and "fetch" not in defs
    py = explain.find_definitions(PY, "py")
    assert py == {"Store": [1], "save": [2], "fetch_all": [5], "run": [8]}


@pytest.fixture
def project(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "client.js").write_text(CLIENT, encoding="utf-8")
    (tmp_path / "src" / "main.js").write_text('import { runAnthropic } from "./client";\n', encoding="utf-8")
    g = graph.build(tmp_path, [], {"findings": []})
    index = {"m1": {"id": "m1", "session": "s1", "ts": "2026-09-12T09:00:00Z", "role": "user", "kind": "text",
                    "text": "AI 总结要调用 Anthropic，不要让陌生人随便用"}}
    return tmp_path, g, index


def doc(**entry):
    base = {"purpose_plain": "负责调用 AI 服务商。", "purpose_dev": "Wraps `runAnthropic`.", "functions": [], "history": []}
    base.update(entry)
    return {"evidence": {"H1": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "AI 总结要调用 Anthropic"},
                         "H2": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "我编的一句话"}},
            "files": {"src/client.js": base}}


def test_functions_are_checked_corrected_or_dropped(project):
    root, g, index = project
    out = explain.verify(doc(functions=[{"name": "runAnthropic", "line": 4, "plain": "a"},
                                        {"name": "send", "line": 40, "plain": "b"},
                                        {"name": "deleteEverything", "line": 3, "plain": "c"}]), g, root, index)
    f = out["files"]["src/client.js"]
    assert [(x["name"], x["line"], x["line_corrected"]) for x in f["functions"]] == [("runAnthropic", 3, False), ("send", 17, True)]
    assert f["dropped_functions"] == [{"name": "deleteEverything", "reason": "not defined in this file"}]
    assert out["verification"]["functions_dropped"] == 1


def test_invented_function_is_dropped(project):
    root, g, index = project
    out = explain.verify(doc(functions=[{"name": "stealKeys", "line": 1, "plain": "x"}]), g, root, index)
    assert out["files"]["src/client.js"]["functions"] == []


def test_backticked_identifiers_must_exist(project):
    root, g, index = project
    good = explain.verify(doc(purpose_plain="调用 `runAnthropic()`，被 `main.js` 使用，见 `npm run dev`。"), g, root, index)
    assert good["files"]["src/client.js"]["purpose_unverified"] is False
    bad = explain.verify(doc(purpose_dev="Uses `secretVault` and `ghost.ts`."), g, root, index)
    f = bad["files"]["src/client.js"]
    assert f["purpose_unverified"] is True and f["missing_identifiers"] == ["ghost.ts", "secretVault"]


def test_history_keeps_only_verified_quotes(project):
    root, g, index = project
    out = explain.verify(doc(history=[{"plain": "用户要求", "evidence": ["H1"]},
                                      {"plain": "编的", "evidence": ["H2"]}]), g, root, index)
    assert [h["plain"] for h in out["files"]["src/client.js"]["history"]] == ["用户要求"]
    assert out["evidence"]["H1"]["ok"] and not out["evidence"]["H2"]["ok"]


def test_paths_outside_the_graph_are_rejected(project):
    root, g, index = project
    d = doc()
    d["files"]["src/nope.js"] = d["files"].pop("src/client.js")
    out = explain.verify(d, g, root, index)
    assert out["files"] == {} and out["rejected"] == [{"path": "src/nope.js", "reason": "not a file in the graph"}]


@pytest.mark.parametrize("mutate, needle", [
    (lambda d: d["files"]["src/client.js"].pop("purpose_plain"), "purpose_plain"),
    (lambda d: d["files"]["src/client.js"].update(functions=[{"name": "x", "line": "3", "plain": "p"}]), "line"),
    (lambda d: d["files"]["src/client.js"].update(history=[{"plain": "p", "evidence": ["H9"]}]), "H9"),
    (lambda d: d["evidence"].update(H3={"kind": "code"}), "transcript"),
    (lambda d: d.update(files=[]), "files"),
])
def test_validate_lists_problems(mutate, needle):
    d = doc()
    mutate(d)
    with pytest.raises(explain.ExplainError) as exc:
        explain.validate(d)
    assert any(needle in p for p in exc.value.problems), exc.value.problems


def test_merge_prefixes_evidence_and_keeps_first_duplicate():
    a, b = doc(), doc()
    b["files"]["src/other.js"] = dict(b["files"]["src/client.js"], history=[{"plain": "h", "evidence": ["H1"]}])
    out = explain.merge([a, b])
    assert set(out["evidence"]) == {"p1_H1", "p1_H2", "p2_H1", "p2_H2"}
    assert out["files"]["src/other.js"]["history"][0]["evidence"] == ["p2_H1"]
    assert out["duplicates"] == ["src/client.js"]
    explain.validate(out)


def test_summary_lines(project):
    root, g, index = project
    out = explain.verify(doc(functions=[{"name": "ghost", "line": 1, "plain": "x"}]), g, root, index)
    text = "\n".join(explain.summary_lines(out))
    assert "1 files kept" in text and "ghost" in text


def test_definitions_after_a_match_pattern_string():
    text = ('const PATTERNS = ["*://*/*"];\nexport async function requestAccess(api) {\n  return api;\n}\n'
            "/** Docs. */\nexport function other() {}\n")
    defs = explain.find_definitions(text, "js")
    assert defs["requestAccess"] == [2] and defs["other"] == [6]


def test_backticked_files_that_exist_outside_the_graph_count(project):
    root, g, index = project
    (root / "manifest.json").write_text("{}", encoding="utf-8")
    (root / "vendor" / "lib").mkdir(parents=True)
    (root / "vendor" / "lib" / "x.mjs").write_text("", encoding="utf-8")
    ok = explain.verify(doc(purpose_dev="Reads `manifest.json` and loads `vendor/lib/x.mjs`."), g, root, index)
    assert ok["files"]["src/client.js"]["purpose_unverified"] is False
    bad = explain.verify(doc(purpose_dev="Reads `missing.json`."), g, root, index)
    assert bad["files"]["src/client.js"]["missing_identifiers"] == ["missing.json"]


def journey_doc(*journeys):
    d = doc()
    d["journeys"] = list(journeys)
    return d


def test_journeys_are_checked_step_by_step(project):
    root, g, index = project
    out = explain.verify(journey_doc(
        {"title": "你点「发送」时", "outcome": "回答出现在页面上",
         "steps": [{"file": "src/main.js", "plain": "页面调用发送"},
                   {"file": "src/client.js", "plain": "把请求发给 Anthropic", "function": "runAnthropic", "line": 4},
                   {"file": "src/ghost.js", "plain": "编出来的文件"}]},
        {"title": "只剩一步的路线", "steps": [{"file": "src/main.js", "plain": "a"}, {"file": "src/nope.js", "plain": "b"}]},
        {"title": "两步没有引用关系", "steps": [{"file": "src/client.js", "plain": "a"}, {"file": "src/client.js", "plain": "b"},
                                          {"file": "src/main.js", "plain": "c", "function": "made_up", "line": 1}]}), g, root, index)
    first, third = out["journeys"]
    assert first["id"] == "J1" and third["id"] == "J2" and first["outcome"] == "回答出现在页面上"
    assert [s["file"] for s in first["steps"]] == ["src/main.js", "src/client.js"]
    assert first["steps"][1]["linked"] is True and first["steps"][1]["line"] == 3  # main.js imports client.js
    assert first["dropped_steps"] == [{"file": "src/ghost.js", "reason": "not a file in the graph"}]
    assert third["steps"][1]["linked"] is True  # the same file twice is a step inside one file
    assert third["steps"][2]["linked"] is True and "function" not in third["steps"][2]
    assert third["steps"][2]["dropped_function"] == {"name": "made_up", "reason": "not defined in this file"}
    assert out["rejected_journeys"] == [{"title": "只剩一步的路线", "reason": "fewer than 2 steps are files in the graph"}]
    assert out["verification"]["journeys"] == 2
    assert out["verification"]["journey_steps_dropped"] == 1  # a rejected journey is reported whole, not step by step


def test_unlinked_steps_are_kept_but_marked(project):
    root, g, index = project
    (root / "src" / "lonely.js").write_text("export const z = 1;\n", encoding="utf-8")
    g = graph.build(root, [], {"findings": []})
    out = explain.verify(journey_doc({"title": "t", "steps": [{"file": "src/lonely.js", "plain": "a"},
                                                              {"file": "src/client.js", "plain": "b"}]}), g, root, index)
    assert out["journeys"][0]["steps"][1]["linked"] is False and out["verification"]["unlinked_steps"] == 1


@pytest.mark.parametrize("journeys, needle", [
    ("x", "journeys: must be a list"),
    ([{"steps": [{"file": "a", "plain": "p"}, {"file": "b", "plain": "q"}]}], "title"),
    ([{"title": "t", "steps": [{"file": "a", "plain": "p"}]}], "at least 2 steps"),
    ([{"title": "t", "steps": [{"file": "a"}, {"file": "b", "plain": "q"}]}], "plain"),
    ([{"title": "t", "steps": [{"file": "a", "plain": "p", "function": "f"}, {"file": "b", "plain": "q"}]}], "line"),
])
def test_validate_lists_journey_problems(journeys, needle):
    d = doc()
    d["journeys"] = journeys
    with pytest.raises(explain.ExplainError) as exc:
        explain.validate(d)
    assert any(needle in p for p in exc.value.problems), exc.value.problems


def test_merge_keeps_journeys_once_and_summary_counts_them(project):
    root, g, index = project
    j = {"title": "你点「发送」时", "steps": [{"file": "src/main.js", "plain": "a"}, {"file": "src/client.js", "plain": "b"}]}
    merged = explain.merge([journey_doc(j), journey_doc(dict(j))])
    assert [x["title"] for x in merged["journeys"]] == ["你点「发送」时"]
    text = "\n".join(explain.summary_lines(explain.verify(merged, g, root, index)))
    assert "Journeys: 1 kept, 0 rejected" in text


def test_a_step_links_to_the_earlier_step_that_calls_it(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "hub.js").write_text('import "./a";\nimport "./b";\n', encoding="utf-8")
    (tmp_path / "src" / "a.js").write_text("export const a = 1;\n", encoding="utf-8")
    (tmp_path / "src" / "b.js").write_text("export const b = 1;\n", encoding="utf-8")
    (tmp_path / "src" / "lone.js").write_text("export const z = 1;\n", encoding="utf-8")
    g = graph.build(tmp_path, [], {"findings": []})
    d = {"evidence": {}, "files": {}, "journeys": [{"title": "t", "steps": [
        {"file": "src/hub.js", "plain": "the page calls a"}, {"file": "src/a.js", "plain": "a works"},
        {"file": "src/b.js", "plain": "then the page calls b"}, {"file": "src/hub.js", "plain": "back on the page"},
        {"file": "src/lone.js", "plain": "something nothing imports"}]}]}
    steps = explain.verify(d, g, tmp_path, {})["journeys"][0]["steps"]
    assert [(s.get("linked"), s.get("from")) for s in steps] == [
        (None, None), (True, 0), (True, 0), (True, 2), (False, None)]


TS = '''export const GET = async (req: Request): Promise<Response> => {
  return new Response("ok");
};
const Foo: React.FC<Props> = ({ a }) => {
  return a;
};
export class Store {
  private async load(): Promise<void> {
  }
  public save(x: number) {
  }
  handle = () => {
  };
  private refresh = async (id: string): Promise<void> => {
  };
  update(
    id: string,
    value: number,
  ): void {
  }
}
const run = useCallback(() => {}, []);
const sum = (a: number, b: number): number => a + b;
doThing(1);
if (ready) {
}
'''


def test_typescript_definitions_are_recognised():
    defs = explain.find_definitions(TS, "js")
    for name, line in (("GET", 1), ("Foo", 4), ("Store", 7), ("load", 8), ("save", 10), ("handle", 12),
                       ("refresh", 14), ("update", 16), ("run", 22), ("sum", 23)):
        assert defs.get(name) == [line], (name, defs.get(name))
    assert "doThing" not in defs and "if" not in defs


TSX_TYPED = '''export const Plane: React.FC<{
  depth?: number;
  drift?: (t: number) => number;
}> = ({depth = 0}) => {
  return null;
};
export const Caret: React.FC<{color?: string; h?: number}> =
  ({color, h = 26}) => null;
export const projectPose = (
  pose: Pose, cam: Pose,
): {x: number; y: number; behind: boolean} => {
  return {x: 0, y: 0, behind: false};
};
export const emphBoxes = (lay: KLayout | null, ai = 0): {line: number; left: number;
  bottom: number}[] => [];
const handler: (e: Event) => void = (e) => {};
export const Wrapped: React.FC<Props> = React.memo(Inner);
const LIMITS: Record<string, number> = {a: 1};
const total: number = compute(a, b);
const picked = (a > b) ? a : b;
const cb: Callback = makeCallback((x) => x);
'''


def test_typed_consts_and_multiline_arrows_are_definitions():
    defs = explain.find_definitions(TSX_TYPED, "js")
    for name, line in (("Plane", 1), ("Caret", 7), ("projectPose", 9), ("emphBoxes", 14),
                       ("handler", 16), ("Wrapped", 17)):
        assert defs.get(name) == [line], (name, defs.get(name))
    for name in ("LIMITS", "total", "picked", "cb"):
        assert name not in defs, (name, defs.get(name))
