import os
import json
import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from fuzzywuzzy import fuzz

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    try:
        text = ""
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def validate_text(text):
    if len(text.strip()) < 100:
        st.warning("The PDF appears to have very little text. It might be image-based.")
        return False
    return True

def split_text_into_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=100,
        length_function=len
    )
    return text_splitter.split_text(text)

def generate_questions(text_chunk):
    retry_count = 0
    while retry_count < 3:
        try:
            system_prompt = """Generate 2 questions in JSON format:
            {
                "questions": [
                    {"question": "clear question", "answer": "concise answer"}
                ]
            }
            Return ONLY valid JSON with properly escaped characters."""

            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Text content:\n{text_chunk}"}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            response = completion.choices[0].message.content
            result = json.loads(response)
            
            # Validate and clean questions
            valid_questions = []
            for q in result.get("questions", []):
                if isinstance(q, dict) and "question" in q and "answer" in q:
                    valid_questions.append({
                        "question": str(q["question"]).strip(),
                        "answer": str(q["answer"]).strip()
                    })
            
            return {"questions": valid_questions}
            
        except (json.JSONDecodeError, ValueError) as e:
            retry_count += 1
    
    return {"questions": []}

def main():
    st.title("AI Teacher App 🤖📚")
    
    # Initialize session state
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    
    with st.sidebar:
        st.header("Settings ⚙️")
        similarity_threshold = st.slider("Minimum correctness (%)", 50, 90, 70)
        questions_per_chunk = st.slider("Questions per section", 1, 5, 2)
    
    # PDF Upload
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    
    if uploaded_file and not st.session_state.questions:
        with st.spinner("Analyzing PDF content..."):
            text = extract_text_from_pdf(uploaded_file)
            
            if not validate_text(text):
                st.error("Could not extract sufficient text from PDF")
                return
                
            chunks = split_text_into_chunks(text)
            
            # Generate questions
            all_questions = []
            for chunk in chunks:
                result = generate_questions(chunk)
                if result.get("questions"):
                    all_questions.extend(result["questions"][:questions_per_chunk])
            
            if all_questions:
                st.session_state.questions = all_questions
                st.rerun()
            else:
                st.error("Failed to generate questions. Please try:")
                st.markdown("""
                - Text-based PDF (not scanned)
                - At least 2-3 paragraphs of content
                - Clear English text structure
                """)

    # Quiz interface
    if st.session_state.questions:
        total_questions = len(st.session_state.questions)
        current_q = st.session_state.current_question
        
        if current_q < total_questions:
            question = st.session_state.questions[current_q]
            
            st.header(f"Question {current_q + 1} of {total_questions}")
            st.markdown(f"#### {question['question']}")
            
            user_answer = st.text_input("Your answer:", key=f"answer_{current_q}")
            
            if user_answer:
                similarity = fuzz.token_sort_ratio(
                    user_answer.lower(),
                    question['answer'].lower()
                )
                
                st.progress(similarity/100)
                st.markdown(f"**Your score:** {similarity}%")
                st.markdown(f"**Correct answer:** {question['answer']}")
                
                if similarity >= similarity_threshold:
                    st.session_state.score += 1
                
                if st.button("Next Question →"):
                    st.session_state.current_question += 1
                    st.rerun()
        else:
            st.balloons()
            st.success(f"Quiz Complete! Final Score: {st.session_state.score}/{total_questions}")
            if st.button("🔄 Start New Quiz"):
                st.session_state.clear()
                st.rerun()

if __name__ == "__main__":
    main()