from __future__ import annotations

from .math_parser import Delim, Frac, Node, Script, Seq, Text, parse_formula


GREEK_TO_LATEX = {
    "α": r"\alpha",
    "β": r"\beta",
    "γ": r"\gamma",
    "δ": r"\delta",
    "ε": r"\epsilon",
    "ζ": r"\zeta",
    "η": r"\eta",
    "θ": r"\theta",
    "ϑ": r"\vartheta",
    "κ": r"\kappa",
    "λ": r"\lambda",
    "μ": r"\mu",
    "ν": r"\nu",
    "ξ": r"\xi",
    "π": r"\pi",
    "ρ": r"\rho",
    "σ": r"\sigma",
    "τ": r"\tau",
    "φ": r"\phi",
    "χ": r"\chi",
    "ψ": r"\psi",
    "ω": r"\omega",
    "Γ": r"\Gamma",
    "Δ": r"\Delta",
    "Θ": r"\Theta",
    "Λ": r"\Lambda",
    "Ξ": r"\Xi",
    "Π": r"\Pi",
    "Σ": r"\Sigma",
    "Φ": r"\Phi",
    "Ψ": r"\Psi",
    "Ω": r"\Omega",
    "ℓ": r"\ell",
    "ℛ": r"\mathcal{R}",
    "𝓡": r"\mathcal{R}",
}

SYMBOL_TO_LATEX = {
    "≤": r"\le",
    "≥": r"\ge",
    "≈": r"\approx",
    "∈": r"\in",
    "∞": r"\infty",
    "∂": r"\partial",
    "∑": r"\sum",
    "∏": r"\prod",
    "±": r"\pm",
    "×": r"\times",
    "·": r"\cdot",
    "−": "-",
}


def formula_to_latex(text: str) -> str:
    """Best-effort LaTeX preview for the Web UI; Word output still uses OMML."""
    try:
        return node_to_latex(parse_formula(text))
    except Exception:
        return escape_latex_text(text)


def node_to_latex(node: Node) -> str:
    if isinstance(node, Seq):
        return "".join(node_to_latex(item) for item in node.items)
    if isinstance(node, Text):
        return escape_latex_text(node.value)
    if isinstance(node, Frac):
        return r"\frac{" + node_to_latex(node.num) + "}{" + node_to_latex(node.den) + "}"
    if isinstance(node, Script):
        base = _wrap_script_base(node.base)
        suffix = ""
        if node.sub is not None:
            suffix += "_{" + node_to_latex(node.sub) + "}"
        if node.sup is not None:
            suffix += "^{" + node_to_latex(node.sup) + "}"
        return base + suffix
    if isinstance(node, Delim):
        return node.begin + node_to_latex(node.body) + node.end
    return ""


def escape_latex_text(value: str) -> str:
    out: list[str] = []
    for index, ch in enumerate(value):
        if ch in GREEK_TO_LATEX:
            command = GREEK_TO_LATEX[ch]
            out.append(command)
            if _needs_command_separator(command, value[index + 1 : index + 2]):
                out.append(" ")
        elif ch in SYMBOL_TO_LATEX:
            out.append(SYMBOL_TO_LATEX[ch])
        elif ch == "\\":
            out.append(r"\backslash ")
        elif ch in {"&", "%", "$", "#"}:
            out.append("\\" + ch)
        else:
            out.append(ch)
    return "".join(out)


def _needs_command_separator(command: str, next_char: str) -> bool:
    return bool(next_char and next_char.isalpha() and command.startswith("\\") and command[-1].isalpha())


def _wrap_script_base(node: Node) -> str:
    if isinstance(node, Text):
        return node_to_latex(node)
    return "{" + node_to_latex(node) + "}"
