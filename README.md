# AI Teacher App 🤖📚

AI Teacher App is a Streamlit-based application that generates quiz questions from uploaded PDFs. The app uses AI to extract text from the document, generate questions, and assess user answers based on similarity scoring.

## Features ✨
- 📄 Upload a PDF file for analysis  
- 🔍 Automatically extract text from the PDF  
- 🤖 Generate multiple-choice or open-ended questions  
- ✅ Assess user responses using fuzzy matching for similarity scoring  
- ⚙️ Adjustable correctness threshold for scoring  
- 📊 Interactive quiz interface with progress tracking  

## Technologies Used 🛠️
- **Python** 🐍  
- **Streamlit** (for UI and interactivity)  
- **PyPDF2** (for PDF text extraction)  
- **Groq API** (for AI-based question generation)  
- **FuzzyWuzzy** (for answer similarity scoring)  
- **Langchain** (for text chunking)  

## Installation & Setup 🚀
### 1. Clone the repository:
```bash
git clone https://github.com/your-repo/ai-teacher-app.git
cd ai-teacher-app
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set up API keys:
- Obtain a Groq API key and set it as an environment variable:
```bash
export GROQ_API_KEY="your_api_key_here"
```

### 4. Run the application:
```bash
streamlit run app.py
```

## Usage 📖
1. 📤 Upload a **text-based** PDF file (scanned PDFs won't work well).  
2. 🔎 The app extracts and processes text from the file.  
3. 🧠 Questions are generated automatically from the text.  
4. ✍️ Answer the questions interactively and receive similarity-based scoring.  
5. 📈 Track your progress and final score!  

## Configuration ⚙️
- Adjust the **minimum correctness threshold** (50% - 90%) for answer evaluation.  
- Select the **number of questions per section** (1-5) in the sidebar settings.  

## Limitations ❗
- ❌ Does not support scanned/image-based PDFs.  
- 📜 Requires sufficient text in the uploaded PDF (at least 2-3 paragraphs).  
- 🤔 AI-generated questions may sometimes be generic or require improvement.  

## Future Enhancements 🚀
- ✅ Support for multiple-choice questions.  
- 📷 Integration with OCR for scanned PDFs.  
- 🎯 Enhanced AI models for better question generation.  

## License 📜
This project is licensed under the **MIT License**. Feel free to contribute and improve it!  

## Contact 📬
For any queries or contributions, feel free to reach out via [GitHub](https://https://github.com/Subhashbisnoi) or email at `rarsubhash1@gmail.com`.  
