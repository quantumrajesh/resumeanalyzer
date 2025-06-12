import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_ai_analysis(resume_text: str):
    """
    Analyzes the resume text using the Gemini model via OpenRouter and returns structured feedback.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")

    prompt = f"""
    You are an expert resume reviewer. Please analyze the following resume text and provide feedback.
    The resume text is as follows:
    ---
    {resume_text}
    ---
    Please return your analysis in a JSON object with the following structure:
    {{
      "score": <an integer score out of 100>,
      "suggestions": [
        "<a short, actionable suggestion for improvement>",
        "<another suggestion>"
      ],
      "sectionFeedback": {{
        "summary": "<'Good', 'Okay', or 'Missing'>",
        "skills": "<'Good', 'Okay', or 'Poor'>",
        "experience": "<'Good', 'Okay', or 'Missing'>",
        "education": "<'Good', 'Okay', or 'Missing'>",
        "grammar": "<'Good', 'Needs Improvement', or 'Poor'>"
      }}
    }}
    Your analysis should be critical and constructive. The score should reflect the overall quality of the resume.
    """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-flash-1.5",
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
            })
        )

        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        # The response is already a JSON object if the API call is successful
        analysis_json = response.json()
        
        # The actual content we need is nested inside the response
        return json.loads(analysis_json['choices'][0]['message']['content'])

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request to OpenRouter: {e}")
        # Fallback error structure
        return {
            "score": 0,
            "suggestions": ["AI analysis failed due to a network error. Please try again later."],
            "sectionFeedback": {
                "summary": "Error", "skills": "Error", "experience": "Error",
                "education": "Error", "grammar": "Error",
            },
        }
    except (KeyError, json.JSONDecodeError) as e:
        print(f"An error occurred while parsing the AI response: {e}")
        # Fallback error structure
        return {
            "score": 0,
            "suggestions": ["AI analysis failed due to an invalid response from the server."],
            "sectionFeedback": {
                "summary": "Error", "skills": "Error", "experience": "Error",
                "education": "Error", "grammar": "Error",
            },
        } 