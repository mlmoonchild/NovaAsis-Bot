let chats = JSON.parse(localStorage.getItem("chats")) || [];
let currentChat = 0;

// если чатов нет — создаём первый
if (chats.length === 0) {
  chats.push({ messages: [] });
  currentChat = 0;
  save();
}

renderChats();
renderMessages();

/* ---------------- CHAT CONTROL ---------------- */

function newChat() {
  chats.push({ messages: [] });
  currentChat = chats.length - 1;
  save();
  renderChats();
  renderMessages();
}

function switchChat(index) {
  currentChat = index;
  renderChats();
  renderMessages();
}

/* ---------------- SEND MESSAGE + AI ---------------- */

async function sendMessage() {
  const input = document.getElementById("input");
  const text = input.value.trim();
  if (!text) return;

  input.value = "";

  // user message
  chats[currentChat].messages.push({
    role: "user",
    text: text
  });

  renderMessages();
  save();

  // формируем формат для API
  const apiMessages = chats[currentChat].messages.map(m => ({
    role: m.role === "user" ? "user" : "assistant",
    content: m.text
  }));

  try {
    const res = await fetch("http://localhost:3710/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ messages: apiMessages })
    });

    const data = await res.json();

    const botText =
      data?.choices?.0?.message?.content ||
      "Ошибка ответа от ИИ";

    chats[currentChat].messages.push({
      role: "bot",
      text: botText
    });

  } catch (err) {
    chats[currentChat].messages.push({
      role: "bot",
      text: "Ошибка подключения к серверу"
    });
  }

  renderMessages();
  save();
}

/* ---------------- STORAGE ---------------- */

function save() {
  localStorage.setItem("chats", JSON.stringify(chats));
}

/* ---------------- RENDER MESSAGES ---------------- */

function renderMessages() {
  const messagesDiv = document.getElementById("messages");
  messagesDiv.innerHTML = "";

  chats[currentChat].messages.forEach(msg => {
    const div = document.createElement("div");
    div.classList.add("message");

    if (msg.role === "user") {
      div.classList.add("user");
    } else {
      div.classList.add("bot");
    }

    div.innerText = msg.text;
    messagesDiv.appendChild(div);
  });

  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

/* ---------------- RENDER CHATS ---------------- */

function renderChats() {
  const list = document.getElementById("chatList");
  list.innerHTML = "";

  chats.forEach((chat, index) => {
    const div = document.createElement("div");
    div.classList.add("chat-item");

    div.innerText = `Чат ${index + 1}`;

    if (index === currentChat) {
      div.style.background = "#2a2a2a";
    }

    div.onclick = () => switchChat(index);

    list.appendChild(div);
  });
  }
