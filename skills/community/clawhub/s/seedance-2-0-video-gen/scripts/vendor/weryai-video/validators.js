export function validateSubmitText(input) {
  const errors = [];

  if (!input.prompt || typeof input.prompt !== 'string' || input.prompt.trim().length === 0) {
    errors.push('prompt is required and must be a non-empty string.');
  }

  const duration = input.duration ?? input.dur;
  if (duration == null) {
    errors.push('duration is required (integer, seconds).');
  } else {
    const value = Number(duration);
    if (!Number.isInteger(value) || value < 1) {
      errors.push('duration must be a positive integer (seconds).');
    }
  }

  return errors;
}

export function validateSubmitImage(input) {
  const errors = validateSubmitText(input);

  if (!input.image || typeof input.image !== 'string') {
    errors.push('image is required and must be a URL string.');
  } else if (!input.image.startsWith('https://')) {
    errors.push(`Invalid image URL: "${input.image}". Only https:// URLs are supported.`);
  }

  return errors;
}

export function validateSubmitMultiImage(input) {
  const errors = validateSubmitText(input);

  if (!input.images || !Array.isArray(input.images) || input.images.length === 0) {
    errors.push('images is required and must be a non-empty array of URLs.');
  } else {
    for (const url of input.images) {
      if (typeof url !== 'string' || !url.startsWith('https://')) {
        errors.push(`Invalid image URL: "${url}". Only https:// URLs are supported.`);
      }
    }
  }

  return errors;
}
