export const SUPPORTED_LAYOUTS = new Set([
  "cover",
  "agenda",
  "section-break",
  "insight",
  "two-column",
  "metrics",
  "chart-focus",
  "timeline",
  "comparison",
  "quote",
  "closing",
]);

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isStringArray(value) {
  return Array.isArray(value) && value.every((item) => typeof item === "string");
}

function isMetricArray(value) {
  return Array.isArray(value) && value.every((item) => item && typeof item === "object" && isNonEmptyString(item.value) && isNonEmptyString(item.label));
}

function isChartArray(value) {
  return Array.isArray(value) && value.every((item) => item && typeof item === "object" && isNonEmptyString(item.label) && Number.isFinite(Number(item.value)));
}

export function validateSlide(slide, index) {
  const errors = [];

  if (!slide || typeof slide !== "object") {
    return [`slides[${index}] must be an object`];
  }

  if (!SUPPORTED_LAYOUTS.has(slide.layout)) {
    errors.push(`slides[${index}].layout must be one of: ${Array.from(SUPPORTED_LAYOUTS).join(", ")}`);
    return errors;
  }

  const requireTitle = !["cover"].includes(slide.layout);
  if (requireTitle && !isNonEmptyString(slide.title)) {
    errors.push(`slides[${index}].title is required for layout "${slide.layout}"`);
  }

  switch (slide.layout) {
    case "agenda":
      if (!isStringArray(slide.points)) errors.push(`slides[${index}].points must be a string array`);
      break;
    case "insight":
      if (!isStringArray(slide.points)) errors.push(`slides[${index}].points must be a string array`);
      break;
    case "two-column":
      if (!isNonEmptyString(slide.leftTitle)) errors.push(`slides[${index}].leftTitle is required`);
      if (!isStringArray(slide.leftPoints)) errors.push(`slides[${index}].leftPoints must be a string array`);
      if (!isNonEmptyString(slide.rightTitle)) errors.push(`slides[${index}].rightTitle is required`);
      if (!isStringArray(slide.rightPoints)) errors.push(`slides[${index}].rightPoints must be a string array`);
      break;
    case "metrics":
      if (!isMetricArray(slide.metrics)) errors.push(`slides[${index}].metrics must be an array of {value,label}`);
      break;
    case "chart-focus":
      if (!isChartArray(slide.chartBars)) errors.push(`slides[${index}].chartBars must be an array of {label,value}`);
      if (!isNonEmptyString(slide.conclusion)) errors.push(`slides[${index}].conclusion is required`);
      break;
    case "timeline":
      if (!isStringArray(slide.steps)) errors.push(`slides[${index}].steps must be a string array`);
      break;
    case "comparison":
      if (!isNonEmptyString(slide.leftTitle)) errors.push(`slides[${index}].leftTitle is required`);
      if (!isStringArray(slide.leftPoints)) errors.push(`slides[${index}].leftPoints must be a string array`);
      if (!isNonEmptyString(slide.rightTitle)) errors.push(`slides[${index}].rightTitle is required`);
      if (!isStringArray(slide.rightPoints)) errors.push(`slides[${index}].rightPoints must be a string array`);
      break;
    default:
      break;
  }

  return errors;
}

export function validateDeckContent(content) {
  const errors = [];

  if (!content || typeof content !== "object") {
    return ["content must be a JSON object"];
  }

  if (content.slides !== undefined && !Array.isArray(content.slides)) {
    errors.push(`content.slides must be an array`);
    return errors;
  }

  for (const [index, slide] of (content.slides ?? []).entries()) {
    errors.push(...validateSlide(slide, index));
  }

  return errors;
}
