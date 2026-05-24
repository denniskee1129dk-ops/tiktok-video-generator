const form = document.getElementById("videoForm");
const generateBtn = document.getElementById("generateBtn");
const loading = document.getElementById("loading");
const emptyState = document.getElementById("emptyState");
const resultBox = document.getElementById("result");
const copyBtn = document.getElementById("copyBtn");
const downloadBtn = document.getElementById("downloadBtn");

let latestResultText = "";

function setLoading(isLoading) {
  if (isLoading) {
    generateBtn.disabled = true;
    loading.classList.remove("hidden");
    emptyState.classList.add("hidden");
    resultBox.classList.add("hidden");
  } else {
    generateBtn.disabled = false;
    loading.classList.add("hidden");
  }
}

function escapeHtml(str) {
  return (str || "").replace(/[&<>\"']/g, (m) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[m]));
}

function buildResultText(data) {
  const hashtagsText = (data.hashtags || []).join(" ");

  return `标题：${data.title}

模板：${data.template_type}

Hook：${data.hook}

脚本摘要：${data.script_summary}

分镜：
${(data.storyboard || []).map(s =>
`- ${s.time}｜${s.scene}
  画面：${s.visual}
  旁白：${s.voiceover}
  字幕：${s.subtitle}
  Prompt：${s.ai_prompt}
`
).join("\n")}

Caption：
${data.caption}

Hashtags：
${hashtagsText}

Tips：
${(data.tips || []).map(t => `- ${t}`).join("\n")}
`;
}

function renderResult(data) {
  latestResultText = buildResultText(data);

  const storyboardHtml = (data.storyboard || []).map(s => `
    <div class="storyboard-item">
      <div class="storyboard-title">${escapeHtml(s.time)}｜${escapeHtml(s.scene)}</div>
      <p><b>画面：</b>${escapeHtml(s.visual)}</p>
      <p><b>旁白：</b>${escapeHtml(s.voiceover)}</p>
      <p><b>字幕：</b>${escapeHtml(s.subtitle)}</p>
      <div class="prompt">${escapeHtml(s.ai_prompt)}</div>
    </div>
  `).join("");

  resultBox.innerHTML = `
    <div class="section">
      <h3>标题</h3>
      <p>${escapeHtml(data.title)}</p>
    </div>

    <div class="section">
      <h3>模板</h3>
      <p>${escapeHtml(data.template_type)}</p>
    </div>

    <div class="section">
      <h3>Hook</h3>
      <p>${escapeHtml(data.hook)}</p>
    </div>

    <div class="section">
      <h3>脚本摘要</h3>
      <p>${escapeHtml(data.script_summary)}</p>
    </div>

    <div class="section">
      <h3>分镜（画面 / 旁白 / 字幕 / Prompt）</h3>
      ${storyboardHtml}
    </div>

    <div class="section">
      <h3>Caption</h3>
      <p>${escapeHtml(data.caption)}</p>
    </div>

    <div class="section">
      <h3>Hashtags</h3>
      <div class="badges">
        ${(data.hashtags || []).map(h => `<span class="badge">${escapeHtml(h)}</span>`).join("")}
      </div>
    </div>

    <div class="section">
      <h3>Tips</h3>
      ${(data.tips || []).map(t => `<p>• ${escapeHtml(t)}</p>`).join("")}
    </div>
  `;

  emptyState.classList.add("hidden");
  resultBox.classList.remove("hidden");
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    product_name: document.getElementById("productName").value.trim(),
    target_audience: document.getElementById("targetAudience").value.trim(),
    selling_points: document.getElementById("sellingPoints").value.trim(),
    price: document.getElementById("price").value.trim(),
    style: document.getElementById("style").value,
    duration: Number(document.getElementById("duration").value),
    language: document.getElementById("language").value,
    template_type: document.getElementById("templateType").value
  };

  if (!payload.product_name || !payload.target_audience || !payload.selling_points || !payload.price) {
    alert("请先填写完整信息");
    return;
  }

  setLoading(true);

  try {
    const resp = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error("后端返回错误：" + text);
    }

    const data = await resp.json();
    renderResult(data);
  } catch (err) {
    alert(err.message || "生成失败");
  } finally {
    setLoading(false);
  }
});

copyBtn.addEventListener("click", async () => {
  if (!latestResultText) {
    alert("还没有生成结果");
    return;
  }
  try {
    await navigator.clipboard.writeText(latestResultText);
    alert("已复制到剪贴板");
  } catch (e) {
    alert("复制失败");
  }
});

downloadBtn.addEventListener("click", () => {
  if (!latestResultText) {
    alert("还没有生成结果");
    return;
  }

  const blob = new Blob([latestResultText], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "tiktok_video_script.txt";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
});
