#!/usr/bin/env sh
# repoviz build_html.sh -- compile diagram URLs + notes + source evidence into a
# standalone HTML report.
# Usage: sh scripts/build_html.sh "<title>" "<output.html>" '<json>'
#   json = [{"title":"...","url":"https://x-cmd.com/draw/...","note":"...","ev":"node|file|symbol|lines|level;..."}, ...]
#   ev is optional per diagram: ";"-separated rows, "|"-separated
#   node|file|symbol|lines|level (level = verified|inferred|unknown). Renders a
#   filterable Source-evidence table under the diagram.
# Value restrictions: no double quotes, no "}", no tabs/newlines inside values.
# Security: every JSON-derived value is HTML-escaped (esc) before output; `url` is
# restricted to draw render URLs (https?://.../draw...), so the generated page can
# only load images from the renderer, never arbitrary tracking origins. The page's
# own JS makes no network requests; its <img> elements fetch the supplied draw URLs
# when viewed -- the same exposure as embedding an image in any web page (see the
# confidentiality rule in SKILL.md).
set -u

PROG=${0##*/}

die() { printf '%s: %s\n' "$PROG" "$*" >&2; exit 1; }

[ $# -eq 3 ] || die "usage: sh $PROG \"<title>\" \"<output.html>\" '<json array of {title,url,note,ev}>'"

doc_title=$1
out=$2
json=$3

case $out in
  *.html) ;;
  *) die "output must end in .html: $out" ;;
esac

