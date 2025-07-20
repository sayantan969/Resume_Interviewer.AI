import re

def calculate_job_fit(resume_keywords, jd_keywords):
    """
    Calculates a job fit score and crucially identifies common and MISSING keywords.
    """
    if not jd_keywords:
        return 0, [], []
    
    # Use sets for efficient comparison
    jd_keywords_lower = {k.lower() for k in jd_keywords}
    resume_keywords_lower = {k.lower() for k in resume_keywords}
    
    common_keywords = list(resume_keywords_lower & jd_keywords_lower)
    missing_keywords = list(jd_keywords_lower - resume_keywords_lower)
    
    fit_score = (len(common_keywords) / len(jd_keywords_lower)) * 100 if jd_keywords_lower else 0
    return min(fit_score, 100), common_keywords, missing_keywords

def evaluate_response(answer, relevant_keywords):
    """
    Evaluates a single answer based on keyword matching, clarity, and checks for STAR method structure.
    """
    if not answer.strip():
        return 0, "No answer provided. In a real interview, it's crucial to articulate your thoughts for every question. Try to explain your thinking process even if you don't know the perfect answer."

    feedback_points = []
    
    # 1. Word Count and Conciseness Feedback
    word_count = len(answer.split())
    if word_count < 25:
        feedback_points.append("Your answer is quite brief. Aim to provide more detail and context. For behavioral questions, structuring your answer with the STAR method can help add necessary depth.")
    elif word_count > 250:
        feedback_points.append("Your answer is very detailed. This is good, but practice being more concise. Focus on delivering the most impactful information first.")
    
    # 2. STAR Method Check (for behavioral/situational questions)
    # This is a simple check looking for keywords related to the STAR method.
    situation_found = bool(re.search(r'\bsituation\b|\bscenario\b|\bcontext\b|\bproject\b', answer, re.IGNORECASE))
    task_found = bool(re.search(r'\btask\b|\bgoal\b|\bobjective\b|\bhad to\b', answer, re.IGNORECASE))
    action_found = bool(re.search(r'\baction\b|\bi did\b|\bi implemented\b|\bi developed\b|\bwe decided\b', answer, re.IGNORECASE))
    result_found = bool(re.search(r'\bresult\b|\boutcome\b|\bachieved\b|\bimpact\b|\bled to\b', answer, re.IGNORECASE))
    
    star_score = sum([situation_found, task_found, action_found, result_found])
    
    if star_score >= 3:
        feedback_points.append("Excellent job structuring your answer. It seems to follow the STAR method, making it clear and impactful.")
    else:
        feedback_points.append("To make your behavioral answers stronger, try to structure them using the STAR method: Clearly describe the **S**ituation, the **T**ask you had to complete, the **A**ction you took, and the **R**esult of your actions.")

    # 3. Keyword Matching
    score = 0
    found_keywords = []
    if relevant_keywords:
        for keyword in relevant_keywords:
            if keyword.lower() in answer.lower():
                score += 1
                found_keywords.append(keyword)

    relevance_score = (score / len(relevant_keywords)) * 100 if relevant_keywords else 100
    
    if found_keywords:
        feedback_points.append(f"Great! You included these relevant keywords from the job description: **{', '.join(found_keywords)}**.")
    else:
        feedback_points.append("Try to naturally include more keywords from the job description in your answers to clearly show your alignment with the role.")

    # Combine all feedback points into one coherent message
    final_feedback = "\n\n- ".join(feedback_points)
    
    return min(relevance_score, 100), "- " + final_feedback