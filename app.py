from flask import Flask, render_template_string, request, jsonify
import requests, urllib.parse

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
  .header{text-align:center;padding:2rem 1rem 1rem}
  .header h1{font-size:2.2rem;background:linear-gradient(90deg,#a78bfa,#38bdf8,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
  .header p{color:#94a3b8;margin-top:.5rem}
  .tabs{display:flex;justify-content:center;gap:.5rem;padding:1rem;flex-wrap:wrap}
  .tab{padding:.6rem 1.4rem;border-radius:2rem;border:1px solid rgba(167,139,250,0.3);background:rgba(255,255,255,0.05);color:#a78bfa;cursor:pointer;transition:all .3s}
  .tab:hover,.tab.active{background:linear-gradient(135deg,#7c3aed,#2563eb);color:#fff;border-color:transparent}
  .panel{display:none;max-width:800px;margin:0 auto;padding:1rem 1.5rem 2rem}
  .panel.active{display:block}
  .card{background:rgba(255,255,255,0.06);border:1px solid rgba(167,139,250,0.2);border-radius:1rem;padding:1.5rem;margin-bottom:1rem}
  textarea{width:100%;background:rgba(0,0,0,0.3);border:1px solid rgba(167,139,250,0.3);border-radius:.75rem;color:#e0e0ff;padding:.9rem;font-size:.95rem;resize:vertical;outline:none}
  select{background:rgba(0,0,0,0.3);border:1px solid rgba(167,139,250,0.3);border-radius:.75rem;color:#e0e0ff;padding:.7rem;font-size:.9rem;width:100%;margin-bottom:.75rem;outline:none}
  .btn{display:inline-block;padding:.75rem 2rem;border-radius:2rem;border:none;background:linear-gradient(135deg,#7c3aed,#2563eb);color:#fff;font-size:1rem;cursor:pointer;transition:all .3s;margin-top:.75rem}
  .btn:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(124,58,237,0.4)}
  .result{margin-top:1rem;background:rgba(0,0,0,0.3);border-radius:.75rem;padding:1rem;min-height:60px;white-space:pre-wrap;line-height:1.7;color:#c4b5fd;border:1px solid rgba(167,139,250,0.15);word-break:break-word}
  .result img{max-width:100%;border-radius:.75rem;margin-top:.5rem;display:block}
  .result audio{width:100%;margin-top:.5rem}
  .loader{text-align:center;padding:1.5rem;color:#a78bfa;animation:pulse 1.5s infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
  label{display:block;margin-bottom:.4rem;color:#94a3b8;font-size:.875rem}
  .status{font-size:.75rem;color:#64748b;margin-top:.4rem}
  .footer{text-align:center;padding:2rem;color:#475569;font-size:.8rem}
</style>
</head>
<body>
<div class="header">
  <h1>🌟 SuperAI</h1>
  <p>AI Chat · Deep Research · Image · Audio · Video · Free · No Login</p>
</div>
<div class="tabs">
  <div class="tab active" onclick="showTab('chat')">💬 AI Chat</div>
  <div class="tab" onclick="showTab('search')">🔍 Deep Research</div>
  <div class="tab" onclick="showTab('image')">🎨 Image</div>
  <div class="tab" onclick="showTab('audio')">🎵 Audio</div>
</div>
<div id="tab-chat" class="panel active">
  <div class="card">
    <label>Ask anything</label>
    <textarea id="chat-input" rows="4" placeholder="Example: Explain quantum computing..."></textarea>
    <br>
    <label style="margin-top:.75rem">Model</label>
    <select id="chat-model">
      <option value="openai">GPT (OpenAI)</option>
      <option value="claude">Claude</option>
      <option value="gemini">Gemini</option>
      <option value="mistral">Mistral</option>
      <option value="llama">Llama</option>
    </select>
    <button class="btn" onclick="doChat()">💬 Ask AI</button>
    <div class="status" id="chat-status"></div>
    <div class="result" id="chat-result" style="display:none"></div>
  </div>
</div>
<div id="tab-search" class="panel">
  <div class="card">
    <label>Deep Research — AI gives detailed researched answer</label>
    <textarea id="search-input" rows="3" placeholder="Example: Latest AI developments in India 2026?"></textarea>
    <button class="btn" onclick="doSearch()">🔍 Deep Research</button>
    <div class="status" id="search-status"></div>
    <div class="result" id="search-result" style="display:none"></div>
  </div>
</div>
<div id="tab-image" class="panel">
  <div class="card">
    <label>Describe the image you want</label>
    <textarea id="image-input" rows="3" placeholder="Example: Sunset over Himalayas, ultra realistic..."></textarea>
    <button class="btn" onclick="doImage()">🎨 Generate Image</button>
    <div class="status" id="image-status"></div>
    <div class="result" id="image-result" style="display:none"></div>
  </div>
</div>
<div id="tab-audio" class="panel">
  <div class="card">
    <label>Type text to convert to AI voice</label>
    <textarea id="audio-input" rows="3" placeholder="Example: Welcome to SuperAI..."></textarea>
    <label style="margin-top:.75rem">Voice</label>
    <select id="audio-voice">
      <option value="alloy">Alloy</option>
      <option value="nova">Nova</option>
      <option value="echo">Echo</option>
      <option value="shimmer">Shimmer</option>
    </select>
    <button class="btn" onclick="doAudio()">🎵 Generate Audio</button>
    <div class="status" id="audio-status"></div>
    <div class="result" id="audio-result" style="display:none"></div>
  </div>
</div>
<div class="footer">Powered by Pollinations.AI · Hosted on Render.com · Free 24/7</div>
<script>
function showTab(name){
  document.querySelectorAll('.tab').forEach((t,i)=>t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  const tabs=['chat','search','image','audio'];
  document.querySelectorAll('.tab')[tabs.indexOf(name)].classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
}
function setStatus(id,msg){document.getElementById(id+'-status').textContent=msg}
function setResult(id,html){const el=document.getElementById(id+'-result');el.innerHTML=html;el.style.display='block'}
async function doChat(){
  const prompt=document.getElementById('chat-input').value.trim();
  const model=document.getElementById('chat-model').value;
  if(!prompt)return alert('Please type a question.');
  setStatus('chat','⏳ Thinking...');
  setResult('chat','<div class="loader">Generating...</div>');
  try{
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt,model})});
    const d=await r.json();
    setStatus('chat','✅ Done');
    setResult('chat',d.result||d.error||'No response');
  }catch(e){setStatus('chat','❌ Error');setResult('chat','Error: '+e.message)}
}
async function doSearch(){
  const prompt=document.getElementById('search-input').value.trim();
  if(!prompt)return alert('Please type a question.');
  setStatus('search','🔍 Researching... (10-20 seconds)');
  setResult('search','<div class="loader">Deep researching...</div>');
  try{
    const r=await fetch('/api/search',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt})});
    const d=await r.json();
    setStatus('search','✅ Done');
    setResult('search',d.result||d.error||'No response');
  }catch(e){setStatus('search','❌ Error');setResult('search','Error: '+e.message)}
}
async function doImage(){
  const prompt=document.getElementById('image-input').value.trim();
  if(!prompt)return alert('Please describe the image.');
  setStatus('image','🎨 Generating image...');
  setResult('image','<div class="loader">Creating image...</div>');
  try{
    const r=await fetch('/api/image',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt})});
    const d=await r.json();
    setStatus('image','✅ Done - long press image to save');
    setResult('image','<img src="'+d.url+'" alt="AI Image">');
  }catch(e){setStatus('image','❌ Error');setResult('image','Error: '+e.message)}
}
async function doAudio(){
  const text=document.getElementById('audio-input').value.trim();
  const voice=document.getElementById('audio-voice').value;
  if(!text)return alert('Please type some text.');
  setStatus('audio','🎵 Generating audio...');
  setResult('audio','<div class="loader">Creating audio...</div>');
  try{
    const r=await fetch('/api/audio',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text,voice})});
    const d=await r.json();
    setStatus('audio','✅ Done');
    setResult('audio','<audio controls><source src="'+d.url+'" type="audio/mpeg"></audio>');
  }catch(e){setStatus('audio','❌ Error');setResult('audio','Error: '+e.message)}
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
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://text.pollinations.ai/{encoded_prompt}?model={model}"
        r = requests.get(url, timeout=60)
        return jsonify({"result": r.text})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.json
    prompt = data.get('prompt','')
    try:
        full_prompt = f"Do a thorough deep research and give detailed answer about: {prompt}"
        encoded = urllib.parse.quote(full_prompt)
        url = f"https://text.pollinations.ai/{encoded}?model=openai"
        r = requests.get(url, timeout=90)
        return jsonify({"result": r.text})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/image', methods=['POST'])
def api_image():
    data = request.json
    prompt = data.get('prompt','')
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?model=flux&width=1024&height=1024&nologo=true"
    return jsonify({"url": url})

@app.route('/api/audio', methods=['POST'])
def api_audio():
    data = request.json
    text = data.get('text','')
    voice = data.get('voice','alloy')
    encoded = urllib.parse.quote(text)
    url = f"https://text.pollinations.ai/{encoded}?model=openai-audio&voice={voice}"
    return jsonify({"url": url})

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
