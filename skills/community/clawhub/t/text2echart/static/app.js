
        // ============================================================
        // i18n: load JSON from lang/
        // ============================================================
        var LANG = {};

        (async function loadLang() {
            var langCode = (document.documentElement.lang || 'en').split('-')[0];
            currentLang = langCode;
            
            // Try fetch first (works when served via HTTP), fallback to embedded JSON
            try {
                var resp = await fetch('static/lang/' + langCode + '.json');
                LANG = await resp.json();
            } catch(e) {
                // Fallback: read from embedded <script type="application/json">
                try {
                    var el = document.getElementById('lang-' + langCode);
                    if (el) {
                        LANG = JSON.parse(el.textContent);
                    } else {
                        var el = document.getElementById('lang-en');
                        if (el) LANG = JSON.parse(el.textContent);
                    }
                } catch(e2) {
                    console.warn('Lang load failed');
                }
            }
            
            // Set initial lang button text
            var langBtn = document.getElementById('langBtn');
            if (langBtn) langBtn.textContent = langCode === 'en' ? '中文' : 'English';
            
            // FIX #5: Reload templates if HTML lang attribute doesn't match the loaded template
            var expectedTemplate = langCode === 'zh' ? 'static/templates.js' : 'static/templates-en.js';
            var currentTemplateScript = document.querySelector('script[src*="templates"]');
            if (currentTemplateScript && currentTemplateScript.src.indexOf(expectedTemplate) === -1) {
                // Template mismatch: reload correct template before init
                currentTemplateScript.remove();
                var newScript = document.createElement('script');
                newScript.src = expectedTemplate;
                // FIX #10: onload/onerror callbacks for dynamic template loading
                newScript.onload = function() { initApp(); };
                newScript.onerror = function() {
                    console.error('Failed to load template:', expectedTemplate);
                    initApp(); // Fall through — templates may still be defined from previous load
                };
                document.body.appendChild(newScript);
            } else {
                initApp();
            }
        })();
        // ============================================================
        // 语言切换
        // ============================================================
        var currentLang = document.documentElement.lang;

        async function switchLang() {
            var newLang = currentLang === 'en' ? 'zh' : 'en';
            try {
                var resp = await fetch('static/lang/' + newLang + '.json');
                var newLangData = await resp.json();
                Object.assign(LANG, newLangData);
            } catch(e) {
                try {
                    var el = document.getElementById('lang-' + newLang);
                    if (el) {
                        var newLangData = JSON.parse(el.textContent);
                        Object.assign(LANG, newLangData);
                    }
                } catch(e2) {}
            }
            try {
                currentLang = newLang;
                document.documentElement.lang = newLang;
                
                // Switch template file
                var templateFile = newLang === 'zh' ? 'static/templates.js' : 'static/templates-en.js';
                // Remove old template script and load new one
                var oldScript = document.querySelector('script[src*="templates"]');
                if (oldScript) oldScript.remove();
                var newScript = document.createElement('script');
                newScript.src = templateFile;
                // FIX #10: Add onload/onerror callbacks — defer UI update until template loads
                newScript.onload = function() {
                    document.getElementById('langBtn').textContent = newLang === 'en' ? '中文' : 'English';
                    document.querySelector('h1').textContent = newLang === 'en' 
                        ? 'ECharts Chart Generator v1' 
                        : 'ECharts图表生成器 v1';
                    updateStatus('valid', LANG.status.valid);
                };
                newScript.onerror = function() {
                    console.error('Failed to load template:', templateFile);
                    updateStatus('error', 'Template load failed: ' + templateFile);
                };
                document.body.appendChild(newScript);
            } catch(e) {
                console.warn('Lang switch failed', e);
            }
        }


        // ============================================================
        // Main init (runs after lang JSON loads)
        // ============================================================
        function initApp() {
            
        // Init ECharts
        window.myChart = echarts.init(document.getElementById('chart'));
        window.publicVar = {};
        window.option = {};


        // DOM elements
        const optionInput = document.getElementById('optionInput');
        const functionInput = document.getElementById('functionInput');
        const generateBtn = document.getElementById('generateBtn');
        const clearBtn = document.getElementById('clearBtn');
        const transparentBg = document.getElementById('transparentBg');
        const exportPng = document.getElementById('exportPng');
        const exportJpg = document.getElementById('exportJpg');
        const exportSvg = document.getElementById('exportSvg');
        const exportJson = document.getElementById('exportJson');
        const formatBtn = document.getElementById('formatBtn');
        const errorPanel = document.getElementById('errorPanel');
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        const chartWidth = document.getElementById('chartWidth');
        const chartHeight = document.getElementById('chartHeight');
        const chartTheme = document.getElementById('chartTheme');
        const barTemplate = document.getElementById('barTemplate');
        const lineTemplate = document.getElementById('lineTemplate');
        const pieTemplate = document.getElementById('pieTemplate');
        const cloudTemplate = document.getElementById('cloudTemplate');

        // Update status indicator
        function updateStatus(status, message) {
            statusIndicator.className = 'status-indicator';

            switch (status) {
                case 'idle':
                    statusText.textContent = LANG.status_idle;
                    break;
                case 'valid':
                    statusIndicator.classList.add('valid');
                    statusText.textContent = message || LANG.status_valid;
                    break;
                case 'error':
                    statusText.textContent = message || LANG.status_error;
                    break;
            }
        }

        // Show error panel
        function showError(message) {
            errorPanel.textContent = message;
            errorPanel.classList.add('active');
        }

        // Hide error panel
        function hideError() {
            errorPanel.classList.remove('active');
            errorPanel.textContent = '';
        }

        // Format JSON textarea
        function formatJSON(textarea) {
            try {
                const inputText = textarea.value.trim();
                if (!inputText) return;

                const parsed = JSON.parse(inputText);
                textarea.value = JSON.stringify(parsed, null, 2);
                hideError();
                updateStatus('valid', LANG.action_formatted);
            } catch (error) {
                showError(LANG.action_format_error + error.message);
            }
        }

        // Generate chart from options
        function generateChart() {
            try {

                // If options provided
                formatJSON(optionInput);
                const inputText = optionInput.value.trim();

                if (inputText) {
                    try {
                        window.option = JSON.parse(inputText);
                        // Set background color
                        if (transparentBg.checked) {
                            option.backgroundColor = 'transparent';
                        } else {
                            option.backgroundColor = 'white';
                        }
                    } catch (e) {
                        updateStatus('error', LANG.err_parse);
                        console.log(LANG.err_parse_detail + e.message + "\n" + inputText)
                        throw e;
                    }
                } else {
                    updateStatus('error', LANG.err_empty);
                    return 0
                }

                // Variable Assignment: pure JSON parse (security: no dynamic code execution)
                const functionText = functionInput.value.trim();
                if (functionText) {
                    try {
                        window.publicVar = JSON.parse(functionText);
                        updateStatus('valid', LANG.action_funcOk + JSON.stringify(window.publicVar).substring(0, 80));
                    } catch (e) {
                        updateStatus('error', LANG.err_func_detail + e.message);
                        throw e;
                    }
                } else {
                    window.publicVar = {};
                }

                // Template replacement: replace ${publicVar.x} or ${expr} in all string values
                window.option = resolveTemplates(window.option, window.publicVar);

                // Set chart container size
                var chartDom = document.getElementById('chart');
                chartDom.style.width = chartWidth.value + 'px';
                chartDom.style.height = chartHeight.value + 'px';

                updateStatus('valid', LANG.status_rendering);

                requestAnimationFrame(() => {
                    try {
                        // Dispose old chart
                        window.myChart.dispose();

                        // Reinit with selected theme
                        var theme = chartTheme.value;
                        window.myChart = echarts.init(chartDom, theme);

                        // Convert string functions to real functions
                        const realOption = transformObject(option);

                        // Set ECharts option
                        window.myChart.setOption(realOption, true);

                        // Update status
                        hideError();
                        updateStatus('valid', LANG.status_done);

                    } catch (e) {
                        updateStatus('error', LANG.err_render + e.message);
                        console.log(LANG.err_render + e.message + "\n" + functionText);
                    }
                });


            } catch (error) {

                updateStatus('error', LANG.err_render_fail);

                let errorMessage = LANG.err_parse_error + error.message + '\n';

                // Provide detailed error info
                if (error instanceof SyntaxError) {
                    const match = error.message.match(/at position (\d+)/);
                    if (match) {
                        const pos = parseInt(match[1]);
                        const text = optionInput.value;
                        const lines = text.substring(0, pos).split('\n');
                        const lineNum = lines.length;
                        const colNum = lines[lines.length - 1].length;

                        errorMessage += LANG.err_position + lineNum + LANG.err_line + colNum + LANG.err_col + text.substring(pos,pos+1) + '\n';
                        errorMessage += LANG.err_context + text.substring(Math.max(0, pos - 20), pos + 20) + '\n';
                    }
                } else {
                    errorMessage += LANG.err_detail + (error.stack || '');
                }

                showError(errorMessage);
            }
        }

        // Export chart as image/config
        function exportChart(format) {
            if (!window.myChart.getOption()) {
                showError(LANG.err_no_chart);
                return;
            }

            try {
                const bgColor = transparentBg.checked ? 'transparent' : 'white';
                let dataUrl;

                if (format === 'json') {
                    // Export config as JSON
                    const option = window.myChart.getOption();
                    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(option, null, 2));
                    const dlAnchorElem = document.createElement('a');
                    dlAnchorElem.setAttribute("href", dataStr);
                    dlAnchorElem.setAttribute("download", "echarts-config.json");
                    dlAnchorElem.click();
                    updateStatus('valid', LANG.action_exported_config);
                    return;
                } else {
                    // Export as image
                    const exportOptions = {
                        type: format,
                        pixelRatio: 2,
                        backgroundColor: bgColor
                    };

                    dataUrl = myChart.getDataURL(exportOptions);
                }

                const link = document.createElement('a');
                link.href = dataUrl;
                link.download = `echart-${new Date().getTime()}.${format}`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                updateStatus('valid', LANG.action_exported + format.toUpperCase());
            } catch (error) {
                showError(LANG.err_export + error.message);
            }
        }

        // Apply chart template
        // Event listeners
        generateBtn.addEventListener('click', generateChart);

        clearBtn.addEventListener('click', () => {
            optionInput.value = '';
            myChart.clear();
            hideError();
            updateStatus('idle');
        });

        // Debounce helper
        function debounce(fn, delay) {
            let timer = null;
            return function(...args) {
                clearTimeout(timer);
                timer = setTimeout(() => fn.apply(this, args), delay);
            };
        }

        const debouncedGenerate = debounce(generateChart, 300);

        transparentBg.addEventListener('change', debouncedGenerate);
        chartTheme.addEventListener('change', debouncedGenerate);
        chartHeight.addEventListener('input', debouncedGenerate);
        chartWidth.addEventListener('input', debouncedGenerate);

        exportPng.addEventListener('click', () => exportChart('png'));
        exportJpg.addEventListener('click', () => exportChart('jpg'));
        exportSvg.addEventListener('click', () => exportChart('svg'));
        exportJson.addEventListener('click', () => exportChart('json'));

        formatBtn.addEventListener('click', () => {
            formatJSON(optionInput);
        });

        barTemplate.addEventListener('click', () => applyTemplate('bar'));
        lineTemplate.addEventListener('click', () => applyTemplate('line'));
        pieTemplate.addEventListener('click', () => applyTemplate('pie'));
        cloudTemplate.addEventListener('click', () => applyTemplate('cloud'));


        // Resize chart on window resize
        window.addEventListener('resize', () => {
            if (window.myChart && !window.myChart.isDisposed()) {
                window.myChart.resize();
            }
        });

        // Load default template on startup
        window.onload = () => {
            applyTemplate('pie');
        };

        // Live JSON validation
        optionInput.addEventListener('blur', function() {
            try {
                if (this.value.trim() === '') {
                    hideError();
                    updateStatus('idle');
                    return;
                }

                JSON.parse(this.value);
                hideError();
                updateStatus('valid', LANG.status_valid);
            } catch (error) {
                updateStatus('error', LANG.err_parse_detail + error.message);
                let errorMessage = LANG.err_parse_error + error.message + '\n';
                const match = error.message.match(/at position (\d+)/);
                if (match) {
                    const pos = parseInt(match[1]);
                    const text = optionInput.value;
                    const lines = text.substring(0, pos).split('\n');
                    const lineNum = lines.length;
                    const colNum = lines[lines.length - 1].length;
                    errorMessage += LANG.err_position + lineNum + LANG.err_line + colNum + LANG.err_col + text.substring(pos,pos+1) + '\n';
                    errorMessage += LANG.err_context + text.substring(Math.max(0, pos - 20), pos + 20) + '\n';
                } else {
                    errorMessage += LANG.err_detail + (error.stack || '');
                }
                showError(errorMessage);
            }
        });

        // ============================================================
        // Template resolution: replace ${...} patterns in all string values
        // ============================================================
        function resolveTemplates(obj, vars) {
            if (typeof obj === 'string') {
                return obj.replace(/\$\{([^}]+)\}/g, function(match, expr) {
                    try {
                        var val = safeEval(expr.trim(), vars);
                        // If result is a number or boolean, convert to string; otherwise keep as-is
                        if (typeof val === 'number' || typeof val === 'boolean') {
                            return String(val);
                        }
                        return val;
                    } catch (e) {
                        // If expression fails, keep original placeholder
                        return match;
                    }
                });
            } else if (Array.isArray(obj)) {
                var result = [];
                for (var i = 0; i < obj.length; i++) {
                    result[i] = resolveTemplates(obj[i], vars);
                }
                return result;
            } else if (obj !== null && typeof obj === 'object') {
                var result = {};
                for (var key in obj) {
                    if (Object.prototype.hasOwnProperty.call(obj, key)) {
                        result[key] = resolveTemplates(obj[key], vars);
                    }
                }
                return result;
            }
            // Primitives (number, boolean, null, undefined) — return as-is
            return obj;
        }

        // ============================================================
        // Safe expression parser (no eval / new Function / Function)
        // Supports: +, -, *, /, %, parentheses, numbers, variable refs, array indices
        // ============================================================
        function safeEval(expr, vars) {
            // Whitelist: only allow safe characters
            if (!/^[\w\s+\-*/%().[\]]+$/.test(expr)) {
                throw new Error('Invalid characters in expression: ' + expr);
            }
            // Reject function call patterns: word + (
            if (/\w\s*\(/.test(expr)) {
                throw new Error('Function calls not allowed: ' + expr);
            }
            var tokens = tokenize(expr);
            var result = parseExpression(tokens, 0, vars);
            return result.value;
        }

        function tokenize(expr) {
            var tokens = [];
            var i = 0;
            var len = expr.length;
            while (i < len) {
                var ch = expr[i];
                // Skip whitespace
                if (/\s/.test(ch)) {
                    i++;
                    continue;
                }
                // Number: integer or decimal
                if (/[0-9]/.test(ch) || (ch === '.' && i + 1 < len && /[0-9]/.test(expr[i + 1]))) {
                    var num = '';
                    while (i < len && /[0-9.]/.test(expr[i])) {
                        num += expr[i];
                        i++;
                    }
                    tokens.push({ type: 'NUMBER', value: parseFloat(num) });
                    continue;
                }
                // Identifier: letter or underscore followed by word chars
                if (/[a-zA-Z_]/.test(ch)) {
                    var ident = '';
                    while (i < len && /[\w]/.test(expr[i])) {
                        ident += expr[i];
                        i++;
                    }
                    tokens.push({ type: 'IDENTIFIER', value: ident });
                    continue;
                }
                // Operators and punctuation
                if (ch === '+' || ch === '-' || ch === '*' || ch === '/' || ch === '%') {
                    tokens.push({ type: 'OPERATOR', value: ch });
                    i++;
                    continue;
                }
                if (ch === '(') { tokens.push({ type: 'LPAREN', value: ch }); i++; continue; }
                if (ch === ')') { tokens.push({ type: 'RPAREN', value: ch }); i++; continue; }
                if (ch === '[') { tokens.push({ type: 'LBRACKET', value: ch }); i++; continue; }
                if (ch === ']') { tokens.push({ type: 'RBRACKET', value: ch }); i++; continue; }
                if (ch === '.') { tokens.push({ type: 'DOT', value: ch }); i++; continue; }
                // Unknown character
                throw new Error('Unexpected character: ' + ch + ' at position ' + i);
            }
            return tokens;
        }

        // Recursive descent parser entry: expression = term (('+' | '-') term)*
        function parseExpression(tokens, pos, vars) {
            var result = parseTerm(tokens, pos, vars);
            pos = result.pos;
            var value = result.value;
            while (pos < tokens.length) {
                var tok = tokens[pos];
                if (tok.type === 'OPERATOR' && (tok.value === '+' || tok.value === '-')) {
                    pos++;
                    var right = parseTerm(tokens, pos, vars);
                    pos = right.pos;
                    if (tok.value === '+') {
                        value = value + right.value;
                    } else {
                        value = value - right.value;
                    }
                } else {
                    break;
                }
            }
            return { value: value, pos: pos };
        }

        // term = factor (('*' | '/' | '%') factor)*
        function parseTerm(tokens, pos, vars) {
            var result = parseFactor(tokens, pos, vars);
            pos = result.pos;
            var value = result.value;
            while (pos < tokens.length) {
                var tok = tokens[pos];
                if (tok.type === 'OPERATOR' && (tok.value === '*' || tok.value === '/' || tok.value === '%')) {
                    pos++;
                    var right = parseFactor(tokens, pos, vars);
                    pos = right.pos;
                    if (tok.value === '*') {
                        value = value * right.value;
                    } else if (tok.value === '/') {
                        value = value / right.value;
                    } else {
                        value = value % right.value;
                    }
                } else {
                    break;
                }
            }
            return { value: value, pos: pos };
        }

        // factor = unary? primary
        function parseFactor(tokens, pos, vars) {
            if (pos >= tokens.length) {
                throw new Error('Unexpected end of expression');
            }
            var tok = tokens[pos];
            // Unary minus
            if (tok.type === 'OPERATOR' && tok.value === '-') {
                pos++;
                var result = parseFactor(tokens, pos, vars);
                return { value: -result.value, pos: result.pos };
            }
            // Unary plus (no-op)
            if (tok.type === 'OPERATOR' && tok.value === '+') {
                pos++;
                return parseFactor(tokens, pos, vars);
            }
            return parsePrimary(tokens, pos, vars);
        }

        // primary = NUMBER | '(' expression ')' | IDENTIFIER postfix*
        function parsePrimary(tokens, pos, vars) {
            if (pos >= tokens.length) {
                throw new Error('Unexpected end of expression');
            }
            var tok = tokens[pos];
            if (tok.type === 'NUMBER') {
                return { value: tok.value, pos: pos + 1 };
            }
            if (tok.type === 'LPAREN') {
                pos++;
                var result = parseExpression(tokens, pos, vars);
                if (result.pos >= tokens.length || tokens[result.pos].type !== 'RPAREN') {
                    throw new Error('Missing closing parenthesis');
                }
                return { value: result.value, pos: result.pos + 1 };
            }
            if (tok.type === 'IDENTIFIER') {
                return parseIdentifierAccess(tokens, pos, vars);
            }
            throw new Error('Unexpected token: ' + JSON.stringify(tok));
        }

        // identifier postfix*  —  handles publicVar.x, x[0], etc.
        function parseIdentifierAccess(tokens, pos, vars) {
            var tok = tokens[pos];
            var rootName = tok.value;
            pos++;
            // Resolve the root variable
            var value;
            if (rootName === 'publicVar') {
                value = vars;
            } else if (vars.hasOwnProperty && vars.hasOwnProperty(rootName)) {
                value = vars[rootName];
            } else if (typeof vars[rootName] !== 'undefined') {
                value = vars[rootName];
            } else {
                throw new Error('Undefined variable: ' + rootName);
            }
            // Handle postfix: .prop, [index]
            while (pos < tokens.length) {
                var next = tokens[pos];
                if (next.type === 'DOT') {
                    pos++;
                    if (pos >= tokens.length || tokens[pos].type !== 'IDENTIFIER') {
                        throw new Error('Expected property name after dot');
                    }
                    var propName = tokens[pos].value;
                    pos++;
                    if (value === null || value === undefined) {
                        throw new Error('Cannot access property ' + propName + ' of null/undefined');
                    }
                    value = value[propName];
                } else if (next.type === 'LBRACKET') {
                    pos++;
                    var idxResult = parseExpression(tokens, pos, vars);
                    pos = idxResult.pos;
                    if (pos >= tokens.length || tokens[pos].type !== 'RBRACKET') {
                        throw new Error('Missing closing bracket ]');
                    }
                    pos++;
                    if (value === null || value === undefined) {
                        throw new Error('Cannot index null/undefined');
                    }
                    value = value[idxResult.value];
                } else {
                    break;
                }
            }
            if (typeof value !== 'number') {
                throw new Error('Variable ' + rootName + ' is not a number: ' + JSON.stringify(value));
            }
            return { value: value, pos: pos };
        }

        // transformObject: pure deep copy — no function conversion (security: no dynamic code execution)
        function transformObject(obj) {
            if (Array.isArray(obj)) {
                var result = [];
                for (var i = 0; i < obj.length; i++) {
                    result[i] = transformObject(obj[i]);
                }
                return result;
            } else if (obj !== null && typeof obj === 'object') {
                var result = {};
                for (var key in obj) {
                    if (Object.prototype.hasOwnProperty.call(obj, key)) {
                        result[key] = transformObject(obj[key]);
                    }
                }
                return result;
            }
            // Primitives (string, number, boolean, null, undefined) — return as-is
            return obj;
        }
        
        } // end initApp()
    