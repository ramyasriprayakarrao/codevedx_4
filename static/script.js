const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const messages = document.getElementById("messages");
const sendButton = document.getElementById("send-button");

function addMessage(text, sender) {
  const row = document.createElement("div");
  row.className = `message ${sender}`;
  if (sender === "bot") {
    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = "IT";
    row.appendChild(avatar);
  }
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  row.appendChild(bubble);
  messages.appendChild(row);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(message) {
  const clean = message.trim();
  if (!clean) return;
  addMessage(clean, "user");
  input.value = "";
  sendButton.disabled = true;
  sendButton.textContent = "Sending...";
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: clean})
    });
    const data = await response.json();
    addMessage(data.answer || "Sorry, I could not process that request.", "bot");
  } catch (error) {
    addMessage("I could not connect to the chatbot server. Please check that main.py is running.", "bot");
  } finally {
    sendButton.disabled = false;
    sendButton.textContent = "Send";
    input.focus();
  }
}

form.addEventListener("submit", event => {
  event.preventDefault();
  sendMessage(input.value);
});

document.querySelectorAll(".suggestions button").forEach(button => {
  button.addEventListener("click", () => sendMessage(button.dataset.question));
});
