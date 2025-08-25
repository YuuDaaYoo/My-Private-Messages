// Load all messages from backend
async function loadMessages() {
    const messagesDiv = document.getElementById("messages");

    try {
        let response = await fetch("/messages");
        let data = await response.json();

        messagesDiv.innerHTML = "";

        data.forEach(msg => {
            // wrapper untuk 1 pesan
            let wrapper = document.createElement("div");
            wrapper.className = "message-wrapper";

            // bubble pesan
            let bubble = document.createElement("div");
            bubble.className = "message-bubble";
            bubble.textContent = msg.text;

            // timestamp
            let time = document.createElement("div");
            time.className = "message-time";
            time.textContent = msg.time;

            wrapper.appendChild(bubble);
            wrapper.appendChild(time);

            messagesDiv.appendChild(wrapper);
        });

        // auto-scroll
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

    } catch (error) {
        console.error("Failed to load messages:", error);
    }
}
