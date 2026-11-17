(function () {
  var root = document.documentElement;
  try {
    var q = new URLSearchParams(location.search);
    if (q.get("theme")) root.setAttribute("data-theme", q.get("theme"));
    if (q.get("view") === "dev") document.body.classList.add("dev");
  } catch (e) {}
  var toggle = document.getElementById("view-toggle");
  if (toggle) toggle.addEventListener("click", function () {
    var on = document.body.classList.toggle("dev");
    toggle.setAttribute("aria-pressed", on ? "true" : "false");
  });
  document.querySelectorAll("[data-filter]").forEach(function (b) {
    b.addEventListener("click", function () {
      var s = b.getAttribute("data-filter");
      document.querySelectorAll("[data-filter]").forEach(function (x) { x.classList.toggle("on", x === b); });
      document.querySelectorAll("tr[data-status]").forEach(function (r) {
        r.hidden = s !== "all" && r.getAttribute("data-status") !== s;
      });
    });
  });
  var PROBLEMS = ["missing", "partial", "changed"];
  document.querySelectorAll("[data-rfilter]").forEach(function (b) {
    b.addEventListener("click", function () {
      var s = b.getAttribute("data-rfilter");
      document.querySelectorAll("[data-rfilter]").forEach(function (x) { x.classList.toggle("on", x === b); });
      document.querySelectorAll(".req-card").forEach(function (c) {
        var st = c.getAttribute("data-rstatus");
        c.hidden = !(s === "all" || st === s || (s === "problems" && PROBLEMS.indexOf(st) >= 0));
      });
      document.querySelectorAll(".req-area").forEach(function (a) {
        a.hidden = !a.querySelector(".req-card:not([hidden])");
      });
    });
  });
  function done(b) { b.textContent = b.getAttribute("data-done"); }
  document.querySelectorAll("button.copy").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = b.getAttribute("data-text");
      var fallback = function () {
        var a = document.createElement("textarea");
        a.value = text; document.body.appendChild(a); a.select();
        try { document.execCommand("copy"); done(b); } catch (e) {}
        a.remove();
      };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { done(b); }, fallback);
      else fallback();
    });
  });
})();
