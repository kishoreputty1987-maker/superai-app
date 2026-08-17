from flask import Flask, render_template_string, request, jsonify
import requests, urllib.parse, json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🌟 SuperAI — Chat · Image · Audio · Video</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:linear-gradient(135deg,#0a0a1a 0%,#1a0a2e 50%,#0a1a2e 100%);min-height:100vh;font-family:'Segoe UI',sans-serif;color:#e0e0ff}
  .header{text-align:center;padding:2rem 1rem 1rem;background:linear-gradient(180deg,rgba(80,0,120,0.4),transparent)}
  .header h1{font-size:2.2rem;background:linear-gradient(90deg,#a78bfa,#38bdf8,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
  .header p{color:#94a3b8;margin-top:.5rem;font-size:.95rem}
  .tabs{display:flex;justify-content:center;gap:.5rem;padding:1rem;flex-wrap:wrap}
  .tab{padding:.6rem 1.4rem;border-radius:2rem;border:1px solid rgba(167,139,250,0.3);background:rgba(255,255,255,0.05);color:#a78bfa;cursor:pointer;transition:all .3s;font-size:.9rem}
  .tab:hover,.tab.active{background:linear-gradient(135deg,#7c3aed,#2563eb);color:#fff;border-color:transparent;box-shadow:0 0 20px rgba(124,58,237,0.5)}
  .panel{display:none;max-width:800px;margin:0 auto;padding:1rem 1.5rem 2rem}
  .panel.active{display:block}
  .card{background:rgba(255,255,255,0.06);border:1px solid rgba(167,139,250,0.2);border-radius:1rem;padding:1.5rem;margin-bottom:1rem}
  textarea,input[type=text]{width:100%;background:rgba(0,0,0,0.3);border:1px solid rgba(167,139,250,0.3);border-radius:.75rem;color:#e0e0ff;padding:.9rem;font-size:.95rem;resize:vertical;outline:none;transition:border .3s}
  textarea:focus,input[type=text]:focus{border-color:#a78bfa}
  .btn{display:inline-block;padding:.75rem 2rem;border-radius:2rem;border:none;background:linear-gradient(135deg,#7c3aed,#2563eb);color:#fff;font-size:1rem;cursor:pointer;transition:all .3s;margin-top:.75rem}
  .btn:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(124,58,237,0.4)}
  .btn:disabled{opacity:.5;cursor:not-allowed;transform:none}
  .result{margin-top:1rem;background:rgba(0,0,0,0.3);border-radius:.75rem;padding:1rem;min-height:60px;white-space:pre-wrap;line-height:1.7;color:#c4b5fd;border:1px solid rgba(167,139,250,0.15);word-break:break-word}
  .result img{max-width:100%;border-radius:.75rem;margin-top:.5rem;display:block}
  .result audio{width:100%;margin-top:.5rem}
  .result video{max-width:100%;border-radius:.75rem;margin-top:.5rem}
  .loader{text-align:center;padding:1.5rem;color:#a78bfa;animation:pulse 1.5s infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
  .badge{display:inline-block;padding:.2rem .7rem;border-radius:1rem;font-size:.75rem;background:rgba(56,189,248,0.15);color:#38bdf8;border:1px solid rgba(56,189,248,0.3);margin-left:.5rem}
  label{display:block;margin-bottom:.4rem;color:#94a3b8;font-size:.875rem}
  select{background:rgba(0,0,0,0.3);border:1px solid rgba(167,139,250,0.3);border-radius:.75rem;color:#e0e0ff;padding:.7rem;font-size:.9rem;width:100%;margin-bottom:.75rem;outline:none}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
  @media(max-width:600px){.grid2{grid-template-columns:1fr}.header h1{font-size:1.6rem}}
  .footer{text-align:center;padding:2rem;color:#475569;font-size:.8rem}
  .status{font-size:.75rem;color:#64748b;margin-top:.4rem}
</style>
</head>
<body>
<div class="header">
  <h1>🌟 SuperAI</h1>
  <p>AI Chat · Deep Research · Image · Audio · Video <span class="badge">Free · No Login</span></p>
</div>

<div class="tabs">
  <div class="tab active" onclick="showTab('chat')">💬 AI Chat</div>
  <div class="tab" onclick="showTab('search')">🔍 Deep Research</div>
  <div class="tab" onclick="showTab('image')">🎨 Image</div>
  <div class="tab" onclick="showTab('audio')">🎵 Audio</div>
  <div class="tab" onclick="showTab('video')">🎬 Video</div>
</div>

<!-- CHAT TAB -->
<div id="tab-chat" class="panel active">
  <div class="card">
    <label>Ask anything — AI will answer deeply</label>
    <textarea id="chat-input" rows="4" placeholder="Example: Explain quantum computing in simple words..."></textarea>
    <br>
    <label style="margin-top:.75rem">Model</label>
    <select id="chat-model">
      <option value="openai">GPT (OpenAI)</option>
      <option value="claude">Claude (Anthropic)</option>
      <option value="gemini">Gemini (Google)</option>
      <option value="deepseek">DeepSeek</option>
      <option value="llama">Llama 3</option>
    </select>
    <button class="btn" onclick="doChat()">💬 Ask AI</button>
    <div class="status" id="chat-status"></div>
    <div class="result" id="chat-result" style="display:none"></div>
  </div>
</div>

<!-- SEARCH TAB -->
<div id="tab-search" class="panel">
  <div class="card">
    <label>Deep Research — AI searches the web live and gives detailed answer</label>
    <textarea id="search-input" rows="3" placeholder="Example: What are the latest developments in AI in India 2026?"></textarea>
    <br>
    <button class="btn" onclick="doSearch()">🔍 Deep Research</button>
    <div class="status" id="search-status"></div>
    <div class="result" id="search-result" style="display:none"></div>
  </div>
</div>

<!-- IMAGE TAB -->
<div id="tab-image" class="panel">
  <div class="card">
    <label>Describe the image you want to generate</label>
    <textarea id="image-input" rows="3" placeholder="Example: A beautiful sunrise over the Himalayas, ultra realistic, 4K..."></textarea>
    <div class="grid2" style="margin-top:.75rem">
      <div>
        <label>Model</label>
        <select id="image-model">
          <option value="flux">Flux (Best Quality)</option>
          <option value="turbo">Turbo (Fastest)</option>
          <option value="gptimage">GPT Image</option>
        </select>
      </div>
      <div>
        <label>Size</label>
        <select id="image-size">
          <option value="1024x1024">Square 1024×1024</option>
          <option value="1280x720">Landscape 1280×720</option>
          <option value="720x1280">Portrait 720×1280</option>
        </select>
      </div>
    </div>
    <button class="btn" onclick="doImage()">🎨 Generate Image</button>
    <div class="status" id="image-status"></div>
    <div class="result" id="image-result" style="display:none"></div>
  </div>
</div>

<!-- AUDIO TAB -->
<div id="tab-audio" class="panel">
  <div class="card">
    <label>Type text to convert to AI voice / speech</label>
    <textarea id="audio-input" rows="3" placeholder="Example: Welcome to India's most advanced AI platform..."></textarea>
    <div style="margin-top:.75rem">
      <label>Voice</label>
      <select id="audio-voice">
        <option value="alloy">Alloy (Neutral)</option>
        <option value="nova">Nova (Female)</option>
        <option value="echo">Echo (Male)</option>
        <option value="shimmer">Shimmer (Soft)</option>
        <option value="fable">Fable (British)</option>
      </select>
    </div>
    <button class="btn" onclick="doAudio()">🎵 Generate Audio</button>
    <div class="status" id="audio-status"></div>
    <div class="result" id="audio-result" style="display:none"></div>
  </div>
</div>

<!-- VIDEO TAB -->
<div id="tab-video" class="panel">
  <div class="card">
    <label>Describe the video scene to generate (4–10 seconds)</label>
    <textarea id="video-input" rows="3" placeholder="Example: A tiger walking through a forest at sunrise, cinematic..."></textarea>
    <div style="margin-top:.75rem">
      <label>Model</label>
      <select id="video-model">
        <option value="seedance-2.0-mini">Seedance Mini (Fast)</option>
        <option value="seedance-2.0-fast">Seedance Fast</option>
      </select>
    </div>
    <button class="btn" onclick="doVideo()">🎬 Generate Video</button>
    <div class="status" id="video-status"></div>
    <div class="result" id="video-result" style="display:none"></div>
    <p style="font-size:.75rem;color:#64748b;margin-top:.5rem">⏳ Video takes 30–90 seconds to generate. Please wait after clicking.</p>
  </div>
</div>

<div class="footer">
  Powered by Pollinations.AI (Free, Open-Source) · Hosted on Render.com<br>
  No data stored · Works 24/7 anywhere in India
</div>

<script>
function showTab(name) {
  document.querySelectorAll('.tab').forEach((t,i)=>{t.classList.remove('active')});
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  const tabs = ['chat','search','image','audio','video'];
  document.querySelectorAll('.tab')[tabs.indexOf(name)].classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
}

function setStatus(id, msg) {
  document.getElementById(id+'-status').textContent = msg;
}
function setResult(id, html, show=true) {
  const el = document.getElementById(id+'-result');
  el.innerHTML = html;
  el.style.display = show ? 'block' : 'none';
}

async function doChat() {
  const prompt = document.getElementById('chat-input').value.trim();
  const model = document.getElementById('chat-model').value;
  if (!prompt) return alert('Please type a question first.');
  setStatus('chat','⏳ AI is thinking...');
  setResult('chat','<div class="loader">Generating response...</div>');
  try {
    const res = await fetch('/api/chat', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({prompt, model})
    });
    const data = await res.json();
    setStatus('chat','✅ Done');
    setResult('chat', data.result || data.error || 'No response');
  } catch(e) {
    setStatus('chat','❌ Error');
    setResult('chat','Error: '+e.message);
  }
}

async function doSearch() {
  const prompt = document.getElementById('search-input').value.trim();
  if (!prompt) return alert('Please type a research question first.');
  setStatus('search','🔍 Searching the web and analysing... (takes 10–20s)');
  setResult('search','<div class="loader">Deep researching your question...</div>');
  try {
    const res = await fetch('/api/search', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({prompt})
    });
    const data = await res.json();
    setStatus('search','✅ Done');
    setResult('search', data.result || data.error || 'No response');
  } catch(e) {
    setStatus('search','❌ Error');
    setResult('search','Error: '+e.message);
  }
}

async function doImage() {
  const prompt = document.getElementById('image-input').value.trim();
  const model = document.getElementById('image-model').value;
  const size = document.getElementById('image-size').value;
  if (!prompt) return alert('Please describe the image first.');
  const [w,h] = size.split('x');
  setStatus('image','🎨 Generating image...');
  setResult('image','<div class="loader">Creating your image...</div>');
  try {
    const res = await fetch('/api/image', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({prompt, model, width:w, height:h})
    });
    const data = await res.json();
    setStatus('image','✅ Done — right-click image to save');
    setResult('image', `<img src="${data.url}" alt="Generated Image"><br><small style="color:#64748b">Prompt: ${prompt}</small>`);
  } catch(e) {
    setStatus('image','❌ Error');
    setResult('image','Error: '+e.message);
  }
}

async function doAudio() {
  const text = document.getElementById('audio-input').value.trim();
  const voice = document.getElementById('audio-voice').value;
  if (!text) return alert('Please type some text first.');
  setStatus('audio','🎵 Generating audio...');
  setResult('audio','<div class="loader">Creating audio...</div>');
  try {
    const res = await fetch('/api/audio', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({text, voice})
    });
    const data = await res.json();
    setStatus('audio','✅ Done — press play');
    setResult('audio', `<audio controls><source src="${data.url}" type="audio/mpeg">Your browser does not support audio.</audio>`);
  } catch(e) {
    setStatus('audio','❌ Error');
    setResult('audio','Error: '+e.message);
  }
}

async function doVideo() {
  const prompt = document.getElementById('video-input').value.trim();
  const model = document.getElementById('video-model').value;
  if (!prompt) return alert('Please describe the video first.');
  setStatus('video','🎬 Generating video (30–90 seconds, please wait)...');
  setResult('video','<div class="loader">Creating video... Please do not close this page.</div>');
  try {
    const res = await fetch('/api/video', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({prompt, model})
    });
    const data = await res.json();
    if (data.url) {
      setStatus('video','✅ Done');
      setResult('video', `<video controls><source src="${data.url}" type="video/mp4">Your browser does not support video.</video>`);
    } else {
      setStatus('video','⚠️ '+( data.error || 'Video not ready yet'));
      setResult('video', data.error || 'Video generation in progress or failed. Try again.');
    }
  } catch(e) {
    setStatus('video','❌ Error');
    setResult('video','Error: '+e.message);
  }
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    prompt = data.get('prompt','')
    model = data.get('model','openai')
    try:
        system_msg = "You are a helpful AI assistant. Give detailed, accurate answers."
        payload = {
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            "model": model,
            "seed": 42,
            "jsonMode": False
        }
        r = requests.post(
            "https://text.pollinations.ai/",
            json=payload,
            timeout=60
        )
        return jsonify({"result": r.text})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.json
    prompt = data.get('prompt','')
    try:
        system_msg = (
            "You are a deep research AI assistant. "
            "The user wants thorough, factual, well-structured research. "
            "Search and analyse the topic deeply. "
            "Provide a detailed answer with key facts, current information, "
            "and clear explanations. Format with sections if helpful."
        )
        payload = {
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Do a deep research on: {prompt}"}
            ],
            "model": "openai",
            "seed": 42,
            "jsonMode": False
        }
        r = requests.post(
            "https://text.pollinations.ai/",
            json=payload,
            timeout=90
        )
        return jsonify({"result": r.text})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/image', methods=['POST'])
def api_image():
    data = request.json
    prompt = data.get('prompt','')
    model = data.get('model','flux')
    width = data.get('width','1024')
    height = data.get('height','1024')
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?model={model}&width={width}&height={height}&nologo=true"
    return jsonify({"url": url})

@app.route('/api/audio', methods=['POST'])
def api_audio():
    data = request.json
    text = data.get('text','')
    voice = data.get('voice','alloy')
    encoded = urllib.parse.quote(text)
    url = f"https://text.pollinations.ai/{encoded}?model=openai-audio&voice={voice}"
    return jsonify({"url": url})

@app.route('/api/video', methods=['POST'])
def api_video():
    data = request.json
    prompt = data.get('prompt','')
    model = data.get('model','seedance-2.0-mini')
    try:
        payload = {
            "prompt": prompt,
            "model": model,
            "width": 720,
            "height": 480
        }
        r = requests.post(
            "https://video.pollinations.ai/",
            json=payload,
            timeout=120
        )
        if r.status_code == 200 and r.headers.get('content-type','').startswith('video'):
            return jsonify({"error": "Video returned as stream — use direct URL method"})
        resp_data = r.json() if 'json' in r.headers.get('content-type','') else {}
        video_url = resp_data.get('url') or resp_data.get('video_url','')
        if video_url:
            return jsonify({"url": video_url})
        else:
            return jsonify({"error": "Video generation in progress. Pollinations video feature is in beta — try a simpler prompt."})
    except Exception as e:
        return jsonify({"error": f"Video error: {str(e)}"})

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
