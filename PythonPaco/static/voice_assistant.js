document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatArea = document.getElementById('chat-area');
    const speakerButton = document.getElementById('speaker-btn');
    let isSpeakerOn = true;

    function toggleSpeaker() {
        isSpeakerOn = !isSpeakerOn;
        speakerButton.textContent = isSpeakerOn ? '🔊' : '🔇';
    }

    let voices = [];
    let selectedVoice = null;

    function setVoice() {
        voices = speechSynthesis.getVoices();
        selectedVoice = voices.find(voice => voice.name === 'Jamie');
        console.log(selectedVoice); // Optionally, log the selected voice for confirmation
    }

    function speak(text) {
        if (isSpeakerOn && selectedVoice) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.voice = selectedVoice;
            speechSynthesis.speak(utterance);
        }
    }

    // Load voices and set the selected voice
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = setVoice;
    }

    function addChatBubble(text, className) {
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble ' + className;
        bubble.textContent = text;
        chatArea.appendChild(bubble);
        chatArea.scrollTop = chatArea.scrollHeight; // Scroll to the bottom
    }

    function sendMessage(message) {
        // Send the message to the OpenAI API
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if(data.message) {
                addChatBubble(data.message, 'incoming'); // Add AI response bubble
                speak(data.message); // Speak out the AI response
            } else {
                console.error('Error with the data:', data);
                // Handle the error properly in the UI
            }
        })
        .catch((error) => {
            console.error('Network error:', error);
            // Handle the error properly in the UI
        });
    }

    speakerButton.addEventListener('click', toggleSpeaker);
    sendButton.addEventListener('click', function() {
        const userInput = chatInput.value.trim();
        if (userInput) {
            addChatBubble(userInput, 'outgoing'); // Add user message bubble
            chatInput.value = ''; // Clear the input field
            sendMessage(userInput);
        }
    });

    // Optionally, send the message when the user presses "Enter"
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });
});
