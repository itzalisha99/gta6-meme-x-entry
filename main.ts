// gta6-meme-x-01 entry: the post itself is the entry, so this program only
// hands the house the post's address. It copies POST.json from the bot
// directory into the output directory, where the gate reads it.
//
// The house then reads the post from X (its first picture, the sick-day meme
// with make.fun's ghost on the couch, and its text) and hands that dossier to
// the judge. Nothing written here is judged.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

try {
  copyFileSync(source, target);
} catch (error) {
  console.error(`could not copy POST.json from ${botDir}: ${(error as Error).message}`);
  process.exit(1);
}

// Fail loudly if what we copied is not a JSON object with a url string, so a
// broken POST.json never slips through silently. The placeholder still parses
// (it is valid JSON), so this does not change the placeholder behaviour.
try {
  const parsed: unknown = JSON.parse(readFileSync(target, "utf8"));
  if (typeof parsed !== "object" || parsed === null || typeof (parsed as { url?: unknown }).url !== "string") {
    throw new Error("POST.json is not an object with a string url");
  }
} catch (error) {
  console.error(`POST.json failed validation: ${(error as Error).message}`);
  process.exit(1);
}
