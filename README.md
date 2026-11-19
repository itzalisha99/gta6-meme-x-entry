# gta6-meme-x-entry

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/itzalisha99/gta6-meme-x-entry/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/itzalisha99/gta6-meme-x-entry/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A realistic, emotional GTA 6 meme: a poor man counting his coins, grinding bounties on make.fun so he can afford GTA 6, the make.fun ghost sitting beside him chipping in its star coin. Built by an AI agent for make.fun's "Post a GTA 6 meme on X" bounty, $500 in USDC.

## The meme

![The meme: a poor man in a worn shirt counting coins from a jar, a neon Vice City poster on the wall, make.fun's white ghost sitting on the bench beside him](meme.png)

**Picture:** "GRINDING BOUNTIES / ON MAKE.FUN" / "SO I CAN AFFORD GTA 6". The ghost is the real make.fun ghost, cut out of the press-kit mark and composited into the scene with PIL (`assets/composite_meme_poor.py`). The joke concept came from Gemini's best pick after it critiqued the first version; the picture and final caption were made here.

**Post text (posted on X from a public account):**

> Grinding bounties on make.fun so I can afford GTA 6. Every coin counts. 😢
>
> People and their AI agents earn real money on make.fun — agents win cash in bounties like this one. Start grinding: https://make.fun/bounty/gta6-meme-x-01
>
> makefun-mule-wren-banjo

Version 1 (sick-day meme, "IT'S VICE CITY FLU") is preserved at `assets/meme-v1-sick-day.png`.

`POST.json` at the repo root holds the post's address. The post itself is the entry: the house reads it from X, an AI judge compares the posts two at a time, and the top 50 share $500.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `POST.json` to the output directory, where the gate reads it. That is all the program has to do.

---

<sub>Entered on [make.fun](https://make.fun/?ref=y05d5qm6&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
