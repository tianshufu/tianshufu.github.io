#!/usr/bin/env python3
"""Generate a self-contained FLARE dataset review console (index.html).

Reads the real FLARE_demo annotation JSONL files from ./data/ and the local
MP4s from ./videos/, and emits a single index.html that plays video LOCALLY
(relative ./videos/ paths) — no Hugging Face fetches at view time.
"""
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
VIDEO_ID = "K759eXmaMTY"
SCENES = ["067", "068", "069"]


def load_jsonl(path):
    rows = []
    for line in open(path):
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def scene_key(video_path):
    # "K759eXmaMTY/K759eXmaMTY-Scene-067.mp4" -> "067"
    base = video_path.split("/")[-1]
    return base.split("Scene-")[-1].split(".")[0]


def main():
    scenes = {}
    for s in SCENES:
        scenes[s] = {
            "scene_id": f"{VIDEO_ID}-Scene-{s}",
            "video_file": f"videos/{VIDEO_ID}-Scene-{s}.mp4",
            "captions": {},
            "queries": [],
        }

    for mod, key in [("vision", "caption"), ("audio", "audio_caption"), ("unified", "unified_caption")]:
        for row in load_jsonl(DATA / f"clip-caption-{mod}.jsonl"):
            k = scene_key(row["video_path"])
            if k in scenes:
                scenes[k]["captions"][mod] = row[key]

    for mod, key in [("vision", "caption"), ("audio", "audio_caption"), ("unified", "unified_caption")]:
        for row in load_jsonl(DATA / f"clip-query-{mod}.jsonl"):
            k = scene_key(row["video_path"])
            if k in scenes:
                scenes[k]["queries"].append({"modality": mod, "text": row[key]})

    video_captions = {}
    for mod in ["vision", "audio", "unified"]:
        rows = load_jsonl(DATA / f"video-caption-{mod}.jsonl")
        if rows:
            video_captions[mod] = rows[0]["video_level_caption"]

    dataset = {
        "video_id": VIDEO_ID,
        "source": "AnonymousFLARE/FLARE_demo (sample_0) — public demo",
        "full_video_file": f"videos/{VIDEO_ID}.mp4",
        "video_captions": video_captions,
        "scenes": scenes,
    }

    payload = json.dumps(dataset)
    # Avoid </script> breaking out of the embedding script tag.
    payload = payload.replace("</", "<\\/")

    page = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FLARE Dataset Review Console — """ + html.escape(VIDEO_ID) + """</title>
