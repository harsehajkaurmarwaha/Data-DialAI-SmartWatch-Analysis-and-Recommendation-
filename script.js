class ProductInsightBotUI {
    constructor() {
        this.conversation = document.getElementById('conversation');
        this.questionInput = document.getElementById('questionInput');
        this.initializeBot();
    }

    initializeBot() {
        setTimeout(() => {
            this.addSystemMessage("Analysis engine ready for queries");
        }, 1000);
    }

    addSystemMessage(content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message system-message';
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-cog"></i>
            </div>
            <div class="message-content">
                <div class="message-header">
                    <span class="sender">System</span>
                    <span class="timestamp">${this.getCurrentTime()}</span>
                </div>
                <div class="message-text">
                    <span style="color: var(--primary)">⚡ ${content}</span>
                </div>
            </div>
        `;
        this.conversation.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const avatarIcon = isUser ? 'fas fa-user' : 'fas fa-brain';
        const senderName = isUser ? 'You' : 'DataDial AI';
        
        // Convert simple text to formatted content
        const formattedContent = this.formatBotResponse(content);
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="${avatarIcon}"></i>
            </div>
            <div class="message-content">
                <div class="message-header">
                    <span class="sender">${senderName}</span>
                    <span class="timestamp">${this.getCurrentTime()}</span>
                </div>
                <div class="message-text">
                    ${formattedContent}
                </div>
                ${!isUser ? this.generateMessageActions(content) : ''}
            </div>
        `;
        
        this.conversation.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatBotResponse(content) {
        // Convert markdown-like formatting to HTML
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong style="color: var(--primary)">$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/```(.*?)```/gs, '<div class="code-block">$1</div>')
            .replace(/\n/g, '<br>')
            .replace(/💰/g, '<span style="color: gold">💰</span>')
            .replace(/⭐/g, '<span style="color: var(--warning)">⭐</span>')
            .replace(/📊/g, '<span style="color: var(--primary)">📊</span>')
            .replace(/🏷️/g, '<span style="color: var(--secondary)">🏷️</span>');
    }

    generateMessageActions(content) {
        if (content.includes('Titan') || content.includes('Casio') || content.includes('brand')) {
            return `
                <div class="message-actions">
                    <button class="action-btn" onclick="askQuestion('Compare Titan and Casio prices')">
                        <i class="fas fa-balance-scale"></i>
                        Compare Brands
                    </button>
                    <button class="action-btn" onclick="askQuestion('Show me all Titan watches')">
                        <i class="fas fa-list"></i>
                        View All
                    </button>
                </div>
            `;
        }
        
        if (content.includes('under') || content.includes('price')) {
            return `
                <div class="message-actions">
                    <button class="action-btn" onclick="askQuestion('Show me premium watches under 25000')">
                        <i class="fas fa-gem"></i>
                        Premium Range
                    </button>
                    <button class="action-btn" onclick="askQuestion('Budget watches under 5000')">
                        <i class="fas fa-wallet"></i>
                        Budget Picks
                    </button>
                </div>
            `;
        }
        
        return '';
    }

    showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-brain"></i>
            </div>
            <div class="message-content">
                <div class="message-header">
                    <span class="sender">DataDial AI</span>
                    <span class="timestamp">${this.getCurrentTime()}</span>
                </div>
                <div class="message-text">
                    <div class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        this.conversation.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTyping() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    async sendToBot(question) {
        this.showTyping();
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });
            
            const data = await response.json();
            
            this.hideTyping();
            
            if (data.response) {
                this.addMessage(data.response);
            } else {
                this.addMessage("❌ Error: Could not get response from server");
            }
        } catch (error) {
            this.hideTyping();
            this.addMessage("❌ Error: Could not connect to server. Make sure the Python backend is running.");
        }
    }

    scrollToBottom() {
        this.conversation.scrollTop = this.conversation.scrollHeight;
    }

    getCurrentTime() {
        return new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
    }
}

// Initialize the UI
const botUI = new ProductInsightBotUI();

// Global functions for HTML interactions
function askQuestion(question) {
    document.getElementById('questionInput').value = question;
    sendQuestion();
}

function sendQuestion() {
    const question = document.getElementById('questionInput').value.trim();
    if (question) {
        botUI.addMessage(question, true);
        botUI.sendToBot(question);
        document.getElementById('questionInput').value = '';
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendQuestion();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Add floating animation to stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add pulse effect to AI avatar periodically
    setInterval(() => {
        const avatar = document.querySelector('.ai-avatar');
        avatar.style.transform = 'scale(1.05)';
        setTimeout(() => {
            avatar.style.transform = 'scale(1)';
        }, 300);
    }, 5000);
});
