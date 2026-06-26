app.displayDialogs = DialogModes.NO;

function fail(message) {
  throw new Error(message);
}

// Replace every Unicode whitespace variant with an ASCII space.
// Covers NBSP (U+00A0), ideographic space (U+3000), various en/em/thin spaces,
// zero-width spaces, and the BOM character that sometimes leaks into layer names.
function normalizeUnicodeSpaces(name) {
  return String(name).replace(/[\u00A0\u1680\u2000-\u200B\u202F\u205F\u3000\uFEFF]/g, " ");
}

// Normalize full-width symbols that are visually identical to ASCII counterparts
// but have different code points (e.g. ￥ U+FFE5 vs ¥ U+00A5).
function normalizeFullWidth(name) {
  var s = String(name);
  // Full-width ASCII block U+FF01..U+FF5E → half-width U+0021..U+007E
  s = s.replace(/[\uFF01-\uFF5E]/g, function(c) {
    return String.fromCharCode(c.charCodeAt(0) - 0xFEE0);
  });
  // Full-width yen ￥ → ¥
  s = s.replace(/\uFFE5/g, "\u00A5");
  return s;
}

function trimSpaces(name) {
  return String(name).replace(/^\s+|\s+$/g, "");
}

function collapseSpaces(name) {
  return String(name).replace(/\s+/g, " ").replace(/^\s+|\s+$/g, "");
}

function stripAllSpaces(name) {
  return String(name).replace(/\s/g, "");
}

// Build a multi-level normalized key for a layer name.
// Returns an array of candidate keys in descending precision order.
function layerKeys(name) {
  var s = normalizeUnicodeSpaces(normalizeFullWidth(String(name)));
  return [
    String(name),             // 0: exact
    trimSpaces(s),            // 1: unicode-normalized + trimmed
    collapseSpaces(s),        // 2: collapsed spaces
    trimSpaces(String(name)), // 3: trim only (original, no full-width remap)
    stripAllSpaces(s),        // 4: strip all whitespace (last resort)
  ];
}

// Multi-level fuzzy layer search.
// Returns { layer, level } where level 0 = exact, 4 = strip-all-whitespace.
function findTextLayerFuzzy(parent, name, best) {
  var reqKeys = layerKeys(name);
  if (!best) { best = { layer: null, level: 999 }; }
  for (var i = 0; i < parent.layers.length; i++) {
    var layer = parent.layers[i];
    if (layer.typename === "ArtLayer" && layer.kind === LayerKind.TEXT) {
      var candidateKeys = layerKeys(String(layer.name));
      for (var level = 0; level < reqKeys.length; level++) {
        if (level >= best.level) break; // already have a better match
        if (reqKeys[level] === candidateKeys[level]) {
          best.layer = layer;
          best.level = level;
          if (level === 0) return best; // exact — stop immediately
          break;
        }
      }
    }
    if (layer.typename === "LayerSet") {
      findTextLayerFuzzy(layer, name, best);
      if (best.level === 0) return best;
    }
  }
  return best;
}

function findTextLayer(parent, name) {
  var result = findTextLayerFuzzy(parent, name, null);
  return result.layer;
}

function listTextLayers(parent, out) {
  for (var i = 0; i < parent.layers.length; i++) {
    var layer = parent.layers[i];
    if (layer.typename === "ArtLayer" && layer.kind === LayerKind.TEXT) {
      out.push(String(layer.name));
    }
    if (layer.typename === "LayerSet") {
      listTextLayers(layer, out);
    }
  }
}

var inputPath = "__INPUT_PATH__";
var layerName = "__LAYER_NAME__";
var newText = "__NEW_TEXT__";
var outputPath = "__OUTPUT_PATH__";
var styleLock = "__STYLE_LOCK__" !== "false";
var inputPathLower = String(inputPath).toLowerCase();
var outputPathLower = String(outputPath).toLowerCase();
var saveInPlace = inputPathLower === outputPathLower;

var inputFile = new File(inputPath);
if (!inputFile.exists) {
  fail("E_FILE_NOT_FOUND: " + inputPath);
}

var doc = app.open(inputFile);
try {
  var layer = findTextLayer(doc, layerName);
  if (!layer) {
    var available = [];
    listTextLayers(doc, available);
    fail("E_LAYER_NOT_FOUND: " + layerName + " | AVAILABLE_LAYERS: " + available.join(", "));
  }

  var textItem = layer.textItem;
  var beforeText = textItem.contents;
  var beforeFont = String(textItem.font);
  var beforeSize = String(textItem.size);

  textItem.contents = newText;

  var afterFont = String(textItem.font);
  var afterSize = String(textItem.size);
  if (styleLock && (beforeFont !== afterFont || beforeSize !== afterSize)) {
    textItem.contents = beforeText;
    fail("E_STYLE_MISMATCH: font/size changed unexpectedly");
  }

  if (saveInPlace || /\.psb$/i.test(outputPathLower)) {
    // Keep large documents as PSB; avoid saveAs PSD 2GB limit.
    doc.save();
  } else {
    var outFile = new File(outputPath);
    var saveOpts = new PhotoshopSaveOptions();
    doc.saveAs(outFile, saveOpts, true, Extension.LOWERCASE);
  }
  doc.close(SaveOptions.DONOTSAVECHANGES);
} catch (e) {
  try {
    doc.close(SaveOptions.DONOTSAVECHANGES);
  } catch (_ignored) {}
  fail(String(e && e.message ? e.message : e));
}
