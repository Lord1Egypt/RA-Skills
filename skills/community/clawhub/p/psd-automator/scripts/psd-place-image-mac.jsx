// Place an image file into an open PSD as an embedded Smart Object layer.
// Template placeholders are substituted by psd-place-image-mac.applescript.
app.displayDialogs = DialogModes.NO;

function fail(message) {
  throw new Error(message);
}

var inputPath = "__INPUT_PATH__";
var imagePath = "__IMAGE_PATH__";
var layerLabel = "__LAYER_LABEL__";      // optional: rename the placed layer
var position = "__POSITION__";           // "top" | "bottom" | "" (leave in place)
var visible = "__VISIBLE__" !== "false";
var targetArtboard = "__TARGET_ARTBOARD__"; // optional: move placed layer into this LayerSet
var outputPath = "__OUTPUT_PATH__";

var inputFile = new File(inputPath);
if (!inputFile.exists) {
  fail("E_FILE_NOT_FOUND: " + inputPath);
}

var imageFile = new File(imagePath);
if (!imageFile.exists) {
  fail("E_IMAGE_NOT_FOUND: " + imagePath);
}

var doc = app.open(inputFile);
try {
  app.activeDocument = doc;

  // Place image as an embedded Smart Object via Photoshop action descriptor.
  // FTcs/Qcsa = "Fit to Canvas" – centers and scales to fit within document bounds.
  var idPlc = charIDToTypeID("Plc ");
  var desc = new ActionDescriptor();
  desc.putPath(charIDToTypeID("null"), imageFile);
  desc.putBoolean(stringIDToTypeID("linked"), false);
  desc.putEnumerated(charIDToTypeID("FTcs"), charIDToTypeID("QCSt"), charIDToTypeID("Qcsa"));
  executeAction(idPlc, desc, DialogModes.NO);

  var placedLayer = doc.activeLayer;

  // Rename the placed layer if a label was provided.
  var labelTrimmed = String(layerLabel).replace(/^\s+|\s+$/g, "");
  if (labelTrimmed !== "" && labelTrimmed !== "__LAYER_LABEL__") {
    placedLayer.name = labelTrimmed;
  }

  // Set visibility.
  placedLayer.visible = visible;

  // Move into a specific artboard (LayerSet) if requested.
  var targetLabel = String(targetArtboard).replace(/^\s+|\s+$/g, "");
  if (targetLabel !== "" && targetLabel !== "__TARGET_ARTBOARD__") {
    var targetSet = null;
    for (var si = 0; si < doc.layers.length; si++) {
      if (doc.layers[si].typename === "LayerSet" && doc.layers[si].name === targetLabel) {
        targetSet = doc.layers[si];
        break;
      }
    }
    if (targetSet) {
      // Move the placed layer to the top of the target artboard's layer stack.
      placedLayer.move(targetSet, ElementPlacement.PLACEATBEGINNING);
    } else {
      // Artboard not found by exact name — fall through to document-level positioning.
    }
  }

  // Document-level position (applied when no artboard target or artboard not found).
  if (!targetLabel || targetLabel === "__TARGET_ARTBOARD__") {
    if (position === "top" || position === "") {
      placedLayer.move(doc, ElementPlacement.PLACEATBEGINNING);
    } else if (position === "bottom") {
      placedLayer.move(doc, ElementPlacement.PLACEATEND);
    }
  }

  // Save — use in-place save for PSB or when input/output paths are the same.
  var outputLower = String(outputPath).toLowerCase();
  var inputLower = String(inputPath).toLowerCase();
  if (inputLower === outputLower || /\.psb$/i.test(outputLower)) {
    doc.save();
  } else {
    var outFile = new File(outputPath);
    var saveOpts = new PhotoshopSaveOptions();
    doc.saveAs(outFile, saveOpts, true, Extension.LOWERCASE);
  }
  doc.close(SaveOptions.DONOTSAVECHANGES);
} catch (e) {
  try { doc.close(SaveOptions.DONOTSAVECHANGES); } catch (_ignored) {}
  fail(String(e && e.message ? e.message : e));
}
