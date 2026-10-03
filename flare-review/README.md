# FLARE Dataset Review Console

Visual review tool for the FLARE demo dataset (video K759eXmaMTY) — built to
unblock the "video won't play" issue from the ChatGPT session.

## What it is
`index.html` — a self-contained page (no external network calls) that lets you
tab between the full video and scenes 067/068/069, watch each clip, read the
real vision/audio/unified captions, and inspect the real benchmark queries with
their gold-clip badges.

## Run it
Just open `index.html` in a browser. Videos are in `videos/` and play locally —
this is the fix: the old version referenced Hugging Face URLs, which browsers
refuse to play from a local page.

## Contents
- `index.html` — the viewer (generated; do not hand-edit)
- `generate_viewer.py` — regenerates `index.html` from `./data/*.jsonl`
- `videos/` — K759eXmaMTY.mp4 (full, ~60 MB) + Scene 067/068/069 mp4s,
  downloaded from AnonymousFLARE/FLARE_demo on Hugging Face
- `data/` — the real annotation JSONL files (clip captions + clip queries per
  modality, video-level captions), also from FLARE_demo sample_0

## Regenerate
`python3 generate_viewer.py` — reads `data/`, writes `index.html`.

## Verified 2026-10-02
Real Chromium check: all four videos reach readyState 4 (HAVE_ENOUGH_DATA),
Scene 067 actually played (currentTime advanced), all tabs switch correctly,
zero JS errors.
