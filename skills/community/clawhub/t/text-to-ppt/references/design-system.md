# Design System — Quick Reference

## CDNs (already in shell)
- Tailwind CSS, Chart.js + DataLabels, Font Awesome 6 Free

## Default Theme Colors
```
bg: #0f172a  paper: #1e293b  paperHover: #334155
textPrimary: #f8fafc  textSecondary: #cbd5e1  textMuted: #64748b
primary: #3b82f6  primaryBg: #1e40af  accent: #f59e0b  accentBg: #d97706
success: #22c55e  warning: #f59e0b  error: #ef4444
border: #334155  borderLight: #475569
```

## Typography
- DO NOT use font-sans/font-serif on individual elements (body inherits)
- Use font-bold/font-extrabold for headings only
- font-mono OK for code/data labels

## Layout Rules
- 16:9 viewport, NO scrollbars
- Compact: gap-3/4, p-4 for cards
- All content MUST fit in one viewport

## Visual Rules
- Numbers/stats → MUST visualize (Chart.js or stat cards), never plain bullets
- Lists → Use numbered badges: `<div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold shadow-md">N</div>`
- Icons → Font Awesome 6: `<i class="fa-solid fa-rocket text-4xl text-amber-500"></i>`
- DO NOT use: Material Symbols, base64 images, font-sans on elements

## Slide Output Format
Generate ONLY: `<div class="slide" style="background-color: #0f172a;">...</div>`
No html/head/body — those come from the shell template.

## Chart.js Template
```html
<div class="relative w-full h-64">
    <canvas id="chart-s{N}-{R}"></canvas>
</div>
<script>
(function(){
    if(typeof Chart==='undefined') return;
    var c=document.getElementById('chart-s{N}-{R}');
    if(!c) return;
    if(typeof ChartDataLabels!=='undefined') Chart.register(ChartDataLabels);
    new Chart(c,{type:'bar',data:{labels:[],datasets:[{data:[],backgroundColor:'#3b82f6'}]},options:{maintainAspectRatio:false,responsive:true,plugins:{legend:{labels:{color:'#cbd5e1'},position:'bottom'},datalabels:{display:true,color:'#f8fafc',font:{weight:'bold',size:11},anchor:'end',align:'top',offset:4}},scales:{y:{ticks:{color:'#64748b'},grid:{color:'#334155'}},x:{ticks:{color:'#64748b'},grid:{display:false}}}}});
})();
</script>
```
CRITICAL: Use unique canvas IDs. Use IIFE wrapper to avoid scope issues.

## Component Snippets

### Stat Card
```html
<div class="bg-slate-800 rounded-xl p-4 border border-slate-700">
    <p class="text-slate-500 text-xs uppercase tracking-wide">Label</p>
    <p class="text-3xl font-extrabold text-blue-500">1.2M</p>
    <p class="text-green-500 text-xs mt-1"><i class="fa-solid fa-arrow-up"></i> 24%</p>
</div>
```

### Numbered Badge + Text
```html
<div class="flex items-start gap-3">
    <div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold shadow-md flex-shrink-0">1</div>
    <div><h3 class="font-bold text-slate-50">Title</h3><p class="text-slate-300 text-sm">Desc</p></div>
</div>
```

### Icon Card
```html
<div class="bg-slate-800 rounded-xl p-4 border border-slate-700 text-center">
    <i class="fa-solid fa-rocket text-3xl text-amber-500 mb-2"></i>
    <h3 class="font-bold text-slate-50 text-sm">Title</h3>
    <p class="text-slate-400 text-xs mt-1">Desc</p>
</div>
```

### Timeline Step
```html
<div class="text-center">
    <div class="w-10 h-10 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold mx-auto mb-2">1</div>
    <p class="text-slate-50 font-semibold text-sm">Step</p>
    <p class="text-slate-500 text-xs">Desc</p>
</div>
```

### Layout Patterns
```
Two-col:  <div class="grid grid-cols-2 gap-6 w-full">
Three-col: <div class="grid grid-cols-3 gap-4 w-full">
Split 3:2: <div class="grid grid-cols-5 gap-6 w-full"><div class="col-span-3">..</div><div class="col-span-2">..</div></div>
Cards row: <div class="grid grid-cols-4 gap-4 w-full">
Timeline:  <div class="flex items-center justify-between w-full"> [steps with <div class="flex-1 h-0.5 bg-slate-700 mx-2"></div> between]
```
