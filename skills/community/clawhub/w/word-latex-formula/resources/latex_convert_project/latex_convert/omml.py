from __future__ import annotations

from lxml import etree

from .math_parser import Delim, Frac, Node, Script, Seq, Text


M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"


def m_tag(name: str) -> str:
    return f"{{{M_NS}}}{name}"


def w_tag(name: str) -> str:
    return f"{{{W_NS}}}{name}"


def node_to_omath(node: Node) -> etree._Element:
    omath = etree.Element(m_tag("oMath"))
    append_node(omath, node)
    return omath


def append_node(parent: etree._Element, node: Node) -> None:
    if isinstance(node, Seq):
        for item in node.items:
            append_node(parent, item)
        return
    if isinstance(node, Text):
        _append_math_text(parent, node.value)
        return
    if isinstance(node, Frac):
        f = etree.SubElement(parent, m_tag("f"))
        fpr = etree.SubElement(f, m_tag("fPr"))
        ftype = etree.SubElement(fpr, m_tag("type"))
        ftype.set(m_tag("val"), "bar")
        num = etree.SubElement(f, m_tag("num"))
        append_node(num, node.num)
        den = etree.SubElement(f, m_tag("den"))
        append_node(den, node.den)
        return
    if isinstance(node, Script):
        tag = "sSubSup" if node.sub is not None and node.sup is not None else "sSub" if node.sub is not None else "sSup"
        elem = etree.SubElement(parent, m_tag(tag))
        base = etree.SubElement(elem, m_tag("e"))
        append_node(base, node.base)
        if node.sub is not None:
            sub = etree.SubElement(elem, m_tag("sub"))
            append_node(sub, node.sub)
        if node.sup is not None:
            sup = etree.SubElement(elem, m_tag("sup"))
            append_node(sup, node.sup)
        return
    if isinstance(node, Delim):
        d = etree.SubElement(parent, m_tag("d"))
        dpr = etree.SubElement(d, m_tag("dPr"))
        beg = etree.SubElement(dpr, m_tag("begChr"))
        beg.set(m_tag("val"), node.begin)
        end = etree.SubElement(dpr, m_tag("endChr"))
        end.set(m_tag("val"), node.end)
        e = etree.SubElement(d, m_tag("e"))
        append_node(e, node.body)
        return
    raise TypeError(f"Unsupported math node: {node!r}")


def _append_math_text(parent: etree._Element, value: str) -> None:
    if not value:
        return
    r = etree.SubElement(parent, m_tag("r"))
    t = etree.SubElement(r, m_tag("t"))
    if value[:1].isspace() or value[-1:].isspace():
        t.set(f"{{{XML_NS}}}space", "preserve")
    t.text = value
