from flask import Flask, render_template_string

app = Flask(__name__)

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
.btn{display:inline-block;padding:.75rem 2rem;border-radius:2rem;border:none;background:linear-gradient(135deg,#7c3aed,#2563eb);color:#fff;font-size:1rem;cursor:pointer;transition:all .3s;margin-top:.75rem;width:100%}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(124,58,237,0.4)}
.result{margin-top:1rem;background:rgba(0,0,0,0.3);border-radius:.75rem;padding:1rem;min-height:60px;line-height:1.8;color:#c4b5fd;border:1px solid rgba(167,139,250,0.15);word-break:break-word;white-space:pre-wrap}
.result img{max-width:100%;border-radius:.75rem;margin-top:.5rem;display:block}
.result audio{width:100%;margin-top:.5rem}
.loader{text-align:center;padding:1.5rem;color:#a78bfa;animation:pulse 1.5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
label{display:block;margin-bottom:.4rem;color:#94a3b8;font-size:.875rem}
.status{font-size:.8rem;color:#38bdf8;margin-top:.5rem;min-height:1.2rem}
.footer{text-align:center;padding:2rem;color:#475569;font-size:.8rem}
</style>
</head>
<body>
<div class="header">
<h1>🌟 SuperAI</h1>
<p>AI Chat · Deep Research · Image Generation · Audio · 100% Free</p>
</div>
<div class="tabs">
<div class="tab active" onclick="showTab('chat')">💬 Chat</div>
<div class="tab" onclick="showTab('research')">🔍 Research</div>
<div class="tab" onclick="showTab('image')">🎨 Image</div>
<div class="tab" onclick="showTab('audio')">🎵 Audio</div>
</div>

<div id="tab-chat" class="panel active">
<div class="card">
<label>Ask any question to AI</label>
<textarea id="chat-input" rows="5" placeholder="Example: Tell me about class 10 CBSE biology chapter 1..."></textarea>
<div class="status" id="chat-status"></div>
<button class="btn" onclick="doChat()">💬 Get Answer</button>
<div class="result" id="chat-result" style="display:none"></div>
</div>
</div>

<div id="tab-research" class="panel">
<div class="card">
<label>Deep Research any topic</label>
<textarea id="research-input" rows="5" placeholder="Example: What are the latest developments in space exploration 2026?"></textarea>
<div class="status" id="research-status"></div>
<button class="btn" onclick="doResearch()">🔍 Deep Research</button>
<div class="result" id="research-result" style="display:none"></div>
</div>
</div>

<div id="tab-image" class="panel">
<div class="card">
<label>Describe the image you want to generate</label>
<textarea id="image-input" rows="4" placeholder="Example: A beautiful sunset over the Himalayas, ultra realistic, 4K quality..."></textarea>
<div class="status" id="image-status"></div>
<button class="btn" onclick="doImage()">🎨 Generate Image</button>
<div class="result" id="image-result" style="display:none"></div>
</div>
</div>

<div id="tab-audio" class="panel">
<div class="card">
<label>Type any text to convert to AI voice</label>
<textarea id="audio-input" rows="4" placeholder="Example: Hello, welcome to SuperAI, your free AI assistant..."></textarea>
<label style="margin-top:.75rem">Select Voice</label>
<select id="audio-voice">
<option value="alloy">Alloy - Neutral</option>
<option value="nova">Nova - Female</option>
<option value="echo">Echo - Male</option>
<option value="shimmer">Shimmer - Soft</option>
</select>
<div class="status" id="audio-status"></div>
<button class="btn" onclick="doAudio()">🎵 Generate Voice</button>
<div class="result" id="audio-result" style="display:none"></div>
</div>
</div>

<div class="footer">SuperAI · Powered by free open AI APIs · Works 24/7 anywhere in India 🇮🇳</div>

<script>
function showTab(name){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  const tabs=['chat','research','image','audio'];
  document.querySelectorAll('.tab')[tabs.indexOf(name)].classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
}

function setStatus(id,msg){
  document.getElementById(id+'-status').textContent=msg;
}

function showResult(id,html){
  const el=document.getElementById(id+'-result');
  el.innerHTML=html;
  el.style.display='block';
}

async function doChat(){
  const prompt=document.getElementById('chat-input').value.trim();
  if(!prompt){alert('Please type a question first.');return;}
  setStatus('chat','⏳ AI is thinking... please wait');
  showResult('chat','<div class="loader">Generating answer...</div>');
  try{
    const messages=[
      {role:'system',content:'You are a helpful AI assistant. Give clear, detailed, accurate answers.'},
      {role:'user',content:prompt}
    ];
    const response=await fetch('https://text.pollinations.ai/',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({messages:messages,model:'openai',seed:42})
    });
    if(!response.ok){throw new Error('API error: '+response.status);}
    const text=await response.text();
    setStatus('chat','✅ Answer ready');
    showResult('chat',text);
  }catch(e){
    setStatus('chat','❌ Failed');
    showResult('chat','Error: '+e.message+'. Please try again.');
  }
}

async function doResearch(){
  const prompt=document.getElementById('research-input').value.trim();
  if(!prompt){alert('Please type a research topic first.');return;}
  setStatus('research','🔍 Deeply researching... please wait 15-30 seconds');
  showResult('research','<div class="loader">Deep researching your topic...</div>');
  try{
    const messages=[
      {role:'system',content:'You are a deep research AI. When given a topic, research it thoroughly and provide a comprehensive, well-structured answer with all important details, facts, explanations and examples. Use clear headings and sections.'},
      {role:'user',content:'Do a thorough deep research on this topic and give me a very detailed comprehensive answer: '+prompt}
    ];
    const response=await fetch('https://text.pollinations.ai/',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({messages:messages,model:'openai',seed:42})
    });
    if(!response.ok){throw new Error('API error: '+response.status);}
    const text=await response.text();
    setStatus('research','✅ Research complete');
    showResult('research',text);
  }catch(e){
    setStatus('research','❌ Failed');
    showResult('research','Error: '+e.message+'. Please try again.');
  }
}

function doImage(){
  const prompt=document.getElementById('image-input').value.trim();
  if(!prompt){alert('Please describe the image first.');return;}
  setStatus('image','🎨 Generating image... please wait 10-20 seconds');
  showResult('image','<div class="loader">Creating your image...</div>');
  const encoded=encodeURIComponent(prompt);
  const imageUrl='https://image.pollinations.ai/prompt/'+encoded+'?model=flux&width=1024&height=1024&nologo=true&seed='+Math.floor(Math.random()*99999);
  const img=new Image();
  img.onload=function(){
    setStatus('image','✅ Image ready - long press to save');
    showResult('image','<img src="'+imageUrl+'" alt="Generated Image">');
  };
  img.onerror=function(){
    setStatus('image','❌ Failed - trying again...');
    const img2=new Image();
    const url2='https://image.pollinations.ai/prompt/'+encoded+'?model=turbo&width=512&height=512&nologo=true';
    img2.onload=function(){
      setStatus('image','✅ Image ready - long press to save');
      showResult('image','<img src="'+url2+'" alt="Generated Image">');
    };
    img2.onerror=function(){
      setStatus('image','❌ Image service busy. Try again in 30 seconds.');
      showResult('image','Image generation failed. Please try again with a simpler description.');
    };
    img2.src=url2;
  };
  img.src=imageUrl;
}

function doAudio(){
  const text=document.getElementById('audio-input').value.trim();
  const voice=document.getElementById('audio-voice').value;
  if(!text){alert('Please type some text first.');return;}
  setStatus('audio','🎵 Generating audio... please wait');
  const encoded=encodeURIComponent(text);
  const audioUrl='https://text.pollinations.ai/'+encoded+'?model=openai-audio&voice='+voice;
  showResult('audio','<audio controls autoplay><source src="'+audioUrl+'" type="audio/mpeg">Your browser does not support audio.</audio>');
  setStatus('audio','✅ Press play button to listen');
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
