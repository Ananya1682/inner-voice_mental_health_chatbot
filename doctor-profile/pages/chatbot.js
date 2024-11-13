import { useState, useEffect } from 'react';
import styles from './Chatbot.module.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isClient, setIsClient] = useState(false); // To check if rendering on client

  // Set isClient to true after the component mounts
  useEffect(() => {
    setIsClient(true);
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return; // Ignore empty messages

    // Add user message to chat
    setMessages([...messages, { sender: "user", text: input }]);

    try {
      const response = await fetch("http://localhost:5000/get-response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input })
      });
      const data = await response.json();
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", text: data.response }
      ]);
    } catch (error) {
      console.error("Error fetching chatbot response:", error);
    }

    setInput(""); // Clear input field after sending
  };

  if (!isClient) return null; // Return nothing on server render

  return (
    <div className={styles.chatbotContainer}>
      {/* Title and Subtitle */}
      <div className={styles.chatbotTitle}>Inner Voice</div>
      <div className={styles.chatbotSubtitle}>Your Mental Health Companion</div>
      
      {/* Chat Window */}
      <div className={styles.chatWindow}>
        {messages.map((msg, index) => (
          <div
            key={index}
            className={msg.sender === "user" ? styles.userMessage : styles.botMessage}
          >
            {msg.text}
          </div>
        ))}
      </div>
      
      {/* Input Container */}
      <div className={styles.inputContainer}>
        <input
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className={styles.inputField}
        />
        <button onClick={sendMessage} className={styles.sendButton}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
