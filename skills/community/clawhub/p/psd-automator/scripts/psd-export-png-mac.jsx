app.displayDialogs = DialogModes.NO;

function fail(message) {
  throw new Error(message);
}

var inputPath = "__INPUT_PATH__";
var pngPath = "__PNG_PATH__";
var exportMode = "__EXPORT_MODE__";
var pngDir = "__PNG_DIR__";
var artboardName = "__ARTBOARD_NAME__"; // if set, export only this named LayerSet

function sanitizeFileName(name) {
  var value = String(name || "");
  value = value.replace(/[\\\/:\*\?"<>\|]/g, "_");
  value = value.replace(/^\s+|\s+$/g, "");
  return value || "layer";
}

function makeSaveForWebPngOptions() {
  var opts = new ExportOptionsSaveForWeb();
  opts.format = SaveDocumentType.PNG;
  opts.PNG8 = false;
  opts.transparency = true;
  opts.interlaced = false;
  opts.optimized = true;
  try {
    opts.includeProfile = false;
  } catch (_ignored) {}
  return opts;
}

// Export all top-level LayerSets as individual PNG files.
function exportLayerSetsAsPng(doc, outputDirPath) {
  var outDir = new Folder(outputDirPath);
  if (!outDir.exists) {
    outDir.create();
  }

  var topLayers = [];
  var visibility = [];
  for (var i = 0; i < doc.layers.length; i++) {
    topLayers.push(doc.layers[i]);
    visibility.push(doc.layers[i].visible);
    doc.layers[i].visible = false;
  }

  var opts = makeSaveForWebPngOptions();
  var exported = 0;
  try {
    for (var j = 0; j < topLayers.length; j++) {
      var layer = topLayers[j];
      if (layer.typename !== "LayerSet") {
        continue;
      }
      layer.visible = true;
      var fileName = sanitizeFileName(layer.name) + ".png";
      var outFile = new File(outputDirPath + "/" + fileName);
      doc.exportDocument(outFile, ExportType.SAVEFORWEB, opts);
      layer.visible = false;
      exported += 1;
    }
  } finally {
    for (var k = 0; k < topLayers.length; k++) {
      topLayers[k].visible = visibility[k];
    }
  }

  if (exported === 0) {
    fail("E_EXPORT_FAILED: no LayerSet found for layer_sets export");
  }
}

// Export a single named artboard as a PNG at the artboard's exact pixel bounds.
//
// Root-cause note: "exportDocumentAs" (Action Manager) does NOT restrict the
// export canvas to the artboard's bounds — it exports the full document canvas
// regardless of which layer is active, and succeeds silently, so any try/catch
// fallback is never reached.  The reliable approach is to:
//
//  1. Read the artboard's rectangle from doc.artboards[i].artboardRect — this is
//     the canonical pixel coordinate data PS uses internally when you choose
//     "File > Export > Export As" and select an artboard.
//  2. Duplicate the document so the original is never modified.
//  3. In the duplicate hide all sibling artboards, then crop to the artboard
//     rectangle using UnitValue objects.  Passing UnitValues (not raw numbers)
//     means PS resolves units natively, giving the same precision as its own
//     artboard export UI path.
//  4. Export the cropped duplicate via Save-for-Web PNG (lossless, transparency).
//  5. Close the duplicate without saving.
function exportSingleArtboardAsPng(doc, targetName, outputDirPath) {
  var outDir = new Folder(outputDirPath);
  if (!outDir.exists) {
    outDir.create();
  }

  // Locate the artboard LayerSet by name.
  var targetLayer = null;
  for (var i = 0; i < doc.layers.length; i++) {
    if (doc.layers[i].typename === "LayerSet" && doc.layers[i].name === targetName) {
      targetLayer = doc.layers[i];
      break;
    }
  }
  if (!targetLayer) {
    fail("E_EXPORT_FAILED: artboard not found: " + targetName);
  }

  // ── Read artboard bounds from PS's native artboard collection ─────────────
  // doc.artboards[i].artboardRect is the definitive [left, top, right, bottom]
  // pixel rectangle PS uses for all artboard-aware operations.
  // Falls back to targetLayer.bounds (already a UnitValue array) for PS versions
  // that don't expose doc.artboards, or for plain LayerSets.
  var artboardBounds = null;
  try {
    var artboardCollection = doc.artboards;
    if (artboardCollection && artboardCollection.length > 0) {
      for (var a = 0; a < artboardCollection.length; a++) {
        if (artboardCollection[a].name === targetName) {
          // artboardRect: [left, top, right, bottom] in document pixel coords.
          var r = artboardCollection[a].artboardRect;
          // r may be a plain Array or an object with left/top/right/bottom keys.
          var rx1, ry1, rx2, ry2;
          try {
            rx1 = Number(r[0]); ry1 = Number(r[1]);
            rx2 = Number(r[2]); ry2 = Number(r[3]);
          } catch (_eIdx) {
            rx1 = Number(r.left); ry1 = Number(r.top);
            rx2 = Number(r.right); ry2 = Number(r.bottom);
          }
          artboardBounds = [
            new UnitValue(rx1, "px"),
            new UnitValue(ry1, "px"),
            new UnitValue(rx2, "px"),
            new UnitValue(ry2, "px"),
          ];
          break;
        }
      }
    }
  } catch (_eArtboards) {
    // doc.artboards unavailable; fall through to LayerSet.bounds.
  }
  if (!artboardBounds) {
    // targetLayer.bounds is already [left, top, right, bottom] as UnitValues.
    artboardBounds = targetLayer.bounds;
  }

  // ── Duplicate → isolate artboard → crop to exact bounds → export ──────────
  var dupDoc = doc.duplicate("__artboard_export__", false);
  app.activeDocument = dupDoc;
  try {
    // Hide every top-level layer except the target artboard so sibling artboard
    // content doesn't appear in the exported PNG.
    for (var j = 0; j < dupDoc.layers.length; j++) {
      dupDoc.layers[j].visible = (dupDoc.layers[j].name === targetName);
    }

    // Crop to the artboard's own pixel rectangle.  UnitValue objects let PS
    // resolve the units exactly as it does internally for artboard export.
    dupDoc.crop(artboardBounds);

    var opts = makeSaveForWebPngOptions();
    var fileName = sanitizeFileName(targetName) + ".png";
    var outFile = new File(outputDirPath + "/" + fileName);
    dupDoc.exportDocument(outFile, ExportType.SAVEFORWEB, opts);
  } finally {
    dupDoc.close(SaveOptions.DONOTSAVECHANGES);
    app.activeDocument = doc;
  }
}

var inputFile = new File(inputPath);
if (!inputFile.exists) {
  fail("E_FILE_NOT_FOUND: " + inputPath);
}

function hasLayerSets(doc) {
  for (var i = 0; i < doc.layers.length; i++) {
    if (doc.layers[i].typename === "LayerSet") return true;
  }
  return false;
}

var doc = app.open(inputFile);
try {
  var artboardTarget = String(artboardName).replace(/^\s+|\s+$/g, "");
  var useArtboard = artboardTarget !== "" && artboardTarget !== "__ARTBOARD_NAME__";

  if (useArtboard) {
    // Export only the named artboard as a PNG in pngDir.
    var artboardDir = pngDir || String(new File(pngPath).parent.fsName);
    exportSingleArtboardAsPng(doc, artboardTarget, artboardDir);
  } else {
    // Auto-fallback: if layer_sets requested but PSD has no LayerSets, use single.
    var effectiveMode = exportMode;
    if (effectiveMode === "layer_sets" && !hasLayerSets(doc)) {
      effectiveMode = "single";
    }
    if (effectiveMode === "layer_sets") {
      exportLayerSetsAsPng(doc, pngDir);
    } else {
      var outFile = new File(pngPath);
      var opts = new PNGSaveOptions();
      doc.saveAs(outFile, opts, true, Extension.LOWERCASE);
    }
  }
  doc.close(SaveOptions.DONOTSAVECHANGES);
} catch (e) {
  try {
    doc.close(SaveOptions.DONOTSAVECHANGES);
  } catch (_ignored) {}
  fail("E_EXPORT_FAILED: " + String(e && e.message ? e.message : e));
}
