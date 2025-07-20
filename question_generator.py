import os
import random
import pyttsx3
import google.generativeai as genai

# Your API key is correctly placed here.
API_KEY = "AIzaSyAyXx6v3X2xpMr9jT7BflbNrX7ujoQRy9g" 

try:
    genai.configure(api_key=API_KEY)
    
    # ============================ THE FINAL FIX ===================================
    # We are using the latest, most compatible model to solve the API version error.
    model = genai.GenerativeModel('gemini-1.5-flash')
    # ==========================================================================

except Exception as e:
    model = None
    print(f"Error configuring Generative AI. The API will not work. Error: {e}")

# Initialize the text-to-speech engine
try:
    engine = pyttsx3.init()
except Exception as e:
    engine = None
    print(f"Could not initialize TTS engine: {e}")


def generate_questions_with_ai(resume_text, job_description, num_questions):
    """
    This function uses the power of a Generative AI to create truly insightful,
    context-aware questions based on the full resume and job description.
    """
    if not model:
        return ["Generative AI model not configured. Please check your API key."]
    
    prompt = f"""
    As an expert technical interviewer, your task is to generate {num_questions} challenging and insightful questions.
    You will be given a candidate's full resume and a job description. Your questions should:
    
    1.  **Be Specific:** Directly reference projects, technologies, or experiences mentioned in the resume.
    2.  **Be Contextual:** Connect the candidate's experience to the specific requirements of the job description.
    3.  **Probe Deeper:** Ask "why," "how," and "what if" questions. Force the candidate to explain their thought process, trade-offs, and reasoning. Do not ask simple definition questions.
    4.  **Format as a List:** Return only a Python list of strings, with each question as a separate string in the list. Do not add any other text or explanation.

    ---
    CANDIDATE'S RESUME:
    {resume_text}
    ---
    JOB DESCRIPTION:
    {job_description}
    ---
    
    Now, generate the {num_questions} questions as a Python list of strings.
    """
    
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.replace("```python", "").replace("```", "").strip()
        
        questions = eval(cleaned_response)
        if isinstance(questions, list):
            return questions
        else:
            return ["Failed to parse AI response. Please try again."]
            
    except Exception as e:
        return [f"An error occurred: {e}. Please check your API key and network connection."]


# --- The behavioral and situational questions can remain the same, as they are standard. ---
def generate_behavioral_questions(num_questions):
    pool = [
        "Tell me about a time you had a fundamental disagreement with a colleague. What was the core issue, and what was the process you followed to resolve it?",
        "Describe a high-stakes project you were responsible for that was falling behind schedule. What specific steps did you take to get it back on track?",
        "Tell me about your most significant professional failure. What did you learn from it, and how has that lesson tangibly influenced your work since?"
    ]
    return random.sample(pool, min(num_questions, len(pool)))

def generate_situational_questions(num_questions):
    pool = [
        "Imagine your team is assigned a project with what you believe is an unrealistic deadline. How would you approach this situation and manage expectations with leadership?",
        "Suppose you join a new team and discover their current workflow is highly inefficient. What steps would you take in the first 30 days to suggest and implement changes?",
        "If you were given a project with a very vague set of requirements, what steps would you take to ensure you deliver a successful outcome?"
    ]
    return random.sample(pool, min(num_questions, len(pool)))


def speak_question(text):
    if engine:
        try:
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error during TTS playback: {e}")
            return False
    return False