dir=${out%/*}
[ "$dir" = "$out" ] && dir=.
[ -d "$dir" ] || mkdir -p "$dir" || die "cannot create directory: $dir"

# Phase 1 -- parse the JSON array into TSV rows: title \t url \t note \t evidence
# Renderer allowlist: only https://x-cmd.com / https://www.x-cmd.com draw URLs --
# any other host is dropped (HTML escaping cannot constrain network requests).
items=$(printf '%s' "$json" | awk '
  BEGIN { RS = "}" }
  function field(rec, key,   re, s) {
    re = "\"" key "\"[ \\t]*:[ \\t]*\"[^\"]*\""
    if (match(rec, re)) {
      s = substr(rec, RSTART, RLENGTH)
      sub("^\".*\"[ \\t]*:[ \\t]*\"", "", s)
      sub("\"$", "", s)
      return s
    }
    return ""
  }
  {
    t = field($0, "title"); u = field($0, "url"); n = field($0, "note"); v = field($0, "ev")
    if (u ~ /^https:\/\/(www\.)?x-cmd\.com\/draw([\/?]|$)/) printf "%s\t%s\t%s\t%s\n", t, u, n, v
  }
')

[ -n "$items" ] || die "no usable {\"title\",\"url\"} entries -- url must be an x-cmd.com draw render URL (https://x-cmd.com/draw...); example: [{\"title\":\"Architecture\",\"url\":\"https://x-cmd.com/draw/archmap?n=a;fe;A&n=b;be;B&e=a;b\",\"note\":\"2 tiers\"}]"

# Phase 2 -- render the standalone report
printf '%s\n' "$items" | awk -F '\t' -v doc="$doc_title" -v docfile="$out" '
  function esc(s)   { gsub(/&/, "\\&amp;", s); gsub(/</, "\\&lt;", s); gsub(/>/, "\\&gt;", s); gsub(/"/, "\\&quot;", s); return s }
  function explore(u) {
    if (u ~ /\/draw\/explore/) return u
    if (u ~ /\/draw\/c\//) return u            # short link: no known editor form -- keep as-is
    sub(/\/draw\//, "/draw/explore/", u)
    sub(/\/draw\?/, "/draw/explore?", u)
    return u
  }
  {
    n++
    T[n] = $1; U[n] = $2; N[n] = $3; V[n] = $4
  }
  END {
    print "<!doctype html>"
    print "<html lang=\"en\">"
    print "<head>"
    print "<meta charset=\"utf-8\">"
    print "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
    print "<meta name=\"generator\" content=\"repoviz\">"
    print "<title>" esc(doc) "</title>"
    print "<style>"
    print ":root{--bg:#f6f7f9;--panel:#ffffff;--ink:#1b1f27;--muted:#5b6472;--line:#e2e5ea;--accent:#2563eb;--chip:#eef2ff;color-scheme:light}"
    print "@media (prefers-color-scheme: dark){:root{--bg:#0b0d12;--panel:#12151d;--ink:#e8ebf1;--muted:#9aa4b2;--line:#232838;--accent:#5b8cff;--chip:#1b2334;color-scheme:dark}}"
    print "*{box-sizing:border-box}"
    print "html{scroll-behavior:smooth}"
    print "body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 -apple-system,BlinkMacSystemFont,\"Segoe UI\",Helvetica,Arial,\"PingFang SC\",\"Microsoft YaHei\",sans-serif;-webkit-font-smoothing:antialiased}"
    print ".layout{display:grid;grid-template-columns:264px 1fr;min-height:100vh}"
    print "aside{position:sticky;top:0;height:100vh;overflow:auto;border-right:1px solid var(--line);background:var(--panel);padding:22px 16px;display:flex;flex-direction:column;gap:4px}"
    print ".brand{font-weight:650;font-size:15px;padding:2px 10px 14px;border-bottom:1px solid var(--line);margin-bottom:10px}"
    print ".brand small{display:block;font-weight:400;color:var(--muted);font-size:12px;margin-top:3px}"
    print "nav button{display:block;width:100%;text-align:left;border:0;background:none;color:var(--muted);font:inherit;font-size:13.5px;padding:8px 10px;border-radius:8px;cursor:pointer;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}"
    print "nav button:hover{background:var(--chip);color:var(--ink)}"
    print "nav button.active{background:var(--chip);color:var(--accent);font-weight:600}"
    print ".foot{margin-top:auto;padding:14px 10px 2px;font-size:11.5px;color:var(--muted)}"
    print "main{min-width:0;padding:34px clamp(18px,4vw,56px) 80px}"
    print "header.doc{margin:0 0 26px}"
    print "header.doc h1{font-size:clamp(22px,3vw,30px);letter-spacing:-.01em;margin:0 0 6px}"
    print "header.doc p{margin:0;color:var(--muted);font-size:13.5px}"
    print "section{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:22px clamp(14px,2.4vw,28px) 26px;margin:0 0 26px;scroll-margin-top:24px}"
    print "section h2{font-size:17.5px;margin:0 0 4px;letter-spacing:-.01em}"
    print ".num{display:inline-block;min-width:26px;height:26px;line-height:26px;text-align:center;border-radius:8px;background:var(--chip);color:var(--accent);font-size:12.5px;font-weight:650;margin-right:9px;vertical-align:2px}"
    print ".toolbar{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 14px}"
    print ".toolbar button,.toolbar a{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:8px;padding:6px 12px;font:inherit;font-size:12.5px;cursor:pointer;text-decoration:none;line-height:1.4}"
    print ".toolbar button:hover,.toolbar a:hover{border-color:var(--accent);color:var(--accent)}"
    print "figure{margin:0}"
    print ".stage{overflow:auto;border:1px solid var(--line);border-radius:10px;background:var(--bg);padding:14px;max-height:78vh}"
    print ".stage .spacer{display:inline-block;min-width:100%}"
    print ".stage img{display:block;max-width:100%;height:auto;transform-origin:0 0;transition:transform .15s ease;margin:0 auto}"
    print "figcaption{color:var(--muted);font-size:13px;margin-top:12px}"
    print "figcaption p{margin:6px 0 0}"
    print "@media (max-width:860px){.layout{grid-template-columns:1fr}aside{position:static;height:auto;flex-direction:row;flex-wrap:wrap;align-items:center;border-right:0;border-bottom:1px solid var(--line)}.brand{width:100%;border:0;margin:0 0 6px;padding:0 10px 8px}.foot{display:none}nav{display:flex;gap:4px;overflow-x:auto;width:100%}nav button{white-space:nowrap;width:auto;flex:none}main{padding-top:22px}}"
    print "details.ev{margin-top:16px;font-size:13px}"
    print "details.ev summary{cursor:pointer;color:var(--muted)}"
    print ".evf{margin:10px 0;width:100%;max-width:300px;padding:5px 9px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink);font:inherit;font-size:12.5px}"
    print "table.ev{width:100%;border-collapse:collapse;font-size:12.5px}"
    print "table.ev th,table.ev td{text-align:left;padding:5px 8px;border-bottom:1px solid var(--line);vertical-align:top}"
    print "table.ev code{background:var(--chip);border-radius:5px;padding:1px 6px;font-size:12px;word-break:break-all}"
    print ".lv{display:inline-block;border-radius:6px;padding:0 7px;font-size:11.5px;font-weight:600}"
    print ".lv.verified{background:#dcfce7;color:#15803d}"
    print ".lv.inferred{background:#fef3c7;color:#b45309}"
    print ".lv.unknown{background:#fee2e2;color:#b91c1c}"
    print "@media print{:root{--bg:#fff;--panel:#fff;--ink:#000;--muted:#444;--line:#bbb}aside,.toolbar,.foot,header.doc p,details.ev summary,.evf{display:none!important}.layout{display:block}main{padding:0}section{border:0;border-bottom:1px solid var(--line);border-radius:0;break-inside:avoid;margin:0;padding:12px 0}.stage{overflow:visible;max-height:none;background:#fff}body{font-size:12px}}"
    print "</style>"
    print "</head>"
    print "<body>"
    print "<div class=\"layout\">"
    print "<aside>"
    print "<div class=\"brand\">" esc(doc) "<small>" n " diagram" (n == 1 ? "" : "s") " &middot; repoviz report</small></div>"
    print "<nav id=\"nav\">"
    for (i = 1; i <= n; i++) printf "<button data-target=\"sec-%d\" type=\"button\">%d. %s</button>\n", i, i, esc(T[i])
    print "</nav>"
    print "<div class=\"foot\">Generated by repoviz &middot; diagrams render live from x-cmd draw URLs</div>"
    print "</aside>"
    print "<main>"
    print "<header class=\"doc\"><h1>" esc(doc) "</h1><p>" n " diagram" (n == 1 ? "" : "s") " &middot; dark/light follows your system &middot; use the toolbar to zoom, fullscreen, or copy the Markdown embed &middot; prints cleanly to PDF</p></header>"
    for (i = 1; i <= n; i++) {
      md = "![" T[i] "](" U[i] ")"
      printf "<section id=\"sec-%d\">\n", i
      printf "<h2><span class=\"num\">%d</span>%s</h2>\n", i, esc(T[i])
      print "<div class=\"toolbar\">"
      printf "<button type=\"button\" onclick=\"zv(this,-0.25)\" aria-label=\"Zoom out\">&minus; Zoom out</button>"
      printf "<button type=\"button\" onclick=\"zv(this,0.25)\" aria-label=\"Zoom in\">+ Zoom in</button>"
      printf "<button type=\"button\" onclick=\"rz(this)\" aria-label=\"Reset zoom\">Reset</button>"
      printf "<button type=\"button\" data-md=\"%s\" onclick=\"cp(this)\" aria-label=\"Copy Markdown embed\">Copy Markdown</button>", esc(md)
      printf "<a href=\"%s\" target=\"_blank\" rel=\"noopener\">Open live diagram</a>", esc(U[i])
      printf "<a href=\"%s\" target=\"_blank\" rel=\"noopener\">Open in editor</a>", esc(explore(U[i]))
      print "</div>"
      printf "<figure data-scale=\"1\"><div class=\"stage\"><span class=\"spacer\"><img src=\"%s\" alt=\"%s\" loading=\"lazy\"></span></div></figure>\n", esc(U[i]), esc(T[i])
      if (N[i] != "") printf "<figcaption><p>%s</p></figcaption>\n", esc(N[i])
      if (V[i] != "") {
        cnt = split(V[i], er, ";")
        printf "<details class=\"ev\"><summary>Source evidence (%d)</summary>\n", cnt
        printf "<input class=\"evf\" type=\"search\" placeholder=\"Filter nodes...\" oninput=\"evf(this,%d)\">\n", i
        printf "<table class=\"ev\"><thead><tr><th>Node</th><th>Level</th><th>File</th><th>Symbol</th><th>Lines</th></tr></thead><tbody id=\"evb-%d\">\n", i
        for (j = 1; j <= cnt; j++) {
          m = split(er[j], c, "|")
          lv = (m >= 5) ? c[5] : "unknown"
          if (lv != "verified" && lv != "inferred" && lv != "unknown") lv = "unknown"
          printf "<tr><td>%s</td><td><span class=\"lv %s\">%s</span></td><td><code>%s</code></td><td>%s</td><td>%s</td></tr>\n", esc(c[1]), lv, esc(lv), esc(m >= 2 ? c[2] : ""), esc(m >= 3 ? c[3] : ""), esc(m >= 4 ? c[4] : "")
        }
        print "</tbody></table></details>"
      }
      print "</section>"
    }
    print "</main>"
    print "</div>"
    print "<script>"
    print "function figOf(b){return b.closest(\"section\").querySelector(\"figure\")}"
    print "function base(fig){var im=fig.querySelector(\"img\");if(!fig._bw){fig._bw=im.clientWidth||im.naturalWidth||600;fig._bh=im.clientHeight||im.naturalHeight||400}return[fig._bw,fig._bh]}"
    print "function apply(fig){var s=parseFloat(fig.getAttribute(\"data-scale\")),im=fig.querySelector(\"img\"),sp=im.parentElement,b=base(fig);im.style.transform=\"scale(\"+s+\")\";sp.style.width=Math.round(b[0]*s)+\"px\";sp.style.height=Math.round(b[1]*s)+\"px\"}"
    print "function zv(b,d){var f=figOf(b),s=parseFloat(f.getAttribute(\"data-scale\"))+d;if(s<0.3||s>4)return;f.setAttribute(\"data-scale\",s);apply(f)}"
    print "function rz(b){var f=figOf(b);f.setAttribute(\"data-scale\",\"1\");apply(f)}"
    print "function fs(b){var f=figOf(b);if(document.fullscreenElement)document.exitFullscreen();else if(f.requestFullscreen)f.requestFullscreen()}"
    print "function cp(b){var t=b.getAttribute(\"data-md\");if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,legacy)}else legacy();function legacy(){var ta=document.createElement(\"textarea\");ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand(\"copy\")}catch(e){}document.body.removeChild(ta);ok()}function ok(){var o=b.textContent;b.textContent=\"Copied!\";setTimeout(function(){b.textContent=o},1400)}}"
    print "function evf(inp,id){var q=inp.value.toLowerCase(),rs=document.querySelectorAll(\"#evb-\"+id+\" tr\");for(var i=0;i<rs.length;i++){rs[i].style.display=rs[i].textContent.toLowerCase().indexOf(q)>=0?\"\":\"none\"}}"
    print "(function(){var btns=document.querySelectorAll(\"#nav button\");for(var i=0;i<btns.length;i++){(function(btn){btn.addEventListener(\"click\",function(){var el=document.getElementById(btn.getAttribute(\"data-target\"));if(el)el.scrollIntoView({behavior:\"smooth\",block:\"start\"})})})(btns[i])}"
    print "var secs=document.querySelectorAll(\"section\");if(\"IntersectionObserver\"in window){var cur=null;var io=new IntersectionObserver(function(es){for(var j=0;j<es.length;j++){if(es[j].isIntersecting){cur=es[j].target.id;break}}if(cur){for(var k=0;k<btns.length;k++)btns[k].classList.toggle(\"active\",btns[k].getAttribute(\"data-target\")===cur)}},{rootMargin:\"-20% 0px -70% 0px\"});for(var m=0;m<secs.length;m++)io.observe(secs[m])}"
    print "var ims=document.querySelectorAll(\"figure img\");for(var q=0;q<ims.length;q++){ims[q].addEventListener(\"load\",function(){var f=this.closest(\"figure\");f._bw=0;apply(f)})}"
    print "})()"
    print "</script>"
    print "</body>"
    print "</html>"
  }
' > "$out" || die "failed to write $out"

[ -s "$out" ] || die "failed to write $out"
cnt=$(printf '%s\n' "$items" | wc -l | tr -d ' ')
plural=""
[ "$cnt" -eq 1 ] || plural="s"
printf 'saved: %s (%s bytes, %s diagram%s)\n' "$out" "$(wc -c < "$out" | tr -d ' ')" "$cnt" "$plural"
