/**
 * Mermaid diagram renderer for Canvas
 * Usage: canvas eval with this script, passing diagram code
 * 
 * Supports: graph, sequenceDiagram, stateDiagram, erDiagram, classDiagram, 
 *           gantt, mindmap, flowchart, pie
 */

function renderMermaid(diagramCode, options = {}) {
  const {
    theme = 'dark',
    backgroundColor = '#1e1e2e',
    fontSize = 14,
    width = 'auto',
    padding = 20
  } = options;

  // Clean up the diagram code
  const cleanCode = diagramCode.trim();

  document.documentElement.style.margin = '0';
  document.documentElement.style.padding = '0';
  document.body.style.margin = '0';
  document.body.style.padding = `${padding}px`;
  document.body.style.backgroundColor = backgroundColor;
  document.body.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace';
  document.body.style.color = '#cdd6f4';

  // Create container
  const container = document.createElement('div');
  container.id = 'mermaid-container';
  container.style.display = 'flex';
  container.style.justifyContent = 'center';
  container.style.alignItems = 'center';
  container.style.minHeight = '200px';
  
  const mermaidDiv = document.createElement('div');
  mermaidDiv.className = 'mermaid';
  mermaidDiv.textContent = cleanCode;
  container.appendChild(mermaidDiv);
  
  document.body.innerHTML = '';
  document.body.appendChild(container);

  // Load Mermaid
  return new Promise((resolve) => {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
    script.onload = () => {
      mermaid.initialize({
        startOnReady: true,
        theme: theme,
        themeVariables: {
          darkMode: true,
          background: backgroundColor,
          primaryColor: '#89b4fa',
          primaryTextColor: '#cdd6f4',
          primaryBorderColor: '#585b70',
          lineColor: '#a6adc8',
          secondaryColor: '#a6e3a1',
          tertiaryColor: '#f9e2af',
          noteBkgColor: '#313244',
          noteTextColor: '#cdd6f4',
          fontSize: `${fontSize}px`
        },
        flowchart: { 
          htmlLabels: true, 
          curve: 'basis',
          padding: 15
        },
        sequence: { 
          actorMargin: 50, 
          messageMargin: 40,
          mirrorActors: false 
        },
        mindmap: {
          padding: 20
        }
      });
      
      // Wait for render
      setTimeout(() => {
        const svg = container.querySelector('svg');
        if (svg) {
          // Make SVG responsive
          svg.style.maxWidth = '100%';
          svg.style.height = 'auto';
          resolve('rendered');
        } else {
          resolve('no-svg');
        }
      }, 2000);
    };
    script.onerror = () => resolve('load-error');
    document.head.appendChild(script);
  });
}

// Title helper
function addTitle(title, subtitle) {
  const header = document.createElement('div');
  header.style.textAlign = 'center';
  header.style.marginBottom = '16px';
  header.style.padding = '0 20px';
  
  if (title) {
    const h = document.createElement('h2');
    h.textContent = title;
    h.style.color = '#cdd6f4';
    h.style.margin = '0 0 4px 0';
    h.style.fontSize = '18px';
    h.style.fontWeight = '600';
    header.appendChild(h);
  }
  if (subtitle) {
    const s = document.createElement('p');
    s.textContent = subtitle;
    s.style.color = '#a6adc8';
    s.style.margin = '0';
    s.style.fontSize = '13px';
    header.appendChild(s);
  }
  
  document.body.insertBefore(header, document.body.firstChild);
}

// Annotation overlay helper  
function addAnnotation(text, x, y, color = '#f9e2af') {
  const note = document.createElement('div');
  note.style.position = 'absolute';
  note.style.left = `${x}px`;
  note.style.top = `${y}px`;
  note.style.backgroundColor = 'rgba(49, 50, 68, 0.95)';
  note.style.color = color;
  note.style.padding = '6px 10px';
  note.style.borderRadius = '6px';
  note.style.fontSize = '12px';
  note.style.maxWidth = '200px';
  note.style.border = `1px solid ${color}`;
  note.style.zIndex = '100';
  note.textContent = text;
  document.body.style.position = 'relative';
  document.body.appendChild(note);
}
