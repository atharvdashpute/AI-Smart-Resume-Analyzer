from flask import Flask, request, jsonify
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

def extract_skills(text):
    with open("skills.txt", "r") as f:
        skills = f.read().splitlines()
    return [skill for skill in skills if skill in text.lower()]

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    resume_path = data.get("resume_path")
    job_desc = data.get("job_description")

    if not resume_path or not job_desc:
        return jsonify({"error": "Missing resume path or job description"}), 400

    if not os.path.exists(resume_path):
        return jsonify({"error": "Resume file not found"}), 400

    # Extract resume text
    resume_text = extract_text(resume_path)

    # Skill extraction
    matched_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)
    missing_skills = list(set(job_skills) - set(matched_skills))

    # Resume–Job matching
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_desc])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]

    return jsonify({
        "match_score": round(score * 100, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    })

if __name__ == "__main__":
    app.run(port=5000)
