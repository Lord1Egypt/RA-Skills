function setStyle(el, style) {
      el.setAttribute("style", style);
    }

    const themeSceneColors = {
      "warm-editorial": {
        summarySurface: "#faf7f0",
        summaryText: "#3d3d3a",
        warningSurface: "#f6e8e4",
        warningText: "#7a2f29",
        warningBorder: "#d97757",
        positiveSurface: "#f1f5ec",
        positiveText: "#5f7748",
        positiveBorder: "#cbd6bd"
      },
      "light-simple": {
        summarySurface: "#f9fafb",
        summaryText: "#2c3e50",
        warningSurface: "#fff1f2",
        warningText: "#e11d48",
        warningBorder: "#fecdd3",
        positiveSurface: "#f0fdf4",
        positiveText: "#166534",
        positiveBorder: "#bbf7d0"
      },
      "tech-blue": {
        summarySurface: "#eff6ff",
        summaryText: "#1e3a8a",
        warningSurface: "#fff1f0",
        warningText: "#cf222e",
        warningBorder: "#fecaca",
        positiveSurface: "#ecfdf5",
        positiveText: "#047857",
        positiveBorder: "#a7f3d0"
      },
      "indigo-card": {
        summarySurface: "#e0e7ff",
        summaryText: "#4338ca",
        warningSurface: "#fff1f2",
        warningText: "#be123c",
        warningBorder: "#fecdd3",
        positiveSurface: "#eff6ff",
        positiveText: "#2563eb",
        positiveBorder: "#bfdbfe"
      },
      "swiss-grid": {
        summarySurface: "#f8f8f8",
        summaryText: "#000000",
        warningSurface: "#fff1f1",
        warningText: "#b91c1c",
        warningBorder: "#000000",
        positiveSurface: "#f1f1f1",
        positiveText: "#1a1a1a",
        positiveBorder: "#1a1a1a"
      },
      "purple-highlight": {
        summarySurface: "#f5f3ff",
        summaryText: "#581c87",
        warningSurface: "#fff1f2",
        warningText: "#be123c",
        warningBorder: "#fecdd3",
        positiveSurface: "#f3e8ff",
        positiveText: "#6b21a8",
        positiveBorder: "#c4b5fd"
      },
      "warm-nature": {
        summarySurface: "#ecfccb",
        summaryText: "#3f6212",
        warningSurface: "#fdf6e3",
        warningText: "#78350f",
        warningBorder: "#fde68a",
        positiveSurface: "#f5f5f4",
        positiveText: "#4d7c0f",
        positiveBorder: "#d9f99d"
      },
      "vitality-orange": {
        summarySurface: "#fff7ed",
        summaryText: "#c2410c",
        warningSurface: "#ffedd5",
        warningText: "#431407",
        warningBorder: "#fdba74",
        positiveSurface: "#fff7ed",
        positiveText: "#db2777",
        positiveBorder: "#fed7aa"
      },
      "wechat-pure-glass": {
        summarySurface: "#f2fbf6",
        summaryText: "#064e3b",
        warningSurface: "#fff7ed",
        warningText: "#c2410c",
        warningBorder: "#fed7aa",
        positiveSurface: "#f2fbf6",
        positiveText: "#065f32",
        positiveBorder: "#07c160"
      },
      "modern-cobalt": {
        summarySurface: "#eff6ff",
        summaryText: "#1e40af",
        warningSurface: "#fff1f2",
        warningText: "#be123c",
        warningBorder: "#fecdd3",
        positiveSurface: "#f1f5f9",
        positiveText: "#2563eb",
        positiveBorder: "#93c5fd"
      },
      "deep-space": {
        summarySurface: "#1e1b4b",
        summaryText: "#e9d5ff",
        warningSurface: "#f3e8ff",
        warningText: "#581c87",
        warningBorder: "#7c3aed",
        positiveSurface: "#e2e8f0",
        positiveText: "#0f172a",
        positiveBorder: "#06b6d4"
      }
    };

    const centeredHeadingThemes = new Set([
      "purple-highlight",
      "modern-cobalt",
      "deep-space"
    ]);

    function headingAlignmentFor(themeId) {
      return centeredHeadingThemes.has(themeId) ? " text-align: center;" : "";
    }

    function getTheme(themeId) {
      const resolvedThemeId = themes[themeId] ? themeId : (themes["warm-editorial"] ? "warm-editorial" : "light-simple");
      const base = themes[resolvedThemeId] || {};
      const scene = themeSceneColors[resolvedThemeId] || themeSceneColors["warm-editorial"];
      return {
        text: base.text || "#3d3d3a",
        heading: base.heading || "#141413",
        accent: base.accent || "#b85c3e",
        muted: base.muted || "#8a8175",
        surface: base.surface || "#faf7f0",
        border: base.border || "#ded7ca",
        quoteSurface: base.quoteSurface || base.surface || "#f0eee6",
        codeSurface: base.codeSurface || "#f0eee6",
        codeText: base.codeText || "#b04a3f",
        tableHeader: base.tableHeader || base.surface || "#fbfaf6",
        tableBorder: base.tableBorder || base.border || "#d1cfc5",
        summarySurface: base.summarySurface || scene.summarySurface || base.surface || "#faf7f0",
        summaryText: base.summaryText || scene.summaryText || base.text || "#3d3d3a",
        warningSurface: base.warningSurface || scene.warningSurface || "#f6e8e4",
        warningText: base.warningText || scene.warningText || "#7a2f29",
        warningBorder: base.warningBorder || scene.warningBorder || base.border || "#ded7ca",
        positiveSurface: base.positiveSurface || scene.positiveSurface || "#f1f5ec",
        positiveText: base.positiveText || scene.positiveText || "#5f7748",
        positiveBorder: base.positiveBorder || scene.positiveBorder || base.border || "#ded7ca"
      };
    }

    function styleFor(name, fallback) {
      return styles[name] || fallback;
    }

    function applyToArticle(selector, style) {
      document.querySelectorAll("#wechatArticle " + selector).forEach(el => setStyle(el, style));
    }

    function applyTheme(themeId) {
      const t = getTheme(themeId);
      const article = document.querySelector("#wechatArticle");
      const articleStyle = styleFor("article", "max-width: 677px; margin: 0 auto; padding: 28px 18px 34px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; font-size: 16px; line-height: 1.8; letter-spacing: 0; word-break: break-word; overflow-wrap: anywhere;");
      setStyle(article, articleStyle + " color: " + t.text + ";");

      const sectionStyle = styleFor("section", "margin: 30px 0 0;");
      const pStyle = styleFor("p", "margin: 0 0 14px; font-size: 16px; line-height: 1.8; letter-spacing: 0; word-break: break-word; overflow-wrap: anywhere;");
      const headingAlignment = headingAlignmentFor(themeId);
      const h1Style = styleFor("h1", "margin: 0 0 14px; font-size: 24px; line-height: 1.25; font-weight: 760; letter-spacing: 0;") + headingAlignment;
      const h2Style = styleFor("h2", "margin: 0 0 14px; font-size: 20px; line-height: 1.35; font-weight: 720; letter-spacing: 0;") + headingAlignment;
      const h3Style = styleFor("h3", "margin: 24px 0 10px; font-size: 16px; line-height: 1.45; font-weight: 700; letter-spacing: 0;");
      const labelStyle = styleFor("moduleLabel", styleFor("eyebrow", "margin: 0 0 10px; font-size: 12px; line-height: 1.5; letter-spacing: 0; font-family: Menlo, Consolas, monospace;"));
      const tableStyle = styleFor("table", "width: 100%; border-collapse: collapse; margin: 18px 0; table-layout: fixed; word-break: break-word; overflow-wrap: anywhere; font-size: 14px; line-height: 1.65;");
      const thStyle = styleFor("th", "padding: 12px 8px; text-align: left; border: 1px solid; font-weight: 700; word-break: break-word; overflow-wrap: anywhere;");
      const tdStyle = styleFor("td", "padding: 12px 8px; border: 1px solid; vertical-align: top; word-break: break-word; overflow-wrap: anywhere;");
      const codeStyle = styleFor("code", "padding: 2px 6px; border-radius: 5px; font-family: Menlo, Consolas, monospace; font-size: 14px; line-height: 1.6; word-break: break-word; overflow-wrap: anywhere;");
      const preStyle = styleFor("pre", "margin: 18px 0; padding: 14px; border-radius: 8px; overflow-x: auto; white-space: pre-wrap; word-break: break-word; font-family: Menlo, Consolas, monospace; font-size: 13px; line-height: 1.65;");

      document.querySelectorAll("[data-role='hero']").forEach(el => setStyle(el, styleFor("hero", "margin: 0 0 24px; padding: 28px 18px 18px; border-bottom: 1px solid;") + " background: " + t.surface + "; border-color: " + t.border + ";"));
      document.querySelectorAll("[data-role='eyebrow']").forEach(el => setStyle(el, styleFor("eyebrow", labelStyle) + headingAlignment + " color: " + t.muted + ";"));
      document.querySelectorAll("[data-role='moduleLabel']").forEach(el => setStyle(el, labelStyle + headingAlignment + " color: " + t.accent + ";"));
      document.querySelectorAll("[data-role='h1']").forEach(el => setStyle(el, h1Style + " color: " + t.heading + ";"));
      document.querySelectorAll("[data-role='dek']").forEach(el => setStyle(el, styleFor("dek", "margin: 12px 0 0; font-size: 17px; line-height: 1.8; letter-spacing: 0;") + headingAlignment + " color: " + t.text + ";"));
      document.querySelectorAll("[data-role='p']").forEach(el => setStyle(el, pStyle + " color: " + t.text + ";"));
      document.querySelectorAll("[data-role='section']").forEach(el => setStyle(el, sectionStyle));
      document.querySelectorAll("[data-role='h2']").forEach(el => setStyle(el, h2Style + " color: " + t.heading + ";"));
      document.querySelectorAll("[data-role='h3']").forEach(el => setStyle(el, h3Style + " color: " + t.heading + ";"));
      document.querySelectorAll("[data-role='quote']").forEach(el => setStyle(el, styleFor("quote", "margin: 20px 0; padding: 16px; border: 1px solid; border-radius: 8px;") + " background: " + t.quoteSurface + "; border-color: " + t.border + "; color: " + t.heading + ";"));
      document.querySelectorAll("[data-role='quoteText']").forEach(el => setStyle(el, styleFor("quoteText", "margin: 0; font-size: 18px; line-height: 1.75; font-family: 'Songti SC', STSong, SimSun, serif;") + " color: inherit;"));
      document.querySelectorAll("[data-role='figure']").forEach(el => setStyle(el, styleFor("figure", "margin: 22px 0;")));
      document.querySelectorAll("[data-role='image']").forEach(el => setStyle(el, styleFor("image", "display: block; width: 100%; height: auto; border: 1px solid; border-radius: 8px;") + " border-color: " + t.border + ";"));
      document.querySelectorAll("[data-role='figcaption']").forEach(el => setStyle(el, styleFor("figcaption", "margin: 8px 0 0; font-size: 13px; line-height: 1.6; text-align: center;") + " color: " + t.muted + ";"));
      document.querySelectorAll("[data-role='callout']").forEach(el => setStyle(el, styleFor("callout", "margin: 20px 0; padding: 16px; border: 1px solid; border-radius: 8px;") + " background: " + t.surface + "; border-color: " + t.border + ";"));
      document.querySelectorAll("[data-role='calloutTitle']").forEach(el => setStyle(el, styleFor("calloutTitle", labelStyle + " font-weight: 700;") + " color: " + t.accent + ";"));
      document.querySelectorAll("[data-role='ul']").forEach(el => setStyle(el, styleFor("ul", "margin: 12px 0 16px; padding-left: 1.2em;") + " color: " + t.text + ";"));
      document.querySelectorAll("[data-role='ol']").forEach(el => setStyle(el, styleFor("ol", styleFor("ul", "margin: 12px 0 16px; padding-left: 1.2em;")) + " color: " + t.text + ";"));
      document.querySelectorAll("[data-role='li']").forEach(el => setStyle(el, styleFor("li", "margin: 0 0 8px; font-size: 16px; line-height: 1.8;") + " color: " + t.text + ";"));
      document.querySelectorAll("[data-role='summary']").forEach(el => setStyle(el, styleFor("summary", "margin: 24px 0 0; padding: 16px; border: 1px solid; border-radius: 8px;") + " background: " + t.summarySurface + "; border-color: " + t.border + ";"));
      document.querySelectorAll("[data-role='summaryTitle']").forEach(el => setStyle(el, styleFor("summaryTitle", labelStyle + " font-weight: 700;") + " color: " + t.accent + ";"));
      document.querySelectorAll("[data-role='summaryText']").forEach((el, index, list) => {
        const margin = index === list.length - 1 ? "margin: 0;" : styleFor("summaryText", "margin: 0 0 10px;");
        setStyle(el, margin + " color: " + t.summaryText + "; font-size: 16px; line-height: 1.8;");
      });
      document.querySelectorAll("[data-role='table']").forEach(el => setStyle(el, tableStyle + " border-color: " + t.tableBorder + ";"));
      document.querySelectorAll("[data-role='th']").forEach(el => setStyle(el, thStyle + " background: " + t.tableHeader + "; border-color: " + t.tableBorder + "; color: " + t.heading + ";"));
      document.querySelectorAll("[data-role='td']").forEach(el => setStyle(el, tdStyle + " border-color: " + t.tableBorder + "; color: " + t.text + ";"));
      document.querySelectorAll("[data-role='code']").forEach(el => setStyle(el, codeStyle + " background: " + t.codeSurface + "; color: " + t.codeText + ";"));
      document.querySelectorAll("[data-role='pre']").forEach(el => setStyle(el, preStyle + " background: " + t.codeSurface + "; color: " + t.text + ";"));
      document.querySelectorAll("[data-role='strong']").forEach(el => setStyle(el, styleFor("strong", "font-weight: 700;") + " color: " + t.heading + ";"));
      document.querySelectorAll("[data-role='a']").forEach(el => setStyle(el, styleFor("a", "text-decoration: none; border-bottom: 1px solid;") + " color: " + t.accent + "; border-color: " + t.accent + ";"));
      document.querySelectorAll("[data-role='hr']").forEach(el => setStyle(el, styleFor("hr", "margin: 30px 0; border: 0; border-top: 1px solid;") + " border-color: " + t.border + ";"));
      document.querySelectorAll("[data-role='warning']").forEach(el => setStyle(el, styleFor("callout", "margin: 20px 0; padding: 16px; border: 1px solid; border-radius: 8px;") + " background: " + t.warningSurface + "; border-color: " + t.warningBorder + "; color: " + t.warningText + ";"));
      document.querySelectorAll("[data-role='positive']").forEach(el => setStyle(el, styleFor("callout", "margin: 20px 0; padding: 16px; border: 1px solid; border-radius: 8px;") + " background: " + t.positiveSurface + "; border-color: " + t.positiveBorder + "; color: " + t.positiveText + ";"));

      applyToArticle("h1:not([data-role])", h1Style + " color: " + t.heading + ";");
      applyToArticle("h2:not([data-role])", h2Style + " color: " + t.heading + ";");
      applyToArticle("h3:not([data-role])", h3Style + " color: " + t.heading + ";");
      applyToArticle("p:not([data-role])", pStyle + " color: " + t.text + ";");
      applyToArticle("ul:not([data-role])", styleFor("ul", "margin: 12px 0 16px; padding-left: 1.2em;") + " color: " + t.text + ";");
      applyToArticle("ol:not([data-role])", styleFor("ol", styleFor("ul", "margin: 12px 0 16px; padding-left: 1.2em;")) + " color: " + t.text + ";");
      applyToArticle("li:not([data-role])", styleFor("li", "margin: 0 0 8px; font-size: 16px; line-height: 1.8;") + " color: " + t.text + ";");
      applyToArticle("blockquote:not([data-role])", styleFor("quote", "margin: 20px 0; padding: 16px; border: 1px solid; border-radius: 8px;") + " background: " + t.quoteSurface + "; border-color: " + t.border + "; color: " + t.heading + ";");
      applyToArticle("figure:not([data-role])", styleFor("figure", "margin: 22px 0;"));
      applyToArticle("img:not([data-role])", styleFor("image", "display: block; width: 100%; height: auto; border: 1px solid; border-radius: 8px;") + " border-color: " + t.border + ";");
      applyToArticle("figcaption:not([data-role])", styleFor("figcaption", "margin: 8px 0 0; font-size: 13px; line-height: 1.6; text-align: center;") + " color: " + t.muted + ";");
      applyToArticle("table:not([data-role])", tableStyle + " border-color: " + t.tableBorder + ";");
      applyToArticle("th:not([data-role])", thStyle + " background: " + t.tableHeader + "; border-color: " + t.tableBorder + "; color: " + t.heading + ";");
      applyToArticle("td:not([data-role])", tdStyle + " border-color: " + t.tableBorder + "; color: " + t.text + ";");
      applyToArticle("pre:not([data-role])", preStyle + " background: " + t.codeSurface + "; color: " + t.text + ";");
      applyToArticle("code:not([data-role])", codeStyle + " background: " + t.codeSurface + "; color: " + t.codeText + ";");
      applyToArticle("strong:not([data-role])", styleFor("strong", "font-weight: 700;") + " color: " + t.heading + ";");
      applyToArticle("a:not([data-role])", styleFor("a", "text-decoration: none; border-bottom: 1px solid;") + " color: " + t.accent + "; border-color: " + t.accent + ";");
      applyToArticle("hr:not([data-role])", styleFor("hr", "margin: 30px 0; border: 0; border-top: 1px solid;") + " border-color: " + t.border + ";");
    }

    function blobToDataUrl(blob) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result || ""));
        reader.onerror = () => reject(reader.error || new Error("读取图片失败"));
        reader.readAsDataURL(blob);
      });
    }

    async function fetchImageAsDataUrl(src) {
      const absoluteUrl = new URL(src, document.baseURI).href;
      const response = await fetch(absoluteUrl);
      if (!response.ok) {
        throw new Error("图片请求失败：" + response.status);
      }
      const blob = await response.blob();
      if (!blob.type.startsWith("image/")) {
        throw new Error("资源不是图片：" + blob.type);
      }
      return await blobToDataUrl(blob);
    }

    function renderedImageToDataUrl(img) {
      if (!img.complete || !img.naturalWidth || !img.naturalHeight) {
        throw new Error("图片尚未加载完成");
      }
      const canvas = document.createElement("canvas");
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      const context = canvas.getContext("2d");
      if (!context) {
        throw new Error("无法创建图片画布");
      }
      context.drawImage(img, 0, 0);
      return canvas.toDataURL("image/png");
    }

    async function inlineImagesForCopy(sourceArticle, clonedArticle) {
      const sourceImages = Array.from(sourceArticle.querySelectorAll("img"));
      const clonedImages = Array.from(clonedArticle.querySelectorAll("img"));
      let inlined = 0;
      let failed = 0;

      for (let index = 0; index < clonedImages.length; index += 1) {
        const clonedImg = clonedImages[index];
        const sourceImg = sourceImages[index];
        const src = (clonedImg.getAttribute("src") || "").trim();
        if (!src) continue;
        if (/^data:image\//i.test(src)) {
          inlined += 1;
          continue;
        }

        try {
          const dataUrl = await fetchImageAsDataUrl(src);
          clonedImg.setAttribute("src", dataUrl);
          inlined += 1;
          continue;
        } catch (fetchError) {
          try {
            if (!sourceImg) throw fetchError;
            const dataUrl = renderedImageToDataUrl(sourceImg);
            clonedImg.setAttribute("src", dataUrl);
            inlined += 1;
          } catch (canvasError) {
            failed += 1;
          }
        }
      }

      return { inlined, failed, total: clonedImages.length };
    }

    // ========== 编辑模式逻辑 (Edit Mode Logic) ==========
    let isEditing = false;
    let currentEditingNode = null;
    let undoStack = [];
    const storageKey = 'wechat_article_' + location.pathname;
    const themeStorageKey = 'wechat_theme_' + location.pathname;
    
    function saveState() {
      const article = document.getElementById('wechatArticle');
      if (!article) return;
      undoStack.push(article.innerHTML);
      if (undoStack.length > 30) undoStack.shift();
    }
    
    function undoOperation() {
      if (undoStack.length > 0) {
        const lastState = undoStack.pop();
        document.getElementById('wechatArticle').innerHTML = lastState;
        currentEditingNode = null;
        saveToStorage();
      }
    }

    function saveToStorage() {
      try {
        const article = document.getElementById('wechatArticle');
        if (!article) return;
        const clone = article.cloneNode(true);
        clone.removeAttribute('contenteditable');
        clone.querySelectorAll('[contenteditable]').forEach(el => {
          el.removeAttribute('contenteditable');
        });
        // 彻底清理掉所有临时生成的悬浮气泡，不将它们持久化到缓存中
        clone.querySelectorAll('.aim-tooltip').forEach(tooltip => {
          tooltip.remove();
        });
        localStorage.setItem(storageKey, clone.innerHTML);
      } catch (e) {
        console.warn('无法保存到 localStorage:', e);
      }
    }

    function resetContent() {
      if (confirm('确定要恢复到初始生成的文章内容吗？所有修改都将丢失。')) {
        try {
          localStorage.removeItem(storageKey);
          localStorage.removeItem(themeStorageKey);
        } catch (e) {
          console.warn('无法清除 localStorage:', e);
        }
        location.reload();
      }
    }

    const editableRoles = ['h1', 'h2', 'h3', 'p', 'li', 'dek', 'quoteText', 'figcaption', 'calloutTitle', 'summaryTitle', 'summaryText', 'eyebrow', 'moduleLabel'];

    function enableEditMode() {
      if (isAnnotating) {
        disableAnnotateMode();
      }
      isEditing = true;
      document.getElementById('toolbarContainer').classList.add('is-editing-mode');
      document.getElementById('toggleEdit').textContent = '完成';
      
      const article = document.getElementById('wechatArticle');
      editableRoles.forEach(role => {
        article.querySelectorAll(`[data-role="${role}"]`).forEach(el => {
          el.setAttribute('contenteditable', 'true');
        });
      });
      article.querySelectorAll('h1:not([data-role]), h2:not([data-role]), h3:not([data-role]), p:not([data-role]), li:not([data-role]), figcaption:not([data-role])').forEach(el => {
        el.setAttribute('contenteditable', 'true');
      });
    }

    function disableEditMode() {
      isEditing = false;
      document.getElementById('toolbarContainer').classList.remove('is-editing-mode');
      document.getElementById('toggleEdit').textContent = '编辑';
      currentEditingNode = null;
      
      const article = document.getElementById('wechatArticle');
      article.querySelectorAll('[contenteditable]').forEach(el => {
        el.removeAttribute('contenteditable');
      });
    }

    function toggleEditMode() {
      if (isEditing) {
        disableEditMode();
      } else {
        enableEditMode();
      }
    }

    // 追踪当前编辑节点
    const articleEl = document.getElementById('wechatArticle');

    articleEl.addEventListener('focusin', function(e) {
      if (isEditing && e.target.hasAttribute('contenteditable')) {
        currentEditingNode = e.target;
      }
    });

    function focusEditableTarget(target) {
      if (!isEditing) return;
      const editable = target.closest && target.closest('[contenteditable="true"]');
      if (!editable || !articleEl.contains(editable)) return;
      currentEditingNode = editable;
      try {
        editable.focus({ preventScroll: true });
      } catch (e) {
        editable.focus();
      }
    }

    articleEl.addEventListener('pointerup', function(e) {
      focusEditableTarget(e.target);
    });

    articleEl.addEventListener('touchend', function(e) {
      const touch = e.changedTouches && e.changedTouches[0];
      if (!touch) return;
      const target = document.elementFromPoint(touch.clientX, touch.clientY);
      if (target) focusEditableTarget(target);
    }, { passive: true });

    // 拦截回车键，防止生成多余标签
    articleEl.addEventListener('keydown', function(e) {
      if (isEditing && e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        insertBlock('after');
      }
    });

    function getCurrentThemeId() {
      return document.getElementById('themePreset').value;
    }

    function changeBlockRole(newRole, tagName) {
      if (!currentEditingNode) return;
      saveState();
      const newNode = document.createElement(tagName);
      newNode.innerHTML = currentEditingNode.innerHTML;
      newNode.setAttribute('data-role', newRole);
      newNode.setAttribute('contenteditable', 'true');
      
      currentEditingNode.replaceWith(newNode);
      currentEditingNode = newNode;
      
      // 重新应用样式
      applyTheme(getCurrentThemeId());
      // 保持焦点
      newNode.focus();
      saveToStorage();
    }

    function insertBlock(position) {
      if (!currentEditingNode) return;
      saveState();
      const newNode = document.createElement('p');
      newNode.setAttribute('data-role', 'p');
      newNode.setAttribute('contenteditable', 'true');
      newNode.innerHTML = '<br>'; // 用于占位，保证可点击
      
      if (position === 'before') {
        currentEditingNode.before(newNode);
      } else {
        currentEditingNode.after(newNode);
      }
      
      applyTheme(getCurrentThemeId());
      newNode.focus();
      saveToStorage();
    }

    function deleteBlock() {
      if (!currentEditingNode) return;
      saveState();
      const parent = currentEditingNode.parentElement;
      currentEditingNode.remove();
      currentEditingNode = null;
      
      // 当容器中没有内容时，删除容器
      if (parent && parent.id !== 'wechatArticle') {
        if (!parent.textContent.trim() && parent.querySelectorAll('img, video, iframe').length === 0) {
          parent.remove();
        }
      }
      saveToStorage();
    }

    // 绑定编辑工具栏按钮
    document.getElementById('toggleEdit').addEventListener('click', toggleEditMode);
    document.getElementById('btnToH1').addEventListener('click', () => changeBlockRole('h1', 'h1'));
    document.getElementById('btnToH2').addEventListener('click', () => changeBlockRole('h2', 'h2'));
    document.getElementById('btnToH3').addEventListener('click', () => changeBlockRole('h3', 'h3'));
    document.getElementById('btnToP').addEventListener('click', () => changeBlockRole('p', 'p'));
    document.getElementById('btnUndo').addEventListener('click', undoOperation);
    document.getElementById('btnReset').addEventListener('click', resetContent);
    document.getElementById('btnInsertBefore').addEventListener('click', () => insertBlock('before'));
    document.getElementById('btnInsertAfter').addEventListener('click', () => insertBlock('after'));
    document.getElementById('btnDeleteBlock').addEventListener('click', deleteBlock);
    
    // 监听输入事件进行自动保存
    articleEl.addEventListener('input', saveToStorage);

    // ========== 批注模式逻辑 (Annotation Mode Logic) ==========
    let isAnnotating = false;
    let savedSelectionRange = null;
    let pendingAnnotationMark = null;
    let annotationSelectionTimer = null;

    function enableAnnotateMode() {
      if (isEditing) {
        disableEditMode();
      }
      isAnnotating = true;
      document.getElementById('toolbarContainer').classList.add('is-annotating-mode');
      document.getElementById('toggleAnnotate').textContent = '完成批注';
      document.getElementById('toggleAnnotate').style.cssText = 'background: #fef08a; border-color: #eab308; color: #854d0e; font-weight: bold;';
    }

    function disableAnnotateMode() {
      isAnnotating = false;
      document.getElementById('toolbarContainer').classList.remove('is-annotating-mode');
      document.getElementById('toggleAnnotate').textContent = '批注';
      document.getElementById('toggleAnnotate').style.cssText = '';
      clearPendingAnnotation();
      hideAnnotationPopup();
    }

    function toggleAnnotateMode() {
      if (isAnnotating) {
        disableAnnotateMode();
      } else {
        enableAnnotateMode();
      }
    }

    function hideAnnotationPopup() {
      document.getElementById('annotationPopup').style.display = 'none';
      document.getElementById('annotationInput').value = '';
      savedSelectionRange = null;
    }

    function unwrapAnnotationMark(mark) {
      const parent = mark.parentNode;
      if (!parent) return;
      while (mark.firstChild) {
        parent.insertBefore(mark.firstChild, mark);
      }
      mark.remove();
      parent.normalize();
    }

    function clearPendingAnnotation() {
      if (pendingAnnotationMark && pendingAnnotationMark.isConnected) {
        unwrapAnnotationMark(pendingAnnotationMark);
        undoStack.pop();
      }
      pendingAnnotationMark = null;
      savedSelectionRange = null;
    }

    function isSelectionInsideArticle(selection) {
      if (!selection || selection.isCollapsed || selection.rangeCount === 0) return false;
      const article = document.getElementById('wechatArticle');
      const range = selection.getRangeAt(0);
      return article.contains(range.commonAncestorContainer);
    }

    function positionAnnotationPopup(anchorEl) {
      const rect = anchorEl.getBoundingClientRect();
      const popup = document.getElementById('annotationPopup');
      const viewportWidth = document.documentElement.clientWidth || window.innerWidth;
      const popupWidth = Math.min(280, Math.max(0, viewportWidth - 24));
      popup.style.display = 'flex';
      popup.style.width = popupWidth + 'px';
      popup.style.top = (window.scrollY + rect.bottom + 10) + 'px';

      let leftPos = window.scrollX + rect.left;
      const minLeft = window.scrollX + 12;
      const maxLeft = window.scrollX + viewportWidth - popupWidth - 12;
      if (leftPos > maxLeft) leftPos = maxLeft;
      if (leftPos < minLeft) leftPos = minLeft;
      popup.style.left = leftPos + 'px';
    }

    function handleAnnotationSelectionEvent(e) {
      if (!isAnnotating) return;
      
      // 不要在弹窗上触发
      if (e.target.closest('#annotationPopup')) return;
      // 不要在工具栏上触发
      if (e.target.closest('#toolbarContainer')) return;
      
      const selection = window.getSelection();
      if (!isSelectionInsideArticle(selection) || selection.toString().trim() === '') {
        return;
      }

      if (pendingAnnotationMark && pendingAnnotationMark.isConnected) {
        return;
      }

      clearPendingAnnotation();

      const range = selection.getRangeAt(0);
      saveState();
      savedSelectionRange = range.cloneRange();

      try {
        const mark = document.createElement('mark');
        mark.className = 'aim-annotation is-pending';
        savedSelectionRange.surroundContents(mark);
        pendingAnnotationMark = mark;
      } catch (err) {
        undoStack.pop();
        pendingAnnotationMark = null;
        savedSelectionRange = null;
        console.warn('批注选区高亮失败，可能由于跨节点选择', err);
        alert('暂不支持跨越多个段落的批注，请仅选择单一节点内的纯文本。');
        return;
      }

      positionAnnotationPopup(pendingAnnotationMark);
      setTimeout(() => document.getElementById('annotationInput').focus(), 50);
    }

    function scheduleAnnotationSelection(e, delay) {
      if (!isAnnotating) return;
      if (annotationSelectionTimer) clearTimeout(annotationSelectionTimer);
      annotationSelectionTimer = setTimeout(() => {
        annotationSelectionTimer = null;
        handleAnnotationSelectionEvent(e);
      }, delay);
    }

    articleEl.addEventListener('mouseup', function(e) {
      scheduleAnnotationSelection(e, 0);
    });

    articleEl.addEventListener('pointerup', function(e) {
      scheduleAnnotationSelection(e, 80);
    });

    articleEl.addEventListener('touchend', function(e) {
      const touch = e.changedTouches && e.changedTouches[0];
      const target = touch ? document.elementFromPoint(touch.clientX, touch.clientY) : e.target;
      const selectionEvent = { target: target || e.target };
      scheduleAnnotationSelection(selectionEvent, 180);
    }, { passive: true });

    document.addEventListener('selectionchange', function() {
      if (!isAnnotating) return;
      const selection = window.getSelection();
      if (!isSelectionInsideArticle(selection)) return;
      scheduleAnnotationSelection({ target: articleEl }, 260);
    });

    document.getElementById('btnCancelAnnotation').addEventListener('click', function() {
      clearPendingAnnotation();
      hideAnnotationPopup();
      window.getSelection().removeAllRanges();
    });

    document.getElementById('btnSaveAnnotation').addEventListener('click', function() {
      const comment = document.getElementById('annotationInput').value.trim();
      if (!comment || !pendingAnnotationMark) return;

      try {
        pendingAnnotationMark.className = 'aim-annotation';
        pendingAnnotationMark.setAttribute('data-comment', comment);
        createTooltip(pendingAnnotationMark);
        pendingAnnotationMark = null;
        saveToStorage();
      } catch (err) {
        console.warn('批注保存失败', err);
        alert('批注保存失败，请重新选择文本后再试。');
      }
      
      hideAnnotationPopup();
      window.getSelection().removeAllRanges();
    });

    // 创建批注悬浮气泡及其关闭与二次确认按钮
    function createTooltip(mark) {
      // 移除已有的临时气泡以确保升级和缓存兼容性
      const existing = mark.querySelector('.aim-tooltip');
      if (existing) existing.remove();

      const comment = mark.getAttribute('data-comment');
      if (!comment) return;

      const tooltip = document.createElement('span');
      tooltip.className = 'aim-tooltip';
      tooltip.setAttribute('contenteditable', 'false');

      const content = document.createElement('span');
      content.className = 'aim-tooltip-content';
      content.textContent = comment;

      const delBtn = document.createElement('span');
      delBtn.className = 'aim-tooltip-delete';
      delBtn.innerHTML = '&times;';
      delBtn.title = '删除此批注';

      const confirmSpan = document.createElement('span');
      confirmSpan.className = 'aim-tooltip-confirm';
      confirmSpan.style.display = 'none';
      confirmSpan.innerHTML = '确定删除？ <span class="aim-confirm-yes" style="color: #ef4444; font-weight: bold; cursor: pointer; margin-right: 6px; margin-left: 4px;">是</span><span class="aim-confirm-no" style="color: #64748b; font-weight: bold; cursor: pointer;">否</span>';

      tooltip.appendChild(content);
      tooltip.appendChild(delBtn);
      tooltip.appendChild(confirmSpan);
      mark.appendChild(tooltip);
    }

    // 事件委托：处理批注删除按钮及二次确认的点击
    document.getElementById('wechatArticle').addEventListener('click', function(e) {
      // 1. 点击删除图标
      const delBtn = e.target.closest('.aim-tooltip-delete');
      if (delBtn) {
        e.stopPropagation();
        e.preventDefault();
        const tooltip = delBtn.closest('.aim-tooltip');
        if (tooltip) {
          const content = tooltip.querySelector('.aim-tooltip-content');
          const confirmSpan = tooltip.querySelector('.aim-tooltip-confirm');
          if (content && confirmSpan) {
            content.style.display = 'none';
            delBtn.style.display = 'none';
            confirmSpan.style.display = 'inline';
          }
        }
        return;
      }

      // 2. 点击取消删除
      const noBtn = e.target.closest('.aim-confirm-no');
      if (noBtn) {
        e.stopPropagation();
        e.preventDefault();
        const tooltip = noBtn.closest('.aim-tooltip');
        if (tooltip) {
          const content = tooltip.querySelector('.aim-tooltip-content');
          const delBtn = tooltip.querySelector('.aim-tooltip-delete');
          const confirmSpan = tooltip.querySelector('.aim-tooltip-confirm');
          if (content && delBtn && confirmSpan) {
            confirmSpan.style.display = 'none';
            content.style.display = 'inline';
            delBtn.style.display = 'inline';
          }
        }
        return;
      }

      // 3. 点击确认删除
      const yesBtn = e.target.closest('.aim-confirm-yes');
      if (yesBtn) {
        e.stopPropagation();
        e.preventDefault();
        const mark = yesBtn.closest('.aim-annotation');
        if (mark) {
          saveState();
          const clone = mark.cloneNode(true);
          const t = clone.querySelector('.aim-tooltip');
          if (t) t.remove();
          const textNode = document.createTextNode(clone.textContent);
          mark.parentNode.replaceChild(textNode, mark);
          saveToStorage();
        }
      }
    });

    async function copyAnnotations() {
      const status = document.querySelector("#copyStatus");
      const marks = document.querySelectorAll('.aim-annotation');
      if (marks.length === 0) {
        if (status) status.textContent = "无批注";
        setTimeout(() => { if (status) status.textContent = ""; }, 3000);
        return;
      }
      
      let markdown = "# 文章批注列表\n\n";
      marks.forEach((mark, index) => {
        const comment = mark.getAttribute('data-comment');
        
        const cleanMark = mark.cloneNode(true);
        const tooltip = cleanMark.querySelector('.aim-tooltip');
        if (tooltip) tooltip.remove();
        const text = cleanMark.textContent;
        
        const container = mark.closest('[data-role]') || mark.parentNode;
        
        let contextHtml = '';
        if (container) {
          const clone = container.cloneNode(true);
          // 清理冗余属性，方便丢给大模型处理（去除 style, contenteditable 等）
          clone.removeAttribute('contenteditable');
          clone.removeAttribute('style');
          clone.querySelectorAll('*').forEach(el => {
            el.removeAttribute('contenteditable');
            el.removeAttribute('style');
          });
          // 进一步精简 mark 标签，去除 class，并移除内部的 tooltip 气泡
          clone.querySelectorAll('mark.aim-annotation').forEach(el => {
            el.removeAttribute('class');
            const t = el.querySelector('.aim-tooltip');
            if (t) t.remove();
          });
          contextHtml = clone.outerHTML;
        }
        
        markdown += `## 批注 ${index + 1}\n`;
        markdown += `- **原文选段**：\`${text}\`\n`;
        markdown += `- **修改意见**：${comment}\n`;
        markdown += `- **上下文HTML**：\n\`\`\`html\n${contextHtml}\n\`\`\`\n\n`;
      });
      
      try {
        if (navigator.clipboard) {
          await navigator.clipboard.writeText(markdown);
          if (status) status.textContent = "批注已复制";
        }
      } catch (e) {
        if (status) status.textContent = "复制失败";
      }
      
      if (copyTimeout) clearTimeout(copyTimeout);
      copyTimeout = setTimeout(() => {
        if (status) status.textContent = "";
      }, 3000);
    }

    document.getElementById('toggleAnnotate').addEventListener('click', toggleAnnotateMode);
    document.getElementById('copyAnnotations').addEventListener('click', copyAnnotations);

    // ====================================================

    let copyTimeout = null;
    async function copyArticle() {
      const status = document.querySelector("#copyStatus");
      const article = document.querySelector("#wechatArticle");
      status.textContent = "正在处理图片...";
      if (copyTimeout) clearTimeout(copyTimeout);
      
      const clonedArticle = article.cloneNode(true);
      
      // 在克隆节点中彻底清理编辑相关的属性
      clonedArticle.removeAttribute('contenteditable');
      clonedArticle.querySelectorAll('[contenteditable]').forEach(el => {
        el.removeAttribute('contenteditable');
      });

      // 清理掉所有的批注标签，将其替换为纯文本，防止复制正文时把批注也带入到微信或剪贴板中
      clonedArticle.querySelectorAll('.aim-annotation').forEach(mark => {
        const tooltip = mark.querySelector('.aim-tooltip');
        if (tooltip) tooltip.remove();
        const textNode = document.createTextNode(mark.textContent);
        mark.parentNode.replaceChild(textNode, mark);
      });

      // 将 h1, h2, h3 转换为 p 标签，防止复制到微信后台后被微信默认样式重置并放大字号
      clonedArticle.querySelectorAll('h1, h2, h3').forEach(heading => {
        const p = document.createElement('p');
        p.innerHTML = heading.innerHTML;
        for (let attr of heading.attributes) {
          p.setAttribute(attr.name, attr.value);
        }
        heading.parentNode.replaceChild(p, heading);
      });

      const imageResult = await inlineImagesForCopy(article, clonedArticle);
      const articleStyle = clonedArticle.getAttribute('style') || '';
      const html = `<section style="${articleStyle}">${clonedArticle.innerHTML}</section>`;
      const text = article.innerText;
      
      try {
        if (navigator.clipboard && window.ClipboardItem) {
          const item = new ClipboardItem({
            "text/html": new Blob([html], { type: "text/html" }),
            "text/plain": new Blob([text], { type: "text/plain" })
          });
          await navigator.clipboard.write([item]);
          status.textContent = "已复制";
          copyTimeout = setTimeout(() => {
            status.textContent = "";
          }, 3000);
          return;
        }
        if (navigator.clipboard) {
          await navigator.clipboard.writeText(text);
          status.textContent = "已复制";
          copyTimeout = setTimeout(() => {
            status.textContent = "";
          }, 3000);
          return;
        }
        status.textContent = "请选择正文后手动复制";
      } catch (error) {
        status.textContent = "复制失败，请手动选择正文";
      }
    }

    document.querySelector("#themePreset").addEventListener("change", event => {
      const themeVal = event.target.value;
      applyTheme(themeVal);
      try {
        localStorage.setItem(themeStorageKey, themeVal);
      } catch (e) {
        console.warn('无法保存主题设置:', e);
      }
      const status = document.querySelector("#copyStatus");
      status.textContent = "主题已切换";
      if (copyTimeout) clearTimeout(copyTimeout);
      copyTimeout = setTimeout(() => {
        status.textContent = "";
      }, 3000);
    });
    document.querySelector("#copyWechat").addEventListener("click", copyArticle);
    
    // 初始化加载缓存数据与主题，并检测内容是否变更以使缓存失效
    try {
      const currentOriginalHTML = document.getElementById('wechatArticle').innerHTML;
      
      // 简单且高效的 String Hash 函数
      function getHtmlHash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
          hash = (hash << 5) - hash + str.charCodeAt(i);
          hash |= 0;
        }
        return String(hash);
      }
      
      const currentHash = getHtmlHash(currentOriginalHTML);
      const savedHashKey = storageKey + '_hash';
      const savedHash = localStorage.getItem(savedHashKey);
      const savedHTML = localStorage.getItem(storageKey);
      
      if (savedHash === currentHash && savedHTML) {
        // 如果文件没有被重新生成（Hash相同），且存在修改缓存，则应用缓存
        document.getElementById('wechatArticle').innerHTML = savedHTML;
      } else {
        // 如果文件已更新（Hash不同）或无缓存，使用新内容并更新 Hash 缓存
        localStorage.setItem(savedHashKey, currentHash);
        localStorage.removeItem(storageKey);
      }
    } catch (e) {
      console.warn('无法加载缓存内容:', e);
    }

    try {
      document.querySelectorAll('.aim-annotation').forEach(createTooltip);
    } catch (e) {
      console.warn('无法初始化批注气泡:', e);
    }

    try {
      const savedTheme = localStorage.getItem(themeStorageKey);
      if (savedTheme) {
        document.getElementById('themePreset').value = savedTheme;
        applyTheme(savedTheme);
      } else {
        applyTheme("warm-editorial");
      }
    } catch (e) {
      applyTheme("warm-editorial");
    }
