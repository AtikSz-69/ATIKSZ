# 🧠 AI Knowledge Assistant

A beautiful, feature-rich AI chatbot powered by Google Gemini that answers questions based on your custom knowledge base.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

## ✨ Features

### 🎨 Modern UI/UX

- Stunning gradient design with glassmorphism effects
- Smooth animations and hover effects
- Responsive layout
- Premium, professional appearance

### 📚 Knowledge Base Management

- Upload multiple `.txt` files
- Dynamic knowledge base updates
- File management (add/delete)
- Automatic source attribution

### 💬 Advanced Chat Features

- Persistent chat history
- Export conversations as JSON
- Clear chat functionality
- Message statistics

### 🚀 Production Ready

- Environment variable support
- Streamlit Cloud deployment ready
- Error handling
- Caching for performance

## 🛠️ Setup Instructions

### 1️⃣ Get Your API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy your API key

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure API Key

**Option A: Using .env file (Recommended for local development)**

1. Copy the example file:

```bash
cp .env.example .env
```

1. Edit `.env` and add your API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**Option B: Using Streamlit Secrets (For Streamlit Cloud deployment)**

1. Create `.streamlit/secrets.toml`:

```bash
mkdir .streamlit
```

1. Add your key to `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Adding Knowledge

1. **Upload Files**: Use the sidebar to upload `.txt` files
2. **Manage Files**: View and delete files in the "Manage Files" section
3. **Ask Questions**: Type your questions in the chat input

### Exporting Chats

1. Click **"Export Chat"** in the sidebar
2. Download the JSON file with your conversation history

### Clearing History

Click **"Clear Chat History"** to start a fresh conversation

## 🌐 Deployment to Streamlit Cloud

1. Push your code to GitHub (make sure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your `GEMINI_API_KEY` in the Secrets section:

   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

5. Deploy!

## 📁 Project Structure

```
ai-knowledge-bot/
├── app.py                  # Main application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── knowledge_base/        # Knowledge files directory
│   └── my_knowledge.txt   # Default knowledge file
└── .streamlit/            # Streamlit configuration
    └── secrets.toml       # API keys (not in git)
```

## 🎯 Customization

### Change Brand Name

Edit the `system_instruction` in `app.py`:

```python
system_instruction = f"""You are an intelligent AI assistant for [YOUR BRAND NAME].
...
```

### Adjust AI Behavior

Modify `generation_config` in `app.py`:

```python
generation_config = {
    "temperature": 0.7,    # 0.0 = focused, 1.0 = creative
    "top_p": 0.95,         # Diversity of responses
    "max_output_tokens": 2048,  # Response length
}
```

### Custom Styling

Edit the CSS in `st.markdown()` section of `app.py` to change colors, fonts, and layout.

## 🐛 Troubleshooting

### "API Key not configured" error

- Make sure you created `.env` file or `.streamlit/secrets.toml`
- Verify your API key is correct
- Restart the Streamlit app

### Import errors

- Run `pip install -r requirements.txt` again
- Make sure you're using Python 3.8 or higher

### Knowledge base not loading

- Check that `knowledge_base/` directory exists
- Verify `.txt` files are UTF-8 encoded
- Check file permissions

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 💡 Tips

- Start with a small knowledge base and expand gradually
- Use clear, well-structured text files for better AI responses
- Export important conversations regularly
- Monitor your API usage in Google AI Studio

---

**Built with ❤️ using Streamlit and Google Gemini**
