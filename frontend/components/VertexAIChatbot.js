"use client";
import React, { useState } from 'react';
export default function VertexAIChatbot() {
    const [chat, setChat] = useState([{sender: 'Chatbot', message: "How can I help you today?"}]);
    const [userInput, setUserInput] = useState('');

    const sendMessage = () => {
        if (userInput.trim() === '') return;

        // Append user message to the chat
        setChat([...chat, { sender: 'You', message: userInput }]);
        
        // Simulate API request (replace this with your actual API endpoint)
        simulateAPIRequest(userInput);

        // Clear the input field
        setUserInput('');
    };

    const simulateAPIRequest = (userMessage) => {
        // Replace this with your actual API endpoint
        // Simulate API response (replace this with your actual API request logic)
        fetch("http://127.0.0.1:8000/vertexai", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                // 'Content-Type': 'application/x-www-form-urlencoded',
              },
            body: JSON.stringify(
                {
                    "message":userMessage, 
                }
            )
        }).then((response) => response.json()) // Parse the response as JSON
        .then((data) => {
            setChat(prevChat => [...prevChat, { sender: 'Chatbot', message: data }]);
        }
        ).catch(error => console.log(error))      
        // Simulate delay (replace this with actual API request)
      };

    return (
        <div className="App font-sans bg-gray-100 flex items-center w-full justify-center min-h-screen">
          <div className="w-full max-w-md bg-white rounded shadow-md p-6">
            <p className='text-black mx-auto font-semibold text-2xl py-2'>Vertex AI</p>
            <div className="h-64 overflow-y-auto mb-4">
              {chat.map((message, index) => (
                <div key={index} className="mb-2 text-black">
                  <strong>{message.sender}:</strong> {message.message}
                </div>
              ))}
            </div>
            <div className="flex">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 py-2 px-4 rounded-l border border-r-0 text-black"
              />
              <button onClick={sendMessage} className="py-2 px-4 bg-blue-500 text-white rounded-r">
                Send
              </button>
            </div>
          </div>
        </div>
      );
}
