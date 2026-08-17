from flask import Flask, render_template_string, request, jsonify
import requests, urllib.parse

app = Flask(__name__)

GROQ_API_KEY = "gsk_QPGwqeNplwSTIILPU3R8WGdyb3FYjAzqg5RpQQEnrm9PoKSUddP"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🌟 SuperAI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:linear-gradient(135deg,#0a0a1a,#1a0a2e,#0a1a2e);min-height:100vh;font-family:'Segoe UI',sans-serif;color:#e0e0ff}
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
.btn{display:block;padding:.75rem 2rem;border-radius:2rem;border:none;background:linear-gradient(135deg,#7c3aed,#2563eb);color:#fff;font-size:1rem;cursor:pointer;transition:all .3s;margin-top:.75rem;width:100%;text-align:center}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(124,58,237,0.4)}
.result{margin-top:1rem;background:rgba(0,0,0,0.3);border-radius:.75rem;padding:1rem;min-height:60px;line-height:1.8;color:#c4b5fd;border:1px solid rgba(167,139,250,0.15);word-break:break-word;white-space:pre-wrap;display:none}
.result img{max-width:100%;border-radius:.75rem;margin-top:.5rem;display:block}
.result audio{width:100%;margin-top:.5rem}
.loader{text-align:center;padding:1.5rem;color:#a78bfa;animation:pulse 1.5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
label{display:block;margin-bottom:.4rem;color:#94a3b8;font-size:.875rem}
.status{font-size:.8rem;color:#38bdf8;margin-top:.5rem;min-height:1.2rem}
.footer{text-align:center;padding:2rem;color:#475569;font-size:.8rem}
.chat-history{max-height:400px;overflow-y:auto;margin-bottom:1rem}
.msg{padding:.75rem 1rem;border-radius:.75rem;margin-bottom:.5rem;line-height:1.7}
.msg.user{background:rgba(124,58,237,0.2);border:1px solid rgba(124,58,237,0.3);text-align:right}
.msg.ai{background:rgba(0,0,0,0.3);border:1px solid rgba(167,139,250,0.2);white-space:pre-wrap}
.msg .label{font-size:.7rem;color:#64748b;margin-bottom:.3rem}
</style>
</head>
<body>
<div class="header">
<h1>🌟 SuperAI</h1>
<p>AI Chat · Deep Research · Image Generation · Audio · 100% Free 🇮🇳</p>
</div>
<div class="tabs">
<div class="tab active" onclick="showTab('chat')">💬 Chat</div>
<div class="tab" onclick="showTab('research')">🔍 Research</div>
<div class="tab" onclick="showTab('image')">🎨 Image</div>
<div class="tab" onclick="showTab('audio')">🎵 Audio</div>
</div>

<div id="tab-chat" class="panel active">
<div class="card">
<div class="chat-history" id="chat-history"></div>
<label>Ask any question</label>
<textarea id="chat-input" rows="3" placeholder="Example: Tell me about class 10 CBSE biology chapter 1..."></textarea>
<div class="status" id="chat-status"></div>
<button class="btn" onclick="doChat()">💬 Send Question</button>
</div>
</div>

<div id="tab-research" class="panel">
<div class="card">
<label>Deep Research any topic</label>
<textarea id="research-input" rows="4" placeholder="Example: Explain photosynthesis in detail..."></textarea>
<div class="status" id="research-status"></div>
<button class="btn" onclick="doResearch()">🔍 Deep Research</button>
<div class="result" id="research-result"></div>
</div>
</div>

<div id="tab-image" class="panel">
<div class="card">
<label>Describe the image you want</label>
<textarea id="image-input" rows="4" placeholder="Example: A beautiful sunset over the Himalayas, ultra realistic 4K..."></textarea>
<div class="status" id="image-status"></div>
<button class="btn" onclick="doImage()">🎨 Generate Image</button>
<div class="result" id="image-result"></div>
</div>
</div>

<div id="tab-audio" class="panel">
<div class="card">
<label>Type text to convert to AI voice</label>
<textarea id="audio-input" rows="4" placeholder="Example: Hello, welcome to SuperAI..."></textarea>
<label style="margin-top:.75rem">Select Voice</label>
<select id="audio-voice">
<option value="alloy">Alloy - Neutral</option>
<option value="nova">Nova - Female</option>
<option value="echo">Echo - Male</option>
<option value="shimmer">Shimmer - Soft</option>
</select>
<div class="status" id="audio-status"></div>
<button class="btn" onclick="doAudio()">🎵 Generate Voice</button>
<div class="result" id="audio-result"></div>
</div>
</div>

<div class="footer">SuperAI · Powered by Groq AI · Free 24/7 anywhere in India 🇮🇳</div>

<script>
function showTab(name){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  const tabs=['chat','research','image','audio'];
  document.querySelectorAll('.tab')[tabs.indexOf(name)].classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
}
function setStatus(id,msg){document.getElementById(id+'-status').textContent=msg}
function showResult(id,html){
  const el=document.getElementById(id+'-result');
  el.innerHTML=html;
  el.style.display='block';
}

let chatMessages=[{role:'system',content:'You are a helpful AI assistant. Give clear, detailed, accurate answers to every question. Answer in the same language the user asks in.'}];

async function doChat(){
  const input=document.getElementById('chat-input');
  const prompt=input.value.trim();
  if(!prompt){alert('Please type a question.');return;}
  input.value='';
  const history=document.getElementById('chat-history');
  history.innerHTML+=`<div class="msg user"><div class="label">You</div>${prompt}</div>`;
  history.innerHTML+=`<div class="msg ai" id="latest-ai"><div class="label">SuperAI</div><div class="loader">Thinking...</div></div>`;
  history.scrollTop=history.scrollHeight;
  setStatus('chat','⏳ AI is thinking...');
  chatMessages.push({role:'user',content:prompt});
  try{
    const r=await fetch('/api/chat',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({messages:chatMessages})
    });
    const d=await r.json();
    if(d.error){throw new Error(d.error);}
    chatMessages.push({role:'assistant',content:d.result});
    document.getElementById('latest-ai').innerHTML=`<div class="label">SuperAI ✅</div>${d.result}`;
    history.scrollTop=history.scrollHeight;
    setStatus('chat','✅ Answer ready - ask another question!');
  }catch(e){
    document.getElementById('latest-ai').innerHTML=`<div class="label">SuperAI ❌</div>Error: ${e.message}`;
    setStatus('chat','❌ Failed - please try again');
  }
}

document.addEventListener('DOMContentLoaded',function(){
  document.getElementById('chat-input').addEventListener('keydown',function(e){
    if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();doChat();}
  });
});

async function doResearch(){
  const prompt=document.getElementById('research-input').value.trim();
  if(!prompt){alert('Please type a topic.');return;}
  setStatus('research','🔍 Deeply researching... please wait 15-30 seconds');
  showResult('research','<div class="loader">Deep researching your topic...</div>');
  try{
    const r=await fetch('/api/chat',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({messages:[
        {role:'system',content:'You are a deep research expert. Give very detailed, comprehensive, well-structured answers with headings, facts, examples and explanations. Cover the topic completely.'},
        {role:'user',content:'Do a thorough deep research on: '+prompt}
      ]})
    });
    const d=await r.json();
    if(d.error){throw new Error(d.error);}
    setStatus('research','✅ Research complete');
    showResult('research',d.result);
  }catch(e){
    setStatus('research','❌ Failed');
    showResult('research','Error: '+e.message+'. Please try again.');
  }
}

function doImage(){
  const prompt=document.getElementById('image-input').value.trim();
  if(!prompt){alert('Please describe the image.');return;}
  setStatus('image','🎨 Generating image... please wait 15 seconds');
  showResult('image','<div class="loader">Creating your image...</div>');
  const seed=Math.floor(Math.random()*99999);
  const encoded=encodeURIComponent(prompt);
  const url='https://image.pollinations.ai/prompt/'+encoded+'?model=flux&width=1024&height=1024&nologo=true&seed='+seed;
  const img=new Image();
  img.onload=function(){
    setStatus('image','✅ Image ready - long press to save');
    showResult('image','<img src="'+url+'" alt="AI Image">');
  };
  img.onerror=function(){
    const url2='https://image.pollinations.ai/prompt/'+encoded+'?model=turbo&width=512&height=512&nologo=true&seed='+seed;
    const img2=new Image();
    img2.onload=function(){
      setStatus('image','✅ Image ready');
      showResult('image','<img src="'+url2+'" alt="AI Image">');
    };
    img2.onerror=function(){
      setStatus('image','❌ Failed - try simpler description');
      showResult('image','Image failed. Try again with simpler words.');
    };
    img2.src=url2;
  };
  img.src=url;
}

function doAudio(){
  const text=document.getElementById('audio-input').value.trim();
  const voice=document.getElementById('audio-voice').value;
  if(!text){alert('Please type some text.');return;}
  const encoded=encodeURIComponent(text);
  const url='https://text.pollinations.ai/'+encoded+'?model=openai-audio&voice='+voice;
  showResult('audio','<audio controls autoplay><source src="'+url+'" type="audio/mpeg">Not supported.</audio>');
  setStatus('audio','✅ Press play to listen');
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
    messages = data.get('messages', [])
    try:
        r = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama3-70b-8192',
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 2048
            },
            timeout=60
        )
        d = r.json()
        if 'choices' in d:
            return jsonify({'result': d['choices'][0]['message']['content']})
        else:
            return jsonify({'error': str(d)})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