<style>
  :root { --bg:#0f1420; --panel:#182034; --line:#2a3556; --ink:#e8ecf4; --dim:#9aa6c0;
          --acc:#6ea8fe; --ok:#4ade80; --warn:#fbbf24; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font:15px/1.55 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  header { padding:20px 28px; border-bottom:1px solid var(--line); }
  header h1 { margin:0 0 4px; font-size:22px; }
  header p { margin:0; color:var(--dim); font-size:13px; }
  .tabs { display:flex; gap:8px; padding:16px 28px 0; flex-wrap:wrap; }
  .tab { border:1px solid var(--line); background:var(--panel); color:var(--ink);
         padding:8px 16px; border-radius:999px; cursor:pointer; font-size:14px; }
  .tab.active { background:var(--acc); border-color:var(--acc); color:#0b1020; font-weight:600; }
  main { display:grid; grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);
         gap:20px; padding:20px 28px 40px; }
  @media (max-width:900px){ main{grid-template-columns:1fr;} }
  .card { background:var(--panel); border:1px solid var(--line); border-radius:14px;
          padding:18px; margin-bottom:16px; }
  .card h2 { margin:0 0 10px; font-size:16px; }
  video { width:100%; border-radius:10px; background:#000; max-height:56vh; }
  .meta { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
  .pill { font-size:12px; padding:3px 10px; border-radius:999px;
          background:#24304d; color:#cdd8ee; border:1px solid var(--line); }
  .pill.mod-vision{ background:#123a2b; color:#7ee2b0; border-color:#1f5c44; }
  .pill.mod-audio{ background:#3a2c12; color:#f5cf6e; border-color:#5c4a1f; }
  .pill.mod-unified{ background:#2c1f4d; color:#c4aef5; border-color:#4a3570; }
  .pill.gold{ background:#0f3a1f; color:var(--ok); border-color:#1f6b3a; }
  .q { border-left:3px solid var(--acc); padding:8px 12px; margin:10px 0;
       background:#141c30; border-radius:0 8px 8px 0; }
  .q p { margin:6px 0 0; }
  .cap { margin:10px 0; }
  .cap h3 { margin:0 0 4px; font-size:13px; color:var(--dim); text-transform:uppercase;
            letter-spacing:.06em; }
  .cap p { margin:0; }
  details.raw summary { cursor:pointer; color:var(--acc); font-size:13px; }
  details.raw pre { background:#0b1020; padding:12px; border-radius:8px; overflow:auto;
                    font-size:12px; max-height:320px; }
  .note { border:1px dashed var(--warn); border-radius:10px; padding:12px 14px;
          font-size:13px; color:#f3d9a0; background:#221c10; }
  .loader { font-size:13px; color:var(--dim); }
  .loader input { margin-top:8px; }
  .err { color:#ff9d9d; font-size:13px; margin-top:8px; display:none; }
  footer { padding:0 28px 28px; color:var(--dim); font-size:12px; }
</style>
</head>
<body>
<header>
  <h1>FLARE Dataset Review Console</h1>
  <p>video_id <b id="h-vid"></b> &middot; <span id="h-src"></span> &middot; all video plays from local files — no network fetches</p>
</header>

<div class="tabs" id="tabs"></div>

<main>
  <section>
    <div class="card">
      <h2 id="v-title">Video</h2>
      <video id="player" controls preload="metadata" playsinline></video>
      <div class="err" id="v-err"></div>
      <div class="meta" id="v-meta"></div>
    </div>
    <div class="card">
      <h2>Captions (corpus text)</h2>
      <div id="caps"></div>
    </div>
  </section>

  <section>
    <div class="card">
      <h2>Benchmark queries <span class="pill" id="q-count"></span></h2>
      <div id="queries"></div>
    </div>
    <div class="card note">
      <b>Why this matters for clustered inference.</b>
      Many benchmark queries share the same source video (here: one video, several scenes,
      several queries per scene). Treating each query as an independent test overstates
      statistical evidence — the paper's core claim. This console lets you inspect the
      video &rarr; clip &rarr; query nesting directly.
    </div>
    <div class="card">
      <h2>Raw selected record</h2>
      <details class="raw"><summary>show JSON</summary><pre id="raw"></pre></details>
    </div>
    <div class="card loader">
      <h2>Load your own manifest</h2>
      Drop a FLARE-style <b>.jsonl</b> manifest to browse more records locally.
      Nothing is uploaded — parsing happens entirely in your browser.
      <br><input type="file" id="manifest" accept=".jsonl,.json">
      <div class="err" id="m-err"></div>
    </div>
  </section>
</main>

<footer>FLARE demo data: AnonymousFLARE/FLARE_demo (sample_0), Hugging Face. Viewer generated locally; videos served from ./videos/.</footer>

<script>
const DATA = __PAYLOAD__;

const player = document.getElementById('player');
const tabsEl = document.getElementById('tabs');

const VIEWS = [
  { id:'full', label:'Full video' },
  ...Object.keys(DATA.scenes).sort().map(s => ({ id:s, label:'Scene '+s }))
];
let current = '067';

function modPill(m){
  const names = {vision:'vision', audio:'audio', unified:'unified'};
  return `<span class="pill mod-${m}">${names[m]||m}</span>`;
}
function esc(s){ return String(s).replace(/[&<>"]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }

function renderTabs(){
  tabsEl.innerHTML = '';
  VIEWS.forEach(v=>{
    const b = document.createElement('button');
    b.className = 'tab' + (v.id===current ? ' active' : '');
    b.textContent = v.label;
    b.onclick = ()=>{ current = v.id; renderTabs(); render(); };
    tabsEl.appendChild(b);
  });
}

function render(){
  document.getElementById('h-vid').textContent = DATA.video_id;
  document.getElementById('h-src').textContent = DATA.source;
  const errEl = document.getElementById('v-err');
  errEl.style.display = 'none'; errEl.textContent = '';

  let title, src, meta, caps, queries, raw;
  if(current === 'full'){
    title = 'Full video — ' + DATA.video_id;
    src = DATA.full_video_file;
    meta = [`<span class="pill">${esc(DATA.video_id)}</span>`,
            `<span class="pill">${Object.keys(DATA.scenes).length} scenes in demo</span>`,
            `<span class="pill">local file</span>`];
    caps = DATA.video_captions;
    queries = [];
    raw = { video_id: DATA.video_id, video_file: src, captions: caps };
  } else {
    const sc = DATA.scenes[current];
    title = 'Scene ' + current + ' — ' + sc.scene_id;
    src = sc.video_file;
    const nq = sc.queries.length;
    meta = [`<span class="pill">${esc(sc.scene_id)}</span>`,
            `<span class="pill">${nq} quer${nq===1?'y':'ies'}</span>`,
            `<span class="pill gold">gold clip</span>`,
            `<span class="pill">local file</span>`];
    caps = sc.captions;
    queries = sc.queries;
    raw = { video_id: DATA.video_id, scene_id: sc.scene_id, video_file: src,
            captions: caps, queries: queries };
  }

  document.getElementById('v-title').textContent = title;
  player.src = src;
  player.load();
  document.getElementById('v-meta').innerHTML = meta.join('');

  const capsEl = document.getElementById('caps');
  capsEl.innerHTML = ['vision','audio','unified'].map(m =>
    caps[m] ? `<div class="cap"><h3>${m} caption</h3><p>${esc(caps[m])}</p></div>` : ''
  ).join('') || '<p class="loader">No captions for this view.</p>';

  const qEl = document.getElementById('queries');
  document.getElementById('q-count').textContent = queries.length + ' total';
  qEl.innerHTML = queries.length ? queries.map(q =>
    `<div class="q">${modPill(q.modality)} <span class="pill gold">gold: ${current==='full'?'video':('Scene '+current)}</span><p>${esc(q.text)}</p></div>`
  ).join('') : '<p class="loader">No benchmark queries attached to the full-video view — pick a scene.</p>';

  document.getElementById('raw').textContent = JSON.stringify(raw, null, 2);
}

player.addEventListener('error', ()=>{
  const e = document.getElementById('v-err');
  const src = player.currentSrc || player.src;
  e.style.display = 'block';
  e.textContent = 'Could not play: ' + src +
    ' — make sure the MP4 sits in ./videos/ next to this HTML file.';
});

document.getElementById('manifest').addEventListener('change', ev=>{
  const f = ev.target.files[0]; if(!f) return;
  const r = new FileReader();
  r.onload = ()=>{
    try{
      const rows = r.result.split(/\\n/).filter(l=>l.trim()).map(l=>JSON.parse(l));
      document.getElementById('m-err').style.display='none';
      alert('Loaded '+rows.length+' manifest records locally (browser only).');
    }catch(err){
      const e = document.getElementById('m-err');
      e.style.display='block'; e.textContent='Could not parse manifest: '+err.message;
    }
  };
  r.readAsText(f);
});

renderTabs();
render();
</script>
</body>
</html>
"""

    page = page.replace("__PAYLOAD__", payload)
    # fix the CSS var typo guard: ensure no stray text
    out = ROOT / "index.html"
    out.write_text(page)
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    print(f"scenes: {list(scenes.keys())}, queries: " +
          f"{[(s, len(scenes[s]['queries'])) for s in scenes]}")


if __name__ == "__main__":
    main()
