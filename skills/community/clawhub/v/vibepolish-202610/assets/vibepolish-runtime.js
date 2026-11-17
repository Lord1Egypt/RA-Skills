(function() {
  "use strict";
  try {
    if (typeof document != "undefined") {
      var elementStyle = document.createElement("style");
      elementStyle.appendChild(document.createTextNode(`:root {
  --dt-blue: #1661ab;
  --dt-blue-dark: #0d4683;
  --dt-border: #cfd5df;
  --dt-text: #344054;
  --dt-muted: #667085;
}
*{box-sizing:border-box} body{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;color:#182230;background:#f5f6f8;overflow:hidden}
    .dt-app{height:100vh;position:relative;display:block;overflow:hidden}
    .dt-app[data-panel-open="true"]{display:grid;grid-template-columns:minmax(0,1fr) 384px}
    .dt-stage{position:relative;min-width:0;width:100%;height:100%;background:#fff;padding:0}
    .dt-stage iframe{width:100%;height:100%;border:0;background:#fff;display:block}
    .dt-app[data-panel-open="true"] .dt-stage{background:#d9dde5;padding:12px}
    .dt-app[data-panel-open="true"] .dt-stage iframe{border:1px solid #c8d0dc}
    .dt-stage.dt-viewport-locked{overflow:auto;display:block}
    .dt-stage.dt-viewport-locked iframe{max-width:none;max-height:none;flex:none}
    .dt-frame-shield{position:absolute;z-index:20;background:transparent;cursor:crosshair}
    #dt-panel-root{min-width:0}
    .dt-panel-launcher{position:fixed;right:18px;bottom:18px;z-index:2147483600;height:38px;padding:0 16px;border-color:rgba(17,17,17,.86);background:rgba(17,17,17,.86);color:#fff;box-shadow:0 8px 24px rgba(16,24,40,.22)}
    .dt-panel-launcher:hover{border-color:rgba(0,0,0,.96);background:rgba(0,0,0,.96);color:#fff}
    .dt-side{min-width:0;background:#fff;border-left:1px solid #d9dde5;display:grid;grid-template-rows:auto auto minmax(0,1fr) auto;height:100vh}
    .dt-side-head{padding:12px 14px 10px;border-bottom:1px solid #eaecf0;background:#fff}
    .dt-side-head-main{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:10px}.dt-side-head strong{font-size:15px}.dt-export-actions{display:flex;align-items:center;justify-content:flex-end;gap:7px}.dt-export-actions button{height:30px}.dt-side-status{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:7px;min-height:20px;color:#667085;font-size:11px}.dt-side-status-actions{display:flex;align-items:center;justify-content:flex-end;gap:7px}.dt-backend-alert,.dt-backend-badge{font-size:11px;font-weight:750;line-height:1.35;white-space:nowrap}.dt-backend-alert{color:#b42318}.dt-backend-badge{display:inline-flex;align-items:center;gap:5px;color:#067647}.dt-backend-badge::before{content:"";width:6px;height:6px;border-radius:50%;background:#12b76a}.dt-export-actions .dt-panel-icon-button{width:30px;height:30px;flex:0 0 30px;padding:0;display:inline-flex;align-items:center;justify-content:center;border:0;background:transparent;color:#667085;font-size:16px;line-height:1}.dt-panel-icon-button:hover{background:#eef2f6;color:#0d4683}.dt-panel-icon-button:disabled{background:transparent;color:#c0c7d1;cursor:not-allowed}.dt-panel-icon-button svg{width:16px;height:16px;display:block;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}.dt-prompt-icon{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:14px;font-weight:800;line-height:1}.dt-save-split{position:relative;display:flex;align-items:center}.dt-save-split .dt-tooltip-trigger{display:flex;align-items:center}.dt-save-split .dt-save-main{width:26px;flex-basis:26px}.dt-save-split .dt-save-toggle{width:16px;flex-basis:16px}.dt-save-chevron{width:6px;height:6px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:translateY(-2px) rotate(45deg)}.dt-save-split.dt-open .dt-panel-icon-button{background:#eef2f6;color:#0d4683}.dt-save-menu{position:absolute;right:0;top:34px;z-index:30;width:max-content;min-width:132px;padding:4px;border:1px solid #d0d5dd;border-radius:6px;background:#fff;box-shadow:0 10px 24px rgba(16,24,40,.16)}.dt-save-menu button{display:block;width:100%;height:30px;border:0;border-radius:4px;background:#fff;padding:0 9px;text-align:left;color:#344054;font-size:12px}.dt-save-menu button:hover{background:#eef5fc;color:#0d4683}.dt-save-menu button:disabled{color:#98a2b3;background:#fff;cursor:not-allowed}
    .dt-capture-section{padding:10px 14px 12px;border-bottom:1px solid #d9dde5;background:#fff}.dt-capture-meta{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:7px;font-size:11px;color:#98a2b3}.dt-capture-meta strong{color:#667085;font-size:11px}.dt-capture-controls{display:grid;grid-template-columns:122px minmax(0,1fr);gap:8px}.dt-capture-switch{display:grid;grid-template-columns:1fr 1fr;padding:2px;border:1px solid #cfd5df;border-radius:6px;background:#f4f6f9}.dt-capture-switch button{height:30px;padding:0 6px;border:0;background:transparent;color:#667085}.dt-capture-switch button.dt-active{background:#fff;color:#0d4683;box-shadow:0 1px 3px rgba(16,24,40,.1)}.dt-capture-main{height:34px;background:#1661ab!important;color:#fff!important;border-color:#1661ab!important}.dt-capture-main::before{content:"";display:inline-block;width:11px;height:11px;margin-right:7px;vertical-align:-1px;border:1px solid currentColor;border-radius:50%;background:linear-gradient(currentColor,currentColor) center/1px 15px no-repeat,linear-gradient(90deg,currentColor,currentColor) center/15px 1px no-repeat}.dt-capture-main:disabled{opacity:1;cursor:not-allowed}
    button{height:30px;border:1px solid #cfd5df;background:#fff;color:#344054;border-radius:6px;padding:0 10px;font-size:12px;font-weight:650;cursor:pointer}
    button:hover{background:#f6f8fb} button.dt-active{border-color:#1661ab;background:#e9f1fb;color:#0d4683}.dt-primary{background:#1661ab;color:#fff;border-color:#1661ab}.dt-primary:hover{background:#0d4683;color:#fff;border-color:#0d4683}.dt-primary:disabled,.dt-primary:disabled:hover{background:#d0d5dd;color:#fff;border-color:#d0d5dd;box-shadow:none;cursor:not-allowed}
    .dt-tabs{min-height:0;overflow:hidden;background:#fbfcfe;display:grid;grid-template-rows:auto minmax(0,1fr)}
    .dt-tab-strip{display:flex;gap:4px;overflow-x:auto;padding:10px 12px 0;border-bottom:1px solid #d9dde5;background:#f6f8fb}
    .dt-tab-note{position:relative;min-width:42px;height:34px;border:1px solid #d9dde5;border-bottom:0;border-radius:7px 7px 0 0;background:#eef2f7;color:#667085;font-size:12px;font-weight:750}
    .dt-tab-note.dt-active{height:38px;margin-bottom:-1px;background:#fff;color:#0d4683;border-color:#1661ab;z-index:1}
    .dt-tab-note.dt-draft::after{content:'';position:absolute;right:6px;top:6px;width:5px;height:5px;border-radius:50%;background:#c03030}
    .dt-tab-close{position:absolute;right:3px;top:3px;width:14px;height:14px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#fff;color:#667085;border:1px solid #d0d5dd;font-size:11px;line-height:1;opacity:0;pointer-events:none}
    .dt-tab-note:hover .dt-tab-close,.dt-tab-note:focus-visible .dt-tab-close{opacity:1;pointer-events:auto}.dt-tab-close:hover{background:#fee4e2;color:#b42318;border-color:#fda29b}
    .dt-tab-panel{min-height:0;overflow:auto;overflow-anchor:none;padding:12px;background:#fff}
    .dt-edit-summary-section{margin-top:14px;border:1px solid #d9e0ea;border-radius:6px;background:#fff;overflow:hidden}.dt-edit-summary-head{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:9px 10px;border-bottom:1px solid #eaecf0;background:#fbfcfe}.dt-edit-summary-head h2{color:#344054;font-size:11px;font-weight:750;letter-spacing:0;text-transform:none}.dt-edit-summary-head span{font-size:11px;color:#98a2b3}.dt-edit-summary-list{display:grid}.dt-edit-summary{min-width:0;padding:8px 10px}.dt-edit-summary+.dt-edit-summary{border-top:1px solid #eaecf0}.dt-edit-summary-thumbnail{width:38px;height:38px;padding:0;overflow:hidden;border:1px solid #d0d5dd;border-radius:5px;background:#f7f8fa}.dt-edit-summary-thumbnail img{display:block;width:100%;height:100%;object-fit:cover}.dt-edit-summary-thumbnail:hover{border-color:#1661ab}.dt-edit-summary-context{margin-bottom:6px;font-size:10px;font-weight:650;color:#667085}.dt-edit-summary-changes{display:grid;gap:7px}.dt-edit-summary-change{display:grid;grid-template-columns:62px minmax(0,1fr) 12px minmax(0,1fr) auto;gap:5px;align-items:center;min-width:0;font-size:11px}.dt-edit-summary-change.dt-has-capture{grid-template-columns:38px 62px minmax(0,1fr) 12px minmax(0,1fr) auto;gap:6px}.dt-edit-summary-change>span{color:#667085}.dt-edit-summary-change>b{display:flex;align-items:center;gap:3px;min-width:0;font-weight:500}.dt-edit-summary-change code{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#344054;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:10px}.dt-edit-summary-change>i{color:#98a2b3;font-style:normal;text-align:center}.dt-edit-summary-swatch{width:9px;height:9px;flex:0 0 auto;border:1px solid rgba(16,24,40,.16);border-radius:2px}
    h2{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#667085;margin:0}.dt-section-head{margin:0 0 7px}.dt-section-title{display:flex;align-items:center;justify-content:space-between;gap:8px}.dt-section-title .dt-copy{letter-spacing:0;text-transform:none}.dt-section-subtitle{margin-top:3px;font-size:11px;font-weight:650;color:#9a3412;line-height:1.35}
	    p,#dt-empty{font-size:12px;color:#667085;line-height:1.45;margin:0 0 8px}.dt-kv{display:grid;grid-template-columns:58px minmax(0,1fr) auto;gap:8px;font-size:12px;margin:7px 0;align-items:start;min-height:30px}.dt-kv span{color:#667085;margin-top:7px}.dt-kv b{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-top:7px}.dt-kv code{min-width:0;white-space:normal;overflow-wrap:anywhere;word-break:break-all;line-height:1.45;color:#344054;margin-top:6px}.dt-kv .dt-copy{margin-top:4px}
	    .dt-copy{height:22px;padding:0 7px;border-radius:5px;font-size:11px;font-weight:650;color:#0d4683;background:#eef5fc;border-color:#c6d7eb}
	    .dt-stepper{display:grid;grid-template-columns:58px 30px minmax(0,1fr) 30px;gap:6px;align-items:center;margin:7px 0;font-size:12px}.dt-stepper span{color:#667085}.dt-stepper b{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#344054}.dt-stepper button{height:26px;padding:0;border-radius:5px}
	    .dt-breadth-loading{display:inline-flex;min-width:90px;color:#667085!important;font-weight:650}.dt-loading-dot-two{animation:dt-loading-dot-two 1.05s steps(1,end) infinite}.dt-loading-dot-three{animation:dt-loading-dot-three 1.05s steps(1,end) infinite}@keyframes dt-loading-dot-two{0%,32%{opacity:0}33%,100%{opacity:1}}@keyframes dt-loading-dot-three{0%,65%{opacity:0}66%,100%{opacity:1}}
	    .dt-seg,.dt-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0}.dt-seg button.dt-active{border-color:#1661ab;background:#e9f1fb;color:#0d4683}
	    .dt-control{display:grid;grid-template-columns:72px minmax(0,1fr);align-items:start;gap:8px;margin:9px 0;min-height:30px}.dt-control>span{font-size:12px;font-weight:650;color:#344054;margin-top:7px}
	    .dt-check-row{display:flex;align-items:center;gap:7px;margin:8px 0 2px;font-size:12px;color:#475467;line-height:1.4}.dt-check-row input{width:14px;height:14px;accent-color:#1661ab}.dt-check-row:has(input:disabled){color:#98a2b3}
    .dt-control-label{display:inline-flex;align-items:center;gap:4px;min-width:0;white-space:nowrap}.dt-control-failure{display:inline-flex;align-items:center;justify-content:center;width:12px;height:12px;border-radius:50%;background:#d92d20;color:#fff;font-style:normal;font-size:9px;font-weight:800;line-height:1;cursor:help;flex:0 0 auto}
    .dt-tooltip-trigger{display:inline-flex;align-items:center}.dt-tooltip-popup{--dt-tooltip-bg:#1f1f1f;position:fixed;z-index:2147483647;width:max-content;max-width:min(260px,calc(100vw - 16px));padding:6px 8px;border-radius:6px;background:var(--dt-tooltip-bg);color:#fff;font-size:12px;font-weight:400;line-height:1.45;letter-spacing:0;white-space:pre-line;pointer-events:none;transform:translate(-50%,-100%);box-shadow:0 3px 10px rgba(0,0,0,.2)}.dt-tooltip-popup::after{content:"";position:absolute;left:var(--dt-tooltip-arrow-left,50%);bottom:-5px;width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-top:5px solid var(--dt-tooltip-bg);transform:translateX(-50%)}.dt-tooltip-popup[data-placement="bottom"]{transform:translate(-50%,0)}.dt-tooltip-popup[data-placement="bottom"]::after{top:-5px;bottom:auto;border-top:0;border-bottom:5px solid var(--dt-tooltip-bg)}
	    .dt-density-label{display:grid;grid-template-columns:minmax(0,1fr) 18px;align-items:center;gap:4px}.dt-density-label .dt-control-label{margin-top:0}.dt-density-toggle{width:18px;height:18px;padding:0;border:0;background:transparent;color:#667085;display:flex;align-items:center;justify-content:center}.dt-density-toggle:hover{background:#eef5fc;color:#0d4683}.dt-density-toggle svg{width:13px;height:13px;transition:transform .15s}.dt-density-toggle.dt-open svg{transform:rotate(90deg)}
	    .dt-control.dt-disabled{min-height:24px}.dt-control.dt-disabled>span{color:#98a2b3;text-decoration:line-through}.dt-control-disabled-reason{font-size:11px;color:#98a2b3;line-height:1.45;margin-top:5px}
	    .dt-control-group{margin:12px 0 0}.dt-control-group:first-of-type{margin-top:0}.dt-control-group-title{font-size:11px;font-weight:750;color:#98a2b3;line-height:1;margin:0 0 6px}
	    .dt-edit-loading{height:72px;display:flex;align-items:center;justify-content:center}.dt-write-spinner{width:24px;height:24px;border-radius:50%;background:conic-gradient(#1661ab 0 92deg,rgba(22,97,171,.13) 92deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 4px),#000 calc(100% - 3px));mask:radial-gradient(farthest-side,transparent calc(100% - 4px),#000 calc(100% - 3px));animation:dt-write-spin .72s linear infinite}@keyframes dt-write-spin{to{transform:rotate(360deg)}}
	    input,textarea,select{width:100%;min-width:0;border:1px solid #cfd5df;border-radius:6px;padding:7px 8px;font:inherit;font-size:12px;background:#fff;color:#344054}input.dt-default-value{color:#98a2b3}select{appearance:none;-webkit-appearance:none;padding-right:36px;text-overflow:ellipsis;white-space:nowrap;background-image:linear-gradient(45deg,transparent 50%,#667085 50%),linear-gradient(135deg,#667085 50%,transparent 50%);background-position:calc(100% - 17px) 50%,calc(100% - 12px) 50%;background-size:5px 5px,5px 5px;background-repeat:no-repeat}textarea{min-height:30px;resize:none;overflow:hidden;line-height:1.45}.dt-text-input{max-height:64px}.dt-text-input:disabled{background:#f8fafc;color:#98a2b3;cursor:not-allowed}
	    .dt-color-field{display:grid;grid-template-columns:38px minmax(0,1fr) 28px;gap:6px;align-items:center}.dt-swatch{height:28px;border-radius:6px;padding:0;background:var(--swatch,#fff);box-shadow:inset 0 0 0 1px rgba(16,24,40,.14)}
	    .dt-swatch:hover{background:var(--swatch,#fff)!important;box-shadow:inset 0 0 0 1px rgba(16,24,40,.24),0 0 0 2px rgba(22,97,171,.14)}
	    .dt-color-field input{height:28px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace}.dt-color-field input.dt-default-value{color:#98a2b3}.dt-color-copy{height:28px;width:28px;padding:0;display:flex;align-items:center;justify-content:center;color:#667085}.dt-color-copy:hover{color:#0d4683;background:#eef5fc}.dt-color-copy svg{width:14px;height:14px;display:block}
	    .dt-family-field,.dt-unit-field,.dt-weight-field{position:relative;min-width:0}.dt-menu-button{width:100%;height:30px;display:grid;grid-template-columns:minmax(0,1fr) 12px;align-items:center;gap:4px;text-align:left;border:1px solid #cfd5df;background:#fff;color:#344054;border-radius:6px;padding:0 8px;font-size:12px;font-weight:500}.dt-menu-button span{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.dt-menu-button::after{content:"";width:6px;height:6px;border-right:1.5px solid #667085;border-bottom:1.5px solid #667085;transform:translateY(-2px) rotate(45deg);justify-self:end}.dt-menu-panel{position:absolute;left:0;right:0;top:34px;z-index:20;display:none;max-height:180px;overflow:auto;border:1px solid #cfd5df;border-radius:6px;background:#fff;box-shadow:0 10px 24px rgba(16,24,40,.14);padding:4px}.dt-family-field.dt-open .dt-menu-panel,.dt-unit-field.dt-open .dt-menu-panel,.dt-weight-field.dt-open .dt-menu-panel{display:block}.dt-menu-option{width:100%;height:28px;border:0;background:#fff;border-radius:4px;padding:0 8px;text-align:left;font-size:12px;font-weight:500;color:#344054;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.dt-menu-option:hover,.dt-menu-option.dt-active{background:#eef5fc;color:#0d4683}.dt-family-button{grid-template-columns:minmax(0,1fr) 16px;gap:8px;padding-right:11px}.dt-weight-button,.dt-weight-option{font-weight:650}
	    .dt-font-field{display:grid;grid-template-columns:minmax(80px,1fr) minmax(58px,72px) 58px 48px;gap:6px;align-items:center}
	    .dt-color-popover{position:fixed;display:none;z-index:2147483647;border:1px solid #d0d5dd;border-radius:8px;background:#fff;box-shadow:0 14px 38px rgba(16,24,40,.16);padding:8px;width:184px}
	    .dt-color-popover.dt-open{display:block}.dt-iro-mount{display:flex;justify-content:center;min-height:138px}.dt-color-actions{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px}.dt-color-actions button,.dt-color-format button{height:28px;font-size:11px;padding:0 8px}.dt-color-action-transparent{background:linear-gradient(45deg,#f2f4f7 25%,transparent 25% 75%,#f2f4f7 75%),linear-gradient(45deg,#f2f4f7 25%,#fff 25% 75%,#f2f4f7 75%);background-position:0 0,4px 4px;background-size:8px 8px;color:#344054}.dt-color-divider{height:1px;background:#eaecf0;margin:8px 0}.dt-color-format{display:grid;grid-template-columns:1fr 1fr;gap:4px}.dt-color-format button.dt-active,.dt-color-actions button.dt-active{border-color:#1661ab;color:#0d4683;box-shadow:0 0 0 2px rgba(22,97,171,.12)}
	    .dt-range-field{display:grid;grid-template-columns:minmax(106px,1fr) minmax(70px,88px) 54px;gap:6px;align-items:center}.dt-range-wrap{position:relative;display:flex;align-items:center}
	    .dt-unit-static{height:30px;border:1px solid #cfd5df;border-radius:6px;background:#f8fafc;color:#667085;font-size:12px;display:flex;align-items:center;padding:0 7px}
	    .dt-box-model{margin:2px 0}.dt-box-diagram{height:124px;border:1px solid #d0d7e2;border-radius:6px;background:#fbfcfe;position:relative;color:#667085;font-size:9px;font-weight:650;overflow:hidden}.dt-box-outer{position:absolute;left:44px;right:44px;top:29px;bottom:17px;border:1.5px solid #9db7d5;border-radius:4px;background:#edf5ff}.dt-box-inner{position:absolute;left:58px;right:58px;top:29px;bottom:29px;border:1px dashed #98a2b3;border-radius:3px;background:#fff;z-index:1}.dt-box-label{position:absolute;white-space:nowrap;z-index:2}.dt-box-label b,.dt-box-measure b{font-weight:750;color:#344054}.dt-box-measure{position:absolute;color:#344054;z-index:3}.dt-box-measure::before{content:"";position:absolute;opacity:.82}.dt-box-measure::after{content:"";position:absolute;opacity:.82}.dt-box-measure span{position:relative;z-index:1;display:block;background:#fbfcfe;padding:0 4px;white-space:nowrap;line-height:1.2}.dt-box-width{left:44px;right:44px;top:9px;height:12px;display:flex;justify-content:center}.dt-box-width::before{left:0;right:0;top:6px;border-top:1px dashed #667085}.dt-box-width::after{left:0;right:0;top:2px;height:9px;background:linear-gradient(#667085,#667085) left center/1px 9px no-repeat,linear-gradient(#667085,#667085) right center/1px 9px no-repeat}.dt-box-height{top:29px;bottom:17px;right:18px;width:9px;display:flex;align-items:center;justify-content:center}.dt-box-height::before{left:4px;top:0;bottom:0;border-left:1px dashed #667085}.dt-box-height::after{left:0;top:0;width:9px;height:100%;background:linear-gradient(#667085,#667085) left top/9px 1px no-repeat,linear-gradient(#667085,#667085) left bottom/9px 1px no-repeat}.dt-box-height span{position:absolute;left:50%;top:50%;width:42px;transform:translate(-50%,-50%);padding:2px;white-space:normal;text-align:center;line-height:1.15}.dt-box-pad-top{top:6px;left:50%;transform:translateX(-50%)}.dt-box-pad-bottom{bottom:6px;left:50%;transform:translateX(-50%)}.dt-box-pad-left{left:5px;top:50%;width:48px;transform:translateY(-50%);line-height:1.1;text-align:center}.dt-box-pad-right{right:5px;top:50%;width:48px;transform:translateY(-50%);line-height:1.1;text-align:center}.dt-box-content{left:50%;top:50%;transform:translate(-50%,-50%);color:#98a2b3}
	    .dt-box-field.dt-disabled label{color:#98a2b3;text-decoration:line-through}.dt-box-field.dt-disabled input,.dt-box-field.dt-disabled .dt-unit-static,.dt-box-field.dt-disabled .dt-menu-button{background:#f8fafc;color:#98a2b3;cursor:not-allowed}
	    .dt-box-grid{display:grid;grid-template-columns:minmax(0,1fr) 1px minmax(0,1fr);gap:7px;align-items:center;margin-top:8px}.dt-box-sep{width:1px;height:26px;background:#d9dde5}.dt-box-field{display:grid;grid-template-columns:26px minmax(0,1fr) 50px;gap:5px;align-items:center}.dt-box-field label{font-size:12px;font-weight:650;color:#344054}.dt-box-field input{height:28px;padding:0 6px}.dt-box-field .dt-unit-static,.dt-box-field .dt-menu-button{height:28px}.dt-box-field .dt-menu-panel{top:32px}
	    .dt-range-wrap::before{content:"";position:absolute;left:0;right:0;top:50%;height:9px;transform:translateY(-50%);border-radius:999px;background:linear-gradient(90deg,rgba(22,97,171,.34) 0 var(--dt-range-progress,0%),transparent var(--dt-range-progress,0%) 100%),linear-gradient(#eef2f6,#eef2f6);pointer-events:none}
	    input[type="range"]{position:relative;width:100%;padding:0;border:0;background:transparent;-webkit-appearance:none;appearance:none;z-index:1}input[type="range"]::-webkit-slider-runnable-track{height:9px;background:transparent;border:0}input[type="range"]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:14px;height:14px;border-radius:50%;background:#1661ab;border:0;margin-top:-2.5px;box-shadow:0 0 0 2px rgba(255,255,255,.85)}input[type="range"]::-moz-range-track{height:9px;background:transparent;border:0}input[type="range"]::-moz-range-thumb{width:14px;height:14px;border-radius:50%;background:#1661ab;border:0;box-shadow:0 0 0 2px rgba(255,255,255,.85)}.dt-range-field input[type="number"],.dt-range-field select{height:30px;padding:0 7px}.dt-unit{min-width:56px;text-align:center}
	    .dt-banner{margin:8px 0 10px;padding:8px 10px;border-radius:6px;background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;font-size:12px;line-height:1.45}
    .dt-divider{height:1px;margin:12px 8px;background:#eaecf0}
    .dt-footer{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:12px 14px;border-top:1px solid #eaecf0;background:#fff}
    .dt-footer[hidden]{display:none}
    #dt-toast{position:absolute;left:22px;bottom:22px;max-width:520px;padding:10px 12px;border-radius:6px;color:#fff;background:rgba(16,24,40,.88);font-size:12px;line-height:1.45;opacity:0;transform:translateY(8px);transition:.18s;pointer-events:none}
    #dt-toast.dt-show{opacity:1;transform:translateY(0)}
    @media(max-width:720px){.dt-app[data-panel-open="true"]{grid-template-columns:minmax(0,1fr) min(384px,54vw)}}
.dt-snapshot-modal{position:fixed;inset:0;z-index:2147483646;display:flex;align-items:center;justify-content:center;padding:28px;background:rgba(16,24,40,.72)}
.dt-snapshot-modal-content{position:relative;width:min(1080px,calc(100vw - 56px));height:min(720px,calc(100vh - 56px));overflow:hidden;border-radius:6px;background:#101828;box-shadow:0 20px 60px rgba(16,24,40,.32)}
.dt-snapshot-modal-content>button{position:absolute;right:clamp(8px,1.4vw,14px);top:clamp(8px,1.4vw,14px);z-index:1;width:clamp(26px,3vw,30px);height:clamp(26px,3vw,30px);padding:0;border-color:rgba(255,255,255,.48);border-radius:50%;background:rgba(16,24,40,.72);color:#fff;font-size:18px;line-height:1;box-shadow:0 1px 3px rgba(16,24,40,.28)}
.dt-snapshot-modal-content>button:hover{background:rgba(16,24,40,.9);border-color:rgba(255,255,255,.72)}
.dt-snapshot-modal-content>img{display:block;width:100%;height:100%;object-fit:contain}`));
      document.head.appendChild(elementStyle);
    }
  } catch (e) {
    console.error("vite-plugin-css-injected-by-js", e);
  }
})();
(function() {
  "use strict";
  function getDefaultExportFromCjs(x2) {
    return x2 && x2.__esModule && Object.prototype.hasOwnProperty.call(x2, "default") ? x2["default"] : x2;
  }
  var jsxRuntime = { exports: {} };
  var reactJsxRuntime_production_min = {};
  var react = { exports: {} };
  var react_production_min = {};
  /**
   * @license React
   * react.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */
  var hasRequiredReact_production_min;
  function requireReact_production_min() {
    if (hasRequiredReact_production_min) return react_production_min;
    hasRequiredReact_production_min = 1;
    var l = Symbol.for("react.element"), n = Symbol.for("react.portal"), p = Symbol.for("react.fragment"), q = Symbol.for("react.strict_mode"), r = Symbol.for("react.profiler"), t = Symbol.for("react.provider"), u = Symbol.for("react.context"), v = Symbol.for("react.forward_ref"), w = Symbol.for("react.suspense"), x2 = Symbol.for("react.memo"), y = Symbol.for("react.lazy"), z = Symbol.iterator;
    function A(a) {
      if (null === a || "object" !== typeof a) return null;
      a = z && a[z] || a["@@iterator"];
      return "function" === typeof a ? a : null;
    }
    var B = { isMounted: function() {
      return false;
    }, enqueueForceUpdate: function() {
    }, enqueueReplaceState: function() {
    }, enqueueSetState: function() {
    } }, C = Object.assign, D = {};
    function E(a, b, e) {
      this.props = a;
      this.context = b;
      this.refs = D;
      this.updater = e || B;
    }
    E.prototype.isReactComponent = {};
    E.prototype.setState = function(a, b) {
      if ("object" !== typeof a && "function" !== typeof a && null != a) throw Error("setState(...): takes an object of state variables to update or a function which returns an object of state variables.");
      this.updater.enqueueSetState(this, a, b, "setState");
    };
    E.prototype.forceUpdate = function(a) {
      this.updater.enqueueForceUpdate(this, a, "forceUpdate");
    };
    function F() {
    }
    F.prototype = E.prototype;
    function G(a, b, e) {
      this.props = a;
      this.context = b;
      this.refs = D;
      this.updater = e || B;
    }
    var H = G.prototype = new F();
    H.constructor = G;
    C(H, E.prototype);
    H.isPureReactComponent = true;
    var I = Array.isArray, J = Object.prototype.hasOwnProperty, K = { current: null }, L = { key: true, ref: true, __self: true, __source: true };
    function M(a, b, e) {
      var d, c = {}, k = null, h = null;
      if (null != b) for (d in void 0 !== b.ref && (h = b.ref), void 0 !== b.key && (k = "" + b.key), b) J.call(b, d) && !L.hasOwnProperty(d) && (c[d] = b[d]);
      var g = arguments.length - 2;
      if (1 === g) c.children = e;
      else if (1 < g) {
        for (var f = Array(g), m = 0; m < g; m++) f[m] = arguments[m + 2];
        c.children = f;
      }
      if (a && a.defaultProps) for (d in g = a.defaultProps, g) void 0 === c[d] && (c[d] = g[d]);
      return { $$typeof: l, type: a, key: k, ref: h, props: c, _owner: K.current };
    }
    function N(a, b) {
      return { $$typeof: l, type: a.type, key: b, ref: a.ref, props: a.props, _owner: a._owner };
    }
    function O(a) {
      return "object" === typeof a && null !== a && a.$$typeof === l;
    }
    function escape(a) {
      var b = { "=": "=0", ":": "=2" };
      return "$" + a.replace(/[=:]/g, function(a2) {
        return b[a2];
      });
    }
    var P = /\/+/g;
    function Q(a, b) {
      return "object" === typeof a && null !== a && null != a.key ? escape("" + a.key) : b.toString(36);
    }
    function R(a, b, e, d, c) {
      var k = typeof a;
      if ("undefined" === k || "boolean" === k) a = null;
      var h = false;
      if (null === a) h = true;
      else switch (k) {
        case "string":
        case "number":
          h = true;
          break;
        case "object":
          switch (a.$$typeof) {
            case l:
            case n:
              h = true;
          }
      }
      if (h) return h = a, c = c(h), a = "" === d ? "." + Q(h, 0) : d, I(c) ? (e = "", null != a && (e = a.replace(P, "$&/") + "/"), R(c, b, e, "", function(a2) {
        return a2;
      })) : null != c && (O(c) && (c = N(c, e + (!c.key || h && h.key === c.key ? "" : ("" + c.key).replace(P, "$&/") + "/") + a)), b.push(c)), 1;
      h = 0;
      d = "" === d ? "." : d + ":";
      if (I(a)) for (var g = 0; g < a.length; g++) {
        k = a[g];
        var f = d + Q(k, g);
        h += R(k, b, e, f, c);
      }
      else if (f = A(a), "function" === typeof f) for (a = f.call(a), g = 0; !(k = a.next()).done; ) k = k.value, f = d + Q(k, g++), h += R(k, b, e, f, c);
      else if ("object" === k) throw b = String(a), Error("Objects are not valid as a React child (found: " + ("[object Object]" === b ? "object with keys {" + Object.keys(a).join(", ") + "}" : b) + "). If you meant to render a collection of children, use an array instead.");
      return h;
    }
    function S(a, b, e) {
      if (null == a) return a;
      var d = [], c = 0;
      R(a, d, "", "", function(a2) {
        return b.call(e, a2, c++);
      });
      return d;
    }
    function T(a) {
      if (-1 === a._status) {
        var b = a._result;
        b = b();
        b.then(function(b3) {
          if (0 === a._status || -1 === a._status) a._status = 1, a._result = b3;
        }, function(b3) {
          if (0 === a._status || -1 === a._status) a._status = 2, a._result = b3;
        });
        -1 === a._status && (a._status = 0, a._result = b);
      }
      if (1 === a._status) return a._result.default;
      throw a._result;
    }
    var U = { current: null }, V = { transition: null }, W = { ReactCurrentDispatcher: U, ReactCurrentBatchConfig: V, ReactCurrentOwner: K };
    function X() {
      throw Error("act(...) is not supported in production builds of React.");
    }
    react_production_min.Children = { map: S, forEach: function(a, b, e) {
      S(a, function() {
        b.apply(this, arguments);
      }, e);
    }, count: function(a) {
      var b = 0;
      S(a, function() {
        b++;
      });
      return b;
    }, toArray: function(a) {
      return S(a, function(a2) {
        return a2;
      }) || [];
    }, only: function(a) {
      if (!O(a)) throw Error("React.Children.only expected to receive a single React element child.");
      return a;
    } };
    react_production_min.Component = E;
    react_production_min.Fragment = p;
    react_production_min.Profiler = r;
    react_production_min.PureComponent = G;
    react_production_min.StrictMode = q;
    react_production_min.Suspense = w;
    react_production_min.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = W;
    react_production_min.act = X;
    react_production_min.cloneElement = function(a, b, e) {
      if (null === a || void 0 === a) throw Error("React.cloneElement(...): The argument must be a React element, but you passed " + a + ".");
      var d = C({}, a.props), c = a.key, k = a.ref, h = a._owner;
      if (null != b) {
        void 0 !== b.ref && (k = b.ref, h = K.current);
        void 0 !== b.key && (c = "" + b.key);
        if (a.type && a.type.defaultProps) var g = a.type.defaultProps;
        for (f in b) J.call(b, f) && !L.hasOwnProperty(f) && (d[f] = void 0 === b[f] && void 0 !== g ? g[f] : b[f]);
      }
      var f = arguments.length - 2;
      if (1 === f) d.children = e;
      else if (1 < f) {
        g = Array(f);
        for (var m = 0; m < f; m++) g[m] = arguments[m + 2];
        d.children = g;
      }
      return { $$typeof: l, type: a.type, key: c, ref: k, props: d, _owner: h };
    };
    react_production_min.createContext = function(a) {
      a = { $$typeof: u, _currentValue: a, _currentValue2: a, _threadCount: 0, Provider: null, Consumer: null, _defaultValue: null, _globalName: null };
      a.Provider = { $$typeof: t, _context: a };
      return a.Consumer = a;
    };
    react_production_min.createElement = M;
    react_production_min.createFactory = function(a) {
      var b = M.bind(null, a);
      b.type = a;
      return b;
    };
    react_production_min.createRef = function() {
      return { current: null };
    };
    react_production_min.forwardRef = function(a) {
      return { $$typeof: v, render: a };
    };
    react_production_min.isValidElement = O;
    react_production_min.lazy = function(a) {
      return { $$typeof: y, _payload: { _status: -1, _result: a }, _init: T };
    };
    react_production_min.memo = function(a, b) {
      return { $$typeof: x2, type: a, compare: void 0 === b ? null : b };
    };
    react_production_min.startTransition = function(a) {
      var b = V.transition;
      V.transition = {};
      try {
        a();
      } finally {
        V.transition = b;
      }
    };
    react_production_min.unstable_act = X;
    react_production_min.useCallback = function(a, b) {
      return U.current.useCallback(a, b);
    };
    react_production_min.useContext = function(a) {
      return U.current.useContext(a);
    };
    react_production_min.useDebugValue = function() {
    };
    react_production_min.useDeferredValue = function(a) {
      return U.current.useDeferredValue(a);
    };
    react_production_min.useEffect = function(a, b) {
      return U.current.useEffect(a, b);
    };
    react_production_min.useId = function() {
      return U.current.useId();
    };
    react_production_min.useImperativeHandle = function(a, b, e) {
      return U.current.useImperativeHandle(a, b, e);
    };
    react_production_min.useInsertionEffect = function(a, b) {
      return U.current.useInsertionEffect(a, b);
    };
    react_production_min.useLayoutEffect = function(a, b) {
      return U.current.useLayoutEffect(a, b);
    };
    react_production_min.useMemo = function(a, b) {
      return U.current.useMemo(a, b);
    };
    react_production_min.useReducer = function(a, b, e) {
      return U.current.useReducer(a, b, e);
    };
    react_production_min.useRef = function(a) {
      return U.current.useRef(a);
    };
    react_production_min.useState = function(a) {
      return U.current.useState(a);
    };
    react_production_min.useSyncExternalStore = function(a, b, e) {
      return U.current.useSyncExternalStore(a, b, e);
    };
    react_production_min.useTransition = function() {
      return U.current.useTransition();
    };
    react_production_min.version = "18.3.1";
    return react_production_min;
  }
  var hasRequiredReact;
  function requireReact() {
    if (hasRequiredReact) return react.exports;
    hasRequiredReact = 1;
    {
      react.exports = requireReact_production_min();
    }
    return react.exports;
  }
  /**
   * @license React
   * react-jsx-runtime.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */
  var hasRequiredReactJsxRuntime_production_min;
  function requireReactJsxRuntime_production_min() {
    if (hasRequiredReactJsxRuntime_production_min) return reactJsxRuntime_production_min;
    hasRequiredReactJsxRuntime_production_min = 1;
    var f = requireReact(), k = Symbol.for("react.element"), l = Symbol.for("react.fragment"), m = Object.prototype.hasOwnProperty, n = f.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, p = { key: true, ref: true, __self: true, __source: true };
    function q(c, a, g) {
      var b, d = {}, e = null, h = null;
      void 0 !== g && (e = "" + g);
      void 0 !== a.key && (e = "" + a.key);
      void 0 !== a.ref && (h = a.ref);
      for (b in a) m.call(a, b) && !p.hasOwnProperty(b) && (d[b] = a[b]);
      if (c && c.defaultProps) for (b in a = c.defaultProps, a) void 0 === d[b] && (d[b] = a[b]);
      return { $$typeof: k, type: c, key: e, ref: h, props: d, _owner: n.current };
    }
    reactJsxRuntime_production_min.Fragment = l;
    reactJsxRuntime_production_min.jsx = q;
    reactJsxRuntime_production_min.jsxs = q;
    return reactJsxRuntime_production_min;
  }
  var hasRequiredJsxRuntime;
  function requireJsxRuntime() {
    if (hasRequiredJsxRuntime) return jsxRuntime.exports;
    hasRequiredJsxRuntime = 1;
    {
      jsxRuntime.exports = requireReactJsxRuntime_production_min();
    }
    return jsxRuntime.exports;
  }
  var jsxRuntimeExports = requireJsxRuntime();
  var client = {};
  var reactDom = { exports: {} };
  var reactDom_production_min = {};
  var scheduler = { exports: {} };
  var scheduler_production_min = {};
  /**
   * @license React
   * scheduler.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */
  var hasRequiredScheduler_production_min;
  function requireScheduler_production_min() {
    if (hasRequiredScheduler_production_min) return scheduler_production_min;
    hasRequiredScheduler_production_min = 1;
    (function(exports) {
      function f(a, b) {
        var c = a.length;
        a.push(b);
        a: for (; 0 < c; ) {
          var d = c - 1 >>> 1, e = a[d];
          if (0 < g(e, b)) a[d] = b, a[c] = e, c = d;
          else break a;
        }
      }
      function h(a) {
        return 0 === a.length ? null : a[0];
      }
      function k(a) {
        if (0 === a.length) return null;
        var b = a[0], c = a.pop();
        if (c !== b) {
          a[0] = c;
          a: for (var d = 0, e = a.length, w = e >>> 1; d < w; ) {
            var m = 2 * (d + 1) - 1, C = a[m], n = m + 1, x2 = a[n];
            if (0 > g(C, c)) n < e && 0 > g(x2, C) ? (a[d] = x2, a[n] = c, d = n) : (a[d] = C, a[m] = c, d = m);
            else if (n < e && 0 > g(x2, c)) a[d] = x2, a[n] = c, d = n;
            else break a;
          }
        }
        return b;
      }
      function g(a, b) {
        var c = a.sortIndex - b.sortIndex;
        return 0 !== c ? c : a.id - b.id;
      }
      if ("object" === typeof performance && "function" === typeof performance.now) {
        var l = performance;
        exports.unstable_now = function() {
          return l.now();
        };
      } else {
        var p = Date, q = p.now();
        exports.unstable_now = function() {
          return p.now() - q;
        };
      }
      var r = [], t = [], u = 1, v = null, y = 3, z = false, A = false, B = false, D = "function" === typeof setTimeout ? setTimeout : null, E = "function" === typeof clearTimeout ? clearTimeout : null, F = "undefined" !== typeof setImmediate ? setImmediate : null;
      "undefined" !== typeof navigator && void 0 !== navigator.scheduling && void 0 !== navigator.scheduling.isInputPending && navigator.scheduling.isInputPending.bind(navigator.scheduling);
      function G(a) {
        for (var b = h(t); null !== b; ) {
          if (null === b.callback) k(t);
          else if (b.startTime <= a) k(t), b.sortIndex = b.expirationTime, f(r, b);
          else break;
          b = h(t);
        }
      }
      function H(a) {
        B = false;
        G(a);
        if (!A) if (null !== h(r)) A = true, I(J);
        else {
          var b = h(t);
          null !== b && K(H, b.startTime - a);
        }
      }
      function J(a, b) {
        A = false;
        B && (B = false, E(L), L = -1);
        z = true;
        var c = y;
        try {
          G(b);
          for (v = h(r); null !== v && (!(v.expirationTime > b) || a && !M()); ) {
            var d = v.callback;
            if ("function" === typeof d) {
              v.callback = null;
              y = v.priorityLevel;
              var e = d(v.expirationTime <= b);
              b = exports.unstable_now();
              "function" === typeof e ? v.callback = e : v === h(r) && k(r);
              G(b);
            } else k(r);
            v = h(r);
          }
          if (null !== v) var w = true;
          else {
            var m = h(t);
            null !== m && K(H, m.startTime - b);
            w = false;
          }
          return w;
        } finally {
          v = null, y = c, z = false;
        }
      }
      var N = false, O = null, L = -1, P = 5, Q = -1;
      function M() {
        return exports.unstable_now() - Q < P ? false : true;
      }
      function R() {
        if (null !== O) {
          var a = exports.unstable_now();
          Q = a;
          var b = true;
          try {
            b = O(true, a);
          } finally {
            b ? S() : (N = false, O = null);
          }
        } else N = false;
      }
      var S;
      if ("function" === typeof F) S = function() {
        F(R);
      };
      else if ("undefined" !== typeof MessageChannel) {
        var T = new MessageChannel(), U = T.port2;
        T.port1.onmessage = R;
        S = function() {
          U.postMessage(null);
        };
      } else S = function() {
        D(R, 0);
      };
      function I(a) {
        O = a;
        N || (N = true, S());
      }
      function K(a, b) {
        L = D(function() {
          a(exports.unstable_now());
        }, b);
      }
      exports.unstable_IdlePriority = 5;
      exports.unstable_ImmediatePriority = 1;
      exports.unstable_LowPriority = 4;
      exports.unstable_NormalPriority = 3;
      exports.unstable_Profiling = null;
      exports.unstable_UserBlockingPriority = 2;
      exports.unstable_cancelCallback = function(a) {
        a.callback = null;
      };
      exports.unstable_continueExecution = function() {
        A || z || (A = true, I(J));
      };
      exports.unstable_forceFrameRate = function(a) {
        0 > a || 125 < a ? console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported") : P = 0 < a ? Math.floor(1e3 / a) : 5;
      };
      exports.unstable_getCurrentPriorityLevel = function() {
        return y;
      };
      exports.unstable_getFirstCallbackNode = function() {
        return h(r);
      };
      exports.unstable_next = function(a) {
        switch (y) {
          case 1:
          case 2:
          case 3:
            var b = 3;
            break;
          default:
            b = y;
        }
        var c = y;
        y = b;
        try {
          return a();
        } finally {
          y = c;
        }
      };
      exports.unstable_pauseExecution = function() {
      };
      exports.unstable_requestPaint = function() {
      };
      exports.unstable_runWithPriority = function(a, b) {
        switch (a) {
          case 1:
          case 2:
          case 3:
          case 4:
          case 5:
            break;
          default:
            a = 3;
        }
        var c = y;
        y = a;
        try {
          return b();
        } finally {
          y = c;
        }
      };
      exports.unstable_scheduleCallback = function(a, b, c) {
        var d = exports.unstable_now();
        "object" === typeof c && null !== c ? (c = c.delay, c = "number" === typeof c && 0 < c ? d + c : d) : c = d;
        switch (a) {
          case 1:
            var e = -1;
            break;
          case 2:
            e = 250;
            break;
          case 5:
            e = 1073741823;
            break;
          case 4:
            e = 1e4;
            break;
          default:
            e = 5e3;
        }
        e = c + e;
        a = { id: u++, callback: b, priorityLevel: a, startTime: c, expirationTime: e, sortIndex: -1 };
        c > d ? (a.sortIndex = c, f(t, a), null === h(r) && a === h(t) && (B ? (E(L), L = -1) : B = true, K(H, c - d))) : (a.sortIndex = e, f(r, a), A || z || (A = true, I(J)));
        return a;
      };
      exports.unstable_shouldYield = M;
      exports.unstable_wrapCallback = function(a) {
        var b = y;
        return function() {
          var c = y;
          y = b;
          try {
            return a.apply(this, arguments);
          } finally {
            y = c;
          }
        };
      };
    })(scheduler_production_min);
    return scheduler_production_min;
  }
  var hasRequiredScheduler;
  function requireScheduler() {
    if (hasRequiredScheduler) return scheduler.exports;
    hasRequiredScheduler = 1;
    {
      scheduler.exports = requireScheduler_production_min();
    }
    return scheduler.exports;
  }
  /**
   * @license React
   * react-dom.production.min.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   */
  var hasRequiredReactDom_production_min;
  function requireReactDom_production_min() {
    if (hasRequiredReactDom_production_min) return reactDom_production_min;
    hasRequiredReactDom_production_min = 1;
    var aa = requireReact(), ca = requireScheduler();
    function p(a) {
      for (var b = "https://reactjs.org/docs/error-decoder.html?invariant=" + a, c = 1; c < arguments.length; c++) b += "&args[]=" + encodeURIComponent(arguments[c]);
      return "Minified React error #" + a + "; visit " + b + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
    }
    var da = /* @__PURE__ */ new Set(), ea = {};
    function fa(a, b) {
      ha(a, b);
      ha(a + "Capture", b);
    }
    function ha(a, b) {
      ea[a] = b;
      for (a = 0; a < b.length; a++) da.add(b[a]);
    }
    var ia = !("undefined" === typeof window || "undefined" === typeof window.document || "undefined" === typeof window.document.createElement), ja = Object.prototype.hasOwnProperty, ka = /^[:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][:A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\-.0-9\u00B7\u0300-\u036F\u203F-\u2040]*$/, la = {}, ma = {};
    function oa(a) {
      if (ja.call(ma, a)) return true;
      if (ja.call(la, a)) return false;
      if (ka.test(a)) return ma[a] = true;
      la[a] = true;
      return false;
    }
    function pa(a, b, c, d) {
      if (null !== c && 0 === c.type) return false;
      switch (typeof b) {
        case "function":
        case "symbol":
          return true;
        case "boolean":
          if (d) return false;
          if (null !== c) return !c.acceptsBooleans;
          a = a.toLowerCase().slice(0, 5);
          return "data-" !== a && "aria-" !== a;
        default:
          return false;
      }
    }
    function qa(a, b, c, d) {
      if (null === b || "undefined" === typeof b || pa(a, b, c, d)) return true;
      if (d) return false;
      if (null !== c) switch (c.type) {
        case 3:
          return !b;
        case 4:
          return false === b;
        case 5:
          return isNaN(b);
        case 6:
          return isNaN(b) || 1 > b;
      }
      return false;
    }
    function v(a, b, c, d, e, f, g) {
      this.acceptsBooleans = 2 === b || 3 === b || 4 === b;
      this.attributeName = d;
      this.attributeNamespace = e;
      this.mustUseProperty = c;
      this.propertyName = a;
      this.type = b;
      this.sanitizeURL = f;
      this.removeEmptyString = g;
    }
    var z = {};
    "children dangerouslySetInnerHTML defaultValue defaultChecked innerHTML suppressContentEditableWarning suppressHydrationWarning style".split(" ").forEach(function(a) {
      z[a] = new v(a, 0, false, a, null, false, false);
    });
    [["acceptCharset", "accept-charset"], ["className", "class"], ["htmlFor", "for"], ["httpEquiv", "http-equiv"]].forEach(function(a) {
      var b = a[0];
      z[b] = new v(b, 1, false, a[1], null, false, false);
    });
    ["contentEditable", "draggable", "spellCheck", "value"].forEach(function(a) {
      z[a] = new v(a, 2, false, a.toLowerCase(), null, false, false);
    });
    ["autoReverse", "externalResourcesRequired", "focusable", "preserveAlpha"].forEach(function(a) {
      z[a] = new v(a, 2, false, a, null, false, false);
    });
    "allowFullScreen async autoFocus autoPlay controls default defer disabled disablePictureInPicture disableRemotePlayback formNoValidate hidden loop noModule noValidate open playsInline readOnly required reversed scoped seamless itemScope".split(" ").forEach(function(a) {
      z[a] = new v(a, 3, false, a.toLowerCase(), null, false, false);
    });
    ["checked", "multiple", "muted", "selected"].forEach(function(a) {
      z[a] = new v(a, 3, true, a, null, false, false);
    });
    ["capture", "download"].forEach(function(a) {
      z[a] = new v(a, 4, false, a, null, false, false);
    });
    ["cols", "rows", "size", "span"].forEach(function(a) {
      z[a] = new v(a, 6, false, a, null, false, false);
    });
    ["rowSpan", "start"].forEach(function(a) {
      z[a] = new v(a, 5, false, a.toLowerCase(), null, false, false);
    });
    var ra = /[\-:]([a-z])/g;
    function sa(a) {
      return a[1].toUpperCase();
    }
    "accent-height alignment-baseline arabic-form baseline-shift cap-height clip-path clip-rule color-interpolation color-interpolation-filters color-profile color-rendering dominant-baseline enable-background fill-opacity fill-rule flood-color flood-opacity font-family font-size font-size-adjust font-stretch font-style font-variant font-weight glyph-name glyph-orientation-horizontal glyph-orientation-vertical horiz-adv-x horiz-origin-x image-rendering letter-spacing lighting-color marker-end marker-mid marker-start overline-position overline-thickness paint-order panose-1 pointer-events rendering-intent shape-rendering stop-color stop-opacity strikethrough-position strikethrough-thickness stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit stroke-opacity stroke-width text-anchor text-decoration text-rendering underline-position underline-thickness unicode-bidi unicode-range units-per-em v-alphabetic v-hanging v-ideographic v-mathematical vector-effect vert-adv-y vert-origin-x vert-origin-y word-spacing writing-mode xmlns:xlink x-height".split(" ").forEach(function(a) {
      var b = a.replace(
        ra,
        sa
      );
      z[b] = new v(b, 1, false, a, null, false, false);
    });
    "xlink:actuate xlink:arcrole xlink:role xlink:show xlink:title xlink:type".split(" ").forEach(function(a) {
      var b = a.replace(ra, sa);
      z[b] = new v(b, 1, false, a, "http://www.w3.org/1999/xlink", false, false);
    });
    ["xml:base", "xml:lang", "xml:space"].forEach(function(a) {
      var b = a.replace(ra, sa);
      z[b] = new v(b, 1, false, a, "http://www.w3.org/XML/1998/namespace", false, false);
    });
    ["tabIndex", "crossOrigin"].forEach(function(a) {
      z[a] = new v(a, 1, false, a.toLowerCase(), null, false, false);
    });
    z.xlinkHref = new v("xlinkHref", 1, false, "xlink:href", "http://www.w3.org/1999/xlink", true, false);
    ["src", "href", "action", "formAction"].forEach(function(a) {
      z[a] = new v(a, 1, false, a.toLowerCase(), null, true, true);
    });
    function ta(a, b, c, d) {
      var e = z.hasOwnProperty(b) ? z[b] : null;
      if (null !== e ? 0 !== e.type : d || !(2 < b.length) || "o" !== b[0] && "O" !== b[0] || "n" !== b[1] && "N" !== b[1]) qa(b, c, e, d) && (c = null), d || null === e ? oa(b) && (null === c ? a.removeAttribute(b) : a.setAttribute(b, "" + c)) : e.mustUseProperty ? a[e.propertyName] = null === c ? 3 === e.type ? false : "" : c : (b = e.attributeName, d = e.attributeNamespace, null === c ? a.removeAttribute(b) : (e = e.type, c = 3 === e || 4 === e && true === c ? "" : "" + c, d ? a.setAttributeNS(d, b, c) : a.setAttribute(b, c)));
    }
    var ua = aa.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED, va = Symbol.for("react.element"), wa = Symbol.for("react.portal"), ya = Symbol.for("react.fragment"), za = Symbol.for("react.strict_mode"), Aa = Symbol.for("react.profiler"), Ba = Symbol.for("react.provider"), Ca = Symbol.for("react.context"), Da = Symbol.for("react.forward_ref"), Ea = Symbol.for("react.suspense"), Fa = Symbol.for("react.suspense_list"), Ga = Symbol.for("react.memo"), Ha = Symbol.for("react.lazy");
    var Ia = Symbol.for("react.offscreen");
    var Ja = Symbol.iterator;
    function Ka(a) {
      if (null === a || "object" !== typeof a) return null;
      a = Ja && a[Ja] || a["@@iterator"];
      return "function" === typeof a ? a : null;
    }
    var A = Object.assign, La;
    function Ma(a) {
      if (void 0 === La) try {
        throw Error();
      } catch (c) {
        var b = c.stack.trim().match(/\n( *(at )?)/);
        La = b && b[1] || "";
      }
      return "\n" + La + a;
    }
    var Na = false;
    function Oa(a, b) {
      if (!a || Na) return "";
      Na = true;
      var c = Error.prepareStackTrace;
      Error.prepareStackTrace = void 0;
      try {
        if (b) if (b = function() {
          throw Error();
        }, Object.defineProperty(b.prototype, "props", { set: function() {
          throw Error();
        } }), "object" === typeof Reflect && Reflect.construct) {
          try {
            Reflect.construct(b, []);
          } catch (l) {
            var d = l;
          }
          Reflect.construct(a, [], b);
        } else {
          try {
            b.call();
          } catch (l) {
            d = l;
          }
          a.call(b.prototype);
        }
        else {
          try {
            throw Error();
          } catch (l) {
            d = l;
          }
          a();
        }
      } catch (l) {
        if (l && d && "string" === typeof l.stack) {
          for (var e = l.stack.split("\n"), f = d.stack.split("\n"), g = e.length - 1, h = f.length - 1; 1 <= g && 0 <= h && e[g] !== f[h]; ) h--;
          for (; 1 <= g && 0 <= h; g--, h--) if (e[g] !== f[h]) {
            if (1 !== g || 1 !== h) {
              do
                if (g--, h--, 0 > h || e[g] !== f[h]) {
                  var k = "\n" + e[g].replace(" at new ", " at ");
                  a.displayName && k.includes("<anonymous>") && (k = k.replace("<anonymous>", a.displayName));
                  return k;
                }
              while (1 <= g && 0 <= h);
            }
            break;
          }
        }
      } finally {
        Na = false, Error.prepareStackTrace = c;
      }
      return (a = a ? a.displayName || a.name : "") ? Ma(a) : "";
    }
    function Pa(a) {
      switch (a.tag) {
        case 5:
          return Ma(a.type);
        case 16:
          return Ma("Lazy");
        case 13:
          return Ma("Suspense");
        case 19:
          return Ma("SuspenseList");
        case 0:
        case 2:
        case 15:
          return a = Oa(a.type, false), a;
        case 11:
          return a = Oa(a.type.render, false), a;
        case 1:
          return a = Oa(a.type, true), a;
        default:
          return "";
      }
    }
    function Qa(a) {
      if (null == a) return null;
      if ("function" === typeof a) return a.displayName || a.name || null;
      if ("string" === typeof a) return a;
      switch (a) {
        case ya:
          return "Fragment";
        case wa:
          return "Portal";
        case Aa:
          return "Profiler";
        case za:
          return "StrictMode";
        case Ea:
          return "Suspense";
        case Fa:
          return "SuspenseList";
      }
      if ("object" === typeof a) switch (a.$$typeof) {
        case Ca:
          return (a.displayName || "Context") + ".Consumer";
        case Ba:
          return (a._context.displayName || "Context") + ".Provider";
        case Da:
          var b = a.render;
          a = a.displayName;
          a || (a = b.displayName || b.name || "", a = "" !== a ? "ForwardRef(" + a + ")" : "ForwardRef");
          return a;
        case Ga:
          return b = a.displayName || null, null !== b ? b : Qa(a.type) || "Memo";
        case Ha:
          b = a._payload;
          a = a._init;
          try {
            return Qa(a(b));
          } catch (c) {
          }
      }
      return null;
    }
    function Ra(a) {
      var b = a.type;
      switch (a.tag) {
        case 24:
          return "Cache";
        case 9:
          return (b.displayName || "Context") + ".Consumer";
        case 10:
          return (b._context.displayName || "Context") + ".Provider";
        case 18:
          return "DehydratedFragment";
        case 11:
          return a = b.render, a = a.displayName || a.name || "", b.displayName || ("" !== a ? "ForwardRef(" + a + ")" : "ForwardRef");
        case 7:
          return "Fragment";
        case 5:
          return b;
        case 4:
          return "Portal";
        case 3:
          return "Root";
        case 6:
          return "Text";
        case 16:
          return Qa(b);
        case 8:
          return b === za ? "StrictMode" : "Mode";
        case 22:
          return "Offscreen";
        case 12:
          return "Profiler";
        case 21:
          return "Scope";
        case 13:
          return "Suspense";
        case 19:
          return "SuspenseList";
        case 25:
          return "TracingMarker";
        case 1:
        case 0:
        case 17:
        case 2:
        case 14:
        case 15:
          if ("function" === typeof b) return b.displayName || b.name || null;
          if ("string" === typeof b) return b;
      }
      return null;
    }
    function Sa(a) {
      switch (typeof a) {
        case "boolean":
        case "number":
        case "string":
        case "undefined":
          return a;
        case "object":
          return a;
        default:
          return "";
      }
    }
    function Ta(a) {
      var b = a.type;
      return (a = a.nodeName) && "input" === a.toLowerCase() && ("checkbox" === b || "radio" === b);
    }
    function Ua(a) {
      var b = Ta(a) ? "checked" : "value", c = Object.getOwnPropertyDescriptor(a.constructor.prototype, b), d = "" + a[b];
      if (!a.hasOwnProperty(b) && "undefined" !== typeof c && "function" === typeof c.get && "function" === typeof c.set) {
        var e = c.get, f = c.set;
        Object.defineProperty(a, b, { configurable: true, get: function() {
          return e.call(this);
        }, set: function(a2) {
          d = "" + a2;
          f.call(this, a2);
        } });
        Object.defineProperty(a, b, { enumerable: c.enumerable });
        return { getValue: function() {
          return d;
        }, setValue: function(a2) {
          d = "" + a2;
        }, stopTracking: function() {
          a._valueTracker = null;
          delete a[b];
        } };
      }
    }
    function Va(a) {
      a._valueTracker || (a._valueTracker = Ua(a));
    }
    function Wa(a) {
      if (!a) return false;
      var b = a._valueTracker;
      if (!b) return true;
      var c = b.getValue();
      var d = "";
      a && (d = Ta(a) ? a.checked ? "true" : "false" : a.value);
      a = d;
      return a !== c ? (b.setValue(a), true) : false;
    }
    function Xa(a) {
      a = a || ("undefined" !== typeof document ? document : void 0);
      if ("undefined" === typeof a) return null;
      try {
        return a.activeElement || a.body;
      } catch (b) {
        return a.body;
      }
    }
    function Ya(a, b) {
      var c = b.checked;
      return A({}, b, { defaultChecked: void 0, defaultValue: void 0, value: void 0, checked: null != c ? c : a._wrapperState.initialChecked });
    }
    function Za(a, b) {
      var c = null == b.defaultValue ? "" : b.defaultValue, d = null != b.checked ? b.checked : b.defaultChecked;
      c = Sa(null != b.value ? b.value : c);
      a._wrapperState = { initialChecked: d, initialValue: c, controlled: "checkbox" === b.type || "radio" === b.type ? null != b.checked : null != b.value };
    }
    function ab(a, b) {
      b = b.checked;
      null != b && ta(a, "checked", b, false);
    }
    function bb(a, b) {
      ab(a, b);
      var c = Sa(b.value), d = b.type;
      if (null != c) if ("number" === d) {
        if (0 === c && "" === a.value || a.value != c) a.value = "" + c;
      } else a.value !== "" + c && (a.value = "" + c);
      else if ("submit" === d || "reset" === d) {
        a.removeAttribute("value");
        return;
      }
      b.hasOwnProperty("value") ? cb(a, b.type, c) : b.hasOwnProperty("defaultValue") && cb(a, b.type, Sa(b.defaultValue));
      null == b.checked && null != b.defaultChecked && (a.defaultChecked = !!b.defaultChecked);
    }
    function db(a, b, c) {
      if (b.hasOwnProperty("value") || b.hasOwnProperty("defaultValue")) {
        var d = b.type;
        if (!("submit" !== d && "reset" !== d || void 0 !== b.value && null !== b.value)) return;
        b = "" + a._wrapperState.initialValue;
        c || b === a.value || (a.value = b);
        a.defaultValue = b;
      }
      c = a.name;
      "" !== c && (a.name = "");
      a.defaultChecked = !!a._wrapperState.initialChecked;
      "" !== c && (a.name = c);
    }
    function cb(a, b, c) {
      if ("number" !== b || Xa(a.ownerDocument) !== a) null == c ? a.defaultValue = "" + a._wrapperState.initialValue : a.defaultValue !== "" + c && (a.defaultValue = "" + c);
    }
    var eb = Array.isArray;
    function fb(a, b, c, d) {
      a = a.options;
      if (b) {
        b = {};
        for (var e = 0; e < c.length; e++) b["$" + c[e]] = true;
        for (c = 0; c < a.length; c++) e = b.hasOwnProperty("$" + a[c].value), a[c].selected !== e && (a[c].selected = e), e && d && (a[c].defaultSelected = true);
      } else {
        c = "" + Sa(c);
        b = null;
        for (e = 0; e < a.length; e++) {
          if (a[e].value === c) {
            a[e].selected = true;
            d && (a[e].defaultSelected = true);
            return;
          }
          null !== b || a[e].disabled || (b = a[e]);
        }
        null !== b && (b.selected = true);
      }
    }
    function gb(a, b) {
      if (null != b.dangerouslySetInnerHTML) throw Error(p(91));
      return A({}, b, { value: void 0, defaultValue: void 0, children: "" + a._wrapperState.initialValue });
    }
    function hb(a, b) {
      var c = b.value;
      if (null == c) {
        c = b.children;
        b = b.defaultValue;
        if (null != c) {
          if (null != b) throw Error(p(92));
          if (eb(c)) {
            if (1 < c.length) throw Error(p(93));
            c = c[0];
          }
          b = c;
        }
        null == b && (b = "");
        c = b;
      }
      a._wrapperState = { initialValue: Sa(c) };
    }
    function ib(a, b) {
      var c = Sa(b.value), d = Sa(b.defaultValue);
      null != c && (c = "" + c, c !== a.value && (a.value = c), null == b.defaultValue && a.defaultValue !== c && (a.defaultValue = c));
      null != d && (a.defaultValue = "" + d);
    }
    function jb(a) {
      var b = a.textContent;
      b === a._wrapperState.initialValue && "" !== b && null !== b && (a.value = b);
    }
    function kb(a) {
      switch (a) {
        case "svg":
          return "http://www.w3.org/2000/svg";
        case "math":
          return "http://www.w3.org/1998/Math/MathML";
        default:
          return "http://www.w3.org/1999/xhtml";
      }
    }
    function lb(a, b) {
      return null == a || "http://www.w3.org/1999/xhtml" === a ? kb(b) : "http://www.w3.org/2000/svg" === a && "foreignObject" === b ? "http://www.w3.org/1999/xhtml" : a;
    }
    var mb, nb = (function(a) {
      return "undefined" !== typeof MSApp && MSApp.execUnsafeLocalFunction ? function(b, c, d, e) {
        MSApp.execUnsafeLocalFunction(function() {
          return a(b, c, d, e);
        });
      } : a;
    })(function(a, b) {
      if ("http://www.w3.org/2000/svg" !== a.namespaceURI || "innerHTML" in a) a.innerHTML = b;
      else {
        mb = mb || document.createElement("div");
        mb.innerHTML = "<svg>" + b.valueOf().toString() + "</svg>";
        for (b = mb.firstChild; a.firstChild; ) a.removeChild(a.firstChild);
        for (; b.firstChild; ) a.appendChild(b.firstChild);
      }
    });
    function ob(a, b) {
      if (b) {
        var c = a.firstChild;
        if (c && c === a.lastChild && 3 === c.nodeType) {
          c.nodeValue = b;
          return;
        }
      }
      a.textContent = b;
    }
    var pb = {
      animationIterationCount: true,
      aspectRatio: true,
      borderImageOutset: true,
      borderImageSlice: true,
      borderImageWidth: true,
      boxFlex: true,
      boxFlexGroup: true,
      boxOrdinalGroup: true,
      columnCount: true,
      columns: true,
      flex: true,
      flexGrow: true,
      flexPositive: true,
      flexShrink: true,
      flexNegative: true,
      flexOrder: true,
      gridArea: true,
      gridRow: true,
      gridRowEnd: true,
      gridRowSpan: true,
      gridRowStart: true,
      gridColumn: true,
      gridColumnEnd: true,
      gridColumnSpan: true,
      gridColumnStart: true,
      fontWeight: true,
      lineClamp: true,
      lineHeight: true,
      opacity: true,
      order: true,
      orphans: true,
      tabSize: true,
      widows: true,
      zIndex: true,
      zoom: true,
      fillOpacity: true,
      floodOpacity: true,
      stopOpacity: true,
      strokeDasharray: true,
      strokeDashoffset: true,
      strokeMiterlimit: true,
      strokeOpacity: true,
      strokeWidth: true
    }, qb = ["Webkit", "ms", "Moz", "O"];
    Object.keys(pb).forEach(function(a) {
      qb.forEach(function(b) {
        b = b + a.charAt(0).toUpperCase() + a.substring(1);
        pb[b] = pb[a];
      });
    });
    function rb(a, b, c) {
      return null == b || "boolean" === typeof b || "" === b ? "" : c || "number" !== typeof b || 0 === b || pb.hasOwnProperty(a) && pb[a] ? ("" + b).trim() : b + "px";
    }
    function sb(a, b) {
      a = a.style;
      for (var c in b) if (b.hasOwnProperty(c)) {
        var d = 0 === c.indexOf("--"), e = rb(c, b[c], d);
        "float" === c && (c = "cssFloat");
        d ? a.setProperty(c, e) : a[c] = e;
      }
    }
    var tb = A({ menuitem: true }, { area: true, base: true, br: true, col: true, embed: true, hr: true, img: true, input: true, keygen: true, link: true, meta: true, param: true, source: true, track: true, wbr: true });
    function ub(a, b) {
      if (b) {
        if (tb[a] && (null != b.children || null != b.dangerouslySetInnerHTML)) throw Error(p(137, a));
        if (null != b.dangerouslySetInnerHTML) {
          if (null != b.children) throw Error(p(60));
          if ("object" !== typeof b.dangerouslySetInnerHTML || !("__html" in b.dangerouslySetInnerHTML)) throw Error(p(61));
        }
        if (null != b.style && "object" !== typeof b.style) throw Error(p(62));
      }
    }
    function vb(a, b) {
      if (-1 === a.indexOf("-")) return "string" === typeof b.is;
      switch (a) {
        case "annotation-xml":
        case "color-profile":
        case "font-face":
        case "font-face-src":
        case "font-face-uri":
        case "font-face-format":
        case "font-face-name":
        case "missing-glyph":
          return false;
        default:
          return true;
      }
    }
    var wb = null;
    function xb(a) {
      a = a.target || a.srcElement || window;
      a.correspondingUseElement && (a = a.correspondingUseElement);
      return 3 === a.nodeType ? a.parentNode : a;
    }
    var yb = null, zb = null, Ab = null;
    function Bb(a) {
      if (a = Cb(a)) {
        if ("function" !== typeof yb) throw Error(p(280));
        var b = a.stateNode;
        b && (b = Db(b), yb(a.stateNode, a.type, b));
      }
    }
    function Eb(a) {
      zb ? Ab ? Ab.push(a) : Ab = [a] : zb = a;
    }
    function Fb() {
      if (zb) {
        var a = zb, b = Ab;
        Ab = zb = null;
        Bb(a);
        if (b) for (a = 0; a < b.length; a++) Bb(b[a]);
      }
    }
    function Gb(a, b) {
      return a(b);
    }
    function Hb() {
    }
    var Ib = false;
    function Jb(a, b, c) {
      if (Ib) return a(b, c);
      Ib = true;
      try {
        return Gb(a, b, c);
      } finally {
        if (Ib = false, null !== zb || null !== Ab) Hb(), Fb();
      }
    }
    function Kb(a, b) {
      var c = a.stateNode;
      if (null === c) return null;
      var d = Db(c);
      if (null === d) return null;
      c = d[b];
      a: switch (b) {
        case "onClick":
        case "onClickCapture":
        case "onDoubleClick":
        case "onDoubleClickCapture":
        case "onMouseDown":
        case "onMouseDownCapture":
        case "onMouseMove":
        case "onMouseMoveCapture":
        case "onMouseUp":
        case "onMouseUpCapture":
        case "onMouseEnter":
          (d = !d.disabled) || (a = a.type, d = !("button" === a || "input" === a || "select" === a || "textarea" === a));
          a = !d;
          break a;
        default:
          a = false;
      }
      if (a) return null;
      if (c && "function" !== typeof c) throw Error(p(231, b, typeof c));
      return c;
    }
    var Lb = false;
    if (ia) try {
      var Mb = {};
      Object.defineProperty(Mb, "passive", { get: function() {
        Lb = true;
      } });
      window.addEventListener("test", Mb, Mb);
      window.removeEventListener("test", Mb, Mb);
    } catch (a) {
      Lb = false;
    }
    function Nb(a, b, c, d, e, f, g, h, k) {
      var l = Array.prototype.slice.call(arguments, 3);
      try {
        b.apply(c, l);
      } catch (m) {
        this.onError(m);
      }
    }
    var Ob = false, Pb = null, Qb = false, Rb = null, Sb = { onError: function(a) {
      Ob = true;
      Pb = a;
    } };
    function Tb(a, b, c, d, e, f, g, h, k) {
      Ob = false;
      Pb = null;
      Nb.apply(Sb, arguments);
    }
    function Ub(a, b, c, d, e, f, g, h, k) {
      Tb.apply(this, arguments);
      if (Ob) {
        if (Ob) {
          var l = Pb;
          Ob = false;
          Pb = null;
        } else throw Error(p(198));
        Qb || (Qb = true, Rb = l);
      }
    }
    function Vb(a) {
      var b = a, c = a;
      if (a.alternate) for (; b.return; ) b = b.return;
      else {
        a = b;
        do
          b = a, 0 !== (b.flags & 4098) && (c = b.return), a = b.return;
        while (a);
      }
      return 3 === b.tag ? c : null;
    }
    function Wb(a) {
      if (13 === a.tag) {
        var b = a.memoizedState;
        null === b && (a = a.alternate, null !== a && (b = a.memoizedState));
        if (null !== b) return b.dehydrated;
      }
      return null;
    }
    function Xb(a) {
      if (Vb(a) !== a) throw Error(p(188));
    }
    function Yb(a) {
      var b = a.alternate;
      if (!b) {
        b = Vb(a);
        if (null === b) throw Error(p(188));
        return b !== a ? null : a;
      }
      for (var c = a, d = b; ; ) {
        var e = c.return;
        if (null === e) break;
        var f = e.alternate;
        if (null === f) {
          d = e.return;
          if (null !== d) {
            c = d;
            continue;
          }
          break;
        }
        if (e.child === f.child) {
          for (f = e.child; f; ) {
            if (f === c) return Xb(e), a;
            if (f === d) return Xb(e), b;
            f = f.sibling;
          }
          throw Error(p(188));
        }
        if (c.return !== d.return) c = e, d = f;
        else {
          for (var g = false, h = e.child; h; ) {
            if (h === c) {
              g = true;
              c = e;
              d = f;
              break;
            }
            if (h === d) {
              g = true;
              d = e;
              c = f;
              break;
            }
            h = h.sibling;
          }
          if (!g) {
            for (h = f.child; h; ) {
              if (h === c) {
                g = true;
                c = f;
                d = e;
                break;
              }
              if (h === d) {
                g = true;
                d = f;
                c = e;
                break;
              }
              h = h.sibling;
            }
            if (!g) throw Error(p(189));
          }
        }
        if (c.alternate !== d) throw Error(p(190));
      }
      if (3 !== c.tag) throw Error(p(188));
      return c.stateNode.current === c ? a : b;
    }
    function Zb(a) {
      a = Yb(a);
      return null !== a ? $b(a) : null;
    }
    function $b(a) {
      if (5 === a.tag || 6 === a.tag) return a;
      for (a = a.child; null !== a; ) {
        var b = $b(a);
        if (null !== b) return b;
        a = a.sibling;
      }
      return null;
    }
    var ac = ca.unstable_scheduleCallback, bc = ca.unstable_cancelCallback, cc = ca.unstable_shouldYield, dc = ca.unstable_requestPaint, B = ca.unstable_now, ec2 = ca.unstable_getCurrentPriorityLevel, fc = ca.unstable_ImmediatePriority, gc = ca.unstable_UserBlockingPriority, hc = ca.unstable_NormalPriority, ic = ca.unstable_LowPriority, jc = ca.unstable_IdlePriority, kc = null, lc = null;
    function mc(a) {
      if (lc && "function" === typeof lc.onCommitFiberRoot) try {
        lc.onCommitFiberRoot(kc, a, void 0, 128 === (a.current.flags & 128));
      } catch (b) {
      }
    }
    var oc = Math.clz32 ? Math.clz32 : nc, pc = Math.log, qc = Math.LN2;
    function nc(a) {
      a >>>= 0;
      return 0 === a ? 32 : 31 - (pc(a) / qc | 0) | 0;
    }
    var rc = 64, sc = 4194304;
    function tc(a) {
      switch (a & -a) {
        case 1:
          return 1;
        case 2:
          return 2;
        case 4:
          return 4;
        case 8:
          return 8;
        case 16:
          return 16;
        case 32:
          return 32;
        case 64:
        case 128:
        case 256:
        case 512:
        case 1024:
        case 2048:
        case 4096:
        case 8192:
        case 16384:
        case 32768:
        case 65536:
        case 131072:
        case 262144:
        case 524288:
        case 1048576:
        case 2097152:
          return a & 4194240;
        case 4194304:
        case 8388608:
        case 16777216:
        case 33554432:
        case 67108864:
          return a & 130023424;
        case 134217728:
          return 134217728;
        case 268435456:
          return 268435456;
        case 536870912:
          return 536870912;
        case 1073741824:
          return 1073741824;
        default:
          return a;
      }
    }
    function uc(a, b) {
      var c = a.pendingLanes;
      if (0 === c) return 0;
      var d = 0, e = a.suspendedLanes, f = a.pingedLanes, g = c & 268435455;
      if (0 !== g) {
        var h = g & ~e;
        0 !== h ? d = tc(h) : (f &= g, 0 !== f && (d = tc(f)));
      } else g = c & ~e, 0 !== g ? d = tc(g) : 0 !== f && (d = tc(f));
      if (0 === d) return 0;
      if (0 !== b && b !== d && 0 === (b & e) && (e = d & -d, f = b & -b, e >= f || 16 === e && 0 !== (f & 4194240))) return b;
      0 !== (d & 4) && (d |= c & 16);
      b = a.entangledLanes;
      if (0 !== b) for (a = a.entanglements, b &= d; 0 < b; ) c = 31 - oc(b), e = 1 << c, d |= a[c], b &= ~e;
      return d;
    }
    function vc(a, b) {
      switch (a) {
        case 1:
        case 2:
        case 4:
          return b + 250;
        case 8:
        case 16:
        case 32:
        case 64:
        case 128:
        case 256:
        case 512:
        case 1024:
        case 2048:
        case 4096:
        case 8192:
        case 16384:
        case 32768:
        case 65536:
        case 131072:
        case 262144:
        case 524288:
        case 1048576:
        case 2097152:
          return b + 5e3;
        case 4194304:
        case 8388608:
        case 16777216:
        case 33554432:
        case 67108864:
          return -1;
        case 134217728:
        case 268435456:
        case 536870912:
        case 1073741824:
          return -1;
        default:
          return -1;
      }
    }
    function wc(a, b) {
      for (var c = a.suspendedLanes, d = a.pingedLanes, e = a.expirationTimes, f = a.pendingLanes; 0 < f; ) {
        var g = 31 - oc(f), h = 1 << g, k = e[g];
        if (-1 === k) {
          if (0 === (h & c) || 0 !== (h & d)) e[g] = vc(h, b);
        } else k <= b && (a.expiredLanes |= h);
        f &= ~h;
      }
    }
    function xc(a) {
      a = a.pendingLanes & -1073741825;
      return 0 !== a ? a : a & 1073741824 ? 1073741824 : 0;
    }
    function yc() {
      var a = rc;
      rc <<= 1;
      0 === (rc & 4194240) && (rc = 64);
      return a;
    }
    function zc(a) {
      for (var b = [], c = 0; 31 > c; c++) b.push(a);
      return b;
    }
    function Ac(a, b, c) {
      a.pendingLanes |= b;
      536870912 !== b && (a.suspendedLanes = 0, a.pingedLanes = 0);
      a = a.eventTimes;
      b = 31 - oc(b);
      a[b] = c;
    }
    function Bc(a, b) {
      var c = a.pendingLanes & ~b;
      a.pendingLanes = b;
      a.suspendedLanes = 0;
      a.pingedLanes = 0;
      a.expiredLanes &= b;
      a.mutableReadLanes &= b;
      a.entangledLanes &= b;
      b = a.entanglements;
      var d = a.eventTimes;
      for (a = a.expirationTimes; 0 < c; ) {
        var e = 31 - oc(c), f = 1 << e;
        b[e] = 0;
        d[e] = -1;
        a[e] = -1;
        c &= ~f;
      }
    }
    function Cc(a, b) {
      var c = a.entangledLanes |= b;
      for (a = a.entanglements; c; ) {
        var d = 31 - oc(c), e = 1 << d;
        e & b | a[d] & b && (a[d] |= b);
        c &= ~e;
      }
    }
    var C = 0;
    function Dc(a) {
      a &= -a;
      return 1 < a ? 4 < a ? 0 !== (a & 268435455) ? 16 : 536870912 : 4 : 1;
    }
    var Ec, Fc, Gc, Hc, Ic, Jc = false, Kc = [], Lc = null, Mc = null, Nc = null, Oc = /* @__PURE__ */ new Map(), Pc = /* @__PURE__ */ new Map(), Qc = [], Rc = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset submit".split(" ");
    function Sc(a, b) {
      switch (a) {
        case "focusin":
        case "focusout":
          Lc = null;
          break;
        case "dragenter":
        case "dragleave":
          Mc = null;
          break;
        case "mouseover":
        case "mouseout":
          Nc = null;
          break;
        case "pointerover":
        case "pointerout":
          Oc.delete(b.pointerId);
          break;
        case "gotpointercapture":
        case "lostpointercapture":
          Pc.delete(b.pointerId);
      }
    }
    function Tc(a, b, c, d, e, f) {
      if (null === a || a.nativeEvent !== f) return a = { blockedOn: b, domEventName: c, eventSystemFlags: d, nativeEvent: f, targetContainers: [e] }, null !== b && (b = Cb(b), null !== b && Fc(b)), a;
      a.eventSystemFlags |= d;
      b = a.targetContainers;
      null !== e && -1 === b.indexOf(e) && b.push(e);
      return a;
    }
    function Uc(a, b, c, d, e) {
      switch (b) {
        case "focusin":
          return Lc = Tc(Lc, a, b, c, d, e), true;
        case "dragenter":
          return Mc = Tc(Mc, a, b, c, d, e), true;
        case "mouseover":
          return Nc = Tc(Nc, a, b, c, d, e), true;
        case "pointerover":
          var f = e.pointerId;
          Oc.set(f, Tc(Oc.get(f) || null, a, b, c, d, e));
          return true;
        case "gotpointercapture":
          return f = e.pointerId, Pc.set(f, Tc(Pc.get(f) || null, a, b, c, d, e)), true;
      }
      return false;
    }
    function Vc(a) {
      var b = Wc(a.target);
      if (null !== b) {
        var c = Vb(b);
        if (null !== c) {
          if (b = c.tag, 13 === b) {
            if (b = Wb(c), null !== b) {
              a.blockedOn = b;
              Ic(a.priority, function() {
                Gc(c);
              });
              return;
            }
          } else if (3 === b && c.stateNode.current.memoizedState.isDehydrated) {
            a.blockedOn = 3 === c.tag ? c.stateNode.containerInfo : null;
            return;
          }
        }
      }
      a.blockedOn = null;
    }
    function Xc(a) {
      if (null !== a.blockedOn) return false;
      for (var b = a.targetContainers; 0 < b.length; ) {
        var c = Yc(a.domEventName, a.eventSystemFlags, b[0], a.nativeEvent);
        if (null === c) {
          c = a.nativeEvent;
          var d = new c.constructor(c.type, c);
          wb = d;
          c.target.dispatchEvent(d);
          wb = null;
        } else return b = Cb(c), null !== b && Fc(b), a.blockedOn = c, false;
        b.shift();
      }
      return true;
    }
    function Zc(a, b, c) {
      Xc(a) && c.delete(b);
    }
    function $c() {
      Jc = false;
      null !== Lc && Xc(Lc) && (Lc = null);
      null !== Mc && Xc(Mc) && (Mc = null);
      null !== Nc && Xc(Nc) && (Nc = null);
      Oc.forEach(Zc);
      Pc.forEach(Zc);
    }
    function ad(a, b) {
      a.blockedOn === b && (a.blockedOn = null, Jc || (Jc = true, ca.unstable_scheduleCallback(ca.unstable_NormalPriority, $c)));
    }
    function bd(a) {
      function b(b3) {
        return ad(b3, a);
      }
      if (0 < Kc.length) {
        ad(Kc[0], a);
        for (var c = 1; c < Kc.length; c++) {
          var d = Kc[c];
          d.blockedOn === a && (d.blockedOn = null);
        }
      }
      null !== Lc && ad(Lc, a);
      null !== Mc && ad(Mc, a);
      null !== Nc && ad(Nc, a);
      Oc.forEach(b);
      Pc.forEach(b);
      for (c = 0; c < Qc.length; c++) d = Qc[c], d.blockedOn === a && (d.blockedOn = null);
      for (; 0 < Qc.length && (c = Qc[0], null === c.blockedOn); ) Vc(c), null === c.blockedOn && Qc.shift();
    }
    var cd = ua.ReactCurrentBatchConfig, dd = true;
    function ed(a, b, c, d) {
      var e = C, f = cd.transition;
      cd.transition = null;
      try {
        C = 1, fd2(a, b, c, d);
      } finally {
        C = e, cd.transition = f;
      }
    }
    function gd(a, b, c, d) {
      var e = C, f = cd.transition;
      cd.transition = null;
      try {
        C = 4, fd2(a, b, c, d);
      } finally {
        C = e, cd.transition = f;
      }
    }
    function fd2(a, b, c, d) {
      if (dd) {
        var e = Yc(a, b, c, d);
        if (null === e) hd(a, b, d, id, c), Sc(a, d);
        else if (Uc(e, a, b, c, d)) d.stopPropagation();
        else if (Sc(a, d), b & 4 && -1 < Rc.indexOf(a)) {
          for (; null !== e; ) {
            var f = Cb(e);
            null !== f && Ec(f);
            f = Yc(a, b, c, d);
            null === f && hd(a, b, d, id, c);
            if (f === e) break;
            e = f;
          }
          null !== e && d.stopPropagation();
        } else hd(a, b, d, null, c);
      }
    }
    var id = null;
    function Yc(a, b, c, d) {
      id = null;
      a = xb(d);
      a = Wc(a);
      if (null !== a) if (b = Vb(a), null === b) a = null;
      else if (c = b.tag, 13 === c) {
        a = Wb(b);
        if (null !== a) return a;
        a = null;
      } else if (3 === c) {
        if (b.stateNode.current.memoizedState.isDehydrated) return 3 === b.tag ? b.stateNode.containerInfo : null;
        a = null;
      } else b !== a && (a = null);
      id = a;
      return null;
    }
    function jd(a) {
      switch (a) {
        case "cancel":
        case "click":
        case "close":
        case "contextmenu":
        case "copy":
        case "cut":
        case "auxclick":
        case "dblclick":
        case "dragend":
        case "dragstart":
        case "drop":
        case "focusin":
        case "focusout":
        case "input":
        case "invalid":
        case "keydown":
        case "keypress":
        case "keyup":
        case "mousedown":
        case "mouseup":
        case "paste":
        case "pause":
        case "play":
        case "pointercancel":
        case "pointerdown":
        case "pointerup":
        case "ratechange":
        case "reset":
        case "resize":
        case "seeked":
        case "submit":
        case "touchcancel":
        case "touchend":
        case "touchstart":
        case "volumechange":
        case "change":
        case "selectionchange":
        case "textInput":
        case "compositionstart":
        case "compositionend":
        case "compositionupdate":
        case "beforeblur":
        case "afterblur":
        case "beforeinput":
        case "blur":
        case "fullscreenchange":
        case "focus":
        case "hashchange":
        case "popstate":
        case "select":
        case "selectstart":
          return 1;
        case "drag":
        case "dragenter":
        case "dragexit":
        case "dragleave":
        case "dragover":
        case "mousemove":
        case "mouseout":
        case "mouseover":
        case "pointermove":
        case "pointerout":
        case "pointerover":
        case "scroll":
        case "toggle":
        case "touchmove":
        case "wheel":
        case "mouseenter":
        case "mouseleave":
        case "pointerenter":
        case "pointerleave":
          return 4;
        case "message":
          switch (ec2()) {
            case fc:
              return 1;
            case gc:
              return 4;
            case hc:
            case ic:
              return 16;
            case jc:
              return 536870912;
            default:
              return 16;
          }
        default:
          return 16;
      }
    }
    var kd = null, ld = null, md = null;
    function nd() {
      if (md) return md;
      var a, b = ld, c = b.length, d, e = "value" in kd ? kd.value : kd.textContent, f = e.length;
      for (a = 0; a < c && b[a] === e[a]; a++) ;
      var g = c - a;
      for (d = 1; d <= g && b[c - d] === e[f - d]; d++) ;
      return md = e.slice(a, 1 < d ? 1 - d : void 0);
    }
    function od(a) {
      var b = a.keyCode;
      "charCode" in a ? (a = a.charCode, 0 === a && 13 === b && (a = 13)) : a = b;
      10 === a && (a = 13);
      return 32 <= a || 13 === a ? a : 0;
    }
    function pd() {
      return true;
    }
    function qd() {
      return false;
    }
    function rd(a) {
      function b(b3, d, e, f, g) {
        this._reactName = b3;
        this._targetInst = e;
        this.type = d;
        this.nativeEvent = f;
        this.target = g;
        this.currentTarget = null;
        for (var c in a) a.hasOwnProperty(c) && (b3 = a[c], this[c] = b3 ? b3(f) : f[c]);
        this.isDefaultPrevented = (null != f.defaultPrevented ? f.defaultPrevented : false === f.returnValue) ? pd : qd;
        this.isPropagationStopped = qd;
        return this;
      }
      A(b.prototype, { preventDefault: function() {
        this.defaultPrevented = true;
        var a2 = this.nativeEvent;
        a2 && (a2.preventDefault ? a2.preventDefault() : "unknown" !== typeof a2.returnValue && (a2.returnValue = false), this.isDefaultPrevented = pd);
      }, stopPropagation: function() {
        var a2 = this.nativeEvent;
        a2 && (a2.stopPropagation ? a2.stopPropagation() : "unknown" !== typeof a2.cancelBubble && (a2.cancelBubble = true), this.isPropagationStopped = pd);
      }, persist: function() {
      }, isPersistent: pd });
      return b;
    }
    var sd = { eventPhase: 0, bubbles: 0, cancelable: 0, timeStamp: function(a) {
      return a.timeStamp || Date.now();
    }, defaultPrevented: 0, isTrusted: 0 }, td2 = rd(sd), ud = A({}, sd, { view: 0, detail: 0 }), vd = rd(ud), wd, xd, yd, Ad = A({}, ud, { screenX: 0, screenY: 0, clientX: 0, clientY: 0, pageX: 0, pageY: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, getModifierState: zd, button: 0, buttons: 0, relatedTarget: function(a) {
      return void 0 === a.relatedTarget ? a.fromElement === a.srcElement ? a.toElement : a.fromElement : a.relatedTarget;
    }, movementX: function(a) {
      if ("movementX" in a) return a.movementX;
      a !== yd && (yd && "mousemove" === a.type ? (wd = a.screenX - yd.screenX, xd = a.screenY - yd.screenY) : xd = wd = 0, yd = a);
      return wd;
    }, movementY: function(a) {
      return "movementY" in a ? a.movementY : xd;
    } }), Bd = rd(Ad), Cd = A({}, Ad, { dataTransfer: 0 }), Dd = rd(Cd), Ed = A({}, ud, { relatedTarget: 0 }), Fd = rd(Ed), Gd = A({}, sd, { animationName: 0, elapsedTime: 0, pseudoElement: 0 }), Hd = rd(Gd), Id = A({}, sd, { clipboardData: function(a) {
      return "clipboardData" in a ? a.clipboardData : window.clipboardData;
    } }), Jd = rd(Id), Kd = A({}, sd, { data: 0 }), Ld = rd(Kd), Md = {
      Esc: "Escape",
      Spacebar: " ",
      Left: "ArrowLeft",
      Up: "ArrowUp",
      Right: "ArrowRight",
      Down: "ArrowDown",
      Del: "Delete",
      Win: "OS",
      Menu: "ContextMenu",
      Apps: "ContextMenu",
      Scroll: "ScrollLock",
      MozPrintableKey: "Unidentified"
    }, Nd = {
      8: "Backspace",
      9: "Tab",
      12: "Clear",
      13: "Enter",
      16: "Shift",
      17: "Control",
      18: "Alt",
      19: "Pause",
      20: "CapsLock",
      27: "Escape",
      32: " ",
      33: "PageUp",
      34: "PageDown",
      35: "End",
      36: "Home",
      37: "ArrowLeft",
      38: "ArrowUp",
      39: "ArrowRight",
      40: "ArrowDown",
      45: "Insert",
      46: "Delete",
      112: "F1",
      113: "F2",
      114: "F3",
      115: "F4",
      116: "F5",
      117: "F6",
      118: "F7",
      119: "F8",
      120: "F9",
      121: "F10",
      122: "F11",
      123: "F12",
      144: "NumLock",
      145: "ScrollLock",
      224: "Meta"
    }, Od = { Alt: "altKey", Control: "ctrlKey", Meta: "metaKey", Shift: "shiftKey" };
    function Pd(a) {
      var b = this.nativeEvent;
      return b.getModifierState ? b.getModifierState(a) : (a = Od[a]) ? !!b[a] : false;
    }
    function zd() {
      return Pd;
    }
    var Qd = A({}, ud, { key: function(a) {
      if (a.key) {
        var b = Md[a.key] || a.key;
        if ("Unidentified" !== b) return b;
      }
      return "keypress" === a.type ? (a = od(a), 13 === a ? "Enter" : String.fromCharCode(a)) : "keydown" === a.type || "keyup" === a.type ? Nd[a.keyCode] || "Unidentified" : "";
    }, code: 0, location: 0, ctrlKey: 0, shiftKey: 0, altKey: 0, metaKey: 0, repeat: 0, locale: 0, getModifierState: zd, charCode: function(a) {
      return "keypress" === a.type ? od(a) : 0;
    }, keyCode: function(a) {
      return "keydown" === a.type || "keyup" === a.type ? a.keyCode : 0;
    }, which: function(a) {
      return "keypress" === a.type ? od(a) : "keydown" === a.type || "keyup" === a.type ? a.keyCode : 0;
    } }), Rd = rd(Qd), Sd = A({}, Ad, { pointerId: 0, width: 0, height: 0, pressure: 0, tangentialPressure: 0, tiltX: 0, tiltY: 0, twist: 0, pointerType: 0, isPrimary: 0 }), Td = rd(Sd), Ud = A({}, ud, { touches: 0, targetTouches: 0, changedTouches: 0, altKey: 0, metaKey: 0, ctrlKey: 0, shiftKey: 0, getModifierState: zd }), Vd = rd(Ud), Wd = A({}, sd, { propertyName: 0, elapsedTime: 0, pseudoElement: 0 }), Xd = rd(Wd), Yd = A({}, Ad, {
      deltaX: function(a) {
        return "deltaX" in a ? a.deltaX : "wheelDeltaX" in a ? -a.wheelDeltaX : 0;
      },
      deltaY: function(a) {
        return "deltaY" in a ? a.deltaY : "wheelDeltaY" in a ? -a.wheelDeltaY : "wheelDelta" in a ? -a.wheelDelta : 0;
      },
      deltaZ: 0,
      deltaMode: 0
    }), Zd = rd(Yd), $d = [9, 13, 27, 32], ae = ia && "CompositionEvent" in window, be = null;
    ia && "documentMode" in document && (be = document.documentMode);
    var ce = ia && "TextEvent" in window && !be, de = ia && (!ae || be && 8 < be && 11 >= be), ee = String.fromCharCode(32), fe = false;
    function ge(a, b) {
      switch (a) {
        case "keyup":
          return -1 !== $d.indexOf(b.keyCode);
        case "keydown":
          return 229 !== b.keyCode;
        case "keypress":
        case "mousedown":
        case "focusout":
          return true;
        default:
          return false;
      }
    }
    function he(a) {
      a = a.detail;
      return "object" === typeof a && "data" in a ? a.data : null;
    }
    var ie = false;
    function je(a, b) {
      switch (a) {
        case "compositionend":
          return he(b);
        case "keypress":
          if (32 !== b.which) return null;
          fe = true;
          return ee;
        case "textInput":
          return a = b.data, a === ee && fe ? null : a;
        default:
          return null;
      }
    }
    function ke(a, b) {
      if (ie) return "compositionend" === a || !ae && ge(a, b) ? (a = nd(), md = ld = kd = null, ie = false, a) : null;
      switch (a) {
        case "paste":
          return null;
        case "keypress":
          if (!(b.ctrlKey || b.altKey || b.metaKey) || b.ctrlKey && b.altKey) {
            if (b.char && 1 < b.char.length) return b.char;
            if (b.which) return String.fromCharCode(b.which);
          }
          return null;
        case "compositionend":
          return de && "ko" !== b.locale ? null : b.data;
        default:
          return null;
      }
    }
    var le = { color: true, date: true, datetime: true, "datetime-local": true, email: true, month: true, number: true, password: true, range: true, search: true, tel: true, text: true, time: true, url: true, week: true };
    function me(a) {
      var b = a && a.nodeName && a.nodeName.toLowerCase();
      return "input" === b ? !!le[a.type] : "textarea" === b ? true : false;
    }
    function ne(a, b, c, d) {
      Eb(d);
      b = oe(b, "onChange");
      0 < b.length && (c = new td2("onChange", "change", null, c, d), a.push({ event: c, listeners: b }));
    }
    var pe = null, qe = null;
    function re(a) {
      se(a, 0);
    }
    function te(a) {
      var b = ue(a);
      if (Wa(b)) return a;
    }
    function ve(a, b) {
      if ("change" === a) return b;
    }
    var we = false;
    if (ia) {
      var xe;
      if (ia) {
        var ye = "oninput" in document;
        if (!ye) {
          var ze = document.createElement("div");
          ze.setAttribute("oninput", "return;");
          ye = "function" === typeof ze.oninput;
        }
        xe = ye;
      } else xe = false;
      we = xe && (!document.documentMode || 9 < document.documentMode);
    }
    function Ae() {
      pe && (pe.detachEvent("onpropertychange", Be), qe = pe = null);
    }
    function Be(a) {
      if ("value" === a.propertyName && te(qe)) {
        var b = [];
        ne(b, qe, a, xb(a));
        Jb(re, b);
      }
    }
    function Ce(a, b, c) {
      "focusin" === a ? (Ae(), pe = b, qe = c, pe.attachEvent("onpropertychange", Be)) : "focusout" === a && Ae();
    }
    function De(a) {
      if ("selectionchange" === a || "keyup" === a || "keydown" === a) return te(qe);
    }
    function Ee(a, b) {
      if ("click" === a) return te(b);
    }
    function Fe(a, b) {
      if ("input" === a || "change" === a) return te(b);
    }
    function Ge(a, b) {
      return a === b && (0 !== a || 1 / a === 1 / b) || a !== a && b !== b;
    }
    var He = "function" === typeof Object.is ? Object.is : Ge;
    function Ie(a, b) {
      if (He(a, b)) return true;
      if ("object" !== typeof a || null === a || "object" !== typeof b || null === b) return false;
      var c = Object.keys(a), d = Object.keys(b);
      if (c.length !== d.length) return false;
      for (d = 0; d < c.length; d++) {
        var e = c[d];
        if (!ja.call(b, e) || !He(a[e], b[e])) return false;
      }
      return true;
    }
    function Je(a) {
      for (; a && a.firstChild; ) a = a.firstChild;
      return a;
    }
    function Ke(a, b) {
      var c = Je(a);
      a = 0;
      for (var d; c; ) {
        if (3 === c.nodeType) {
          d = a + c.textContent.length;
          if (a <= b && d >= b) return { node: c, offset: b - a };
          a = d;
        }
        a: {
          for (; c; ) {
            if (c.nextSibling) {
              c = c.nextSibling;
              break a;
            }
            c = c.parentNode;
          }
          c = void 0;
        }
        c = Je(c);
      }
    }
    function Le(a, b) {
      return a && b ? a === b ? true : a && 3 === a.nodeType ? false : b && 3 === b.nodeType ? Le(a, b.parentNode) : "contains" in a ? a.contains(b) : a.compareDocumentPosition ? !!(a.compareDocumentPosition(b) & 16) : false : false;
    }
    function Me() {
      for (var a = window, b = Xa(); b instanceof a.HTMLIFrameElement; ) {
        try {
          var c = "string" === typeof b.contentWindow.location.href;
        } catch (d) {
          c = false;
        }
        if (c) a = b.contentWindow;
        else break;
        b = Xa(a.document);
      }
      return b;
    }
    function Ne(a) {
      var b = a && a.nodeName && a.nodeName.toLowerCase();
      return b && ("input" === b && ("text" === a.type || "search" === a.type || "tel" === a.type || "url" === a.type || "password" === a.type) || "textarea" === b || "true" === a.contentEditable);
    }
    function Oe(a) {
      var b = Me(), c = a.focusedElem, d = a.selectionRange;
      if (b !== c && c && c.ownerDocument && Le(c.ownerDocument.documentElement, c)) {
        if (null !== d && Ne(c)) {
          if (b = d.start, a = d.end, void 0 === a && (a = b), "selectionStart" in c) c.selectionStart = b, c.selectionEnd = Math.min(a, c.value.length);
          else if (a = (b = c.ownerDocument || document) && b.defaultView || window, a.getSelection) {
            a = a.getSelection();
            var e = c.textContent.length, f = Math.min(d.start, e);
            d = void 0 === d.end ? f : Math.min(d.end, e);
            !a.extend && f > d && (e = d, d = f, f = e);
            e = Ke(c, f);
            var g = Ke(
              c,
              d
            );
            e && g && (1 !== a.rangeCount || a.anchorNode !== e.node || a.anchorOffset !== e.offset || a.focusNode !== g.node || a.focusOffset !== g.offset) && (b = b.createRange(), b.setStart(e.node, e.offset), a.removeAllRanges(), f > d ? (a.addRange(b), a.extend(g.node, g.offset)) : (b.setEnd(g.node, g.offset), a.addRange(b)));
          }
        }
        b = [];
        for (a = c; a = a.parentNode; ) 1 === a.nodeType && b.push({ element: a, left: a.scrollLeft, top: a.scrollTop });
        "function" === typeof c.focus && c.focus();
        for (c = 0; c < b.length; c++) a = b[c], a.element.scrollLeft = a.left, a.element.scrollTop = a.top;
      }
    }
    var Pe = ia && "documentMode" in document && 11 >= document.documentMode, Qe = null, Re = null, Se = null, Te = false;
    function Ue(a, b, c) {
      var d = c.window === c ? c.document : 9 === c.nodeType ? c : c.ownerDocument;
      Te || null == Qe || Qe !== Xa(d) || (d = Qe, "selectionStart" in d && Ne(d) ? d = { start: d.selectionStart, end: d.selectionEnd } : (d = (d.ownerDocument && d.ownerDocument.defaultView || window).getSelection(), d = { anchorNode: d.anchorNode, anchorOffset: d.anchorOffset, focusNode: d.focusNode, focusOffset: d.focusOffset }), Se && Ie(Se, d) || (Se = d, d = oe(Re, "onSelect"), 0 < d.length && (b = new td2("onSelect", "select", null, b, c), a.push({ event: b, listeners: d }), b.target = Qe)));
    }
    function Ve(a, b) {
      var c = {};
      c[a.toLowerCase()] = b.toLowerCase();
      c["Webkit" + a] = "webkit" + b;
      c["Moz" + a] = "moz" + b;
      return c;
    }
    var We = { animationend: Ve("Animation", "AnimationEnd"), animationiteration: Ve("Animation", "AnimationIteration"), animationstart: Ve("Animation", "AnimationStart"), transitionend: Ve("Transition", "TransitionEnd") }, Xe = {}, Ye = {};
    ia && (Ye = document.createElement("div").style, "AnimationEvent" in window || (delete We.animationend.animation, delete We.animationiteration.animation, delete We.animationstart.animation), "TransitionEvent" in window || delete We.transitionend.transition);
    function Ze(a) {
      if (Xe[a]) return Xe[a];
      if (!We[a]) return a;
      var b = We[a], c;
      for (c in b) if (b.hasOwnProperty(c) && c in Ye) return Xe[a] = b[c];
      return a;
    }
    var $e = Ze("animationend"), af = Ze("animationiteration"), bf = Ze("animationstart"), cf = Ze("transitionend"), df = /* @__PURE__ */ new Map(), ef = "abort auxClick cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");
    function ff(a, b) {
      df.set(a, b);
      fa(b, [a]);
    }
    for (var gf = 0; gf < ef.length; gf++) {
      var hf = ef[gf], jf = hf.toLowerCase(), kf = hf[0].toUpperCase() + hf.slice(1);
      ff(jf, "on" + kf);
    }
    ff($e, "onAnimationEnd");
    ff(af, "onAnimationIteration");
    ff(bf, "onAnimationStart");
    ff("dblclick", "onDoubleClick");
    ff("focusin", "onFocus");
    ff("focusout", "onBlur");
    ff(cf, "onTransitionEnd");
    ha("onMouseEnter", ["mouseout", "mouseover"]);
    ha("onMouseLeave", ["mouseout", "mouseover"]);
    ha("onPointerEnter", ["pointerout", "pointerover"]);
    ha("onPointerLeave", ["pointerout", "pointerover"]);
    fa("onChange", "change click focusin focusout input keydown keyup selectionchange".split(" "));
    fa("onSelect", "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));
    fa("onBeforeInput", ["compositionend", "keypress", "textInput", "paste"]);
    fa("onCompositionEnd", "compositionend focusout keydown keypress keyup mousedown".split(" "));
    fa("onCompositionStart", "compositionstart focusout keydown keypress keyup mousedown".split(" "));
    fa("onCompositionUpdate", "compositionupdate focusout keydown keypress keyup mousedown".split(" "));
    var lf = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "), mf = new Set("cancel close invalid load scroll toggle".split(" ").concat(lf));
    function nf(a, b, c) {
      var d = a.type || "unknown-event";
      a.currentTarget = c;
      Ub(d, b, void 0, a);
      a.currentTarget = null;
    }
    function se(a, b) {
      b = 0 !== (b & 4);
      for (var c = 0; c < a.length; c++) {
        var d = a[c], e = d.event;
        d = d.listeners;
        a: {
          var f = void 0;
          if (b) for (var g = d.length - 1; 0 <= g; g--) {
            var h = d[g], k = h.instance, l = h.currentTarget;
            h = h.listener;
            if (k !== f && e.isPropagationStopped()) break a;
            nf(e, h, l);
            f = k;
          }
          else for (g = 0; g < d.length; g++) {
            h = d[g];
            k = h.instance;
            l = h.currentTarget;
            h = h.listener;
            if (k !== f && e.isPropagationStopped()) break a;
            nf(e, h, l);
            f = k;
          }
        }
      }
      if (Qb) throw a = Rb, Qb = false, Rb = null, a;
    }
    function D(a, b) {
      var c = b[of];
      void 0 === c && (c = b[of] = /* @__PURE__ */ new Set());
      var d = a + "__bubble";
      c.has(d) || (pf(b, a, 2, false), c.add(d));
    }
    function qf(a, b, c) {
      var d = 0;
      b && (d |= 4);
      pf(c, a, d, b);
    }
    var rf = "_reactListening" + Math.random().toString(36).slice(2);
    function sf(a) {
      if (!a[rf]) {
        a[rf] = true;
        da.forEach(function(b3) {
          "selectionchange" !== b3 && (mf.has(b3) || qf(b3, false, a), qf(b3, true, a));
        });
        var b = 9 === a.nodeType ? a : a.ownerDocument;
        null === b || b[rf] || (b[rf] = true, qf("selectionchange", false, b));
      }
    }
    function pf(a, b, c, d) {
      switch (jd(b)) {
        case 1:
          var e = ed;
          break;
        case 4:
          e = gd;
          break;
        default:
          e = fd2;
      }
      c = e.bind(null, b, c, a);
      e = void 0;
      !Lb || "touchstart" !== b && "touchmove" !== b && "wheel" !== b || (e = true);
      d ? void 0 !== e ? a.addEventListener(b, c, { capture: true, passive: e }) : a.addEventListener(b, c, true) : void 0 !== e ? a.addEventListener(b, c, { passive: e }) : a.addEventListener(b, c, false);
    }
    function hd(a, b, c, d, e) {
      var f = d;
      if (0 === (b & 1) && 0 === (b & 2) && null !== d) a: for (; ; ) {
        if (null === d) return;
        var g = d.tag;
        if (3 === g || 4 === g) {
          var h = d.stateNode.containerInfo;
          if (h === e || 8 === h.nodeType && h.parentNode === e) break;
          if (4 === g) for (g = d.return; null !== g; ) {
            var k = g.tag;
            if (3 === k || 4 === k) {
              if (k = g.stateNode.containerInfo, k === e || 8 === k.nodeType && k.parentNode === e) return;
            }
            g = g.return;
          }
          for (; null !== h; ) {
            g = Wc(h);
            if (null === g) return;
            k = g.tag;
            if (5 === k || 6 === k) {
              d = f = g;
              continue a;
            }
            h = h.parentNode;
          }
        }
        d = d.return;
      }
      Jb(function() {
        var d2 = f, e2 = xb(c), g2 = [];
        a: {
          var h2 = df.get(a);
          if (void 0 !== h2) {
            var k2 = td2, n = a;
            switch (a) {
              case "keypress":
                if (0 === od(c)) break a;
              case "keydown":
              case "keyup":
                k2 = Rd;
                break;
              case "focusin":
                n = "focus";
                k2 = Fd;
                break;
              case "focusout":
                n = "blur";
                k2 = Fd;
                break;
              case "beforeblur":
              case "afterblur":
                k2 = Fd;
                break;
              case "click":
                if (2 === c.button) break a;
              case "auxclick":
              case "dblclick":
              case "mousedown":
              case "mousemove":
              case "mouseup":
              case "mouseout":
              case "mouseover":
              case "contextmenu":
                k2 = Bd;
                break;
              case "drag":
              case "dragend":
              case "dragenter":
              case "dragexit":
              case "dragleave":
              case "dragover":
              case "dragstart":
              case "drop":
                k2 = Dd;
                break;
              case "touchcancel":
              case "touchend":
              case "touchmove":
              case "touchstart":
                k2 = Vd;
                break;
              case $e:
              case af:
              case bf:
                k2 = Hd;
                break;
              case cf:
                k2 = Xd;
                break;
              case "scroll":
                k2 = vd;
                break;
              case "wheel":
                k2 = Zd;
                break;
              case "copy":
              case "cut":
              case "paste":
                k2 = Jd;
                break;
              case "gotpointercapture":
              case "lostpointercapture":
              case "pointercancel":
              case "pointerdown":
              case "pointermove":
              case "pointerout":
              case "pointerover":
              case "pointerup":
                k2 = Td;
            }
            var t = 0 !== (b & 4), J = !t && "scroll" === a, x2 = t ? null !== h2 ? h2 + "Capture" : null : h2;
            t = [];
            for (var w = d2, u; null !== w; ) {
              u = w;
              var F = u.stateNode;
              5 === u.tag && null !== F && (u = F, null !== x2 && (F = Kb(w, x2), null != F && t.push(tf(w, F, u))));
              if (J) break;
              w = w.return;
            }
            0 < t.length && (h2 = new k2(h2, n, null, c, e2), g2.push({ event: h2, listeners: t }));
          }
        }
        if (0 === (b & 7)) {
          a: {
            h2 = "mouseover" === a || "pointerover" === a;
            k2 = "mouseout" === a || "pointerout" === a;
            if (h2 && c !== wb && (n = c.relatedTarget || c.fromElement) && (Wc(n) || n[uf])) break a;
            if (k2 || h2) {
              h2 = e2.window === e2 ? e2 : (h2 = e2.ownerDocument) ? h2.defaultView || h2.parentWindow : window;
              if (k2) {
                if (n = c.relatedTarget || c.toElement, k2 = d2, n = n ? Wc(n) : null, null !== n && (J = Vb(n), n !== J || 5 !== n.tag && 6 !== n.tag)) n = null;
              } else k2 = null, n = d2;
              if (k2 !== n) {
                t = Bd;
                F = "onMouseLeave";
                x2 = "onMouseEnter";
                w = "mouse";
                if ("pointerout" === a || "pointerover" === a) t = Td, F = "onPointerLeave", x2 = "onPointerEnter", w = "pointer";
                J = null == k2 ? h2 : ue(k2);
                u = null == n ? h2 : ue(n);
                h2 = new t(F, w + "leave", k2, c, e2);
                h2.target = J;
                h2.relatedTarget = u;
                F = null;
                Wc(e2) === d2 && (t = new t(x2, w + "enter", n, c, e2), t.target = u, t.relatedTarget = J, F = t);
                J = F;
                if (k2 && n) b: {
                  t = k2;
                  x2 = n;
                  w = 0;
                  for (u = t; u; u = vf(u)) w++;
                  u = 0;
                  for (F = x2; F; F = vf(F)) u++;
                  for (; 0 < w - u; ) t = vf(t), w--;
                  for (; 0 < u - w; ) x2 = vf(x2), u--;
                  for (; w--; ) {
                    if (t === x2 || null !== x2 && t === x2.alternate) break b;
                    t = vf(t);
                    x2 = vf(x2);
                  }
                  t = null;
                }
                else t = null;
                null !== k2 && wf(g2, h2, k2, t, false);
                null !== n && null !== J && wf(g2, J, n, t, true);
              }
            }
          }
          a: {
            h2 = d2 ? ue(d2) : window;
            k2 = h2.nodeName && h2.nodeName.toLowerCase();
            if ("select" === k2 || "input" === k2 && "file" === h2.type) var na = ve;
            else if (me(h2)) if (we) na = Fe;
            else {
              na = De;
              var xa = Ce;
            }
            else (k2 = h2.nodeName) && "input" === k2.toLowerCase() && ("checkbox" === h2.type || "radio" === h2.type) && (na = Ee);
            if (na && (na = na(a, d2))) {
              ne(g2, na, c, e2);
              break a;
            }
            xa && xa(a, h2, d2);
            "focusout" === a && (xa = h2._wrapperState) && xa.controlled && "number" === h2.type && cb(h2, "number", h2.value);
          }
          xa = d2 ? ue(d2) : window;
          switch (a) {
            case "focusin":
              if (me(xa) || "true" === xa.contentEditable) Qe = xa, Re = d2, Se = null;
              break;
            case "focusout":
              Se = Re = Qe = null;
              break;
            case "mousedown":
              Te = true;
              break;
            case "contextmenu":
            case "mouseup":
            case "dragend":
              Te = false;
              Ue(g2, c, e2);
              break;
            case "selectionchange":
              if (Pe) break;
            case "keydown":
            case "keyup":
              Ue(g2, c, e2);
          }
          var $a;
          if (ae) b: {
            switch (a) {
              case "compositionstart":
                var ba = "onCompositionStart";
                break b;
              case "compositionend":
                ba = "onCompositionEnd";
                break b;
              case "compositionupdate":
                ba = "onCompositionUpdate";
                break b;
            }
            ba = void 0;
          }
          else ie ? ge(a, c) && (ba = "onCompositionEnd") : "keydown" === a && 229 === c.keyCode && (ba = "onCompositionStart");
          ba && (de && "ko" !== c.locale && (ie || "onCompositionStart" !== ba ? "onCompositionEnd" === ba && ie && ($a = nd()) : (kd = e2, ld = "value" in kd ? kd.value : kd.textContent, ie = true)), xa = oe(d2, ba), 0 < xa.length && (ba = new Ld(ba, a, null, c, e2), g2.push({ event: ba, listeners: xa }), $a ? ba.data = $a : ($a = he(c), null !== $a && (ba.data = $a))));
          if ($a = ce ? je(a, c) : ke(a, c)) d2 = oe(d2, "onBeforeInput"), 0 < d2.length && (e2 = new Ld("onBeforeInput", "beforeinput", null, c, e2), g2.push({ event: e2, listeners: d2 }), e2.data = $a);
        }
        se(g2, b);
      });
    }
    function tf(a, b, c) {
      return { instance: a, listener: b, currentTarget: c };
    }
    function oe(a, b) {
      for (var c = b + "Capture", d = []; null !== a; ) {
        var e = a, f = e.stateNode;
        5 === e.tag && null !== f && (e = f, f = Kb(a, c), null != f && d.unshift(tf(a, f, e)), f = Kb(a, b), null != f && d.push(tf(a, f, e)));
        a = a.return;
      }
      return d;
    }
    function vf(a) {
      if (null === a) return null;
      do
        a = a.return;
      while (a && 5 !== a.tag);
      return a ? a : null;
    }
    function wf(a, b, c, d, e) {
      for (var f = b._reactName, g = []; null !== c && c !== d; ) {
        var h = c, k = h.alternate, l = h.stateNode;
        if (null !== k && k === d) break;
        5 === h.tag && null !== l && (h = l, e ? (k = Kb(c, f), null != k && g.unshift(tf(c, k, h))) : e || (k = Kb(c, f), null != k && g.push(tf(c, k, h))));
        c = c.return;
      }
      0 !== g.length && a.push({ event: b, listeners: g });
    }
    var xf = /\r\n?/g, yf = /\u0000|\uFFFD/g;
    function zf(a) {
      return ("string" === typeof a ? a : "" + a).replace(xf, "\n").replace(yf, "");
    }
    function Af(a, b, c) {
      b = zf(b);
      if (zf(a) !== b && c) throw Error(p(425));
    }
    function Bf() {
    }
    var Cf = null, Df = null;
    function Ef(a, b) {
      return "textarea" === a || "noscript" === a || "string" === typeof b.children || "number" === typeof b.children || "object" === typeof b.dangerouslySetInnerHTML && null !== b.dangerouslySetInnerHTML && null != b.dangerouslySetInnerHTML.__html;
    }
    var Ff = "function" === typeof setTimeout ? setTimeout : void 0, Gf = "function" === typeof clearTimeout ? clearTimeout : void 0, Hf = "function" === typeof Promise ? Promise : void 0, Jf = "function" === typeof queueMicrotask ? queueMicrotask : "undefined" !== typeof Hf ? function(a) {
      return Hf.resolve(null).then(a).catch(If);
    } : Ff;
    function If(a) {
      setTimeout(function() {
        throw a;
      });
    }
    function Kf(a, b) {
      var c = b, d = 0;
      do {
        var e = c.nextSibling;
        a.removeChild(c);
        if (e && 8 === e.nodeType) if (c = e.data, "/$" === c) {
          if (0 === d) {
            a.removeChild(e);
            bd(b);
            return;
          }
          d--;
        } else "$" !== c && "$?" !== c && "$!" !== c || d++;
        c = e;
      } while (c);
      bd(b);
    }
    function Lf(a) {
      for (; null != a; a = a.nextSibling) {
        var b = a.nodeType;
        if (1 === b || 3 === b) break;
        if (8 === b) {
          b = a.data;
          if ("$" === b || "$!" === b || "$?" === b) break;
          if ("/$" === b) return null;
        }
      }
      return a;
    }
    function Mf(a) {
      a = a.previousSibling;
      for (var b = 0; a; ) {
        if (8 === a.nodeType) {
          var c = a.data;
          if ("$" === c || "$!" === c || "$?" === c) {
            if (0 === b) return a;
            b--;
          } else "/$" === c && b++;
        }
        a = a.previousSibling;
      }
      return null;
    }
    var Nf = Math.random().toString(36).slice(2), Of = "__reactFiber$" + Nf, Pf = "__reactProps$" + Nf, uf = "__reactContainer$" + Nf, of = "__reactEvents$" + Nf, Qf = "__reactListeners$" + Nf, Rf = "__reactHandles$" + Nf;
    function Wc(a) {
      var b = a[Of];
      if (b) return b;
      for (var c = a.parentNode; c; ) {
        if (b = c[uf] || c[Of]) {
          c = b.alternate;
          if (null !== b.child || null !== c && null !== c.child) for (a = Mf(a); null !== a; ) {
            if (c = a[Of]) return c;
            a = Mf(a);
          }
          return b;
        }
        a = c;
        c = a.parentNode;
      }
      return null;
    }
    function Cb(a) {
      a = a[Of] || a[uf];
      return !a || 5 !== a.tag && 6 !== a.tag && 13 !== a.tag && 3 !== a.tag ? null : a;
    }
    function ue(a) {
      if (5 === a.tag || 6 === a.tag) return a.stateNode;
      throw Error(p(33));
    }
    function Db(a) {
      return a[Pf] || null;
    }
    var Sf = [], Tf = -1;
    function Uf(a) {
      return { current: a };
    }
    function E(a) {
      0 > Tf || (a.current = Sf[Tf], Sf[Tf] = null, Tf--);
    }
    function G(a, b) {
      Tf++;
      Sf[Tf] = a.current;
      a.current = b;
    }
    var Vf = {}, H = Uf(Vf), Wf = Uf(false), Xf = Vf;
    function Yf(a, b) {
      var c = a.type.contextTypes;
      if (!c) return Vf;
      var d = a.stateNode;
      if (d && d.__reactInternalMemoizedUnmaskedChildContext === b) return d.__reactInternalMemoizedMaskedChildContext;
      var e = {}, f;
      for (f in c) e[f] = b[f];
      d && (a = a.stateNode, a.__reactInternalMemoizedUnmaskedChildContext = b, a.__reactInternalMemoizedMaskedChildContext = e);
      return e;
    }
    function Zf(a) {
      a = a.childContextTypes;
      return null !== a && void 0 !== a;
    }
    function $f() {
      E(Wf);
      E(H);
    }
    function ag(a, b, c) {
      if (H.current !== Vf) throw Error(p(168));
      G(H, b);
      G(Wf, c);
    }
    function bg(a, b, c) {
      var d = a.stateNode;
      b = b.childContextTypes;
      if ("function" !== typeof d.getChildContext) return c;
      d = d.getChildContext();
      for (var e in d) if (!(e in b)) throw Error(p(108, Ra(a) || "Unknown", e));
      return A({}, c, d);
    }
    function cg(a) {
      a = (a = a.stateNode) && a.__reactInternalMemoizedMergedChildContext || Vf;
      Xf = H.current;
      G(H, a);
      G(Wf, Wf.current);
      return true;
    }
    function dg(a, b, c) {
      var d = a.stateNode;
      if (!d) throw Error(p(169));
      c ? (a = bg(a, b, Xf), d.__reactInternalMemoizedMergedChildContext = a, E(Wf), E(H), G(H, a)) : E(Wf);
      G(Wf, c);
    }
    var eg = null, fg = false, gg = false;
    function hg(a) {
      null === eg ? eg = [a] : eg.push(a);
    }
    function ig(a) {
      fg = true;
      hg(a);
    }
    function jg() {
      if (!gg && null !== eg) {
        gg = true;
        var a = 0, b = C;
        try {
          var c = eg;
          for (C = 1; a < c.length; a++) {
            var d = c[a];
            do
              d = d(true);
            while (null !== d);
          }
          eg = null;
          fg = false;
        } catch (e) {
          throw null !== eg && (eg = eg.slice(a + 1)), ac(fc, jg), e;
        } finally {
          C = b, gg = false;
        }
      }
      return null;
    }
    var kg = [], lg = 0, mg = null, ng = 0, og = [], pg = 0, qg = null, rg = 1, sg = "";
    function tg(a, b) {
      kg[lg++] = ng;
      kg[lg++] = mg;
      mg = a;
      ng = b;
    }
    function ug(a, b, c) {
      og[pg++] = rg;
      og[pg++] = sg;
      og[pg++] = qg;
      qg = a;
      var d = rg;
      a = sg;
      var e = 32 - oc(d) - 1;
      d &= ~(1 << e);
      c += 1;
      var f = 32 - oc(b) + e;
      if (30 < f) {
        var g = e - e % 5;
        f = (d & (1 << g) - 1).toString(32);
        d >>= g;
        e -= g;
        rg = 1 << 32 - oc(b) + e | c << e | d;
        sg = f + a;
      } else rg = 1 << f | c << e | d, sg = a;
    }
    function vg(a) {
      null !== a.return && (tg(a, 1), ug(a, 1, 0));
    }
    function wg(a) {
      for (; a === mg; ) mg = kg[--lg], kg[lg] = null, ng = kg[--lg], kg[lg] = null;
      for (; a === qg; ) qg = og[--pg], og[pg] = null, sg = og[--pg], og[pg] = null, rg = og[--pg], og[pg] = null;
    }
    var xg = null, yg = null, I = false, zg = null;
    function Ag(a, b) {
      var c = Bg(5, null, null, 0);
      c.elementType = "DELETED";
      c.stateNode = b;
      c.return = a;
      b = a.deletions;
      null === b ? (a.deletions = [c], a.flags |= 16) : b.push(c);
    }
    function Cg(a, b) {
      switch (a.tag) {
        case 5:
          var c = a.type;
          b = 1 !== b.nodeType || c.toLowerCase() !== b.nodeName.toLowerCase() ? null : b;
          return null !== b ? (a.stateNode = b, xg = a, yg = Lf(b.firstChild), true) : false;
        case 6:
          return b = "" === a.pendingProps || 3 !== b.nodeType ? null : b, null !== b ? (a.stateNode = b, xg = a, yg = null, true) : false;
        case 13:
          return b = 8 !== b.nodeType ? null : b, null !== b ? (c = null !== qg ? { id: rg, overflow: sg } : null, a.memoizedState = { dehydrated: b, treeContext: c, retryLane: 1073741824 }, c = Bg(18, null, null, 0), c.stateNode = b, c.return = a, a.child = c, xg = a, yg = null, true) : false;
        default:
          return false;
      }
    }
    function Dg(a) {
      return 0 !== (a.mode & 1) && 0 === (a.flags & 128);
    }
    function Eg(a) {
      if (I) {
        var b = yg;
        if (b) {
          var c = b;
          if (!Cg(a, b)) {
            if (Dg(a)) throw Error(p(418));
            b = Lf(c.nextSibling);
            var d = xg;
            b && Cg(a, b) ? Ag(d, c) : (a.flags = a.flags & -4097 | 2, I = false, xg = a);
          }
        } else {
          if (Dg(a)) throw Error(p(418));
          a.flags = a.flags & -4097 | 2;
          I = false;
          xg = a;
        }
      }
    }
    function Fg(a) {
      for (a = a.return; null !== a && 5 !== a.tag && 3 !== a.tag && 13 !== a.tag; ) a = a.return;
      xg = a;
    }
    function Gg(a) {
      if (a !== xg) return false;
      if (!I) return Fg(a), I = true, false;
      var b;
      (b = 3 !== a.tag) && !(b = 5 !== a.tag) && (b = a.type, b = "head" !== b && "body" !== b && !Ef(a.type, a.memoizedProps));
      if (b && (b = yg)) {
        if (Dg(a)) throw Hg(), Error(p(418));
        for (; b; ) Ag(a, b), b = Lf(b.nextSibling);
      }
      Fg(a);
      if (13 === a.tag) {
        a = a.memoizedState;
        a = null !== a ? a.dehydrated : null;
        if (!a) throw Error(p(317));
        a: {
          a = a.nextSibling;
          for (b = 0; a; ) {
            if (8 === a.nodeType) {
              var c = a.data;
              if ("/$" === c) {
                if (0 === b) {
                  yg = Lf(a.nextSibling);
                  break a;
                }
                b--;
              } else "$" !== c && "$!" !== c && "$?" !== c || b++;
            }
            a = a.nextSibling;
          }
          yg = null;
        }
      } else yg = xg ? Lf(a.stateNode.nextSibling) : null;
      return true;
    }
    function Hg() {
      for (var a = yg; a; ) a = Lf(a.nextSibling);
    }
    function Ig() {
      yg = xg = null;
      I = false;
    }
    function Jg(a) {
      null === zg ? zg = [a] : zg.push(a);
    }
    var Kg = ua.ReactCurrentBatchConfig;
    function Lg(a, b, c) {
      a = c.ref;
      if (null !== a && "function" !== typeof a && "object" !== typeof a) {
        if (c._owner) {
          c = c._owner;
          if (c) {
            if (1 !== c.tag) throw Error(p(309));
            var d = c.stateNode;
          }
          if (!d) throw Error(p(147, a));
          var e = d, f = "" + a;
          if (null !== b && null !== b.ref && "function" === typeof b.ref && b.ref._stringRef === f) return b.ref;
          b = function(a2) {
            var b3 = e.refs;
            null === a2 ? delete b3[f] : b3[f] = a2;
          };
          b._stringRef = f;
          return b;
        }
        if ("string" !== typeof a) throw Error(p(284));
        if (!c._owner) throw Error(p(290, a));
      }
      return a;
    }
    function Mg(a, b) {
      a = Object.prototype.toString.call(b);
      throw Error(p(31, "[object Object]" === a ? "object with keys {" + Object.keys(b).join(", ") + "}" : a));
    }
    function Ng(a) {
      var b = a._init;
      return b(a._payload);
    }
    function Og(a) {
      function b(b3, c2) {
        if (a) {
          var d2 = b3.deletions;
          null === d2 ? (b3.deletions = [c2], b3.flags |= 16) : d2.push(c2);
        }
      }
      function c(c2, d2) {
        if (!a) return null;
        for (; null !== d2; ) b(c2, d2), d2 = d2.sibling;
        return null;
      }
      function d(a2, b3) {
        for (a2 = /* @__PURE__ */ new Map(); null !== b3; ) null !== b3.key ? a2.set(b3.key, b3) : a2.set(b3.index, b3), b3 = b3.sibling;
        return a2;
      }
      function e(a2, b3) {
        a2 = Pg(a2, b3);
        a2.index = 0;
        a2.sibling = null;
        return a2;
      }
      function f(b3, c2, d2) {
        b3.index = d2;
        if (!a) return b3.flags |= 1048576, c2;
        d2 = b3.alternate;
        if (null !== d2) return d2 = d2.index, d2 < c2 ? (b3.flags |= 2, c2) : d2;
        b3.flags |= 2;
        return c2;
      }
      function g(b3) {
        a && null === b3.alternate && (b3.flags |= 2);
        return b3;
      }
      function h(a2, b3, c2, d2) {
        if (null === b3 || 6 !== b3.tag) return b3 = Qg(c2, a2.mode, d2), b3.return = a2, b3;
        b3 = e(b3, c2);
        b3.return = a2;
        return b3;
      }
      function k(a2, b3, c2, d2) {
        var f2 = c2.type;
        if (f2 === ya) return m(a2, b3, c2.props.children, d2, c2.key);
        if (null !== b3 && (b3.elementType === f2 || "object" === typeof f2 && null !== f2 && f2.$$typeof === Ha && Ng(f2) === b3.type)) return d2 = e(b3, c2.props), d2.ref = Lg(a2, b3, c2), d2.return = a2, d2;
        d2 = Rg(c2.type, c2.key, c2.props, null, a2.mode, d2);
        d2.ref = Lg(a2, b3, c2);
        d2.return = a2;
        return d2;
      }
      function l(a2, b3, c2, d2) {
        if (null === b3 || 4 !== b3.tag || b3.stateNode.containerInfo !== c2.containerInfo || b3.stateNode.implementation !== c2.implementation) return b3 = Sg(c2, a2.mode, d2), b3.return = a2, b3;
        b3 = e(b3, c2.children || []);
        b3.return = a2;
        return b3;
      }
      function m(a2, b3, c2, d2, f2) {
        if (null === b3 || 7 !== b3.tag) return b3 = Tg(c2, a2.mode, d2, f2), b3.return = a2, b3;
        b3 = e(b3, c2);
        b3.return = a2;
        return b3;
      }
      function q(a2, b3, c2) {
        if ("string" === typeof b3 && "" !== b3 || "number" === typeof b3) return b3 = Qg("" + b3, a2.mode, c2), b3.return = a2, b3;
        if ("object" === typeof b3 && null !== b3) {
          switch (b3.$$typeof) {
            case va:
              return c2 = Rg(b3.type, b3.key, b3.props, null, a2.mode, c2), c2.ref = Lg(a2, null, b3), c2.return = a2, c2;
            case wa:
              return b3 = Sg(b3, a2.mode, c2), b3.return = a2, b3;
            case Ha:
              var d2 = b3._init;
              return q(a2, d2(b3._payload), c2);
          }
          if (eb(b3) || Ka(b3)) return b3 = Tg(b3, a2.mode, c2, null), b3.return = a2, b3;
          Mg(a2, b3);
        }
        return null;
      }
      function r(a2, b3, c2, d2) {
        var e2 = null !== b3 ? b3.key : null;
        if ("string" === typeof c2 && "" !== c2 || "number" === typeof c2) return null !== e2 ? null : h(a2, b3, "" + c2, d2);
        if ("object" === typeof c2 && null !== c2) {
          switch (c2.$$typeof) {
            case va:
              return c2.key === e2 ? k(a2, b3, c2, d2) : null;
            case wa:
              return c2.key === e2 ? l(a2, b3, c2, d2) : null;
            case Ha:
              return e2 = c2._init, r(
                a2,
                b3,
                e2(c2._payload),
                d2
              );
          }
          if (eb(c2) || Ka(c2)) return null !== e2 ? null : m(a2, b3, c2, d2, null);
          Mg(a2, c2);
        }
        return null;
      }
      function y(a2, b3, c2, d2, e2) {
        if ("string" === typeof d2 && "" !== d2 || "number" === typeof d2) return a2 = a2.get(c2) || null, h(b3, a2, "" + d2, e2);
        if ("object" === typeof d2 && null !== d2) {
          switch (d2.$$typeof) {
            case va:
              return a2 = a2.get(null === d2.key ? c2 : d2.key) || null, k(b3, a2, d2, e2);
            case wa:
              return a2 = a2.get(null === d2.key ? c2 : d2.key) || null, l(b3, a2, d2, e2);
            case Ha:
              var f2 = d2._init;
              return y(a2, b3, c2, f2(d2._payload), e2);
          }
          if (eb(d2) || Ka(d2)) return a2 = a2.get(c2) || null, m(b3, a2, d2, e2, null);
          Mg(b3, d2);
        }
        return null;
      }
      function n(e2, g2, h2, k2) {
        for (var l2 = null, m2 = null, u = g2, w = g2 = 0, x2 = null; null !== u && w < h2.length; w++) {
          u.index > w ? (x2 = u, u = null) : x2 = u.sibling;
          var n2 = r(e2, u, h2[w], k2);
          if (null === n2) {
            null === u && (u = x2);
            break;
          }
          a && u && null === n2.alternate && b(e2, u);
          g2 = f(n2, g2, w);
          null === m2 ? l2 = n2 : m2.sibling = n2;
          m2 = n2;
          u = x2;
        }
        if (w === h2.length) return c(e2, u), I && tg(e2, w), l2;
        if (null === u) {
          for (; w < h2.length; w++) u = q(e2, h2[w], k2), null !== u && (g2 = f(u, g2, w), null === m2 ? l2 = u : m2.sibling = u, m2 = u);
          I && tg(e2, w);
          return l2;
        }
        for (u = d(e2, u); w < h2.length; w++) x2 = y(u, e2, w, h2[w], k2), null !== x2 && (a && null !== x2.alternate && u.delete(null === x2.key ? w : x2.key), g2 = f(x2, g2, w), null === m2 ? l2 = x2 : m2.sibling = x2, m2 = x2);
        a && u.forEach(function(a2) {
          return b(e2, a2);
        });
        I && tg(e2, w);
        return l2;
      }
      function t(e2, g2, h2, k2) {
        var l2 = Ka(h2);
        if ("function" !== typeof l2) throw Error(p(150));
        h2 = l2.call(h2);
        if (null == h2) throw Error(p(151));
        for (var u = l2 = null, m2 = g2, w = g2 = 0, x2 = null, n2 = h2.next(); null !== m2 && !n2.done; w++, n2 = h2.next()) {
          m2.index > w ? (x2 = m2, m2 = null) : x2 = m2.sibling;
          var t2 = r(e2, m2, n2.value, k2);
          if (null === t2) {
            null === m2 && (m2 = x2);
            break;
          }
          a && m2 && null === t2.alternate && b(e2, m2);
          g2 = f(t2, g2, w);
          null === u ? l2 = t2 : u.sibling = t2;
          u = t2;
          m2 = x2;
        }
        if (n2.done) return c(
          e2,
          m2
        ), I && tg(e2, w), l2;
        if (null === m2) {
          for (; !n2.done; w++, n2 = h2.next()) n2 = q(e2, n2.value, k2), null !== n2 && (g2 = f(n2, g2, w), null === u ? l2 = n2 : u.sibling = n2, u = n2);
          I && tg(e2, w);
          return l2;
        }
        for (m2 = d(e2, m2); !n2.done; w++, n2 = h2.next()) n2 = y(m2, e2, w, n2.value, k2), null !== n2 && (a && null !== n2.alternate && m2.delete(null === n2.key ? w : n2.key), g2 = f(n2, g2, w), null === u ? l2 = n2 : u.sibling = n2, u = n2);
        a && m2.forEach(function(a2) {
          return b(e2, a2);
        });
        I && tg(e2, w);
        return l2;
      }
      function J(a2, d2, f2, h2) {
        "object" === typeof f2 && null !== f2 && f2.type === ya && null === f2.key && (f2 = f2.props.children);
        if ("object" === typeof f2 && null !== f2) {
          switch (f2.$$typeof) {
            case va:
              a: {
                for (var k2 = f2.key, l2 = d2; null !== l2; ) {
                  if (l2.key === k2) {
                    k2 = f2.type;
                    if (k2 === ya) {
                      if (7 === l2.tag) {
                        c(a2, l2.sibling);
                        d2 = e(l2, f2.props.children);
                        d2.return = a2;
                        a2 = d2;
                        break a;
                      }
                    } else if (l2.elementType === k2 || "object" === typeof k2 && null !== k2 && k2.$$typeof === Ha && Ng(k2) === l2.type) {
                      c(a2, l2.sibling);
                      d2 = e(l2, f2.props);
                      d2.ref = Lg(a2, l2, f2);
                      d2.return = a2;
                      a2 = d2;
                      break a;
                    }
                    c(a2, l2);
                    break;
                  } else b(a2, l2);
                  l2 = l2.sibling;
                }
                f2.type === ya ? (d2 = Tg(f2.props.children, a2.mode, h2, f2.key), d2.return = a2, a2 = d2) : (h2 = Rg(f2.type, f2.key, f2.props, null, a2.mode, h2), h2.ref = Lg(a2, d2, f2), h2.return = a2, a2 = h2);
              }
              return g(a2);
            case wa:
              a: {
                for (l2 = f2.key; null !== d2; ) {
                  if (d2.key === l2) if (4 === d2.tag && d2.stateNode.containerInfo === f2.containerInfo && d2.stateNode.implementation === f2.implementation) {
                    c(a2, d2.sibling);
                    d2 = e(d2, f2.children || []);
                    d2.return = a2;
                    a2 = d2;
                    break a;
                  } else {
                    c(a2, d2);
                    break;
                  }
                  else b(a2, d2);
                  d2 = d2.sibling;
                }
                d2 = Sg(f2, a2.mode, h2);
                d2.return = a2;
                a2 = d2;
              }
              return g(a2);
            case Ha:
              return l2 = f2._init, J(a2, d2, l2(f2._payload), h2);
          }
          if (eb(f2)) return n(a2, d2, f2, h2);
          if (Ka(f2)) return t(a2, d2, f2, h2);
          Mg(a2, f2);
        }
        return "string" === typeof f2 && "" !== f2 || "number" === typeof f2 ? (f2 = "" + f2, null !== d2 && 6 === d2.tag ? (c(a2, d2.sibling), d2 = e(d2, f2), d2.return = a2, a2 = d2) : (c(a2, d2), d2 = Qg(f2, a2.mode, h2), d2.return = a2, a2 = d2), g(a2)) : c(a2, d2);
      }
      return J;
    }
    var Ug = Og(true), Vg = Og(false), Wg = Uf(null), Xg = null, Yg = null, Zg = null;
    function $g() {
      Zg = Yg = Xg = null;
    }
    function ah(a) {
      var b = Wg.current;
      E(Wg);
      a._currentValue = b;
    }
    function bh(a, b, c) {
      for (; null !== a; ) {
        var d = a.alternate;
        (a.childLanes & b) !== b ? (a.childLanes |= b, null !== d && (d.childLanes |= b)) : null !== d && (d.childLanes & b) !== b && (d.childLanes |= b);
        if (a === c) break;
        a = a.return;
      }
    }
    function ch(a, b) {
      Xg = a;
      Zg = Yg = null;
      a = a.dependencies;
      null !== a && null !== a.firstContext && (0 !== (a.lanes & b) && (dh = true), a.firstContext = null);
    }
    function eh(a) {
      var b = a._currentValue;
      if (Zg !== a) if (a = { context: a, memoizedValue: b, next: null }, null === Yg) {
        if (null === Xg) throw Error(p(308));
        Yg = a;
        Xg.dependencies = { lanes: 0, firstContext: a };
      } else Yg = Yg.next = a;
      return b;
    }
    var fh = null;
    function gh(a) {
      null === fh ? fh = [a] : fh.push(a);
    }
    function hh(a, b, c, d) {
      var e = b.interleaved;
      null === e ? (c.next = c, gh(b)) : (c.next = e.next, e.next = c);
      b.interleaved = c;
      return ih(a, d);
    }
    function ih(a, b) {
      a.lanes |= b;
      var c = a.alternate;
      null !== c && (c.lanes |= b);
      c = a;
      for (a = a.return; null !== a; ) a.childLanes |= b, c = a.alternate, null !== c && (c.childLanes |= b), c = a, a = a.return;
      return 3 === c.tag ? c.stateNode : null;
    }
    var jh = false;
    function kh(a) {
      a.updateQueue = { baseState: a.memoizedState, firstBaseUpdate: null, lastBaseUpdate: null, shared: { pending: null, interleaved: null, lanes: 0 }, effects: null };
    }
    function lh(a, b) {
      a = a.updateQueue;
      b.updateQueue === a && (b.updateQueue = { baseState: a.baseState, firstBaseUpdate: a.firstBaseUpdate, lastBaseUpdate: a.lastBaseUpdate, shared: a.shared, effects: a.effects });
    }
    function mh(a, b) {
      return { eventTime: a, lane: b, tag: 0, payload: null, callback: null, next: null };
    }
    function nh(a, b, c) {
      var d = a.updateQueue;
      if (null === d) return null;
      d = d.shared;
      if (0 !== (K & 2)) {
        var e = d.pending;
        null === e ? b.next = b : (b.next = e.next, e.next = b);
        d.pending = b;
        return ih(a, c);
      }
      e = d.interleaved;
      null === e ? (b.next = b, gh(d)) : (b.next = e.next, e.next = b);
      d.interleaved = b;
      return ih(a, c);
    }
    function oh(a, b, c) {
      b = b.updateQueue;
      if (null !== b && (b = b.shared, 0 !== (c & 4194240))) {
        var d = b.lanes;
        d &= a.pendingLanes;
        c |= d;
        b.lanes = c;
        Cc(a, c);
      }
    }
    function ph(a, b) {
      var c = a.updateQueue, d = a.alternate;
      if (null !== d && (d = d.updateQueue, c === d)) {
        var e = null, f = null;
        c = c.firstBaseUpdate;
        if (null !== c) {
          do {
            var g = { eventTime: c.eventTime, lane: c.lane, tag: c.tag, payload: c.payload, callback: c.callback, next: null };
            null === f ? e = f = g : f = f.next = g;
            c = c.next;
          } while (null !== c);
          null === f ? e = f = b : f = f.next = b;
        } else e = f = b;
        c = { baseState: d.baseState, firstBaseUpdate: e, lastBaseUpdate: f, shared: d.shared, effects: d.effects };
        a.updateQueue = c;
        return;
      }
      a = c.lastBaseUpdate;
      null === a ? c.firstBaseUpdate = b : a.next = b;
      c.lastBaseUpdate = b;
    }
    function qh(a, b, c, d) {
      var e = a.updateQueue;
      jh = false;
      var f = e.firstBaseUpdate, g = e.lastBaseUpdate, h = e.shared.pending;
      if (null !== h) {
        e.shared.pending = null;
        var k = h, l = k.next;
        k.next = null;
        null === g ? f = l : g.next = l;
        g = k;
        var m = a.alternate;
        null !== m && (m = m.updateQueue, h = m.lastBaseUpdate, h !== g && (null === h ? m.firstBaseUpdate = l : h.next = l, m.lastBaseUpdate = k));
      }
      if (null !== f) {
        var q = e.baseState;
        g = 0;
        m = l = k = null;
        h = f;
        do {
          var r = h.lane, y = h.eventTime;
          if ((d & r) === r) {
            null !== m && (m = m.next = {
              eventTime: y,
              lane: 0,
              tag: h.tag,
              payload: h.payload,
              callback: h.callback,
              next: null
            });
            a: {
              var n = a, t = h;
              r = b;
              y = c;
              switch (t.tag) {
                case 1:
                  n = t.payload;
                  if ("function" === typeof n) {
                    q = n.call(y, q, r);
                    break a;
                  }
                  q = n;
                  break a;
                case 3:
                  n.flags = n.flags & -65537 | 128;
                case 0:
                  n = t.payload;
                  r = "function" === typeof n ? n.call(y, q, r) : n;
                  if (null === r || void 0 === r) break a;
                  q = A({}, q, r);
                  break a;
                case 2:
                  jh = true;
              }
            }
            null !== h.callback && 0 !== h.lane && (a.flags |= 64, r = e.effects, null === r ? e.effects = [h] : r.push(h));
          } else y = { eventTime: y, lane: r, tag: h.tag, payload: h.payload, callback: h.callback, next: null }, null === m ? (l = m = y, k = q) : m = m.next = y, g |= r;
          h = h.next;
          if (null === h) if (h = e.shared.pending, null === h) break;
          else r = h, h = r.next, r.next = null, e.lastBaseUpdate = r, e.shared.pending = null;
        } while (1);
        null === m && (k = q);
        e.baseState = k;
        e.firstBaseUpdate = l;
        e.lastBaseUpdate = m;
        b = e.shared.interleaved;
        if (null !== b) {
          e = b;
          do
            g |= e.lane, e = e.next;
          while (e !== b);
        } else null === f && (e.shared.lanes = 0);
        rh |= g;
        a.lanes = g;
        a.memoizedState = q;
      }
    }
    function sh(a, b, c) {
      a = b.effects;
      b.effects = null;
      if (null !== a) for (b = 0; b < a.length; b++) {
        var d = a[b], e = d.callback;
        if (null !== e) {
          d.callback = null;
          d = c;
          if ("function" !== typeof e) throw Error(p(191, e));
          e.call(d);
        }
      }
    }
    var th = {}, uh = Uf(th), vh = Uf(th), wh = Uf(th);
    function xh(a) {
      if (a === th) throw Error(p(174));
      return a;
    }
    function yh(a, b) {
      G(wh, b);
      G(vh, a);
      G(uh, th);
      a = b.nodeType;
      switch (a) {
        case 9:
        case 11:
          b = (b = b.documentElement) ? b.namespaceURI : lb(null, "");
          break;
        default:
          a = 8 === a ? b.parentNode : b, b = a.namespaceURI || null, a = a.tagName, b = lb(b, a);
      }
      E(uh);
      G(uh, b);
    }
    function zh2() {
      E(uh);
      E(vh);
      E(wh);
    }
    function Ah(a) {
      xh(wh.current);
      var b = xh(uh.current);
      var c = lb(b, a.type);
      b !== c && (G(vh, a), G(uh, c));
    }
    function Bh(a) {
      vh.current === a && (E(uh), E(vh));
    }
    var L = Uf(0);
    function Ch(a) {
      for (var b = a; null !== b; ) {
        if (13 === b.tag) {
          var c = b.memoizedState;
          if (null !== c && (c = c.dehydrated, null === c || "$?" === c.data || "$!" === c.data)) return b;
        } else if (19 === b.tag && void 0 !== b.memoizedProps.revealOrder) {
          if (0 !== (b.flags & 128)) return b;
        } else if (null !== b.child) {
          b.child.return = b;
          b = b.child;
          continue;
        }
        if (b === a) break;
        for (; null === b.sibling; ) {
          if (null === b.return || b.return === a) return null;
          b = b.return;
        }
        b.sibling.return = b.return;
        b = b.sibling;
      }
      return null;
    }
    var Dh = [];
    function Eh() {
      for (var a = 0; a < Dh.length; a++) Dh[a]._workInProgressVersionPrimary = null;
      Dh.length = 0;
    }
    var Fh = ua.ReactCurrentDispatcher, Gh = ua.ReactCurrentBatchConfig, Hh = 0, M = null, N = null, O = null, Ih = false, Jh = false, Kh = 0, Lh = 0;
    function P() {
      throw Error(p(321));
    }
    function Mh(a, b) {
      if (null === b) return false;
      for (var c = 0; c < b.length && c < a.length; c++) if (!He(a[c], b[c])) return false;
      return true;
    }
    function Nh(a, b, c, d, e, f) {
      Hh = f;
      M = b;
      b.memoizedState = null;
      b.updateQueue = null;
      b.lanes = 0;
      Fh.current = null === a || null === a.memoizedState ? Oh : Ph;
      a = c(d, e);
      if (Jh) {
        f = 0;
        do {
          Jh = false;
          Kh = 0;
          if (25 <= f) throw Error(p(301));
          f += 1;
          O = N = null;
          b.updateQueue = null;
          Fh.current = Qh;
          a = c(d, e);
        } while (Jh);
      }
      Fh.current = Rh;
      b = null !== N && null !== N.next;
      Hh = 0;
      O = N = M = null;
      Ih = false;
      if (b) throw Error(p(300));
      return a;
    }
    function Sh() {
      var a = 0 !== Kh;
      Kh = 0;
      return a;
    }
    function Th() {
      var a = { memoizedState: null, baseState: null, baseQueue: null, queue: null, next: null };
      null === O ? M.memoizedState = O = a : O = O.next = a;
      return O;
    }
    function Uh() {
      if (null === N) {
        var a = M.alternate;
        a = null !== a ? a.memoizedState : null;
      } else a = N.next;
      var b = null === O ? M.memoizedState : O.next;
      if (null !== b) O = b, N = a;
      else {
        if (null === a) throw Error(p(310));
        N = a;
        a = { memoizedState: N.memoizedState, baseState: N.baseState, baseQueue: N.baseQueue, queue: N.queue, next: null };
        null === O ? M.memoizedState = O = a : O = O.next = a;
      }
      return O;
    }
    function Vh(a, b) {
      return "function" === typeof b ? b(a) : b;
    }
    function Wh(a) {
      var b = Uh(), c = b.queue;
      if (null === c) throw Error(p(311));
      c.lastRenderedReducer = a;
      var d = N, e = d.baseQueue, f = c.pending;
      if (null !== f) {
        if (null !== e) {
          var g = e.next;
          e.next = f.next;
          f.next = g;
        }
        d.baseQueue = e = f;
        c.pending = null;
      }
      if (null !== e) {
        f = e.next;
        d = d.baseState;
        var h = g = null, k = null, l = f;
        do {
          var m = l.lane;
          if ((Hh & m) === m) null !== k && (k = k.next = { lane: 0, action: l.action, hasEagerState: l.hasEagerState, eagerState: l.eagerState, next: null }), d = l.hasEagerState ? l.eagerState : a(d, l.action);
          else {
            var q = {
              lane: m,
              action: l.action,
              hasEagerState: l.hasEagerState,
              eagerState: l.eagerState,
              next: null
            };
            null === k ? (h = k = q, g = d) : k = k.next = q;
            M.lanes |= m;
            rh |= m;
          }
          l = l.next;
        } while (null !== l && l !== f);
        null === k ? g = d : k.next = h;
        He(d, b.memoizedState) || (dh = true);
        b.memoizedState = d;
        b.baseState = g;
        b.baseQueue = k;
        c.lastRenderedState = d;
      }
      a = c.interleaved;
      if (null !== a) {
        e = a;
        do
          f = e.lane, M.lanes |= f, rh |= f, e = e.next;
        while (e !== a);
      } else null === e && (c.lanes = 0);
      return [b.memoizedState, c.dispatch];
    }
    function Xh(a) {
      var b = Uh(), c = b.queue;
      if (null === c) throw Error(p(311));
      c.lastRenderedReducer = a;
      var d = c.dispatch, e = c.pending, f = b.memoizedState;
      if (null !== e) {
        c.pending = null;
        var g = e = e.next;
        do
          f = a(f, g.action), g = g.next;
        while (g !== e);
        He(f, b.memoizedState) || (dh = true);
        b.memoizedState = f;
        null === b.baseQueue && (b.baseState = f);
        c.lastRenderedState = f;
      }
      return [f, d];
    }
    function Yh() {
    }
    function Zh(a, b) {
      var c = M, d = Uh(), e = b(), f = !He(d.memoizedState, e);
      f && (d.memoizedState = e, dh = true);
      d = d.queue;
      $h(ai.bind(null, c, d, a), [a]);
      if (d.getSnapshot !== b || f || null !== O && O.memoizedState.tag & 1) {
        c.flags |= 2048;
        bi(9, ci.bind(null, c, d, e, b), void 0, null);
        if (null === Q) throw Error(p(349));
        0 !== (Hh & 30) || di(c, b, e);
      }
      return e;
    }
    function di(a, b, c) {
      a.flags |= 16384;
      a = { getSnapshot: b, value: c };
      b = M.updateQueue;
      null === b ? (b = { lastEffect: null, stores: null }, M.updateQueue = b, b.stores = [a]) : (c = b.stores, null === c ? b.stores = [a] : c.push(a));
    }
    function ci(a, b, c, d) {
      b.value = c;
      b.getSnapshot = d;
      ei(b) && fi(a);
    }
    function ai(a, b, c) {
      return c(function() {
        ei(b) && fi(a);
      });
    }
    function ei(a) {
      var b = a.getSnapshot;
      a = a.value;
      try {
        var c = b();
        return !He(a, c);
      } catch (d) {
        return true;
      }
    }
    function fi(a) {
      var b = ih(a, 1);
      null !== b && gi(b, a, 1, -1);
    }
    function hi(a) {
      var b = Th();
      "function" === typeof a && (a = a());
      b.memoizedState = b.baseState = a;
      a = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: Vh, lastRenderedState: a };
      b.queue = a;
      a = a.dispatch = ii.bind(null, M, a);
      return [b.memoizedState, a];
    }
    function bi(a, b, c, d) {
      a = { tag: a, create: b, destroy: c, deps: d, next: null };
      b = M.updateQueue;
      null === b ? (b = { lastEffect: null, stores: null }, M.updateQueue = b, b.lastEffect = a.next = a) : (c = b.lastEffect, null === c ? b.lastEffect = a.next = a : (d = c.next, c.next = a, a.next = d, b.lastEffect = a));
      return a;
    }
    function ji() {
      return Uh().memoizedState;
    }
    function ki(a, b, c, d) {
      var e = Th();
      M.flags |= a;
      e.memoizedState = bi(1 | b, c, void 0, void 0 === d ? null : d);
    }
    function li(a, b, c, d) {
      var e = Uh();
      d = void 0 === d ? null : d;
      var f = void 0;
      if (null !== N) {
        var g = N.memoizedState;
        f = g.destroy;
        if (null !== d && Mh(d, g.deps)) {
          e.memoizedState = bi(b, c, f, d);
          return;
        }
      }
      M.flags |= a;
      e.memoizedState = bi(1 | b, c, f, d);
    }
    function mi(a, b) {
      return ki(8390656, 8, a, b);
    }
    function $h(a, b) {
      return li(2048, 8, a, b);
    }
    function ni(a, b) {
      return li(4, 2, a, b);
    }
    function oi(a, b) {
      return li(4, 4, a, b);
    }
    function pi(a, b) {
      if ("function" === typeof b) return a = a(), b(a), function() {
        b(null);
      };
      if (null !== b && void 0 !== b) return a = a(), b.current = a, function() {
        b.current = null;
      };
    }
    function qi(a, b, c) {
      c = null !== c && void 0 !== c ? c.concat([a]) : null;
      return li(4, 4, pi.bind(null, b, a), c);
    }
    function ri() {
    }
    function si(a, b) {
      var c = Uh();
      b = void 0 === b ? null : b;
      var d = c.memoizedState;
      if (null !== d && null !== b && Mh(b, d[1])) return d[0];
      c.memoizedState = [a, b];
      return a;
    }
    function ti(a, b) {
      var c = Uh();
      b = void 0 === b ? null : b;
      var d = c.memoizedState;
      if (null !== d && null !== b && Mh(b, d[1])) return d[0];
      a = a();
      c.memoizedState = [a, b];
      return a;
    }
    function ui(a, b, c) {
      if (0 === (Hh & 21)) return a.baseState && (a.baseState = false, dh = true), a.memoizedState = c;
      He(c, b) || (c = yc(), M.lanes |= c, rh |= c, a.baseState = true);
      return b;
    }
    function vi(a, b) {
      var c = C;
      C = 0 !== c && 4 > c ? c : 4;
      a(true);
      var d = Gh.transition;
      Gh.transition = {};
      try {
        a(false), b();
      } finally {
        C = c, Gh.transition = d;
      }
    }
    function wi() {
      return Uh().memoizedState;
    }
    function xi(a, b, c) {
      var d = yi(a);
      c = { lane: d, action: c, hasEagerState: false, eagerState: null, next: null };
      if (zi(a)) Ai(b, c);
      else if (c = hh(a, b, c, d), null !== c) {
        var e = R();
        gi(c, a, d, e);
        Bi(c, b, d);
      }
    }
    function ii(a, b, c) {
      var d = yi(a), e = { lane: d, action: c, hasEagerState: false, eagerState: null, next: null };
      if (zi(a)) Ai(b, e);
      else {
        var f = a.alternate;
        if (0 === a.lanes && (null === f || 0 === f.lanes) && (f = b.lastRenderedReducer, null !== f)) try {
          var g = b.lastRenderedState, h = f(g, c);
          e.hasEagerState = true;
          e.eagerState = h;
          if (He(h, g)) {
            var k = b.interleaved;
            null === k ? (e.next = e, gh(b)) : (e.next = k.next, k.next = e);
            b.interleaved = e;
            return;
          }
        } catch (l) {
        } finally {
        }
        c = hh(a, b, e, d);
        null !== c && (e = R(), gi(c, a, d, e), Bi(c, b, d));
      }
    }
    function zi(a) {
      var b = a.alternate;
      return a === M || null !== b && b === M;
    }
    function Ai(a, b) {
      Jh = Ih = true;
      var c = a.pending;
      null === c ? b.next = b : (b.next = c.next, c.next = b);
      a.pending = b;
    }
    function Bi(a, b, c) {
      if (0 !== (c & 4194240)) {
        var d = b.lanes;
        d &= a.pendingLanes;
        c |= d;
        b.lanes = c;
        Cc(a, c);
      }
    }
    var Rh = { readContext: eh, useCallback: P, useContext: P, useEffect: P, useImperativeHandle: P, useInsertionEffect: P, useLayoutEffect: P, useMemo: P, useReducer: P, useRef: P, useState: P, useDebugValue: P, useDeferredValue: P, useTransition: P, useMutableSource: P, useSyncExternalStore: P, useId: P, unstable_isNewReconciler: false }, Oh = { readContext: eh, useCallback: function(a, b) {
      Th().memoizedState = [a, void 0 === b ? null : b];
      return a;
    }, useContext: eh, useEffect: mi, useImperativeHandle: function(a, b, c) {
      c = null !== c && void 0 !== c ? c.concat([a]) : null;
      return ki(
        4194308,
        4,
        pi.bind(null, b, a),
        c
      );
    }, useLayoutEffect: function(a, b) {
      return ki(4194308, 4, a, b);
    }, useInsertionEffect: function(a, b) {
      return ki(4, 2, a, b);
    }, useMemo: function(a, b) {
      var c = Th();
      b = void 0 === b ? null : b;
      a = a();
      c.memoizedState = [a, b];
      return a;
    }, useReducer: function(a, b, c) {
      var d = Th();
      b = void 0 !== c ? c(b) : b;
      d.memoizedState = d.baseState = b;
      a = { pending: null, interleaved: null, lanes: 0, dispatch: null, lastRenderedReducer: a, lastRenderedState: b };
      d.queue = a;
      a = a.dispatch = xi.bind(null, M, a);
      return [d.memoizedState, a];
    }, useRef: function(a) {
      var b = Th();
      a = { current: a };
      return b.memoizedState = a;
    }, useState: hi, useDebugValue: ri, useDeferredValue: function(a) {
      return Th().memoizedState = a;
    }, useTransition: function() {
      var a = hi(false), b = a[0];
      a = vi.bind(null, a[1]);
      Th().memoizedState = a;
      return [b, a];
    }, useMutableSource: function() {
    }, useSyncExternalStore: function(a, b, c) {
      var d = M, e = Th();
      if (I) {
        if (void 0 === c) throw Error(p(407));
        c = c();
      } else {
        c = b();
        if (null === Q) throw Error(p(349));
        0 !== (Hh & 30) || di(d, b, c);
      }
      e.memoizedState = c;
      var f = { value: c, getSnapshot: b };
      e.queue = f;
      mi(ai.bind(
        null,
        d,
        f,
        a
      ), [a]);
      d.flags |= 2048;
      bi(9, ci.bind(null, d, f, c, b), void 0, null);
      return c;
    }, useId: function() {
      var a = Th(), b = Q.identifierPrefix;
      if (I) {
        var c = sg;
        var d = rg;
        c = (d & ~(1 << 32 - oc(d) - 1)).toString(32) + c;
        b = ":" + b + "R" + c;
        c = Kh++;
        0 < c && (b += "H" + c.toString(32));
        b += ":";
      } else c = Lh++, b = ":" + b + "r" + c.toString(32) + ":";
      return a.memoizedState = b;
    }, unstable_isNewReconciler: false }, Ph = {
      readContext: eh,
      useCallback: si,
      useContext: eh,
      useEffect: $h,
      useImperativeHandle: qi,
      useInsertionEffect: ni,
      useLayoutEffect: oi,
      useMemo: ti,
      useReducer: Wh,
      useRef: ji,
      useState: function() {
        return Wh(Vh);
      },
      useDebugValue: ri,
      useDeferredValue: function(a) {
        var b = Uh();
        return ui(b, N.memoizedState, a);
      },
      useTransition: function() {
        var a = Wh(Vh)[0], b = Uh().memoizedState;
        return [a, b];
      },
      useMutableSource: Yh,
      useSyncExternalStore: Zh,
      useId: wi,
      unstable_isNewReconciler: false
    }, Qh = { readContext: eh, useCallback: si, useContext: eh, useEffect: $h, useImperativeHandle: qi, useInsertionEffect: ni, useLayoutEffect: oi, useMemo: ti, useReducer: Xh, useRef: ji, useState: function() {
      return Xh(Vh);
    }, useDebugValue: ri, useDeferredValue: function(a) {
      var b = Uh();
      return null === N ? b.memoizedState = a : ui(b, N.memoizedState, a);
    }, useTransition: function() {
      var a = Xh(Vh)[0], b = Uh().memoizedState;
      return [a, b];
    }, useMutableSource: Yh, useSyncExternalStore: Zh, useId: wi, unstable_isNewReconciler: false };
    function Ci(a, b) {
      if (a && a.defaultProps) {
        b = A({}, b);
        a = a.defaultProps;
        for (var c in a) void 0 === b[c] && (b[c] = a[c]);
        return b;
      }
      return b;
    }
    function Di(a, b, c, d) {
      b = a.memoizedState;
      c = c(d, b);
      c = null === c || void 0 === c ? b : A({}, b, c);
      a.memoizedState = c;
      0 === a.lanes && (a.updateQueue.baseState = c);
    }
    var Ei = { isMounted: function(a) {
      return (a = a._reactInternals) ? Vb(a) === a : false;
    }, enqueueSetState: function(a, b, c) {
      a = a._reactInternals;
      var d = R(), e = yi(a), f = mh(d, e);
      f.payload = b;
      void 0 !== c && null !== c && (f.callback = c);
      b = nh(a, f, e);
      null !== b && (gi(b, a, e, d), oh(b, a, e));
    }, enqueueReplaceState: function(a, b, c) {
      a = a._reactInternals;
      var d = R(), e = yi(a), f = mh(d, e);
      f.tag = 1;
      f.payload = b;
      void 0 !== c && null !== c && (f.callback = c);
      b = nh(a, f, e);
      null !== b && (gi(b, a, e, d), oh(b, a, e));
    }, enqueueForceUpdate: function(a, b) {
      a = a._reactInternals;
      var c = R(), d = yi(a), e = mh(c, d);
      e.tag = 2;
      void 0 !== b && null !== b && (e.callback = b);
      b = nh(a, e, d);
      null !== b && (gi(b, a, d, c), oh(b, a, d));
    } };
    function Fi(a, b, c, d, e, f, g) {
      a = a.stateNode;
      return "function" === typeof a.shouldComponentUpdate ? a.shouldComponentUpdate(d, f, g) : b.prototype && b.prototype.isPureReactComponent ? !Ie(c, d) || !Ie(e, f) : true;
    }
    function Gi(a, b, c) {
      var d = false, e = Vf;
      var f = b.contextType;
      "object" === typeof f && null !== f ? f = eh(f) : (e = Zf(b) ? Xf : H.current, d = b.contextTypes, f = (d = null !== d && void 0 !== d) ? Yf(a, e) : Vf);
      b = new b(c, f);
      a.memoizedState = null !== b.state && void 0 !== b.state ? b.state : null;
      b.updater = Ei;
      a.stateNode = b;
      b._reactInternals = a;
      d && (a = a.stateNode, a.__reactInternalMemoizedUnmaskedChildContext = e, a.__reactInternalMemoizedMaskedChildContext = f);
      return b;
    }
    function Hi(a, b, c, d) {
      a = b.state;
      "function" === typeof b.componentWillReceiveProps && b.componentWillReceiveProps(c, d);
      "function" === typeof b.UNSAFE_componentWillReceiveProps && b.UNSAFE_componentWillReceiveProps(c, d);
      b.state !== a && Ei.enqueueReplaceState(b, b.state, null);
    }
    function Ii(a, b, c, d) {
      var e = a.stateNode;
      e.props = c;
      e.state = a.memoizedState;
      e.refs = {};
      kh(a);
      var f = b.contextType;
      "object" === typeof f && null !== f ? e.context = eh(f) : (f = Zf(b) ? Xf : H.current, e.context = Yf(a, f));
      e.state = a.memoizedState;
      f = b.getDerivedStateFromProps;
      "function" === typeof f && (Di(a, b, f, c), e.state = a.memoizedState);
      "function" === typeof b.getDerivedStateFromProps || "function" === typeof e.getSnapshotBeforeUpdate || "function" !== typeof e.UNSAFE_componentWillMount && "function" !== typeof e.componentWillMount || (b = e.state, "function" === typeof e.componentWillMount && e.componentWillMount(), "function" === typeof e.UNSAFE_componentWillMount && e.UNSAFE_componentWillMount(), b !== e.state && Ei.enqueueReplaceState(e, e.state, null), qh(a, c, e, d), e.state = a.memoizedState);
      "function" === typeof e.componentDidMount && (a.flags |= 4194308);
    }
    function Ji(a, b) {
      try {
        var c = "", d = b;
        do
          c += Pa(d), d = d.return;
        while (d);
        var e = c;
      } catch (f) {
        e = "\nError generating stack: " + f.message + "\n" + f.stack;
      }
      return { value: a, source: b, stack: e, digest: null };
    }
    function Ki(a, b, c) {
      return { value: a, source: null, stack: null != c ? c : null, digest: null != b ? b : null };
    }
    function Li(a, b) {
      try {
        console.error(b.value);
      } catch (c) {
        setTimeout(function() {
          throw c;
        });
      }
    }
    var Mi = "function" === typeof WeakMap ? WeakMap : Map;
    function Ni(a, b, c) {
      c = mh(-1, c);
      c.tag = 3;
      c.payload = { element: null };
      var d = b.value;
      c.callback = function() {
        Oi || (Oi = true, Pi = d);
        Li(a, b);
      };
      return c;
    }
    function Qi(a, b, c) {
      c = mh(-1, c);
      c.tag = 3;
      var d = a.type.getDerivedStateFromError;
      if ("function" === typeof d) {
        var e = b.value;
        c.payload = function() {
          return d(e);
        };
        c.callback = function() {
          Li(a, b);
        };
      }
      var f = a.stateNode;
      null !== f && "function" === typeof f.componentDidCatch && (c.callback = function() {
        Li(a, b);
        "function" !== typeof d && (null === Ri ? Ri = /* @__PURE__ */ new Set([this]) : Ri.add(this));
        var c2 = b.stack;
        this.componentDidCatch(b.value, { componentStack: null !== c2 ? c2 : "" });
      });
      return c;
    }
    function Si(a, b, c) {
      var d = a.pingCache;
      if (null === d) {
        d = a.pingCache = new Mi();
        var e = /* @__PURE__ */ new Set();
        d.set(b, e);
      } else e = d.get(b), void 0 === e && (e = /* @__PURE__ */ new Set(), d.set(b, e));
      e.has(c) || (e.add(c), a = Ti.bind(null, a, b, c), b.then(a, a));
    }
    function Ui(a) {
      do {
        var b;
        if (b = 13 === a.tag) b = a.memoizedState, b = null !== b ? null !== b.dehydrated ? true : false : true;
        if (b) return a;
        a = a.return;
      } while (null !== a);
      return null;
    }
    function Vi(a, b, c, d, e) {
      if (0 === (a.mode & 1)) return a === b ? a.flags |= 65536 : (a.flags |= 128, c.flags |= 131072, c.flags &= -52805, 1 === c.tag && (null === c.alternate ? c.tag = 17 : (b = mh(-1, 1), b.tag = 2, nh(c, b, 1))), c.lanes |= 1), a;
      a.flags |= 65536;
      a.lanes = e;
      return a;
    }
    var Wi = ua.ReactCurrentOwner, dh = false;
    function Xi(a, b, c, d) {
      b.child = null === a ? Vg(b, null, c, d) : Ug(b, a.child, c, d);
    }
    function Yi(a, b, c, d, e) {
      c = c.render;
      var f = b.ref;
      ch(b, e);
      d = Nh(a, b, c, d, f, e);
      c = Sh();
      if (null !== a && !dh) return b.updateQueue = a.updateQueue, b.flags &= -2053, a.lanes &= ~e, Zi(a, b, e);
      I && c && vg(b);
      b.flags |= 1;
      Xi(a, b, d, e);
      return b.child;
    }
    function $i(a, b, c, d, e) {
      if (null === a) {
        var f = c.type;
        if ("function" === typeof f && !aj(f) && void 0 === f.defaultProps && null === c.compare && void 0 === c.defaultProps) return b.tag = 15, b.type = f, bj(a, b, f, d, e);
        a = Rg(c.type, null, d, b, b.mode, e);
        a.ref = b.ref;
        a.return = b;
        return b.child = a;
      }
      f = a.child;
      if (0 === (a.lanes & e)) {
        var g = f.memoizedProps;
        c = c.compare;
        c = null !== c ? c : Ie;
        if (c(g, d) && a.ref === b.ref) return Zi(a, b, e);
      }
      b.flags |= 1;
      a = Pg(f, d);
      a.ref = b.ref;
      a.return = b;
      return b.child = a;
    }
    function bj(a, b, c, d, e) {
      if (null !== a) {
        var f = a.memoizedProps;
        if (Ie(f, d) && a.ref === b.ref) if (dh = false, b.pendingProps = d = f, 0 !== (a.lanes & e)) 0 !== (a.flags & 131072) && (dh = true);
        else return b.lanes = a.lanes, Zi(a, b, e);
      }
      return cj(a, b, c, d, e);
    }
    function dj(a, b, c) {
      var d = b.pendingProps, e = d.children, f = null !== a ? a.memoizedState : null;
      if ("hidden" === d.mode) if (0 === (b.mode & 1)) b.memoizedState = { baseLanes: 0, cachePool: null, transitions: null }, G(ej, fj), fj |= c;
      else {
        if (0 === (c & 1073741824)) return a = null !== f ? f.baseLanes | c : c, b.lanes = b.childLanes = 1073741824, b.memoizedState = { baseLanes: a, cachePool: null, transitions: null }, b.updateQueue = null, G(ej, fj), fj |= a, null;
        b.memoizedState = { baseLanes: 0, cachePool: null, transitions: null };
        d = null !== f ? f.baseLanes : c;
        G(ej, fj);
        fj |= d;
      }
      else null !== f ? (d = f.baseLanes | c, b.memoizedState = null) : d = c, G(ej, fj), fj |= d;
      Xi(a, b, e, c);
      return b.child;
    }
    function gj(a, b) {
      var c = b.ref;
      if (null === a && null !== c || null !== a && a.ref !== c) b.flags |= 512, b.flags |= 2097152;
    }
    function cj(a, b, c, d, e) {
      var f = Zf(c) ? Xf : H.current;
      f = Yf(b, f);
      ch(b, e);
      c = Nh(a, b, c, d, f, e);
      d = Sh();
      if (null !== a && !dh) return b.updateQueue = a.updateQueue, b.flags &= -2053, a.lanes &= ~e, Zi(a, b, e);
      I && d && vg(b);
      b.flags |= 1;
      Xi(a, b, c, e);
      return b.child;
    }
    function hj(a, b, c, d, e) {
      if (Zf(c)) {
        var f = true;
        cg(b);
      } else f = false;
      ch(b, e);
      if (null === b.stateNode) ij(a, b), Gi(b, c, d), Ii(b, c, d, e), d = true;
      else if (null === a) {
        var g = b.stateNode, h = b.memoizedProps;
        g.props = h;
        var k = g.context, l = c.contextType;
        "object" === typeof l && null !== l ? l = eh(l) : (l = Zf(c) ? Xf : H.current, l = Yf(b, l));
        var m = c.getDerivedStateFromProps, q = "function" === typeof m || "function" === typeof g.getSnapshotBeforeUpdate;
        q || "function" !== typeof g.UNSAFE_componentWillReceiveProps && "function" !== typeof g.componentWillReceiveProps || (h !== d || k !== l) && Hi(b, g, d, l);
        jh = false;
        var r = b.memoizedState;
        g.state = r;
        qh(b, d, g, e);
        k = b.memoizedState;
        h !== d || r !== k || Wf.current || jh ? ("function" === typeof m && (Di(b, c, m, d), k = b.memoizedState), (h = jh || Fi(b, c, h, d, r, k, l)) ? (q || "function" !== typeof g.UNSAFE_componentWillMount && "function" !== typeof g.componentWillMount || ("function" === typeof g.componentWillMount && g.componentWillMount(), "function" === typeof g.UNSAFE_componentWillMount && g.UNSAFE_componentWillMount()), "function" === typeof g.componentDidMount && (b.flags |= 4194308)) : ("function" === typeof g.componentDidMount && (b.flags |= 4194308), b.memoizedProps = d, b.memoizedState = k), g.props = d, g.state = k, g.context = l, d = h) : ("function" === typeof g.componentDidMount && (b.flags |= 4194308), d = false);
      } else {
        g = b.stateNode;
        lh(a, b);
        h = b.memoizedProps;
        l = b.type === b.elementType ? h : Ci(b.type, h);
        g.props = l;
        q = b.pendingProps;
        r = g.context;
        k = c.contextType;
        "object" === typeof k && null !== k ? k = eh(k) : (k = Zf(c) ? Xf : H.current, k = Yf(b, k));
        var y = c.getDerivedStateFromProps;
        (m = "function" === typeof y || "function" === typeof g.getSnapshotBeforeUpdate) || "function" !== typeof g.UNSAFE_componentWillReceiveProps && "function" !== typeof g.componentWillReceiveProps || (h !== q || r !== k) && Hi(b, g, d, k);
        jh = false;
        r = b.memoizedState;
        g.state = r;
        qh(b, d, g, e);
        var n = b.memoizedState;
        h !== q || r !== n || Wf.current || jh ? ("function" === typeof y && (Di(b, c, y, d), n = b.memoizedState), (l = jh || Fi(b, c, l, d, r, n, k) || false) ? (m || "function" !== typeof g.UNSAFE_componentWillUpdate && "function" !== typeof g.componentWillUpdate || ("function" === typeof g.componentWillUpdate && g.componentWillUpdate(d, n, k), "function" === typeof g.UNSAFE_componentWillUpdate && g.UNSAFE_componentWillUpdate(d, n, k)), "function" === typeof g.componentDidUpdate && (b.flags |= 4), "function" === typeof g.getSnapshotBeforeUpdate && (b.flags |= 1024)) : ("function" !== typeof g.componentDidUpdate || h === a.memoizedProps && r === a.memoizedState || (b.flags |= 4), "function" !== typeof g.getSnapshotBeforeUpdate || h === a.memoizedProps && r === a.memoizedState || (b.flags |= 1024), b.memoizedProps = d, b.memoizedState = n), g.props = d, g.state = n, g.context = k, d = l) : ("function" !== typeof g.componentDidUpdate || h === a.memoizedProps && r === a.memoizedState || (b.flags |= 4), "function" !== typeof g.getSnapshotBeforeUpdate || h === a.memoizedProps && r === a.memoizedState || (b.flags |= 1024), d = false);
      }
      return jj(a, b, c, d, f, e);
    }
    function jj(a, b, c, d, e, f) {
      gj(a, b);
      var g = 0 !== (b.flags & 128);
      if (!d && !g) return e && dg(b, c, false), Zi(a, b, f);
      d = b.stateNode;
      Wi.current = b;
      var h = g && "function" !== typeof c.getDerivedStateFromError ? null : d.render();
      b.flags |= 1;
      null !== a && g ? (b.child = Ug(b, a.child, null, f), b.child = Ug(b, null, h, f)) : Xi(a, b, h, f);
      b.memoizedState = d.state;
      e && dg(b, c, true);
      return b.child;
    }
    function kj(a) {
      var b = a.stateNode;
      b.pendingContext ? ag(a, b.pendingContext, b.pendingContext !== b.context) : b.context && ag(a, b.context, false);
      yh(a, b.containerInfo);
    }
    function lj(a, b, c, d, e) {
      Ig();
      Jg(e);
      b.flags |= 256;
      Xi(a, b, c, d);
      return b.child;
    }
    var mj = { dehydrated: null, treeContext: null, retryLane: 0 };
    function nj(a) {
      return { baseLanes: a, cachePool: null, transitions: null };
    }
    function oj(a, b, c) {
      var d = b.pendingProps, e = L.current, f = false, g = 0 !== (b.flags & 128), h;
      (h = g) || (h = null !== a && null === a.memoizedState ? false : 0 !== (e & 2));
      if (h) f = true, b.flags &= -129;
      else if (null === a || null !== a.memoizedState) e |= 1;
      G(L, e & 1);
      if (null === a) {
        Eg(b);
        a = b.memoizedState;
        if (null !== a && (a = a.dehydrated, null !== a)) return 0 === (b.mode & 1) ? b.lanes = 1 : "$!" === a.data ? b.lanes = 8 : b.lanes = 1073741824, null;
        g = d.children;
        a = d.fallback;
        return f ? (d = b.mode, f = b.child, g = { mode: "hidden", children: g }, 0 === (d & 1) && null !== f ? (f.childLanes = 0, f.pendingProps = g) : f = pj(g, d, 0, null), a = Tg(a, d, c, null), f.return = b, a.return = b, f.sibling = a, b.child = f, b.child.memoizedState = nj(c), b.memoizedState = mj, a) : qj(b, g);
      }
      e = a.memoizedState;
      if (null !== e && (h = e.dehydrated, null !== h)) return rj(a, b, g, d, h, e, c);
      if (f) {
        f = d.fallback;
        g = b.mode;
        e = a.child;
        h = e.sibling;
        var k = { mode: "hidden", children: d.children };
        0 === (g & 1) && b.child !== e ? (d = b.child, d.childLanes = 0, d.pendingProps = k, b.deletions = null) : (d = Pg(e, k), d.subtreeFlags = e.subtreeFlags & 14680064);
        null !== h ? f = Pg(h, f) : (f = Tg(f, g, c, null), f.flags |= 2);
        f.return = b;
        d.return = b;
        d.sibling = f;
        b.child = d;
        d = f;
        f = b.child;
        g = a.child.memoizedState;
        g = null === g ? nj(c) : { baseLanes: g.baseLanes | c, cachePool: null, transitions: g.transitions };
        f.memoizedState = g;
        f.childLanes = a.childLanes & ~c;
        b.memoizedState = mj;
        return d;
      }
      f = a.child;
      a = f.sibling;
      d = Pg(f, { mode: "visible", children: d.children });
      0 === (b.mode & 1) && (d.lanes = c);
      d.return = b;
      d.sibling = null;
      null !== a && (c = b.deletions, null === c ? (b.deletions = [a], b.flags |= 16) : c.push(a));
      b.child = d;
      b.memoizedState = null;
      return d;
    }
    function qj(a, b) {
      b = pj({ mode: "visible", children: b }, a.mode, 0, null);
      b.return = a;
      return a.child = b;
    }
    function sj(a, b, c, d) {
      null !== d && Jg(d);
      Ug(b, a.child, null, c);
      a = qj(b, b.pendingProps.children);
      a.flags |= 2;
      b.memoizedState = null;
      return a;
    }
    function rj(a, b, c, d, e, f, g) {
      if (c) {
        if (b.flags & 256) return b.flags &= -257, d = Ki(Error(p(422))), sj(a, b, g, d);
        if (null !== b.memoizedState) return b.child = a.child, b.flags |= 128, null;
        f = d.fallback;
        e = b.mode;
        d = pj({ mode: "visible", children: d.children }, e, 0, null);
        f = Tg(f, e, g, null);
        f.flags |= 2;
        d.return = b;
        f.return = b;
        d.sibling = f;
        b.child = d;
        0 !== (b.mode & 1) && Ug(b, a.child, null, g);
        b.child.memoizedState = nj(g);
        b.memoizedState = mj;
        return f;
      }
      if (0 === (b.mode & 1)) return sj(a, b, g, null);
      if ("$!" === e.data) {
        d = e.nextSibling && e.nextSibling.dataset;
        if (d) var h = d.dgst;
        d = h;
        f = Error(p(419));
        d = Ki(f, d, void 0);
        return sj(a, b, g, d);
      }
      h = 0 !== (g & a.childLanes);
      if (dh || h) {
        d = Q;
        if (null !== d) {
          switch (g & -g) {
            case 4:
              e = 2;
              break;
            case 16:
              e = 8;
              break;
            case 64:
            case 128:
            case 256:
            case 512:
            case 1024:
            case 2048:
            case 4096:
            case 8192:
            case 16384:
            case 32768:
            case 65536:
            case 131072:
            case 262144:
            case 524288:
            case 1048576:
            case 2097152:
            case 4194304:
            case 8388608:
            case 16777216:
            case 33554432:
            case 67108864:
              e = 32;
              break;
            case 536870912:
              e = 268435456;
              break;
            default:
              e = 0;
          }
          e = 0 !== (e & (d.suspendedLanes | g)) ? 0 : e;
          0 !== e && e !== f.retryLane && (f.retryLane = e, ih(a, e), gi(d, a, e, -1));
        }
        tj();
        d = Ki(Error(p(421)));
        return sj(a, b, g, d);
      }
      if ("$?" === e.data) return b.flags |= 128, b.child = a.child, b = uj.bind(null, a), e._reactRetry = b, null;
      a = f.treeContext;
      yg = Lf(e.nextSibling);
      xg = b;
      I = true;
      zg = null;
      null !== a && (og[pg++] = rg, og[pg++] = sg, og[pg++] = qg, rg = a.id, sg = a.overflow, qg = b);
      b = qj(b, d.children);
      b.flags |= 4096;
      return b;
    }
    function vj(a, b, c) {
      a.lanes |= b;
      var d = a.alternate;
      null !== d && (d.lanes |= b);
      bh(a.return, b, c);
    }
    function wj(a, b, c, d, e) {
      var f = a.memoizedState;
      null === f ? a.memoizedState = { isBackwards: b, rendering: null, renderingStartTime: 0, last: d, tail: c, tailMode: e } : (f.isBackwards = b, f.rendering = null, f.renderingStartTime = 0, f.last = d, f.tail = c, f.tailMode = e);
    }
    function xj(a, b, c) {
      var d = b.pendingProps, e = d.revealOrder, f = d.tail;
      Xi(a, b, d.children, c);
      d = L.current;
      if (0 !== (d & 2)) d = d & 1 | 2, b.flags |= 128;
      else {
        if (null !== a && 0 !== (a.flags & 128)) a: for (a = b.child; null !== a; ) {
          if (13 === a.tag) null !== a.memoizedState && vj(a, c, b);
          else if (19 === a.tag) vj(a, c, b);
          else if (null !== a.child) {
            a.child.return = a;
            a = a.child;
            continue;
          }
          if (a === b) break a;
          for (; null === a.sibling; ) {
            if (null === a.return || a.return === b) break a;
            a = a.return;
          }
          a.sibling.return = a.return;
          a = a.sibling;
        }
        d &= 1;
      }
      G(L, d);
      if (0 === (b.mode & 1)) b.memoizedState = null;
      else switch (e) {
        case "forwards":
          c = b.child;
          for (e = null; null !== c; ) a = c.alternate, null !== a && null === Ch(a) && (e = c), c = c.sibling;
          c = e;
          null === c ? (e = b.child, b.child = null) : (e = c.sibling, c.sibling = null);
          wj(b, false, e, c, f);
          break;
        case "backwards":
          c = null;
          e = b.child;
          for (b.child = null; null !== e; ) {
            a = e.alternate;
            if (null !== a && null === Ch(a)) {
              b.child = e;
              break;
            }
            a = e.sibling;
            e.sibling = c;
            c = e;
            e = a;
          }
          wj(b, true, c, null, f);
          break;
        case "together":
          wj(b, false, null, null, void 0);
          break;
        default:
          b.memoizedState = null;
      }
      return b.child;
    }
    function ij(a, b) {
      0 === (b.mode & 1) && null !== a && (a.alternate = null, b.alternate = null, b.flags |= 2);
    }
    function Zi(a, b, c) {
      null !== a && (b.dependencies = a.dependencies);
      rh |= b.lanes;
      if (0 === (c & b.childLanes)) return null;
      if (null !== a && b.child !== a.child) throw Error(p(153));
      if (null !== b.child) {
        a = b.child;
        c = Pg(a, a.pendingProps);
        b.child = c;
        for (c.return = b; null !== a.sibling; ) a = a.sibling, c = c.sibling = Pg(a, a.pendingProps), c.return = b;
        c.sibling = null;
      }
      return b.child;
    }
    function yj(a, b, c) {
      switch (b.tag) {
        case 3:
          kj(b);
          Ig();
          break;
        case 5:
          Ah(b);
          break;
        case 1:
          Zf(b.type) && cg(b);
          break;
        case 4:
          yh(b, b.stateNode.containerInfo);
          break;
        case 10:
          var d = b.type._context, e = b.memoizedProps.value;
          G(Wg, d._currentValue);
          d._currentValue = e;
          break;
        case 13:
          d = b.memoizedState;
          if (null !== d) {
            if (null !== d.dehydrated) return G(L, L.current & 1), b.flags |= 128, null;
            if (0 !== (c & b.child.childLanes)) return oj(a, b, c);
            G(L, L.current & 1);
            a = Zi(a, b, c);
            return null !== a ? a.sibling : null;
          }
          G(L, L.current & 1);
          break;
        case 19:
          d = 0 !== (c & b.childLanes);
          if (0 !== (a.flags & 128)) {
            if (d) return xj(a, b, c);
            b.flags |= 128;
          }
          e = b.memoizedState;
          null !== e && (e.rendering = null, e.tail = null, e.lastEffect = null);
          G(L, L.current);
          if (d) break;
          else return null;
        case 22:
        case 23:
          return b.lanes = 0, dj(a, b, c);
      }
      return Zi(a, b, c);
    }
    var zj, Aj, Bj, Cj;
    zj = function(a, b) {
      for (var c = b.child; null !== c; ) {
        if (5 === c.tag || 6 === c.tag) a.appendChild(c.stateNode);
        else if (4 !== c.tag && null !== c.child) {
          c.child.return = c;
          c = c.child;
          continue;
        }
        if (c === b) break;
        for (; null === c.sibling; ) {
          if (null === c.return || c.return === b) return;
          c = c.return;
        }
        c.sibling.return = c.return;
        c = c.sibling;
      }
    };
    Aj = function() {
    };
    Bj = function(a, b, c, d) {
      var e = a.memoizedProps;
      if (e !== d) {
        a = b.stateNode;
        xh(uh.current);
        var f = null;
        switch (c) {
          case "input":
            e = Ya(a, e);
            d = Ya(a, d);
            f = [];
            break;
          case "select":
            e = A({}, e, { value: void 0 });
            d = A({}, d, { value: void 0 });
            f = [];
            break;
          case "textarea":
            e = gb(a, e);
            d = gb(a, d);
            f = [];
            break;
          default:
            "function" !== typeof e.onClick && "function" === typeof d.onClick && (a.onclick = Bf);
        }
        ub(c, d);
        var g;
        c = null;
        for (l in e) if (!d.hasOwnProperty(l) && e.hasOwnProperty(l) && null != e[l]) if ("style" === l) {
          var h = e[l];
          for (g in h) h.hasOwnProperty(g) && (c || (c = {}), c[g] = "");
        } else "dangerouslySetInnerHTML" !== l && "children" !== l && "suppressContentEditableWarning" !== l && "suppressHydrationWarning" !== l && "autoFocus" !== l && (ea.hasOwnProperty(l) ? f || (f = []) : (f = f || []).push(l, null));
        for (l in d) {
          var k = d[l];
          h = null != e ? e[l] : void 0;
          if (d.hasOwnProperty(l) && k !== h && (null != k || null != h)) if ("style" === l) if (h) {
            for (g in h) !h.hasOwnProperty(g) || k && k.hasOwnProperty(g) || (c || (c = {}), c[g] = "");
            for (g in k) k.hasOwnProperty(g) && h[g] !== k[g] && (c || (c = {}), c[g] = k[g]);
          } else c || (f || (f = []), f.push(
            l,
            c
          )), c = k;
          else "dangerouslySetInnerHTML" === l ? (k = k ? k.__html : void 0, h = h ? h.__html : void 0, null != k && h !== k && (f = f || []).push(l, k)) : "children" === l ? "string" !== typeof k && "number" !== typeof k || (f = f || []).push(l, "" + k) : "suppressContentEditableWarning" !== l && "suppressHydrationWarning" !== l && (ea.hasOwnProperty(l) ? (null != k && "onScroll" === l && D("scroll", a), f || h === k || (f = [])) : (f = f || []).push(l, k));
        }
        c && (f = f || []).push("style", c);
        var l = f;
        if (b.updateQueue = l) b.flags |= 4;
      }
    };
    Cj = function(a, b, c, d) {
      c !== d && (b.flags |= 4);
    };
    function Dj(a, b) {
      if (!I) switch (a.tailMode) {
        case "hidden":
          b = a.tail;
          for (var c = null; null !== b; ) null !== b.alternate && (c = b), b = b.sibling;
          null === c ? a.tail = null : c.sibling = null;
          break;
        case "collapsed":
          c = a.tail;
          for (var d = null; null !== c; ) null !== c.alternate && (d = c), c = c.sibling;
          null === d ? b || null === a.tail ? a.tail = null : a.tail.sibling = null : d.sibling = null;
      }
    }
    function S(a) {
      var b = null !== a.alternate && a.alternate.child === a.child, c = 0, d = 0;
      if (b) for (var e = a.child; null !== e; ) c |= e.lanes | e.childLanes, d |= e.subtreeFlags & 14680064, d |= e.flags & 14680064, e.return = a, e = e.sibling;
      else for (e = a.child; null !== e; ) c |= e.lanes | e.childLanes, d |= e.subtreeFlags, d |= e.flags, e.return = a, e = e.sibling;
      a.subtreeFlags |= d;
      a.childLanes = c;
      return b;
    }
    function Ej(a, b, c) {
      var d = b.pendingProps;
      wg(b);
      switch (b.tag) {
        case 2:
        case 16:
        case 15:
        case 0:
        case 11:
        case 7:
        case 8:
        case 12:
        case 9:
        case 14:
          return S(b), null;
        case 1:
          return Zf(b.type) && $f(), S(b), null;
        case 3:
          d = b.stateNode;
          zh2();
          E(Wf);
          E(H);
          Eh();
          d.pendingContext && (d.context = d.pendingContext, d.pendingContext = null);
          if (null === a || null === a.child) Gg(b) ? b.flags |= 4 : null === a || a.memoizedState.isDehydrated && 0 === (b.flags & 256) || (b.flags |= 1024, null !== zg && (Fj(zg), zg = null));
          Aj(a, b);
          S(b);
          return null;
        case 5:
          Bh(b);
          var e = xh(wh.current);
          c = b.type;
          if (null !== a && null != b.stateNode) Bj(a, b, c, d, e), a.ref !== b.ref && (b.flags |= 512, b.flags |= 2097152);
          else {
            if (!d) {
              if (null === b.stateNode) throw Error(p(166));
              S(b);
              return null;
            }
            a = xh(uh.current);
            if (Gg(b)) {
              d = b.stateNode;
              c = b.type;
              var f = b.memoizedProps;
              d[Of] = b;
              d[Pf] = f;
              a = 0 !== (b.mode & 1);
              switch (c) {
                case "dialog":
                  D("cancel", d);
                  D("close", d);
                  break;
                case "iframe":
                case "object":
                case "embed":
                  D("load", d);
                  break;
                case "video":
                case "audio":
                  for (e = 0; e < lf.length; e++) D(lf[e], d);
                  break;
                case "source":
                  D("error", d);
                  break;
                case "img":
                case "image":
                case "link":
                  D(
                    "error",
                    d
                  );
                  D("load", d);
                  break;
                case "details":
                  D("toggle", d);
                  break;
                case "input":
                  Za(d, f);
                  D("invalid", d);
                  break;
                case "select":
                  d._wrapperState = { wasMultiple: !!f.multiple };
                  D("invalid", d);
                  break;
                case "textarea":
                  hb(d, f), D("invalid", d);
              }
              ub(c, f);
              e = null;
              for (var g in f) if (f.hasOwnProperty(g)) {
                var h = f[g];
                "children" === g ? "string" === typeof h ? d.textContent !== h && (true !== f.suppressHydrationWarning && Af(d.textContent, h, a), e = ["children", h]) : "number" === typeof h && d.textContent !== "" + h && (true !== f.suppressHydrationWarning && Af(
                  d.textContent,
                  h,
                  a
                ), e = ["children", "" + h]) : ea.hasOwnProperty(g) && null != h && "onScroll" === g && D("scroll", d);
              }
              switch (c) {
                case "input":
                  Va(d);
                  db(d, f, true);
                  break;
                case "textarea":
                  Va(d);
                  jb(d);
                  break;
                case "select":
                case "option":
                  break;
                default:
                  "function" === typeof f.onClick && (d.onclick = Bf);
              }
              d = e;
              b.updateQueue = d;
              null !== d && (b.flags |= 4);
            } else {
              g = 9 === e.nodeType ? e : e.ownerDocument;
              "http://www.w3.org/1999/xhtml" === a && (a = kb(c));
              "http://www.w3.org/1999/xhtml" === a ? "script" === c ? (a = g.createElement("div"), a.innerHTML = "<script><\/script>", a = a.removeChild(a.firstChild)) : "string" === typeof d.is ? a = g.createElement(c, { is: d.is }) : (a = g.createElement(c), "select" === c && (g = a, d.multiple ? g.multiple = true : d.size && (g.size = d.size))) : a = g.createElementNS(a, c);
              a[Of] = b;
              a[Pf] = d;
              zj(a, b, false, false);
              b.stateNode = a;
              a: {
                g = vb(c, d);
                switch (c) {
                  case "dialog":
                    D("cancel", a);
                    D("close", a);
                    e = d;
                    break;
                  case "iframe":
                  case "object":
                  case "embed":
                    D("load", a);
                    e = d;
                    break;
                  case "video":
                  case "audio":
                    for (e = 0; e < lf.length; e++) D(lf[e], a);
                    e = d;
                    break;
                  case "source":
                    D("error", a);
                    e = d;
                    break;
                  case "img":
                  case "image":
                  case "link":
                    D(
                      "error",
                      a
                    );
                    D("load", a);
                    e = d;
                    break;
                  case "details":
                    D("toggle", a);
                    e = d;
                    break;
                  case "input":
                    Za(a, d);
                    e = Ya(a, d);
                    D("invalid", a);
                    break;
                  case "option":
                    e = d;
                    break;
                  case "select":
                    a._wrapperState = { wasMultiple: !!d.multiple };
                    e = A({}, d, { value: void 0 });
                    D("invalid", a);
                    break;
                  case "textarea":
                    hb(a, d);
                    e = gb(a, d);
                    D("invalid", a);
                    break;
                  default:
                    e = d;
                }
                ub(c, e);
                h = e;
                for (f in h) if (h.hasOwnProperty(f)) {
                  var k = h[f];
                  "style" === f ? sb(a, k) : "dangerouslySetInnerHTML" === f ? (k = k ? k.__html : void 0, null != k && nb(a, k)) : "children" === f ? "string" === typeof k ? ("textarea" !== c || "" !== k) && ob(a, k) : "number" === typeof k && ob(a, "" + k) : "suppressContentEditableWarning" !== f && "suppressHydrationWarning" !== f && "autoFocus" !== f && (ea.hasOwnProperty(f) ? null != k && "onScroll" === f && D("scroll", a) : null != k && ta(a, f, k, g));
                }
                switch (c) {
                  case "input":
                    Va(a);
                    db(a, d, false);
                    break;
                  case "textarea":
                    Va(a);
                    jb(a);
                    break;
                  case "option":
                    null != d.value && a.setAttribute("value", "" + Sa(d.value));
                    break;
                  case "select":
                    a.multiple = !!d.multiple;
                    f = d.value;
                    null != f ? fb(a, !!d.multiple, f, false) : null != d.defaultValue && fb(
                      a,
                      !!d.multiple,
                      d.defaultValue,
                      true
                    );
                    break;
                  default:
                    "function" === typeof e.onClick && (a.onclick = Bf);
                }
                switch (c) {
                  case "button":
                  case "input":
                  case "select":
                  case "textarea":
                    d = !!d.autoFocus;
                    break a;
                  case "img":
                    d = true;
                    break a;
                  default:
                    d = false;
                }
              }
              d && (b.flags |= 4);
            }
            null !== b.ref && (b.flags |= 512, b.flags |= 2097152);
          }
          S(b);
          return null;
        case 6:
          if (a && null != b.stateNode) Cj(a, b, a.memoizedProps, d);
          else {
            if ("string" !== typeof d && null === b.stateNode) throw Error(p(166));
            c = xh(wh.current);
            xh(uh.current);
            if (Gg(b)) {
              d = b.stateNode;
              c = b.memoizedProps;
              d[Of] = b;
              if (f = d.nodeValue !== c) {
                if (a = xg, null !== a) switch (a.tag) {
                  case 3:
                    Af(d.nodeValue, c, 0 !== (a.mode & 1));
                    break;
                  case 5:
                    true !== a.memoizedProps.suppressHydrationWarning && Af(d.nodeValue, c, 0 !== (a.mode & 1));
                }
              }
              f && (b.flags |= 4);
            } else d = (9 === c.nodeType ? c : c.ownerDocument).createTextNode(d), d[Of] = b, b.stateNode = d;
          }
          S(b);
          return null;
        case 13:
          E(L);
          d = b.memoizedState;
          if (null === a || null !== a.memoizedState && null !== a.memoizedState.dehydrated) {
            if (I && null !== yg && 0 !== (b.mode & 1) && 0 === (b.flags & 128)) Hg(), Ig(), b.flags |= 98560, f = false;
            else if (f = Gg(b), null !== d && null !== d.dehydrated) {
              if (null === a) {
                if (!f) throw Error(p(318));
                f = b.memoizedState;
                f = null !== f ? f.dehydrated : null;
                if (!f) throw Error(p(317));
                f[Of] = b;
              } else Ig(), 0 === (b.flags & 128) && (b.memoizedState = null), b.flags |= 4;
              S(b);
              f = false;
            } else null !== zg && (Fj(zg), zg = null), f = true;
            if (!f) return b.flags & 65536 ? b : null;
          }
          if (0 !== (b.flags & 128)) return b.lanes = c, b;
          d = null !== d;
          d !== (null !== a && null !== a.memoizedState) && d && (b.child.flags |= 8192, 0 !== (b.mode & 1) && (null === a || 0 !== (L.current & 1) ? 0 === T && (T = 3) : tj()));
          null !== b.updateQueue && (b.flags |= 4);
          S(b);
          return null;
        case 4:
          return zh2(), Aj(a, b), null === a && sf(b.stateNode.containerInfo), S(b), null;
        case 10:
          return ah(b.type._context), S(b), null;
        case 17:
          return Zf(b.type) && $f(), S(b), null;
        case 19:
          E(L);
          f = b.memoizedState;
          if (null === f) return S(b), null;
          d = 0 !== (b.flags & 128);
          g = f.rendering;
          if (null === g) if (d) Dj(f, false);
          else {
            if (0 !== T || null !== a && 0 !== (a.flags & 128)) for (a = b.child; null !== a; ) {
              g = Ch(a);
              if (null !== g) {
                b.flags |= 128;
                Dj(f, false);
                d = g.updateQueue;
                null !== d && (b.updateQueue = d, b.flags |= 4);
                b.subtreeFlags = 0;
                d = c;
                for (c = b.child; null !== c; ) f = c, a = d, f.flags &= 14680066, g = f.alternate, null === g ? (f.childLanes = 0, f.lanes = a, f.child = null, f.subtreeFlags = 0, f.memoizedProps = null, f.memoizedState = null, f.updateQueue = null, f.dependencies = null, f.stateNode = null) : (f.childLanes = g.childLanes, f.lanes = g.lanes, f.child = g.child, f.subtreeFlags = 0, f.deletions = null, f.memoizedProps = g.memoizedProps, f.memoizedState = g.memoizedState, f.updateQueue = g.updateQueue, f.type = g.type, a = g.dependencies, f.dependencies = null === a ? null : { lanes: a.lanes, firstContext: a.firstContext }), c = c.sibling;
                G(L, L.current & 1 | 2);
                return b.child;
              }
              a = a.sibling;
            }
            null !== f.tail && B() > Gj && (b.flags |= 128, d = true, Dj(f, false), b.lanes = 4194304);
          }
          else {
            if (!d) if (a = Ch(g), null !== a) {
              if (b.flags |= 128, d = true, c = a.updateQueue, null !== c && (b.updateQueue = c, b.flags |= 4), Dj(f, true), null === f.tail && "hidden" === f.tailMode && !g.alternate && !I) return S(b), null;
            } else 2 * B() - f.renderingStartTime > Gj && 1073741824 !== c && (b.flags |= 128, d = true, Dj(f, false), b.lanes = 4194304);
            f.isBackwards ? (g.sibling = b.child, b.child = g) : (c = f.last, null !== c ? c.sibling = g : b.child = g, f.last = g);
          }
          if (null !== f.tail) return b = f.tail, f.rendering = b, f.tail = b.sibling, f.renderingStartTime = B(), b.sibling = null, c = L.current, G(L, d ? c & 1 | 2 : c & 1), b;
          S(b);
          return null;
        case 22:
        case 23:
          return Hj(), d = null !== b.memoizedState, null !== a && null !== a.memoizedState !== d && (b.flags |= 8192), d && 0 !== (b.mode & 1) ? 0 !== (fj & 1073741824) && (S(b), b.subtreeFlags & 6 && (b.flags |= 8192)) : S(b), null;
        case 24:
          return null;
        case 25:
          return null;
      }
      throw Error(p(156, b.tag));
    }
    function Ij(a, b) {
      wg(b);
      switch (b.tag) {
        case 1:
          return Zf(b.type) && $f(), a = b.flags, a & 65536 ? (b.flags = a & -65537 | 128, b) : null;
        case 3:
          return zh2(), E(Wf), E(H), Eh(), a = b.flags, 0 !== (a & 65536) && 0 === (a & 128) ? (b.flags = a & -65537 | 128, b) : null;
        case 5:
          return Bh(b), null;
        case 13:
          E(L);
          a = b.memoizedState;
          if (null !== a && null !== a.dehydrated) {
            if (null === b.alternate) throw Error(p(340));
            Ig();
          }
          a = b.flags;
          return a & 65536 ? (b.flags = a & -65537 | 128, b) : null;
        case 19:
          return E(L), null;
        case 4:
          return zh2(), null;
        case 10:
          return ah(b.type._context), null;
        case 22:
        case 23:
          return Hj(), null;
        case 24:
          return null;
        default:
          return null;
      }
    }
    var Jj = false, U = false, Kj = "function" === typeof WeakSet ? WeakSet : Set, V = null;
    function Lj(a, b) {
      var c = a.ref;
      if (null !== c) if ("function" === typeof c) try {
        c(null);
      } catch (d) {
        W(a, b, d);
      }
      else c.current = null;
    }
    function Mj(a, b, c) {
      try {
        c();
      } catch (d) {
        W(a, b, d);
      }
    }
    var Nj = false;
    function Oj(a, b) {
      Cf = dd;
      a = Me();
      if (Ne(a)) {
        if ("selectionStart" in a) var c = { start: a.selectionStart, end: a.selectionEnd };
        else a: {
          c = (c = a.ownerDocument) && c.defaultView || window;
          var d = c.getSelection && c.getSelection();
          if (d && 0 !== d.rangeCount) {
            c = d.anchorNode;
            var e = d.anchorOffset, f = d.focusNode;
            d = d.focusOffset;
            try {
              c.nodeType, f.nodeType;
            } catch (F) {
              c = null;
              break a;
            }
            var g = 0, h = -1, k = -1, l = 0, m = 0, q = a, r = null;
            b: for (; ; ) {
              for (var y; ; ) {
                q !== c || 0 !== e && 3 !== q.nodeType || (h = g + e);
                q !== f || 0 !== d && 3 !== q.nodeType || (k = g + d);
                3 === q.nodeType && (g += q.nodeValue.length);
                if (null === (y = q.firstChild)) break;
                r = q;
                q = y;
              }
              for (; ; ) {
                if (q === a) break b;
                r === c && ++l === e && (h = g);
                r === f && ++m === d && (k = g);
                if (null !== (y = q.nextSibling)) break;
                q = r;
                r = q.parentNode;
              }
              q = y;
            }
            c = -1 === h || -1 === k ? null : { start: h, end: k };
          } else c = null;
        }
        c = c || { start: 0, end: 0 };
      } else c = null;
      Df = { focusedElem: a, selectionRange: c };
      dd = false;
      for (V = b; null !== V; ) if (b = V, a = b.child, 0 !== (b.subtreeFlags & 1028) && null !== a) a.return = b, V = a;
      else for (; null !== V; ) {
        b = V;
        try {
          var n = b.alternate;
          if (0 !== (b.flags & 1024)) switch (b.tag) {
            case 0:
            case 11:
            case 15:
              break;
            case 1:
              if (null !== n) {
                var t = n.memoizedProps, J = n.memoizedState, x2 = b.stateNode, w = x2.getSnapshotBeforeUpdate(b.elementType === b.type ? t : Ci(b.type, t), J);
                x2.__reactInternalSnapshotBeforeUpdate = w;
              }
              break;
            case 3:
              var u = b.stateNode.containerInfo;
              1 === u.nodeType ? u.textContent = "" : 9 === u.nodeType && u.documentElement && u.removeChild(u.documentElement);
              break;
            case 5:
            case 6:
            case 4:
            case 17:
              break;
            default:
              throw Error(p(163));
          }
        } catch (F) {
          W(b, b.return, F);
        }
        a = b.sibling;
        if (null !== a) {
          a.return = b.return;
          V = a;
          break;
        }
        V = b.return;
      }
      n = Nj;
      Nj = false;
      return n;
    }
    function Pj(a, b, c) {
      var d = b.updateQueue;
      d = null !== d ? d.lastEffect : null;
      if (null !== d) {
        var e = d = d.next;
        do {
          if ((e.tag & a) === a) {
            var f = e.destroy;
            e.destroy = void 0;
            void 0 !== f && Mj(b, c, f);
          }
          e = e.next;
        } while (e !== d);
      }
    }
    function Qj(a, b) {
      b = b.updateQueue;
      b = null !== b ? b.lastEffect : null;
      if (null !== b) {
        var c = b = b.next;
        do {
          if ((c.tag & a) === a) {
            var d = c.create;
            c.destroy = d();
          }
          c = c.next;
        } while (c !== b);
      }
    }
    function Rj(a) {
      var b = a.ref;
      if (null !== b) {
        var c = a.stateNode;
        switch (a.tag) {
          case 5:
            a = c;
            break;
          default:
            a = c;
        }
        "function" === typeof b ? b(a) : b.current = a;
      }
    }
    function Sj(a) {
      var b = a.alternate;
      null !== b && (a.alternate = null, Sj(b));
      a.child = null;
      a.deletions = null;
      a.sibling = null;
      5 === a.tag && (b = a.stateNode, null !== b && (delete b[Of], delete b[Pf], delete b[of], delete b[Qf], delete b[Rf]));
      a.stateNode = null;
      a.return = null;
      a.dependencies = null;
      a.memoizedProps = null;
      a.memoizedState = null;
      a.pendingProps = null;
      a.stateNode = null;
      a.updateQueue = null;
    }
    function Tj(a) {
      return 5 === a.tag || 3 === a.tag || 4 === a.tag;
    }
    function Uj(a) {
      a: for (; ; ) {
        for (; null === a.sibling; ) {
          if (null === a.return || Tj(a.return)) return null;
          a = a.return;
        }
        a.sibling.return = a.return;
        for (a = a.sibling; 5 !== a.tag && 6 !== a.tag && 18 !== a.tag; ) {
          if (a.flags & 2) continue a;
          if (null === a.child || 4 === a.tag) continue a;
          else a.child.return = a, a = a.child;
        }
        if (!(a.flags & 2)) return a.stateNode;
      }
    }
    function Vj(a, b, c) {
      var d = a.tag;
      if (5 === d || 6 === d) a = a.stateNode, b ? 8 === c.nodeType ? c.parentNode.insertBefore(a, b) : c.insertBefore(a, b) : (8 === c.nodeType ? (b = c.parentNode, b.insertBefore(a, c)) : (b = c, b.appendChild(a)), c = c._reactRootContainer, null !== c && void 0 !== c || null !== b.onclick || (b.onclick = Bf));
      else if (4 !== d && (a = a.child, null !== a)) for (Vj(a, b, c), a = a.sibling; null !== a; ) Vj(a, b, c), a = a.sibling;
    }
    function Wj(a, b, c) {
      var d = a.tag;
      if (5 === d || 6 === d) a = a.stateNode, b ? c.insertBefore(a, b) : c.appendChild(a);
      else if (4 !== d && (a = a.child, null !== a)) for (Wj(a, b, c), a = a.sibling; null !== a; ) Wj(a, b, c), a = a.sibling;
    }
    var X = null, Xj = false;
    function Yj(a, b, c) {
      for (c = c.child; null !== c; ) Zj(a, b, c), c = c.sibling;
    }
    function Zj(a, b, c) {
      if (lc && "function" === typeof lc.onCommitFiberUnmount) try {
        lc.onCommitFiberUnmount(kc, c);
      } catch (h) {
      }
      switch (c.tag) {
        case 5:
          U || Lj(c, b);
        case 6:
          var d = X, e = Xj;
          X = null;
          Yj(a, b, c);
          X = d;
          Xj = e;
          null !== X && (Xj ? (a = X, c = c.stateNode, 8 === a.nodeType ? a.parentNode.removeChild(c) : a.removeChild(c)) : X.removeChild(c.stateNode));
          break;
        case 18:
          null !== X && (Xj ? (a = X, c = c.stateNode, 8 === a.nodeType ? Kf(a.parentNode, c) : 1 === a.nodeType && Kf(a, c), bd(a)) : Kf(X, c.stateNode));
          break;
        case 4:
          d = X;
          e = Xj;
          X = c.stateNode.containerInfo;
          Xj = true;
          Yj(a, b, c);
          X = d;
          Xj = e;
          break;
        case 0:
        case 11:
        case 14:
        case 15:
          if (!U && (d = c.updateQueue, null !== d && (d = d.lastEffect, null !== d))) {
            e = d = d.next;
            do {
              var f = e, g = f.destroy;
              f = f.tag;
              void 0 !== g && (0 !== (f & 2) ? Mj(c, b, g) : 0 !== (f & 4) && Mj(c, b, g));
              e = e.next;
            } while (e !== d);
          }
          Yj(a, b, c);
          break;
        case 1:
          if (!U && (Lj(c, b), d = c.stateNode, "function" === typeof d.componentWillUnmount)) try {
            d.props = c.memoizedProps, d.state = c.memoizedState, d.componentWillUnmount();
          } catch (h) {
            W(c, b, h);
          }
          Yj(a, b, c);
          break;
        case 21:
          Yj(a, b, c);
          break;
        case 22:
          c.mode & 1 ? (U = (d = U) || null !== c.memoizedState, Yj(a, b, c), U = d) : Yj(a, b, c);
          break;
        default:
          Yj(a, b, c);
      }
    }
    function ak(a) {
      var b = a.updateQueue;
      if (null !== b) {
        a.updateQueue = null;
        var c = a.stateNode;
        null === c && (c = a.stateNode = new Kj());
        b.forEach(function(b3) {
          var d = bk.bind(null, a, b3);
          c.has(b3) || (c.add(b3), b3.then(d, d));
        });
      }
    }
    function ck(a, b) {
      var c = b.deletions;
      if (null !== c) for (var d = 0; d < c.length; d++) {
        var e = c[d];
        try {
          var f = a, g = b, h = g;
          a: for (; null !== h; ) {
            switch (h.tag) {
              case 5:
                X = h.stateNode;
                Xj = false;
                break a;
              case 3:
                X = h.stateNode.containerInfo;
                Xj = true;
                break a;
              case 4:
                X = h.stateNode.containerInfo;
                Xj = true;
                break a;
            }
            h = h.return;
          }
          if (null === X) throw Error(p(160));
          Zj(f, g, e);
          X = null;
          Xj = false;
          var k = e.alternate;
          null !== k && (k.return = null);
          e.return = null;
        } catch (l) {
          W(e, b, l);
        }
      }
      if (b.subtreeFlags & 12854) for (b = b.child; null !== b; ) dk(b, a), b = b.sibling;
    }
    function dk(a, b) {
      var c = a.alternate, d = a.flags;
      switch (a.tag) {
        case 0:
        case 11:
        case 14:
        case 15:
          ck(b, a);
          ek(a);
          if (d & 4) {
            try {
              Pj(3, a, a.return), Qj(3, a);
            } catch (t) {
              W(a, a.return, t);
            }
            try {
              Pj(5, a, a.return);
            } catch (t) {
              W(a, a.return, t);
            }
          }
          break;
        case 1:
          ck(b, a);
          ek(a);
          d & 512 && null !== c && Lj(c, c.return);
          break;
        case 5:
          ck(b, a);
          ek(a);
          d & 512 && null !== c && Lj(c, c.return);
          if (a.flags & 32) {
            var e = a.stateNode;
            try {
              ob(e, "");
            } catch (t) {
              W(a, a.return, t);
            }
          }
          if (d & 4 && (e = a.stateNode, null != e)) {
            var f = a.memoizedProps, g = null !== c ? c.memoizedProps : f, h = a.type, k = a.updateQueue;
            a.updateQueue = null;
            if (null !== k) try {
              "input" === h && "radio" === f.type && null != f.name && ab(e, f);
              vb(h, g);
              var l = vb(h, f);
              for (g = 0; g < k.length; g += 2) {
                var m = k[g], q = k[g + 1];
                "style" === m ? sb(e, q) : "dangerouslySetInnerHTML" === m ? nb(e, q) : "children" === m ? ob(e, q) : ta(e, m, q, l);
              }
              switch (h) {
                case "input":
                  bb(e, f);
                  break;
                case "textarea":
                  ib(e, f);
                  break;
                case "select":
                  var r = e._wrapperState.wasMultiple;
                  e._wrapperState.wasMultiple = !!f.multiple;
                  var y = f.value;
                  null != y ? fb(e, !!f.multiple, y, false) : r !== !!f.multiple && (null != f.defaultValue ? fb(
                    e,
                    !!f.multiple,
                    f.defaultValue,
                    true
                  ) : fb(e, !!f.multiple, f.multiple ? [] : "", false));
              }
              e[Pf] = f;
            } catch (t) {
              W(a, a.return, t);
            }
          }
          break;
        case 6:
          ck(b, a);
          ek(a);
          if (d & 4) {
            if (null === a.stateNode) throw Error(p(162));
            e = a.stateNode;
            f = a.memoizedProps;
            try {
              e.nodeValue = f;
            } catch (t) {
              W(a, a.return, t);
            }
          }
          break;
        case 3:
          ck(b, a);
          ek(a);
          if (d & 4 && null !== c && c.memoizedState.isDehydrated) try {
            bd(b.containerInfo);
          } catch (t) {
            W(a, a.return, t);
          }
          break;
        case 4:
          ck(b, a);
          ek(a);
          break;
        case 13:
          ck(b, a);
          ek(a);
          e = a.child;
          e.flags & 8192 && (f = null !== e.memoizedState, e.stateNode.isHidden = f, !f || null !== e.alternate && null !== e.alternate.memoizedState || (fk = B()));
          d & 4 && ak(a);
          break;
        case 22:
          m = null !== c && null !== c.memoizedState;
          a.mode & 1 ? (U = (l = U) || m, ck(b, a), U = l) : ck(b, a);
          ek(a);
          if (d & 8192) {
            l = null !== a.memoizedState;
            if ((a.stateNode.isHidden = l) && !m && 0 !== (a.mode & 1)) for (V = a, m = a.child; null !== m; ) {
              for (q = V = m; null !== V; ) {
                r = V;
                y = r.child;
                switch (r.tag) {
                  case 0:
                  case 11:
                  case 14:
                  case 15:
                    Pj(4, r, r.return);
                    break;
                  case 1:
                    Lj(r, r.return);
                    var n = r.stateNode;
                    if ("function" === typeof n.componentWillUnmount) {
                      d = r;
                      c = r.return;
                      try {
                        b = d, n.props = b.memoizedProps, n.state = b.memoizedState, n.componentWillUnmount();
                      } catch (t) {
                        W(d, c, t);
                      }
                    }
                    break;
                  case 5:
                    Lj(r, r.return);
                    break;
                  case 22:
                    if (null !== r.memoizedState) {
                      gk(q);
                      continue;
                    }
                }
                null !== y ? (y.return = r, V = y) : gk(q);
              }
              m = m.sibling;
            }
            a: for (m = null, q = a; ; ) {
              if (5 === q.tag) {
                if (null === m) {
                  m = q;
                  try {
                    e = q.stateNode, l ? (f = e.style, "function" === typeof f.setProperty ? f.setProperty("display", "none", "important") : f.display = "none") : (h = q.stateNode, k = q.memoizedProps.style, g = void 0 !== k && null !== k && k.hasOwnProperty("display") ? k.display : null, h.style.display = rb("display", g));
                  } catch (t) {
                    W(a, a.return, t);
                  }
                }
              } else if (6 === q.tag) {
                if (null === m) try {
                  q.stateNode.nodeValue = l ? "" : q.memoizedProps;
                } catch (t) {
                  W(a, a.return, t);
                }
              } else if ((22 !== q.tag && 23 !== q.tag || null === q.memoizedState || q === a) && null !== q.child) {
                q.child.return = q;
                q = q.child;
                continue;
              }
              if (q === a) break a;
              for (; null === q.sibling; ) {
                if (null === q.return || q.return === a) break a;
                m === q && (m = null);
                q = q.return;
              }
              m === q && (m = null);
              q.sibling.return = q.return;
              q = q.sibling;
            }
          }
          break;
        case 19:
          ck(b, a);
          ek(a);
          d & 4 && ak(a);
          break;
        case 21:
          break;
        default:
          ck(
            b,
            a
          ), ek(a);
      }
    }
    function ek(a) {
      var b = a.flags;
      if (b & 2) {
        try {
          a: {
            for (var c = a.return; null !== c; ) {
              if (Tj(c)) {
                var d = c;
                break a;
              }
              c = c.return;
            }
            throw Error(p(160));
          }
          switch (d.tag) {
            case 5:
              var e = d.stateNode;
              d.flags & 32 && (ob(e, ""), d.flags &= -33);
              var f = Uj(a);
              Wj(a, f, e);
              break;
            case 3:
            case 4:
              var g = d.stateNode.containerInfo, h = Uj(a);
              Vj(a, h, g);
              break;
            default:
              throw Error(p(161));
          }
        } catch (k) {
          W(a, a.return, k);
        }
        a.flags &= -3;
      }
      b & 4096 && (a.flags &= -4097);
    }
    function hk(a, b, c) {
      V = a;
      ik(a);
    }
    function ik(a, b, c) {
      for (var d = 0 !== (a.mode & 1); null !== V; ) {
        var e = V, f = e.child;
        if (22 === e.tag && d) {
          var g = null !== e.memoizedState || Jj;
          if (!g) {
            var h = e.alternate, k = null !== h && null !== h.memoizedState || U;
            h = Jj;
            var l = U;
            Jj = g;
            if ((U = k) && !l) for (V = e; null !== V; ) g = V, k = g.child, 22 === g.tag && null !== g.memoizedState ? jk(e) : null !== k ? (k.return = g, V = k) : jk(e);
            for (; null !== f; ) V = f, ik(f), f = f.sibling;
            V = e;
            Jj = h;
            U = l;
          }
          kk(a);
        } else 0 !== (e.subtreeFlags & 8772) && null !== f ? (f.return = e, V = f) : kk(a);
      }
    }
    function kk(a) {
      for (; null !== V; ) {
        var b = V;
        if (0 !== (b.flags & 8772)) {
          var c = b.alternate;
          try {
            if (0 !== (b.flags & 8772)) switch (b.tag) {
              case 0:
              case 11:
              case 15:
                U || Qj(5, b);
                break;
              case 1:
                var d = b.stateNode;
                if (b.flags & 4 && !U) if (null === c) d.componentDidMount();
                else {
                  var e = b.elementType === b.type ? c.memoizedProps : Ci(b.type, c.memoizedProps);
                  d.componentDidUpdate(e, c.memoizedState, d.__reactInternalSnapshotBeforeUpdate);
                }
                var f = b.updateQueue;
                null !== f && sh(b, f, d);
                break;
              case 3:
                var g = b.updateQueue;
                if (null !== g) {
                  c = null;
                  if (null !== b.child) switch (b.child.tag) {
                    case 5:
                      c = b.child.stateNode;
                      break;
                    case 1:
                      c = b.child.stateNode;
                  }
                  sh(b, g, c);
                }
                break;
              case 5:
                var h = b.stateNode;
                if (null === c && b.flags & 4) {
                  c = h;
                  var k = b.memoizedProps;
                  switch (b.type) {
                    case "button":
                    case "input":
                    case "select":
                    case "textarea":
                      k.autoFocus && c.focus();
                      break;
                    case "img":
                      k.src && (c.src = k.src);
                  }
                }
                break;
              case 6:
                break;
              case 4:
                break;
              case 12:
                break;
              case 13:
                if (null === b.memoizedState) {
                  var l = b.alternate;
                  if (null !== l) {
                    var m = l.memoizedState;
                    if (null !== m) {
                      var q = m.dehydrated;
                      null !== q && bd(q);
                    }
                  }
                }
                break;
              case 19:
              case 17:
              case 21:
              case 22:
              case 23:
              case 25:
                break;
              default:
                throw Error(p(163));
            }
            U || b.flags & 512 && Rj(b);
          } catch (r) {
            W(b, b.return, r);
          }
        }
        if (b === a) {
          V = null;
          break;
        }
        c = b.sibling;
        if (null !== c) {
          c.return = b.return;
          V = c;
          break;
        }
        V = b.return;
      }
    }
    function gk(a) {
      for (; null !== V; ) {
        var b = V;
        if (b === a) {
          V = null;
          break;
        }
        var c = b.sibling;
        if (null !== c) {
          c.return = b.return;
          V = c;
          break;
        }
        V = b.return;
      }
    }
    function jk(a) {
      for (; null !== V; ) {
        var b = V;
        try {
          switch (b.tag) {
            case 0:
            case 11:
            case 15:
              var c = b.return;
              try {
                Qj(4, b);
              } catch (k) {
                W(b, c, k);
              }
              break;
            case 1:
              var d = b.stateNode;
              if ("function" === typeof d.componentDidMount) {
                var e = b.return;
                try {
                  d.componentDidMount();
                } catch (k) {
                  W(b, e, k);
                }
              }
              var f = b.return;
              try {
                Rj(b);
              } catch (k) {
                W(b, f, k);
              }
              break;
            case 5:
              var g = b.return;
              try {
                Rj(b);
              } catch (k) {
                W(b, g, k);
              }
          }
        } catch (k) {
          W(b, b.return, k);
        }
        if (b === a) {
          V = null;
          break;
        }
        var h = b.sibling;
        if (null !== h) {
          h.return = b.return;
          V = h;
          break;
        }
        V = b.return;
      }
    }
    var lk = Math.ceil, mk = ua.ReactCurrentDispatcher, nk = ua.ReactCurrentOwner, ok = ua.ReactCurrentBatchConfig, K = 0, Q = null, Y = null, Z = 0, fj = 0, ej = Uf(0), T = 0, pk = null, rh = 0, qk = 0, rk = 0, sk = null, tk = null, fk = 0, Gj = Infinity, uk = null, Oi = false, Pi = null, Ri = null, vk = false, wk = null, xk = 0, yk = 0, zk = null, Ak = -1, Bk = 0;
    function R() {
      return 0 !== (K & 6) ? B() : -1 !== Ak ? Ak : Ak = B();
    }
    function yi(a) {
      if (0 === (a.mode & 1)) return 1;
      if (0 !== (K & 2) && 0 !== Z) return Z & -Z;
      if (null !== Kg.transition) return 0 === Bk && (Bk = yc()), Bk;
      a = C;
      if (0 !== a) return a;
      a = window.event;
      a = void 0 === a ? 16 : jd(a.type);
      return a;
    }
    function gi(a, b, c, d) {
      if (50 < yk) throw yk = 0, zk = null, Error(p(185));
      Ac(a, c, d);
      if (0 === (K & 2) || a !== Q) a === Q && (0 === (K & 2) && (qk |= c), 4 === T && Ck(a, Z)), Dk(a, d), 1 === c && 0 === K && 0 === (b.mode & 1) && (Gj = B() + 500, fg && jg());
    }
    function Dk(a, b) {
      var c = a.callbackNode;
      wc(a, b);
      var d = uc(a, a === Q ? Z : 0);
      if (0 === d) null !== c && bc(c), a.callbackNode = null, a.callbackPriority = 0;
      else if (b = d & -d, a.callbackPriority !== b) {
        null != c && bc(c);
        if (1 === b) 0 === a.tag ? ig(Ek.bind(null, a)) : hg(Ek.bind(null, a)), Jf(function() {
          0 === (K & 6) && jg();
        }), c = null;
        else {
          switch (Dc(d)) {
            case 1:
              c = fc;
              break;
            case 4:
              c = gc;
              break;
            case 16:
              c = hc;
              break;
            case 536870912:
              c = jc;
              break;
            default:
              c = hc;
          }
          c = Fk(c, Gk.bind(null, a));
        }
        a.callbackPriority = b;
        a.callbackNode = c;
      }
    }
    function Gk(a, b) {
      Ak = -1;
      Bk = 0;
      if (0 !== (K & 6)) throw Error(p(327));
      var c = a.callbackNode;
      if (Hk() && a.callbackNode !== c) return null;
      var d = uc(a, a === Q ? Z : 0);
      if (0 === d) return null;
      if (0 !== (d & 30) || 0 !== (d & a.expiredLanes) || b) b = Ik(a, d);
      else {
        b = d;
        var e = K;
        K |= 2;
        var f = Jk();
        if (Q !== a || Z !== b) uk = null, Gj = B() + 500, Kk(a, b);
        do
          try {
            Lk();
            break;
          } catch (h) {
            Mk(a, h);
          }
        while (1);
        $g();
        mk.current = f;
        K = e;
        null !== Y ? b = 0 : (Q = null, Z = 0, b = T);
      }
      if (0 !== b) {
        2 === b && (e = xc(a), 0 !== e && (d = e, b = Nk(a, e)));
        if (1 === b) throw c = pk, Kk(a, 0), Ck(a, d), Dk(a, B()), c;
        if (6 === b) Ck(a, d);
        else {
          e = a.current.alternate;
          if (0 === (d & 30) && !Ok(e) && (b = Ik(a, d), 2 === b && (f = xc(a), 0 !== f && (d = f, b = Nk(a, f))), 1 === b)) throw c = pk, Kk(a, 0), Ck(a, d), Dk(a, B()), c;
          a.finishedWork = e;
          a.finishedLanes = d;
          switch (b) {
            case 0:
            case 1:
              throw Error(p(345));
            case 2:
              Pk(a, tk, uk);
              break;
            case 3:
              Ck(a, d);
              if ((d & 130023424) === d && (b = fk + 500 - B(), 10 < b)) {
                if (0 !== uc(a, 0)) break;
                e = a.suspendedLanes;
                if ((e & d) !== d) {
                  R();
                  a.pingedLanes |= a.suspendedLanes & e;
                  break;
                }
                a.timeoutHandle = Ff(Pk.bind(null, a, tk, uk), b);
                break;
              }
              Pk(a, tk, uk);
              break;
            case 4:
              Ck(a, d);
              if ((d & 4194240) === d) break;
              b = a.eventTimes;
              for (e = -1; 0 < d; ) {
                var g = 31 - oc(d);
                f = 1 << g;
                g = b[g];
                g > e && (e = g);
                d &= ~f;
              }
              d = e;
              d = B() - d;
              d = (120 > d ? 120 : 480 > d ? 480 : 1080 > d ? 1080 : 1920 > d ? 1920 : 3e3 > d ? 3e3 : 4320 > d ? 4320 : 1960 * lk(d / 1960)) - d;
              if (10 < d) {
                a.timeoutHandle = Ff(Pk.bind(null, a, tk, uk), d);
                break;
              }
              Pk(a, tk, uk);
              break;
            case 5:
              Pk(a, tk, uk);
              break;
            default:
              throw Error(p(329));
          }
        }
      }
      Dk(a, B());
      return a.callbackNode === c ? Gk.bind(null, a) : null;
    }
    function Nk(a, b) {
      var c = sk;
      a.current.memoizedState.isDehydrated && (Kk(a, b).flags |= 256);
      a = Ik(a, b);
      2 !== a && (b = tk, tk = c, null !== b && Fj(b));
      return a;
    }
    function Fj(a) {
      null === tk ? tk = a : tk.push.apply(tk, a);
    }
    function Ok(a) {
      for (var b = a; ; ) {
        if (b.flags & 16384) {
          var c = b.updateQueue;
          if (null !== c && (c = c.stores, null !== c)) for (var d = 0; d < c.length; d++) {
            var e = c[d], f = e.getSnapshot;
            e = e.value;
            try {
              if (!He(f(), e)) return false;
            } catch (g) {
              return false;
            }
          }
        }
        c = b.child;
        if (b.subtreeFlags & 16384 && null !== c) c.return = b, b = c;
        else {
          if (b === a) break;
          for (; null === b.sibling; ) {
            if (null === b.return || b.return === a) return true;
            b = b.return;
          }
          b.sibling.return = b.return;
          b = b.sibling;
        }
      }
      return true;
    }
    function Ck(a, b) {
      b &= ~rk;
      b &= ~qk;
      a.suspendedLanes |= b;
      a.pingedLanes &= ~b;
      for (a = a.expirationTimes; 0 < b; ) {
        var c = 31 - oc(b), d = 1 << c;
        a[c] = -1;
        b &= ~d;
      }
    }
    function Ek(a) {
      if (0 !== (K & 6)) throw Error(p(327));
      Hk();
      var b = uc(a, 0);
      if (0 === (b & 1)) return Dk(a, B()), null;
      var c = Ik(a, b);
      if (0 !== a.tag && 2 === c) {
        var d = xc(a);
        0 !== d && (b = d, c = Nk(a, d));
      }
      if (1 === c) throw c = pk, Kk(a, 0), Ck(a, b), Dk(a, B()), c;
      if (6 === c) throw Error(p(345));
      a.finishedWork = a.current.alternate;
      a.finishedLanes = b;
      Pk(a, tk, uk);
      Dk(a, B());
      return null;
    }
    function Qk(a, b) {
      var c = K;
      K |= 1;
      try {
        return a(b);
      } finally {
        K = c, 0 === K && (Gj = B() + 500, fg && jg());
      }
    }
    function Rk(a) {
      null !== wk && 0 === wk.tag && 0 === (K & 6) && Hk();
      var b = K;
      K |= 1;
      var c = ok.transition, d = C;
      try {
        if (ok.transition = null, C = 1, a) return a();
      } finally {
        C = d, ok.transition = c, K = b, 0 === (K & 6) && jg();
      }
    }
    function Hj() {
      fj = ej.current;
      E(ej);
    }
    function Kk(a, b) {
      a.finishedWork = null;
      a.finishedLanes = 0;
      var c = a.timeoutHandle;
      -1 !== c && (a.timeoutHandle = -1, Gf(c));
      if (null !== Y) for (c = Y.return; null !== c; ) {
        var d = c;
        wg(d);
        switch (d.tag) {
          case 1:
            d = d.type.childContextTypes;
            null !== d && void 0 !== d && $f();
            break;
          case 3:
            zh2();
            E(Wf);
            E(H);
            Eh();
            break;
          case 5:
            Bh(d);
            break;
          case 4:
            zh2();
            break;
          case 13:
            E(L);
            break;
          case 19:
            E(L);
            break;
          case 10:
            ah(d.type._context);
            break;
          case 22:
          case 23:
            Hj();
        }
        c = c.return;
      }
      Q = a;
      Y = a = Pg(a.current, null);
      Z = fj = b;
      T = 0;
      pk = null;
      rk = qk = rh = 0;
      tk = sk = null;
      if (null !== fh) {
        for (b = 0; b < fh.length; b++) if (c = fh[b], d = c.interleaved, null !== d) {
          c.interleaved = null;
          var e = d.next, f = c.pending;
          if (null !== f) {
            var g = f.next;
            f.next = e;
            d.next = g;
          }
          c.pending = d;
        }
        fh = null;
      }
      return a;
    }
    function Mk(a, b) {
      do {
        var c = Y;
        try {
          $g();
          Fh.current = Rh;
          if (Ih) {
            for (var d = M.memoizedState; null !== d; ) {
              var e = d.queue;
              null !== e && (e.pending = null);
              d = d.next;
            }
            Ih = false;
          }
          Hh = 0;
          O = N = M = null;
          Jh = false;
          Kh = 0;
          nk.current = null;
          if (null === c || null === c.return) {
            T = 1;
            pk = b;
            Y = null;
            break;
          }
          a: {
            var f = a, g = c.return, h = c, k = b;
            b = Z;
            h.flags |= 32768;
            if (null !== k && "object" === typeof k && "function" === typeof k.then) {
              var l = k, m = h, q = m.tag;
              if (0 === (m.mode & 1) && (0 === q || 11 === q || 15 === q)) {
                var r = m.alternate;
                r ? (m.updateQueue = r.updateQueue, m.memoizedState = r.memoizedState, m.lanes = r.lanes) : (m.updateQueue = null, m.memoizedState = null);
              }
              var y = Ui(g);
              if (null !== y) {
                y.flags &= -257;
                Vi(y, g, h, f, b);
                y.mode & 1 && Si(f, l, b);
                b = y;
                k = l;
                var n = b.updateQueue;
                if (null === n) {
                  var t = /* @__PURE__ */ new Set();
                  t.add(k);
                  b.updateQueue = t;
                } else n.add(k);
                break a;
              } else {
                if (0 === (b & 1)) {
                  Si(f, l, b);
                  tj();
                  break a;
                }
                k = Error(p(426));
              }
            } else if (I && h.mode & 1) {
              var J = Ui(g);
              if (null !== J) {
                0 === (J.flags & 65536) && (J.flags |= 256);
                Vi(J, g, h, f, b);
                Jg(Ji(k, h));
                break a;
              }
            }
            f = k = Ji(k, h);
            4 !== T && (T = 2);
            null === sk ? sk = [f] : sk.push(f);
            f = g;
            do {
              switch (f.tag) {
                case 3:
                  f.flags |= 65536;
                  b &= -b;
                  f.lanes |= b;
                  var x2 = Ni(f, k, b);
                  ph(f, x2);
                  break a;
                case 1:
                  h = k;
                  var w = f.type, u = f.stateNode;
                  if (0 === (f.flags & 128) && ("function" === typeof w.getDerivedStateFromError || null !== u && "function" === typeof u.componentDidCatch && (null === Ri || !Ri.has(u)))) {
                    f.flags |= 65536;
                    b &= -b;
                    f.lanes |= b;
                    var F = Qi(f, h, b);
                    ph(f, F);
                    break a;
                  }
              }
              f = f.return;
            } while (null !== f);
          }
          Sk(c);
        } catch (na) {
          b = na;
          Y === c && null !== c && (Y = c = c.return);
          continue;
        }
        break;
      } while (1);
    }
    function Jk() {
      var a = mk.current;
      mk.current = Rh;
      return null === a ? Rh : a;
    }
    function tj() {
      if (0 === T || 3 === T || 2 === T) T = 4;
      null === Q || 0 === (rh & 268435455) && 0 === (qk & 268435455) || Ck(Q, Z);
    }
    function Ik(a, b) {
      var c = K;
      K |= 2;
      var d = Jk();
      if (Q !== a || Z !== b) uk = null, Kk(a, b);
      do
        try {
          Tk();
          break;
        } catch (e) {
          Mk(a, e);
        }
      while (1);
      $g();
      K = c;
      mk.current = d;
      if (null !== Y) throw Error(p(261));
      Q = null;
      Z = 0;
      return T;
    }
    function Tk() {
      for (; null !== Y; ) Uk(Y);
    }
    function Lk() {
      for (; null !== Y && !cc(); ) Uk(Y);
    }
    function Uk(a) {
      var b = Vk(a.alternate, a, fj);
      a.memoizedProps = a.pendingProps;
      null === b ? Sk(a) : Y = b;
      nk.current = null;
    }
    function Sk(a) {
      var b = a;
      do {
        var c = b.alternate;
        a = b.return;
        if (0 === (b.flags & 32768)) {
          if (c = Ej(c, b, fj), null !== c) {
            Y = c;
            return;
          }
        } else {
          c = Ij(c, b);
          if (null !== c) {
            c.flags &= 32767;
            Y = c;
            return;
          }
          if (null !== a) a.flags |= 32768, a.subtreeFlags = 0, a.deletions = null;
          else {
            T = 6;
            Y = null;
            return;
          }
        }
        b = b.sibling;
        if (null !== b) {
          Y = b;
          return;
        }
        Y = b = a;
      } while (null !== b);
      0 === T && (T = 5);
    }
    function Pk(a, b, c) {
      var d = C, e = ok.transition;
      try {
        ok.transition = null, C = 1, Wk(a, b, c, d);
      } finally {
        ok.transition = e, C = d;
      }
      return null;
    }
    function Wk(a, b, c, d) {
      do
        Hk();
      while (null !== wk);
      if (0 !== (K & 6)) throw Error(p(327));
      c = a.finishedWork;
      var e = a.finishedLanes;
      if (null === c) return null;
      a.finishedWork = null;
      a.finishedLanes = 0;
      if (c === a.current) throw Error(p(177));
      a.callbackNode = null;
      a.callbackPriority = 0;
      var f = c.lanes | c.childLanes;
      Bc(a, f);
      a === Q && (Y = Q = null, Z = 0);
      0 === (c.subtreeFlags & 2064) && 0 === (c.flags & 2064) || vk || (vk = true, Fk(hc, function() {
        Hk();
        return null;
      }));
      f = 0 !== (c.flags & 15990);
      if (0 !== (c.subtreeFlags & 15990) || f) {
        f = ok.transition;
        ok.transition = null;
        var g = C;
        C = 1;
        var h = K;
        K |= 4;
        nk.current = null;
        Oj(a, c);
        dk(c, a);
        Oe(Df);
        dd = !!Cf;
        Df = Cf = null;
        a.current = c;
        hk(c);
        dc();
        K = h;
        C = g;
        ok.transition = f;
      } else a.current = c;
      vk && (vk = false, wk = a, xk = e);
      f = a.pendingLanes;
      0 === f && (Ri = null);
      mc(c.stateNode);
      Dk(a, B());
      if (null !== b) for (d = a.onRecoverableError, c = 0; c < b.length; c++) e = b[c], d(e.value, { componentStack: e.stack, digest: e.digest });
      if (Oi) throw Oi = false, a = Pi, Pi = null, a;
      0 !== (xk & 1) && 0 !== a.tag && Hk();
      f = a.pendingLanes;
      0 !== (f & 1) ? a === zk ? yk++ : (yk = 0, zk = a) : yk = 0;
      jg();
      return null;
    }
    function Hk() {
      if (null !== wk) {
        var a = Dc(xk), b = ok.transition, c = C;
        try {
          ok.transition = null;
          C = 16 > a ? 16 : a;
          if (null === wk) var d = false;
          else {
            a = wk;
            wk = null;
            xk = 0;
            if (0 !== (K & 6)) throw Error(p(331));
            var e = K;
            K |= 4;
            for (V = a.current; null !== V; ) {
              var f = V, g = f.child;
              if (0 !== (V.flags & 16)) {
                var h = f.deletions;
                if (null !== h) {
                  for (var k = 0; k < h.length; k++) {
                    var l = h[k];
                    for (V = l; null !== V; ) {
                      var m = V;
                      switch (m.tag) {
                        case 0:
                        case 11:
                        case 15:
                          Pj(8, m, f);
                      }
                      var q = m.child;
                      if (null !== q) q.return = m, V = q;
                      else for (; null !== V; ) {
                        m = V;
                        var r = m.sibling, y = m.return;
                        Sj(m);
                        if (m === l) {
                          V = null;
                          break;
                        }
                        if (null !== r) {
                          r.return = y;
                          V = r;
                          break;
                        }
                        V = y;
                      }
                    }
                  }
                  var n = f.alternate;
                  if (null !== n) {
                    var t = n.child;
                    if (null !== t) {
                      n.child = null;
                      do {
                        var J = t.sibling;
                        t.sibling = null;
                        t = J;
                      } while (null !== t);
                    }
                  }
                  V = f;
                }
              }
              if (0 !== (f.subtreeFlags & 2064) && null !== g) g.return = f, V = g;
              else b: for (; null !== V; ) {
                f = V;
                if (0 !== (f.flags & 2048)) switch (f.tag) {
                  case 0:
                  case 11:
                  case 15:
                    Pj(9, f, f.return);
                }
                var x2 = f.sibling;
                if (null !== x2) {
                  x2.return = f.return;
                  V = x2;
                  break b;
                }
                V = f.return;
              }
            }
            var w = a.current;
            for (V = w; null !== V; ) {
              g = V;
              var u = g.child;
              if (0 !== (g.subtreeFlags & 2064) && null !== u) u.return = g, V = u;
              else b: for (g = w; null !== V; ) {
                h = V;
                if (0 !== (h.flags & 2048)) try {
                  switch (h.tag) {
                    case 0:
                    case 11:
                    case 15:
                      Qj(9, h);
                  }
                } catch (na) {
                  W(h, h.return, na);
                }
                if (h === g) {
                  V = null;
                  break b;
                }
                var F = h.sibling;
                if (null !== F) {
                  F.return = h.return;
                  V = F;
                  break b;
                }
                V = h.return;
              }
            }
            K = e;
            jg();
            if (lc && "function" === typeof lc.onPostCommitFiberRoot) try {
              lc.onPostCommitFiberRoot(kc, a);
            } catch (na) {
            }
            d = true;
          }
          return d;
        } finally {
          C = c, ok.transition = b;
        }
      }
      return false;
    }
    function Xk(a, b, c) {
      b = Ji(c, b);
      b = Ni(a, b, 1);
      a = nh(a, b, 1);
      b = R();
      null !== a && (Ac(a, 1, b), Dk(a, b));
    }
    function W(a, b, c) {
      if (3 === a.tag) Xk(a, a, c);
      else for (; null !== b; ) {
        if (3 === b.tag) {
          Xk(b, a, c);
          break;
        } else if (1 === b.tag) {
          var d = b.stateNode;
          if ("function" === typeof b.type.getDerivedStateFromError || "function" === typeof d.componentDidCatch && (null === Ri || !Ri.has(d))) {
            a = Ji(c, a);
            a = Qi(b, a, 1);
            b = nh(b, a, 1);
            a = R();
            null !== b && (Ac(b, 1, a), Dk(b, a));
            break;
          }
        }
        b = b.return;
      }
    }
    function Ti(a, b, c) {
      var d = a.pingCache;
      null !== d && d.delete(b);
      b = R();
      a.pingedLanes |= a.suspendedLanes & c;
      Q === a && (Z & c) === c && (4 === T || 3 === T && (Z & 130023424) === Z && 500 > B() - fk ? Kk(a, 0) : rk |= c);
      Dk(a, b);
    }
    function Yk(a, b) {
      0 === b && (0 === (a.mode & 1) ? b = 1 : (b = sc, sc <<= 1, 0 === (sc & 130023424) && (sc = 4194304)));
      var c = R();
      a = ih(a, b);
      null !== a && (Ac(a, b, c), Dk(a, c));
    }
    function uj(a) {
      var b = a.memoizedState, c = 0;
      null !== b && (c = b.retryLane);
      Yk(a, c);
    }
    function bk(a, b) {
      var c = 0;
      switch (a.tag) {
        case 13:
          var d = a.stateNode;
          var e = a.memoizedState;
          null !== e && (c = e.retryLane);
          break;
        case 19:
          d = a.stateNode;
          break;
        default:
          throw Error(p(314));
      }
      null !== d && d.delete(b);
      Yk(a, c);
    }
    var Vk;
    Vk = function(a, b, c) {
      if (null !== a) if (a.memoizedProps !== b.pendingProps || Wf.current) dh = true;
      else {
        if (0 === (a.lanes & c) && 0 === (b.flags & 128)) return dh = false, yj(a, b, c);
        dh = 0 !== (a.flags & 131072) ? true : false;
      }
      else dh = false, I && 0 !== (b.flags & 1048576) && ug(b, ng, b.index);
      b.lanes = 0;
      switch (b.tag) {
        case 2:
          var d = b.type;
          ij(a, b);
          a = b.pendingProps;
          var e = Yf(b, H.current);
          ch(b, c);
          e = Nh(null, b, d, a, e, c);
          var f = Sh();
          b.flags |= 1;
          "object" === typeof e && null !== e && "function" === typeof e.render && void 0 === e.$$typeof ? (b.tag = 1, b.memoizedState = null, b.updateQueue = null, Zf(d) ? (f = true, cg(b)) : f = false, b.memoizedState = null !== e.state && void 0 !== e.state ? e.state : null, kh(b), e.updater = Ei, b.stateNode = e, e._reactInternals = b, Ii(b, d, a, c), b = jj(null, b, d, true, f, c)) : (b.tag = 0, I && f && vg(b), Xi(null, b, e, c), b = b.child);
          return b;
        case 16:
          d = b.elementType;
          a: {
            ij(a, b);
            a = b.pendingProps;
            e = d._init;
            d = e(d._payload);
            b.type = d;
            e = b.tag = Zk(d);
            a = Ci(d, a);
            switch (e) {
              case 0:
                b = cj(null, b, d, a, c);
                break a;
              case 1:
                b = hj(null, b, d, a, c);
                break a;
              case 11:
                b = Yi(null, b, d, a, c);
                break a;
              case 14:
                b = $i(null, b, d, Ci(d.type, a), c);
                break a;
            }
            throw Error(p(
              306,
              d,
              ""
            ));
          }
          return b;
        case 0:
          return d = b.type, e = b.pendingProps, e = b.elementType === d ? e : Ci(d, e), cj(a, b, d, e, c);
        case 1:
          return d = b.type, e = b.pendingProps, e = b.elementType === d ? e : Ci(d, e), hj(a, b, d, e, c);
        case 3:
          a: {
            kj(b);
            if (null === a) throw Error(p(387));
            d = b.pendingProps;
            f = b.memoizedState;
            e = f.element;
            lh(a, b);
            qh(b, d, null, c);
            var g = b.memoizedState;
            d = g.element;
            if (f.isDehydrated) if (f = { element: d, isDehydrated: false, cache: g.cache, pendingSuspenseBoundaries: g.pendingSuspenseBoundaries, transitions: g.transitions }, b.updateQueue.baseState = f, b.memoizedState = f, b.flags & 256) {
              e = Ji(Error(p(423)), b);
              b = lj(a, b, d, c, e);
              break a;
            } else if (d !== e) {
              e = Ji(Error(p(424)), b);
              b = lj(a, b, d, c, e);
              break a;
            } else for (yg = Lf(b.stateNode.containerInfo.firstChild), xg = b, I = true, zg = null, c = Vg(b, null, d, c), b.child = c; c; ) c.flags = c.flags & -3 | 4096, c = c.sibling;
            else {
              Ig();
              if (d === e) {
                b = Zi(a, b, c);
                break a;
              }
              Xi(a, b, d, c);
            }
            b = b.child;
          }
          return b;
        case 5:
          return Ah(b), null === a && Eg(b), d = b.type, e = b.pendingProps, f = null !== a ? a.memoizedProps : null, g = e.children, Ef(d, e) ? g = null : null !== f && Ef(d, f) && (b.flags |= 32), gj(a, b), Xi(a, b, g, c), b.child;
        case 6:
          return null === a && Eg(b), null;
        case 13:
          return oj(a, b, c);
        case 4:
          return yh(b, b.stateNode.containerInfo), d = b.pendingProps, null === a ? b.child = Ug(b, null, d, c) : Xi(a, b, d, c), b.child;
        case 11:
          return d = b.type, e = b.pendingProps, e = b.elementType === d ? e : Ci(d, e), Yi(a, b, d, e, c);
        case 7:
          return Xi(a, b, b.pendingProps, c), b.child;
        case 8:
          return Xi(a, b, b.pendingProps.children, c), b.child;
        case 12:
          return Xi(a, b, b.pendingProps.children, c), b.child;
        case 10:
          a: {
            d = b.type._context;
            e = b.pendingProps;
            f = b.memoizedProps;
            g = e.value;
            G(Wg, d._currentValue);
            d._currentValue = g;
            if (null !== f) if (He(f.value, g)) {
              if (f.children === e.children && !Wf.current) {
                b = Zi(a, b, c);
                break a;
              }
            } else for (f = b.child, null !== f && (f.return = b); null !== f; ) {
              var h = f.dependencies;
              if (null !== h) {
                g = f.child;
                for (var k = h.firstContext; null !== k; ) {
                  if (k.context === d) {
                    if (1 === f.tag) {
                      k = mh(-1, c & -c);
                      k.tag = 2;
                      var l = f.updateQueue;
                      if (null !== l) {
                        l = l.shared;
                        var m = l.pending;
                        null === m ? k.next = k : (k.next = m.next, m.next = k);
                        l.pending = k;
                      }
                    }
                    f.lanes |= c;
                    k = f.alternate;
                    null !== k && (k.lanes |= c);
                    bh(
                      f.return,
                      c,
                      b
                    );
                    h.lanes |= c;
                    break;
                  }
                  k = k.next;
                }
              } else if (10 === f.tag) g = f.type === b.type ? null : f.child;
              else if (18 === f.tag) {
                g = f.return;
                if (null === g) throw Error(p(341));
                g.lanes |= c;
                h = g.alternate;
                null !== h && (h.lanes |= c);
                bh(g, c, b);
                g = f.sibling;
              } else g = f.child;
              if (null !== g) g.return = f;
              else for (g = f; null !== g; ) {
                if (g === b) {
                  g = null;
                  break;
                }
                f = g.sibling;
                if (null !== f) {
                  f.return = g.return;
                  g = f;
                  break;
                }
                g = g.return;
              }
              f = g;
            }
            Xi(a, b, e.children, c);
            b = b.child;
          }
          return b;
        case 9:
          return e = b.type, d = b.pendingProps.children, ch(b, c), e = eh(e), d = d(e), b.flags |= 1, Xi(a, b, d, c), b.child;
        case 14:
          return d = b.type, e = Ci(d, b.pendingProps), e = Ci(d.type, e), $i(a, b, d, e, c);
        case 15:
          return bj(a, b, b.type, b.pendingProps, c);
        case 17:
          return d = b.type, e = b.pendingProps, e = b.elementType === d ? e : Ci(d, e), ij(a, b), b.tag = 1, Zf(d) ? (a = true, cg(b)) : a = false, ch(b, c), Gi(b, d, e), Ii(b, d, e, c), jj(null, b, d, true, a, c);
        case 19:
          return xj(a, b, c);
        case 22:
          return dj(a, b, c);
      }
      throw Error(p(156, b.tag));
    };
    function Fk(a, b) {
      return ac(a, b);
    }
    function $k(a, b, c, d) {
      this.tag = a;
      this.key = c;
      this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null;
      this.index = 0;
      this.ref = null;
      this.pendingProps = b;
      this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null;
      this.mode = d;
      this.subtreeFlags = this.flags = 0;
      this.deletions = null;
      this.childLanes = this.lanes = 0;
      this.alternate = null;
    }
    function Bg(a, b, c, d) {
      return new $k(a, b, c, d);
    }
    function aj(a) {
      a = a.prototype;
      return !(!a || !a.isReactComponent);
    }
    function Zk(a) {
      if ("function" === typeof a) return aj(a) ? 1 : 0;
      if (void 0 !== a && null !== a) {
        a = a.$$typeof;
        if (a === Da) return 11;
        if (a === Ga) return 14;
      }
      return 2;
    }
    function Pg(a, b) {
      var c = a.alternate;
      null === c ? (c = Bg(a.tag, b, a.key, a.mode), c.elementType = a.elementType, c.type = a.type, c.stateNode = a.stateNode, c.alternate = a, a.alternate = c) : (c.pendingProps = b, c.type = a.type, c.flags = 0, c.subtreeFlags = 0, c.deletions = null);
      c.flags = a.flags & 14680064;
      c.childLanes = a.childLanes;
      c.lanes = a.lanes;
      c.child = a.child;
      c.memoizedProps = a.memoizedProps;
      c.memoizedState = a.memoizedState;
      c.updateQueue = a.updateQueue;
      b = a.dependencies;
      c.dependencies = null === b ? null : { lanes: b.lanes, firstContext: b.firstContext };
      c.sibling = a.sibling;
      c.index = a.index;
      c.ref = a.ref;
      return c;
    }
    function Rg(a, b, c, d, e, f) {
      var g = 2;
      d = a;
      if ("function" === typeof a) aj(a) && (g = 1);
      else if ("string" === typeof a) g = 5;
      else a: switch (a) {
        case ya:
          return Tg(c.children, e, f, b);
        case za:
          g = 8;
          e |= 8;
          break;
        case Aa:
          return a = Bg(12, c, b, e | 2), a.elementType = Aa, a.lanes = f, a;
        case Ea:
          return a = Bg(13, c, b, e), a.elementType = Ea, a.lanes = f, a;
        case Fa:
          return a = Bg(19, c, b, e), a.elementType = Fa, a.lanes = f, a;
        case Ia:
          return pj(c, e, f, b);
        default:
          if ("object" === typeof a && null !== a) switch (a.$$typeof) {
            case Ba:
              g = 10;
              break a;
            case Ca:
              g = 9;
              break a;
            case Da:
              g = 11;
              break a;
            case Ga:
              g = 14;
              break a;
            case Ha:
              g = 16;
              d = null;
              break a;
          }
          throw Error(p(130, null == a ? a : typeof a, ""));
      }
      b = Bg(g, c, b, e);
      b.elementType = a;
      b.type = d;
      b.lanes = f;
      return b;
    }
    function Tg(a, b, c, d) {
      a = Bg(7, a, d, b);
      a.lanes = c;
      return a;
    }
    function pj(a, b, c, d) {
      a = Bg(22, a, d, b);
      a.elementType = Ia;
      a.lanes = c;
      a.stateNode = { isHidden: false };
      return a;
    }
    function Qg(a, b, c) {
      a = Bg(6, a, null, b);
      a.lanes = c;
      return a;
    }
    function Sg(a, b, c) {
      b = Bg(4, null !== a.children ? a.children : [], a.key, b);
      b.lanes = c;
      b.stateNode = { containerInfo: a.containerInfo, pendingChildren: null, implementation: a.implementation };
      return b;
    }
    function al(a, b, c, d, e) {
      this.tag = b;
      this.containerInfo = a;
      this.finishedWork = this.pingCache = this.current = this.pendingChildren = null;
      this.timeoutHandle = -1;
      this.callbackNode = this.pendingContext = this.context = null;
      this.callbackPriority = 0;
      this.eventTimes = zc(0);
      this.expirationTimes = zc(-1);
      this.entangledLanes = this.finishedLanes = this.mutableReadLanes = this.expiredLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0;
      this.entanglements = zc(0);
      this.identifierPrefix = d;
      this.onRecoverableError = e;
      this.mutableSourceEagerHydrationData = null;
    }
    function bl(a, b, c, d, e, f, g, h, k) {
      a = new al(a, b, c, h, k);
      1 === b ? (b = 1, true === f && (b |= 8)) : b = 0;
      f = Bg(3, null, null, b);
      a.current = f;
      f.stateNode = a;
      f.memoizedState = { element: d, isDehydrated: c, cache: null, transitions: null, pendingSuspenseBoundaries: null };
      kh(f);
      return a;
    }
    function cl(a, b, c) {
      var d = 3 < arguments.length && void 0 !== arguments[3] ? arguments[3] : null;
      return { $$typeof: wa, key: null == d ? null : "" + d, children: a, containerInfo: b, implementation: c };
    }
    function dl(a) {
      if (!a) return Vf;
      a = a._reactInternals;
      a: {
        if (Vb(a) !== a || 1 !== a.tag) throw Error(p(170));
        var b = a;
        do {
          switch (b.tag) {
            case 3:
              b = b.stateNode.context;
              break a;
            case 1:
              if (Zf(b.type)) {
                b = b.stateNode.__reactInternalMemoizedMergedChildContext;
                break a;
              }
          }
          b = b.return;
        } while (null !== b);
        throw Error(p(171));
      }
      if (1 === a.tag) {
        var c = a.type;
        if (Zf(c)) return bg(a, c, b);
      }
      return b;
    }
    function el(a, b, c, d, e, f, g, h, k) {
      a = bl(c, d, true, a, e, f, g, h, k);
      a.context = dl(null);
      c = a.current;
      d = R();
      e = yi(c);
      f = mh(d, e);
      f.callback = void 0 !== b && null !== b ? b : null;
      nh(c, f, e);
      a.current.lanes = e;
      Ac(a, e, d);
      Dk(a, d);
      return a;
    }
    function fl2(a, b, c, d) {
      var e = b.current, f = R(), g = yi(e);
      c = dl(c);
      null === b.context ? b.context = c : b.pendingContext = c;
      b = mh(f, g);
      b.payload = { element: a };
      d = void 0 === d ? null : d;
      null !== d && (b.callback = d);
      a = nh(e, b, g);
      null !== a && (gi(a, e, g, f), oh(a, e, g));
      return g;
    }
    function gl(a) {
      a = a.current;
      if (!a.child) return null;
      switch (a.child.tag) {
        case 5:
          return a.child.stateNode;
        default:
          return a.child.stateNode;
      }
    }
    function hl(a, b) {
      a = a.memoizedState;
      if (null !== a && null !== a.dehydrated) {
        var c = a.retryLane;
        a.retryLane = 0 !== c && c < b ? c : b;
      }
    }
    function il(a, b) {
      hl(a, b);
      (a = a.alternate) && hl(a, b);
    }
    function jl() {
      return null;
    }
    var kl = "function" === typeof reportError ? reportError : function(a) {
      console.error(a);
    };
    function ll(a) {
      this._internalRoot = a;
    }
    ml.prototype.render = ll.prototype.render = function(a) {
      var b = this._internalRoot;
      if (null === b) throw Error(p(409));
      fl2(a, b, null, null);
    };
    ml.prototype.unmount = ll.prototype.unmount = function() {
      var a = this._internalRoot;
      if (null !== a) {
        this._internalRoot = null;
        var b = a.containerInfo;
        Rk(function() {
          fl2(null, a, null, null);
        });
        b[uf] = null;
      }
    };
    function ml(a) {
      this._internalRoot = a;
    }
    ml.prototype.unstable_scheduleHydration = function(a) {
      if (a) {
        var b = Hc();
        a = { blockedOn: null, target: a, priority: b };
        for (var c = 0; c < Qc.length && 0 !== b && b < Qc[c].priority; c++) ;
        Qc.splice(c, 0, a);
        0 === c && Vc(a);
      }
    };
    function nl(a) {
      return !(!a || 1 !== a.nodeType && 9 !== a.nodeType && 11 !== a.nodeType);
    }
    function ol(a) {
      return !(!a || 1 !== a.nodeType && 9 !== a.nodeType && 11 !== a.nodeType && (8 !== a.nodeType || " react-mount-point-unstable " !== a.nodeValue));
    }
    function pl() {
    }
    function ql(a, b, c, d, e) {
      if (e) {
        if ("function" === typeof d) {
          var f = d;
          d = function() {
            var a2 = gl(g);
            f.call(a2);
          };
        }
        var g = el(b, d, a, 0, null, false, false, "", pl);
        a._reactRootContainer = g;
        a[uf] = g.current;
        sf(8 === a.nodeType ? a.parentNode : a);
        Rk();
        return g;
      }
      for (; e = a.lastChild; ) a.removeChild(e);
      if ("function" === typeof d) {
        var h = d;
        d = function() {
          var a2 = gl(k);
          h.call(a2);
        };
      }
      var k = bl(a, 0, false, null, null, false, false, "", pl);
      a._reactRootContainer = k;
      a[uf] = k.current;
      sf(8 === a.nodeType ? a.parentNode : a);
      Rk(function() {
        fl2(b, k, c, d);
      });
      return k;
    }
    function rl(a, b, c, d, e) {
      var f = c._reactRootContainer;
      if (f) {
        var g = f;
        if ("function" === typeof e) {
          var h = e;
          e = function() {
            var a2 = gl(g);
            h.call(a2);
          };
        }
        fl2(b, g, a, e);
      } else g = ql(c, b, a, e, d);
      return gl(g);
    }
    Ec = function(a) {
      switch (a.tag) {
        case 3:
          var b = a.stateNode;
          if (b.current.memoizedState.isDehydrated) {
            var c = tc(b.pendingLanes);
            0 !== c && (Cc(b, c | 1), Dk(b, B()), 0 === (K & 6) && (Gj = B() + 500, jg()));
          }
          break;
        case 13:
          Rk(function() {
            var b3 = ih(a, 1);
            if (null !== b3) {
              var c2 = R();
              gi(b3, a, 1, c2);
            }
          }), il(a, 1);
      }
    };
    Fc = function(a) {
      if (13 === a.tag) {
        var b = ih(a, 134217728);
        if (null !== b) {
          var c = R();
          gi(b, a, 134217728, c);
        }
        il(a, 134217728);
      }
    };
    Gc = function(a) {
      if (13 === a.tag) {
        var b = yi(a), c = ih(a, b);
        if (null !== c) {
          var d = R();
          gi(c, a, b, d);
        }
        il(a, b);
      }
    };
    Hc = function() {
      return C;
    };
    Ic = function(a, b) {
      var c = C;
      try {
        return C = a, b();
      } finally {
        C = c;
      }
    };
    yb = function(a, b, c) {
      switch (b) {
        case "input":
          bb(a, c);
          b = c.name;
          if ("radio" === c.type && null != b) {
            for (c = a; c.parentNode; ) c = c.parentNode;
            c = c.querySelectorAll("input[name=" + JSON.stringify("" + b) + '][type="radio"]');
            for (b = 0; b < c.length; b++) {
              var d = c[b];
              if (d !== a && d.form === a.form) {
                var e = Db(d);
                if (!e) throw Error(p(90));
                Wa(d);
                bb(d, e);
              }
            }
          }
          break;
        case "textarea":
          ib(a, c);
          break;
        case "select":
          b = c.value, null != b && fb(a, !!c.multiple, b, false);
      }
    };
    Gb = Qk;
    Hb = Rk;
    var sl = { usingClientEntryPoint: false, Events: [Cb, ue, Db, Eb, Fb, Qk] }, tl = { findFiberByHostInstance: Wc, bundleType: 0, version: "18.3.1", rendererPackageName: "react-dom" };
    var ul = { bundleType: tl.bundleType, version: tl.version, rendererPackageName: tl.rendererPackageName, rendererConfig: tl.rendererConfig, overrideHookState: null, overrideHookStateDeletePath: null, overrideHookStateRenamePath: null, overrideProps: null, overridePropsDeletePath: null, overridePropsRenamePath: null, setErrorHandler: null, setSuspenseHandler: null, scheduleUpdate: null, currentDispatcherRef: ua.ReactCurrentDispatcher, findHostInstanceByFiber: function(a) {
      a = Zb(a);
      return null === a ? null : a.stateNode;
    }, findFiberByHostInstance: tl.findFiberByHostInstance || jl, findHostInstancesForRefresh: null, scheduleRefresh: null, scheduleRoot: null, setRefreshHandler: null, getCurrentFiber: null, reconcilerVersion: "18.3.1-next-f1338f8080-20240426" };
    if ("undefined" !== typeof __REACT_DEVTOOLS_GLOBAL_HOOK__) {
      var vl = __REACT_DEVTOOLS_GLOBAL_HOOK__;
      if (!vl.isDisabled && vl.supportsFiber) try {
        kc = vl.inject(ul), lc = vl;
      } catch (a) {
      }
    }
    reactDom_production_min.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = sl;
    reactDom_production_min.createPortal = function(a, b) {
      var c = 2 < arguments.length && void 0 !== arguments[2] ? arguments[2] : null;
      if (!nl(b)) throw Error(p(200));
      return cl(a, b, null, c);
    };
    reactDom_production_min.createRoot = function(a, b) {
      if (!nl(a)) throw Error(p(299));
      var c = false, d = "", e = kl;
      null !== b && void 0 !== b && (true === b.unstable_strictMode && (c = true), void 0 !== b.identifierPrefix && (d = b.identifierPrefix), void 0 !== b.onRecoverableError && (e = b.onRecoverableError));
      b = bl(a, 1, false, null, null, c, false, d, e);
      a[uf] = b.current;
      sf(8 === a.nodeType ? a.parentNode : a);
      return new ll(b);
    };
    reactDom_production_min.findDOMNode = function(a) {
      if (null == a) return null;
      if (1 === a.nodeType) return a;
      var b = a._reactInternals;
      if (void 0 === b) {
        if ("function" === typeof a.render) throw Error(p(188));
        a = Object.keys(a).join(",");
        throw Error(p(268, a));
      }
      a = Zb(b);
      a = null === a ? null : a.stateNode;
      return a;
    };
    reactDom_production_min.flushSync = function(a) {
      return Rk(a);
    };
    reactDom_production_min.hydrate = function(a, b, c) {
      if (!ol(b)) throw Error(p(200));
      return rl(null, a, b, true, c);
    };
    reactDom_production_min.hydrateRoot = function(a, b, c) {
      if (!nl(a)) throw Error(p(405));
      var d = null != c && c.hydratedSources || null, e = false, f = "", g = kl;
      null !== c && void 0 !== c && (true === c.unstable_strictMode && (e = true), void 0 !== c.identifierPrefix && (f = c.identifierPrefix), void 0 !== c.onRecoverableError && (g = c.onRecoverableError));
      b = el(b, null, a, 1, null != c ? c : null, e, false, f, g);
      a[uf] = b.current;
      sf(a);
      if (d) for (a = 0; a < d.length; a++) c = d[a], e = c._getVersion, e = e(c._source), null == b.mutableSourceEagerHydrationData ? b.mutableSourceEagerHydrationData = [c, e] : b.mutableSourceEagerHydrationData.push(
        c,
        e
      );
      return new ml(b);
    };
    reactDom_production_min.render = function(a, b, c) {
      if (!ol(b)) throw Error(p(200));
      return rl(null, a, b, false, c);
    };
    reactDom_production_min.unmountComponentAtNode = function(a) {
      if (!ol(a)) throw Error(p(40));
      return a._reactRootContainer ? (Rk(function() {
        rl(null, null, a, false, function() {
          a._reactRootContainer = null;
          a[uf] = null;
        });
      }), true) : false;
    };
    reactDom_production_min.unstable_batchedUpdates = Qk;
    reactDom_production_min.unstable_renderSubtreeIntoContainer = function(a, b, c, d) {
      if (!ol(c)) throw Error(p(200));
      if (null == a || void 0 === a._reactInternals) throw Error(p(38));
      return rl(a, b, c, false, d);
    };
    reactDom_production_min.version = "18.3.1-next-f1338f8080-20240426";
    return reactDom_production_min;
  }
  var hasRequiredReactDom;
  function requireReactDom() {
    if (hasRequiredReactDom) return reactDom.exports;
    hasRequiredReactDom = 1;
    function checkDCE() {
      if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ === "undefined" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE !== "function") {
        return;
      }
      try {
        __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(checkDCE);
      } catch (err2) {
        console.error(err2);
      }
    }
    {
      checkDCE();
      reactDom.exports = requireReactDom_production_min();
    }
    return reactDom.exports;
  }
  var hasRequiredClient;
  function requireClient() {
    if (hasRequiredClient) return client;
    hasRequiredClient = 1;
    var m = requireReactDom();
    {
      client.createRoot = m.createRoot;
      client.hydrateRoot = m.hydrateRoot;
    }
    return client;
  }
  var clientExports = requireClient();
  var reactDomExports = requireReactDom();
  var reactExports = requireReact();
  const React = /* @__PURE__ */ getDefaultExportFromCjs(reactExports);
  function createInitialPanelViewModel(sourceName = "demo.html") {
    return {
      revision: 0,
      sourceName,
      sourceKind: "single-html",
      runtimeMode: "edit",
      status: "浏览中",
      backendConnected: false,
      backendPort: "",
      captureMode: "now",
      selectLabel: "选择",
      selectActive: false,
      settleArmed: false,
      activeTab: "empty",
      tabs: [],
      selection: {
        hasSelection: false,
        key: "empty",
        stateHint: "",
        copyEnabled: false,
        breadthLoading: false,
        object: emptyStepper("无选区"),
        scope: emptyStepper("当前")
      },
      controls: [],
      textHint: "",
      draftPanel: {
        hasSelection: false,
        loading: false,
        hasEditableText: false,
        textHint: "",
        controls: [],
        densityExpanded: false,
        values: {
          text: "",
          colors: {},
          ranges: {},
          boxes: {},
          boxDiagram: {},
          fontWeight: {
            value: "400",
            title: "400"
          }
        },
        fontFamily: {
          current: "",
          options: []
        },
        summaries: []
      },
      snapshotPanel: null,
      footer: {
        visible: false,
        canApply: false,
        canCancel: false
      },
      dirty: false,
      editCount: 0
    };
  }
  function emptyStepper(label) {
    return {
      label,
      index: 0,
      total: 0,
      canStepDown: false,
      canStepUp: false
    };
  }
  const PanelRuntimeContext = reactExports.createContext(null);
  function createPanelRuntimeStore(initialViewModel = createInitialPanelViewModel()) {
    let snapshot = initialViewModel;
    let dispatchCommand = () => {
    };
    const listeners = /* @__PURE__ */ new Set();
    return {
      getSnapshot() {
        return snapshot;
      },
      publish(viewModel) {
        snapshot = viewModel;
        listeners.forEach((listener) => listener());
      },
      subscribe(listener) {
        listeners.add(listener);
        return () => listeners.delete(listener);
      },
      dispatch(command) {
        dispatchCommand(command);
      },
      setCommandDispatcher(dispatcher) {
        dispatchCommand = dispatcher;
      }
    };
  }
  function PanelRuntimeProvider({
    store,
    children
  }) {
    return /* @__PURE__ */ jsxRuntimeExports.jsx(PanelRuntimeContext.Provider, { value: store, children });
  }
  function usePanelRuntime() {
    const store = reactExports.useContext(PanelRuntimeContext);
    if (!store) throw new Error("PanelRuntimeProvider is missing.");
    const viewModel = reactExports.useSyncExternalStore(store.subscribe, store.getSnapshot, store.getSnapshot);
    return reactExports.useMemo(() => ({
      viewModel,
      dispatch: store.dispatch
    }), [store, viewModel]);
  }
  function SelectionBar() {
    const { viewModel, dispatch } = usePanelRuntime();
    const readOnly = viewModel.runtimeMode === "review";
    const interactionLocked = readOnly || viewModel.settleArmed || viewModel.footer.visible;
    const captureStatus = readOnly ? "使用 VibePolish 打开后可继续编辑" : viewModel.footer.visible ? "选区已冻结" : viewModel.settleArmed ? "等待页面停稳" : viewModel.selectActive ? "正在选择" : "等待选择";
    const selectLabel = viewModel.settleArmed ? "等待停稳" : "选择页面元素";
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("section", { className: "dt-capture-section", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-capture-meta", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("strong", { children: "捕获方式" }),
        /* @__PURE__ */ jsxRuntimeExports.jsx("span", { children: captureStatus })
      ] }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-capture-controls", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-capture-switch", "aria-label": "选择快照模式", children: [
          /* @__PURE__ */ jsxRuntimeExports.jsx(
            "button",
            {
              id: "dt-mode-now",
              className: viewModel.captureMode === "now" ? "dt-active" : "",
              disabled: interactionLocked,
              onClick: () => dispatch({ type: "setCaptureMode", mode: "now" }),
              children: "快照"
            }
          ),
          /* @__PURE__ */ jsxRuntimeExports.jsx(
            "button",
            {
              id: "dt-mode-settle",
              className: viewModel.captureMode === "settle" ? "dt-active" : "",
              disabled: interactionLocked,
              onClick: () => dispatch({ type: "setCaptureMode", mode: "settle" }),
              children: "延迟"
            }
          )
        ] }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "button",
          {
            id: "dt-select",
            className: `dt-capture-main${viewModel.selectActive ? " dt-active" : ""}`,
            disabled: interactionLocked,
            onClick: () => dispatch({ type: "startSelection" }),
            children: selectLabel
          }
        )
      ] })
    ] });
  }
  function Tooltip({
    content,
    children,
    placement = "top",
    maxWidth
  }) {
    const anchorRef = reactExports.useRef(null);
    const popupRef = reactExports.useRef(null);
    const timerRef = reactExports.useRef(null);
    const [anchor, setAnchor] = reactExports.useState(null);
    const [position, setPosition] = reactExports.useState(null);
    const close = () => {
      if (timerRef.current != null) window.clearTimeout(timerRef.current);
      timerRef.current = null;
      setAnchor(null);
      setPosition(null);
    };
    const open = (delay = 100) => {
      if (timerRef.current != null) window.clearTimeout(timerRef.current);
      timerRef.current = window.setTimeout(() => {
        var _a2;
        const rect = (_a2 = anchorRef.current) == null ? void 0 : _a2.getBoundingClientRect();
        if (rect) {
          const nextAnchor = { center: rect.left + rect.width / 2, top: rect.top, bottom: rect.bottom };
          setAnchor(nextAnchor);
          setPosition({
            left: nextAnchor.center,
            top: placement === "bottom" ? nextAnchor.bottom + 8 : nextAnchor.top - 8,
            arrowLeft: 0
          });
        }
        timerRef.current = null;
      }, delay);
    };
    reactExports.useLayoutEffect(() => {
      if (!anchor || !popupRef.current) return;
      const width = popupRef.current.offsetWidth;
      const viewportPadding = 8;
      const minCenter = viewportPadding + width / 2;
      const maxCenter = Math.max(minCenter, window.innerWidth - viewportPadding - width / 2);
      const left = Math.min(Math.max(anchor.center, minCenter), maxCenter);
      const arrowLeft = anchor.center - (left - width / 2);
      setPosition((current) => current && current.left === left && current.arrowLeft === arrowLeft ? current : {
        left,
        top: placement === "bottom" ? anchor.bottom + 8 : anchor.top - 8,
        arrowLeft
      });
    }, [anchor, placement]);
    reactExports.useEffect(() => () => {
      if (timerRef.current != null) window.clearTimeout(timerRef.current);
    }, []);
    return /* @__PURE__ */ jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        "span",
        {
          ref: anchorRef,
          className: "dt-tooltip-trigger",
          onMouseEnter: () => open(),
          onMouseLeave: close,
          onFocus: () => open(0),
          onBlur: close,
          children
        }
      ),
      position && reactDomExports.createPortal(
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "div",
          {
            ref: popupRef,
            className: "dt-tooltip-popup",
            "data-placement": placement,
            role: "tooltip",
            style: {
              left: position.left,
              top: position.top,
              "--dt-tooltip-arrow-left": `${position.arrowLeft}px`,
              ...maxWidth ? { maxWidth: `min(${maxWidth}px, calc(100vw - 16px))` } : {}
            },
            children: content
          }
        ),
        document.body
      )
    ] });
  }
  const CONTROL_GROUPS = [
    { key: "content", groups: ["content"], label: "内容" },
    { key: "typography", groups: ["typography"], label: "文字" },
    { key: "appearance", groups: ["appearance"], label: "外观" },
    { key: "boxModel", groups: ["size", "insetSpacing"], label: "盒模型", boxModel: true },
    { key: "position", groups: ["position"], label: "位置" }
  ];
  const FONT_SIZE_UNITS = ["px", "rem", "%"];
  const WIDTH_UNITS = ["px", "%", "rem"];
  const FONT_WEIGHT_OPTIONS = [
    { value: "300", title: "300 Light" },
    { value: "400", title: "400 Regular" },
    { value: "500", title: "500 Medium" },
    { value: "600", title: "600 Semibold" },
    { value: "700", title: "700 Bold" },
    { value: "800", title: "800 Extra Bold" },
    { value: "900", title: "900 Black" }
  ];
  function SnapshotTabs() {
    const { viewModel, dispatch } = usePanelRuntime();
    const activeTab = String(viewModel.activeTab);
    reactExports.useLayoutEffect(() => {
      dispatch({ type: "panelRendered", revision: viewModel.revision });
    }, [dispatch, viewModel.revision]);
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { id: "dt-tabs", className: "dt-tabs", children: [
      viewModel.tabs.length > 0 && /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-tab-strip", children: viewModel.tabs.map((tab) => {
        const canRollback = viewModel.runtimeMode !== "review" && !tab.draft && Number(tab.key) === viewModel.tabs.filter((item) => !item.draft).length - 1;
        return /* @__PURE__ */ jsxRuntimeExports.jsxs(
          "button",
          {
            className: `dt-tab-note${String(tab.key) === activeTab ? " dt-active" : ""}${tab.draft ? " dt-draft" : ""}`,
            "data-tab": tab.key,
            onClick: () => dispatch({ type: "setActiveTab", tab: tab.key === "draft" ? "draft" : Number(tab.key) }),
            children: [
              /* @__PURE__ */ jsxRuntimeExports.jsx("span", { children: tab.index }),
              canRollback && /* @__PURE__ */ jsxRuntimeExports.jsx(
                "span",
                {
                  role: "button",
                  tabIndex: -1,
                  className: "dt-tab-close",
                  title: "回退此快照",
                  onClick: (event) => {
                    event.preventDefault();
                    event.stopPropagation();
                    dispatch({ type: "rollbackSnapshot", index: Number(tab.key) });
                  },
                  children: "×"
                }
              )
            ]
          },
          tab.key
        );
      }) }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { id: "dt-tabs-panel", className: "dt-tab-panel", children: [
        viewModel.tabs.length === 0 && /* @__PURE__ */ jsxRuntimeExports.jsx("p", { children: "还没有快照。选择快照模式后点“选择”开始编辑。" }),
        activeTab === "draft" ? /* @__PURE__ */ jsxRuntimeExports.jsx(DraftPanel, {}, `draft-${viewModel.selection.key}`) : /* @__PURE__ */ jsxRuntimeExports.jsx(SnapshotPanel, {})
      ] })
    ] });
  }
  function DraftPanel() {
    const { viewModel } = usePanelRuntime();
    return /* @__PURE__ */ jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(SelectionPanel, {}),
      viewModel.selection.hasSelection && /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-divider" }),
      /* @__PURE__ */ jsxRuntimeExports.jsx(EditPanel, {}),
      /* @__PURE__ */ jsxRuntimeExports.jsx(ColorPopover, {}),
      /* @__PURE__ */ jsxRuntimeExports.jsx(EditSummaryList, { title: "本次修改", summaries: viewModel.draftPanel.summaries })
    ] });
  }
  function SnapshotPanel() {
    const { viewModel } = usePanelRuntime();
    const panel = viewModel.snapshotPanel;
    const [previewOpen, setPreviewOpen] = reactExports.useState(false);
    if (viewModel.tabs.length === 0) return null;
    if (!panel) return /* @__PURE__ */ jsxRuntimeExports.jsx("p", { children: "没有可展示的快照。" });
    return /* @__PURE__ */ jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        EditSummaryList,
        {
          title: "修改摘要",
          summaries: panel.summaries,
          captureDataUrl: panel.captureDataUrl,
          onPreviewCapture: () => setPreviewOpen(true)
        }
      ),
      previewOpen && panel.captureDataUrl && /* @__PURE__ */ jsxRuntimeExports.jsx(
        SnapshotCaptureModal,
        {
          src: panel.captureDataUrl,
          alt: `快照 ${panel.index} 的修改现场`,
          onClose: () => setPreviewOpen(false)
        }
      )
    ] });
  }
  function EditSummaryList({
    title,
    summaries,
    captureDataUrl = "",
    onPreviewCapture
  }) {
    if (!summaries.length) return null;
    const changeCount = summaries.reduce((total, summary) => total + summary.changes.length, 0);
    const targetCount = summaries.reduce((total, summary) => total + summary.targetCount, 0);
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("section", { className: "dt-edit-summary-section", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-edit-summary-head", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsxs("h2", { children: [
          title,
          " · ",
          changeCount,
          " 项"
        ] }),
        /* @__PURE__ */ jsxRuntimeExports.jsxs("span", { children: [
          targetCount,
          " 个目标"
        ] })
      ] }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-edit-summary-list", children: summaries.map((summary) => /* @__PURE__ */ jsxRuntimeExports.jsxs(
        "article",
        {
          className: "dt-edit-summary",
          children: [
            (summaries.length > 1 || summary.state) && /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-edit-summary-context", children: [
              summary.targetCount,
              " 个目标",
              summary.state ? ` · ${summary.state}` : ""
            ] }),
            /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-edit-summary-changes", children: summary.changes.map((change) => /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: `dt-edit-summary-change${captureDataUrl ? " dt-has-capture" : ""}`, children: [
              captureDataUrl && /* @__PURE__ */ jsxRuntimeExports.jsx(
                "button",
                {
                  className: "dt-edit-summary-thumbnail",
                  type: "button",
                  "aria-label": `查看${change.label}修改现场`,
                  onClick: onPreviewCapture,
                  children: /* @__PURE__ */ jsxRuntimeExports.jsx("img", { src: captureDataUrl, alt: "" })
                }
              ),
              /* @__PURE__ */ jsxRuntimeExports.jsx("span", { children: change.label }),
              /* @__PURE__ */ jsxRuntimeExports.jsx(EditSummaryValue, { value: change.before, color: change.color }),
              /* @__PURE__ */ jsxRuntimeExports.jsx("i", { "aria-hidden": "true", children: "→" }),
              /* @__PURE__ */ jsxRuntimeExports.jsx(EditSummaryValue, { value: change.after, color: change.color }),
              change.failed && /* @__PURE__ */ jsxRuntimeExports.jsx(Tooltip, { content: change.failureReason || "该修改没有稳定生效。", children: /* @__PURE__ */ jsxRuntimeExports.jsx("em", { className: "dt-control-failure", "aria-label": "修改未生效", children: "!" }) })
            ] }, change.property)) })
          ]
        },
        summary.id
      )) })
    ] });
  }
  function SnapshotCaptureModal({ src, alt, onClose }) {
    reactExports.useEffect(() => {
      const onKeyDown = (event) => {
        if (event.key === "Escape") onClose();
      };
      document.addEventListener("keydown", onKeyDown);
      return () => document.removeEventListener("keydown", onKeyDown);
    }, [onClose]);
    return reactDomExports.createPortal(
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        "div",
        {
          className: "dt-snapshot-modal",
          role: "dialog",
          "aria-modal": "true",
          "aria-label": "修改现场",
          onMouseDown: (event) => {
            if (event.target === event.currentTarget) onClose();
          },
          children: /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-snapshot-modal-content", children: [
            /* @__PURE__ */ jsxRuntimeExports.jsx("button", { type: "button", "aria-label": "关闭修改现场", onClick: onClose, children: "×" }),
            /* @__PURE__ */ jsxRuntimeExports.jsx("img", { src, alt })
          ] })
        }
      ),
      document.body
    );
  }
  function EditSummaryValue({ value, color }) {
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("b", { children: [
      color && /* @__PURE__ */ jsxRuntimeExports.jsx("i", { className: "dt-edit-summary-swatch", style: { background: value }, "aria-hidden": "true" }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("code", { children: value })
    ] });
  }
  function SelectionPanel() {
    var _a2;
    const { viewModel, dispatch } = usePanelRuntime();
    const selection = viewModel.selection;
    if (!selection.hasSelection) {
      return /* @__PURE__ */ jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-section-head", children: /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-section-title", children: /* @__PURE__ */ jsxRuntimeExports.jsx("h2", { children: "选区" }) }) }),
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { id: "dt-empty", children: "移动鼠标会显示红色热区。点击页面元素选择；普通点击编辑同类，Alt/Option 点击只编辑当前元素。" })
      ] });
    }
    return /* @__PURE__ */ jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-section-head", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-section-title", children: [
          /* @__PURE__ */ jsxRuntimeExports.jsx("h2", { children: "选区" }),
          /* @__PURE__ */ jsxRuntimeExports.jsx(
            "button",
            {
              className: "dt-copy",
              id: "dt-copy-selection",
              type: "button",
              disabled: !selection.copyEnabled,
              onClick: () => dispatch({ type: "copySelection" }),
              children: "复制"
            }
          )
        ] }),
        selection.stateHint && /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-section-subtitle", children: selection.stateHint })
      ] }),
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        Stepper,
        {
          label: "对象",
          downId: "dt-object-down",
          upId: "dt-object-up",
          titleDown: "选择更内层对象",
          titleUp: "选择更外层对象",
          value: selection.object.label,
          canDown: selection.object.canStepDown,
          canUp: selection.object.canStepUp,
          onDown: () => dispatch({ type: "stepObject", delta: -1 }),
          onUp: () => dispatch({ type: "stepObject", delta: 1 })
        }
      ),
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        Stepper,
        {
          label: "范围",
          downId: "dt-scope-down",
          upId: "dt-scope-up",
          titleDown: "缩小作用范围",
          titleUp: "扩大作用范围",
          value: selection.breadthLoading ? /* @__PURE__ */ jsxRuntimeExports.jsx(BreadthLoadingLabel, {}) : selection.scope.label,
          canDown: selection.scope.canStepDown,
          canUp: selection.scope.canStepUp,
          onDown: () => dispatch({ type: "stepScope", delta: -1 }),
          onUp: () => dispatch({ type: "stepScope", delta: 1 })
        }
      ),
      ((_a2 = selection.tableScope) == null ? void 0 : _a2.visible) && /* @__PURE__ */ jsxRuntimeExports.jsxs("label", { className: "dt-check-row", title: selection.tableScope.disabled ? "相似表格计算中" : "", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id: "dt-table-scope-all",
            type: "checkbox",
            checked: selection.tableScope.checked,
            disabled: selection.tableScope.disabled,
            onChange: (event) => dispatch({
              type: "setTableScopeView",
              view: event.currentTarget.checked ? "all-similar-tables" : "current-table"
            })
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx("span", { children: selection.tableScope.label })
      ] })
    ] });
  }
  function EditPanel() {
    const { viewModel, dispatch } = usePanelRuntime();
    const draft = viewModel.draftPanel;
    if (!draft.hasSelection) return null;
    if (draft.loading) {
      return /* @__PURE__ */ jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-section-head", children: /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-section-title", children: /* @__PURE__ */ jsxRuntimeExports.jsx("h2", { children: "编辑" }) }) }),
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-edit-loading", role: "status", "aria-label": "写入规则计算中", children: /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-write-spinner", "aria-hidden": "true" }) })
      ] });
    }
    return /* @__PURE__ */ jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-section-head", children: /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-section-title", children: /* @__PURE__ */ jsxRuntimeExports.jsx("h2", { children: "编辑" }) }) }),
      CONTROL_GROUPS.map((group) => {
        const controls = draft.controls.filter((control) => group.groups.includes(control.group));
        if (!controls.length) return null;
        return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-control-group", children: [
          /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-control-group-title", children: group.label }),
          "boxModel" in group && group.boxModel ? /* @__PURE__ */ jsxRuntimeExports.jsx(LayoutBoxControl, { controls }) : controls.map((control) => /* @__PURE__ */ jsxRuntimeExports.jsx(React.Fragment, { children: /* @__PURE__ */ jsxRuntimeExports.jsx(Control, { control }) }, control.key))
        ] }, group.key);
      })
    ] });
  }
  function BreadthLoadingLabel() {
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("span", { className: "dt-breadth-loading", "aria-label": "广度轴计算中", children: [
      "广度轴计算中",
      /* @__PURE__ */ jsxRuntimeExports.jsx("span", { "aria-hidden": "true", children: "." }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-loading-dot-two", "aria-hidden": "true", children: "." }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-loading-dot-three", "aria-hidden": "true", children: "." })
    ] });
  }
  function Control({ control }) {
    const { viewModel, dispatch } = usePanelRuntime();
    const key = control.key;
    if ((key === "paddingX" || key === "paddingY") && !control.enabled) {
      return /* @__PURE__ */ jsxRuntimeExports.jsx(DensityExtraWrapper, { open: viewModel.draftPanel.densityExpanded, children: /* @__PURE__ */ jsxRuntimeExports.jsx(DisabledControl, { control }) });
    }
    if (!control.enabled) return /* @__PURE__ */ jsxRuntimeExports.jsx(DisabledControl, { control });
    if (key === "text") {
      if (!viewModel.draftPanel.hasEditableText) return null;
      return /* @__PURE__ */ jsxRuntimeExports.jsxs("label", { className: "dt-control", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx(ControlLabel, { label: "文案", props: "textContent" }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "textarea",
          {
            id: "dt-text",
            className: "dt-text-input",
            rows: 1,
            defaultValue: viewModel.draftPanel.values.text,
            onInput: (event) => dispatch({ type: "editTextInput", value: event.currentTarget.value }),
            onChange: (event) => dispatch({ type: "editTextCommit", value: event.currentTarget.value })
          }
        )
      ] });
    }
    if (key === "color") return /* @__PURE__ */ jsxRuntimeExports.jsx(ColorControl, { label: "文字色", id: "dt-color", prop: "color" });
    if (key === "fontFamily") return /* @__PURE__ */ jsxRuntimeExports.jsx(FontFamilyControl, {});
    if (key === "backgroundColor") return /* @__PURE__ */ jsxRuntimeExports.jsx(ColorControl, { label: "填充色", id: "dt-bg", prop: "backgroundColor" });
    if (key === "borderColor") return /* @__PURE__ */ jsxRuntimeExports.jsx(ColorControl, { label: "边框色", id: "dt-border", prop: "borderColor" });
    if (key === "fontSize") return /* @__PURE__ */ jsxRuntimeExports.jsx(FontSizeControl, {});
    if (key === "lineHeight") return /* @__PURE__ */ jsxRuntimeExports.jsx(StaticUnitRangeControl, { label: "行高", id: "dt-line-height", prop: "lineHeight", min: 1, max: 2.4, step: 0.05, unitLabel: "倍" });
    if (key === "letterSpacing") return /* @__PURE__ */ jsxRuntimeExports.jsx(StaticUnitRangeControl, { label: "字距", id: "dt-letter-spacing", prop: "letterSpacing", min: -2, max: 12, step: 0.1, unitLabel: "px" });
    if (key === "borderRadius") return /* @__PURE__ */ jsxRuntimeExports.jsx(RadiusControl, {});
    if (key === "padding") return /* @__PURE__ */ jsxRuntimeExports.jsx(DensityControl, {});
    if (key === "paddingX") return /* @__PURE__ */ jsxRuntimeExports.jsx(DensityExtraWrapper, { open: viewModel.draftPanel.densityExpanded, children: /* @__PURE__ */ jsxRuntimeExports.jsx(StaticUnitRangeControl, { label: "横向", id: "dt-padding-x", prop: "paddingX", min: 0, max: 200, step: 1, unitLabel: "px" }) });
    if (key === "paddingY") return /* @__PURE__ */ jsxRuntimeExports.jsx(DensityExtraWrapper, { open: viewModel.draftPanel.densityExpanded, children: /* @__PURE__ */ jsxRuntimeExports.jsx(StaticUnitRangeControl, { label: "纵向", id: "dt-padding-y", prop: "paddingY", min: 0, max: 200, step: 1, unitLabel: "px" }) });
    if (key === "width") return /* @__PURE__ */ jsxRuntimeExports.jsx(WidthControl, {});
    if (key === "height") return /* @__PURE__ */ jsxRuntimeExports.jsx(StaticUnitRangeControl, { label: "高度", id: "dt-height", prop: "height", min: 0, max: 900, step: 1, unitLabel: "px" });
    if (key === "offsetX") return /* @__PURE__ */ jsxRuntimeExports.jsx(StaticUnitRangeControl, { label: "水平偏移", id: "dt-offset-x", prop: "offsetX", min: -120, max: 120, step: 1, unitLabel: "px" });
    if (key === "offsetY") return /* @__PURE__ */ jsxRuntimeExports.jsx(StaticUnitRangeControl, { label: "垂直偏移", id: "dt-offset-y", prop: "offsetY", min: -120, max: 120, step: 1, unitLabel: "px" });
    return null;
  }
  function DisabledControl({ control }) {
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-control dt-disabled", title: control.reason || "当前选区不推荐编辑该项。", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(ControlLabel, { label: controlLabel(control.key), props: control.prop || control.key, failureReason: control.failureReason }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-control-disabled-reason", children: control.reason || "不可用于当前选区" })
    ] });
  }
  function ControlLabel({
    label,
    props,
    failureReason
  }) {
    const { viewModel } = usePanelRuntime();
    const propList = (Array.isArray(props) ? props : [props]).filter(Boolean);
    const controls = viewModel.draftPanel.controls;
    const failures = propList.map((prop) => {
      var _a2;
      return failureReason || ((_a2 = controls.find((control) => control.prop === prop || control.key === prop)) == null ? void 0 : _a2.failureReason);
    }).filter(Boolean);
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("span", { className: "dt-control-label", "data-control-label-props": propList.join(","), children: [
      label,
      failures.length > 0 && /* @__PURE__ */ jsxRuntimeExports.jsx(Tooltip, { content: failures.join("\n"), children: /* @__PURE__ */ jsxRuntimeExports.jsx("i", { className: "dt-control-failure", role: "img", tabIndex: 0, "aria-label": failures.join("；"), children: "!" }) })
    ] });
  }
  function ColorControl({ label, id, prop }) {
    const { viewModel, dispatch } = usePanelRuntime();
    const value = viewModel.draftPanel.values.colors[id] || { value: "", defaultValue: "", isDefault: false, swatch: "#fff" };
    const clearDefaultMarker = (input, options = {}) => {
      if (!input.dataset.styleDefaultValue) return;
      delete input.dataset.styleDefaultValue;
      input.classList.remove("dt-default-value");
      if (options.clearValue) input.value = "";
    };
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-control", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(ControlLabel, { label, props: prop }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-color-field", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "button",
          {
            type: "button",
            className: "dt-swatch",
            id: `${id}-swatch`,
            "data-color-for": id,
            "data-style-prop": prop,
            style: { "--swatch": value.swatch },
            "aria-label": `打开${label}色板`,
            onClick: () => dispatch({ type: "openColorPopover", id, prop })
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id,
            "data-style-prop": prop,
            type: "text",
            defaultValue: value.value,
            "data-style-default-value": value.defaultValue || void 0,
            className: value.isDefault ? "dt-default-value" : void 0,
            onFocus: (event) => {
              const defaultValue = event.currentTarget.dataset.styleDefaultValue;
              if (defaultValue) {
                event.currentTarget.dataset.colorFocusDefault = defaultValue;
                event.currentTarget.dataset.colorInputDirty = "false";
              }
              clearDefaultMarker(event.currentTarget, { clearValue: true });
              dispatch({ type: "focusColorInput", id });
            },
            onInput: (event) => {
              event.currentTarget.dataset.colorInputDirty = "true";
              clearDefaultMarker(event.currentTarget);
              dispatch({ type: "editColorInput", id, prop, value: event.currentTarget.value });
            },
            onBlur: (event) => {
              const input = event.currentTarget;
              const defaultValue = input.dataset.colorFocusDefault;
              if (defaultValue && input.dataset.colorInputDirty !== "true" && !input.value) {
                input.dataset.styleDefaultValue = defaultValue;
                input.classList.add("dt-default-value");
                input.value = `${defaultValue} (默认)`;
              }
              delete input.dataset.colorFocusDefault;
              delete input.dataset.colorInputDirty;
            }
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "button",
          {
            type: "button",
            className: "dt-color-copy",
            "data-color-copy-for": id,
            "aria-label": `复制${label}值`,
            title: "复制当前值",
            onClick: () => dispatch({ type: "copyColorInput", id }),
            children: /* @__PURE__ */ jsxRuntimeExports.jsx(CopyIcon, {})
          }
        )
      ] })
    ] });
  }
  function FontFamilyControl() {
    const { viewModel, dispatch } = usePanelRuntime();
    const current = viewModel.draftPanel.fontFamily.current;
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-control", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(ControlLabel, { label: "字体", props: "fontFamily" }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-family-field", id: "dt-family-field", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "button",
          {
            type: "button",
            className: "dt-menu-button dt-family-button",
            id: "dt-family",
            "data-style-prop": "fontFamily",
            "data-value": current,
            title: current,
            onClick: (event) => {
              event.stopPropagation();
              dispatch({ type: "toggleMenu", fieldId: "dt-family-field" });
            },
            children: /* @__PURE__ */ jsxRuntimeExports.jsx("span", { children: current || "默认字体" })
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-menu-panel dt-family-menu", id: "dt-family-menu", children: viewModel.draftPanel.fontFamily.options.map((value) => /* @__PURE__ */ jsxRuntimeExports.jsx(
          "button",
          {
            type: "button",
            className: `dt-menu-option dt-family-option${value === current ? " dt-active" : ""}`,
            "data-font-family": value,
            title: value,
            onClick: (event) => {
              event.stopPropagation();
              dispatch({ type: "selectFontFamily", value });
            },
            children: value || "默认字体"
          },
          value || "default"
        )) })
      ] })
    ] });
  }
  function FontSizeControl() {
    const { viewModel, dispatch } = usePanelRuntime();
    const value = viewModel.draftPanel.values.ranges["dt-font"] || emptyRangeValue("14", "6", "120", "1", "px");
    const weight = viewModel.draftPanel.values.fontWeight;
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-control", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(ControlLabel, { label: "字号", props: ["fontSize", "fontWeight"] }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-font-field", "data-range-field": "dt-font", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-range-wrap", style: rangeWrapStyle(value.progress), children: /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id: "dt-font-range",
            "data-range-for": "dt-font",
            type: "range",
            min: value.min,
            max: value.max,
            step: value.step,
            defaultValue: value.value,
            onInput: (event) => dispatch({ type: "editRangeInput", id: "dt-font", prop: "fontSize", value: event.currentTarget.value, source: "range" })
          }
        ) }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id: "dt-font",
            "data-style-prop": "fontSize",
            type: "number",
            min: value.min,
            max: value.max,
            step: "any",
            defaultValue: value.value,
            "data-current-px": value.currentPx,
            "data-parent-px": value.parentPx,
            "data-root-px": value.rootPx,
            onInput: (event) => dispatch({ type: "editRangeInput", id: "dt-font", prop: "fontSize", value: event.currentTarget.value, source: "input" })
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx(UnitMenu, { id: "dt-font-unit", units: FONT_SIZE_UNITS, dataAttr: "data-font-unit", value: value.unit || "px" }),
        /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-weight-field", id: "dt-weight-field", children: [
          /* @__PURE__ */ jsxRuntimeExports.jsx(
            "button",
            {
              type: "button",
              className: "dt-menu-button dt-weight-button",
              id: "dt-weight",
              title: weight.title || "字重",
              "data-value": weight.value,
              onClick: (event) => {
                event.stopPropagation();
                dispatch({ type: "toggleMenu", fieldId: "dt-weight-field" });
              },
              children: /* @__PURE__ */ jsxRuntimeExports.jsx("span", { children: weight.value || "400" })
            }
          ),
          /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-menu-panel dt-weight-menu", id: "dt-weight-menu", children: FONT_WEIGHT_OPTIONS.map((item) => /* @__PURE__ */ jsxRuntimeExports.jsx(
            "button",
            {
              type: "button",
              className: `dt-menu-option dt-weight-option${item.value === weight.value ? " dt-active" : ""}`,
              "data-font-weight": item.value,
              title: item.title,
              onClick: (event) => {
                event.stopPropagation();
                dispatch({ type: "selectFontWeight", value: item.value });
              },
              children: item.value
            },
            item.value
          )) })
        ] })
      ] })
    ] });
  }
  function WidthControl() {
    const { viewModel, dispatch } = usePanelRuntime();
    const value = viewModel.draftPanel.values.ranges["dt-width"] || emptyRangeValue("0", "0", "1200", "2", "px");
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-control", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(ControlLabel, { label: "宽度", props: "width" }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-range-field", "data-range-field": "dt-width", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-range-wrap", style: rangeWrapStyle(value.progress), children: /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id: "dt-width-range",
            "data-range-for": "dt-width",
            type: "range",
            min: value.min,
            max: value.max,
            step: value.step,
            defaultValue: value.value,
            onInput: (event) => dispatch({ type: "editRangeInput", id: "dt-width", prop: "width", value: event.currentTarget.value, source: "range" })
          }
        ) }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id: "dt-width",
            "data-style-prop": "width",
            type: "number",
            min: value.min,
            max: value.max,
            step: "any",
            defaultValue: value.value,
            "data-current-px": value.currentPx,
            "data-parent-px": value.parentPx,
            "data-root-px": value.rootPx,
            onInput: (event) => dispatch({ type: "editRangeInput", id: "dt-width", prop: "width", value: event.currentTarget.value, source: "input" })
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx(UnitMenu, { id: "dt-width-unit", units: WIDTH_UNITS, dataAttr: "data-width-unit", value: value.unit || "px" })
      ] })
    ] });
  }
  function UnitMenu({ id, units, dataAttr, value, disabled, title }) {
    const { dispatch } = usePanelRuntime();
    const fieldId = `${id}-field`;
    const menuId = `${id}-menu`;
    const unitKind = dataAttr === "data-font-unit" ? "font" : "width";
    const current = value || "px";
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-unit-field", id: fieldId, children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        "button",
        {
          type: "button",
          className: "dt-menu-button dt-unit-button",
          id,
          "data-unit-for": id.replace(/-unit$/, ""),
          "data-value": current,
          title: title || current,
          disabled,
          onClick: (event) => {
            event.stopPropagation();
            dispatch({ type: "toggleMenu", fieldId });
          },
          children: /* @__PURE__ */ jsxRuntimeExports.jsx("span", { children: current })
        }
      ),
      /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-menu-panel dt-unit-menu", id: menuId, children: units.map((unit) => /* @__PURE__ */ reactExports.createElement(
        "button",
        {
          type: "button",
          className: `dt-menu-option dt-unit-option${unit === current ? " dt-active" : ""}`,
          ...{ [dataAttr]: unit },
          title: unit,
          key: unit,
          onClick: (event) => {
            event.stopPropagation();
            dispatch({ type: "selectUnit", id: id.replace(/-unit$/, ""), unitKind, value: unit });
          }
        },
        unit
      )) })
    ] });
  }
  function DensityControl() {
    const { viewModel, dispatch } = usePanelRuntime();
    const open = viewModel.draftPanel.densityExpanded;
    const value = viewModel.draftPanel.values.ranges["dt-padding"] || emptyRangeValue("0", "0", "200", "1");
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-control", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsxs("span", { className: "dt-density-label", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx(ControlLabel, { label: "密度", props: "padding" }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "button",
          {
            type: "button",
            id: "dt-density-toggle",
            className: `dt-density-toggle${open ? " dt-open" : ""}`,
            "aria-label": open ? "收起密度细分" : "展开密度细分",
            title: open ? "收起横向/纵向密度" : "展开横向/纵向密度",
            onClick: (event) => {
              event.preventDefault();
              event.stopPropagation();
              dispatch({ type: "toggleDensity" });
            },
            children: /* @__PURE__ */ jsxRuntimeExports.jsx(ChevronIcon, {})
          }
        )
      ] }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-range-field", "data-range-field": "dt-padding", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-range-wrap", style: rangeWrapStyle(value.progress), children: /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id: "dt-padding-range",
            "data-range-for": "dt-padding",
            type: "range",
            min: value.min,
            max: value.max,
            step: value.step,
            defaultValue: value.value,
            onInput: (event) => dispatch({ type: "editRangeInput", id: "dt-padding", prop: "padding", value: event.currentTarget.value, source: "range" })
          }
        ) }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id: "dt-padding",
            "data-style-prop": "padding",
            type: "number",
            min: value.min,
            max: value.max,
            step: "any",
            defaultValue: value.value,
            onInput: (event) => dispatch({ type: "editRangeInput", id: "dt-padding", prop: "padding", value: event.currentTarget.value, source: "input" })
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-unit-static", children: "px" })
      ] })
    ] });
  }
  function DensityExtraWrapper({ open, children }) {
    return React.cloneElement(children, {
      className: `${children.props.className || "dt-control"} dt-density-extra`,
      hidden: !open
    });
  }
  function StaticUnitRangeControl({ label, id, prop, min, max: max2, step, unitLabel }) {
    const { viewModel, dispatch } = usePanelRuntime();
    const value = viewModel.draftPanel.values.ranges[id] || emptyRangeValue(String(min), String(min), String(max2), String(step));
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-control", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(ControlLabel, { label, props: prop }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-range-field", "data-range-field": id, children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-range-wrap", style: rangeWrapStyle(value.progress), children: /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id: `${id}-range`,
            "data-range-for": id,
            type: "range",
            min: value.min || min,
            max: value.max || max2,
            step: value.step || step,
            defaultValue: value.value,
            onInput: (event) => dispatch({ type: "editRangeInput", id, prop, value: event.currentTarget.value, source: "range" })
          }
        ) }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id,
            "data-style-prop": prop,
            type: "number",
            min: value.min || min,
            max: value.max || max2,
            step: "any",
            defaultValue: value.value,
            onInput: (event) => dispatch({ type: "editRangeInput", id, prop, value: event.currentTarget.value, source: "input" })
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-unit-static", children: unitLabel })
      ] })
    ] });
  }
  function RadiusControl() {
    const { viewModel, dispatch } = usePanelRuntime();
    const value = viewModel.draftPanel.values.ranges["dt-radius"] || emptyRangeValue("0", "0", "60", "1");
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-control", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(ControlLabel, { label: "圆角", props: "borderRadius" }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-range-field", "data-range-field": "dt-radius", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-range-wrap", style: rangeWrapStyle(value.progress), children: /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id: "dt-radius-range",
            "data-range-for": "dt-radius",
            type: "range",
            min: value.min,
            max: value.max,
            step: value.step,
            defaultValue: value.sliderValue || value.value,
            onInput: (event) => dispatch({ type: "editRangeInput", id: "dt-radius", prop: "borderRadius", value: event.currentTarget.value, source: "range" })
          }
        ) }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(
          "input",
          {
            id: "dt-radius",
            "data-style-prop": "borderRadius",
            type: "number",
            min: value.min,
            max: value.inputMax || "9999",
            step: value.step,
            defaultValue: value.value,
            onInput: (event) => dispatch({ type: "editRangeInput", id: "dt-radius", prop: "borderRadius", value: event.currentTarget.value, source: "input" })
          }
        ),
        /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-unit-static", children: "px" })
      ] })
    ] });
  }
  function LayoutBoxControl({ controls }) {
    const { viewModel } = usePanelRuntime();
    const byKey = new Map(controls.map((control) => [control.key, control]));
    const diagram = viewModel.draftPanel.values.boxDiagram;
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-box-model", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-box-diagram", "aria-hidden": "true", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-box-measure dt-box-width", children: /* @__PURE__ */ jsxRuntimeExports.jsxs("span", { children: [
          "宽度 ",
          /* @__PURE__ */ jsxRuntimeExports.jsx("b", { id: "dt-box-width-value", children: diagram["dt-box-width-value"] || "-" })
        ] }) }),
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-box-measure dt-box-height", children: /* @__PURE__ */ jsxRuntimeExports.jsxs("span", { children: [
          "高度",
          /* @__PURE__ */ jsxRuntimeExports.jsx("br", {}),
          /* @__PURE__ */ jsxRuntimeExports.jsx("b", { id: "dt-box-height-value", children: diagram["dt-box-height-value"] || "-" })
        ] }) }),
        /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-box-outer", children: [
          /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-box-label dt-box-pad-top", children: [
            "上留白 ",
            /* @__PURE__ */ jsxRuntimeExports.jsx("b", { id: "dt-box-padding-top-value", children: diagram["dt-box-padding-top-value"] || "-" })
          ] }),
          /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-box-label dt-box-pad-bottom", children: [
            "下留白 ",
            /* @__PURE__ */ jsxRuntimeExports.jsx("b", { id: "dt-box-padding-bottom-value", children: diagram["dt-box-padding-bottom-value"] || "-" })
          ] }),
          /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-box-label dt-box-pad-left", children: [
            "左留白",
            /* @__PURE__ */ jsxRuntimeExports.jsx("br", {}),
            /* @__PURE__ */ jsxRuntimeExports.jsx("b", { id: "dt-box-padding-left-value", children: diagram["dt-box-padding-left-value"] || "-" })
          ] }),
          /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-box-label dt-box-pad-right", children: [
            "右留白",
            /* @__PURE__ */ jsxRuntimeExports.jsx("br", {}),
            /* @__PURE__ */ jsxRuntimeExports.jsx("b", { id: "dt-box-padding-right-value", children: diagram["dt-box-padding-right-value"] || "-" })
          ] }),
          /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-box-inner", children: /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-box-label dt-box-content", children: "内容" }) })
        ] })
      ] }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-box-grid", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx(BoxNumberField, { label: "宽:", id: "dt-width", prop: "width", hasUnitMenu: true, control: byKey.get("width") }),
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-box-sep", "aria-hidden": "true" }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(BoxNumberField, { label: "高:", id: "dt-height", prop: "height", control: byKey.get("height") }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(BoxNumberField, { label: "左:", id: "dt-padding-left", prop: "paddingLeft", control: byKey.get("paddingLeft") }),
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-box-sep", "aria-hidden": "true" }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(BoxNumberField, { label: "右:", id: "dt-padding-right", prop: "paddingRight", control: byKey.get("paddingRight") }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(BoxNumberField, { label: "上:", id: "dt-padding-top", prop: "paddingTop", control: byKey.get("paddingTop") }),
        /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-box-sep", "aria-hidden": "true" }),
        /* @__PURE__ */ jsxRuntimeExports.jsx(BoxNumberField, { label: "下:", id: "dt-padding-bottom", prop: "paddingBottom", control: byKey.get("paddingBottom") })
      ] })
    ] });
  }
  function BoxNumberField({ label, id, prop, hasUnitMenu, control }) {
    const { viewModel, dispatch } = usePanelRuntime();
    const value = viewModel.draftPanel.values.boxes[id] || emptyBoxValue();
    const disabled = !!control && !control.enabled;
    const reason = (control == null ? void 0 : control.reason) || "当前选区不适合该配置。";
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: `dt-box-field${disabled ? " dt-disabled" : ""}`, children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx("label", { htmlFor: id, children: /* @__PURE__ */ jsxRuntimeExports.jsx(ControlLabel, { label, props: prop, failureReason: control == null ? void 0 : control.failureReason }) }),
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        "input",
        {
          id,
          "data-style-prop": prop,
          type: "number",
          step: "any",
          disabled,
          title: disabled ? reason : void 0,
          defaultValue: value.value,
          min: value.min,
          max: value.max,
          "data-current-px": value.currentPx,
          "data-parent-px": value.parentPx,
          "data-root-px": value.rootPx,
          "data-layout-default-value": value.isDefault ? value.value : void 0,
          className: value.isDefault ? "dt-default-value" : void 0,
          onInput: (event) => dispatch({ type: "editBoxInput", id, prop, value: event.currentTarget.value })
        }
      ),
      hasUnitMenu ? /* @__PURE__ */ jsxRuntimeExports.jsx(UnitMenu, { id: `${id}-unit`, units: WIDTH_UNITS, dataAttr: "data-width-unit", value: value.unit, disabled, title: disabled ? reason : value.unit }) : /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-unit-static", children: "px" })
    ] });
  }
  function ColorPopover() {
    const { dispatch } = usePanelRuntime();
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-color-popover", id: "dt-color-popover", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-iro-mount", id: "dt-iro-mount" }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-color-actions", role: "group", "aria-label": "颜色特殊值", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("button", { type: "button", className: "dt-color-action-transparent", id: "dt-color-transparent", onClick: () => dispatch({ type: "applyActiveColor", value: "transparent", close: true }), children: "透明" }),
        /* @__PURE__ */ jsxRuntimeExports.jsx("button", { type: "button", id: "dt-color-empty", onClick: () => dispatch({ type: "clearActiveColor" }), children: "清空" })
      ] }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "dt-color-divider", "aria-hidden": "true" }),
      /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-color-format", role: "group", "aria-label": "颜色输出格式", children: [
        /* @__PURE__ */ jsxRuntimeExports.jsx("button", { type: "button", "data-color-format": "hex", onClick: () => dispatch({ type: "setColorFormat", format: "hex" }), children: "HEX" }),
        /* @__PURE__ */ jsxRuntimeExports.jsx("button", { type: "button", "data-color-format": "rgba", className: "dt-active", onClick: () => dispatch({ type: "setColorFormat", format: "rgba" }), children: "RGBA" })
      ] })
    ] });
  }
  function Stepper({
    label,
    downId,
    upId,
    titleDown,
    titleUp,
    value,
    canDown,
    canUp,
    onDown,
    onUp
  }) {
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-stepper", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx("span", { children: label }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("button", { id: downId, title: titleDown, disabled: !canDown, onClick: onDown, children: "‹" }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("b", { children: value }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("button", { id: upId, title: titleUp, disabled: !canUp, onClick: onUp, children: "›" })
    ] });
  }
  function controlLabel(key) {
    return {
      text: "文案",
      color: "文字色",
      fontFamily: "字体",
      fontSize: "字号",
      fontWeight: "字重",
      lineHeight: "行高",
      letterSpacing: "字距",
      backgroundColor: "填充色",
      borderColor: "边框色",
      borderRadius: "圆角",
      padding: "密度",
      paddingX: "横向",
      paddingY: "纵向",
      width: "宽度",
      height: "高度",
      offsetX: "水平偏移",
      offsetY: "垂直偏移"
    }[key] || key;
  }
  function emptyRangeValue(value, min, max2, step, unit = "") {
    return {
      value,
      min,
      max: max2,
      step,
      unit,
      progress: "0%"
    };
  }
  function emptyBoxValue() {
    return {
      value: "",
      min: "0",
      max: "9999",
      step: "1",
      unit: "px",
      isDefault: false
    };
  }
  function rangeWrapStyle(progress) {
    return {
      "--dt-ruler-step": "10%",
      "--dt-range-progress": progress || "0%"
    };
  }
  function CopyIcon() {
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("svg", { viewBox: "0 0 24 24", "aria-hidden": "true", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx("rect", { x: "9", y: "9", width: "13", height: "13", rx: "2", ry: "2" }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("path", { d: "M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" })
    ] });
  }
  function ChevronIcon() {
    return /* @__PURE__ */ jsxRuntimeExports.jsx("svg", { viewBox: "0 0 24 24", "aria-hidden": "true", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round", children: /* @__PURE__ */ jsxRuntimeExports.jsx("path", { d: "m9 18 6-6-6-6" }) });
  }
  function FooterActions() {
    const { viewModel, dispatch } = usePanelRuntime();
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("footer", { id: "dt-footer", className: "dt-footer", hidden: !viewModel.footer.visible, children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        "button",
        {
          id: "dt-cancel",
          disabled: !viewModel.footer.canCancel,
          onClick: () => dispatch({ type: "cancelDraft" }),
          children: "取消"
        }
      ),
      /* @__PURE__ */ jsxRuntimeExports.jsx(
        "button",
        {
          id: "dt-apply",
          className: "dt-primary",
          disabled: !viewModel.footer.canApply,
          onClick: () => dispatch({ type: "applyDraft" }),
          children: "应用"
        }
      )
    ] });
  }
  function Panel() {
    var _a2;
    const { viewModel, dispatch } = usePanelRuntime();
    const [open, setOpen] = reactExports.useState(viewModel.runtimeMode === "review");
    const [saveMenuOpen, setSaveMenuOpen] = reactExports.useState(false);
    const hasInjectedBackend = typeof window !== "undefined" && typeof window.__DESIGNTOOLS_CDP_STYLE_PROVIDER__ === "function";
    const backendConnected = viewModel.backendConnected || hasInjectedBackend;
    const backendPort = viewModel.backendPort || (((_a2 = window.__DESIGNTOOLS_CDP_STYLE_PROVIDER_META__) == null ? void 0 : _a2.port) ?? "");
    const closeDisabled = viewModel.footer.visible;
    const closeTooltip = viewModel.settleArmed ? "延迟捕获等待中，请先取消。" : viewModel.footer.visible ? viewModel.footer.canApply ? "当前快照有未保存修改，请先应用或取消。" : "当前快照尚未修改，请先取消。" : "关闭配置面板";
    const hasModifications = viewModel.editCount > 0;
    const persistenceLocked = viewModel.footer.visible || viewModel.settleArmed;
    const unavailableTooltip = "修改后可用";
    const copyTooltip = hasModifications ? "复制适合交给 AI 的结构化修改说明，用于在生产代码中复现当前调整。" : unavailableTooltip;
    const exportDisabled = !hasModifications || persistenceLocked || !backendConnected;
    const exportTooltip = !hasModifications ? unavailableTooltip : persistenceLocked ? "请先应用或取消当前快照。" : !backendConnected ? "后台服务未连接，暂时无法导出协作包。" : "导出包含修改后源码、视觉快照和可继续编辑历史的 VibePolish 协作包。";
    const applySourceDisabled = viewModel.runtimeMode === "review" || !hasModifications || persistenceLocked || !backendConnected;
    const saveAsDisabled = viewModel.runtimeMode === "review" || !hasModifications || persistenceLocked || viewModel.sourceKind === "project" && !backendConnected;
    const applySourceTooltip = viewModel.runtimeMode === "review" ? "当前为只读评审模式，请使用 VibePolish 打开工程包继续编辑。" : !hasModifications ? unavailableTooltip : persistenceLocked ? "请先应用或取消当前快照。" : !backendConnected ? "后台服务未连接，暂时无法写回原文件。" : viewModel.sourceKind === "project" ? "将当前全部修改直接写回原项目文件。" : "将当前全部修改直接写回原 HTML 文件。";
    reactExports.useEffect(() => {
      if (viewModel.runtimeMode === "review") setOpen(true);
    }, [viewModel.runtimeMode]);
    reactExports.useEffect(() => {
      if (!saveMenuOpen) return;
      const closeSaveMenu = (event) => {
        var _a3;
        if (!((_a3 = event.target) == null ? void 0 : _a3.closest(".dt-save-split"))) setSaveMenuOpen(false);
      };
      document.addEventListener("pointerdown", closeSaveMenu);
      return () => document.removeEventListener("pointerdown", closeSaveMenu);
    }, [saveMenuOpen]);
    reactExports.useEffect(() => {
      const app = document.querySelector(".dt-app");
      if (!app) return;
      app.dataset.panelOpen = open ? "true" : "false";
    }, [open]);
    if (!open) {
      return /* @__PURE__ */ jsxRuntimeExports.jsx(
        "button",
        {
          id: "dt-panel-launcher",
          className: "dt-panel-launcher",
          type: "button",
          onClick: () => setOpen(true),
          children: "VibePolish"
        }
      );
    }
    return /* @__PURE__ */ jsxRuntimeExports.jsxs(
      "aside",
      {
        className: "dt-side",
        "data-panel-capture-mode": viewModel.captureMode,
        "data-panel-active-tab": String(viewModel.activeTab),
        "data-panel-dirty": viewModel.dirty ? "true" : "false",
        children: [
          /* @__PURE__ */ jsxRuntimeExports.jsxs("header", { className: "dt-side-head", children: [
            /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-side-head-main", children: [
              /* @__PURE__ */ jsxRuntimeExports.jsx("strong", { children: "VibePolish" }),
              /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-export-actions", children: [
                /* @__PURE__ */ jsxRuntimeExports.jsx(Tooltip, { content: copyTooltip, placement: "bottom", maxWidth: 220, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
                  "button",
                  {
                    id: "dt-copy-prompt",
                    className: "dt-panel-icon-button",
                    type: "button",
                    "aria-label": "复制 Prompt",
                    disabled: !hasModifications,
                    onClick: () => dispatch({ type: "copyPrompt" }),
                    children: /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-prompt-icon", "aria-hidden": "true", children: "P" })
                  }
                ) }),
                /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: `dt-save-split${saveMenuOpen ? " dt-open" : ""}`, children: [
                  /* @__PURE__ */ jsxRuntimeExports.jsx(Tooltip, { content: applySourceTooltip, placement: "bottom", maxWidth: 220, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
                    "button",
                    {
                      id: "dt-apply-source",
                      className: "dt-panel-icon-button dt-save-main",
                      type: "button",
                      "aria-label": "保存到原项目",
                      disabled: applySourceDisabled,
                      onClick: () => dispatch({ type: "applySource" }),
                      children: /* @__PURE__ */ jsxRuntimeExports.jsx(SaveIcon, {})
                    }
                  ) }),
                  /* @__PURE__ */ jsxRuntimeExports.jsx(
                    "button",
                    {
                      id: "dt-save-menu-toggle",
                      className: "dt-panel-icon-button dt-save-toggle",
                      type: "button",
                      "aria-label": "打开保存菜单",
                      "aria-expanded": saveMenuOpen,
                      disabled: saveAsDisabled,
                      onClick: () => setSaveMenuOpen((value) => !value),
                      children: /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-save-chevron", "aria-hidden": "true" })
                    }
                  ),
                  saveMenuOpen && /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-save-menu", role: "menu", children: [
                    /* @__PURE__ */ jsxRuntimeExports.jsx("button", { type: "button", role: "menuitem", disabled: applySourceDisabled, onClick: () => {
                      setSaveMenuOpen(false);
                      dispatch({ type: "applySource" });
                    }, children: "保存到原项目" }),
                    /* @__PURE__ */ jsxRuntimeExports.jsx("button", { id: "dt-save-as", type: "button", role: "menuitem", disabled: saveAsDisabled, onClick: () => {
                      setSaveMenuOpen(false);
                      dispatch({ type: "saveSourceAs" });
                    }, children: "另存为…" })
                  ] })
                ] }),
                /* @__PURE__ */ jsxRuntimeExports.jsx(Tooltip, { content: exportTooltip, placement: "bottom", maxWidth: 220, children: /* @__PURE__ */ jsxRuntimeExports.jsx("button", { id: "dt-export", className: "dt-panel-icon-button", type: "button", "aria-label": "导出协作包", disabled: exportDisabled, onClick: () => dispatch({ type: "export" }), children: /* @__PURE__ */ jsxRuntimeExports.jsx(ShareIcon, {}) }) }),
                /* @__PURE__ */ jsxRuntimeExports.jsx(Tooltip, { content: closeTooltip, placement: "bottom", maxWidth: 160, children: /* @__PURE__ */ jsxRuntimeExports.jsx(
                  "button",
                  {
                    id: "dt-panel-close",
                    className: "dt-panel-icon-button",
                    type: "button",
                    "aria-label": "关闭配置面板",
                    disabled: closeDisabled,
                    onClick: () => setOpen(false),
                    children: /* @__PURE__ */ jsxRuntimeExports.jsx("span", { "aria-hidden": "true", children: "×" })
                  }
                ) })
              ] })
            ] }),
            /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-side-status", children: [
              /* @__PURE__ */ jsxRuntimeExports.jsx("span", { id: "dt-status", children: viewModel.status }),
              /* @__PURE__ */ jsxRuntimeExports.jsxs("div", { className: "dt-side-status-actions", children: [
                viewModel.runtimeMode !== "review" && !backendConnected && /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-backend-alert", children: "后台服务未连接" }),
                viewModel.runtimeMode !== "review" && backendConnected && backendPort && /* @__PURE__ */ jsxRuntimeExports.jsxs("span", { className: "dt-backend-badge", children: [
                  "CDP ",
                  backendPort
                ] }),
                viewModel.runtimeMode === "review" && /* @__PURE__ */ jsxRuntimeExports.jsx("span", { className: "dt-backend-badge", children: "只读评审" })
              ] })
            ] })
          ] }),
          /* @__PURE__ */ jsxRuntimeExports.jsx(SelectionBar, {}),
          /* @__PURE__ */ jsxRuntimeExports.jsx(SnapshotTabs, {}),
          /* @__PURE__ */ jsxRuntimeExports.jsx(FooterActions, {})
        ]
      }
    );
  }
  function ShareIcon() {
    return /* @__PURE__ */ jsxRuntimeExports.jsxs("svg", { viewBox: "0 0 24 24", "aria-hidden": "true", children: [
      /* @__PURE__ */ jsxRuntimeExports.jsx("path", { d: "M9 7H5v12h14v-7" }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("path", { d: "M9 15c0-4.4 2.7-7 8-7" }),
      /* @__PURE__ */ jsxRuntimeExports.jsx("path", { d: "m14 5 3 3-3 3" })
    ] });
  }
  function SaveIcon() {
    return /* @__PURE__ */ jsxRuntimeExports.jsx("svg", { viewBox: "0 0 24 24", "aria-hidden": "true", children: /* @__PURE__ */ jsxRuntimeExports.jsx("path", { d: "M5 4h12l2 2v14H5zM8 4v6h8V4M8 20v-6h8v6" }) });
  }
  function toCssProp(prop) {
    return prop.replace(/[A-Z]/g, (match) => `-${match.toLowerCase()}`);
  }
  function downloadTextFile({
    filename,
    content,
    mimeType,
    root = document,
    urlApi = URL
  }) {
    const blob = new Blob([content], { type: mimeType });
    const anchor = root.createElement("a");
    anchor.href = urlApi.createObjectURL(blob);
    anchor.download = filename;
    anchor.click();
    urlApi.revokeObjectURL(anchor.href);
  }
  function downloadBase64File({
    filename,
    content,
    mimeType,
    root = document,
    urlApi = URL
  }) {
    const binary = atob(content);
    const bytes = new Uint8Array(binary.length);
    for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
    const blob = new Blob([bytes], { type: mimeType });
    const anchor = root.createElement("a");
    anchor.href = urlApi.createObjectURL(blob);
    anchor.download = filename;
    anchor.click();
    urlApi.revokeObjectURL(anchor.href);
  }
  var u8 = Uint8Array, u16 = Uint16Array, i32 = Int32Array;
  var fleb = new u8([
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    2,
    2,
    2,
    2,
    3,
    3,
    3,
    3,
    4,
    4,
    4,
    4,
    5,
    5,
    5,
    5,
    0,
    /* unused */
    0,
    0,
    /* impossible */
    0
  ]);
  var fdeb = new u8([
    0,
    0,
    0,
    0,
    1,
    1,
    2,
    2,
    3,
    3,
    4,
    4,
    5,
    5,
    6,
    6,
    7,
    7,
    8,
    8,
    9,
    9,
    10,
    10,
    11,
    11,
    12,
    12,
    13,
    13,
    /* unused */
    0,
    0
  ]);
  var clim = new u8([16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]);
  var freb = function(eb, start) {
    var b = new u16(31);
    for (var i2 = 0; i2 < 31; ++i2) {
      b[i2] = start += 1 << eb[i2 - 1];
    }
    var r = new i32(b[30]);
    for (var i2 = 1; i2 < 30; ++i2) {
      for (var j = b[i2]; j < b[i2 + 1]; ++j) {
        r[j] = j - b[i2] << 5 | i2;
      }
    }
    return { b, r };
  };
  var _a = freb(fleb, 2), fl = _a.b, revfl = _a.r;
  fl[28] = 258, revfl[258] = 28;
  var _b = freb(fdeb, 0), fd = _b.b;
  var rev = new u16(32768);
  for (var i = 0; i < 32768; ++i) {
    var x = (i & 43690) >> 1 | (i & 21845) << 1;
    x = (x & 52428) >> 2 | (x & 13107) << 2;
    x = (x & 61680) >> 4 | (x & 3855) << 4;
    rev[i] = ((x & 65280) >> 8 | (x & 255) << 8) >> 1;
  }
  var hMap = (function(cd, mb, r) {
    var s = cd.length;
    var i2 = 0;
    var l = new u16(mb);
    for (; i2 < s; ++i2) {
      if (cd[i2])
        ++l[cd[i2] - 1];
    }
    var le = new u16(mb);
    for (i2 = 1; i2 < mb; ++i2) {
      le[i2] = le[i2 - 1] + l[i2 - 1] << 1;
    }
    var co;
    if (r) {
      co = new u16(1 << mb);
      var rvb = 15 - mb;
      for (i2 = 0; i2 < s; ++i2) {
        if (cd[i2]) {
          var sv = i2 << 4 | cd[i2];
          var r_1 = mb - cd[i2];
          var v = le[cd[i2] - 1]++ << r_1;
          for (var m = v | (1 << r_1) - 1; v <= m; ++v) {
            co[rev[v] >> rvb] = sv;
          }
        }
      }
    } else {
      co = new u16(s);
      for (i2 = 0; i2 < s; ++i2) {
        if (cd[i2]) {
          co[i2] = rev[le[cd[i2] - 1]++] >> 15 - cd[i2];
        }
      }
    }
    return co;
  });
  var flt = new u8(288);
  for (var i = 0; i < 144; ++i)
    flt[i] = 8;
  for (var i = 144; i < 256; ++i)
    flt[i] = 9;
  for (var i = 256; i < 280; ++i)
    flt[i] = 7;
  for (var i = 280; i < 288; ++i)
    flt[i] = 8;
  var fdt = new u8(32);
  for (var i = 0; i < 32; ++i)
    fdt[i] = 5;
  var flrm = /* @__PURE__ */ hMap(flt, 9, 1);
  var fdrm = /* @__PURE__ */ hMap(fdt, 5, 1);
  var max = function(a) {
    var m = a[0];
    for (var i2 = 1; i2 < a.length; ++i2) {
      if (a[i2] > m)
        m = a[i2];
    }
    return m;
  };
  var bits = function(d, p, m) {
    var o = p / 8 | 0;
    return (d[o] | d[o + 1] << 8) >> (p & 7) & m;
  };
  var bits16 = function(d, p) {
    var o = p / 8 | 0;
    return (d[o] | d[o + 1] << 8 | d[o + 2] << 16) >> (p & 7);
  };
  var shft = function(p) {
    return (p + 7) / 8 | 0;
  };
  var slc = function(v, s, e) {
    if (s == null || s < 0)
      s = 0;
    if (e == null || e > v.length)
      e = v.length;
    return new u8(v.subarray(s, e));
  };
  var ec = [
    "unexpected EOF",
    "invalid block type",
    "invalid length/literal",
    "invalid distance",
    "stream finished",
    "no stream handler",
    ,
    // determined by compression function
    "no callback",
    "invalid UTF-8 data",
    "extra field too long",
    "date not in range 1980-2099",
    "filename too long",
    "stream finishing",
    "invalid zip data"
    // determined by unknown compression method
  ];
  var err = function(ind, msg, nt) {
    var e = new Error(msg || ec[ind]);
    e.code = ind;
    if (Error.captureStackTrace)
      Error.captureStackTrace(e, err);
    if (!nt)
      throw e;
    return e;
  };
  var inflt = function(dat, st, buf, dict) {
    var sl = dat.length, dl = dict ? dict.length : 0;
    if (!sl || st.f && !st.l)
      return buf || new u8(0);
    var noBuf = !buf;
    var resize = noBuf || st.i != 2;
    var noSt = st.i;
    if (noBuf)
      buf = new u8(sl * 3);
    var cbuf = function(l2) {
      var bl = buf.length;
      if (l2 > bl) {
        var nbuf = new u8(Math.max(bl * 2, l2));
        nbuf.set(buf);
        buf = nbuf;
      }
    };
    var final = st.f || 0, pos = st.p || 0, bt = st.b || 0, lm = st.l, dm = st.d, lbt = st.m, dbt = st.n;
    var tbts = sl * 8;
    do {
      if (!lm) {
        final = bits(dat, pos, 1);
        var type = bits(dat, pos + 1, 3);
        pos += 3;
        if (!type) {
          var s = shft(pos) + 4, l = dat[s - 4] | dat[s - 3] << 8, t = s + l;
          if (t > sl) {
            if (noSt)
              err(0);
            break;
          }
          if (resize)
            cbuf(bt + l);
          buf.set(dat.subarray(s, t), bt);
          st.b = bt += l, st.p = pos = t * 8, st.f = final;
          continue;
        } else if (type == 1)
          lm = flrm, dm = fdrm, lbt = 9, dbt = 5;
        else if (type == 2) {
          var hLit = bits(dat, pos, 31) + 257, hcLen = bits(dat, pos + 10, 15) + 4;
          var tl = hLit + bits(dat, pos + 5, 31) + 1;
          pos += 14;
          var ldt = new u8(tl);
          var clt = new u8(19);
          for (var i2 = 0; i2 < hcLen; ++i2) {
            clt[clim[i2]] = bits(dat, pos + i2 * 3, 7);
          }
          pos += hcLen * 3;
          var clb = max(clt), clbmsk = (1 << clb) - 1;
          var clm = hMap(clt, clb, 1);
          for (var i2 = 0; i2 < tl; ) {
            var r = clm[bits(dat, pos, clbmsk)];
            pos += r & 15;
            var s = r >> 4;
            if (s < 16) {
              ldt[i2++] = s;
            } else {
              var c = 0, n = 0;
              if (s == 16)
                n = 3 + bits(dat, pos, 3), pos += 2, c = ldt[i2 - 1];
              else if (s == 17)
                n = 3 + bits(dat, pos, 7), pos += 3;
              else if (s == 18)
                n = 11 + bits(dat, pos, 127), pos += 7;
              while (n--)
                ldt[i2++] = c;
            }
          }
          var lt = ldt.subarray(0, hLit), dt = ldt.subarray(hLit);
          lbt = max(lt);
          dbt = max(dt);
          lm = hMap(lt, lbt, 1);
          dm = hMap(dt, dbt, 1);
        } else
          err(1);
        if (pos > tbts) {
          if (noSt)
            err(0);
          break;
        }
      }
      if (resize)
        cbuf(bt + 131072);
      var lms = (1 << lbt) - 1, dms = (1 << dbt) - 1;
      var lpos = pos;
      for (; ; lpos = pos) {
        var c = lm[bits16(dat, pos) & lms], sym = c >> 4;
        pos += c & 15;
        if (pos > tbts) {
          if (noSt)
            err(0);
          break;
        }
        if (!c)
          err(2);
        if (sym < 256)
          buf[bt++] = sym;
        else if (sym == 256) {
          lpos = pos, lm = null;
          break;
        } else {
          var add = sym - 254;
          if (sym > 264) {
            var i2 = sym - 257, b = fleb[i2];
            add = bits(dat, pos, (1 << b) - 1) + fl[i2];
            pos += b;
          }
          var d = dm[bits16(dat, pos) & dms], dsym = d >> 4;
          if (!d)
            err(3);
          pos += d & 15;
          var dt = fd[dsym];
          if (dsym > 3) {
            var b = fdeb[dsym];
            dt += bits16(dat, pos) & (1 << b) - 1, pos += b;
          }
          if (pos > tbts) {
            if (noSt)
              err(0);
            break;
          }
          if (resize)
            cbuf(bt + 131072);
          var end = bt + add;
          if (bt < dt) {
            var shift = dl - dt, dend = Math.min(dt, end);
            if (shift + bt < 0)
              err(3);
            for (; bt < dend; ++bt)
              buf[bt] = dict[shift + bt];
          }
          for (; bt < end; ++bt)
            buf[bt] = buf[bt - dt];
        }
      }
      st.l = lm, st.p = lpos, st.b = bt, st.f = final;
      if (lm)
        final = 1, st.m = lbt, st.d = dm, st.n = dbt;
    } while (!final);
    return bt != buf.length && noBuf ? slc(buf, 0, bt) : buf.subarray(0, bt);
  };
  var et = /* @__PURE__ */ new u8(0);
  var b2 = function(d, b) {
    return d[b] | d[b + 1] << 8;
  };
  var b4 = function(d, b) {
    return (d[b] | d[b + 1] << 8 | d[b + 2] << 16 | d[b + 3] << 24) >>> 0;
  };
  var b8 = function(d, b) {
    return b4(d, b) + b4(d, b + 4) * 4294967296;
  };
  function inflateSync(data, opts) {
    return inflt(data, { i: 2 }, opts && opts.out, opts && opts.dictionary);
  }
  var td = typeof TextDecoder != "undefined" && /* @__PURE__ */ new TextDecoder();
  var tds = 0;
  try {
    td.decode(et, { stream: true });
    tds = 1;
  } catch (e) {
  }
  var dutf8 = function(d) {
    for (var r = "", i2 = 0; ; ) {
      var c = d[i2++];
      var eb = (c > 127) + (c > 223) + (c > 239);
      if (i2 + eb > d.length)
        return { s: r, r: slc(d, i2 - 1) };
      if (!eb)
        r += String.fromCharCode(c);
      else if (eb == 3) {
        c = ((c & 15) << 18 | (d[i2++] & 63) << 12 | (d[i2++] & 63) << 6 | d[i2++] & 63) - 65536, r += String.fromCharCode(55296 | c >> 10, 56320 | c & 1023);
      } else if (eb & 1)
        r += String.fromCharCode((c & 31) << 6 | d[i2++] & 63);
      else
        r += String.fromCharCode((c & 15) << 12 | (d[i2++] & 63) << 6 | d[i2++] & 63);
    }
  };
  function strFromU8(dat, latin1) {
    if (latin1) {
      var r = "";
      for (var i2 = 0; i2 < dat.length; i2 += 16384)
        r += String.fromCharCode.apply(null, dat.subarray(i2, i2 + 16384));
      return r;
    } else if (td) {
      return td.decode(dat);
    } else {
      var _a2 = dutf8(dat), s = _a2.s, r = _a2.r;
      if (r.length)
        err(8);
      return s;
    }
  }
  var slzh = function(d, b) {
    return b + 30 + b2(d, b + 26) + b2(d, b + 28);
  };
  var zh = function(d, b, z) {
    var fnl = b2(d, b + 28), efl = b2(d, b + 30), fn = strFromU8(d.subarray(b + 46, b + 46 + fnl), !(b2(d, b + 8) & 2048)), es = b + 46 + fnl;
    var _a2 = z64hs(d, es, efl, z, b4(d, b + 20), b4(d, b + 24), b4(d, b + 42)), sc = _a2[0], su = _a2[1], off = _a2[2];
    return [b2(d, b + 10), sc, su, fn, es + efl + b2(d, b + 32), off];
  };
  var z64hs = function(d, b, l, z, sc, su, off) {
    var nsc = sc == 4294967295, nsu = su == 4294967295, noff = off == 4294967295, e = b + l;
    var nf = nsc + nsu + noff;
    if (z && nf) {
      for (; b + 4 < e; b += 4 + b2(d, b + 2)) {
        if (b2(d, b) == 1) {
          return [
            nsc ? b8(d, b + 4 + 8 * nsu) : sc,
            nsu ? b8(d, b + 4) : su,
            noff ? b8(d, b + 4 + 8 * (nsu + nsc)) : off,
            1
          ];
        }
      }
      if (z < 2)
        err(13);
    }
    return [sc, su, off, 0];
  };
  function unzipSync(data, opts) {
    var files = {};
    var e = data.length - 22;
    for (; b4(data, e) != 101010256; --e) {
      if (!e || data.length - e > 65558)
        err(13);
    }
    var c = b2(data, e + 8);
    if (!c)
      return {};
    var o = b4(data, e + 16);
    var z = b4(data, e - 20) == 117853008;
    if (z) {
      var ze = b4(data, e - 12);
      z = b4(data, ze) == 101075792;
      if (z) {
        c = b4(data, ze + 32);
        o = b4(data, ze + 48);
      }
    }
    for (var i2 = 0; i2 < c; ++i2) {
      var _a2 = zh(data, o, z), c_2 = _a2[0], sc = _a2[1], su = _a2[2], fn = _a2[3], no = _a2[4], off = _a2[5], b = slzh(data, off);
      o = no;
      {
        if (!c_2)
          files[fn] = slc(data, b, b + sc);
        else if (c_2 == 8)
          files[fn] = inflateSync(data.subarray(b, b + sc), { out: new u8(su) });
        else
          err(14, "unknown compression type " + c_2);
      }
    }
    return files;
  }
  function isElementVisible(el, view = window) {
    const rect = el.getBoundingClientRect();
    const computed = view.getComputedStyle(el);
    return rect.width > 1 && rect.height > 1 && computed.visibility !== "hidden" && computed.display !== "none";
  }
  function deepElementsFromPoint(sourceDocument, x2, y) {
    var _a2;
    const stack = typeof sourceDocument.elementsFromPoint === "function" ? Array.from(sourceDocument.elementsFromPoint(x2, y) || []) : [sourceDocument.elementFromPoint(x2, y)].filter((item) => !!item);
    for (const element of stack) {
      const FrameElement = (_a2 = sourceDocument.defaultView) == null ? void 0 : _a2.HTMLIFrameElement;
      if (!FrameElement || !(element instanceof FrameElement)) continue;
      const childDocument = sameOriginFrameDocument(element);
      if (!childDocument) continue;
      const rect = element.getBoundingClientRect();
      const childStack = deepElementsFromPoint(
        childDocument,
        x2 - rect.left - element.clientLeft,
        y - rect.top - element.clientTop
      );
      if (childStack.length) return [...childStack, ...stack];
    }
    return stack;
  }
  function sameOriginFrameDocument(frame) {
    try {
      return frame.contentDocument;
    } catch {
      return null;
    }
  }
  function cssPathForElement(el, rootBody, ignoredClassPrefixes = []) {
    const parts = [];
    let node = el;
    while (node && node.nodeType === 1 && node !== rootBody && parts.length < 6) {
      let part = node.tagName.toLowerCase();
      const classes = [...node.classList].filter((item) => !ignoredClassPrefixes.some((prefix) => item.startsWith(prefix))).slice(0, 2);
      if (classes.length) part += `.${classes.map((item) => CSS.escape(item)).join(".")}`;
      else if (node.id) part += `#${CSS.escape(node.id)}`;
      const parent = node.parentElement;
      if (parent && selectorPartNeedsNth(node, part)) {
        const sameTagSiblings = [...parent.children].filter((item) => item.tagName === node.tagName);
        part += `:nth-of-type(${sameTagSiblings.indexOf(node) + 1})`;
      }
      parts.unshift(part);
      node = node.parentElement;
    }
    return parts.join(" > ");
  }
  function selectorPartNeedsNth(node, part) {
    const parent = node.parentElement;
    if (!parent || node.id) return false;
    try {
      return parent.querySelectorAll(`:scope > ${part}`).length > 1;
    } catch {
      return false;
    }
  }
  function escapeHtml(value) {
    return String(value).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function escapeAttr(value) {
    return escapeHtml(value).replace(/'/g, "&#39;");
  }
  function compactText(value, limit = 80) {
    return String(value || "").replace(/\s+/g, " ").trim().slice(0, limit);
  }
  const LAYOUT_EFFECT_SOURCE_PROPS = [
    "width",
    "height",
    "padding",
    "paddingX",
    "paddingY",
    "paddingLeft",
    "paddingRight",
    "paddingTop",
    "paddingBottom",
    "fontSize",
    "lineHeight",
    "letterSpacing",
    "fontFamily",
    "fontWeight",
    "textContent"
  ];
  function isLayoutEffectSource(prop) {
    return LAYOUT_EFFECT_SOURCE_PROPS.includes(prop);
  }
  function controlIdForLayoutEffectSource(prop) {
    return {
      width: "dt-width",
      height: "dt-height",
      paddingLeft: "dt-padding-left",
      paddingRight: "dt-padding-right",
      paddingTop: "dt-padding-top",
      paddingBottom: "dt-padding-bottom"
    }[prop] || "";
  }
  function createExplicitLayoutValueController({
    values,
    getVisualSelection,
    getScope,
    resolveCurrentStyleRoute,
    cssPath
  }) {
    function keyFor(prop) {
      if (!getVisualSelection() || prop !== "width" && prop !== "height") return "";
      const route = resolveCurrentStyleRoute(prop);
      if (!route.targets.length) return "";
      return `${prop}|${route.targets.map((el) => cssPath(el)).join("|")}|${getScope()}`;
    }
    return {
      mark(prop, value) {
        const key = keyFor(prop);
        if (key) values.set(key, value);
      },
      value(prop) {
        const key = keyFor(prop);
        return key ? values.get(key) : void 0;
      },
      keyFor
    };
  }
  function scheduleLayoutSideEffectSync({
    requestFrame,
    hasSelected,
    getVisualSelection,
    getSelectedVisual,
    syncLayoutBoxControls,
    syncRangeControlFromRoute,
    scheduleOverlayRender
  }, activeId) {
    requestFrame(() => {
      requestFrame(() => {
        if (!hasSelected()) return;
        const visual = getVisualSelection() || getSelectedVisual();
        syncLayoutBoxControls(visual, { skipId: activeId });
        syncRangeControlFromRoute("dt-radius", "borderRadius", visual, 0);
        scheduleOverlayRender();
      });
    });
  }
  const PROPERTY_CONTROL_ORDER = [
    "text",
    "fontFamily",
    "fontSize",
    "lineHeight",
    "letterSpacing",
    "color",
    "backgroundColor",
    "borderColor",
    "borderRadius",
    "width",
    "height",
    "paddingLeft",
    "paddingRight",
    "paddingTop",
    "paddingBottom",
    "offsetX",
    "offsetY"
  ];
  function buildPropertyCapability({
    key,
    route,
    groupCapability,
    traits,
    isContentEditableTarget = () => false
  }) {
    const control = controlDefinition(key);
    switch (key) {
      case "text":
        return availabilityForTextContent(control, groupCapability, route, isContentEditableTarget);
      case "borderRadius": {
        const suitable = groupCapability.suitable && !traits.tableCell;
        return availabilityFromRoute(control, groupCapability, route, {
          suitable,
          reason: suitable ? "" : traits.tableCell ? "表格单元格不提供独立圆角配置。" : groupCapability.reason
        });
      }
      default:
        return availabilityFromRoute(control, groupCapability, route, {
          suitable: groupCapability.suitable,
          reason: groupCapability.reason
        });
    }
  }
  function buildCapabilityGroups(traits) {
    const content = !traits.replacedMedia && !traits.icon;
    const typography = !traits.replacedMedia;
    const appearance = traits.stableBox || traits.fragmentedInline;
    const size = traits.stableBox && !traits.directText && !traits.fragmentedInline && !traits.tableCell;
    const insetSpacing = traits.tableCell || traits.stableBox && !traits.directText && !traits.fragmentedInline && !traits.replacedMedia && !traits.icon && !traits.table;
    const position = traits.stableBox && !traits.directText && !traits.fragmentedInline && !traits.tableCell && !traits.table;
    return {
      content: capabilityGroup("content", content, "当前选区没有可编辑的文案目标。"),
      typography: capabilityGroup("typography", typography, "当前选区不承载可编辑文字样式。"),
      appearance: capabilityGroup("appearance", appearance, "当前选区没有稳定的外观承载盒。"),
      size: capabilityGroup("size", size, sizeReason(traits)),
      insetSpacing: capabilityGroup("insetSpacing", insetSpacing, insetSpacingReason(traits)),
      position: capabilityGroup("position", position, positionReason(traits))
    };
  }
  function capabilityGroup(key, suitable, reason) {
    return { key, suitable, reason: suitable ? "" : reason };
  }
  function controlDefinition(key) {
    const definitions = {
      text: { key, prop: "textContent", group: "content" },
      fontFamily: { key, prop: "fontFamily", group: "typography" },
      fontSize: { key, prop: "fontSize", group: "typography" },
      fontWeight: { key, prop: "fontWeight", group: "typography" },
      lineHeight: { key, prop: "lineHeight", group: "typography" },
      letterSpacing: { key, prop: "letterSpacing", group: "typography" },
      color: { key, prop: "color", group: "typography" },
      backgroundColor: { key, prop: "backgroundColor", group: "appearance" },
      borderColor: { key, prop: "borderColor", group: "appearance" },
      borderRadius: { key, prop: "borderRadius", group: "appearance" },
      padding: { key, prop: "padding", group: "insetSpacing" },
      paddingX: { key, prop: "paddingX", group: "insetSpacing" },
      paddingY: { key, prop: "paddingY", group: "insetSpacing" },
      paddingLeft: { key, prop: "paddingLeft", group: "insetSpacing" },
      paddingRight: { key, prop: "paddingRight", group: "insetSpacing" },
      paddingTop: { key, prop: "paddingTop", group: "insetSpacing" },
      paddingBottom: { key, prop: "paddingBottom", group: "insetSpacing" },
      width: { key, prop: "width", group: "size" },
      height: { key, prop: "height", group: "size" },
      offsetX: { key, prop: "offsetX", group: "position" },
      offsetY: { key, prop: "offsetY", group: "position" }
    };
    return definitions[key] || { key, prop: key, group: "appearance" };
  }
  function propertyGroup(key) {
    return controlDefinition(key).group;
  }
  function isPaddingSideProp(prop) {
    return prop === "paddingLeft" || prop === "paddingRight" || prop === "paddingTop" || prop === "paddingBottom";
  }
  function availabilityForTextContent(control, groupCapability, route, isContentEditableTarget) {
    const targets = route.targets || [];
    const suitable = groupCapability.suitable;
    const enabled = suitable && !!route.visible && targets.length >= 1 && targets.every(isContentEditableTarget);
    return buildAvailability(control, groupCapability, route, {
      enabled,
      show: suitable,
      reason: enabled ? "" : route.reason || "该选区包含多段文字，请点选具体文字后编辑。"
    });
  }
  function availabilityFromRoute(control, groupCapability, route, options = {}) {
    const targets = route.targets || [];
    const suitable = options.suitable !== false;
    const enabled = suitable && !!route.visible && targets.length > 0;
    return buildAvailability(control, groupCapability, route, {
      enabled,
      show: suitable,
      reason: enabled ? "" : route.reason || options.reason || groupCapability.reason
    });
  }
  function buildAvailability(control, groupCapability, route, options = {}) {
    const enabled = !!options.enabled;
    return {
      key: control.key,
      prop: control.prop,
      group: control.group,
      groupCapability,
      show: options.show !== false,
      enabled,
      targets: route.targets || [],
      route,
      reason: enabled ? "" : options.reason || route.reason || groupCapability.reason || "当前选区不适合该配置。"
    };
  }
  function sizeReason(traits) {
    if (traits.tableCell) return "表格单元格尺寸由行列和整表布局共同决定。";
    if (traits.directText || traits.fragmentedInline) return "当前文字范围不是独立的尺寸责任层。";
    return "当前选区没有稳定的尺寸责任层。";
  }
  function insetSpacingReason(traits) {
    if (traits.table) return "表格对象不把单元格 padding 视为自身留白。";
    if (traits.replacedMedia || traits.icon) return "当前对象不承载内部内容留白。";
    if (traits.directText || traits.fragmentedInline) return "当前文字范围不承载内部内容留白。";
    return "当前选区没有稳定的内间距责任层。";
  }
  function positionReason(traits) {
    if (traits.table || traits.tableCell) return "表格位置由表格布局共同决定。";
    if (traits.directText || traits.fragmentedInline) return "当前文字范围不是独立的位置责任层。";
    return "当前选区没有稳定的位置责任层。";
  }
  function rectArea(rect) {
    return Math.max(0, rect.width || 0) * Math.max(0, rect.height || 0);
  }
  function rectOverlapRatio(a, b) {
    const left = Math.max(a.left, b.left);
    const right = Math.min(a.right, b.right);
    const top = Math.max(a.top, b.top);
    const bottom = Math.min(a.bottom, b.bottom);
    const overlap = Math.max(0, right - left) * Math.max(0, bottom - top);
    return overlap / Math.max(1, Math.min(rectArea(a), rectArea(b)));
  }
  function roundedRect(rect) {
    return {
      x: Math.round(rect.x),
      y: Math.round(rect.y),
      width: Math.round(rect.width),
      height: Math.round(rect.height)
    };
  }
  function cleanRuntimeArtifactsForExport(sourceDocument) {
    const clone = sourceDocument.cloneNode(true);
    clone.querySelectorAll("#dt-freeze-runtime-style,#dt-hover-lock-style,#dt-hover-freeze-style,#dt-mark-layer,#dt-freeze-bridge-script,#dt-input-shield").forEach((el) => el.remove());
    clone.querySelectorAll(".dt-mark-box").forEach((el) => el.remove());
    clone.querySelectorAll("*").forEach((el) => {
      el.removeAttribute("data-vibepolish-cdp-probe-id");
      [...el.classList].forEach((className) => {
        if (/^(dt-picked|dt-group|dt-hover-hot|dt-force-hover|dt-force-focus|dt-force-paused|dt-hover-edit-|dt-interaction-frozen)/.test(className)) {
          el.classList.remove(className);
        }
      });
    });
    return clone;
  }
  const AI_PATCH_INSTRUCTION = "请在当前代码库中实现 changes。target.locatorHint 仅用于识别应受影响的页面元素，不代表必须创建或修改同名 CSS selector；请结合源码选择最合适的实现，不得扩大 target.count 表达的影响范围。完成后验证刷新仍生效、非目标不变，并说明修改文件和验证结果。";
  function buildVisualEditPatchPayload(sourceName, edits) {
    return {
      format: "vibepolish-ai-patch/v1",
      source: sourceName,
      instruction: AI_PATCH_INSTRUCTION,
      changes: compactAiEdits(edits)
    };
  }
  function buildVisualEditPrompt(sourceName, edits) {
    const changes = compactAiEdits(edits);
    const lines = [
      "请在当前代码库中完成以下视觉修改。",
      "",
      `来源：${sourceName}`,
      "",
      "修改清单："
    ];
    if (!changes.length) lines.push("- 暂无修改。");
    changes.forEach((change, index) => {
      var _a2, _b2;
      const documentPaths = targetDocumentPaths(change.target);
      if (documentPaths.length) lines.push(`${index + 1}. 页面：${documentPaths.join(" / ")}`);
      lines.push(`${documentPaths.length ? "   " : `${index + 1}. `}目标：${((_a2 = change.target) == null ? void 0 : _a2.locatorHint) || "当前选区"}（${((_b2 = change.target) == null ? void 0 : _b2.count) || 1} 个）`);
      if (change.pseudo) lines.push(`   状态：${change.pseudo}`);
      if (change.replaceText) {
        lines.push(`   文案：${readableValue(change.replaceText.from)} -> ${readableValue(change.replaceText.to)}`);
      }
      Object.entries(change.set || {}).forEach(([property, value]) => {
        lines.push(`   ${property}: ${readableValue(value)}`);
      });
    });
    lines.push(
      "",
      "实现要求：",
      "- 目标定位仅用于识别应受影响的页面元素，不要求创建或修改同名 CSS selector。",
      "- 请结合现有源码选择最合适的实现，不要扩大标注的影响范围。",
      "- 完成后验证刷新仍然生效、非目标元素保持不变，并说明修改文件和验证结果。"
    );
    return lines.join("\n");
  }
  function readableValue(value) {
    if (Array.isArray(value)) return value.map((item) => String(item)).join(" / ");
    const text = String(value ?? "");
    return text || "空";
  }
  function targetDocumentPaths(target) {
    return uniqueValues([
      ...Array.isArray(target == null ? void 0 : target.documentPaths) ? target.documentPaths : [],
      (target == null ? void 0 : target.documentPath) || ""
    ].filter(Boolean));
  }
  function compactAiEdits(edits) {
    const latest = /* @__PURE__ */ new Map();
    edits.forEach((edit, index) => {
      const key = `${aiEditContextKey(edit)}::${edit.kind || ""}`;
      latest.set(key, { edit, index });
    });
    const groups = /* @__PURE__ */ new Map();
    [...latest.values()].sort((a, b) => a.index - b.index).forEach(({ edit, index }) => {
      const key = aiEditContextKey(edit);
      const group = groups.get(key) || { edits: [], index };
      group.edits.push(edit);
      groups.set(key, group);
    });
    return [...groups.values()].sort((a, b) => a.index - b.index).map(({ edits: groupedEdits }) => compactAiEditGroup(groupedEdits));
  }
  function compactAiEditGroup(edits) {
    const edit = edits[edits.length - 1] || {};
    if (edit.kind === "textContent") return compactTextChange(edit);
    const locatorHint = locatorHintForEdit(edit);
    const count = edit.count || uniqueValues(edit.appliedTargets || []).length || 1;
    const result = {
      target: compactTarget(edit, locatorHint, count),
      set: {}
    };
    const pseudo = pseudoFromEdit(edit);
    if (pseudo) result.pseudo = pseudo;
    edits.forEach((item) => {
      result.set[cssPropertyFromEdit(item)] = item.value;
    });
    return result;
  }
  function compactTextChange(edit) {
    const count = edit.count || uniqueValues(edit.appliedTargets || []).length || 1;
    const before = uniqueValues((edit.before || []).filter((value) => value != null));
    return {
      target: compactTarget(edit, locatorHintForEdit(edit), count),
      replaceText: {
        from: before.length === 1 ? before[0] : before,
        to: edit.value
      }
    };
  }
  function compactTarget(edit, locatorHint, count) {
    const documentPaths = uniqueValues(edit.documentPaths || []);
    const target = { locatorHint, count };
    if (documentPaths.length === 1) target.documentPath = documentPaths[0];
    if (documentPaths.length > 1) target.documentPaths = documentPaths;
    return target;
  }
  function cssPropertyFromEdit(edit) {
    const property = edit.kind && edit.kind.startsWith("hover.") ? toCssProp(edit.kind.replace(/^hover\./, "")) : toCssProp(edit.kind);
    return property;
  }
  function pseudoFromEdit(edit) {
    var _a2;
    if (edit.kind && edit.kind.startsWith("hover.")) return ":hover";
    const selector = String(((_a2 = edit.stateCondition) == null ? void 0 : _a2.selector) || "").trim();
    return selector.startsWith(":") ? selector : "";
  }
  function aiEditContextKey(edit) {
    return [
      edit.kind === "textContent" ? "text" : "style",
      pseudoFromEdit(edit),
      edit.cssSelector || "",
      edit.route || "",
      edit.scope || "",
      edit.target || "",
      uniqueValues(edit.documentPaths || []).join("|"),
      uniqueValues(edit.sourcePaths || []).join("|"),
      uniqueValues(edit.appliedTargets || []).join("|")
    ].join("::");
  }
  function locatorHintForEdit(edit) {
    const selector = String(edit.cssSelector || "").trim();
    if (selector) {
      const pseudo = pseudoFromEdit(edit);
      return pseudo ? selector.split(",").map((part) => part.split(pseudo).join("").trim()).join(",") : selector;
    }
    const refs = Array.isArray(edit.refs) ? edit.refs.filter(Boolean) : [];
    const common = commonElementLocatorHint(refs);
    if (common) return common;
    return String(edit.target || uniqueValues(edit.appliedTargets || [])[0] || "").trim();
  }
  function commonElementLocatorHint(elements) {
    if (!elements.length) return "";
    if (elements.length === 1 && elements[0].id) return `#${elements[0].id}`;
    const tagNames = uniqueValues(elements.map((element) => element.tagName.toLowerCase()));
    const tag = tagNames.length === 1 ? tagNames[0] : "";
    const commonClasses = [...elements[0].classList].filter(
      (className) => !className.startsWith("dt-") && /^-?[_a-zA-Z]+[\w-]*$/.test(className) && elements.every((element) => element.classList.contains(className))
    );
    if (commonClasses.length) return `${tag}${commonClasses.slice(0, 2).map((className) => `.${className}`).join("")}`;
    return tag;
  }
  function compactStateCondition(condition) {
    if (!condition) return null;
    return {
      selector: condition.selector || null,
      source: condition.source || null,
      confidence: condition.confidence || null
    };
  }
  function uniqueValues(values) {
    return [...new Set((values || []).map((value) => String(value)))];
  }
  const BRIDGE_ID = "dt-export-test-bridge";
  function setupRuntimeTestBridge(root = document) {
    if (root.getElementById(BRIDGE_ID)) return;
    const box = root.createElement("div");
    box.id = BRIDGE_ID;
    box.hidden = true;
    box.innerHTML = [
      '<textarea id="dt-test-selection"></textarea>',
      '<textarea id="dt-test-ai-patch"></textarea>',
      '<textarea id="dt-test-html"></textarea>',
      '<textarea id="dt-test-meta"></textarea>'
    ].join("");
    root.body.appendChild(box);
  }
  function refreshRuntimeTestBridge(payload, root = document) {
    writeBridgeValue(root, "dt-test-selection", payload.selection);
    writeBridgeValue(root, "dt-test-ai-patch", payload.aiPatch);
    writeBridgeValue(root, "dt-test-html", payload.html);
    writeBridgeValue(root, "dt-test-meta", payload.meta);
  }
  function writeBridgeValue(root, id, value) {
    const node = root.getElementById(id);
    if (node) node.value = value;
  }
  function createRuntimeFeedback(root = document, nav = navigator) {
    let toastTimer = null;
    const toast = (text) => {
      const node = root.querySelector("#dt-toast");
      if (!node) return;
      node.textContent = text;
      node.classList.add("dt-show");
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => node.classList.remove("dt-show"), 1800);
    };
    const fallbackCopyText = (text) => {
      const input = root.createElement("textarea");
      input.value = text;
      input.style.position = "fixed";
      input.style.left = "-9999px";
      root.body.appendChild(input);
      input.select();
      try {
        root.execCommand("copy");
        toast("已复制。");
      } catch {
        toast("复制失败，请手动复制。");
      }
      input.remove();
    };
    return {
      setStatus(text) {
        const node = root.querySelector("#dt-status");
        if (node) node.textContent = text;
      },
      toast,
      copyText(text) {
        var _a2;
        const value = String(text || "");
        if (!value) return;
        if ((_a2 = nav.clipboard) == null ? void 0 : _a2.writeText) {
          nav.clipboard.writeText(value).then(() => toast("已复制。")).catch(() => fallbackCopyText(value));
          return;
        }
        fallbackCopyText(value);
      }
    };
  }
  const STRUCTURE_SIMILAR_THRESHOLD = 0.68;
  const PARENT_SIMILAR_THRESHOLD = 0.62;
  const CORE_VISUAL_PROPERTIES = [
    "backgroundColor",
    "backgroundImage",
    "borderTopColor",
    "borderRightColor",
    "borderBottomColor",
    "borderLeftColor",
    "borderTopStyle",
    "borderRightStyle",
    "borderBottomStyle",
    "borderLeftStyle",
    "borderTopWidth",
    "borderRightWidth",
    "borderBottomWidth",
    "borderLeftWidth",
    "borderRadius",
    "boxShadow",
    "opacity",
    "color",
    "fontFamily",
    "fontSize",
    "fontWeight",
    "lineHeight",
    "letterSpacing",
    "textAlign"
  ];
  const CLASSIFICATION_ANCHOR_PROPS = [
    "backgroundColor",
    "borderTopColor",
    "borderTopWidth",
    "borderTopStyle",
    "borderRadius",
    "boxShadow",
    "color",
    "fontFamily",
    "fontSize",
    "fontWeight",
    "paddingTop",
    "display"
  ];
  function createSelectionPlan(input) {
    const breadth = input.breadth || "similar-kind";
    const parentScope = input.parentScope || "all-similar-parents";
    const fallbackReasons = [];
    const rootElement = rootAsElement(input.root);
    const discovery = findCurrentParent(input.selectionOwner);
    const fixedUniverse = visibleElements(input.fixedUniverse || []);
    const similarParents = visibleElements(fixedUniverse.length ? fixedUniverse : findSimilarParents(rootElement, discovery.currentParent));
    const stableSimilarParents = similarParents.length > 0;
    const targetParents = parentScope === "all-similar-parents" && stableSimilarParents ? similarParents : [discovery.currentParent];
    if (parentScope === "all-similar-parents" && !stableSimilarParents) {
      fallbackReasons.push("similar parents were not stable; downgraded parentScope to current-parent");
    }
    const ownerRelativePath = relativeChildPath(discovery.itemInParent, input.selectionOwner);
    const structuralItems = visibleElements(input.candidateScope || collectStructuralItems(targetParents, discovery, input.selectionOwner, ownerRelativePath));
    if (breadth !== "single" && structuralItems.length <= 1) {
      fallbackReasons.push("similar structural items were not stable; breadth effectively downgraded to single");
    }
    const propertyTargets = visibleElements(resolvePropertyTarget(input.selectionOwner, input.property, input.propertyTargetResolver).targets);
    const pseudoKind = pseudoKindFromState(input.stateContext || null);
    const visualItems = pseudoKind ? structuralItems : breadth === "single" ? [input.selectionOwner] : structuralItems;
    const visualGroups = buildVisualGroups(visualItems, input.cdpStyleInfo || null);
    const diffVisualProps = uniqueStrings(visualGroups.flatMap((group) => diffPropsForGroup(group, visualGroups)));
    const currentVisualGroup = visualGroups.find((group) => group.items.includes(input.selectionOwner)) || visualGroups[0] || {
      id: "group-0",
      items: [input.selectionOwner],
      signature: coreVisualSignature(input.selectionOwner, void 0, input.cdpStyleInfo || null),
      diffProps: [],
      fallbackReasons: []
    };
    for (const group of visualGroups) {
      group.diffProps = diffPropsForGroup(group, visualGroups);
      const classification = findClassificationSelector({
        group,
        allGroups: visualGroups,
        scopes: targetParents,
        cdpStyleInfo: input.cdpStyleInfo || null,
        stateContext: pseudoKind ? null : input.stateContext || null,
        breadth
      });
      group.classificationSelector = classification.selector;
      group.classificationSelectorMode = classification.mode;
      group.classificationVerification = classification.verification;
      group.fallbackReasons.push(...classification.fallbackReasons);
    }
    const breadthTargetGroups = breadth === "single" ? [singleTargetGroup(input.selectionOwner, currentVisualGroup)] : breadth === "all-kind" ? visualGroups : [currentVisualGroup];
    const pseudoRuleInfoByItem = pseudoKind ? inspectPseudoRules({
      items: visualItems,
      property: input.property,
      stateContext: input.stateContext || null,
      cdpStyleInfo: input.cdpStyleInfo || null,
      propertyTargetResolver: input.propertyTargetResolver,
      pseudoKind
    }) : [];
    const targetGroups = pseudoKind ? filterGroupsByPseudoAvailability(breadthTargetGroups, pseudoRuleInfoByItem) : breadthTargetGroups;
    const excludedItems = pseudoKind ? pseudoRuleInfoByItem.filter((info) => !info.rule).map((info) => info.item) : [];
    if (pseudoKind && !input.cdpStyleInfo) fallbackReasons.push("pseudo branch is waiting for CDP rule inspection");
    if (pseudoKind && !targetGroups.length) fallbackReasons.push("no existing pseudo rule matched this selection/property");
    const writePlans = targetGroups.flatMap(
      (group) => buildWritePlans({
        group,
        property: input.property,
        value: input.value,
        cdpStyleInfo: input.cdpStyleInfo || null,
        stateContext: input.stateContext || null,
        scopes: targetParents,
        propertyTargetResolver: input.propertyTargetResolver,
        pseudoOnly: !!pseudoKind,
        breadth
      })
    );
    return {
      selectionOwner: input.selectionOwner,
      propertyTargets,
      property: input.property,
      value: input.value,
      breadth,
      parentScope: stableSimilarParents ? parentScope : "current-parent",
      pseudoKind: pseudoKind || null,
      cdpStatus: input.cdpStyleInfo ? "ready" : "loading",
      currentParent: discovery.currentParent,
      currentParentSimilarItems: visibleElements(discovery.currentParentSimilarItems),
      similarParents,
      targetParents,
      structuralItems,
      allKindItems: structuralItems,
      diffVisualProps,
      excludedItems,
      pseudoRuleInfoByItem,
      visualGroups,
      currentVisualGroup,
      targetGroups,
      writePlans,
      generatedCssRules: writePlans.map((plan) => plan.generatedRule).filter(Boolean),
      fallbackReasons,
      verificationResults: visualGroups.map((group) => group.classificationVerification).filter(Boolean)
    };
  }
  function retargetSelectionPlanProperty(plan, property, value, propertyTargetResolver) {
    const propertyTargets = visibleElements(resolvePropertyTarget(plan.selectionOwner, property, propertyTargetResolver).targets);
    const pseudoOnly = !!plan.pseudoKind;
    const breadthTargetGroups = plan.breadth === "single" ? [singleTargetGroup(plan.selectionOwner, plan.currentVisualGroup)] : plan.breadth === "all-kind" ? plan.visualGroups : [plan.currentVisualGroup];
    const pseudoRuleInfoByItem = pseudoOnly ? inspectPseudoRules({
      items: plan.structuralItems || [],
      property,
      stateContext: plan.stateContext || null,
      cdpStyleInfo: plan.cdpStyleInfo || null,
      propertyTargetResolver,
      pseudoKind: plan.pseudoKind || ""
    }) : [];
    const targetGroups = pseudoOnly ? filterGroupsByPseudoAvailability(breadthTargetGroups, pseudoRuleInfoByItem) : breadthTargetGroups;
    const writePlans = targetGroups.flatMap(
      (group) => buildWritePlans({
        group,
        property,
        value,
        cdpStyleInfo: plan.cdpStyleInfo || null,
        stateContext: plan.stateContext || null,
        scopes: plan.targetParents || [],
        propertyTargetResolver,
        pseudoOnly,
        breadth: plan.breadth
      })
    );
    return {
      ...plan,
      propertyTargets,
      property,
      value,
      targetGroups,
      excludedItems: pseudoOnly ? pseudoRuleInfoByItem.filter((info) => !info.rule).map((info) => info.item) : plan.excludedItems,
      pseudoRuleInfoByItem: pseudoOnly ? pseudoRuleInfoByItem : plan.pseudoRuleInfoByItem,
      writePlans,
      generatedCssRules: writePlans.map((item) => item.generatedRule).filter(Boolean)
    };
  }
  function inspectPseudoRules({
    items,
    property,
    stateContext,
    cdpStyleInfo,
    propertyTargetResolver,
    pseudoKind
  }) {
    const pseudoSelector = pseudoSelectorForState(stateContext, pseudoKind);
    return items.map((item) => {
      var _a2;
      const target = resolvePropertyTarget(item, property, propertyTargetResolver).targets[0] || null;
      const rule = target ? ((_a2 = cdpStyleInfo == null ? void 0 : cdpStyleInfo.getWinningRule) == null ? void 0 : _a2.call(cdpStyleInfo, target, property, stateContext)) || null : null;
      const accepted = target && rule && rule.targetIdentityVerified === true && !rule.isInline && selectorHasPseudo(rule.selector, pseudoSelector);
      return {
        item,
        target: target || item,
        rule: accepted ? rule : null,
        reason: accepted ? "" : target ? "no-existing-pseudo-rule" : "no-property-target"
      };
    });
  }
  function filterGroupsByPseudoAvailability(groups, ruleInfo) {
    const editable = new Set(ruleInfo.filter((info) => info.rule).map((info) => info.item));
    return groups.map((group) => ({ ...group, items: group.items.filter((item) => editable.has(item)) })).filter((group) => group.items.length > 0);
  }
  function rootAsElement(root) {
    return root instanceof Document ? root.documentElement : root;
  }
  function resolvePropertyTarget(owner, property, resolver) {
    if (!resolver) return { kind: "self", targets: [owner] };
    const resolved = resolver(owner, property);
    return {
      kind: (resolved == null ? void 0 : resolved.kind) || "self",
      targets: uniqueElements((resolved == null ? void 0 : resolved.targets) || []),
      reason: (resolved == null ? void 0 : resolved.reason) || ""
    };
  }
  function findCurrentParent(selectionOwner) {
    let ancestor = selectionOwner.parentElement;
    while (ancestor) {
      const item2 = directChildContaining(ancestor, selectionOwner);
      if (item2) {
        const similar = Array.from(ancestor.children).filter((child) => structureSimilarity(child, item2) >= STRUCTURE_SIMILAR_THRESHOLD);
        if (similar.length >= 2) {
          return {
            currentParent: ancestor,
            itemInParent: item2,
            currentParentSimilarItems: similar
          };
        }
      }
      ancestor = ancestor.parentElement;
    }
    const parent = selectionOwner.parentElement || selectionOwner;
    const item = directChildContaining(parent, selectionOwner) || selectionOwner;
    return {
      currentParent: parent,
      itemInParent: item,
      currentParentSimilarItems: [item]
    };
  }
  function directChildContaining(parent, target) {
    return Array.from(parent.children).find((child) => child === target || child.contains(target)) || null;
  }
  function findSimilarParents(root, currentParent) {
    const tag = currentParent.tagName.toLowerCase();
    const candidates = Array.from(root.querySelectorAll(tag));
    const matches = candidates.filter((candidate) => structureSimilarity(candidate, currentParent) >= PARENT_SIMILAR_THRESHOLD);
    if (!matches.includes(currentParent)) matches.unshift(currentParent);
    return uniqueElements(matches);
  }
  function collectStructuralItems(targetParents, discovery, selectionOwner, ownerRelativePath) {
    const targets = [];
    for (const parent of targetParents) {
      const similarItems = Array.from(parent.children).filter(
        (child) => structureSimilarity(child, discovery.itemInParent) >= STRUCTURE_SIMILAR_THRESHOLD
      );
      const items = similarItems.length ? similarItems : [directChildContaining(parent, selectionOwner)].filter(Boolean);
      for (const item of items) {
        const target = resolveRelativePath(item, ownerRelativePath) || bestSimilarDescendant(item, selectionOwner);
        if (target) targets.push(target);
      }
    }
    return uniqueElements(targets);
  }
  function relativeChildPath(base, target) {
    const path = [];
    let node = target;
    while (node && node !== base) {
      const parent = node.parentElement;
      if (!parent) return [];
      path.unshift(Array.from(parent.children).indexOf(node));
      node = parent;
    }
    return node === base ? path : [];
  }
  function resolveRelativePath(base, path) {
    let node = base;
    for (const index of path) {
      node = (node == null ? void 0 : node.children[index]) || null;
      if (!node) return null;
    }
    return node;
  }
  function bestSimilarDescendant(root, sample) {
    const candidates = [root, ...Array.from(root.querySelectorAll(sample.tagName.toLowerCase()))];
    let best = null;
    let bestScore = 0;
    for (const candidate of candidates) {
      const score = structureSimilarity(candidate, sample);
      if (score > bestScore) {
        best = candidate;
        bestScore = score;
      }
    }
    return bestScore >= STRUCTURE_SIMILAR_THRESHOLD ? best : null;
  }
  function buildVisualGroups(items, cdpStyleInfo) {
    const buckets = /* @__PURE__ */ new Map();
    for (const item of items) {
      const signature = coreVisualSignature(item, void 0, cdpStyleInfo);
      const current = buckets.get(signature.key) || [];
      current.push(item);
      buckets.set(signature.key, current);
    }
    return Array.from(buckets.entries()).map(([key, groupItems], index) => ({
      id: `visual-${index}`,
      items: groupItems,
      signature: coreVisualSignature(groupItems[0], key, cdpStyleInfo),
      diffProps: [],
      fallbackReasons: []
    }));
  }
  function singleTargetGroup(item, source) {
    return {
      ...source,
      id: "single",
      items: [item],
      fallbackReasons: [...source.fallbackReasons || []]
    };
  }
  function coreVisualSignature(element, knownKey, cdpStyleInfo = null) {
    var _a2, _b2;
    const styles = (_a2 = element.ownerDocument.defaultView) == null ? void 0 : _a2.getComputedStyle(element);
    const props = {};
    if (!styles) return { key: knownKey || "", props };
    for (const prop of CORE_VISUAL_PROPERTIES) {
      const baseValue = (_b2 = cdpStyleInfo == null ? void 0 : cdpStyleInfo.getBaseVisualValue) == null ? void 0 : _b2.call(cdpStyleInfo, element, prop);
      props[prop] = baseValue == null ? effectiveVisualValue(styles, prop) : normalizeCssValue(baseValue);
    }
    const key = knownKey || CORE_VISUAL_PROPERTIES.map((prop) => `${prop}:${props[prop]}`).join("|");
    return { key, props };
  }
  function effectiveVisualValue(styles, prop) {
    const side = borderSideForProperty(prop);
    if (side) {
      const style = normalizeCssValue(styles.getPropertyValue(`border-${side}-style`));
      const width = normalizeCssValue(styles.getPropertyValue(`border-${side}-width`));
      if (style === "none" || style === "hidden" || parseFloat(width) === 0) {
        if (prop.endsWith("Style")) return "none";
        if (prop.endsWith("Width")) return "0px";
        return "transparent";
      }
    }
    return normalizeCssValue(styles.getPropertyValue(kebab(prop)));
  }
  function borderSideForProperty(prop) {
    const match = /^border(Top|Right|Bottom|Left)(Color|Style|Width)$/.exec(prop);
    return match ? match[1].toLowerCase() : "";
  }
  function diffPropsForGroup(group, groups) {
    const diff = /* @__PURE__ */ new Set();
    for (const prop of CORE_VISUAL_PROPERTIES) {
      const own = group.signature.props[prop];
      if (groups.some((other) => other !== group && other.signature.props[prop] !== own)) {
        diff.add(prop);
      }
    }
    return Array.from(diff);
  }
  function pseudoKindFromState(state) {
    const kind = String((state == null ? void 0 : state.kind) || "").toLowerCase();
    return ["hover", "focus"].includes(kind) ? kind : "";
  }
  function pseudoSelectorForKind(kind) {
    if (kind === "hover") return ":hover";
    if (kind === "focus") return ":focus";
    if (kind === "checked") return ":checked";
    if (kind === "aria-selected") return '[aria-selected="true"]';
    if (kind === "aria-pressed") return '[aria-pressed="true"]';
    return "";
  }
  function pseudoSelectorForState(state, kind = pseudoKindFromState(state)) {
    return (state == null ? void 0 : state.selector) || pseudoSelectorForKind(kind);
  }
  function selectorHasPseudo(selector, pseudoSelector) {
    return !!pseudoSelector && splitSelectorText(selector).some((part) => part.includes(pseudoSelector));
  }
  function splitSelectorText(selector) {
    const branches = [];
    let current = "";
    let roundDepth = 0;
    let squareDepth = 0;
    let quote = "";
    for (const char of String(selector || "")) {
      if (quote) {
        current += char;
        if (char === quote) quote = "";
        continue;
      }
      if (char === '"' || char === "'") {
        quote = char;
        current += char;
        continue;
      }
      if (char === "(") roundDepth += 1;
      else if (char === ")") roundDepth = Math.max(0, roundDepth - 1);
      else if (char === "[") squareDepth += 1;
      else if (char === "]") squareDepth = Math.max(0, squareDepth - 1);
      if (char === "," && roundDepth === 0 && squareDepth === 0) {
        if (current.trim()) branches.push(current.trim());
        current = "";
        continue;
      }
      current += char;
    }
    if (current.trim()) branches.push(current.trim());
    return branches;
  }
  function structureSimilarity(a, b) {
    const scores = [
      a.tagName === b.tagName ? 1 : 0,
      jaccard(classList(a), classList(b)),
      attributeShapeSimilarity(a, b),
      childOutlineSimilarity(a, b),
      layoutSimilarity(a, b)
    ];
    return weightedAverage(scores, [0.24, 0.24, 0.16, 0.24, 0.12]);
  }
  function attributeShapeSimilarity(a, b) {
    const attrs = ["role", "aria-label", "aria-selected", "aria-pressed"];
    const aKeys = attrs.filter((name) => a.hasAttribute(name)).concat(dataAttributeNames(a));
    const bKeys = attrs.filter((name) => b.hasAttribute(name)).concat(dataAttributeNames(b));
    return jaccard(aKeys, bKeys);
  }
  function childOutlineSimilarity(a, b) {
    const outlineA = childOutline(a);
    const outlineB = childOutline(b);
    return jaccard(outlineA, outlineB);
  }
  function childOutline(element) {
    return Array.from(element.children).slice(0, 12).map((child) => {
      const classes = classList(child).slice(0, 3).join(".");
      return `${child.tagName.toLowerCase()}${classes ? `.${classes}` : ""}:${Math.min(child.children.length, 6)}`;
    });
  }
  function layoutSimilarity(a, b) {
    const win = a.ownerDocument.defaultView;
    if (!win) return 0.5;
    const as = win.getComputedStyle(a);
    const bs = win.getComputedStyle(b);
    const props = ["display", "position", "flexDirection", "alignItems", "justifyContent", "gridTemplateColumns"];
    const equal = props.filter((prop) => normalizeCssValue(as.getPropertyValue(kebab(prop))) === normalizeCssValue(bs.getPropertyValue(kebab(prop)))).length;
    return equal / props.length;
  }
  function findClassificationSelector({
    group,
    allGroups,
    scopes,
    cdpStyleInfo,
    stateContext,
    breadth
  }) {
    const fallbackReasons = [];
    const bareTag = tagName(group.items[0]);
    const structuralItems = uniqueElements(allGroups.flatMap((item) => item.items));
    const structuralBases = structuralBaseSelectorCandidates(structuralItems);
    const primitiveCandidates = uniqueStrings([
      ...winningSelectorCandidates(group, cdpStyleInfo, stateContext),
      ...classSelectorCandidates(group.items),
      ...attributeSelectorCandidates(group.items)
    ]).filter(selectorHasPersistentIdentity);
    const groupDiscriminators = primitiveCandidates.filter(
      (selector2) => selectorLooksSameElement(selector2) && selectorMatchesEveryTarget(selector2, group.items) && structuralItems.some((item) => !elementMatchesSelector(item, selector2))
    );
    const baseAwareCandidates = structuralBases.flatMap(
      (base) => groupDiscriminators.map((discriminator) => intersectStructuralBase(base, discriminator))
    );
    const negativeCandidates = negativeSelectorCandidates(group, allGroups, structuralBases);
    const candidates = uniqueStrings([
      ...baseAwareCandidates,
      ...negativeCandidates,
      ...primitiveCandidates,
      ...selectorIntersectionCandidates(primitiveCandidates)
    ]);
    for (const selector2 of candidates) {
      const verification2 = verifySelectorTargetSet({ selector: selector2, scopes, expected: group.items, breadth, queryDomain: "scopes" });
      if (verification2.ok) {
        return { selector: selector2, mode: "classification", verification: verification2, fallbackReasons };
      }
    }
    for (const selector2 of scopedSelectorCandidates([...candidates, bareTag], scopes).filter(selectorHasPersistentIdentity)) {
      const verification2 = verifySelectorTargetSet({ selector: selector2, scopes, expected: group.items, breadth, queryDomain: "scopes" });
      if (verification2.ok) {
        return { selector: selector2, mode: "structure-narrow", verification: verification2, fallbackReasons };
      }
    }
    const nth = nthFallbackSelector(group.items, scopes, { preferSharedParent: breadth === "single" });
    if (nth) {
      const verification2 = verifySelectorTargetSet({
        selector: nth,
        scopes,
        expected: group.items,
        breadth,
        queryDomain: nth.includes(":scope") ? "scopes" : "document"
      });
      if (verification2.ok) {
        fallbackReasons.push("classification required nth fallback because stable selectors did not uniquely match the visual group");
        return { selector: nth, mode: "nth-fallback", verification: verification2, fallbackReasons };
      }
    }
    const selector = bareTag;
    const verification = verifySelectorTargetSet({ selector, scopes, expected: group.items, breadth, queryDomain: "scopes" });
    fallbackReasons.push("classification selector could not be verified; group is not safely persistable");
    return { selector, mode: "unverified", verification, fallbackReasons };
  }
  function selectorIntersectionCandidates(candidates) {
    const sameElement = candidates.filter(selectorLooksSameElement);
    const intersections = [];
    for (let leftIndex = 0; leftIndex < sameElement.length; leftIndex += 1) {
      for (let rightIndex = leftIndex + 1; rightIndex < sameElement.length; rightIndex += 1) {
        const left = sameElement[leftIndex];
        const right = sameElement[rightIndex];
        if (selectorContains(left, right) || selectorContains(right, left)) continue;
        intersections.push(`${left}:where(${right})`);
        intersections.push(`${right}:where(${left})`);
      }
    }
    return intersections;
  }
  function selectorHasPersistentIdentity(selector) {
    const branches = splitSelectorText(selector);
    return branches.length > 0 && branches.every(selectorBranchHasPersistentIdentity);
  }
  function selectorBranchHasPersistentIdentity(selector) {
    let quote = "";
    let escaped = false;
    for (let index = 0; index < selector.length; index += 1) {
      const char = selector[index];
      if (escaped) {
        escaped = false;
        continue;
      }
      if (char === "\\") {
        escaped = true;
        continue;
      }
      if (quote) {
        if (char === quote) quote = "";
        continue;
      }
      if (char === '"' || char === "'") {
        quote = char;
        continue;
      }
      if (char === "[" || char === "#" || char === ".") return true;
    }
    return false;
  }
  function winningSelectorCandidates(group, cdpStyleInfo, stateContext) {
    if (!(cdpStyleInfo == null ? void 0 : cdpStyleInfo.getWinningRule)) return [];
    const props = group.diffProps.length ? group.diffProps : CLASSIFICATION_ANCHOR_PROPS;
    const selectors = [];
    for (const item of group.items) {
      for (const prop of props) {
        const rule = cdpStyleInfo.getWinningRule(item, prop, stateContext);
        if ((rule == null ? void 0 : rule.selector) && !rule.isInline) selectors.push(rule.selector);
      }
    }
    return selectors;
  }
  function classSelectorCandidates(items) {
    if (!items.length) return [];
    const tag = tagName(items[0]);
    const common = intersect(items.map(classList));
    const candidates = [];
    for (const cls of common) {
      candidates.push(`.${escapeCss(cls)}`);
      candidates.push(`${tag}.${escapeCss(cls)}`);
    }
    if (common.length > 1) {
      const intersection = common.map((cls) => `.${escapeCss(cls)}`).join("");
      candidates.push(intersection);
      candidates.push(`${tag}:where(${intersection})`);
    }
    return candidates;
  }
  function attributeSelectorCandidates(items) {
    if (!items.length) return [];
    const first = items[0];
    const candidates = [];
    for (const attr of ["role", "aria-label", "data-kind", "data-type", "data-role"]) {
      if (!first.hasAttribute(attr)) continue;
      const value = first.getAttribute(attr) || "";
      if (items.every((item) => item.getAttribute(attr) === value)) {
        candidates.push(`${tagName(first)}[${attr}="${escapeAttribute(value)}"]`);
      }
    }
    return candidates;
  }
  function structuralBaseSelectorCandidates(items) {
    if (!items.length || !items.every((item) => item.tagName === items[0].tagName)) return [];
    const tag = tagName(items[0]);
    const commonClasses = intersect(items.map(classList));
    const selectors = commonClasses.flatMap((cls) => [`.${escapeCss(cls)}`, `${tag}.${escapeCss(cls)}`]);
    if (commonClasses.length > 1) {
      const intersection = commonClasses.map((cls) => `.${escapeCss(cls)}`).join("");
      selectors.unshift(intersection, `${tag}${intersection}`);
    }
    return uniqueStrings(selectors).filter(selectorHasPersistentIdentity);
  }
  function intersectStructuralBase(base, discriminator) {
    if (selectorContains(discriminator, base)) return discriminator;
    const filter = selectorDifferenceFilter(discriminator, base);
    return filter ? `${base}:where(${filter})` : base;
  }
  function negativeSelectorCandidates(group, groups, structuralBases) {
    if (!structuralBases.length) return [];
    const baseClasses = intersect(groups.flatMap((item) => item.items).map(classList));
    const otherGroupDiscriminators = uniqueStrings(groups.filter((other) => other !== group).map((other) => intersect(other.items.map(classList)).filter((cls) => !baseClasses.includes(cls) && !group.items.some((item) => item.classList.contains(cls))).map((cls) => `.${escapeCss(cls)}`).join("")).filter(Boolean));
    if (!otherGroupDiscriminators.length) return [];
    const exclusion = otherGroupDiscriminators.join(", ");
    return structuralBases.map((base) => `${base}:not(:where(${exclusion}))`);
  }
  function elementMatchesSelector(element, selector) {
    try {
      return element.matches(selector);
    } catch {
      return false;
    }
  }
  function scopedSelectorCandidates(candidates, scopes) {
    if (!scopes.length) return [];
    const scopeSelectors = uniqueStrings(scopes.map(bestElementSelector).filter(Boolean));
    if (!scopeSelectors.length) return [];
    return candidates.flatMap((candidate) => scopeSelectors.map((scope) => `:where(${scope}) ${candidate}`));
  }
  function nthFallbackSelector(items, scopes, options = {}) {
    if (options.preferSharedParent) {
      const sharedParent = sharedDirectParent(scopes);
      const scopeSelector = sharedParent ? persistentScopeSelector(sharedParent) : "";
      if (scopeSelector) {
        const paths = items.filter((item) => sharedParent == null ? void 0 : sharedParent.contains(item)).map((item) => scopedNthPath(sharedParent, item)).filter(Boolean).map((path) => path.replace(":scope", `:where(${scopeSelector})`));
        if (paths.length) return uniqueStrings(paths).join(", ");
      }
    }
    const selectors = [];
    for (const scope of scopes) {
      for (const item of items) {
        if (!scope.contains(item)) continue;
        const path = scopedNthPath(scope, item);
        if (path) selectors.push(path);
      }
    }
    return selectors.length ? uniqueStrings(selectors).join(", ") : "";
  }
  function sharedDirectParent(elements) {
    const parents = uniqueElements(elements.map((element) => element.parentElement).filter(Boolean));
    return parents.length === 1 ? parents[0] : null;
  }
  function scopedNthPath(scope, item) {
    const parts = [];
    let node = item;
    while (node && node !== scope) {
      const parent = node.parentElement;
      if (!parent) return "";
      const index = Array.from(parent.children).indexOf(node) + 1;
      parts.unshift({ tag: tagName(node), index, needsNth: true });
      node = parent;
    }
    if (node !== scope) return "";
    const selectorFor = () => `:scope > ${parts.map((part) => `${part.tag}${part.needsNth ? `:nth-child(${part.index})` : ""}`).join(" > ")}`;
    for (let index = parts.length - 1; index >= 0; index -= 1) {
      parts[index].needsNth = false;
      const matches = Array.from(scope.querySelectorAll(selectorFor()));
      if (matches.length !== 1 || matches[0] !== item) parts[index].needsNth = true;
    }
    return selectorFor();
  }
  function verifySelectorTargetSet({
    selector,
    scopes,
    expected,
    breadth,
    queryDomain
  }) {
    var _a2, _b2;
    const scopedQuery = () => uniqueElements(scopes.flatMap((scope) => queryWithin(scope, selector)));
    let allMatches;
    if (queryDomain === "document" && selector && !selector.includes(":scope")) {
      const document2 = ((_a2 = expected[0]) == null ? void 0 : _a2.ownerDocument) || ((_b2 = scopes[0]) == null ? void 0 : _b2.ownerDocument);
      try {
        allMatches = document2 ? uniqueElements(splitSelectorText(selector).flatMap((branch) => Array.from(document2.querySelectorAll(branch)))) : scopedQuery();
      } catch {
        allMatches = scopedQuery();
      }
    } else {
      allMatches = scopedQuery();
    }
    const actual = breadth === "single" ? allMatches : visibleElements(allMatches);
    const comparedExpected = breadth === "single" ? uniqueElements(expected) : visibleElements(expected);
    const extra = actual.filter((item) => !comparedExpected.includes(item));
    const missing = comparedExpected.filter((item) => !actual.includes(item));
    const ok = extra.length === 0 && missing.length === 0 && actual.length === comparedExpected.length;
    return {
      ok,
      selector,
      expectedCount: comparedExpected.length,
      actualCount: actual.length,
      extra,
      missing,
      reason: ok ? "" : breadth === "single" ? "selector did not match exactly the expected targets" : "selector visible matches did not equal the expected targets"
    };
  }
  function buildWritePlans({
    group,
    property,
    value,
    cdpStyleInfo,
    stateContext,
    scopes,
    propertyTargetResolver,
    pseudoOnly = false,
    breadth
  }) {
    const resolvedOwnerTargets = group.items.map((owner) => {
      const relation = resolvePropertyTarget(owner, property, propertyTargetResolver);
      return { owner, targets: visibleElements(relation.targets), relation };
    });
    return partitionOwnerTargets(resolvedOwnerTargets).map(
      (ownerTargets) => buildWritePlanForTargets({
        group,
        property,
        value,
        cdpStyleInfo,
        stateContext,
        scopes,
        pseudoOnly,
        breadth,
        ownerTargets
      })
    );
  }
  function buildWritePlanForTargets({
    group,
    property,
    value,
    cdpStyleInfo,
    stateContext,
    scopes,
    pseudoOnly = false,
    breadth,
    ownerTargets
  }) {
    var _a2, _b2;
    const first = group.items[0];
    const propertyTargets = uniqueElements(ownerTargets.flatMap((item) => item.targets));
    const hasPropertyTargets = propertyTargets.length > 0;
    const firstTarget = propertyTargets[0] || first;
    const winningRule = hasPropertyTargets ? ((_a2 = cdpStyleInfo == null ? void 0 : cdpStyleInfo.getWinningRule) == null ? void 0 : _a2.call(cdpStyleInfo, firstTarget, property, stateContext)) || null : null;
    const baseWinningRule = pseudoOnly && hasPropertyTargets ? ((_b2 = cdpStyleInfo == null ? void 0 : cdpStyleInfo.getWinningRule) == null ? void 0 : _b2.call(cdpStyleInfo, firstTarget, property, null)) || null : winningRule;
    const classificationSelector = group.classificationSelector || tagName(first);
    const classificationSelectorMode = group.classificationSelectorMode || "";
    const fallbackReasons = [...group.fallbackReasons];
    const anchorRule = hasPropertyTargets ? classificationAnchorRule(group, propertyTargets, property, cdpStyleInfo, pseudoOnly ? null : stateContext) : null;
    const classificationTargetSelector = propertyTargetSelectorForOwners({
      classificationSelector,
      ownerTargets,
      candidateRules: [winningRule, anchorRule],
      scopes,
      fallbackReasons,
      breadth
    });
    const insertionAnchorRule = pseudoOnly ? latestSameSheetRule([winningRule, baseWinningRule, anchorRule]) : anchorRule || ((winningRule == null ? void 0 : winningRule.styleSheetId) ? winningRule : null);
    const selectorPlan = classificationTargetSelector ? generateWriteSelectorPlan({
      classificationSelector: classificationTargetSelector,
      classificationSelectorMode,
      winningRule,
      scopes,
      expectedTargets: propertyTargets,
      stateContext,
      fallbackReasons,
      pseudoOnly,
      breadth
    }) : { selector: "", mode: "structure-narrow" };
    const materializedSelector = materializeScopedSelector(selectorPlan.selector, scopes);
    const verificationTargets = propertyTargets;
    const selectorVerification = verifySelectorTargetSet({
      selector: materializedSelector || classificationTargetSelector,
      scopes,
      expected: verificationTargets,
      breadth,
      queryDomain: "document"
    });
    const targetRangeVerified = pseudoOnly || selectorVerification.ok;
    const writeRule = editableOriginalRule(
      pseudoOnly ? [winningRule] : [winningRule, anchorRule],
      materializedSelector,
      verificationTargets,
      breadth
    );
    const writeMode = !hasPropertyTargets || !targetRangeVerified ? "unavailable" : writeRule ? "edit-original" : materializedSelector && (insertionAnchorRule == null ? void 0 : insertionAnchorRule.styleSheetId) && (insertionAnchorRule == null ? void 0 : insertionAnchorRule.styleRange) ? "insert-rule" : "unavailable";
    const unavailableReason = writeMode === "unavailable" ? !hasPropertyTargets ? "property target resolver returned no editable targets" : !targetRangeVerified ? "write selector did not match property targets exactly" : !materializedSelector ? "write plan has no materialized selector" : !(insertionAnchorRule == null ? void 0 : insertionAnchorRule.styleSheetId) || !(insertionAnchorRule == null ? void 0 : insertionAnchorRule.styleRange) ? "write plan has no persistent stylesheet insertion anchor" : "write plan could not materialize a persistent write" : "";
    if (unavailableReason) fallbackReasons.push(unavailableReason);
    const generatedRule = generateCssRule({
      selector: materializedSelector,
      mode: writeMode === "edit-original" ? "original" : selectorPlan.mode,
      important: selectorPlan.important,
      property,
      value,
      insertionAnchorRule,
      comment: selectorPlan.comment
    });
    return {
      groupId: group.id,
      items: group.items,
      property,
      value,
      stateContext,
      ownerTargets,
      propertyTargets,
      verificationTargets,
      classificationSelector,
      classificationSelectorMode,
      propertyWinningSelector: winningRule == null ? void 0 : winningRule.selector,
      propertyWinningRule: winningRule,
      classificationAnchorRule: anchorRule,
      insertionAnchorRule,
      generatedSelector: generatedRule.selector,
      materializedSelector,
      writeMode,
      writeRule,
      writeSourceProperty: writeRule === winningRule ? winningRule == null ? void 0 : winningRule.sourceProperty : void 0,
      unavailableReason,
      generatedRule,
      fallbackReasons,
      verification: {
        selector: selectorVerification,
        computed: verifyComputedValue(group.items, property, value)
      }
    };
  }
  function partitionOwnerTargets(ownerTargets) {
    const partitions = /* @__PURE__ */ new Map();
    for (const item of ownerTargets) {
      if (!item.targets.length) continue;
      for (const target of item.targets) {
        const relationKey = target === item.owner ? "self" : item.owner.contains(target) ? `descendant:${relativeSelectorFromOwner(item.owner, target)}` : target.contains(item.owner) ? `ancestor:${relativeSelectorFromOwner(target, item.owner)}` : "";
        if (!relationKey || relationKey.endsWith(":")) continue;
        const partition = partitions.get(relationKey) || [];
        partition.push({
          owner: item.owner,
          targets: [target],
          relation: item.relation
        });
        partitions.set(relationKey, partition);
      }
    }
    return partitions.size ? [...partitions.values()] : [[]];
  }
  function propertyTargetSelectorForOwners({
    classificationSelector,
    ownerTargets,
    candidateRules,
    scopes,
    fallbackReasons,
    breadth
  }) {
    const owners = ownerTargets.map((item) => item.owner);
    const propertyTargets = uniqueElements(ownerTargets.flatMap((item) => item.targets));
    if (sameElementSet(owners, propertyTargets)) return classificationSelector;
    const descendantSuffix = propertyTargetSuffixForOwners(ownerTargets);
    if (descendantSuffix) {
      const projected = projectOwnerClassificationThroughPropertyRules({
        classificationSelector,
        candidateRules,
        scopes,
        owners,
        propertyTargets,
        breadth
      });
      if (projected) return projected;
      return appendDescendantSelector(classificationSelector, descendantSuffix);
    }
    const ancestorSelector = ancestorTargetSelector(classificationSelector, ownerTargets, scopes, propertyTargets, breadth);
    if (ancestorSelector) return ancestorSelector;
    for (const rule of candidateRules) {
      if ((rule == null ? void 0 : rule.selector) && selectorMatchesExactDocumentSet(rule.selector, propertyTargets, breadth)) return rule.selector;
    }
    const nth = nthFallbackSelector(propertyTargets, scopes, { preferSharedParent: breadth === "single" });
    if (nth && selectorMatchesTargetsExactly(nth, scopes, propertyTargets, breadth)) {
      fallbackReasons.push("property target relation required nth fallback because no stable selector preserved the owner classification");
      return nth;
    }
    fallbackReasons.push("property target relation could not be materialized without changing the target range");
    return "";
  }
  function projectOwnerClassificationThroughPropertyRules({
    classificationSelector,
    candidateRules,
    scopes,
    owners,
    propertyTargets,
    breadth
  }) {
    for (const rule of candidateRules) {
      for (const propertyBranch of splitSelectorText((rule == null ? void 0 : rule.selector) || "")) {
        const propertyContext = selectorContextParts(propertyBranch);
        if (!propertyContext.ancestor || !propertyContext.target) continue;
        const projectedOwner = specificityPreservingClassificationSelector(
          classificationSelector,
          propertyContext.ancestor,
          scopes,
          owners,
          breadth
        );
        if (!projectedOwner) continue;
        const candidate = `${projectedOwner} ${propertyContext.target}`;
        if (selectorMatchesTargetsExactly(candidate, scopes, propertyTargets, breadth)) return candidate;
      }
    }
    return "";
  }
  function ancestorTargetSelector(classificationSelector, ownerTargets, scopes, expectedTargets, breadth) {
    if (!ownerTargets.length || ownerTargets.some(
      (item) => item.targets.length !== 1 || !item.targets[0].contains(item.owner)
    )) return "";
    const relativePaths = ownerTargets.map((item) => relativeSelectorFromOwner(item.targets[0], item.owner));
    const relativePath = relativePaths[0] || "";
    if (!relativePath || !relativePaths.every((path) => path === relativePath)) return "";
    const targetItems = ownerTargets.map((item) => item.targets[0]);
    const targetBases = uniqueStrings([
      ...classSelectorCandidates(targetItems),
      ...attributeSelectorCandidates(targetItems),
      targetItems.every((item) => item.tagName === targetItems[0].tagName) ? tagName(targetItems[0]) : ""
    ]);
    const ownerBranches = splitSelectorText(classificationSelector);
    for (const targetBase of targetBases) {
      const mappedBranches = ownerBranches.map((branch) => {
        const ownerContext = selectorContextParts(branch);
        const relativeOwner = constrainRelativeTarget(relativePath, ownerContext.target);
        const target = `${targetBase}:has(> ${relativeOwner})`;
        return joinSelectorParts(ownerContext.ancestor, target);
      });
      const candidates = [mappedBranches.join(", "), ...mappedBranches];
      for (const candidate of candidates) {
        if (selectorMatchesTargetsExactly(candidate, scopes, expectedTargets, breadth)) return candidate;
      }
    }
    return "";
  }
  function constrainRelativeTarget(relativePath, ownerFilter) {
    if (!ownerFilter) return relativePath;
    const separator = " > ";
    const index = relativePath.lastIndexOf(separator);
    const prefix = index >= 0 ? relativePath.slice(0, index + separator.length) : "";
    const target = index >= 0 ? relativePath.slice(index + separator.length) : relativePath;
    return `${prefix}${target}:where(${ownerFilter})`;
  }
  function selectorMatchesTargetsExactly(selector, scopes, expectedTargets, breadth) {
    const materialized = materializeScopedSelector(selector, scopes);
    return verifySelectorTargetSet({
      selector: materialized || selector,
      scopes,
      expected: expectedTargets,
      breadth,
      queryDomain: "document"
    }).ok;
  }
  function materializeScopedSelector(selector, scopes) {
    const raw = String(selector || "").trim();
    if (!raw || raw === "inline-style") return "";
    if (!raw.includes(":scope")) return raw;
    const scopeSelectors = uniqueStrings(scopes.map(persistentScopeSelector).filter(Boolean));
    if (!scopeSelectors.length) return "";
    return uniqueStrings(scopeSelectors.flatMap(
      (scopeSelector) => splitSelectorText(raw).map((branch) => branch.split(":scope").join(`:where(${scopeSelector})`))
    )).join(", ");
  }
  function persistentScopeSelector(element) {
    const own = stableElementSelectorCandidates(element);
    const direct = own.find((selector) => selectorSelectsOnlyElement(element, selector));
    if (direct) return direct;
    let ancestor = element.parentElement;
    for (let depth = 0; ancestor && depth < 3; depth += 1, ancestor = ancestor.parentElement) {
      const ancestorSelector = stableElementSelectorCandidates(ancestor).find((selector) => selectorSelectsOnlyElement(ancestor, selector));
      if (!ancestorSelector) continue;
      const nested = own.map((selector) => `${ancestorSelector} ${selector}`).find((selector) => selectorSelectsOnlyElement(element, selector));
      if (nested) return nested;
    }
    return "";
  }
  function stableElementSelectorCandidates(element) {
    const candidates = [];
    if (element.id && !element.id.startsWith("dt-")) candidates.push(`#${escapeCss(element.id)}`);
    const classes = Array.from(element.classList).filter((name) => name && !name.startsWith("dt-")).map((name) => `.${escapeCss(name)}`);
    if (classes.length) {
      candidates.push(`${tagName(element)}${classes.join("")}`, classes.join(""), ...classes);
    }
    for (const name of ["role", "aria-label", "data-testid", "data-id", "data-key"]) {
      const value = element.getAttribute(name);
      if (value) candidates.push(`${tagName(element)}[${name}="${escapeCss(value)}"]`);
    }
    return uniqueStrings(candidates);
  }
  function selectorSelectsOnlyElement(element, selector) {
    try {
      const matches = Array.from(element.ownerDocument.querySelectorAll(selector));
      return matches.length === 1 && matches[0] === element;
    } catch {
      return false;
    }
  }
  function editableOriginalRule(candidates, selector, targets, breadth) {
    for (const rule of candidates) {
      if (!(rule == null ? void 0 : rule.selector) || rule.selector === "inline-style" || rule.sharedSelectorList) continue;
      if (!rule.styleSheetId || !rule.styleRange) continue;
      if (selectorMatchesExactDocumentSet(rule.selector, targets, breadth)) {
        return rule;
      }
    }
    return null;
  }
  function selectorMatchesExactDocumentSet(selector, expected, breadth) {
    return verifySelectorTargetSet({
      selector,
      scopes: [],
      expected,
      breadth,
      queryDomain: "document"
    }).ok;
  }
  function sameElementSet(left, right) {
    const a = uniqueElements(left);
    const b = uniqueElements(right);
    if (a.length !== b.length) return false;
    const expected = new Set(b);
    return a.every((item) => expected.has(item));
  }
  function generateWriteSelectorPlan({
    classificationSelector,
    classificationSelectorMode,
    winningRule,
    scopes,
    expectedTargets,
    stateContext,
    fallbackReasons,
    pseudoOnly,
    breadth
  }) {
    const pseudoSelector = pseudoSelectorForState(stateContext);
    if (pseudoOnly && (!(winningRule == null ? void 0 : winningRule.selector) || !selectorHasPseudo(winningRule.selector, pseudoSelector))) {
      fallbackReasons.push("pseudo write requires an existing matching pseudo rule");
      return {
        selector: "",
        mode: "structure-narrow"
      };
    }
    const propertySelector = (winningRule == null ? void 0 : winningRule.selector) || "";
    const selector = pseudoOnly ? composePseudoWriteSelector(classificationSelector, propertySelector, pseudoSelector, fallbackReasons) : composeWriteSelector(
      classificationSelector,
      classificationSelectorMode,
      winningRule,
      scopes,
      expectedTargets,
      fallbackReasons,
      breadth
    );
    const stateSelector = pseudoOnly ? selector : applyConfirmedState(selector, stateContext);
    const important = !!(winningRule == null ? void 0 : winningRule.isInline);
    const comment = selectorUsesPositionalFallback(stateSelector) ? "design-tool fallback: positional selector; verify if DOM order changes" : "";
    const mode = comment ? "nth-fallback" : (winningRule == null ? void 0 : winningRule.isInline) ? "classification-intersection" : winningRule ? "classification-intersection" : "structure-narrow";
    return {
      selector: stateSelector,
      mode,
      important,
      comment
    };
  }
  function generateCssRule({
    selector,
    mode,
    important,
    property,
    value,
    insertionAnchorRule,
    comment
  }) {
    const importantSuffix = important ? " !important" : "";
    const commentText = comment ? `/* ${comment} */
` : "";
    return {
      selector,
      property,
      value,
      cssText: `${commentText}${selector} {
  ${kebab(property)}: ${value}${importantSuffix};
}`,
      mode,
      insertAfter: insertionAnchorRule == null ? void 0 : insertionAnchorRule.range,
      comment,
      important
    };
  }
  function composePseudoWriteSelector(classificationSelector, propertySelector, pseudoSelector, fallbackReasons) {
    if (!classificationSelector || !propertySelector || !pseudoSelector) return "";
    const selectors = [];
    for (const propertyBranch of splitSelectorText(propertySelector).filter((branch) => branch.includes(pseudoSelector))) {
      const basePropertyBranch = normalizeSelectorSpaces(propertyBranch.split(pseudoSelector).join(""));
      for (const classificationBranch of splitSelectorText(classificationSelector)) {
        const narrowed = intersectSelectorBranches(basePropertyBranch, classificationBranch);
        const stateful = applyPseudoAtMatchingCompound(narrowed, propertyBranch, pseudoSelector);
        if (stateful) selectors.push(stateful);
      }
    }
    const selector = uniqueStrings(selectors).join(", ");
    if (selector) return selector;
    fallbackReasons.push("pseudo write could not intersect its state selector with the visual classification");
    return "";
  }
  function intersectSelectorBranches(propertyBranch, classificationBranch) {
    const propertyParts = splitSelectorByDescendant(propertyBranch);
    const classificationParts = splitSelectorByDescendant(classificationBranch);
    if (!propertyParts.length) return classificationBranch;
    if (!classificationParts.length) return propertyBranch;
    const result = propertyParts.slice();
    const shared = Math.min(propertyParts.length, classificationParts.length);
    for (let offset = 1; offset <= shared; offset += 1) {
      const propertyPart = propertyParts[propertyParts.length - offset];
      const classificationPart = classificationParts[classificationParts.length - offset];
      const filter = selectorDifferenceFilter(classificationPart, propertyPart);
      if (filter) {
        result[result.length - offset] = filter.startsWith(":not(") || filter.startsWith(":where(") ? `${propertyPart}${filter}` : `${propertyPart}:where(${filter})`;
      }
    }
    if (classificationParts.length > propertyParts.length) {
      result.unshift(...classificationParts.slice(0, classificationParts.length - propertyParts.length));
    }
    return normalizeSelectorSpaces(result.join(" "));
  }
  function applyPseudoAtMatchingCompound(selector, propertySelector, pseudoSelector) {
    const selectorParts = splitSelectorByDescendant(selector);
    const propertyParts = splitSelectorByDescendant(propertySelector);
    const propertyIndex = propertyParts.findIndex((part) => part.includes(pseudoSelector));
    if (propertyIndex < 0) return "";
    const offsetFromTarget = propertyParts.length - 1 - propertyIndex;
    const targetIndex = selectorParts.length - 1 - offsetFromTarget;
    if (targetIndex < 0 || !selectorParts[targetIndex]) return "";
    if (!selectorParts[targetIndex].includes(pseudoSelector)) {
      selectorParts[targetIndex] = `${selectorParts[targetIndex]}${pseudoSelector}`;
    }
    return normalizeSelectorSpaces(selectorParts.join(" "));
  }
  function latestSameSheetRule(rules) {
    const available = rules.filter((rule) => !!(rule == null ? void 0 : rule.styleSheetId) && !!(rule == null ? void 0 : rule.styleRange));
    if (!available.length) return null;
    const primary = available[0];
    return available.reduce((latest, rule) => {
      if (rule.styleSheetId !== primary.styleSheetId) return latest;
      return compareRuleStart(rule, latest) > 0 ? rule : latest;
    }, primary);
  }
  function compareRuleStart(left, right) {
    var _a2, _b2, _c, _d, _e, _f, _g, _h;
    const leftLine = ((_a2 = left.styleRange) == null ? void 0 : _a2.startLine) ?? ((_b2 = left.range) == null ? void 0 : _b2.startLine) ?? -1;
    const rightLine = ((_c = right.styleRange) == null ? void 0 : _c.startLine) ?? ((_d = right.range) == null ? void 0 : _d.startLine) ?? -1;
    if (leftLine !== rightLine) return leftLine - rightLine;
    const leftColumn = ((_e = left.styleRange) == null ? void 0 : _e.startColumn) ?? ((_f = left.range) == null ? void 0 : _f.startColumn) ?? -1;
    const rightColumn = ((_g = right.styleRange) == null ? void 0 : _g.startColumn) ?? ((_h = right.range) == null ? void 0 : _h.startColumn) ?? -1;
    return leftColumn - rightColumn;
  }
  function composeWriteSelector(classificationSelector, classificationSelectorMode, winningRule, scopes, expectedTargets, fallbackReasons, breadth) {
    if ((winningRule == null ? void 0 : winningRule.inherited) && winningRule.ownerSelector) {
      const inheritedSelector = inheritedContextSelector(
        classificationSelector,
        winningRule.ownerSelector,
        winningRule.targetSelector || "",
        scopes,
        expectedTargets,
        breadth
      );
      if (inheritedSelector) return inheritedSelector;
      fallbackReasons.push("inherited owner selector did not verify; using classification selector");
      return classificationSelector;
    }
    if (winningRule == null ? void 0 : winningRule.inherited) {
      fallbackReasons.push("inherited winning selector lacked owner context; used classification selector for write");
      return classificationSelector;
    }
    if (classificationSelectorMode === "nth-fallback" && (winningRule == null ? void 0 : winningRule.selector) && winningRule.selector !== classificationSelector) {
      const narrowed = narrowWinningSelectorWithNthScope(
        classificationSelector,
        winningRule.selector,
        scopes,
        expectedTargets,
        breadth
      );
      if (narrowed) return narrowed;
      fallbackReasons.push("nth scope could not be aligned to the winning selector; used the materialized nth scope");
    }
    return classificationSelector;
  }
  function narrowWinningSelectorWithNthScope(nthScopeSelector, winningSelector, scopes, expectedTargets, breadth) {
    const target = expectedTargets[0];
    if (!target) return "";
    const nthBranches = splitSelectorText(nthScopeSelector);
    for (const winningBranch of splitSelectorText(winningSelector)) {
      const winningParts = selectorStructureParts(winningBranch);
      const winningNodes = selectorNodesForTarget(winningParts, target);
      if (!winningNodes) continue;
      for (const nthBranch of nthBranches) {
        const nthParts = selectorStructureParts(nthBranch);
        const nthNodes = selectorNodesForTarget(nthParts, target);
        if (!nthNodes) continue;
        const rewritten = winningParts.map((part) => ({ ...part }));
        let changed = false;
        for (let index = 0; index < nthParts.length; index += 1) {
          const positional = positionalFilters(nthParts[index].compound);
          if (!positional.length) continue;
          const matchingIndex = winningNodes.findIndex((node) => node === nthNodes[index]);
          if (matchingIndex < 0) continue;
          rewritten[matchingIndex].compound += `:where(${positional.join("")})`;
          changed = true;
        }
        if (!changed) continue;
        const candidate = selectorFromStructureParts(rewritten);
        if (verifySelectorTargetSet({ selector: candidate, scopes, expected: expectedTargets, breadth, queryDomain: "document" }).ok) {
          return candidate;
        }
      }
    }
    return "";
  }
  function selectorStructureParts(selector) {
    const parts = [];
    let compound = "";
    let depth = 0;
    let quote = "";
    let escaped = false;
    let combinatorBefore = "";
    const flush = () => {
      if (!compound.trim()) return;
      parts.push({ compound: compound.trim(), combinatorBefore });
      compound = "";
      combinatorBefore = " ";
    };
    for (const char of selector.trim()) {
      if (escaped) {
        compound += char;
        escaped = false;
        continue;
      }
      if (char === "\\") {
        compound += char;
        escaped = true;
        continue;
      }
      if (quote) {
        compound += char;
        if (char === quote) quote = "";
        continue;
      }
      if (char === '"' || char === "'") {
        compound += char;
        quote = char;
        continue;
      }
      if (char === "(" || char === "[") {
        compound += char;
        depth += 1;
        continue;
      }
      if (char === ")" || char === "]") {
        compound += char;
        depth = Math.max(0, depth - 1);
        continue;
      }
      if (depth === 0 && char === ">") {
        flush();
        combinatorBefore = ">";
        continue;
      }
      if (depth === 0 && /\s/.test(char)) {
        flush();
        continue;
      }
      compound += char;
    }
    flush();
    return parts;
  }
  function selectorNodesForTarget(parts, target) {
    var _a2;
    if (!parts.length || !elementMatchesSelector(target, parts[parts.length - 1].compound)) return null;
    const nodes = new Array(parts.length);
    nodes[parts.length - 1] = target;
    for (let index = parts.length - 1; index > 0; index -= 1) {
      const relation = parts[index].combinatorBefore;
      const previous = parts[index - 1].compound;
      const current = nodes[index];
      const candidate = relation === ">" ? current.parentElement : ((_a2 = current.parentElement) == null ? void 0 : _a2.closest(previous)) || null;
      if (!candidate || !elementMatchesSelector(candidate, previous)) return null;
      nodes[index - 1] = candidate;
    }
    return nodes;
  }
  function positionalFilters(compound) {
    const filters = [];
    for (let index = 0; index < compound.length; index += 1) {
      if (!compound.startsWith(":nth-", index)) continue;
      const start = index;
      const open = compound.indexOf("(", index);
      if (open < 0) continue;
      let depth = 1;
      index = open;
      while (index + 1 < compound.length && depth > 0) {
        index += 1;
        if (compound[index] === "(") depth += 1;
        if (compound[index] === ")") depth -= 1;
      }
      if (depth === 0) filters.push(compound.slice(start, index + 1));
    }
    return filters;
  }
  function selectorFromStructureParts(parts) {
    return parts.map((part, index) => {
      if (index === 0) return part.compound;
      return `${part.combinatorBefore === ">" ? " > " : " "}${part.compound}`;
    }).join("");
  }
  function inheritedContextSelector(classificationSelector, ownerSelector, targetSelector, scopes, expectedTargets, breadth) {
    const candidates = [];
    for (const classificationBranch of splitSelectorText(classificationSelector)) {
      if (targetSelector) {
        const narrowedTarget = specificityPreservingSelectorBranch(
          classificationBranch,
          selectorContextParts(targetSelector)
        );
        candidates.push(`${ownerSelector} ${narrowedTarget}`);
      }
      candidates.push(`${ownerSelector} ${classificationBranch}`);
      candidates.push(classificationBranch);
    }
    return uniqueStrings(candidates.map(normalizeSelectorSpaces)).find((candidate) => verifySelectorTargetSet({ selector: candidate, scopes, expected: expectedTargets, breadth, queryDomain: "scopes" }).ok) || "";
  }
  function specificityPreservingClassificationSelector(classificationSelector, propertySelector, scopes, expectedTargets, breadth) {
    const classificationBranches = splitSelectorText(classificationSelector);
    for (const propertyBranch of splitSelectorText(propertySelector)) {
      const propertyContext = selectorContextParts(propertyBranch);
      const candidates = uniqueStrings(classificationBranches.map((classificationBranch) => specificityPreservingSelectorBranch(classificationBranch, propertyContext)).filter(Boolean));
      const combined = candidates.join(", ");
      if (combined && verifySelectorTargetSet({ selector: combined, scopes, expected: expectedTargets, breadth, queryDomain: "scopes" }).ok) return combined;
      const exact = candidates.find((candidate) => verifySelectorTargetSet({ selector: candidate, scopes, expected: expectedTargets, breadth, queryDomain: "scopes" }).ok);
      if (exact) return exact;
    }
    return "";
  }
  function specificityPreservingSelectorBranch(classificationSelector, propertyContext) {
    const classificationContext = selectorContextParts(classificationSelector);
    const targetFilter = selectorDifferenceFilter(classificationContext.target, propertyContext.target);
    const target = targetFilter ? `${propertyContext.target}:where(${targetFilter})` : propertyContext.target;
    if (!classificationContext.ancestor) return target;
    const ancestor = propertyContext.ancestor ? propertyContext.ancestor : `:where(${classificationContext.ancestor})`;
    return joinSelectorParts(ancestor, target);
  }
  function selectorDifferenceFilter(selector, baseSelector) {
    if (!selector || selector === baseSelector || selectorContains(baseSelector, selector)) return "";
    if (selector.startsWith(baseSelector)) return selector.slice(baseSelector.length).trim();
    return selector;
  }
  function selectorUsesPositionalFallback(selector) {
    return /:nth-(child|of-type)\(/.test(selector);
  }
  function selectorContextParts(selector) {
    const parts = splitSelectorByDescendant(selector);
    const target = parts.pop() || selector.trim();
    const ancestor = parts.join(" ");
    return {
      full: normalizeSelectorSpaces(selector),
      ancestor: normalizeSelectorSpaces(ancestor),
      target: normalizeSelectorSpaces(target)
    };
  }
  function splitSelectorByDescendant(selector) {
    const parts = [];
    let current = "";
    let depth = 0;
    for (const char of selector.trim()) {
      if (char === "(" || char === "[") depth += 1;
      if (char === ")" || char === "]") depth = Math.max(0, depth - 1);
      if (/\s/.test(char) && depth === 0) {
        if (current.trim()) parts.push(current.trim());
        current = "";
        continue;
      }
      current += char;
    }
    if (current.trim()) parts.push(current.trim());
    return parts;
  }
  function joinSelectorParts(...parts) {
    return normalizeSelectorSpaces(parts.filter(Boolean).join(" "));
  }
  function normalizeSelectorSpaces(selector) {
    return selector.replace(/\s+/g, " ").trim();
  }
  function classificationAnchorRule(group, propertyTargets, property, cdpStyleInfo, stateContext) {
    if (!(cdpStyleInfo == null ? void 0 : cdpStyleInfo.getWinningRule)) return null;
    const props = uniqueStrings([
      ...group.diffProps.filter((prop) => prop !== property),
      ...CLASSIFICATION_ANCHOR_PROPS.filter((prop) => prop !== property)
    ]);
    const targets = propertyTargets.length ? propertyTargets : group.items;
    for (const target of targets) {
      for (const prop of props) {
        const rule = cdpStyleInfo.getWinningRule(target, prop, stateContext);
        if ((rule == null ? void 0 : rule.selector) && !rule.isInline && rule.styleSheetId && selectorMatchesEveryTarget(rule.selector, targets)) {
          return rule;
        }
      }
    }
    return null;
  }
  function selectorMatchesEveryTarget(selector, targets) {
    if (!selector || !targets.length) return false;
    return splitSelectorText(selector).some((branch) => {
      try {
        return targets.every((target) => target.matches(branch));
      } catch {
        return false;
      }
    });
  }
  function propertyTargetSuffixForOwners(ownerTargets) {
    const suffixes = ownerTargets.map(({ owner, targets }) => {
      if (targets.length !== 1) return "";
      const target = targets[0];
      if (target === owner) return "";
      if (!owner.contains(target)) return "";
      return relativeSelectorFromOwner(owner, target);
    });
    const first = suffixes[0] || "";
    return suffixes.every((item) => item === first) ? first : "";
  }
  function relativeSelectorFromOwner(owner, target) {
    const parts = [];
    let node = target;
    while (node && node !== owner) {
      const parent = node.parentElement;
      if (!parent) return "";
      parts.unshift(bestChildSelector(node, parent));
      node = parent;
    }
    return parts.join(" > ");
  }
  function bestChildSelector(node, parent) {
    const stable = classList(node).find((cls) => !isStateLikeClass(cls));
    if (stable) return `${tagName(node)}.${escapeCss(stable)}`;
    const siblings = Array.from(parent.children).filter((child) => child.tagName === node.tagName);
    if (siblings.length <= 1) return tagName(node);
    return `${tagName(node)}:nth-of-type(${siblings.indexOf(node) + 1})`;
  }
  function appendDescendantSelector(selector, suffix) {
    if (!suffix) return selector;
    return splitSelectorText(selector).map((part) => `${part} ${suffix}`).join(", ");
  }
  function isStateLikeClass(token) {
    return /(^|[-_:])(active|selected|current|open|expanded|collapsed|checked|pressed|focus|focused|hover|disabled|enabled|on|off)([-_:]|$)/i.test(token);
  }
  function selectorLooksSameElement(selector) {
    return !/[ >+~,]/.test(selector.replace(/:where\([^)]*\)/g, ""));
  }
  function selectorContains(a, b) {
    return a === b || a.includes(b);
  }
  function applyConfirmedState(selector, state) {
    if (!(state == null ? void 0 : state.selector)) return selector;
    if (selector.includes(state.selector)) return selector;
    if (state.selector.includes("&")) return state.selector.replace(/&/g, selector);
    return `${selector}${state.selector}`;
  }
  function verifyComputedValue(items, property, value) {
    const actual = items.map((item) => {
      var _a2;
      return ((_a2 = item.ownerDocument.defaultView) == null ? void 0 : _a2.getComputedStyle(item).getPropertyValue(kebab(property))) || "";
    });
    return {
      ok: actual.every((itemValue) => normalizeCssValue(itemValue) === normalizeCssValue(value)),
      expected: value,
      actual
    };
  }
  function queryWithin(scope, selector) {
    try {
      const direct = scope.matches(selector) ? [scope] : [];
      return direct.concat(Array.from(scope.querySelectorAll(selector)));
    } catch {
      return [];
    }
  }
  function bestElementSelector(element) {
    if (element.id) return `#${escapeCss(element.id)}`;
    const classes = classList(element).slice(0, 3);
    if (classes.length) return `${tagName(element)}${classes.map((cls) => `.${escapeCss(cls)}`).join("")}`;
    return tagName(element);
  }
  function tagName(element) {
    return element ? element.tagName.toLowerCase() : "*";
  }
  function classList(element) {
    return Array.from(element.classList || []).filter((cls) => cls && !cls.startsWith("dt-")).sort();
  }
  function dataAttributeNames(element) {
    return Array.from(element.attributes).map((attr) => attr.name).filter((name) => name.startsWith("data-") && !name.startsWith("data-vibepolish-")).sort();
  }
  function kebab(prop) {
    return prop.replace(/[A-Z]/g, (match) => `-${match.toLowerCase()}`);
  }
  function normalizeCssValue(value) {
    return value.trim().replace(/\s+/g, " ").replace(/(-?\d+\.\d{2})\d+px/g, "$1px").replace(/0px/g, "0");
  }
  function weightedAverage(values, weights) {
    const total = weights.reduce((sum, weight) => sum + weight, 0);
    return values.reduce((sum, value, index) => sum + value * weights[index], 0) / total;
  }
  function jaccard(a, b) {
    if (!a.length && !b.length) return 1;
    const setA = new Set(a);
    const setB = new Set(b);
    const intersection = Array.from(setA).filter((item) => setB.has(item)).length;
    const union = (/* @__PURE__ */ new Set([...a, ...b])).size;
    return union ? intersection / union : 0;
  }
  function intersect(lists) {
    if (!lists.length) return [];
    return lists[0].filter((item) => lists.every((list) => list.includes(item)));
  }
  function uniqueElements(items) {
    return Array.from(new Set(items));
  }
  function visibleElements(items) {
    return uniqueElements(items).filter((item) => {
      const view = item.ownerDocument.defaultView;
      return !!view && isElementVisible(item, view);
    });
  }
  function uniqueStrings(items) {
    return Array.from(new Set(items.filter(Boolean)));
  }
  function escapeCss(value) {
    const css = globalThis.CSS;
    return (css == null ? void 0 : css.escape) ? css.escape(value) : value.replace(/[^a-zA-Z0-9_-]/g, (match) => `\\${match}`);
  }
  function escapeAttribute(value) {
    return value.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  }
  function runPropertyTargetConflictFixtureTests(doc) {
    return [
      fixtureTextSlotKeepsInheritedSourceSeparate(doc),
      fixtureDirectTextOwnerKeepsChildProxy(doc),
      fixtureLayerProxyIntersectsOwnerClassification(doc),
      fixtureAncestorLayerProjectsOwnerClassification(doc),
      fixtureIconSlotRequiresResolvedTarget(doc),
      fixtureEmptyPropertyTargetStaysUnavailable(doc)
    ];
  }
  function runSelectorVisibilityFixtureTests(doc) {
    return [
      fixtureDefaultGroupKeepsStructuralBase(doc),
      fixtureBroadSelectorIgnoresHiddenMatches(doc),
      fixtureHiddenMatchesDoNotCauseNthFallback(doc),
      fixtureBroadSelectorRejectsVisibleExtra(doc),
      fixtureSingleSelectorRejectsHiddenExtra(doc)
    ];
  }
  function fixtureDefaultGroupKeepsStructuralBase(doc) {
    return withFixture(doc, "default visual group keeps its structural base selector", `
    <nav class="nav">
      <div class="nav-item active">A</div>
      <div class="nav-item">B</div>
      <div class="nav-item">C</div>
    </nav>
    <main><div class="unrelated">Outside</div></main>
  `, `.nav-item{display:block;color:black;background:transparent}.nav-item.active{background:white}`, (root) => {
      var _a2;
      const selection = root.querySelector(".nav-item:not(.active)");
      const plan = createSelectionPlan({
        root,
        selectionOwner: selection,
        property: "backgroundColor",
        value: "red",
        breadth: "similar-kind"
      });
      const selector = plan.currentVisualGroup.classificationSelector || "";
      return assertResult(
        selector === ".nav-item:not(:where(.active))" && ((_a2 = plan.currentVisualGroup.classificationVerification) == null ? void 0 : _a2.ok) === true,
        `expected .nav-item:not(:where(.active)), got ${selector}`,
        plan
      );
    });
  }
  function fixtureHiddenMatchesDoNotCauseNthFallback(doc) {
    return withFixture(doc, "hidden selector matches do not cause nth fallback", `
    <div class="titles">
      <h3 class="card-title">A</h3><h3 class="card-title">B</h3><h3 class="card-title">C</h3>
      <h3 class="card-title">D</h3><h3 class="card-title">E</h3>
      <h3 class="card-title hidden">F</h3><h3 class="card-title hidden">G</h3>
    </div>
  `, `.card-title{display:block;color:black}.hidden{display:none}`, (root) => {
      var _a2;
      const all = Array.from(root.querySelectorAll(".card-title"));
      const plan = createSelectionPlan({
        root,
        selectionOwner: all[0],
        property: "color",
        value: "red",
        breadth: "similar-kind",
        candidateScope: all,
        fixedUniverse: [root]
      });
      const group = plan.currentVisualGroup;
      return assertResult(
        group.classificationSelectorMode !== "nth-fallback" && !((_a2 = group.classificationSelector) == null ? void 0 : _a2.includes(":nth-")) && !group.fallbackReasons.some((reason) => reason.includes("nth fallback")),
        "expected hidden matches not to force positional selector fallback",
        plan
      );
    });
  }
  function fixtureBroadSelectorIgnoresHiddenMatches(doc) {
    return withFixture(doc, "similar-kind ignores hidden selector matches without nth fallback", `
    <div class="titles">
      <h3 class="card-title">A</h3><h3 class="card-title">B</h3><h3 class="card-title">C</h3>
      <h3 class="card-title">D</h3><h3 class="card-title">E</h3>
      <h3 class="card-title hidden">F</h3><h3 class="card-title hidden">G</h3>
    </div>
  `, `.card-title{display:block;color:black}.hidden{display:none}`, (root) => {
      var _a2, _b2;
      const all = Array.from(root.querySelectorAll(".card-title"));
      const selection = all[0];
      const plan = createSelectionPlan({
        root,
        selectionOwner: selection,
        property: "color",
        value: "red",
        breadth: "similar-kind",
        candidateScope: all,
        fixedUniverse: [root],
        cdpStyleInfo: fakeCdp({ color: ".card-title" })
      });
      const group = plan.currentVisualGroup;
      return assertResult(
        plan.structuralItems.length === 5 && group.items.length === 5 && group.classificationSelector === ".card-title" && ((_a2 = group.classificationVerification) == null ? void 0 : _a2.ok) === true && group.classificationSelectorMode !== "nth-fallback" && !((_b2 = plan.writePlans[0]) == null ? void 0 : _b2.materializedSelector.includes(":nth-")),
        "expected five visible titles to use .card-title directly while ignoring two hidden matches",
        plan
      );
    });
  }
  function fixtureBroadSelectorRejectsVisibleExtra(doc) {
    return withFixture(doc, "similar-kind rejects an extra visible selector match", `
    <div class="titles">
      <h3 class="card-title">A</h3><h3 class="card-title">B</h3><h3 class="card-title">C</h3>
    </div>
  `, `.card-title{display:block;color:black}`, (root) => {
      const all = Array.from(root.querySelectorAll(".card-title"));
      const verification = verifySelectorTargetSet({
        selector: ".card-title",
        scopes: [root],
        expected: all.slice(0, 2),
        breadth: "similar-kind",
        queryDomain: "scopes"
      });
      const plan = createSelectionPlan({
        root,
        selectionOwner: all[0],
        property: "color",
        value: "red",
        candidateScope: all.slice(0, 2),
        fixedUniverse: [root]
      });
      return assertResult(
        !verification.ok && verification.extra.length === 1,
        "expected an extra visible title to invalidate the candidate selector",
        plan
      );
    });
  }
  function fixtureSingleSelectorRejectsHiddenExtra(doc) {
    return withFixture(doc, "single rejects an extra hidden selector match", `
    <div class="titles">
      <h3 class="card-title">A</h3><h3 class="card-title hidden">B</h3>
    </div>
  `, `.card-title{display:block;color:black}.hidden{display:none}`, (root) => {
      const all = Array.from(root.querySelectorAll(".card-title"));
      const verification = verifySelectorTargetSet({
        selector: ".card-title",
        scopes: [root],
        expected: [all[0]],
        breadth: "single",
        queryDomain: "scopes"
      });
      const plan = createSelectionPlan({
        root,
        selectionOwner: all[0],
        property: "color",
        value: "red",
        breadth: "single",
        candidateScope: all,
        fixedUniverse: [root]
      });
      return assertResult(
        !verification.ok && verification.extra.length === 1,
        "expected single mode to reject a selector that also matches a hidden title",
        plan
      );
    });
  }
  function fixtureEmptyPropertyTargetStaysUnavailable(doc) {
    return withFixture(doc, "empty property target remains unavailable", `
    <div class="tags">
      <span class="tag hot">A</span><span class="tag hot">B</span>
    </div>
  `, `.tag{display:inline-flex}.hot{background:red}`, (root) => {
      const selection = root.querySelector(".hot");
      const plan = createSelectionPlan({
        root,
        selectionOwner: selection,
        property: "paddingTop",
        value: "8px",
        propertyTargetResolver: () => ({ kind: "table", targets: [], reason: "fixture-disabled" })
      });
      const writePlan = plan.writePlans[0];
      return assertResult(
        plan.propertyTargets.length === 0 && (writePlan == null ? void 0 : writePlan.propertyTargets.length) === 0 && (writePlan == null ? void 0 : writePlan.verificationTargets.length) === 0 && (writePlan == null ? void 0 : writePlan.writeMode) === "unavailable",
        "expected an explicit empty property target to remain unavailable instead of falling back to the owner",
        plan
      );
    });
  }
  function fixtureTextSlotKeepsInheritedSourceSeparate(doc) {
    return withFixture(doc, "text slot target stays separate from inherited style source", `
    <section class="theme">
      <article class="card hot"><h3 class="title">A</h3><span class="meta">Meta A</span></article>
      <article class="card cold"><h3 class="title">B</h3><span class="meta">Meta B</span></article>
      <article class="card hot"><h3 class="title">C</h3><span class="meta">Meta C</span></article>
    </section>
  `, `.theme{color:black}.card{display:block}.hot{background:red}.cold{background:blue}`, (root) => {
      const selection = root.querySelector(".card.hot");
      const cdp = {
        getWinningRule: (element, property) => {
          if (property === "color" && element.matches(".title")) {
            return {
              selector: ".theme",
              ownerSelector: ".theme",
              targetSelector: ".title",
              inherited: true
            };
          }
          if (property === "backgroundColor" && element.matches(".card.hot")) return { selector: ".hot" };
          if (property === "backgroundColor" && element.matches(".card.cold")) return { selector: ".cold" };
          return null;
        }
      };
      const plan = createSelectionPlan({
        root,
        selectionOwner: selection,
        property: "color",
        value: "red",
        cdpStyleInfo: cdp,
        propertyTargetResolver: (owner) => ({
          kind: "slot-text",
          targets: Array.from(owner.querySelectorAll(":scope > .title"))
        })
      });
      const writePlan = plan.writePlans[0];
      const selector = (writePlan == null ? void 0 : writePlan.generatedSelector) || "";
      return assertResult(
        (writePlan == null ? void 0 : writePlan.ownerTargets.every((item) => item.relation.kind === "slot-text")) && (writePlan == null ? void 0 : writePlan.propertyTargets.every((item) => item.matches(".title"))) && !(writePlan == null ? void 0 : writePlan.propertyTargets.some((item) => item.matches(".theme,.card,.meta"))) && selector.includes(".theme") && selector.includes(".title") && selector.includes(".hot"),
        "expected text intent to keep title targets while inherited source only contributes selector context",
        plan
      );
    });
  }
  function fixtureDirectTextOwnerKeepsChildProxy(doc) {
    return withFixture(doc, "direct text owner keeps independent child proxy", `
    <div class="tabs">
      <button class="tab hot">Doubt <span class="n">4</span></button>
      <button class="tab cold">Okay <span class="n">2</span></button>
      <button class="tab hot">Doubt <span class="n">4</span></button>
    </div>
  `, `.tab{color:#556}.tab.hot{background:red}.tab.cold{background:blue}.tab .n{color:green}`, (root) => {
      var _a2, _b2;
      const selection = root.querySelector(".tab.hot");
      const cdp = {
        getWinningRule: (element, property) => {
          if (property !== "color") return null;
          return element.matches(".n") ? { selector: ".tab .n", property } : { selector: ".tab", property };
        }
      };
      const plan = createSelectionPlan({
        root,
        selectionOwner: selection,
        property: "color",
        value: "red",
        cdpStyleInfo: cdp,
        propertyTargetResolver: (owner) => ({
          kind: "slot-text",
          targets: [owner, ...Array.from(owner.querySelectorAll(":scope > .n"))]
        })
      });
      const ownerWrite = plan.writePlans.find((write) => write.propertyTargets.every((target) => target.matches(".tab")));
      const numberWrite = plan.writePlans.find((write) => write.propertyTargets.every((target) => target.matches(".n")));
      return assertResult(
        plan.writePlans.length === 2 && ((_a2 = ownerWrite == null ? void 0 : ownerWrite.verification.selector) == null ? void 0 : _a2.ok) === true && ((_b2 = numberWrite == null ? void 0 : numberWrite.verification.selector) == null ? void 0 : _b2.ok) === true && !((ownerWrite == null ? void 0 : ownerWrite.materializedSelector) || "").includes(".n") && ((numberWrite == null ? void 0 : numberWrite.materializedSelector) || "").includes(".n"),
        "expected direct owner text and independent child text to produce separate verified write plans",
        plan
      );
    });
  }
  function fixtureLayerProxyIntersectsOwnerClassification(doc) {
    return withFixture(doc, "visual layer target intersects owner classification", `
    <section class="cards">
      <article class="card hot"><div class="surface"><button class="inner-action">A</button></div></article>
      <article class="card cold"><div class="surface"><button class="inner-action">B</button></div></article>
      <article class="card hot"><div class="surface"><button class="inner-action">C</button></div></article>
    </section>
  `, `.card{display:block}.hot{color:red}.cold{color:blue}.surface{background:white}.inner-action{background:black}`, (root) => {
      const selection = root.querySelector(".card.hot");
      const cdp = {
        getWinningRule: (element, property) => {
          if (property === "backgroundColor" && element.matches(".surface")) return { selector: ".surface" };
          if (property === "color" && element.matches(".card.hot")) return { selector: ".hot" };
          if (property === "color" && element.matches(".card.cold")) return { selector: ".cold" };
          return null;
        }
      };
      const plan = createSelectionPlan({
        root,
        selectionOwner: selection,
        property: "backgroundColor",
        value: "green",
        cdpStyleInfo: cdp,
        propertyTargetResolver: (owner) => ({
          kind: "layer-background",
          targets: Array.from(owner.querySelectorAll(":scope > .surface"))
        })
      });
      const writePlan = plan.writePlans[0];
      const selector = (writePlan == null ? void 0 : writePlan.generatedSelector) || "";
      return assertResult(
        (writePlan == null ? void 0 : writePlan.ownerTargets.every((item) => item.relation.kind === "layer-background")) && (writePlan == null ? void 0 : writePlan.propertyTargets.every((item) => item.matches(".surface"))) && !(writePlan == null ? void 0 : writePlan.propertyTargets.some((item) => item.matches(".card,.inner-action"))) && selector.includes(".hot") && selector.includes(".surface"),
        "expected layer intent to target only the composite surface under the classified owners",
        plan
      );
    });
  }
  function fixtureAncestorLayerProjectsOwnerClassification(doc) {
    return withFixture(doc, "ancestor layer projects owner classification through :has", `
    <section class="cards">
      <div class="frame"><div class="surface hot"></div></div>
      <div class="frame"><div class="surface cold"></div></div>
      <div class="frame"><div class="surface hot"></div></div>
    </section>
  `, `.frame{border:1px solid black}.surface{height:20px}.hot{background:red}.cold{background:blue}`, (root) => {
      var _a2;
      const selection = root.querySelector(".surface.hot");
      const cdp = {
        getWinningRule: (element, property) => {
          if (property === "borderColor" && element.matches(".frame")) return { selector: ".frame" };
          if (property === "backgroundColor" && element.matches(".surface.hot")) return { selector: ".hot" };
          if (property === "backgroundColor" && element.matches(".surface.cold")) return { selector: ".cold" };
          return null;
        }
      };
      const plan = createSelectionPlan({
        root,
        selectionOwner: selection,
        property: "borderColor",
        value: "green",
        cdpStyleInfo: cdp,
        propertyTargetResolver: (owner) => {
          var _a3;
          return {
            kind: "layer-border",
            targets: ((_a3 = owner.parentElement) == null ? void 0 : _a3.matches(".frame")) ? [owner.parentElement] : []
          };
        }
      });
      const writePlan = plan.writePlans[0];
      const selector = (writePlan == null ? void 0 : writePlan.materializedSelector) || "";
      const matched = selector ? Array.from(root.ownerDocument.querySelectorAll(selector)).filter((item) => root.contains(item)) : [];
      return assertResult(
        selector.includes(":has(") && ((_a2 = writePlan == null ? void 0 : writePlan.verification.selector) == null ? void 0 : _a2.ok) === true && (writePlan == null ? void 0 : writePlan.propertyTargets.length) === 2 && matched.length === 2 && matched.every((item) => item.matches(".frame") && item.querySelector(".surface.hot")) && !matched.some((item) => item.querySelector(".surface.cold")),
        `expected ancestor frames to be selected through the hot owner classification, got ${selector || "(empty)"}`,
        plan
      );
    });
  }
  function fixtureIconSlotRequiresResolvedTarget(doc) {
    return withFixture(doc, "icon slot requires one mechanically resolved target per owner", `
    <section class="tools">
      <button class="tool hot"><svg class="glyph"></svg><span>A</span></button>
      <button class="tool cold"><svg class="glyph"></svg><svg class="glyph secondary"></svg><span>B</span></button>
      <button class="tool hot"><svg class="glyph"></svg><span>C</span></button>
    </section>
  `, `.hot{color:red}.cold{color:blue}.glyph{display:block}`, (root) => {
      const selection = root.querySelector(".tool.hot");
      const cdp = fakeCdp({ color: ".tool" });
      const uniquePlan = createSelectionPlan({
        root,
        selectionOwner: selection,
        property: "color",
        value: "green",
        cdpStyleInfo: cdp,
        propertyTargetResolver: (owner) => {
          const icons = Array.from(owner.querySelectorAll(":scope > .glyph"));
          return {
            kind: "slot-icon",
            targets: icons.length === 1 ? icons : [],
            reason: icons.length === 1 ? "" : "ambiguous-icon-slot"
          };
        }
      });
      const ambiguous = root.querySelector(".tool.cold");
      const ambiguousPlan = createSelectionPlan({
        root,
        selectionOwner: ambiguous,
        property: "color",
        value: "green",
        breadth: "single",
        cdpStyleInfo: cdp,
        propertyTargetResolver: (owner) => {
          const icons = Array.from(owner.querySelectorAll(":scope > .glyph"));
          return {
            kind: "slot-icon",
            targets: icons.length === 1 ? icons : [],
            reason: icons.length === 1 ? "" : "ambiguous-icon-slot"
          };
        }
      });
      const uniqueWrite = uniquePlan.writePlans[0];
      const ambiguousWrite = ambiguousPlan.writePlans[0];
      return assertResult(
        (uniqueWrite == null ? void 0 : uniqueWrite.ownerTargets.every((item) => item.relation.kind === "slot-icon")) && (uniqueWrite == null ? void 0 : uniqueWrite.propertyTargets.every((item) => item.matches(".glyph"))) && ((uniqueWrite == null ? void 0 : uniqueWrite.generatedSelector) || "").includes(".glyph") && (ambiguousWrite == null ? void 0 : ambiguousWrite.propertyTargets.length) === 0 && (ambiguousWrite == null ? void 0 : ambiguousWrite.writeMode) === "unavailable",
        "expected unique icon slots to resolve and ambiguous icon slots to stay unavailable without owner fallback",
        uniquePlan
      );
    });
  }
  function withFixture(doc, name, html, css, run) {
    const host = doc.createElement("div");
    const style = doc.createElement("style");
    style.textContent = css;
    host.innerHTML = html;
    doc.body.appendChild(style);
    doc.body.appendChild(host);
    try {
      const result = run(host);
      return { ...result, name };
    } catch (error) {
      return { name, ok: false, reason: error instanceof Error ? error.message : String(error) };
    } finally {
      host.remove();
      style.remove();
    }
  }
  function assertResult(ok, reason, plan) {
    return { name: "", ok, reason: ok ? "" : reason, plan };
  }
  function fakeCdp(selectors) {
    return {
      getWinningRule: (_element, property) => {
        const selector = selectors[property] || selectors[kebab(property)];
        return selector ? { selector, property, targetIdentityVerified: true } : null;
      }
    };
  }
  class Diff {
    diff(oldStr, newStr, options = {}) {
      let callback;
      if (typeof options === "function") {
        callback = options;
        options = {};
      } else if ("callback" in options) {
        callback = options.callback;
      }
      const oldString = this.castInput(oldStr, options);
      const newString = this.castInput(newStr, options);
      const oldTokens = this.removeEmpty(this.tokenize(oldString, options));
      const newTokens = this.removeEmpty(this.tokenize(newString, options));
      return this.diffWithOptionsObj(oldTokens, newTokens, options, callback);
    }
    diffWithOptionsObj(oldTokens, newTokens, options, callback) {
      var _a2;
      const done = (value) => {
        value = this.postProcess(value, options);
        if (callback) {
          setTimeout(function() {
            callback(value);
          }, 0);
          return void 0;
        } else {
          return value;
        }
      };
      const newLen = newTokens.length, oldLen = oldTokens.length;
      let editLength = 1;
      let maxEditLength = newLen + oldLen;
      if (options.maxEditLength != null) {
        maxEditLength = Math.min(maxEditLength, options.maxEditLength);
      }
      const maxExecutionTime = (_a2 = options.timeout) !== null && _a2 !== void 0 ? _a2 : Infinity;
      const abortAfterTimestamp = Date.now() + maxExecutionTime;
      const bestPath = [{ oldPos: -1, lastComponent: void 0 }];
      let newPos = this.extractCommon(bestPath[0], newTokens, oldTokens, 0, options);
      if (bestPath[0].oldPos + 1 >= oldLen && newPos + 1 >= newLen) {
        return done(this.buildValues(bestPath[0].lastComponent, newTokens, oldTokens));
      }
      let minDiagonalToConsider = -Infinity, maxDiagonalToConsider = Infinity;
      const execEditLength = () => {
        for (let diagonalPath = Math.max(minDiagonalToConsider, -editLength); diagonalPath <= Math.min(maxDiagonalToConsider, editLength); diagonalPath += 2) {
          let basePath;
          const removePath = bestPath[diagonalPath - 1], addPath = bestPath[diagonalPath + 1];
          if (removePath) {
            bestPath[diagonalPath - 1] = void 0;
          }
          let canAdd = false;
          if (addPath) {
            const addPathNewPos = addPath.oldPos - diagonalPath;
            canAdd = addPath && 0 <= addPathNewPos && addPathNewPos < newLen;
          }
          const canRemove = removePath && removePath.oldPos + 1 < oldLen;
          if (!canAdd && !canRemove) {
            bestPath[diagonalPath] = void 0;
            continue;
          }
          if (!canRemove || canAdd && removePath.oldPos < addPath.oldPos) {
            basePath = this.addToPath(addPath, true, false, 0, options);
          } else {
            basePath = this.addToPath(removePath, false, true, 1, options);
          }
          newPos = this.extractCommon(basePath, newTokens, oldTokens, diagonalPath, options);
          if (basePath.oldPos + 1 >= oldLen && newPos + 1 >= newLen) {
            return done(this.buildValues(basePath.lastComponent, newTokens, oldTokens)) || true;
          } else {
            bestPath[diagonalPath] = basePath;
            if (basePath.oldPos + 1 >= oldLen) {
              maxDiagonalToConsider = Math.min(maxDiagonalToConsider, diagonalPath - 1);
            }
            if (newPos + 1 >= newLen) {
              minDiagonalToConsider = Math.max(minDiagonalToConsider, diagonalPath + 1);
            }
          }
        }
        editLength++;
      };
      if (callback) {
        (function exec() {
          setTimeout(function() {
            if (editLength > maxEditLength || Date.now() > abortAfterTimestamp) {
              return callback(void 0);
            }
            if (!execEditLength()) {
              exec();
            }
          }, 0);
        })();
      } else {
        while (editLength <= maxEditLength && Date.now() <= abortAfterTimestamp) {
          const ret = execEditLength();
          if (ret) {
            return ret;
          }
        }
      }
    }
    addToPath(path, added, removed, oldPosInc, options) {
      const last = path.lastComponent;
      if (last && !options.oneChangePerToken && last.added === added && last.removed === removed) {
        return {
          oldPos: path.oldPos + oldPosInc,
          lastComponent: { count: last.count + 1, added, removed, previousComponent: last.previousComponent }
        };
      } else {
        return {
          oldPos: path.oldPos + oldPosInc,
          lastComponent: { count: 1, added, removed, previousComponent: last }
        };
      }
    }
    extractCommon(basePath, newTokens, oldTokens, diagonalPath, options) {
      const newLen = newTokens.length, oldLen = oldTokens.length;
      let oldPos = basePath.oldPos, newPos = oldPos - diagonalPath, commonCount = 0;
      while (newPos + 1 < newLen && oldPos + 1 < oldLen && this.equals(oldTokens[oldPos + 1], newTokens[newPos + 1], options)) {
        newPos++;
        oldPos++;
        commonCount++;
        if (options.oneChangePerToken) {
          basePath.lastComponent = { count: 1, previousComponent: basePath.lastComponent, added: false, removed: false };
        }
      }
      if (commonCount && !options.oneChangePerToken) {
        basePath.lastComponent = { count: commonCount, previousComponent: basePath.lastComponent, added: false, removed: false };
      }
      basePath.oldPos = oldPos;
      return newPos;
    }
    equals(left, right, options) {
      if (options.comparator) {
        return options.comparator(left, right);
      } else {
        return left === right || !!options.ignoreCase && left.toLowerCase() === right.toLowerCase();
      }
    }
    removeEmpty(array) {
      const ret = [];
      for (let i2 = 0; i2 < array.length; i2++) {
        if (array[i2]) {
          ret.push(array[i2]);
        }
      }
      return ret;
    }
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    castInput(value, options) {
      return value;
    }
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    tokenize(value, options) {
      return Array.from(value);
    }
    join(chars) {
      return chars.join("");
    }
    postProcess(changeObjects, options) {
      return changeObjects;
    }
    get useLongestToken() {
      return false;
    }
    buildValues(lastComponent, newTokens, oldTokens) {
      const components = [];
      let nextComponent;
      while (lastComponent) {
        components.push(lastComponent);
        nextComponent = lastComponent.previousComponent;
        delete lastComponent.previousComponent;
        lastComponent = nextComponent;
      }
      components.reverse();
      const componentLen = components.length;
      let componentPos = 0, newPos = 0, oldPos = 0;
      for (; componentPos < componentLen; componentPos++) {
        const component = components[componentPos];
        if (!component.removed) {
          if (!component.added && this.useLongestToken) {
            let value = newTokens.slice(newPos, newPos + component.count);
            value = value.map(function(value2, i2) {
              const oldValue = oldTokens[oldPos + i2];
              return oldValue.length > value2.length ? oldValue : value2;
            });
            component.value = this.join(value);
          } else {
            component.value = this.join(newTokens.slice(newPos, newPos + component.count));
          }
          newPos += component.count;
          if (!component.added) {
            oldPos += component.count;
          }
        } else {
          component.value = this.join(oldTokens.slice(oldPos, oldPos + component.count));
          oldPos += component.count;
        }
      }
      return components;
    }
  }
  class LineDiff extends Diff {
    constructor() {
      super(...arguments);
      this.tokenize = tokenize;
    }
    equals(left, right, options) {
      if (options.ignoreWhitespace) {
        if (!options.newlineIsToken || !left.includes("\n")) {
          left = left.trim();
        }
        if (!options.newlineIsToken || !right.includes("\n")) {
          right = right.trim();
        }
      } else if (options.ignoreNewlineAtEof && !options.newlineIsToken) {
        if (left.endsWith("\n")) {
          left = left.slice(0, -1);
        }
        if (right.endsWith("\n")) {
          right = right.slice(0, -1);
        }
      }
      return super.equals(left, right, options);
    }
  }
  const lineDiff = new LineDiff();
  function diffLines(oldStr, newStr, options) {
    return lineDiff.diff(oldStr, newStr, options);
  }
  function tokenize(value, options) {
    if (options.stripTrailingCr) {
      value = value.replace(/\r\n/g, "\n");
    }
    const retLines = [], linesAndNewlines = value.split(/(\n|\r\n)/);
    if (!linesAndNewlines[linesAndNewlines.length - 1]) {
      linesAndNewlines.pop();
    }
    for (let i2 = 0; i2 < linesAndNewlines.length; i2++) {
      const line = linesAndNewlines[i2];
      if (i2 % 2 && !options.newlineIsToken) {
        retLines[retLines.length - 1] += line;
      } else {
        retLines.push(line);
      }
    }
    return retLines;
  }
  function needsQuoting(s) {
    for (let i2 = 0; i2 < s.length; i2++) {
      if (s[i2] < " " || s[i2] > "~" || s[i2] === '"' || s[i2] === "\\") {
        return true;
      }
    }
    return false;
  }
  function quoteFileNameIfNeeded(s) {
    if (!needsQuoting(s)) {
      return s;
    }
    let result = '"';
    const bytes = new TextEncoder().encode(s);
    let i2 = 0;
    while (i2 < bytes.length) {
      const b = bytes[i2];
      if (b === 7) {
        result += "\\a";
      } else if (b === 8) {
        result += "\\b";
      } else if (b === 9) {
        result += "\\t";
      } else if (b === 10) {
        result += "\\n";
      } else if (b === 11) {
        result += "\\v";
      } else if (b === 12) {
        result += "\\f";
      } else if (b === 13) {
        result += "\\r";
      } else if (b === 34) {
        result += '\\"';
      } else if (b === 92) {
        result += "\\\\";
      } else if (b >= 32 && b <= 126) {
        result += String.fromCharCode(b);
      } else {
        result += "\\" + b.toString(8).padStart(3, "0");
      }
      i2++;
    }
    result += '"';
    return result;
  }
  const INCLUDE_HEADERS = {
    includeIndex: true,
    includeUnderline: true,
    includeFileHeaders: true
  };
  function structuredPatch(oldFileName, newFileName, oldStr, newStr, oldHeader, newHeader, options) {
    let optionsObj;
    {
      optionsObj = {};
    }
    if (typeof optionsObj.context === "undefined") {
      optionsObj.context = 4;
    }
    const context = optionsObj.context;
    if (optionsObj.newlineIsToken) {
      throw new Error("newlineIsToken may not be used with patch-generation functions, only with diffing functions");
    }
    if (!optionsObj.callback) {
      return diffLinesResultToPatch(diffLines(oldStr, newStr, optionsObj));
    } else {
      const { callback } = optionsObj;
      diffLines(oldStr, newStr, Object.assign(Object.assign({}, optionsObj), { callback: (diff) => {
        const patch = diffLinesResultToPatch(diff);
        callback(patch);
      } }));
    }
    function diffLinesResultToPatch(diff) {
      if (!diff) {
        return;
      }
      diff.push({ value: "", lines: [] });
      function contextLines(lines) {
        return lines.map(function(entry) {
          return " " + entry;
        });
      }
      const hunks = [];
      let oldRangeStart = 0, newRangeStart = 0, curRange = [], oldLine = 1, newLine = 1;
      for (let i2 = 0; i2 < diff.length; i2++) {
        const current = diff[i2], lines = current.lines || splitLines(current.value);
        current.lines = lines;
        if (current.added || current.removed) {
          if (!oldRangeStart) {
            const prev = diff[i2 - 1];
            oldRangeStart = oldLine;
            newRangeStart = newLine;
            if (prev) {
              curRange = context > 0 ? contextLines(prev.lines.slice(-context)) : [];
              oldRangeStart -= curRange.length;
              newRangeStart -= curRange.length;
            }
          }
          for (const line of lines) {
            curRange.push((current.added ? "+" : "-") + line);
          }
          if (current.added) {
            newLine += lines.length;
          } else {
            oldLine += lines.length;
          }
        } else {
          if (oldRangeStart) {
            if (lines.length <= context * 2 && i2 < diff.length - 2) {
              for (const line of contextLines(lines)) {
                curRange.push(line);
              }
            } else {
              const contextSize = Math.min(lines.length, context);
              for (const line of contextLines(lines.slice(0, contextSize))) {
                curRange.push(line);
              }
              const hunk = {
                oldStart: oldRangeStart,
                oldLines: oldLine - oldRangeStart + contextSize,
                newStart: newRangeStart,
                newLines: newLine - newRangeStart + contextSize,
                lines: curRange
              };
              hunks.push(hunk);
              oldRangeStart = 0;
              newRangeStart = 0;
              curRange = [];
            }
          }
          oldLine += lines.length;
          newLine += lines.length;
        }
      }
      for (const hunk of hunks) {
        for (let i2 = 0; i2 < hunk.lines.length; i2++) {
          if (hunk.lines[i2].endsWith("\n")) {
            hunk.lines[i2] = hunk.lines[i2].slice(0, -1);
          } else {
            hunk.lines.splice(i2 + 1, 0, "\\ No newline at end of file");
            i2++;
          }
        }
      }
      return {
        oldFileName,
        newFileName,
        oldHeader,
        newHeader,
        hunks
      };
    }
  }
  function formatPatch(patch, headerOptions) {
    var _a2, _b2, _c, _d, _e, _f;
    if (!headerOptions) {
      headerOptions = INCLUDE_HEADERS;
    }
    if (Array.isArray(patch)) {
      if (patch.length > 1 && !headerOptions.includeFileHeaders && !patch.every((p) => p.isGit)) {
        throw new Error("Cannot omit file headers on a multi-file patch. (The result would be unparseable; how would a tool trying to apply the patch know which changes are to which file?)");
      }
      return patch.map((p) => formatPatch(p, headerOptions)).join("\n");
    }
    const ret = [];
    if (patch.isGit) {
      headerOptions = INCLUDE_HEADERS;
      if (!patch.oldFileName) {
        throw new Error("oldFileName must be specified for Git patches");
      }
      if (!patch.newFileName) {
        throw new Error("newFileName must be specified for Git patches");
      }
      let gitOldName = patch.oldFileName;
      let gitNewName = patch.newFileName;
      if (patch.isCreate && gitOldName === "/dev/null") {
        gitOldName = gitNewName.replace(/^b\//, "a/");
      } else if (patch.isDelete && gitNewName === "/dev/null") {
        gitNewName = gitOldName.replace(/^a\//, "b/");
      }
      ret.push("diff --git " + quoteFileNameIfNeeded(gitOldName) + " " + quoteFileNameIfNeeded(gitNewName));
      if (patch.isDelete) {
        ret.push("deleted file mode " + ((_a2 = patch.oldMode) !== null && _a2 !== void 0 ? _a2 : "100644"));
      }
      if (patch.isCreate) {
        ret.push("new file mode " + ((_b2 = patch.newMode) !== null && _b2 !== void 0 ? _b2 : "100644"));
      }
      if (patch.oldMode && patch.newMode && !patch.isDelete && !patch.isCreate) {
        ret.push("old mode " + patch.oldMode);
        ret.push("new mode " + patch.newMode);
      }
      if (patch.isRename) {
        ret.push("rename from " + quoteFileNameIfNeeded(((_c = patch.oldFileName) !== null && _c !== void 0 ? _c : "").replace(/^a\//, "")));
        ret.push("rename to " + quoteFileNameIfNeeded(((_d = patch.newFileName) !== null && _d !== void 0 ? _d : "").replace(/^b\//, "")));
      }
      if (patch.isCopy) {
        ret.push("copy from " + quoteFileNameIfNeeded(((_e = patch.oldFileName) !== null && _e !== void 0 ? _e : "").replace(/^a\//, "")));
        ret.push("copy to " + quoteFileNameIfNeeded(((_f = patch.newFileName) !== null && _f !== void 0 ? _f : "").replace(/^b\//, "")));
      }
    } else {
      if (headerOptions.includeIndex && patch.oldFileName == patch.newFileName && patch.oldFileName !== void 0) {
        ret.push("Index: " + patch.oldFileName);
      }
      if (headerOptions.includeUnderline) {
        ret.push("===================================================================");
      }
    }
    const hasHunks = patch.hunks.length > 0;
    if (headerOptions.includeFileHeaders && patch.oldFileName !== void 0 && patch.newFileName !== void 0 && (!patch.isGit || hasHunks)) {
      ret.push("--- " + quoteFileNameIfNeeded(patch.oldFileName) + (patch.oldHeader ? "	" + patch.oldHeader : ""));
      ret.push("+++ " + quoteFileNameIfNeeded(patch.newFileName) + (patch.newHeader ? "	" + patch.newHeader : ""));
    }
    for (let i2 = 0; i2 < patch.hunks.length; i2++) {
      const hunk = patch.hunks[i2];
      const oldStart = hunk.oldLines === 0 ? hunk.oldStart - 1 : hunk.oldStart;
      const newStart = hunk.newLines === 0 ? hunk.newStart - 1 : hunk.newStart;
      ret.push("@@ -" + oldStart + "," + hunk.oldLines + " +" + newStart + "," + hunk.newLines + " @@");
      for (const line of hunk.lines) {
        ret.push(line);
      }
    }
    return ret.join("\n") + "\n";
  }
  function createTwoFilesPatch(oldFileName, newFileName, oldStr, newStr, oldHeader, newHeader, options) {
    {
      const patchObj = structuredPatch(oldFileName, newFileName, oldStr, newStr, oldHeader, newHeader);
      if (!patchObj) {
        return;
      }
      return formatPatch(patchObj, void 0);
    }
  }
  function createPatch(fileName, oldStr, newStr, oldHeader, newHeader, options) {
    return createTwoFilesPatch(fileName, fileName, oldStr, newStr, oldHeader, newHeader);
  }
  function splitLines(text) {
    const hasTrailingNl = text.endsWith("\n");
    const result = text.split("\n").map((line) => line + "\n");
    if (hasTrailingNl) {
      result.pop();
    } else {
      result.push(result.pop().slice(0, -1));
    }
    return result;
  }
  const VIBEPOLISH_SESSION_FORMAT = "vibepolish-session/v1";
  async function buildSessionFileTransaction(beforeFiles, afterFiles) {
    const beforeByPath = sourceFilesByPath(beforeFiles);
    const afterByPath = sourceFilesByPath(afterFiles);
    const paths = [.../* @__PURE__ */ new Set([...beforeByPath.keys(), ...afterByPath.keys()])].sort();
    const transactions = await Promise.all(paths.map(async (path) => {
      const beforeContent = beforeByPath.get(path);
      const afterContent = afterByPath.get(path);
      if (beforeContent == null || afterContent == null || beforeContent === afterContent) return null;
      return {
        path,
        beforeHash: await sha256(beforeContent),
        afterHash: await sha256(afterContent),
        reversePatch: createPatch(path, afterContent, beforeContent)
      };
    }));
    return transactions.filter((transaction) => !!transaction);
  }
  function createVibePolishSession(sourceName, snapshots) {
    return {
      format: VIBEPOLISH_SESSION_FORMAT,
      sourceName,
      snapshots: snapshots.map((snapshot) => {
        var _a2;
        return {
          id: String(snapshot.id || ""),
          label: String(snapshot.label || ""),
          createdAt: String(snapshot.createdAt || ""),
          edits: serializableRecords(snapshot.edits || []),
          transaction: normalizeSessionTransaction(snapshot.transaction || []),
          capture: ((_a2 = snapshot.capture) == null ? void 0 : _a2.imageDataUrl) ? { imageDataUrl: String(snapshot.capture.imageDataUrl) } : null
        };
      })
    };
  }
  function normalizeVibePolishSession(value) {
    if (!value || typeof value !== "object") return null;
    const candidate = value;
    if (candidate.format !== VIBEPOLISH_SESSION_FORMAT || !Array.isArray(candidate.snapshots)) return null;
    return createVibePolishSession(String(candidate.sourceName || ""), candidate.snapshots);
  }
  function sourceFilesByPath(files) {
    const result = /* @__PURE__ */ new Map();
    (files || []).forEach((file) => {
      const path = normalizedSourcePath(file == null ? void 0 : file.path);
      if (!path) return;
      result.set(path, String(file.content ?? ""));
    });
    return result;
  }
  function normalizeSessionTransaction(transaction) {
    return (transaction || []).flatMap((file) => {
      const path = normalizedSourcePath(file == null ? void 0 : file.path);
      if (!path) return [];
      return [{
        path,
        beforeHash: String(file.beforeHash ?? ""),
        afterHash: String(file.afterHash ?? ""),
        reversePatch: String(file.reversePatch ?? "")
      }];
    });
  }
  async function sha256(content) {
    const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(content));
    return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
  }
  function serializableRecords(records) {
    return JSON.parse(JSON.stringify(records || []));
  }
  function normalizedSourcePath(value) {
    const normalized = String(value || "").replace(/\\/g, "/").replace(/^\/+/, "");
    if (!normalized || normalized.split("/").some((part) => part === "..")) return "";
    return normalized;
  }
  const BRIDGE_SCRIPT_ID = "dt-freeze-bridge-script";
  function freezeBridgeScriptSource() {
    return `;(${installFreezeBridge.toString()})();`;
  }
  function injectFreezeBridgeIntoHtml(html, options = {}) {
    if (String(html).includes(`id="${BRIDGE_SCRIPT_ID}"`)) return String(html);
    const prelude = options.scriptSrc ? `<script id="${BRIDGE_SCRIPT_ID}" src="${options.scriptSrc}"><\/script>` : `<script id="${BRIDGE_SCRIPT_ID}">${freezeBridgeScriptSource()}<\/script>`;
    if (/<head[\s>]/i.test(html)) return String(html).replace(/<head([^>]*)>/i, `<head$1>${prelude}`);
    return prelude + html;
  }
  function installFreezeBridge() {
    var _a2;
    if (window.__dtFreezeBridge) return;
    const native = {
      setTimeout: window.setTimeout.bind(window),
      clearTimeout: window.clearTimeout.bind(window),
      setInterval: window.setInterval.bind(window),
      clearInterval: window.clearInterval.bind(window),
      requestAnimationFrame: window.requestAnimationFrame ? window.requestAnimationFrame.bind(window) : null,
      cancelAnimationFrame: window.cancelAnimationFrame ? window.cancelAnimationFrame.bind(window) : null,
      dateNow: Date.now.bind(Date),
      perfNow: ((_a2 = window.performance) == null ? void 0 : _a2.now) ? window.performance.now.bind(window.performance) : null
    };
    const control = {
      paused: false,
      interactionFrozen: false,
      seq: 1,
      tasks: /* @__PURE__ */ new Map(),
      frozenWall: 0,
      frozenPerf: 0,
      pauseWall: 0,
      pausePerf: 0
    };
    const blockedInteractionEvents = [
      "pointerover",
      "pointerout",
      "pointerenter",
      "pointerleave",
      "pointermove",
      "pointerdown",
      "pointerup",
      "pointercancel",
      "mouseover",
      "mouseout",
      "mouseenter",
      "mouseleave",
      "mousemove",
      "mousedown",
      "mouseup",
      "click",
      "dblclick",
      "contextmenu",
      "focus",
      "blur",
      "focusin",
      "focusout",
      "keydown",
      "keyup",
      "keypress",
      "wheel",
      "scroll",
      "touchstart",
      "touchmove",
      "touchend",
      "touchcancel",
      "dragstart",
      "drag",
      "dragend",
      "drop"
    ];
    const blockInteraction = (event) => {
      if (!control.interactionFrozen) return;
      if (event.cancelable) event.preventDefault();
      event.stopImmediatePropagation();
    };
    blockedInteractionEvents.forEach((type) => window.addEventListener(type, blockInteraction, true));
    const virtualDateNow = () => control.paused ? control.pauseWall - control.frozenWall : native.dateNow() - control.frozenWall;
    const virtualPerfNow = () => {
      if (!native.perfNow) return 0;
      return control.paused ? control.pausePerf - control.frozenPerf : native.perfNow() - control.frozenPerf;
    };
    const normalizedDelay = (value) => Math.max(0, Number(value) || 0);
    const clearNativeTask = (task) => {
      var _a3;
      if (!task || task.nativeId == null) return;
      if (task.type === "raf") (_a3 = native.cancelAnimationFrame) == null ? void 0 : _a3.call(native, task.nativeId);
      else native.clearTimeout(task.nativeId);
      task.nativeId = null;
    };
    const scheduleTimeoutTask = (task) => {
      if (control.paused || !control.tasks.has(task.id)) return;
      const remaining = Math.max(0, task.deadline - virtualPerfNow());
      task.nativeId = native.setTimeout(() => fireTimeoutTask(task.id), remaining);
    };
    const fireTimeoutTask = (id) => {
      const task = control.tasks.get(id);
      if (!task || control.paused) return;
      if (virtualPerfNow() + 1 < task.deadline) {
        scheduleTimeoutTask(task);
        return;
      }
      control.tasks.delete(id);
      task.nativeId = null;
      if (typeof task.cb === "function") task.cb(...task.args);
    };
    const scheduleIntervalTask = (task) => {
      if (control.paused || !control.tasks.has(task.id)) return;
      const remaining = Math.max(0, task.deadline - virtualPerfNow());
      task.nativeId = native.setTimeout(() => fireIntervalTask(task.id), remaining);
    };
    const fireIntervalTask = (id) => {
      const task = control.tasks.get(id);
      if (!task || control.paused) return;
      const now = virtualPerfNow();
      if (now + 1 < task.deadline) {
        scheduleIntervalTask(task);
        return;
      }
      if (typeof task.cb === "function") task.cb(...task.args);
      const step = Math.max(task.delay, 1);
      do
        task.deadline += step;
      while (task.deadline <= now);
      scheduleIntervalTask(task);
    };
    const scheduleRafTask = (task) => {
      if (control.paused || !native.requestAnimationFrame || !control.tasks.has(task.id)) return;
      task.nativeId = native.requestAnimationFrame(() => {
        if (!control.tasks.has(task.id) || control.paused) return;
        control.tasks.delete(task.id);
        task.nativeId = null;
        if (typeof task.cb === "function") task.cb(virtualPerfNow());
      });
    };
    const suspendNativeTasks = () => control.tasks.forEach(clearNativeTask);
    const resumeNativeTasks = () => control.tasks.forEach((task) => {
      if (task.type === "timeout") scheduleTimeoutTask(task);
      else if (task.type === "interval") scheduleIntervalTask(task);
      else if (task.type === "raf") scheduleRafTask(task);
    });
    const pauseScheduler = () => {
      if (control.paused) return;
      control.pauseWall = native.dateNow();
      control.pausePerf = native.perfNow ? native.perfNow() : 0;
      control.paused = true;
      suspendNativeTasks();
    };
    const resumeScheduler = () => {
      if (!control.paused) return;
      control.frozenWall += native.dateNow() - control.pauseWall;
      if (native.perfNow) control.frozenPerf += native.perfNow() - control.pausePerf;
      control.paused = false;
      resumeNativeTasks();
    };
    Date.now = virtualDateNow;
    if (window.performance && native.perfNow) {
      try {
        Object.defineProperty(window.performance, "now", { value: virtualPerfNow, configurable: true });
      } catch {
      }
    }
    window.setTimeout = (cb, delay = 0, ...args) => {
      const id = control.seq++;
      const task = { id, type: "timeout", nativeId: null, cb, args, deadline: virtualPerfNow() + normalizedDelay(delay) };
      control.tasks.set(id, task);
      scheduleTimeoutTask(task);
      return id;
    };
    window.clearTimeout = (id) => {
      const task = control.tasks.get(id);
      if (!task) return native.clearTimeout(id);
      clearNativeTask(task);
      control.tasks.delete(id);
    };
    window.setInterval = (cb, delay = 0, ...args) => {
      const id = control.seq++;
      const normalized = normalizedDelay(delay);
      const task = { id, type: "interval", nativeId: null, cb, args, delay: normalized, deadline: virtualPerfNow() + normalized };
      control.tasks.set(id, task);
      scheduleIntervalTask(task);
      return id;
    };
    window.clearInterval = (id) => {
      const task = control.tasks.get(id);
      if (!task) return native.clearInterval(id);
      clearNativeTask(task);
      control.tasks.delete(id);
    };
    if (native.requestAnimationFrame && native.cancelAnimationFrame) {
      window.requestAnimationFrame = (cb) => {
        const id = control.seq++;
        const task = { id, type: "raf", nativeId: null, cb };
        control.tasks.set(id, task);
        scheduleRafTask(task);
        return id;
      };
      window.cancelAnimationFrame = (id) => {
        const task = control.tasks.get(id);
        if (!task) return native.cancelAnimationFrame(id);
        clearNativeTask(task);
        control.tasks.delete(id);
      };
    }
    window.__dtFreezeBridge = {
      freeze() {
        var _a3;
        if (control.interactionFrozen && control.paused) return;
        control.interactionFrozen = true;
        pauseScheduler();
        (_a3 = document.documentElement) == null ? void 0 : _a3.classList.add("dt-force-paused", "dt-interaction-frozen");
      },
      resume() {
        var _a3;
        if (!control.interactionFrozen && !control.paused) return;
        resumeScheduler();
        control.interactionFrozen = false;
        (_a3 = document.documentElement) == null ? void 0 : _a3.classList.remove("dt-force-paused", "dt-interaction-frozen");
      },
      state() {
        return { frozen: control.interactionFrozen, paused: control.paused, pendingTasks: control.tasks.size };
      }
    };
  }
  function startLegacyFreezeEditor(options) {
    var _a2;
    const { runtimeSource, sourceName, testMode, runtimeDebug, panelStore, cdpStyleProvider } = options;
    const runtimeMode = options.mode === "review" ? "review" : "edit";
    const initialSession = normalizeVibePolishSession(options.session);
    const sourceHtml = runtimeSource.kind === "single-html" ? runtimeSource.html : "";
    const ENABLE_EXPORT_TEST_BRIDGE = testMode;
    const ENABLE_RUNTIME_DEBUG = !!runtimeDebug || isRuntimeDebugEnabled();
    const frame = $("#dt-frame");
    const feedback = createRuntimeFeedback(document, navigator);
    const SETTLE_IDLE_MS = 600;
    const CDP_PROBE_ATTR = "data-vibepolish-cdp-style-id";
    panelStore == null ? void 0 : panelStore.publish(createInitialPanelViewModel(sourceName));
    panelStore == null ? void 0 : panelStore.setCommandDispatcher(dispatchPanelCommand);
    const state = {
      paused: false,
      frozen: false,
      selectMode: false,
      selected: null,
      selectedRaw: null,
      selectionPromoted: false,
      visualSelection: null,
      objectLadder: [],
      objectIndex: 0,
      scopeLadder: [],
      scopeIndex: 0,
      groupResult: null,
      frozenSignature: null,
      group: [],
      scope: "one",
      hovered: null,
      hoveredRaw: null,
      summaryPreviewRefs: [],
      lastHoverPoint: null,
      interactionDocument: null,
      runtimeDocuments: /* @__PURE__ */ new Set(),
      runtimeDocumentObservers: /* @__PURE__ */ new Map(),
      runtimeFrameDocuments: /* @__PURE__ */ new WeakMap(),
      hoverHot: null,
      hoverHosts: [],
      hoverPrimaryHost: null,
      hoverStateLocked: false,
      hoverMirrorRegistry: [],
      focusLocks: [],
      focusStateLocked: false,
      focusMirrorRegistry: [],
      inputShield: null,
      viewportLock: null,
      snapshots: ((initialSession == null ? void 0 : initialSession.snapshots) || []).map((snapshot) => ({ ...snapshot, persisted: true })),
      edits: ((initialSession == null ? void 0 : initialSession.snapshots) || []).flatMap((snapshot) => snapshot.edits || []),
      draft: null,
      activeTab: ((_a2 = initialSession == null ? void 0 : initialSession.snapshots) == null ? void 0 : _a2.length) ? initialSession.snapshots.length - 1 : "empty",
      dirty: false,
      captureMode: "now",
      settleArmed: false,
      hoverEditSeq: 0,
      selectionBreadthRules: [],
      selectionBreadthRuleSeq: 0,
      selectionBreadthWriteSeqByProp: /* @__PURE__ */ new Map(),
      selectionBreadthCurrentPlanCache: null,
      selectionBreadthWritePlanRevision: 0,
      selectionBreadthWritePlanPrepareSeq: 0,
      selectionBreadthWritePlansLoading: false,
      selectionBreadthWritePlansReadyRevision: -1,
      selectionBreadthWritePlanAttemptedProps: /* @__PURE__ */ new Set(),
      selectionBreadthScopeSeq: 0,
      selectionBreadthPlanningStateContext: null,
      selectionPlanningRevision: 0,
      selectionPlanningJobSeq: 0,
      selectionPlanningJob: null,
      selectionStateContext: null,
      tableScopeView: "current-table",
      tableScopePlan: null,
      pendingStyleWrites: /* @__PURE__ */ new Set(),
      styleApplyTimers: /* @__PURE__ */ new Map(),
      styleApplyQueued: /* @__PURE__ */ new Map(),
      styleApplyInFlight: /* @__PURE__ */ new Set(),
      revertTransaction: null,
      activeColor: null,
      colorFormat: "rgba",
      iroPicker: null,
      suppressColorPickerChange: false,
      colorInputTimers: /* @__PURE__ */ new Map(),
      colorDocBound: false,
      familyDocBound: false,
      fontUnitDocBound: false,
      widthUnitDocBound: false,
      weightDocBound: false,
      failedControls: /* @__PURE__ */ new Map(),
      densityExpanded: false,
      explicitLayoutValues: /* @__PURE__ */ new Map(),
      cdpProbeSeq: 0,
      cdpProbeAttributes: /* @__PURE__ */ new Set(),
      cdpPseudoDebugSeq: 0,
      cdpProviderConnected: null
    };
    const explicitLayout = createExplicitLayoutValueController({
      values: state.explicitLayoutValues,
      getVisualSelection: () => state.visualSelection,
      getScope: () => state.scope,
      resolveCurrentStyleRoute,
      cssPath
    });
    const visualIds = /* @__PURE__ */ new WeakMap();
    const originalCursorByElement = /* @__PURE__ */ new WeakMap();
    let visualIdSeq = 0;
    function recordCdpPseudoDebug(event, detail = {}) {
      if (!ENABLE_RUNTIME_DEBUG) return null;
      const w = win();
      const entry = {
        seq: ++state.cdpPseudoDebugSeq,
        time: (/* @__PURE__ */ new Date()).toISOString(),
        event,
        ...detail
      };
      const log = Array.isArray(w.__DESIGNTOOLS_CDP_PSEUDO_LOG__) ? w.__DESIGNTOOLS_CDP_PSEUDO_LOG__ : [];
      log.push(entry);
      if (log.length > 200) log.splice(0, log.length - 200);
      w.__DESIGNTOOLS_CDP_PSEUDO_LOG__ = log;
      try {
        console.debug("[vibepolish-cdp-pseudo]", entry);
      } catch {
      }
      return entry;
    }
    function recordFlowDebug(event, detail = {}) {
      if (!ENABLE_RUNTIME_DEBUG) return null;
      let w = null;
      try {
        w = win();
      } catch {
      }
      if (!w) return null;
      const entry = { time: (/* @__PURE__ */ new Date()).toISOString(), event, ...detail };
      const log = Array.isArray(w.__DT_FLOW_DEBUG__) ? w.__DT_FLOW_DEBUG__ : [];
      log.push(entry);
      if (log.length > 500) log.splice(0, log.length - 500);
      w.__DT_FLOW_DEBUG__ = log;
      return entry;
    }
    function isRuntimeDebugEnabled() {
      var _a3;
      try {
        if (((_a3 = window.localStorage) == null ? void 0 : _a3.getItem("DESIGNTOOLS_DEBUG")) === "1") return true;
        return !!window.__DESIGNTOOLS_DEBUG__;
      } catch {
        return false;
      }
    }
    loadSource();
    setupExportTestBridge();
    function loadSource(afterLoad) {
      state.runtimeDocumentObservers.forEach((observer) => observer.disconnect());
      state.runtimeDocumentObservers.clear();
      state.runtimeDocuments.clear();
      state.interactionDocument = null;
      frame.addEventListener("load", () => {
        installFrameRuntime();
        if (afterLoad) afterLoad();
        renderAll();
      }, { once: true });
      if (runtimeSource.kind === "project") {
        frame.removeAttribute("srcdoc");
        frame.src = runtimeSource.url;
        return;
      }
      frame.removeAttribute("src");
      frame.srcdoc = prepareSourceHtml(runtimeSource.html);
    }
    function prepareSourceHtml(html) {
      return injectFreezeBridgeIntoHtml(html);
    }
    function installFrameRuntime() {
      installDocumentRuntime(frame.contentDocument);
    }
    function installDocumentRuntime(d) {
      var _a3, _b2, _c;
      if (!d || state.runtimeDocuments.has(d)) return;
      state.runtimeDocuments.add(d);
      recordFlowDebug("runtime-document-installed", { url: ((_a3 = d.location) == null ? void 0 : _a3.href) || "" });
      const style = d.createElement("style");
      style.id = "dt-freeze-runtime-style";
      style.textContent = `
      .dt-hover-hot{cursor:crosshair!important}
      .dt-mark-layer{position:fixed!important;inset:0!important;z-index:2147483647!important;pointer-events:none!important}
      .dt-mark-box{position:fixed!important;box-sizing:border-box!important;pointer-events:none!important;background:transparent!important}
      .dt-mark-box-picked{border:2px solid #1661ab!important;box-shadow:0 0 0 1px rgba(255,255,255,.85)!important}
      .dt-mark-box-group{border:2px dashed #1661ab!important}
      .dt-mark-box-hover{border:2px dashed #c03030!important}
      .dt-mark-box-summary{border:2px solid #1661ab!important;background:rgba(22,97,171,.08)!important;box-shadow:0 0 0 2px rgba(255,255,255,.9)!important}
      .dt-input-shield{position:fixed!important;inset:0!important;z-index:2147483646!important;background:transparent!important;cursor:crosshair!important;pointer-events:auto!important}
      .dt-force-paused *, .dt-force-paused *::before, .dt-force-paused *::after{animation-play-state:paused!important;transition-duration:0s!important}
    `;
      d.head.appendChild(style);
      try {
        installProbeMutationDebug(d);
      } catch (error) {
        recordFlowDebug("runtime-probe-observer-error", {
          url: ((_b2 = d.location) == null ? void 0 : _b2.href) || "",
          error: (error == null ? void 0 : error.message) || String(error)
        });
      }
      d.addEventListener("mousemove", onFrameMouseMove, true);
      d.addEventListener("pointermove", onFrameMouseMove, true);
      d.addEventListener("click", onFrameClick, true);
      const settleEvents = ["pointermove", "pointerdown", "pointerup", "mousedown", "mouseup", "click", "wheel", "touchstart", "touchmove", "touchend", "keydown", "keyup", "scroll"];
      settleEvents.forEach((type) => d.addEventListener(type, onSettleActivity, true));
      d.addEventListener("scroll", scheduleOverlayRender, true);
      (_c = d.defaultView) == null ? void 0 : _c.addEventListener("resize", onFrameResize);
      ["pointerdown", "mousedown", "mouseup", "click", "dblclick", "blur", "focusout", "keydown"].forEach((type) => {
        d.addEventListener(type, (e) => {
          if (!state.frozen) return;
          if (state.selectMode && e.type === "click") return;
          if (e.type === "keydown" && e.key !== "Escape") return;
          e.stopPropagation();
        }, true);
      });
      if (state.frozen) d.documentElement.classList.add("dt-force-paused", "dt-interaction-frozen");
      installChildFrameRuntimes(d);
    }
    function installChildFrameRuntimes(d) {
      var _a3;
      const installFrame = (childFrame) => {
        const install = () => {
          const previousDocument = state.runtimeFrameDocuments.get(childFrame);
          const nextDocument = sameOriginFrameDocument(childFrame);
          if (previousDocument && previousDocument !== nextDocument) releaseDocumentRuntime(previousDocument);
          if (!nextDocument) return;
          state.runtimeFrameDocuments.set(childFrame, nextDocument);
          installDocumentRuntime(nextDocument);
        };
        childFrame.addEventListener("load", install);
        install();
      };
      d.querySelectorAll("iframe").forEach(installFrame);
      const Observer = (_a3 = d.defaultView) == null ? void 0 : _a3.MutationObserver;
      if (!Observer) return;
      const observer = new Observer((records) => {
        records.forEach((record) => record.addedNodes.forEach((node) => {
          var _a4, _b2;
          if (node.nodeType !== 1) return;
          if ((_a4 = node.matches) == null ? void 0 : _a4.call(node, "iframe")) installFrame(node);
          (_b2 = node.querySelectorAll) == null ? void 0 : _b2.call(node, "iframe").forEach(installFrame);
        }));
        records.forEach((record) => record.removedNodes.forEach((node) => {
          var _a4, _b2;
          if (node.nodeType !== 1) return;
          if ((_a4 = node.matches) == null ? void 0 : _a4.call(node, "iframe")) releaseFrameRuntime(node);
          (_b2 = node.querySelectorAll) == null ? void 0 : _b2.call(node, "iframe").forEach(releaseFrameRuntime);
        }));
      });
      observer.observe(d.documentElement, { childList: true, subtree: true });
      state.runtimeDocumentObservers.set(d, observer);
    }
    function releaseFrameRuntime(childFrame) {
      const runtimeDocument = state.runtimeFrameDocuments.get(childFrame);
      if (runtimeDocument) releaseDocumentRuntime(runtimeDocument);
      state.runtimeFrameDocuments.delete(childFrame);
    }
    function releaseDocumentRuntime(runtimeDocument) {
      var _a3, _b2, _c;
      recordFlowDebug("runtime-document-released", { url: ((_a3 = runtimeDocument.location) == null ? void 0 : _a3.href) || "" });
      (_b2 = runtimeDocument.querySelectorAll) == null ? void 0 : _b2.call(runtimeDocument, "iframe").forEach(releaseFrameRuntime);
      (_c = state.runtimeDocumentObservers.get(runtimeDocument)) == null ? void 0 : _c.disconnect();
      state.runtimeDocumentObservers.delete(runtimeDocument);
      state.runtimeDocuments.delete(runtimeDocument);
      if (state.interactionDocument === runtimeDocument) state.interactionDocument = frame.contentDocument;
    }
    function installProbeMutationDebug(d) {
      var _a3;
      if (d.__dtProbeMutationDebugInstalled) return;
      const Observer = (_a3 = d.defaultView) == null ? void 0 : _a3.MutationObserver;
      if (!Observer) return;
      d.__dtProbeMutationDebugInstalled = true;
      const observer = new Observer((records) => {
        records.forEach((record) => {
          if (record.type !== "attributes" || record.attributeName !== CDP_PROBE_ATTR) return;
          recordFlowDebug("probe-attr-change", {
            attr: record.attributeName,
            oldValue: record.oldValue || "",
            newValue: record.target.getAttribute(record.attributeName) || "",
            target: cssPath(record.target),
            className: record.target.className || ""
          });
        });
      });
      observer.observe(d.documentElement, {
        subtree: true,
        attributes: true,
        attributeOldValue: true,
        attributeFilter: [CDP_PROBE_ATTR]
      });
    }
    function onFrameMouseMove(e) {
      var _a3;
      onSettleActivity(e);
      state.hoveredRaw = e.target && e.target.nodeType === 1 ? e.target : null;
      state.lastHoverPoint = { document: ((_a3 = e.target) == null ? void 0 : _a3.ownerDocument) || doc(), x: e.clientX, y: e.clientY };
      const target = normalizeTarget(e.target);
      state.hovered = target;
      if (!state.selected && (target == null ? void 0 : target.ownerDocument)) state.interactionDocument = target.ownerDocument;
      if (state.selectMode) renderHoverHot(target);
    }
    function onFrameResize(e) {
      scheduleOverlayRender();
      onSettleActivity(e);
    }
    function onSettleActivity(event) {
      if (!state.settleArmed) return;
      resetSettleTimer((event == null ? void 0 : event.type) || "activity");
    }
    function resetSettleTimer(reason) {
      if (!state.settleArmed) return;
      clearTimeout(state.settleTimer);
      state.settleTimer = setTimeout(() => {
        state.settleArmed = false;
        state.settleTimer = null;
        beginDraft("延迟快照");
      }, SETTLE_IDLE_MS);
    }
    function clearSettleTimer() {
      clearTimeout(state.settleTimer);
      state.settleTimer = null;
      state.settleArmed = false;
    }
    function onFrameClick(e) {
      if (!state.selectMode || !state.draft) return;
      e.preventDefault();
      e.stopPropagation();
      selectElement(e.target, e.altKey);
    }
    function installInteractionShield() {
      var _a3, _b2, _c;
      const d = doc();
      if (!d || ((_a3 = state.inputShield) == null ? void 0 : _a3.isConnected)) return;
      (_b2 = d.getElementById("dt-input-shield")) == null ? void 0 : _b2.remove();
      let shield = document.getElementById("dt-frame-shield");
      if (!shield) {
        shield = document.createElement("div");
        shield.id = "dt-frame-shield";
        shield.className = "dt-frame-shield";
        (_c = document.querySelector(".dt-stage")) == null ? void 0 : _c.appendChild(shield);
      }
      positionInteractionShield(shield);
      state.inputShield = shield;
      state.runtimeDocuments.forEach((runtimeDocument) => {
        var _a4;
        (_a4 = runtimeDocument.documentElement) == null ? void 0 : _a4.classList.add("dt-interaction-frozen");
      });
      shield.addEventListener("pointermove", onShieldPointerMove, true);
      shield.addEventListener("mousemove", onShieldPointerMove, true);
      shield.addEventListener("click", onShieldClick, true);
      ["pointerdown", "pointerup", "mousedown", "mouseup", "dblclick", "contextmenu", "wheel", "touchstart", "touchmove", "touchend", "keydown", "keyup"].forEach((type) => {
        shield.addEventListener(type, stopShieldEvent, { capture: true, passive: false });
      });
    }
    function removeInteractionShield() {
      state.runtimeDocuments.forEach((runtimeDocument) => {
        var _a3;
        (_a3 = runtimeDocument.documentElement) == null ? void 0 : _a3.classList.remove("dt-interaction-frozen");
      });
      if (state.inputShield) state.inputShield.remove();
      state.inputShield = null;
    }
    function positionInteractionShield(shield = state.inputShield) {
      const stage = document.querySelector(".dt-stage");
      if (!shield || !stage) return;
      shield.style.left = `${frame.offsetLeft}px`;
      shield.style.top = `${frame.offsetTop}px`;
      shield.style.width = `${frame.offsetWidth}px`;
      shield.style.height = `${frame.offsetHeight}px`;
    }
    function onShieldPointerMove(e) {
      e.preventDefault();
      e.stopPropagation();
      const target = hitTestFrozenPoint(e.clientX, e.clientY);
      state.hovered = target;
      if (state.selectMode) renderHoverHot(target);
    }
    function onShieldClick(e) {
      e.preventDefault();
      e.stopPropagation();
      if (!state.selectMode || !state.draft) return;
      const target = hitTestFrozenPoint(e.clientX, e.clientY);
      if (target) selectElement(target, e.altKey);
    }
    function stopShieldEvent(e) {
      e.preventDefault();
      e.stopPropagation();
    }
    function hitTestFrozenPoint(x2, y) {
      const target = hitTestFrozenStack(x2, y).find(isBusinessHitTestElement);
      if (!target) return null;
      state.interactionDocument = target.ownerDocument;
      return normalizeTarget(target);
    }
    function hitTestFrozenStack(x2, y) {
      const d = doc();
      if (!d) return [];
      const rect = frame.getBoundingClientRect();
      const frameX = x2 - rect.left;
      const frameY = y - rect.top;
      return deepElementsFromPoint(frame.contentDocument, frameX, frameY);
    }
    function isBusinessHitTestElement(el) {
      return !!el && el.nodeType === 1 && !isRuntimeHitTestElement(el);
    }
    function isRuntimeHitTestElement(el) {
      var _a3, _b2;
      if (!el || el.nodeType !== 1) return true;
      if (el.id === "dt-input-shield" || el.id === "dt-mark-layer" || el.id === "dt-frame-shield") return true;
      if ((_a3 = el.classList) == null ? void 0 : _a3.contains("dt-mark-box")) return true;
      if ((_b2 = el.closest) == null ? void 0 : _b2.call(el, "#dt-mark-layer")) return true;
      return false;
    }
    async function beginDraft(label) {
      var _a3;
      if (state.draft && !confirm("当前快照还没有应用，是否丢弃并创建新快照？")) return;
      clearSettleTimer();
      if (label === "延迟快照") {
        await lockHoverAtLastPoint();
        await lockFocusAtCurrentElement();
      } else {
        await clearForceHover("begin-normal-draft");
        await clearForceFocus("begin-normal-draft");
      }
      pauseDemo();
      installInteractionShield();
      state.selectMode = true;
      state.selected = null;
      state.selectionStateContext = null;
      state.selectedRaw = null;
      state.selectionPromoted = false;
      state.visualSelection = null;
      state.objectLadder = [];
      state.objectIndex = 0;
      state.scopeLadder = [];
      state.scopeIndex = 0;
      state.groupResult = null;
      state.frozenSignature = null;
      state.group = [];
      state.scope = "one";
      clearControlFailures();
      state.draft = {
        id: `draft-${String(state.snapshots.length + 1).padStart(3, "0")}`,
        label,
        htmlBefore: currentHtml(),
        editBase: state.edits.length,
        hoverStyleBefore: ((_a3 = doc().getElementById("dt-hover-edit-style")) == null ? void 0 : _a3.textContent) ?? null,
        sourceBeforePromise: captureCurrentSourceState(),
        createdAt: (/* @__PURE__ */ new Date()).toISOString()
      };
      state.activeTab = "draft";
      $("#dt-select").classList.add("dt-active");
      setStatus(`${label} / 编辑中`);
      renderAll();
      toast(`${label}已冻结，可直接选择编辑。`);
    }
    function armSettleSnapshot() {
      state.settleArmed = true;
      clearTimeout(state.settleTimer);
      state.settleTimer = null;
      renderAll();
      toast(`延迟快照已开启：停止输入 ${SETTLE_IDLE_MS}ms 后冻结。`);
    }
    function setCaptureMode(mode) {
      if (state.draft || state.settleArmed || state.frozen || state.selectMode) {
        toast("当前快照未结束，请先应用或取消。");
        renderCaptureMode();
        return;
      }
      state.captureMode = mode;
      clearSettleTimer();
      renderCaptureMode();
      toast(mode === "settle" ? "已切换为延迟快照。" : "已切换为普通快照。");
    }
    function startSelectionFlow() {
      if (state.draft || state.settleArmed) {
        toast("当前快照未结束，请使用底部取消退出。");
        renderCaptureMode();
        return;
      }
      if (state.captureMode === "settle") armSettleSnapshot();
      else {
        clearSettleTimer();
        beginDraft("快照");
      }
    }
    function pauseDemo() {
      state.paused = true;
      state.frozen = true;
      lockFrameViewport();
      state.runtimeDocuments.forEach((runtimeDocument) => {
        var _a3, _b2, _c;
        (_a3 = runtimeDocument.documentElement) == null ? void 0 : _a3.classList.add("dt-force-paused");
        (_c = (_b2 = runtimeDocument.defaultView) == null ? void 0 : _b2.__dtFreezeBridge) == null ? void 0 : _c.freeze();
      });
    }
    function resumeDemo() {
      removeInteractionShield();
      clearHoverHot();
      clearMarks();
      clearForceHover("resume-demo");
      clearForceFocus("resume-demo");
      unlockFrameViewport();
      state.paused = false;
      state.frozen = false;
      state.selectMode = false;
      $("#dt-select").classList.remove("dt-active");
      state.runtimeDocuments.forEach((runtimeDocument) => {
        var _a3, _b2, _c;
        (_a3 = runtimeDocument.documentElement) == null ? void 0 : _a3.classList.remove("dt-force-paused");
        (_c = (_b2 = runtimeDocument.defaultView) == null ? void 0 : _b2.__dtFreezeBridge) == null ? void 0 : _c.resume();
      });
      setStatus("浏览中");
    }
    function lockFrameViewport() {
      if (state.viewportLock) return;
      const stage = document.querySelector(".dt-stage");
      const rect = frame.getBoundingClientRect();
      state.viewportLock = {
        width: rect.width,
        height: rect.height,
        frameWidth: frame.style.width,
        frameHeight: frame.style.height
      };
      if (stage) stage.classList.add("dt-viewport-locked");
      frame.style.width = `${Math.max(1, Math.round(rect.width))}px`;
      frame.style.height = `${Math.max(1, Math.round(rect.height))}px`;
    }
    function unlockFrameViewport() {
      if (!state.viewportLock) return;
      const stage = document.querySelector(".dt-stage");
      frame.style.width = state.viewportLock.frameWidth || "";
      frame.style.height = state.viewportLock.frameHeight || "";
      if (stage) stage.classList.remove("dt-viewport-locked");
      state.viewportLock = null;
    }
    async function applyDraft() {
      if (!state.draft) return;
      if (!hasDraftEdits()) {
        toast("请先修改内容，再应用快照。");
        return;
      }
      await flushQueuedStyleApplies();
      await waitForPendingStyleWrites();
      clearSettleTimer();
      const sourceBefore = await state.draft.sourceBeforePromise;
      const sourceAfter = await captureCurrentSourceState();
      const transaction = await buildSessionFileTransaction(sourceBefore.files || [], sourceAfter.files || []);
      clearHoverHot();
      await nextVisualFrame();
      const capture = await captureCurrentReviewImage();
      clearMarks();
      const snap = {
        id: `snap-${String(state.snapshots.length + 1).padStart(3, "0")}`,
        label: state.draft.label,
        edits: state.edits.slice(state.draft.editBase),
        transaction,
        capture,
        persisted: false,
        createdAt: (/* @__PURE__ */ new Date()).toISOString()
      };
      state.snapshots.push(snap);
      state.activeTab = state.snapshots.length - 1;
      await clearForceHover("apply-draft");
      await clearForceFocus("apply-draft");
      state.draft = null;
      state.dirty = true;
      resetDraftRuntimeState();
      resumeDemo();
      renderAll();
      toast("已应用并保存快照。");
    }
    function hasDraftEdits() {
      if (!state.draft) return false;
      return state.edits.slice(state.draft.editBase).some((edit) => edit.applied !== false);
    }
    function nextVisualFrame() {
      return new Promise((resolve) => requestAnimationFrame(() => resolve()));
    }
    async function waitForPendingStyleWrites() {
      var _a3;
      while ((_a3 = state.pendingStyleWrites) == null ? void 0 : _a3.size) {
        const pending = [...state.pendingStyleWrites];
        await Promise.allSettled(pending);
      }
    }
    async function cancelDraft() {
      if (!state.draft && !state.settleArmed) return;
      clearSettleTimer();
      if (!state.draft) {
        resetDraftRuntimeState();
        resumeDemo();
        renderAll();
        toast("已取消选择。");
        return;
      }
      const draft = state.draft;
      const reverted = await runRevertTransaction("cancel-draft", state.edits.slice(draft.editBase));
      if (!reverted) return;
      restoreDraftHoverStyle(draft);
      await clearForceHover("cancel-draft");
      await clearForceFocus("cancel-draft");
      state.edits = state.edits.slice(0, draft.editBase);
      state.draft = null;
      state.activeTab = state.snapshots.length ? state.snapshots.length - 1 : "empty";
      state.explicitLayoutValues.clear();
      resetDraftRuntimeState();
      resumeDemo();
      renderAll();
      toast("已取消，未保存快照。");
    }
    async function rollbackSnapshot(index) {
      var _a3;
      if (state.draft || state.settleArmed) {
        toast("当前快照未结束，请先应用或取消。");
        return;
      }
      if (index !== state.snapshots.length - 1) {
        toast("当前只支持回退最新快照。");
        return;
      }
      const snap = state.snapshots[index];
      if (!snap) return;
      if (snap.persisted && ((_a3 = snap.transaction) == null ? void 0 : _a3.length)) {
        const reverted2 = await rollbackPersistedSnapshot(index, snap);
        if (reverted2) toast("已回退该快照。");
        return;
      }
      const reverted = await runRevertTransaction("rollback-snapshot", snap.edits || []);
      if (!reverted) return;
      const editSet = new Set(snap.edits || []);
      state.edits = state.edits.filter((edit) => !editSet.has(edit));
      state.snapshots.splice(index, 1);
      state.activeTab = state.snapshots.length ? state.snapshots.length - 1 : "empty";
      state.dirty = true;
      resetDraftRuntimeState();
      resumeDemo();
      renderAll();
      toast("已回退该快照。");
    }
    async function rollbackPersistedSnapshot(index, snap) {
      var _a3, _b2;
      if (state.revertTransaction) {
        toast("正在处理上一次回退，请稍候。");
        return false;
      }
      const provider = currentCdpStyleProvider();
      if (typeof provider !== "function") {
        toast("后台服务未连接，无法回退已恢复的快照。");
        return false;
      }
      state.revertTransaction = "rollback-persisted-snapshot";
      try {
        const result = await provider({
          action: "restoreSessionTransaction",
          files: snap.transaction
        });
        if (!(result == null ? void 0 : result.ok)) throw new Error((result == null ? void 0 : result.error) || "Session transaction restore failed");
        if (runtimeSource.kind === "single-html") {
          const restored = ((_a3 = result.restoredFiles) == null ? void 0 : _a3.find((file) => file.path === runtimeSource.file)) || ((_b2 = result.restoredFiles) == null ? void 0 : _b2[0]);
          if (restored) runtimeSource.html = restored.content;
        }
        const editSet = new Set(snap.edits || []);
        state.edits = state.edits.filter((edit) => !editSet.has(edit));
        state.snapshots.splice(index, 1);
        state.activeTab = state.snapshots.length ? state.snapshots.length - 1 : "empty";
        state.dirty = true;
        resetDraftRuntimeState();
        loadSource(() => {
          resumeDemo();
          renderAll();
        });
        return true;
      } catch (error) {
        recordFlowDebug("persisted-snapshot-rollback-failed", {
          snapshotId: snap.id || "",
          error: (error == null ? void 0 : error.message) || String(error)
        });
        toast("快照回退失败，项目文件可能已变化。");
        return false;
      } finally {
        state.revertTransaction = null;
      }
    }
    async function runRevertTransaction(kind, edits) {
      if (state.revertTransaction) {
        toast("正在处理上一次回退，请稍候。");
        return false;
      }
      state.revertTransaction = kind;
      clearQueuedStyleApplies();
      try {
        await waitForPendingStyleWrites();
        await revertEditList(edits);
        return true;
      } catch (error) {
        recordFlowDebug("revert-transaction-failed", {
          kind,
          editCount: (edits == null ? void 0 : edits.length) || 0,
          error: (error == null ? void 0 : error.message) || String(error)
        });
        toast(kind === "rollback-snapshot" ? "快照回退失败，原快照和页面样式已保留。" : "取消失败，当前修改仍然保留。");
        return false;
      } finally {
        state.revertTransaction = null;
      }
    }
    function resetDraftRuntimeState() {
      state.selected = null;
      state.interactionDocument = frame.contentDocument;
      state.selectionStateContext = null;
      state.selectedRaw = null;
      state.selectionPromoted = false;
      state.visualSelection = null;
      state.objectLadder = [];
      state.objectIndex = 0;
      state.scopeLadder = [];
      state.scopeIndex = 0;
      state.groupResult = null;
      state.frozenSignature = null;
      state.group = [];
      state.scope = "one";
      state.tableScopeView = "current-table";
      state.tableScopePlan = null;
      state.selectionBreadthScopeSeq += 1;
      state.selectionBreadthWritePlanPrepareSeq += 1;
      state.selectionBreadthWritePlansLoading = false;
      state.selectionBreadthWritePlansReadyRevision = -1;
      state.selectionBreadthWriteSeqByProp.clear();
      clearQueuedStyleApplies();
      invalidateSelectionBreadthWritePlanCache();
      clearControlFailures();
      clearCdpProbeTargets();
      closeTransientEditors();
    }
    function closeTransientEditors() {
      resetColorPopover();
      ["dt-family-field", "dt-weight-field", "dt-font-unit-field", "dt-width-unit-field"].forEach((id) => {
        var _a3;
        (_a3 = $("#" + id)) == null ? void 0 : _a3.classList.remove("dt-open");
      });
    }
    function selectElement(raw, single) {
      state.interactionDocument = (raw == null ? void 0 : raw.ownerDocument) || frame.contentDocument;
      const ladder = buildObjectLadder(raw);
      const visual = resolveVisualSelection(raw);
      const index = Math.max(0, ladder.findIndex((item) => item.anchor === visual.anchor));
      state.objectLadder = ladder.length ? ladder : [visual];
      state.objectIndex = index >= 0 ? index : 0;
      activateObjectSelection(state.objectIndex, { single });
    }
    function activateObjectSelection(index, options2 = {}) {
      const ladder = state.objectLadder.length ? state.objectLadder : state.visualSelection ? [state.visualSelection] : [];
      if (!ladder.length) return;
      const visual = ladder[Math.max(0, Math.min(index, ladder.length - 1))];
      const raw = visual.raw || state.selectedRaw || visual.anchor;
      const el = visual.anchor;
      clearHoverHot();
      state.selected = el;
      state.selectedRaw = raw;
      state.selectionPromoted = !!(raw && el && raw !== el);
      state.selectionStateContext = confirmedStateContextForSelection();
      state.tableScopeView = "current-table";
      state.tableScopePlan = null;
      state.visualSelection = visual;
      state.objectIndex = ladder.indexOf(visual);
      state.frozenSignature = buildFrozenSignature(visual);
      invalidateSelectionBreadthWritePlanCache();
      clearControlFailures();
      state.scopeLadder = options2.single ? [selectionBreadthSingleScope(visual, "alt-single")] : initialScopeLadderForVisual(visual);
      state.scopeIndex = options2.single ? 0 : defaultScopeIndex(state.scopeLadder);
      applyScopeSelection(state.scopeIndex);
      startSelectionBreadthWritePlanPreparation();
      syncControls();
      renderAll();
      if (!options2.single) refreshSelectionBreadthScopes(visual);
    }
    function applyScopeSelection(index) {
      const ladder = state.scopeLadder.length ? state.scopeLadder : [selectionBreadthSingleScope(state.visualSelection, "empty-scope")];
      state.scopeIndex = Math.max(0, Math.min(index, ladder.length - 1));
      state.groupResult = ladder[state.scopeIndex];
      state.group = state.groupResult.members;
      state.scope = state.group.length < 2 ? "one" : "group";
      invalidateSelectionBreadthWritePlanCache();
      clearControlFailures();
    }
    function invalidateSelectionBreadthWritePlanCache() {
      state.selectionBreadthWritePlanRevision += 1;
      invalidateSelectionPlanningJob("selection-changed");
      state.selectionBreadthCurrentPlanCache = null;
      state.selectionBreadthWritePlansReadyRevision = -1;
      state.selectionBreadthWritePlanAttemptedProps.clear();
    }
    function invalidateSelectionPlanningJob(reason) {
      state.selectionPlanningRevision += 1;
      const job = state.selectionPlanningJob;
      if (job && job.status === "running") {
        job.status = "cancelled";
        job.cancelReason = reason;
      }
    }
    function beginSelectionPlanningJob(kind) {
      var _a3, _b2;
      const previous = state.selectionPlanningJob;
      if (previous && previous.status === "running") {
        previous.status = "cancelled";
        previous.cancelReason = "superseded";
      }
      const job = {
        id: `selection-plan-${state.selectionPlanningRevision}-${++state.selectionPlanningJobSeq}`,
        revision: state.selectionPlanningRevision,
        kind,
        status: "running",
        cancelReason: "",
        selectionAnchor: ((_a3 = state.visualSelection) == null ? void 0 : _a3.anchor) || state.selected || null,
        selectionOwner: cssPath(((_b2 = state.visualSelection) == null ? void 0 : _b2.anchor) || state.selected || doc().body)
      };
      state.selectionPlanningJob = job;
      return job;
    }
    function isSelectionPlanningJobCurrent(job) {
      var _a3, _b2;
      return !!job && job.status === "running" && job.revision === state.selectionPlanningRevision && job.selectionAnchor === (((_a3 = state.visualSelection) == null ? void 0 : _a3.anchor) || state.selected || null) && ((_b2 = state.selectionPlanningJob) == null ? void 0 : _b2.id) === job.id;
    }
    function finishSelectionPlanningJob(job, status) {
      var _a3;
      if (!job || ((_a3 = state.selectionPlanningJob) == null ? void 0 : _a3.id) !== job.id) return;
      job.status = status;
    }
    function initialScopeLadderForVisual(visual) {
      if (!(visual == null ? void 0 : visual.anchor)) return [selectionBreadthSingleScope(visual, "missing-anchor")];
      if (isTransientStateContext(currentSelectionStateContext())) return [selectionBreadthSingleScope(visual, "transient-state-current")];
      if (closestCell(visual.anchor)) {
        return [
          selectionBreadthSingleScope({ ...visual, anchor: closestCell(visual.anchor) }, "table-cell"),
          selectionBreadthLoadingScope({ ...visual, anchor: closestCell(visual.anchor) })
        ];
      }
      return [
        selectionBreadthSingleScope(visual, "current"),
        selectionBreadthLoadingScope(visual)
      ];
    }
    async function refreshSelectionBreadthScopes(visual) {
      var _a3;
      if (!(visual == null ? void 0 : visual.anchor)) return;
      if (isTransientStateContext(currentSelectionStateContext())) return;
      if (closestCell(visual.anchor)) {
        refreshTableSelectionBreadthScopes(visual);
        return;
      }
      const seq = ++state.selectionBreadthScopeSeq;
      const similarPlan = await buildSelectionBreadthPlanForBreadth({
        props: cdpClassificationAnchorProperties(),
        breadth: "similar-kind",
        selectionOwner: visual.anchor
      });
      if (seq !== state.selectionBreadthScopeSeq || ((_a3 = state.visualSelection) == null ? void 0 : _a3.anchor) !== visual.anchor) return;
      if (!similarPlan.cdpStyleInfoAvailable) {
        settleSelectionBreadthScopeToSingle(visual, "cdp-unavailable");
        return;
      }
      const allPlan = createSelectionBreadthPlanSync({
        ...selectionBreadthPlanBaseInput(cdpClassificationAnchorProperties(), "all-kind", {
          selectionOwner: visual.anchor,
          stateContext: similarPlan.stateContext || currentSelectionStateContext()
        }),
        breadth: "all-kind",
        cdpStyleInfo: similarPlan.cdpStyleInfo || null
      });
      const scopes = [
        selectionBreadthSingleScope(visual, "current"),
        selectionBreadthScopeFromPlan(similarPlan, "selection-similar-kind", "同视觉类型"),
        selectionBreadthScopeFromPlan(allPlan, "selection-all-kind", "全部结构同类")
      ].filter(Boolean);
      const next = uniqueScopeResults(scopes);
      if (next.length <= 1) {
        state.scopeLadder = [selectionBreadthSingleScope(visual, "current")];
      } else {
        state.scopeLadder = next;
      }
      state.scopeIndex = defaultScopeIndex(state.scopeLadder);
      applyScopeSelection(state.scopeIndex);
      startSelectionBreadthWritePlanPreparation();
      syncControls();
      renderAll();
    }
    function settleSelectionBreadthScopeToSingle(visual, reason = "fallback-single") {
      if (!(visual == null ? void 0 : visual.anchor)) return;
      state.scopeLadder = [selectionBreadthSingleScope(visual, reason)];
      state.scopeIndex = 0;
      applyScopeSelection(0);
      startSelectionBreadthWritePlanPreparation();
      syncControls();
      renderAll();
    }
    async function refreshTableSelectionBreadthScopes(visual) {
      var _a3;
      const cell = closestCell(visual.anchor);
      if (!cell) return;
      const seq = ++state.selectionBreadthScopeSeq;
      const tablePlan = await createTableScopePlan(visual, cell);
      if (seq !== state.selectionBreadthScopeSeq || closestCell((_a3 = state.visualSelection) == null ? void 0 : _a3.anchor) !== cell) return;
      if (!(tablePlan == null ? void 0 : tablePlan.cdpStyleInfoAvailable)) {
        settleSelectionBreadthScopeToSingle({ ...visual, anchor: cell }, "table-cdp-unavailable");
        return;
      }
      state.tableScopePlan = tablePlan;
      state.scopeLadder = tableScopeLadderForView(tablePlan, state.tableScopeView || "current-table");
      state.scopeIndex = defaultScopeIndex(state.scopeLadder);
      applyScopeSelection(state.scopeIndex);
      startSelectionBreadthWritePlanPreparation();
      syncControls();
      renderAll();
    }
    async function createTableScopePlan(visual, cell) {
      var _a3;
      const currentTable = cell.closest("table");
      const row = cell.parentElement;
      const rowIndex = row ? [...currentTable.querySelectorAll("tr")].indexOf(row) : -1;
      const columnIndex = row ? tableCellChildren(row).indexOf(cell) : -1;
      const allSimilarTables = similarTablesFor(currentTable).filter((table) => table !== currentTable);
      const tableUniverse = uniqueElements2([currentTable, ...allSimilarTables]).filter(Boolean).filter(isVisible);
      const candidateCells = uniqueElements2(tableUniverse.flatMap((table) => [...table.querySelectorAll("td,th")].filter(isVisible)));
      const plan = await buildSelectionBreadthPlanForBreadth({
        props: cdpClassificationAnchorProperties(),
        selectionOwner: cell,
        breadth: "similar-kind",
        parentScope: "all-similar-parents",
        candidateScope: candidateCells,
        fixedUniverse: tableUniverse
      });
      const fullSimilarCells = uniqueElements2(((_a3 = plan.currentVisualGroup) == null ? void 0 : _a3.items) || [cell]).filter((el) => {
        var _a4;
        return (_a4 = el.matches) == null ? void 0 : _a4.call(el, "td,th");
      });
      const compatibleTables = tableUniverse.filter((table) => tableHasCellAt(table, rowIndex, columnIndex));
      const fallbackReasons = [
        ...plan.fallbackReasons || [],
        ...tableUniverse.filter((table) => !compatibleTables.includes(table)).map((table) => `similar table excluded from all-similar view because row/column ${rowIndex}/${columnIndex} was not stable: ${cssPath(table)}`)
      ];
      const currentTableSimilarCells = fullSimilarCells.filter((item) => item.closest("table") === currentTable);
      const currentTableRowCells = tableRowCells(currentTable, rowIndex);
      const currentTableColumnCells = tableColumnCells(currentTable, columnIndex);
      const currentTableAllCells = tableAllCells(currentTable);
      const allSimilarTableCells = fullSimilarCells.filter((item) => compatibleTables.includes(item.closest("table")));
      const allSimilarTablesRowCells = uniqueElements2(compatibleTables.flatMap((table) => tableRowCells(table, rowIndex)));
      const allSimilarTablesColumnCells = uniqueElements2(compatibleTables.flatMap((table) => tableColumnCells(table, columnIndex)));
      const allSimilarTablesAllCells = uniqueElements2(compatibleTables.flatMap((table) => tableAllCells(table)));
      const signature = stableScopeKey(fullSimilarCells);
      return {
        id: `table-plan-${signature}`,
        signature,
        selectionCell: cell,
        currentTable,
        tableUniverse,
        allSimilarTables,
        compatibleTables,
        candidateCells,
        fullSimilarCells,
        cdpStyleInfo: plan.cdpStyleInfo || null,
        cdpStyleInfoAvailable: !!plan.cdpStyleInfoAvailable,
        rowIndex,
        columnIndex,
        fallbackReasons,
        views: {
          "current-table": [
            tableScope(cell, [cell], "selection-single", "单个单元格", "current-table", signature, fullSimilarCells, "single"),
            tableScope(cell, currentTableSimilarCells, "selection-table-similar-cells", "同表相似单元格", "current-table", signature, fullSimilarCells, "similar"),
            tableScope(cell, currentTableRowCells, "selection-table-row", "当前行", "current-table", signature, fullSimilarCells, "row"),
            tableScope(cell, currentTableColumnCells, "selection-table-column", "当前列", "current-table", signature, fullSimilarCells, "column"),
            tableScope(cell, currentTableAllCells, "selection-table-all-cells", "整表单元格", "current-table", signature, fullSimilarCells, "all")
          ],
          "all-similar-tables": [
            tableScope(cell, [cell], "selection-single", "当前单元格", "all-similar-tables", signature, fullSimilarCells, "single"),
            tableScope(cell, allSimilarTableCells, "selection-table-all-similar-cells", "所有相似表格中的相似单元格", "all-similar-tables", signature, fullSimilarCells, "similar"),
            tableScope(cell, allSimilarTablesRowCells, "selection-table-all-similar-rows", "所有相似表格中的对应行", "all-similar-tables", signature, fullSimilarCells, "row"),
            tableScope(cell, allSimilarTablesColumnCells, "selection-table-all-similar-columns", "所有相似表格中的对应列", "all-similar-tables", signature, fullSimilarCells, "column"),
            tableScope(cell, allSimilarTablesAllCells, "selection-table-all-similar-cells-all", "所有相似表格单元格", "all-similar-tables", signature, fullSimilarCells, "all")
          ]
        }
      };
    }
    function similarTablesFor(currentTable) {
      if (!currentTable) return [];
      const root = boundedAreaSearchRoot(currentTable);
      const baseFp = GroupEngine.buildFingerprint(currentTable);
      const primaryClasses = stableClasses(currentTable);
      const candidates = [currentTable, ...root.querySelectorAll("table")].filter(isVisible);
      return uniqueElements2(candidates).filter((table) => {
        if (table === currentTable) return true;
        const score = GroupEngine.scoreCandidate(baseFp, GroupEngine.buildFingerprint(table));
        const sharesClass = primaryClasses.length && primaryClasses.some((cls) => table.classList.contains(cls));
        return score >= (sharesClass ? 0.52 : 0.64);
      });
    }
    function tableScopeLadderForView(tablePlan, view) {
      var _a3;
      if (!((_a3 = tablePlan == null ? void 0 : tablePlan.views) == null ? void 0 : _a3[view])) return [];
      return mergeTableScopes(tablePlan.views[view].filter((scope) => {
        var _a4;
        return (_a4 = scope == null ? void 0 : scope.members) == null ? void 0 : _a4.length;
      }));
    }
    function mergeTableScopes(scopes) {
      var _a3, _b2;
      const priority = { single: 1, similar: 2, row: 3, column: 4, all: 5 };
      const byKey = /* @__PURE__ */ new Map();
      for (const scope of scopes) {
        const key = stableScopeKey(scope.members || []);
        const current = byKey.get(key);
        if (!current || (priority[(_a3 = scope.evidence) == null ? void 0 : _a3.scopeKind] || 0) > (priority[(_b2 = current.evidence) == null ? void 0 : _b2.scopeKind] || 0)) {
          byKey.set(key, scope);
        }
      }
      return scopes.map((scope) => byKey.get(stableScopeKey(scope.members || []))).filter((scope, index, list) => scope && list.indexOf(scope) === index);
    }
    function tableScope(anchor, members, mode, label, view, planSignature, fullSimilarCells, scopeKind) {
      const visibleMembers = uniqueElements2(members || []).filter(isVisible);
      if (!visibleMembers.length) return null;
      const selector = visibleMembers.map(tableCellEffectiveSelector).join(",");
      return {
        anchor,
        members: visibleMembers,
        mode,
        confidence: 0.94,
        effectiveGroupSelector: selector,
        effectiveSelectorMode: "table-axis-materialized",
        effectiveSelectorVerification: {
          ok: true,
          selector,
          expectedCount: visibleMembers.length,
          actualCount: visibleMembers.length,
          extra: [],
          missing: []
        },
        evidence: {
          source: "selection-breadth",
          tableAxis: true,
          label,
          view,
          scopeKind,
          tablePlanSignature: planSignature,
          fullSimilarCells: fullSimilarCells.map(cssPath),
          fullSimilarCount: fullSimilarCells.length
        },
        rejected: []
      };
    }
    function stableScopeKey(cells) {
      return uniqueElements2(cells || []).map((cell) => visualIdFor(cell)).sort().join("|");
    }
    function tableHasCellAt(table, rowIndex, columnIndex) {
      return !!tableCellAt(table, rowIndex, columnIndex);
    }
    function tableCellAt(table, rowIndex, columnIndex) {
      const row = [...(table == null ? void 0 : table.querySelectorAll("tr")) || []][rowIndex];
      if (!row) return null;
      return tableCellChildren(row)[columnIndex] || null;
    }
    function tableRowCells(table, rowIndex) {
      const row = [...(table == null ? void 0 : table.querySelectorAll("tr")) || []][rowIndex];
      return tableCellChildren(row).filter(isVisible);
    }
    function tableColumnCells(table, columnIndex) {
      return [...(table == null ? void 0 : table.querySelectorAll("tr")) || []].map((row) => tableCellChildren(row)[columnIndex]).filter(Boolean).filter(isVisible);
    }
    function tableAllCells(table) {
      return [...(table == null ? void 0 : table.querySelectorAll("td,th")) || []].filter(isVisible);
    }
    function tableCellEffectiveSelector(cell) {
      var _a3;
      const table = (_a3 = cell == null ? void 0 : cell.closest) == null ? void 0 : _a3.call(cell, "table");
      const row = cell == null ? void 0 : cell.parentElement;
      if (!table || !row) return strictElementSelector(cell);
      const rowIndex = [...table.querySelectorAll("tr")].indexOf(row) + 1;
      const cellIndex = tableCellChildren(row).indexOf(cell) + 1;
      const tag = cell.tagName.toLowerCase();
      return `${tableEffectiveSelector(table)} tr:nth-of-type(${rowIndex}) > ${tag}:nth-of-type(${cellIndex})`;
    }
    function tableEffectiveSelector(table) {
      const id = table.getAttribute("id");
      if (id) {
        const selector = `#${CSS.escape(id)}`;
        try {
          if (doc().querySelectorAll(selector).length === 1) return selector;
        } catch {
        }
      }
      return strictElementSelector(table);
    }
    function strictElementSelector(el) {
      if (!el || el === doc().documentElement) return "html";
      const parts = [];
      let node = el;
      while (node && node.nodeType === 1 && node !== doc().documentElement) {
        const parent = node.parentElement;
        const tag = node.tagName.toLowerCase();
        if (node.id) {
          const selector = `#${CSS.escape(node.id)}`;
          try {
            if (doc().querySelectorAll(selector).length === 1) {
              parts.unshift(selector);
              break;
            }
          } catch {
          }
        }
        if (!parent) {
          parts.unshift(tag);
          break;
        }
        const siblings = [...parent.children].filter((child) => child.tagName === node.tagName);
        parts.unshift(siblings.length > 1 ? `${tag}:nth-of-type(${siblings.indexOf(node) + 1})` : tag);
        node = parent;
      }
      return parts.join(" > ");
    }
    function selectionBreadthSingleScope(visual, reason = "current") {
      const anchor = (visual == null ? void 0 : visual.anchor) || null;
      return {
        anchor,
        members: anchor ? [anchor] : [],
        mode: "selection-single",
        confidence: anchor ? 0.96 : 0,
        evidence: { source: "selection-breadth", reason },
        rejected: []
      };
    }
    function selectionBreadthLoadingScope(visual) {
      const anchor = (visual == null ? void 0 : visual.anchor) || null;
      return {
        anchor,
        members: anchor ? [anchor] : [],
        mode: "selection-breadth-loading",
        confidence: 0,
        evidence: { source: "selection-breadth", loading: true, label: "计算广度轴" },
        rejected: []
      };
    }
    function selectionBreadthScopeFromPlan(plan, mode, label) {
      var _a3, _b2;
      if (!((_a3 = plan == null ? void 0 : plan.targetGroups) == null ? void 0 : _a3.length)) return null;
      const members = uniqueElements2(plan.targetGroups.flatMap((group) => group.items || [])).filter(isVisible);
      if (!members.length) return null;
      return {
        anchor: plan.selectionOwner,
        members,
        mode,
        confidence: ((_b2 = plan.fallbackReasons) == null ? void 0 : _b2.length) ? 0.7 : 0.9,
        evidence: {
          source: "selection-breadth",
          label,
          breadth: plan.breadth,
          parentScope: plan.parentScope,
          currentParent: cssPath(plan.currentParent),
          similarParents: (plan.similarParents || []).map((el) => cssPath(el)).slice(0, 20),
          visualGroups: (plan.visualGroups || []).map((group) => ({
            id: group.id,
            count: group.items.length,
            selector: group.classificationSelector || "",
            mode: group.classificationSelectorMode || ""
          })),
          fallbackReasons: plan.fallbackReasons || []
        },
        selectionPlan: summarizeSelectionBreadthPlan(plan),
        rejected: []
      };
    }
    function uniqueScopeResults(scopes) {
      const seen = /* @__PURE__ */ new Set();
      return scopes.filter((scope) => {
        const key = (scope.members || []).map((el) => visualIdFor(el)).sort().join("|");
        if (!key || seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    }
    function defaultScopeIndex(ladder) {
      var _a3;
      if (!(ladder == null ? void 0 : ladder.length)) return 0;
      const loadingIndex = ladder.findIndex((item) => item.mode === "selection-breadth-loading");
      if (loadingIndex >= 0) return loadingIndex;
      const breadthIndex = ladder.findIndex((item) => {
        var _a4;
        return item.mode === "selection-similar-kind" && ((_a4 = item.members) == null ? void 0 : _a4.length) > 1;
      });
      if (breadthIndex >= 0) return breadthIndex;
      const hasOrdinaryBreadthAxis = ladder.some(
        (item) => item.mode === "selection-similar-kind" || item.mode === "selection-all-kind"
      );
      if (hasOrdinaryBreadthAxis) return 0;
      const candidates = ladder.map((item, index) => ({ item, index })).filter((entry) => {
        var _a4;
        return ((_a4 = entry.item.members) == null ? void 0 : _a4.length) > 1 && (entry.item.confidence || 0) >= 0.58;
      }).sort((a, b) => (b.item.confidence || 0) - (a.item.confidence || 0));
      return ((_a3 = candidates[0]) == null ? void 0 : _a3.index) || 0;
    }
    function stepObject(delta) {
      if (!state.objectLadder.length) return;
      activateObjectSelection(state.objectIndex + delta, { single: false });
    }
    function stepScope(delta) {
      if (!state.scopeLadder.length) return;
      applyScopeSelection(state.scopeIndex + delta);
      startSelectionBreadthWritePlanPreparation();
      syncControls();
      renderAll();
    }
    function setTableScopeView(view) {
      var _a3, _b2;
      if (!state.tableScopePlan) return;
      const currentScopeKind = ((_b2 = (_a3 = state.groupResult) == null ? void 0 : _a3.evidence) == null ? void 0 : _b2.scopeKind) || "";
      state.tableScopeView = view === "all-similar-tables" ? "all-similar-tables" : "current-table";
      state.scopeLadder = tableScopeLadderForView(state.tableScopePlan, state.tableScopeView);
      const nextIndex = state.scopeLadder.findIndex((scope) => {
        var _a4;
        return ((_a4 = scope.evidence) == null ? void 0 : _a4.scopeKind) === currentScopeKind;
      });
      state.scopeIndex = nextIndex >= 0 ? nextIndex : defaultScopeIndex(state.scopeLadder);
      applyScopeSelection(state.scopeIndex);
      startSelectionBreadthWritePlanPreparation();
      syncControls();
      renderAll();
    }
    function applyText(value) {
      if (!state.selected) return;
      const route = resolveCurrentStyleRoute("textContent");
      const list = route.targets;
      if (!list.length || !list.every(isStructurallyEditableTextSelection) || !hasConsistentTextContent(list)) {
        toast("该选区包含复杂子元素，不能直接编辑文案。");
        return;
      }
      const before = list.map((el) => el.textContent);
      list.forEach((el) => {
        el.textContent = value;
      });
      recordEdit({
        kind: "textContent",
        route: route.route,
        value,
        before,
        sourcePaths: uniqueValues2(list.map((el) => sourcePathForDocument(el.ownerDocument)).filter(Boolean)),
        sourceTargets: list.map((el, index) => ({
          path: sourcePathForDocument(el.ownerDocument),
          locator: sourceLocatorForElement(el),
          before: before[index] ?? "",
          after: value
        })),
        applyMode: list.length > 1 ? "text-bulk-same-value" : "text-single-leaf",
        suggestedImplementation: suggestedTextImplementation(list, before, value)
      }, list);
      scheduleLayoutSideEffectSync$1();
    }
    function sourceLocatorForElement(el) {
      const locator = [];
      let node = el;
      while (node && node.nodeType === 1) {
        const parent = node.parentElement;
        const sameTagSiblings = parent ? [...parent.children].filter((item) => item.tagName === node.tagName) : [node];
        locator.unshift({
          tagName: node.tagName.toLowerCase(),
          id: node.id || "",
          classes: [...node.classList].filter((name) => !name.startsWith("dt-")),
          nthOfType: Math.max(1, sameTagSiblings.indexOf(node) + 1)
        });
        if (node === el.ownerDocument.documentElement) break;
        node = parent;
      }
      return locator;
    }
    function applyStyle(prop, value) {
      if (state.styleApplyTimers.has(prop)) {
        clearTimeout(state.styleApplyTimers.get(prop));
        state.styleApplyTimers.delete(prop);
      }
      state.styleApplyQueued.set(prop, value);
      return trackPendingStyleWrite(runLatestStyleApply(prop));
    }
    function queueLatestStyleApply(prop, value, delay = 140) {
      state.styleApplyQueued.set(prop, value);
      if (state.styleApplyTimers.has(prop)) clearTimeout(state.styleApplyTimers.get(prop));
      const timer = setTimeout(() => {
        state.styleApplyTimers.delete(prop);
        trackPendingStyleWrite(runLatestStyleApply(prop));
      }, delay);
      state.styleApplyTimers.set(prop, timer);
    }
    function trackPendingStyleWrite(promise) {
      if (!promise || typeof promise.finally !== "function") return promise;
      state.pendingStyleWrites.add(promise);
      promise.finally(() => state.pendingStyleWrites.delete(promise));
      return promise;
    }
    async function runLatestStyleApply(prop) {
      if (state.styleApplyInFlight.has(prop)) return;
      state.styleApplyInFlight.add(prop);
      try {
        while (state.styleApplyQueued.has(prop)) {
          const value = state.styleApplyQueued.get(prop);
          state.styleApplyQueued.delete(prop);
          await applyStyleAsync(prop, value);
        }
      } finally {
        state.styleApplyInFlight.delete(prop);
        if (state.styleApplyQueued.has(prop)) runLatestStyleApply(prop);
      }
    }
    function clearQueuedStyleApplies() {
      var _a3, _b2, _c, _d, _e, _f, _g, _h;
      for (const timer of ((_b2 = (_a3 = state.styleApplyTimers) == null ? void 0 : _a3.values) == null ? void 0 : _b2.call(_a3)) || []) clearTimeout(timer);
      (_d = (_c = state.styleApplyTimers) == null ? void 0 : _c.clear) == null ? void 0 : _d.call(_c);
      (_f = (_e = state.styleApplyQueued) == null ? void 0 : _e.clear) == null ? void 0 : _f.call(_e);
      (_h = (_g = state.styleApplyInFlight) == null ? void 0 : _g.clear) == null ? void 0 : _h.call(_g);
    }
    async function flushQueuedStyleApplies() {
      var _a3, _b2, _c, _d, _e, _f;
      for (const timer of ((_b2 = (_a3 = state.styleApplyTimers) == null ? void 0 : _a3.values) == null ? void 0 : _b2.call(_a3)) || []) clearTimeout(timer);
      (_d = (_c = state.styleApplyTimers) == null ? void 0 : _c.clear) == null ? void 0 : _d.call(_c);
      const props = [...((_f = (_e = state.styleApplyQueued) == null ? void 0 : _e.keys) == null ? void 0 : _f.call(_e)) || []];
      await Promise.all(props.map((prop) => runLatestStyleApply(prop)));
    }
    async function applyStyleAsync(prop, value) {
      var _a3, _b2, _c, _d, _e, _f, _g;
      if (!state.selected) return;
      if (((_a3 = state.groupResult) == null ? void 0 : _a3.mode) === "selection-breadth-loading") {
        toast("广度轴仍在计算中，请稍候。");
        return;
      }
      if (state.selectionBreadthWritePlansLoading) {
        toast("写入规则仍在计算中，请稍候。");
        return;
      }
      const writeSeq = (state.selectionBreadthWriteSeqByProp.get(prop) || 0) + 1;
      state.selectionBreadthWriteSeqByProp.set(prop, writeSeq);
      const normalized = normalizeStyleValue(prop, value);
      if (value && normalized == null) {
        toast("当前样式值无效，未应用。");
        return;
      }
      const createWritePlan = (options2 = {}) => cachedSelectionBreadthWritePlan(prop, normalized, options2);
      recordFlowDebug("style-apply-start", {
        prop,
        value: normalized,
        selected: cssPath(state.selected),
        visualAnchor: cssPath((_b2 = state.visualSelection) == null ? void 0 : _b2.anchor),
        stateContext: ((_c = currentSelectionStateContext()) == null ? void 0 : _c.kind) || "default",
        scopeMode: ((_d = state.groupResult) == null ? void 0 : _d.mode) || "",
        scopeCount: ((_f = (_e = state.groupResult) == null ? void 0 : _e.members) == null ? void 0 : _f.length) || 0
      });
      let plan = await createWritePlan();
      if (writeSeq !== state.selectionBreadthWriteSeqByProp.get(prop)) return;
      if (!plan) {
        toast("当前选区没有可写入目标。");
        return;
      }
      recordFlowDebug("style-apply-plan", {
        prop,
        stateContext: ((_g = plan.stateContext) == null ? void 0 : _g.kind) || "default",
        cdpStyleInfoAvailable: !!plan.cdpStyleInfoAvailable,
        targetGroups: (plan.targetGroups || []).map((group) => {
          var _a4;
          return {
            id: group.id,
            count: ((_a4 = group.items) == null ? void 0 : _a4.length) || 0,
            selector: group.classificationSelector || "",
            items: (group.items || []).map((el) => cssPath(el))
          };
        }),
        writePlans: (plan.writePlans || []).map((writePlan) => {
          var _a4, _b3, _c2, _d2;
          return {
            groupId: writePlan.groupId || "",
            selector: writePlan.materializedSelector,
            writeMode: writePlan.writeMode,
            propertyWinningSelector: ((_a4 = writePlan.propertyWinningRule) == null ? void 0 : _a4.selector) || "",
            insertionAnchorSelector: ((_b3 = writePlan.insertionAnchorRule) == null ? void 0 : _b3.selector) || "",
            propertyWinningStyleSheetId: ((_c2 = writePlan.propertyWinningRule) == null ? void 0 : _c2.styleSheetId) || "",
            insertionAnchorStyleSheetId: ((_d2 = writePlan.insertionAnchorRule) == null ? void 0 : _d2.styleSheetId) || ""
          };
        })
      });
      if (writeSeq !== state.selectionBreadthWriteSeqByProp.get(prop)) return;
      const summaryBeforeComputed = draftEditSummaryBaseline(prop, plan.writePlans);
      let write = await applySelectionBreadthPlan(plan.writePlans);
      if (writeSeq !== state.selectionBreadthWriteSeqByProp.get(prop)) return;
      recordFlowDebug("style-apply-write", {
        prop,
        targetCount: write.targets.length,
        selectors: write.selectors,
        reason: write.reason || "",
        targets: write.targets.map((el) => cssPath(el))
      });
      if (!write.targets.length && shouldRetryStyleWrite(plan, prop)) {
        await waitForStyleWriteSettle(plan.stateContext);
        if (writeSeq !== state.selectionBreadthWriteSeqByProp.get(prop)) return;
        state.selectionBreadthCurrentPlanCache = null;
        plan = await createWritePlan({ forceRefresh: true });
        if (writeSeq !== state.selectionBreadthWriteSeqByProp.get(prop)) return;
        if (!plan) {
          toast("当前选区没有可写入目标。");
          return;
        }
        if (writeSeq !== state.selectionBreadthWriteSeqByProp.get(prop)) return;
        write = await applySelectionBreadthPlan(plan.writePlans);
        if (writeSeq !== state.selectionBreadthWriteSeqByProp.get(prop)) return;
        recordFlowDebug("style-apply-retry-write", {
          prop,
          retry: "settle",
          targetCount: write.targets.length,
          selectors: write.selectors,
          reason: write.reason || "",
          targets: write.targets.map((el) => cssPath(el))
        });
      }
      if (!write.targets.length && selectionBreadthPlanHasWritableTarget(plan)) {
        state.selectionBreadthCurrentPlanCache = null;
        plan = await createWritePlan({ forceRefresh: true });
        if (writeSeq !== state.selectionBreadthWriteSeqByProp.get(prop)) return;
        if (!plan) {
          toast("当前选区没有可写入目标。");
          return;
        }
        if (writeSeq !== state.selectionBreadthWriteSeqByProp.get(prop)) return;
        write = await applySelectionBreadthPlan(plan.writePlans);
        if (writeSeq !== state.selectionBreadthWriteSeqByProp.get(prop)) return;
        recordFlowDebug("style-apply-refresh-write", {
          prop,
          retry: "force-refresh",
          targetCount: write.targets.length,
          selectors: write.selectors,
          reason: write.reason || "",
          targets: write.targets.map((el) => cssPath(el))
        });
      }
      if (!write.targets.length) {
        toast(write.reason || "当前选区不支持该配置。");
        return;
      }
      const validationTargets = observableValidationTargets(plan.stateContext, write.targets);
      const validationBefore = validationTargets.map((target) => write.beforeComputed[write.targets.indexOf(target)] || "");
      const validation = isTransientStateContext(plan.stateContext) && isStateAppearanceProp(prop) ? { success: true, computedAfter: comparableStyleValuesForTargets(write.targets, prop), expectedValue: [] } : validateStyleApplication(prop, normalized, validationTargets, validationBefore);
      recordFlowDebug("style-apply-validation", {
        prop,
        success: !!validation.success,
        reason: validation.reason || "",
        computedAfter: validation.computedAfter || [],
        expectedValue: validation.expectedValue || []
      });
      updateControlFailure(prop, validation);
      recordEdit({
        kind: prop,
        route: "selection-plan",
        value: normalized,
        before: write.before,
        beforeComputed: summaryBeforeComputed || write.beforeComputed,
        applied: validation.success,
        failureReason: validation.reason || "",
        computedAfter: validation.computedAfter || [],
        expectedValue: validation.expectedValue || [],
        applyMode: write.applyMode,
        cssSelector: write.selectors.join(","),
        selectionBreadthRuleIds: write.ruleIds,
        generatedCssRules: write.rules,
        sourcePaths: write.sourcePaths || [],
        cdpUndoEdits: write.cdpUndoEdits || [],
        stateCondition: plan.stateContext || null,
        selectionPlan: summarizeSelectionBreadthPlan(plan),
        suggestedImplementation: {
          strategy: "selection-breadth-css-write",
          property: cssProp(prop),
          breadth: plan.breadth,
          parentScope: plan.parentScope,
          avoid: ["semantic classification", "live scope class fallback"]
        }
      }, write.targets);
      if (validation.success) clearToast();
      if (validation.success && isLayoutEffectSource$1(prop)) scheduleLayoutSideEffectSync$1(controlIdForLayoutEffectSource$1(prop));
    }
    async function cachedSelectionBreadthWritePlan(prop, value, options2 = {}) {
      const key = selectionBreadthPlanCacheKey();
      const cached = state.selectionBreadthCurrentPlanCache;
      if (!options2.forceRefresh && cached && cached.revision === state.selectionBreadthWritePlanRevision && cached.key === key) {
        return selectionPlanForProperty(cached.plan, prop, value);
      }
      const plan = await buildSelectionBreadthMasterPlan(editableStylePropsForSelection());
      if (plan == null ? void 0 : plan.cdpStyleInfoAvailable) {
        state.selectionBreadthCurrentPlanCache = {
          revision: state.selectionBreadthWritePlanRevision,
          key,
          plan
        };
      }
      return selectionPlanForProperty(plan, prop, value);
    }
    function startSelectionBreadthWritePlanPreparation() {
      var _a3;
      if (!state.selected || ((_a3 = state.groupResult) == null ? void 0 : _a3.mode) === "selection-breadth-loading") return;
      const seq = ++state.selectionBreadthWritePlanPrepareSeq;
      state.selectionBreadthWritePlansLoading = true;
      state.selectionBreadthWritePlansReadyRevision = -1;
      state.selectionBreadthWritePlanAttemptedProps.clear();
      publishPanelViewModel();
      prepareSelectionBreadthWritePlans(seq).catch((error) => {
        console.warn("[vibepolish] failed to prepare selection write plans", error);
      }).finally(() => {
        if (seq !== state.selectionBreadthWritePlanPrepareSeq) return;
        state.selectionBreadthWritePlansReadyRevision = state.selectionBreadthWritePlanRevision;
        state.selectionBreadthWritePlansLoading = false;
        syncControls();
        renderAll();
        publishPanelViewModel();
      });
    }
    async function prepareSelectionBreadthWritePlans(seq) {
      if (seq !== state.selectionBreadthWritePlanPrepareSeq || !state.selected) return;
      const props = editableStylePropsForSelection();
      if (!props.length) return;
      const plan = await buildSelectionBreadthMasterPlan(props);
      if (seq !== state.selectionBreadthWritePlanPrepareSeq || !state.selected) return;
      if ((plan == null ? void 0 : plan.stateContextFallbackReason) === "no-visible-pseudo-winner") {
        state.selectionStateContext = {
          kind: "default",
          selector: "",
          source: "pseudo-not-visible"
        };
        recordFlowDebug("selection-state-resolved-default", {
          selectionOwner: cssPath(plan.selectionOwner),
          reason: plan.stateContextFallbackReason
        });
        await refreshSelectionBreadthScopes(state.visualSelection);
        return;
      }
      if (plan == null ? void 0 : plan.cdpStyleInfoAvailable) {
        state.selectionBreadthCurrentPlanCache = {
          revision: state.selectionBreadthWritePlanRevision,
          key: selectionBreadthPlanCacheKey(),
          plan
        };
      }
      recordFlowDebug("selection-master-plan-ready", {
        props,
        plan: summarizeSelectionBreadthPlan(plan)
      });
      props.forEach((prop) => state.selectionBreadthWritePlanAttemptedProps.add(prop));
    }
    async function buildSelectionBreadthMasterPlan(props) {
      const requestedProps = uniqueValues2((props || []).filter((prop) => prop && prop !== "textContent"));
      if (!requestedProps.length || !state.selected) return null;
      return buildSelectionBreadthPlanForBreadth({
        props: requestedProps,
        breadth: breadthForCurrentScope()
      });
    }
    async function buildSelectionBreadthPlanForBreadth({ props, breadth, selectionOwner = null, parentScope = "all-similar-parents", stateContext = currentSelectionStateContext(), candidateScope = null, fixedUniverse = null }) {
      var _a3;
      const planningJob = beginSelectionPlanningJob("selection-plan");
      const baseInput = selectionBreadthPlanBaseInput(props, breadth, {
        selectionOwner,
        parentScope,
        stateContext,
        candidateScope,
        fixedUniverse
      });
      const basePlan = createSelectionBreadthPlanSync(baseInput);
      applyExplicitScopeToSelectionPlan(basePlan);
      const cdpStyleInfo = reusableCdpStyleInfoForCurrentScope() || await cdpStyleInfoForSelectionPlan(basePlan, selectionBreadthPlanningProps(props), stateContext, planningJob);
      if (!isSelectionPlanningJobCurrent(planningJob)) return basePlan;
      const noVisiblePseudoWinner = isTransientStateContext(stateContext) && ((_a3 = cdpStyleInfo == null ? void 0 : cdpStyleInfo.hasWinningRuleForState) == null ? void 0 : _a3.call(cdpStyleInfo, stateContext)) === false;
      const effectiveStateContext = noVisiblePseudoWinner ? { kind: "default", selector: "", source: "pseudo-not-visible" } : stateContext;
      const plan = cdpStyleInfo ? createSelectionBreadthPlanSync({ ...baseInput, stateContext: effectiveStateContext, cdpStyleInfo }) : basePlan;
      applyExplicitScopeToSelectionPlan(plan);
      plan.stateContext = effectiveStateContext;
      if (noVisiblePseudoWinner) plan.stateContextFallbackReason = "no-visible-pseudo-winner";
      if (cdpStyleInfo) {
        plan.cdpStyleInfoAvailable = true;
        plan.cdpStyleInfo = cdpStyleInfo;
      }
      const capabilityModel = selectionCapabilityModel(state.visualSelection);
      plan.mechanicalTraits = capabilityModel.traits;
      plan.capabilityGroups = capabilityModel.groups;
      finishSelectionPlanningJob(planningJob, "completed");
      return plan;
    }
    function reusableCdpStyleInfoForCurrentScope() {
      var _a3, _b2, _c;
      if (!((_b2 = (_a3 = state.groupResult) == null ? void 0 : _a3.mode) == null ? void 0 : _b2.startsWith("selection-table-"))) return null;
      return ((_c = state.tableScopePlan) == null ? void 0 : _c.cdpStyleInfoAvailable) ? state.tableScopePlan.cdpStyleInfo || null : null;
    }
    function selectionBreadthPlanBaseInput(props, breadth, options2 = {}) {
      var _a3;
      const requestedProps = selectionBreadthPlanningProps(props);
      const placeholderProp = requestedProps.includes("backgroundColor") ? "backgroundColor" : requestedProps[0];
      const owner = options2.selectionOwner || ((_a3 = state.visualSelection) == null ? void 0 : _a3.anchor) || state.selected;
      return {
        root: doc(),
        selectionOwner: owner,
        property: placeholderProp,
        value: currentWritableStyleValue(placeholderProp),
        breadth,
        parentScope: options2.parentScope || "all-similar-parents",
        stateContext: options2.stateContext || null,
        cdpStyleInfo: options2.cdpStyleInfo || null,
        candidateScope: options2.candidateScope || null,
        fixedUniverse: options2.fixedUniverse || null,
        propertyTargetResolver: selectionBreadthPropertyTargets
      };
    }
    function selectionBreadthPlanningProps(props = null) {
      return uniqueValues2([
        ...(props || editableStylePropsForSelection()).filter((prop) => prop && prop !== "textContent"),
        ...cdpClassificationAnchorProperties()
      ]);
    }
    function editableStylePropsForSelection() {
      return uniqueValues2(propertyCapabilitiesForSelection().filter((cap) => cap.show && cap.enabled && cap.prop && cap.prop !== "textContent").map((cap) => cap.prop));
    }
    function selectionBreadthPlanHasWritableTarget(plan) {
      return !!((plan == null ? void 0 : plan.writePlans) || []).some(
        (writePlan) => {
          var _a3;
          return writePlan.writeMode !== "unavailable" && writePlan.materializedSelector && ((_a3 = writePlan.verificationTargets) == null ? void 0 : _a3.length);
        }
      );
    }
    function selectionBreadthWritePlanCacheReady(prop) {
      const cached = state.selectionBreadthCurrentPlanCache;
      if (!(cached && cached.revision === state.selectionBreadthWritePlanRevision && cached.key === selectionBreadthPlanCacheKey())) return false;
      return selectionBreadthPlanHasWritableTarget(selectionPlanForProperty(cached.plan, prop, currentWritableStyleValue(prop)));
    }
    function selectionBreadthWritePlanAttempted(prop) {
      return state.selectionBreadthWritePlanAttemptedProps.has(prop);
    }
    function selectionBreadthWritePlanUnavailableReason(prop) {
      const context = currentSelectionStateContext();
      if ((context == null ? void 0 : context.kind) === "hover") return `当前 hover 态没有明确${stylePropLabel(prop)}规则。`;
      return "当前选区没有可写入目标。";
    }
    function stylePropLabel(prop) {
      if (prop === "color") return "文字色";
      if (prop === "backgroundColor") return "填充色";
      if (prop === "borderColor") return "边框色";
      return "该属性";
    }
    function currentWritableStyleValue(prop) {
      var _a3, _b2;
      const route = resolveCurrentStyleRoute(prop);
      const target = ((_a3 = route.targets) == null ? void 0 : _a3[0]) || ((_b2 = state.visualSelection) == null ? void 0 : _b2.anchor) || state.selected;
      if (!target) return "";
      const cs = win().getComputedStyle(target);
      if (prop === "borderColor") return computedBorderColor(cs);
      if (prop === "paddingX") return cs.paddingLeft || "";
      if (prop === "paddingY") return cs.paddingTop || "";
      if (prop === "offsetX" || prop === "offsetY") return comparableStyleValue(cs, prop) || "0px";
      return cs[prop] || "";
    }
    function selectionBreadthPlanCacheKey() {
      var _a3, _b2;
      const stateContext = currentSelectionStateContext();
      return [
        state.scopeIndex,
        ((_a3 = state.groupResult) == null ? void 0 : _a3.mode) || "",
        state.tableScopeView || "",
        (stateContext == null ? void 0 : stateContext.kind) || "default",
        cssPath(state.selected || ((_b2 = state.visualSelection) == null ? void 0 : _b2.anchor) || doc().body)
      ].join("|");
    }
    function selectionPlanForProperty(plan, prop, value) {
      if (!plan) return null;
      return retargetSelectionPlanProperty(plan, prop, value, selectionBreadthPropertyTargets);
    }
    function shouldRetryStyleWrite(plan, prop) {
      var _a3;
      return ((_a3 = plan == null ? void 0 : plan.stateContext) == null ? void 0 : _a3.kind) === "hover" && isStateAppearanceProp(prop);
    }
    function waitForStyleWriteSettle(stateContext) {
      const delay = (stateContext == null ? void 0 : stateContext.kind) === "hover" ? 260 : 80;
      return new Promise((resolve) => setTimeout(resolve, delay));
    }
    function createSelectionBreadthPlanSync({ selectionOwner, property, value, breadth, parentScope = "all-similar-parents", stateContext = null, cdpStyleInfo = null, candidateScope = null, fixedUniverse = null }) {
      state.selectionBreadthPlanningStateContext = stateContext || null;
      try {
        const plan = createSelectionPlan({
          root: doc(),
          selectionOwner,
          property,
          value,
          breadth,
          parentScope,
          stateContext,
          cdpStyleInfo,
          candidateScope,
          fixedUniverse,
          propertyTargetResolver: selectionBreadthPropertyTargets
        });
        plan.stateContext = stateContext || null;
        return plan;
      } finally {
        state.selectionBreadthPlanningStateContext = null;
      }
    }
    async function cdpStyleInfoForSelectionPlan(plan, property, stateContext, planningJob) {
      let targets2 = [];
      let probeElements = [];
      let probeAttr = "";
      try {
        if (!isSelectionPlanningJobCurrent(planningJob)) return null;
        const provider = currentCdpStyleProvider();
        if (typeof provider !== "function") {
          syncCdpProviderConnection(false);
          return null;
        }
        const planItems = uniqueElements2([
          plan.selectionOwner,
          ...plan.structuralItems || [],
          ...(plan.visualGroups || []).flatMap((group) => group.items || []),
          ...(plan.targetGroups || []).flatMap((group) => group.items || [])
        ]).filter(isElementNode);
        const requestedProperties = uniqueValues2(Array.isArray(property) ? property : [property]).filter(Boolean);
        const propertyTargets = uniqueElements2(requestedProperties.flatMap(
          (prop) => selectionBreadthOwnerTargetsForStateContext(stateContext, planItems, prop).flatMap((item) => item.targets || [])
        )).filter(isElementNode);
        const elements = selectionBreadthCdpProbeTargets(plan, planItems, propertyTargets, stateContext).filter(isElementNode);
        if (!elements.length) return null;
        const includeBaseVisualValues = transientVisualNormalizationActive();
        const properties = uniqueValues2([
          ...requestedProperties,
          ...(stateContext == null ? void 0 : stateContext.kind) === "hover" ? [] : cdpClassificationAnchorProperties(),
          ...includeBaseVisualValues ? CORE_VISUAL_PROPERTIES : [],
          ...(stateContext == null ? void 0 : stateContext.kind) === "hover" ? [] : (plan.visualGroups || []).flatMap((group) => group.diffProps || [])
        ]).filter(Boolean);
        if (!properties.length) return null;
        const token = `vp-cdp-plan-${Date.now().toString(36)}-${++state.cdpProbeSeq}`;
        probeAttr = `${CDP_PROBE_ATTR}-${token}`;
        state.cdpProbeAttributes.add(probeAttr);
        const idByElement = /* @__PURE__ */ new WeakMap();
        probeElements = elements.slice();
        targets2 = probeElements.map((el, index) => {
          const id = `${token}-${index}`;
          idByElement.set(el, id);
          el.setAttribute(probeAttr, id);
          return {
            id,
            selector: `[${probeAttr}="${cssStringEscape(id)}"]`,
            cssPath: cssPath(el),
            tag: el.tagName.toLowerCase()
          };
        });
        recordFlowDebug("cdp-plan-request", {
          token,
          attr: probeAttr,
          planningJob: { id: planningJob.id, revision: planningJob.revision },
          stateContext: (stateContext == null ? void 0 : stateContext.kind) || "default",
          selectionOwner: cssPath(plan.selectionOwner),
          properties,
          targets: targets2.map((target) => ({
            id: target.id,
            cssPath: target.cssPath,
            presentNow: !!doc().querySelector(target.selector)
          }))
        });
        const response = await provider({
          token,
          attr: probeAttr,
          planningJob: { id: planningJob.id, revision: planningJob.revision },
          properties,
          stateContext,
          includeBaseVisualValues,
          targets: targets2
        });
        if (!isSelectionPlanningJobCurrent(planningJob) || (response == null ? void 0 : response.cancelled)) return null;
        syncCdpProviderConnection(true);
        const rules = (response == null ? void 0 : response.rules) || {};
        const baseRules = (response == null ? void 0 : response.baseRules) || {};
        const baseVisualValues = (response == null ? void 0 : response.baseVisualValues) || {};
        recordFlowDebug("cdp-plan-response", {
          token,
          attr: probeAttr,
          planningJob: { id: planningJob.id, revision: planningJob.revision },
          stateContext: (stateContext == null ? void 0 : stateContext.kind) || "default",
          resolvedTargets: (response == null ? void 0 : response.resolvedTargets) || 0,
          rules: Object.entries(rules || {}).map(([key, rule]) => ({
            key,
            selector: (rule == null ? void 0 : rule.selector) || "",
            property: (rule == null ? void 0 : rule.property) || "",
            sourceProperty: (rule == null ? void 0 : rule.sourceProperty) || ""
          })),
          baseRules: Object.entries(baseRules || {}).map(([key, rule]) => ({
            key,
            selector: (rule == null ? void 0 : rule.selector) || "",
            property: (rule == null ? void 0 : rule.property) || "",
            sourceProperty: (rule == null ? void 0 : rule.sourceProperty) || ""
          }))
        });
        if (!rules || typeof rules !== "object") return null;
        return {
          getWinningRule(element, prop, state2) {
            const id = idByElement.get(element) || idByElement.get(selectionBreadthPrimaryTargetForStateContext(stateContext, element, prop));
            if (!id) return null;
            if (!(state2 == null ? void 0 : state2.kind) && Object.prototype.hasOwnProperty.call(baseRules, cdpBaseVisualKey(id, prop))) {
              return baseRules[cdpBaseVisualKey(id, prop)];
            }
            return rules[cdpRuleKey(id, prop, state2)] || rules[cdpRuleKey(id, prop, null)] || null;
          },
          getBaseVisualValue(element, prop) {
            const id = idByElement.get(element);
            if (!id) return null;
            return Object.prototype.hasOwnProperty.call(baseVisualValues, cdpBaseVisualKey(id, prop)) ? baseVisualValues[cdpBaseVisualKey(id, prop)] : null;
          },
          hasWinningRuleForState(state2) {
            if (!(state2 == null ? void 0 : state2.kind)) return false;
            const suffix = `::${state2.kind}`;
            return Object.keys(rules).some((key) => key.endsWith(suffix));
          }
        };
      } catch (error) {
        if (!isSelectionPlanningJobCurrent(planningJob)) return null;
        finishSelectionPlanningJob(planningJob, "failed");
        syncCdpProviderConnection(false);
        console.warn("[vibepolish] CDP style provider failed", error);
        return null;
      } finally {
        if (probeAttr) {
          probeElements.forEach((el) => {
            var _a3;
            return (_a3 = el.removeAttribute) == null ? void 0 : _a3.call(el, probeAttr);
          });
          state.cdpProbeAttributes.delete(probeAttr);
        }
      }
    }
    function isElementNode(value) {
      return !!value && value.nodeType === 1 && typeof value.getBoundingClientRect === "function";
    }
    function selectionBreadthCdpProbeTargets(plan, planItems, propertyTargets, stateContext = null) {
      const transientHost = (stateContext == null ? void 0 : stateContext.kind) === "hover" ? confirmedHoverHostForSelection(state.selected) : (stateContext == null ? void 0 : stateContext.kind) === "focus" ? confirmedFocusHostForSelection(state.selected, doc().activeElement) : null;
      const priority = [
        transientHost,
        plan.selectionOwner,
        ...propertyTargets,
        ...(plan.targetGroups || []).flatMap((group) => group.items || []),
        ...(plan.visualGroups || []).flatMap((group) => group.items || []),
        ...plan.structuralItems || [],
        ...planItems || []
      ];
      return uniqueElements2(priority);
    }
    function selectionBreadthOwnerTargetsForStateContext(stateContext, owners, prop) {
      state.selectionBreadthPlanningStateContext = stateContext || null;
      try {
        return selectionBreadthOwnerTargets(owners, prop);
      } finally {
        state.selectionBreadthPlanningStateContext = null;
      }
    }
    function selectionBreadthPrimaryTargetForStateContext(stateContext, owner, prop) {
      var _a3, _b2;
      const target = (_b2 = (_a3 = selectionBreadthOwnerTargetsForStateContext(stateContext, [owner], prop)[0]) == null ? void 0 : _a3.targets) == null ? void 0 : _b2[0];
      return target || owner;
    }
    function cdpRuleKey(id, prop, stateContext = null) {
      return `${id}::${prop}::${(stateContext == null ? void 0 : stateContext.kind) || "default"}`;
    }
    function cdpBaseVisualKey(id, prop) {
      return `${id}::${prop}`;
    }
    function transientVisualNormalizationActive() {
      if (state.hoverStateLocked || state.focusStateLocked) return true;
      const active = doc().activeElement;
      if (!active || active === doc().body || active === doc().documentElement) return false;
      return !!confirmedFocusStateForSelection(state.selected || active, active);
    }
    function cdpClassificationAnchorProperties() {
      return [
        "backgroundColor",
        "borderTopColor",
        "borderTopWidth",
        "borderTopStyle",
        "borderRadius",
        "boxShadow",
        "color",
        "fontFamily",
        "fontSize",
        "fontWeight",
        "paddingTop",
        "display"
      ];
    }
    function breadthForCurrentScope() {
      var _a3;
      const mode = ((_a3 = state.groupResult) == null ? void 0 : _a3.mode) || "";
      if (mode === "selection-all-kind") return "all-kind";
      if (mode === "selection-table-row" || mode === "selection-table-column" || mode === "selection-table-all-cells") return "all-kind";
      if (mode === "selection-single" || state.scope !== "group") return "single";
      return "similar-kind";
    }
    function applyExplicitScopeToSelectionPlan(plan) {
      var _a3, _b2, _c;
      const mode = ((_a3 = state.groupResult) == null ? void 0 : _a3.mode) || "";
      if (!mode.startsWith("selection-table-")) return plan;
      const items = uniqueElements2(state.group || []).filter(isVisible);
      const scope = state.groupResult || {};
      const selector = scope.effectiveGroupSelector || items.map(cssPath).join(",");
      const group = {
        id: mode,
        items,
        signature: { key: mode, props: {} },
        diffProps: [],
        classificationSelector: selector,
        classificationSelectorMode: scope.effectiveSelectorMode || "table-axis",
        classificationVerification: scope.effectiveSelectorVerification || null,
        fallbackReasons: []
      };
      const previousAnchor = ((_b2 = (plan.writePlans || []).find((item) => item.insertionAnchorRule)) == null ? void 0 : _b2.insertionAnchorRule) || ((_c = (plan.writePlans || []).find((item) => item.propertyWinningRule)) == null ? void 0 : _c.propertyWinningRule) || null;
      plan.structuralItems = items;
      plan.visualGroups = [group];
      plan.currentVisualGroup = group;
      plan.targetGroups = [group];
      plan.writePlans = [{
        groupId: mode,
        items,
        property: plan.property,
        value: plan.value,
        stateContext: plan.stateContext || null,
        ownerTargets: items.map((owner) => ({
          owner,
          targets: [owner],
          relation: { kind: "table", targets: [owner] }
        })),
        propertyTargets: items,
        verificationTargets: items,
        classificationSelector: selector,
        classificationSelectorMode: group.classificationSelectorMode,
        propertyWinningSelector: "",
        propertyWinningRule: null,
        insertionAnchorRule: previousAnchor,
        generatedSelector: selector,
        materializedSelector: selector,
        writeMode: selector && (previousAnchor == null ? void 0 : previousAnchor.styleSheetId) && (previousAnchor == null ? void 0 : previousAnchor.styleRange) ? "insert-rule" : "unavailable",
        writeRule: null,
        unavailableReason: selector && (previousAnchor == null ? void 0 : previousAnchor.styleSheetId) && (previousAnchor == null ? void 0 : previousAnchor.styleRange) ? "" : "table write plan has no persistent stylesheet insertion anchor",
        generatedRule: {
          selector,
          property: plan.property,
          value: plan.value,
          cssText: `${selector} {
  ${cssProp(plan.property)}: ${plan.value};
}`,
          mode: group.classificationSelectorMode === "table-axis-materialized" ? "classification-intersection" : "structure-narrow"
        },
        fallbackReasons: [],
        verification: {
          selector: scope.effectiveSelectorVerification || null,
          computed: null
        }
      }];
      return plan;
    }
    function confirmedStateContextForSelection() {
      if (!state.selected) return null;
      if (isConfirmedHoverSelection()) {
        return {
          kind: "hover",
          selector: ":hover",
          source: "pseudo-hover"
        };
      }
      const focusState = confirmedFocusStateForSelection(state.selected, doc().activeElement);
      if (focusState) {
        return {
          kind: "focus",
          selector: focusState.selector,
          source: "pseudo-focus"
        };
      }
      if (isConfirmedCheckedSelection()) {
        return {
          kind: "checked",
          selector: ":checked",
          source: "pseudo-checked"
        };
      }
      const ariaSelected = closestAriaStateOwner(state.selected, "aria-selected");
      if (ariaSelected) {
        return {
          kind: "aria-selected",
          selector: '[aria-selected="true"]',
          source: "aria-selected"
        };
      }
      const ariaPressed = closestAriaStateOwner(state.selected, "aria-pressed");
      if (ariaPressed) {
        return {
          kind: "aria-pressed",
          selector: '[aria-pressed="true"]',
          source: "aria-pressed"
        };
      }
      return null;
    }
    function currentSelectionStateContext() {
      if (state.selectionStateContext) return state.selectionStateContext;
      const label = stateConditionLabel(state.groupResult);
      if (label === "hover") return { kind: "hover", selector: ":hover", source: "selection-state" };
      if (label === "focus") return { kind: "focus", selector: ":focus", source: "selection-state" };
      if (label === "checked") return { kind: "checked", selector: ":checked", source: "selection-state" };
      if (label === "selected") return { kind: "aria-selected", selector: '[aria-selected="true"]', source: "selection-state" };
      if (label === "pressed") return { kind: "aria-pressed", selector: '[aria-pressed="true"]', source: "selection-state" };
      return confirmedStateContextForSelection();
    }
    function isConfirmedHoverSelection() {
      var _a3;
      if (!state.hoverStateLocked || !((_a3 = state.hoverHosts) == null ? void 0 : _a3.length) || !state.selected) return false;
      return !!confirmedHoverHostForSelection(state.selected);
    }
    function isConfirmedCheckedSelection() {
      var _a3, _b2;
      const target = state.selected;
      if (!target) return false;
      if ((_a3 = target.matches) == null ? void 0 : _a3.call(target, 'input[type="checkbox"],input[type="radio"]')) return !!target.checked;
      const checked = (_b2 = target.querySelector) == null ? void 0 : _b2.call(target, 'input[type="checkbox"]:checked,input[type="radio"]:checked');
      return !!checked;
    }
    function closestAriaStateOwner(target, attr) {
      var _a3;
      let node = target;
      while (node && node.nodeType === 1 && !isPageLike(node)) {
        if (((_a3 = node.getAttribute) == null ? void 0 : _a3.call(node, attr)) === "true") return node;
        node = node.parentElement;
      }
      return null;
    }
    function isTransientStateContext(context) {
      const kind = String((context == null ? void 0 : context.kind) || "").toLowerCase();
      return kind === "hover" || kind === "focus";
    }
    function confirmedHoverHostForSelection(selected) {
      if (!selected) return null;
      const primary = state.hoverPrimaryHost;
      if ((primary == null ? void 0 : primary.isConnected) && (primary === selected || primary.contains(selected))) return primary;
      return uniqueElements2(state.hoverHosts || []).filter((host) => (host == null ? void 0 : host.isConnected) && host === selected).find((host) => elementHasOwnStateSelector(host, ":hover")) || null;
    }
    function confirmedFocusHostForSelection(selected, active) {
      var _a3;
      return ((_a3 = confirmedFocusStateForSelection(selected, active)) == null ? void 0 : _a3.host) || null;
    }
    function confirmedFocusStateForSelection(selected, active) {
      var _a3;
      if (!selected) return null;
      if (state.focusStateLocked) {
        const locks = (state.focusLocks || []).filter(
          (lock) => {
            var _a4;
            return ((_a4 = lock.host) == null ? void 0 : _a4.isConnected) && (lock.host === selected || lock.host.contains(selected) || selected.contains(lock.host));
          }
        );
        const exact = locks.find((lock) => lock.host === selected);
        if (exact) return exact;
        if (locks.length) return locks[0];
      }
      if (!active) return null;
      const candidates = [selected];
      let node = active;
      while (node && node.nodeType === 1 && !isPageLike(node)) {
        if (node === selected || node.contains(selected) || selected.contains(node)) candidates.push(node);
        node = node.parentElement;
      }
      for (const host of uniqueElements2(candidates)) {
        const selectors = host === active ? [":focus-visible", ":focus", ":focus-within"] : [":focus-within"];
        for (const selector of selectors) {
          if (!((_a3 = host.matches) == null ? void 0 : _a3.call(host, selector))) continue;
          if (elementHasOwnStateSelector(host, selector)) return { host, selector };
        }
      }
      return null;
    }
    function elementHasOwnStateSelector(element, stateSelector) {
      if (!element || !stateSelector) return false;
      return allStyleRules().some((rule) => splitSelectorList(rule.selectorText || "").some(
        (branch) => selectorBranchTargetsOwnState(element, branch, stateSelector)
      ));
    }
    function selectorBranchTargetsOwnState(element, branch, stateSelector) {
      const text = String(branch || "").trim();
      if (!text.includes(stateSelector)) return false;
      const compounds = splitSelectorCompounds(text);
      const stateIndex = compounds.findIndex((part) => part.includes(stateSelector));
      if (stateIndex < 0 || stateIndex !== compounds.length - 1) return false;
      const withoutState = text.replaceAll(stateSelector, "").replace(/\s+/g, " ").trim();
      try {
        return !!withoutState && element.matches(withoutState);
      } catch {
        return false;
      }
    }
    function splitSelectorCompounds(selector) {
      const parts = [];
      let current = "";
      let depth = 0;
      for (const char of String(selector || "")) {
        if (char === "(" || char === "[") depth += 1;
        if (char === ")" || char === "]") depth = Math.max(0, depth - 1);
        if (depth === 0 && (char === ">" || char === "+" || char === "~" || /\s/.test(char))) {
          if (current.trim()) {
            parts.push(current.trim());
            current = "";
          }
          continue;
        }
        current += char;
      }
      if (current.trim()) parts.push(current.trim());
      return parts;
    }
    function stateContextLabel(context) {
      const kind = String((context == null ? void 0 : context.kind) || "").toLowerCase();
      if (kind === "aria-selected") return "selected";
      if (kind === "aria-pressed") return "pressed";
      if (kind === "checked") return "checked";
      if (kind === "focus") return "focus";
      if (kind === "hover") return "hover";
      return "";
    }
    function selectionBreadthPropertyTargets(owner, prop) {
      const visual = owner === state.selected && state.visualSelection ? state.visualSelection : resolveVisualSelectionFromAnchor(owner);
      return propertyTargetsForVisual(visual, prop);
    }
    function propertyTargetsForVisual(visual, prop) {
      if (!(visual == null ? void 0 : visual.anchor)) return { kind: "self", targets: [], reason: "missing-visual-owner" };
      const iconTargets = selectionBreadthIconTargets(visual, prop);
      if (iconTargets) {
        return {
          kind: "slot-icon",
          targets: iconTargets,
          reason: iconTargets.length ? "" : "icon-slot-is-missing-or-ambiguous"
        };
      }
      if (isTextStyleProp(prop)) {
        const targets2 = selectionBreadthTextTargets(visual, prop);
        if (!targets2.length) return { kind: "slot-text", targets: [], reason: "text-targets-are-missing-or-mixed" };
        return {
          kind: targets2.length === 1 && targets2[0] === visual.anchor ? "self" : "slot-text",
          targets: targets2
        };
      }
      if (prop === "padding" || prop === "paddingX" || prop === "paddingY" || isPaddingSideProp(prop)) {
        const tableTargets = selectionBreadthTablePaddingTargets(visual, prop);
        if (tableTargets) return { kind: "table", ...tableTargets };
      }
      const layer = confirmedLayerTargetForProperty(visual, prop);
      if (layer) return { kind: layer.kind, targets: [layer.target] };
      return { kind: "self", targets: [visual.anchor] };
    }
    function selectionBreadthIconTargets(visual, prop) {
      if (prop !== "color") return null;
      if (isIconLikeElement(visual.anchor)) return visibleElements2([visual.anchor]);
      if (!isIconOnlyControl(visual.anchor)) return null;
      const icons = visibleElements2([...visual.anchor.querySelectorAll("svg")].filter(isIconLikeElement));
      return icons.length === 1 ? icons : [];
    }
    function selectionBreadthTextTargets(visual, prop) {
      var _a3;
      const anchor = visual.anchor;
      const leaves = visibleElements2(((_a3 = visual.textLeaves) == null ? void 0 : _a3.length) ? visual.textLeaves : [anchor].filter(isTextLeaf));
      const directTextOwner = directVisibleText(anchor) ? [anchor] : [];
      const childTextTargets = directTextOwner.length ? collectDescendantTextLeaves(anchor) : leaves;
      const targets2 = uniqueElements2([...directTextOwner, ...childTextTargets]);
      if (!targets2.length) return [];
      if (directTextOwner.length) return targets2;
      if (targets2.length === 1) return targets2;
      return hasConsistentComputedValue(targets2, prop) ? targets2 : [];
    }
    function collectDescendantTextLeaves(anchor) {
      const leaves = [];
      [...(anchor == null ? void 0 : anchor.children) || []].forEach((child) => collectTextLeavesInto(child, leaves, anchor));
      return visibleElements2(leaves);
    }
    function selectionBreadthTablePaddingTargets(visual, prop) {
      var _a3;
      const anchor = visual.anchor;
      const cell = closestCell(anchor);
      if (!cell && !isTableElement(anchor)) return null;
      if (!cell) return { targets: [], reason: "table-owner-does-not-proxy-cell-padding" };
      const mode = ((_a3 = state.groupResult) == null ? void 0 : _a3.mode) || "";
      const isRowScope = mode === "selection-table-row" || mode === "selection-table-all-similar-rows";
      const isColumnScope = mode === "selection-table-column" || mode === "selection-table-all-similar-columns";
      const isAllScope = mode === "selection-table-all-cells" || mode === "selection-table-all-similar-cells-all";
      const isVertical = prop === "paddingY" || prop === "paddingTop" || prop === "paddingBottom";
      const isHorizontal = prop === "paddingX" || prop === "paddingLeft" || prop === "paddingRight";
      if (isAllScope || isRowScope && isVertical || isColumnScope && isHorizontal) return { targets: [cell] };
      return { targets: [], reason: "table-padding-axis-does-not-match-current-scope" };
    }
    function confirmedLayerTargetForProperty(visual, prop) {
      var _a3;
      const layerKey = prop === "backgroundColor" ? "background" : prop === "borderColor" ? "border" : prop === "borderRadius" ? "radius" : prop === "boxShadow" ? "shadow" : "";
      if (!layerKey) return null;
      const target = (_a3 = visual.layers) == null ? void 0 : _a3[layerKey];
      if (!target || target === visual.anchor) return null;
      if (isControlElement(target) || isMediaElement(target)) return null;
      if (!isConfirmedCompositeLayerRelation(visual.anchor, target)) return null;
      return { kind: `layer-${layerKey}`, target };
    }
    function isConfirmedCompositeLayerRelation(owner, target) {
      if (!owner || !target || owner === target) return false;
      const outer = owner.contains(target) ? owner : target.contains(owner) ? target : null;
      const inner = outer === owner ? target : owner;
      if (!outer) return false;
      if (!sameCompositeSurfaceGeometry(owner, target)) return false;
      let node = inner;
      while (node && node !== outer) {
        const parent = node.parentElement;
        if (!parent) return false;
        const visibleSiblings = [...parent.children].filter((child) => child !== node && isVisible(child));
        if (visibleSiblings.length) return false;
        node = parent;
      }
      return node === outer;
    }
    function sameCompositeSurfaceGeometry(owner, target) {
      const outer = owner.getBoundingClientRect();
      const inner = target.getBoundingClientRect();
      if (rectArea$1(outer) <= 1 || rectArea$1(inner) <= 1) return false;
      const widthTolerance = Math.max(24, outer.width * 0.2);
      const heightTolerance = Math.max(24, outer.height * 0.2);
      return Math.abs(outer.left - inner.left) <= widthTolerance && Math.abs(outer.right - inner.right) <= widthTolerance && Math.abs(outer.top - inner.top) <= heightTolerance && Math.abs(outer.bottom - inner.bottom) <= heightTolerance;
    }
    function visibleElements2(list) {
      return uniqueElements2((list || []).filter(Boolean)).filter(isVisible);
    }
    function isStateAppearanceProp(prop) {
      return ["backgroundColor", "borderColor", "borderRadius", "boxShadow"].includes(prop);
    }
    function splitSelectorList(selectorText) {
      const selectors = [];
      let current = "";
      let depth = 0;
      for (const char of String(selectorText || "")) {
        if (char === "(" || char === "[") depth += 1;
        if (char === ")" || char === "]") depth = Math.max(0, depth - 1);
        if (char === "," && depth === 0) {
          if (current.trim()) selectors.push(current.trim());
          current = "";
          continue;
        }
        current += char;
      }
      if (current.trim()) selectors.push(current.trim());
      return selectors;
    }
    function allStyleRules() {
      const rules = [];
      for (const sheet of [...doc().styleSheets]) {
        let cssRules;
        try {
          cssRules = sheet.cssRules;
        } catch {
          continue;
        }
        collectStyleRules(cssRules, rules);
      }
      return rules;
    }
    function collectStyleRules(cssRules, output) {
      for (const rule of [...cssRules]) {
        if (rule.selectorText && rule.style) output.push(rule);
        if (rule.cssRules) collectStyleRules(rule.cssRules, output);
      }
    }
    function resolveCurrentStyleRoute(prop) {
      if (state.scope !== "group") return resolveStyleRoute(prop, state.visualSelection);
      const routes = targets().map((anchor) => {
        const visual = anchor === state.selected ? state.visualSelection : resolveVisualSelectionFromAnchor(anchor);
        return resolveStyleRoute(prop, visual);
      });
      const refs = uniqueElements2(routes.flatMap((route) => route.targets));
      const first = routes.find((route) => route.targets.length) || routes[0] || routeResult(prop, [], "none", false);
      if (prop === "textContent") {
        if (!refs.length) return routeResult(prop, [], first.route, false, first.reason || "该选区没有可编辑文案。");
        if (!refs.every(isContentEditableSelection)) return routeResult(prop, [], first.route, false, "该选区包含复杂子元素，不能直接编辑文案。");
        if (!hasConsistentTextContent(refs)) return routeResult(prop, [], first.route, false, "当前范围内文案不一致，请缩小范围或选择同文案项。");
      }
      return {
        prop,
        targets: refs,
        route: first.route,
        visible: routes.some((route) => route.visible),
        reason: first.reason
      };
    }
    function normalizeStyleValue(prop, value) {
      if (value === "") return "";
      if (prop === "color" || prop === "backgroundColor" || prop === "borderColor") {
        return normalizeColorStyleValue(value);
      }
      if (prop === "offsetX" || prop === "offsetY") {
        return normalizeOffsetStyleValue(value);
      }
      if (prop === "paddingX" || prop === "paddingY" || isPaddingSideProp(prop)) {
        const probe2 = document.createElement("div");
        probe2.style.width = value;
        return probe2.style.width || null;
      }
      const probe = document.createElement("div");
      probe.style[prop] = value;
      return probe.style[prop] || null;
    }
    function normalizeColorStyleValue(value) {
      const raw = String(value || "").trim();
      if (!raw) return "";
      const probe = document.createElement("span");
      probe.style.position = "absolute";
      probe.style.visibility = "hidden";
      probe.style.pointerEvents = "none";
      probe.style.color = raw;
      if (!probe.style.color) return null;
      document.body.appendChild(probe);
      const normalized = getComputedStyle(probe).color || "";
      probe.remove();
      return /^(?:rgb|rgba)\(/i.test(normalized) ? normalized : null;
    }
    function normalizeOffsetStyleValue(value) {
      const raw = String(value || "").trim();
      if (!raw) return null;
      const amount = parseFloat(raw);
      if (!Number.isFinite(amount)) return null;
      const unit = raw.replace(/^-?\d*\.?\d+/, "").trim() || "px";
      const normalized = `${amount}${unit}`;
      const probe = document.createElement("div");
      probe.style.translate = `${normalized} 0px`;
      return probe.style.translate ? normalized : null;
    }
    function cssDeclarationsForPatch(prop, value, refs = [], important = false) {
      const suffix = important ? "!important" : "";
      if (prop === "paddingX") return [`padding-left:${value}${suffix};`, `padding-right:${value}${suffix};`].join("");
      if (prop === "paddingY") return [`padding-top:${value}${suffix};`, `padding-bottom:${value}${suffix};`].join("");
      if (isPaddingSideProp(prop)) return `${cssProp(prop)}:${value}${suffix};`;
      if (prop === "offsetX" || prop === "offsetY") return offsetDeclarationsForPatch(prop, value, suffix, refs);
      const declarations = [`${cssProp(prop)}:${value}${suffix}`];
      if (prop === "borderColor" && refs.some((el) => !hasBorder(el))) {
        declarations.push(`border-style:solid${suffix}`, `border-width:1px${suffix}`);
      }
      return declarations.map((item) => `${item};`).join("");
    }
    function offsetDeclarationsForPatch(prop, value, suffix = "", refs = []) {
      const current = translateAxesFromValue(refs[0] ? win().getComputedStyle(refs[0]).translate : "none");
      if (prop === "offsetX") current[0] = value;
      else current[1] = value;
      return `translate:${current.join(" ")}${suffix};`;
    }
    function translateAxesFromValue(value) {
      const tokens = String(value || "").trim().match(/(?:calc|min|max|clamp)\([^)]*\)|[^\s]+/g) || [];
      if (!tokens.length || tokens[0] === "none") return ["0px", "0px"];
      return [tokens[0] || "0px", tokens[1] || "0px", ...tokens.slice(2)];
    }
    async function applySelectionBreadthPlan(writePlans) {
      var _a3, _b2, _c, _d;
      const property = ((_a3 = writePlans == null ? void 0 : writePlans[0]) == null ? void 0 : _a3.property) || "";
      const value = ((_b2 = writePlans == null ? void 0 : writePlans[0]) == null ? void 0 : _b2.value) || "";
      const writeTargets = [];
      const rules = [];
      const selectors = [];
      const ruleIds = [];
      const before = [];
      const beforeComputed = [];
      const cdpEdits = [];
      for (const writePlan of writePlans || []) {
        const prop = writePlan.property;
        const value2 = writePlan.value;
        const groupTargets = uniqueElements2(writePlan.verificationTargets);
        const selector = writePlan.materializedSelector;
        if (writePlan.writeMode === "unavailable" || !selector || !groupTargets.length) {
          recordFlowDebug("selection-write-skip", {
            prop,
            reason: writePlan.unavailableReason || (!selector ? "missing-selector" : "missing-targets"),
            groupId: writePlan.groupId || "",
            ownerTargets: (writePlan.ownerTargets || []).map((item) => {
              var _a4, _b3;
              return {
                owner: cssPath(item.owner),
                targets: (item.targets || []).map((el) => cssPath(el)),
                relation: ((_a4 = item.relation) == null ? void 0 : _a4.kind) || "self",
                relationReason: ((_b3 = item.relation) == null ? void 0 : _b3.reason) || ""
              };
            })
          });
          continue;
        }
        const winningRule = writePlan.propertyWinningRule || null;
        const classificationAnchorRule2 = writePlan.classificationAnchorRule || null;
        const insertionAnchorRule = writePlan.insertionAnchorRule || null;
        const editRule = writePlan.writeMode === "edit-original" ? writePlan.writeRule : null;
        const executionRule = editRule || insertionAnchorRule;
        if (!(executionRule == null ? void 0 : executionRule.styleSheetId) || !(executionRule == null ? void 0 : executionRule.styleRange)) {
          recordFlowDebug("selection-write-skip", {
            prop,
            reason: "incomplete-write-plan",
            selector,
            groupId: writePlan.groupId || "",
            targets: groupTargets.map((el) => cssPath(el)),
            writeMode: writePlan.writeMode,
            winningSelector: (winningRule == null ? void 0 : winningRule.selector) || "",
            winningStyleSheetId: (winningRule == null ? void 0 : winningRule.styleSheetId) || "",
            winningHasRange: !!(winningRule == null ? void 0 : winningRule.styleRange),
            insertionAnchorSelector: (insertionAnchorRule == null ? void 0 : insertionAnchorRule.selector) || "",
            insertionAnchorStyleSheetId: (insertionAnchorRule == null ? void 0 : insertionAnchorRule.styleSheetId) || "",
            insertionAnchorHasRange: !!(insertionAnchorRule == null ? void 0 : insertionAnchorRule.styleRange)
          });
          continue;
        }
        before.push(...groupTargets.map((el) => el.style[prop] || ""));
        beforeComputed.push(...comparableStyleValuesForTargets(groupTargets, prop));
        const ruleId = `selection-breadth-${++state.selectionBreadthRuleSeq}`;
        const cssText = `/* ${ruleId} */
/* dt-write:${ruleId} */
${selector}{${cssDeclarationsForPatch(prop, value2, groupTargets)}}`;
        recordFlowDebug("selection-write-group", {
          prop,
          ruleId,
          selector,
          editOriginal: !!editRule,
          targets: groupTargets.map((el) => cssPath(el)),
          winningSelector: (winningRule == null ? void 0 : winningRule.selector) || "",
          winningSourceProperty: (winningRule == null ? void 0 : winningRule.sourceProperty) || "",
          classificationAnchorSelector: (classificationAnchorRule2 == null ? void 0 : classificationAnchorRule2.selector) || "",
          insertionAnchorSelector: (insertionAnchorRule == null ? void 0 : insertionAnchorRule.selector) || "",
          styleSheetId: ((_c = editRule || insertionAnchorRule) == null ? void 0 : _c.styleSheetId) || ""
        });
        rules.push(cssText);
        selectors.push(selector);
        ruleIds.push(ruleId);
        writeTargets.push(...groupTargets);
        cdpEdits.push(editRule ? {
          mode: "edit-style-text",
          ruleId,
          selector,
          property: prop,
          value: value2,
          styleSheetId: editRule.styleSheetId,
          sourcePath: editRule.sourcePath || "",
          range: editRule.styleRange,
          ruleLocator: editRule.ruleLocator,
          sourceProperty: writePlan.writeSourceProperty,
          existingText: editRule.styleText || "",
          text: cdpStyleTextWithDeclaration(editRule.styleText || "", prop, value2, writePlan.writeSourceProperty, groupTargets)
        } : {
          mode: "insert-rule",
          ruleId,
          selector,
          property: prop,
          value: value2,
          styleSheetId: insertionAnchorRule.styleSheetId,
          sourcePath: insertionAnchorRule.sourcePath || "",
          ruleText: cssText,
          reason: winningRule ? "winning selector affects elements outside the requested selection range" : "property has no winning declaration; inserting near a related rule"
        });
      }
      const targets2 = uniqueElements2(writeTargets).filter(isVisible);
      let cdpResult = { ok: true, undoEdits: [] };
      if (targets2.length) {
        const liveMerge = await removeOverlappingDraftSelectionWrites(property, targets2);
        cdpResult = await applyCdpStyleTextEdits(cdpEdits);
        if (!(cdpResult == null ? void 0 : cdpResult.ok)) {
          return {
            targets: [],
            before,
            beforeComputed,
            selectors,
            ruleIds,
            rules,
            applyMode: "cdp-stylesheet",
            reason: "CDP 写入失败，未应用样式。"
          };
        }
        commitDeferredDraftSelectionWrites(liveMerge);
        if ((_d = liveMerge == null ? void 0 : liveMerge.baselineUndoEdits) == null ? void 0 : _d.length) cdpResult.undoEdits = liveMerge.baselineUndoEdits;
        if ((writePlans || []).some((writePlan) => {
          var _a4;
          return ((_a4 = writePlan.stateContext) == null ? void 0 : _a4.kind) === "hover";
        })) refreshHoverFreezeMirror();
        if ((writePlans || []).some((writePlan) => {
          var _a4;
          return ((_a4 = writePlan.stateContext) == null ? void 0 : _a4.kind) === "focus";
        })) refreshFocusFreezeMirror();
      }
      state.selectionBreadthRules.push({
        property,
        value,
        selectors,
        ruleIds,
        rules
      });
      scheduleOverlayRender();
      return {
        targets: targets2,
        before,
        beforeComputed,
        selectors,
        ruleIds,
        rules,
        sourcePaths: uniqueValues2(cdpEdits.map((edit) => edit.sourcePath).filter(Boolean)),
        cdpUndoEdits: (cdpResult == null ? void 0 : cdpResult.undoEdits) || [],
        applyMode: "cdp-stylesheet",
        reason: !targets2.length ? "新选区算法没有找到可写入目标。" : ""
      };
    }
    async function removeOverlappingDraftSelectionWrites(prop, nextTargets) {
      var _a3, _b2;
      if (!state.draft || !(nextTargets == null ? void 0 : nextTargets.length)) return { baselineUndoEdits: [], deferredEdits: [], deferredRuleIds: [] };
      const nextSet = new Set(uniqueElements2(nextTargets));
      const draftEdits = state.edits.slice(state.draft.editBase);
      const immediateRuleIds = [];
      const immediateEdits = [];
      const deferredRuleIds = [];
      const deferredEdits = [];
      let baselineUndoEdits = [];
      for (const edit of draftEdits) {
        if (edit.kind !== prop) continue;
        if (edit.applyMode !== "selection-breadth-css" && edit.applyMode !== "cdp-stylesheet") continue;
        const refs = uniqueElements2(edit.refs || []);
        if (!refs.some((ref) => nextSet.has(ref))) continue;
        if (sameElementSet2(refs, nextTargets)) {
          if (!baselineUndoEdits.length && ((_a3 = edit.cdpUndoEdits) == null ? void 0 : _a3.length)) baselineUndoEdits = edit.cdpUndoEdits.slice();
          deferredEdits.push(edit);
          deferredRuleIds.push(...edit.selectionBreadthRuleIds || []);
        } else {
          if ((_b2 = edit.cdpUndoEdits) == null ? void 0 : _b2.length) await applyCdpStyleTextEdits(edit.cdpUndoEdits);
          immediateEdits.push(edit);
          immediateRuleIds.push(...edit.selectionBreadthRuleIds || []);
        }
      }
      removeDraftSelectionWriteRecords(immediateEdits, immediateRuleIds);
      return { baselineUndoEdits, deferredEdits, deferredRuleIds };
    }
    function draftEditSummaryBaseline(prop, writePlans) {
      var _a3;
      if (!state.draft) return null;
      const plannedTargets = uniqueElements2((writePlans || []).flatMap((writePlan) => writePlan.verificationTargets || []));
      if (!plannedTargets.length) return null;
      const previous = state.edits.slice(state.draft.editBase).find((edit) => {
        var _a4;
        return edit.kind === prop && sameElementSet2(edit.refs || [], plannedTargets) && ((_a4 = edit.beforeComputed) == null ? void 0 : _a4.length);
      });
      return ((_a3 = previous == null ? void 0 : previous.beforeComputed) == null ? void 0 : _a3.slice()) || null;
    }
    function commitDeferredDraftSelectionWrites(liveMerge) {
      removeDraftSelectionWriteRecords((liveMerge == null ? void 0 : liveMerge.deferredEdits) || [], (liveMerge == null ? void 0 : liveMerge.deferredRuleIds) || []);
    }
    function removeDraftSelectionWriteRecords(edits, ruleIds) {
      if (!(edits == null ? void 0 : edits.length)) return;
      removeSelectionBreadthRules(ruleIds || []);
      const removeSet = new Set(edits);
      state.edits = state.edits.filter((edit) => !removeSet.has(edit));
    }
    function sameElementSet2(a, b) {
      const left = uniqueElements2(a || []);
      const right = uniqueElements2(b || []);
      if (left.length !== right.length) return false;
      const set = new Set(left);
      return right.every((item) => set.has(item));
    }
    function cdpStyleTextWithDeclaration(existingText, prop, value, _sourceProperty, refs = []) {
      return mergeExactCssDeclarations(existingText, cssDeclarationsForPatch(prop, value, refs));
    }
    function mergeExactCssDeclarations(existingText, patchText) {
      const declarations = parseCssDeclarationText(existingText);
      for (const [key, next] of parseCssDeclarationText(patchText)) {
        declarations.set(key, next);
      }
      return serializeCssDeclarations(declarations);
    }
    function parseCssDeclarationText(text) {
      const declarations = /* @__PURE__ */ new Map();
      String(text || "").split(";").forEach((item) => {
        const separator = item.indexOf(":");
        if (separator < 0) return;
        const name = item.slice(0, separator).trim();
        if (!name) return;
        declarations.set(name.toLowerCase(), {
          name,
          value: item.slice(separator + 1).trim()
        });
      });
      return declarations;
    }
    function serializeCssDeclarations(declarations) {
      return Array.from(declarations.values()).map((item) => `${item.name}: ${item.value};`).join(" ");
    }
    async function applyCdpStyleTextEdits(edits) {
      const provider = currentCdpStyleProvider();
      if (typeof provider !== "function") {
        syncCdpProviderConnection(false);
        return { ok: false };
      }
      try {
        recordFlowDebug("cdp-apply-request", {
          edits: (edits || []).map((edit) => ({
            mode: edit.mode || "",
            selector: edit.selector || "",
            property: edit.property || "",
            styleSheetId: edit.styleSheetId || "",
            ruleLocator: edit.ruleLocator || null,
            reason: edit.reason || ""
          }))
        });
        const response = await provider({
          action: "applyStyleTexts",
          edits
        });
        recordFlowDebug("cdp-apply-response", {
          ok: !!(response == null ? void 0 : response.ok),
          debug: (response == null ? void 0 : response.debug) || null,
          error: (response == null ? void 0 : response.error) || ""
        });
        syncCdpProviderConnection(!!(response == null ? void 0 : response.ok));
        return response || { ok: false };
      } catch (error) {
        recordFlowDebug("cdp-apply-error", {
          error: (error == null ? void 0 : error.message) || String(error)
        });
        syncCdpProviderConnection(false);
        throw error;
      }
    }
    function selectionBreadthOwnerTargets(owners, prop) {
      return (owners || []).map((owner) => {
        const relation = selectionBreadthPropertyTargets(owner, prop);
        return { owner, targets: relation.targets, relation };
      }).filter((item) => item.targets.length);
    }
    function recordEdit(edit, refs = targets()) {
      const { cdpUndoEdits, ...publicEdit } = edit || {};
      const full = {
        ...publicEdit,
        target: state.selected ? cssPath(state.selected) : null,
        appliedTargets: refs.map((el) => cssPath(el)),
        documentPaths: uniqueValues2(refs.map((el) => sourcePathForDocument(el.ownerDocument)).filter(Boolean)),
        visualSelection: summarizeVisualSelection(state.visualSelection),
        groupResult: summarizeGroupResult(state.groupResult),
        frozenSignature: state.frozenSignature,
        scope: state.scope,
        objectLevel: objectLadderLabel(state.visualSelection, state.objectIndex, state.objectLadder.length),
        scopeLevel: scopeLadderLabel(state.groupResult, state.scopeIndex, state.scopeLadder.length),
        count: refs.length,
        time: (/* @__PURE__ */ new Date()).toISOString()
      };
      Object.defineProperty(full, "refs", { value: refs.slice(), enumerable: false });
      if (edit.scopeRefs) Object.defineProperty(full, "scopeRefs", { value: edit.scopeRefs.slice(), enumerable: false });
      if (cdpUndoEdits == null ? void 0 : cdpUndoEdits.length) Object.defineProperty(full, "cdpUndoEdits", { value: cdpUndoEdits.slice(), enumerable: false });
      state.edits.push(full);
      state.dirty = true;
      refreshExportTestBridge();
      publishPanelViewModel();
    }
    function editSummaryGroups(edits) {
      const groups = /* @__PURE__ */ new Map();
      (edits || []).forEach((edit) => {
        const paths = uniqueValues2((edit.appliedTargets || []).filter(Boolean)).sort();
        const stateLabel = editStateLabel(edit.stateCondition);
        const key = `${paths.join("|") || edit.target || "unknown"}::${stateLabel}`;
        let group = groups.get(key);
        if (!group) {
          group = {
            id: `edit-summary-${groups.size}`,
            targetCount: Math.max(paths.length, edit.count || 0, 1),
            state: stateLabel,
            changes: /* @__PURE__ */ new Map(),
            refs: [],
            paths: []
          };
          groups.set(key, group);
        }
        group.refs = uniqueElements2([...group.refs || [], ...edit.refs || []]);
        group.paths = uniqueValues2([...group.paths || [], ...paths]);
        group.targetCount = Math.max(group.targetCount, group.refs.length, group.paths.length);
        const property = edit.kind === "textContent" ? "text" : edit.kind;
        const previous = group.changes.get(property);
        const before = (previous == null ? void 0 : previous.before) || editSummaryDisplayValue(property, editBeforeSummaryValue(edit));
        group.changes.set(property, {
          property,
          label: editPropertyLabel(property),
          before,
          after: editSummaryDisplayValue(property, String(edit.value ?? "")),
          color: isEditSummaryColor(property),
          failed: edit.applied === false,
          failureReason: edit.failureReason || ""
        });
      });
      return [...groups.values()].map((group) => ({
        ...group,
        changes: [...group.changes.values()]
      }));
    }
    function editBeforeSummaryValue(edit) {
      var _a3;
      const values = edit.kind === "textContent" ? edit.before : ((_a3 = edit.beforeComputed) == null ? void 0 : _a3.length) ? edit.beforeComputed : edit.before;
      const value = Array.isArray(values) ? values[0] : values;
      return String(value ?? "") || "未设置";
    }
    function editStateLabel(condition) {
      const kind = String((condition == null ? void 0 : condition.kind) || "").toLowerCase();
      if (!kind || kind === "default") return "";
      if (kind === "hover") return "Hover";
      if (kind === "focus" || kind === "focus-visible") return "Focus";
      if (kind === "checked") return "Checked";
      return kind;
    }
    function editPropertyLabel(property) {
      return {
        text: "文案",
        color: "文字色",
        fontFamily: "字体",
        fontSize: "字号",
        fontWeight: "字重",
        lineHeight: "行高",
        letterSpacing: "字距",
        backgroundColor: "填充色",
        borderColor: "边框色",
        borderRadius: "圆角",
        paddingX: "横向留白",
        paddingY: "纵向留白",
        width: "宽度",
        height: "高度",
        offsetX: "水平偏移",
        offsetY: "垂直偏移"
      }[property] || property;
    }
    function isEditSummaryColor(property) {
      return property === "color" || property === "backgroundColor" || property === "borderColor";
    }
    function editSummaryDisplayValue(property, value) {
      return isEditSummaryColor(property) ? comparableColorValue(value) : value;
    }
    function buildFrozenSignature(visual) {
      if (!(visual == null ? void 0 : visual.anchor)) return null;
      const el = visual.anchor;
      const cs = win().getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return {
        classes: stableClasses(el),
        attrs: stableAttrs(el),
        computed: {
          color: cs.color,
          backgroundColor: cs.backgroundColor,
          borderColor: computedBorderColor(cs),
          borderRadius: cs.borderRadius,
          boxShadow: cs.boxShadow,
          fontSize: cs.fontSize,
          display: cs.display
        },
        rect: {
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          x: Math.round(rect.left),
          y: Math.round(rect.top)
        }
      };
    }
    function summarizeVisualSelection(visual) {
      if (!(visual == null ? void 0 : visual.anchor)) return null;
      const layerSummary = {};
      Object.entries(visual.layers || {}).forEach(([key, el]) => {
        if (el) layerSummary[key] = cssPath(el);
      });
      return {
        anchor: cssPath(visual.anchor),
        raw: visual.raw ? cssPath(visual.raw) : null,
        roles: visual.roles || [],
        confidence: visual.confidence,
        reason: visual.reason,
        layers: layerSummary,
        textLeaves: (visual.textLeaves || []).map((el) => cssPath(el)).slice(0, 12)
      };
    }
    function summarizeGroupResult(result) {
      if (!result) return null;
      return {
        mode: result.mode,
        confidence: result.confidence,
        evidence: result.evidence || {},
        identityScope: result.identityScope ? {
          className: result.identityScope.className,
          confidence: result.identityScope.confidence,
          sharedClasses: result.identityScope.sharedClasses || [],
          sharedAttrs: result.identityScope.sharedAttrs || {},
          members: (result.identityScope.members || []).map((el) => cssPath(el)).slice(0, 80)
        } : null,
        selectedDiffSelector: result.selectedDiffSelector || null,
        members: (result.members || []).map((el) => cssPath(el)).slice(0, 80),
        rejected: (result.rejected || []).slice(0, 12)
      };
    }
    function summarizeSelectionBreadthPlan(plan) {
      if (!plan) return null;
      return {
        breadth: plan.breadth,
        parentScope: plan.parentScope,
        selectionOwner: plan.selectionOwner ? cssPath(plan.selectionOwner) : "",
        currentParent: plan.currentParent ? cssPath(plan.currentParent) : "",
        targetParents: (plan.targetParents || []).map((el) => cssPath(el)).slice(0, 40),
        structuralItems: (plan.structuralItems || []).map((el) => cssPath(el)).slice(0, 120),
        visualGroups: (plan.visualGroups || []).map((group) => ({
          id: group.id,
          count: group.items.length,
          selector: group.classificationSelector || "",
          selectorMode: group.classificationSelectorMode || "",
          fallbackReasons: group.fallbackReasons || [],
          items: (group.items || []).map((el) => cssPath(el)).slice(0, 80)
        })),
        targetGroups: (plan.targetGroups || []).map((group) => group.id),
        mechanicalTraits: plan.mechanicalTraits || null,
        capabilityGroups: plan.capabilityGroups || null,
        writePlans: (plan.writePlans || []).map((writePlan) => {
          var _a3, _b2, _c;
          return {
            groupId: writePlan.groupId,
            writeMode: writePlan.writeMode,
            selector: writePlan.materializedSelector,
            propertyWinningSelector: writePlan.propertyWinningSelector || "",
            writeRuleSelector: ((_a3 = writePlan.writeRule) == null ? void 0 : _a3.selector) || "",
            insertionAnchorSelector: ((_b2 = writePlan.insertionAnchorRule) == null ? void 0 : _b2.selector) || "",
            ownerTargets: (writePlan.ownerTargets || []).map((item) => {
              var _a4, _b3;
              return {
                owner: cssPath(item.owner),
                targets: item.targets.map((target) => cssPath(target)),
                relation: ((_a4 = item.relation) == null ? void 0 : _a4.kind) || "self",
                relationReason: ((_b3 = item.relation) == null ? void 0 : _b3.reason) || ""
              };
            }),
            verificationTargets: (writePlan.verificationTargets || []).map((target) => cssPath(target)),
            unavailableReason: writePlan.unavailableReason || "",
            fallbackReasons: writePlan.fallbackReasons || [],
            verification: ((_c = writePlan.verification) == null ? void 0 : _c.selector) ? {
              ok: writePlan.verification.selector.ok,
              expectedCount: writePlan.verification.selector.expectedCount,
              actualCount: writePlan.verification.selector.actualCount,
              reason: writePlan.verification.selector.reason || ""
            } : null
          };
        }),
        generatedCssRules: (plan.generatedCssRules || []).map((rule) => ({
          selector: rule.selector,
          property: rule.property,
          value: rule.value,
          mode: rule.mode,
          comment: rule.comment || ""
        })),
        fallbackReasons: plan.fallbackReasons || [],
        verificationResults: (plan.verificationResults || []).map((result) => ({
          ok: result.ok,
          selector: result.selector,
          expectedCount: result.expectedCount,
          actualCount: result.actualCount,
          reason: result.reason || ""
        }))
      };
    }
    async function revertEditList(edits) {
      const orderedEdits = [...edits || []].reverse();
      const cdpUndoEdits = orderedEdits.flatMap(
        (edit) => edit.applyMode === "selection-breadth-css" || edit.applyMode === "cdp-stylesheet" ? edit.cdpUndoEdits || [] : []
      );
      if (cdpUndoEdits.length) {
        const result = await applyCdpStyleTextEdits(cdpUndoEdits);
        if (!(result == null ? void 0 : result.ok)) throw new Error((result == null ? void 0 : result.error) || "CDP rejected the revert transaction");
      }
      for (const edit of orderedEdits) {
        const refs = edit.refs || [];
        if (edit.kind === "textContent") {
          refs.forEach((el, i2) => {
            if (el && el.isConnected) el.textContent = edit.before[i2] ?? "";
          });
          continue;
        }
        if (edit.applyMode === "selection-breadth-css" || edit.applyMode === "cdp-stylesheet") {
          removeSelectionBreadthRules(edit.selectionBreadthRuleIds || []);
          continue;
        }
        if (edit.kind.startsWith("hover.")) continue;
        refs.forEach((el, i2) => {
          if (el && el.isConnected && edit.kind in el.style) el.style[edit.kind] = edit.before[i2] ?? "";
        });
      }
    }
    function restoreDraftHoverStyle(draft) {
      const hoverStyle = doc().getElementById("dt-hover-edit-style");
      if (hoverStyle && draft.hoverStyleBefore == null) hoverStyle.remove();
      else if (hoverStyle) hoverStyle.textContent = draft.hoverStyleBefore;
    }
    function removeSelectionBreadthRules(ruleIds) {
      if (!(ruleIds == null ? void 0 : ruleIds.length)) return;
      const ids = new Set(ruleIds);
      const style = doc().getElementById("dt-selection-breadth-style");
      if (style) {
        const blocks = String(style.textContent || "").split(/(?=\/\* selection-breadth-\d+ \*\/)/g);
        style.textContent = blocks.filter((block) => {
          var _a3;
          const id = (_a3 = block.match(/\/\* (selection-breadth-\d+) \*\//)) == null ? void 0 : _a3[1];
          return !id || !ids.has(id);
        }).join("");
      }
      state.selectionBreadthRules = (state.selectionBreadthRules || []).filter((rule) => !(rule.ruleIds || []).some((id) => ids.has(id)));
    }
    function renderAll() {
      renderMarks();
      renderCaptureMode();
      refreshExportTestBridge();
      publishPanelViewModel();
    }
    function renderCaptureMode() {
      const locked = !!(state.settleArmed || state.draft || state.frozen || state.selectMode);
      const now = $("#dt-mode-now");
      const settle = $("#dt-mode-settle");
      const select = $("#dt-select");
      now == null ? void 0 : now.classList.toggle("dt-active", state.captureMode === "now");
      settle == null ? void 0 : settle.classList.toggle("dt-active", state.captureMode === "settle");
      if (now) now.disabled = locked;
      if (settle) settle.disabled = locked;
      if (select) {
        select.textContent = state.settleArmed ? "等待停稳" : state.draft && state.selectMode ? "选择中" : "选择";
        select.disabled = locked;
      }
    }
    function objectLadderLabel(visual, index, total) {
      if (!(visual == null ? void 0 : visual.anchor)) return "无选区";
      const roles = visual.roles || [];
      let name = visual.anchor.tagName.toLowerCase();
      if (roles.includes("text-leaf")) name = "文字";
      else if (roles.includes("media")) name = "媒体";
      else if (roles.includes("control")) name = "控件";
      else if (roles.includes("surface")) name = "视觉对象";
      else if (roles.includes("layout")) name = "布局层";
      return `${index + 1}/${Math.max(total, 1)} ${name}`;
    }
    function scopeLadderLabel(result, index, total) {
      var _a3;
      if (!result) return "当前";
      const count = ((_a3 = result.members) == null ? void 0 : _a3.length) || 0;
      const labels = {
        "fallback-single": "当前",
        "selection-single": "当前",
        "selection-breadth-loading": "广度计算中",
        "selection-similar-kind": "同视觉类型",
        "selection-all-kind": "全部同类",
        "selection-table-similar-cells": "同表相似单元格",
        "selection-table-row": "当前行",
        "selection-table-column": "当前列",
        "selection-table-all-cells": "整表单元格",
        "selection-table-all-similar-cells": "所有相似表格相似单元格",
        "selection-table-all-similar-rows": "所有相似表格对应行",
        "selection-table-all-similar-columns": "所有相似表格对应列",
        "selection-table-all-similar-cells-all": "所有相似表格单元格",
        "sibling-repeat": "同父级",
        "cousin-slot": "同位",
        "pattern-area": "同区域同类",
        "cross-region": "跨区域同类",
        "class-repeat": "同类",
        "visual-fingerprint": "视觉同类"
      };
      const label = labels[result.mode] || "范围";
      const state2 = stateConditionLabel(result);
      return `${index + 1}/${Math.max(total, 1)} ${label}${state2 ? ` · ${state2}` : ""} · ${count || 1} 个`;
    }
    function stateConditionLabel(result = state.groupResult) {
      const condition = result == null ? void 0 : result.selectedDiffSelector;
      if (condition && condition.confidence >= 0.72) return "当前状态";
      const label = stateContextLabel(state.selectionStateContext);
      if (label) return label;
      if (state.selectionStateContext) return "";
      if (isConfirmedHoverSelection()) return "hover";
      return "";
    }
    function stateConditionHint() {
      const label = stateConditionLabel();
      if (!label || state.scope !== "group") return "";
      return label === "hover" ? "当前为 hover 状态样式，其他同类 hover 时生效。" : "当前为状态样式，其他同类进入相同状态时生效。";
    }
    function publishPanelViewModel() {
      if (!panelStore) return;
      panelStore.publish(buildPanelViewModel());
    }
    function currentCdpStyleProvider() {
      return cdpStyleProvider || window.__DESIGNTOOLS_CDP_STYLE_PROVIDER__;
    }
    function currentCdpProviderMeta() {
      return window.__DESIGNTOOLS_CDP_STYLE_PROVIDER_META__ || {};
    }
    function syncCdpProviderConnection(connected) {
      const next = !!connected;
      if (state.cdpProviderConnected === next) return;
      state.cdpProviderConnected = next;
      publishPanelViewModel();
    }
    function hasCdpStyleProvider() {
      return typeof currentCdpStyleProvider() === "function";
    }
    function buildPanelViewModel() {
      var _a3, _b2, _c, _d;
      const hasSelection = !!state.selected;
      const breadthLoading = hasSelection && ((_a3 = state.groupResult) == null ? void 0 : _a3.mode) === "selection-breadth-loading";
      const writePlanLoading = hasSelection && !!state.selectionBreadthWritePlansLoading;
      const editLoading = breadthLoading || writePlanLoading;
      const capabilities = hasSelection ? propertyCapabilitiesForSelection() : [];
      const controls = hasSelection ? capabilities.map(capabilityToPanelControl) : [];
      const entries = [];
      state.snapshots.forEach((snap, index) => {
        var _a4;
        return entries.push({
          key: String(index),
          index: index + 1,
          active: String(state.activeTab) === String(index),
          draft: false,
          editCount: ((_a4 = snap.edits) == null ? void 0 : _a4.length) || 0,
          createdAt: snap.createdAt
        });
      });
      if (state.draft) {
        entries.push({
          key: "draft",
          index: state.snapshots.length + 1,
          active: state.activeTab === "draft",
          draft: true,
          editCount: Math.max(0, state.edits.length - state.draft.editBase)
        });
      }
      const activeEntry = state.activeTab === "empty" && entries.length ? entries[entries.length - 1] : null;
      const activeTab = activeEntry ? activeEntry.key === "draft" ? "draft" : Number(activeEntry.key) : state.activeTab;
      const activeSnapshotIndex = typeof activeTab === "number" ? activeTab : null;
      const activeSnapshot = activeSnapshotIndex == null ? null : state.snapshots[activeSnapshotIndex];
      const draftEdits = state.draft ? state.edits.slice(state.draft.editBase) : [];
      const textHint = breadthLoading ? "广度轴计算中，正在确认可编辑范围。" : writePlanLoading ? "写入规则计算中，正在确认可编辑属性。" : hasSelection ? textEditHint(capabilities) : "";
      const controlValues = hasSelection ? buildPanelControlValues(state.visualSelection || resolveVisualSelection(state.selected)) : emptyPanelControlValues();
      state.panelRevision = (state.panelRevision || 0) + 1;
      return {
        revision: state.panelRevision,
        sourceName,
        sourceKind: runtimeSource.kind,
        runtimeMode,
        status: ((_b2 = $("#dt-status")) == null ? void 0 : _b2.textContent) || "浏览中",
        backendConnected: hasCdpStyleProvider() && state.cdpProviderConnected !== false,
        backendPort: String(currentCdpProviderMeta().port || ""),
        captureMode: state.captureMode,
        selectLabel: state.settleArmed ? "等待停稳" : state.draft && state.selectMode ? "选择中" : "选择",
        selectActive: !!(state.selectMode || state.settleArmed),
        settleArmed: !!state.settleArmed,
        activeTab,
        tabs: entries.map((item) => ({ ...item, active: String(item.key) === String(activeTab) })),
        selection: buildPanelSelectionViewModel(),
        controls,
        textHint,
        draftPanel: {
          hasSelection,
          loading: !!editLoading,
          hasEditableText: hasSelection && !!capabilities.find((cap) => cap.key === "text" && cap.enabled),
          textHint,
          controls,
          densityExpanded: !!state.densityExpanded,
          values: controlValues,
          fontFamily: {
            current: hasSelection ? currentFontFamilyValue() : "",
            options: hasSelection ? fontFamilyCandidates() : []
          },
          summaries: panelEditSummaries(draftEdits)
        },
        snapshotPanel: activeSnapshot ? {
          index: activeSnapshotIndex + 1,
          createdAt: activeSnapshot.createdAt,
          editCount: ((_c = activeSnapshot.edits) == null ? void 0 : _c.length) || 0,
          summaries: panelEditSummaries(activeSnapshot.edits || []),
          captureDataUrl: ((_d = activeSnapshot.capture) == null ? void 0 : _d.imageDataUrl) || ""
        } : null,
        footer: {
          visible: !!(state.draft || state.settleArmed),
          canApply: hasDraftEdits(),
          canCancel: !!(state.draft || state.settleArmed)
        },
        dirty: !!state.dirty,
        editCount: state.edits.length
      };
    }
    function panelEditSummaries(edits) {
      return editSummaryGroups(edits).map(({ refs, paths, ...summary }) => summary);
    }
    function buildPanelSelectionViewModel() {
      var _a3, _b2, _c, _d, _e;
      if (!state.selected || !state.visualSelection) {
        return {
          hasSelection: false,
          key: "empty",
          stateHint: "",
          copyEnabled: false,
          breadthLoading: false,
          object: panelStepper("无选区", 0, 0),
          scope: panelStepper("当前", 0, 0)
        };
      }
      return {
        hasSelection: true,
        key: [
          cssPath(state.selected),
          state.objectIndex,
          state.scopeIndex,
          ((_a3 = state.groupResult) == null ? void 0 : _a3.mode) || "",
          ((_b2 = state.selectionStateContext) == null ? void 0 : _b2.kind) || ((_c = currentSelectionStateContext()) == null ? void 0 : _c.kind) || "default",
          closestCell((_d = state.visualSelection) == null ? void 0 : _d.anchor) ? state.tableScopeView : ""
        ].join("|"),
        stateHint: stateConditionHint(),
        copyEnabled: !!selectionPayloadData(),
        breadthLoading: ((_e = state.groupResult) == null ? void 0 : _e.mode) === "selection-breadth-loading",
        object: panelStepper(
          objectLadderLabel(state.visualSelection, state.objectIndex, state.objectLadder.length),
          state.objectIndex,
          state.objectLadder.length
        ),
        scope: panelStepper(
          scopeLadderLabel(state.groupResult, state.scopeIndex, state.scopeLadder.length),
          state.scopeIndex,
          state.scopeLadder.length
        ),
        tableScope: panelTableScopeViewModel()
      };
    }
    function panelTableScopeViewModel() {
      var _a3, _b2, _c, _d, _e, _f;
      const cell = closestCell((_a3 = state.visualSelection) == null ? void 0 : _a3.anchor);
      if (!cell) return { visible: false, checked: false, disabled: false, label: "应用到所有相似表格", fullSimilarCount: 0, currentTableCount: 0, signature: "" };
      const plan = state.tableScopePlan;
      const currentCount = ((_e = (_d = (_c = (_b2 = plan == null ? void 0 : plan.views) == null ? void 0 : _b2["current-table"]) == null ? void 0 : _c.find((scope) => {
        var _a4;
        return ((_a4 = scope == null ? void 0 : scope.evidence) == null ? void 0 : _a4.scopeKind) === "similar";
      })) == null ? void 0 : _d.members) == null ? void 0 : _e.length) || 0;
      return {
        visible: true,
        checked: state.tableScopeView === "all-similar-tables",
        disabled: !plan,
        label: "应用到所有相似表格",
        fullSimilarCount: ((_f = plan == null ? void 0 : plan.fullSimilarCells) == null ? void 0 : _f.length) || 0,
        currentTableCount: currentCount,
        signature: (plan == null ? void 0 : plan.signature) || ""
      };
    }
    function panelStepper(label, index, total) {
      const count = Math.max(total || 0, 0);
      return {
        label,
        index,
        total: count,
        canStepDown: index > 0,
        canStepUp: count > 0 && index < count - 1
      };
    }
    function capabilityToPanelControl(cap) {
      var _a3, _b2, _c, _d, _e;
      const prop = cap.prop || cap.key;
      const needsWritePlan = prop && prop !== "textContent";
      const writePlanReady = !needsWritePlan || selectionBreadthWritePlanCacheReady(prop);
      const writePlanAttempted = !needsWritePlan || selectionBreadthWritePlanAttempted(prop);
      const waitingForWritePlan = cap.enabled && needsWritePlan && !writePlanReady && !writePlanAttempted;
      const writePlanUnavailable = cap.enabled && needsWritePlan && !writePlanReady && writePlanAttempted;
      const reason = cap.reason || (waitingForWritePlan ? "写入规则计算中，请稍候。" : "") || (writePlanUnavailable ? selectionBreadthWritePlanUnavailableReason(prop) : "");
      return {
        key: cap.key,
        prop: cap.prop,
        group: cap.group,
        show: cap.show,
        enabled: cap.enabled && writePlanReady,
        reason,
        failureReason: state.failedControls.get(cap.prop || cap.key) || state.failedControls.get(cap.key) || "",
        route: {
          prop: ((_a3 = cap.route) == null ? void 0 : _a3.prop) || "",
          route: ((_b2 = cap.route) == null ? void 0 : _b2.route) || "",
          visible: !!((_c = cap.route) == null ? void 0 : _c.visible),
          reason: ((_d = cap.route) == null ? void 0 : _d.reason) || "",
          targets: (((_e = cap.route) == null ? void 0 : _e.targets) || []).map((el) => cssPath(el))
        }
      };
    }
    function emptyPanelControlValues() {
      return {
        text: "",
        colors: {},
        ranges: {},
        boxes: {},
        boxDiagram: {},
        fontWeight: {
          value: "400",
          title: "400"
        }
      };
    }
    function buildPanelControlValues(visual) {
      return {
        text: panelTextValue(visual),
        colors: {
          "dt-color": panelColorValue("color", visual),
          "dt-bg": panelColorValue("backgroundColor", visual),
          "dt-border": panelColorValue("borderColor", visual)
        },
        ranges: {
          "dt-font": panelFontSizeValue("dt-font", visual, 14),
          "dt-line-height": panelStaticRangeValue("dt-line-height", "lineHeight", visual, 1.2, { min: 1, max: 2.4, step: 0.05 }),
          "dt-letter-spacing": panelStaticRangeValue("dt-letter-spacing", "letterSpacing", visual, 0, { min: -2, max: 12, step: 0.1 }),
          "dt-radius": panelRadiusValue("dt-radius", visual, 0),
          "dt-padding": panelStaticRangeValue("dt-padding", "padding", visual, 0, { min: 0, max: 200, step: 1 }),
          "dt-padding-x": panelStaticRangeValue("dt-padding-x", "paddingX", visual, 0, { min: 0, max: 200, step: 1 }),
          "dt-padding-y": panelStaticRangeValue("dt-padding-y", "paddingY", visual, 0, { min: 0, max: 200, step: 1 }),
          "dt-width": panelWidthRangeValue("dt-width", visual, 0),
          "dt-height": panelStaticRangeValue("dt-height", "height", visual, 0, { min: 0, max: 900, step: 1 }),
          "dt-offset-x": panelStaticRangeValue("dt-offset-x", "offsetX", visual, 0, { min: -120, max: 120, step: 1 }),
          "dt-offset-y": panelStaticRangeValue("dt-offset-y", "offsetY", visual, 0, { min: -120, max: 120, step: 1 })
        },
        boxes: {
          "dt-width": panelBoxWidthValue("dt-width", visual, 0),
          "dt-height": panelBoxPxValue("dt-height", "height", visual, 0),
          "dt-padding-left": panelBoxPxValue("dt-padding-left", "paddingLeft", visual, 0),
          "dt-padding-right": panelBoxPxValue("dt-padding-right", "paddingRight", visual, 0),
          "dt-padding-top": panelBoxPxValue("dt-padding-top", "paddingTop", visual, 0),
          "dt-padding-bottom": panelBoxPxValue("dt-padding-bottom", "paddingBottom", visual, 0)
        },
        boxDiagram: panelBoxDiagramValues(visual),
        fontWeight: panelFontWeightValue(visual)
      };
    }
    function panelTextValue(visual) {
      const textRoute = resolveStyleRoute("textContent", visual);
      return textRoute.targets.length === 1 ? textRoute.targets[0].innerText || textRoute.targets[0].textContent || "" : "";
    }
    function panelColorValue(prop, visual) {
      const route = resolveStyleRoute(prop, visual);
      if (!route.targets.length) return { value: "", defaultValue: "", isDefault: false, swatch: "#fff" };
      const cs = win().getComputedStyle(route.targets[0]);
      const value = prop === "borderColor" ? computedBorderColor(cs) : firstVisibleColor(cs[prop], "");
      const actual = value || "";
      return {
        value: actual ? `${actual} (默认)` : "",
        defaultValue: actual,
        isDefault: !!actual,
        swatch: normalizeStyleValue("color", actual) || "#fff"
      };
    }
    function panelFontWeightValue(visual) {
      const route = resolveStyleRoute("fontWeight", visual);
      if (!route.targets.length) return { value: "400", title: fontWeightTitle("400") };
      const weight = normalizedFontWeight(win().getComputedStyle(route.targets[0]).fontWeight);
      const value = String(nearestFontWeightOption(weight));
      return { value, title: fontWeightTitle(value) };
    }
    function panelFontSizeValue(id, visual, fallback) {
      const route = resolveStyleRoute("fontSize", visual);
      if (!route.targets.length) return panelRangeValue("", 6, 120, 1, "px");
      const target = route.targets[0];
      const cs = win().getComputedStyle(target);
      const px = parseFloat(cs.fontSize) || fallback;
      const parent = target.parentElement ? win().getComputedStyle(target.parentElement) : null;
      const parentPx = parseFloat(parent == null ? void 0 : parent.fontSize) || px;
      const rootPx = parseFloat(win().getComputedStyle(doc().documentElement).fontSize) || 16;
      const unitValue = panelUnitValue(id, "px");
      const value = fontSizeFromPxWithMetrics(px, unitValue, { parentPx, rootPx });
      const config = fontSizeRangeConfig(value, unitValue);
      const formatted = formatFontSizeValue(value, unitValue);
      return panelRangeValue(formatted, config.min, config.max, config.step, unitValue, {
        currentPx: String(px),
        parentPx: String(parentPx),
        rootPx: String(rootPx)
      });
    }
    function panelWidthRangeValue(id, visual, fallback) {
      const route = resolveStyleRoute("width", visual);
      if (!route.targets.length) return panelRangeValue("", 0, 1200, 2, "px");
      const data = panelWidthMetrics(route.targets[0], fallback, id);
      return panelRangeValue(data.value, data.min, data.max, data.step, data.unit, data.metrics);
    }
    function panelStaticRangeValue(id, prop, visual, fallback, config) {
      const route = resolveStyleRoute(prop, visual);
      if (!route.targets.length) return panelRangeValue("", config.min, config.max, config.step);
      const target = route.targets[0];
      const cs = win().getComputedStyle(target);
      let value;
      if (prop === "lineHeight") {
        const fontSize = parseFloat(cs.fontSize) || 16;
        const lineHeight = parseFloat(cs.lineHeight) || fontSize * (fallback || 1.2);
        value = Math.max(1, Math.min(2.4, lineHeight / fontSize));
      } else if (prop === "letterSpacing") {
        value = Math.max(-2, Math.min(12, cs.letterSpacing === "normal" ? 0 : parseFloat(cs.letterSpacing) || fallback || 0));
      } else if (prop === "paddingX") {
        value = average([parseFloat(cs.paddingLeft) || 0, parseFloat(cs.paddingRight) || 0]);
      } else if (prop === "paddingY") {
        value = average([parseFloat(cs.paddingTop) || 0, parseFloat(cs.paddingBottom) || 0]);
      } else if (prop === "padding") {
        value = Math.round(parseFloat(cs.paddingTop) || fallback || 0);
      } else if (prop === "height") {
        const rect = target.getBoundingClientRect();
        value = Math.round(parseFloat(cs.height) || rect.height || fallback || 0);
      } else if (prop === "offsetX" || prop === "offsetY") {
        value = parseFloat(comparableStyleValue(cs, prop)) || fallback || 0;
      } else {
        value = Math.round(parseFloat(cs[prop]) || fallback || 0);
      }
      return panelRangeValue(formatRangeValue(value, config.step), config.min, config.max, config.step);
    }
    function panelRadiusValue(id, visual, fallback) {
      const route = resolveStyleRoute("borderRadius", visual);
      if (!route.targets.length) return panelRangeValue("", 0, 60, 1);
      const target = route.targets[0];
      const current = Math.round(parseFloat(win().getComputedStyle(target).borderRadius) || fallback || 0);
      const config = radiusRangeConfig(target);
      return panelRangeValue(String(current), config.min, config.max, config.step, "", {
        sliderValue: String(Math.min(current, config.max)),
        inputMax: "9999"
      });
    }
    function panelBoxWidthValue(id, visual, fallback) {
      const route = resolveStyleRoute("width", visual);
      if (!route.targets.length) return panelBoxValue("", 0, 1200, 1, "px", false);
      const data = panelWidthMetrics(route.targets[0], fallback, id);
      return panelBoxValue(data.value, data.min, data.max, data.step, data.unit, data.isDefault, data.metrics);
    }
    function panelBoxPxValue(id, prop, visual, fallback) {
      const route = resolveStyleRoute(prop, visual);
      if (!route.targets.length) return panelBoxValue("", 0, 9999, 1, "px", false);
      const explicit = explicitLayoutValue(prop);
      if (explicit != null) return panelBoxValue(String(Math.round(parseFloat(explicit) || 0)), 0, 9999, 1, "px", false);
      const target = route.targets[0];
      const cs = win().getComputedStyle(target);
      const rect = target.getBoundingClientRect();
      const value = prop === "height" ? rect.height || parseFloat(cs.height) || fallback || 0 : parseFloat(comparableStyleValue(cs, prop)) || fallback || 0;
      return panelBoxValue(String(Math.round(value)), 0, 9999, 1, "px", prop === "height");
    }
    function panelWidthMetrics(target, fallback, id) {
      var _a3, _b2, _c;
      const rect = target.getBoundingClientRect();
      const cs = win().getComputedStyle(target);
      const px = rect.width || parseFloat(cs.width) || fallback || 0;
      const parentWidth = ((_b2 = (_a3 = target.parentElement) == null ? void 0 : _a3.getBoundingClientRect) == null ? void 0 : _b2.call(_a3).width) || px || 1;
      const rootPx = parseFloat(win().getComputedStyle(doc().documentElement).fontSize) || 16;
      const explicit = explicitLayoutValue("width");
      const unit = ((_c = explicit == null ? void 0 : explicit.match(/[a-z%]+$/i)) == null ? void 0 : _c[0]) || panelUnitValue(id, "px");
      const sourcePx = explicit != null ? widthToPxWithMetrics(parseFloat(explicit) || 0, unit, { parentPx: parentWidth, rootPx }) : px;
      const value = widthFromPxWithMetrics(sourcePx, unit, { parentPx: parentWidth, rootPx });
      const config = widthRangeConfig(value, unit);
      return {
        value: formatWidthValue(value, unit),
        min: config.min,
        max: config.max,
        step: config.step,
        unit,
        isDefault: explicit == null,
        metrics: {
          currentPx: String(sourcePx),
          parentPx: String(parentWidth),
          rootPx: String(rootPx)
        }
      };
    }
    function panelBoxDiagramValues(visual) {
      const boxes = {
        "dt-width": panelBoxWidthValue("dt-width", visual, 0),
        "dt-height": panelBoxPxValue("dt-height", "height", visual, 0),
        "dt-padding-left": panelBoxPxValue("dt-padding-left", "paddingLeft", visual, 0),
        "dt-padding-right": panelBoxPxValue("dt-padding-right", "paddingRight", visual, 0),
        "dt-padding-top": panelBoxPxValue("dt-padding-top", "paddingTop", visual, 0),
        "dt-padding-bottom": panelBoxPxValue("dt-padding-bottom", "paddingBottom", visual, 0)
      };
      return {
        "dt-box-width-value": panelDiagramValue(boxes["dt-width"]),
        "dt-box-height-value": panelDiagramValue(boxes["dt-height"]),
        "dt-box-padding-left-value": panelDiagramValue(boxes["dt-padding-left"]),
        "dt-box-padding-right-value": panelDiagramValue(boxes["dt-padding-right"]),
        "dt-box-padding-top-value": panelDiagramValue(boxes["dt-padding-top"]),
        "dt-box-padding-bottom-value": panelDiagramValue(boxes["dt-padding-bottom"])
      };
    }
    function panelDiagramValue(value) {
      return (value == null ? void 0 : value.value) ? `${value.value}${value.unit || "px"}` : "-";
    }
    function panelRangeValue(value, min, max2, step, unit = "", metrics = {}) {
      return {
        value: String(value ?? ""),
        min: String(min),
        max: String(max2),
        step: String(step),
        unit,
        progress: rangeProgressValue(value, min, max2),
        ...metrics
      };
    }
    function panelBoxValue(value, min, max2, step, unit, isDefault, metrics = {}) {
      return {
        value: String(value ?? ""),
        min: String(min),
        max: String(max2),
        step: String(step),
        unit,
        isDefault: !!isDefault,
        ...metrics
      };
    }
    function rangeProgressValue(value, min, max2) {
      const start = Number(min) || 0;
      const end = Number(max2) || start + 1;
      const n = Number(value) || 0;
      const pct = (n - start) / Math.max(end - start, 1) * 100;
      return `${Math.max(0, Math.min(100, pct))}%`;
    }
    function panelUnitValue(id, fallback) {
      var _a3;
      return ((_a3 = $("#" + id + "-unit")) == null ? void 0 : _a3.dataset.value) || fallback;
    }
    function dispatchPanelCommand(command) {
      if (runtimeMode === "review" && !["copyPrompt", "export", "setActiveTab", "previewEditSummary", "panelRendered"].includes(command.type)) {
        toast("当前为只读评审模式，请使用 VibePolish 打开工程包继续编辑。");
        return;
      }
      switch (command.type) {
        case "setCaptureMode":
          setCaptureMode(command.mode);
          break;
        case "startSelection":
          startSelectionFlow();
          break;
        case "export":
          exportCurrentArtifact();
          break;
        case "copyPrompt":
          copyPrompt();
          break;
        case "applySource":
          applyCurrentSource();
          break;
        case "saveSourceAs":
          saveCurrentSourceAs();
          break;
        case "setActiveTab":
          clearEditSummaryPreview();
          state.activeTab = command.tab;
          renderAll();
          break;
        case "stepObject":
          stepObject(command.delta);
          break;
        case "stepScope":
          stepScope(command.delta);
          break;
        case "setTableScopeView":
          setTableScopeView(command.view);
          break;
        case "copySelection":
          copySelectionPayload();
          break;
        case "updateProperty":
          applyStyle(command.key, command.value);
          break;
        case "updateText":
          applyText(command.value);
          break;
        case "editTextInput":
          handleTextInput(command.value);
          break;
        case "editTextCommit":
          applyText(command.value);
          break;
        case "editColorInput":
          handleColorInput(command.id, command.prop, command.value);
          break;
        case "focusColorInput":
          clearDefaultColorValue($("#" + command.id));
          break;
        case "copyColorInput":
          copyColorControlValue(command.id);
          break;
        case "openColorPopover":
          openColorPopover(command.id, command.prop, $("#" + command.id + "-swatch"));
          break;
        case "setColorFormat":
          setColorFormat(command.format);
          break;
        case "applyActiveColor":
          applyActiveColor(command.value, { close: !!command.close });
          break;
        case "clearActiveColor":
          clearActiveColor();
          break;
        case "toggleMenu":
          toggleMenuField(command.fieldId);
          break;
        case "selectFontFamily":
          handleFontFamilySelect(command.value);
          break;
        case "selectFontWeight":
          handleFontWeightSelect(command.value);
          break;
        case "selectUnit":
          handleUnitSelect(command.id, command.unitKind, command.value);
          break;
        case "editRangeInput":
          handleRangeInput(command.id, command.prop, command.value, command.source);
          break;
        case "editBoxInput":
          handleBoxInput(command.id, command.prop, command.value);
          break;
        case "toggleDensity":
          state.densityExpanded = !state.densityExpanded;
          updateDensityExpansion();
          break;
        case "applyDraft":
          applyDraft();
          break;
        case "cancelDraft":
          cancelDraft();
          break;
        case "rollbackSnapshot":
          rollbackSnapshot(command.index);
          break;
        case "previewEditSummary":
          previewEditSummary(command.summaryId, command.active);
          break;
        case "panelRendered":
          if (command.revision === state.panelRevision) bindDraftControls();
          break;
      }
    }
    function copySelectionPayload() {
      const payload = selectionPayloadData();
      if (!payload) return;
      copyText(JSON.stringify(payload, null, 2));
    }
    function selectionPayloadData() {
      var _a3;
      const visual = state.visualSelection;
      const group = state.groupResult;
      if (!state.selected || !(visual == null ? void 0 : visual.anchor) || !group) return null;
      group.selectedDiffSelector || null;
      return {
        source: sourceName,
        anchor: cssPath(visual.anchor),
        raw: state.selectedRaw ? cssPath(state.selectedRaw) : cssPath(state.selected),
        object: {
          index: state.objectIndex,
          total: state.objectLadder.length || 1,
          label: objectLadderLabel(visual, state.objectIndex, state.objectLadder.length),
          selector: cssPath(visual.anchor),
          roles: visual.roles || [],
          confidence: visual.confidence || 0,
          reason: visual.reason || ""
        },
        range: {
          index: state.scopeIndex,
          total: state.scopeLadder.length || 1,
          label: scopeLadderLabel(group, state.scopeIndex, state.scopeLadder.length),
          mode: group.mode || "fallback-single",
          count: ((_a3 = group.members) == null ? void 0 : _a3.length) || 1,
          members: (group.members || [visual.anchor]).map((el) => cssPath(el))
        },
        state: selectionStatePayload(group)
      };
    }
    function selectionStatePayload(group = state.groupResult) {
      const label = stateConditionLabel(group) || "default";
      if (label === "hover") {
        return {
          label,
          source: "pseudo-hover",
          selector: ":hover"
        };
      }
      if (label === "focus") {
        const context = currentSelectionStateContext();
        return {
          label,
          source: "pseudo-focus",
          selector: (context == null ? void 0 : context.selector) || ":focus"
        };
      }
      if (label === "checked") {
        return {
          label,
          source: "pseudo-checked",
          selector: ":checked"
        };
      }
      if (label === "selected") {
        return {
          label,
          source: "aria-selected",
          selector: '[aria-selected="true"]'
        };
      }
      if (label === "pressed") {
        return {
          label,
          source: "aria-pressed",
          selector: '[aria-pressed="true"]'
        };
      }
      const condition = group == null ? void 0 : group.selectedDiffSelector;
      if (condition && condition.confidence >= 0.72) {
        return {
          label,
          source: condition.source || "state-diff",
          selector: condition.selector,
          token: condition.token || null,
          value: condition.value || null,
          confidence: condition.confidence
        };
      }
      return { label: "default", selector: null };
    }
    function fontWeightOptions() {
      return [
        { value: "300", title: "300 Light" },
        { value: "400", title: "400 Regular" },
        { value: "500", title: "500 Medium" },
        { value: "600", title: "600 Semibold" },
        { value: "700", title: "700 Bold" },
        { value: "800", title: "800 Extra Bold" },
        { value: "900", title: "900 Black" }
      ];
    }
    function fontFamilyCandidates() {
      const current = currentFontFamilyValue();
      const pageFamilies = collectTextLeaves([doc().body]).map((el) => win().getComputedStyle(el).fontFamily).filter(Boolean);
      return uniqueValues2([current, ...pageFamilies, "sans-serif", "serif", "monospace"]);
    }
    function currentFontFamilyValue() {
      const route = resolveStyleRoute("fontFamily", state.visualSelection);
      if (!route.targets.length) return "";
      return win().getComputedStyle(route.targets[0]).fontFamily || "";
    }
    function propertyCapabilitiesForSelection() {
      if (!state.visualSelection) return [];
      const model = selectionCapabilityModel(state.visualSelection);
      return PROPERTY_CONTROL_ORDER.map((key) => propertyCapability(key, state.visualSelection, model));
    }
    function propertyCapability(key, visual, model = selectionCapabilityModel(visual)) {
      const control = { prop: key === "text" ? "textContent" : key };
      const route = resolveCapabilityRoute(control.prop, visual);
      return buildPropertyCapability({
        key,
        route,
        traits: model.traits,
        groupCapability: model.groups[propertyGroup(key)],
        isContentEditableTarget: isContentEditableSelection
      });
    }
    function resolveCapabilityRoute(prop, visual) {
      return visual === state.visualSelection ? resolveCurrentStyleRoute(prop) : resolveStyleRoute(prop, visual);
    }
    function selectionCapabilityModel(visual) {
      const roles = (visual == null ? void 0 : visual.roles) || [];
      const anchor = visual == null ? void 0 : visual.anchor;
      const tableCell = isTableCellElement(anchor);
      const table = isTableElement(anchor);
      const icon = isIconLikeElement(anchor);
      const traits = {
        directText: roles.includes("text-leaf") && !tableCell,
        replacedMedia: isMediaElement(anchor) && !icon,
        icon,
        tableCell,
        table,
        fragmentedInline: isInlineLayoutElement(anchor) && !isMediaElement(anchor),
        stableBox: hasStableBoxModel(anchor)
      };
      return { traits, groups: buildCapabilityGroups(traits) };
    }
    function isTableCellElement(el) {
      var _a3;
      if (!el || el.nodeType !== 1) return false;
      const tag = (_a3 = el.tagName) == null ? void 0 : _a3.toLowerCase();
      if (tag === "td" || tag === "th") return true;
      const display = win().getComputedStyle(el).display;
      return display === "table-cell";
    }
    function isTableElement(el) {
      var _a3;
      if (!el || el.nodeType !== 1) return false;
      const tag = (_a3 = el.tagName) == null ? void 0 : _a3.toLowerCase();
      if (tag === "table") return true;
      return win().getComputedStyle(el).display === "table";
    }
    function isTablePartElement(el) {
      var _a3;
      if (!el || el.nodeType !== 1) return false;
      if (isTableCellElement(el)) return true;
      const tag = (_a3 = el.tagName) == null ? void 0 : _a3.toLowerCase();
      if (["thead", "tbody", "tfoot", "tr", "col", "colgroup", "caption"].includes(tag)) return true;
      return /^(table-row|table-header-group|table-row-group|table-footer-group|table-column|table-column-group|table-caption)$/.test(win().getComputedStyle(el).display || "");
    }
    function isInlineLayoutElement(el) {
      if (!el || el.nodeType !== 1) return false;
      const display = win().getComputedStyle(el).display;
      return display === "inline";
    }
    function hasStableBoxModel(el) {
      if (!el || el.nodeType !== 1) return false;
      const display = win().getComputedStyle(el).display;
      if (!display || display === "none" || display === "contents") return false;
      return display !== "inline" || isMediaElement(el);
    }
    function isIconLikeElement(el) {
      var _a3;
      if (!el || ((_a3 = el.tagName) == null ? void 0 : _a3.toLowerCase()) !== "svg") return false;
      const rect = el.getBoundingClientRect();
      return rect.width <= 48 && rect.height <= 48;
    }
    function textEditHint(capabilities = propertyCapabilitiesForSelection()) {
      if (!state.selected || !state.visualSelection) return "";
      const hasText = !!(state.selected.textContent || "").trim();
      if (!hasText) return "";
      const textCap = capabilities.find((cap) => cap.key === "text");
      if (textCap && !textCap.enabled) return "该选区包含多种文字样式，请点选具体文字后编辑";
      return "";
    }
    function isMediaElement(el) {
      return /^(img|picture|video|canvas|svg)$/i.test((el == null ? void 0 : el.tagName) || "");
    }
    function isFormElement(el) {
      return /^(input|textarea|select)$/i.test((el == null ? void 0 : el.tagName) || "");
    }
    function isControlElement(el) {
      var _a3, _b2, _c;
      if (!el) return false;
      if (/^(button|a|input|textarea|select|summary|label)$/i.test(el.tagName || "")) return true;
      const role = (_a3 = el.getAttribute) == null ? void 0 : _a3.call(el, "role");
      if (/^(button|link|menuitem|tab|checkbox|radio|switch)$/i.test(role || "")) return true;
      if ((_b2 = el.hasAttribute) == null ? void 0 : _b2.call(el, "onclick")) return true;
      const tabIndex = (_c = el.getAttribute) == null ? void 0 : _c.call(el, "tabindex");
      if (tabIndex != null && Number(tabIndex) >= 0) return true;
      return hasPointerControlBoundary(el);
    }
    function hasPointerControlBoundary(el) {
      const cursor = originalCursorByElement.get(el) || win().getComputedStyle(el).cursor;
      if (cursor !== "pointer") return false;
      const parent = el.parentElement;
      if (!parent || parent === doc().body || parent === doc().documentElement) return true;
      const parentCursor = originalCursorByElement.get(parent) || win().getComputedStyle(parent).cursor;
      return parentCursor !== "pointer";
    }
    function isIconOnlyControl(control) {
      return !!control && !compactText(control.textContent || "");
    }
    function closestControlElement(el, includeSelf = true) {
      let node = includeSelf ? el : el == null ? void 0 : el.parentElement;
      while (node && node.nodeType === 1 && node !== doc().body && node !== doc().documentElement) {
        if (isControlElement(node)) return node;
        node = node.parentElement;
      }
      return null;
    }
    function isTextLeaf(el) {
      if (!el || isMediaElement(el) || isFormElement(el)) return false;
      const text = directVisibleText(el);
      if (!text) return false;
      return ![...el.children || []].some((child) => isVisible(child) && hasVisibleText(child));
    }
    function isInlineTextHost(el) {
      if (!el || isMediaElement(el) || isFormElement(el)) return false;
      if (!directVisibleText(el)) return false;
      const visibleTextChildren = [...el.children || []].filter((child) => isVisible(child) && hasVisibleText(child));
      if (!visibleTextChildren.length) return false;
      return visibleTextChildren.every(isInlineTextFragment);
    }
    function isInlineTextFragment(el) {
      if (!el || isMediaElement(el) || isFormElement(el)) return false;
      const cs = win().getComputedStyle(el);
      if (cs.display === "contents") return true;
      if (!cs.display.startsWith("inline")) return false;
      return [...el.children || []].filter((child) => isVisible(child) && hasVisibleText(child)).every(isInlineTextFragment);
    }
    function directVisibleText(el) {
      return [...el.childNodes || []].filter((node) => node.nodeType === 3).map((node) => node.textContent || "").join("").trim();
    }
    function hasVisibleText(el) {
      return !!(el && isVisible(el) && (el.textContent || "").trim());
    }
    function hasBackground(el) {
      return !isTransparentColor(win().getComputedStyle(el).backgroundColor);
    }
    function hasBorder(el) {
      const cs = win().getComputedStyle(el);
      return ["Top", "Right", "Bottom", "Left"].some((side) => {
        return (parseFloat(cs[`border${side}Width`]) || 0) > 0 && !isTransparentColor(cs[`border${side}Color`]);
      });
    }
    function hasRadius(el) {
      return (parseFloat(win().getComputedStyle(el).borderRadius) || 0) > 0;
    }
    function hasShadow(el) {
      const shadow = win().getComputedStyle(el).boxShadow;
      return !!shadow && shadow !== "none";
    }
    function hasPadding(el) {
      const cs = win().getComputedStyle(el);
      return ["Top", "Right", "Bottom", "Left"].some((side) => (parseFloat(cs[`padding${side}`]) || 0) > 0);
    }
    function hasLayout(el) {
      const cs = win().getComputedStyle(el);
      if (!cs.display.includes("flex") && !cs.display.includes("grid")) return false;
      return [...el.children || []].filter(isVisible).length >= 2;
    }
    function isPageLike(el) {
      if (!el || el === doc().body || el === doc().documentElement) return true;
      const rect = el.getBoundingClientRect();
      const viewportW = Math.max(win().innerWidth || 0, 1);
      const viewportH = Math.max(win().innerHeight || 0, 1);
      return rect.width >= viewportW * 0.9 && rect.height >= viewportH * 0.85;
    }
    function hasConsistentComputedValue(elements, prop) {
      const values = elements.map((el) => comparableStyleValue(win().getComputedStyle(el), prop)).filter(Boolean);
      return values.length > 0 && new Set(values).size === 1;
    }
    function comparableStyleValue(cs, prop) {
      if (prop === "fontSize") return String(Math.round((parseFloat(cs.fontSize) || 0) * 2) / 2);
      if (prop === "fontWeight") return String(normalizedFontWeight(cs.fontWeight));
      if (prop === "fontFamily") return cs.fontFamily || "";
      if (prop === "letterSpacing") return cs.letterSpacing === "normal" ? "0px" : cs.letterSpacing;
      if (prop === "paddingX") return `${cs.paddingLeft} ${cs.paddingRight}`;
      if (prop === "paddingY") return `${cs.paddingTop} ${cs.paddingBottom}`;
      if (isPaddingSideProp(prop)) return cs[prop];
      if (prop === "offsetX") return translateAxisValue(cs.translate, 0);
      if (prop === "offsetY") return translateAxisValue(cs.translate, 1);
      if (prop === "color" || prop === "backgroundColor" || prop === "borderColor") return comparableColorValue(cs[prop]);
      return cs[prop];
    }
    function comparableColorValue(value) {
      if (isTransparentColor(value)) return "transparent";
      return colorToHex(value) || value;
    }
    function translateAxisValue(value, axis) {
      const token = translateAxesFromValue(value)[axis] || "0px";
      const amount = parseFloat(token);
      return Number.isFinite(amount) ? `${Math.round(amount * 100) / 100}px` : "0px";
    }
    function comparableStyleValuesForTargets(list, prop) {
      return (list || []).map((el) => computedComparableStyleValue(el, prop));
    }
    function observableValidationTargets(stateContext, targets2) {
      if (isTransientStateContext(stateContext)) return targets2;
      const hoverHosts = state.hoverStateLocked ? uniqueElements2(state.hoverHosts || []).filter((host) => (host == null ? void 0 : host.isConnected) && elementHasOwnStateSelector(host, ":hover")) : [];
      const active = doc().activeElement;
      return (targets2 || []).filter((target) => {
        if (hoverHosts.some((host) => host === target || host.contains(target))) return false;
        if (active && active !== doc().body && active !== doc().documentElement) {
          if (confirmedFocusHostForSelection(target, active)) return false;
        }
        return true;
      });
    }
    function computedComparableStyleValue(el, prop) {
      if (!el || !el.isConnected) return "";
      const cs = win().getComputedStyle(el);
      if (prop === "borderColor") return comparableColorValue(computedBorderColor(cs));
      return comparableStyleValue(cs, prop);
    }
    function validateStyleApplication(prop, value, list, beforeComputed = []) {
      const targets2 = (list || []).filter((el) => el && el.isConnected);
      const computedAfter = comparableStyleValuesForTargets(targets2, prop);
      if (!value || !targets2.length) return { success: true, computedAfter };
      const expectedValue = targets2.map((el) => expectedComparableStyleValue(el, prop, value));
      const failures = computedAfter.map((actual, index) => ({
        actual,
        expected: expectedValue[index],
        before: beforeComputed[index],
        target: targets2[index]
      })).filter((item) => item.expected && !styleValuesMatch(prop, item.actual, item.expected));
      if (!failures.length) return { success: true, computedAfter, expectedValue };
      return {
        success: false,
        computedAfter,
        expectedValue,
        reason: `${cssProp(prop)} 写入后被页面原 CSS 覆盖，当前生效值为 ${failures[0].actual || "空"}，期望值为 ${failures[0].expected}。可复制 AI Patch 修改源 CSS。`
      };
    }
    function expectedComparableStyleValue(el, prop, value) {
      if (prop === "color" || prop === "backgroundColor" || prop === "borderColor") {
        const normalized = normalizeStyleValue(prop === "borderColor" ? "color" : prop, value);
        return comparableColorValue(normalized || "");
      }
      if (prop === "fontWeight") return String(normalizedFontWeight(value));
      if (prop === "fontFamily") return normalizeFontFamilyForCompare(value);
      if (prop === "lineHeight" && /^-?\d*\.?\d+$/.test(String(value || "").trim())) {
        const fontSize = parseFloat(win().getComputedStyle(el).fontSize) || 16;
        return `${fontSize * Number(value)}px`;
      }
      if (prop === "paddingX") return `${value} ${value}`;
      if (prop === "paddingY") return `${value} ${value}`;
      if (prop === "offsetX" || prop === "offsetY") return value;
      const probe = doc().createElement((el == null ? void 0 : el.tagName) || "div");
      probe.style.position = "absolute";
      probe.style.visibility = "hidden";
      probe.style.pointerEvents = "none";
      probe.style[prop] = value;
      ((el == null ? void 0 : el.parentElement) || doc().body).appendChild(probe);
      const result = computedComparableStyleValue(probe, prop);
      probe.remove();
      return result;
    }
    function styleValuesMatch(prop, actual, expected) {
      if (prop === "fontFamily") return normalizeFontFamilyForCompare(actual) === normalizeFontFamilyForCompare(expected);
      if (prop === "fontSize" || prop === "lineHeight" || prop === "letterSpacing" || prop === "offsetX" || prop === "offsetY" || isPaddingSideProp(prop)) return Math.abs((parseFloat(actual) || 0) - (parseFloat(expected) || 0)) < 0.6;
      if (prop === "paddingX" || prop === "paddingY") {
        const a = String(actual).split(/\s+/).map((value) => parseFloat(value) || 0);
        const e = String(expected).split(/\s+/).map((value) => parseFloat(value) || 0);
        return a.length === e.length && a.every((value, index) => Math.abs(value - e[index]) < 0.6);
      }
      if (prop === "width" || prop === "height" || prop === "padding" || prop === "borderRadius") {
        if (String(actual) === String(expected)) return true;
        return Math.abs((parseFloat(actual) || 0) - (parseFloat(expected) || 0)) < 0.6;
      }
      return String(actual || "").trim() === String(expected || "").trim();
    }
    function normalizeFontFamilyForCompare(value) {
      return String(value || "").replaceAll('"', "").replaceAll("'", "").replace(/\s+/g, " ").trim().toLowerCase();
    }
    function updateControlFailure(prop, validation) {
      if (validation == null ? void 0 : validation.success) clearControlFailure(prop);
      else setControlFailure(prop, (validation == null ? void 0 : validation.reason) || "该配置写入后未成为当前生效样式。");
    }
    function setControlFailure(prop, reason) {
      if (!prop) return;
      if (state.failedControls.get(prop) === reason) return;
      state.failedControls.set(prop, reason);
      publishPanelViewModel();
    }
    function clearControlFailure(prop) {
      if (!prop || !state.failedControls.has(prop)) return;
      state.failedControls.delete(prop);
      publishPanelViewModel();
    }
    function clearControlFailures() {
      if (!state.failedControls.size) return;
      state.failedControls.clear();
      publishPanelViewModel();
    }
    function normalizedFontWeight(value) {
      if (value === "bold") return 700;
      if (value === "normal") return 400;
      return Math.round(Number(value) || 400);
    }
    function isContentEditableSelection(el) {
      if (!el) return false;
      return isStructurallyEditableTextSelection(el);
    }
    function isStructurallyEditableTextSelection(el) {
      if (!el) return false;
      const textChildren = [...el.children || []].filter((child) => {
        const childText = (child.textContent || "").trim();
        if (!childText) return false;
        const rect = child.getBoundingClientRect();
        const cs = win().getComputedStyle(child);
        return rect.width > 1 && rect.height > 1 && cs.display !== "none" && cs.visibility !== "hidden";
      });
      return textChildren.length === 0;
    }
    function normalizedTextContent(el) {
      return String((el == null ? void 0 : el.textContent) || "").replace(/\s+/g, " ").trim();
    }
    function hasConsistentTextContent(list) {
      const values = (list || []).map(normalizedTextContent);
      return values.length > 0 && new Set(values).size === 1;
    }
    function suggestedTextImplementation(list, before, value) {
      const sourceText = normalizedTextForSource((before == null ? void 0 : before[0]) || "");
      const matchCount = sourceText ? countTextOccurrences(sourceHtml, sourceText) : 0;
      return {
        strategy: matchCount === 1 ? "replace-source-text-literal" : "regex-or-ast-text-replace",
        persistence: matchCount === 1 ? "stable-source-match" : "weak-source-match",
        matchCount,
        affects: list.length === 1 ? "single-text-leaf" : "same-text-leaf-group",
        before: sourceText,
        after: value,
        verify: ["match source occurrence count before writing", "rerender or refresh to confirm persistence"],
        fallback: "runtime-dom-textContent"
      };
    }
    function normalizedTextForSource(value) {
      return String(value || "").trim();
    }
    function countTextOccurrences(haystack, needle) {
      if (!needle) return 0;
      let count = 0;
      let index = 0;
      const text = String(haystack || "");
      while ((index = text.indexOf(needle, index)) >= 0) {
        count += 1;
        index += Math.max(needle.length, 1);
      }
      return count;
    }
    function bindDraftControls() {
      if (!state.draft || state.activeTab !== "draft") return;
      autoResizeTextInput($("#dt-text"));
      bindPanelDocumentHandlers();
    }
    function bindPanelDocumentHandlers() {
      bindColorPopoverDocumentClose();
      bindMenuDocumentClose("familyDocBound", "dt-family-field");
      bindMenuDocumentClose("weightDocBound", "dt-weight-field");
      bindMenuDocumentClose("fontUnitDocBound", "dt-font-unit-field");
      bindMenuDocumentClose("widthUnitDocBound", "dt-width-unit-field");
    }
    function bindMenuDocumentClose(flagName, fieldId) {
      if (state[flagName]) return;
      document.addEventListener("click", (e) => {
        const current = $("#" + fieldId);
        if (current && !current.contains(e.target)) current.classList.remove("dt-open");
      });
      state[flagName] = true;
    }
    function bindColorPopoverDocumentClose() {
      if (state.colorDocBound) return;
      state.colorDocBound = true;
      document.addEventListener("pointerdown", (e) => {
        var _a3, _b2;
        const active = $("#dt-color-popover");
        if (!active || !active.classList.contains("dt-open")) return;
        if (active.contains(e.target) || ((_b2 = (_a3 = e.target).closest) == null ? void 0 : _b2.call(_a3, ".dt-swatch"))) return;
        closeColorPopover();
      }, true);
    }
    function handleTextInput() {
      autoResizeTextInput($("#dt-text"));
    }
    function handleColorInput(id, prop, value) {
      const input = $("#" + id);
      if (!input) return;
      clearDefaultColorValue(input);
      input.value = value;
      const normalized = normalizeStyleValue(prop, value);
      if (value && normalized == null) {
        clearQueuedColorInput(id);
        input.setAttribute("aria-invalid", "true");
        setControlFailure(prop, "请输入有效的颜色值，如 HEX、RGB、RGBA 或颜色名称。");
        return;
      }
      input.removeAttribute("aria-invalid");
      clearControlFailure(prop);
      updateSwatch(id, normalized || value);
      queueColorInputApply(id, prop);
    }
    function queueColorInputApply(id, prop, value) {
      var _a3;
      if ((_a3 = state.colorInputTimers) == null ? void 0 : _a3.has(id)) clearTimeout(state.colorInputTimers.get(id));
      const timer = setTimeout(() => {
        state.colorInputTimers.delete(id);
        const input = $("#" + id);
        if (!input) return;
        const current = input.value.trim();
        const normalized = normalizeStyleValue(prop, current);
        if (current && normalized == null) return;
        queueLatestStyleApply(prop, normalized || current, 0);
      }, 220);
      state.colorInputTimers.set(id, timer);
    }
    function toggleMenuField(fieldId) {
      const field = $("#" + fieldId);
      if (!field) return;
      field.classList.toggle("dt-open");
    }
    function handleFontFamilySelect(value) {
      var _a3;
      (_a3 = $("#dt-family-field")) == null ? void 0 : _a3.classList.remove("dt-open");
      setFontFamilyButtonValue(value);
      applyStyle("fontFamily", value);
    }
    function handleFontWeightSelect(value) {
      var _a3;
      const actual = value || "400";
      (_a3 = $("#dt-weight-field")) == null ? void 0 : _a3.classList.remove("dt-open");
      setFontWeightButtonValue(actual);
      applyStyle("fontWeight", actual);
    }
    function handleUnitSelect(id, unitKind, value) {
      var _a3, _b2;
      if (unitKind === "font") {
        const input2 = $("#" + id);
        const button2 = $("#" + id + "-unit");
        if (!input2 || !button2) return;
        const previous2 = button2.dataset.value || "px";
        const px2 = Number(input2.dataset.currentPx) || fontSizeToPx(input2.value, previous2, input2);
        (_a3 = $("#" + id + "-unit-field")) == null ? void 0 : _a3.classList.remove("dt-open");
        setFontUnitButtonValue(id, value || "px");
        setFontSizeControlValue(id, px2, value || "px");
        return;
      }
      const input = $("#" + id);
      const button = $("#" + id + "-unit");
      if (!input || !button) return;
      const previous = button.dataset.value || "px";
      const px = Number(input.dataset.currentPx) || widthToPx(input.value, previous, input);
      (_b2 = $("#" + id + "-unit-field")) == null ? void 0 : _b2.classList.remove("dt-open");
      setWidthControlValue(id, px, value || "px");
      syncLayoutBoxDiagramFromInputs();
    }
    function handleRangeInput(id, prop, value, source) {
      const range = $("#" + id + "-range");
      const input = $("#" + id);
      if (!range || !input) return;
      if (prop === "fontSize") {
        handleFontSizeInput(id, value, source);
        return;
      }
      if (prop === "borderRadius") {
        handleRadiusInput(id, prop, value, source);
        return;
      }
      if (prop === "lineHeight") {
        handleStaticUnitRangeInput(id, prop, value, (display) => String(display), source);
        return;
      }
      if (prop === "letterSpacing") {
        handleStaticUnitRangeInput(id, prop, value, (display) => `${display}px`, source);
        return;
      }
      if (prop === "padding" || prop === "paddingX" || prop === "paddingY" || prop === "height" || prop === "offsetX" || prop === "offsetY") {
        handleStaticUnitRangeInput(id, prop, value, (display) => `${display}px`, source);
        return;
      }
      if (prop === "width") {
        handleWidthRangeInput(id, value, source);
        return;
      }
      const unit = $("#" + id + "-unit");
      if (!unit) return;
      if (source === "range") input.value = value;
      else range.value = value;
      updateRangeProgress(range);
      queueLatestStyleApply(prop, `${value}${unit.value}`);
    }
    function handleWidthRangeInput(id, value, source) {
      const range = $("#" + id + "-range");
      const input = $("#" + id);
      const unit = $("#" + id + "-unit");
      if (!range || !input || !unit) return;
      const unitValue = unit.dataset.value || "px";
      const normalized = normalizeWidthInput(value, unitValue);
      if (source === "range") input.value = normalized;
      range.value = normalized;
      input.dataset.currentPx = String(widthToPx(normalized, unitValue, input));
      updateRangeProgress(range);
      queueLatestStyleApply("width", `${normalized}${unitValue}`);
    }
    function handleStaticUnitRangeInput(id, prop, value, formatValue, source) {
      const range = $("#" + id + "-range");
      const input = $("#" + id);
      if (!range || !input) return;
      const next = clampNumber(value, Number(range.min || 0), Number(range.max || value));
      const display = formatRangeValue(next, range.step);
      if (source === "range") input.value = display;
      range.value = display;
      updateRangeProgress(range);
      queueLatestStyleApply(prop, formatValue(display));
    }
    function handleRadiusInput(id, prop, value, source) {
      const range = $("#" + id + "-range");
      const input = $("#" + id);
      if (!range || !input) return;
      const next = clampNumber(value, Number(range.min || 0), Number(range.max || value));
      if (source === "range") input.value = String(next);
      range.value = String(next);
      updateRangeProgress(range);
      queueLatestStyleApply(prop, `${next}px`);
    }
    function handleFontSizeInput(id, value, source) {
      const range = $("#" + id + "-range");
      const input = $("#" + id);
      const unit = $("#" + id + "-unit");
      if (!range || !input || !unit) return;
      if (source === "range") {
        const normalized = normalizeFontSizeInput(value, unit.dataset.value || "px");
        input.value = normalized;
        range.value = normalized;
        input.dataset.currentPx = String(fontSizeToPx(normalized, unit.dataset.value || "px", input));
        updateRangeProgress(range);
        queueLatestStyleApply("fontSize", `${normalized}${unit.dataset.value || "px"}`);
        return;
      }
      range.value = value;
      updateRangeProgress(range);
      const unitValue = unit.dataset.value || "px";
      queueLatestStyleApply("fontSize", `${value}${unitValue}`);
      input.dataset.currentPx = String(fontSizeToPx(value, unitValue, input));
    }
    function handleBoxInput(id, prop, value) {
      const input = $("#" + id);
      if (!input) return;
      if (prop === "width") {
        const unit = $("#" + id + "-unit");
        if (!unit) return;
        const unitValue = unit.dataset.value || "px";
        const normalized = normalizeWidthInput(value, unitValue);
        input.dataset.currentPx = String(widthToPx(normalized, unitValue, input));
        markExplicitLayoutValue("width", `${normalized}${unitValue}`);
        setLayoutInputDefaultState(input, false);
        queueLatestStyleApply("width", `${normalized}${unitValue}`);
        syncLayoutBoxDiagramFromInputs();
        scheduleLayoutSideEffectSync$1(id);
        return;
      }
      input.min = input.min || "0";
      input.max = input.max || "9999";
      input.step = "1";
      const clamped = clampNumber(value, Number(input.min), Number(input.max));
      const next = String(Math.round(clamped));
      markExplicitLayoutValue(prop, `${next}px`);
      if (prop === "height") setLayoutInputDefaultState(input, false);
      queueLatestStyleApply(prop, `${next}px`);
      syncLayoutBoxDiagramFromInputs();
      scheduleLayoutSideEffectSync$1(id);
    }
    function formatRangeValue(value, stepValue) {
      var _a3;
      const step = Number(stepValue || 1);
      const precision = step < 1 ? ((_a3 = String(step).split(".")[1]) == null ? void 0 : _a3.length) || 2 : 0;
      return precision ? Number(value).toFixed(precision).replace(/0+$/, "").replace(/\.$/, "") : String(Math.round(Number(value) || 0));
    }
    function clampNumber(value, min, max2) {
      const n = Number(value);
      if (!Number.isFinite(n)) return min;
      return Math.max(min, Math.min(max2, n));
    }
    function scheduleLayoutSideEffectSync$1(activeId) {
      scheduleLayoutSideEffectSync({
        requestFrame: requestAnimationFrame,
        hasSelected: () => !!state.selected,
        getVisualSelection: () => state.visualSelection,
        getSelectedVisual: () => resolveVisualSelection(state.selected),
        syncLayoutBoxControls,
        syncRangeControlFromRoute,
        scheduleOverlayRender
      }, activeId);
    }
    function isLayoutEffectSource$1(prop) {
      return isLayoutEffectSource(prop);
    }
    function controlIdForLayoutEffectSource$1(prop) {
      return controlIdForLayoutEffectSource(prop);
    }
    function markExplicitLayoutValue(prop, value) {
      explicitLayout.mark(prop, value);
    }
    function explicitLayoutValue(prop) {
      return explicitLayout.value(prop);
    }
    function updateDensityExpansion() {
      const panel = document.querySelector(".dt-tab-panel");
      const scrollTop = panel ? panel.scrollTop : 0;
      document.querySelectorAll(".dt-density-extra").forEach((row) => {
        row.hidden = !state.densityExpanded;
      });
      const toggle = $("#dt-density-toggle");
      if (!toggle) return;
      toggle.classList.toggle("dt-open", state.densityExpanded);
      toggle.setAttribute("aria-label", state.densityExpanded ? "收起密度细分" : "展开密度细分");
      toggle.title = state.densityExpanded ? "收起横向/纵向密度" : "展开横向/纵向密度";
      if (panel) panel.scrollTop = scrollTop;
      requestAnimationFrame(() => {
        const latest = document.querySelector(".dt-tab-panel");
        if (latest) latest.scrollTop = scrollTop;
      });
    }
    function renderMarks() {
      clearSelectionMarks();
      if (!state.selected) return;
      targets().forEach((el) => {
        if (el === state.selected) return;
        el.classList.add("dt-group");
        createMarkBox(el, "group");
      });
      state.selected.classList.add("dt-picked");
      createMarkBox(state.selected, "picked");
    }
    function previewEditSummary(summaryId, active) {
      var _a3;
      if (!active) {
        clearEditSummaryPreview();
        return;
      }
      const edits = state.activeTab === "draft" ? state.draft ? state.edits.slice(state.draft.editBase) : [] : Number.isInteger(state.activeTab) ? ((_a3 = state.snapshots[state.activeTab]) == null ? void 0 : _a3.edits) || [] : [];
      const summary = editSummaryGroups(edits).find((item) => item.id === summaryId);
      const documents = new Set(runtimeDocs());
      state.summaryPreviewRefs = uniqueElements2((summary == null ? void 0 : summary.refs) || []).filter((el) => (el == null ? void 0 : el.isConnected) && documents.has(el.ownerDocument) && isVisible(el));
      renderEditSummaryPreview();
    }
    function renderEditSummaryPreview() {
      removeMarkBoxes("summary");
      (state.summaryPreviewRefs || []).forEach((el) => createMarkBox(el, "summary"));
    }
    function clearEditSummaryPreview() {
      state.summaryPreviewRefs = [];
      removeMarkBoxes("summary");
    }
    function renderHoverHot(el, force) {
      if (state.hoverHot === el && !force) return;
      clearHoverHot();
      state.hoverHot = el;
      if (el && !el.classList.contains("dt-picked")) {
        if (!originalCursorByElement.has(el)) originalCursorByElement.set(el, win().getComputedStyle(el).cursor);
        el.classList.add("dt-hover-hot");
        createMarkBox(el, "hover");
      }
    }
    function clearHoverHot() {
      if (state.hoverHot) {
        state.hoverHot.classList.remove("dt-hover-hot");
        originalCursorByElement.delete(state.hoverHot);
      }
      state.hoverHot = null;
      removeMarkBoxes("hover");
    }
    function clearMarks() {
      clearSelectionMarks();
      clearHoverHot();
      clearEditSummaryPreview();
    }
    function clearSelectionMarks() {
      runtimeDocs().forEach((d) => {
        d.querySelectorAll(".dt-picked,.dt-group").forEach((el) => el.classList.remove("dt-picked", "dt-group"));
      });
      removeMarkBoxes("picked");
      removeMarkBoxes("group");
    }
    function scheduleOverlayRender() {
      cancelAnimationFrame(state.markRaf);
      state.markRaf = requestAnimationFrame(() => {
        positionInteractionShield();
        const hot = state.hoverHot;
        renderMarks();
        if (hot) renderHoverHot(hot, true);
        renderEditSummaryPreview();
      });
    }
    function ensureMarkLayer(targetDocument = doc()) {
      const d = targetDocument;
      let layer = d.getElementById("dt-mark-layer");
      if (!layer) {
        layer = d.createElement("div");
        layer.id = "dt-mark-layer";
        layer.className = "dt-mark-layer";
        d.body.appendChild(layer);
      }
      return layer;
    }
    function removeMarkBoxes(kind) {
      runtimeDocs().forEach((d) => {
        d.querySelectorAll(`.dt-mark-box[data-kind="${kind}"]`).forEach((el) => el.remove());
      });
    }
    function runtimeDocs() {
      const documents = Array.from(state.runtimeDocuments || []).filter((d) => d == null ? void 0 : d.documentElement);
      const active = doc();
      if (active && !documents.includes(active)) documents.push(active);
      return documents;
    }
    function createMarkBox(el, kind) {
      if (!el || !isVisible(el)) return;
      const rect = el.getBoundingClientRect();
      const inset = 5;
      const box = el.ownerDocument.createElement("div");
      box.className = `dt-mark-box dt-mark-box-${kind}`;
      box.dataset.kind = kind;
      box.style.left = `${rect.left - inset}px`;
      box.style.top = `${rect.top - inset}px`;
      box.style.width = `${rect.width + inset * 2}px`;
      box.style.height = `${rect.height + inset * 2}px`;
      const radius = parseFloat(win().getComputedStyle(el).borderRadius) || 0;
      box.style.borderRadius = `${Math.max(2, radius + inset)}px`;
      ensureMarkLayer(el.ownerDocument).appendChild(box);
    }
    function syncControls() {
      if (!state.selected) return;
      const visual = state.visualSelection || resolveVisualSelection(state.selected);
      const text = $("#dt-text");
      const textRoute = resolveCurrentStyleRoute("textContent");
      if (text) {
        if (!isActiveInputControl(text)) text.value = textRoute.targets.length >= 1 ? textRoute.targets[0].innerText || textRoute.targets[0].textContent || "" : "";
        autoResizeTextInput(text);
      }
      syncColorControlFromRoute("dt-color", "color", visual);
      syncColorControlFromRoute("dt-bg", "backgroundColor", visual);
      syncColorControlFromRoute("dt-border", "borderColor", visual);
      syncFontFamilyControl(visual);
      syncRangeControlFromRoute("dt-font", "fontSize", visual, 14);
      syncFontWeightControl(visual);
      syncRangeControlFromRoute("dt-line-height", "lineHeight", visual, 1.2);
      syncRangeControlFromRoute("dt-letter-spacing", "letterSpacing", visual, 0);
      syncRangeControlFromRoute("dt-radius", "borderRadius", visual, 0);
      syncLayoutBoxControls(visual);
      syncRangeControlFromRoute("dt-offset-x", "offsetX", visual, 0);
      syncRangeControlFromRoute("dt-offset-y", "offsetY", visual, 0);
    }
    function syncLayoutBoxControls(visual, options2 = {}) {
      const widthRoute = resolveStyleRoute("width", visual);
      if (widthRoute.targets.length) syncWidthControl("dt-width", widthRoute.targets[0], 0, options2);
      syncBoxPxControlFromRoute("dt-height", "height", visual, 0, options2);
      syncBoxPxControlFromRoute("dt-padding-left", "paddingLeft", visual, 0);
      syncBoxPxControlFromRoute("dt-padding-right", "paddingRight", visual, 0);
      syncBoxPxControlFromRoute("dt-padding-top", "paddingTop", visual, 0);
      syncBoxPxControlFromRoute("dt-padding-bottom", "paddingBottom", visual, 0);
      syncLayoutBoxDiagramFromInputs();
    }
    function syncBoxPxControlFromRoute(id, prop, visual, fallback, options2 = {}) {
      const input = $("#" + id);
      if (!input) return;
      if (options2.skipId === id) return;
      const preserveValue = isActiveInputControl(input);
      const route = resolveStyleRoute(prop, visual);
      if (!route.targets.length) {
        if (!preserveValue) input.value = "";
        setLayoutInputDefaultState(input, false);
        return;
      }
      const explicit = explicitLayoutValue(prop);
      if (explicit != null) {
        if (!preserveValue) input.value = String(Math.round(parseFloat(explicit) || 0));
        setLayoutInputDefaultState(input, false);
        return;
      }
      const target = route.targets[0];
      const cs = win().getComputedStyle(target);
      const rect = target.getBoundingClientRect();
      const value = prop === "height" ? rect.height || parseFloat(cs.height) || fallback || 0 : parseFloat(comparableStyleValue(cs, prop)) || fallback || 0;
      if (!preserveValue) input.value = String(Math.round(value));
      if (prop === "height") setLayoutInputDefaultState(input, true);
    }
    function syncLayoutBoxDiagramFromInputs() {
      setBoxDiagramValue("dt-box-width-value", diagramValueWithUnit("dt-width"));
      setBoxDiagramValue("dt-box-height-value", diagramValueWithUnit("dt-height"));
      setBoxDiagramValue("dt-box-padding-left-value", diagramValueWithUnit("dt-padding-left"));
      setBoxDiagramValue("dt-box-padding-right-value", diagramValueWithUnit("dt-padding-right"));
      setBoxDiagramValue("dt-box-padding-top-value", diagramValueWithUnit("dt-padding-top"));
      setBoxDiagramValue("dt-box-padding-bottom-value", diagramValueWithUnit("dt-padding-bottom"));
    }
    function diagramValueWithUnit(id) {
      var _a3;
      const input = $("#" + id);
      if (!input || input.value === "") return "-";
      const unit = ((_a3 = $("#" + id + "-unit")) == null ? void 0 : _a3.dataset.value) || "px";
      return `${input.value}${unit}`;
    }
    function setBoxDiagramValue(id, value) {
      const el = $("#" + id);
      if (el) el.textContent = value;
    }
    function setLayoutInputDefaultState(input, isDefault) {
      if (!input) return;
      input.classList.toggle("dt-default-value", !!isDefault);
      if (isDefault) input.dataset.layoutDefaultValue = input.value || "";
      else delete input.dataset.layoutDefaultValue;
    }
    function autoResizeTextInput(textarea) {
      if (!textarea) return;
      textarea.style.height = "30px";
      textarea.style.height = `${Math.min(textarea.scrollHeight, 64)}px`;
      textarea.style.overflowY = textarea.scrollHeight > 64 ? "auto" : "hidden";
    }
    function syncColorControlFromRoute(id, prop, visual) {
      const route = resolveStyleRoute(prop, visual);
      if (!route.targets.length) return;
      const cs = win().getComputedStyle(route.targets[0]);
      const value = prop === "borderColor" ? computedBorderColor(cs) : firstVisibleColor(cs[prop], "");
      setColorControlValue(id, value);
    }
    function syncFontFamilyControl(visual) {
      const button = $("#dt-family");
      if (!button) return;
      const route = resolveStyleRoute("fontFamily", visual);
      if (!route.targets.length) return;
      const value = win().getComputedStyle(route.targets[0]).fontFamily || "";
      const menu = $("#dt-family-menu");
      if (menu && ![...menu.querySelectorAll(".dt-family-option")].some((option) => option.dataset.fontFamily === value)) {
        menu.insertAdjacentHTML("afterbegin", `<button type="button" class="dt-family-option" data-font-family="${escapeAttr(value)}" title="${escapeAttr(value)}">${escapeHtml(value || "默认字体")}</button>`);
      }
      setFontFamilyButtonValue(value);
    }
    function setFontFamilyButtonValue(value) {
      const button = $("#dt-family");
      const label = button == null ? void 0 : button.querySelector("span");
      if (!button || !label) return;
      const actual = value || "";
      button.dataset.value = actual;
      button.title = actual;
      label.textContent = actual || "默认字体";
      const menu = $("#dt-family-menu");
      menu == null ? void 0 : menu.querySelectorAll(".dt-family-option").forEach((option) => {
        option.classList.toggle("dt-active", option.dataset.fontFamily === actual);
      });
    }
    function syncFontWeightControl(visual) {
      const button = $("#dt-weight");
      if (!button) return;
      const route = resolveStyleRoute("fontWeight", visual);
      const enabled = route.targets.length > 0;
      button.disabled = !enabled;
      if (!enabled) return;
      const weight = normalizedFontWeight(win().getComputedStyle(route.targets[0]).fontWeight);
      setFontWeightButtonValue(String(nearestFontWeightOption(weight)));
    }
    function setFontWeightButtonValue(value) {
      const button = $("#dt-weight");
      const label = button == null ? void 0 : button.querySelector("span");
      if (!button || !label) return;
      const actual = String(value || "400");
      button.dataset.value = actual;
      button.title = fontWeightTitle(actual);
      label.textContent = actual;
      const menu = $("#dt-weight-menu");
      menu == null ? void 0 : menu.querySelectorAll(".dt-weight-option").forEach((option) => {
        option.classList.toggle("dt-active", option.dataset.fontWeight === actual);
      });
    }
    function nearestFontWeightOption(weight) {
      const options2 = fontWeightOptions().map((item) => Number(item.value));
      return options2.reduce((best, value) => Math.abs(value - weight) < Math.abs(best - weight) ? value : best, 400);
    }
    function fontWeightTitle(value) {
      var _a3;
      return ((_a3 = fontWeightOptions().find((item) => item.value === String(value))) == null ? void 0 : _a3.title) || String(value || "");
    }
    function syncRangeControlFromRoute(id, prop, visual, fallback) {
      const route = resolveStyleRoute(prop, visual);
      if (!route.targets.length) return;
      const cs = win().getComputedStyle(route.targets[0]);
      if (prop === "fontSize") {
        syncFontSizeControl(id, route.targets[0], fallback);
        return;
      }
      if (prop === "borderRadius") {
        syncRadiusControl(id, route.targets[0], fallback);
        return;
      }
      if (prop === "lineHeight") {
        syncLineHeightControl(id, route.targets[0], fallback);
        return;
      }
      if (prop === "letterSpacing") {
        syncLetterSpacingControl(id, route.targets[0], fallback);
        return;
      }
      if (prop === "paddingX") {
        syncStaticPxControl(id, average([parseFloat(cs.paddingLeft) || 0, parseFloat(cs.paddingRight) || 0]));
        return;
      }
      if (prop === "paddingY") {
        syncStaticPxControl(id, average([parseFloat(cs.paddingTop) || 0, parseFloat(cs.paddingBottom) || 0]));
        return;
      }
      if (prop === "padding") {
        syncStaticPxControl(id, Math.round(parseFloat(cs.paddingTop) || fallback || 0));
        return;
      }
      if (prop === "height") {
        const rect = route.targets[0].getBoundingClientRect();
        syncStaticPxControl(id, Math.round(parseFloat(cs.height) || rect.height || fallback || 0));
        return;
      }
      if (prop === "width") {
        syncWidthControl(id, route.targets[0], fallback);
        return;
      }
      if (prop === "offsetX" || prop === "offsetY") {
        syncStaticPxControl(id, parseFloat(comparableStyleValue(cs, prop)) || fallback || 0);
        return;
      }
      const value = prop === "padding" ? cs.paddingTop : cs[prop];
      setRangeControlValue(id, Math.round(parseFloat(value) || fallback), "px");
    }
    function syncStaticPxControl(id, value) {
      setStaticUnitRangeValue(id, value);
    }
    function isActiveInputControl(el) {
      return !!(el && document.activeElement === el && /^(input|textarea)$/i.test(el.tagName || ""));
    }
    function syncWidthControl(id, target, fallback, options2 = {}) {
      var _a3, _b2, _c;
      const rect = target.getBoundingClientRect();
      const cs = win().getComputedStyle(target);
      const px = rect.width || parseFloat(cs.width) || fallback || 0;
      const parentWidth = ((_b2 = (_a3 = target.parentElement) == null ? void 0 : _a3.getBoundingClientRect) == null ? void 0 : _b2.call(_a3).width) || px || 1;
      const rootPx = parseFloat(win().getComputedStyle(doc().documentElement).fontSize) || 16;
      const input = $("#" + id);
      if (!input) return;
      input.dataset.currentPx = String(px);
      input.dataset.parentPx = String(parentWidth);
      input.dataset.rootPx = String(rootPx);
      if (options2.skipId === id) return;
      const unit = $("#" + id + "-unit");
      const explicit = explicitLayoutValue("width");
      if (explicit != null) {
        const unitValue = ((_c = explicit.match(/[a-z%]+$/i)) == null ? void 0 : _c[0]) || (unit == null ? void 0 : unit.dataset.value) || "px";
        const explicitPx = widthToPx(parseFloat(explicit) || 0, unitValue, input);
        input.dataset.currentPx = String(explicitPx);
        setWidthControlValue(id, explicitPx, unitValue);
        setLayoutInputDefaultState(input, false);
        return;
      }
      setWidthControlValue(id, px, (unit == null ? void 0 : unit.dataset.value) || "px");
      setLayoutInputDefaultState(input, true);
    }
    function syncLineHeightControl(id, target, fallback) {
      const cs = win().getComputedStyle(target);
      const fontSize = parseFloat(cs.fontSize) || 16;
      const lineHeight = parseFloat(cs.lineHeight) || fontSize * (fallback || 1.2);
      const ratio = Math.max(1, Math.min(2.4, lineHeight / fontSize));
      setStaticUnitRangeValue(id, ratio);
    }
    function syncLetterSpacingControl(id, target, fallback) {
      const cs = win().getComputedStyle(target);
      const value = cs.letterSpacing === "normal" ? 0 : parseFloat(cs.letterSpacing) || fallback || 0;
      setStaticUnitRangeValue(id, Math.max(-2, Math.min(12, value)));
    }
    function setStaticUnitRangeValue(id, value) {
      var _a3;
      const range = $("#" + id + "-range");
      const input = $("#" + id);
      if (!range || !input) return;
      const step = Number(range.step || 1);
      const precision = step < 1 ? ((_a3 = String(step).split(".")[1]) == null ? void 0 : _a3.length) || 2 : 0;
      const formatted = precision ? Number(value).toFixed(precision).replace(/0+$/, "").replace(/\.$/, "") : String(Math.round(Number(value) || 0));
      range.value = formatted;
      if (!isActiveInputControl(input)) input.value = formatted;
      updateRangeProgress(range);
    }
    function syncRadiusControl(id, target, fallback) {
      const cs = win().getComputedStyle(target);
      const current = Math.round(parseFloat(cs.borderRadius) || fallback || 0);
      const config = radiusRangeConfig(target);
      const range = $("#" + id + "-range");
      const input = $("#" + id);
      if (!range || !input) return;
      range.min = config.min;
      range.max = config.max;
      range.step = config.step;
      input.min = config.min;
      input.max = "9999";
      input.step = config.step;
      range.value = String(Math.min(current, config.max));
      input.value = String(current);
      updateRangeProgress(range);
    }
    function radiusRangeConfig(target) {
      var _a3;
      const rect = (_a3 = target == null ? void 0 : target.getBoundingClientRect) == null ? void 0 : _a3.call(target);
      const positiveCircle = rect ? Math.ceil(Math.max(0, Math.min(rect.width || 0, rect.height || 0) / 2)) : 60;
      const max2 = Math.max(1, positiveCircle);
      return { min: 0, max: max2, step: 1 };
    }
    function syncFontSizeControl(id, target, fallback) {
      const cs = win().getComputedStyle(target);
      const px = parseFloat(cs.fontSize) || fallback || 14;
      const parent = target.parentElement ? win().getComputedStyle(target.parentElement) : null;
      const parentPx = parseFloat(parent == null ? void 0 : parent.fontSize) || px;
      const rootPx = parseFloat(win().getComputedStyle(doc().documentElement).fontSize) || 16;
      const input = $("#" + id);
      const range = $("#" + id + "-range");
      const unit = $("#" + id + "-unit");
      if (!input || !range || !unit) return;
      input.dataset.currentPx = String(px);
      input.dataset.parentPx = String(parentPx);
      input.dataset.rootPx = String(rootPx);
      const unitValue = unit.dataset.value || "px";
      setFontSizeControlValue(id, px, unitValue);
    }
    function lockHover(el) {
      const hosts = el ? hoverHostsFor(el) : [];
      return lockHoverHosts(hosts, primaryHoverHostForElement(el));
    }
    function lockHoverAtLastPoint() {
      const primaryHost = primaryHoverHostForElement(state.hoveredRaw) || primaryHoverHostFromPoint(state.lastHoverPoint) || primaryHoverHostForElement(state.hovered || state.selected);
      const hosts = uniqueElements2([
        ...hoverHostsFor(primaryHost),
        ...hoverHostsFromCurrentPseudoState(),
        ...hoverHostsFromPoint(state.lastHoverPoint)
      ]);
      if (hosts.length) return lockHoverHosts(hosts, primaryHost);
      return lockHover(state.hoveredRaw || state.hovered || state.selected);
    }
    function lockFocusAtCurrentElement() {
      const active = deepestActiveElement();
      if (!active) return clearForceFocus("lock-focus-empty");
      state.interactionDocument = active.ownerDocument;
      const locks = [];
      let node = active;
      while (node && node.nodeType === 1 && !isPageLike(node)) {
        const selectors = node === active ? [":focus-visible", ":focus", ":focus-within"] : [":focus-within"];
        selectors.forEach((selector) => {
          var _a3;
          if (((_a3 = node.matches) == null ? void 0 : _a3.call(node, selector)) && elementHasOwnStateSelector(node, selector)) {
            locks.push({ host: node, selector });
          }
        });
        node = node.parentElement;
      }
      const hosts = uniqueElements2(locks.map((lock) => lock.host));
      hosts.forEach((host) => host.classList.add("dt-force-focus"));
      state.focusLocks = locks;
      state.focusStateLocked = !!locks.length;
      installFocusFreezeMirror();
      recordCdpPseudoDebug("lock-focus-hosts", {
        count: locks.length,
        hosts: locks.map((lock) => cssPath(lock.host)),
        selectors: locks.map((lock) => lock.selector)
      });
      return Promise.resolve(!!locks.length);
    }
    function deepestActiveElement() {
      const candidates = uniqueElements2([doc(), ...state.runtimeDocuments].map((runtimeDocument) => runtimeDocument == null ? void 0 : runtimeDocument.activeElement).filter((element) => {
        var _a3, _b2;
        return element && element !== ((_a3 = element.ownerDocument) == null ? void 0 : _a3.body) && element !== ((_b2 = element.ownerDocument) == null ? void 0 : _b2.documentElement);
      }));
      return candidates.sort((left, right) => documentNestingDepth(right.ownerDocument) - documentNestingDepth(left.ownerDocument))[0] || null;
    }
    function documentNestingDepth(documentNode) {
      var _a3;
      let depth = 0;
      let current = documentNode;
      while ((_a3 = current == null ? void 0 : current.defaultView) == null ? void 0 : _a3.frameElement) {
        depth += 1;
        current = current.defaultView.frameElement.ownerDocument;
      }
      return depth;
    }
    function lockHoverHosts(hosts, primaryHost = null) {
      hosts = uniqueElements2(hosts || []).filter(isElementNode);
      applyForceHoverClasses(hosts);
      installHoverFreezeMirror(hosts);
      state.hoverHosts = hosts;
      state.hoverPrimaryHost = primaryHost && hosts.includes(primaryHost) ? primaryHost : null;
      state.hoverStateLocked = !!hosts.length;
      recordCdpPseudoDebug("lock-hover-hosts", {
        count: hosts.length,
        hosts: hosts.map((el) => cssPath(el)),
        primaryHost: state.hoverPrimaryHost ? cssPath(state.hoverPrimaryHost) : ""
      });
      return Promise.resolve(!!hosts.length);
    }
    function hoverHostsFromPoint(point) {
      if (!point) return [];
      const d = point.document || doc();
      let stack = [];
      if (typeof d.elementsFromPoint === "function") {
        stack = Array.from(d.elementsFromPoint(point.x, point.y) || []);
      } else {
        const el = d.elementFromPoint(point.x, point.y);
        if (el) stack = [el];
      }
      return uniqueElements2(stack.flatMap((el) => hoverHostsFor(el)));
    }
    function hoverHostsFromCurrentPseudoState() {
      const d = doc();
      if (typeof d.querySelectorAll !== "function") return [];
      try {
        return uniqueElements2(Array.from(d.querySelectorAll(":hover") || []).filter(isElementNode));
      } catch {
        return [];
      }
    }
    function clearForceHover(source = "unknown") {
      var _a3, _b2;
      const hadPseudoState = state.hoverStateLocked || ((_a3 = state.hoverHosts) == null ? void 0 : _a3.length);
      recordCdpPseudoDebug("clear-hover-state", {
        source,
        hadPseudoState: !!hadPseudoState,
        count: ((_b2 = state.hoverHosts) == null ? void 0 : _b2.length) || 0,
        hosts: (state.hoverHosts || []).filter(isElementNode).map((el) => cssPath(el))
      });
      state.hoverHosts.forEach((el) => el.classList.remove("dt-force-hover"));
      state.hoverHosts = [];
      state.hoverPrimaryHost = null;
      state.hoverStateLocked = false;
      clearHoverFreezeMirror();
      return Promise.resolve(!!hadPseudoState);
    }
    function clearForceFocus(source = "unknown") {
      var _a3, _b2;
      const hadPseudoState = state.focusStateLocked || ((_a3 = state.focusLocks) == null ? void 0 : _a3.length);
      recordCdpPseudoDebug("clear-focus-state", {
        source,
        hadPseudoState: !!hadPseudoState,
        count: ((_b2 = state.focusLocks) == null ? void 0 : _b2.length) || 0,
        hosts: uniqueElements2((state.focusLocks || []).map((lock) => lock.host)).filter(isElementNode).map((el) => cssPath(el))
      });
      uniqueElements2((state.focusLocks || []).map((lock) => lock.host)).forEach((el) => el.classList.remove("dt-force-focus"));
      state.focusLocks = [];
      state.focusStateLocked = false;
      clearFocusFreezeMirror();
      return Promise.resolve(!!hadPseudoState);
    }
    function applyForceHoverClasses(hosts) {
      const next = uniqueElements2(hosts || []).filter(isElementNode);
      const current = uniqueElements2(state.hoverHosts || []).filter(isElementNode);
      current.forEach((el) => {
        if (!next.includes(el)) el.classList.remove("dt-force-hover");
      });
      next.forEach((el) => el.classList.add("dt-force-hover"));
    }
    function installHoverFreezeMirror(hosts) {
      clearHoverFreezeMirror();
      if (!(hosts == null ? void 0 : hosts.length)) return;
      state.hoverMirrorRegistry = installPseudoFreezeMirrorRules([":hover"], ".dt-force-hover");
    }
    function clearHoverFreezeMirror() {
      clearPseudoFreezeMirrorRules(".dt-force-hover");
      state.hoverMirrorRegistry = [];
    }
    function refreshHoverFreezeMirror() {
      const hosts = uniqueElements2(state.hoverHosts || []).filter(isElementNode);
      if (!state.hoverStateLocked || !hosts.length) return;
      installHoverFreezeMirror(hosts);
    }
    function installFocusFreezeMirror() {
      var _a3;
      clearFocusFreezeMirror();
      if (!state.focusStateLocked || !((_a3 = state.focusLocks) == null ? void 0 : _a3.length)) return;
      state.focusMirrorRegistry = installPseudoFreezeMirrorRules(
        [":focus-within", ":focus-visible", ":focus"],
        ".dt-force-focus"
      );
    }
    function clearFocusFreezeMirror() {
      clearPseudoFreezeMirrorRules(".dt-force-focus");
      state.focusMirrorRegistry = [];
    }
    function refreshFocusFreezeMirror() {
      var _a3;
      if (!state.focusStateLocked || !((_a3 = state.focusLocks) == null ? void 0 : _a3.length)) return;
      installFocusFreezeMirror();
    }
    function installPseudoFreezeMirrorRules(pseudoSelectors, markerSelector) {
      var _a3;
      const d = doc();
      if (!d) return [];
      const registry = [];
      for (const sheet of Array.from(d.styleSheets || [])) {
        const ownerId = ((_a3 = sheet.ownerNode) == null ? void 0 : _a3.id) || "";
        if (ownerId === "dt-freeze-runtime-style" || ownerId === "dt-selection-breadth-style") continue;
        installPseudoFreezeMirrorRulesInContainer(sheet, registry, pseudoSelectors, markerSelector);
      }
      return registry;
    }
    function installPseudoFreezeMirrorRulesInContainer(container, registry, pseudoSelectors, markerSelector) {
      var _a3;
      let rules;
      try {
        rules = container.cssRules;
      } catch {
        return;
      }
      if (!rules) return;
      for (let index = 0; index < rules.length; index += 1) {
        const rule = rules[index];
        const stateSelectors = rule.selectorText ? splitSelectorList(rule.selectorText).filter((selector) => pseudoSelectors.some((pseudo) => selector.includes(pseudo))) : [];
        if (stateSelectors.length) {
          const originalSelector = stateSelectors.join(", ");
          const mirrorSelector = stateSelectors.map((selector) => pseudoSelectors.reduce((result, pseudo) => result.replaceAll(pseudo, markerSelector), selector)).join(", ");
          try {
            container.insertRule(`${mirrorSelector}{${((_a3 = rule.style) == null ? void 0 : _a3.cssText) || ""}}`, index + 1);
            registry.push({ originalSelector, mirrorSelector });
            index += 1;
          } catch {
          }
          continue;
        }
        if (rule.cssRules && typeof rule.insertRule === "function") {
          installPseudoFreezeMirrorRulesInContainer(rule, registry, pseudoSelectors, markerSelector);
        }
      }
    }
    function clearPseudoFreezeMirrorRules(markerSelector) {
      const d = doc();
      for (const sheet of Array.from((d == null ? void 0 : d.styleSheets) || [])) {
        removePseudoFreezeMirrorRulesFromContainer(sheet, markerSelector);
      }
    }
    function removePseudoFreezeMirrorRulesFromContainer(container, markerSelector) {
      let rules;
      try {
        rules = container.cssRules;
      } catch {
        return;
      }
      if (!rules) return;
      for (let index = rules.length - 1; index >= 0; index -= 1) {
        const rule = rules[index];
        if (rule.selectorText && splitSelectorList(rule.selectorText).some((selector) => selector.includes(markerSelector))) {
          try {
            container.deleteRule(index);
          } catch {
          }
          continue;
        }
        if (rule.cssRules && typeof rule.deleteRule === "function") {
          removePseudoFreezeMirrorRulesFromContainer(rule, markerSelector);
        }
      }
    }
    function hoverHostsFor(el) {
      const hosts = [];
      let node = el;
      const viewportW = Math.max(win().innerWidth || 0, 1);
      const viewportH = Math.max(win().innerHeight || 0, 1);
      while (node && node.nodeType === 1 && node !== doc().body && node !== doc().documentElement) {
        hosts.push(node);
        const rect = node.getBoundingClientRect();
        const isViewportLike = rect.width >= viewportW * 0.9 && rect.height >= viewportH * 0.85;
        if (hosts.length > 1 && isViewportLike || hosts.length >= 8) break;
        node = node.parentElement;
      }
      return hosts;
    }
    function primaryHoverHostFromPoint(point) {
      if (!point) return null;
      const d = point.document || doc();
      const stack = typeof d.elementsFromPoint === "function" ? Array.from(d.elementsFromPoint(point.x, point.y) || []) : [d.elementFromPoint(point.x, point.y)].filter(Boolean);
      const hit = stack.find(isBusinessHitTestElement) || null;
      return primaryHoverHostForElement(hit);
    }
    function primaryHoverHostForElement(element) {
      let node = element;
      while (node && node.nodeType === 1 && !isPageLike(node)) {
        if (elementHasOwnStateSelector(node, ":hover")) return node;
        node = node.parentElement;
      }
      return null;
    }
    function normalizeTarget(el) {
      return resolveVisualSelection(el).anchor;
    }
    function resolveVisualSelection(rawElement, options2 = {}) {
      var _a3;
      const raw = normalizeRawHit(rawElement);
      if (!raw) return emptyVisualSelection(null, null, "empty");
      if (options2.preserveAnchor) return resolveVisualSelectionFromAnchor(raw);
      const iconControl = isIconLikeElement(raw) ? closestControlElement(raw, false) : null;
      if (iconControl && isIconOnlyControl(iconControl) && !isPageLike(iconControl)) return selfVisualSelection(iconControl, rawElement, ["control", "surface", "text-host"], 0.94, "control-icon-host");
      if (isMediaElement(raw)) return selfVisualSelection(raw, raw, ["media", "box"], 0.95, "media-self");
      if (isControlElement(raw)) return selfVisualSelection(raw, rawElement, ["control", "surface", "text-host"], 0.95, "control-self");
      if (isTextLeaf(raw)) return selfVisualSelection(raw, raw, ["text-leaf", "box"], 0.95, "text-leaf");
      const control = (_a3 = raw.closest) == null ? void 0 : _a3.call(raw, 'button,a,label,summary,[role="button"],[role="link"],[role="menuitem"],[role="tab"],[onclick],[tabindex]');
      if (control && !isPageLike(control)) return selfVisualSelection(control, rawElement, ["control", "surface", "text-host"], 0.92, "control-host");
      const visual = collectVisualLayers(raw);
      const layerList = visual.layerList;
      const anchor = chooseVisualAnchor(raw, visual.layers, layerList);
      const roles = rolesForVisualSelection(anchor, visual.layers, layerList);
      const confidence = layerList.length >= 2 ? 0.82 : layerList.length === 1 ? 0.68 : 0.35;
      return {
        id: visualIdFor(anchor),
        anchor,
        raw,
        layers: visual.layers,
        textLeaves: collectTextLeaves([anchor]),
        roles,
        confidence,
        reason: layerList.length ? "ancestor-visual-layers" : "raw-dom-fallback",
        selectors: {
          anchor: cssPath(anchor),
          raw: cssPath(raw)
        }
      };
    }
    function buildObjectLadder(rawElement) {
      const raw = normalizeRawHit(rawElement);
      if (!raw) return [];
      const auto = resolveVisualSelection(raw);
      const items = [auto];
      let node = raw;
      let depth = 0;
      while (node && node.nodeType === 1 && node !== doc().body && node !== doc().documentElement && depth < 7) {
        if (!isVisible(node) || isPageLike(node)) break;
        if ((sameVisualRegion(raw, node) || node === raw || node.contains(auto.anchor)) && isObjectLadderCandidate(raw, node, auto.anchor)) {
          items.push(resolveVisualSelectionFromAnchor(node));
        }
        node = node.parentElement;
        depth += 1;
      }
      return uniqueElementsBy(items.filter((item) => item == null ? void 0 : item.anchor), (item) => item.anchor).sort((a, b) => ancestorDistance(raw, a.anchor) - ancestorDistance(raw, b.anchor));
    }
    function isObjectLadderCandidate(raw, node, autoAnchor) {
      if (!node) return false;
      if (node === raw || node === autoAnchor) return true;
      if (isMediaElement(node) || isControlElement(node) || isTextLeaf(node)) return true;
      if (hasBackground(node) || hasBorder(node) || hasRadius(node) || hasShadow(node)) return true;
      return false;
    }
    function emptyVisualSelection(anchor, raw, reason) {
      return { anchor, raw, layers: {}, textLeaves: [], roles: [], confidence: 0, reason, selectors: {} };
    }
    function selfVisualSelection(anchor, raw, roles, confidence, reason) {
      const layers = {};
      if (hasBackground(anchor)) layers.background = anchor;
      if (hasBorder(anchor)) layers.border = anchor;
      if (hasRadius(anchor)) layers.radius = anchor;
      if (hasShadow(anchor)) layers.shadow = anchor;
      if (hasPadding(anchor) || hasLayout(anchor) || hasVisibleText(anchor)) layers.content = anchor;
      if (hasPadding(anchor)) layers.padding = anchor;
      return {
        id: visualIdFor(anchor),
        anchor,
        raw,
        layers,
        textLeaves: collectTextLeaves([anchor]),
        roles: uniqueValues2(roles),
        confidence,
        reason,
        selectors: {
          anchor: cssPath(anchor),
          raw: cssPath(raw || anchor)
        }
      };
    }
    function resolveVisualSelectionFromAnchor(anchor) {
      if (!anchor) return emptyVisualSelection(null, null, "empty-anchor");
      if (isMediaElement(anchor)) return selfVisualSelection(anchor, anchor, ["media", "box"], 0.95, "media-anchor");
      if (isControlElement(anchor)) return selfVisualSelection(anchor, anchor, ["control", "surface", "text-host"], 0.95, "control-anchor");
      if (isTextLeaf(anchor)) return selfVisualSelection(anchor, anchor, ["text-leaf", "box"], 0.95, "text-anchor");
      const layers = collectVisualLayersInsideAnchor(anchor);
      const layerList = uniqueElements2(Object.values(layers).filter(Boolean));
      const roles = rolesForVisualSelection(anchor, layers, layerList);
      return {
        id: visualIdFor(anchor),
        anchor,
        raw: anchor,
        layers,
        textLeaves: collectTextLeaves([anchor]),
        roles,
        confidence: layerList.length >= 2 ? 0.82 : layerList.length === 1 ? 0.68 : 0.5,
        reason: "anchor-visual-object",
        selectors: {
          anchor: cssPath(anchor),
          raw: cssPath(anchor)
        }
      };
    }
    function collectVisualLayersInsideAnchor(anchor) {
      const own = {};
      const anchorIsTable = isTableElement(anchor);
      if (hasBackground(anchor)) own.background = anchor;
      if (hasBorder(anchor)) own.border = anchor;
      if (hasRadius(anchor)) own.radius = anchor;
      if (hasShadow(anchor)) own.shadow = anchor;
      if (hasPadding(anchor)) own.padding = anchor;
      if (hasLayout(anchor) || hasVisibleText(anchor)) own.content = anchor;
      const descendants = [...anchor.querySelectorAll("*")].filter((el) => isVisible(el) && !isControlElement(el) && !isMediaElement(el) && isConfirmedCompositeLayerRelation(anchor, el)).slice(0, 36);
      descendants.forEach((el) => {
        if (!own.background && hasBackground(el)) own.background = el;
        if (!own.border && hasBorder(el)) own.border = el;
        if (!own.radius && hasRadius(el)) own.radius = el;
        if (!own.shadow && hasShadow(el)) own.shadow = el;
        if (!own.padding && !(anchorIsTable && isTablePartElement(el)) && hasPadding(el)) own.padding = el;
        if (!own.content && (hasLayout(el) || hasVisibleText(el))) own.content = el;
      });
      collectCompositeAncestorLayers(anchor, own);
      if (!own.content) own.content = anchor;
      return own;
    }
    function collectCompositeAncestorLayers(anchor, layers) {
      let node = anchor.parentElement;
      let depth = 0;
      while (node && !isPageLike(node) && depth < 4 && isConfirmedCompositeLayerRelation(anchor, node)) {
        if (!layers.border && hasBorder(node)) layers.border = node;
        if (!layers.shadow && hasShadow(node)) layers.shadow = node;
        if (hasBorder(node) && hasRadius(node)) layers.radius = node;
        else if (!layers.radius && hasRadius(node)) layers.radius = node;
        node = node.parentElement;
        depth += 1;
      }
    }
    function normalizeRawHit(el) {
      var _a3;
      if (!el || el.nodeType !== 1) return null;
      if (/^(path|g|use|defs|circle|rect|line|polyline|polygon)$/i.test(el.tagName)) return el.closest("svg") || el;
      if (isIconLikeElement(el)) {
        const control = (_a3 = el.closest) == null ? void 0 : _a3.call(el, 'button,a,label,summary,[role="button"],[role="link"],[role="menuitem"],[role="tab"],[onclick],[tabindex]');
        if (control && isIconOnlyControl(control) && !isPageLike(control)) return control;
      }
      return el;
    }
    function collectVisualLayers(rawElement) {
      const layers = {};
      const layerList = [];
      let node = rawElement;
      let depth = 0;
      while (node && node.nodeType === 1 && node !== doc().body && node !== doc().documentElement && depth < 6) {
        if (!isVisible(node) || isPageLike(node)) break;
        const contributed = [];
        if (!layers.background && hasBackground(node)) {
          layers.background = node;
          contributed.push("background");
        }
        if (!layers.border && hasBorder(node)) {
          layers.border = node;
          contributed.push("border");
        }
        if (!layers.radius && hasRadius(node)) {
          layers.radius = node;
          contributed.push("radius");
        }
        if (!layers.shadow && hasShadow(node)) {
          layers.shadow = node;
          contributed.push("shadow");
        }
        if (!layers.padding && hasPadding(node)) {
          layers.padding = node;
          contributed.push("padding");
        }
        if (!layers.content && (hasLayout(node) || hasVisibleText(node) || node === rawElement)) {
          layers.content = node;
          contributed.push("content");
        }
        if (contributed.length && sameVisualRegion(rawElement, node)) layerList.push(node);
        node = node.parentElement;
        depth += 1;
      }
      return { layers, layerList: uniqueElements2(layerList) };
    }
    function chooseVisualAnchor(raw, layers, layerList) {
      var _a3;
      if (!layerList.length) return raw;
      const candidates = layerList.filter((el) => el && !isPageLike(el) && sameVisualRegion(raw, el)).map((el) => {
        const score = visualAnchorScore(raw, el, layers);
        return { el, score };
      }).sort((a, b) => b.score - a.score);
      return ((_a3 = candidates[0]) == null ? void 0 : _a3.el) || layers.shadow || layers.border || layers.background || layers.radius || layers.content || raw;
    }
    function visualAnchorScore(raw, el, layers) {
      const roles = ["background", "border", "radius", "shadow"].filter((role) => layers[role] === el).length;
      const spacing = layers.padding === el || layers.content === el ? 1 : 0;
      const rr = raw.getBoundingClientRect();
      const er = el.getBoundingClientRect();
      const areaRatio = rectArea$1(rr) / Math.max(rectArea$1(er), 1);
      const depthPenalty = ancestorDistance(raw, el) * 0.16;
      const completeness = roles * 2 + spacing;
      const minimal = roles > 0 && areaRatio > 0.18 ? 1.4 : 0.2;
      return completeness + minimal - depthPenalty;
    }
    function sameVisualRegion(inner, outer) {
      if (!inner || !outer) return false;
      const a = inner.getBoundingClientRect();
      const b = outer.getBoundingClientRect();
      if (rectArea$1(a) <= 1 || rectArea$1(b) <= 1) return false;
      if (b.width > Math.max(a.width * 8, a.width + 520)) return false;
      if (b.height > Math.max(a.height * 8, a.height + 520)) return false;
      return rectOverlapRatio$1(a, b) >= 0.82;
    }
    function rolesForVisualSelection(anchor, layers, layerList) {
      const roles = [];
      if (isControlElement(anchor)) roles.push("control");
      if (isMediaElement(anchor)) roles.push("media", "box");
      if (layers.background || layers.border || layers.shadow || layers.radius) roles.push("surface");
      if (layers.content || hasLayout(anchor)) roles.push("layout");
      const textLeaves = collectTextLeaves([anchor]);
      if (textLeaves.length) roles.push("text-host");
      if (isTextLeaf(anchor)) roles.push("text-leaf");
      if (!roles.length && layerList.length) roles.push("box");
      return uniqueValues2(roles);
    }
    function collectTextLeaves(rootElements) {
      const leaves = [];
      rootElements.filter(Boolean).forEach((root) => {
        collectTextLeavesInto(root, leaves, root);
      });
      return uniqueElements2(leaves);
    }
    function collectTextLeavesInto(root, leaves, slotRoot) {
      if (!root || !isVisible(root)) return;
      if (root !== slotRoot && isIndependentSlotBoundary(root, slotRoot)) return;
      if (isTextLeaf(root) || isInlineTextHost(root)) {
        leaves.push(root);
        return;
      }
      [...root.children || []].forEach((child) => collectTextLeavesInto(child, leaves, slotRoot));
    }
    function isIndependentSlotBoundary(element, slotRoot) {
      if (isControlElement(element) || isMediaElement(element)) return true;
      const hasOwnSurface = hasBackground(element) || hasBorder(element) || hasShadow(element);
      return hasOwnSurface && !isConfirmedCompositeLayerRelation(slotRoot, element);
    }
    function resolveStyleRoute(prop, visualSelection) {
      var _a3;
      const visual = visualSelection || state.visualSelection;
      if (!visual || !visual.anchor) return routeResult(prop, [], "none", false, "没有选区。");
      if (isTextStyleProp(prop)) {
        const resolution2 = propertyTargetsForVisual(visual, prop);
        if (!resolution2.targets.length) {
          const leaves = visibleElements2(((_a3 = visual.textLeaves) == null ? void 0 : _a3.length) ? visual.textLeaves : [visual.anchor].filter(isTextLeaf));
          return routeResult(
            prop,
            [],
            leaves.length ? "text-leaves-mixed" : "text-leaves",
            false,
            leaves.length ? "文字样式不一致，请点选具体文字。" : "当前选区没有可见文字。"
          );
        }
        return routeResult(prop, resolution2.targets, resolution2.kind, true);
      }
      if (prop === "textContent") {
        const textTargets = isTextLeaf(visual.anchor) ? [visual.anchor] : visual.textLeaves;
        return routeResult(prop, textTargets.length === 1 ? textTargets : [], "text-leaf", textTargets.length === 1, "该选区包含多段文字。");
      }
      const resolution = propertyTargetsForVisual(visual, prop);
      if (prop === "padding" || prop === "paddingX" || prop === "paddingY" || isPaddingSideProp(prop)) {
        const cell = closestCell(visual.anchor);
        const reason = resolution.reason || (cell ? "表格 padding 只能在当前行编辑上下、当前列编辑左右，或在整表范围编辑四个方向。" : "当前选区不适合编辑留白。");
        return routeResult(prop, resolution.targets, resolution.kind, resolution.targets.length > 0, reason);
      }
      return routeResult(
        prop,
        resolution.targets,
        resolution.kind,
        resolution.targets.length > 0,
        resolution.reason || "当前选区没有可写入目标。"
      );
    }
    function routeResult(prop, targets2, route, visible, reason = "") {
      return { prop, targets: uniqueElements2(targets2.filter(Boolean)), route, visible, reason };
    }
    function isTextStyleProp(prop) {
      return prop === "color" || prop === "fontSize" || prop === "fontFamily" || prop === "fontWeight" || prop === "lineHeight" || prop === "letterSpacing";
    }
    const GroupEngine = {
      findGroup(visualSelection, options2 = {}) {
        const ladder = this.findScopeLadder(visualSelection, options2);
        return ladder[defaultScopeIndex(ladder)] || this.single(visualSelection, "empty-group");
      },
      findScopeLadder(visualSelection, options2 = {}) {
        const anchor = visualSelection == null ? void 0 : visualSelection.anchor;
        if (!anchor || !isVisible(anchor)) return [this.single(visualSelection, "missing-anchor")];
        const maxMembers = options2.maxMembers || 80;
        const baseFp = this.buildFingerprint(anchor, visualSelection);
        const candidates = this.collectCandidates(visualSelection, { maxMembers });
        const attempts = [
          this.findSiblingRepeatGroup(anchor, candidates, baseFp),
          ...this.findCousinSlotGroups(anchor, baseFp),
          ...this.findPatternAreaGroups(anchor, baseFp),
          ...this.findCrossRegionGroups(anchor, baseFp)
        ].filter(Boolean);
        const groups = attempts.map((group) => {
          group.members = uniqueElements2(group.members).filter(isVisible).slice(0, maxMembers);
          group.rejected = group.rejected || [];
          return group;
        }).filter((group) => group.members.length >= 2 && group.confidence >= 0.58);
        groups.forEach((group) => this.attachScopeAndDiff(group, baseFp));
        return this.orderScopeGroups([this.single(visualSelection, "current"), ...groups]);
      },
      single(visualSelection, reason = "fallback-single") {
        const anchor = (visualSelection == null ? void 0 : visualSelection.anchor) || null;
        return {
          anchor,
          members: anchor ? [anchor] : [],
          mode: "fallback-single",
          confidence: anchor ? 0.4 : 0,
          evidence: { reason },
          rejected: []
        };
      },
      buildFingerprint(element, visualSelection) {
        const visual = visualSelection && visualSelection.anchor === element ? visualSelection : resolveVisualSelectionFromAnchor(element);
        const cs = win().getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        const textLeaves = collectTextLeaves([element]);
        return {
          tag: element.tagName.toLowerCase(),
          roles: visual.roles || [],
          tokens: {
            classes: stableClasses(element),
            attrs: stableAttrs(element)
          },
          visual: {
            hasBackground: hasBackground(element),
            hasBorder: hasBorder(element),
            hasRadius: hasRadius(element),
            hasShadow: hasShadow(element),
            display: cs.display,
            position: cs.position,
            fontSize: Math.round(parseFloat(cs.fontSize) || 0)
          },
          rect: {
            width: rect.width,
            height: rect.height,
            widthBucket: sizeBucket(rect.width),
            heightBucket: sizeBucket(rect.height),
            aspectBucket: aspectBucket(rect)
          },
          structure: {
            childCountBucket: childCountBucket(element),
            directChildTags: [...element.children].filter(isVisible).slice(0, 8).map((child) => child.tagName.toLowerCase()),
            textLeafCount: textLeaves.length,
            textTagPath: textLeaves.slice(0, 8).map((leaf) => leaf.tagName.toLowerCase())
          }
        };
      },
      collectCandidates(visualSelection, options2 = {}) {
        const anchor = visualSelection.anchor;
        const maxMembers = options2.maxMembers || 80;
        const near = anchor.parentElement ? [...anchor.parentElement.children].filter((el) => el.nodeType === 1 && isVisible(el)) : [];
        const root = nearestGroupRoot(anchor);
        const global = [...root.querySelectorAll(anchor.tagName.toLowerCase())].filter((el) => el !== anchor && isVisible(el) && !isPageLike(el)).slice(0, Math.max(maxMembers * 4, 160));
        return uniqueElements2([anchor, ...near, ...global]).filter((el) => !isPageLike(el));
      },
      findSiblingRepeatGroup(anchor, candidates, baseFp) {
        const tableRow = this.findTableRowGroup(anchor, baseFp);
        if (tableRow) return tableRow;
        const parent = anchor.parentElement;
        if (!parent) return null;
        const siblings = candidates.filter((el) => el.parentElement === parent);
        const scored = siblings.map((el) => ({
          el,
          score: this.scoreCandidate(baseFp, this.buildFingerprint(el))
        })).filter((item) => {
          if (isTextLeaf(anchor)) return sameIdentityFamily(anchor, item.el, item.score);
          return item.score >= 0.64 || sameIdentityFamily(anchor, item.el, item.score);
        });
        const members = scored.map((item) => item.el);
        if (members.length < 2) return null;
        return {
          anchor,
          members,
          mode: "sibling-repeat",
          confidence: Math.min(0.94, 0.68 + members.length * 0.035),
          evidence: {
            sameParent: true,
            tagMatchRatio: ratioOf(scored, (item) => item.el.tagName === anchor.tagName),
            rectSimilarity: average(scored.map((item) => item.score)),
            structureSimilarity: average(scored.map((item) => item.score))
          },
          rejected: candidates.filter((el) => el.parentElement === parent && !members.includes(el)).slice(0, 12).map((el) => ({ selector: cssPath(el), reason: "low-sibling-score" }))
        };
      },
      findCousinSlotGroups(anchor, baseFp) {
        const tableSlot = this.findTableSlotGroup(anchor, baseFp);
        if (tableSlot) return [tableSlot];
        const stablePartSlot = this.findStablePartSlotGroup(anchor, baseFp);
        return stablePartSlot ? [stablePartSlot] : [];
      },
      findTableRowGroup(anchor, baseFp) {
        const cell = closestCell(anchor);
        if (!cell) return null;
        const row = cell.parentElement;
        const cells = tableCellChildren(row).map((el) => anchor === cell ? el : findEquivalentInsideCell(cell, anchor, el)).filter((el) => el && isVisible(el));
        const scored = cells.map((el) => ({ el, score: this.scoreCandidate(baseFp, this.buildFingerprint(el)) })).filter((item) => item.el === anchor || item.el === cell || item.score >= 0.45);
        const members = uniqueElements2(scored.map((item) => item.el));
        if (members.length < 2) return null;
        return {
          anchor,
          members,
          mode: "sibling-repeat",
          confidence: Math.min(0.94, 0.7 + members.length * 0.025),
          evidence: { slotKind: "table-row", rectSimilarity: average(scored.map((item) => item.score)) },
          rejected: []
        };
      },
      findTableSlotGroup(anchor, baseFp) {
        const cell = closestCell(anchor);
        if (!cell) return null;
        const row = cell.parentElement;
        const table = cell.closest("table");
        if (!row || !table) return null;
        const cells = tableCellChildren(row);
        const index = cells.indexOf(cell);
        if (index < 0) return null;
        const scored = [...table.querySelectorAll("tr")].map((tr) => tableCellChildren(tr)[index]).filter((el) => el && isVisible(el)).map((el) => ({ el: anchor === cell ? el : findEquivalentInsideCell(cell, anchor, el), score: 0 })).filter((item) => item.el && isVisible(item.el)).map((item) => ({ el: item.el, score: this.scoreCandidate(baseFp, this.buildFingerprint(item.el)) })).filter((item) => item.score >= 0.5 || item.el === anchor || item.el === cell);
        const members = uniqueElements2(scored.map((item) => item.el));
        if (members.length < 2) return null;
        return {
          anchor,
          members,
          mode: "cousin-slot",
          confidence: Math.min(0.92, 0.68 + members.length * 0.025 + average(scored.map((item) => item.score)) * 0.16),
          evidence: {
            slotKind: "table-column",
            columnIndex: index,
            rectSimilarity: average(scored.map((item) => item.score))
          },
          rejected: []
        };
      },
      findTableAreaGroup(anchor, baseFp) {
        const cell = closestCell(anchor);
        const table = cell == null ? void 0 : cell.closest("table");
        if (!cell || !table) return null;
        const tag = cell.tagName.toLowerCase();
        const cells = [...table.querySelectorAll(tag)].map((el) => anchor === cell ? el : findEquivalentInsideCell(cell, anchor, el)).filter((el) => el && isVisible(el));
        const scored = cells.map((el) => ({ el, score: this.scoreCandidate(baseFp, this.buildFingerprint(el)) })).filter((item) => item.el === anchor || item.el === cell || item.score >= 0.45);
        const members = uniqueElements2(scored.map((item) => item.el));
        if (members.length < 2) return null;
        return {
          anchor,
          members,
          mode: "pattern-area",
          confidence: Math.min(0.88, 0.58 + members.length * 8e-3 + average(scored.map((item) => item.score)) * 0.16),
          evidence: { slotKind: "table-area", rectSimilarity: average(scored.map((item) => item.score)) },
          rejected: []
        };
      },
      findCrossTableGroup(anchor, baseFp) {
        const cell = closestCell(anchor);
        const table = cell == null ? void 0 : cell.closest("table");
        if (!cell || !table) return null;
        const tag = cell.tagName.toLowerCase();
        const tables = similarPatternAreas(table, this);
        if (tables.length < 2) return null;
        const cells = uniqueElements2(tables.flatMap((root) => [...root.querySelectorAll(tag)])).map((el) => anchor === cell ? el : findEquivalentInsideCell(cell, anchor, el)).filter((el) => el && isVisible(el));
        const scored = cells.map((el) => ({ el, score: this.scoreCandidate(baseFp, this.buildFingerprint(el)) })).filter((item) => item.el === anchor || item.el === cell || item.score >= 0.45);
        const members = uniqueElements2(scored.map((item) => item.el));
        if (members.length < 2) return null;
        return {
          anchor,
          members,
          mode: "cross-region",
          confidence: Math.min(0.8, 0.5 + tables.length * 0.025 + members.length * 4e-3 + average(scored.map((item) => item.score)) * 0.14),
          evidence: { slotKind: "cross-table-area", tableCount: tables.length, rectSimilarity: average(scored.map((item) => item.score)) },
          rejected: []
        };
      },
      findStablePartSlotGroup(anchor, baseFp) {
        const groups = [];
        forEachSelectionContainer(anchor, (container, depth) => {
          const relatives = relatedRepeatContainers(container, this);
          if (relatives.length < 2) return;
          if (!hasStablePartIdentity(anchor)) return;
          const scored = relatives.map((root) => findStablePartInHost(root, anchor)).filter((el) => el && isVisible(el)).map((el) => ({ el, score: this.scoreCandidate(baseFp, this.buildFingerprint(el)) })).filter((item) => sameIdentityFamily(anchor, item.el, item.score) || item.score >= 0.72);
          const members = uniqueElements2(scored.map((item) => item.el));
          if (members.length < 2 || members.length !== relatives.length) return;
          groups.push({
            anchor,
            members,
            mode: "cousin-slot",
            confidence: Math.min(0.9, 0.62 + members.length * 0.025 + average(scored.map((item) => item.score)) * 0.18),
            evidence: {
              slotKind: "stable-part",
              repeatContainer: selectorToken(container),
              containerCount: relatives.length,
              depth,
              rectSimilarity: average(scored.map((item) => item.score))
            },
            rejected: []
          });
        });
        return groups.sort((a, b) => (a.evidence.depth || 0) - (b.evidence.depth || 0))[0] || null;
      },
      findPatternAreaGroups(anchor, baseFp) {
        const tableArea = this.findTableAreaGroup(anchor, baseFp);
        if (tableArea) return [tableArea];
        const groups = [];
        const tag = anchor.tagName.toLowerCase();
        forEachSelectionContainer(anchor, (container) => {
          const relatives = relatedRepeatContainers(container, this);
          if (relatives.length < 2) return;
          const pool = uniqueElements2(relatives.flatMap((root) => {
            var _a3;
            return [
              ((_a3 = root.matches) == null ? void 0 : _a3.call(root, tag)) ? root : null,
              ...root.querySelectorAll(tag)
            ].filter(Boolean);
          }));
          const scored = pool.filter((el) => isVisible(el) && !isPageLike(el)).map((el) => ({ el, score: this.scoreCandidate(baseFp, this.buildFingerprint(el)) })).filter((item) => {
            if (isTextLeaf(anchor)) return sameIdentityFamily(anchor, item.el, item.score);
            return item.score >= 0.72 || sameIdentityFamily(anchor, item.el, item.score);
          });
          const members = uniqueElements2(scored.map((item) => item.el));
          if (members.length < 2) return;
          groups.push({
            anchor,
            members,
            mode: "pattern-area",
            confidence: Math.min(0.84, 0.56 + members.length * 0.012 + average(scored.map((item) => item.score)) * 0.2),
            evidence: {
              repeatContainer: selectorToken(container),
              containerCount: relatives.length,
              rectSimilarity: average(scored.map((item) => item.score))
            },
            rejected: []
          });
        });
        return groups;
      },
      findCrossRegionGroups(anchor, baseFp) {
        const crossTable = this.findCrossTableGroup(anchor, baseFp);
        if (crossTable) return [crossTable];
        const groups = [];
        const tag = anchor.tagName.toLowerCase();
        forEachSelectionContainer(anchor, (container) => {
          const area = nearestPatternArea(anchor, container, this);
          if (!area || area === doc().body || isPageLike(area)) return;
          const areas = similarPatternAreas(area, this);
          if (areas.length < 2) return;
          const pool = uniqueElements2(areas.flatMap((root) => {
            var _a3;
            return [
              ((_a3 = root.matches) == null ? void 0 : _a3.call(root, tag)) ? root : null,
              ...root.querySelectorAll(tag)
            ].filter(Boolean);
          }));
          const scored = pool.filter((el) => isVisible(el) && !isPageLike(el)).map((el) => ({ el, score: this.scoreCandidate(baseFp, this.buildFingerprint(el)) })).filter((item) => {
            if (isTextLeaf(anchor)) return sameIdentityFamily(anchor, item.el, item.score);
            return item.score >= 0.72 || sameIdentityFamily(anchor, item.el, item.score);
          });
          const members = uniqueElements2(scored.map((item) => item.el));
          if (members.length < 2) return;
          groups.push({
            anchor,
            members,
            mode: "cross-region",
            confidence: Math.min(0.8, 0.52 + areas.length * 0.025 + members.length * 6e-3 + average(scored.map((item) => item.score)) * 0.18),
            evidence: {
              area: selectorToken(area),
              areaCount: areas.length,
              rectSimilarity: average(scored.map((item) => item.score))
            },
            rejected: []
          });
        });
        return groups;
      },
      findRepeatedClassGroup(anchor, candidates, baseFp) {
        const cls = bestIdentityClass(anchor, candidates);
        if (!cls) return null;
        const scored = candidates.filter((el) => el.classList.contains(cls)).map((el) => ({ el, score: this.scoreCandidate(baseFp, this.buildFingerprint(el)) })).filter((item) => item.score >= 0.56);
        const members = scored.map((item) => item.el);
        if (members.length < 2) return null;
        return {
          anchor,
          members,
          mode: "class-repeat",
          confidence: Math.min(0.88, 0.58 + members.length * 0.025 + siblingClassCount(anchor, cls) * 0.04),
          evidence: {
            repeatedClass: cls,
            sameParent: members.some((el) => el !== anchor && el.parentElement === anchor.parentElement),
            rectSimilarity: average(scored.map((item) => item.score)),
            tagMatchRatio: ratioOf(scored, (item) => item.el.tagName === anchor.tagName)
          },
          rejected: []
        };
      },
      findVisualFingerprintGroup(anchor, candidates, baseFp) {
        const scored = candidates.map((el) => ({
          el,
          score: this.scoreCandidate(baseFp, this.buildFingerprint(el))
        })).filter((item) => item.score >= 0.7);
        const members = scored.map((item) => item.el);
        if (members.length < 2) return null;
        return {
          anchor,
          members,
          mode: "visual-fingerprint",
          confidence: Math.min(0.78, 0.52 + members.length * 0.02),
          evidence: {
            rectSimilarity: average(scored.map((item) => item.score)),
            structureSimilarity: average(scored.map((item) => item.score)),
            roleSimilarity: ratioOf(scored, (item) => rolesOverlap(baseFp.roles, this.buildFingerprint(item.el).roles) > 0)
          },
          rejected: []
        };
      },
      scoreCandidate(baseFp, candidateFp) {
        let score = 0;
        if (baseFp.tag === candidateFp.tag) score += 0.18;
        const roleOverlap = rolesOverlap(baseFp.roles, candidateFp.roles);
        score += Math.min(0.18, roleOverlap * 0.09);
        score += classOverlapScore(baseFp.tokens.classes, candidateFp.tokens.classes) * 0.2;
        score += rectSimilarityScore(baseFp.rect, candidateFp.rect) * 0.2;
        score += structureSimilarityScore(baseFp.structure, candidateFp.structure) * 0.14;
        score += visualSimilarityScore(baseFp.visual, candidateFp.visual) * 0.1;
        return Math.max(0, Math.min(1, score));
      },
      attachScopeAndDiff(result, baseFp) {
        result.identityScope = {
          className: "",
          members: result.members,
          confidence: result.confidence,
          sharedClasses: sharedGroupClasses(result.members),
          sharedAttrs: sharedGroupAttrs(result.members)
        };
        result.selectedDiffSelector = selectedDiffSelector(result.anchor, result.members, baseFp);
      },
      orderScopeGroups(groups) {
        const seen = /* @__PURE__ */ new Set();
        const seenModes = /* @__PURE__ */ new Set();
        return groups.filter((group) => {
          var _a3;
          return (_a3 = group == null ? void 0 : group.members) == null ? void 0 : _a3.length;
        }).map((group) => {
          group.members = uniqueElements2(group.members).filter(Boolean);
          return group;
        }).filter((group) => {
          const key = group.members.map((el) => visualIdFor(el)).sort().join("|");
          if (seen.has(key)) return false;
          seen.add(key);
          return true;
        }).filter((group) => {
          const mode = group.mode || "unknown";
          if (seenModes.has(mode)) return false;
          seenModes.add(mode);
          return true;
        }).sort((a, b) => {
          const rankA = scopeRank(a);
          const rankB = scopeRank(b);
          if (rankA !== rankB) return rankA - rankB;
          if (a.members.length !== b.members.length) return a.members.length - b.members.length;
          return (b.confidence || 0) - (a.confidence || 0);
        });
      },
      explain(result) {
        if (!result) return "";
        return `${result.mode} / ${Math.round((result.confidence || 0) * 100)}%`;
      }
    };
    function sharedGroupClasses(members) {
      if (!(members == null ? void 0 : members.length)) return [];
      const lists = members.map(stableClasses);
      return lists[0].filter((cls) => lists.every((list) => list.includes(cls)));
    }
    function sharedGroupAttrs(members) {
      if (!(members == null ? void 0 : members.length)) return {};
      const first = stableAttrs(members[0]);
      const shared = {};
      Object.entries(first).forEach(([name, value]) => {
        if (members.every((el) => stableAttrs(el)[name] === value)) shared[name] = value;
      });
      return shared;
    }
    function selectedDiffSelector(anchor, members, baseFp) {
      if (!anchor || !(members == null ? void 0 : members.length)) return null;
      new Set(members);
      const others = members.filter((el) => el !== anchor);
      if (!others.length) return null;
      const anchorClasses = stableClasses(anchor);
      const classCandidates = anchorClasses.filter((cls) => isLikelyStateClass(cls) && !others.every((el) => el.classList.contains(cls))).map((cls) => {
        const count = members.filter((el) => el.classList.contains(cls)).length;
        const selector = `.${CSS.escape(cls)}`;
        return {
          selector,
          token: cls,
          source: "class-diff",
          semantic: false,
          confidence: diffTokenConfidence({ count, total: members.length, token: cls, source: "class-diff" })
        };
      });
      const absentClassCandidates = uniqueValues2(members.flatMap((el) => stableClasses(el))).filter((cls) => isLikelyStateClass(cls) && !anchorClasses.includes(cls) && members.some((el) => el.classList.contains(cls))).map((cls) => {
        const count = members.filter((el) => !el.classList.contains(cls)).length;
        const selector = `:not(.${CSS.escape(cls)})`;
        return {
          selector,
          token: cls,
          source: "class-absence-diff",
          semantic: false,
          confidence: diffTokenConfidence({ count, total: members.length, token: cls, source: "class-diff" })
        };
      });
      const anchorAttrs = stableAttrs(anchor);
      const attrCandidates = Object.entries(anchorAttrs).filter(([name, value]) => others.some((el) => stableAttrs(el)[name] !== value)).map(([name, value]) => {
        const count = members.filter((el) => stableAttrs(el)[name] === value).length;
        return {
          selector: `[${CSS.escape(name)}="${cssStringEscape(value)}"]`,
          token: name,
          value,
          source: "attr-diff",
          semantic: false,
          confidence: diffTokenConfidence({ count, total: members.length, token: name, source: "attr-diff" })
        };
      });
      const candidates = [...attrCandidates, ...classCandidates, ...absentClassCandidates].filter((item) => item.confidence >= 0.62).sort((a, b) => b.confidence - a.confidence);
      const best = candidates[0] || null;
      if (!best) return null;
      best.baseline = {
        sharedClasses: sharedGroupClasses(members),
        selectedClasses: stableClasses(anchor),
        groupSize: members.length,
        selectedMatches: members.filter((el) => elementMatchesSelector2(el, best.selector)).length,
        tag: (baseFp == null ? void 0 : baseFp.tag) || anchor.tagName.toLowerCase()
      };
      return best;
    }
    function diffTokenConfidence({ count, total, token, source }) {
      if (!total || count <= 0 || count >= total) return 0;
      let score = source === "attr-diff" ? 0.78 : 0.72;
      const rarity = 1 - count / total;
      score += Math.min(0.16, rarity * 0.18);
      if (source === "class-diff" && isStableToken(token)) score += 0.06;
      if (/^(aria-|data-(state|selected|active|open|pressed|current|expanded)$)/i.test(token)) score += 0.08;
      return Math.max(0, Math.min(0.96, score));
    }
    function isLikelyStateClass(token) {
      return /(^|[-_:])(active|selected|current|open|expanded|collapsed|checked|pressed|focus|focused|hover|disabled|enabled|on|off)([-_:]|$)/i.test(String(token || ""));
    }
    function elementMatchesSelector2(el, selector) {
      try {
        return el.matches(selector);
      } catch {
        return false;
      }
    }
    function cssStringEscape(value) {
      return String(value).replaceAll("\\", "\\\\").replaceAll('"', '\\"');
    }
    function stableClasses(el) {
      return [...el.classList].filter((c) => !c.startsWith("dt-") && isStableToken(c));
    }
    function stableAttrs(el) {
      const attrs = {};
      [...el.attributes || []].forEach((attr) => {
        const name = attr.name;
        const value = attr.value;
        if (name === "class" || name === "style" || name === "id") return;
        if (/^(aria-|role$)/.test(name)) attrs[name] = value;
        else if (/^data-(state|selected|active|open|pressed|current|expanded)$/i.test(name)) attrs[name] = value;
      });
      return attrs;
    }
    function isStableToken(token) {
      const value = String(token || "");
      if (!value || value.length > 42) return false;
      if (/^(dt-|enter|leave|leaving|entered|exiting|animating|animation|transition|motion|temp|tmp)/i.test(value)) return false;
      if (/^[a-f0-9]{6,}$/i.test(value)) return false;
      if (/[a-z]+-\d{5,}$/i.test(value)) return false;
      return true;
    }
    function visualIdFor(el) {
      if (!el) return "";
      if (!visualIds.has(el)) visualIds.set(el, `v${++visualIdSeq}`);
      return visualIds.get(el);
    }
    function rectArea$1(rect) {
      return rectArea(rect);
    }
    function rectOverlapRatio$1(a, b) {
      return rectOverlapRatio(a, b);
    }
    function ancestorDistance(from, to) {
      let node = from;
      let distance = 0;
      while (node && node !== to && distance < 20) {
        node = node.parentElement;
        distance += 1;
      }
      return node === to ? distance : 20;
    }
    function sizeBucket(value) {
      const n = Math.max(0, Number(value) || 0);
      if (n < 24) return 1;
      if (n < 48) return 2;
      if (n < 96) return 3;
      if (n < 180) return 4;
      if (n < 360) return 5;
      if (n < 720) return 6;
      return 7;
    }
    function aspectBucket(rect) {
      const ratio = (rect.width || 1) / Math.max(rect.height || 1, 1);
      if (ratio < 0.55) return "tall";
      if (ratio < 0.85) return "portrait";
      if (ratio < 1.25) return "square";
      if (ratio < 2.2) return "wide";
      return "banner";
    }
    function childCountBucket(el) {
      const count = [...el.children || []].filter(isVisible).length;
      if (count === 0) return 0;
      if (count === 1) return 1;
      if (count <= 3) return 2;
      if (count <= 6) return 3;
      return 4;
    }
    function nearestGroupRoot(anchor) {
      let node = anchor == null ? void 0 : anchor.parentElement;
      let root = doc().body;
      let depth = 0;
      while (node && node !== doc().body && node !== doc().documentElement && depth < 4) {
        if (isPageLike(node)) break;
        root = node;
        const visibleChildren = [...node.children].filter(isVisible).length;
        if (visibleChildren >= 2) break;
        node = node.parentElement;
        depth += 1;
      }
      return root || doc().body;
    }
    function forEachSelectionContainer(anchor, callback) {
      let node = anchor == null ? void 0 : anchor.parentElement;
      let depth = 0;
      while (node && node !== doc().body && node !== doc().documentElement && depth < 6) {
        if (!isVisible(node) || isPageLike(node)) break;
        callback(node, depth);
        node = node.parentElement;
        depth += 1;
      }
    }
    function relatedRepeatContainers(container, engine) {
      const parent = container == null ? void 0 : container.parentElement;
      if (!parent) return [container].filter(Boolean);
      const base = engine.buildFingerprint(container);
      const siblings = [...parent.children].filter((el) => el.nodeType === 1 && isVisible(el) && !isPageLike(el));
      const primaryClasses = stableClasses(container);
      const scored = siblings.filter((el) => el.tagName === container.tagName).map((el) => ({
        el,
        score: engine.scoreCandidate(base, engine.buildFingerprint(el))
      })).filter((item) => {
        if (item.el === container) return true;
        const sharesClass = primaryClasses.length && primaryClasses.some((cls) => item.el.classList.contains(cls));
        return item.score >= (sharesClass ? 0.5 : 0.62);
      }).sort((a, b) => b.score - a.score);
      return uniqueElements2(scored.map((item) => item.el));
    }
    function nearestPatternArea(anchor, start, engine) {
      var _a3, _b2;
      const tag = (_a3 = anchor == null ? void 0 : anchor.tagName) == null ? void 0 : _a3.toLowerCase();
      let node = start;
      let best = null;
      let depth = 0;
      while (node && node !== doc().body && node !== doc().documentElement && depth < 7) {
        if (!isVisible(node) || isPageLike(node)) break;
        const sameTagCount = tag ? [...node.querySelectorAll(tag)].filter(isVisible).length + (((_b2 = node.matches) == null ? void 0 : _b2.call(node, tag)) ? 1 : 0) : 0;
        const repeatedChildren = relatedRepeatContainers(node, engine).length;
        if (sameTagCount >= 3 || repeatedChildren >= 2 || isPatternAreaElement(node)) best = node;
        node = node.parentElement;
        depth += 1;
      }
      return best || start;
    }
    function similarPatternAreas(area, engine) {
      if (!area || !area.tagName) return [];
      const tag = area.tagName.toLowerCase();
      const baseFp = engine.buildFingerprint(area);
      const root = boundedAreaSearchRoot(area);
      const candidates = [area, ...root.querySelectorAll(tag)].filter((el) => el && el !== doc().body && el !== doc().documentElement && isVisible(el) && !isPageLike(el));
      const primaryClasses = stableClasses(area);
      const scored = uniqueElements2(candidates).map((el) => ({
        el,
        score: engine.scoreCandidate(baseFp, engine.buildFingerprint(el))
      })).filter((item) => {
        if (item.el === area) return true;
        const sharesClass = primaryClasses.length && primaryClasses.some((cls) => item.el.classList.contains(cls));
        if (!isStructuralPatternArea(area) && !sharesClass) return false;
        return item.score >= (sharesClass ? 0.52 : 0.64);
      });
      return uniqueElements2(scored.map((item) => item.el));
    }
    function boundedAreaSearchRoot(area) {
      let node = area.parentElement;
      let root = area.parentElement || doc().body;
      let depth = 0;
      while (node && node !== doc().body && node !== doc().documentElement && depth < 5) {
        if (isPageLike(node)) break;
        root = node;
        node = node.parentElement;
        depth += 1;
      }
      return root || doc().body;
    }
    function isPatternAreaElement(el) {
      if (!el || !el.tagName) return false;
      el.tagName.toLowerCase();
      if (isStructuralPatternArea(el)) return true;
      const cs = win().getComputedStyle(el);
      return (cs.display === "grid" || cs.display === "flex") && [...el.children].filter(isVisible).length >= 3;
    }
    function isStructuralPatternArea(el) {
      var _a3, _b2;
      return ["table", "tbody", "thead", "ul", "ol"].includes((_b2 = (_a3 = el == null ? void 0 : el.tagName) == null ? void 0 : _a3.toLowerCase) == null ? void 0 : _b2.call(_a3));
    }
    function closestCell(anchor) {
      var _a3;
      return ((_a3 = anchor == null ? void 0 : anchor.closest) == null ? void 0 : _a3.call(anchor, "td,th")) || null;
    }
    function tableCellChildren(row) {
      return [...(row == null ? void 0 : row.children) || []].filter((el) => /^(td|th)$/i.test(el.tagName));
    }
    function findEquivalentInsideCell(sourceCell, source, targetCell) {
      if (!sourceCell || !source || !targetCell) return null;
      if (source === sourceCell) return targetCell;
      if (hasStablePartIdentity(source)) return findStablePartInHost(targetCell, source);
      if (isTextLeaf(source) || isInlineTextHost(source) || hasVisibleText(source)) return targetCell;
      return null;
    }
    function hasStablePartIdentity(anchor) {
      if (!anchor) return false;
      if (isMediaElement(anchor) || isControlElement(anchor)) return true;
      return stableClasses(anchor).filter((cls) => !isLikelyStateClass(cls)).length > 0;
    }
    function findStablePartInHost(host, source) {
      var _a3, _b2;
      if (!host || !source) return null;
      const classes = stableClasses(source).filter((cls) => !isLikelyStateClass(cls));
      if (classes.length) {
        const selector = classes.map((cls) => `.${CSS.escape(cls)}`).join("");
        const matches = [((_a3 = host.matches) == null ? void 0 : _a3.call(host, selector)) ? host : null, ...host.querySelectorAll(selector)].filter(Boolean).filter(isVisible);
        if (matches.length === 1) return matches[0];
      }
      if (isMediaElement(source) || isControlElement(source)) {
        const tag = source.tagName.toLowerCase();
        const matches = [((_b2 = host.matches) == null ? void 0 : _b2.call(host, tag)) ? host : null, ...host.querySelectorAll(tag)].filter(Boolean).filter(isVisible);
        if (matches.length === 1) return matches[0];
      }
      return null;
    }
    function selectorToken(el) {
      if (!el) return "";
      const classes = stableClasses(el).slice(0, 2);
      return el.tagName.toLowerCase() + (classes.length ? "." + classes.join(".") : "");
    }
    function scopeRank(group) {
      const ranks = {
        "fallback-single": 0,
        "sibling-repeat": 1,
        "cousin-slot": 2,
        "pattern-area": 3,
        "cross-region": 4
      };
      return ranks[group == null ? void 0 : group.mode] ?? 9;
    }
    function bestIdentityClass(anchor, candidates) {
      const classes = stableClasses(anchor);
      let best = null;
      let bestScore = 0;
      classes.forEach((cls) => {
        const total = candidates.filter((el) => el.classList.contains(cls)).length;
        const siblings = siblingClassCount(anchor, cls);
        const selectedOnly = total <= 1;
        if (selectedOnly) return;
        const score = siblings * 8 + Math.min(total, 16);
        if (score > bestScore) {
          best = cls;
          bestScore = score;
        }
      });
      return best;
    }
    function sameIdentityFamily(anchor, candidate, score) {
      if (!anchor || !candidate || anchor.tagName !== candidate.tagName || score < 0.42) return false;
      const a = stableClasses(anchor).filter((cls) => !isLikelyStateClass(cls));
      const b = stableClasses(candidate).filter((cls) => !isLikelyStateClass(cls));
      if (!a.length || !b.length) return false;
      return a.some((cls) => b.includes(cls));
    }
    function siblingClassCount(anchor, cls) {
      const parent = anchor.parentElement;
      if (!parent) return 0;
      return [...parent.children].filter((el) => el.nodeType === 1 && isVisible(el) && el.classList.contains(cls)).length;
    }
    function average(values) {
      const list = values.filter((value) => Number.isFinite(value));
      return list.length ? list.reduce((sum, value) => sum + value, 0) / list.length : 0;
    }
    function ratioOf(list, predicate) {
      return list.length ? list.filter(predicate).length / list.length : 0;
    }
    function rolesOverlap(a, b) {
      const set = new Set(a || []);
      return (b || []).filter((role) => set.has(role)).length;
    }
    function classOverlapScore(a, b) {
      if (!a.length && !b.length) return 0.5;
      const set = new Set(a);
      const overlap = b.filter((cls) => set.has(cls)).length;
      return overlap / Math.max(1, Math.max(a.length, b.length));
    }
    function rectSimilarityScore(a, b) {
      const width = nearSize(a.width, b.width, 0.4) ? 0.42 : Math.max(0, 0.42 - Math.abs(a.widthBucket - b.widthBucket) * 0.12);
      const height = nearSize(a.height, b.height, 0.4) ? 0.42 : Math.max(0, 0.42 - Math.abs(a.heightBucket - b.heightBucket) * 0.12);
      const aspect = a.aspectBucket === b.aspectBucket ? 0.16 : 0;
      return Math.max(0, Math.min(1, width + height + aspect));
    }
    function structureSimilarityScore(a, b) {
      let score = 0;
      if (a.childCountBucket === b.childCountBucket) score += 0.32;
      if (a.textLeafCount === b.textLeafCount) score += 0.28;
      score += tagListSimilarity(a.directChildTags, b.directChildTags) * 0.22;
      score += tagListSimilarity(a.textTagPath, b.textTagPath) * 0.18;
      return Math.max(0, Math.min(1, score));
    }
    function tagListSimilarity(a, b) {
      if (!a.length && !b.length) return 1;
      const length = Math.max(a.length, b.length, 1);
      let same = 0;
      for (let i2 = 0; i2 < Math.min(a.length, b.length); i2 += 1) {
        if (a[i2] === b[i2]) same += 1;
      }
      return same / length;
    }
    function visualSimilarityScore(a, b) {
      const keys = ["hasBackground", "hasBorder", "hasRadius", "hasShadow", "display", "position"];
      const same = keys.filter((key) => a[key] === b[key]).length;
      const font = Math.abs((a.fontSize || 0) - (b.fontSize || 0)) <= 2 ? 1 : 0;
      return (same + font) / (keys.length + 1);
    }
    function nearSize(a, b, tolerance) {
      const max2 = Math.max(Math.abs(a), Math.abs(b), 1);
      return Math.abs(a - b) / max2 <= tolerance;
    }
    function uniqueElements2(list) {
      return [...new Set(list)];
    }
    function uniqueElementsBy(list, keyFn) {
      const seen = /* @__PURE__ */ new Set();
      return list.filter((item) => {
        const key = keyFn(item);
        if (!key || seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    }
    function uniqueValues2(list) {
      return [...new Set(list.filter(Boolean))];
    }
    function copyColorControlValue(id) {
      const input = $("#" + id);
      if (!input) return;
      const value = input.dataset.styleDefaultValue || input.value.replace(/\s*\(默认\)\s*$/, "").trim();
      if (!value) {
        toast("当前没有可复制的颜色值。");
        return;
      }
      copyText(value);
    }
    function setColorControlValue(id, value) {
      const input = $("#" + id);
      if (!input) return;
      if (isActiveInputControl(input)) {
        updateSwatch(id, value || input.dataset.styleDefaultValue || input.value || "");
        return;
      }
      const actual = value || "";
      if (actual) {
        input.value = `${actual} (默认)`;
        input.dataset.styleDefaultValue = actual;
        input.classList.add("dt-default-value");
      } else {
        input.value = "";
        delete input.dataset.styleDefaultValue;
        input.classList.remove("dt-default-value");
      }
      updateSwatch(id, actual);
    }
    function setRangeControlValue(id, value, unitValue) {
      const range = $("#" + id + "-range");
      const input = $("#" + id);
      const unit = $("#" + id + "-unit");
      if (!range || !input || !unit) return;
      const clamped = Math.max(Number(range.min || 0), Math.min(Number(range.max || value), Number(value) || 0));
      range.value = clamped;
      if (!isActiveInputControl(input)) input.value = clamped;
      unit.value = unitValue;
      updateRangeProgress(range);
    }
    function setFontSizeControlValue(id, px, unitValue) {
      const range = $("#" + id + "-range");
      const input = $("#" + id);
      const unit = $("#" + id + "-unit");
      if (!range || !input || !unit) return;
      const value = fontSizeFromPx(px, unitValue, input);
      const config = fontSizeRangeConfig(value, unitValue);
      range.min = config.min;
      range.max = config.max;
      range.step = config.step;
      input.min = config.min;
      input.max = config.max;
      input.step = config.step;
      setFontUnitButtonValue(id, unitValue);
      const formatted = formatFontSizeValue(value, unitValue);
      range.value = formatted;
      if (!isActiveInputControl(input)) input.value = formatted;
      input.dataset.currentPx = String(px);
      updateRangeProgress(range);
    }
    function setWidthControlValue(id, px, unitValue) {
      const range = $("#" + id + "-range");
      const input = $("#" + id);
      if (!input) return;
      const value = widthFromPx(px, unitValue, input);
      const config = widthRangeConfig(value, unitValue);
      if (range) {
        range.min = config.min;
        range.max = config.max;
        range.step = config.step;
      }
      input.min = config.min;
      input.max = config.max;
      input.step = config.step;
      setUnitButtonValue(id, unitValue, "widthUnit");
      const formatted = formatWidthValue(value, unitValue);
      if (range) range.value = formatted;
      if (!isActiveInputControl(input)) input.value = formatted;
      input.dataset.currentPx = String(px);
      if (range) updateRangeProgress(range);
    }
    function setFontUnitButtonValue(id, unitValue) {
      setUnitButtonValue(id, unitValue, "fontUnit");
    }
    function setUnitButtonValue(id, unitValue, dataName) {
      const button = $("#" + id + "-unit");
      const label = button == null ? void 0 : button.querySelector("span");
      if (!button || !label) return;
      const actual = unitValue || "px";
      button.dataset.value = actual;
      button.title = actual;
      label.textContent = actual;
      const menu = $("#" + id + "-unit-menu");
      menu == null ? void 0 : menu.querySelectorAll(".dt-unit-option").forEach((option) => {
        option.classList.toggle("dt-active", option.dataset[dataName] === actual);
      });
    }
    function fontSizeFromPx(px, unitValue, input) {
      const value = Number(px) || 0;
      if (unitValue === "rem") return value / fontMetric(input, "rootPx", 16);
      if (unitValue === "%") return value / fontMetric(input, "parentPx", value || 16) * 100;
      return value;
    }
    function fontSizeFromPxWithMetrics(px, unitValue, metrics) {
      const value = Number(px) || 0;
      if (unitValue === "rem") return value / (Number(metrics == null ? void 0 : metrics.rootPx) || 16);
      if (unitValue === "%") return value / (Number(metrics == null ? void 0 : metrics.parentPx) || value || 16) * 100;
      return value;
    }
    function fontSizeToPx(value, unitValue, input) {
      const n = Number(value) || 0;
      if (unitValue === "rem") return n * fontMetric(input, "rootPx", 16);
      if (unitValue === "%") return n / 100 * fontMetric(input, "parentPx", 16);
      return n;
    }
    function fontMetric(input, key, fallback) {
      var _a3;
      return Number((_a3 = input == null ? void 0 : input.dataset) == null ? void 0 : _a3[key]) || fallback;
    }
    function widthFromPx(px, unitValue, input) {
      const value = Number(px) || 0;
      if (unitValue === "rem") return value / fontMetric(input, "rootPx", 16);
      if (unitValue === "%") return value / fontMetric(input, "parentPx", value || 1) * 100;
      return value;
    }
    function widthFromPxWithMetrics(px, unitValue, metrics) {
      const value = Number(px) || 0;
      if (unitValue === "rem") return value / (Number(metrics == null ? void 0 : metrics.rootPx) || 16);
      if (unitValue === "%") return value / (Number(metrics == null ? void 0 : metrics.parentPx) || value || 1) * 100;
      return value;
    }
    function widthToPx(value, unitValue, input) {
      const n = Number(value) || 0;
      if (unitValue === "rem") return n * fontMetric(input, "rootPx", 16);
      if (unitValue === "%") return n / 100 * fontMetric(input, "parentPx", 1);
      return n;
    }
    function widthToPxWithMetrics(value, unitValue, metrics) {
      const n = Number(value) || 0;
      if (unitValue === "rem") return n * (Number(metrics == null ? void 0 : metrics.rootPx) || 16);
      if (unitValue === "%") return n / 100 * (Number(metrics == null ? void 0 : metrics.parentPx) || 1);
      return n;
    }
    function normalizeWidthInput(value, unitValue) {
      return formatWidthValue(Number(value) || 0, unitValue);
    }
    function formatWidthValue(value, unitValue) {
      if (unitValue === "rem") return String(Math.round((Number(value) || 0) * 1e3) / 1e3);
      if (unitValue === "%") return String(Math.round((Number(value) || 0) * 10) / 10);
      return String(Math.round(Number(value) || 0));
    }
    function widthRangeConfig(value, unitValue) {
      const n = Math.max(Number(value) || 0, unitValue === "%" ? 100 : 1);
      if (unitValue === "rem") {
        return {
          min: roundStep(Math.max(0.25, n * 0.4), 0.05),
          max: roundStep(Math.min(120, n * 2), 0.05),
          step: 0.05
        };
      }
      if (unitValue === "%") {
        return {
          min: roundStep(Math.max(5, n * 0.4), 0.5),
          max: roundStep(Math.min(300, n * 2), 0.5),
          step: 0.5
        };
      }
      return {
        min: Math.round(Math.max(0, n * 0.4)),
        max: Math.round(Math.min(2400, Math.max(n * 2, n + 80))),
        step: 1
      };
    }
    function fontSizeRangeConfig(value, unitValue) {
      const n = Math.max(Number(value) || 0, unitValue === "%" ? 100 : 1);
      if (unitValue === "rem") {
        return {
          min: roundStep(Math.max(0.375, n * 0.5), 0.05),
          max: roundStep(Math.min(10, n * 2), 0.05),
          step: 0.05
        };
      }
      if (unitValue === "%") {
        return {
          min: Math.round(Math.max(50, n * 0.5)),
          max: Math.round(Math.min(300, n * 2)),
          step: 1
        };
      }
      return {
        min: Math.round(Math.max(6, n * 0.5)),
        max: Math.round(Math.min(160, n * 2)),
        step: 1
      };
    }
    function normalizeFontSizeInput(value, unitValue) {
      return formatFontSizeValue(Number(value) || 0, unitValue);
    }
    function formatFontSizeValue(value, unitValue) {
      if (unitValue === "rem") return String(Math.round((Number(value) || 0) * 1e3) / 1e3);
      if (unitValue === "%") return String(Math.round(Number(value) || 0));
      return String(Math.round(Number(value) || 0));
    }
    function roundStep(value, step) {
      return Number((Math.round(value / step) * step).toFixed(4));
    }
    function updateSwatch(id, value) {
      const swatch = $("#" + id + "-swatch");
      if (!swatch) return;
      const normalized = normalizeStyleValue("color", value);
      swatch.style.setProperty("--swatch", normalized || "#fff");
    }
    function clearDefaultColorValue(input) {
      if (!input || !input.dataset || !input.dataset.styleDefaultValue) return;
      delete input.dataset.styleDefaultValue;
      input.classList.remove("dt-default-value");
      input.value = "";
    }
    function colorControlValue(input) {
      var _a3;
      if (!input) return "";
      return (((_a3 = input.dataset) == null ? void 0 : _a3.styleDefaultValue) || input.value.replace(/\s*\(默认\)\s*$/, "")).trim();
    }
    function sameColorValue(prop, left, right) {
      if (left === right) return true;
      if (!left || !right) return false;
      return normalizeStyleValue(prop, left) === normalizeStyleValue(prop, right);
    }
    function openColorPopover(id, prop, anchor) {
      const input = $("#" + id);
      const value = colorControlValue(input);
      const activeColor = { id, prop, ready: false };
      state.activeColor = activeColor;
      const displayValue = value && value !== "transparent" ? value : "#ffffff";
      ensureIroColorPicker(displayValue);
      syncColorSpecialButtons(value ? value === "transparent" ? "transparent" : "normal" : "empty");
      const popover = $("#dt-color-popover");
      if (!popover) return;
      popover.classList.add("dt-open");
      positionColorPopover(popover, anchor);
      requestAnimationFrame(() => {
        if (state.activeColor === activeColor) activeColor.ready = true;
      });
    }
    function closeColorPopover() {
      var _a3;
      (_a3 = $("#dt-color-popover")) == null ? void 0 : _a3.classList.remove("dt-open");
    }
    function resetColorPopover() {
      state.activeColor = null;
      state.iroPicker = null;
      closeColorPopover();
    }
    function positionColorPopover(popover, anchor) {
      if (!popover || !anchor || !anchor.getBoundingClientRect) return;
      const rect = anchor.getBoundingClientRect();
      const width = Math.max(184, popover.offsetWidth || 184);
      const height = Math.max(230, popover.offsetHeight || 230);
      const below = rect.bottom + 8;
      const above = rect.top - height - 8;
      const left = Math.max(8, Math.min(window.innerWidth - width - 8, rect.left));
      const top = below + height > window.innerHeight - 8 && above >= 8 ? above : Math.max(8, Math.min(window.innerHeight - height - 8, below));
      popover.style.left = `${left}px`;
      popover.style.top = `${top}px`;
    }
    function ensureIroColorPicker(value) {
      if (!window.iro && window.DESIGNTOOLS_IRO_SOURCE) {
        try {
          new Function(window.DESIGNTOOLS_IRO_SOURCE)();
        } catch (e) {
          console.warn("[vibepolish] iro.js failed to load", e);
        }
      }
      if (!window.iro || !window.iro.ColorPicker) return;
      const mount = $("#dt-iro-mount");
      if (!mount) return;
      const color = colorToPickerValue(value) || "#ffffff";
      if (state.iroPicker && !mount.querySelector(".IroColorPicker")) {
        state.iroPicker = null;
      }
      if (!state.iroPicker) {
        state.iroPicker = new iro.ColorPicker(mount, {
          width: 142,
          color,
          layout: [
            { component: iro.ui.Wheel },
            { component: iro.ui.Slider, options: { sliderType: "value" } },
            { component: iro.ui.Slider, options: { sliderType: "alpha" } }
          ]
        });
        state.iroPicker.on("color:change", (picked) => {
          var _a3;
          if (state.suppressColorPickerChange || !((_a3 = state.activeColor) == null ? void 0 : _a3.ready)) return;
          applyActiveColor(formatPickerColor(picked));
        });
      } else {
        state.suppressColorPickerChange = true;
        try {
          state.iroPicker.color.set(color);
        } finally {
          state.suppressColorPickerChange = false;
        }
      }
      syncColorFormatButtons();
    }
    function setColorFormat(format) {
      state.colorFormat = format === "hex" ? "hex" : "rgba";
      syncColorFormatButtons();
      if (!state.iroPicker || !state.activeColor) return;
      const input = $("#" + state.activeColor.id);
      const current = colorControlValue(input);
      if (!input || !current || current === "transparent") return;
      const formatted = formatPickerColor(state.iroPicker.color);
      if (input.dataset.styleDefaultValue) {
        input.dataset.styleDefaultValue = formatted;
        input.value = `${formatted} (默认)`;
      } else {
        input.value = formatted;
      }
      updateSwatch(state.activeColor.id, formatted);
    }
    function syncColorFormatButtons() {
      document.querySelectorAll("[data-color-format]").forEach((btn) => {
        btn.classList.toggle("dt-active", btn.dataset.colorFormat === state.colorFormat);
      });
    }
    function syncColorSpecialButtons(mode) {
      var _a3, _b2;
      (_a3 = $("#dt-color-transparent")) == null ? void 0 : _a3.classList.toggle("dt-active", mode === "transparent");
      (_b2 = $("#dt-color-empty")) == null ? void 0 : _b2.classList.toggle("dt-active", mode === "empty");
    }
    function applyActiveColor(value, options2 = {}) {
      if (!state.activeColor) return;
      const { id, prop } = state.activeColor;
      const input = $("#" + id);
      if (!input) return;
      if (sameColorValue(prop, colorControlValue(input), value)) return;
      clearDefaultColorValue(input);
      input.value = value;
      updateSwatch(id, value);
      syncColorSpecialButtons(value === "transparent" ? "transparent" : "normal");
      if (options2.close) {
        clearQueuedColorInput(id);
        applyStyle(prop, value);
      } else {
        queueColorInputApply(id, prop);
      }
      if (options2.close) closeColorPopover();
    }
    function clearActiveColor() {
      if (!state.activeColor) return;
      const { id, prop } = state.activeColor;
      const input = $("#" + id);
      if (!input) return;
      clearQueuedColorInput(id);
      clearDefaultColorValue(input);
      input.value = "";
      updateSwatch(id, "transparent");
      syncColorSpecialButtons("empty");
      applyStyle(prop, "");
      closeColorPopover();
    }
    function clearQueuedColorInput(id) {
      var _a3;
      if (!((_a3 = state.colorInputTimers) == null ? void 0 : _a3.has(id))) return;
      clearTimeout(state.colorInputTimers.get(id));
      state.colorInputTimers.delete(id);
    }
    function formatPickerColor(color) {
      return state.colorFormat === "hex" ? color.hex8String : color.rgbaString;
    }
    function colorToPickerValue(value) {
      if (!value || value === "transparent") return "";
      const normalized = normalizeStyleValue("color", value);
      return normalized && normalized !== "transparent" ? normalized : colorToHex(value);
    }
    function firstVisibleColor(value, fallback) {
      return isTransparentColor(value) ? fallback : value;
    }
    function isTransparentColor(value) {
      const text = String(value || "").trim();
      return !text || text === "transparent" || text === "rgba(0, 0, 0, 0)" || /^rgba\([^)]*,\s*0\)$/i.test(text);
    }
    function computedBorderColor(cs) {
      const width = ["Top", "Right", "Bottom", "Left"].map((side) => parseFloat(cs[`border${side}Width`]) || 0).find((value) => value > 0) || 0;
      return width > 0 ? firstVisibleColor(cs.borderTopColor, "") : "";
    }
    function updateRangeProgress(range) {
      var _a3;
      const min = Number(range.min || 0);
      const max2 = Number(range.max || 100);
      const value = Number(range.value || 0);
      const pct = max2 === min ? 0 : (value - min) / (max2 - min) * 100;
      (_a3 = range.parentElement) == null ? void 0 : _a3.style.setProperty("--dt-range-progress", `${Math.max(0, Math.min(100, pct))}%`);
    }
    function colorToHex(value) {
      const match = String(value || "").match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/i);
      if (!match) return /^#[0-9a-f]{6}$/i.test(String(value || "")) ? value : "";
      return "#" + [match[1], match[2], match[3]].map((part) => {
        return Math.max(0, Math.min(255, Number(part) || 0)).toString(16).padStart(2, "0");
      }).join("");
    }
    function targets() {
      if (!state.selected) return [];
      return state.scope === "group" ? state.group.filter(isVisible) : [state.selected];
    }
    function isVisible(el) {
      return isElementVisible(el, win());
    }
    function cssPath(el) {
      return cssPathForElement(el, doc().body, ["dt-"]);
    }
    async function exportCurrentArtifact() {
      if (!persistenceActionReady()) return;
      const provider = currentCdpStyleProvider();
      if (typeof provider !== "function") {
        syncCdpProviderConnection(false);
        toast("后台服务未连接，无法导出协作包。");
        return;
      }
      clearHoverHot();
      clearMarks();
      try {
        await waitForPendingStyleWrites();
        const result = await provider({
          action: runtimeSource.kind === "project" ? "exportProject" : "exportSingleHtmlPackage",
          ...runtimeSource.kind === "project" ? { textEdits: projectTextSourceEdits() } : { documents: [{ path: runtimeSource.file, content: currentHtml() }] },
          session: currentPortableSession()
        });
        if (!(result == null ? void 0 : result.base64) || !(result == null ? void 0 : result.filename)) throw new Error("Collaboration archive payload is empty");
        downloadBase64File({
          filename: result.filename,
          content: result.base64,
          mimeType: "application/zip"
        });
        toast("协作包已导出。");
      } catch (error) {
        recordFlowDebug("collaboration-export-failed", { error: (error == null ? void 0 : error.message) || String(error) });
        toast("协作包导出失败。");
      }
    }
    function persistenceActionReady() {
      if (!state.draft && !state.settleArmed) return true;
      toast("请先应用或取消当前快照。");
      return false;
    }
    function copyPrompt() {
      copyText(buildVisualEditPrompt(sourceName, state.edits));
    }
    async function applyCurrentSource() {
      if (!persistenceActionReady()) return;
      const provider = currentCdpStyleProvider();
      if (typeof provider !== "function") {
        syncCdpProviderConnection(false);
        toast("后台服务未连接，无法写回原文件。");
        return;
      }
      clearHoverHot();
      clearMarks();
      try {
        await waitForPendingStyleWrites();
        const result = await provider({
          action: "applySource",
          ...runtimeSource.kind === "project" ? { textEdits: projectTextSourceEdits() } : { documents: [{ path: runtimeSource.file, content: currentHtml() }] }
        });
        if (!result || !Array.isArray(result.changedPaths)) throw new Error("Source apply result is invalid");
        state.snapshots.forEach((snapshot) => {
          snapshot.persisted = true;
        });
        state.dirty = false;
        publishPanelViewModel();
        toast(result.changedPaths.length ? `已写回原文件 · ${result.changedPaths.length} 个文件` : "原文件已是最新状态。");
      } catch (error) {
        recordFlowDebug("source-apply-failed", { error: (error == null ? void 0 : error.message) || String(error) });
        toast("写回原文件失败。");
      }
    }
    async function saveCurrentSourceAs() {
      if (!persistenceActionReady()) return;
      clearHoverHot();
      clearMarks();
      try {
        await waitForPendingStyleWrites();
        if (runtimeSource.kind === "single-html") {
          await saveSingleHtmlAs();
        } else {
          await saveProjectAs();
        }
        toast("已另存为。");
      } catch (error) {
        if ((error == null ? void 0 : error.name) === "AbortError") return;
        recordFlowDebug("source-save-as-failed", { error: (error == null ? void 0 : error.message) || String(error) });
        toast("另存为失败。");
      }
    }
    async function saveSingleHtmlAs() {
      const filename = sourceName.replace(/\.html?$/i, "") + "-copy.html";
      const content = currentHtml();
      const picker = window.showSaveFilePicker;
      if (typeof picker !== "function") {
        downloadTextFile({ filename, content, mimeType: "text/html;charset=utf-8" });
        return;
      }
      const handle = await picker({
        suggestedName: filename,
        types: [{ description: "HTML", accept: { "text/html": [".html"] } }]
      });
      const writable = await handle.createWritable();
      await writable.write(content);
      await writable.close();
    }
    async function saveProjectAs() {
      const provider = currentCdpStyleProvider();
      if (typeof provider !== "function") throw new Error("Project source copy requires the background service");
      const result = await provider({
        action: "exportProjectSourceCopy",
        textEdits: projectTextSourceEdits()
      });
      if (!(result == null ? void 0 : result.base64) || !(result == null ? void 0 : result.filename)) throw new Error("Project source copy payload is empty");
      const picker = window.showDirectoryPicker;
      if (typeof picker !== "function") {
        downloadBase64File({ filename: result.filename, content: result.base64, mimeType: "application/zip" });
        return;
      }
      const parent = await picker({ mode: "readwrite" });
      const target = await parent.getDirectoryHandle(result.folderName || "vibepolish-copy", { create: true });
      const entries = unzipSync(base64Bytes(result.base64));
      for (const [relativePath, bytes] of Object.entries(entries)) {
        await writeDirectoryFile(target, relativePath, bytes);
      }
    }
    function base64Bytes(value) {
      const binary = atob(value);
      const bytes = new Uint8Array(binary.length);
      for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
      return bytes;
    }
    async function writeDirectoryFile(rootHandle, relativePath, bytes) {
      const parts = String(relativePath).split("/").filter(Boolean);
      const filename = parts.pop();
      if (!filename) return;
      let directory = rootHandle;
      for (const part of parts) directory = await directory.getDirectoryHandle(part, { create: true });
      const file = await directory.getFileHandle(filename, { create: true });
      const writable = await file.createWritable();
      await writable.write(bytes);
      await writable.close();
    }
    function buildAiPatchPayload() {
      return buildVisualEditPatchPayload(sourceName, state.edits);
    }
    function currentPortableSession() {
      return createVibePolishSession(sourceName, state.snapshots.map((snapshot) => ({
        id: snapshot.id,
        label: snapshot.label,
        createdAt: snapshot.createdAt,
        edits: snapshot.edits || [],
        transaction: snapshot.transaction || [],
        capture: snapshot.capture || null
      })));
    }
    async function captureCurrentSourceState() {
      const documents = runtimeSource.kind === "project" ? [] : [{ path: runtimeSource.file, content: currentHtml() }];
      const provider = currentCdpStyleProvider();
      if (typeof provider !== "function") return { files: documents };
      try {
        const result = await provider({
          action: "captureSourceState",
          documents,
          sourcePaths: runtimeSource.kind === "project" ? projectLoadedSourcePaths() : [],
          textEdits: runtimeSource.kind === "project" ? projectTextSourceEdits() : []
        });
        return { files: Array.isArray(result == null ? void 0 : result.files) ? result.files : documents };
      } catch (error) {
        recordFlowDebug("source-state-capture-failed", { error: (error == null ? void 0 : error.message) || String(error) });
        return { files: documents };
      }
    }
    async function captureCurrentReviewImage() {
      const provider = currentCdpStyleProvider();
      if (typeof provider !== "function") return null;
      const rect = frame.getBoundingClientRect();
      try {
        const result = await provider({
          action: "captureReviewImage",
          clip: {
            x: rect.left,
            y: rect.top,
            width: rect.width,
            height: rect.height
          }
        });
        if (!(result == null ? void 0 : result.imageDataUrl)) return null;
        const imageDataUrl = result.viewportCapture ? await cropViewportReviewImage(result.imageDataUrl, rect) : result.imageDataUrl;
        return imageDataUrl ? { imageDataUrl } : null;
      } catch (error) {
        recordFlowDebug("review-image-capture-failed", { error: (error == null ? void 0 : error.message) || String(error) });
        return null;
      }
    }
    function cropViewportReviewImage(imageDataUrl, rect) {
      return new Promise((resolve) => {
        const image = new Image();
        image.onload = () => {
          const scaleX = image.naturalWidth / Math.max(window.innerWidth, 1);
          const scaleY = image.naturalHeight / Math.max(window.innerHeight, 1);
          const canvas = document.createElement("canvas");
          canvas.width = Math.max(1, Math.round(rect.width * scaleX));
          canvas.height = Math.max(1, Math.round(rect.height * scaleY));
          const context = canvas.getContext("2d");
          if (!context) return resolve("");
          context.drawImage(
            image,
            rect.left * scaleX,
            rect.top * scaleY,
            rect.width * scaleX,
            rect.height * scaleY,
            0,
            0,
            canvas.width,
            canvas.height
          );
          resolve(canvas.toDataURL("image/png"));
        };
        image.onerror = () => resolve("");
        image.src = imageDataUrl;
      });
    }
    function currentHtml() {
      const clone = cleanRuntimeArtifactsForExport(doc());
      injectSelectionBreadthRulesForExport(clone);
      return serializeExportDocument(clone);
    }
    function projectTextSourceEdits() {
      return (state.edits || []).filter((edit) => edit.kind === "textContent" && edit.applied !== false).flatMap((edit) => edit.sourceTargets || []).filter((edit) => edit.path && Array.isArray(edit.locator) && edit.locator.length);
    }
    function projectLoadedSourcePaths() {
      if (runtimeSource.kind !== "project") return [];
      const paths = [];
      const visit = (sourceDocument) => {
        const sourcePath = sourcePathForDocument(sourceDocument);
        if (sourcePath) paths.push(sourcePath);
        for (const childFrame of sourceDocument.querySelectorAll("iframe")) {
          try {
            if (childFrame.contentDocument) visit(childFrame.contentDocument);
          } catch {
          }
        }
      };
      visit(doc());
      return uniqueValues2(paths);
    }
    function serializeExportDocument(sourceDocument) {
      return "<!DOCTYPE html>\n" + sourceDocument.documentElement.outerHTML;
    }
    function sourcePathForDocument(sourceDocument) {
      var _a3;
      if (runtimeSource.kind !== "project") return runtimeSource.file;
      try {
        const pathname = new URL(((_a3 = sourceDocument == null ? void 0 : sourceDocument.location) == null ? void 0 : _a3.href) || "").pathname;
        return pathname.startsWith("/project/") ? decodeURIComponent(pathname.slice("/project/".length)) : runtimeSource.entryFile;
      } catch {
        return runtimeSource.entryFile;
      }
    }
    function injectSelectionBreadthRulesForExport(targetDocument) {
      const rules = uniqueValues2((state.selectionBreadthRules || []).flatMap((rule) => rule.rules || []).filter(Boolean));
      if (!rules.length) return;
      const style = targetDocument.createElement("style");
      style.id = "dt-selection-breadth-style";
      style.setAttribute("data-vibepolish-style-write", "selection-breadth-export");
      style.textContent = rules.join("\n");
      targetDocument.head.appendChild(style);
    }
    window.__DESIGNTOOLS_FREEZE_TEST__ = {
      /*
      Bridge boundary:
      - Product export contract: selectionPayload, aiPatchPayload, currentHtml.
      - Read-only product computed state: ready, capabilities, meta, editCount, settleIdleMs.
      - CDP read-probe identity binding: cdpProbeTargets, clearCdpProbeTargets.
      - Forbidden shortcuts/writes: selecting, scope switching, applying edits, enumerating candidates, or resetting drafts.
      Runtime tests may read product contracts and computed state, but must drive editor writes through visible UI.
      */
      ready: () => {
        var _a3;
        return !!((_a3 = doc()) == null ? void 0 : _a3.body) && !!win();
      },
      capabilities: testCapabilities,
      selectionPayload: selectionPayloadData,
      aiPatchPayload: buildAiPatchPayload,
      currentHtml,
      meta: testMeta,
      editCount: () => state.edits.length,
      debugLog: () => ({
        enabled: ENABLE_RUNTIME_DEBUG,
        flow: (win().__DT_FLOW_DEBUG__ || []).slice(),
        pseudo: (win().__DESIGNTOOLS_CDP_PSEUDO_LOG__ || []).slice()
      }),
      clearDebugLog: () => {
        win().__DT_FLOW_DEBUG__ = [];
        win().__DESIGNTOOLS_CDP_PSEUDO_LOG__ = [];
        return true;
      },
      selectionBreadthFixtures: () => [
        ...runPropertyTargetConflictFixtureTests(doc()),
        ...runSelectorVisibilityFixtureTests(doc())
      ].map((result) => ({
        name: result.name,
        ok: result.ok,
        reason: result.reason || ""
      })),
      settleIdleMs: () => SETTLE_IDLE_MS,
      cdpProbeTargets: testCdpProbeTargets,
      clearCdpProbeTargets
    };
    function testCapabilities() {
      return propertyCapabilitiesForSelection().map((cap) => {
        var _a3, _b2, _c, _d, _e;
        return {
          key: cap.key,
          prop: cap.prop,
          group: cap.group,
          groupCapability: cap.groupCapability,
          show: cap.show,
          enabled: cap.enabled,
          reason: cap.reason || "",
          route: {
            prop: ((_a3 = cap.route) == null ? void 0 : _a3.prop) || "",
            route: ((_b2 = cap.route) == null ? void 0 : _b2.route) || "",
            visible: !!((_c = cap.route) == null ? void 0 : _c.visible),
            reason: ((_d = cap.route) == null ? void 0 : _d.reason) || "",
            targets: (((_e = cap.route) == null ? void 0 : _e.targets) || []).map((el) => cssPath(el))
          }
        };
      });
    }
    function testCdpProbeTargets(options2 = {}) {
      if (!ENABLE_EXPORT_TEST_BRIDGE) throw new Error("dt-test bridge is disabled");
      clearCdpProbeTargets();
      const kind = options2.kind || "anchor";
      const prop = options2.prop || "backgroundColor";
      const elements = cdpProbeElements(kind, prop);
      const token = `vp-cdp-${Date.now().toString(36)}-${++state.cdpProbeSeq}`;
      const items = elements.map((el, index) => {
        const id = `${token}-${index}`;
        el.setAttribute(CDP_PROBE_ATTR, id);
        const rect = el.getBoundingClientRect();
        const computed = win().getComputedStyle(el);
        return {
          id,
          selector: `[${CDP_PROBE_ATTR}="${cssStringEscape(id)}"]`,
          cssPath: cssPath(el),
          kind,
          prop,
          tag: el.tagName.toLowerCase(),
          text: compactText(el.textContent || ""),
          visible: isVisible(el),
          display: computed.display,
          visibility: computed.visibility,
          rect: roundedRect(rect)
        };
      });
      return {
        token,
        attr: CDP_PROBE_ATTR,
        kind,
        prop,
        count: items.length,
        targets: items
      };
    }
    function cdpProbeElements(kind, prop) {
      var _a3;
      if (!state.selected) return [];
      if (kind === "raw") return uniqueElementsBy([state.selectedRaw || state.selected], (el) => el);
      if (kind === "selected") return uniqueElementsBy([state.selected], (el) => el);
      if (kind === "scope") return uniqueElementsBy(targets(), (el) => el);
      if (kind === "route") {
        const route = resolveCurrentStyleRoute(prop);
        return uniqueElementsBy(route.targets || [], (el) => el);
      }
      const anchor = ((_a3 = state.visualSelection) == null ? void 0 : _a3.anchor) || state.selected;
      return uniqueElementsBy([anchor], (el) => el);
    }
    function clearCdpProbeTargets() {
      var _a3, _b2;
      const d = doc();
      if (!d) return { cleared: 0 };
      let cleared = 0;
      const attributes = /* @__PURE__ */ new Set([CDP_PROBE_ATTR, ...state.cdpProbeAttributes || []]);
      attributes.forEach((attr) => {
        const nodes = [...d.querySelectorAll(`[${attr}]`)];
        nodes.forEach((el) => {
          el.removeAttribute(attr);
          cleared += 1;
        });
      });
      (_b2 = (_a3 = state.cdpProbeAttributes) == null ? void 0 : _a3.clear) == null ? void 0 : _b2.call(_a3);
      return { cleared };
    }
    function testMeta() {
      var _a3;
      return {
        source: sourceName,
        editCount: state.edits.length,
        hasSelection: !!state.selected,
        dirty: state.dirty,
        loading: {
          breadth: ((_a3 = state.groupResult) == null ? void 0 : _a3.mode) === "selection-breadth-loading",
          writePlans: !!state.selectionBreadthWritePlansLoading
        },
        planningJob: state.selectionPlanningJob ? {
          id: state.selectionPlanningJob.id,
          revision: state.selectionPlanningJob.revision,
          kind: state.selectionPlanningJob.kind,
          status: state.selectionPlanningJob.status,
          cancelReason: state.selectionPlanningJob.cancelReason || ""
        } : null,
        selection: selectionPayloadData(),
        tableScope: testTableScopeMeta(),
        capabilities: state.selected ? testCapabilities() : [],
        objectLadder: (state.objectLadder || []).map((item, index) => ({
          index,
          selector: cssPath(item.anchor),
          roles: item.roles || [],
          confidence: item.confidence || 0,
          reason: item.reason || ""
        })),
        scopeLadder: (state.scopeLadder || []).map((item, index) => {
          var _a4;
          return {
            index,
            mode: item.mode || "",
            label: scopeLadderLabel(item, index, state.scopeLadder.length),
            confidence: item.confidence || 0,
            count: ((_a4 = item.members) == null ? void 0 : _a4.length) || 0,
            members: (item.members || []).map((el) => cssPath(el)).slice(0, 240),
            state: selectionStatePayload(item)
          };
        }),
        edits: state.edits.map((edit) => ({
          kind: edit.kind,
          value: edit.value,
          applied: edit.applied !== false,
          failureReason: edit.failureReason || "",
          target: edit.target,
          route: edit.route,
          scope: edit.scope,
          scopeLevel: edit.scopeLevel,
          count: edit.count,
          appliedTargets: edit.appliedTargets || [],
          cssSelector: edit.cssSelector || null,
          stateCondition: compactStateCondition(edit.stateCondition)
        }))
      };
    }
    function testTableScopeMeta() {
      var _a3;
      const plan = state.tableScopePlan;
      if (!plan) {
        return {
          visible: !!closestCell((_a3 = state.visualSelection) == null ? void 0 : _a3.anchor),
          view: state.tableScopeView || "current-table",
          ready: false,
          signature: "",
          fullSimilarCells: []
        };
      }
      return {
        visible: true,
        view: state.tableScopeView || "current-table",
        ready: true,
        signature: plan.signature || "",
        currentTable: cssPath(plan.currentTable),
        tableUniverse: (plan.tableUniverse || []).map(cssPath),
        compatibleTables: (plan.compatibleTables || []).map(cssPath),
        fullSimilarCells: (plan.fullSimilarCells || []).map(cssPath),
        fallbackReasons: plan.fallbackReasons || []
      };
    }
    function setupExportTestBridge() {
      if (!ENABLE_EXPORT_TEST_BRIDGE) return;
      setupRuntimeTestBridge(document);
    }
    function refreshExportTestBridge() {
      if (!ENABLE_EXPORT_TEST_BRIDGE) return;
      try {
        refreshRuntimeTestBridge({
          selection: JSON.stringify(selectionPayloadData(), null, 2),
          aiPatch: JSON.stringify(buildAiPatchPayload(), null, 2),
          html: currentHtml(),
          meta: JSON.stringify({
            source: sourceName,
            editCount: state.edits.length,
            hasSelection: !!state.selected,
            dirty: state.dirty
          }, null, 2)
        }, document);
      } catch (error) {
        refreshRuntimeTestBridge({
          selection: "",
          aiPatch: "",
          html: "",
          meta: JSON.stringify({
            source: sourceName,
            error: String(error && error.message || error)
          }, null, 2)
        }, document);
      }
    }
    const setStatus = feedback.setStatus;
    const toast = feedback.toast;
    const copyText = feedback.copyText;
    function clearToast() {
      const node = $("#dt-toast");
      if (!node) return;
      node.textContent = "";
      node.classList.remove("dt-show");
    }
    function doc() {
      var _a3;
      return ((_a3 = state.interactionDocument) == null ? void 0 : _a3.defaultView) ? state.interactionDocument : frame.contentDocument;
    }
    function win() {
      var _a3;
      return ((_a3 = doc()) == null ? void 0 : _a3.defaultView) || frame.contentWindow;
    }
    function $(selector) {
      return document.querySelector(selector);
    }
    function cssProp(prop) {
      return toCssProp(prop);
    }
    return { isDirty: () => state.dirty };
  }
  const DEFAULT_SOURCE_HTML = "<!doctype html><p>Missing source HTML</p>";
  function bootstrap() {
    const frame = document.getElementById("dt-frame");
    const panelRoot = document.getElementById("dt-panel-root");
    const sourceNode = document.getElementById("dt-source-html");
    if (!frame || !panelRoot || !sourceNode) {
      throw new Error("Freeze editor template is missing #dt-frame, #dt-panel-root, or #dt-source-html.");
    }
    const panelStore = createPanelRuntimeStore();
    const root = clientExports.createRoot(panelRoot);
    reactDomExports.flushSync(() => {
      root.render(
        /* @__PURE__ */ jsxRuntimeExports.jsx(PanelRuntimeProvider, { store: panelStore, children: /* @__PURE__ */ jsxRuntimeExports.jsx(Panel, {}) })
      );
    });
    const testMode = isTestMode(window.location);
    const runtimeSource = readRuntimeSource(window, sourceNode);
    const runtime = startLegacyFreezeEditor({
      runtimeSource,
      sourceName: readSourceName(window),
      testMode,
      runtimeDebug: isRuntimeDebugMode(window.location),
      panelStore,
      mode: readRuntimeMode(window),
      session: readRuntimeSession(window)
    });
    if (!testMode) installDirtyBeforeUnloadGuard(window, runtime.isDirty);
  }
  function readRuntimeMode(host) {
    return host.DESIGNTOOLS_RUNTIME_MODE === "review" ? "review" : "edit";
  }
  function readRuntimeSession(host) {
    return normalizeVibePolishSession(host.DESIGNTOOLS_SESSION);
  }
  function readRuntimeSource(host, sourceNode) {
    const configured = host.DESIGNTOOLS_RUNTIME_SOURCE;
    if ((configured == null ? void 0 : configured.kind) === "project" && configured.url) return configured;
    return {
      kind: "single-html",
      file: readSourceName(host),
      html: readSourceHtml(sourceNode)
    };
  }
  bootstrap();
  function readSourceHtml(sourceNode) {
    return JSON.parse(sourceNode.textContent || JSON.stringify(DEFAULT_SOURCE_HTML));
  }
  function readSourceName(host) {
    return host.DESIGNTOOLS_FREEZE_SOURCE_NAME || "demo.html";
  }
  function isTestMode(location) {
    const search = typeof location === "string" ? new URL(location, "http://vibepolish.local").search : location.search;
    return new URLSearchParams(search).has("dt-test");
  }
  function isRuntimeDebugMode(location) {
    const search = typeof location === "string" ? new URL(location, "http://vibepolish.local").search : location.search;
    return new URLSearchParams(search).has("dt-debug");
  }
  function installDirtyBeforeUnloadGuard(host, isDirty) {
    host.addEventListener("beforeunload", (event) => {
      if (!isDirty()) return;
      event.preventDefault();
      event.returnValue = "";
    });
  }
})();
//# sourceMappingURL=vibepolish-runtime.js.map
