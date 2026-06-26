
(function () {
  function num(value, fallback) {
    var parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  function clipRange(element) {
    var start = num(element.dataset.start, 0);
    var duration = element.dataset.duration == null ? Infinity : num(element.dataset.duration, Infinity);
    return { start: start, duration: duration, end: start + duration };
  }

  function activeCaption(captions, time) {
    for (var i = 0; i < captions.length; i += 1) {
      var item = captions[i];
      if (time >= num(item.start, 0) && time < num(item.end, 0)) return item;
    }
    return null;
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function ease(value) {
    value = clamp(value, 0, 1);
    return 1 - Math.pow(1 - value, 3);
  }

  function applyTimeline() {
    var items = (window.__senseframes && window.__senseframes.timeline && window.__senseframes.timeline.items) || [];
    items.forEach(function (item) {
      var selector = item.selector || (item.id ? '[data-timeline-id="' + item.id + '"], [data-scene="' + item.id + '"]' : "");
      if (!selector) return;
      document.querySelectorAll(selector).forEach(function (element) {
        if (item.start != null) element.dataset.start = String(item.start);
        if (item.end != null && item.start != null) element.dataset.duration = String(Number(item.end) - Number(item.start));
        if (item.duration != null) element.dataset.duration = String(item.duration);
        if (item.effect) element.dataset.effect = item.effect;
        if (item.easing) element.dataset.easing = item.easing;
      });
    });
  }

  function applyEffect(element, time) {
    var effect = element.dataset.effect;
    if (!effect) return;
    var range = clipRange(element);
    var progress = ease((time - range.start) / Math.max(0.001, Math.min(1.2, range.duration || 1)));
    var exitProgress = ease((range.end - time) / Math.max(0.001, Math.min(1.0, range.duration || 1)));
    var opacity = Math.min(progress, exitProgress);
    var transform = "";
    if (effect === "fade-up") transform = "translateY(" + ((1 - progress) * 28).toFixed(2) + "px)";
    else if (effect === "slide-left") transform = "translateX(" + ((1 - progress) * 44).toFixed(2) + "px)";
    else if (effect === "zoom-in") transform = "scale(" + (0.94 + progress * 0.06).toFixed(4) + ")";
    else if (effect === "spotlight") transform = "scale(" + (0.985 + progress * 0.015).toFixed(4) + ")";
    else if (effect === "parallax") transform = "translate3d(" + ((0.5 - progress) * 30).toFixed(2) + "px," + ((1 - progress) * 18).toFixed(2) + "px,0)";
    element.style.opacity = String(clamp(opacity, 0, 1));
    if (transform) element.style.transform = transform;
  }

  function renderCaption(element, caption, time) {
    if (!caption) {
      element.textContent = "";
      element.dataset.sfActive = "false";
      return;
    }
    if (Array.isArray(caption.words) && caption.words.length) {
      element.textContent = "";
      caption.words.forEach(function (word) {
        var span = document.createElement("span");
        var active = time >= num(word.start, caption.start) && time < num(word.end, caption.end);
        var emphasis = /senseaudio|audio|视频|生成|克隆|音色|旁白|搜索/i.test(String(word.text || ""));
        var wordProgress = clamp((time - num(word.start, caption.start)) / Math.max(0.001, num(word.end, caption.end) - num(word.start, caption.start)), 0, 1);
        var pop = Math.sin(wordProgress * Math.PI);
        var scale = active ? (emphasis ? 1.14 : 1.07) + pop * (emphasis ? 0.08 : 0.04) : 1;
        span.className = "sf-word";
        if (emphasis) span.className += " sf-word-emphasis";
        span.dataset.sfActive = active ? "true" : "false";
        span.dataset.sfEmphasis = emphasis ? "true" : "false";
        span.style.transform = "scale(" + scale.toFixed(3) + ")";
        span.style.filter = active && emphasis ? "drop-shadow(0 0 12px rgba(255,214,140,.45))" : "none";
        span.textContent = word.text;
        element.appendChild(span);
      });
    } else {
      element.textContent = caption.text;
    }
    element.dataset.sfActive = "true";
  }

  function seekTimelines(time) {
    var timelines = window.__timelines || {};
    Object.keys(timelines).forEach(function (key) {
      var timeline = timelines[key];
      if (timeline && typeof timeline.seek === "function") {
        timeline.seek(time);
      }
    });
  }

  window.__senseframes = {
    time: 0,
    captions: [],
    timeline: null,
    audioData: null,
    apply: function (time) {
      document.documentElement.style.setProperty("--sf-time", String(time));
      document.documentElement.dataset.sfTime = String(time);
      var clips = document.querySelectorAll("[data-start], [data-scene]");
      clips.forEach(function (element) {
        var range = clipRange(element);
        var active = time >= range.start && time < range.end;
        if (element.dataset.compositionId && !element.dataset.compositionSrc) active = true;
        element.dataset.sfActive = active ? "true" : "false";
        if (element.dataset.scene != null) element.dataset.sceneActive = active ? "true" : "false";
        if (element.dataset.enter && active) element.dataset.sfEnter = element.dataset.enter;
        if (element.dataset.exit && !active) element.dataset.sfExit = element.dataset.exit;
        applyEffect(element, time);
        if (element.classList.contains("clip") || element.matches("video,audio,img,[data-duration]")) {
          element.style.visibility = active ? "visible" : "hidden";
        }
        if (active && (element.tagName === "VIDEO" || element.tagName === "AUDIO")) {
          try {
            element.pause();
            element.currentTime = Math.max(0, time - range.start + num(element.dataset.mediaStart, 0));
          } catch (_) {}
        }
      });
      document.querySelectorAll("[data-caption-source], [data-caption-target]").forEach(function (element) {
        var caption = activeCaption(window.__senseframes.captions || [], time);
        renderCaption(element, caption, time);
      });
      seekTimelines(time);
      if (typeof window.renderFrame === "function") window.renderFrame(time);
      window.dispatchEvent(new CustomEvent("sf-seek", { detail: { time: time } }));
    },
  };

  var params = new URLSearchParams(location.search);
  var time = num(params.get("t"), 0);
  window.__senseframes.time = time;
  window.addEventListener("load", function () {
    var captionElement = document.querySelector("[data-caption-source]");
    var source = captionElement && captionElement.dataset.captionSource;
    var timelineElement = document.querySelector("[data-timeline-source]");
    var timelineSource = timelineElement && timelineElement.dataset.timelineSource;
    var audioElement = document.querySelector("[data-audio-source]");
    var audioSource = audioElement && audioElement.dataset.audioSource;
    var ready = Promise.resolve();
    if (Array.isArray(window.__sfCaptions)) {
      window.__senseframes.captions = window.__sfCaptions;
    } else if (source) {
      ready = fetch(source).then(function (response) { return response.json(); }).then(function (data) {
        window.__senseframes.captions = Array.isArray(data) ? data : (data.captions || []);
      }).catch(function () {
        window.__senseframes.captions = [];
      });
    }
    if (timelineSource) {
      ready = ready.then(function () {
        return fetch(timelineSource).then(function (response) { return response.json(); }).then(function (data) {
          window.__senseframes.timeline = data;
          applyTimeline();
        }).catch(function () {
          window.__senseframes.timeline = null;
        });
      });
    }
    if (audioSource) {
      ready = ready.then(function () {
        return fetch(audioSource).then(function (response) { return response.json(); }).then(function (data) {
          window.__senseframes.audioData = data;
        }).catch(function () {
          window.__senseframes.audioData = null;
        });
      });
    }
    ready.then(function () {
      window.__senseframes.apply(time);
      window.__sfReady = true;
    });
  });
})();
