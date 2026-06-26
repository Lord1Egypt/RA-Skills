export function validateSubmitText(input) {
  const errors = [];

  if (!input.prompt || typeof input.prompt !== 'string' || input.prompt.trim().length === 0) {
    errors.push('prompt is required and must be a non-empty string.');
  }

  return errors;
}

export function validateSubmitImage(input) {
  const errors = validateSubmitText(input);

  if (!input.images || !Array.isArray(input.images) || input.images.length === 0) {
    errors.push('images is required for image-to-image and must be a non-empty array of image sources.');
  } else {
    for (const source of input.images) {
      if (typeof source !== 'string' || source.trim().length === 0) {
        errors.push(`Invalid image source: "${source}".`);
      }
    }
  }

  return errors;
}
