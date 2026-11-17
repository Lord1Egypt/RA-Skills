import fs from 'fs';

export default async function detect(dir) {
  try {
    return (
      fs.existsSync(`${dir}/SKILL.md`) &&
      fs.existsSync(`${dir}/SPEC.md`) &&
      fs.existsSync(`${dir}/package.json`)
    );
  } catch {
    return false;
  }
}
