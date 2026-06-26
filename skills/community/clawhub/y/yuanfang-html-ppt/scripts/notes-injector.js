// notes-injector.js — post-process dom-to-pptx output to fill in speaker notes
//
// dom-to-pptx already creates empty notesSlideN.xml files for each slide.
// This module reads those, injects the actual notes text from the slide data,
// and writes the zip back. No-op if a slide has no notes.

'use strict';

function xmlEscape(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function buildParagraphs(text) {
  const lines = String(text).split(/\r?\n/);
  return lines.map(line => {
    const safe = xmlEscape(line);
    return `<a:p><a:r><a:rPr lang="en-US" dirty="0"/><a:t>${safe}</a:t></a:r><a:endParaRPr lang="en-US" dirty="0"/></a:p>`;
  }).join('');
}

function injectNotes(pptxBuffer, notesBySlideIndex) {
  if (!notesBySlideIndex || Object.keys(notesBySlideIndex).length === 0) {
    return Promise.resolve(pptxBuffer);
  }
  const JSZip = require('jszip');
  return JSZip.loadAsync(pptxBuffer).then(async (zip) => {
    const notesSlideNames = Object.keys(zip.files)
      .filter(n => /^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(n))
      .sort((a, b) => {
        const na = parseInt(a.match(/(\d+)\.xml$/)[1], 10);
        const nb = parseInt(b.match(/(\d+)\.xml$/)[1], 10);
        return na - nb;
      });

    for (const fileName of notesSlideNames) {
      const slideNum = fileName.match(/notesSlide(\d+)\.xml$/)[1];
      const notes = notesBySlideIndex[slideNum];
      if (!notes || !notes.trim()) continue;
      const xml = await zip.file(fileName).async('string');
      const newParas = buildParagraphs(notes);
      const newXml = xml.replace(
        /<a:p><a:r><a:rPr lang="en-US" dirty="0"\/><a:t><\/a:t><\/a:r><a:endParaRPr lang="en-US" dirty="0"\/><\/a:p>/,
        newParas
      );
      if (newXml !== xml) {
        zip.file(fileName, newXml);
      }
    }
    return zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' });
  });
}

module.exports = { injectNotes, buildParagraphs, xmlEscape };
