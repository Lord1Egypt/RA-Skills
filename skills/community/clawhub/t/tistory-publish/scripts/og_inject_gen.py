import json, sys

url = sys.argv[1] if len(sys.argv) > 1 else ''
esc_url = json.dumps(url)
section_title = '\ub9b4\ub9ac\uc988 \ub178\ud2b8'  # 릴리즈 노트

js = (
    "(()=>{"
    "const ed=tinymce.activeEditor,doc=ed.getDoc(),"
    "h2s=Array.from(doc.querySelectorAll('h2')),"
    "h2=h2s.find(h=>h.textContent.trim()===" + json.dumps(section_title) + ");"
    "if(!h2)return 'h2 not found';"
    "let s=h2.nextSibling;"
    "while(s&&(s.nodeType===3||(s.tagName==='P'&&(!s.textContent.trim()||s.textContent.charCodeAt(0)===8203)))){"
    "const n=s.nextSibling;s.parentNode.removeChild(s);s=n;}"
    "const p=doc.createElement('p');"
    "p.setAttribute('data-ke-size','size16');"
    "p.textContent=" + esc_url + ";"
    "h2.parentNode.insertBefore(p,h2.nextSibling);"
    "const r=ed.dom.createRng(),tn=p.firstChild;"
    "r.setStart(tn,tn.length);r.setEnd(tn,tn.length);"
    "ed.selection.setRng(r);ed.focus();"
    "return 'ready';})()"
)

print(js)
