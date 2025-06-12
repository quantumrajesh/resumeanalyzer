from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from docx import Document
from typing import List, Dict
import io
import re
from ai_service import get_ai_analysis  # Import the new AI service

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Predefined skills list
RELEVANT_SKILLS = {
    'programming': ['python', 'javascript', 'java', 'c++', 'react', 'node.js', 'sql'],
    'tools': ['git', 'docker', 'kubernetes', 'aws', 'azure'],
    'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving']
}

def extract_text_from_pdf(file_content: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_content: bytes) -> str:
    doc = Document(io.BytesIO(file_content))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def identify_sections(text: str) -> Dict[str, str]:
    sections = {
        'summary': '',
        'education': '',
        'experience': '',
        'skills': '',
        'projects': ''
    }
    
    # Simple section detection based on common headers
    text_blocks = text.split('\n\n')
    current_section = None
    
    for block in text_blocks:
        block_lower = block.lower()
        if 'summary' in block_lower or 'objective' in block_lower:
            current_section = 'summary'
        elif 'education' in block_lower:
            current_section = 'education'
        elif 'experience' in block_lower or 'work' in block_lower:
            current_section = 'experience'
        elif 'skill' in block_lower:
            current_section = 'skills'
        elif 'project' in block_lower:
            current_section = 'projects'
        
        if current_section:
            sections[current_section] += block + '\n'
    
    return sections

def calculate_score(sections: Dict[str, str], text: str) -> tuple[int, Dict[str, str], List[str]]:
    score = 0
    section_feedback = {
        'summary': 'Missing',
        'skills': 'Missing',
        'education': 'Missing',
        'experience': 'Missing',
        'grammar': 'Not checked'  # Simplified without language tool
    }
    suggestions = []

    # Summary scoring
    if sections['summary'].strip():
        score += 10
        section_feedback['summary'] = 'Good'
    else:
        suggestions.append("Add a professional summary section")

    # Skills scoring
    found_skills = []
    for category in RELEVANT_SKILLS.values():
        for skill in category:
            if skill in sections['skills'].lower():
                found_skills.append(skill)
    
    skills_score = min(15, len(found_skills) * 3)
    score += skills_score
    if skills_score >= 12:
        section_feedback['skills'] = 'Good'
    elif skills_score >= 6:
        section_feedback['skills'] = 'Okay'
        suggestions.append("Add more relevant technical skills")
    else:
        section_feedback['skills'] = 'Poor'
        suggestions.append("Skills section needs significant improvement")

    # Experience scoring
    if sections['experience'].strip():
        score += 15
        section_feedback['experience'] = 'Good'
    else:
        suggestions.append("Add detailed work experience")
        section_feedback['experience'] = 'Missing'

    # Education scoring
    if sections['education'].strip():
        score += 10
        section_feedback['education'] = 'Good'
    else:
        suggestions.append("Add education details")
        section_feedback['education'] = 'Missing'

    # Format scoring (bullet points, proper spacing)
    bullet_points = len(re.findall(r'[•·-]\s', text))
    if bullet_points >= 5:
        score += 10
    else:
        suggestions.append("Use bullet points to better organize information")

    return score, section_feedback, suggestions

@app.get("/")
async def root():
    return {"message": "Resume Analyzer API is running"}

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(content)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(content)
        elif file.filename.endswith('.txt'):
            text = content.decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Get analysis from the AI service
        analysis_result = get_ai_analysis(text)
        
        return analysis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 